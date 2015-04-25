#!/usr/bin/env python

import asyncio
import websockets
import json
import logging

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

@asyncio.coroutine
def handle_message(websocket, path):
    running = True
    while running:
        msg_str = yield from websocket.recv()
        if msg_str is None:
            running = False
            continue
        msg = json.loads(msg_str)
        print("Got message: %2".format(json.dumps(msg)))

start_server = websockets.serve(handle_message, 'localhost', 8765)

if __name__ == "__main__":
    logger.warning("Go, go, go!")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
