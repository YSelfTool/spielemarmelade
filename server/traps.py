TRAP_PITFALL = 1


class Trap(object):
    def __init__(self, trap_id, owner, position, durability):
        self.trap_id = trap_id
        self.owner = owner
        self.position = position
        self.upgrades = []
        self.durability = durability

    def to_dict(self):
        return {
            "id": self.trap_id,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades,
            "durability": self.durability
        }


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
