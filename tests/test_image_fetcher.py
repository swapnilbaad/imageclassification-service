import io
import pytest
import requests
from PIL import Image
from src.image_fetcher import fetch_image

def fake_requests_get(url, timeout):
    # A fake response class
    class FakeResponse:
        def __init__(self, content):
            self.content = content
        def raise_for_status(self):
            pass  # Assume the request is always successful for this fake.
    # Create a dummy 10x10 red image.
    image = Image.new("RGB", (10, 10), color="red")
    buf = io.BytesIO()
    image.save(buf, format="JPEG")
    return FakeResponse(buf.getvalue())

def test_fetch_image(monkeypatch):
    # Replace requests.get with our fake function
    monkeypatch.setattr(requests, "get", fake_requests_get)
    url = "http://fakeurl.com/fake.jpg"
    image = fetch_image(url)
    assert image is not None
    assert image.size == (10, 10)
