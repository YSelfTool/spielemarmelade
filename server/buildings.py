BUILDING_HQ = 0
BUILDING_SPAWNER = 1


class Building(object):
    def __init__(self, building_id, building_kind, size, owner, position):
        self.building_id = building_id
        self.building_kind = building_kind
        self.size = size
        self.owner = owner
        self.position = position
        self.upgrades = []

    def to_dict(self):
        return {
            "id": self.building_id,
            "kind": self.building_kind,
            "size": [self.size[0], self.size[1]],
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades
        }

    def copy(self):
        return Building(self.building_kind, self.building_id, self.size, self.owner, self.position)

    def __repr__(self):
        return "<Building: Id={}, Kind={}, Size={}, Owner={}, Position={}, Upgrades=[]>".format(self.building_id, self.building_kind, self.size, self.owner, self.position, self.upgrades)

    def equals(self, building):
        return (self.id == building.id) and (self.building_kind == building.building_kind) and (self.position == building.position)


class Headquaters(Building):
    def __init__(self, building_id, owner, position):
        super().__init__(building_id, BUILDING_HQ, (1, 4), owner, position)

    def __repr__(self):
        return "<Headquaters: Id={}, Size={}, Owner={}, Position={}, Upgrades=[]>".format(self.building_id, self.size, self.owner, self.position, self.upgrades)

    def copy(self):
        return Headquaters(self.building_id, self.owner, self.position)


class Spawner(Building):
    def __init__(self, building_id, owner, position, mob_kind):
        super().__init__(building_id, BUILDING_SPAWNER, (1, 1), owner, position)
        self.mob_kind = mob_kind

    def __repr__(self):
        return "<Spawner: Id={}, Owner={}, Position={}, Upgrades=[], MobKind={}>".format(self.building_id, self.size, self.owner, self.position, self.upgrades, self.mob_kind)

    def equals(self, building):
        return super.equals(building) and (isinstance(building, Spawner)) and (self.mob_kind == building.mob_kind)

    def copy(self):
        return Spawner(self.building_id, self.owner, self.position, self.mob_kind)

    def to_dict(self):
        d = super().to_dict()
        d["mob_kind"] = self.mob_kind
        return d
