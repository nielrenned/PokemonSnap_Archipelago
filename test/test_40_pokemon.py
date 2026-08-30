from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..constants import POKEMON_TOTAL_40, ALL_LEVELS

class Test40PokemonNotAvailable(PokemonSnapTestBase):

    def test_40_pokemon_check_unavailable(self):
        rule_40_pokemon = self.multiworld.get_location(POKEMON_TOTAL_40, self.player).access_rule
        state = CollectionState(self.multiworld, self.player)
        for item in self.get_items_by_name(ALL_LEVELS):
            state.remove_item(item, self.player)
        for item in self.get_items_by_name(["Beach", "River", "Cave", "Volcano", "Pester Ball", "Dash Engine"]):
            state.add_item(item, self.player)

        if rule_40_pokemon(state):
            self.fail(f"Should not be able to reach 40 Pokemon")