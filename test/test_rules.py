
from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..locations import wonderful, multiple
from ..pokemon_rules import SPECIES_RULE_DATA
from ..items import PokemonSnapItemCategory, item_dictionary
from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class TestRuleInheritance(PokemonSnapTestBase):

    options = {
        "photo_bonuses": "technique_and_multiple",
        "rng_checks": True,
        "hard_checks": True
    }

    def test_multiple_implies_wonderful(self):
        '''Professor Oak will not give you the multiple species bonus if the picture is not Wonderful'''
        for species_data_list in SPECIES_RULE_DATA.values():
            for species_data in species_data_list:
                if species_data.soft_logic.multiple is None or species_data.soft_logic.wonderful is None:
                    continue

                with self.subTest(name=species_data.name):
                    self._assert_multiple_implies_wonderful(species_data.name)
    
    def _assert_multiple_implies_wonderful(self, species_name):
        mult_rule = self.multiworld.get_location(multiple(species_name), self.player).access_rule
        wdfl_rule = self.multiworld.get_location(wonderful(species_name), self.player).access_rule

        tools = [self.get_item_by_name(name)
                 for name, item in item_dictionary.items() 
                 if item.category is PokemonSnapItemCategory.TOOL]

        for combo in powerset(tools):
            state = CollectionState(self.multiworld)
            for tool in combo:
                state.collect(self.get_item_by_name(tool.name))

            if mult_rule(state) and not wdfl_rule(state):
                self.fail(f'"{wonderful(species_name)}" can not be collected with {combo}, but "{multiple(species_name)}" can')