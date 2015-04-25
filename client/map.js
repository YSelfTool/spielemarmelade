
function Map(size, units, traps, buildings) {
    this.size = new Position(size[0], size[1]);
    this.units = units;
    this.traps = traps;
    this.buildings = buildings;
    this.tileImg = new Image();
}

Map.prototype.setTileImg = function(imgloader) {
    this.tileImg = imgloader.get("tile-green");
};
Map.prototype.draw = function(ctx, tileSize) {
    for (var x = 0; x < this.size.x; x++) {
        for (var y = 0; y < this.size.y; y++) {
            ctx.drawImage(this.tileImg, x * tileSize, y * tileSize);
        }
    }
};
