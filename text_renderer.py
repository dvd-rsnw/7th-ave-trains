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