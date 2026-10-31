from .constants import *
from .poses import *
from typing import NamedTuple
from rule_builder.rules import Rule, True_

class Shot(NamedTuple):
    size: int
    pose: int | PokemonSnapPoseData = 0
    multiple: int = 0
    wonderful: bool = False
    special: str | None = None
    rule: Rule = True_()

'''
Thoughts on how to collect this data:
- For the base set of photos, we really only need the best possible shot with each subset of items, including multiple scoring
  - And for some pokemon, this doesn't even matter. E.g. if PokeFlute does nothing for it, we can ignore subsets with only PokeFlute
- Then we also need a photo for each pose, just to also have those in the scoring logic
  - And again, we sort of need to do it with each subset of items that impact it
- So if I take the best photo I can, we can use the fudge factor to make the logic a little softer.
- After some people do some playtesting, we can update this logic if needed

Can we programatically make a list of all the photos I need to take?
And then programatically generate the lines of code from my playthrough?

Also I think it would be pretty reasonable to compare the score of the photos I take with the
Retro Achievements "Perfect Picture" list: https://retroachievements.org/game/10155?set=33039.
On second thought, the "Perfect Picture" achievements are _hard_. It can still be a reference,
but we'll need to take those scores with a grain of salt.
'''

# Actual in-game shots to help with report score logic.
# SHOTS = {}
SHOTS: dict[str, list[Shot]] = {
    ###########
    ## Beach ##
    ###########
    BUTTERFREE: [
        Shot(size=1000, pose=1000, wonderful=True),
        Shot(size=800,  pose=1000, wonderful=True, multiple=600),
    ],
    PIDGEY: [
        Shot(size=740,  pose=PIDGEY_SCREECH, wonderful=True, multiple=270),
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
        Shot(size=260, pose=800, wonderful=False, multiple=570),
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