### src/server.py
import zmq
import concurrent.futures
from classifier import classify_image
from image_fetcher import fetch_image

# ZeroMQ Context
context = zmq.Context()

# REP socket for receiving requests
rep_socket = context.socket(zmq.REP)
rep_socket.bind("tcp://*:5555")

# PUB socket for publishing results
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5556")

# Worker pool for processing images
executor = concurrent.futures.ThreadPoolExecutor(max_workers=4)

print("Toy-service started, listening on port 5555")
while True:
    # Receive list of image URLs
    message = rep_socket.recv_json()
    urls = message.get("urls", [])
    rep_socket.send_json({"status": "received", "num_urls": len(urls)})
    
    # Process each image asynchronously
    for url in urls:
        executor.submit(classify_image, url, pub_socket)