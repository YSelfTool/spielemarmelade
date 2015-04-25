
function Map(size, units, traps, buildings) {
    this.size = new Position(size[0], size[1]);
    this.units = units;
    this.traps = traps;
    this.buildings = buildings;
}

Map.prototype.draw = function(ctx, tileSize, imgloader) {
    for (var x = 0; x < this.size.x; x++) {
        for (var y = 0; y < this.size.y; y++) {
            ctx.drawImage(imgloader.get("tile-green"), x * tileSize, y * tileSize);
        }
    }
    for (var i = 0; i < this.buildings.length; i++) {
        var building = this.buildings[i];
        ctx.drawImage(building.img, building.position.x * tileSize, building.position.y * tileSize);
    }
    for (var i = 0; i < this.traps.length; i++) {
        var trap = this.traps[i];
        ctx.drawImage(trap.img, trap.position.x * tileSize, trap.position.y * tileSize);
    }
    for (var i = 0; i < this.size.x * this.size.y; i++) {
        this.hist[i] = 0;
    }
    var hists = new Array(UNIT_TYPE_COUNT);
    for (var i = 0; i < UNIT_TYPE_COUNT; i++) {
        hists[i] = new Uint16Array(this.size.x * this.size.y);
    }
    for (var i = 0; i < this.units.length; i++) {
        var unit = this.units[i];
        hists[unit.kind][unit.position.x + unit.position.y * this.size.x] += 1;
    }
    for (var x = 0; x < this.size.x; x++) {
        for (var y = 0; y < this.size.y; y++) { 
            var typecount = 0;
            var unitcount = 0;
            var existentkinds = [];
            var lastkind = 0;
            for (var i = 0; i < UNIT_TYPE_COUNT; i++) {
                var tileunitcount = hists[i][x + y * this.size.x] > 0;
                if (tileunitcount > 0) {
                    existentkinds.push(i);
                    typecount += 1;
                    lastkind = i;
                }
                unitcount += tileunitcount;
            }
            if (unitcount == 1) {
                ctx.drawImage(imgloader.get("unit-" + lastkind), x * tileSize, y * tileSize);
            } else {
                var insize = Math.ceil(Math.sqrt(typecount*2));
                var typeindex = 0;
                var locindex = 0;
                for (var lx = 0; lx < insize; lx++) {
                    for (var ly = 0; ly < insize; ly++) {
                        var locx = x * tileSize + lx * tileSize / insize;
                        var locy = y * tileSize + ly * tileSize / insize;
                        var locSize = tileSize / insize;
                        if (typeindex * 2 == locindex) {
                            ctx.drawImage(UnitKindImage(imgloader, existentkinds[typeindex]), locx, locy, locSize, locSize);
                        } else {
                            ctx.fillText(hists[existentkinds[typeindex]][x + y * this.size.x], locx, locy, locSize);
                            typeindex += 1;
                        }
                        locindex += 1;
                    }
                }
            }
        }
    }
};
