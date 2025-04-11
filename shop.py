import random
from item import Item
from weapon import Weapon

class Shop:
    def __init__(self):
        self.buffs = [
            Item("Strength Up", "buff", 50, "32"),  # Green
            Item("Speed Up", "buff", 50, "34"),  # Blue
            Item("Defense Up", "buff", 50, "33"),  # Yellow
            Item("Shield of Immunity", "buff", 50, "35"),  # Magenta
            Item("Beryl of Chaos", "buff", 50, "31"),  # Red
        ]
        self.weapons = [
            Weapon("Rusty Sword", "sharp", (5, 15), 100, "33"),  # Brown
            Weapon("Iron Sword", "sharp", (10, 30), 200, "37"),  # Silver
            Weapon("Short Bow", "ranged", (5, 10), 150, "33"),   # Brown
            Weapon("Battle Axe", "sharp", (15, 35), 250, "31"),  # Red
            Weapon("Wooden Staff", "magic", (20, 40), 120, "32"),  # Green
            Weapon("Twin Dagger", "sharp", (5, 20), 180, "34"),  # Blue
            Weapon("Crossbow", "ranged", (10, 20), 200, "35"),  # Cyan
            Weapon("War Hammer", "blunt", (25, 45), 300, "33"),  # Yellow
            Weapon("Flaming Sword", "sharp", (20, 50), 300, "31;1"),  # Bold Red
            Weapon("Throwing Knives", "ranged", (5, 12), 200, "37"),  # White
            Weapon("Mace", "blunt", (10, 25), 150, "35"),  # Magenta
            Weapon("Poison Needles", "ranged", (5, 20), 180, "32;1"),  # Bold Green
        ]
        self.armors = [
            Item("Iron Chestplate", "armor", 100, "37"),  # Silver
            Item("Leather Body Armor", "armor", 50, "33"),  # Brown
            Item("Robe of Magus", "armor", 75, "34"),  # Blue
            Item("Shoes of Wind", "accessory", 60, "36"),  # Cyan
            Item("Crown of Fire", "accessory", 90, "31"),  # Red
            Item("Amulet of Life", "accessory", 100, "32"),  # Green
            Item("Ring of Light", "accessory", 75, "33"),  # Yellow
        ]
        self.consumables = [
            Item("Health Potion", "consumable", 30, "31"),  # Red
            Item("Strength Potion", "consumable", 40, "32"),  # Green
            Item("Speed Potion", "consumable", 40, "34"),  # Blue
        ]

    def display_items(self):
        items = [
            random.choice(self.buffs),
            random.choice(self.weapons),
            random.choice(self.armors),
            random.choice(self.consumables)
        ]
        print("\n" + "="*50)
        print("Welcome to the Shop!")
        print("="*50)
        for i, item in enumerate(items):
            if isinstance(item, Weapon):
                print(f"{i + 1}. \033[{item.color}m{item.name}\033[0m - {item.value} Gold (Damage: {item.damage_range[0]}-{item.damage_range[1]})")
            else:
                print(f"{i + 1}. \033[{item.color}m{item.name}\033[0m - {item.value} Gold")
        print(f"{len(items) + 1}. Exit Shop")
        print("="*50)
        return items

    def buy_item(self, hero, items, choice):
        item = items[choice - 1]
        if hero.coins >= item.value:
            hero.coins -= item.value
            hero.add_item(item)
            print(f"\033[{item.color}mYou bought {item.name}!\033[0m")
            return True
        else:
            print("Not enough gold to buy this item.")
            return False
