from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..constants import POKEMON_TOTAL_40

class Test40PokemonNotAvailable(PokemonSnapTestBase):

    options = {
        "photo_bonuses": "none",
        "special_poses": False,
        "pokemon_signs": False,
        "secret_exits": False,
        "rng_checks": False,
        "hard_checks": False,
        "start_with_dash_engine": True,
        "report_photo_count": True,
    }

    def test_40_pokemon_check_unavailable(self):
        self.collect_by_name(["Beach", "River", "Cave", "Volcano", "Pester Ball", "Dash Engine"])

        if self.can_reach_location(POKEMON_TOTAL_40):
            self.fail("Should not be able to reach 40 Pokemon")