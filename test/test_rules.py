
from BaseClasses import CollectionState
from .bases import PokemonSnapTestBase
from ..locations import POKEMON_IN_MULTIPLE_LEVELS, species_data_tables, regional, wonderful, multiple
from ..items import PokemonSnapItemCategory, item_dictionary
from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

class TestRuleInheritance(PokemonSnapTestBase):

    def test_multiple_implies_wonderful(self):
        '''Professor Oak will not give you the multiple species bonus if the picture is not Wonderful'''
        for region, species_data_list in species_data_tables.items():
            for species_data in species_data_list:
                if not (species_data.multiple and species_data.wonderful):
                    continue

                species_name = species_data.name
                if species_name in POKEMON_IN_MULTIPLE_LEVELS:
                    species_name = regional(species_name, region)

                with self.subTest(name=species_data.name):
                    self._assert_multiple_implies_wonderful(species_name)
    
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