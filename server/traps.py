TRAP_PITFALL = 0


class Trap(object):
    def __init__(self, trap_id, owner, position, durability, has_durability):
        self.trap_id = trap_id
        self.owner = owner
        self.position = position
        self.upgrades = []
        self.durability = durability
        self.has_durability = has_durability

    def to_dict(self):
        return {
            "id": self.trap_id,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades,
            "durability": self.durability
        }

    def copy(self):
        return Trap(self.trap_id, self.owner, self.position, self.durability)

    def handle_unit(self, unit):
        pass

class PitfallTrap(Trap):
    def __init__(self, owner, position, capacity):
        super().__init__(TRAP_PITFALL, owner, position, -1)
        self.capacity = capacity
        self.mobs_in_trap = 0

    def to_dict(self):
        d = super().to_dict()
        d["capacity"] = self.capacity
        d["mobs_in_trap"] = self.mobs_in_trap
        return d
