from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, HasAny, And, Rule
from .items import SIGN_PIC_NAMES
from .locations import wonderful, multiple, secret_exit, course, bonus, PokemonSnapLocationCategory as Category
from .constants import *

if TYPE_CHECKING:
    from . import PokemonSnapWorld


_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE = Has(POKEMON_FOOD)
_HAS_FLUTE = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(PESTER_BALL, POKEMON_FOOD)

location_name_functions = {
    Category.NORMAL_PHOTO: (lambda s: s),
    Category.WONDERFUL_PHOTO: wonderful,
    Category.MULTIPLE_PHOTO: multiple,
    Category.SPECIAL_POSE: (lambda s: s),
    Category.POKEMON_SIGN: (lambda s: s),
    Category.SECRET_EXIT: secret_exit,
}

def set_location_rule(world: "PokemonSnapWorld", name: str, category: Category, rule: Rule):
    try:
        name_func = location_name_functions[category]
        base_name = name_func(name)
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

    # World Location Rules
    set_beach_rules(world)
    set_tunnel_rules(world)
    set_volcano_rules(world)
    set_river_rules(world)
    set_cave_rules(world)
    set_valley_rules(world)

    # Rainbow Cloud Rules
    set_location_rule(world, MEW, Category.NORMAL_PHOTO, _HAS_PESTER)


def set_beach_rules(world: "PokemonSnapWorld"):
    set_location_rule(world, SCYTHER, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, SCYTHER, Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, CHANSEY, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, CHANSEY, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    
    set_location_rule(world, SNORLAX, Category.NORMAL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))
    set_location_rule(world, SNORLAX, Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))

    set_location_rule(world, KANGASKHAN, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, course(MAGIKARP, LVL_BEACH), Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(MAGIKARP, LVL_BEACH), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, course(PIKACHU, LVL_BEACH), Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, SURFING_PIKACHU, Category.SPECIAL_POSE, _HAS_APPLE)
    set_location_rule(world, PIKACHU_ON_A_STUMP, Category.SPECIAL_POSE, _HAS_PESTER)

    set_location_rule(world, BEACH_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))


def set_tunnel_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] mult: Technically possible without anything (difficult)
    set_location_rule(world, KAKUNA, Category.MULTIPLE_PHOTO, HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE))

    # Without Zapdos you have to ignore the first and throw at the second - spoiler in doc
    set_location_rule(world, ELECTABUZZ, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, MAGNEMITE, Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, MAGNEMITE, Category.WONDERFUL_PHOTO, _HAS_APPLE)
    set_location_rule(world, MAGNEMITE, Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, MAGNETON, Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, MAGNETON, Category.WONDERFUL_PHOTO, _HAS_APPLE)

    set_location_rule(world, ZAPDOS, Category.NORMAL_PHOTO, HasAll(POKEMON_FOOD, POKEFLUTE))
    set_location_rule(world, ZAPDOS, Category.WONDERFUL_PHOTO, HasAll(POKEMON_FOOD, POKEFLUTE))

    set_location_rule(world, TUNNEL_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE))
    set_location_rule(world, LVL_TUNNEL, Category.SECRET_EXIT, _HAS_APPLE_OR_PESTER)


def set_volcano_rules(world: "PokemonSnapWorld"):
    set_location_rule(world, CHARMANDER, Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, CHARMELEON, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, CHARMELEON, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, CHARIZARD, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, CHARIZARD, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] mult: Technically possible with dash (rng)
    set_location_rule(world, VULPIX, Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, GROWLITHE, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, GROWLITHE, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, GROWLITHE, Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, ARCANINE, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, ARCANINE, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, ARCANINE, Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, MOLTRES, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, MOLTRES, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, MAGMAR, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, course(MAGIKARP, LVL_VOLCANO), Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(MAGIKARP, LVL_VOLCANO), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, FIGHTING_MAGMAR, Category.SPECIAL_POSE, _HAS_APPLE)

    set_location_rule(world, VOLCANO_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, PESTER_BALL))


def set_river_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (rng)
    set_location_rule(world, SHELLDER, Category.WONDERFUL_PHOTO, Has(DASH_ENGINE))
    set_location_rule(world, SHELLDER, Category.MULTIPLE_PHOTO, Has(DASH_ENGINE))

    set_location_rule(world, VILEPLUME, Category.NORMAL_PHOTO, _HAS_FLUTE)
    set_location_rule(world, VILEPLUME, Category.WONDERFUL_PHOTO, _HAS_FLUTE)

    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    set_location_rule(world, METAPOD, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, METAPOD, Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, PSYDUCK, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] base: Technically possible without anything (difficult)
    set_location_rule(world, POLIWAG, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, POLIWAG, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, POLIWAG, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, SLOWBRO, Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, SLOWBRO, Category.WONDERFUL_PHOTO, _HAS_APPLE)

    set_location_rule(world, PORYGON, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, PORYGON, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, PORYGON, Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, course(BULBASAUR, LVL_RIVER), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(BULBASAUR, LVL_RIVER), Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, course(MAGIKARP, LVL_RIVER), Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(MAGIKARP, LVL_RIVER), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # Speed pikachu has no requirements, it will begin to run if you take a close picture

    set_location_rule(world, RIVER_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, POKEFLUTE))
    set_location_rule(world, LVL_RIVER,  Category.SECRET_EXIT, _HAS_PESTER)


def set_cave_rules(world: "PokemonSnapWorld"):
    set_location_rule(world, VICTREEBEL, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, VICTREEBEL, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, JIGGLYPUFF, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, DITTO, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, DITTO, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, DITTO, Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, ARTICUNO, Category.NORMAL_PHOTO, _HAS_FLUTE)
    set_location_rule(world, ARTICUNO, Category.WONDERFUL_PHOTO, _HAS_FLUTE)

    set_location_rule(world, MUK, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, MUK, Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, JYNX, Category.MULTIPLE_PHOTO, _HAS_FLUTE)

    set_location_rule(world, course(MAGIKARP, LVL_CAVE), Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(MAGIKARP, LVL_CAVE), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] base: Technically possible without anything (difficult)
    set_location_rule(world, course(PIKACHU, LVL_CAVE), Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(PIKACHU, LVL_CAVE), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, BALLOON_PIKACHU, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, FLYING_PIKACHU, Category.SPECIAL_POSE, And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER))
    set_location_rule(world, JIGGLYPUFF_ON_STAGE, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, JIGGLYPUFF_TRIO, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, CAVE_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))


def set_valley_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] wdfl: Technically possible without anything. mult: Technically possible with just dash (difficult)
    set_location_rule(world, SQUIRTLE, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, SQUIRTLE, Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, GOLDEEN, Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, GOLDEEN, Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    set_location_rule(world, GRAVELER, Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))
    set_location_rule(world, GRAVELER, Category.MULTIPLE_PHOTO, _HAS_FLUTE)

    set_location_rule(world, GYARADOS, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, GYARADOS, Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, DRAGONITE, Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, DRAGONITE, Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, SANDSHREW, Category.NORMAL_PHOTO, HasAny(PESTER_BALL, DASH_ENGINE))
    set_location_rule(world, SANDSHREW, Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, SANDSHREW, Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, SANDSLASH, Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, DASH_ENGINE))

    set_location_rule(world, DRATINI, Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, course(MAGIKARP, LVL_VALLEY), Category.NORMAL_PHOTO, HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE))
    set_location_rule(world, course(MAGIKARP, LVL_VALLEY), Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, course(MAGIKARP, LVL_VALLEY), Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, GRAVELERS_GROUP_DANCE, Category.SPECIAL_POSE, _HAS_FLUTE)

    set_location_rule(world, VALLEY_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))
    set_location_rule(world, LVL_VALLEY, Category.SECRET_EXIT, _HAS_PESTER)
