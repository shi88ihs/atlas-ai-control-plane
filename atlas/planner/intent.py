from enum import Enum

class Intent(Enum):
    STATUS = "status"
    DOCTOR = "doctor"
    BACKUP = "backup"
    REPORT = "report"
    GIT = "git"
    INVENTORY = "inventory"
    HEALTH = "health"
    STABILIZE = "stabilize"
    DIAGNOSE = "diagnose"
    RELEASE = "release"
    ONBOARD_DESKTOP = "onboard-desktop"
    UPDATE_MACHINE = "update-machine"
