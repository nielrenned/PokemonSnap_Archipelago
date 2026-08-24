from typing import TYPE_CHECKING, override
from dataclasses import dataclass
from itertools import product

from rule_builder.rules import Has, HasAll, HasAny, And, Rule, CanReachLocation, CollectionState, False_, HasGroup
from .future_rules import AtLeast
from .items import SIGN_PIC_NAMES, POKEMON_PIC_NAMES
from .locations import wonderful, multiple, secret_exit, course, bonus, PokemonSnapLocationCategory as Category, RNG_LOCATIONS, HARD_LOCATIONS
from .pokemon_rules import SPECIES_RULE_DATA
from .constants import *
from .items import PokemonSnapItemCategory
if TYPE_CHECKING:
    from . import PokemonSnapWorld


_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE = Has(POKEMON_FOOD)
_HAS_FLUTE = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(PESTER_BALL, POKEMON_FOOD)

REPORT_EXCLUSIONS = RNG_LOCATIONS + HARD_LOCATIONS

location_name_functions = {
    Category.NORMAL_PHOTO:   (lambda s: s),
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO:  multiple,
    Category.SPECIAL_POSE:   (lambda s: s),
    Category.POKEMON_SIGN:   (lambda s: s),
    Category.SECRET_EXIT:     secret_exit,
    Category.PHOTO_COUNT:    (lambda s: s),
    Category.REPORT_SCORE:   (lambda s: s),
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

    if world.options.goal_type == GOAL_SIGN_PICS:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(f"{PokemonSnapItemCategory.SIGN_PIC}", world.options.signs_required.value))
    elif world.options.goal_type == GOAL_POKEMON_PICS:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'),
                       HasGroup(f"{PokemonSnapItemCategory.POKEMON_PIC}", world.options.pokemon_required.value))
    else:
        assert"Invalid goal type set. Must be 0 or 1."

    # Species Photo Rules
    for rules in SPECIES_RULE_DATA.values():
        for name, _, soft_logic, _ in rules:
            set_location_rule(world, name, Category.NORMAL_PHOTO, soft_logic.normal)
            if soft_logic.wonderful is not None:
                set_location_rule(world, name, Category.WONDERFUL_PHOTO, soft_logic.wonderful)
            if soft_logic.multiple is not None:
                set_location_rule(world, name, Category.MULTIPLE_PHOTO, soft_logic.multiple)

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

    set_location_rule(world, POKEMON_TOTAL_6,  Category.PHOTO_COUNT, AtLeast(6,  *can_reach_all_pokemon))
    set_location_rule(world, POKEMON_TOTAL_22, Category.PHOTO_COUNT, AtLeast(22, *can_reach_all_pokemon))
    set_location_rule(world, POKEMON_TOTAL_40, Category.PHOTO_COUNT, AtLeast(40, *can_reach_all_pokemon))

    set_location_rule(world, REPORT_SCORE_24_000,  Category.REPORT_SCORE, ReportScoreAchievable( 24_000))
    set_location_rule(world, REPORT_SCORE_72_500,  Category.REPORT_SCORE, ReportScoreAchievable( 72_500))
    set_location_rule(world, REPORT_SCORE_130_000, Category.REPORT_SCORE, ReportScoreAchievable(130_000))


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
                if not any(species_data.name == location_name for species_data in SPECIES_RULE_DATA[level_name]): continue

                this_pokemon_rules.append(self.build_rules_triplet(world, location_name))
            all_pokemon_rules.append(tuple(this_pokemon_rules))

        return self.Resolved(self.score_goal, tuple(all_pokemon_rules), player=world.player)

    def build_rules_triplet(self, world: "PokemonSnapWorld", location: str):
        species_data = [species_data for region in SPECIES_RULE_DATA for species_data in SPECIES_RULE_DATA[region] if species_data.name == location][0]
        
        normal_rule = CanReachLocation(location_name(location, Category.NORMAL_PHOTO))

        wonderful_rule = False_()
        if species_data.soft_logic.wonderful is not None and wonderful(location) not in REPORT_EXCLUSIONS:
            wonderful_rule = And(normal_rule, species_data.soft_logic.wonderful)

        multiple_rule = False_()
        if species_data.soft_logic.multiple is not None and multiple(location) not in REPORT_EXCLUSIONS:
            multiple_rule = And(wonderful_rule, species_data.soft_logic.multiple)

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
    SURFING_PIKACHU:    { Category.SPECIAL_POSE: _HAS_APPLE },
    PIKACHU_ON_A_STUMP: { Category.SPECIAL_POSE: _HAS_PESTER },
    BEACH_SIGN:         { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },

    # Tunnel
    TUNNEL_SIGN: { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE) },
    LVL_TUNNEL:  { Category.SECRET_EXIT: _HAS_APPLE_OR_PESTER },

    # Volcano
    FIGHTING_MAGMAR: { Category.SPECIAL_POSE: _HAS_APPLE },
    VOLCANO_SIGN:    { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, PESTER_BALL) },

    # River
    RIVER_SIGN: { Category.POKEMON_SIGN: HasAll(SIGN_DETECTOR, POKEFLUTE) },
    LVL_RIVER:  { Category.SECRET_EXIT: _HAS_PESTER },

    # Cave
    BALLOON_PIKACHU:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    FLYING_PIKACHU:      { Category.SPECIAL_POSE: And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER) },
    JIGGLYPUFF_ON_STAGE: { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    JIGGLYPUFF_TRIO:     { Category.SPECIAL_POSE: _HAS_APPLE_OR_PESTER },
    CAVE_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },

    # Valley
    GRAVELERS_GROUP_DANCE: { Category.SPECIAL_POSE: _HAS_FLUTE },
    VALLEY_SIGN:           { Category.POKEMON_SIGN: Has(SIGN_DETECTOR) },
    LVL_VALLEY:            { Category.SECRET_EXIT:  _HAS_PESTER },
}
