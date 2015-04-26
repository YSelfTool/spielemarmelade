
function Map(size, units, traps, buildings) {
    this.size = new Position(size[0], size[1]);
    this.units = units;
    this.traps = traps;
    this.buildings = buildings;
    this.range = 2;
}

Map.prototype.draw = function(ctx, tileSize, imgloader) {
    var visible = new Uint8Array(this.size.x * this.size.y);
    for (var i = 0; i < this.buildings.length; i++) {
        var b = this.buildings[i];
        for (var x = b.position.x - this.range; x <= b.position.x + this.range; x++) {
            for (var y = b.position.y - this.range; y <= b.position.y + this.range; y++) {
                if (x >= 0 && x < this.size.x && y >= 0 && y < this.size.y) {
                    visible[x + this.size.x * y] = 1;
                }
            }
        }
    }
    for (var i = 0; i < this.traps.length; i++) {
        var t = this.traps[i];
        for (var x = t.pos.x - this.range; x <= t.pos.x + this.range; x++) {
            for (var y = t.pos.y - this.range; y <= t.pos.y + this.range; y++) {
                if (x >= 0 && x < this.size.x && y >= 0 && y < this.size.y) {
                    visible[x + this.size.x * y] = 1;
                }
            }
        }
    }
    for (var x = 2; x < this.size.x - 2; x++) {
        for (var y = 0; y < this.size.y; y++) {
            ctx.drawImage(imgloader.get("tile-grass"), x * tileSize, y * tileSize, tileSize, tileSize);
        }
    }
    for (var x = 0; x < 2; x++) {
        for (var y = 0; y < this.size.y; y++) {
            ctx.drawImage(imgloader.get("tile-ground"), x * tileSize, y * tileSize, tileSize, tileSize);
        }
    }
    for (var x = this.size.x - 2; x < this.size.x; x++) {
        for (var y = 0; y < this.size.y; y++) {
            ctx.drawImage(imgloader.get("tile-ground"), x * tileSize, y * tileSize, tileSize, tileSize);
        }
    }
    for (var i = 0; i < this.buildings.length; i++) {
        var building = this.buildings[i];
        if (visible[building.position.x + this.size.x * building.position.y] == 1) {
            building.draw(ctx, tileSize, imgloader);
        }
    }
    for (var i = 0; i < this.traps.length; i++) {
        var trap = this.traps[i];
        if (visible[trap.pos.x + this.size.x * trap.pos.y] == 1) {
            trap.draw(ctx, tileSize, imgloader);
        }
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
                ctx.drawImage(imgloader.get("unit-" + lastkind), x * tileSize, y * tileSize, tileSize, tileSize);
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
Map.prototype.addUnit = function(u) {
    this.units.push(new Unit(u.id, u.owner, new Position(u.position[0], u.position[1]), u.kind, u.upgrades, u.hp, u.bounty, u.wear));
};
Map.prototype.addBuilding = function(b) {
    this.buildings.push(new Building(b.id, BuildingImage(imgloader, b.kind), b.owner, new Position(b.position[0], b.position[1]), new Position(b.size[0], b.size[1]), b.kind, b.mob_kind));
};
Map.prototype.addTrap = function(t) {
    this.traps.push(new Trap(t.id, TrapImage(imgloader, t.kind), t.owner, new Position(t.position[0], t.position[1]), t.kind, t.upgrades, t.durability)); 
}
Map.prototype.removeUnits = function(ids) {
    if (ids.length > 0) {
        var remids = [];
        for (var j = 0; j < this.units.length; j++) {
            if (ids.indexOf(this.units[j].id) != -1) {
                remids.push(j);
            }
        }
        console.log(remids);
        for (var i = remids.length - 1; i >= 0; i--) {
            this.units.splice(remids[i], 1);
        }
    }
}
Map.prototype.removeTraps = function(ids) {
    if (ids.length > 0) {
        for (var j = 0; j < this.traps.length; j++) {
            if (this.traps[j].id in ids) {
                this.traps.splice(j--, 1);
            }
        }
    }
}
Map.prototype.removeBuildings = function(ids) {
    if (ids.length > 0) {
        for (var j = 0; j < this.buildings.length; j++) {
            if (this.buildings[j].id in ids) {
                this.buildings.splice(j--, 1);
            }
        }
    }
}
Map.prototype.buildingByPos = function(pos) {
    for (var i = 0; i < this.buildings.length; i++) {
        if (this.buildings[i].position.equals(pos)) {
            return this.buildings[i];
        }
    }
    return null;
}
