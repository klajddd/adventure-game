#!/usr/bin/env python3
"""
Main entry point for the OOP Adventure Game.
This file initializes the game and handles high-level program flow.
"""

import os
import sys
import pygame

# Add the src directory to the path so we can import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.game import Game

def main():
    """Initialize and run the game."""
    # Initialize pygame
    pygame.init()
    
    # Get the screen dimensions based on the user's display
    display_info = pygame.display.Info()
    width, height = 1000, 1000  # Default fallback resolution
    
    # Create the game instance
    game = Game(width, height, "OOP Adventure Game")
    
    # Run the game
    game.run()
    
    # Clean up
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main() 