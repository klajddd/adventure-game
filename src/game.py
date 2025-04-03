"""
Game module containing the main Game class that handles the game loop and state.
"""

import os
import sys
import pygame
from enum import Enum, auto

from src.player import Player
from src.rooms import Room, RoomFactory
from src.ui import UI
from src.npc import NPC

class GameState(Enum):
    """Represents the different states the game can be in."""
    MENU = auto()
    PLAYING = auto()
    DIALOGUE = auto()

class Game:
    """Main game class that manages the game loop and coordinates game components."""
    
    def __init__(self, width, height, title):
        """Initialize the game with screen dimensions and title."""
        self.width = width
        self.height = height
        self.title = title
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        
        # Set up the game clock
        self.clock = pygame.time.Clock()
        self.FPS = 60
        
        # Game state
        self.running = True
        self.state = GameState.MENU
        
        # Game objects
        self.player = Player("Hero", 100, 50, 10)
        self.room_factory = RoomFactory()
        self.current_room = self.room_factory.create_starting_room()
        
        # Create NPC
        self.npc = NPC("X", 700, 300)  # Position X on the right side of the screen
        
        # UI elements
        self.ui = UI(self.screen)
        
        # Font setup
        pygame.font.init()
        self.font = pygame.font.SysFont('Arial', 24)
        
        # Tutorial messages to teach OOP concepts
        self.tutorials = [
            "Welcome to the OOP Adventure Game! This game teaches object-oriented programming concepts.",
            "CLASSES: Notice how our player is an OBJECT created from the Player CLASS.",
            "INHERITANCE: Different enemy types inherit from a base Enemy class.",
            "POLYMORPHISM: Items behave differently when used based on their type.",
            "ENCAPSULATION: The player's health is protected and can only be changed through methods."
        ]
        self.current_tutorial = 0
        self.tutorial_timer = 0
        self.tutorial_duration = 300  # 5 seconds at 60 FPS
        
        # Track key presses for continuous movement
        self.keys_pressed = {
            pygame.K_UP: False,
            pygame.K_DOWN: False,
            pygame.K_LEFT: False,
            pygame.K_RIGHT: False,
        }
        
    def handle_events(self):
        """Process all game events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if self.state == GameState.DIALOGUE:
                        self.npc.end_dialogue()
                        self.state = GameState.PLAYING
                    else:
                        self.running = False
                
                if self.state == GameState.MENU and event.key == pygame.K_RETURN:
                    self.state = GameState.PLAYING
                
                elif self.state == GameState.PLAYING:
                    # Track directional key presses for continuous movement
                    if event.key in self.keys_pressed:
                        self.keys_pressed[event.key] = True
                    
                    # Check for dialogue initiation
                    if event.key == pygame.K_t:
                        # Check if player is close enough to NPC
                        dx = abs(self.player.x - self.npc.x)
                        dy = abs(self.player.y - self.npc.y)
                        if dx < 100 and dy < 100:  # Within interaction range
                            self.state = GameState.DIALOGUE
                            self.npc.start_dialogue()
                
                elif self.state == GameState.DIALOGUE:
                    self.npc.handle_input(event)
            
            elif event.type == pygame.KEYUP:
                # Stop tracking key when released
                if event.key in self.keys_pressed:
                    self.keys_pressed[event.key] = False
    
    def update(self):
        """Update the game state."""
        if self.state == GameState.PLAYING:
            # Update tutorial messages
            self.tutorial_timer += 1
            if self.tutorial_timer > self.tutorial_duration:
                self.tutorial_timer = 0
                self.current_tutorial = (self.current_tutorial + 1) % len(self.tutorials)
            
            # Handle continuous movement based on keys being pressed
            if self.keys_pressed[pygame.K_UP]:
                self.player.move(0, -1)
            if self.keys_pressed[pygame.K_DOWN]:
                self.player.move(0, 1)
            if self.keys_pressed[pygame.K_LEFT]:
                self.player.move(-1, 0)
            if self.keys_pressed[pygame.K_RIGHT]:
                self.player.move(1, 0)
            
            # Keep player within screen bounds
            self.player.x = max(0, min(self.player.x, self.width - self.player.width))
            self.player.y = max(0, min(self.player.y, self.height - self.player.height))
    
    def render(self):
        """Render the game screen."""
        if self.state == GameState.MENU:
            self.ui.draw_menu()
        else:
            # Draw the current room
            self.current_room.draw(self.screen)
            
            # Draw the NPC
            self.npc.draw(self.screen)
            
            # Draw the player
            self.player.draw(self.screen)
            
            # Draw the UI elements
            self.ui.draw_player_stats(self.player)
            
            # Draw tutorial message (only when not in dialogue)
            if self.state == GameState.PLAYING:
                tutorial_text = self.font.render(self.tutorials[self.current_tutorial], True, (255, 255, 255))
                self.screen.blit(tutorial_text, (20, self.height - 40))
                
                # Draw interaction prompt when near NPC
                dx = abs(self.player.x - self.npc.x)
                dy = abs(self.player.y - self.npc.y)
                if dx < 100 and dy < 100:
                    prompt_text = self.font.render("Press T to talk", True, (255, 255, 0))
                    self.screen.blit(prompt_text, (self.width // 2 - prompt_text.get_width() // 2, 50))
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS) 