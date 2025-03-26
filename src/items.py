"""
Items module containing various item classes that the player can interact with.
This module demonstrates inheritance and polymorphism through different item types.
"""

import pygame
from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class Entity(ABC):
    """
    Abstract base class for all game entities that have a position and can be drawn.
    """
    
    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        """
        Initialize a new Entity.
        
        Args:
            name: The entity's name
            x: The entity's x position
            y: The entity's y position
            width: The entity's width
            height: The entity's height
        """
        self.name = name
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        
    @abstractmethod
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the entity on the screen.
        
        Args:
            screen: The Pygame surface to draw on
        """
        pass

class Item(Entity):
    """
    Base class for all items in the game.
    """
    
    def __init__(self, name: str, description: str, x: int, y: int):
        """
        Initialize a new Item.
        
        Args:
            name: The item's name
            description: The item's description
            x: The item's x position
            y: The item's y position
        """
        super().__init__(name, x, y, 30, 30)
        self.description = description
        self.consumable = True
        self.color = (255, 255, 0)  # Default color: yellow
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the item on the screen.
        
        Args:
            screen: The Pygame surface to draw on
        """
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        
        # Draw a small label
        font = pygame.font.SysFont('Arial', 12)
        name_text = font.render(self.name[0], True, (0, 0, 0))
        screen.blit(name_text, (self.x + self.width // 2 - name_text.get_width() // 2, 
                                self.y + self.height // 2 - name_text.get_height() // 2))
        
    def use(self, player: 'Player') -> bool:
        """
        Use the item, affecting the player in some way.
        Returns True if the item was used successfully, False otherwise.
        
        This is where polymorphism occurs - different item types override this
        method to provide different behavior.
        
        Args:
            player: The player using the item
            
        Returns:
            bool: Whether the item was used successfully
        """
        print(f"{player.name} uses {self.name}: {self.description}")
        return True
    
    def __str__(self) -> str:
        """String representation of the item."""
        return f"{self.name}: {self.description}"

class HealingPotion(Item):
    """
    A potion that restores health to the player when used.
    This class demonstrates inheritance from the Item class and polymorphism by
    overriding the use method.
    """
    
    def __init__(self, healing_amount: int, x: int, y: int):
        """
        Initialize a new HealingPotion.
        
        Args:
            healing_amount: How much health the potion restores
            x: The potion's x position
            y: The potion's y position
        """
        super().__init__(
            name=f"Healing Potion ({healing_amount}hp)", 
            description=f"Restores {healing_amount} health points when consumed.", 
            x=x, 
            y=y
        )
        self.healing_amount = healing_amount
        self.color = (255, 0, 255)  # Magenta
        
    def use(self, player: 'Player') -> bool:
        """
        Use the potion to heal the player.
        
        Args:
            player: The player using the potion
            
        Returns:
            bool: True if the player was healed, False otherwise
        """
        if player.health < player._max_health:
            super().use(player)
            player.heal(self.healing_amount)
            return True
        else:
            print(f"{player.name} is already at full health!")
            return False

class Weapon(Item):
    """
    A weapon that increases the player's attack power when equipped.
    """
    
    def __init__(self, name: str, attack_bonus: int, x: int, y: int):
        """
        Initialize a new Weapon.
        
        Args:
            name: The weapon's name
            attack_bonus: How much the weapon increases attack power
            x: The weapon's x position
            y: The weapon's y position
        """
        super().__init__(
            name=name, 
            description=f"Increases attack power by {attack_bonus}.", 
            x=x, 
            y=y
        )
        self.attack_bonus = attack_bonus
        self.consumable = False
        self.color = (150, 75, 0)  # Brown
        
    def use(self, player: 'Player') -> bool:
        """
        Equip the weapon, increasing the player's attack power.
        
        Args:
            player: The player equipping the weapon
            
        Returns:
            bool: True if the weapon was equipped successfully
        """
        super().use(player)
        player.attack_power += self.attack_bonus
        print(f"{player.name}'s attack power is now {player.attack_power}!")
        return True

class Armor(Item):
    """
    Armor that increases the player's defense when equipped.
    """
    
    def __init__(self, name: str, defense_bonus: int, x: int, y: int):
        """
        Initialize a new Armor.
        
        Args:
            name: The armor's name
            defense_bonus: How much the armor increases defense
            x: The armor's x position
            y: The armor's y position
        """
        super().__init__(
            name=name, 
            description=f"Increases defense by {defense_bonus}.", 
            x=x, 
            y=y
        )
        self.defense_bonus = defense_bonus
        self.consumable = False
        self.color = (192, 192, 192)  # Silver
        
    def use(self, player: 'Player') -> bool:
        """
        Equip the armor, increasing the player's defense.
        
        Args:
            player: The player equipping the armor
            
        Returns:
            bool: True if the armor was equipped successfully
        """
        super().use(player)
        player.defense += self.defense_bonus
        print(f"{player.name}'s defense is now {player.defense}!")
        return True

class Key(Item):
    """
    A key that can unlock a specific door or chest.
    """
    
    def __init__(self, target_id: str, x: int, y: int):
        """
        Initialize a new Key.
        
        Args:
            target_id: The ID of the door or chest this key unlocks
            x: The key's x position
            y: The key's y position
        """
        super().__init__(
            name=f"Key to {target_id}", 
            description=f"Unlocks the {target_id}.", 
            x=x, 
            y=y
        )
        self.target_id = target_id
        self.consumable = False
        self.color = (255, 215, 0)  # Gold
        
    def use(self, player: 'Player') -> bool:
        """
        The key can't be directly used - it's used automatically when 
        interacting with the corresponding door or chest.
        
        Args:
            player: The player using the key
            
        Returns:
            bool: Always False as the key can't be directly used
        """
        print(f"You need to find the {self.target_id} to use this key.")
        return False

class ItemFactory:
    """
    A factory class for creating items.
    This demonstrates the Factory design pattern.
    """
    
    @staticmethod
    def create_healing_potion(x: int, y: int, amount: int = 20) -> HealingPotion:
        """Create a healing potion."""
        return HealingPotion(amount, x, y)
        
    @staticmethod
    def create_weapon(x: int, y: int, tier: int = 1) -> Weapon:
        """Create a weapon based on tier."""
        weapons = {
            1: ("Wooden Sword", 5),
            2: ("Iron Sword", 10),
            3: ("Steel Sword", 15),
            4: ("Mythril Blade", 20),
            5: ("Legendary Sword", 30)
        }
        name, bonus = weapons.get(tier, weapons[1])
        return Weapon(name, bonus, x, y)
        
    @staticmethod
    def create_armor(x: int, y: int, tier: int = 1) -> Armor:
        """Create armor based on tier."""
        armors = {
            1: ("Leather Armor", 2),
            2: ("Chain Mail", 5),
            3: ("Plate Armor", 8),
            4: ("Mythril Armor", 12),
            5: ("Legendary Armor", 20)
        }
        name, bonus = armors.get(tier, armors[1])
        return Armor(name, bonus, x, y)
        
    @staticmethod
    def create_key(x: int, y: int, target: str) -> Key:
        """Create a key for a specific target."""
        return Key(target, x, y)
        
    @staticmethod
    def create_random_item(x: int, y: int) -> Item:
        """Create a random item."""
        import random
        item_type = random.choice(["potion", "weapon", "armor"])
        tier = random.randint(1, 3)
        
        if item_type == "potion":
            return ItemFactory.create_healing_potion(x, y, amount=tier * 10)
        elif item_type == "weapon":
            return ItemFactory.create_weapon(x, y, tier=tier)
        else:
            return ItemFactory.create_armor(x, y, tier=tier) 