
function spawnerNameByKind(kind) {
    switch(kind) {
        case UNIT_SOLDIER:
            return "SOLDIER";
        default:
            return "UNKNOWN";
    }
}

function unitInfoByKind(kind) {
    switch (kind) {
        case UNIT_SOLDIER:
            return "Der SOLDIER ist deine dämlichste, aber auch billigste Einheit.";
        default:
            return "Diese Einheit ist dem Informationssystem nicht bekannt.";
    }
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
