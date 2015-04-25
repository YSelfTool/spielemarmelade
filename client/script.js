
var imgloader;
var network;
var state = "";


function draw() {

};

function readFullGameState(data) {
    console.log(data);
}

function login() {
    name = document.getElementById("login-name").value;
    if (name.length > 0) {
        network.setName(name);
        document.getElementById("login-div").style.display = "none";
    }
    state = "loggedin";
}

function quit() {
    network.quit();
    state = "stopped";
}

function serverErrorHandler(data) {
    console.log(["Server sent error", data.message]);
    if (!data.can_continue) {
        quit();
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
            "error": serverErrorHandler
        };
    // ws://134.61.40.201:8765/game
    //network = new Network("ws://134.61.40.201:8765/game", "trapstrat", executors);
    network = new Network("ws://localhost:8765/game", "trapstrat", executors);
    network.connect();
    document.getElementById("login-button").onclick = login;
    document.getElementById("login-name").onkeypress = function(event) {
        if (event.keyCode == 13)
            login();
    }
    
    
};

window.onclose = quit;
