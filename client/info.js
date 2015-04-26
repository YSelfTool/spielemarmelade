
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
    return s;
}

function showSpawnerInfo(kind) {
    showInfo("Spawner: " + spawnerNameByKind(kind), 
        "Spawner schicken Einheiten für dich los, wenn du sie anklickst. " + unitInfoByKind(kind));
}

function showTrapInfo(kind) {
    
}

function showCancelInfo() {
    showInfo("", "");
}

function showPlayerInfo(player) {
    var div = document.getElementById("infospace-player");
    div.innerHTML = "Name: " + player.id + "<br>" + 
        "Seite: " + (player.side == "left" ? "links" : "rechts") + "<br>" + 
        "Lebenspunkte: " + player.hp + "<br>" + 
        "Guthaben: " + player.money;
}
