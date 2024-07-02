import os
import random
import time

# Weapon class for different weapon types
class Weapon:
    def __init__(self, name: str, weapon_type: str, damage_range: tuple, value: int):
        self.name = name
        self.weapon_type = weapon_type
        self.damage_range = damage_range
        self.value = value

    def get_damage(self):
        return random.randint(self.damage_range[0], self.damage_range[1])

# HealthBar class to display health visually
class HealthBar:
    def __init__(self, entity):
        self.entity = entity

    def draw(self):
        if isinstance(self.entity, Hero):
            color = "\033[92m"  # Green color for hero
        elif isinstance(self.entity, Enemy):
            color = "\033[91m"  # Red color for enemy
        else:
            color = "\033[0m"   # Default color

        health_bar = '|' + '█' * (self.entity.health // 5) + '_' * ((self.entity.health_max - self.entity.health) // 5) + '|'
        print(f"{self.entity.name}'s Health: {self.entity.health}/{self.entity.health_max}")
        print(f"{color}{health_bar}\033[0m")  # Reset color to default after printing

# Character base class
class Character:
    def __init__(self, name: str, health: int):
        self.name = name
        self.health = health
        self.health_max = health
        self.weapon = None

    def attack(self):
        return self.weapon.get_damage() if self.weapon else 0

# Hero class inheriting from Character
class Hero(Character):
    def __init__(self, name: str, health: int):
        super().__init__(name, health)
        self.inventory = []
        self.health_bar = HealthBar(self)

    def equip_weapon(self, weapon: Weapon):
        self.weapon = weapon
        print(f"You equipped {weapon.name}!")
        self.inventory.append(weapon)

    def display_inventory(self):
        print("Inventory:")
        for item in self.inventory:
            print(item.name)

# Enemy class inheriting from Character
class Enemy(Character):
    def __init__(self, name: str, health: int, damage: int):
        super().__init__(name, health)
        self.damage = damage
        self.health_bar = HealthBar(self)

    def attack(self):
        return self.damage

# Event class for random events
class Event:
    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description

# Game class to manage game flow
class Game:
    def __init__(self):
        self.hero = Hero("Hero", 100)
        self.current_enemy = None
        self.events = [
            Event("Walking by a Corpse and Loot", "You find a corpse with some valuable items."),
            Event("Seeing a Fire", "You notice a flickering light nearby, indicating life or danger."),
            Event("Looking around", "You observe your surroundings, searching for clues."),
            Event("Random Thoughts", "You reflect on your past life, trying to piece together memories."),
            Event("Fun Facts", "You learn interesting tidbits about the castle's history."),
            Event("Spooky Stuff", "You hear eerie sounds echoing through the corridors."),
        ]
        self.enemies = [
            Enemy("Skeleton Guard", 30, 10),
            Enemy("Sewer Rat", 20, 5),
            Enemy("Slime", 40, 8),
            Enemy("Bat", 25, 7),
        ]
        self.weapons = [
            Weapon(name="Iron Sword", weapon_type="sharp", damage_range=(5, 10), value=10),
            Weapon(name="Short Bow", weapon_type="ranged", damage_range=(4, 8), value=8),
            Weapon(name="Fists", weapon_type="blunt", damage_range=(2, 4), value=0),
        ]

    def clear_screen(self):
        os.system('cls' if os.name ==         'nt' else 'clear')

    def game_over(self, message):
        self.clear_screen()
        print(message)
        exit()

    def trigger_random_event(self):
        event = random.choice(self.events)
        print(f"\n{event.name}: {event.description}\n")
        return event

    def encounter_enemy(self, enemy, event_description):
        self.current_enemy = enemy
        while self.current_enemy.health > 0 and self.hero.health > 0:
            self.clear_screen()
            print(event_description)  # Display event description
            print(f"\nYou encounter a {enemy.name}!")
            self.hero.health_bar.draw()
            self.current_enemy.health_bar.draw()

            hero_attack = self.hero.attack()
            self.current_enemy.health -= hero_attack
            print(f"You dealt {hero_attack} damage to the {self.current_enemy.name}.")

            if self.current_enemy.health <= 0:
                print(f"You defeated the {self.current_enemy.name}!")
                self.current_enemy = None
                break

            enemy_attack = self.current_enemy.attack()
            self.hero.health -= enemy_attack
            print(f"The {self.current_enemy.name} dealt {enemy_attack} damage to you.")

            if self.hero.health <= 0:
                self.game_over("Game Over! You were defeated by the enemy.")

            time.sleep(2)

    def explore(self):
        self.clear_screen()
        event = self.trigger_random_event()
        if random.random() < 0.5:
            enemy = random.choice(self.enemies)
            self.encounter_enemy(enemy, event.description)

    def view_inventory(self):
        self.clear_screen()
        self.hero.display_inventory()
        input("\nPress Enter to continue...")

    def quit_game(self):
        self.game_over("You quit the game.")

    def select_weapon(self):
        while True:
            self.clear_screen()
            print("Choose your weapon:")
            for i, weapon in enumerate(self.weapons):
                print(f"{i + 1}. {weapon.name} (Damage: {weapon.damage_range[0]}-{weapon.damage_range[1]})")

            choice = input("Enter the number of your choice: ")

            if choice.isdigit() and 1 <= int(choice) <= len(self.weapons):
                self.hero.equip_weapon(self.weapons[int(choice) - 1])
                break
            else:
                input("Invalid choice. Press Enter to try again...")

    def main_menu(self):
        self.select_weapon()  # Allow weapon selection before the main menu
        while True:
            #self.clear_screen()
            print("1. Explore")
            print("2. View Inventory")
            print("3. Quit")

            choice = input("Enter your choice: ")

            if choice == '1':
                self.explore()
            elif choice == '2':
                self.view_inventory()
            elif choice == '3':
                self.quit_game()
            else:
                input("Invalid choice. Press Enter to continue...")

# Initialize game and start main loop
def main():
    game = Game()
    game.main_menu()

if __name__ == "__main__":
    main()

