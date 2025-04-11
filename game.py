import os
import random
import time
from character import Hero, Enemy, Boss
from weapon import Weapon, fists, iron_sword, short_bow, flaming_sword, frost_axe, poison_dagger
from item import Item
from shop import Shop
from event import Event

class Game:
    def __init__(self):
        # Initialize the hero
        self.hero = Hero("Hero", 999)
        
        # Game state
        self.current_enemies = None
        self.current_zone = 1
        self.max_zones = 5
        self.boss_defeated = False
        self.game_completed = False
        
        # Load events
        self.events = Event.generate_random_events()
        
        # Initialize shop
        self.shop = Shop()
        
        # Story progress tracking
        self.story_progress = 0
        self.story_events = [
            "You wake up in a dark dungeon with no memory of how you got here.",
            "The air is damp and cold. You must find a way out of this place.",
            "Rumors speak of a powerful artifact hidden in the depths of this dungeon.",
            "The artifact is said to grant immense power to its wielder.",
            "Beware of the dungeon's master who guards the artifact."
        ]
        
        # Initialize weapons
        self.weapons = [
            fists,
            iron_sword,
            short_bow,
            flaming_sword,
            frost_axe,
            poison_dagger
        ]
        
        # Initialize enemies for each zone
        self.zone_enemies = {
            1: [
                Enemy("Skeleton Guard", 30, (3, 8), 1),
                Enemy("Sewer Rat", 20, (2, 5), 1),
                Enemy("Slime", 25, (2, 6), 1)
            ],
            2: [
                Enemy("Bat", 35, (4, 9), 2),
                Enemy("Lesser Lich", 45, (5, 12), 2),
                Enemy("Undead Knight", 50, (6, 14), 2)
            ],
            3: [
                Enemy("Undying Noble", 60, (8, 16), 3),
                Enemy("Mimic", 55, (7, 15), 3),
                Enemy("Lesser Demon", 70, (10, 18), 3)
            ],
            4: [
                Enemy("Shadow Assassin", 75, (12, 20), 4),
                Enemy("Corrupted Mage", 65, (15, 25), 4),
                Enemy("Stone Golem", 90, (10, 22), 4)
            ],
            5: [
                Enemy("Elite Guard", 100, (15, 25), 5),
                Enemy("Dark Priest", 85, (18, 28), 5),
                Enemy("Chaos Beast", 110, (20, 30), 5)
            ]
        }
        
        # Zone bosses
        self.zone_bosses = {
            1: Boss("Dungeon Keeper", 120, (10, 20), 2),
            2: Boss("Necromancer", 180, (15, 25), 3),
            3: Boss("Demon Lord", 250, (20, 30), 4),
            4: Boss("Ancient Golem", 300, (25, 35), 5),
            5: Boss("Dungeon Master", 400, (30, 50), 6, flaming_sword)
        }
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def game_over(self, message):
        """End the game with a message"""
        self.clear_screen()
        print("\n" + "="*50)
        print(message)
        print("="*50 + "\n")
        exit()
    
    def display_zone_info(self):
        """Display information about the current zone"""
        zone_names = {
            1: "Dungeon Entrance",
            2: "Forgotten Catacombs",
            3: "Demon's Lair",
            4: "Ancient Ruins",
            5: "Master's Chamber"
        }
        
        zone_descriptions = {
            1: "The entrance to the dungeon. Damp walls and flickering torches line the corridors.",
            2: "Ancient burial chambers filled with the restless dead.",
            3: "A fiery cavern where demons roam freely.",
            4: "Crumbling ruins of an ancient civilization, filled with powerful guardians.",
            5: "The final chamber where the dungeon master awaits."
        }
        
        print("\n" + "="*50)
        print(f"\033[33;1mZONE {self.current_zone}: {zone_names[self.current_zone]}\033[0m")
        print(zone_descriptions[self.current_zone])
        print("="*50 + "\n")
    
    def advance_story(self):
        """Advance the story and display the next story event"""
        if self.story_progress < len(self.story_events):
            print("\n" + "*"*50)
            print(f"\033[36;1mSTORY: {self.story_events[self.story_progress]}\033[0m")
            print("*"*50 + "\n")
            self.story_progress += 1
            time.sleep(2)
    
    def trigger_random_event(self):
        """Trigger a random event"""
        event = random.choice(self.events)
        return event
    
    def encounter_enemies(self, enemies, event_description):
        """Handle a battle with enemies"""
        self.current_enemies = enemies
        enemy_index = 0  # Track which enemy to target
        turn_counter = 0  # Track battle turns
        
        # Battle loop
        while any(enemy.health > 0 for enemy in self.current_enemies) and self.hero.health > 0:
            turn_counter += 1
            self.clear_screen()
            
            # Display event and battle info
            print("\n" + "="*50)
            print(f"\033[31;1mBATTLE!\033[0m {event_description}")
            print("="*50 + "\n")
            
            # Display health bars
            self.hero.health_bar.draw()
            print("\nEnemies:")
            for enemy in self.current_enemies:
                if enemy.health > 0:
                    enemy.health_bar.draw()
            
            # Apply status effects at the start of turn
            self.hero.apply_status_effects()
            for enemy in self.current_enemies:
                if enemy.health > 0:
                    enemy.apply_status_effects()
            
            # Update ability cooldowns
            self.hero.update_cooldowns()
            
            # Check if any enemies died from status effects
            for enemy in self.current_enemies:
                if enemy.health <= 0:
                    print(f"{enemy.name} has been defeated!")
            
            # Player's turn
            if self.hero.health > 0:
                # Select target enemy (only consider alive enemies)
                alive_enemies = [e for e in self.current_enemies if e.health > 0]
                if not alive_enemies:
                    break  # All enemies defeated
                
                # Automatically target the first alive enemy
                target_enemy = alive_enemies[0]
                
                # Show battle options
                print("\nYour turn! Choose an action:")
                print("1. Attack")
                
                # Show available abilities
                ability_options = []
                for i, (ability_name, ability_data) in enumerate(self.hero.abilities.items(), start=2):
                    if self.hero.level >= ability_data["level"] and ability_data["cooldown"] == 0:
                        print(f"{i}. {ability_name}")
                        ability_options.append(ability_name)
                    elif self.hero.level >= ability_data["level"]:
                        print(f"{i}. {ability_name} (Cooldown: {ability_data['cooldown']} turns)")
                        ability_options.append(ability_name)
                
                # Get player choice
                choice = input("Enter your choice: ")
                
                if choice == "1":
                    # Regular attack
                    self.hero.attack(target_enemy)
                elif choice.isdigit() and 2 <= int(choice) <= len(ability_options) + 1:
                    # Use ability
                    ability_index = int(choice) - 2
                    if ability_index < len(ability_options):
                        ability_name = ability_options[ability_index]
                        self.hero.use_ability(ability_name, alive_enemies)
                else:
                    print("Invalid choice. Performing regular attack.")
                    self.hero.attack(target_enemy)
            
            # Check if all enemies are defeated
            if not any(enemy.health > 0 for enemy in self.current_enemies):
                break
            
            # Enemies' turn
            for enemy in self.current_enemies:
                if enemy.health > 0:
                    # Boss enemies can use special abilities
                    if isinstance(enemy, Boss):
                        # Check for phase transition
                        enemy.check_phase_transition()
                        
                        # Try to use a special ability
                        ability_result = enemy.use_special_ability([self.hero])
                        
                        # If the boss wants to summon a minion
                        if ability_result == "summon":
                            # Create a minion based on the boss level
                            minion = Enemy(f"{enemy.name}'s Minion", enemy.health_max // 3, 
                                          (enemy.weapon.damage_range[0] // 2, enemy.weapon.damage_range[1] // 2),
                                          enemy.level - 1)
                            self.current_enemies.append(minion)
                            print(f"A {minion.name} appears!")
                        
                        # If no special ability was used, perform regular attack
                        if not ability_result or ability_result == "summon":
                            enemy.attack(self.hero)
                    else:
                        # Regular enemies might use special abilities
                        if not enemy.use_special_ability([self.hero]):
                            enemy.attack(self.hero)
                    
                    # Check if hero is defeated
                    if self.hero.health <= 0:
                        self.hero.health_bar.draw()  # Show updated health
                        self.game_over("Game Over! You were defeated by the enemy.")
            
            # Short pause between turns
            time.sleep(1.5)
        
        # Battle rewards
        total_xp = 0
        total_coins = 0
        
        for enemy in self.current_enemies:
            if isinstance(enemy, Boss):
                print(f"\033[33;1mYou have defeated the {enemy.name}!\033[0m")
            else:
                print(f"You have defeated the {enemy.name}!")
            
            # Award XP and coins
            if hasattr(enemy, 'experience_reward'):
                total_xp += enemy.experience_reward
            else:
                total_xp += 10 * (self.current_zone)
                
            if hasattr(enemy, 'coin_reward'):
                total_coins += enemy.coin_reward
            else:
                total_coins += random.randint(5, 15) * self.current_zone
        
        # Award rewards
        self.hero.add_experience(total_xp)
        self.hero.add_coins(total_coins)
        
        # Chance to find an item after battle
        if random.random() < 0.3:  # 30% chance
            item_types = ["weapon", "armor", "consumable"]
            item_type = random.choice(item_types)
            
            if item_type == "weapon" and random.random() < 0.7:
                # Find a weapon appropriate for the zone
                possible_weapons = [w for w in self.weapons if w.value <= self.current_zone * 100 and w.value > (self.current_zone - 1) * 50]
                if possible_weapons:
                    weapon = random.choice(possible_weapons)
                    self.hero.add_item(weapon)
                    self.hero.equip(weapon)
            elif item_type == "armor":
                armor_names = ["Leather Armor", "Chain Mail", "Plate Armor", "Dragon Scale", "Mystic Robe"]
                armor = Item(f"{random.choice(armor_names)}", "armor", 50 * self.current_zone, "33")
                self.hero.add_item(armor)
            elif item_type == "consumable":
                potion_types = ["Health", "Strength", "Speed"]
                potion = Item(f"{random.choice(potion_types)} Potion", "consumable", 30, "31")
                self.hero.add_item(potion)
        
        # Restore some of hero's health after battle
        heal_amount = self.hero.health_max // 5
        self.hero.health = min(self.hero.health + heal_amount, self.hero.health_max)
        print(f"You recover {heal_amount} health after the battle.")
        
        # Update health bar
        self.hero.health_bar.update()
        time.sleep(2)
    
    def handle_event_loot(self, event):
        """Handle loot from events"""
        if event.name == "Walking by a Corpse and Loot":
            # Set loot for corpse event
            loot_options = Event.generate_loot_options()
            event.loot = random.choice(loot_options)
        
        if event.loot:
            description, coins, item = event.loot
            chosen_loot = random.choice([coins, item])
            print(f"{event.name}: {event.description}")
            print(description)
            
            if isinstance(chosen_loot, int) and coins > 0:
                self.hero.add_coins(coins)
            elif isinstance(chosen_loot, (Item, Weapon)) and item:
                self.hero.add_item(item)
                if isinstance(item, Weapon):
                    choice = input(f"Do you want to equip the {item.name}? (y/n): ")
                    if choice.lower() == 'y':
                        self.hero.equip(item)
        else:
            print(f"{event.name}: {event.description}")
    
    def handle_special_event(self, event):
        """Handle special events with unique effects"""
        result = Event.handle_special_event(event.name, self.hero)
        if result:
            print(f"{event.name}: {event.description}")
            return True
        return False
    
    def explore(self):
        """Explore the current zone"""
        self.clear_screen()
        
        # Display zone info
        self.display_zone_info()
        
        # Random chance for different events
        rand = random.random()
        
        if rand < 0.1 and self.story_progress < len(self.story_events):
            # Story event
            self.advance_story()
        elif rand < 0.25:
            # Shop encounter
            self.handle_shop()
        elif rand < 0.5:
            # Random event
            event = self.trigger_random_event()
            
            if event.name == "Walking by a Corpse and Loot":
                self.handle_event_loot(event)
            elif not self.handle_special_event(event):
                print(f"\n{event.name}: {event.description}\n")
                
                # Chance for battle after event
                if random.random() < 0.6:
                    self.trigger_battle(event.description)
        else:
            # Battle encounter
            self.trigger_battle("You encounter enemies!")
        
        # Check if player can advance to next zone
        if self.boss_defeated and self.current_zone < self.max_zones:
            self.offer_zone_advancement()
    
    def trigger_battle(self, description):
        """Trigger a battle with random enemies or boss"""
        # Determine if this is a boss battle
        is_boss_battle = random.random() < 0.2 and not self.boss_defeated
        
        if is_boss_battle:
            # Boss battle
            boss = self.zone_bosses[self.current_zone]
            self.encounter_enemies([boss], f"BOSS BATTLE: {description}")
            
            # Mark boss as defeated if hero survived
            if self.hero.health > 0:
                self.boss_defeated = True
                
                # Special reward for defeating boss
                special_reward = None
                if self.current_zone == 1:
                    special_reward = Item("Dungeon Key", "key", 0, "33")
                elif self.current_zone == 2:
                    special_reward = frost_axe
                elif self.current_zone == 3:
                    special_reward = poison_dagger
                elif self.current_zone == 4:
                    special_reward = Item("Ancient Artifact", "artifact", 0, "35;1")
                elif self.current_zone == 5:
                    special_reward = flaming_sword
                
                if special_reward:
                    self.hero.add_item(special_reward)
                    if isinstance(special_reward, Weapon):
                        choice = input(f"Do you want to equip the {special_reward.name}? (y/n): ")
                        if choice.lower() == 'y':
                            self.hero.equip(special_reward)
                
                # Final boss defeated
                if self.current_zone == self.max_zones:
                    self.game_completed = True
                    self.victory()
        else:
            # Regular battle
            num_enemies = random.randint(1, 3)
            enemies = random.sample(self.zone_enemies[self.current_zone], min(num_enemies, len(self.zone_enemies[self.current_zone])))
            self.encounter_enemies(enemies, description)
    
    def offer_zone_advancement(self):
        """Offer the player to advance to the next zone"""
        print(f"\n\033[33;1mYou have defeated the boss of Zone {self.current_zone}!\033[0m")
        print(f"You can now advance to Zone {self.current_zone + 1}.")
        
        choice = input("Do you want to proceed to the next zone? (y/n): ")
        if choice.lower() == 'y':
            self.current_zone += 1
            self.boss_defeated = False
            
            # Fully restore hero's health when advancing zones
            self.hero.health = self.hero.health_max
            self.hero.health_bar.update()
            
            print(f"\033[36;1mAdvancing to Zone {self.current_zone}...\033[0m")
            time.sleep(2)
            
            # Advance story when entering new zone
            self.advance_story()
    
    def handle_shop(self):
        """Handle shop interaction"""
        self.clear_screen()
        items = self.shop.display_items()
        
        while True:
            choice = input("Enter the number of the item you want to buy (or '0' to leave): ")
            if choice.isdigit():
                choice = int(choice)
                if 0 <= choice <= len(items):
                    if choice == 0:
                        break
                    else:
                        if self.shop.buy_item(self.hero, items, choice):
                            # If it's a weapon, ask if player wants to equip it
                            if isinstance(items[choice-1], Weapon):
                                equip_choice = input(f"Do you want to equip the {items[choice-1].name}? (y/n): ")
                                if equip_choice.lower() == 'y':
                                    self.hero.equip(items[choice-1])
                        break
            else:
                print("Invalid choice. Please try again.")
    
    def view_inventory(self):
        """Display the hero's inventory"""
        self.clear_screen()
        
        # Display hero stats
        print("\n" + "="*50)
        print(f"\033[33;1m{self.hero.name} - Level {self.hero.level}\033[0m")
        print(f"Experience: {self.hero.experience}/{self.hero.experience_to_level}")
        print(f"Health: {self.hero.health}/{self.hero.health_max}")
        print(f"Strength: {self.hero.get_total_strength()} (Base: {self.hero.strength} + Bonus: {self.hero.strength_bonus})")
        print(f"Defense: {self.hero.get_total_defense()} (Base: {self.hero.defense} + Bonus: {self.hero.defense_bonus})")
        print(f"Speed: {self.hero.get_total_speed()} (Base: {self.hero.speed} + Bonus: {self.hero.speed_bonus})")
        print("="*50)
        
        # Display inventory
        weapons = [item for item in self.hero.inventory if isinstance(item, Weapon)]
        consumables = [item for item in self.hero.inventory if isinstance(item, Item) and item.item_type == "consumable"]
        equipment = [item for item in self.hero.inventory if isinstance(item, Item) and item.item_type in ["armor", "accessory"]]  
        other_items = [item for item in self.hero.inventory if isinstance(item, Item) and item.item_type not in ["consumable", "armor", "accessory"]]
        
        print("\n\033[36;1mINVENTORY:\033[0m")
        print(f"\033[33mGold: {self.hero.coins}\033[0m")
        
        print("\n\033[37;1mWeapons:\033[0m")
        if weapons:
            for i, weapon in enumerate(weapons):
                equipped = "(Equipped)" if weapon == self.hero.weapon else ""
                print(f"{i+1}. \033[{weapon.color}m{weapon.name}\033[0m - Damage: {weapon.damage_range[0]}-{weapon.damage_range[1]} {equipped}")
        else:
            print("None")
        
        print("\n\033[37;1mEquipment:\033[0m")
        if equipment:
            for i, item in enumerate(equipment):
                print(f"{i+1}. \033[{item.color}m{item.name}\033[0m")
        else:
            print("None")
        
        print("\n\033[37;1mConsumables:\033[0m")
        if consumables:
            for i, item in enumerate(consumables):
                print(f"{i+1}. \033[{item.color}m{item.name}\033[0m")
        else:
            print("None")
        
        if other_items:
            print("\n\033[37;1mOther Items:\033[0m")
            for i, item in enumerate(other_items):
                print(f"{i+1}. \033[{item.color}m{item.name}\033[0m")
        
        # Inventory actions
        print("\n\033[37;1mActions:\033[0m")
        print("1. Change Weapon")
        print("2. Use Consumable")
        print("3. Return to Main Menu")
        
        choice = input("Enter your choice: ")
        
        if choice == "1" and weapons:
            self.change_weapon(weapons)
        elif choice == "2" and consumables:
            self.use_consumable(consumables)
        
        input("\nPress Enter to continue...")
    
    def change_weapon(self, weapons):
        """Allow the player to change weapons"""
        print("\nSelect a weapon to equip:")
        for i, weapon in enumerate(weapons):
            equipped = "(Equipped)" if weapon == self.hero.weapon else ""
            print(f"{i+1}. {weapon.name} {equipped}")
        
        choice = input("Enter the number of the weapon to equip (or 0 to cancel): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(weapons):
                self.hero.equip(weapons[choice-1])
    
    def use_consumable(self, consumables):
        """Allow the player to use a consumable item"""
        print("\nSelect a consumable to use:")
        for i, item in enumerate(consumables):
            print(f"{i+1}. {item.name}")
        
        choice = input("Enter the number of the item to use (or 0 to cancel): ")
        if choice.isdigit():
            choice = int(choice)
            if 1 <= choice <= len(consumables):
                item = consumables[choice-1]
                if item.use(self.hero):
                    self.hero.inventory.remove(item)
    
    def victory(self):
        """Display victory message when game is completed"""
        self.clear_screen()
        print("\n" + "*"*50)
        print("\033[33;1mCONGRATULATIONS!\033[0m")
        print("\033[36;1mYou have defeated the Dungeon Master and completed the game!\033[0m")
        print("The artifact's power is now yours. You can feel its energy coursing through your veins.")
        print("With newfound strength, you make your way out of the dungeon and into the light.")
        print("\033[32;1mTHE END\033[0m")
        print("*"*50)
        
        # Display final stats
        print(f"\n\033[37;1mFinal Stats:\033[0m")
        print(f"Level: {self.hero.level}")
        print(f"Gold collected: {self.hero.coins}")
        print(f"Strength: {self.hero.get_total_strength()}")
        print(f"Defense: {self.hero.get_total_defense()}")
        print(f"Speed: {self.hero.get_total_speed()}")
        
        input("\nPress Enter to exit...")
        exit()
    
    def quit_game(self):
        """Quit the game"""
        self.clear_screen()
        print("Are you sure you want to quit? Your progress will be lost.")
        choice = input("(y/n): ")
        if choice.lower() == 'y':
            self.game_over("You have quit the game. Thanks for playing!")
    
    def select_weapon(self):
        """Allow the player to select a starting weapon"""
        starting_weapons = [fists, iron_sword, short_bow]
        
        self.clear_screen()
        print("\n" + "="*50)
        print("\033[36;1mWelcome to the Dungeon!\033[0m")
        print("Before you begin your adventure, choose your weapon:")
        print("="*50)
        
        for i, weapon in enumerate(starting_weapons):
            print(f"{i+1}. \033[{weapon.color}m{weapon.name}\033[0m (Damage: {weapon.damage_range[0]}-{weapon.damage_range[1]})")
        
        while True:
            choice = input("Enter your choice (1-3): ")
            if choice.isdigit() and 1 <= int(choice) <= len(starting_weapons):
                self.hero.equip(starting_weapons[int(choice)-1])
                break
            else:
                print("Invalid choice. Please try again.")
        
        # Start the story
        self.advance_story()
    
    def main_menu(self):
        """Display the main menu"""
        # First select a weapon
        self.select_weapon()
        
        while not self.game_completed:
            self.clear_screen()
            print("\n" + "="*50)
            print(f"\033[36;1mMAIN MENU\033[0m")
            print(f"Zone: {self.current_zone}/{self.max_zones} | Level: {self.hero.level} | Gold: {self.hero.coins}")
            print("="*50)
            
            print("\n1. Explore")
            print("2. View Inventory")
            print("3. Visit Shop")
            print("4. Rest (Restore Health)")
            print("5. Quit Game")
            
            choice = input("\nEnter your choice: ")
            
            if choice == "1":
                self.explore()
            elif choice == "2":
                self.view_inventory()
            elif choice == "3":
                self.handle_shop()
            elif choice == "4":
                self.rest()
            elif choice == "5":
                self.quit_game()
            else:
                print("Invalid choice. Please try again.")
                time.sleep(1)
    
    def rest(self):
        """Allow the hero to rest and restore health"""
        self.clear_screen()
        
        # Check if hero is already at full health
        if self.hero.health >= self.hero.health_max:
            print("You are already at full health!")
            time.sleep(2)
            return
        
        # Rest costs gold based on how much health is missing
        missing_health = self.hero.health_max - self.hero.health
        cost = max(5, missing_health // 2)
        
        print(f"Resting will restore you to full health for {cost} gold.")
        choice = input("Do you want to rest? (y/n): ")
        
        if choice.lower() == 'y':
            if self.hero.coins >= cost:
                self.hero.coins -= cost
                self.hero.health = self.hero.health_max
                self.hero.health_bar.update()
                print(f"\033[32mYou rest and recover to full health!\033[0m")
                
                # Clear status effects
                self.hero.status_effects = {}
                print("All status effects have been cleared.")
            else:
                print("You don't have enough gold to rest.")
        
        time.sleep(2)
