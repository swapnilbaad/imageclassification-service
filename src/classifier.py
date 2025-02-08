# src/classifier.py
import os
import time
import json
import torch
import torchvision.transforms as transforms
from PIL import Image
from torchvision import models
import io
from image_fetcher import fetch_image

# Load ImageNet class index mapping from JSON file.
# Ensure that 'imagenet_class_index.json' is placed in the same directory as this file.
imagenet_json = os.path.join(os.path.dirname(__file__), 'imagenet_class_index.json')
with open(imagenet_json) as f:
    class_idx = json.load(f)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = models.mobilenet_v2(pretrained=True).to(device)
model.eval()

# Image transformation pipeline
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

def classify_image(url, pub_socket):
    try:
        image = fetch_image(url)
        if image is None:
            raise ValueError("Failed to fetch image")
        
        # Artificial delay to simulate long processing (e.g., 5 seconds)
        time.sleep(5)
        image = transform(image).unsqueeze(0).to(device)
        
        with torch.no_grad():
            outputs = model(image)
            _, predicted = outputs.max(1)
        
        pred_class = predicted.item()
        # Retrieve the human-readable label from the mapping.
        label = class_idx[str(pred_class)][1]
        result = {"url": url, "class": label}
        pub_socket.send_json(result)  # Publish result
    except Exception as e:
        pub_socket.send_json({"url": url, "error": str(e)})
