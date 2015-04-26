
function Cache() {
    this.buildingCache = [];
    this.trapCache = [];
}
Cache.prototype.clear = function() {
    this.buildingCache = [];
    this.trapCache = [];
}
Cache.prototype.addBuilding = function(imgloader, kind, subkind, pos, size, player) {
    this.buildingCache.push(new Building(0, BuildingImage(imgloader, kind), player, pos, size, kind, subkind));
};
Cache.prototype.addTrap = function(imgloader, kind, pos, player) {
    this.trapCache.push(new Trap(0, TrapImage(imgloader, kind), player, pos, kind, [], 0));
}
