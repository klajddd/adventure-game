"""
UI module for handling game interface elements.
"""

import pygame
from typing import List, Dict, Any, Optional

class UI:
    """
    Handles the user interface elements of the game.
    """
    
    def __init__(self, screen: pygame.Surface):
        """
        Initialize the UI manager.
        
        Args:
            screen: The Pygame surface to draw on
        """
        self.screen = screen
        self.width = screen.get_width()
        self.height = screen.get_height()
        
        # Initialize fonts
        pygame.font.init()
        self.title_font = pygame.font.SysFont('Arial', 48)
        self.heading_font = pygame.font.SysFont('Arial', 32)
        self.normal_font = pygame.font.SysFont('Arial', 24)
        self.small_font = pygame.font.SysFont('Arial', 16)
        
        # Colors
        self.text_color = (255, 255, 255)
        self.highlight_color = (255, 255, 0)
        self.bg_color = (0, 0, 50)
        self.button_color = (80, 80, 200)
        self.button_hover_color = (100, 100, 255)
        self.id_card_color = (40, 40, 40)  # Dark gray for ID card
        
        # Menu options
        self.menu_options = ["Start Game", "Help", "Quit"]
        self.selected_option = 0
        
    def draw_text(self, text: str, font: pygame.font.Font, color: tuple, x: int, y: int, 
                 centered: bool = False) -> None:
        """
        Draw text on the screen.
        
        Args:
            text: The text to draw
            font: The font to use
            color: The color of the text (RGB tuple)
            x, y: The position to draw at
            centered: Whether to center the text at the given position
        """
        text_surface = font.render(text, True, color)
        if centered:
            text_rect = text_surface.get_rect(center=(x, y))
            self.screen.blit(text_surface, text_rect)
        else:
            self.screen.blit(text_surface, (x, y))
            
    def draw_menu(self) -> None:
        """Draw the main menu screen."""
        # Fill the background
        self.screen.fill(self.bg_color)
        
        # Draw the title
        self.draw_text("OOP Adventure Game", self.title_font, self.text_color, 
                     self.width // 2, 100, centered=True)
        
        # Draw the tagline
        self.draw_text("Learn Object-Oriented Programming while having fun!", 
                     self.normal_font, self.text_color, 
                     self.width // 2, 160, centered=True)
        
        # Draw the menu options
        for i, option in enumerate(self.menu_options):
            color = self.highlight_color if i == self.selected_option else self.text_color
            self.draw_text(option, self.heading_font, color,
                         self.width // 2, 250 + i * 60, centered=True)
        
        # Draw control instructions
        self.draw_text("Use UP/DOWN arrows to select, ENTER to confirm", 
                     self.small_font, self.text_color,
                     self.width // 2, self.height - 100, centered=True)
        
        # Draw OOP concept explanation
        self.draw_text("This game is built using Object-Oriented Programming concepts:",
                     self.small_font, self.text_color,
                     self.width // 2, self.height - 70, centered=True)
        self.draw_text("Classes, Inheritance, Polymorphism, Encapsulation, and Abstraction",
                     self.small_font, self.text_color,
                     self.width // 2, self.height - 50, centered=True)
                     
    def draw_player_id_card(self, player: 'Player') -> None:
        """
        Draw a player ID card in the top-right corner of the screen.
        
        Args:
            player: The player object to display info for
        """
        # Card dimensions and position
        card_width = 200
        card_height = 100
        card_x = self.width - card_width - 20
        card_y = 20
        
        # Draw card background
        card_surface = pygame.Surface((card_width, card_height))
        card_surface.set_alpha(220)  # Semi-transparent
        card_surface.fill(self.id_card_color)
        self.screen.blit(card_surface, (card_x, card_y))
        
        # Draw card border
        pygame.draw.rect(self.screen, (100, 100, 100), (card_x, card_y, card_width, card_height), 2)
        
        # Draw player name
        name_text = self.normal_font.render(player.name, True, self.highlight_color)
        self.screen.blit(name_text, (card_x + 10, card_y + 10))
        
        # Draw health bar
        health_pct = player.health / player._max_health
        bar_width = 180
        health_width = bar_width * health_pct
        
        # Health bar background (red)
        pygame.draw.rect(self.screen, (255, 0, 0), (card_x + 10, card_y + 40, bar_width, 15))
        # Health bar foreground (green)
        pygame.draw.rect(self.screen, (0, 255, 0), (card_x + 10, card_y + 40, health_width, 15))
        
        # Draw health text
        health_text = self.small_font.render(f"HP: {player.health}/{player._max_health}", True, self.text_color)
        self.screen.blit(health_text, (card_x + 10, card_y + 60))
        
        # Draw level
        level_text = self.small_font.render(f"Level: {player.level}", True, self.text_color)
        self.screen.blit(level_text, (card_x + card_width - 60, card_y + 60))
        
    def draw_player_stats(self, player: 'Player') -> None:
        """
        Draw the player's stats on the screen.
        
        Args:
            player: The player object to display stats for
        """
        # Only draw the ID card in top-right corner
        self.draw_player_id_card(player)
        
    def draw_inventory(self, inventory: List['Item']) -> None:
        """
        Draw the player's inventory screen.
        
        Args:
            inventory: The list of items in the player's inventory
        """
        # Fill the background
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 50))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        self.draw_text("Inventory", self.heading_font, self.text_color, 
                     self.width // 2, 50, centered=True)
        
        # Draw items
        if not inventory:
            self.draw_text("Your inventory is empty.", self.normal_font, self.text_color,
                         self.width // 2, self.height // 2, centered=True)
        else:
            item_y = 120
            for i, item in enumerate(inventory):
                # Draw item box
                pygame.draw.rect(self.screen, (50, 50, 100), 
                               (self.width // 4, item_y, self.width // 2, 80))
                
                # Draw item color square
                pygame.draw.rect(self.screen, item.color, 
                               (self.width // 4 + 20, item_y + 20, 40, 40))
                
                # Draw item name and description
                self.draw_text(item.name, self.normal_font, self.text_color,
                             self.width // 4 + 80, item_y + 15)
                self.draw_text(item.description, self.small_font, self.text_color,
                             self.width // 4 + 80, item_y + 45)
                
                # Draw usage instruction
                consumable_text = "(Consumable)" if item.consumable else "(Equipment)"
                self.draw_text(f"Press {i+1} to use {consumable_text}", self.small_font, 
                             self.highlight_color, self.width // 4 + 300, item_y + 20)
                
                item_y += 100
                
        # Draw instructions
        self.draw_text("Press I to close inventory", self.normal_font, self.text_color,
                     self.width // 2, self.height - 50, centered=True)
                     
    def draw_pause_menu(self) -> None:
        """Draw the pause menu."""
        # Semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        # Draw title
        self.draw_text("Game Paused", self.heading_font, self.text_color,
                     self.width // 2, self.height // 3, centered=True)
        
        # Draw options
        self.draw_text("Press ESC to resume", self.normal_font, self.text_color,
                     self.width // 2, self.height // 2, centered=True)
        self.draw_text("Press Q to quit", self.normal_font, self.text_color,
                     self.width // 2, self.height // 2 + 40, centered=True)
                     
    def draw_game_over(self) -> None:
        """Draw the game over screen."""
        # Fill screen with dark color
        self.screen.fill((50, 0, 0))
        
        # Draw game over message
        self.draw_text("Game Over", self.title_font, self.text_color,
                     self.width // 2, self.height // 3, centered=True)
        
        # Draw restart instructions
        self.draw_text("Press R to restart", self.normal_font, self.text_color,
                     self.width // 2, self.height // 2, centered=True)
        self.draw_text("Press Q to quit", self.normal_font, self.text_color,
                     self.width // 2, self.height // 2 + 40, centered=True)
                     
    def draw_victory(self) -> None:
        """Draw the victory screen."""
        # Fill screen with celebratory color
        self.screen.fill((0, 50, 0))
        
        # Draw victory message
        self.draw_text("Victory!", self.title_font, self.highlight_color,
                     self.width // 2, self.height // 3, centered=True)
        
        # Draw congratulatory message
        self.draw_text("You have completed the adventure!", self.normal_font, self.text_color,
                     self.width // 2, self.height // 2, centered=True)
        
        # Draw OOP congratulations
        self.draw_text("You've also learned about Object-Oriented Programming concepts:", 
                     self.normal_font, self.text_color,
                     self.width // 2, self.height // 2 + 60, centered=True)
        
        concepts = [
            "Classes: Blueprint templates for creating objects",
            "Inheritance: Child classes inheriting from parent classes",
            "Polymorphism: Different behavior based on object type",
            "Encapsulation: Protecting data inside classes",
            "Abstraction: Simplifying complex systems"
        ]
        
        for i, concept in enumerate(concepts):
            self.draw_text(concept, self.small_font, self.highlight_color,
                         self.width // 2, self.height // 2 + 100 + i * 25, centered=True)
        
        # Draw restart/quit instructions
        self.draw_text("Press R to play again", self.normal_font, self.text_color,
                     self.width // 2, self.height - 60, centered=True)
        self.draw_text("Press Q to quit", self.normal_font, self.text_color,
                     self.width // 2, self.height - 30, centered=True) 