from typing import TYPE_CHECKING

from rule_builder.rules import Has, HasAll, HasAny, And
from .items import SIGN_PIC_NAMES
from .locations import wonderful as wdfl, multiple as mult
from .constants import *

if TYPE_CHECKING:
    from . import PokemonSnapWorld


_HAS_PESTER = Has(PESTER_BALL)
_HAS_APPLE = Has(POKEMON_FOOD)
_HAS_FLUTE = Has(POKEFLUTE)
_HAS_APPLE_OR_PESTER = HasAny(PESTER_BALL, POKEMON_FOOD)


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(Has(VICTORY_ITEM_NAME))

    for level in [LVL_BEACH, LVL_TUNNEL, LVL_VOLCANO, LVL_RIVER, LVL_CAVE, LVL_VALLEY]:
        world.set_rule(world.get_entrance(f'{START_GAME} -> {level}'), Has(level))

    world.set_rule(world.get_entrance(f'{START_GAME} -> {LVL_CLOUD}'), HasAll(*SIGN_PIC_NAMES))


    # beach
    world.set_rule(world.get_location("Scyther"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Scyther")), _HAS_PESTER)

    world.set_rule(world.get_location("Chansey"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Chansey")), _HAS_APPLE_OR_PESTER)
    
    world.set_rule(world.get_location("Snorlax"), HasAny(PESTER_BALL, POKEFLUTE))
    world.set_rule(world.get_location(wdfl("Snorlax")), HasAny(PESTER_BALL, POKEFLUTE))

    world.set_rule(world.get_location(wdfl("Kangaskhan")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Magikarp (Beach)"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Magikarp (Beach)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(mult("Pikachu (Beach)")), _HAS_PESTER)

    world.set_rule(world.get_location("Surfing Pikachu"), _HAS_APPLE)
    world.set_rule(world.get_location("Pikachu on a Stump"), _HAS_PESTER)

    world.set_rule(world.get_location(BEACH_SIGN), Has(SIGN_DETECTOR))


    # tunnel
    world.set_rule(world.get_location(mult("Electabuzz")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Magnemite"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Magnemite")), _HAS_APPLE)
    world.set_rule(world.get_location(mult("Magnemite")), _HAS_APPLE)

    world.set_rule(world.get_location("Magneton"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Magneton")), _HAS_APPLE)

    world.set_rule(world.get_location("Zapdos"), HasAll(POKEMON_FOOD, POKEFLUTE))
    world.set_rule(world.get_location(wdfl("Zapdos")), HasAll(POKEMON_FOOD, POKEFLUTE))

    world.set_rule(world.get_location(TUNNEL_SIGN), HasAll(SIGN_DETECTOR, POKEMON_FOOD, POKEFLUTE))


    # volcano
    world.set_rule(world.get_location(wdfl("Charmander")), _HAS_APPLE)
    world.set_rule(world.get_location(mult("Charmander")), _HAS_APPLE)

    world.set_rule(world.get_location("Charmeleon"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Charmeleon")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Charizard"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Charizard")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(mult("Vulpix")), _HAS_APPLE)

    world.set_rule(world.get_location("Growlithe"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Growlithe")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Growlithe")), HasAll(PESTER_BALL, POKEMON_FOOD))

    world.set_rule(world.get_location("Arcanine"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Arcanine")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Arcanine")), HasAll(PESTER_BALL, POKEMON_FOOD))

    world.set_rule(world.get_location("Moltres"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Moltres")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(mult("Magmar")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Magikarp (Volcano)"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Magikarp (Volcano)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Fighting Magmar"), _HAS_APPLE)

    world.set_rule(world.get_location(VOLCANO_SIGN), HasAll(SIGN_DETECTOR, PESTER_BALL))


    # river
    world.set_rule(world.get_location("Vileplume"), _HAS_FLUTE)
    world.set_rule(world.get_location(wdfl("Vileplume")), _HAS_FLUTE)

    # TODO: This is technically possible without pester, but is hard
    world.set_rule(world.get_location(wdfl("Metapod")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Metapod")), _HAS_PESTER)

    world.set_rule(world.get_location(mult("Psyduck")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(wdfl("Poliwag")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Poliwag")), _HAS_PESTER)

    world.set_rule(world.get_location("Slowbro"), _HAS_APPLE)
    world.set_rule(world.get_location(wdfl("Slowbro")), _HAS_APPLE)

    world.set_rule(world.get_location("Porygon"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Porygon")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Porygon")), HasAll(PESTER_BALL, POKEMON_FOOD))

    world.set_rule(world.get_location(wdfl("Bulbasaur (River)")), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(mult("Bulbasaur (River)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Magikarp (River)"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Magikarp (River)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(wdfl("Pikachu (River)")), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location("Speed Pikachu"), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(RIVER_SIGN), HasAll(SIGN_DETECTOR, POKEFLUTE))


    # cave
    world.set_rule(world.get_location("Victreebel"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Victreebel")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(mult("Jigglypuff")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Ditto"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Ditto")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Ditto")), _HAS_PESTER)

    world.set_rule(world.get_location("Articuno"), _HAS_FLUTE)
    world.set_rule(world.get_location(wdfl("Articuno")), _HAS_FLUTE)

    world.set_rule(world.get_location("Muk"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Muk")), _HAS_PESTER)

    world.set_rule(world.get_location(mult("Jynx")), _HAS_FLUTE)

    world.set_rule(world.get_location("Magikarp (Cave)"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Magikarp (Cave)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(wdfl("Pikachu (Cave)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Balloon Pikachu"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location("Flying Pikachu"), And(_HAS_FLUTE, _HAS_APPLE_OR_PESTER))
    world.set_rule(world.get_location("Jigglypuff on Stage"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location("Jigglypuff Trio on Stage"), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location(CAVE_SIGN), Has(SIGN_DETECTOR))


    # valley
    world.set_rule(world.get_location(mult("Squirtle")), HasAny(PESTER_BALL, DASH_ENGINE))

    world.set_rule(world.get_location("Goldeen"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Goldeen")), _HAS_APPLE_OR_PESTER)

    # TODO: Ali's logic claims we can get Valley karp without Apple/Pester, but I couldn't do it
    world.set_rule(world.get_location("Magikarp (Valley)"), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(wdfl("Magikarp (Valley)")), _HAS_APPLE_OR_PESTER)
    world.set_rule(world.get_location(mult("Magikarp (Valley)")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Gyarados"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Gyarados")), _HAS_PESTER)

    world.set_rule(world.get_location("Dragonite"), _HAS_PESTER)
    world.set_rule(world.get_location(wdfl("Dragonite")), _HAS_PESTER)

    world.set_rule(world.get_location("Sandshrew"), HasAny(PESTER_BALL, DASH_ENGINE))
    world.set_rule(world.get_location(wdfl("Sandshrew")), _HAS_PESTER)
    world.set_rule(world.get_location(mult("Sandshrew")), HasAll(PESTER_BALL, POKEMON_FOOD))

    world.set_rule(world.get_location(wdfl("Sandslash")), HasAny(PESTER_BALL, DASH_ENGINE))

    world.set_rule(world.get_location(mult("Dratini")), _HAS_APPLE_OR_PESTER)

    world.set_rule(world.get_location("Graveler's Group Dance"), _HAS_FLUTE)

    world.set_rule(world.get_location(VALLEY_SIGN), Has(SIGN_DETECTOR))


    # rainbow cloud
    world.set_rule(world.get_location("Mew"), _HAS_PESTER)
