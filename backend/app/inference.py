"""Lazy adapter for the official FASHN VTON v1.5 inference package."""
from __future__ import annotations

import threading
from pathlib import Path
from typing import Any

from PIL import Image


class ModelNotReadyError(RuntimeError):
    pass


class FashnVtonEngine:
    """Loads one pipeline per worker process and serializes access to its GPU."""

    def __init__(self, weights_dir: str, device: str = "auto") -> None:
        self.weights_dir = Path(weights_dir)
        self.device = device
        self._pipeline: Any | None = None
        self._lock = threading.Lock()

    def runtime_info(self) -> dict[str, Any]:
        try:
            import torch
            cuda_available = torch.cuda.is_available()
            gpu_name = torch.cuda.get_device_name(0) if cuda_available else None
            torch_version = torch.__version__
        except Exception as exc:
            return {"torch_available": False, "error": str(exc), "cuda_available": False}
        return {
            "torch_available": True,
            "torch_version": torch_version,
            "cuda_available": cuda_available,
            "gpu_name": gpu_name,
            "weights_present": (self.weights_dir / "model.safetensors").is_file(),
        }

    def _load(self) -> Any:
        if self._pipeline is not None:
            return self._pipeline
        info = self.runtime_info()
        if not info.get("torch_available"):
            raise ModelNotReadyError("PyTorch is not installed or could not be imported.")
        if not info.get("weights_present"):
            raise ModelNotReadyError(
                f"Model weights not found in {self.weights_dir}. Run the official download script."
            )
        try:
            from fashn_vton import TryOnPipeline
            # Official package automatically selects CUDA when available.
            self._pipeline = TryOnPipeline(weights_dir=str(self.weights_dir))
        except Exception as exc:
            raise ModelNotReadyError(f"Could not initialize FASHN VTON: {exc}") from exc
        return self._pipeline

    def generate(self, person_path: Path, garment_path: Path, category: str) -> Image.Image:
        with self._lock:
            pipeline = self._load()
            person = Image.open(person_path).convert("RGB")
            garment = Image.open(garment_path).convert("RGB")
            try:
                result = pipeline(
                    person_image=person,
                    garment_image=garment,
                    category=category,
                )
                if not result.images:
                    raise RuntimeError("The model returned no output images.")
                output = result.images[0].convert("RGB")
                output.load()
                return output
            finally:
                person.close()
                garment.close()
