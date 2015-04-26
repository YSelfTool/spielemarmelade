import json
import asyncio
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import buildings
import traps
import units

MAP_SIZE_X = 32
MAP_SIZE_Y = 16


class Game(object):
    def __init__(self, name):
        self.name = name
        self.player1 = None
        self.player2 = None
        self.running = False
        self.state = None


class GameState(object):
    def __init__(self, the_game):
        self.game = the_game
        self.map = [[None for _ in range(MAP_SIZE_Y)] for _ in range(MAP_SIZE_X)]
        self.units = []
        self.traps = []
        self.buildings = []
        self.unit_id_counter = 1
        self.trap_id_counter = 1
        self.building_id_counter = 1
        self.action_buffer = []
        self.spawn_headquaters()

    def get_building_bounds(self, building):
        building_x_start = building.position[0]
        building_y_start = building.position[1]
        if isinstance(building, traps.Trap):
            building_x_stop = building_x_start + 1
            building_y_stop = building_y_start + 1
        else:
            building_x_stop = building_x_start + building.size[0]
            building_y_stop = building_y_start + building.size[1]

        return building_x_start, building_x_stop, building_y_start, building_y_stop

    def get_building_bounds_at_position(self, building, position):
        building_x_start = position[0]
        building_y_start = position[1]
        if isinstance(building, traps.Trap):
            building_x_stop = building_x_start + 1
            building_y_stop = building_y_start + 1
        else:
            building_x_stop = building_x_start + building.size[0]
            building_y_stop = building_y_start + building.size[1]

        return building_x_start, building_x_stop, building_y_start, building_y_stop

    def place_building_in_map(self, building):
        (x1, x2, y1, y2) = self.get_building_bounds(building)

        for x in range(x1, x2):
            for y in range(y1, y2):
                self.map[x][y] = building

    def can_place_building_at(self, building, position):
        (x1, x2, y1, y2) = self.get_building_bounds_at_position(building, position)
        if (x1 < 0) or (x2 > MAP_SIZE_X) or (y1 < 0) or (y1 > MAP_SIZE_Y):  # don't place out of bounds
            return False

        can_place = True
        for x in range(x1, x2):
            for y in range(y1, y2):
                if self.map[x][y] is not None:
                    can_place = False
                    break
            if not can_place:
                break
        return can_place

    def spawn_headquaters(self):
        hq_player1 = buildings.Headquaters(self.get_next_building_id(), self.game.player1.player_id, (0, int(MAP_SIZE_Y/2-2)))
        self.buildings.append(hq_player1)
        logger.info("Spawning headquaters for player %s in map at %s", self.game.player1.name, hq_player1.position)
        hq_player2 = buildings.Headquaters(self.get_next_building_id(), self.game.player2.player_id, (MAP_SIZE_X-1, int(MAP_SIZE_Y/2-2)))
        self.buildings.append(hq_player2)
        logger.info("Spawning headquaters for player %s in map at %s", self.game.player2.name, hq_player2.position)

        self.place_building_in_map(hq_player1)
        self.place_building_in_map(hq_player2)

    def spawn_spawner(self, msg, player):
        (x, y) = msg["position"]
        kind = msg["kind"]
        owner = player.player_id
        spawner = buildings.Spawner(self.get_next_building_id(), owner, (x, y), kind)
        if self.can_place_building_at(spawner, (x, y)):
            logger.info("Spawning spawner of kind %d for player %s in map at (%d,%d)", kind, player.name, x, y)
            self.place_building_in_map(spawner)
            self.buildings.append(spawner)

    def spawn_trap(self, msg, player):
        (x, y) = msg["position"]
        kind = msg["kind"]
        owner = player.player_id
        trap = traps.lookup[kind](self.get_next_trap_id(), owner, (x, y))
        if self.can_place_building_at(trap, (x, y)):
            logger.info("Spawning trap of kind %d for player %s in map at (%d,%d)", kind, player.name, x, y)
            self.place_building_in_map(trap)
            self.traps.append(trap)

    def trigger_spawner(self, spawner, player):
        if not spawner.can_spawn():
            return
        spawner.reset_cooldown()
        mob_pos = spawner.position
        mob_pos[0] += player.direction
        for n in range(spawner.num_mobs):
            mob = units.lookup[spawner.mob_kind](self.get_next_unit_id(), player.player_id, mob_pos, [], player.direction)
            self.units.append(mob)

    # update game state
    def tick(self):
        the_actions = self.action_buffer.copy()
        self.action_buffer = []

        old_state = self.save_game_state()

        self.move_units()

        for (msg, player) in the_actions:
            action = msg["action"]
            if action == "place_spawner":
                self.spawn_spawner(msg, player)
            elif action == "place_trap":
                self.spawn_trap(msg, player)
            elif action == "trigger_spawner":
                (x, y) = msg["position"]
                spawner_id = msg["spawner_id"]
                if isinstance(self.map[x][y], buildings.Spawner) and (self.map[x][y].building_id == spawner_id):
                    self.trigger_spawner(self.map[x][y], player)
            else:
                logger.warning("Unknown action %s in action buffer, ignoring.", action)
                continue

        self.apply_field_effects()
        self.do_send_data(self.send_state_delta(old_state))

    # initial state
    def send_full_state(self):
        self.do_send_data({
            "action": "full_game_state",
            "size": [MAP_SIZE_X, MAP_SIZE_Y],
            "units": [unit.to_dict() for unit in self.units],
            "traps": [trap.to_dict() for trap in self.traps],
            "buildings": [building.to_dict() for building in self.buildings]
        })

    # changes after each tick
    def send_state_delta(self, old_state):
        changed_units = []
        changed_traps = []
        players = []

        previous_state_units = old_state["units"]
        old_units_id_max = 0
        for old_unit in previous_state_units:
            if old_unit.unit_id > old_units_id_max:
                old_units_id_max = previous_state_units.unit_id

        unit_to_id = lambda unit: unit.unit_id
        current_state_unit_ids = map(unit_to_id, self.units)
        previous_state_unit_ids = map(unit_to_id, previous_state_units)
        new_units = list(filter(lambda unit: unit.unit_id not in previous_state_unit_ids, self.units))
        deleted_units = list(filter(lambda unit: unit.unit_id not in current_state_unit_ids, previous_state_units))

        for unit in self.units:
            unit_id = unit.unit_id
            old_unit = [unit for unit in previous_state_units if unit.unit_id == unit_id]
            if len(old_unit) == 1:
                old_unit = old_unit[0]
                if not unit.equals(old_unit):
                    changed_units.append(unit)

        previous_state_traps = old_state["traps"]
        trap_to_id = lambda trap: trap.trap_id
        current_trap_ids = map(trap_to_id, self.traps)
        previous_state_trap_ids = map(trap_to_id, previous_state_traps)
        new_traps = list(filter(lambda trap: trap.trap_id not in previous_state_trap_ids, self.traps))
        deleted_traps = list(filter(lambda trap: trap.trap_id not in current_trap_ids, previous_state_traps))

        new_trap_ids = map(trap_to_id, new_traps)
        deleted_trap_ids = map(trap_to_id, deleted_traps)
        candidate_trap_filter = lambda trap: (trap.trap_id not in new_trap_ids) or (trap.trap_id not in deleted_trap_ids)
        candidate_traps = list(filter(candidate_trap_filter, self.traps))

        for trap in candidate_traps:
            trap_id = trap.trap_id
            old_trap = [trap for trap in previous_state_traps if trap.trap_id == trap_id]
            if len(old_trap) == 1:
                old_trap = old_trap[0]
                if not trap.equals(old_trap):
                    changed_traps.append(trap)
            else:
                logger.debug("More than one trap with the same id found. Wat. (%s)", old_trap)

        old_buildings = old_state["buildings"]
        old_building_id_max = 0
        for old_building in old_buildings:
            if old_building.building_id > old_building_id_max:
                old_building_id_max = old_building.building_id

        new_buildings = [building for building in self.buildings if building.building_id > old_building_id_max]

        (hp, money) = old_state["players"]["player1"]
        if (hp != self.game.player1.health_points) or (money != self.game.player1.money):
            players.append(self.game.player1)

        (hp, money) = old_state["players"]["player2"]
        if (hp != self.game.player2.health_points) or (money != self.game.player2.money):
            players.append(self.game.player2)

        return {
            "action": "changed_game_state",
            "changed_units": [unit.to_dict() for unit in changed_units],
            "deleted_units": [unit.to_dict() for unit in deleted_units],
            "new_units": [unit.to_dict() for unit in new_units],
            "changed_traps": [unit.to_dict() for unit in changed_traps],
            "deleted_traps": [unit.to_dict() for unit in deleted_traps],
            "new_traps": [trap.to_dict() for trap in new_traps],
            "new_buildings": [unit.to_dict() for unit in new_buildings],
            "changed_players": [player.to_dict() for player in players]
        }

    def handle_message(self, msg, player):
        ok_actions = ["place_spawner", "place_trap", "trigger_spawner"]
        action = msg["action"]
        logger.debug("Handeling message with action %s for player %s ", action, player.name)
        ok = action in ok_actions

        if ok:
            logger.debug("Placing message from player %s in buffer for next tick", player.name)
            self.action_buffer.append((msg, player))
        else:
            logger.info("Unknown action %s from player %s", action, player.name)
        return ok

    def get_next_unit_id(self):
        tmp = self.unit_id_counter
        self.unit_id_counter += 1
        return tmp

    def get_next_trap_id(self):
        tmp = self.trap_id_counter
        self.trap_id_counter += 1
        return tmp

    def get_next_building_id(self):
        tmp = self.building_id_counter
        self.building_id_counter += 1
        return tmp

    def save_game_state(self):
        money1 = self.game.player1.money
        hp1 = self.game.player1.health_points
        money2 = self.game.player2.money
        hp2 = self.game.player2.health_points
        return {
            "units": [unit.copy() for unit in self.units],
            "traps": [trap.copy() for trap in self.traps],
            "buildings": [building.copy() for building in self.buildings],
            "players": {"player1": (hp1, money1), "player2": (hp2, money2)}
        }

    def do_send_data(self, data):
        json_str = json.dumps(data)
        asyncio.async(self.game.player1.socket.send(json_str))
        asyncio.async(self.game.player2.socket.send(json_str))

    def get_player_by_id(self, player_id):
        if self.game.player1.player_id == player_id:
            return self.game.player1
        elif self.game.player2.player_id == player_id:
            return self.game.player2
        else:
            logger.error("Trying to get unknown player by id %s", player_id)

    def move_units(self):
        for unit in self.units:
            if unit.may_move():
                (x, y) = unit.get_next_position()
                # (ox, oy) = unit.position
                if (1 <= x < MAP_SIZE_X-1) and (0 <= y < MAP_SIZE_Y):
                    unit.set_new_position([x, y])
                if y == -1:
                    y += MAP_SIZE_Y
                    unit.set_new_position([x, y])
                elif y == MAP_SIZE_Y:
                    y -= MAP_SIZE_Y
                    unit.set_new_position([x, y])

    def apply_field_effects(self):
        for unit in self.units:
            (x, y) = unit.position
            if (unit.player == self.game.player1.player_id) and (x == MAP_SIZE_X-2):
                self.game.player2.add_money(unit.bounty)
                self.game.player2.lose_health_points()
                self.units.remove(unit)
            elif (unit.player == self.game.player2.player_id) and (x == 1):
                self.game.player1.add_money(unit.bounty)
                self.game.player1.lose_health_points()
                self.units.remove(unit)
            else:
                trap = self.map[x][y]
                if (trap is not None) and (trap.owner != unit.owner):
                    trap.handleUnit(unit, self.get_player_by_id(unit.owner))
                    if unit.hp <= 0:
                        self.units.remove(unit)
                    if trap.has_durability and trap.durability <= 0:
                        self.traps.remove(trap)
                        self.map[x][y] = None
                    elif isinstance(trap, traps.PitfallTrap) and (trap.mobs_in_trap == trap.capacity):
                        self.traps.remove(trap)
                        self.map[x][y] = None
