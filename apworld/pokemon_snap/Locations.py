from enum import IntEnum
from typing import Optional, NamedTuple, Dict

from BaseClasses import Location, Region
from .Items import PokemonSnapItem


class PokemonSnapLocationCategory(IntEnum):
    MISC = 0
    EVENT = 1
    SKIP = 2,
    PHOTO = 3


class PokemonSnapLocationData(NamedTuple):
    id: int
    name: str
    default_item: str
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
            default_item_name: str,
            address: Optional[int] = None,
            parent: Optional[Region] = None):
        super().__init__(player, name, address, parent)
        self.default_item_name = default_item_name
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
    "Start Game": [
        PokemonSnapLocationData(9999, "Start Area", "Point Modifier", PokemonSnapLocationCategory.MISC),
    ],
    "Beach": [
        PokemonSnapLocationData(7, "Butterfree", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(9, "Pidgey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(19, "Meowth", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(34, "Doduo", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(42, "Chansey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(43, "Kangaskhan", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(47, "Scyther", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(53, "Lapras", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(55, "Eevee", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(57, "Snorlax", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Tunnel": [
        PokemonSnapLocationData(8, "Kakuna", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(17, "Diglett", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(18, "Dugtrio", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(32, "Magnemite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(33, "Magneton", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(39, "Haunter", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(40, "Electrode", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(49, "Electabuzz", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(59, "Zapdos", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Volcano": [
        PokemonSnapLocationData(2, "Charmander", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(3, "Charmeleon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(4, "Charizard", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(13, "Vulpix", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(22, "Growlithe", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(23, "Arcanine", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(29, "Rapidash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(50, "Magmar", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(60, "Moltres", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "River": [
        PokemonSnapLocationData(6, "Metapod", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(16, "Vileplume", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(20, "Psyduck", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(24, "Poliwag", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(30, "Slowpoke", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(31, "Slowbro", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(37, "Shellder", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(38, "Cloyster", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(56, "Porygon", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Cave": [
        PokemonSnapLocationData(14, "Jigglypuff", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(25, "Weepinbell", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(26, "Victreebel", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(35, "Grimer", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(36, "Muk", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(48, "Jynx", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(54, "Ditto", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(58, "Articuno", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(41, "Koffing", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Valley": [
        PokemonSnapLocationData(5, "Squirtle", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(11, "Sandshrew", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(12, "Sandslash", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(21, "Mankey", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(27, "Geodude", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(28, "Graveler", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(44, "Goldeen", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(45, "Staryu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(46, "Starmie", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(52, "Gyarados", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(61, "Dratini", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
        PokemonSnapLocationData(62, "Dragonite", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Rainbow Cloud": [
        PokemonSnapLocationData(63, "Mew", "Point Modifier", PokemonSnapLocationCategory.PHOTO)
    ],
    "Bulbasaur": [
        PokemonSnapLocationData(1, "Bulbasaur", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Pikachu": [
        PokemonSnapLocationData(10, "Pikachu", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Zubat": [
        PokemonSnapLocationData(15, "Zubat", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ],
    "Magikarp": [
        PokemonSnapLocationData(51, "Magikarp", "Point Modifier", PokemonSnapLocationCategory.PHOTO),
    ]
}

location_dictionary: Dict[str, PokemonSnapLocationData] = {}
for location_table in location_tables.values():
    location_dictionary.update({location_data.name: location_data for location_data in location_table})
