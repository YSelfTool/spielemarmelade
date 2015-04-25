#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import base64
import os

from server.player import Player
from server import error_codes

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ws_logger = logging.getLogger('websockets.server')
ws_logger.setLevel(logging.DEBUG)
ws_logger.addHandler(logging.StreamHandler())

players = {}
player_id_counter = 1


def get_next_player_id():
    global player_id_counter
    tmp = player_id_counter
    player_id_counter += 1
    return tmp


def send_error_message(socket, msg, code=-1, can_continue=True):
    data = {"action": "error", "message": msg, "error_code": code, "can_continue": can_continue}
    print("sending error message",data)
    yield from socket.send(json.dumps(data))
    print("sent error message")


def handle_set_name(msg, socket, token):
    name = msg["nickname"]
    msg_token = msg["token"]
    if msg_token is None or token != msg_token:
        send_error_message(socket, "Token fehlt oder falsch", error_codes.INVALID_TOKEN, False)
        logger.error("Client token missing or wrong")
        socket.close()
        return None

    if name is not None:
        if name in players:
            maybe_the_player = players[name]
            if maybe_the_player.token == msg_token:
                the_player = maybe_the_player
            else:
                asyncio.async(send_error_message(socket, "Name ist bereits belegt", error_codes.NICKNAME_ALREADY_IN_USE))
                the_player = None
        else:
            the_player = Player(name, get_next_player_id(), token)
            players[name] = the_player
    else:
        logger.error("set_player_name did not contain any name")
    return the_player

def dumpObjectInfo(obj):
    for e in dir(obj):
        attr=getattr(obj,e)
        print("name:", str(e), "type:", type(attr), "content:", attr)


@asyncio.coroutine
def handle_message(websocket, path):
    running = True
    the_player = None
    the_token = base64.b64encode(os.urandom(8)).decode("UTF-8")

    yield from websocket.send(json.dumps({"action": "set_token", "token": the_token}))

    while running:
        msg_str = yield from websocket.recv()
        if msg_str is None:
            running = False
            if the_player is not None:
                players.pop(the_player.name)
            continue
        print("Message String:",msg_str)
        try:
            msg = json.loads(msg_str)
        except Exception as e:
            logger.error("Error decoding json ", e)
            running = False
            websocket.close()
        logger.debug("Got message: {}".format(json.dumps(msg)))

        action = msg["action"]
        if action == "set_name":
            the_player = handle_set_name(msg, websocket, the_token)
            logger.debug("Added player %s", the_player)
        elif action == "quit":
            logger.info("Client is quitting")
            websocket.close()
            running = False
            if the_player is not None:
                players.pop(the_player.name)
        else:
            logger.error("Unknown action {} ", str(action))

start_server = websockets.serve(handle_message, '', 8765)

if __name__ == "__main__":
    logger.info("Go, go, go!")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
