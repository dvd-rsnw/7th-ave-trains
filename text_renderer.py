import time
from typing import Dict, Any, Optional


class TextRenderer:
    """Handles text rendering on the LED matrix display."""
    
    def __init__(self, matrix: Any, font: Any, graphics: Any, is_mock: bool = False):
        """Initialize the text renderer.
        
        Args:
            matrix: The LED matrix instance
            font: The font to use for rendering text
            graphics: The graphics library
            is_mock: Whether to use mock mode
        """
        self.matrix = matrix
        self.font = font
        self.graphics = graphics
        self.is_mock = is_mock
        self.text_color = None if is_mock else graphics.Color(255, 255, 255)
    
    def get_text_width(self, text: str) -> int:
        """Get the pixel width of text using the current font.
        
        Args:
            text: The text to measure
            
        Returns:
            The width in pixels
        """
        if self.is_mock:
            return len(text) * 5  # Approximate for mock
        return sum(self.font.CharacterWidth(ord(c)) for c in text)
    
    def draw_text(self, text: str, x: int, y: int) -> None:
        """Draw text at the specified position.
        
        Args:
            text: Text to draw
            x: Starting x-coordinate
            y: Y-coordinate (text baseline)
        """
        if self.is_mock:
            return
            
        self.graphics.DrawText(
            self.matrix, self.font, x, y,
            self.text_color, text
        )
        
    def draw_text_with_fixed_suffix(self, variable_text: str, fixed_text: str, end_x: int, y: int) -> None:
        """Draw text where the fixed suffix stays at a fixed position and variable text aligns to the left of it.
        
        Args:
            variable_text: Variable part of the text (e.g., the number)
            fixed_text: Fixed part of the text (e.g., "mins")
            end_x: The x-coordinate where the fixed_text should end
            y: Y-coordinate (text baseline)
        """
        if self.is_mock:
            return
            
        # Calculate the width of the fixed text
        fixed_width = self.get_text_width(fixed_text)
        
        # Position the fixed text so its end aligns with end_x
        fixed_x = end_x - fixed_width
        
        # Draw the fixed text at the calculated position
        self.graphics.DrawText(
            self.matrix, self.font, fixed_x, y,
            self.text_color, fixed_text
        )
        
        # Calculate and draw the variable text to the left of the fixed text
        variable_x = fixed_x - self.get_text_width(variable_text)
        self.graphics.DrawText(
            self.matrix, self.font, variable_x, y,
            self.text_color, variable_text
        )