
function Unit(id, player, pos, kind, upgrades, health, bounty, trapwear) {
    this.id = id;
    this.player = player;
    this.position = pos;
    this.kind = kind;
    this.upgrades = upgrades;
    this.health = health;
    this.bounty = bounty;
    this.trapwear = trapwear;
}

function UnitKindImage(imgloader, kind) {
    return imgloader.get("unit-" + kind);
}
