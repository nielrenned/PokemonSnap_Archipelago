import random
from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Item, MultiWorld


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
    "Beach", "Tunnel", "Volcano", "River", "Cave", "Valley", "Rainbow Cloud",
    "Apple", "Pester Ball", "Flute", "Dash Engine"
}

useful_item_names = {
    "Film Capacity Upgrade"
}

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    ("Apple", 1000, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Pester Ball", 1001, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Flute", 1002, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Dash Engine", 1003, PokemonSnapItemCategory.TOOL),  # 803AE51F

    ("Beach", 2000, PokemonSnapItemCategory.AREA),
    ("Tunnel", 2001, PokemonSnapItemCategory.AREA),
    ("Volcano", 2002, PokemonSnapItemCategory.AREA),
    ("River", 2003, PokemonSnapItemCategory.AREA),
    ("Cave", 2004, PokemonSnapItemCategory.AREA),
    ("Valley", 2005, PokemonSnapItemCategory.AREA),
    ("Rainbow Cloud", 2006, PokemonSnapItemCategory.AREA),

    # ("Point Modifier", 3000, PokemonSnapItemCategory.MISC),  # 81232E6A
    ("Film Capacity Upgrade", 3001, PokemonSnapItemCategory.MISC),  # 800AC0E3
    # ("Rapid Fire Upgrade", 3002, PokemonSnapItemCategory.MISC),  # 80382CB7

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH),
    ("A used reel of film", 4001, PokemonSnapItemCategory.TRASH),
    ("A reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH),
    ("A burger king voucher", 4005, PokemonSnapItemCategory.TRASH),
    ("A super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH),
]]

filler_items = {}

item_name_groups = {}

item_descriptions = {}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def build_item_pool(world) -> list[PokemonSnapItemData]:
    item_pool = []
    trash_items = [item for item in _all_items if item.category == PokemonSnapItemCategory.TRASH]

    item_pool.append(PokemonSnapItemData("Apple", 1000, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Pester Ball", 1001, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Flute", 1002, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Dash Engine", 1003, PokemonSnapItemCategory.TOOL))

    all_areas = [
        PokemonSnapItemData("Beach", 2000, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Tunnel", 2001, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Volcano", 2002, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("River", 2003, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Cave", 2004, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Valley", 2005, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Rainbow Cloud", 2006, PokemonSnapItemCategory.AREA)
    ]

    for area in all_areas:
        if area.name == world.start_area.name:
            continue
        else:
            item_pool.append(area)

    # Nine +5 film upgrades take the cap from 15 up to the max of 60.
    for _ in range(9):
        item_pool.append(PokemonSnapItemData("Film Capacity Upgrade", 3001, PokemonSnapItemCategory.MISC))

    for i in range(len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)):
        random_trash_item = random.choice(trash_items)
        item_pool.append(
            PokemonSnapItemData(random_trash_item.name, random_trash_item.ps_code, random_trash_item.category))

    random.shuffle(item_pool)
    return item_pool
