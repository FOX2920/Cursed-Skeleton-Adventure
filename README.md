# Cursed Skeleton Adventure

## Overview

**Cursed Skeleton Adventure** is a text-based adventure game where you play as a cursed skeleton striving to reach the surface from the depths of a forgotten castle dungeon. Along the journey, you'll encounter various events, face enemies, collect weapons, and experience an engaging story that offers multiple endings.

## Features

- **Hero and Enemy Health Bars**: Visual representation of health with green bars for heroes and red bars for enemies.
- **Weapon System**: Equip different weapons like Iron Sword, Short Bow, or use your Fists.
- **Random Events**: Encounter diverse and unpredictable events that add depth to the gameplay.
- **Enemy Encounters**: Face off against various enemies, each with unique health and attack stats.
- **Inventory Management**: Keep track of your collected items and weapons.
- **Game Over Scenarios**: Multiple ways to end the game, either by quitting or being defeated.

## Classes

### Weapon

Represents different types of weapons with specific attributes like name, type, damage range, and value.

### HealthBar

Displays the health of heroes and enemies visually.

### Character

A base class for all characters in the game with attributes like name, health, and weapon.

### Hero

Inherits from Character, representing the player's character with additional inventory management and weapon equipping capabilities.

### Enemy

Inherits from Character, representing various enemies with their own attack damage.

### Event

Defines random events with a name and description to enrich the gameplay experience.

### Game

Manages the overall game flow including hero creation, event triggering, enemy encounters, and main menu navigation.

## Getting Started

### Prerequisites

- Python 3.x
- Compatible terminal or command prompt

### Running the Game

1. Clone the repository or download the game files.
2. Open a terminal or command prompt.
3. Navigate to the directory containing the game files.
4. Run the game using the command:
   ```sh
   python game.py
   ```

## Gameplay

1. **Weapon Selection**: At the start of the game, select a weapon to equip your hero.
2. **Main Menu**: Navigate through the main menu to explore, view inventory, or quit the game.
3. **Exploration**: Encounter random events and enemies as you explore the dungeon.
4. **Combat**: Engage in battles with enemies, utilizing your equipped weapon.
5. **Inventory**: Check and manage your inventory of collected items and weapons.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.
