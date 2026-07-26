from dataclasses import dataclass

from Options import (ExcludeLocations, PerGameCommonOptions, Choice)

class RNGLocations(ExcludeLocations):
    """These photos rely on RNG to capture."""
    display_name = "RNG Required Photos"
    default = frozenset({"Zubat (Cave): Multiple", "Cloyster: Multiple", "Staryu: Multiple","Dratini: Multiple","Magikarp (Valley): Multiple", "Arcanine: Multiple"})

class RNGLocationBehaviorOption(Choice):
    """How to choose items for photos marked as requiring RNG in Pokemon Snap.

    - **Allow Useful:** Excluded locations can't have progression items, but they can have useful
      items.
    - **Forbid Useful:** Neither progression items nor useful items can be placed in excluded
      locations.
    - **Do Not Randomize:** Excluded locations always contain the same item as in vanilla Dark Souls
      III.

    A "progression item" is anything that's required to unlock another location in some game. A
    "useful item" is something each game defines individually, usually items that are quite
    desirable but not strictly necessary.
    """
    display_name = "RNG Photo Behavior"
    option_allow_useful = 1
    option_forbid_useful = 2
    option_do_not_randomize = 3
    default = 2

@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    exclude_locations: RNGLocations
    excluded_location_behavior: RNGLocationBehaviorOption