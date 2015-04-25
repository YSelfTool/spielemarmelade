
function Position(x, y) {
    this.x = x;
    this.y = y;
}
Position.prototype.add = function(pos) {
    return Position(this.x + pos.x, this.y + pos.y);
};
Position.prototype.sub = function(pos) {
    return Position(this.x - pos.x, this.y - pos.y);
};
Position.prototype.mul = function(ska) {
    return Position(this.x * ska, this.y * ska);
};
Position.prototype.div = function(ska) {
    return Position(this.x / ska, this.y / ska);
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
