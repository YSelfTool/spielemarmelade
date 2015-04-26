BUILDING_HQ = 0
BUILDING_SPAWNER = 1

from game_object import Placeable, cost_lookup
import units


class Building(Placeable):
    def __init__(self, object_id, kind, size, owner, position):
        super().__init__(object_id, kind, owner, position, size, [])

    def __repr__(self):
        return "<Building: Id={}, Kind={}, Size={}, Owner={}, Position={}, Upgrades=[]>".format(self.object_id, self.kind, self.size, self.owner, self.position, self.upgrades)

    def equals(self, building):
        return (self.object_id == building.object_id) and (self.kind == building.kind) and (self.position == building.position)

    def tick(self, player):
        pass


class Headquaters(Building):
    def __init__(self, object_id, owner, position):
        size = (1, 4)
        super().__init__(object_id, BUILDING_HQ, size, owner, position)
        self.income_per_tick = 10

    def __repr__(self):
        return "<Headquaters: Id={}, Size={}, Owner={}, Position={}, Upgrades=[]>".format(self.object_id, self.size, self.owner, self.position, self.upgrades)

    def tick(self, player):
        player.add_money(self.income_per_tick)

    def to_dict(self):
        d = super().to_dict()
        d["income_per_tick"] = self.income_per_tick
        return d


class Spawner(Building):
    def __init__(self, object_id, owner, position, mob_kind, num_mobs, cooldown_ticks):
        size = (1, 1)
        super().__init__(object_id, BUILDING_SPAWNER, size, owner, position)
        self.mob_kind = mob_kind
        self.num_mobs = num_mobs
        self.cooldown_ticks = cooldown_ticks
        self.current_cooldown = 0
        self.spawned_units = 0
        _, _, self.money_per_tick = cost_lookup[units.lookup[self.mob_kind]]
        self.money_per_tick *= 0.01

    def __repr__(self):
        return "<Spawner: Id={}, Owner={}, Position={}, Upgrades=[], MobKind={}, NumMobs={}, CooldownTicks={}, CurrentCooldown={}>".format(self.object_id, self.size, self.owner, self.position, self.upgrades, self.mob_kind, self.num_mobs, self.cooldown_ticks, self.current_cooldown)

    def equals(self, building):
        return super().equals(building) and \
            isinstance(building, Spawner) and \
            (self.mob_kind == building.mob_kind) and \
            (self.num_mobs == building.num_mobs) and \
            (self.cooldown_ticks == building.cooldown_ticks) and \
            (self.current_cooldown == building.current_cooldown)

    def to_dict(self):
        d = super().to_dict()
        d["mob_kind"] = self.mob_kind
        d["cooldown_ticks"] = self.cooldown_ticks
        d["current_cooldown"] = self.current_cooldown
        return d

    def tick(self, player):
        player.add_money(self.spawned_units*self.money_per_tick)
        self.current_cooldown -= 1
        if self.current_cooldown < 0:
            self.current_cooldown = 0

    def can_spawn(self):
        return self.current_cooldown == 0

    def reset_cooldown(self):
        self.current_cooldown = self.cooldown_ticks

cost_lookup[Headquaters] = ("building", BUILDING_HQ, 0)
cost_lookup[Spawner] = ("building", BUILDING_SPAWNER, 100)
