from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, HasAny, And, Rule
from .items import SIGN_PIC_NAMES
from .locations import wonderful, multiple, secret_exit, bonus, PokemonSnapLocationCategory as Category
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

    # Secret Exits
    set_location_rule(world, LVL_TUNNEL, Category.SECRET_EXIT, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, LVL_RIVER,  Category.SECRET_EXIT, _HAS_PESTER)
    set_location_rule(world, LVL_VALLEY, Category.SECRET_EXIT, _HAS_PESTER)

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
    set_location_rule(world, "Scyther", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Scyther", Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Chansey", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Chansey", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    
    set_location_rule(world, "Snorlax", Category.NORMAL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))
    set_location_rule(world, "Snorlax", Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))

    set_location_rule(world, "Kangaskhan", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magikarp (Beach)", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Magikarp (Beach)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Pikachu (Beach)", Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, SURFING_PIKACHU, Category.SPECIAL_POSE, _HAS_APPLE)
    set_location_rule(world, PIKACHU_ON_A_STUMP, Category.SPECIAL_POSE, _HAS_PESTER)

    set_location_rule(world, BEACH_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))


def set_tunnel_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] mult: Technically possible without anything (difficult)
    set_location_rule(world, "Kakuna", Category.MULTIPLE_PHOTO, HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE))

    # Without Zapdos you have to ignore the first and throw at the second - spoiler in doc
    set_location_rule(world, "Electabuzz", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magnemite", Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, "Magnemite", Category.WONDERFUL_PHOTO, _HAS_APPLE)
    set_location_rule(world, "Magnemite", Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, "Magneton", Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, "Magneton", Category.WONDERFUL_PHOTO, _HAS_APPLE)

    set_location_rule(world, "Zapdos", Category.NORMAL_PHOTO, HasAll(POKEMON_FOOD, POKEFLUTE))
    set_location_rule(world, "Zapdos", Category.WONDERFUL_PHOTO, HasAll(POKEMON_FOOD, POKEFLUTE))

    set_location_rule(world, TUNNEL_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE))


def set_volcano_rules(world: "PokemonSnapWorld"):
    set_location_rule(world, "Charmander", Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, "Charmeleon", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Charmeleon", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Charizard", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Charizard", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] mult: Technically possible with dash (rng)
    set_location_rule(world, "Vulpix", Category.MULTIPLE_PHOTO, _HAS_APPLE)

    set_location_rule(world, "Growlithe", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Growlithe", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Growlithe", Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, "Arcanine", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Arcanine", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Arcanine", Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, "Moltres", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Moltres", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magmar", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magikarp (Volcano)", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Magikarp (Volcano)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, FIGHTING_MAGMAR, Category.SPECIAL_POSE, _HAS_APPLE)

    set_location_rule(world, VOLCANO_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, PESTER_BALL))


def set_river_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] wdfl&mult: Technically possible without anything (rng)
    set_location_rule(world, "Shellder", Category.WONDERFUL_PHOTO, Has(DASH_ENGINE))
    set_location_rule(world, "Shellder", Category.MULTIPLE_PHOTO, Has(DASH_ENGINE))

    set_location_rule(world, "Vileplume", Category.NORMAL_PHOTO, _HAS_FLUTE)
    set_location_rule(world, "Vileplume", Category.WONDERFUL_PHOTO, _HAS_FLUTE)

    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    set_location_rule(world, "Metapod", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Metapod", Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Psyduck", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Poliwag", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Poliwag", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Slowbro", Category.NORMAL_PHOTO, _HAS_APPLE)
    set_location_rule(world, "Slowbro", Category.WONDERFUL_PHOTO, _HAS_APPLE)

    set_location_rule(world, "Porygon", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Porygon", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Porygon", Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, "Bulbasaur (River)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Bulbasaur (River)", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magikarp (River)", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Magikarp (River)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # Speed pikachu has no requirements, it will begin to run if you take a close picture

    set_location_rule(world, RIVER_SIGN, Category.POKEMON_SIGN, HasAll(SIGN_DETECTOR, POKEFLUTE))


def set_cave_rules(world: "PokemonSnapWorld"):
    set_location_rule(world, "Victreebel", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Victreebel", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Jigglypuff", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Ditto", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Ditto", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Ditto", Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Articuno", Category.NORMAL_PHOTO, _HAS_FLUTE)
    set_location_rule(world, "Articuno", Category.WONDERFUL_PHOTO, _HAS_FLUTE)

    set_location_rule(world, "Muk", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Muk", Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Jynx", Category.MULTIPLE_PHOTO, _HAS_FLUTE)

    set_location_rule(world, "Magikarp (Cave)", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Magikarp (Cave)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] base: Technically possible without anything (difficult)
    set_location_rule(world, "Pikachu (Cave)", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Pikachu (Cave)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, BALLOON_PIKACHU, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, FLYING_PIKACHU, Category.SPECIAL_POSE, And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER))
    set_location_rule(world, JIGGLYPUFF_ON_STAGE, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, JIGGLYPUFF_TRIO, Category.SPECIAL_POSE, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, CAVE_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))


def set_valley_rules(world: "PokemonSnapWorld"):
    # TODO: [SOFT] wdfl: Technically possible without anything. mult: Technically possible with just dash (difficult)
    set_location_rule(world, "Squirtle", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Squirtle", Category.MULTIPLE_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Goldeen", Category.NORMAL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Goldeen", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, "Magikarp (Valley)", Category.NORMAL_PHOTO, HasAny(PESTER_BALL, POKEMON_FOOD, DASH_ENGINE))
    set_location_rule(world, "Magikarp (Valley)", Category.WONDERFUL_PHOTO, _HAS_APPLE_OR_PESTER)
    set_location_rule(world, "Magikarp (Valley)", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    # TODO: [SOFT] wdfl&mult: Technically possible without anything (difficult)
    set_location_rule(world, "Graveler", Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, POKEFLUTE))
    set_location_rule(world, "Graveler", Category.MULTIPLE_PHOTO, _HAS_FLUTE)

    set_location_rule(world, "Gyarados", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Gyarados", Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Dragonite", Category.NORMAL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Dragonite", Category.WONDERFUL_PHOTO, _HAS_PESTER)

    set_location_rule(world, "Sandshrew", Category.NORMAL_PHOTO, HasAny(PESTER_BALL, DASH_ENGINE))
    set_location_rule(world, "Sandshrew", Category.WONDERFUL_PHOTO, _HAS_PESTER)
    set_location_rule(world, "Sandshrew", Category.MULTIPLE_PHOTO, HasAll(PESTER_BALL, POKEMON_FOOD))

    set_location_rule(world, "Sandslash", Category.WONDERFUL_PHOTO, HasAny(PESTER_BALL, DASH_ENGINE))

    set_location_rule(world, "Dratini", Category.MULTIPLE_PHOTO, _HAS_APPLE_OR_PESTER)

    set_location_rule(world, GRAVELERS_GROUP_DANCE, Category.SPECIAL_POSE, _HAS_FLUTE)

    set_location_rule(world, VALLEY_SIGN, Category.POKEMON_SIGN, Has(SIGN_DETECTOR))
