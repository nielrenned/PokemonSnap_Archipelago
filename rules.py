from typing import TYPE_CHECKING, override
from dataclasses import dataclass
from itertools import product

from rule_builder.rules import Has, HasAll, HasAny, And, Rule, AtLeast, CanReachLocation, CollectionState, False_
from .items import SIGN_PIC_NAMES
from .locations import wonderful, multiple, secret_exit, course, bonus, PokemonSnapLocationCategory as Category, species_data_tables, RNG_LOCATIONS, HARD_LOCATIONS
from .constants import *

if TYPE_CHECKING:
    from . import PokemonSnapWorld


_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE = Has(POKEMON_FOOD)
_HAS_FLUTE = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(PESTER_BALL, POKEMON_FOOD)

REPORT_EXCLUSIONS = RNG_LOCATIONS + HARD_LOCATIONS

location_name_functions = {
    Category.NORMAL_PHOTO: (lambda s: s),
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO:  multiple,
    Category.SPECIAL_POSE: (lambda s: s),
    Category.POKEMON_SIGN: (lambda s: s),
    Category.SECRET_EXIT: secret_exit,
    Category.OAK_REWARD: (lambda s: s),
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

def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level))

    world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'), HasAll(*SIGN_PIC_NAMES))

    # World location rules
    for name, categories in LOCATION_RULES.items():
        for category, rule in categories.items():
            set_location_rule(world, name, category, rule)

    set_oak_rules(world)


def set_oak_rules(world: "PokemonSnapWorld"):
    can_reach_all_pokemon = [
        CanReachLocation(pokemon_name)
        for pokemon_name in ALL_INGAME_POKEMON
        if pokemon_name not in POKEMON_IN_MULTIPLE_LEVELS
    ] + [
        CanReachLocation(course(pokemon_name, level))
        for pokemon_name, level in product(POKEMON_IN_MULTIPLE_LEVELS, ALL_LEVELS)
        if course(pokemon_name, level) in LOCATION_RULES
    ]

    set_location_rule(world, POKEMON_TOTAL_6, Category.OAK_REWARD, AtLeast(6, *can_reach_all_pokemon))
    set_location_rule(world, POKEMON_TOTAL_22, Category.OAK_REWARD, AtLeast(22, *can_reach_all_pokemon))
    set_location_rule(world, POKEMON_TOTAL_40, Category.OAK_REWARD, AtLeast(40, *can_reach_all_pokemon))

    set_location_rule(world, REPORT_SCORE_24_000, Category.OAK_REWARD, ReportScoreAchievable( 24_000))
    set_location_rule(world, REPORT_SCORE_72_500, Category.OAK_REWARD, ReportScoreAchievable( 72_500))
    set_location_rule(world, REPORT_SCORE_130_000, Category.OAK_REWARD, ReportScoreAchievable(130_000))


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
                wonderful_rule = And(normal_rule, LOCATION_RULES[location][Category.WONDERFUL_PHOTO])

        multiple_rule = False_()
        if species_data.multiple and multiple(location) not in REPORT_EXCLUSIONS:
            if (location not in LOCATION_RULES or Category.MULTIPLE_PHOTO not in LOCATION_RULES[location]):
                multiple_rule = wonderful_rule
            else:
                multiple_rule = And(wonderful_rule, LOCATION_RULES[location][Category.MULTIPLE_PHOTO])

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

LOCATION_RULES = {
    # Beach
    SCYTHER: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    CHANSEY: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER
    },
    SNORLAX: {
        Category.NORMAL_PHOTO:    HasAny(PESTER_BALL, POKEFLUTE),
        Category.WONDERFUL_PHOTO: HasAny(PESTER_BALL, POKEFLUTE),
    },
    KANGASKHAN: {
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER
    },
    course(MAGIKARP, LVL_BEACH): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER
    },
    course(PIKACHU, LVL_BEACH): {
        Category.MULTIPLE_PHOTO:  _HAS_PESTER
    },
    SURFING_PIKACHU:    { Category.SPECIAL_POSE: _HAS_APPLE },
    PIKACHU_ON_A_STUMP: { Category.SPECIAL_POSE: _HAS_PESTER },
    BEACH_SIGN:         { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Tunnel
    KAKUNA: {
        Category.MULTIPLE_PHOTO:  HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE),
    },
    # Without Zapdos you have to ignore the first Buzz and throw at the second - spoiler in doc
    ELECTABUZZ: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    MAGNEMITE: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE,
    },
    MAGNETON: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
    },
    ZAPDOS: {
        Category.NORMAL_PHOTO:    HasAll(POKEMON_FOOD, POKEFLUTE),
        Category.WONDERFUL_PHOTO: HasAll(POKEMON_FOOD, POKEFLUTE),
    },
    TUNNEL_SIGN: { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE) },
    LVL_TUNNEL:  { Category.SECRET_EXIT: _HAS_APPLE_OR_PESTER },


    # Volcano
    CHARMANDER: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE,
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
        Category.MULTIPLE_PHOTO:  _HAS_APPLE,
    },
    GROWLITHE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(PESTER_BALL, POKEMON_FOOD),
    },
    ARCANINE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(PESTER_BALL, POKEMON_FOOD),
    },
    MOLTRES: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    MAGMAR: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    course(MAGIKARP, LVL_VOLCANO): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    FIGHTING_MAGMAR: { Category.SPECIAL_POSE: _HAS_APPLE },
    VOLCANO_SIGN:    { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, PESTER_BALL) },


    # River
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (rng)
    SHELLDER: {
        Category.WONDERFUL_PHOTO: Has(DASH_ENGINE),
        Category.MULTIPLE_PHOTO:  Has(DASH_ENGINE),
    },
    VILEPLUME: {
        Category.NORMAL_PHOTO:    _HAS_FLUTE,
        Category.WONDERFUL_PHOTO: _HAS_FLUTE,
    },
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    METAPOD: {
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER,
    },
    PSYDUCK: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    POLIWAG: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    SLOWBRO: {
        Category.NORMAL_PHOTO:    _HAS_APPLE,
        Category.WONDERFUL_PHOTO: _HAS_APPLE,
    },
    PORYGON: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(PESTER_BALL, POKEMON_FOOD),
    },
    course(BULBASAUR, LVL_RIVER): {
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    course(MAGIKARP, LVL_RIVER): {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    RIVER_SIGN: { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEFLUTE) },
    LVL_RIVER:  { Category.SECRET_EXIT: _HAS_PESTER },


    # Cave
    VICTREEBEL: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    JIGGLYPUFF: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    DITTO: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER,
    },
    ARTICUNO: {
        Category.NORMAL_PHOTO:    _HAS_FLUTE,
        Category.WONDERFUL_PHOTO: _HAS_FLUTE,
    },
    MUK: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    JYNX: {
        Category.MULTIPLE_PHOTO:  _HAS_FLUTE,
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
    BALLOON_PIKACHU:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    FLYING_PIKACHU:      { Category.SPECIAL_POSE: And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER) },
    JIGGLYPUFF_ON_STAGE: { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    JIGGLYPUFF_TRIO:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    CAVE_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },


    # Valley
    # TODO: [SOFT] wdfl: Technically possible without anything. mult: Technically possible with just dash (difficult)
    SQUIRTLE: {
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_PESTER,
    },
    GOLDEEN: {
        Category.NORMAL_PHOTO:    _HAS_APPLE_OR_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
    },
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    GRAVELER: {
        Category.WONDERFUL_PHOTO: HasAny(PESTER_BALL, POKEFLUTE),
        Category.MULTIPLE_PHOTO:  _HAS_FLUTE,
    },
    GYARADOS: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    DRAGONITE: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
    },
    SANDSHREW: {
        Category.NORMAL_PHOTO:    _HAS_PESTER,
        Category.WONDERFUL_PHOTO: _HAS_PESTER,
        Category.MULTIPLE_PHOTO:  HasAll(PESTER_BALL, POKEMON_FOOD),
    },
    SANDSLASH: {
        Category.WONDERFUL_PHOTO: HasAny(PESTER_BALL, DASH_ENGINE),
    },
    DRATINI: {
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    course(MAGIKARP, LVL_VALLEY): {
        Category.NORMAL_PHOTO:    HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE),
        Category.WONDERFUL_PHOTO: _HAS_APPLE_OR_PESTER,
        Category.MULTIPLE_PHOTO:  _HAS_APPLE_OR_PESTER,
    },
    GRAVELERS_GROUP_DANCE: { Category.SPECIAL_POSE: _HAS_FLUTE },
    VALLEY_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    LVL_VALLEY:            { Category.SECRET_EXIT:  _HAS_PESTER },

    # Cloud
    MEW: { Category.NORMAL_PHOTO:    _HAS_PESTER }
}
