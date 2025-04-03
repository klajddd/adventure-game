"""
Unit tests for the NPC class.
"""

from . import GameTestCase
import pygame
from src.npc import NPC

class TestNPC(GameTestCase):
    """Test cases for the NPC class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        super().setUp()  # Call the parent class's setUp
        # Create a test NPC
        self.npc = NPC("TestNPC", 100, 100)
        
    def test_npc_initialization(self):
        """Test that NPC is initialized with correct attributes."""
        self.assertEqual(self.npc.name, "TestNPC")
        self.assert_position(self.npc, 100, 100)
        self.assert_dimensions(self.npc, 32, 48)
        self.assertFalse(self.npc.dialogue_active)
        self.assertEqual(self.npc.current_message, "")
        self.assertEqual(len(self.npc.messages), 0)
        
    def test_sprite_creation(self):
        """Test that the sprite is created with correct dimensions."""
        sprite = self.npc._create_pixel_person()
        self.assert_sprite_properties(sprite, self.npc.width, self.npc.height)
        
    def test_dialogue_activation(self):
        """Test starting and ending dialogue."""
        # Test starting dialogue
        self.npc.start_dialogue()
        self.assertTrue(self.npc.dialogue_active)
        self.assertEqual(len(self.npc.messages), 1)
        self.assertTrue(self.npc.messages[0].startswith(f"{self.npc.name}: Hello!"))
        
        # Test ending dialogue
        self.npc.end_dialogue()
        self.assertFalse(self.npc.dialogue_active)
        self.assertEqual(self.npc.current_message, "")
        
    def test_message_responses(self):
        """Test NPC responses to different message types."""
        test_messages = {
            "hello": "Hello! Nice to meet you!",
            "how are you": "I'm doing well, thanks for asking!",
            "goodbye": "Goodbye! Take care!",
            "what's your name": "My name is TestNPC, as you can see above my head!",
            "I need help": "I'm here to help you learn about Object-Oriented Programming!",
            "tell me about classes": "Yes! I'm an object created from the NPC class, just like you're an object from the Player class!",
            "random message": "Interesting... Tell me more about that!"
        }
        
        self.npc.dialogue_active = True
        
        for message, expected_response in test_messages.items():
            self.npc.messages = []  # Clear previous messages
            self.npc._respond_to_message(message)
            self.assertEqual(self.npc.messages[-1], f"{self.npc.name}: {expected_response}")
            
    def test_message_input_handling(self):
        """Test handling of keyboard input for messages."""
        self.npc.dialogue_active = True
        
        # Test adding characters to message
        for char in "Hello":
            self.npc.handle_input(self.create_key_event(ord(char), char))
        self.assertEqual(self.npc.current_message, "Hello")
        
        # Test backspace
        self.npc.handle_input(self.create_key_event(pygame.K_BACKSPACE))
        self.assertEqual(self.npc.current_message, "Hell")
        
        # Test sending message with enter
        self.npc.handle_input(self.create_key_event(pygame.K_RETURN))
        self.assertEqual(self.npc.current_message, "")  # Message should be cleared
        self.assertEqual(len(self.npc.messages), 2)  # User message + NPC response
        self.assertTrue(self.npc.messages[0].startswith("You: Hell"))
        
    def test_inactive_dialogue_input(self):
        """Test that input is ignored when dialogue is inactive."""
        self.npc.dialogue_active = False
        
        # Try to add a message
        self.npc.handle_input(self.create_key_event(ord('a'), 'a'))
        self.assertEqual(self.npc.current_message, "")
        self.assertEqual(len(self.npc.messages), 0)

if __name__ == '__main__':
    unittest.main() 