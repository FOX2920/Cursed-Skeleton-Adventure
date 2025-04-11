import random
from item import Item
from weapon import Weapon

class Event:
    def __init__(self, name: str, description: str, loot=None):
        self.name = name
        self.description = description
        self.loot = loot

    @staticmethod
    def generate_random_events():
        """Generate a list of possible random events"""
        events = [
            Event("Walking by a Corpse and Loot", "You find a corpse with potential loot."),
            Event("Seeing a Fire", "A fire, this could come in handy. Lets rest here for a while"),
            Event("Looking around", "You observe your surroundings, searching for clues."),
            Event("Random Thoughts", "You reflect on your past life, trying to piece together memories."),
            Event("Fun Facts", "You learn interesting tidbits about the castle's history."),
            Event("Spooky Stuff", "You hear eerie sounds echoing through the corridors."),
            Event("Hidden Passage", "You discover a secret passage in the wall."),
            Event("Mysterious Altar", "You find an ancient altar with strange symbols."),
            Event("Abandoned Camp", "You stumble upon an abandoned camp with scattered supplies."),
            Event("Magical Fountain", "You discover a fountain glowing with magical energy."),
        ]
        return events

    @staticmethod
    def generate_loot_options():
        """Generate loot options for the corpse event"""
        loot_options = [
            ("Oh, another me, how awkward this is, but since you are not going to move and use your stuff, you will not mind your stuff being missing then!", 10, Item("Silver Ring", "jewelry", 50, "37")),
            ("A fallen one, may your soul rest in peace. Leave the rest to me.", 5, Item("Health Potion", "consumable", 30, "31")),
            ("Well well well, let's look at what we have here!", 20, Weapon("Rusty Sword", "sharp", (5, 15), 2, "33")),
            ("All of these are great, and they are mine now!", 15, Item("Magic Amulet", "jewelry", 75, "35")),
            ("Another great find!", 30, Item("Map", "misc", 10, "34")),
            ("I am rich now!", 50, Item("Gemstone", "misc", 100, "36")),
            ("All of these are getting harder to carry around!", 40, Item("Ancient Scroll", "misc", 20, "32")),
            ("Dang it, there is nothing here!!", 0, None),
            ("What a shame, there is nothing this time to take.", 0, None)
        ]
        return loot_options

    @staticmethod
    def handle_special_event(event_name, hero):
        """Handle special events with unique effects"""
        if event_name == "Seeing a Fire":
            # Resting at a fire restores some health
            heal_amount = hero.health_max // 4
            hero.health = min(hero.health + heal_amount, hero.health_max)
            print(f"You rest by the fire and recover {heal_amount} health.")
            return True
        elif event_name == "Magical Fountain":
            # Fountain can give random buffs
            effects = ["strength", "speed", "defense", "health"]
            effect = random.choice(effects)
            
            if effect == "health":
                hero.health = hero.health_max
                print("You drink from the fountain and your health is fully restored!")
            elif effect == "strength":
                hero.strength_bonus += 2
                print("You drink from the fountain and feel stronger! (+2 Strength)")
            elif effect == "speed":
                hero.speed_bonus += 2
                print("You drink from the fountain and feel faster! (+2 Speed)")
            elif effect == "defense":
                hero.defense_bonus += 2
                print("You drink from the fountain and your skin hardens slightly! (+2 Defense)")
            
            return True
        
        return False
