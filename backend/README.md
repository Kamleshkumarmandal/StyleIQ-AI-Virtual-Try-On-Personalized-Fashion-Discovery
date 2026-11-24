# StyleIQ inference backend

FastAPI adapter for the official [FASHN VTON v1.5](https://github.com/fashn-AI/fashn-vton-1.5) local inference package.

> **Status:** First backend integration slice. API/job lifecycle and validation are implemented; real inference requires model weights and a compatible runtime/GPU and has not been verified in this repository environment. This generates a visual preview, not a physical-fit prediction.

## Model and licence review

The official FASHN VTON v1.5 repository identifies its project code/model release as Apache-2.0. It also lists third-party components, including FASHN Human Parser with a separate licence reference. Review the current licences and notices for every dependency and downloaded weight before commercial deployment; do not assume the top-level licence automatically covers all third-party assets.

Official repository instructions state:
- Python >=3.10
- Install the model package with `pip install -e .`
- Download about 2 GB of weights using `python scripts/download_weights.py --weights-dir ./weights`
- Human-parser weights (~244 MB) download on first use
- GPU acceleration uses `onnxruntime-gpu`; ensure CUDA is configured
- Published guidance reports ~8 GB VRAM and ~5 seconds on an H100; actual latency varies by GPU, inputs, and runtime
- Categories: `tops`, `bottoms`, `one-pieces`

## 1. Install the model

Use a Linux machine with an NVIDIA GPU and a CUDA-compatible PyTorch/ONNX Runtime setup for practical inference.

```bash
git clone https://github.com/fashn-AI/fashn-vton-1.5.git
cd fashn-vton-1.5
python -m venv .venv
source .venv/bin/activate
pip install -e .
python scripts/download_weights.py --weights-dir ./weights
```

Copy the downloaded `weights/` directory into StyleIQ's `backend/weights/` (or set `STYLEIQ_WEIGHTS_DIR` to its absolute path). Keep weights out of Git.

## 2. Install and run StyleIQ API

From the StyleIQ repository root:

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Set STYLEIQ_WEIGHTS_DIR to the model weights directory.
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/docs` for interactive API docs and `http://localhost:8000/health` for runtime readiness.

## 3. API

### Create job

`POST /v1/try-on` multipart form fields:
- `person_image`: JPEG/PNG/WEBP, at least 256×256
- `garment_image`: JPEG/PNG/WEBP, at least 256×256
- `category`: `tops`, `bottoms`, or `one-pieces`
- `consent`: `true` (explicit user confirmation)

Returns HTTP 202 with `job_id`, `status`, and expiry.

### Poll status

`GET /v1/try-on/{job_id}`

Statuses: `queued`, `processing`, `completed`, `failed`.

### Retrieve result

`GET /v1/try-on/{job_id}/result`

Returns a private, no-store JPEG after completion.

### Delete job and assets

`DELETE /v1/try-on/{job_id}`

## 4. Privacy and operational limitations

- Uploaded images are held in a per-job temporary directory and removed after inference; generated output is temporary and expires after `STYLEIQ_JOB_TTL_SECONDS` (default 15 minutes).
- The result endpoint is intentionally not a public URL. Add authentication/authorization before exposing this API to users.
- The initial job registry is in process memory and the executor is single-worker. It is suitable only for a single-process prototype. Use Redis/Celery or another durable queue, per-user ownership checks, and private object storage before production/multi-replica deployment.
- Configure reverse-proxy request-body limits and rate limiting. The application validates each image after receipt; a production edge should also cap total multipart request size.
- Use HTTPS, authentication, audit events without image data, and explicit retention/deletion policies in production.
- The current API stores the generated result temporarily until expiry or explicit deletion. A periodic cleanup task is required in a long-running production service; expiry is enforced on API access.
- Do not log image bytes, photo URLs, or body measurements. Do not use uploaded photos for model training absent separate opt-in.
- A successful visual result does not establish garment size or physical fit. Fit guidance remains a separate service using confirmed body and garment measurements.

## 5. Tests

```bash
cd backend
pytest -q
```

The tests exercise API validation and job lifecycle with the model adapter replaced by a deterministic test double. They do not prove GPU inference quality.
