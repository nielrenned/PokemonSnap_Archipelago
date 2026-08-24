from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Location, Region
from .pokemon_rules import SPECIES_RULE_DATA
from .addresses import COURSE_IDS
from .items import PokemonSnapItem
from .constants import *

class PokemonSnapLocationCategory(IntEnum):
    NORMAL_PHOTO    = 0
    WONDERFUL_PHOTO = 1
    MULTIPLE_PHOTO  = 2
    SPECIAL_POSE    = 3
    POKEMON_SIGN    = 4
    SECRET_EXIT     = 5
    PHOTO_COUNT     = 6
    REPORT_SCORE    = 7

    # for when there aren't enough locations in the pool
    BONUS_LOCATION = 10


class PokemonSnapLocationData(NamedTuple):
    id: int
    name: str
    category: PokemonSnapLocationCategory


class PokemonSnapLocation(Location):
    game: str = "Pokemon Snap"
    category: PokemonSnapLocationCategory
    default_item_name: str

    def __init__(
            self,
            player: int,
            name: str,
            category: PokemonSnapLocationCategory,
            address: int | None = None,
            parent: Region | None = None):
        super().__init__(player, name, address, parent)
        self.category = category
        self.id = id

    @staticmethod
    def get_name_to_id() -> dict:
        table_offset = 1000

        table_order = [
            START_GAME, LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD
        ]

        output = {}
        for i, region_name in enumerate(table_order):
            if len(location_tables[region_name]) > table_offset:
                raise Exception("A location table has {} entries, that is more than {} entries (table #{})".format(
                    len(location_tables[region_name]), table_offset, i))
            output.update({location_data.name: location_data.id for location_data in location_tables[region_name]})
        return output

    def place_locked_item(self, item: PokemonSnapItem):
        self.item = item
        self.locked = True
        item.location = self


# Location naming functions
wonderful   = lambda name:         f'{name}: Good Technique'
multiple    = lambda name:         f'{name}: Multiple'
course      = lambda name, course: f'{name} ({course})'
secret_exit = lambda level_name:   f'{level_name}: Secret Exit'
bonus       = lambda loc_name:     f'{loc_name} 2'

# Alternate ID functions
wonderful_id    = lambda poke_id:  100 + poke_id
multiple_id     = lambda poke_id:  200 + poke_id
special_pose_id = lambda pose_id:  300 + pose_id
sign_id         = lambda lvl_id:   400 + lvl_id
secret_exit_id  = lambda lvl_id:   500 + lvl_id
oak_reward_id   = lambda reward:   600 + reward
bonus_id        = lambda loc_id:  1000 + loc_id


RNG_LOCATIONS = [
    # Volcano
    multiple(ARCANINE),
    # River
    multiple(CLOYSTER),
    multiple(PSYDUCK),
    # Valley
    multiple(DRATINI),
    multiple(course(MAGIKARP, LVL_VALLEY)),
]

HARD_LOCATIONS = [
    # River
    wonderful(course(PIKACHU, LVL_RIVER)),
    # Cave
    wonderful(course(MAGIKARP, LVL_CAVE)),
    multiple(course(ZUBAT, LVL_CAVE)),
    BALLOON_PIKACHU,
    FLYING_PIKACHU,
    # Valley
    multiple(STARYU),
    multiple(STARMIE),
    wonderful(GOLDEEN),
]


POKEMON_TO_SLOTS = {
    pokemon.name: [pokemon.loc_id]
    for species_data in SPECIES_RULE_DATA.values() 
    for pokemon in species_data 
    if pokemon.name in ALL_INGAME_POKEMON
} | {
    BULBASAUR: [1, 64],
    MAGIKARP: [51, 65, 66, 67, 68, 69],
    PIKACHU: [10, 70, 71, 72],
    ZUBAT: [15, 73]
}


location_tables = {
    START_GAME: [],
}

for region, species_data_list in SPECIES_RULE_DATA.items():
    location_data_list = []
    region_id = COURSE_IDS[region]
    for name, id, soft_logic, _ in species_data_list:
        location_data_list.append(PokemonSnapLocationData(id, name, PokemonSnapLocationCategory.NORMAL_PHOTO))
        if soft_logic.wonderful is not None:
            location_data_list.append(PokemonSnapLocationData(wonderful_id(id), wonderful(name), PokemonSnapLocationCategory.WONDERFUL_PHOTO))
        if soft_logic.multiple is not None:
            location_data_list.append(PokemonSnapLocationData(multiple_id(id), multiple(name), PokemonSnapLocationCategory.MULTIPLE_PHOTO))
    location_tables[region] = location_data_list


special_poses = {
    1:  SURFING_PIKACHU,
    2:  PIKACHU_ON_A_BALL,
    3:  BALLOON_PIKACHU,
    4:  SPEED_PIKACHU,
    5:  PIKACHU_ON_A_STUMP,
    6:  FLYING_PIKACHU,
    7:  GUST_USING_PIDGEY,
    8:  JIGGLYPUFF_ON_STAGE,
    9:  GRAVELERS_GROUP_DANCE,
    10: RARE_POKEMON_MEW,
    11: FIGHTING_MAGMAR,
    12: JIGGLYPUFF_TRIO,
}

pose_locations = {
    LVL_BEACH:   [1, 5, 7],
    LVL_TUNNEL:  [2],
    LVL_VOLCANO: [11],
    LVL_RIVER:   [4],
    LVL_CAVE:    [3, 6, 8, 12],
    LVL_VALLEY:  [9],
 
    # I don't think we want this? Or maybe it's the goal item eventually?
    # LVL_CLOUD:   [10]
}

# Add the poses
for region, pose_ids in pose_locations.items():
    location_data_list = location_tables[region]
    for pose_id in pose_ids:
        pose_name = special_poses[pose_id]
        location_data_list.append(PokemonSnapLocationData(special_pose_id(pose_id), pose_name, PokemonSnapLocationCategory.SPECIAL_POSE))


# Add the signs
for level, sign in zip([LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY], ALL_SIGNS):
    location_tables[level].append(PokemonSnapLocationData(sign_id(COURSE_IDS[level]), sign, PokemonSnapLocationCategory.POKEMON_SIGN))


# Add the secret exits
for level in [LVL_TUNNEL, LVL_RIVER, LVL_VALLEY]:
    id = secret_exit_id(COURSE_IDS[level])
    name = secret_exit(level)
    location_tables[level].append(PokemonSnapLocationData(id, name, PokemonSnapLocationCategory.SECRET_EXIT))


OAK_SCORE_REWARDS = {
    REPORT_SCORE_24_000:  1, # Normally unlocks Pokemon Food
    REPORT_SCORE_72_500:  2, # Normally unlocks Pester Ball
    REPORT_SCORE_130_000: 3, # Normally unlocks PokeFlute
}

OAK_COUNT_REWARDS = {
    POKEMON_TOTAL_6 : 4, # Normally unlocks Tunnel
    POKEMON_TOTAL_22: 5, # Normally unlocks River
    POKEMON_TOTAL_40: 6, # Normally unlocks Valley
}

OAK_REWARDS = OAK_SCORE_REWARDS | OAK_COUNT_REWARDS

# Add the oak rewards
for name, id in OAK_SCORE_REWARDS.items():
    location_tables[START_GAME].append(PokemonSnapLocationData(oak_reward_id(id), name, PokemonSnapLocationCategory.REPORT_SCORE))

for name, id in OAK_COUNT_REWARDS.items():
    location_tables[START_GAME].append(PokemonSnapLocationData(oak_reward_id(id), name, PokemonSnapLocationCategory.PHOTO_COUNT))

# Must be done last: add the bonus locations
for region, location_data_list in location_tables.items():
    location_data_list.extend([
        PokemonSnapLocationData(bonus_id(id), bonus(name), PokemonSnapLocationCategory.BONUS_LOCATION)
        for id, name, _ in location_data_list
    ])
    