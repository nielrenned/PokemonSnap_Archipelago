from dataclasses import dataclass

from Options import Choice, DefaultOnToggle, ExcludeLocations, PerGameCommonOptions, Toggle

class RNGLocations(ExcludeLocations):
    """These photos rely on heavy RNG to capture.
    This prevents progress from being trapped behind them."""
    display_name = "Excluded RNG Required Photos"
    default = frozenset({"Zubat (Cave): Multiple", "Cloyster: Multiple", "Staryu: Multiple", "Starmie: Multiple","Dratini: Multiple","Magikarp (Valley): Multiple", "Arcanine: Multiple"})


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
    """
    Includes the 11 "Special Pose" photos as checks. The special poses are:
    - Beach:   Surfing Pikachu, Pikachu on a Stump, Gust-Using Pidgey
    - Tunnel:  Pikachu on a Ball
    - Volcano: Fighting Magmar
    - River:   Speed Pikachu
    - Cave:    Balloon Pikachu, Flying Pikachu, Jigglypuff on Stage, Jigglypuff Trio on Stage
    - Valley:  Graveler's Group Dance
    """
    display_name = "Include special poses"


class PokemonSigns(DefaultOnToggle):
    """
    Includes the 6 Pokemon Sign photos as checks (requires Pokemon Sign Detector).
    """
    display_name = "Include pokemon signs"


class SecretExits(DefaultOnToggle):
    """
    Include taking each of the 3 Secret Exits (Tunnel, River, and Valley) as checks. 
    """
    display_name = "Include secret exits"


class IncludeRNGChecks(Toggle):
    """
    Include the luck-heavy photos as checks. They are:
      Arcanine: Multiple, Cloyster: Multiple, Dratini: Multiple, 
      Magikarp (Valley): Multiple, and Psyduck: Multiple
    """
    display_name = "Include random checks"


class IncludeHardChecks(Toggle):
    """
    Include the hard photos as checks. They are:
      Staryu: Multiple, Starmie: Multiple, and Zubat (Cave): Multiple.
    """
    display_name = "Include hard checks"


class StartWithDashEngine(Toggle):
    """
    Start with the Dash Engine.

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