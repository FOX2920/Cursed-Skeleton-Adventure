import random

# ------------ class setup ------------
class Weapon:
    def __init__(self,
                 name: str,
                 weapon_type: str,
                 damage_range: tuple,
                 value: int,
                 color: str = "37"
                 ) -> None:
        self.name = name
        self.weapon_type = weapon_type
        self.damage_range = damage_range
        self.value = value
        self.color = color
        self.damage_boost = 0  # Temporary damage boost from potions
        self.special_effect = None  # Special effect like poison, burn, etc.
        self.special_effect_chance = 0.2  # 20% chance to apply special effect
        
    def get_damage(self):
        """Calculate damage with random range and any boosts"""
        base_damage = random.randint(self.damage_range[0], self.damage_range[1])
        total_damage = base_damage + self.damage_boost
        return total_damage
        
    def has_special_effect(self):
        """Check if weapon applies a special effect on hit"""
        if self.special_effect and random.random() < self.special_effect_chance:
            return self.special_effect
        return None

# ------------ object creation ------------
iron_sword = Weapon(name="Iron Sword",
                    weapon_type="sharp",
                    damage_range=(5, 99),
                    value=10,
                    color="37")  # Silver

short_bow = Weapon(name="Short Bow",
                   weapon_type="ranged",
                   damage_range=(3, 8),
                   value=8,
                   color="33")  # Brown

fists = Weapon(name="Fists",
               weapon_type="blunt",
               damage_range=(1, 3),
               value=0,
               color="31")  # Red

# Advanced weapons with special effects
flaming_sword = Weapon(name="Flaming Sword",
                      weapon_type="sharp",
                      damage_range=(15, 25),
                      value=300,
                      color="31;1")  # Bold Red
flaming_sword.special_effect = "burn"  # Deals extra damage over time

frost_axe = Weapon(name="Frost Axe",
                  weapon_type="sharp",
                  damage_range=(12, 22),
                  value=250,
                  color="36;1")  # Bold Cyan
frost_axe.special_effect = "freeze"  # Slows enemy attacks

poison_dagger = Weapon(name="Poison Dagger",
                      weapon_type="sharp",
                      damage_range=(8, 15),
                      value=200,
                      color="32;1")  # Bold Green
poison_dagger.special_effect = "poison"  # Deals damage over time
