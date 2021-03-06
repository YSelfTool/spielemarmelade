
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
            this.network.buffer = this.network.buffer.splice(1);
        }
    };
    this.socket.onerror = function(e) {
        console.log(e);
    };
    this.socket.onclose = function(e) {
        this.state = false;
        console.log(e);
        console.log("Connection closed");
        alert("Spiel vorbei, Verbindung zu!");
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
    if (data.action in this.executors) {
        this.executors[data.action](data);
    } else {
        console.log("Unkown Package Incoming");
        console.log(data); 
    }
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
Network.prototype.placeSpawner = function(pos, kind) {
    msg = { "position": pos.toJSON(), "kind": kind };
    this.fillMsg("place_spawner", msg);
    this.send(msg);
}
Network.prototype.placeTrap = function(pos, kind) {
    msg = { "position": pos.toJSON(), "kind": kind };
    this.fillMsg("place_trap", msg);
    this.send(msg);
}
Network.prototype.triggerSpawner = function(id, pos) {
    msg = { "spawner_id": id, "position": pos.toJSON() };
    this.fillMsg("trigger_spawner", msg);
    this.send(msg);
}
