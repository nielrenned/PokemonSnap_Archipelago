from typing import TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, HasAll, HasAny

if TYPE_CHECKING:
    from . import PokemonSnapWorld


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(CanReachLocation("Mew"))

    world.set_rule(world.get_entrance("Start Game -> Beach"), Has("Beach Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> Tunnel"), Has("Tunnel Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> Volcano"), Has("Volcano Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> River"), Has("River Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> Cave"), Has("Cave Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> Valley"), Has("Valley Unlocked"))
    world.set_rule(world.get_entrance("Start Game -> Rainbow Cloud"), Has("Rainbow Cloud Unlocked"))

    # Mew (goal) must have its shield broken with Pester Balls to be photographed.
    world.set_rule(world.get_location("Mew"), Has("Pester Ball Unlocked"))

    apple_or_pester = HasAny("Pester Ball Unlocked", "Apple Unlocked")
    world.set_rule(world.get_entrance("Beach -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("Volcano -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("River -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("Cave -> Magikarp"), apple_or_pester)

    # beach
    world.set_rule(world.get_location("Scyther"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Chansey"), apple_or_pester)
    world.set_rule(world.get_location("Snorlax"), HasAny("Pester Ball Unlocked", "Flute Unlocked"))

    # tunnel
    world.set_rule(world.get_location("Magnemite"), Has("Apple Unlocked"))
    world.set_rule(world.get_location("Magneton"), Has("Apple Unlocked"))
    world.set_rule(world.get_location("Zapdos"), HasAll("Apple Unlocked", "Flute Unlocked"))

    # volcano
    world.set_rule(world.get_location("Charmeleon"), apple_or_pester)
    world.set_rule(world.get_location("Charizard"), apple_or_pester)
    world.set_rule(world.get_location("Growlithe"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Arcanine"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Moltres"), apple_or_pester)

    # river
    world.set_rule(world.get_location("Vileplume"), Has("Flute Unlocked"))
    world.set_rule(world.get_location("Slowbro"), Has("Apple Unlocked"))
    world.set_rule(world.get_location("Porygon"), Has("Pester Ball Unlocked"))

    # cave
    world.set_rule(world.get_location("Victreebel"), apple_or_pester)
    world.set_rule(world.get_location("Ditto"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Articuno"), Has("Flute Unlocked"))
    world.set_rule(world.get_location("Muk"), Has("Pester Ball Unlocked"))

    # valley
    world.set_rule(world.get_location("Goldeen"), apple_or_pester)
    world.set_rule(world.get_location("Gyarados"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Dragonite"), Has("Pester Ball Unlocked"))
    world.set_rule(world.get_location("Sandshrew"), HasAny("Pester Ball Unlocked", "Speed Boost Unlocked"))
