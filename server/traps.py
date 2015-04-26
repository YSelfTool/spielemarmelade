TRAP_PITFALL = 0
TRAP_SPIKE = 1
TRAP_CATAPULT = 2
TRAP_LOOT = 3

import game
import logging
logger = logging.getLogger(__name__)


class Trap(object):
    def __init__(self, trap_id, trap_type, owner, position, durability, has_durability=True):
        self.trap_id = trap_id
        self.trap_type = trap_type
        self.owner = owner
        self.position = position
        self.upgrades = []
        self.durability = durability
        self.has_durability = has_durability

    def to_dict(self):
        return {
            "id": self.trap_id,
            "type": self.trap_type,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades,
            "durability": self.durability
        }

    def copy(self):
        return Trap(self.trap_id, self.trap_type, self.owner, self.position, self.durability, self.has_durability)

    def handle_unit(self, unit, player):
        pass

    def equals(self, trap):
        #TODO if (upgrades):
        if (trap.durability != self.durability):
            return False
        return True


class PitfallTrap(Trap):
    def __init__(self, trap_id, owner, position, capacity=10):
        super().__init__(trap_id, TRAP_PITFALL, owner, position, -1, False)
        self.capacity = capacity
        self.mobs_in_trap = 0

    def to_dict(self):
        d = super().to_dict()
        d["capacity"] = self.capacity
        d["mobs_in_trap"] = self.mobs_in_trap
        return d

    def copy(self):
        return PitfallTrap(self.trap_id, self.owner, self.position, self.capacity)

    def equals(self, trap):
        return super.equals(trap) and (self.mobs_in_trap != trap.mobs_in_trap)

    def handle_unit(self, unit, player):
        if self.mobs_in_trap <= self.capacity:
            self.mobs_in_trap += 1
            unit.hp = 0


class SpikeTrap(Trap):
    def __init__(self, trap_id, owner, position):
        super().__init__(trap_id, TRAP_SPIKE, owner, position, 25)

    def copy(self):
        return SpikeTrap(self.trap_id, self.owner, self.position)

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 4


class CatapultTrap(Trap):
    def __init__(self, trap_id, owner, position):
        super().__init__(trap_id, TRAP_CATAPULT, owner, position, 50)
        self.range = 4

    def to_dict(self):
        d = super().to_dict()
        d["range"] = self.range

    def copy(self):
        return CatapultTrap(self.trap_id, self.owner, self.position)

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 1
        (x, y) = unit.position
        new_x = x - unit.direction * self.range
        if (unit.direction == -1) and (new_x < 2):
            new_x = 2
        elif (unit.direction == 1) and (new_x > game.MAP_SIZE_X-2):
            new_x = game.MAP_SIZE_X-2

        unit.position[0] = new_x


class LootTrap(Trap):
    def __init__(self, trap_id, owner, position):
        super().__init__(trap_id, TRAP_LOOT, owner, position, 15)

    def copy(self):
        return LootTrap(self.trap_id, self.owner, self.position)

    def handle_unit(self, unit, player):
        self.durability -= unit.trap_wear
        unit.hp -= 1
        player.money += 0.1*unit.bounty


lookup = {0: PitfallTrap, 1: SpikeTrap, 2: CatapultTrap, 3: LootTrap}
