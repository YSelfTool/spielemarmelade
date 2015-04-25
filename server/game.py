import logging
logger = logging.getLogger(__name__)

class Game(object):
    def __init__(self, name):
        self.name = name
        self.player1 = None
        self.player2 = None
        self.running = False

class GameState(object):
    def __init__(self):
        pass
