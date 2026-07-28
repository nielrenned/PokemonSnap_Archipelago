from dataclasses import dataclass

from Options import (ExcludeLocations, PerGameCommonOptions)

class RNGLocations(ExcludeLocations):
    """These photos rely on heavy RNG to capture.
    This prevents progress from being trapped behind them."""
    display_name = "Excluded RNG Required Photos"
    default = frozenset({"Zubat (Cave): Multiple", "Cloyster: Multiple", "Staryu: Multiple", "Starmie: Multiple","Dratini: Multiple","Magikarp (Valley): Multiple", "Arcanine: Multiple"})

@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    exclude_locations: RNGLocations