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
    Category.MULTIPLE_PHOTO:  multiple,
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

    # World location rules
    for name, categories in LOCATION_RULES.items():
        for category, rule in categories.items():
            set_location_rule(world, name, category, rule)


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
        Category.NORMAL_PHOTO:    HasAny(PESTER_BALL, DASH_ENGINE),
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