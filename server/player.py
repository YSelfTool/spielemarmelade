import logging
logger = logging.getLogger(__name__)


class Player(object):
    def __init__(self, name, player_id, token, socket):
        self.name = name
        self.player_id = player_id
        self.token = token
        self.socket = socket
        self.money = 0
        self.health_points = 20
        pass

    def __repr__(self):
        return "<Player Nickname={}, Id={}, Token={}>".format(self.name, self.player_id, self.token)

    def lose_health_points(self):
        self.health_points -= 1

    def add_money(self, money):
        self.money += money

    def to_dict(self):
        return {
            "id": self.player_id,
            "hp": self.health_points,
            "money": money 
        }