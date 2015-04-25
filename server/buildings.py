BUILDING_HQ = 0
BUILDING_SPAWNER = 1


class Building(object):
    def __init__(self, building_id, size, owner, position):
        self.building_id = building_id
        self.size = size
        self.owner = owner
        self.position = position
        self.upgrades = []

    def to_dict(self):
        return {
            "id": self.building_id,
            "size": [self.size[0], self.size[1]],
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades
        }

    def copy(self):
        Building(self.building_id, self.size, self.owner, self.position) 

class Headquaters(Building):
    def __init__(self, owner, position):
        super().__init__(BUILDING_HQ, (1, 4), owner, position)


class Spawner(Building):
    def __init__(self, owner, position, mob_kind):
        super().__init__(BUILDING_SPAWNER, (1, 1), owner, position)
        self.mob_kind = mob_kind

    def to_dict(self):
        d = super().to_dict()
        d["mob_kind"] = self.mob_kind
        return d
