
function Trap(id, img, player, pos, kind, upgrades, durability) {
    this.id = id;
    this.img = img;
    this.player = player;
    this.pos = pos;
    this.kind = kind;
    this.upgrades = upgrades;
    this.durability = durability;
}
Trap.prototype.draw = function(ctx, tileSize, imgloader, pl) {
    ctx.drawImage(this.img, this.pos.x * tileSize, this.pos.y * tileSize, tileSize, tileSize);
};

function TrapImage(imgloader, kind) {
    if (kind == TRAP_SPIKE)
        return imgloader.get("spikes");
    else if (kind == TRAP_PITFALL)
        return imgloader.get("pitfall");
    else if (kind == TRAP_CATAPULT)
        return imgloader.get("catapult");
    else if (kind == TRAP_LOOT)
        return imgloader.get("loot");
    else 
        return imgloader.get("tile-blue");
}
