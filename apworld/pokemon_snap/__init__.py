from typing import Dict, Set, List

from BaseClasses import MultiWorld, Region, Entrance, Tutorial, ItemClassification
from worlds.AutoWorld import World, WebWorld
from .Items import PokemonSnapItem, PokemonSnapItemCategory, item_dictionary, key_item_names, item_descriptions, \
    _all_items, build_item_pool
from .Locations import PokemonSnapLocation, PokemonSnapLocationCategory, location_tables, location_dictionary
from .Options import PokemonSnapOption
from .Rules import set_rules


class PokemonSnapWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Pokemon Snap randomizer on your computer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin"]
    )

    tutorials = [setup_en]


class PokemonSnapWorld(World):
    """
    Pokemon Snap is a game about taking photographs of monsters to score points.
    """

    game = "Pokemon Snap"
    options_dataclass = PokemonSnapOption
    options: PokemonSnapOption
    topology_present: bool = True
    web = PokemonSnapWeb()
    data_version = 0
    enabled_location_categories: Set[PokemonSnapLocationCategory]
    required_client_version = (0, 5, 0)
    item_name_to_id = PokemonSnapItem.get_name_to_id()
    location_name_to_id = PokemonSnapLocation.get_name_to_id()
    item_name_groups = {
    }
    item_descriptions = item_descriptions

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.locked_items = []
        self.locked_locations = []
        self.main_path_locations = []
        self.enabled_location_categories = set()
        self.start_area = None

    def generate_early(self):
        self.enabled_location_categories.add(PokemonSnapLocationCategory.MISC)
        self.enabled_location_categories.add(PokemonSnapLocationCategory.EVENT)
        self.enabled_location_categories.add(PokemonSnapLocationCategory.PHOTO)

    def create_regions(self):
        # Create Regions
        regions = {"Menu": self.create_region("Menu", [])}
        regions.update({region_name: self.create_region(region_name, location_tables[region_name]) for region_name in [
            "Start Game", "Beach", "Tunnel", "Volcano", "River", "Cave", "Valley", "Rainbow Cloud", "Bulbasaur",
            "Pikachu", "Zubat", "Magikarp"
        ]})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", "Start Game")

        create_connection("Start Game", "Beach")
        create_connection("Start Game", "Tunnel")
        create_connection("Start Game", "Volcano")
        create_connection("Start Game", "River")
        create_connection("Start Game", "Cave")
        create_connection("Start Game", "Valley")
        create_connection("Start Game", "Rainbow Cloud")

        create_connection("River", "Bulbasaur")
        create_connection("Cave", "Bulbasaur")

        create_connection("Tunnel", "Zubat")
        create_connection("Cave", "Zubat")

        create_connection("Beach", "Pikachu")
        create_connection("River", "Pikachu")
        create_connection("Tunnel", "Pikachu")
        create_connection("Cave", "Pikachu")

        create_connection("Beach", "Magikarp")
        create_connection("Tunnel", "Magikarp")
        create_connection("Volcano", "Magikarp")
        create_connection("River", "Magikarp")
        create_connection("Cave", "Magikarp")
        create_connection("Valley", "Magikarp")

        # For each region, add the associated locations retrieved from the corresponding location_table

    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            if location.name == "Start Area":
                areas = [item for item in _all_items if item.category == PokemonSnapItemCategory.AREA]
                self.start_area = self.random.choice(areas)
                start_item = self.create_item(self.start_area.name)
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                new_location.place_locked_item(start_item)
            elif location.category in self.enabled_location_categories:
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    self.location_name_to_id[location.name],
                    new_region
                )
            else:
                # Replace non-randomized progression items with events
                event_item = self.create_item(location.default_item)
                new_location = PokemonSnapLocation(
                    self.player,
                    location.name,
                    location.category,
                    location.default_item,
                    None,
                    new_region
                )
                event_item.code = None
                new_location.place_locked_item(event_item)

            new_region.locations.append(new_location)
        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        skip_items: List[PokemonSnapItem] = []
        itempool: List[PokemonSnapItem] = []
        itempool_size = 0

        for location in self.get_locations():
            if location.name == "Start Area":
                continue
            item_data = item_dictionary[location.default_item_name]
            if item_data.category in [PokemonSnapItemCategory.SKIP, PokemonSnapItemCategory.EVENT]:
                skip_items.append(self.create_item(location.default_item_name))
            elif location.category in self.enabled_location_categories:
                itempool_size += 1
                itempool.append(self.create_item(location.default_item_name))

        additional_items = build_item_pool(itempool_size, self.start_area)

        removable_items = [item for item in itempool if item.classification != ItemClassification.progression]

        for item in removable_items:
            itempool.remove(item)
            itempool.append(self.create_item(additional_items.pop().name))

        # Add regular items to itempool
        self.multiworld.itempool.extend(itempool)

        # Handle SKIP items separately
        for skip_item in skip_items:
            location = next(loc for loc in self.get_locations()
                            if loc.default_item_name == skip_item.name)
            location.place_locked_item(skip_item)

    def create_item(self, name: str) -> PokemonSnapItem:
        useful_categories = {}
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif item_dictionary[name].category in useful_categories:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return PokemonSnapItem(name, item_classification, data, self.player)

    def get_filler_item_name(self) -> str:
        return "Nothing, literally nothing at all"

    def set_rules(self) -> None:
        set_rules(self)

    def fill_slot_data(self) -> Dict[str, object]:
        name_to_ps_code = {item.name: item.ps_code for item in item_dictionary.values()}
        # Create the mandatory lists to generate the player's output file
        items_id = []
        items_address = []
        locations_id = []
        locations_address = []
        locations_target = []
        for location in self.multiworld.get_filled_locations():

            if location.item.player == self.player:
                # we are the receiver of the item
                items_id.append(location.item.code)
                items_address.append(name_to_ps_code[location.item.name])

            if location.player == self.player:
                # we are the sender of the location check
                locations_address.append(item_dictionary[location_dictionary[location.name].default_item].ps_code)
                locations_id.append(location.address)
                if location.item.player == self.player:
                    locations_target.append(name_to_ps_code[location.item.name])
                else:
                    locations_target.append(0)

        slot_data = {
            "options": {
                "guaranteed_items": self.options.guaranteed_items.value,
            },
            "seed": self.multiworld.seed_name,  # to verify the server's multiworld
            "slot": self.multiworld.player_name[self.player],  # to connect to server
            "base_id": 0,  # to merge location and items lists
            "locationsId": locations_id,
            "locationsAddress": locations_address,
            "locationsTarget": locations_target,
            "itemsId": items_id,
            "itemsAddress": items_address
        }

        return slot_data
