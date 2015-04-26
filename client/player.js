
function Player(id, name, side) {
    this.id = id;
    this.name = name;
    this.side = side;
}
Player.prototype.spawnerLane = function() {
    return this.side == "left" ? 1 : map.size.x - 2;
};


