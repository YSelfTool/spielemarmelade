
function Position(x, y) {
    this.x = x;
    this.y = y;
}
Position.prototype.add = function(pos) {
    return new Position(this.x + pos.x, this.y + pos.y);
};
Position.prototype.sub = function(pos) {
    return new Position(this.x - pos.x, this.y - pos.y);
};
Position.prototype.mul = function(ska) {
    return new Position(this.x * ska, this.y * ska);
};
Position.prototype.div = function(ska) {
    return new Position(this.x / ska, this.y / ska);
};
Position.prototype.set = function(pos) {
    this.x = pos.x;
    this.y = pos.y;
};
Position.prototype.normsquare = function() {
    return this.x * this.x + this.y * this.y;
};
Position.prototype.norm = function() {
    return Math.sqrt(this.normsquare());
};
Position.prototype.round = function() {
    return new Position(Math.round(this.x), Math.round(this.y));
};
Position.prototype.floor = function() {
    return new Position(Math.floor(this.x), Math.floor(this.y));
};
Position.prototype.toJSON = function() {
    return [ this.x, this.y ];
};
Position.prototype.equals = function(pos) {
    return (this.x == pos.x) && (this.y == pos.y);
}
