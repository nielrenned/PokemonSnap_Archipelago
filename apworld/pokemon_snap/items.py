import random
from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Item


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
    "Beach Unlocked", "Tunnel Unlocked", "Volcano Unlocked", "River Unlocked", "Cave Unlocked", "Valley Unlocked",
    "Rainbow Cloud Unlocked",
    "Apple Unlocked", "Pester Ball Unlocked", "Flute Unlocked"
}

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    ("Apple Unlocked", 1000, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Pester Ball Unlocked", 1001, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Flute Unlocked", 1002, PokemonSnapItemCategory.TOOL),  # 803AE51F
    ("Speed Boost Unlocked", 1003, PokemonSnapItemCategory.TOOL),  # 803AE51F

    ("Beach Unlocked", 2000, PokemonSnapItemCategory.AREA),
    ("Tunnel Unlocked", 2001, PokemonSnapItemCategory.AREA),
    ("Volcano Unlocked", 2002, PokemonSnapItemCategory.AREA),
    ("River Unlocked", 2003, PokemonSnapItemCategory.AREA),
    ("Cave Unlocked", 2004, PokemonSnapItemCategory.AREA),
    ("Valley Unlocked", 2005, PokemonSnapItemCategory.AREA),
    ("Rainbow Cloud Unlocked", 2006, PokemonSnapItemCategory.AREA),

    ("Point Modifier", 3000, PokemonSnapItemCategory.MISC),  # 81232E6A
    ("Film Capacity Upgrade", 3001, PokemonSnapItemCategory.MISC),  # 800AC0E3
    ("Rapid Fire Upgrade", 3002, PokemonSnapItemCategory.MISC),  # 80382CB7

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH),
    ("A used reel of film", 4001, PokemonSnapItemCategory.TRASH),
    ("A reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH),
    ("A burger king voucher", 4005, PokemonSnapItemCategory.TRASH),
    ("A super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH),
]]

item_descriptions = {
}

item_dictionary = {item_data.name: item_data for item_data in _all_items}


def build_item_pool(count, start_area) -> list[PokemonSnapItemData]:
    item_pool = []
    trash_items = [item for item in _all_items if item.category == PokemonSnapItemCategory.TRASH]

    remaining_count = count
    item_pool.append(PokemonSnapItemData("Apple Unlocked", 1000, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Pester Ball Unlocked", 1001, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Flute Unlocked", 1002, PokemonSnapItemCategory.TOOL))
    item_pool.append(PokemonSnapItemData("Speed Boost Unlocked", 1003, PokemonSnapItemCategory.TOOL))
    remaining_count = remaining_count - 4
    start_areas = [
        PokemonSnapItemData("Beach Unlocked", 2000, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Tunnel Unlocked", 2001, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Volcano Unlocked", 2002, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("River Unlocked", 2003, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Cave Unlocked", 2004, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Valley Unlocked", 2005, PokemonSnapItemCategory.AREA),
        PokemonSnapItemData("Rainbow Cloud Unlocked", 2006, PokemonSnapItemCategory.AREA)
    ]
    for area in start_areas:
        if area.name == start_area.name:
            continue
        else:
            item_pool.append(area)
    remaining_count = remaining_count - 6

    item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
    item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
    item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
    item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
    item_pool.append(PokemonSnapItemData("Point Modifier", 3000, PokemonSnapItemCategory.MISC))
    remaining_count = remaining_count - 5

    for i in range(remaining_count):
        random_trash_item = random.choice(trash_items)
        item_pool.append(
            PokemonSnapItemData(random_trash_item.name, random_trash_item.ps_code, random_trash_item.category))

    random.shuffle(item_pool)
    return item_pool
