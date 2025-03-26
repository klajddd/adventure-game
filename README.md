# OOP Adventure Game

## Introduction

This is an object-oriented programming (OOP) adventure game built using Python and Pygame. The game serves as a learning tool for understanding object-oriented programming concepts while having fun with a text-based adventure game.

## Learning Objectives

- Understand classes and objects
- Implement inheritance and polymorphism
- Use encapsulation and abstraction
- Apply design patterns in game development

## Directory Structure

```
adventure_game/
├── assets/
│   ├── images/     # Game images and sprites
│   └── sounds/     # Game sound effects and music
├── src/            # Source code files
│   ├── main.py     # Entry point of the game
│   ├── game.py     # Game class and main game loop
│   ├── player.py   # Player class
│   ├── items.py    # Item classes
│   ├── enemies.py  # Enemy classes
│   ├── rooms.py    # Room/location classes
│   └── ui.py       # User interface classes
└── README.md       # This file
```

## Installation and Running

1. Ensure you have Python 3.6+ installed
2. Install required packages: `pip install pygame`
3. Run the game: `python adventure_game/src/main.py`

## Controls

- Arrow keys: Navigate through the game world
- Space/Enter: Interact with objects/NPCs
- I: Open inventory
- ESC: Pause menu

## Game Features

- Text-based adventure with simple graphics
- Inventory system for collecting and using items
- Multiple areas to explore
- Enemies to battle
- Puzzles to solve

## OOP Concepts Demonstrated

Each file and class in the game demonstrates specific OOP principles:

- **Inheritance**: Enemy types inherit from a base Enemy class
- **Polymorphism**: Different items behave differently when used
- **Encapsulation**: Game state and player attributes are protected
- **Abstraction**: Complex systems are simplified into class interfaces
