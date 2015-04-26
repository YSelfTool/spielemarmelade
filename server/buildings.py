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
        return (self.building_id == building.building_id) and (self.building_kind == building.building_kind) and (self.position == building.position)

    def tick(self, player):
        pass

class Headquaters(Building):
    def __init__(self, building_id, owner, position):
        super().__init__(building_id, BUILDING_HQ, (1, 4), owner, position)

    def __repr__(self):
        return "<Headquaters: Id={}, Size={}, Owner={}, Position={}, Upgrades=[]>".format(self.building_id, self.size, self.owner, self.position, self.upgrades)

    def copy(self):
        return Headquaters(self.building_id, self.owner, self.position)

    def tick(self, player):
        player.add_money(10)


class Spawner(Building):
    def __init__(self, building_id, owner, position, mob_kind, num_mobs, cooldown_ticks):
        super().__init__(building_id, BUILDING_SPAWNER, (1, 1), owner, position)
        self.mob_kind = mob_kind
        self.num_mobs = num_mobs
        self.cooldown_ticks = cooldown_ticks
        self.current_cooldown = 0

    def __repr__(self):
        return "<Spawner: Id={}, Owner={}, Position={}, Upgrades=[], MobKind={}, NumMobs={}, CooldownTicks={}, CurrentCooldown={}>".format(self.building_id, self.size, self.owner, self.position, self.upgrades, self.mob_kind, self.num_mobs, self.cooldown_ticks, self.current_cooldown)

    def equals(self, building):
        return super().equals(building) and \
            isinstance(building, Spawner) and \
            (self.mob_kind == building.mob_kind) and \
            (self.num_mobs == building.num_mobs) and \
            (self.cooldown_ticks == building.cooldown_ticks) and \
            (self.current_cooldown == building.current_cooldown)

    def copy(self):
        s = Spawner(self.building_id, self.owner, self.position, self.mob_kind, self.num_mobs, self.cooldown_ticks)
        s.current_cooldown = self.current_cooldown
        return s

    def to_dict(self):
        d = super().to_dict()
        d["mob_kind"] = self.mob_kind
        return d

    def tick(self, player):
        self.current_cooldown -= 1
        if self.current_cooldown < 0:
            self.current_cooldown = 0

    def can_spawn(self):
        return self.current_cooldown == 0

    def reset_cooldown(self):
        self.current_cooldown = self.cooldown_ticks

