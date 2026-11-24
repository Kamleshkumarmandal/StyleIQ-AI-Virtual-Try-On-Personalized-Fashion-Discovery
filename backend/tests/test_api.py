import io
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from app import main


def image_bytes(color=(120, 80, 60)) -> bytes:
    buffer = io.BytesIO()
    Image.new("RGB", (320, 480), color).save(buffer, format="JPEG")
    return buffer.getvalue()


client = TestClient(main.app)


def test_health_has_model_identity():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model"] == "FASHN VTON v1.5"


def test_requires_consent():
    response = client.post(
        "/v1/try-on",
        data={"category": "tops", "consent": "false"},
        files={
            "person_image": ("person.jpg", image_bytes(), "image/jpeg"),
            "garment_image": ("garment.jpg", image_bytes(), "image/jpeg"),
        },
    )
    assert response.status_code == 400


def test_rejects_unsupported_category():
    response = client.post(
        "/v1/try-on",
        data={"category": "shoes", "consent": "true"},
        files={
            "person_image": ("person.jpg", image_bytes(), "image/jpeg"),
            "garment_image": ("garment.jpg", image_bytes(), "image/jpeg"),
        },
    )
    assert response.status_code == 422


def test_rejects_non_image_upload():
    response = client.post(
        "/v1/try-on",
        data={"category": "tops", "consent": "true"},
        files={
            "person_image": ("person.txt", b"not an image", "image/jpeg"),
            "garment_image": ("garment.jpg", image_bytes(), "image/jpeg"),
        },
    )
    assert response.status_code == 422


def test_unknown_job_returns_404():
    response = client.get("/v1/try-on/not-a-real-job")
    assert response.status_code == 404
