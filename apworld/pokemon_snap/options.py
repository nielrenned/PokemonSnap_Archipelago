import typing
from dataclasses import dataclass
from Options import ItemDict, PerGameCommonOptions



class GuaranteedItemsOption(ItemDict):
    """Guarantees that the specified items will be in the item pool"""
    display_name = "Guaranteed Items"

@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    guaranteed_items: GuaranteedItemsOption