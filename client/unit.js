
function Unit(player, pos, kind, upgrades, health, bounty, trapwear) {
    this.player = player;
    this.position = pos;
    this.kind = kind;
    this.upgrades = upgrades;
    this.health = health;
    this.bounty = bounty;
    this.trapwear = trapwear;
}

function UnitKindImage(imgloader, kind) {
    return imgloader.get("tile-red");
}
