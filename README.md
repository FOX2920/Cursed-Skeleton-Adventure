
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

Inherits from Character, representing the player's character with additional inventory management and weapon equipping functionalities.

### Enemy

Inherits from Character, representing various enemies with specific health and damage attributes.

### Event

Represents random events that the player may encounter during exploration.

### Game

Manages the game flow, including hero creation, enemy encounters, random events, and user interactions.

## Gameplay

1. **Select Your Weapon**: Choose from available weapons to equip your hero.
2. **Main Menu**:
    - **Explore**: Trigger random events and possibly encounter enemies.
    - **View Inventory**: Check your collected items and weapons.
    - **Quit**: Exit the game.

## Installation

To play the game, simply run the `main.py` script.

## Requirements

- Python 3.x

## How to Run

1. Ensure you have Python 3 installed.
2. Download the game files.
3. Run the game by executing:

```sh
python main.py
```

Enjoy your adventure as the cursed skeleton!
