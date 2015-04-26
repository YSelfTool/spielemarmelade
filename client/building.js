
function Building(id, img, player, pos, size, kind, subkind) {
    this.id = id;
    this.img = img;
    this.player = player;
    this.position = pos;
    this.size = size;
    this.kind = kind;
    this.subkind = subkind;
}
Building.prototype.draw = function(ctx, tileSize, imgloader) {
    ctx.drawImage(this.img, this.position.x * tileSize, this.position.y * tileSize, tileSize * this.size.x, tileSize * this.size.y);
};

function BuildingImage(imgloader, kind) {
    if (kind == BUILDING_CASTLE)
        return imgloader.get("castle");
    else if (kind == BUILDING_SPAWNER)
        return imgloader.get("spawner");
    else
        return imgloader.get("tile-yellow");
}
