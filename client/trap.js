
function Trap(img, player, pos, kind, upgrades, durability) {
    this.img = img;
    this.player = player;
    this.pos = pos;
    this.kind = kind;
    this.upgrades = upgrades;
    this.durability = durability;
}

function TrapImage(imgloader, kind) {
    return imgloader.get("tile-blue");
}
