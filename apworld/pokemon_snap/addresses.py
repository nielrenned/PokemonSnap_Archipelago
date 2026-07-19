"""Game memory addresses for the client, loaded from the ROM build's export.

`pokemonsnap.symbols.json` is emitted by the decomp build (tools/export_symbols.py)
and copied here, so the addresses stay in sync with the ROM.
"""
import json
from importlib.resources import files

_data = json.loads(
    files(__package__).joinpath("data/pokemonsnap.symbols.json").read_text(encoding="utf-8")
)


def _addr(section: str, name: str) -> int:
    return int(_data[section][name]["addr"], 16)


def _ident(name: str):
    e = _data["idents"][name]
    return int(e["addr"], 16), int(e["rom_offset"], 16), e["len"]


# Expansion interface (volatile, written by the client to drive unlocks)
EXPANSION_MAGIC = _addr("symbols", "gExpansionMagic")
MAX_FILM = _addr("symbols", "gMaxFilm")
CAN_USE_OVERRIDE = _addr("symbols", "gCanUseOverride")
CAN_USE_MASK = _addr("symbols", "gCanUseMask")
COURSE_OVERRIDE = _addr("symbols", "gCourseOverride")
COURSE_UNLOCK_MASK = _addr("symbols", "gCourseUnlockMask")

# Vanilla save block (read-only)
SAVE_BASE = _addr("save", "saveBase")
RANK = _addr("save", "rank")
REPORT_SCORES = _addr("save", "reportScores")
SPECIES_SCORES = _addr("symbols", "speciesScores")

# Per-seed auth token: RAM addr (read), ROM offset (write), length.
AUTH_ADDR, AUTH_ROM, AUTH_LEN = _ident("auth")
UNPATCHED_AUTH = b"PSAP-UNPATCHED!!"

# gExpansionMagic reads as 'OKAY' once the expansion segment has booted.
EXPANSION_LOADED = 0x4F4B4159

# 63 snappable Pokemon; AP location id N maps to save slot (N - 1).
NUM_SPECIES = 63

# Photographing Mew (the last species) is the goal.
MEW_LOCATION = 63

# Item name -> bit in gCanUseMask.
CAN_USE_BITS = {
    "Apple": 0,
    "Pester Ball": 1,
    "Flute": 2,
    "Dash Engine": 3,
}

# Item name -> bit in gCourseUnlockMask. Note Cave/River are swapped relative to
# the apworld's sequential area codes, so this maps by name deliberately.
COURSE_BITS = {
    "Beach": 0,
    "Tunnel": 1,
    "Volcano": 2,
    "Cave": 3,
    "River": 4,
    "Valley": 5,
    "Rainbow Cloud": 6,
}

FILM_ITEM = "Film Capacity Upgrade"
FILM_BASE = 15
FILM_STEP = 5
FILM_CAP = 60
