from __future__ import annotations

import asyncio
import io
import shutil
import tempfile
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from threading import Lock
from typing import Literal

from fastapi import BackgroundTasks, FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from PIL import Image, UnidentifiedImageError
from pydantic import BaseModel

from .config import get_settings
from .inference import FashnVtonEngine, ModelNotReadyError

settings = get_settings()
app = FastAPI(title="StyleIQ Virtual Try-On API", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["GET", "POST", "DELETE"],
    allow_headers=["Content-Type"],
)

engine = FashnVtonEngine(settings.weights_dir, settings.device)
executor = ThreadPoolExecutor(max_workers=1, thread_name_prefix="vton")
jobs: dict[str, dict] = {}
jobs_lock = Lock()
CATEGORIES = {"tops", "bottoms", "one-pieces"}
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


class JobStatus(BaseModel):
    job_id: str
    status: Literal["queued", "processing", "completed", "failed", "expired"]
    created_at: float
    expires_at: float
    error: str | None = None


def _purge_expired() -> None:
    now = time.time()
    with jobs_lock:
        expired = [key for key, job in jobs.items() if job["expires_at"] <= now]
        for key in expired:
            shutil.rmtree(job["workdir"], ignore_errors=True)
            jobs.pop(key, None)


async def _read_valid_image(upload: UploadFile, label: str) -> bytes:
    if upload.content_type not in {"image/jpeg", "image/png", "image/webp"}:
        raise HTTPException(415, f"{label} must be JPEG, PNG, or WEBP.")
    limit = settings.max_upload_mb * 1024 * 1024
    data = await upload.read(limit + 1)
    if not data or len(data) > limit:
        raise HTTPException(413, f"{label} is empty or exceeds {settings.max_upload_mb} MB.")
    try:
        with Image.open(io.BytesIO(data)) as image:
            image.verify()
        with Image.open(io.BytesIO(data)) as image:
            if image.format not in ALLOWED_FORMATS:
                raise HTTPException(415, f"{label} has an unsupported image format.")
            width, height = image.size
            if width < 256 or height < 256:
                raise HTTPException(422, f"{label} must be at least 256 × 256 pixels.")
            if width * height > settings.max_image_pixels:
                raise HTTPException(413, f"{label} has too many pixels.")
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError):
        raise HTTPException(422, f"{label} is not a valid supported image.")
    return data


def _run_job(job_id: str, person_path: Path, garment_path: Path, category: str) -> None:
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            return
        job["status"] = "processing"
    try:
        result = engine.generate(person_path, garment_path, category)
        output_path = Path(jobs[job_id]["workdir"]) / "result.jpg"
        result.save(output_path, format="JPEG", quality=92, optimize=True)
        result.close()
        with jobs_lock:
            if job_id in jobs:
                jobs[job_id]["status"] = "completed"
                jobs[job_id]["result_path"] = str(output_path)
    except ModelNotReadyError as exc:
        with jobs_lock:
            if job_id in jobs:
                jobs[job_id]["status"] = "failed"
                jobs[job_id]["error"] = str(exc)
    except Exception:
        # Do not return stack traces, file paths, or image data to clients.
        with jobs_lock:
            if job_id in jobs:
                jobs[job_id]["status"] = "failed"
                jobs[job_id]["error"] = "Try-on generation failed. Please retry with different images."
    finally:
        person_path.unlink(missing_ok=True)
        garment_path.unlink(missing_ok=True)


@app.get("/health")
def health() -> dict:
    _purge_expired()
    runtime = engine.runtime_info()
    ready = runtime.get("torch_available") and runtime.get("weights_present")
    if settings.require_cuda:
        ready = ready and runtime.get("cuda_available")
    return {
        "status": "ready" if ready else "not_ready",
        "model": "FASHN VTON v1.5",
        "runtime": runtime,
        "cuda_required": settings.require_cuda,
    }


@app.post("/v1/try-on", response_model=JobStatus, status_code=202)
async def create_try_on(
    background_tasks: BackgroundTasks,
    person_image: UploadFile = File(...),
    garment_image: UploadFile = File(...),
    category: str = Form(...),
    consent: bool = Form(...),
) -> JobStatus:
    _purge_expired()
    if consent is not True:
        raise HTTPException(400, "Explicit consent is required to process the person image.")
    category = category.strip().lower()
    if category not in CATEGORIES:
        raise HTTPException(422, "category must be tops, bottoms, or one-pieces.")

    person_bytes, garment_bytes = await asyncio.gather(
        _read_valid_image(person_image, "Person image"),
        _read_valid_image(garment_image, "Garment image"),
    )
    job_id = str(uuid.uuid4())
    workdir = Path(tempfile.mkdtemp(prefix="styleiq-"))
    person_path = workdir / "person-input"
    garment_path = workdir / "garment-input"
    person_path.write_bytes(person_bytes)
    garment_path.write_bytes(garment_bytes)
    now = time.time()
    job = {
        "status": "queued",
        "created_at": now,
        "expires_at": now + settings.job_ttl_seconds,
        "workdir": str(workdir),
        "result_path": None,
        "error": None,
    }
    with jobs_lock:
        jobs[job_id] = job
    background_tasks.add_task(executor.submit, _run_job, job_id, person_path, garment_path, category)
    return JobStatus(
        job_id=job_id,
        status="queued",
        created_at=now,
        expires_at=job["expires_at"],
    )


@app.get("/v1/try-on/{job_id}", response_model=JobStatus)
def get_try_on_status(job_id: str) -> JobStatus:
    _purge_expired()
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            raise HTTPException(404, "Try-on job not found or expired.")
        return JobStatus(
            job_id=job_id,
            status=job["status"],
            created_at=job["created_at"],
            expires_at=job["expires_at"],
            error=job["error"],
        )


@app.get("/v1/try-on/{job_id}/result")
def get_try_on_result(job_id: str) -> Response:
    _purge_expired()
    with jobs_lock:
        job = jobs.get(job_id)
        if not job:
            raise HTTPException(404, "Try-on job not found or expired.")
        if job["status"] != "completed" or not job["result_path"]:
            raise HTTPException(409, "Try-on result is not ready.")
        result_path = Path(job["result_path"])
        if not result_path.is_file():
            raise HTTPException(410, "Try-on result is no longer available.")
        image_bytes = result_path.read_bytes()
    return Response(
        content=image_bytes,
        media_type="image/jpeg",
        headers={"Cache-Control": "private, no-store", "X-Content-Type-Options": "nosniff"},
    )


@app.delete("/v1/try-on/{job_id}", status_code=204)
def delete_try_on_job(job_id: str) -> Response:
    with jobs_lock:
        job = jobs.pop(job_id, None)
    if job:
        shutil.rmtree(job["workdir"], ignore_errors=True)
    return Response(status_code=204)
