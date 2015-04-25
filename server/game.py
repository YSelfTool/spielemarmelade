import json
import asyncio
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

import buildings

MAP_SIZE_X = 64
MAP_SIZE_Y = 32


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
        self.action_buffer = []
        self.spawn_headquaters()

    def get_building_bounds(self, building):
        building_x_start = building.position[0]
        building_x_stop = building_x_start+building.size[0]
        building_y_start = building.position[1]
        building_y_stop = building_y_start+building.size[1]

        return building_x_start, building_x_stop, building_y_start, building_y_stop

    def get_building_bounds_at_position(self, building, position):
        building_x_start = position[0]
        building_x_stop = building_x_start+building.size[0]
        building_y_start = position[1]
        building_y_stop = building_y_start+building.size[1]

        return building_x_start, building_x_stop, building_y_start, building_y_stop

    def place_building_in_map(self, building):
        (x1, x2, y1, y2) = self.get_building_bounds(building)

        for x in range(x1, x2):
            for y in range(y1, y2):
                self.map[x][y] = building

    def can_place_building_at(self, building, position):
        (x1, x2, y1, y2) = self.get_building_bounds_at_position(building, position)

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
        hq_player1 = buildings.Headquaters(self.game.player1.player_id, (0, int(MAP_SIZE_Y/2-2)))
        self.buildings.append(hq_player1)
        hq_player2 = buildings.Headquaters(self.game.player2.player_id, (MAP_SIZE_X-1, int(MAP_SIZE_Y/2-2)))
        self.buildings.append(hq_player2)

        self.place_building_in_map(hq_player1)
        self.place_building_in_map(hq_player2)

    def spawn_spawner(self, msg, player):
        (x, y) = msg["position"]
        kind = msg["kind"]
        owner = player.player_id
        spawner = buildings.Spawner(owner, (x, y), kind)
        if self.can_place_building_at(spawner, (x, y)):
            logger.debug("Spawning spawner of kind %d for player %s in map at (%d,%d)", kind, player.name, x, y)
            self.place_building_in_map(spawner)
            self.buildings.append(spawner)

    # after each round
    def tick(self):
        old_state = self.save_game_state()
        the_actions = self.action_buffer.copy()
        self.action_buffer = []

        for (msg, player) in the_actions:
            action = msg["action"]
            if action == "place_spawner":
                self.spawn_spawner(msg, player)
            else:
                logger.warning("Unknown action %s in action buffer, ignoring.", action)
                continue

        self.send_state_delta()

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
    def send_state_delta(self):
        pass

    def handle_message(self, msg, player):
        ok = False
        action = msg["action"]
        logger.debug("Handeling message with action %s for player %s ", action, player.name)
        if action == "place_spawner":
            ok = True

        if ok:
            logger.debug("Placing message from player %s in buffer for next tick", player.name)
            self.action_buffer.append((msg, player))
        return ok


    def get_next_unit_id(self):
        tmp = self.unit_id_counter
        self.unit_id_counter += 1
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
