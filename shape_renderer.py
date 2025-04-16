from typing import Tuple, Any

class ShapeRenderer:
    """Renders shapes on the LED matrix display."""
    
    def __init__(self, matrix: Any, is_mock: bool = False):
        """Initialize the shape renderer.
        
        Args:
            matrix: The LED matrix instance
            is_mock: Whether to use mock mode
        """
        self.matrix = matrix
        self.is_mock = is_mock
    
    def draw_circle(self, x: int, y: int, radius: int, color: Tuple[int, int, int]) -> None:
        """Draw a filled circle.
        
        Args:
            x: Center x-coordinate
            y: Center y-coordinate
            radius: Circle radius
            color: RGB color tuple (r, g, b)
        """
        if self.is_mock:
            return
            
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i*i + j*j <= radius*radius:
                    self.matrix.SetPixel(x + i, y + j, *color)
    
    def draw_diamond(self, x: int, y: int, radius: int, color: Tuple[int, int, int]) -> None:
        """Draw a filled diamond.
        
        Args:
            x: Center x-coordinate
            y: Center y-coordinate
            radius: Diamond radius (from center to tip)
            color: RGB color tuple (r, g, b)
        """
        if self.is_mock:
            return
            
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if abs(i) + abs(j) <= radius:
                    self.matrix.SetPixel(x + i, y + j, *color)
    
    def draw_thick_F(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Draw a 2px thick F letter.
        
        Args:
            x: Starting x-coordinate (left edge)
            y: Starting y-coordinate (top edge)
            color: RGB color tuple (r, g, b)
        """
        if self.is_mock:
            return
            
        # Vertical line
        for i in range(6):  # Height of 6px
            self.matrix.SetPixel(x, y + i, *color)
            self.matrix.SetPixel(x + 1, y + i, *color)
        
        # Top horizontal line
        for i in range(4):  # Width of 4px
            self.matrix.SetPixel(x + i, y, *color)
            self.matrix.SetPixel(x + i, y + 1, *color)
        
        # Middle horizontal line
        for i in range(3):  # Width of 3px
            self.matrix.SetPixel(x + i, y + 3, *color)
            self.matrix.SetPixel(x + i, y + 4, *color)
    
    def draw_thick_G(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Draw a 2px thick G letter.
        
        Args:
            x: Starting x-coordinate (left edge)
            y: Starting y-coordinate (top edge) 
            color: RGB color tuple (r, g, b)
        """
        if self.is_mock:
            return
            
        # Top curve
        for i in range(4):  # Width of 4px
            self.matrix.SetPixel(x + 1 + i, y, *color)
            self.matrix.SetPixel(x + 1 + i, y + 1, *color)
        
        # Left vertical line
        for i in range(6):  # Height of 6px
            self.matrix.SetPixel(x, y + 1 + i, *color)
            self.matrix.SetPixel(x + 1, y + 1 + i, *color)
        
        # Bottom curve
        for i in range(4):  # Width of 4px
            self.matrix.SetPixel(x + 1 + i, y + 6, *color)
            self.matrix.SetPixel(x + 1 + i, y + 7, *color)
        
        # Right vertical stub
        for i in range(3):  # Height of 3px
            self.matrix.SetPixel(x + 4, y + 4 + i, *color)
            self.matrix.SetPixel(x + 5, y + 4 + i, *color)
        
        # Middle horizontal line
        for i in range(2):  # Width of 2px
            self.matrix.SetPixel(x + 3, y + 4, *color)
            self.matrix.SetPixel(x + 3, y + 5, *color) 