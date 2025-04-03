"""
NPC module for non-player characters that can engage in dialogue.
"""

import pygame
from typing import List, Optional

class NPC:
    """A non-player character that can engage in dialogue with the player."""
    
    def __init__(self, name: str, x: int, y: int):
        """
        Initialize a new NPC.
        
        Args:
            name: The NPC's name
            x: The NPC's x position
            y: The NPC's y position
        """
        self.name = name
        self.x = x
        self.y = y
        self.width = 32  # Same size as player
        self.height = 48
        self.sprite = self._create_pixel_person()
        self.dialogue_active = False
        self.current_message = ""
        self.messages = []  # Store conversation history
        
    def _create_pixel_person(self) -> pygame.Surface:
        """Create a pixelated person sprite with different colors than the player."""
        sprite = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Colors - using different colors than the player
        skin_color = (255, 218, 185)  # Peach
        shirt_color = (220, 20, 60)   # Crimson red
        pants_color = (25, 25, 112)   # Dark blue
        
        # Head (8x8 pixels at the top)
        pygame.draw.rect(sprite, skin_color, (12, 0, 8, 8))
        
        # Body (12x16 pixels in the middle)
        pygame.draw.rect(sprite, shirt_color, (10, 8, 12, 16))
        
        # Arms (4x12 pixels on each side of body)
        pygame.draw.rect(sprite, shirt_color, (6, 8, 4, 12))   # Left arm
        pygame.draw.rect(sprite, shirt_color, (22, 8, 4, 12))  # Right arm
        
        # Legs (6x16 pixels each)
        pygame.draw.rect(sprite, pants_color, (10, 24, 6, 20))  # Left leg
        pygame.draw.rect(sprite, pants_color, (16, 24, 6, 20))  # Right leg
        
        return sprite
        
    def draw(self, screen: pygame.Surface) -> None:
        """
        Draw the NPC on the screen.
        
        Args:
            screen: The Pygame surface to draw on
        """
        # Draw the NPC sprite
        screen.blit(self.sprite, (self.x, self.y))
        
        # Draw NPC name above sprite
        font = pygame.font.SysFont('Arial', 18)
        name_text = font.render(self.name, True, (255, 255, 255))
        screen.blit(name_text, (self.x + self.width // 2 - name_text.get_width() // 2, self.y - 20))
        
        # If dialogue is active, draw the dialogue box
        if self.dialogue_active:
            self._draw_dialogue_box(screen)
            
    def _draw_dialogue_box(self, screen: pygame.Surface) -> None:
        """Draw the dialogue box with conversation history and input prompt."""
        # Create dialogue box background
        box_width = 600
        box_height = 200
        box_x = screen.get_width() // 2 - box_width // 2
        box_y = screen.get_height() - box_height - 20
        
        # Draw semi-transparent background
        dialogue_surface = pygame.Surface((box_width, box_height))
        dialogue_surface.set_alpha(220)
        dialogue_surface.fill((40, 40, 40))
        screen.blit(dialogue_surface, (box_x, box_y))
        
        # Draw border
        pygame.draw.rect(screen, (100, 100, 100), (box_x, box_y, box_width, box_height), 2)
        
        # Draw conversation history
        font = pygame.font.SysFont('Arial', 18)
        y_offset = 20
        for message in self.messages[-5:]:  # Show last 5 messages
            text = font.render(message, True, (255, 255, 255))
            screen.blit(text, (box_x + 20, box_y + y_offset))
            y_offset += 25
            
        # Draw input prompt
        prompt = f"> {self.current_message}_"
        prompt_text = font.render(prompt, True, (0, 255, 0))
        screen.blit(prompt_text, (box_x + 20, box_y + box_height - 30))
        
        # Draw instructions
        instructions = "Press ENTER to send, ESC to exit dialogue"
        inst_text = font.render(instructions, True, (200, 200, 200))
        screen.blit(inst_text, (box_x + box_width - inst_text.get_width() - 20, box_y + box_height - 30))
        
    def handle_input(self, event: pygame.event.Event) -> None:
        """Handle keyboard input for dialogue."""
        if not self.dialogue_active:
            return
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and self.current_message:
                # Add player's message to conversation
                self.messages.append(f"You: {self.current_message}")
                # Add NPC's response
                self._respond_to_message(self.current_message)
                self.current_message = ""
            elif event.key == pygame.K_BACKSPACE:
                self.current_message = self.current_message[:-1]
            elif event.unicode.isprintable():
                self.current_message += event.unicode
                
    def _respond_to_message(self, message: str) -> None:
        """Generate a response to the player's message."""
        message = message.lower()
        
        if "hello" in message or "hi" in message:
            self.messages.append(f"{self.name}: Hello! Nice to meet you!")
        elif "how are you" in message:
            self.messages.append(f"{self.name}: I'm doing well, thanks for asking!")
        elif "bye" in message or "goodbye" in message:
            self.messages.append(f"{self.name}: Goodbye! Take care!")
        elif "name" in message:
            self.messages.append(f"{self.name}: My name is {self.name}, as you can see above my head!")
        elif "help" in message:
            self.messages.append(f"{self.name}: I'm here to help you learn about Object-Oriented Programming!")
        elif "class" in message or "object" in message:
            self.messages.append(f"{self.name}: Yes! I'm an object created from the NPC class, just like you're an object from the Player class!")
        else:
            self.messages.append(f"{self.name}: Interesting... Tell me more about that!")
            
    def start_dialogue(self) -> None:
        """Start a dialogue session."""
        self.dialogue_active = True
        if not self.messages:
            self.messages.append(f"{self.name}: Hello! Press T to talk to me!")
            
    def end_dialogue(self) -> None:
        """End the dialogue session."""
        self.dialogue_active = False
        self.current_message = "" 