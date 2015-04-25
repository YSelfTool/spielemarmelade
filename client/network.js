
function Network(endpoint, executors) {
    this.endpoint = endpoint;
    executors["set_token"] = this.handleSetToken;
    executors.network = this;
    this.executors = executors;
    this.buffer = [];
    this.state = false;
    this.token = "";
}
Network.prototype.connect = function() {
    this.socket = new WebSocket(this.endpoint);
    this.socket.network = this;
    this.socket.onopen = function(e) {
        console.log("Connection open");
        this.network.state = true;
        while (this.network.buffer.length > 0) {
            this.network.send(this.network.buffer[0]);
            this.network.buffer = this.network.buffer.slice(1);
        }
    };
    this.socket.onerror = function(e) {
        console.log(["error", e]);
    };
    this.socket.onclose = function(e) {
        this.state = false;
        console.log(["close", e]);
        console.log("Connection closed");
    };
    this.socket.onmessage = function(e) {
        this.network.parse(e.data);
    };
};
Network.prototype.send = function(data) {
    if (this.state) {
        console.log(data);
        this.socket.send(JSON.stringify(data));
    } else {
        this.buffer.push(data);
    }
};
Network.prototype.parse = function(message) {
    data = JSON.parse(message);
    console.log(data); 
    this.executors[data.action](data);
};

Network.prototype.handleSetToken = function(data) {
    this.network.token = data.token;
};

Network.prototype.fillMsg = function(action, data) {
    data.action = action;
    data.token = this.token;
};
Network.prototype.setName = function(name) {
    msg = { "nickname": name };
    this.fillMsg("set_name", msg)
    this.send(msg);
};
Network.prototype.quit = function() {
    msg = { };
    this.fillMsg("quit", msg)
    this.send(msg);
    this.socket.close();
};
Network.prototype.joinGame = function(name) {
    msg = { "game_name": name };
    this.fillMsg("join_game", msg);
    this.send(msg);
};
