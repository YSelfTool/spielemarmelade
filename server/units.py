UNIT_SOLIDER = 0
UNIT_JUMPER = 1
UNIT_RUNNER = 2
UNIT_TANK = 3
UNIT_CROOKEDSOLDIER = 4
UNIT_TOPSTEPSOLDIER = 5
UNIT_BOTTOMSTEPSOLDIER = 6

from game_object import GameObject, cost_lookup


class Unit(GameObject):
    def __init__(self, object_id, kind, owner, position, upgrades, hp, bounty, trap_wear, direction, speed):
        super().__init__(object_id, kind, owner, position, upgrades)
        self.hp = hp
        self.bounty = bounty
        self.trap_wear = trap_wear
        self.direction = direction  # 1 = left, -1 = right
        self.speed = speed
        self.speed_counter = speed

    def to_dict(self):
        d = super().to_dict()
        d["hp"] = self.hp
        d["bounty"] = self.bounty
        d["wear"] = self.trap_wear
        return d

    def get_next_position(self):
        pass

    def may_move(self):
        move = False
        self.speed_counter -= 1
        if self.speed_counter == 0:
            move = True
            self.speed_counter = self.speed
        return move

    def set_new_position(self, position):
        self.position = position

    def equals(self, unit):
        if unit.kind != self.kind:
            return False
        if unit.position != self.position:
            return False
        #TODO if (upgrades):
        if unit.hp != self.hp:
            return False
        return True


class UnitSolider(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 2
        hp = 20
        bounty = 150
        super().__init__(object_id, UNIT_SOLIDER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return x + self.direction, y


class UnitJumper(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        speed = 8
        trap_wear = 3
        hp = 20
        bounty = 200
        super().__init__(object_id, UNIT_JUMPER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return x + (2 * self.direction), y


class UnitRunner(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        speed = 2
        trap_wear = 1
        hp = 20
        bounty = 200
        super().__init__(object_id, UNIT_RUNNER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return x + self.direction, y


class UnitTank(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 3
        hp = 50
        bounty = 500
        super().__init__(object_id, UNIT_TANK, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return x + self.direction, y


class UnitCrookedSoldier(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 2
        hp = 20
        bounty = 750
        super().__init__(object_id, UNIT_CROOKEDSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return x + self.direction, y + 1


class UnitTopStepSoldier(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        self.step_counter = 0
        self.step_number = 5

        speed = 5
        trap_wear = 2
        hp = 20
        bounty = 600
        super().__init__(object_id, UNIT_TOPSTEPSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        self.step_counter += 1
        if self.step_counter < self.step_number:
            new_position = (x + self.direction, y)
        else:
            self.step_counter = 0
            new_position = (x, y + 1)
        return new_position


class UnitBottomStepSoldier(Unit):
    def __init__(self, object_id, owner, position, upgrades, direction):
        self.step_counter = 0
        self.step_number = 5

        speed = 5
        trap_wear = 2
        hp = 20
        bounty = 600
        super().__init__(object_id, UNIT_BOTTOMSTEPSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position

        self.step_counter += 1
        if self.step_counter < self.step_number:
            new_position = (x + self.direction, y)
        else:
            self.step_counter = 0
            new_position = (x, y - 1)
        return new_position

lookup = {
    UNIT_SOLIDER: UnitSolider,
    UNIT_JUMPER: UnitJumper,
    UNIT_RUNNER: UnitRunner,
    UNIT_TANK: UnitTank,
    UNIT_CROOKEDSOLDIER: UnitCrookedSoldier,
    UNIT_TOPSTEPSOLDIER: UnitTopStepSoldier,
    UNIT_BOTTOMSTEPSOLDIER: UnitBottomStepSoldier
}

cost_lookup[UnitSolider] = ("unit", UNIT_SOLIDER, 50)
cost_lookup[UnitJumper] = ("unit", UNIT_JUMPER, 150)
cost_lookup[UnitRunner] = ("unit", UNIT_RUNNER, 150)
cost_lookup[UnitTank] = ("unit", UNIT_TANK, 200)
cost_lookup[UnitCrookedSoldier] = ("unit", UNIT_CROOKEDSOLDIER, 500)
cost_lookup[UnitTopStepSoldier] = ("unit", UNIT_TOPSTEPSOLDIER, 400)
cost_lookup[UnitBottomStepSoldier] = ("unit", UNIT_BOTTOMSTEPSOLDIER, 400)
