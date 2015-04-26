
var imgloader;
var network;
var state = "";
var canvas, ctx;
var map;
var player, enemy;
var tileSize = 32;
var currentlyBuilding = false;
var currentBuildingKind = 0;
var currentBuildingSpawnerKind = 0;
var currentTrapType = 0;
var buildingcache = [];
var cache;
var costs = {};

function draw() {
    if (state == "running")
        requestAnimationFrame(draw);
    if (map) {
        map.draw(ctx, tileSize, imgloader, player);
    }
    ctx.globalAlpha = 0.5;
    for (var i = 0; i < cache.buildingCache.length; i++) {
        var building = cache.buildingCache[i];
        building.draw(ctx, tileSize, imgloader);
    }
    for (var i = 0; i < cache.trapCache.length; i++) {
        var trap = cache.trapCache[i];
        trap.draw(ctx, tileSize, imgloader);
    }
};

function login() {
    name = document.getElementById("login-name").value;
    if (name.length > 0) {
        network.setName(name);
        document.getElementById("login-div").style.display = "none";
        player = new Player(0, name);
        state = "loggedin";
        document.getElementById("lobby-div").style.display = "block";
    }
}

function joinGame() {
    if (state == "loggedin") {
        gamename = document.getElementById("lobby-name").value;
        network.joinGame(gamename);
        document.getElementById("lobby-message").innerHTML = "Kommuniziere mit dem Server...";
        state = "lobby";
    }
}

function quit() {
    network.quit();
    state = "stopped";
}

function serverErrorHandler(data) {
    if (!data.can_continue) {
        quit();
    }
    if (data.error_code) {
        if (data.error_code == NICKNAME_ALREADY_IN_USE) {
            document.getElementById("login-message").innerHTML = data.message;
            document.getElementById("login-name").value = "";
            document.getElementById("login-div").style.display = "block";
            document.getElementById("lobby-div").style.display = "none";
            state = "starting";
        } else if (data.error_code == GAME_WITH_NAME_ALREADY_RUNNING) {
            document.getElementById("lobby-message").innerHTML = data.message;
            state = "loggedin";
        }
    }
}

function setPlayerIdHandler(data) {
    player.id = data.id;
}

function gameStartHandler(data) {
    if (state == "lobby" || state == "queued") {
        console.log(data);
        enemy = new Player(data["enemy"]["enemy_id"], data["enemy"]["enemy_name"], data["enemy"]["enemy_side"]);
        document.getElementById("lobby-div").style.display = "none";
        player.side = (enemy.side == "left" ? "right" : "left");
        state = "running";
        showMessage("Mögen die Spiele gegen " + enemy.name  + " beginnen.");
        draw();
    }
}

function gameQueuedHandler(data) {
    if (state == "lobby") {
        state = "queued";
        document.getElementById("lobby-message").innerHTML = "Warte auf Mitspieler für Spiel " + data.game_name;
    }
}

function fullGameStateHandler(data) {
    if (state == "running") {
        map = new Map(data.size, [], [], []);
        for (var i = 0; i < data.units.length; i++) {
            map.addUnit(data.units[1]);
        }
        for (var i = 0; i < data.traps.length; i++) {
            map.addTrap(data.traps[i]);
        }
        for (var i = 0; i < data.buildings.length; i++) {
            map.addBuilding(data.buildings[i]);
        }
        tileSize = canvas.width / map.size.x;
        console.log("Houston, we have a map!");
    }
}

function changedGameStateHandler(data) {
    cache.clear();
    if (state == "running") {
        for (var i = 0; i < data.new_units.length; i++) {
            map.addUnit(data.new_units[i]);
        }
        for (var i = 0; i < data.new_buildings.length; i++) {
            map.addBuilding(data.new_buildings[i]);
        }
        for (var i = 0; i < data.new_traps.length; i++) {
            map.addTrap(data.new_traps[i]);
        }
        var unitIdsToDelete = [];
        for (var i = 0; i < data.deleted_units.length; i++) {
            unitIdsToDelete.push(data.deleted_units[i].id);
        }
        map.removeUnits(unitIdsToDelete);
        var trapIdsToDelete = [];
        for (var i = 0; i < data.deleted_traps.length; i++) {
            trapIdsToDelete.push(data.deleted_traps[i].id);
        }
        map.removeTraps(trapIdsToDelete);
        for (var i = 0; i < data.changed_units.length; i++) {
            var u = data.changed_units[i];
            var unit = map.unitById(u.id);
            if (unit != null) {
                unit.kind = u.kind;
                unit.player = u.owner;
                unit.position = new Position(u.position[0], u.position[1]);
                unit.upgrades = u.upgrades;
                unit.health = u.hp;
                unit.bounty = u.bounty;
                unit.trapwear = u.wear;
            } else {
                console.log("Trying to change invalid unit!");
                console.log(u);
            }
        }
        for (var i = 0; i < data.changed_traps.length; i++) {
            var t = data.changed_traps[i];
            var trap = map.trapById(t.id);
            if (trap != null) {
                trap.kind = t.kind;
                trap.player = t.owner;
                trap.pos = new Position(t.position[0], t.position[1]);
                trap.upgrades = t.upgrades;
                trap.durability = t.durability;
            }
        }
        for (var i = 0; i < data.changed_buildings.length; i++) {
            var b = data.changed_buildings[i];
            var building = map.buildingById(b.id);
            if (building != null) {
                building.kind = b.kind;
                building.size = new Position(b.size[0], b.size[1]);
                building.player = b.owner;
                building.position = new Position(b.position[0], b.position[1]);
                building.upgrades = b.upgrades;
            }
        }
        for (var i = 0; i < data.changed_players.length; i++) {
            var p = data.changed_players[i];
            var pl = playerById(p.id);
            if (pl != null) {
                pl.hp = p.hp;
                pl.money = p.money;
                if (pl == player) {
                    showPlayerInfo(player);
                }
            }
        }
    }
}

function setCostListHandler(data) {
    costs = {};
    var d = data.data;
    console.log(d);
    for (var i = 0; i < d.length; i++) {
        var e = d[i];
        costs[e[0] + "-" + e[1]] = e[2];
    }
}

function placeSpawner(pos) {
    var kind = currentBuildingSpawnerKind;
    var b = map.buildingByPos(pos);
    if (b == null) {
        network.placeSpawner(pos, kind);
        cache.addBuilding(imgloader, BUILDING_SPAWNER, kind, pos, new Position(1, 1), player.id);
    } else {
        if (b.kind == BUILDING_SPAWNER) {
            triggerSpawner(b);
        }
    }
}

function placeTrap(pos) {
    var oldTrap = map.trapByPos(pos);
    if (oldTrap == null) {
        var kind = currentTrapType;
        network.placeTrap(pos, kind);
        cache.addTrap(imgloader, kind, pos, player.id);
    } else {
        showTrapInfo(oldTrap);
    }
}

function triggerSpawner(spawner) {
    network.triggerSpawner(spawner.id, spawner.position);
    showSpawnerInfo(spawner);
}

function canvasClickHandler(canvasPos) {
    if (state == "running") {
        var mapPos = canvasPos.div(tileSize).floor();
        if (currentlyBuilding == "building") {
            if (currentBuildingKind == BUILDING_SPAWNER && mapPos.x == player.spawnerLane()) {
                placeSpawner(mapPos);
            } else {
                var b = map.buildingByPos(mapPos);
                if (b != null) {
                    if (b.kind == BUILDING_SPAWNER) {
                        showSpawnerInfo(b);
                    }
                } else {
                    var t = map.trapByPos(mapPos);
                    if (t != null) {
                        showTrapInfo(t);   
                    }
                }
            }
        } else if (currentlyBuilding == "trap") {
            if (mapPos.x >= 2 && mapPos.x < map.size.x - 2)
                placeTrap(mapPos);
        } else {
            if (mapPos.x == player.spawnerLane()) {
                var b = map.buildingByPos(mapPos);
                if (b != null) {
                    triggerSpawner(b);
                }
            } else if (mapPos.x >= 2 && mapPos.x <= 61) {
                var t = map.trapByPos(mapPos);
                if (t != null) {
                    showTrapInfo(t);
                }
            }
        }
    }
}


window.onload=function() {
    state = "starting";
    console.log("The game is on!");
    imgloader = new ImageLoader();
    preloadImages(imgloader);
    console.log("Loaded Images!");
    executors = 
        { 
            "error": serverErrorHandler,
            "set_player_id": setPlayerIdHandler,
            "game_queued": gameQueuedHandler,
            "game_started": gameStartHandler,
            "full_game_state": fullGameStateHandler,
            "changed_game_state": changedGameStateHandler,
            "set_cost_table": setCostListHandler
        };
    network = new Network("ws://linewars.steckdo.se:8765/", executors);
    network.connect();
    setButtonAndReturnFunc(login, "login-button", "login-name");
    setButtonAndReturnFunc(joinGame, "lobby-button", "lobby-name");
    cache = new Cache();
    canvas = document.getElementById("canvas");
    canvas.onclick = function(e) {
        var rect = e.target.getBoundingClientRect();
        var pos = new Position(e.clientX - rect.x, e.clientY - rect.y);
        canvasClickHandler(pos);
    };
    ctx = canvas.getContext("2d");
    ctx.imageSmoothingEnabled = false;
    ctx.mozImageSmoothingEnabled = false;
    ctx.webkitImageSmoothingEnabled = false;
    map = undefined;
    document.getElementById("known-building-spawner-soldier").onclick = function(e) {
        spawnerBuildingClick(UNIT_SOLDIER);
    };
    document.getElementById("known-building-spawner-jumper").onclick = function(e) {
        spawnerBuildingClick(UNIT_JUMPER);
    };
    document.getElementById("known-building-spawner-runner").onclick = function(e) {
        spawnerBuildingClick(UNIT_RUNNER);
    };
    document.getElementById("known-building-spawner-tank").onclick = function(e) {
        spawnerBuildingClick(UNIT_TANK);
    };
    document.getElementById("known-building-spawner-crooked").onclick = function(e) {
        spawnerBuildingClick(UNIT_CROOKEDSOLDIER);
    };
    document.getElementById("known-building-spawner-topstep").onclick = function(e) {
        spawnerBuildingClick(UNIT_TOPSTEPSOLDIER);
    };
    document.getElementById("known-building-spawner-bottomstep").onclick = function(e) {
        spawnerBuildingClick(UNIT_BOTTOMSTEPSOLDIER);
    };
    document.getElementById("known-traps-pitfall").onclick = function(e) {
        trapBuildingClick(TRAP_PITFALL);
    }
    document.getElementById("known-traps-spike").onclick = function(e) {
        trapBuildingClick(TRAP_SPIKE);
    }
    document.getElementById("known-traps-catapult").onclick = function(e) {
        trapBuildingClick(TRAP_CATAPULT);
    }
    document.getElementById("known-traps-looting").onclick = function(e) {
        trapBuildingClick(TRAP_LOOT);
    }
    document.getElementById("known-building-cancel").onclick = function(e) {
        currentlyBuilding = null;
        showCancelInfo();
    }
};

window.onclose = quit;

function spawnerBuildingClick(unitKind) {
    currentBuildingKind = BUILDING_SPAWNER;
    currentBuildingSpawnerKind = unitKind;
    currentlyBuilding = "building";
    showSpawnerKindInfo(unitKind);
}

function trapBuildingClick(trapKind) {
    currentTrapType = trapKind;
    currentlyBuilding = "trap";
    showTrapKindInfo(trapKind);
}

function setButtonAndReturnFunc(func, buttonname, inputname) {
    document.getElementById(buttonname).onclick = func;
    document.getElementById(inputname).onkeypress = function(e) {
        if (e.keyCode == 13)
            func();
    };
}

function showMessage(msg) {
    document.getElementById("footer").style.color = "darkgreen";
    document.getElementById("footer").innerHTML = msg;
}

function showError(msg) {
    document.getElementById("footer").style.color = "darkred";
    document.getElementById("footer").innerHTML = msg;
}

function showInfo(title, content) {
    document.getElementById("infospace-title").innerHTML = title;
    document.getElementById("infospace-content").innerHTML = content;
}

function removeIdsFromArray(array, ids) {
    if (ids.length > 0) {
        var remids = [];
        for (var j = 0; j < array.length; j++) {
            if (ids.indexOf(array[j].id) != -1) {
                remids.push(j);
            }
        }
        for (var i = remids.length - 1; i >= 0; i--) {
            array.splice(remids[i], 1);
        }
    }
}

function playerById(id) {
    if (id == player.id)
        return player;
    return enemy;
}
