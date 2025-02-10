# src/client.py
import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import argparse
import csv
import zmq.asyncio
import configparser
import sys
import asyncio
import os

def parse_csv(file_path):
    """
    Reads a CSV file and extracts valid URLs.

    :param file_path: Path to the CSV file
    :return: List of valid URLs
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    urls = []
    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()  # Remove extra spaces and newlines
            if line and (line.startswith("http://") or line.startswith("https://")):
                urls.append(line)
    
    return urls

async def main():
    parser = argparse.ArgumentParser(
        description='Async Client for toy-service that sends image URLs and prints classification results.'
    )
    parser.add_argument('csv_file', help='Path to the CSV file containing image URLs')
    args = parser.parse_args()

    urls = parse_csv(args.csv_file)
    num_urls = len(urls)
    if num_urls == 0:
        print("No URLs found in the CSV file.")
        sys.exit(1)

    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    server_req_address = config.get('client', 'server_req_address')
    server_pub_address = config.get('client', 'server_pub_address')

    ctx = zmq.asyncio.Context()
    req_socket = ctx.socket(zmq.REQ)
    req_socket.connect(server_req_address)
    sub_socket = ctx.socket(zmq.SUB)
    sub_socket.connect(server_pub_address)
    sub_socket.setsockopt_string(zmq.SUBSCRIBE, "")  # Subscribe to all messages

    # Send the list of URLs to the server
    await req_socket.send_json({"urls": urls})
    ack = await req_socket.recv_json()
    print("Server Acknowledged:", ack)
    expected_results = ack.get("num_urls", num_urls)
    received = 0
    print("Waiting for classification results...\n")
    while received < expected_results:
        result = await sub_socket.recv_json()
        print("Received:", result)
        received += 1
    print("\nAll inferences received.")
    req_socket.close()
    sub_socket.close()
    ctx.term()

if __name__ == '__main__':
    asyncio.run(main())
