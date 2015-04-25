
var imgloader;
var network;
var state = "";
var canvas, ctx;
var map;
var player;
var enemy;
var tileSize = 16;


function draw() {
    if (state == "running")
        requestAnimationFrame(draw);
    if (map) {
        map.draw(ctx, tileSize, imgloader);
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
        enemy = new Player(data["enemy"][0], data["enemy"][1]);
        document.getElementById("lobby-div").style.display = "none";
        state = "running";
        showMessage("Mögen die Spiele beginnen.");
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
    console.log("handler runnning");
    console.log(state);
    if (state == "running") {
        var units = [];
        for (var i = 0; i < data.units.length; i++) {
            var u = data.units[i];
            units.push(new Unit(u.owner, new Position(u.position[0], u.position[1]), u.id, u.upgrades, u.hp, u.bounty, u.wear));
        }
        var traps = [];
        for (var i = 0; i < data.traps.length; i++) {
            var t = data.traps[i];
            traps.push(new Trap(TrapImage(imgloader, t.id), t.owner, new Position(t.position[0], t.position[1]), t.id, t.upgrades, t.durability));
        }
        var buildings = [];
        for (var i = 0; i < data.buildings.length; i++) {
            var b = data.buildings[i];
            buildings.push(new Building(BuildingImage(imgloader, b.id), b.owner, new Position(b.position[0], b.position[1]), b.size, b.upgrades));
        }
        map = new Map(data.size, units, traps, buildings);
        console.log("Houston, we have a map!");
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
            "full_game_state": fullGameStateHandler 
        };
    // ws://134.61.40.201:8765/game
    network = new Network("ws://134.61.40.201:8765/game", executors);
    //network = new Network("ws://localhost:8765/game", "trapstrat", executors);
    network.connect();
    setButtonAndReturnFunc(login, "login-button", "login-name");
    setButtonAndReturnFunc(joinGame, "lobby-button", "lobby-name");
    canvas = document.getElementById("canvas");
    ctx = canvas.getContext("2d");
    map = undefined;
};

window.onclose = quit;

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
