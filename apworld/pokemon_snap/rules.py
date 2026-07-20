from typing import TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, HasAll, HasAny
from .locations import wonderful as wdfl, multiple as mult
from .constants import *

if TYPE_CHECKING:
    from . import PokemonSnapWorld


_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE = Has(POKEMON_FOOD)
_HAS_FLUTE = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(PESTER_BALL, POKEMON_FOOD)


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(CanReachLocation("Mew"))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY, LVL_CLOUD]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level))


    world.set_rule(world.get_entrance("Beach -> Magikarp"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_entrance("Volcano -> Magikarp"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_entrance("River -> Magikarp"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_entrance("Cave -> Magikarp"), _HAS_APPLE_OR_PESTER)

    # beach
    world.set_rule(world.get_location("Scyther"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Scyther")), _HAS_PESTER)

    world.set_rule(world.get_location("Chansey"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Chansey")), _HAS_APPLE_OR_PESTER)
    
    world.set_rule(world.get_location("Snorlax"), HasAny(PESTER_BALL, POKEFLUTE))
    world.set_rule(world.get_location(wdfl("Snorlax")), HasAny(PESTER_BALL, POKEFLUTE))

    world.set_rule(world.get_location(wdfl("Kangaskhan")), _HAS_APPLE_OR_PESTER)


    # tunnel
    world.set_rule(world.get_location("Magnemite"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Magnemite")), _HAS_APPLE)

    world.set_rule(world.get_location("Magneton"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Magneton")), _HAS_APPLE)

    world.set_rule(world.get_location("Zapdos"), HasAll(POKEMON_FOOD, POKEFLUTE))
    world.set_rule(world.get_location(wdfl("Zapdos")), HasAll(POKEMON_FOOD, POKEFLUTE))


    # volcano
    world.set_rule(world.get_location("Charmeleon"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Charmeleon")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Charizard"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Charizard")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Growlithe"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Growlithe")), _HAS_PESTER)

    world.set_rule(world.get_location("Arcanine"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Arcanine")), _HAS_PESTER)

    world.set_rule(world.get_location("Moltres"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Moltres")), _HAS_APPLE_OR_PESTER)


    # river
    world.set_rule(world.get_location("Vileplume"), _HAS_FLUTE)
    world.set_rule(world.get_location(wdfl("Vileplume")), _HAS_FLUTE)

    world.set_rule(world.get_location("Slowbro"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Slowbro")), _HAS_APPLE)

    world.set_rule(world.get_location("Porygon"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Porygon")), _HAS_PESTER)

    # cave
    world.set_rule(world.get_location("Victreebel"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Victreebel")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Ditto"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Ditto")), _HAS_PESTER)

    world.set_rule(world.get_location("Articuno"), _HAS_FLUTE)
    world.set_rule(world.get_location(wdfl("Articuno")), _HAS_FLUTE)

    world.set_rule(world.get_location("Muk"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Muk")), _HAS_PESTER)

    # valley
    world.set_rule(world.get_location("Goldeen"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Goldeen")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Gyarados"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Gyarados")), _HAS_PESTER)

    world.set_rule(world.get_location("Dragonite"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Dragonite")), _HAS_PESTER)

    world.set_rule(world.get_location("Sandshrew"), HasAny(PESTER_BALL, DASH_ENGINE))
    world.set_rule(world.get_location(wdfl("Sandshrew")), _HAS_PESTER)

    world.set_rule(world.get_location(wdfl("Sandslash")), HasAny(PESTER_BALL, DASH_ENGINE))

    # rainbow cloud
    world.set_rule(world.get_location("Mew"), _HAS_PESTER)
