
function Trap(img, player, pos, kind, upgrades, durability) {
    this.img = img;
    this.player = player;
    this.pos = pos;
    this.kind = kind;
    this.upgrades = upgrades;
    this.durability = durability;
}
Trap.prototype.draw = function(ctx, tileSize, imgloader) {
    ctx.drawImage(this.img, this.pos.x * tileSize, this.pos.y * tileSize);
};

function TrapImage(imgloader, kind) {
    if (kind == TRAP_SPIKE)
        return imgloader.get("spikes");
    if (kind == TRAP_PITFALL)
        return imgloader.get("pitfall");
    else 
        return imgloader.get("tile-blue");
}
