# Dungeon Crawler: A Text-Based Battle Adventure

A dungeon crawler RPG with turn-based combat, inventory management, and character progression, built entirely in Python.

## Game Overview

In Dungeon Crawler, you awaken in a dark dungeon with no memory of how you got there. Armed with only your wits, you must fight your way through the dungeon, defeat enemies, and uncover the secrets within. The game features:

- **Turn-based combat** with a variety of enemies and bosses
- **Character progression** with level-ups and ability unlocks
- **Inventory management** with weapons, armor, and consumable items
- **Shop system** to purchase new equipment and items
- **Random events** that can help or hinder your adventure
- **Multiple zones** with increasing difficulty
- **Boss battles** with unique mechanics and rewards
- **Status effects** like poison, burn, and freeze
- **Special abilities** that unlock as you level up

## Game Structure

The game is built using object-oriented programming principles, with the following components:

### Core Classes

- **Game**: Manages the game state, combat, exploration, and menus
- **Character**: Base class for all characters in the game
  - **Hero**: Player character with inventory, equipment, and abilities
  - **Enemy**: Standard enemies with scaling difficulty
  - **Boss**: Powerful enemies with phases and special abilities
- **Weapon**: Various weapons with different damage ranges and special effects
- **Item**: Consumables, armor, and other items that can be used or equipped
- **Shop**: Allows the player to purchase items and equipment
- **Event**: Random encounters that can provide loot or special effects
- **HealthBar**: Visual representation of character health with status indicators

### Game Zones

The game features 5 zones with increasing difficulty:

1. **Dungeon Entrance**: The starting area with basic enemies
2. **Forgotten Catacombs**: Ancient burial chambers with undead enemies
3. **Demon's Lair**: A fiery cavern with demonic foes
4. **Ancient Ruins**: Crumbling ruins with powerful guardians
5. **Master's Chamber**: The final area where the dungeon master awaits

Each zone has its own set of enemies and a powerful boss that must be defeated to progress.

## How to Play

1. Run `main.py` to start the game
2. Choose your starting weapon
3. Navigate through the main menu to explore, manage your inventory, visit the shop, or rest
4. Battle enemies, collect loot, and level up your character
5. Defeat the boss of each zone to progress to the next area
6. Defeat the final boss to complete the game

## Controls

The game uses simple text-based controls:
- Enter the number or letter corresponding to your choice
- Follow the prompts to navigate menus, battle enemies, and interact with the game world

## Requirements

- Python 3.6 or higher
- No external libraries required

## Credits

This game was created as a demonstration of object-oriented programming in Python, featuring class inheritance, encapsulation, and polymorphism.
