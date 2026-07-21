import os
import pkgutil
from typing import ClassVar

from BaseClasses import MultiWorld, Region, Entrance, Tutorial, ItemClassification
from NetUtils import MultiData
from worlds.AutoWorld import World, WebWorld
from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch_subprocess
from .constants import *
from .items import PokemonSnapItem, PokemonSnapItemCategory, key_item_names, useful_item_names, \
    _all_items, build_item_pool, PokemonSnapItemData
from .locations import PokemonSnapLocation, PokemonSnapLocationCategory, location_tables
from .options import PokemonSnapOption
from .psnap_settings import PokemonSnapSettings
from .rom import PokemonSnapProcedurePatch
from .rules import set_rules


def run_client(*args):
    from .client import main  # lazy import
    launch_subprocess(main, name="PokemonSnapClient", args=args)

# Adds the launcher for our component and our client logo.
components.append(
    Component("Pokemon Snap Client", func=run_client, component_type=Type.CLIENT,
              file_identifier=SuffixIdentifier(".apsnap")))


class PokemonSnapWeb(WebWorld):
    bug_report_page = ""
    theme = "stone"
    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Archipelago Pokemon Snap randomizer.",
        "English",
        "setup_en.md",
        "setup/en",
        ["ArsonAssassin", "SomeJakeGuy", "gerbiljames", "nielrenned"]
    )

    tutorials = [setup_en]


class PokemonSnapWorld(World):
    """
    Pokemon Snap is a game about taking photographs of monsters to score points.
    """

    game = "Pokemon Snap"
    web = PokemonSnapWeb()

    options_dataclass = PokemonSnapOption
    options: PokemonSnapOption
    topology_present: bool = True

    enabled_location_categories: set[PokemonSnapLocationCategory]
    required_client_version = (0, 6, 7)
    item_name_to_id = PokemonSnapItem.get_name_to_id()
    location_name_to_id = PokemonSnapLocation.get_name_to_id()
    item_name_groups = items.item_name_groups
    settings: ClassVar[PokemonSnapSettings]
    start_area: PokemonSnapItemData
    auth: bytes

    def __init__(self, multiworld: MultiWorld, player: int):
        super().__init__(multiworld, player)
        self.enabled_location_categories = set()

    def generate_early(self):
        self.enabled_location_categories.add(PokemonSnapLocationCategory.PHOTO)

        # Per-seed connect token, baked into the ROM and registered server-side.
        self.auth = self.random.randbytes(16)

        # Starting course as precollected (build_item_pool excludes it). Exclude
        # Rainbow Cloud so the goal course can't be the start.
        areas = [item for item in _all_items
                 if item.category == PokemonSnapItemCategory.AREA
                 and item.name != LVL_CLOUD]
        self.start_area = self.random.choice(areas)
        self.multiworld.push_precollected(self.create_item(self.start_area.name))

    def create_regions(self):
        # Create Regions
        regions = {"Menu": self.create_region("Menu", [])}
        regions.update({region_name: self.create_region(region_name, region_entry)
                        for region_name, region_entry in location_tables.items()})

        # Connect Regions
        def create_connection(from_region: str, to_region: str):
            connection = Entrance(self.player, f"{from_region} -> {to_region}", regions[from_region])
            regions[from_region].exits.append(connection)
            connection.connect(regions[to_region])

        create_connection("Menu", START_GAME)

        create_connection(START_GAME, LVL_BEACH)
        create_connection(START_GAME, LVL_TUNNEL)
        create_connection(START_GAME, LVL_VOLCANO)
        create_connection(START_GAME, LVL_RIVER)
        create_connection(START_GAME, LVL_CAVE)
        create_connection(START_GAME, LVL_VALLEY)
        create_connection(START_GAME, LVL_CLOUD)

    def create_region(self, region_name, location_table) -> Region:
        new_region = Region(region_name, self.player, self.multiworld)
        for location in location_table:
            new_location = PokemonSnapLocation(
                self.player,
                location.name,
                location.category,
                self.location_name_to_id[location.name],
                new_region
            )
            new_region.locations.append(new_location)
        self.multiworld.regions.append(new_region)
        return new_region

    def create_items(self):
        item_pool = build_item_pool(self)
        self.multiworld.itempool.extend(self.create_item(item.name) for item in item_pool)

    def create_item(self, name: str) -> PokemonSnapItem:
        data = self.item_name_to_id[name]

        if name in key_item_names:
            item_classification = ItemClassification.progression
        elif name in useful_item_names:
            item_classification = ItemClassification.useful
        else:
            item_classification = ItemClassification.filler

        return PokemonSnapItem(name, item_classification, data, self.player)

    def get_filler_item_name(self) -> str:
        return self.random.choice(items.filler_item_names)

    def set_rules(self) -> None:
        set_rules(self)

    def modify_multidata(self, multidata: MultiData) -> None:
        import base64
        # Let the client connect with base64(token); a wrong-seed ROM's token
        # isn't registered here, so the server rejects it.
        multidata["connect_names"][base64.b64encode(self.auth).decode("ascii")] = \
            multidata["connect_names"][self.player_name]

    def generate_output(self, output_directory: str) -> None:
        from . import addresses as addr
        from worlds.Files import APTokenTypes

        patch = PokemonSnapProcedurePatch(player=self.player, player_name=self.player_name)
        patch.write_file("basepatch.bsdiff4", pkgutil.get_data(__name__, "data/basepatch.bsdiff4"))
        patch.write_token(APTokenTypes.WRITE, addr.AUTH_ROM, self.auth)
        patch.write_file("token_patch.bin", patch.get_token_binary())
        out_path = os.path.join(
            output_directory,
            f"{self.multiworld.get_out_file_name_base(self.player)}{patch.patch_file_ending}")
        patch.write(out_path)