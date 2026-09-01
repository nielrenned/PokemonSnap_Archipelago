import typing
from enum import StrEnum
from math import ceil
from typing import NamedTuple
from .constants import *
from .options import ScoringBonus

from BaseClasses import Item

if typing.TYPE_CHECKING:
    from worlds.pokemon_snap import PokemonSnapWorld


class PokemonSnapItemCategory(StrEnum):
    VICTORY = "Victory"
    TOOL = "Tools"
    SCORING_BONUS = "Score"
    AREA = "Courses"
    MISC = "Miscellaneous"
    POKEMON_PIC = "Pokemon Pictures"
    SIGN_PIC = "Sign Pictures"
    TRASH_CUSTOM = "Special Garbage"
    TRASH_PICTURE = "Garbage Photos"


class PokemonSnapItemData(NamedTuple):
    name: str
    ps_code: int
    category: PokemonSnapItemCategory


class PokemonSnapItem(Item):
    game: str = "Pokemon Snap"

    @staticmethod
    def get_name_to_id() -> dict:
        return {item_data.name: item_data.ps_code for item_data in _all_items}


base_key_item_names = {
    VICTORY_ITEM_NAME,
    LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD,
    POKEMON_FOOD, PESTER_BALL, POKEFLUTE, DASH_ENGINE, SIGN_DETECTOR,
    PROG_SCORING, WDFL_SCORING, MULT_SCORING
}

useful_item_names = {
    FILM_UPGRADE
}

pokemon_pics = [
    PokemonSnapItemData(f"Pokemon Picture: {name}", 5000 + i, PokemonSnapItemCategory.POKEMON_PIC)
    for i, name in enumerate(ALL_INGAME_POKEMON)
]
POKEMON_PIC_NAMES = {item.name for item in pokemon_pics}

sign_pics = [
    PokemonSnapItemData(f"Sign Picture: {name}", 6000 + i, PokemonSnapItemCategory.SIGN_PIC)
    for i, name in enumerate(ALL_SIGNS)
]
SIGN_PIC_NAMES = {item.name for item in sign_pics}

def key_item_names(world: "PokemonSnapWorld") -> list:
    key_item_names_list = base_key_item_names
    if world.options.goal_type == GOAL_SIGN_PICS:
        key_item_names_list |= SIGN_PIC_NAMES
    elif world.options.goal_type == GOAL_POKEMON_PICS:
        key_item_names_list |= POKEMON_PIC_NAMES

    return key_item_names_list

# We're doing this weirdness so that each adjective/pokemon combo has its own ID.
# This way, when a tracker connects, it knows exactly which trash item you got.
# This also removes the mismatched checksum warning from Universal Tracker.
trash_pokemon_pics = {
    pokemon_name: [
        PokemonSnapItemData(
            f"A {adjective} Photo of {pokemon_name}",
            10000 + i*len(TRASH_PIC_ADJECTIVES) + j, 
            PokemonSnapItemCategory.TRASH_PICTURE
        )
        for j, adjective in enumerate(TRASH_PIC_ADJECTIVES)
    ]
    for i, pokemon_name in enumerate(ORIGINAL_151)
    if pokemon_name not in ALL_INGAME_POKEMON
}

_all_items = [PokemonSnapItemData(row[0], row[1], row[2]) for row in [
    (VICTORY_ITEM_NAME, VICTORY_ITEM_ID, PokemonSnapItemCategory.VICTORY),

    (POKEMON_FOOD,  1000, PokemonSnapItemCategory.TOOL),
    (PESTER_BALL,   1001, PokemonSnapItemCategory.TOOL),
    (POKEFLUTE,     1002, PokemonSnapItemCategory.TOOL),
    (DASH_ENGINE,   1003, PokemonSnapItemCategory.TOOL),
    (SIGN_DETECTOR, 1004, PokemonSnapItemCategory.TOOL),

    (WDFL_SCORING,  1500, PokemonSnapItemCategory.SCORING_BONUS),
    (MULT_SCORING,  1501, PokemonSnapItemCategory.SCORING_BONUS),
    (PROG_SCORING,  1502, PokemonSnapItemCategory.SCORING_BONUS),

    (LVL_BEACH,   2000, PokemonSnapItemCategory.AREA),
    (LVL_TUNNEL,  2001, PokemonSnapItemCategory.AREA),
    (LVL_VOLCANO, 2002, PokemonSnapItemCategory.AREA),
    (LVL_RIVER,   2003, PokemonSnapItemCategory.AREA),
    (LVL_CAVE,    2004, PokemonSnapItemCategory.AREA),
    (LVL_VALLEY,  2005, PokemonSnapItemCategory.AREA),

    (FILM_UPGRADE, 3000, PokemonSnapItemCategory.MISC),

    ("ArsonAssassin's pokemon card collection", 4000, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A used reel of film", 4001, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A reminder to remove the lens cap", 4002, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Nothing, literally nothing at all", 4003, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("Several decades worth of nostalgia", 4004, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A burger king voucher", 4005, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A super close-up of a thumb", 4006, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A Futuristic Photo of Mareep", 4007, PokemonSnapItemCategory.TRASH_CUSTOM),
    ("A Full Art Swinub Card", 4008, PokemonSnapItemCategory.TRASH_CUSTOM),

]] + pokemon_pics + sign_pics + [pic for pics in trash_pokemon_pics.values() for pic in pics]

filler_item_names = [item.name for item in _all_items if item.category is PokemonSnapItemCategory.TRASH_CUSTOM]

item_dictionary = {item_data.name: item_data for item_data in _all_items}

def build_item_pool(world: "PokemonSnapWorld") -> list[PokemonSnapItemData]:
    item_pool = []

    def unfilled_count():
        return len(world.multiworld.get_unfilled_locations(world.player)) - len(item_pool)

    ## Add all the required items
    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.TOOL)
    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.AREA and item.name != world.start_area.name)
    item_pool.extend(item for item in _all_items if item.category is PokemonSnapItemCategory.SIGN_PIC)
    item_pool.extend(pokemon_pics)

    film_upgrade_count = (
        ceil((world.options.maximum_film - world.options.starting_film) / world.options.film_upgrade_amount) +
        world.options.extra_film_upgrades
    )
    item_pool.extend([item_dictionary[FILM_UPGRADE]] * film_upgrade_count)

    # Remove items depending on options
    if world.options.start_with_dash_engine: item_pool.remove(item_dictionary[DASH_ENGINE])
    if not world.options.pokemon_signs:      item_pool.remove(item_dictionary[SIGN_DETECTOR])

    if world.options.scoring_bonuses == ScoringBonus.option_separate:
        item_pool.extend([item_dictionary[WDFL_SCORING], item_dictionary[MULT_SCORING]])
    elif world.options.scoring_bonuses == ScoringBonus.option_progressive:
        item_pool.extend([item_dictionary[PROG_SCORING], item_dictionary[PROG_SCORING]])
    
    ## Fill with one of each custom trash item, then one of each trash pokemon pic, then random pokemon pics
    trash_items = [item for item in _all_items if item.category is PokemonSnapItemCategory.TRASH_CUSTOM]

    trash_pics = list(trash_pokemon_pics.values())
    while len(trash_items) < unfilled_count():
        for pictures in trash_pics:
            trash_items.append(world.random.choice(pictures))
        world.random.shuffle(trash_pics)
    item_pool.extend(trash_items[:unfilled_count()])

    world.random.shuffle(item_pool)
    return item_pool


item_name_groups: typing.Dict[str, typing.Set[str]] = {}
for item in _all_items:
    category = f"{item.category}"
    if category not in item_name_groups.keys():
        item_name_groups[category] = set()
    item_name_groups[category].add(item.name)

