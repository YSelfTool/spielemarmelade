
function Building(id, img, player, pos, size, kind) {
    this.id = id;
    this.img = img;
    this.player = player;
    this.position = new Position(pos[0], pos[1]);
    this.size = new Position(size[0], size[1]);
}

function BuildingImage(imgloader, building) {
    return imgloader.get("tile-yellow");
}