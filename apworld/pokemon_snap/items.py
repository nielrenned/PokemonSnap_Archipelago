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
    LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD,
    POKEMON_FOOD, PESTER_BALL, POKEFLUTE, DASH_ENGINE
}

useful_item_names = {
    FILM_UPGRADE
}

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    (POKEMON_FOOD, 1000, PokemonSnapItemCategory.TOOL),
    (PESTER_BALL,  1001, PokemonSnapItemCategory.TOOL),
    (POKEFLUTE,    1002, PokemonSnapItemCategory.TOOL),
    (DASH_ENGINE,  1003, PokemonSnapItemCategory.TOOL),

    (LVL_BEACH,   2000, PokemonSnapItemCategory.AREA),
    (LVL_TUNNEL,  2001, PokemonSnapItemCategory.AREA),
    (LVL_VOLCANO, 2002, PokemonSnapItemCategory.AREA),
    (LVL_RIVER,   2003, PokemonSnapItemCategory.AREA),
    (LVL_CAVE,    2004, PokemonSnapItemCategory.AREA),
    (LVL_VALLEY,  2005, PokemonSnapItemCategory.AREA),
    (LVL_CLOUD,   2006, PokemonSnapItemCategory.AREA),

    (FILM_UPGRADE, 3000, PokemonSnapItemCategory.MISC),

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH),
    ("A used reel of film", 4001, PokemonSnapItemCategory.TRASH),
    ("A reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH),
    ("A burger king voucher", 4005, PokemonSnapItemCategory.TRASH),
    ("A super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH),
    # TODO: More filler items
]]

filler_item_names = [item.name for item in _all_items if item.category is PokemonSnapItemCategory.TRASH]

item_name_groups = {}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def build_item_pool(world: "PokemonSnapWorld") -> list[PokemonSnapItemData]:
    item_pool = []

    trash_items = [item for item in _all_items if item.category is PokemonSnapItemCategory.TRASH]
    all_areas = [item for item in _all_items if item.category is PokemonSnapItemCategory.AREA]

    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.TOOL)

    for area in all_areas:
        if area.name == world.start_area.name:
            continue
        else:
            item_pool.append(area)

    # Nine +5 film upgrades take the cap from 15 up to the max of 60.
    for _ in range(9):
        item_pool.append(item_dictionary[FILM_UPGRADE])

    for i in range(len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)):
        random_trash_item = random.choice(trash_items)
        item_pool.append(random_trash_item)

    random.shuffle(item_pool)
    return item_pool
