
var imgloader;
var network;
var state = "";
var canvas, ctx;
var map;
var player;
var enemy;


function draw() {
    if (state == "running")
        requestAnimationFrame(draw);
    if (map) {
        map.draw(ctx, tileSize);
    }
};

function readFullGameState(data) {
    console.log(data);
}

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

function startGame() {
    document.getElementById("lobby-div").style.display = "none";
    state = "running";
    draw();
}

function serverErrorHandler(data) {
    console.log(data.message);
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
            document.getElementById("lobby-message").innerHTML = "Ein Spiel mit dem Namen läuft bereits.";
            state = "loggedin";
        }
    }
}

function setPlayerIdHandler(data) {
    player.id = data.id;
}

function startGameHandler(data) {
    enemy = new Player(data["enemy"][0], data["enemy"][1]);
}

function gameQueuedHandler(data) {
    if (state == "lobby") {
        state = "queued";
        document.getElementById("lobby-message").innerHTML = "Warte auf Mitspieler für Spiel " + data.game_name;
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
            "full_game_state": readFullGameState, 
            "error": serverErrorHandler,
            "set_player_id": setPlayerIdHandler,
            "game_queued": gameQueuedHandler
        };
    // ws://134.61.40.201:8765/game
    network = new Network("ws://134.61.40.201:8765/game", "trapstrat", executors);
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
