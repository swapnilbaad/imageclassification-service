# Image Classification Service

A service that accepts a list of image URLs via a ZeroMQ REQ/REP socket, fetches the images, runs a CNN-based image classification on them, and publishes the results over a ZeroMQ PUB/SUB socket. The service is designed to remain responsive to new requests even while processing previous ones concurrently.

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
docker build -t image-classification-service .
```
### 2. Run the Server Container
```sh
docker run -p 5555:5555 -p 5556:5556 image-classification-service
```

### 3. Running the Client
```sh
python src/client.py urls.csv
```
## Running Tests
To ensure the correctness of the code, we have a test suite using `pytest`.

### Running Tests in Docker
If you want to run tests inside a Docker container, use the following command:
```sh
docker run --rm image-classification-service pytest
```
This will start a temporary container, execute all tests, and remove the container after completion.

## Input CSV File Format
The input CSV file should contain a list of image URLs, one per line. For example:
```csv
https://picsum.photos/200/300
```
The client reads these URLs, sends them to the server for classification, and listens for results.

### About `https://picsum.photos/200/300`
[`https://picsum.photos`](https://picsum.photos/) is a free image placeholder service that provides random images with the specified width and height. The URL `https://picsum.photos/200/300` fetches a random image with dimensions **200x300 pixels**. This can be useful for testing the image classification service without needing specific image files.

# Running Locally with Virtual Environment

To run the project locally using a virtual environment:

1. **Create and activate a virtual environment:**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   venv\Scripts\activate     # On Windows
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

### Running the Server Locally
To start the server locally after setting up the virtual environment:
```sh
python src/server.py
```

### Running the Client Locally
To run the client after setting up the virtual environment:
```sh
python src/client.py path/to/urls.csv
```

## Running Tests
To ensure the correctness of the code, we have a test suite using `pytest`.

### Running Tests Locally
   ```sh
   pytest
   ```
   This will execute all test cases in the `tests/` directory.
