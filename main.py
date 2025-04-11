#!/usr/bin/env python3

"""
Text-Based Battle Game

A dungeon crawler RPG with turn-based combat, inventory management,
and character progression.
"""

import os
import time
from game import Game

def display_intro():
    """Display the game introduction"""
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n" + "="*60)
    print("\033[36;1m"
          "                DUNGEON CRAWLER                \n"
          "          A Text-Based Battle Adventure        "
          "\033[0m")
    print("="*60)
    print("\nYou awaken in a dark dungeon with no memory of how you got here.")
    print("Armed with only your wits, you must fight your way through")
    print("the dungeon, defeat enemies, and uncover the secrets within.")
    print("\nControls are simple - just follow the prompts and enter")
    print("the number or letter corresponding to your choice.")
    print("\nGood luck, adventurer! You'll need it...")
    print("\n" + "="*60)
    input("\nPress Enter to begin your adventure...")

def main():
    """Main entry point for the game"""
    display_intro()
    game = Game()
    game.main_menu()

if __name__ == "__main__":
    main()