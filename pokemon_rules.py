from rule_builder.rules import Rule, True_, Has, HasAny, HasAll
from typing import NamedTuple, Optional
from locations import course
from constants import *

_NO_ITEMS = True_()


class PokemonSnapPhotoLogic(NamedTuple):
    normal:    Optional[Rule]
    wonderful: Optional[Rule]
    multiple:  Optional[Rule]


class PokemonSnapSpeciesPhotoData(NamedTuple):
    name: str
    loc_id: int
    soft_logic: PokemonSnapPhotoLogic
    hard_logic: Optional[PokemonSnapPhotoLogic] = None


SPECIES_RULE_DATA = {
    LVL_BEACH: [
        PokemonSnapSpeciesPhotoData(
            name       = BUTTERFREE, 
            loc_id     = 7,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = PIDGEY, 
            loc_id     = 9,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MEOWTH, 
            loc_id     = 19,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DODUO, 
            loc_id     = 34,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = CHANSEY, 
            loc_id     = 42,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = KANGASKHAN, 
            loc_id     = 43,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SCYTHER, 
            loc_id     = 47,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = LAPRAS, 
            loc_id     = 53,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = EEVEE, 
            loc_id     = 55,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SNORLAX, 
            loc_id     = 57,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(PESTER_BALL, POKEFLUTE),
                wonderful = HasAny(PESTER_BALL, POKEFLUTE),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            species_name  = PIKACHU,
            location_name = course(PIKACHU, LVL_BEACH), 
            loc_id        = 10,
            soft_logic    = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = Has(PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_BEACH), 
            loc_id     = 51,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
    ],

    LVL_TUNNEL: [
        PokemonSnapSpeciesPhotoData(
            name       = KAKUNA, 
            loc_id     = 8,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, DASH_ENGINE, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DIGLETT, 
            loc_id     = 17,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DUGTRIO, 
            loc_id     = 18,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MAGNEMITE, 
            loc_id     = 32,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(POKEMON_FOOD),
                wonderful = Has(POKEMON_FOOD),
                multiple  = Has(POKEMON_FOOD),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MAGNETON, 
            loc_id     = 33,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(POKEMON_FOOD),
                wonderful = Has(POKEMON_FOOD),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = HAUNTER, 
            loc_id     = 39,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = ELECTRODE, 
            loc_id     = 40,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = ELECTABUZZ, 
            loc_id     = 49,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = ZAPDOS, 
            loc_id     = 59,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAll(POKEMON_FOOD, POKEFLUTE),
                wonderful = HasAll(POKEMON_FOOD, POKEFLUTE),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(ZUBAT, LVL_TUNNEL), 
            loc_id     = 15,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_TUNNEL), 
            loc_id     = 65,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(PIKACHU, LVL_TUNNEL), 
            loc_id     = 70,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
    ],

    LVL_VOLCANO: [
        PokemonSnapSpeciesPhotoData(
            name       = CHARMANDER, 
            loc_id     = 2,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = Has(POKEMON_FOOD),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = CHARMELEON, 
            loc_id     = 3,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = CHARIZARD, 
            loc_id     = 4,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = VULPIX, 
            loc_id     = 13,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = Has(POKEMON_FOOD),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GROWLITHE, 
            loc_id     = 22,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = HasAll(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = ARCANINE, 
            loc_id     = 23,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = HasAll(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = RAPIDASH, 
            loc_id     = 29,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MAGMAR, 
            loc_id     = 50,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MOLTRES, 
            loc_id     = 60,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_VOLCANO), 
            loc_id     = 66,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
    ],

    LVL_RIVER: [
        PokemonSnapSpeciesPhotoData(
            name       = METAPOD, 
            loc_id     = 6,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = Has(PESTER_BALL),
                multiple  = Has(PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = VILEPLUME, 
            loc_id     = 16,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(POKEFLUTE),
                wonderful = Has(POKEFLUTE),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = PSYDUCK, 
            loc_id     = 20,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = POLIWAG, 
            loc_id     = 24,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SLOWPOKE, 
            loc_id     = 30,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SLOWBRO, 
            loc_id     = 31,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(POKEMON_FOOD),
                wonderful = Has(POKEMON_FOOD),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SHELLDER, 
            loc_id     = 37,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = Has(DASH_ENGINE),
                multiple  = Has(DASH_ENGINE),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = CLOYSTER, 
            loc_id     = 38,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = PORYGON, 
            loc_id     = 56,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = HasAll(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(BULBASAUR, LVL_RIVER), 
            loc_id     = 1,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_RIVER), 
            loc_id     = 67,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(PIKACHU, LVL_RIVER), 
            loc_id     = 71,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
    ],

    LVL_CAVE: [
        PokemonSnapSpeciesPhotoData(
            name       = JIGGLYPUFF, 
            loc_id     = 14,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = WEEPINBELL, 
            loc_id     = 25,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = VICTREEBEL, 
            loc_id     = 26,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GRIMER, 
            loc_id     = 35,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MUK, 
            loc_id     = 36,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = JYNX, 
            loc_id     = 48,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = Has(POKEFLUTE),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DITTO, 
            loc_id     = 54,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = Has(PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = ARTICUNO, 
            loc_id     = 58,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(POKEFLUTE),
                wonderful = Has(POKEFLUTE),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = KOFFING, 
            loc_id     = 41,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(BULBASAUR, LVL_CAVE), 
            loc_id     = 64,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_CAVE), 
            loc_id     = 68,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(PIKACHU, LVL_CAVE), 
            loc_id     = 72,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(ZUBAT, LVL_CAVE), 
            loc_id     = 73,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
    ],

    LVL_VALLEY: [
        PokemonSnapSpeciesPhotoData(
            name       = SQUIRTLE, 
            loc_id     = 5,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = Has(PESTER_BALL),
                multiple  = Has(PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SANDSHREW, 
            loc_id     = 11,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = HasAll(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = SANDSLASH, 
            loc_id     = 12,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = HasAny(DASH_ENGINE, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = MANKEY, 
            loc_id     = 21,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GEODUDE, 
            loc_id     = 27,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GRAVELER, 
            loc_id     = 28,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = HasAny(PESTER_BALL, POKEFLUTE),
                multiple  = Has(POKEFLUTE),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GOLDEEN, 
            loc_id     = 44,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = STARYU, 
            loc_id     = 45,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = STARMIE, 
            loc_id     = 46,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = _NO_ITEMS,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = GYARADOS, 
            loc_id     = 52,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DRATINI, 
            loc_id     = 61,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = _NO_ITEMS,
                wonderful = _NO_ITEMS,
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = DRAGONITE, 
            loc_id     = 62,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = Has(PESTER_BALL),
                wonderful = Has(PESTER_BALL),
                multiple  = None,
            ),
        ),
        PokemonSnapSpeciesPhotoData(
            name       = course(MAGIKARP, LVL_VALLEY), 
            loc_id     = 69,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, DASH_ENGINE, PESTER_BALL),
                wonderful = HasAny(POKEMON_FOOD, PESTER_BALL),
                multiple  = HasAny(POKEMON_FOOD, PESTER_BALL),
            ),
        ),
    ],

    LVL_CLOUD: [
        PokemonSnapSpeciesPhotoData(
            name       = MEW, 
            loc_id     = 63,
            soft_logic = PokemonSnapPhotoLogic(
                normal    = HasAny(POKEMON_FOOD, PESTER_BALL),
                wonderful = None,
                multiple  = None,
            ),
        ),
    ],
}