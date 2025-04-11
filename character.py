# ------------ imports ------------
import random
from weapon import fists
from health_bar import HealthBar


# ------------ parent class setup ------------
class Character:
    def __init__(self,
                 name: str,
                 health: int,
                 ) -> None:
        self.name = name
        self.health = health
        self.health_max = health
        
        # Base stats
        self.strength = 5  # Affects damage
        self.defense = 5   # Reduces damage taken
        self.speed = 5     # Affects turn order and dodge chance
        
        # Stat bonuses from items/buffs
        self.strength_bonus = 0
        self.defense_bonus = 0
        self.speed_bonus = 0
        
        # Status effects
        self.status_effects = {}
        
        self.weapon = fists
        self.health_bar = None

    def get_total_strength(self):
        return self.strength + self.strength_bonus
        
    def get_total_defense(self):
        return self.defense + self.defense_bonus
        
    def get_total_speed(self):
        return self.speed + self.speed_bonus

    def attack(self, target) -> None:
        # Calculate damage with weapon and strength
        base_damage = self.weapon.get_damage()
        damage_bonus = self.get_total_strength() // 2
        total_damage = base_damage + damage_bonus
        
        # Check for critical hit (10% chance)
        is_critical = random.random() < 0.1
        if is_critical:
            total_damage = int(total_damage * 1.5)
            
        # Check for dodge (based on target's speed)
        dodge_chance = min(0.05 + (target.get_total_speed() - self.get_total_speed()) * 0.01, 0.25)
        is_dodged = random.random() < dodge_chance
        
        if is_dodged:
            print(f"{target.name} dodged the attack from {self.name}!")
            return
            
        # Apply defense reduction
        damage_reduction = target.get_total_defense() // 3
        final_damage = max(1, total_damage - damage_reduction)
        
        # Apply damage
        target.health -= final_damage
        target.health = max(target.health, 0)
        if target.health_bar:
            target.health_bar.update()
            
        # Display attack message
        crit_text = " CRITICAL HIT!" if is_critical else ""
        print(f"{self.name} dealt {final_damage} damage to "
              f"{target.name} with {self.weapon.name}{crit_text}")
              
        # Apply weapon special effects
        effect = self.weapon.has_special_effect()
        if effect and target.health > 0:
            if effect == "burn":
                target.status_effects["burn"] = {"duration": 3, "damage": final_damage // 4}
                print(f"{target.name} is burning!")
            elif effect == "poison":
                target.status_effects["poison"] = {"duration": 3, "damage": final_damage // 3}
                print(f"{target.name} is poisoned!")
            elif effect == "freeze":
                target.status_effects["freeze"] = {"duration": 2, "slow": 2}
                print(f"{target.name} is frozen!")
    
    def apply_status_effects(self):
        """Apply all active status effects and reduce their duration"""
        effects_to_remove = []
        
        for effect, data in self.status_effects.items():
            if effect == "burn" or effect == "poison":
                damage = data["damage"]
                self.health -= damage
                self.health = max(0, self.health)
                if self.health_bar:
                    self.health_bar.update()
                print(f"{self.name} took {damage} damage from {effect}!")
            
            data["duration"] -= 1
            if data["duration"] <= 0:
                effects_to_remove.append(effect)
                print(f"{effect.capitalize()} effect on {self.name} has worn off.")
        
        # Remove expired effects
        for effect in effects_to_remove:
            del self.status_effects[effect]


# ------------ subclass setup ------------
class Hero(Character):
    def __init__(self,
                 name: str,
                 health: int
                 ) -> None:
        super().__init__(name=name, health=health)

        self.default_weapon = self.weapon
        self.health_bar = HealthBar(self, color="green")
        
        # Inventory and progression
        self.inventory = []
        self.coins = 50  # Start with some coins
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        
        # Special abilities
        self.abilities = {
            "Heroic Strike": {"level": 1, "cooldown": 0, "max_cooldown": 3},
            "Quick Recovery": {"level": 3, "cooldown": 0, "max_cooldown": 5},
            "Whirlwind": {"level": 5, "cooldown": 0, "max_cooldown": 7}
        }

    def equip(self, weapon) -> None:
        self.weapon = weapon
        print(f"{self.name} equipped a(n) {self.weapon.name}!")

    def drop(self) -> None:
        print(f"{self.name} dropped the {self.weapon.name}!")
        self.weapon = self.default_weapon
        
    def add_item(self, item):
        self.inventory.append(item)
        print(f"\033[{item.color}mYou have looted {item.name}!\033[0m")
        
    def add_coins(self, amount):
        self.coins += amount
        print(f"\033[33mYou have looted {amount} gold coins!\033[0m")
        
    def add_experience(self, amount):
        self.experience += amount
        print(f"You gained {amount} experience points!")
        
        # Check for level up
        while self.experience >= self.experience_to_level:
            self.level_up()
    
    def level_up(self):
        self.level += 1
        self.experience -= self.experience_to_level
        self.experience_to_level = int(self.experience_to_level * 1.5)
        
        # Increase stats
        stat_increase = 2
        self.health_max += 10
        self.health = self.health_max
        self.strength += stat_increase
        self.defense += stat_increase
        self.speed += stat_increase
        
        print(f"\033[33;1m*** LEVEL UP! ***\033[0m")
        print(f"You are now level {self.level}!")
        print(f"Health: +10, Strength: +{stat_increase}, Defense: +{stat_increase}, Speed: +{stat_increase}")
        
        # Check for new abilities
        for ability, data in self.abilities.items():
            if data["level"] == self.level:
                print(f"\033[36;1mNew ability unlocked: {ability}!\033[0m")
    
    def use_ability(self, ability_name, targets):
        if ability_name not in self.abilities:
            print(f"You don't have the {ability_name} ability.")
            return False
            
        ability = self.abilities[ability_name]
        
        # Check if ability is unlocked
        if self.level < ability["level"]:
            print(f"{ability_name} unlocks at level {ability['level']}.")
            return False
            
        # Check cooldown
        if ability["cooldown"] > 0:
            print(f"{ability_name} is on cooldown for {ability['cooldown']} more turns.")
            return False
            
        # Use the ability
        if ability_name == "Heroic Strike":
            if not targets or len(targets) < 1:
                print("No target for Heroic Strike.")
                return False
                
            target = targets[0]
            base_damage = self.weapon.get_damage() * 2
            target.health -= base_damage
            target.health = max(0, target.health)
            if target.health_bar:
                target.health_bar.update()
            print(f"\033[33;1mHEROIC STRIKE!\033[0m You deal {base_damage} damage to {target.name}!")
            
        elif ability_name == "Quick Recovery":
            heal_amount = self.health_max // 3
            self.health = min(self.health + heal_amount, self.health_max)
            self.health_bar.update()
            print(f"\033[32;1mQUICK RECOVERY!\033[0m You heal for {heal_amount} health!")
            
        elif ability_name == "Whirlwind":
            if not targets:
                print("No targets for Whirlwind.")
                return False
                
            base_damage = self.weapon.get_damage() // 2
            print(f"\033[31;1mWHIRLWIND ATTACK!\033[0m")
            for target in targets:
                target.health -= base_damage
                target.health = max(0, target.health)
                if target.health_bar:
                    target.health_bar.update()
                print(f"You deal {base_damage} damage to {target.name}!")
        
        # Set cooldown
        ability["cooldown"] = ability["max_cooldown"]
        return True
    
    def update_cooldowns(self):
        """Reduce cooldowns for all abilities"""
        for ability in self.abilities.values():
            if ability["cooldown"] > 0:
                ability["cooldown"] -= 1


# ------------ subclass setup ------------
class Enemy(Character):
    def __init__(self,
                 name: str,
                 health: int,
                 damage_range: tuple,
                 level: int = 1,
                 weapon = None,
                 ) -> None:
        super().__init__(name=name, health=health)
        
        # Create a basic weapon if none provided
        if weapon is None:
            from weapon import Weapon
            weapon = Weapon(f"{name}'s Attack", "natural", damage_range, 0, "31")
            
        self.weapon = weapon
        self.level = level
        self.health_bar = HealthBar(self, color="red")
        
        # Scale stats based on level
        self.strength = 5 + (level - 1) * 2
        self.defense = 5 + (level - 1) * 1
        self.speed = 5 + (level - 1) * 1
        
        # Experience and gold rewards
        self.experience_reward = 20 * level
        self.coin_reward = random.randint(5 * level, 15 * level)
        
        # Special abilities for higher level enemies
        self.special_abilities = []
        if level >= 3:
            self.special_abilities.append("Power Attack")
        if level >= 5:
            self.special_abilities.append("Heal")
    
    def use_special_ability(self, targets):
        """Use a special ability if available"""
        if not self.special_abilities or random.random() > 0.3:  # 30% chance to use special ability
            return False
            
        ability = random.choice(self.special_abilities)
        
        if ability == "Power Attack":
            if not targets:
                return False
                
            target = targets[0]
            base_damage = self.weapon.get_damage() * 1.5
            target.health -= base_damage
            target.health = max(0, target.health)
            if target.health_bar:
                target.health_bar.update()
            print(f"\033[31;1m{self.name} uses POWER ATTACK!\033[0m Dealing {base_damage} damage to {target.name}!")
            return True
            
        elif ability == "Heal":
            if self.health >= self.health_max * 0.8:  # Only heal if below 80% health
                return False
                
            heal_amount = self.health_max // 5
            self.health = min(self.health + heal_amount, self.health_max)
            self.health_bar.update()
            print(f"\033[32;1m{self.name} uses HEAL!\033[0m Recovering {heal_amount} health!")
            return True
            
        return False


# ------------ boss subclass ------------
class Boss(Enemy):
    def __init__(self,
                 name: str,
                 health: int,
                 damage_range: tuple,
                 level: int = 5,
                 weapon = None,
                 ) -> None:
        super().__init__(name=name, health=health, damage_range=damage_range, level=level, weapon=weapon)
        
        # Bosses have enhanced stats
        self.health *= 2
        self.health_max = self.health
        self.strength += 5
        self.defense += 5
        self.speed += 3
        
        # Better rewards
        self.experience_reward *= 3
        self.coin_reward *= 3
        
        # Boss-specific abilities
        self.special_abilities.append("Ultimate Attack")
        self.special_abilities.append("Summon Minion")
        self.health_bar = HealthBar(self, color="purple")
        
        # Boss phases
        self.phase = 1
        self.phase_thresholds = [0.7, 0.4, 0.2]  # At 70%, 40%, and 20% health
        self.current_phase_index = 0
    
    def check_phase_transition(self):
        """Check if boss should transition to next phase"""
        if self.current_phase_index >= len(self.phase_thresholds):
            return False
            
        health_percent = self.health / self.health_max
        if health_percent <= self.phase_thresholds[self.current_phase_index]:
            self.phase += 1
            self.current_phase_index += 1
            
            # Buff boss in new phase
            self.strength += 3
            self.defense += 2
            
            print(f"\033[35;1m{self.name} enters Phase {self.phase}!\033[0m")
            print(f"\033[35;1m{self.name}'s power increases!\033[0m")
            return True
            
        return False
    
    def use_special_ability(self, targets):
        """Enhanced special abilities for bosses"""
        # Always use special abilities in later phases
        ability_chance = 0.3 + (self.phase - 1) * 0.2  # Increases with each phase
        
        if random.random() > ability_chance:
            return False
            
        ability = random.choice(self.special_abilities)
        
        if ability == "Ultimate Attack" and self.phase >= 2:  # Only available in phase 2+
            if not targets:
                return False
                
            target = targets[0]
            base_damage = self.weapon.get_damage() * 2.5
            target.health -= base_damage
            target.health = max(0, target.health)
            if target.health_bar:
                target.health_bar.update()
            print(f"\033[31;1m{self.name} uses ULTIMATE ATTACK!\033[0m")
            print(f"A devastating blow deals {base_damage} damage to {target.name}!")
            return True
            
        elif ability == "Summon Minion" and self.phase >= 3:  # Only available in phase 3+
            print(f"\033[35;1m{self.name} SUMMONS A MINION!\033[0m")
            # The actual summoning logic would be handled in the game class
            return "summon"
            
        return super().use_special_ability(targets)  # Use regular abilities
