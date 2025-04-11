# Item class for different types of items
class Item:
    def __init__(self, name: str, item_type: str, value: int, color: str):
        self.name = name
        self.item_type = item_type
        self.value = value
        self.color = color
        
    def use(self, character):
        """Use the item on a character"""
        if self.item_type == "consumable":
            if "Health Potion" in self.name:
                heal_amount = 30
                character.health = min(character.health + heal_amount, character.health_max)
                print(f"\033[32mYou used {self.name} and recovered {heal_amount} health!\033[0m")
                return True
            elif "Strength Potion" in self.name:
                if hasattr(character, 'weapon') and character.weapon:
                    # Temporarily boost weapon damage
                    character.weapon.damage_boost = 10
                    print(f"\033[31mYou used {self.name} and your weapon damage increased!\033[0m")
                    return True
        elif self.item_type == "buff":
            if "Strength Up" in self.name:
                character.strength_bonus = 5
                print(f"\033[32mYou used {self.name} and gained +5 strength!\033[0m")
                return True
            elif "Speed Up" in self.name:
                character.speed_bonus = 5
                print(f"\033[34mYou used {self.name} and gained +5 speed!\033[0m")
                return True
            elif "Defense Up" in self.name:
                character.defense_bonus = 5
                print(f"\033[33mYou used {self.name} and gained +5 defense!\033[0m")
                return True
        
        print(f"You can't use {self.name} right now.")
        return False
