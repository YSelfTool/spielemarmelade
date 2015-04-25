
function Building(img, player, pos, size, kind) {
    this.img = img;
    this.player = player;
    this.position = new Position(pos[0], pos[1]);
    this.size = new Position(size[0], size[1]);
}

function BuildingImage(imgloader, kind) {
    return imgloader.get("tile-yellow");
}
