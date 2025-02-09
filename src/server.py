import asyncio
import zmq.asyncio
import configparser
import logging
from classifier import classify_image_async

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)

async def main():
    """
    Main server loop handling ZeroMQ communication.
    """
    # Load configuration
    config = configparser.ConfigParser()
    config.read('config.ini')
    rep_address = config.get('server', 'rep_address')
    pub_address = config.get('server', 'pub_address')

    # Create ZeroMQ context and sockets
    ctx = zmq.asyncio.Context()
    rep_socket = ctx.socket(zmq.REP)
    rep_socket.bind(rep_address)
    pub_socket = ctx.socket(zmq.PUB)
    pub_socket.bind(pub_address)

    loop = asyncio.get_event_loop()

    logger.info(f"Toy-service started, listening on {rep_address}")
    while True:
        message = await rep_socket.recv_json()
        urls = message.get("urls", [])
        logger.info(f"Received request with {len(urls)} URLs")
        await rep_socket.send_json({"status": "received", "num_urls": len(urls)})

        for url in urls:
            asyncio.create_task(classify_image_async(url, pub_socket, loop))

if __name__ == '__main__':
    asyncio.run(main())