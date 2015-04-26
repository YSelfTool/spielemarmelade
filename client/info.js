
function spawnerNameByKind(kind) {
    switch(kind) {
        case UNIT_SOLDIER:
            return "SOLDIER";
        case UNIT_JUMPER:
            return "JUMPER";
        case UNIT_RUNNER:
            return "RUNNER";
        case UNIT_TANK:
            return "TANK";
        case UNIT_CROOKEDSOLDIER:
            return "CROOKEDSOLDIER";
        case UNIT_TOPSTEPSOLDIER:
            return "TOPSTEPSOLDIER";
        case UNIT_BOTTOMSTEPSOLDIER:
            return "BOTTOMSTEPSOLDIER";
        default:
            return "UNKNOWN";
    }
}

function unitInfoByKind(kind) {
    var s = "Der " + spawnerNameByKind(kind) + " ";
    switch (kind) {
        case UNIT_SOLDIER:
            s += "deine dämlichste, aber auch billigste Einheit.";
            break;
        case UNIT_JUMPER:
            s += "springt mehrere Felder auf einmal weit.";
            break;
        case UNIT_RUNNER:
            s += "ist besonders schnell.";
            break;
        case UNIT_TANK:
            s += "hat besonders viel Leben und verursacht mehr Schaden.";
            break;
        case UNIT_CROOKEDSOLDIER:
            s += "läuft diagonal.";
            break;
        case UNIT_TOPSTEPSOLDIER:
            s += "läuft regelmäßig einen Block nach oben.";
            break;
        case UNIT_BOTTOMSTEPSOLDIER:
            s += "läuft regelmäßig einen Block nach unten.";
            break;
        default:
            s += "ist dem Informationssystem nicht bekannt.";
            break;
    }
    s += "<br>";
    s += "Kosten: " + costs["unit-" + kind];
    return s;
}

function spawnerKindInfo(kind) {
    return "Spawner schicken Einheiten für dich los, wenn du sie anklickst. " + unitInfoByKind(kind);
}

function showSpawnerKindInfo(kind) {
    showInfo("Spawner: " + spawnerNameByKind(kind), spawnerKindInfo(kind));
}

function showSpawnerInfo(spawner) {
    s = spawnerKindInfo(spawner.kind);
    s += "<br>";
    s += "Besitzer: " + playerById(spawner.player).name + "<br>";
    showInfo("Spawner: " + spawnerNameByKind(spawner.kind), s);
}

function trapNameByKind(kind) {
    switch (kind) {
        case TRAP_PITFALL:
            return "PITFALL-TRAP";
        case TRAP_SPIKE:
            return "SPIKE-TRAP";
        case TRAP_CATAPULT:
            return "CATAPULT-TRAP";
        case TRAP_LOOT:
            return "LOOT-TRAP";
        default:
            return "UNKNOWN-TRAP";
    }
}

function showTrapInfo(trap) {
    var s = trapKindInfo(trap.kind);
    s += "<br>";
    s += "Spieler: " + playerById(trap.player).name + "<br>";
    s += "Haltbarkeit: " + trap.durability;
    showInfo(trapNameByKind(trap.kind), s);
}

function showTrapKindInfo(kind) {
    showInfo(trapNameByKind(kind), trapKindInfo(kind));
}

function trapKindInfo(kind) {
    var s = "Fallen kämpfen für dich gegen gegnerische Einheiten. Die ";
    s += trapNameByKind(kind);
    switch (kind) {
        case TRAP_PITFALL:
            s += " töten alle Einheiten, die auf sie treten, instantan, wird aber voll.";
            break;
        case TRAP_SPIKE:
            s += " fügen Einheiten, die auf sie treten, Schaden zu.";
            break;
        case TRAP_CATAPULT:
            s += " werfen Einheiten, die auf sie treten, zurück und fügen ihnen wenig Schaden zu.";
            break;
        case TRAP_LOOT:
            s += " nehmen Einheiten, die auf sie treten, Ausrüstung ab und verkaufen diese, sodass du Geld bekommst.";
            break;
        default:
            s += " ist dem Informationssystem unbekannt.";
            break;
    }
    s += "<br>";
    s += "Kosten: " + costs["trap-" + kind];
    return s;
}

function showCancelInfo() {
    showInfo("", "");
}

function showPlayerInfo(player) {
    var div = document.getElementById("infospace-player");
    div.innerHTML = "Name: " + player.name + "<br>" + 
        "Seite: " + (player.side == "left" ? "links" : "rechts") + "<br>" + 
        "Lebenspunkte: " + player.hp + "<br>" + 
        "Guthaben: " + player.money;
}
