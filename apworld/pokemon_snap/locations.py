from enum import IntEnum
from typing import NamedTuple

from BaseClasses import Location, Region
from .items import PokemonSnapItem


class PokemonSnapLocationCategory(IntEnum):
    PHOTO = 0


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
            "Start Game", "Beach", "Tunnel", "Volcano", "River", "Cave", "Valley", "Rainbow Cloud", "Bulbasaur",
            "Pikachu", "Zubat", "Magikarp"
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


location_tables = {
    "Start Game": [],
    "Beach": [
        PokemonSnapLocationData(7, "Butterfree", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(9, "Pidgey", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(19, "Meowth", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(34, "Doduo", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(42, "Chansey", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(43, "Kangaskhan", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(47, "Scyther", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(53, "Lapras", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(55, "Eevee", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(57, "Snorlax", PokemonSnapLocationCategory.PHOTO),
    ],
    "Tunnel": [
        PokemonSnapLocationData(8, "Kakuna", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(17, "Diglett", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(18, "Dugtrio", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(32, "Magnemite", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(33, "Magneton", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(39, "Haunter", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(40, "Electrode", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(49, "Electabuzz", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(59, "Zapdos", PokemonSnapLocationCategory.PHOTO),
    ],
    "Volcano": [
        PokemonSnapLocationData(2, "Charmander", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(3, "Charmeleon", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(4, "Charizard", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(13, "Vulpix", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(22, "Growlithe", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(23, "Arcanine", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(29, "Rapidash", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(50, "Magmar", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(60, "Moltres", PokemonSnapLocationCategory.PHOTO),
    ],
    "River": [
        PokemonSnapLocationData(6, "Metapod", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(16, "Vileplume", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(20, "Psyduck", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(24, "Poliwag", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(30, "Slowpoke", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(31, "Slowbro", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(37, "Shellder", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(38, "Cloyster", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(56, "Porygon", PokemonSnapLocationCategory.PHOTO),
    ],
    "Cave": [
        PokemonSnapLocationData(14, "Jigglypuff", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(25, "Weepinbell", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(26, "Victreebel", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(35, "Grimer", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(36, "Muk", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(48, "Jynx", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(54, "Ditto", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(58, "Articuno", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(41, "Koffing", PokemonSnapLocationCategory.PHOTO),
    ],
    "Valley": [
        PokemonSnapLocationData(5, "Squirtle", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(11, "Sandshrew", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(12, "Sandslash", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(21, "Mankey", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(27, "Geodude", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(28, "Graveler", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(44, "Goldeen", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(45, "Staryu", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(46, "Starmie", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(52, "Gyarados", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(61, "Dratini", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(62, "Dragonite", PokemonSnapLocationCategory.PHOTO),
    ],
    "Rainbow Cloud": [
        PokemonSnapLocationData(63, "Mew", PokemonSnapLocationCategory.PHOTO)
    ],
    "Bulbasaur": [
        PokemonSnapLocationData(1, "Bulbasaur", PokemonSnapLocationCategory.PHOTO),
    ],
    "Pikachu": [
        PokemonSnapLocationData(10, "Pikachu", PokemonSnapLocationCategory.PHOTO),
    ],
    "Zubat": [
        PokemonSnapLocationData(15, "Zubat", PokemonSnapLocationCategory.PHOTO),
    ],
    "Magikarp": [
        PokemonSnapLocationData(51, "Magikarp", PokemonSnapLocationCategory.PHOTO),
    ]
}

location_dictionary: dict[str, PokemonSnapLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
