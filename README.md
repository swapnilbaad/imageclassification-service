# Image Classification Service

A toy service that accepts a list of image URLs via a ZeroMQ REQ/REP socket, fetches the images, runs a CNN-based image classification on them, and publishes the results over a ZeroMQ PUB/SUB socket. The service is designed to remain responsive to new requests even while processing previous ones concurrently.

## Project Overview

This project demonstrates how to build an asynchronous, responsive image classification service using Python, ZeroMQ, and a pre-trained CNN (MobileNetV2). It is structured into several modules:

- **Server (`src/server.py`):**  
  - Receives image URL lists from clients.
  - Immediately acknowledges each request.
  - Offloads image fetching and classification tasks to a worker thread pool.
  - Publishes classification results (with human-readable labels) via a PUB socket.

- **Classifier (`src/classifier.py`):**  
  - Loads a pre-trained MobileNetV2 model.
  - Transforms and classifies images.
  - Uses an ImageNet class index (provided via `imagenet_class_index.json`) to map numerical predictions to human-readable labels.

- **Image Fetcher (`src/image_fetcher.py`):**  
  - Downloads images from provided URLs.

- **Client (`src/client.py`):**  
  - Parses a CSV file containing image URLs.
  - Sends the URLs to the server.
  - Listens for and prints classification results.


## Prerequisites

- [Docker](https://www.docker.com/) (for containerizing and running the service)
- Python 3.9+ (if running locally)
- [Optional] A virtual environment if running without Docker

## Running the Project with Docker

### 1. Build the Server Docker Image

In the project root (where your `Dockerfile` is located), run:

```sh
docker build -t toy-service .
```
### 2. Run the Server Container
```sh
docker run -p 5555:5555 -p 5556:5556 toy-service
```

### 3. Running the Client
```sh
python src/client.py urls.csv
```

## Running Tests
```sh
pytest
```
This will run tests located in the tests/ directory.