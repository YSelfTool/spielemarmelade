UNIT_SOLIDER = 1

class Unit(object):
    def __init__(self, unit_id, owner, position, upgrades, hp, bounty, trap_wear):
        self.unit_id = unit_id
        self.owner = owner
        self.position = position
        self.upgrades = upgrades
        self.hp = hp
        self.bounty = bounty
        self.trap_wear = trap_wear

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

class UnitSolider(Unit):
    def __init__(self, owner, position, upgrades):
        super().__init__(UNIT_SOLIDER, owner, position, upgrades, 10, 20, 1)