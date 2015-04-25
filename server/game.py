import json
import logging
logger = logging.getLogger(__name__)

MAP_SIZE_X = 64
MAP_SIZE_Y = 32


class Game(object):
    def __init__(self, name):
        self.name = name
        self.player1 = None
        self.player2 = None
        self.running = False
        self.state = None


class GameState(object):
    def __init__(self, the_game):
        self.game = the_game
        self.map = [[None for y in range(MAP_SIZE_Y)] for x in range(MAP_SIZE_X)]
        self.units = []
        self.traps = []
        self.buildings = []
        self.unit_id_counter = 1
        self.action_buffer = []

    # after each round
    def tick(self):
        the_actions = self.action_buffer.copy()
        self.action_buffer = []


    #beginning state
    def send_full_state(self):
        self.do_send_data({
            "action": "full_game_state",
            "size": [MAP_SIZE_X, MAP_SIZE_Y],
            "units": [unit.to_dict() for unit in self.units],
            "traps": [trap.to_dict() for trap in self.traps],
            "buildings": [building.to_dict() for building in self.buildings]
        })

    #changes after each tick
    def send_state_delta(self):
        pass

    def handle_message(self, msg):
        self.action_buffer.append(msg)

    def get_next_unit_id(self):
        tmp = self.unit_id_counter
        self.unit_id_counter += 1
        return tmp

    def do_send_data(self, data):
        json_str = json.dumps(data)
        self.game.player1.socket.send(json_str)
        self.game.player2.socket.send(json_str)
