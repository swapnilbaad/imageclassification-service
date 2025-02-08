import requests
from PIL import Image
import io

def fetch_image(url):
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return Image.open(io.BytesIO(response.content)).convert("RGB")
    except Exception as e:
        print(f"Error fetching image from {url}: {e}")
        return None
