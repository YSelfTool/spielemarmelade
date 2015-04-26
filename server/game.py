import json
import random
import asyncio
import copy
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import buildings
import traps
import units
import game_object

MAP_SIZE_X = 32
MAP_SIZE_Y = 16
GAME_SPEED = 1 / 8
PLACEMENT_RADIUS_IN_TILES = 2


class Game(object):
    def __init__(self, name):
        self.name = name
        self.player1 = None
        self.player2 = None
        self.running = False
        self.state = None
        self.winner = None
        self.loser = None


def get_new_changed_deleted(current, previous, id_lambda):
    current_state_ids = list(map(id_lambda, current))
    previous_state_ids = list(map(id_lambda, previous))
    new_things = list(filter(lambda thing: id_lambda(thing) not in previous_state_ids, current))
    deleted_things = list(filter(lambda thing: id_lambda(thing) not in current_state_ids, previous))

    changed_things = []
    for thing in current:
        thing_id = id_lambda(thing)
        old_thing = [thing for thing in previous if id_lambda(thing) == thing_id]
        if len(old_thing) == 1:
            old_thing = old_thing[0]
            if not thing.equals(old_thing):
                changed_things.append(thing)

    return new_things, changed_things, deleted_things


def get_placeable_bounds(placeable):
    placeable_x_start = placeable.position[0]
    placeable_y_start = placeable.position[1]
    placeable_x_stop = placeable_x_start + placeable.size[0]
    placeable_y_stop = placeable_y_start + placeable.size[1]

    return placeable_x_start, placeable_x_stop, placeable_y_start, placeable_y_stop


def get_placeable_bounds_at_position(placeable, position):
    placeable_x_start = position[0]
    placeable_y_start = position[1]
    placeable_x_stop = placeable_x_start + placeable.size[0]
    placeable_y_stop = placeable_y_start + placeable.size[1]

    return placeable_x_start, placeable_x_stop, placeable_y_start, placeable_y_stop


class GameState(object):
    def __init__(self, the_game):
        self.game = the_game
        self.map = [[None for _ in range(MAP_SIZE_Y)] for _ in range(MAP_SIZE_X)]
        self.units = []
        self.traps = []
        self.buildings = []
        self.id_counter = 1
        self.action_buffer = []
        self.spawn_headquaters()

    def place_building_in_map(self, building):
        (x1, x2, y1, y2) = get_placeable_bounds(building)

        for x in range(x1, x2):
            for y in range(y1, y2):
                self.map[x][y] = building

    def can_place_building_at(self, building, position):
        logger.debug("Checking wether we can place a placeable at %s", position)
        (x1, x2, y1, y2) = get_placeable_bounds_at_position(building, position)
        if (x1 < 0) or (x2 > MAP_SIZE_X) or (y1 < 0) or (y1 > MAP_SIZE_Y):  # don't place out of bounds
            logger.debug("trying to place something out of bounds...")
            return False

        can_place = True
        for x in range(x1, x2):
            for y in range(y1, y2):
                if self.map[x][y] is not None:
                    can_place = False
                    break
            if not can_place:
                break

        logger.debug("We can place it? %s", can_place)
        return can_place

    def spawn_headquaters(self):
        hq_player1 = buildings.Headquaters(self.get_next_id(), self.game.player1.player_id, (0, int(MAP_SIZE_Y / 2 - 2)))
        self.buildings.append(hq_player1)
        logger.debug("Spawning headquaters for player %s in map at %s", self.game.player1.name, hq_player1.position)
        hq_player2 = buildings.Headquaters(self.get_next_id(), self.game.player2.player_id, (MAP_SIZE_X-1, int(MAP_SIZE_Y / 2 - 2)))
        self.buildings.append(hq_player2)
        logger.debug("Spawning headquaters for player %s in map at %s", self.game.player2.name, hq_player2.position)

        self.place_building_in_map(hq_player1)
        self.place_building_in_map(hq_player2)

    def spawn_spawner(self, msg, player):
        (x, y) = msg["position"]
        kind = msg["kind"]
        owner = player.player_id
        logger.debug("%s is trying to spawn spawner", player.name)
        spawner = buildings.Spawner(self.get_next_id(), owner, (x, y), kind, 1, 10)
        if self.can_place_building_at(spawner, (x, y)) and self.pay_for(player, spawner):
            logger.debug("Spawning spawner of kind %d for player %s in map at (%d,%d)", kind, player.name, x, y)
            self.place_building_in_map(spawner)
            self.buildings.append(spawner)

    def spawn_trap(self, msg, player):
        (x, y) = msg["position"]
        kind = msg["kind"]
        owner = player.player_id
        trap = traps.lookup[kind](self.get_next_id(), owner, (x, y))
        if self.can_place_building_at(trap, (x, y)) and self.pay_for(player, trap):
            logger.debug("Spawning trap of kind %d for player %s in map at (%d,%d)", kind, player.name, x, y)
            self.place_building_in_map(trap)
            self.traps.append(trap)

    def trigger_spawner(self, spawner, player):
        logger.debug("Player %s triggered a spawner for mob kind %d at %s", player.name, spawner.mob_kind, spawner.position)
        if not spawner.can_spawn():
            logger.debug("Spawner is still in cooldown. %d ticks left", spawner.current_cooldown)
            return
        spawner.reset_cooldown()
        mob_pos = [spawner.position[0], spawner.position[1]]
        mob_pos[0] += player.direction
        for n in range(spawner.num_mobs):
            mob = units.lookup[spawner.mob_kind](self.get_next_id(), player.player_id, mob_pos, [], player.direction)
            if self.pay_for(player, mob):
                self.units.append(mob)

    def pay_for(self, player, obj):
        if obj.__class__ in game_object.cost_lookup:
            _, _, cost = game_object.cost_lookup[obj.__class__]
            if player.money >= cost:
                player.add_money(-cost)
                return True
        return False

    # update game state
    def tick(self):
        the_actions = self.action_buffer.copy()
        self.action_buffer = []

        old_state = self.save_game_state()

        self.move_units()
        self.tick_buildings()

        for (msg, player) in the_actions:
            action = msg["action"]
            if action == "place_spawner":
                self.spawn_spawner(msg, player)
            elif action == "place_trap":
                self.spawn_trap(msg, player)
            elif action == "trigger_spawner":
                (x, y) = msg["position"]
                spawner_id = msg["spawner_id"]
                if isinstance(self.map[x][y], buildings.Spawner) and (self.map[x][y].object_id == spawner_id):
                    self.trigger_spawner(self.map[x][y], player)
            else:
                logger.warning("Unknown action %s in action buffer, ignoring.", action)
                continue

        self.apply_field_effects()

        winners = []
        if self.game.player1.health_points == 0:
            winners.append(self.game.player2)
            self.game.winner = self.game.player2
            self.game.loser = self.game.player1
        if self.game.player2.health_points == 0:
            winners.append(self.game.player1)
            self.game.winner = self.game.player1
            self.game.loser = self.game.player2

        if len(winners) > 0:
            self.game.running = False
            if len(winners) == 2:
                if random.randint(0, 1) == 0:
                    self.game.winner = winners[0]
                    self.game.loser = winners[1]
                else:
                    self.game.winner = winners[1]
                    self.game.loser = winners[0]
        else:
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
        players = []

        new_units, changed_units, deleted_units = get_new_changed_deleted(self.units, old_state["units"], lambda u: u.object_id)
        new_traps, changed_traps, deleted_traps = get_new_changed_deleted(self.traps, old_state["traps"], lambda t: t.object_id)
        new_buildings, changed_buildings, deleted_buildings = get_new_changed_deleted(self.buildings, old_state["buildings"], lambda b: b.object_id)

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
            "changed_traps": [trap.to_dict() for trap in changed_traps],
            "deleted_traps": [trap.to_dict() for trap in deleted_traps],
            "new_traps": [trap.to_dict() for trap in new_traps],
            "new_buildings": [building.to_dict() for building in new_buildings],
            "changed_buildings": [building.to_dict() for building in changed_buildings],
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

    def get_next_id(self):
        tmp = self.id_counter
        self.id_counter += 1
        return tmp

    def save_game_state(self):
        money1 = self.game.player1.money
        hp1 = self.game.player1.health_points
        money2 = self.game.player2.money
        hp2 = self.game.player2.health_points
        return {
            "units": [copy.copy(unit) for unit in self.units],
            "traps": [copy.copy(trap) for trap in self.traps],
            "buildings": [copy.copy(building) for building in self.buildings],
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

    def tick_buildings(self):
        for building in self.buildings:
            building.tick(self.get_player_by_id(building.owner))

    def apply_field_effects(self):
        for unit in self.units:
            (x, y) = unit.position
            if (unit.owner == self.game.player1.player_id) and (x >= MAP_SIZE_X-2):
                self.game.player2.add_money(unit.bounty)
                self.game.player2.lose_health_points()
                self.units.remove(unit)
            elif (unit.owner == self.game.player2.player_id) and (x <= 1):
                self.game.player1.add_money(unit.bounty)
                self.game.player1.lose_health_points()
                self.units.remove(unit)
            else:
                trap = self.map[x][y]
                if (trap is not None) and (trap.owner != unit.owner):
                    trap.handle_unit(unit, self.get_player_by_id(unit.owner))
                    if unit.hp <= 0:
                        self.units.remove(unit)
                    if trap.has_durability and trap.durability <= 0:
                        self.traps.remove(trap)
                        self.map[x][y] = None
                    elif isinstance(trap, traps.PitfallTrap) and (trap.mobs_in_trap == trap.capacity):
                        self.traps.remove(trap)
                        self.map[x][y] = None
