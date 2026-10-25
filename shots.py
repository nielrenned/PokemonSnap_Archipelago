from .constants import *
from .poses import *
from typing import NamedTuple
from rule_builder.rules import Rule, True_

class Shot(NamedTuple):
    size: int
    pose: int | PokemonSnapPoseData = 0
    multiple: int = 0
    wonderful: bool = True
    special: str | None = None
    rule: Rule = True_()

# Actual in-game shots to help with report score logic.
SHOTS: dict[str, list[Shot]] = {
    ###########
    ## Beach ##
    ###########
    BUTTERFREE: [
        Shot(size=0),
    ],
    PIDGEY: [
        Shot(size=0),
    ],
    MEOWTH: [
        Shot(size=0),
    ],
    DODUO: [
        Shot(size=0),
    ],
    CHANSEY: [
        Shot(size=0),
    ],
    KANGASKHAN: [
        Shot(size=0),
    ],
    SCYTHER: [
        Shot(size=0),
    ],
    LAPRAS: [
        Shot(size=0),
    ],
    EEVEE: [
        Shot(size=0),
    ],
    SNORLAX: [
        Shot(size=0),
    ],
    course(PIKACHU, LVL_BEACH): [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_BEACH): [
        Shot(size=0),
    ],


    ############
    ## Tunnel ##
    ############
    KAKUNA: [
        Shot(size=0),
    ],
    DIGLETT: [
        Shot(size=0),
    ],
    DUGTRIO: [
        Shot(size=0),
    ],
    MAGNEMITE: [
        Shot(size=0),
    ],
    MAGNETON: [
        Shot(size=0),
    ],
    HAUNTER: [
        Shot(size=0),
    ],
    ELECTRODE: [
        Shot(size=0),
    ],
    ELECTABUZZ: [
        Shot(size=0),
    ],
    ZAPDOS: [
        Shot(size=0),
    ],
    course(ZUBAT, LVL_TUNNEL): [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_TUNNEL): [
        Shot(size=0),
    ],
    course(PIKACHU, LVL_TUNNEL): [
        Shot(size=0),
    ],

    #############
    ## Volcano ##
    #############
    CHARMANDER: [
        Shot(size=0),
    ],
    CHARMELEON: [
        Shot(size=0),
    ],
    CHARIZARD: [
        Shot(size=0),
    ],
    VULPIX: [
        Shot(size=0),
    ],
    GROWLITHE: [
        Shot(size=0),
    ],
    ARCANINE: [
        Shot(size=0),
    ],
    RAPIDASH: [
        Shot(size=0),
    ],
    MAGMAR: [
        Shot(size=0),
    ],
    MOLTRES: [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_VOLCANO): [
        Shot(size=0),
    ],


    ###########
    ## River ##
    ###########
    METAPOD: [
        Shot(size=0),
    ],
    VILEPLUME: [
        Shot(size=0),
    ],
    PSYDUCK: [
        Shot(size=0),
    ],
    POLIWAG: [
        Shot(size=0),
    ],
    SLOWPOKE: [
        Shot(size=0),
    ],
    SLOWBRO: [
        Shot(size=0),
    ],
    SHELLDER: [
        Shot(size=0),
    ],
    CLOYSTER: [
        Shot(size=0),
    ],
    PORYGON: [
        Shot(size=0),
    ],
    course(BULBASAUR, LVL_RIVER): [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_RIVER): [
        Shot(size=0),
    ],
    course(PIKACHU, LVL_RIVER): [
        Shot(size=0),
    ],


    ##########
    ## Cave ##
    ##########
    JIGGLYPUFF: [
        Shot(size=0),
    ],
    WEEPINBELL: [
        Shot(size=0),
    ],
    VICTREEBEL: [
        Shot(size=0),
    ],
    GRIMER: [
        Shot(size=0),
    ],
    MUK: [
        Shot(size=0),
    ],
    JYNX: [
        Shot(size=0),
    ],
    DITTO: [
        Shot(size=0),
    ],
    ARTICUNO: [
        Shot(size=0),
    ],
    KOFFING: [
        Shot(size=0),
    ],
    course(BULBASAUR, LVL_CAVE): [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_CAVE): [
        Shot(size=0),
    ],
    course(PIKACHU, LVL_CAVE): [
        Shot(size=0),
    ],
    course(ZUBAT, LVL_CAVE): [
        Shot(size=0),
    ],


    ############
    ## Valley ##
    ############
    SQUIRTLE: [
        Shot(size=0),
    ],
    SANDSHREW: [
        Shot(size=0),
    ],
    SANDSLASH: [
        Shot(size=0),
    ],
    MANKEY: [
        Shot(size=0),
    ],
    GEODUDE: [
        Shot(size=0),
    ],
    GRAVELER: [
        Shot(size=0),
    ],
    GOLDEEN: [
        Shot(size=0),
    ],
    STARYU: [
        Shot(size=0),
    ],
    STARMIE: [
        Shot(size=0),
    ],
    GYARADOS: [
        Shot(size=0),
    ],
    DRATINI: [
        Shot(size=0),
    ],
    DRAGONITE: [
        Shot(size=0),
    ],
    course(MAGIKARP, LVL_VALLEY): [
        Shot(size=0),
    ],

    ###################
    ## Rainbow Cloud ##
    ###################
    MEW: [
        Shot(size=0),
    ],
}