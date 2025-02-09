import pytest
import aiohttp
from src.image_fetcher import async_fetch_image
from PIL import Image
import io
from unittest.mock import AsyncMock, MagicMock

@pytest.mark.asyncio
async def test_fetch_image(monkeypatch):
    """Test async_fetch_image by correctly mocking aiohttp.ClientSession.get()."""

    class MockResponse:
        """Mock response object for aiohttp."""
        def __init__(self):
            self.status = 200
            self.headers = {'Content-Type': 'image/jpeg'}

        async def read(self):
            """Return binary image data."""
            img = Image.new("RGB", (10, 10), color="red")
            buf = io.BytesIO()
            img.save(buf, format="JPEG")
            return buf.getvalue()

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    class MockSession:
        """Mock aiohttp ClientSession to always return MockResponse."""
        def __init__(self):
            self.get = AsyncMock(return_value=MockResponse())

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            pass

    # Patch `aiohttp.ClientSession` to return our `MockSession`
    monkeypatch.setattr(aiohttp, "ClientSession", lambda: MockSession())

    # Now run the actual function with the mock
    image = await async_fetch_image("http://fakeurl.com/image.jpg")
    
    # Assertions
    assert image is not None, "Image fetching failed, returned None"
    assert isinstance(image, Image.Image), "Returned object is not a PIL Image"
    assert image.size == (10, 10), f"Image size incorrect, got {image.size}"
