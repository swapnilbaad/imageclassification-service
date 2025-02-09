# src/server.py
import asyncio
import sys

if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import asyncio
import zmq.asyncio
import configparser
from classifier import classify_image_async

async def main():
    # Load configuration from config.ini
    config = configparser.ConfigParser()
    config.read('config.ini')
    rep_address = config.get('server', 'rep_address')
    pub_address = config.get('server', 'pub_address')

    # Create asynchronous ZeroMQ context and sockets
    ctx = zmq.asyncio.Context()
    rep_socket = ctx.socket(zmq.REP)
    rep_socket.bind(rep_address)
    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind(pub_address)

    loop = asyncio.get_event_loop()

    print(f"Toy-service started, listening on {rep_address}")
    while True:
        # Await a JSON message from a client (a list of image URLs)
        message = await rep_socket.recv_json()
        urls = message.get("urls", [])
        # Immediately send an acknowledgment back to the client
        await rep_socket.send_json({"status": "received", "num_urls": len(urls)})

        # For each URL, schedule the classification task concurrently
        for url in urls:
            asyncio.create_task(classify_image_async(url, pub_socket, loop))

if __name__ == '__main__':
    asyncio.run(main())
