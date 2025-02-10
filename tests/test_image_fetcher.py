import pytest
import aiohttp
from src.image_fetcher import async_fetch_image
from PIL import Image
import io
from aioresponses import aioresponses
import asyncio


@pytest.mark.asyncio
async def test_async_fetch_image_success():
    url = "http://example.com/image.jpg"
    
    # Create a simple in-memory image
    img = Image.new("RGB", (100, 100), color=(255, 0, 0))
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_bytes = img_byte_arr.getvalue()
    
    with aioresponses() as mock_response:
        mock_response.get(url, status=200, body=img_bytes)
        
        result = await async_fetch_image(url)
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == (100, 100)

@pytest.mark.asyncio
async def test_async_fetch_image_http_error():
    url = "http://example.com/bad.jpg"
    with aioresponses() as mock_response:
        mock_response.get(url, status=404)
        
        result = await async_fetch_image(url)
        
        assert result is None

@pytest.mark.asyncio
async def test_async_fetch_image_timeout():
    url = "http://example.com/timeout.jpg"
    with aioresponses() as mock_response:
        mock_response.get(url, exception=asyncio.TimeoutError)
        
        result = await async_fetch_image(url)
        
        assert result is None

@pytest.mark.asyncio
async def test_async_fetch_image_empty_response():
    url = "http://example.com/empty.jpg"
    with aioresponses() as mock_response:
        mock_response.get(url, status=200, body=b"")
        
        result = await async_fetch_image(url)
        
        assert result is None
