#!/usr/bin/env python

import asyncio
import websockets
import json
import logging
import base64
import os

from player import Player
import error_codes
import game

logging.basicConfig(format='%(asctime)s %(name)s %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

ws_logger = logging.getLogger('websockets.server')
ws_logger.setLevel(logging.DEBUG)
ws_logger.addHandler(logging.StreamHandler())

players = {}
player_id_counter = 1
waiting_games = {}
running_games = {}
player_id_to_game = {}


def get_next_player_id():
    global player_id_counter
    tmp = player_id_counter
    player_id_counter += 1
    return tmp


def send_error_message(socket, msg, code=-1, can_continue=True):
    data = {"action": "error", "message": msg, "error_code": code, "can_continue": can_continue}
    yield from socket.send(json.dumps(data))


def send_game_queued(socket, game_name):
    data = {"action": "game_queued", "game_name": game_name}
    yield from socket.send(json.dumps(data))


def send_game_started(socket, enemy):
    data = {"action": "game_started", "enemy": {"enemy_id": enemy.player_id, "enemy_name": enemy.name}}
    yield from socket.send(json.dumps(data))


def handle_set_name(msg, socket, token):
    name = msg["nickname"]
    msg_token = msg["token"]
    the_player = None

    if name is not None:
        if name in players:
            maybe_the_player = players[name]
            if maybe_the_player.token == msg_token:
                the_player = maybe_the_player
            else:
                asyncio.async(send_error_message(socket, "Name ist bereits belegt", error_codes.NICKNAME_ALREADY_IN_USE))
                the_player = None
        else:
            the_player = Player(name, get_next_player_id(), token, socket)
            players[name] = the_player
    else:
        logger.error("set_player_name did not contain any name")
    return the_player


def validate_token(msg, token):
    return msg["token"] is not None and msg["token"] == token


def handle_join_game(msg, socket, player):
    global waiting_games, running_games
    game_name = msg["game_name"]
    if game_name in running_games:
        logger.info("Player %s is trying to join already running game %s", player.name, game_name)
        asyncio.async(send_error_message(socket, "Ein Spiel mit diesem Namen läuft bereits. Bitte gib einen neuen Namen für dein Spiel an", error_codes.GAME_WITH_NAME_ALREADY_RUNNING))
        return
    elif game_name in waiting_games:
        logger.info("Player %s joining waiting game %s", player.name, game_name)
        the_game = waiting_games[game_name]
        the_game.player2 = player
        the_game.running = True
        running_games[game_name] = the_game
        waiting_games.pop(game_name)
        logger.info("Staring game %s with %s and %s", the_game.name, the_game.player1.name, the_game.player2.name)
        asyncio.async(send_game_started(the_game.player1.socket, the_game.player2))
        asyncio.async(send_game_started(the_game.player2.socket, the_game.player1))
        player_id_to_game[the_game.player1.player_id] = the_game
        player_id_to_game[the_game.player2.player_id] = the_game
        the_game_state = game.GameState(the_game)
        the_game.state = the_game_state
        asyncio.async(simulate_game(the_game))
    else:
        logger.info("Player %s started a new game called %s", player.name, game_name)
        the_game = game.Game(game_name)
        the_game.player1 = player
        waiting_games[game_name] = the_game
        player_id_to_game[the_game.player1.player_id] = the_game
        asyncio.async(send_game_queued(socket, game_name))


def send_player_id(socket, player):
    data = {"action": "set_player_id", "id": player.player_id}
    yield from socket.send(json.dumps(data))


def dump_object_info(obj):
    for e in dir(obj):
        attr = getattr(obj, e)
        print("name:", str(e), "type:", type(attr), "content:", attr)


@asyncio.coroutine
def simulate_game(the_game):
    if the_game.state is None:
        logger.error("Game named %s has no state", the_game.name)
        return
    logger.info("Now simulating the game name %s", the_game.name)
    the_game.state.send_full_state()
    while the_game.running:
        logger.debug("Updating game named %s", the_game.name)
        the_game.state.tick()
        the_game.state.send_state_delta()
        yield from asyncio.sleep(0.5)
    logger.info("The game named %s is done", the_game.name)
    player1_still_here = the_game.player1.player_id in player_id_to_game
    player2_still_here = the_game.player2.player_id in player_id_to_game
    logger.info("Player 1 is still here: %s, Player 2 is still here: %s", player1_still_here, player2_still_here)
    if player1_still_here:
        player_id_to_game.pop(the_game.player1.player_id)
    elif player2_still_here:
        asyncio.async(send_error_message(the_game.player2.socket, "Der andere Spieler hat das Spiel verlassen", error_codes. GAME_OVER_PLAYER_QUIT, False))

    if player2_still_here:
        player_id_to_game.pop(the_game.player2.player_id)
    elif player1_still_here:
        asyncio.async(send_error_message(the_game.player1.socket, "Der andere Spieler hat das Spiel verlassen", error_codes. GAME_OVER_PLAYER_QUIT, False))


def handle_game_message(the_game, msg):
    return the_game.state.handle_message(msg)


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
                logger.info("Player %s disconnected...", the_player.name)
                players.pop(the_player.name)
                if the_player.player_id in player_id_to_game:
                    the_game = player_id_to_game[the_player.player_id]
                    player_id_to_game.pop(the_player.player_id)
                    if the_game is not None:
                        the_game.running = False
                        if the_game.name in waiting_games:
                            waiting_games.pop(the_game.name)

            continue
        try:
            msg = json.loads(msg_str)
            if not validate_token(msg, the_token):
                raise Exception("Invalid token")
        except Exception as e:
            logger.error("Error decoding json ", e)
            running = False
            websocket.close()
        logger.debug("Got message: {}".format(json.dumps(msg)))

        action = msg["action"]
        if action == "set_name":
            the_player = handle_set_name(msg, websocket, the_token)
            if the_player is not None:
                asyncio.async(send_player_id(websocket, the_player))
                logger.debug("Added player %s", the_player)
        elif action == "quit":
            logger.info("Client is quitting")
            websocket.close()
            running = False
            if the_player is not None:
                players.pop(the_player.name)
        elif action == "join_game":
            handle_join_game(msg, websocket, the_player)
        else:
            the_game = player_id_to_game[the_player]
            if (the_game is not None) and (handle_game_message(the_game, msg)):
                pass
            else:
                logger.error("Unknown action {} ", str(action))

start_server = websockets.serve(handle_message, '', 8765)

if __name__ == "__main__":
    logger.info("Server loaded and ready to rock!")
    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()
