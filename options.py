from dataclasses import dataclass
from .constants import DEFAULT_GOAL_TYPE, DEFAULT_SIGN_REQUIREMENT, DEFAULT_POKEMON_REQUIREMENT, GOAL_SIGN_PICS, GOAL_POKEMON_PICS
from Options import Choice, DefaultOnToggle, PerGameCommonOptions, Toggle, OptionGroup, StartInventoryPool, Range
from .addresses import CAMERA_INVERSION_OPTION_INVERTED, CAMERA_INVERSION_OPTION_NORMAL


class GoalType(Choice):
    """
    Determines what is required to unlock The Rainbow Cloud where Mew (the Goal Condtion) lives.
    Note: If significantly lowering requirements, we recommend disabling the # pokemon and score cehcks
    - signs: What is used in Vanilla Pokemon Snap - spread accross the multiworlds. Can be adjusted.
    - pokemon_pictures: A number of Pokemon Pictures spread accross the multiworlds.  Can be adjusted.
    """
    display_name = "Goal Type"
    default = DEFAULT_GOAL_TYPE
    option_signs = GOAL_SIGN_PICS
    option_pokemon_pictures = GOAL_POKEMON_PICS


class SignsRequired(Range):
    """
    Determines the number of Sign Pictures required to unlock the Rainbow Cloud.
    Only matters if Goal Type is set to "Signs"
    """
    display_name = "Signs Required"
    range_start = 1
    range_end = 6
    default = DEFAULT_SIGN_REQUIREMENT


class PokemonRequired(Range):
    """
    Determines the number of Pokemon Pictures required to unlock the Rainbow Cloud.
    Only matters if Goal Type is set to "Pokemon"
    """
    display_name = "Pokemon Required"
    range_start = 1
    range_end = 63
    default = DEFAULT_POKEMON_REQUIREMENT


class ScoringBonus(Choice):
    """
    """
    display_name = "Photo Score Bonuses"
    option_always_available = 0
    option_progressive      = 1
    option_separate         = 2


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
    Include the 11 "Special Pose" photos as checks. The special poses are:
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
    Include the 6 Pokemon Sign photos as checks (requires Pokemon Sign Detector).
    """
    display_name = "Include pokemon signs"


class SecretExits(DefaultOnToggle):
    """
    Include taking each of the 3 Secret Exits (Tunnel, River, and Valley) as checks. 
    """
    display_name = "Include secret exits"


class PokemonReportPhotoCount(DefaultOnToggle):
    """
    Include the three photo count rewards from Professor Oak as checks. 
    They are rewarded for having 6, 22, and 40 pictures in your PKMN Report.
    """
    display_name = "PKMN Report Photo Rewards"


class PokemonReportTotalScore(DefaultOnToggle):
    """
    Include the three PKMN Report score checkpoint rewards from Professor Oak as checks. 
    They are rewarded for having a score of 24,000, 72,500, and 130,000 in your PKMN Report.
    """
    display_name = "PKMN Report Score Rewards"


class IncludeRNGChecks(Toggle):
    """
    Include the luck-heavy photos as checks. They are:
    - [Volcano] Arcanine: Multiple
    - [  River] Cloyster: Multiple and Psyduck: Multiple
    - [ Valley] Magikarp (Valley): Multiple and Dratini: Multiple
    """
    display_name = "Include random checks"


class IncludeHardChecks(Toggle):
    """
    Include the hard photos as checks. They are:
    - [ River] Pikachu (River): Good Technique
    - [  Cave] Zubat (Cave): Multiple, Magikarp (Cave): Wonderful, Balloon Pikachu, and Flying Pikachu
    - [Valley] Staryu: Multiple, Starmie: Multiple, and Goldeen: Good Technique
    """
    display_name = "Include hard checks"


class StartWithDashEngine(Toggle):
    """
    Start with the Dash Engine.

    This makes up to six more checks available from the beginning.
    """
    display_name = "Start with Dash Engine"


class PressLeftBumperToToggleZeroOne(Toggle):
    """
    Adds the ability to start/stop the Zero-One by pressing L.
    """
    display_name = "Press L to start/stop"


class CameraInversion(Choice):
    """
    Choose if the camera controls are Normal or Inverted.
    """
    display_name = "Camera Inversion"

    # DO NOT change these values, they match the values in the ROM
    default = CAMERA_INVERSION_OPTION_NORMAL
    option_inverted = CAMERA_INVERSION_OPTION_INVERTED
    option_normal = CAMERA_INVERSION_OPTION_NORMAL


@dataclass
class PokemonSnapOption(PerGameCommonOptions):
    goal_type: GoalType
    signs_required: SignsRequired
    pokemon_required: PokemonRequired

    scoring_bonuses: ScoringBonus

    photo_bonuses: PhotoBonusChecks
    special_poses: SpecialPoses
    pokemon_signs: PokemonSigns
    secret_exits:  SecretExits
    report_photo_count: PokemonReportPhotoCount
    report_score_total: PokemonReportTotalScore

    rng_checks:  IncludeRNGChecks
    hard_checks: IncludeHardChecks

    start_with_dash_engine: StartWithDashEngine
    enable_left_bumper_to_start_stop: PressLeftBumperToToggleZeroOne
    camera_inversion: CameraInversion
    start_inventory_from_pool: StartInventoryPool

pokemon_snap_option_groups = [
    OptionGroup("Goal Settings", [
        GoalType,
        SignsRequired,
        PokemonRequired,
    ]),
    OptionGroup("Items", [
        ScoringBonus,
    ]),
    OptionGroup("Checks - Categories", [
        PhotoBonusChecks,
        SpecialPoses,
        PokemonSigns,
        SecretExits,
        PokemonReportPhotoCount,
        PokemonReportTotalScore,
    ]),
    OptionGroup("Checks - Pokemon", [
		IncludeRNGChecks,
		IncludeHardChecks,
	]),
    OptionGroup("Quality Of Life", [
		StartWithDashEngine,
        PressLeftBumperToToggleZeroOne,
        CameraInversion,
	]),
]