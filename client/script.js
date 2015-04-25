
var imgloader;
var network;



function draw() {

};

function readFullGameState(data) {
    console.log(data);
}

window.onload=function() {
    console.log("The game is on!");
    imgloader = new ImageLoader();
    preloadImages(imgloader);
    console.log("Loaded Images!");
    executors = 
        { 
            "full_game_state": readFullGameState 
        };
    network = new Network("ws://localhost:8765/a", "trapstrat", executors);
    network.connect();
    network.setName("tester");
};
