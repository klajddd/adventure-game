"""
Player module with the Player class that handles player attributes, inventory, and actions.
"""

import pygame
from typing import List, Optional

class Player:
    """
    Player class representing the character controlled by the user.
    This class demonstrates encapsulation by protecting attributes like health.
    """
    
    def __init__(self, name: str, health: int, x: int = 400, y: int = 300):
        """
        Initialize a new Player instance.
        
        Args:
            name: The player's name
            health: The player's starting health
            x: The player's starting x position
            y: The player's starting y position
        """
        self.name = name
        self._health = health  # Encapsulated health attribute
        self._max_health = health
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.inventory = []
        self.speed = 5  # Movement speed per frame
        self.attack_power = 10
        self.defense = 5
        self.level = 1
        self.experience = 0
        self.experience_to_level = 100
        
        # Sprite and animation
        self.color = (0, 255, 0)  # Default color: green
        
    @property
    def health(self) -> int:
        """Get the player's current health."""
        return self._health
        
    @health.setter
    def health(self, value: int):
        """Set the player's health with validation."""
        if value < 0:
            self._health = 0
        elif value > self._max_health:
            self._health = self._max_health
        else:
            self._health = value
            
    def take_damage(self, amount: int) -> None:
        """Reduce the player's health by the given amount."""
        damage = max(1, amount - self.defense)
        self.health -= damage
        print(f"{self.name} takes {damage} damage!")
        
    def heal(self, amount: int) -> None:
        """Increase the player's health by the given amount."""
        self.health += amount
        print(f"{self.name} heals for {amount} health!")
        
    def move(self, dx: int, dy: int) -> None:
        """
        Move the player by the given delta x and y, multiplied by speed.
        This method is called continuously when a movement key is held down.
        
        Args:
            dx: Delta x direction (-1 for left, 1 for right, 0 for no horizontal movement)
            dy: Delta y direction (-1 for up, 1 for down, 0 for no vertical movement)
        """
        # Apply movement based on speed
        self.x += dx * self.speed
        self.y += dy * self.speed
        
    def add_to_inventory(self, item: 'Item') -> None:
        """Add an item to the player's inventory."""
        self.inventory.append(item)
        
    def remove_from_inventory(self, item: 'Item') -> None:
        """Remove an item from the player's inventory."""
        if item in self.inventory:
            self.inventory.remove(item)
            
    def use_item(self, item_index: int) -> bool:
        """Use an item from the inventory."""
        if 0 <= item_index < len(self.inventory):
            item = self.inventory[item_index]
            result = item.use(self)
            if item.consumable:
                self.inventory.pop(item_index)
            return result
        return False
        
    def attack(self, target: 'Enemy') -> bool:
        """
        Attack an enemy, dealing damage based on attack power.
        Returns True if the enemy is defeated, False otherwise.
        """
        damage = self.attack_power
        target.take_damage(damage)
        
        # If the enemy is still alive, they counter-attack
        if target.health > 0:
            target.attack(self)
            return False
        else:
            self.gain_experience(target.experience_value)
            return True
            
    def gain_experience(self, amount: int) -> None:
        """
        Add experience to the player and level up if enough experience is gained.
        """
        self.experience += amount
        print(f"{self.name} gains {amount} experience!")
        
        # Check for level up
        if self.experience >= self.experience_to_level:
            self.level_up()
            
    def level_up(self) -> None:
        """
        Increase the player's level and stats.
        """
        self.experience -= self.experience_to_level
        self.level += 1
        self._max_health += 10
        self.health = self._max_health
        self.attack_power += 2
        self.defense += 1
        self.experience_to_level = int(self.experience_to_level * 1.5)
        print(f"{self.name} leveled up to level {self.level}!")
        
    def collides_with(self, entity: 'Entity') -> bool:
        """
        Check if the player collides with another entity.
        """
        # Simple box collision
        return (
            self.x < entity.x + entity.width and
            self.x + self.width > entity.x and
            self.y < entity.y + entity.height and
            self.y + self.height > entity.y
        )
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the player on the screen.
        """
        # Draw a simple rectangle for the player
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw player name above rectangle
        font = pygame.font.SysFont('Arial', 18)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.x + self.width // 2 - name_text.get_width() // 2, self.y - 20)) 