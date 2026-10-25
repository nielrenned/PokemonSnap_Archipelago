from typing import TYPE_CHECKING, override
from dataclasses import dataclass
from collections import defaultdict

from rule_builder.rules import Rule, True_, False_, And, Or, Has, HasGroup, CanReachLocation, CollectionState, OptionFilter
from .locations import wonderful, multiple, secret_exit, course, bonus, regular_pose, species_data_tables, special_pose_by_pokemon, special_pose_scores, \
    PokemonSnapLocationCategory as Category, RNG_LOCATIONS, HARD_LOCATIONS, POKEMON_IN_MULTIPLE_LEVELS, POKEMON_LOCATION_TO_SPECIES
from .constants import *
from .items import PokemonSnapItemCategory as ItemCategory, fragment, course as course_item
from .options import GoalType, PhotoScoring, IncludeRNGChecks, UseHardLogic, PhotoBonusChecks
from .poses import *
from .shots import SHOTS, Shot
if TYPE_CHECKING:
    from . import PokemonSnapWorld

try:
    from rule_builder.rules import AtLeast # Added in 0.6.8
except ImportError:
    from .future_rules import AtLeast

_NO_ITEMS   = True_()

_SEPARATE_SCORING = OptionFilter(PhotoScoring, [PhotoScoring.option_separate, PhotoScoring.option_separate_unlocks], operator="in")
_RNG_LOCATIONS_ON = OptionFilter(IncludeRNGChecks, IncludeRNGChecks.option_true)
_HARD_LOGIC_ON    = OptionFilter(UseHardLogic, UseHardLogic.option_true)

_identity = lambda s: s

location_name_functions = {
    Category.NORMAL_PHOTO:    _identity,
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO:  multiple,
    Category.SPECIAL_POSE:    _identity,
    Category.REGULAR_POSE:    regular_pose,
    Category.POKEMON_SIGN:    _identity,
    Category.SECRET_EXIT:     secret_exit,
    Category.PHOTO_COUNT:     _identity,
    Category.REPORT_SCORE:    _identity,
}


def location_name(name: str, category: Category):
    return location_name_functions[category](name)


def set_location_rule(world: "PokemonSnapWorld", name: str, category: Category, rule: Rule):
    try:
        base_name = location_name(name, category)
        world.set_rule(world.get_location(base_name), rule)
        # Make sure the bonus locations also have the same rules
        world.set_rule(world.get_location(bonus(base_name)), rule)
    except KeyError:
        # The location wasn't added, so skip the logic for it
        # TODO: this is hacky, let's do it better eventually
        pass


def wonderful_requirement(world: "PokemonSnapWorld"):
    if world.options.photo_scoring == PhotoScoring.option_progressive_unlocks:
        return Has(PROG_SCORING, 1)
    elif world.options.photo_scoring == PhotoScoring.option_separate_unlocks:
        return Has(WDFL_SCORING)
    
    return _NO_ITEMS


def multiple_requirement(world: "PokemonSnapWorld"):
    if world.options.photo_scoring == PhotoScoring.option_progressive_unlocks:
        return Has(PROG_SCORING, 2)
    elif world.options.photo_scoring == PhotoScoring.option_separate_unlocks:
        return Has(MULT_SCORING)

    return _NO_ITEMS


def has(item_name: str, course_name: str):
    if item_name == POKEMON_FOOD or item_name == APPLE:
        return Has(POKEMON_FOOD) | Has(course_item(POKEMON_FOOD, course_name)) | Has(APPLE) | Has(course_item(APPLE, course_name))
    return Has(item_name) | Has(course_item(item_name, course_name))


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level) | Has(fragment(level), world.options.map_fragments.value))

    if world.options.goal_type == GoalType.option_signs:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(ItemCategory.SIGN_PIC.value, world.options.signs_required.value))
    elif world.options.goal_type == GoalType.option_pokemon_pictures:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(ItemCategory.POKEMON_PIC.value, world.options.pokemon_required.value))

    # World location rules
    for name, categories in LOCATION_RULES.items():
        for category, rule in categories.items():
            if category == Category.WONDERFUL_PHOTO:
                rule = And(wonderful_requirement(world), rule)
            if category == Category.MULTIPLE_PHOTO:
                rule = And(multiple_requirement(world), rule)
            
            set_location_rule(world, name, category, rule)


@dataclass()
class ReportScoreAchievable(Rule["PokemonSnapWorld"], game="Pokemon Snap"):
    score_goal: int

    @override
    def _instantiate(self, world: "PokemonSnapWorld") -> Rule.Resolved:
        exclusions = set()
        if not world.options.hard_checks: exclusions.update(HARD_LOCATIONS)
        if not world.options.rng_checks:  exclusions.update(RNG_LOCATIONS)

        fudge_multiplier = 0.9 if world.options.hard_logic else 0.8 # TODO: this may not be necessary after all

        shots_by_species = defaultdict(list)
        for location, species in POKEMON_LOCATION_TO_SPECIES.items():
            for shot in SHOTS[location]:
                resolved = self.resolve_shot(world, location, shot, fudge_multiplier, exclusions)
                if resolved is not None: shots_by_species[species].append(resolved)
        
        return self.Resolved(
            self.score_goal, 
            wonderful_requirement(world).resolve(world),
            multiple_requirement(world).resolve(world),
            world.options.photo_scoring.value in (PhotoScoring.option_separate, PhotoScoring.option_separate_unlocks),
            tuple(tuple(shots) for shots in shots_by_species.values()),
            player=world.player)

    @staticmethod
    def resolve_shot(world: "PokemonSnapWorld", location: str, shot: Shot, fudge: float, exclusions: set[str]):
        if shot.wonderful and wonderful(location) in exclusions:   return None
        if shot.multiple > 0 and multiple(location) in exclusions: return None

        rule = CanReachLocation(location) & shot.rule
        if isinstance(shot.pose, PokemonSnapPoseData):
            if regular_pose(shot.pose) in exclusions: return None
            rule &= LOCATION_RULES[shot.pose][Category.REGULAR_POSE]
            pose_score = shot.pose.score
        else:
            pose_score = int(shot.pose * fudge)

        special_score = 0
        if shot.special is not None:
            if shot.special in exclusions: return None
            rule &= LOCATION_RULES[shot.special][Category.SPECIAL_POSE]
            special_score = special_pose_scores[shot.special]

        wonderful_rule = False_().resolve(world)
        if shot.wonderful and Category.WONDERFUL_PHOTO in LOCATION_RULES[location]:
            wonderful_rule = LOCATION_RULES[location][Category.WONDERFUL_PHOTO].resolve(world)

        multiple_rule = False_().resolve(world)
        if shot.multiple > 0 and Category.MULTIPLE_PHOTO in LOCATION_RULES[location]:
            multiple_rule = LOCATION_RULES[location][Category.MULTIPLE_PHOTO].resolve(world)

        base_rule = rule.resolve(world)
        if base_rule.always_false: return None

        return base_rule, wonderful_rule, multiple_rule, int(shot.size * fudge) + pose_score + special_score, shot.wonderful, int(shot.multiple * fudge)

    class Resolved(Rule.Resolved):
        score_goal: int
        wonderful_requirement: Rule.Resolved
        multiple_requirement: Rule.Resolved
        multiple_without_wonderful: bool
        species_data: tuple[tuple[tuple[Rule.Resolved, Rule.Resolved, Rule.Resolved, int, bool, int], ...], ...]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            return self.achievable_total(state, goal=self.score_goal) >= self.score_goal

        def achievable_total(self, state: CollectionState, goal: int | None = None) -> int:
            total = 0
            for shots in self.species_data:
                total += max((self.achievable_score(state, *shot) for shot in shots), default=0)
                if goal is not None and total >= goal: break
            return total

        def achievable_score(self, state: CollectionState, shot_rule: Rule.Resolved, wdfl_rule: Rule.Resolved, mult_rule: Rule.Resolved, base_score: int, is_wonderful: bool, multiple_score: int) -> int:
            if not shot_rule(state): return 0
            scored_wonderful = is_wonderful and self.wonderful_requirement(state) and wdfl_rule(state)
            scored_multiple = multiple_score > 0 and self.multiple_requirement(state) and mult_rule(state) and (self.multiple_without_wonderful or scored_wonderful)

            score = base_score
            if scored_wonderful: score *= 2
            if scored_multiple:  score += multiple_score
            return score


@dataclass()
class HasFilm(Rule["PokemonSnapWorld"], game="Pokemon Snap"):
    film_requirement: int

    @override
    def _instantiate(self, world: "PokemonSnapWorld") -> Rule.Resolved:
        return self.Resolved(self.film_requirement,
                             world.options.starting_film.value,
                             world.options.film_upgrade_amount.value,
                             world.options.maximum_film.value,
                             player=world.player)

    class Resolved(Rule.Resolved):
        film_requirement: int
        film_start: int
        film_step: int
        film_cap: int

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            upgrade_count = state.count(FILM_UPGRADE, self.player)
            total_film = min(self.film_cap, self.film_start + upgrade_count * self.film_step)
            return total_film >= self.film_requirement


_CAN_REACH_ALL_POKEMON = [
    CanReachLocation(pokemon_name)
    for pokemon_name in ALL_INGAME_POKEMON
    if pokemon_name not in POKEMON_IN_MULTIPLE_LEVELS
] + [
    Or(*[
        CanReachLocation(course(pokemon_name, level))
        for level in levels
    ])
    for pokemon_name, levels in POKEMON_IN_MULTIPLE_LEVELS.items()
]


LOCATION_RULES = {
    ###########
    ## Beach ##
    ###########
    # Pokemon
    BUTTERFREE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    PIDGEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    MEOWTH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    DODUO: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    CHANSEY: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    KANGASKHAN: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    SCYTHER: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_BEACH),
    },
    LAPRAS: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
    },
    EEVEE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SNORLAX: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_BEACH) | has(POKEFLUTE, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_BEACH) | has(POKEFLUTE, LVL_BEACH),
    },
    course(PIKACHU, LVL_BEACH): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_BEACH),
    },
    course(MAGIKARP, LVL_BEACH): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH),
    },
    # Special Poses
    SURFING_PIKACHU:     { Category.SPECIAL_POSE: has(POKEMON_FOOD, LVL_BEACH) },
    PIKACHU_ON_A_STUMP:  { Category.SPECIAL_POSE: has(PESTER_BALL, LVL_BEACH) },
    GUST_USING_PIDGEY:   { Category.SPECIAL_POSE: _NO_ITEMS },
    # Environment
    BEACH_SIGN:          { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    # Regular Poses
    PIDGEY_SCREECH:             { Category.REGULAR_POSE: _NO_ITEMS },
    MEOWTH_FUNNY:               { Category.REGULAR_POSE: _NO_ITEMS },
    MEOWTH_FAINTED:             { Category.REGULAR_POSE: _NO_ITEMS },
    MEOWTH_PESTER:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_BEACH) },
    MEOWTH_DANCING:             { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH) | has(POKEFLUTE, LVL_BEACH) },
    DODUO_HIT:                  { Category.REGULAR_POSE: (Has(DASH_ENGINE) | _HARD_LOGIC_ON) & (has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH)) },
    DODUO_FAINTED:              { Category.REGULAR_POSE: (Has(DASH_ENGINE) | _HARD_LOGIC_ON) & (has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH)) },
    DODUO_WAKING:               { Category.REGULAR_POSE: (Has(DASH_ENGINE) | _HARD_LOGIC_ON) & (has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH)) },
    CHANSEY_FUNNY:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH) },
    CHANSEY_JOLLY:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) },
    KANGASKHAN_ANGRY:           { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH) },
    KANGASKHAN_DANCE:           { Category.REGULAR_POSE: has(POKEFLUTE, LVL_BEACH) & (has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH)) },
    SCYTHER_FIGHTING:           { Category.REGULAR_POSE: has(PESTER_BALL, LVL_BEACH) },
    LAPRAS_RELAXED:             { Category.REGULAR_POSE: HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON) },
    EEVEE_HAPPY:                { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) },
    SNORLAX_FOR_SURE:           { Category.REGULAR_POSE: has(POKEFLUTE, LVL_BEACH) },
    SNORLAX_JOLLY:              { Category.REGULAR_POSE: has(POKEFLUTE, LVL_BEACH) },
    SNORLAX_WAKING:             { Category.REGULAR_POSE: has(POKEFLUTE, LVL_BEACH) },
    SNORLAX_SCRATCHING:         { Category.REGULAR_POSE: has(PESTER_BALL, LVL_BEACH) },
    PIKACHU_BEACH_ZAPS_EVEN_ME: { Category.REGULAR_POSE: has(POKEFLUTE, LVL_BEACH) },
    PIKACHU_BEACH_VERY_LIVELY:  { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_BEACH) | has(PESTER_BALL, LVL_BEACH) }, 
    MAGIKARP_BEACH_GOOD_SPLASH: { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_BEACH)) },


    ############
    ## Tunnel ##
    ############
    # Pokemon
    KAKUNA: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL) | Has(DASH_ENGINE)) | _SEPARATE_SCORING | _HARD_LOGIC_ON,
    },
    DIGLETT: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    DUGTRIO: {
        Category.NORMAL_PHOTO:    HasFilm(5) | (HasFilm(4) & _HARD_LOGIC_ON),
        Category.WONDERFUL_PHOTO: HasFilm(5) | (HasFilm(4) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(7) | (HasFilm(5) & _HARD_LOGIC_ON),
    },
    MAGNEMITE: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_TUNNEL),
    },
    MAGNETON: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL),
    },
    HAUNTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    ELECTRODE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    ELECTABUZZ: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        # Without Zapdos you have to ignore the first Buzz and throw at the second - spoiler in doc
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL)
    },
    ZAPDOS: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL),
    },
    course(ZUBAT, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(MAGIKARP, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(PIKACHU, LVL_TUNNEL): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    # Special Poses
    PIKACHU_ON_A_BALL: { Category.SPECIAL_POSE: HasFilm(5) | (HasFilm(3) & _HARD_LOGIC_ON) },
    TUNNEL_SIGN:       { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(POKEMON_FOOD, LVL_TUNNEL) & has(POKEFLUTE, LVL_TUNNEL) },
    # Environment
    LVL_TUNNEL:        { Category.SECRET_EXIT: has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL) },
    # Regular Poses
    ELECTRODE_ROLLING:           { Category.REGULAR_POSE: _NO_ITEMS },
    ELECTRODE_EXPLODED:          { Category.REGULAR_POSE: _NO_ITEMS },
    ELECTABUZZ_BLAST:            { Category.REGULAR_POSE: _NO_ITEMS },
    ELECTABUZZ_FAINTED:          { Category.REGULAR_POSE: _NO_ITEMS },
    ELECTABUZZ_PESTER:           { Category.REGULAR_POSE: has(PESTER_BALL, LVL_TUNNEL) },
    ELECTABUZZ_ANGRY:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_TUNNEL) | has(PESTER_BALL, LVL_TUNNEL) },
    ELECTABUZZ_YUMMY:            { Category.REGULAR_POSE: CanReachLocation(ZAPDOS) & has(POKEMON_FOOD, LVL_TUNNEL) },
    PIKACHU_TUNNEL_ZAPS_EVEN_ME: { Category.REGULAR_POSE: has(POKEFLUTE, LVL_TUNNEL) },
    PIKACHU_TUNNEL_VERY_LIVELY:  { Category.REGULAR_POSE: CanReachLocation(ZAPDOS) },
    PIKACHU_TUNNEL_THATS_PIKA:   { Category.REGULAR_POSE: CanReachLocation(ZAPDOS) },
    ZAPDOS_THUNDER:              { Category.REGULAR_POSE: CanReachLocation(ZAPDOS) },
    MAGIKARP_TUNNEL_SPLASHED:    { Category.REGULAR_POSE: _NO_ITEMS },
    DIGLETT_POP_UP:              { Category.REGULAR_POSE: _NO_ITEMS },
    DIGLETT_UNDERGROUND:         { Category.REGULAR_POSE: _NO_ITEMS },
    DUGTRIO_POP_UP:              { Category.REGULAR_POSE: CanReachLocation(DUGTRIO) },
    DUGTRIO_UNDERGROUND:         { Category.REGULAR_POSE: CanReachLocation(DUGTRIO) },
    MAGNEMITE_HAPPY:             { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_TUNNEL) },

    #############
    ## Volcano ##
    #############
    # Pokemon
    CHARMANDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | [_SEPARATE_SCORING, _RNG_LOCATIONS_ON] | _HARD_LOGIC_ON,
    },
    CHARMELEON: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    CHARIZARD: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    VULPIX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | _SEPARATE_SCORING | (Has(DASH_ENGINE) & _HARD_LOGIC_ON),
    },
    GROWLITHE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VOLCANO),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VOLCANO) & has(PESTER_BALL, LVL_VOLCANO)) | (has(PESTER_BALL, LVL_VOLCANO) & _SEPARATE_SCORING),
    },
    ARCANINE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VOLCANO),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VOLCANO) & has(PESTER_BALL, LVL_VOLCANO)) | (has(PESTER_BALL, LVL_VOLCANO) & _SEPARATE_SCORING),
    },
    RAPIDASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    MAGMAR: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        # This _might_ be possible without moving the Moltres egg, but I don't think you can get close enough
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    MOLTRES: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    course(MAGIKARP, LVL_VOLCANO): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO),
    },
    # Special Poses
    FIGHTING_MAGMAR: { Category.SPECIAL_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    # Environment
    VOLCANO_SIGN:    { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(PESTER_BALL, LVL_VOLCANO) },
    # Regular Poses
    RAPIDASH_NEIGHING:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    VULPIX_PESTER:                { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) },
    VULPIX_HAPPY:                 { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    CHARMANDER_UNSTABLE:          { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    CHARMANDER_HMM:               { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    CHARMANDER_PESTER:            { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) },
    CHARMANDER_HAPPY:             { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    CHARMELEON_FALL:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) },
    CHARMELEON_FAINTED:           { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) },
    CHARMELEON_AWOKEN:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    CHARMELEON_ROARING:           { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    MAGMAR_UNSTABLE:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    MAGMAR_PRETTY_FUNNY:          { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    MAGMAR_SO_FUNNY:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) | has(PESTER_BALL, LVL_VOLCANO) },
    MAGMAR_DIZZY:                 { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    MAGMAR_HOT:                   { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VOLCANO) },
    MOLTRES_WONDERFUL:            { Category.REGULAR_POSE: CanReachLocation(MOLTRES) },
    GROWLITHE_EMBERS:             { Category.REGULAR_POSE: CanReachLocation(GROWLITHE) },
    ARCANINE_EMBERS:              { Category.REGULAR_POSE: CanReachLocation(ARCANINE) },
    MAGIKARP_VOLCANO_GOOD_SPLASH: { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_VOLCANO)) },
    CHARIZARD_SHOCKED:            { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) },
    CHARIZARD_FLAME:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VOLCANO) | has(POKEMON_FOOD, LVL_VOLCANO) },


    ###########
    ## River ##
    ###########
    # Pokemon
    METAPOD: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_RIVER) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_RIVER) | _SEPARATE_SCORING | _HARD_LOGIC_ON,
    },
    VILEPLUME: {
        Category.NORMAL_PHOTO:    has(POKEFLUTE, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEFLUTE, LVL_RIVER),
    },
    PSYDUCK: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    POLIWAG: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) | _HARD_LOGIC_ON,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    SLOWPOKE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SLOWBRO: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER),
    },
    SHELLDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | Has(DASH_ENGINE) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  Has(DASH_ENGINE) | _HARD_LOGIC_ON,
    },
    CLOYSTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    PORYGON: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_RIVER) & has(PESTER_BALL, LVL_RIVER)) | (has(PESTER_BALL, LVL_RIVER) & _SEPARATE_SCORING & _RNG_LOCATIONS_ON),
    },
    course(BULBASAUR, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER)
    },
    course(MAGIKARP, LVL_RIVER): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER),
    },
    course(PIKACHU, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    # Special Poses
    SPEED_PIKACHU: { Category.SPECIAL_POSE: HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON) | has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    # Environment
    RIVER_SIGN:    { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) & has(POKEFLUTE, LVL_RIVER) },
    LVL_RIVER:     { Category.SECRET_EXIT: has(PESTER_BALL, LVL_RIVER) },
    # Regular Poses
    MAGIKARP_RIVER_SPLASHED:      { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    MAGIKARP_RIVER_GOOD_SPLASH:   { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    MAGIKARP_RIVER_WHAT_A_SPLASH: { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_DIZZY:                { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_FAINTED:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_WAKING:               { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_JUMPING_IN:           { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_NICE_JUMP:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_JUMPING:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    POLIWAG_WHAT_A_JUMP:          { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    BULBASAUR_RIVER_PESTER:       { Category.REGULAR_POSE: has(PESTER_BALL, LVL_RIVER) },
    BULBASAUR_RIVER_HAPPY:        { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    VILEPLUME_FUN_DANCE:          { Category.REGULAR_POSE: CanReachLocation(VILEPLUME) },
    VILEPLUME_ROCKIN:             { Category.REGULAR_POSE: CanReachLocation(VILEPLUME) },
    VILEPLUME_WAKING:             { Category.REGULAR_POSE: CanReachLocation(VILEPLUME) },
    SLOWPOKE_WILL_FISH:           { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    SLOWPOKE_FISHING:             { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    SLOWPOKE_OH_A_BITE:           { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    SLOWBRO_EATING:               { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    SHELLDER_CAUGHT:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    SHELLDER_SNAPPING:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) },
    PSYDUCK_SUBMERGING:           { Category.REGULAR_POSE: Has(DASH_ENGINE) },
    PSYDUCK_UNIQUE:               { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    PSYDUCK_FALLING:              { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    PSYDUCK_NICE_JUMP:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    PSYDUCK_IT_JUMPED:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    PSYDUCK_WHAT_A_JUMP:          { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_RIVER) | has(PESTER_BALL, LVL_RIVER) },
    PORYGON_HAPPY:                { Category.REGULAR_POSE: CanReachLocation(PORYGON) & has(POKEMON_FOOD, LVL_RIVER) },
    PORYGON_LOOKS_JOLLY:          { Category.REGULAR_POSE: CanReachLocation(PORYGON) & has(POKEMON_FOOD, LVL_RIVER) },
    PORYGON_SURE_JOLLY:           { Category.REGULAR_POSE: CanReachLocation(PORYGON) & has(POKEMON_FOOD, LVL_RIVER) },
    PIKACHU_RIVER_ZAPS_EVEN_ME:   { Category.REGULAR_POSE: CanReachLocation(SPEED_PIKACHU) & has(POKEFLUTE, LVL_RIVER) },


    ##########
    ## Cave ##
    ##########
    # Pokemon
    JIGGLYPUFF: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    WEEPINBELL: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    VICTREEBEL: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    GRIMER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON),
    },
    MUK: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)),
    },
    JYNX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEFLUTE, LVL_CAVE),
    },
    DITTO: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_CAVE),
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_CAVE),
    },
    ARTICUNO: {
        Category.NORMAL_PHOTO:    has(POKEFLUTE, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEFLUTE, LVL_CAVE),
    },
    KOFFING: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(BULBASAUR, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    course(MAGIKARP, LVL_CAVE): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE),
    },
    course(PIKACHU, LVL_CAVE): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) | _HARD_LOGIC_ON,
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) | _HARD_LOGIC_ON,
    },
    course(ZUBAT, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    # Special Poses
    BALLOON_PIKACHU:     { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    FLYING_PIKACHU:      { Category.SPECIAL_POSE: (has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE)) & has(POKEFLUTE, LVL_CAVE) },
    JIGGLYPUFF_ON_STAGE: { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    JIGGLYPUFF_TRIO:     { Category.SPECIAL_POSE:  has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    # Environment
    CAVE_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    # Regular Poses
    GRIMER_HAPPY:                { Category.REGULAR_POSE: has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)) },
    MUK_HAPPY:                   { Category.REGULAR_POSE: has(PESTER_BALL, LVL_CAVE) & (HasFilm(4) | (HasFilm(2) & _HARD_LOGIC_ON)) },
    DITTO_HAPPY:                 { Category.REGULAR_POSE: has(PESTER_BALL, LVL_CAVE) & has(POKEMON_FOOD, LVL_CAVE) },
    KOFFING_WEIRD_DANCE:         { Category.REGULAR_POSE: has(POKEFLUTE, LVL_CAVE) },
    JIGGLYPUFF_DANCE:            { Category.REGULAR_POSE: CanReachLocation(JIGGLYPUFF_TRIO) },
    JIGGLYPUFF_SHAME:            { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_CAVE) | has(PESTER_BALL, LVL_CAVE) },
    JIGGLYPUFF_SINGING:          { Category.REGULAR_POSE: CanReachLocation(JIGGLYPUFF_ON_STAGE) },
    VICTREEBEL_LEAPING:          { Category.REGULAR_POSE: CanReachLocation(VICTREEBEL) },
    JYNX_JOLLY_DANCE:            { Category.REGULAR_POSE: has(POKEFLUTE, LVL_CAVE) },
    ARTICUNO_BEAUTIFUL:          { Category.REGULAR_POSE: CanReachLocation(ARTICUNO) },
    MAGIKARP_CAVE_WHAT_A_SPLASH: { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_CAVE)) },
    PIKACHU_CAVE_VERY_LIVELY:    { Category.REGULAR_POSE: CanReachLocation(course(PIKACHU, LVL_CAVE)) & has(POKEFLUTE, LVL_CAVE) },
    PIKACHU_CAVE_ZAPS_EVEN_ME:   { Category.REGULAR_POSE: CanReachLocation(course(PIKACHU, LVL_CAVE)) & has(POKEFLUTE, LVL_CAVE) },


    ############
    ## Valley ##
    ############
    # Pokemon
    SQUIRTLE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(PESTER_BALL, LVL_VALLEY) | (Has(DASH_ENGINE) & _HARD_LOGIC_ON),
    },
    SANDSHREW: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
        Category.MULTIPLE_PHOTO:  (has(POKEMON_FOOD, LVL_VALLEY) & has(PESTER_BALL, LVL_VALLEY)),
    },
    SANDSLASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: Has(DASH_ENGINE) | has(PESTER_BALL, LVL_VALLEY),
    },
    MANKEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    GEODUDE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    GRAVELER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY) | has(POKEFLUTE, LVL_VALLEY) | _HARD_LOGIC_ON,
        Category.MULTIPLE_PHOTO:  has(POKEFLUTE, LVL_VALLEY) | _HARD_LOGIC_ON,
    },
    GOLDEEN: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    STARYU: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS,
    },
    STARMIE: {
        Category.NORMAL_PHOTO:    HasFilm(5) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.WONDERFUL_PHOTO: HasFilm(7) | (HasFilm(2) & _HARD_LOGIC_ON),
        Category.MULTIPLE_PHOTO:  HasFilm(9) | (HasFilm(3) & _HARD_LOGIC_ON),
    },
    GYARADOS: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
    },
    DRATINI: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    DRAGONITE: {
        Category.NORMAL_PHOTO:    has(PESTER_BALL, LVL_VALLEY),
        Category.WONDERFUL_PHOTO: has(PESTER_BALL, LVL_VALLEY),
    },
    course(MAGIKARP, LVL_VALLEY): {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY) | Has(DASH_ENGINE),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
        Category.MULTIPLE_PHOTO:  has(POKEMON_FOOD, LVL_VALLEY) | has(PESTER_BALL, LVL_VALLEY),
    },
    # Special Poses
    GRAVELERS_GROUP_DANCE: { Category.SPECIAL_POSE: has(POKEFLUTE, LVL_VALLEY) },
    # Environment
    VALLEY_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    LVL_VALLEY:            { Category.SECRET_EXIT:  has(PESTER_BALL, LVL_VALLEY) },
    # Regular Poses
    SQUIRTLE_SHELL:                { Category.REGULAR_POSE: _NO_ITEMS },
    SQUIRTLE_WITHDRAW:             { Category.REGULAR_POSE: _NO_ITEMS },
    SQUIRTLE_PESTER:               { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    SQUIRTLE_COMING_OUT:           { Category.REGULAR_POSE: _NO_ITEMS },
    SQUIRTLE_HAPPY:                { Category.REGULAR_POSE: has(POKEMON_FOOD, LVL_VALLEY) | Has(DASH_ENGINE) | _HARD_LOGIC_ON },
    SANDSHREW_PESTER:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    SANDSHREW_JOLLY:               { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) & has(POKEMON_FOOD, LVL_VALLEY) },
    SANDSHREW_POP_UP:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    SANDSLASH_STUMBLED:            { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    SANDSLASH_GO_UNDER:            { Category.REGULAR_POSE: Has(DASH_ENGINE) | _HARD_LOGIC_ON },
    SANDSLASH_HAPPY:               { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) & has(POKEMON_FOOD, LVL_VALLEY) },
    SANDSLASH_POP_UP:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    MANKEY_PESTER:                 { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    MANKEY_IN_THE_SKY:             { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    MANKEY_BLASTED:                { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    GRAVELER_FALLING:              { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    GRAVELER_FELL:                 { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },
    GOLDEEN_SPLASHING:             { Category.REGULAR_POSE: CanReachLocation(GOLDEEN) },
    GOLDEEN_GOOD_SPLASH:           { Category.REGULAR_POSE: CanReachLocation(GOLDEEN) },
    GOLDEEN_WHAT_A:                { Category.REGULAR_POSE: CanReachLocation(GOLDEEN) },
    GYARADOS_SHOW_FACE:            { Category.REGULAR_POSE: CanReachLocation(GYARADOS) },
    GYARADOS_SCARY:                { Category.REGULAR_POSE: CanReachLocation(GYARADOS) },
    GYARADOS_FURIOUS:              { Category.REGULAR_POSE: CanReachLocation(GYARADOS) },
    GYARADOS_ASTONISHED:           { Category.REGULAR_POSE: CanReachLocation(GYARADOS) & has(PESTER_BALL, LVL_VALLEY) },
    GYARADOS_POWERFUL:             { Category.REGULAR_POSE: CanReachLocation(GYARADOS) },
    DRATINI_JUMPING:               { Category.REGULAR_POSE: _NO_ITEMS },
    DRATINI_GOOD:                  { Category.REGULAR_POSE: _NO_ITEMS },
    DRATINI_AMAZING:               { Category.REGULAR_POSE: _NO_ITEMS },
    DRAGONITE_OH_IT_IS:            { Category.REGULAR_POSE: CanReachLocation(DRAGONITE) },
    MAGIKARP_VALLEY_IT_SPLASHED:   { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_VALLEY)) },
    MAGIKARP_VALLEY_GOOD_SPLASH:   { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_VALLEY)) },
    MAGIKARP_VALLEY_WHAT_A_SPLASH: { Category.REGULAR_POSE: CanReachLocation(course(MAGIKARP, LVL_VALLEY)) },
    MAGIKARP_VALLEY_ITS_SPLASHING: { Category.REGULAR_POSE: has(PESTER_BALL, LVL_VALLEY) },

    ###################
    ## Rainbow Cloud ##
    ###################
    MEW: {
        Category.NORMAL_PHOTO:    has(POKEMON_FOOD, LVL_CLOUD) | has(PESTER_BALL, LVL_CLOUD),
        Category.WONDERFUL_PHOTO: has(POKEMON_FOOD, LVL_CLOUD) | has(PESTER_BALL, LVL_CLOUD),
    },
    # Special Poses
    RARE_POKEMON_MEW: { Category.SPECIAL_POSE: CanReachLocation(MEW) },
    # Regular Poses
    MEW_SPINNING:  { Category.REGULAR_POSE: CanReachLocation(MEW) },
    MEW_WELL_DONE: { Category.REGULAR_POSE: CanReachLocation(MEW) },
    MEW_PERFECT:   { Category.REGULAR_POSE: CanReachLocation(MEW) },

    #################
    ## Oak Rewards ##
    #################
    POKEMON_TOTAL_6:  { Category.PHOTO_COUNT: AtLeast(6,  *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_22: { Category.PHOTO_COUNT: AtLeast(22, *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_40: { Category.PHOTO_COUNT: AtLeast(40, *_CAN_REACH_ALL_POKEMON) },

    REPORT_SCORE_24_000:  { Category.REPORT_SCORE: ReportScoreAchievable( 24_000) },
    REPORT_SCORE_72_500:  { Category.REPORT_SCORE: ReportScoreAchievable( 72_500) },
    REPORT_SCORE_130_000: { Category.REPORT_SCORE: ReportScoreAchievable(130_000) },
}
