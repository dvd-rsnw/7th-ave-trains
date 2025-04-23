import time
from typing import Dict, Any, Optional
from contextlib import contextmanager
from typing import Protocol, TypeVar

# Define protocol for matrix interface
class RGBMatrixProtocol(Protocol):
    def SetPixel(self, x: int, y: int, red: int, green: int, blue: int) -> None: ...

# Define protocol for font interface
class FontProtocol(Protocol):
    def CharacterWidth(self, char: int) -> int: ...
    def Height(self) -> int: ...

# Define protocol for graphics interface
class GraphicsProtocol(Protocol):
    def Color(self, red: int, green: int, blue: int) -> int: ...
    def DrawText(self, matrix: RGBMatrixProtocol, font: FontProtocol, x: int, y: int, color: int, text: str) -> None: ...

T = TypeVar('T')

class TextRenderer:
    """Handles text rendering on the LED matrix display."""
    
    # Class constants
    DEFAULT_COLOR = (255, 255, 255)
    MOCK_CHAR_WIDTH = 5  # Approximate width for mock mode
    
    def __init__(
        self, 
        matrix: RGBMatrixProtocol, 
        font: FontProtocol, 
        graphics: GraphicsProtocol, 
        is_mock: bool = False
    ) -> None:
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
        self._text_color = None if is_mock else self.graphics.Color(*self.DEFAULT_COLOR)
        self._char_width_cache: Dict[str, int] = {}
        
    @property
    def text_color(self) -> Optional[int]:
        """Get the current text color."""
        return self._text_color
    
    @contextmanager
    def _mock_guard(self):
        """Context manager to handle mock mode checks."""
        if not self.is_mock:
            yield
    
    def _get_char_width(self, char: str) -> int:
        """Get cached character width.
        
        Args:
            char: Single character to measure
            
        Returns:
            Width in pixels
        """
        if char not in self._char_width_cache:
            self._char_width_cache[char] = (
                self.MOCK_CHAR_WIDTH if self.is_mock 
                else self.font.CharacterWidth(ord(char))
            )
        return self._char_width_cache[char]
    
    def get_text_width(self, text: str) -> int:
        """Get the pixel width of text using the current font.
        
        Args:
            text: The text to measure
            
        Returns:
            The width in pixels
        """
        return sum(self._get_char_width(c) for c in text)
    
    def draw_text(self, text: str, x: int, y: int) -> None:
        """Draw text at the specified position.
        
        Args:
            text: Text to draw
            x: Starting x-coordinate
            y: Y-coordinate (text baseline)
        """
        with self._mock_guard():
            self.graphics.DrawText(
                self.matrix, self.font, x, y,
                self.text_color, text
            )
        
    def draw_text_with_fixed_suffix(
        self, 
        variable_text: str, 
        fixed_text: str, 
        end_x: int, 
        y: int
    ) -> None:
        """Draw text where the fixed suffix stays at a fixed position and variable text aligns to the left of it.
        
        Args:
            variable_text: Variable part of the text (e.g., the number)
            fixed_text: Fixed part of the text (e.g., "mins")
            end_x: The x-coordinate where the fixed_text should end
            y: Y-coordinate (text baseline)
        """
        with self._mock_guard():
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