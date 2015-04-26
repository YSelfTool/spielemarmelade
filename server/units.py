UNIT_SOLIDER = 0


class Unit(object):
    def __init__(self, unit_id, owner, position, upgrades, hp, bounty, trap_wear, direction):
        self.unit_id = unit_id
        self.owner = owner
        self.position = position
        self.upgrades = upgrades
        self.hp = hp
        self.bounty = bounty
        self.trap_wear = trap_wear
        self.direction = direction # 1 = left, -1 = right

    def to_dict(self):
        return {
            "id": self.unit_id,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades,
            "hp": self.hp,
            "bounty": self.bounty,
            "wear": self.trap_wear
        }

    def copy(self):
        return Unit(self.unit_id, self.owner, self.position.copy(), self.upgrades.copy(), self.hp, self.bounty, self.trap_wear, self.direction)

    def get_next_position(self):
        return None

    def may_move(self):
        return None

    def set_new_position(self, position):
        self.position = position

    def equals(self, unit):
        if unit.position != self.position:
            return False
        #TODO if (upgrades):
        if unit.hp != self.hp:
            return False
        return True

class UnitSolider(Unit):
    def __init__(self, owner, position, upgrades):
        super().__init__(UNIT_SOLIDER, owner, position, upgrades, 10, 20, 1)
