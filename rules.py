from typing import TYPE_CHECKING, override
from dataclasses import dataclass

from rule_builder.rules import Rule, True_, False_, And, Or, Has, HasAll, HasAny, HasGroup, CanReachLocation, CollectionState, OptionFilter
from .future_rules import AtLeast
from .locations import wonderful, multiple, secret_exit, course, bonus, species_data_tables, \
    PokemonSnapLocationCategory as Category, RNG_LOCATIONS, HARD_LOCATIONS, POKEMON_IN_MULTIPLE_LEVELS
from .constants import *
from .items import PokemonSnapItemCategory as ItemCategory
from .options import GoalType, ScoringBonus
if TYPE_CHECKING:
    from . import PokemonSnapWorld

_NO_ITEMS   = True_()
_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE  = Has(POKEMON_FOOD)
_HAS_FLUTE  = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(POKEMON_FOOD, PESTER_BALL)

_SEPARATE_SCORING = OptionFilter(ScoringBonus, ScoringBonus.option_separate)

REPORT_EXCLUSIONS = RNG_LOCATIONS + HARD_LOCATIONS

_identity = lambda s: s

location_name_functions = {
    Category.NORMAL_PHOTO:    _identity,
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO:  multiple,
    Category.SPECIAL_POSE:    _identity,
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
    if world.options.scoring_bonuses == ScoringBonus.option_progressive:
        return Has(PROG_SCORING, 1)
    elif world.options.scoring_bonuses == ScoringBonus.option_separate:
        return Has(WDFL_SCORING)
    
    return _NO_ITEMS

def multiple_requirement(world: "PokemonSnapWorld"):
    if world.options.scoring_bonuses == ScoringBonus.option_progressive:
        return Has(PROG_SCORING, 2)
    elif world.options.scoring_bonuses == ScoringBonus.option_separate:
        return Has(MULT_SCORING)

    return _NO_ITEMS

def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level))

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
    """
    This is hacky at best, but works for now. 

    In _instantiate, for each pokemon, we create a list of location rules
    that are independent of the world options (otherwise wonderful/multiple 
    would be inaccessible). This list is passed to the Resolved rule. This
    will probably need to be revisited when we add progressive lenses.

    In the resolved rule, we heuristically estimate an upper bound for
    the achievable score given the current game state, based on some
    crude estimates for each line on the score sheet. Notably, we are
    ignoring special poses. This is potentially a To-Do, but I think
    the logic will actually be nicer without it.
    """
    score_goal: int

    @override
    def _instantiate(self, world: "PokemonSnapWorld") -> Rule.Resolved:
        all_pokemon_rules = [
            (self.build_rules_triplet(world, pokemon_name), ) # 1-tuple for pokemon only in one course
            for pokemon_name in ALL_INGAME_POKEMON
            if pokemon_name not in POKEMON_IN_MULTIPLE_LEVELS
        ]

        for pokemon_name in POKEMON_IN_MULTIPLE_LEVELS:
            this_pokemon_rules = []
            for level_name in ALL_LEVELS:
                location_name = course(pokemon_name, level_name)
                if location_name not in LOCATION_RULES: continue

                this_pokemon_rules.append(self.build_rules_triplet(world, location_name))
            all_pokemon_rules.append(tuple(this_pokemon_rules))

        return self.Resolved(self.score_goal, tuple(all_pokemon_rules), player=world.player)

    def build_rules_triplet(self, world: "PokemonSnapWorld", location: str):
        species_data = [species_data for region in species_data_tables for species_data in species_data_tables[region] if species_data.name == location][0]
        
        normal_rule = CanReachLocation(location_name(location, Category.NORMAL_PHOTO))

        wonderful_rule = False_()
        if species_data.wonderful and wonderful(location) not in REPORT_EXCLUSIONS:
            if (location not in LOCATION_RULES or Category.WONDERFUL_PHOTO not in LOCATION_RULES[location]):
                wonderful_rule = normal_rule
            else:
                wonderful_rule = And(normal_rule, LOCATION_RULES[location][Category.WONDERFUL_PHOTO], wonderful_requirement(world))

        multiple_rule = False_()
        if species_data.multiple and multiple(location) not in REPORT_EXCLUSIONS:
            access_requirement = wonderful_rule | (normal_rule & _SEPARATE_SCORING)
            if (location not in LOCATION_RULES or Category.MULTIPLE_PHOTO not in LOCATION_RULES[location]):
                multiple_rule = access_requirement
            else:
                multiple_rule = And(access_requirement, LOCATION_RULES[location][Category.MULTIPLE_PHOTO], multiple_requirement(world))

        return normal_rule.resolve(world), wonderful_rule.resolve(world), multiple_rule.resolve(world)

    class Resolved(Rule.Resolved):
        score_goal: int
        all_pokemon_rules: tuple[tuple[tuple[Rule.Resolved, Rule.Resolved, Rule.Resolved]]]

        @override
        def _evaluate(self, state: CollectionState) -> bool:
            achievable_score_total = 0
            for rule_set in self.all_pokemon_rules:
                achievable_score_total += max((self.achievable_score(state, *rule_tuple) for rule_tuple in rule_set), default=0)
                if achievable_score_total >= self.score_goal: return True
            return False

        def achievable_score(self, state: CollectionState, normal_rule: Rule.Resolved, wonderful_rule: Rule.Resolved, multiple_rule: Rule.Resolved):
            # This is a heuristic, as it can change drastically between pokemon
            if not normal_rule(state): return 0

            score = 200
            if wonderful_rule(state):
                score += 900 # 150 more for size, and 750 more for pose
                score *= 2
            if multiple_rule(state):
                score += 150

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
    # Beach
    BUTTERFREE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    PIDGEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
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
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    KANGASKHAN: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    SCYTHER: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    LAPRAS: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    EEVEE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SNORLAX: {
        Category.NORMAL_PHOTO:    HasAny(PESTER_BALL, POKEFLUTE),
        Category.WONDERFUL_PHOTO: HasAny(PESTER_BALL, POKEFLUTE),
    },
    course(PIKACHU, LVL_BEACH): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER, # TODO: validate
    },
    course(MAGIKARP, LVL_BEACH): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    SURFING_PIKACHU:    { Category.SPECIAL_POSE: _HAS_APPLE },
    PIKACHU_ON_A_STUMP: { Category.SPECIAL_POSE: _HAS_PESTER },
    GUST_USING_PIDGEY:  { Category.SPECIAL_POSE: _NO_ITEMS },
    BEACH_SIGN:         { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Tunnel
    # TODO: [SOFT] mult: Technically possible without anything (difficult)
    KAKUNA: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  HasAny(POKEMON_FOOD, DASH_ENGINE, PESTER_BALL) | _SEPARATE_SCORING, # TODO: validate
    },
    DIGLETT: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    DUGTRIO: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    MAGNEMITE: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE, # TODO: validate
    },
    MAGNETON: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
    },
    HAUNTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    ELECTRODE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    ELECTABUZZ: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        # Without Zapdos you have to ignore the first Buzz and throw at the second - spoiler in doc
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER | _SEPARATE_SCORING # TODO: validate
    },
    ZAPDOS: {
        Category.NORMAL_PHOTO:    HasAll(POKEMON_FOOD, POKEFLUTE),
        Category.WONDERFUL_PHOTO: HasAll(POKEMON_FOOD, POKEFLUTE),
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
    PIKACHU_ON_A_BALL: { Category.SPECIAL_POSE: _NO_ITEMS },
    TUNNEL_SIGN:       { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE) },
    LVL_TUNNEL:        { Category.SECRET_EXIT: _HAS_APPLE_OR_PESTER },


    # Volcano
    CHARMANDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE | _SEPARATE_SCORING, # TODO: validate
    },
    CHARMELEON: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    CHARIZARD: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    # TODO: [SOFT] mult: Technically possible with dash (rng)
    VULPIX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE | _SEPARATE_SCORING, # TODO: validate
    },
    GROWLITHE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(POKEMON_FOOD, PESTER_BALL) | (_HAS_PESTER & _SEPARATE_SCORING), # TODO: validate
    },
    ARCANINE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(POKEMON_FOOD, PESTER_BALL) | (_HAS_PESTER & _SEPARATE_SCORING), # TODO: validate
    },
    RAPIDASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    MAGMAR: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER | _SEPARATE_SCORING, # TODO: validate
    },
    MOLTRES: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    course(MAGIKARP, LVL_VOLCANO): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    FIGHTING_MAGMAR: { Category.SPECIAL_POSE: _HAS_APPLE },
    VOLCANO_SIGN:    { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, PESTER_BALL) },


    # River
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    METAPOD: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER, # TODO: validate
    },
    VILEPLUME: {
        Category.NORMAL_PHOTO:    _HAS_FLUTE,
        Category.WONDERFUL_PHOTO: _HAS_FLUTE,
    },
    PSYDUCK: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER, # TODO: validate
    },
    # TODO: [SOFT] base: Technically possible without anything (difficult)
    POLIWAG: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER, # TODO: validate
    },
    SLOWPOKE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SLOWBRO: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
    },
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (rng)
    SHELLDER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: Has(DASH_ENGINE),
        Category.MULTIPLE_PHOTO:  Has(DASH_ENGINE) | _SEPARATE_SCORING, # TODO: validate
    },
    CLOYSTER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    PORYGON: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(POKEMON_FOOD, PESTER_BALL)  | (_HAS_PESTER & _SEPARATE_SCORING), # TODO: validate
    },
    course(BULBASAUR, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER | _SEPARATE_SCORING, # TODO: validate
    },
    course(MAGIKARP, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    course(PIKACHU, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    SPEED_PIKACHU: { Category.SPECIAL_POSE: _NO_ITEMS },
    RIVER_SIGN:    { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEFLUTE) },
    LVL_RIVER:     { Category.SECRET_EXIT: _HAS_PESTER },


    # Cave
    JIGGLYPUFF: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER, # TODO: validate
    },
    WEEPINBELL: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    VICTREEBEL: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    GRIMER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    MUK: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    JYNX: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_FLUTE | _SEPARATE_SCORING, # TODO: validate
    },
    DITTO: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER, # TODO: validate
    },
    ARTICUNO: {
        Category.NORMAL_PHOTO:    _HAS_FLUTE,
        Category.WONDERFUL_PHOTO: _HAS_FLUTE,
    },
    KOFFING: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    course(BULBASAUR, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    course(MAGIKARP, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    # TODO: [SOFT] base: Technically possible without anything (difficult)
    course(PIKACHU, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    course(ZUBAT, LVL_CAVE): {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    BALLOON_PIKACHU:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    FLYING_PIKACHU:      { Category.SPECIAL_POSE: And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER) },
    JIGGLYPUFF_ON_STAGE: { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    JIGGLYPUFF_TRIO:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    CAVE_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Valley
    # TODO: [SOFT] wdfl: Technically possible without anything. mult: Technically possible with just dash (difficult)
    SQUIRTLE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER | _SEPARATE_SCORING, # TODO: validate
    },
    SANDSHREW: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(POKEMON_FOOD, PESTER_BALL), # TODO: validate
    },
    SANDSLASH: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasAny(DASH_ENGINE, PESTER_BALL),
    },
    MANKEY: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
    },
    GEODUDE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    GRAVELER: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: HasAny(PESTER_BALL, POKEFLUTE),
        Category.MULTIPLE_PHOTO:  _HAS_FLUTE | _SEPARATE_SCORING, # TODO: validate
    },
    GOLDEEN: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    STARYU: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    STARMIE: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _NO_ITEMS, # TODO: validate
    },
    GYARADOS: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    DRATINI: {
        Category.NORMAL_PHOTO:    _NO_ITEMS,
        Category.WONDERFUL_PHOTO: _NO_ITEMS,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER, # TODO: validate
    },
    DRAGONITE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    course(MAGIKARP, LVL_VALLEY): {
        Category.NORMAL_PHOTO:    HasAny(POKEMON_FOOD, DASH_ENGINE, PESTER_BALL),
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER, # TODO: validate
    },
    GRAVELERS_GROUP_DANCE: { Category.SPECIAL_POSE: _HAS_FLUTE },
    VALLEY_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    LVL_VALLEY:            { Category.SECRET_EXIT:  _HAS_PESTER },

    # Cloud
    # Rainbow Cloud
    MEW: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER
    },

    # Oak Rewards
    POKEMON_TOTAL_6:  { Category.PHOTO_COUNT: AtLeast(6,  *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_22: { Category.PHOTO_COUNT: AtLeast(22, *_CAN_REACH_ALL_POKEMON) },
    POKEMON_TOTAL_40: { Category.PHOTO_COUNT: AtLeast(40, *_CAN_REACH_ALL_POKEMON) },

    REPORT_SCORE_24_000:  { Category.REPORT_SCORE: ReportScoreAchievable( 24_000) },
    REPORT_SCORE_72_500:  { Category.REPORT_SCORE: ReportScoreAchievable( 72_500) },
    REPORT_SCORE_130_000: { Category.REPORT_SCORE: ReportScoreAchievable(130_000) },
}
