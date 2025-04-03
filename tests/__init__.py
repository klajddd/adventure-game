"""
Test package for the adventure game.
Provides common test utilities and base test cases.
"""

import unittest
import pygame
from typing import Tuple

class GameTestCase(unittest.TestCase):
    """
    Base test case class for all game tests.
    Provides common setup and teardown functionality.
    """
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        pygame.init()
        self.screen_size: Tuple[int, int] = (800, 600)
        self.screen = pygame.Surface(self.screen_size)
        
    def tearDown(self):
        """Clean up after each test method."""
        pygame.quit()
        
    def create_key_event(self, key: int, char: str = '') -> pygame.event.Event:
        """
        Create a keyboard event for testing.
        
        Args:
            key: The pygame key code
            char: The unicode character (for printable keys)
            
        Returns:
            A pygame keyboard event
        """
        return pygame.event.Event(pygame.KEYDOWN, {
            'unicode': char,
            'key': key
        })
        
    def simulate_key_press(self, key: int, char: str = '') -> pygame.event.Event:
        """
        Simulate a key press and return the event.
        
        Args:
            key: The pygame key code
            char: The unicode character (for printable keys)
            
        Returns:
            The created event
        """
        event = self.create_key_event(key, char)
        pygame.event.post(event)
        return event
        
    def assert_position(self, entity: any, x: int, y: int, msg: str = None):
        """
        Assert that an entity is at the specified position.
        
        Args:
            entity: The game entity to check
            x: Expected x position
            y: Expected y position
            msg: Optional assertion message
        """
        self.assertEqual(entity.x, x, msg or f"Expected x position {x}, got {entity.x}")
        self.assertEqual(entity.y, y, msg or f"Expected y position {y}, got {entity.y}")
        
    def assert_dimensions(self, entity: any, width: int, height: int, msg: str = None):
        """
        Assert that an entity has the specified dimensions.
        
        Args:
            entity: The game entity to check
            width: Expected width
            height: Expected height
            msg: Optional assertion message
        """
        self.assertEqual(entity.width, width, msg or f"Expected width {width}, got {entity.width}")
        self.assertEqual(entity.height, height, msg or f"Expected height {height}, got {entity.height}")
        
    def assert_sprite_properties(self, sprite: pygame.Surface, 
                               expected_width: int, 
                               expected_height: int,
                               has_alpha: bool = True):
        """
        Assert that a sprite has the expected properties.
        
        Args:
            sprite: The pygame surface to check
            expected_width: Expected sprite width
            expected_height: Expected sprite height
            has_alpha: Whether the sprite should have an alpha channel
        """
        self.assertEqual(sprite.get_width(), expected_width)
        self.assertEqual(sprite.get_height(), expected_height)
        if has_alpha:
            self.assertEqual(sprite.get_flags() & pygame.SRCALPHA, pygame.SRCALPHA) 