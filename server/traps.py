TRAP_PITFALL = 0
TRAP_SPIKE = 1
TRAP_CATAPULT = 2
TRAP_LOOT = 3

import game
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

from game_object import Placeable, cost_lookup


class Trap(Placeable):
    def __init__(self, object_id, kind, owner, position, durability, has_durability=True):
        super().__init__(object_id, kind, owner, position, (1, 1), [])
        self.durability = durability
        self.has_durability = has_durability

    def __repr__(self):
        return "<Trap: Id={}, Kind={}, Owner={}, Position={}, HasDurability={}, Durability={}".format(self.object_id, self.kind, self.owner, self.position, self.has_durability, self.durability)

    def to_dict(self):
        d = super().to_dict()
        d["durability"] = self.durability
        return d

    def handle_unit(self, unit, player):
        pass

    def equals(self, trap):
        #TODO if (upgrades):
        return trap.durability == self.durability


class PitfallTrap(Trap):
    def __init__(self, object_id, owner, position, capacity=10):
        super().__init__(object_id, TRAP_PITFALL, owner, position, -1, False)
        self.capacity = capacity
        self.mobs_in_trap = 0

    def __repr__(self):
        return "<PitfallTrap: Id={}, Owner={}, Position={}, MobsInTrap={}, Capacity={}>".format(self.object_id, self.owner, self.position, self.mobs_in_trap, self.capacity)

    def to_dict(self):
        d = super().to_dict()
        d["capacity"] = self.capacity
        d["mobs_in_trap"] = self.mobs_in_trap
        return d

    def equals(self, trap):
        return super().equals(trap) and (self.mobs_in_trap == trap.mobs_in_trap)

    def handle_unit(self, unit, player):
        if self.mobs_in_trap <= self.capacity:
            self.mobs_in_trap += 1
            unit.hp = 0


class SpikeTrap(Trap):
    def __init__(self, object_id, owner, position):
        super().__init__(object_id, TRAP_SPIKE, owner, position, 25)

    def __repr__(self):
        return "<SpikeTrap: Id={}, Owner={}, Position={}, Durability={}>".format(self.object_id, self.owner, self.position, self.durability)

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 4


class CatapultTrap(Trap):
    def __init__(self, object_id, owner, position):
        super().__init__(object_id, TRAP_CATAPULT, owner, position, 10)
        self.range = 4

    def __repr__(self):
        return "<CatapultTrap: Id={}, Owner={}, Position={}, Durability={}, Range={}>".format(self.object_id, self.owner, self.position, self.durability, self.range)

    def to_dict(self):
        d = super().to_dict()
        d["range"] = self.range
        return d

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 1
        (x, y) = unit.position
        new_x = x - (unit.direction * self.range)
        if (unit.direction == -1) and (new_x > game.MAP_SIZE_X-3):
            new_x = game.MAP_SIZE_X-3
        elif (unit.direction == 1) and (new_x < 2):
            new_x = 2

        unit.position[0] = new_x


class LootTrap(Trap):
    def __init__(self, object_id, owner, position):
        super().__init__(object_id, TRAP_LOOT, owner, position, 15)

    def __repr__(self):
        return "<LootTrap: Id={}, Owner={}, Position={}, Durability={}>".format(self.object_id, self.owner, self.position, self.durability)

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 1
        player.money += 0.1*unit.bounty


lookup = {
    TRAP_PITFALL: PitfallTrap,
    TRAP_SPIKE: SpikeTrap,
    TRAP_CATAPULT: CatapultTrap,
    TRAP_LOOT: LootTrap
}

cost_lookup[PitfallTrap] = ("trap", TRAP_PITFALL, 500)
cost_lookup[SpikeTrap] = ("trap", TRAP_SPIKE, 750)
cost_lookup[CatapultTrap] = ("trap", TRAP_CATAPULT, 4000)
cost_lookup[LootTrap] = ("trap", TRAP_LOOT, 3000)
