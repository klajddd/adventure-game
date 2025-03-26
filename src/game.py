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

class GameState(Enum):
    """Represents the different states the game can be in."""
    MENU = auto()
    PLAYING = auto()
    INVENTORY = auto()
    DIALOGUE = auto()
    GAME_OVER = auto()
    VICTORY = auto()
    PAUSED = auto()

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
                    if self.state == GameState.PLAYING:
                        self.state = GameState.PAUSED
                    elif self.state == GameState.PAUSED:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.MENU:
                        self.running = False
                
                if self.state == GameState.MENU and event.key == pygame.K_RETURN:
                    self.state = GameState.PLAYING
                
                if self.state == GameState.PLAYING:
                    # Track directional key presses for continuous movement
                    if event.key in self.keys_pressed:
                        self.keys_pressed[event.key] = True
                        
                    if event.key == pygame.K_i:
                        self.state = GameState.INVENTORY
                    elif event.key == pygame.K_SPACE:
                        self.interact()
                
                elif self.state == GameState.INVENTORY and event.key == pygame.K_i:
                    self.state = GameState.PLAYING
            
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
            
            # Update player and room state
            self.current_room.update()
            
            # Check for room transitions
            if self.player.x < 0:
                if self.current_room.west:
                    self.current_room = self.current_room.west
                    self.player.x = self.width - self.player.width
                else:
                    # Stop at the edge of the screen if there's no room
                    self.player.x = 0
            elif self.player.x > self.width - self.player.width:
                if self.current_room.east:
                    self.current_room = self.current_room.east
                    self.player.x = 0
                else:
                    # Stop at the edge of the screen if there's no room
                    self.player.x = self.width - self.player.width
            elif self.player.y < 0:
                if self.current_room.north:
                    self.current_room = self.current_room.north
                    self.player.y = self.height - self.player.height
                else:
                    # Stop at the edge of the screen if there's no room
                    self.player.y = 0
            elif self.player.y > self.height - self.player.height:
                if self.current_room.south:
                    self.current_room = self.current_room.south
                    self.player.y = 0
                else:
                    # Stop at the edge of the screen if there's no room
                    self.player.y = self.height - self.player.height
            
            # Check player health
            if self.player.health <= 0:
                self.state = GameState.GAME_OVER
    
    def render(self):
        """Render the game screen."""
        # Fill the screen with a background color
        self.screen.fill((0, 0, 0))
        
        if self.state == GameState.MENU:
            self.ui.draw_menu()
        elif self.state == GameState.PLAYING:
            # Draw the current room
            self.current_room.draw(self.screen)
            
            # Draw the player
            self.player.draw(self.screen)
            
            # Draw the UI elements
            self.ui.draw_player_stats(self.player)
            
            # Draw tutorial message
            tutorial_text = self.font.render(self.tutorials[self.current_tutorial], True, (255, 255, 255))
            self.screen.blit(tutorial_text, (20, self.height - 40))
            
        elif self.state == GameState.INVENTORY:
            self.ui.draw_inventory(self.player.inventory)
        elif self.state == GameState.PAUSED:
            self.ui.draw_pause_menu()
        elif self.state == GameState.GAME_OVER:
            self.ui.draw_game_over()
        elif self.state == GameState.VICTORY:
            self.ui.draw_victory()
        
        # Update the display
        pygame.display.flip()
    
    def interact(self):
        """Handle player interactions with the environment."""
        # Check for items to pick up or NPCs to talk to
        for item in self.current_room.items[:]:
            if self.player.collides_with(item):
                self.player.add_to_inventory(item)
                self.current_room.items.remove(item)
                print(f"Picked up {item.name}")
        
        # Check for enemies to battle
        for enemy in self.current_room.enemies[:]:
            if self.player.collides_with(enemy):
                result = self.player.attack(enemy)
                if result:
                    print(f"Defeated {enemy.name}")
                    self.current_room.enemies.remove(enemy)
                else:
                    print(f"Attacked {enemy.name}, health: {enemy.health}")
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
            self.clock.tick(self.FPS) 