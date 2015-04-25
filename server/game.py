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

    def tick(self):
        pass

    def send_full_state(self):
        pass

    def send_state_delta(self):
        pass

    def handle_message(self, msg):
        pass
