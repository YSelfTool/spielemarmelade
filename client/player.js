
function Player(id, name, side, hp, money) {
    this.id = id;
    this.name = name;
    this.side = side;
    this.hp = hp;
    this.money = money;
}
Player.prototype.spawnerLane = function() {
    return this.side == "left" ? 1 : map.size.x - 2;
};


