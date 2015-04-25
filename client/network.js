
function Network(endpoint, protocol, executors) {
    this.endpoint = endpoint;
    this.protocol = protocol;
    this.executors = executors;
    this.buffer = [];
    this.status = false;
}
Network.prototype.connect = function() {
    this.socket = new WebSocket(this.endpoint, this.protocol);
    this.socket.network = this;
    this.socket.onopen = function(e) {
        console.log("Connection open");
        this.network.status = true;
        while (this.network.buffer.length > 0) {
            this.network.send(this.network.buffer[0]);
            this.network.buffer = this.network.buffer.slice(1);
        }
    };
    this.socket.onerror = function(e) {
        console.log(["error", e]);
    };
    this.socket.onclose = function(e) {
        console.log(["close", e]);
    };
    this.socket.onmessage = function(e) {
        console.log(e);
        //this.parse(event);
    };
};
Network.prototype.send = function(data) {
    if (this.status) {
        this.socket.send(JSON.stringify(data));
    } else {
        console.log(this);
        this.buffer.push(data);
    }
};
Network.prototype.parse = function(message) {
    data = JSON.parse(message);
    this.executors[data.action](data);
};
Network.prototype.setName = function(name) {
    msg = { "action": "set_name", "nickname": name };
    this.send(msg);
};
Network.prototype.quit = function() {
    msg = { "action": "quit" };
    this.send(msg);
    this.socket.close();
};
