import random
import typing
from enum import IntEnum
from typing import NamedTuple
from .constants import *

from BaseClasses import Item

if typing.TYPE_CHECKING:
    from worlds.pokemon_snap import PokemonSnapWorld


class PokemonSnapItemCategory(IntEnum):
    TOOL = 0
    AREA = 1,
    MISC = 2,
    SKIP = 3,
    EVENT = 4,
    TRASH = 5
    VICTORY = 6
    POKEMON_PIC = 7


class PokemonSnapItemData(NamedTuple):
    name: str
    ps_code: int
    category: PokemonSnapItemCategory


class PokemonSnapItem(Item):
    game: str = "Pokemon Snap"

    @staticmethod
    def get_name_to_id() -> dict:
        return {item_data.name: item_data.ps_code for item_data in _all_items}


key_item_names = {
    VICTORY_ITEM_NAME,
    LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD,
    POKEMON_FOOD, PESTER_BALL, POKEFLUTE, DASH_ENGINE, SIGN_DETECTOR
}

useful_item_names = {
    FILM_UPGRADE
}

pokemon_pics = [
    PokemonSnapItemData(f"A Picture of {name}", 5000 + i, PokemonSnapItemCategory.POKEMON_PIC)
    for i, name in enumerate(ALL_INGAME_POKEMON)
]

sign_pics = [
    PokemonSnapItemData(f"A Picture of {name}", 6000 + i, PokemonSnapItemCategory.MISC)
    for i, name in enumerate(ALL_SIGNS)
]
SIGN_PIC_NAMES = {item.name for item in sign_pics}
key_item_names |= SIGN_PIC_NAMES

trash_pokemon_pics = [
    PokemonSnapItemData(f"A {random.choice(TRASH_PIC_ADJECTIVES)} Picture of {pokemon_name}", 7000 + i, PokemonSnapItemCategory.TRASH)
    for i, pokemon_name in enumerate(ORIGINAL_151)
    if pokemon_name not in ALL_INGAME_POKEMON
]

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    (VICTORY_ITEM_NAME, VICTORY_ITEM_ID, PokemonSnapItemCategory.VICTORY),

    (POKEMON_FOOD,  1000, PokemonSnapItemCategory.TOOL),
    (PESTER_BALL,   1001, PokemonSnapItemCategory.TOOL),
    (POKEFLUTE,     1002, PokemonSnapItemCategory.TOOL),
    (DASH_ENGINE,   1003, PokemonSnapItemCategory.TOOL),
    (SIGN_DETECTOR, 1004, PokemonSnapItemCategory.TOOL),

    (LVL_BEACH,   2000, PokemonSnapItemCategory.AREA),
    (LVL_TUNNEL,  2001, PokemonSnapItemCategory.AREA),
    (LVL_VOLCANO, 2002, PokemonSnapItemCategory.AREA),
    (LVL_RIVER,   2003, PokemonSnapItemCategory.AREA),
    (LVL_CAVE,    2004, PokemonSnapItemCategory.AREA),
    (LVL_VALLEY,  2005, PokemonSnapItemCategory.AREA),

    (FILM_UPGRADE,     3000, PokemonSnapItemCategory.MISC),

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH),
    ("A used reel of film", 4001, PokemonSnapItemCategory.TRASH),
    ("A reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH),
    ("A burger king voucher", 4005, PokemonSnapItemCategory.TRASH),
    ("A super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH),
    ("A Futuristic Picture of Mareep", 4007, PokemonSnapItemCategory.TRASH),
    ("A Full Art Swinub Card", 4008, PokemonSnapItemCategory.TRASH),

]] + pokemon_pics + sign_pics + trash_pokemon_pics

filler_item_names = [item.name for item in _all_items if item.category is PokemonSnapItemCategory.TRASH]

item_name_groups = {}

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def build_item_pool(world: "PokemonSnapWorld") -> list[PokemonSnapItemData]:
    item_pool = []

    def unfilled_count():
        return len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)

    ## Add all the required items
    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.TOOL)
    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.AREA and item.name != world.start_area.name)
    item_pool.extend(pokemon_pics)
    item_pool.extend(sign_pics)

    # Nine +5 film upgrades take the cap from 15 up to the max of 60.
    item_pool.extend(item_dictionary[FILM_UPGRADE] for _ in range(9))
    
    ## Fill with one of each trash item, then random duplicate trash items
    trash_items = [item for item in _all_items if item.category is PokemonSnapItemCategory.TRASH]
    random.shuffle(trash_items)
    item_pool.extend(trash_items[:min(len(trash_items), unfilled_count())])
    item_pool.extend(random.choice(trash_items) for _ in range(unfilled_count()))

    random.shuffle(item_pool)
    return item_pool
