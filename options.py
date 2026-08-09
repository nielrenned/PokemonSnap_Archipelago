from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle
from .constants import *
from .locations import HARD_LOCATIONS, RNG_LOCATIONS

class PhotoBonusChecks(Choice):
    """
    Determines which photo bonuses to include as checks.
    - technique_and_multiple: adds "Good Technique" and "Multiple Pokemon" photos as checks 
    - technique_only: adds "Good Technique" photos as checks
    - none: only normal photos are checks
    """
    display_name = "Include photo bonuses"
    default = 2
    option_none = 0
    option_technique_only = 1
    option_technique_and_multiple = 2


class SpecialPoses(DefaultOnToggle):
    f"""
    Include the 11 "Special Pose" photos as checks. The special poses are:
    - Beach:   {SURFING_PIKACHU}, {PIKACHU_ON_A_STUMP}, {GUST_USING_PIDGEY}
    - Tunnel:  {PIKACHU_ON_A_BALL}
    - Volcano: {FIGHTING_MAGMAR}
    - River:   {SPEED_PIKACHU}
    - Cave:    {BALLOON_PIKACHU}, {FLYING_PIKACHU}, {JIGGLYPUFF_ON_STAGE}, {JIGGLYPUFF_TRIO}
    - Valley:  {GRAVELERS_GROUP_DANCE}
    """
    display_name = "Include special poses"


class PokemonSigns(DefaultOnToggle):
    """
    Include the 6 Pokemon Sign photos as checks (requires Pokemon Sign Detector).
    """
    display_name = "Include pokemon signs"


class SecretExits(DefaultOnToggle):
    """
    Include taking each of the 3 Secret Exits (Tunnel, River, and Valley) as checks. 
    """
    display_name = "Include secret exits"


class IncludeRNGChecks(Toggle):
    f"""
    Include the luck-heavy photos as checks. They are:
      {', '.join(RNG_LOCATIONS)}
    """
    display_name = "Include random checks"


class IncludeHardChecks(Toggle):
    f"""
    Include the hard photos as checks. They are:
      {', '.join(HARD_LOCATIONS)}
    """
    display_name = "Include hard checks"


class StartWithDashEngine(Toggle):
    f"""
    Start with the {DASH_ENGINE}.

    This makes up to six more checks available from the beginning.
    """
    display_name = "Start with Dash Engine"


@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    photo_bonuses: PhotoBonusChecks
    special_poses: SpecialPoses
    pokemon_signs: PokemonSigns
    secret_exits:  SecretExits

    rng_checks:  IncludeRNGChecks
    hard_checks: IncludeHardChecks

    start_with_dash_engine: StartWithDashEngine