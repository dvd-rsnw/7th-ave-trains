import time
from typing import Dict, Any, Optional


class TextRenderer:
    """Handles rendering and scrolling text on the LED matrix."""
    
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
        
        # State for scrolling
        self.scroll_positions: Dict[str, int] = {}
        self.scroll_timestamps: Dict[str, float] = {}
    
    def get_text_width(self, text: str) -> int:
        """Get the pixel width of text using the current font.
        
        Args:
            text: The text to measure
            
        Returns:
            The width in pixels
        """
        if self.is_mock:
            return len(text) * 6  # Approximate for mock
        return sum(self.font.CharacterWidth(ord(c)) for c in text)
    
    def draw_scrolling_text(
        self, 
        text: str, 
        x: int, 
        y: int, 
        max_width: int, 
        scroll_key: str, 
        scroll_speed: int = 2
    ) -> None:
        """Draw text with scrolling if it exceeds max_width.
        
        Args:
            text: The text to display
            x: The x-coordinate to start drawing
            y: The y-coordinate to draw at
            max_width: Maximum width in pixels
            scroll_key: Unique identifier for this text (for scroll state)
            scroll_speed: Speed of scrolling in pixels per second
        """
        if self.is_mock:
            return
            
        text_width = self.get_text_width(text)
        
        if text_width <= max_width:
            # Text fits, no scrolling needed
            self.graphics.DrawText(
                self.matrix, self.font, x, y, self.text_color, text
            )
            self.scroll_positions[scroll_key] = 0  # Reset scroll position
            self.scroll_timestamps[scroll_key] = time.time()  # Reset timestamp
        else:
            # Calculate scroll position using individual timestamp
            current_time = time.time()
            if scroll_key not in self.scroll_timestamps:
                self.scroll_timestamps[scroll_key] = current_time
            
            time_diff = current_time - self.scroll_timestamps[scroll_key]
            scroll_amount = int(scroll_speed * time_diff)
            
            # Update scroll position
            if scroll_key not in self.scroll_positions:
                self.scroll_positions[scroll_key] = 0
            self.scroll_positions[scroll_key] = (
                (self.scroll_positions[scroll_key] + scroll_amount) % text_width
            )
            
            # Update timestamp
            self.scroll_timestamps[scroll_key] = current_time
            
            # Draw scrolled text
            offset_x = x - self.scroll_positions[scroll_key]
            self.graphics.DrawText(
                self.matrix, self.font, offset_x, y, self.text_color, text
            )
            # Draw text again if it's scrolled partially off
            if offset_x + text_width < x + max_width:
                self.graphics.DrawText(
                    self.matrix, self.font, 
                    offset_x + text_width, y, self.text_color, text
                ) 