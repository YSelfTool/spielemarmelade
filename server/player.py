import logging
logger = logging.getLogger(__name__)


class Player(object):
    def __init__(self, name, player_id, token, socket):
        self.name = name
        self.player_id = player_id
        self.token = token
        self.socket = socket
        pass

    def __repr__(self):
        return "<Player Nickname={}, Id={}, Token={}>".format(self.name, self.player_id, self.token)
