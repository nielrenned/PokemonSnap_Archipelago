
from .bases import PokemonSnapTestBase
from ..items import PokemonSnapItemCategory, build_item_pool
from ..constants import MINIMAL_OPEN_LOCATION_COUNT

class TestSparseLocationGeneration(PokemonSnapTestBase):

    minimal_options = {
        "photo_bonuses": "none",
        "special_poses": False,
        "pokemon_signs": False,
        "secret_exits": False,
        "rng_checks": False,
        "hard_checks": False
    }

    def test_minimal_settings_include_enough_locations(self):
        # First we generate the default multiworld, which _should_ have enough locations.
        # We use that to get the count of non-trash items. Doing it this way is resilient
        # to us changing the item pool in the future.
        required_count = sum(
            1 for item in build_item_pool(self.world)
            if item.category not in [
                PokemonSnapItemCategory.TRASH_CUSTOM,
                PokemonSnapItemCategory.TRASH_PICTURE
            ])

        # Set minimal options and regenerate
        self.options = self.minimal_options
        self.world_setup()

        # Exclude the locked victory location
        actual_count = sum(1 for loc in self.multiworld.get_locations(self.player) if not loc.locked)

        # And check that there are enough slots
        if required_count > actual_count:
            msg = f'Minimal world does not generate enough locations. Generated: {actual_count}, required: {required_count}.'
            if required_count != MINIMAL_OPEN_LOCATION_COUNT:
                msg += f' {MINIMAL_OPEN_LOCATION_COUNT=} is different to generated {required_count=}. Please update MINIMAL_OPEN_LOCATION_COUNT.'
            self.fail(msg)