
function Unit(id, img, player, pos, kind, upgrades, health, bounty, trapwear) {
    this.id = id;
    this.img = img;
    this.player = player;
    this.position = new Position(pos[0], pos[1]);
    this.kind = kind;
    this.upgrades = upgrades;
    this.health = health;
    this.bounty = bounty;
    this.trapwear = trapwear;
}

function UnitImage(imgloader, unit) {
    return imgloader.get("tile-red");
}
