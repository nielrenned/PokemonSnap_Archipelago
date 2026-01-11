from typing import TYPE_CHECKING

from ..generic.Rules import set_rule

if TYPE_CHECKING:
    from . import PokemonSnapWorld


def set_rules(world: "PokemonSnapWorld"):
    world.multiworld.completion_condition[world.player] = lambda state: state.can_reach_location("Mew", world.player)

    set_rule(world.get_entrance("Start Game -> Beach"), lambda state: state.has("Beach Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> Tunnel"), lambda state: state.has("Tunnel Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> Volcano"), lambda state: state.has("Volcano Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> River"), lambda state: state.has("River Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> Cave"), lambda state: state.has("Cave Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> Valley"), lambda state: state.has("Valley Unlocked", world.player))
    set_rule(world.get_entrance("Start Game -> Rainbow Cloud"),
             lambda state: state.has("Rainbow Cloud Unlocked", world.player))

    set_rule(world.get_entrance("Beach -> Magikarp"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_entrance("Volcano -> Magikarp"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_entrance("River -> Magikarp"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_entrance("Cave -> Magikarp"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))

    # beach
    set_rule(world.get_location("Scyther"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Chansey"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Snorlax"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Flute Unlocked", world.player))

    # tunnel
    set_rule(world.get_location("Magnemite"), lambda state: state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Magneton"), lambda state: state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Zapdos"),
             lambda state: state.has("Apple Unlocked", world.player) and state.has("Flute Unlocked", world.player))

    # volcano
    set_rule(world.get_location("Charmeleon"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Charizard"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Growlithe"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Arcanine"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Moltres"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))

    # river
    set_rule(world.get_location("Vileplume"), lambda state: state.has("Flute Unlocked", world.player))
    set_rule(world.get_location("Slowbro"), lambda state: state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Porygon"), lambda state: state.has("Pester Ball Unlocked", world.player))

    # cave
    set_rule(world.get_location("Victreebel"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Ditto"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Articuno"), lambda state: state.has("Flute Unlocked", world.player))
    set_rule(world.get_location("Muk"), lambda state: state.has("Pester Ball Unlocked", world.player))

    # valley
    set_rule(world.get_location("Goldeen"),
             lambda state: state.has("Pester Ball Unlocked", world.player) or state.has("Apple Unlocked", world.player))
    set_rule(world.get_location("Gyarados"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Dragonite"), lambda state: state.has("Pester Ball Unlocked", world.player))
    set_rule(world.get_location("Sandshrew"),
             lambda state: state.has("Pester Ball Unlocked", world.player)
                           or state.has("Speed Boost Unlocked", world.player))
