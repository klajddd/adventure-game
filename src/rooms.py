"""
Rooms module containing classes for different game locations.
"""

import pygame
from typing import Optional, Tuple

class Room:
    """
    Represents a single room or area in the game world.
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
        
        # Connections to adjacent rooms
        self.north: Optional[Room] = None
        self.south: Optional[Room] = None
        self.east: Optional[Room] = None
        self.west: Optional[Room] = None
            
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the room and all its contents.
        
        Args:
            screen: The Pygame surface to draw on
        """
        # Draw background
        screen.fill(self.background_color)

class RoomFactory:
    """
    Factory class for creating rooms.
    """
    
    def create_starting_room(self) -> Room:
        """
        Create the first room of the game.
        
        Returns:
            A new Room instance for the starting area
        """
        return Room(
            "Starting Room", 
            "An empty room where your adventure begins.",
            (50, 50, 100)  # Dark blue background
        ) 