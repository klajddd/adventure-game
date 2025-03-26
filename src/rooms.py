"""
Rooms module containing classes for different game locations.
"""

import pygame
import random
from typing import List, Optional, Dict, Any, Tuple

from src.items import Item, ItemFactory
from src.enemies import Enemy, EnemyFactory

class Room:
    """
    Represents a single room or area in the game world.
    Rooms can contain items and enemies, and connect to other rooms.
    """
    
    def __init__(self, name: str, description: str, background_color: Tuple[int, int, int] = (50, 50, 100)):
        """
        Initialize a new Room.
        
        Args:
            name: The room's name
            description: The room's description
            background_color: RGB tuple for the room's background color
        """
        self.name = name
        self.description = description
        self.background_color = background_color
        self.items: List[Item] = []
        self.enemies: List[Enemy] = []
        
        # Connections to adjacent rooms
        self.north: Optional[Room] = None
        self.south: Optional[Room] = None
        self.east: Optional[Room] = None
        self.west: Optional[Room] = None
        
        # Visual elements
        self.features: List[Dict[str, Any]] = []  # Decorative elements
        
    def add_item(self, item: Item) -> None:
        """Add an item to the room."""
        self.items.append(item)
        
    def add_enemy(self, enemy: Enemy) -> None:
        """Add an enemy to the room."""
        self.enemies.append(enemy)
        
    def connect_rooms(self, direction: str, room: 'Room') -> None:
        """
        Connect this room to another room in the specified direction.
        
        Args:
            direction: The direction ('north', 'south', 'east', or 'west')
            room: The room to connect to
        """
        if direction.lower() == 'north':
            self.north = room
            room.south = self
        elif direction.lower() == 'south':
            self.south = room
            room.north = self
        elif direction.lower() == 'east':
            self.east = room
            room.west = self
        elif direction.lower() == 'west':
            self.west = room
            room.east = self
        else:
            raise ValueError(f"Invalid direction: {direction}")
            
    def add_feature(self, feature_type: str, x: int, y: int, width: int, height: int, 
                   color: Tuple[int, int, int]) -> None:
        """
        Add a visual feature to the room.
        
        Args:
            feature_type: The type of feature ('rect', 'circle', etc.)
            x, y: The position of the feature
            width, height: The dimensions of the feature
            color: The RGB color tuple
        """
        self.features.append({
            'type': feature_type,
            'x': x,
            'y': y,
            'width': width,
            'height': height,
            'color': color
        })
        
    def update(self) -> None:
        """Update all entities in the room."""
        for enemy in self.enemies:
            enemy.update()
            
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the room and all its contents.
        
        Args:
            screen: The Pygame surface to draw on
        """
        # Draw background
        screen.fill(self.background_color)
        
        # Draw features
        for feature in self.features:
            if feature['type'] == 'rect':
                pygame.draw.rect(
                    screen,
                    feature['color'],
                    (feature['x'], feature['y'], feature['width'], feature['height'])
                )
            elif feature['type'] == 'circle':
                pygame.draw.circle(
                    screen,
                    feature['color'],
                    (feature['x'], feature['y']),
                    feature['width']  # Using width as radius
                )
                
        # Draw room name
        font = pygame.font.SysFont('Arial', 24)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (20, 20))
        
        # Draw items
        for item in self.items:
            item.draw(screen)
            
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
            
        # Draw room connections/exits
        exit_width = 40
        exit_height = 10
        
        if self.north:
            pygame.draw.rect(screen, (0, 255, 0), (400 - exit_width//2, 0, exit_width, exit_height))
        if self.south:
            pygame.draw.rect(screen, (0, 255, 0), (400 - exit_width//2, 590, exit_width, exit_height))
        if self.east:
            pygame.draw.rect(screen, (0, 255, 0), (790, 300 - exit_height//2, exit_height, exit_width))
        if self.west:
            pygame.draw.rect(screen, (0, 255, 0), (0, 300 - exit_height//2, exit_height, exit_width))

class RoomFactory:
    """
    Factory class for creating rooms with different layouts and difficulties.
    """
    
    def __init__(self):
        """Initialize the RoomFactory."""
        self.item_factory = ItemFactory()
        self.enemy_factory = EnemyFactory()
        self.room_types = {
            'forest': (34, 139, 34),  # Forest green
            'cave': (50, 50, 70),     # Dark blue-gray
            'castle': (110, 90, 90),  # Brown
            'dungeon': (60, 30, 30),  # Dark red-brown
            'village': (100, 140, 100)  # Light green
        }
        
    def create_room(self, name: str, description: str, room_type: str, 
                   num_items: int = 0, num_enemies: int = 0, 
                   difficulty: int = 1) -> Room:
        """
        Create a room with the specified parameters.
        
        Args:
            name: The room's name
            description: The room's description
            room_type: The type of room (affects background color)
            num_items: Number of random items to place
            num_enemies: Number of random enemies to place
            difficulty: Difficulty level (1-5)
            
        Returns:
            A new Room instance
        """
        # Create the room with the appropriate background color
        background_color = self.room_types.get(room_type.lower(), (50, 50, 100))
        room = Room(name, description, background_color)
        
        # Add decorative features based on room type
        self._add_features_by_type(room, room_type)
        
        # Add random items
        for _ in range(num_items):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            item = self.item_factory.create_random_item(x, y)
            room.add_item(item)
            
        # Add random enemies
        for _ in range(num_enemies):
            x = random.randint(50, 750)
            y = random.randint(50, 550)
            enemy = self.enemy_factory.create_random_enemy(x, y, difficulty)
            room.add_enemy(enemy)
            
        return room
        
    def _add_features_by_type(self, room: Room, room_type: str) -> None:
        """
        Add visual features based on the room type.
        
        Args:
            room: The room to add features to
            room_type: The type of room
        """
        if room_type.lower() == 'forest':
            # Add trees
            for _ in range(5):
                x = random.randint(50, 750)
                y = random.randint(50, 550)
                room.add_feature('rect', x, y, 20, 50, (0, 100, 0))  # Tree trunk
                room.add_feature('circle', x + 10, y - 20, 30, 30, (0, 200, 0))  # Tree top
                
        elif room_type.lower() == 'cave':
            # Add stalactites and rocks
            for _ in range(3):
                x = random.randint(50, 750)
                room.add_feature('rect', x, 0, 10, random.randint(20, 50), (100, 100, 100))
                
            for _ in range(4):
                x = random.randint(50, 750)
                y = random.randint(300, 550)
                room.add_feature('circle', x, y, random.randint(10, 30), 10, (80, 80, 80))
                
        elif room_type.lower() == 'castle' or room_type.lower() == 'dungeon':
            # Add walls and columns
            for x in range(100, 701, 200):
                room.add_feature('rect', x, 100, 20, 400, (60, 60, 60))
                
            # Add torches
            for x in range(150, 751, 200):
                room.add_feature('rect', x, 150, 5, 20, (90, 90, 90))  # Torch holder
                room.add_feature('circle', x + 2, 140, 8, 8, (255, 165, 0))  # Flame
                
        elif room_type.lower() == 'village':
            # Add houses
            for _ in range(3):
                x = random.randint(100, 600)
                y = random.randint(100, 400)
                # House body
                room.add_feature('rect', x, y, 80, 60, (200, 150, 100))
                # Roof
                points = [(x - 10, y), (x + 40, y - 30), (x + 90, y)]
                room.add_feature('rect', x - 10, y - 30, 100, 30, (150, 75, 0))
                # Door
                room.add_feature('rect', x + 30, y + 30, 20, 30, (100, 50, 0))
                # Window
                room.add_feature('rect', x + 10, y + 15, 15, 15, (200, 200, 255))
                
    def create_starting_room(self) -> Room:
        """
        Create the first room of the game.
        
        Returns:
            A new Room instance for the starting area
        """
        room = self.create_room(
            "Village Square", 
            "The central square of a small village. A good place to start your adventure.",
            "village",
            num_items=2,
            num_enemies=0
        )
        
        # Add specific items to help the player get started
        room.add_item(self.item_factory.create_healing_potion(200, 300))
        room.add_item(self.item_factory.create_weapon(400, 400, 1))
        
        return room
        
    def create_dungeon(self, size: int = 3, difficulty: int = 1) -> Room:
        """
        Create a dungeon with multiple connected rooms.
        
        Args:
            size: The size of the dungeon (number of rooms per side)
            difficulty: The starting difficulty level
            
        Returns:
            The starting (entrance) room of the dungeon
        """
        # Create a grid of rooms
        rooms = [[None for _ in range(size)] for _ in range(size)]
        
        # Room types for variety
        room_types = ['cave', 'dungeon', 'castle']
        
        # Create each room
        for i in range(size):
            for j in range(size):
                room_type = random.choice(room_types)
                room_difficulty = difficulty + i  # Difficulty increases as you go deeper
                
                # Customize number of items and enemies based on position
                num_items = random.randint(0, 2)
                num_enemies = random.randint(0, min(3, room_difficulty))
                
                # Create the room
                room_name = f"Dungeon Room {i+1}-{j+1}"
                room_desc = f"A {room_type} room at level {room_difficulty} of the dungeon."
                rooms[i][j] = self.create_room(
                    room_name, room_desc, room_type,
                    num_items=num_items, 
                    num_enemies=num_enemies,
                    difficulty=room_difficulty
                )
        
        # Connect the rooms
        for i in range(size):
            for j in range(size):
                if i > 0:  # Connect to the room above
                    rooms[i][j].connect_rooms('north', rooms[i-1][j])
                if j > 0:  # Connect to the room to the left
                    rooms[i][j].connect_rooms('west', rooms[i][j-1])
        
        # Add boss to the furthest room
        boss_room = rooms[size-1][size-1]
        boss = self.enemy_factory.create_dragon(400, 300)
        boss_room.add_enemy(boss)
        
        # Add special treasure
        boss_room.add_item(self.item_factory.create_weapon(300, 300, 5))  # Legendary weapon
        boss_room.add_item(self.item_factory.create_armor(500, 300, 5))  # Legendary armor
        
        # Return the entrance room
        return rooms[0][0] 