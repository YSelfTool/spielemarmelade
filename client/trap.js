
function Trap(id, img, player, pos, kind, upgrades) {
    this.id = id;
    this.img = img;
    this.player = player;
    this.pos = new Position(pos[0], pos[1]);
    this.kind = kind;
    this.upgrades = upgrades;
}

function TrapImage(imgloader, trap) {
    return imgloader.get("tile-blue");
}
