"""
Enemies module containing various enemy classes that the player can battle.
This module demonstrates inheritance and polymorphism through different enemy types.
"""

import pygame
import random
from typing import Optional, List, Tuple

from src.items import Entity

class Enemy(Entity):
    """
    Base class for all enemies in the game.
    This demonstrates inheritance from the Entity class.
    """
    
    def __init__(self, name: str, health: int, attack: int, defense: int, x: int, y: int):
        """
        Initialize a new Enemy.
        
        Args:
            name: The enemy's name
            health: The enemy's starting health
            attack: The enemy's attack power
            defense: The enemy's defense
            x: The enemy's x position
            y: The enemy's y position
        """
        super().__init__(name, x, y, 40, 40)
        self._health = health
        self._max_health = health
        self.attack_power = attack
        self.defense = defense
        self.color = (255, 0, 0)  # Red
        self.experience_value = health + attack + defense
        self.move_counter = 0
        self.move_direction = (0, 0)
        
    @property
    def health(self) -> int:
        """Get the enemy's current health."""
        return self._health
        
    @health.setter
    def health(self, value: int):
        """Set the enemy's health with validation."""
        if value < 0:
            self._health = 0
        elif value > self._max_health:
            self._health = self._max_health
        else:
            self._health = value
            
    def take_damage(self, amount: int) -> None:
        """
        Reduce the enemy's health by the given amount, accounting for defense.
        
        Args:
            amount: The amount of damage to take
        """
        damage = max(1, amount - self.defense)
        self.health -= damage
        print(f"{self.name} takes {damage} damage!")
        
    def attack(self, target: 'Player') -> None:
        """
        Attack a target, dealing damage based on attack power.
        
        Args:
            target: The target to attack (usually the player)
        """
        damage = self.attack_power
        print(f"{self.name} attacks {target.name} for {damage} damage!")
        target.take_damage(damage)
        
    def update(self) -> None:
        """Update the enemy's state each frame."""
        # Simple AI - move randomly every few frames
        self.move_counter += 1
        if self.move_counter >= 30:  # Change direction every 30 frames
            self.move_counter = 0
            # Random direction: (-1, -1) to (1, 1)
            self.move_direction = (random.randint(-1, 1), random.randint(-1, 1))
            
        # Move the enemy
        self.x += self.move_direction[0]
        self.y += self.move_direction[1]
        
        # Keep enemy on screen (assuming 800x600 screen size)
        self.x = max(0, min(self.x, 800 - self.width))
        self.y = max(0, min(self.y, 600 - self.height))
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the enemy on the screen.
        
        Args:
            screen: The Pygame surface to draw on
        """
        # Draw enemy as a rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw enemy name
        font = pygame.font.SysFont('Arial', 14)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.x + self.width // 2 - name_text.get_width() // 2, self.y - 15))
        
        # Draw health bar
        health_pct = self.health / self._max_health
        bar_width = self.width
        health_width = bar_width * health_pct
        
        # Health bar background (red)
        pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y - 5, bar_width, 5))
        # Health bar foreground (green)
        pygame.draw.rect(screen, (0, 255, 0), (self.x, self.y - 5, health_width, 5))

class Slime(Enemy):
    """
    A basic enemy with low stats.
    """
    
    def __init__(self, x: int, y: int):
        """
        Initialize a new Slime enemy.
        
        Args:
            x: The slime's x position
            y: The slime's y position
        """
        super().__init__("Slime", health=15, attack=3, defense=1, x=x, y=y)
        self.color = (0, 255, 255)  # Cyan
        
    def attack(self, target: 'Player') -> None:
        """
        Slimes have a chance to deal less damage.
        This demonstrates polymorphism by overriding the attack method.
        
        Args:
            target: The target to attack
        """
        if random.random() < 0.3:  # 30% chance of a weaker attack
            damage = max(1, self.attack_power // 2)
            print(f"{self.name} weakly attacks {target.name} for {damage} damage!")
            target.take_damage(damage)
        else:
            super().attack(target)

class Goblin(Enemy):
    """
    A medium-difficulty enemy with balanced stats.
    """
    
    def __init__(self, x: int, y: int):
        """
        Initialize a new Goblin enemy.
        
        Args:
            x: The goblin's x position
            y: The goblin's y position
        """
        super().__init__("Goblin", health=25, attack=6, defense=2, x=x, y=y)
        self.color = (0, 100, 0)  # Dark green
        
    def attack(self, target: 'Player') -> None:
        """
        Goblins have a chance to attack twice.
        
        Args:
            target: The target to attack
        """
        super().attack(target)
        
        # 20% chance to attack twice
        if random.random() < 0.2:
            print(f"{self.name} attacks a second time!")
            damage = max(1, self.attack_power // 2)  # Second attack is weaker
            print(f"{self.name} attacks {target.name} for {damage} damage!")
            target.take_damage(damage)

class Dragon(Enemy):
    """
    A powerful enemy with high stats.
    """
    
    def __init__(self, x: int, y: int):
        """
        Initialize a new Dragon enemy.
        
        Args:
            x: The dragon's x position
            y: The dragon's y position
        """
        super().__init__("Dragon", health=100, attack=15, defense=8, x=x, y=y)
        self.color = (255, 165, 0)  # Orange
        self.width = 60  # Dragons are larger
        self.height = 60
        self.fire_breath_cooldown = 0
        
    def update(self) -> None:
        """Update the dragon's state each frame."""
        super().update()
        
        # Reduce fire breath cooldown
        if self.fire_breath_cooldown > 0:
            self.fire_breath_cooldown -= 1
        
    def attack(self, target: 'Player') -> None:
        """
        Dragons can use a powerful fire breath attack.
        
        Args:
            target: The target to attack
        """
        # Check if fire breath is available
        if self.fire_breath_cooldown <= 0 and random.random() < 0.3:  # 30% chance when available
            # Fire breath attack
            damage = self.attack_power * 2
            print(f"{self.name} uses FIRE BREATH on {target.name} for {damage} damage!")
            target.take_damage(damage)
            self.fire_breath_cooldown = 5  # Set cooldown
        else:
            # Regular attack
            super().attack(target)

class EnemyFactory:
    """
    A factory class for creating enemies.
    This demonstrates the Factory design pattern.
    """
    
    @staticmethod
    def create_slime(x: int, y: int) -> Slime:
        """Create a slime enemy."""
        return Slime(x, y)
        
    @staticmethod
    def create_goblin(x: int, y: int) -> Goblin:
        """Create a goblin enemy."""
        return Goblin(x, y)
        
    @staticmethod
    def create_dragon(x: int, y: int) -> Dragon:
        """Create a dragon enemy."""
        return Dragon(x, y)
        
    @staticmethod
    def create_random_enemy(x: int, y: int, difficulty: int = 1) -> Enemy:
        """
        Create a random enemy with difficulty scaling.
        
        Args:
            x: The enemy's x position
            y: The enemy's y position
            difficulty: The difficulty level (1-5)
            
        Returns:
            A randomly selected enemy
        """
        if difficulty <= 2:
            # Lower difficulties primarily spawn slimes
            enemy_type = random.choices(
                ["slime", "goblin", "dragon"],
                weights=[0.7, 0.25, 0.05],
                k=1
            )[0]
        elif difficulty <= 4:
            # Medium difficulties spawn more goblins
            enemy_type = random.choices(
                ["slime", "goblin", "dragon"],
                weights=[0.3, 0.6, 0.1],
                k=1
            )[0]
        else:
            # Higher difficulties spawn more dragons
            enemy_type = random.choices(
                ["slime", "goblin", "dragon"],
                weights=[0.1, 0.5, 0.4],
                k=1
            )[0]
            
        if enemy_type == "slime":
            return EnemyFactory.create_slime(x, y)
        elif enemy_type == "goblin":
            return EnemyFactory.create_goblin(x, y)
        else:
            return EnemyFactory.create_dragon(x, y) 