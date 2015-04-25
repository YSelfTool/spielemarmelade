
function Building(img, player, pos, size, kind) {
    this.img = img;
    this.player = player;
    this.position = pos;
    this.size = size;
}

function BuildingImage(imgloader, kind) {
    if (kind == BUILDING_CASTLE)
        return imgloader.get("castle");
    else
        return imgloader.get("tile-yellow");
}
