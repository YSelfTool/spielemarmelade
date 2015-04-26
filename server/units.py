UNIT_SOLIDER = 0
UNIT_JUMPER = 1
UNIT_RUNNER = 2
UNIT_TANK = 3
UNIT_CROOKEDSOLDIER = 4
UNIT_TOPSTEPSOLDIER = 5
UNIT_BOTTOMSTEPSOLDIER = 6


class Unit(object):
    def __init__(self, unit_id, unit_kind, owner, position, upgrades, hp, bounty, trap_wear, direction, speed):
        self.unit_id = unit_id
        self.unit_kind = unit_kind
        self.owner = owner
        self.position = position
        self.upgrades = upgrades
        self.hp = hp
        self.bounty = bounty
        self.trap_wear = trap_wear
        self.direction = direction # 1 = left, -1 = right
        self.speed = speed
        self.speed_counter = speed

    def to_dict(self):
        return {
            "id": self.unit_id,
            "kind": self.unit_kind,
            "owner": self.owner,
            "position": [self.position[0], self.position[1]],
            "upgrades": self.upgrades,
            "hp": self.hp,
            "bounty": self.bounty,
            "wear": self.trap_wear
        }

    def copy(self):
        return Unit(self.unit_id, self.unit_kind, self.owner, self.position.copy(), self.upgrades.copy(), self.hp, self.bounty, self.trap_wear, self.direction, self.speed, self.speed_counter)

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
        if unit.unit_kind != self.unit_kind:
            return False
        if unit.position != self.position:
            return False
        #TODO if (upgrades):
        if unit.hp != self.hp:
            return False
        return True


class UnitSolider(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 2
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_SOLIDER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return (x + self.direction, y)


class UnitJumper(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        speed = 8
        trap_wear = 3
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_JUMPER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return (x + (2 * self.direction), y)


class UnitRunner(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        speed = 2
        trap_wear = 1
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_RUNNER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return (x + self.direction, y)


class UnitTank(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 3
        hp = 30
        bounty = 20
        super().__init__(unit_id, UNIT_TANK, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return (x + self.direction, y)


class UnitCrookedSoldier(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        speed = 5
        trap_wear = 2
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_CROOKEDSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        return (x + self.direction, y + 1)


class UnitTopStepSoldier(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        self.step_counter = 0
        
        speed = 5
        trap_wear = 2
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_TOPSTEPSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position
        new_position = ()
        self.step_counter += 1
        if self.step_counter < 5:
            new_position = (x + self.direction, y)
        else:
            self.step_counter = 0
            new_position = (x, y + 1)


class UnitBottomStepSoldier(Unit):
    def __init__(self, unit_id, owner, position, upgrades, direction):
        self.step_counter = 0
        
        speed = 5
        trap_wear = 2
        hp = 10
        bounty = 20
        super().__init__(unit_id, UNIT_BOTTOMSTEPSOLDIER, owner, position, upgrades, hp, bounty, trap_wear, direction, speed)

    def get_next_position(self):
        (x, y) = self.position

        new_position = ()
        self.step_counter += 1
        if self.step_counter < 5:
            new_position = (x + self.direction, y)
        else:
            self.step_counter = 0
            new_position = (x, y - 1)

lookup = {UNIT_SOLIDER: UnitSolider, UNIT_JUMPER: UnitJumper, UNIT_RUNNER: UnitRunner, UNIT_TANK: UnitTank, UNIT_CROOKEDSOLDIER: UnitCrookedSoldier, UNIT_TOPSTEPSOLDIER: UnitTopStepSoldier, UNIT_BOTTOMSTEPSOLDIER: UnitBottomStepSoldier}
