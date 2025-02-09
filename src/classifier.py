import os
import json
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import asyncio
import logging
from image_fetcher import async_fetch_image

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

# Load ImageNet class index mapping
imagenet_json = os.path.join(os.path.dirname(__file__), 'imagenet_class_index.json')
with open(imagenet_json) as f:
    class_idx = json.load(f)

# Set up the device and load a pre-trained model
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.mobilenet_v2(pretrained=True).to(device)
model.eval()

# Define image transformation pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225]),
])

def classify_image_sync(image: Image.Image) -> str:
    """
    Synchronously classify an image using the pre-trained model.
    """
    image = transform(image).unsqueeze(0).to(device)
    with torch.no_grad():
        outputs = model(image)
        _, predicted = outputs.max(1)
    pred_class = predicted.item()
    label = class_idx[str(pred_class)][1]
    logger.info(f"Image classified as: {label}")
    return label

async def classify_image_async(url: str, pub_socket, loop: asyncio.AbstractEventLoop):
    """
    Asynchronously fetch the image, run the classification, and publish the result.
    """
    logger.info(f"Processing image from {url}")
    image = await async_fetch_image(url)
    if image is None:
        result = {"url": url, "error": "Failed to fetch image"}
        logger.error(f"Failed to process {url}")
    else:
        label = await loop.run_in_executor(None, classify_image_sync, image)
        result = {"url": url, "class": label}
    await pub_socket.send_json(result)