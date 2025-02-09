### src/server.py
import zmq
import concurrent.futures
from classifier import classify_image
from image_fetcher import fetch_image
import configparser
import os
# Load configuration
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), '../config.ini')
config.read('config.ini')

rep_address = config.get('server', 'rep_address')
pub_address = config.get('server', 'pub_address')
max_workers = config.getint('general', 'max_workers')

# ZeroMQ Context
context = zmq.Context()

# REP socket for receiving requests
rep_socket = context.socket(zmq.REP)
rep_socket.bind(rep_address)

# PUB socket for publishing results
pub_socket = context.socket(zmq.PUB)
pub_socket.bind(pub_address)

# Worker pool for processing images
executor = concurrent.futures.ThreadPoolExecutor(max_workers=max_workers)

print("Toy-service started, listening on port 5555")
while True:
    # Receive list of image URLs
    message = rep_socket.recv_json()
    urls = message.get("urls", [])
    rep_socket.send_json({"status": "received", "num_urls": len(urls)})
    
    # Process each image asynchronously
    for url in urls:
        executor.submit(classify_image, url, pub_socket)