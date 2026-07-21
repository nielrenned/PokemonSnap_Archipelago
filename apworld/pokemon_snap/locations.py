from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Location, Region
from .items import PokemonSnapItem
from .constants import *

class PokemonSnapLocationCategory(IntEnum):
    PHOTO = 0


_PHOTO = PokemonSnapLocationCategory.PHOTO


class PokemonSnapLocationData(NamedTuple):
    id: int
    name: str
    category: PokemonSnapLocationCategory


class PokemonSnapSpeciesData(NamedTuple):
    id: int
    name: str
    wonderful: bool = True
    multiple: bool = False


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


POKEMON_IN_MULTIPLE_LEVELS = ["Pikachu", "Bulbasaur", "Zubat", "Magikarp"]

def wonderful(pokemon_name: str):
    return f'{pokemon_name}: Wonderful!'


def wonderful_id(id: int):
    return id + 100


def multiple(pokemon_name: str):
    return f'{pokemon_name}: Multiple'


def multiple_id(id: int):
    return id + 200


def regional(pokemon_name: str, region_name: str):
    return f'{pokemon_name} ({region_name})'


def regional_id(id: int, region_id: int):
    return 1000*(region_id + 1) + id


def special_id(pose_id: int):
    return 10000 + pose_id


species_data_tables = {
    LVL_BEACH: [
        PokemonSnapSpeciesData(id=7,  name="Butterfree", multiple=True),
        PokemonSnapSpeciesData(id=9,  name="Pidgey", multiple=True),
        PokemonSnapSpeciesData(id=10, name="Pikachu", multiple=True),
        PokemonSnapSpeciesData(id=19, name="Meowth"),
        PokemonSnapSpeciesData(id=34, name="Doduo"),
        PokemonSnapSpeciesData(id=42, name="Chansey"),
        PokemonSnapSpeciesData(id=43, name="Kangaskhan"),
        PokemonSnapSpeciesData(id=47, name="Scyther"),
        PokemonSnapSpeciesData(id=51, name="Magikarp"),
        PokemonSnapSpeciesData(id=53, name="Lapras", multiple=True),
        PokemonSnapSpeciesData(id=55, name="Eevee"),
        PokemonSnapSpeciesData(id=57, name="Snorlax"),
    ],
    LVL_TUNNEL: [
        PokemonSnapSpeciesData(id=8,  name="Kakuna", multiple=True),
        PokemonSnapSpeciesData(id=10, name="Pikachu"),
        PokemonSnapSpeciesData(id=15, name="Zubat"),
        PokemonSnapSpeciesData(id=17, name="Diglett"),
        PokemonSnapSpeciesData(id=18, name="Dugtrio", multiple=True),
        PokemonSnapSpeciesData(id=32, name="Magnemite", multiple=True),
        PokemonSnapSpeciesData(id=33, name="Magneton"),
        PokemonSnapSpeciesData(id=39, name="Haunter"),
        PokemonSnapSpeciesData(id=40, name="Electrode", multiple=True),
        PokemonSnapSpeciesData(id=49, name="Electabuzz", multiple=True),
        PokemonSnapSpeciesData(id=51, name="Magikarp"),
        PokemonSnapSpeciesData(id=59, name="Zapdos"),
    ],
    LVL_VOLCANO: [
        PokemonSnapSpeciesData(id=2,  name="Charmander", multiple=True),
        PokemonSnapSpeciesData(id=3,  name="Charmeleon"),
        PokemonSnapSpeciesData(id=4,  name="Charizard"),
        PokemonSnapSpeciesData(id=13, name="Vulpix", multiple=True),
        PokemonSnapSpeciesData(id=22, name="Growlithe", multiple=True),
        PokemonSnapSpeciesData(id=23, name="Arcanine", multiple=True),
        PokemonSnapSpeciesData(id=29, name="Rapidash", multiple=True),
        PokemonSnapSpeciesData(id=50, name="Magmar", multiple=True),
        PokemonSnapSpeciesData(id=51, name="Magikarp"),
        PokemonSnapSpeciesData(id=60, name="Moltres"),
    ],
    LVL_RIVER: [
        PokemonSnapSpeciesData(id=1,  name="Bulbasaur", multiple=True),
        PokemonSnapSpeciesData(id=6,  name="Metapod", multiple=True),
        PokemonSnapSpeciesData(id=10, name="Pikachu"),
        PokemonSnapSpeciesData(id=16, name="Vileplume"),
        PokemonSnapSpeciesData(id=20, name="Psyduck", multiple=True),
        PokemonSnapSpeciesData(id=24, name="Poliwag", multiple=True),
        PokemonSnapSpeciesData(id=30, name="Slowpoke"),
        PokemonSnapSpeciesData(id=31, name="Slowbro"),
        PokemonSnapSpeciesData(id=37, name="Shellder", multiple=True),
        PokemonSnapSpeciesData(id=38, name="Cloyster", multiple=True),
        PokemonSnapSpeciesData(id=51, name="Magikarp"),
        PokemonSnapSpeciesData(id=56, name="Porygon", multiple=True),
    ],
    LVL_CAVE: [
        PokemonSnapSpeciesData(id=1,  name="Bulbasaur", multiple=True),
        PokemonSnapSpeciesData(id=10, name="Pikachu"),
        PokemonSnapSpeciesData(id=14, name="Jigglypuff", multiple=True),
        PokemonSnapSpeciesData(id=15, name="Zubat", multiple=True),
        PokemonSnapSpeciesData(id=25, name="Weepinbell"),
        PokemonSnapSpeciesData(id=26, name="Victreebel"),
        PokemonSnapSpeciesData(id=35, name="Grimer"),
        PokemonSnapSpeciesData(id=36, name="Muk"),
        PokemonSnapSpeciesData(id=48, name="Jynx", multiple=True),
        PokemonSnapSpeciesData(id=51, name="Magikarp"),
        PokemonSnapSpeciesData(id=54, name="Ditto", multiple=True),
        PokemonSnapSpeciesData(id=58, name="Articuno"),
        PokemonSnapSpeciesData(id=41, name="Koffing"),
    ],
    LVL_VALLEY: [
        PokemonSnapSpeciesData(id=5,  name="Squirtle", multiple=True),
        PokemonSnapSpeciesData(id=11, name="Sandshrew", multiple=True),
        PokemonSnapSpeciesData(id=12, name="Sandslash"),
        PokemonSnapSpeciesData(id=21, name="Mankey"),
        PokemonSnapSpeciesData(id=27, name="Geodude", multiple=True),
        PokemonSnapSpeciesData(id=28, name="Graveler", multiple=True),
        PokemonSnapSpeciesData(id=44, name="Goldeen"),
        PokemonSnapSpeciesData(id=45, name="Staryu", multiple=True),
        PokemonSnapSpeciesData(id=46, name="Starmie", multiple=True),
        PokemonSnapSpeciesData(id=51, name="Magikarp", multiple=True),
        PokemonSnapSpeciesData(id=52, name="Gyarados"),
        PokemonSnapSpeciesData(id=61, name="Dratini", multiple=True),
        PokemonSnapSpeciesData(id=62, name="Dragonite"),
    ],
    LVL_CLOUD: [
        PokemonSnapSpeciesData(id=63, name="Mew", wonderful=False, multiple=False),
    ],
}


location_tables = {
    START_GAME: [],
}

for region, species_data_list in species_data_tables.items():
    location_data_list = []
    region_id = COURSE_IDS[region]
    for base_id, name, can_wonderful, can_multiple in species_data_list:
        id = regional_id(base_id, region_id)
        if name in POKEMON_IN_MULTIPLE_LEVELS:
            name = regional(name, region)
        location_data_list.append(PokemonSnapLocationData(id, name, _PHOTO))
        if can_wonderful:
            location_data_list.append(PokemonSnapLocationData(wonderful_id(id), wonderful(name), _PHOTO))
        if can_multiple:
            location_data_list.append(PokemonSnapLocationData(multiple_id(id), multiple(name), _PHOTO))
    location_tables[region] = location_data_list


special_poses = {
    1: "Surfing Pikachu",
    2: "Pikachu on a Ball",
    3: "Balloon Pikachu",
    4: "Speed Pikachu",
    5: "Pikachu on a Stump",
    6: "Flying Pikachu",
    7: "Gust-Using Pidgey",
    8: "Jigglypuff on Stage",
    9: "Graveler's Group Dance",
    10: "Rare Pokemon Mew",
    11: "Fighting Magmar",
    12: "Jigglypuff Trio on Stage",
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

for region, pose_ids in pose_locations.items():
    location_data_list = location_tables[region]
    for pose_id in pose_ids:
        pose_name = special_poses[pose_id]
        location_data_list.append(PokemonSnapLocationData(special_id(pose_id), pose_name, _PHOTO))