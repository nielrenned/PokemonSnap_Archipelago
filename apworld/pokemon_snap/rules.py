from typing import TYPE_CHECKING

from rule_builder.rules import CanReachLocation, Has, HasAll, HasAny

if TYPE_CHECKING:
    from . import PokemonSnapWorld


def set_rules(world: "PokemonSnapWorld"):
    world.set_completion_rule(CanReachLocation("Mew"))

    world.set_rule(world.get_entrance("Start Game -> Beach"), Has("Beach"))
    world.set_rule(world.get_entrance("Start Game -> Tunnel"), Has("Tunnel"))
    world.set_rule(world.get_entrance("Start Game -> Volcano"), Has("Volcano"))
    world.set_rule(world.get_entrance("Start Game -> River"), Has("River"))
    world.set_rule(world.get_entrance("Start Game -> Cave"), Has("Cave"))
    world.set_rule(world.get_entrance("Start Game -> Valley"), Has("Valley"))
    world.set_rule(world.get_entrance("Start Game -> Rainbow Cloud"), Has("Rainbow Cloud"))

    apple_or_pester = HasAny("Pester Ball", "Apple")
    world.set_rule(world.get_entrance("Beach -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("Volcano -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("River -> Magikarp"), apple_or_pester)
    world.set_rule(world.get_entrance("Cave -> Magikarp"), apple_or_pester)

    # beach
    world.set_rule(world.get_location("Scyther"), Has("Pester Ball"))
    world.set_rule(world.get_location("Chansey"), apple_or_pester)
    world.set_rule(world.get_location("Snorlax"), HasAny("Pester Ball", "Flute"))

    # tunnel
    world.set_rule(world.get_location("Magnemite"), Has("Apple"))
    world.set_rule(world.get_location("Magneton"), Has("Apple"))
    world.set_rule(world.get_location("Zapdos"), HasAll("Apple", "Flute"))

    # volcano
    world.set_rule(world.get_location("Charmeleon"), apple_or_pester)
    world.set_rule(world.get_location("Charizard"), apple_or_pester)
    world.set_rule(world.get_location("Growlithe"), Has("Pester Ball"))
    world.set_rule(world.get_location("Arcanine"), Has("Pester Ball"))
    world.set_rule(world.get_location("Moltres"), apple_or_pester)

    # river
    world.set_rule(world.get_location("Vileplume"), Has("Flute"))
    world.set_rule(world.get_location("Slowbro"), Has("Apple"))
    world.set_rule(world.get_location("Porygon"), Has("Pester Ball"))

    # cave
    world.set_rule(world.get_location("Victreebel"), apple_or_pester)
    world.set_rule(world.get_location("Ditto"), Has("Pester Ball"))
    world.set_rule(world.get_location("Articuno"), Has("Flute"))
    world.set_rule(world.get_location("Muk"), Has("Pester Ball"))

    # valley
    world.set_rule(world.get_location("Goldeen"), apple_or_pester)
    world.set_rule(world.get_location("Gyarados"), Has("Pester Ball"))
    world.set_rule(world.get_location("Dragonite"), Has("Pester Ball"))
    world.set_rule(world.get_location("Sandshrew"), HasAny("Pester Ball", "Dash Engine"))

    # rainbow cloud
    world.set_rule(world.get_location("Mew"), Has("Pester Ball"))
