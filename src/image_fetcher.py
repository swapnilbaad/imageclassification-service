# src/image_fetcher.py
import aiohttp
import io
from PIL import Image

async def async_fetch_image(url: str):
    """
    Asynchronously fetch an image from a URL and return a PIL Image.
    """
    try:
        async with aiohttp.ClientSession() as session:
            # Add a custom header to mimic a real browser (optional)
            headers = {'User-Agent': 'Mozilla/5.0'}
            async with session.get(url, headers=headers, timeout=10) as response:
                # Log status and content-type for debugging
                print(f"[DEBUG] URL: {url} | Status: {response.status}")
                content_type = response.headers.get('Content-Type', '')
                print(f"[DEBUG] Content-Type: {content_type}")
                
                # Raise an error for non-200 responses
                response.raise_for_status()
                content = await response.read()
                
                if not content:
                    raise ValueError("No content returned from URL.")

                # Optionally, print the size of the content
                print(f"[DEBUG] Content length: {len(content)} bytes")
                
                # Try to open the image
                image = Image.open(io.BytesIO(content)).convert("RGB")
                return image
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        return None
