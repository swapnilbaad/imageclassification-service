import aiohttp
import io
import logging
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

async def async_fetch_image(url: str):
    """
    Asynchronously fetch an image from a URL and return a PIL Image.
    """
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as response:
                logger.info(f"Fetching image from {url} | Status: {response.status}")

                if response.status != 200:
                    logger.error(f"HTTP Error {response.status} when fetching {url}")
                    return None

                content = await response.read()
                logger.info(f"Fetched {len(content)} bytes from {url}")

                if not content:
                    logger.error(f"Empty response from {url}")
                    return None

                image = Image.open(io.BytesIO(content)).convert("RGB")
                logger.info(f"Successfully processed image from {url}")
                return image
    except Exception as e:
        logger.error(f"Error fetching image from {url}: {e}")
        return None