from typing import Tuple, Dict, Any, List

from styles import F_TRAIN_COLOR, G_TRAIN_COLOR
from matrix_setup import (
    PADDING_X, PADDING_Y, ROW_HEIGHT, CENTER_GAP, MATRIX_WIDTH,
    CIRCLE_WIDTH, FIRST_GAP, LINE_NAME_WIDTH, SECOND_GAP, MINUTES_WIDTH
)


class TrainRenderer:
    """Renders train information on the LED matrix display."""
    
    def __init__(
        self, matrix, graphics, text_renderer, shape_renderer, is_mock=False
    ):
        """Initialize the train renderer.
        
        Args:
            matrix: The LED matrix instance
            graphics: The graphics library
            text_renderer: Text rendering component
            shape_renderer: Shape rendering component
            is_mock: Whether to use mock mode (print to console instead)
        """
        self.matrix = matrix
        self.graphics = graphics
        self.text_renderer = text_renderer
        self.shape_renderer = shape_renderer
        self.is_mock = is_mock
        
        # Define colors
        if not is_mock:
            self.f_line_color = graphics.Color(*F_TRAIN_COLOR)
            self.g_line_color = graphics.Color(*G_TRAIN_COLOR)
            self.text_color = graphics.Color(255, 255, 255)
    
    def get_section_coordinates(self, section: int) -> Tuple[int, int, int, int]:
        """Get the coordinates for a section (0=top, 1=bottom).
        
        Args:
            section: Section index (0 for top, 1 for bottom)
            
        Returns:
            Tuple of (start_x, start_y, width, height)
        """
        start_x = PADDING_X
        start_y = PADDING_Y if section == 0 else PADDING_Y + ROW_HEIGHT + CENTER_GAP
        return (start_x, start_y, MATRIX_WIDTH - (PADDING_X * 2), ROW_HEIGHT)
    
    def render_train_line(self, section: int, train_data: Dict[str, Any]) -> None:
        """Render a train line with its text in the specified section.
        
        Args:
            section: Section index (0 for top, 1 for bottom)
            train_data: Dictionary containing train information
        """
        if self.is_mock:
            line = train_data['line']
            express = '(express)' if train_data['express'] else '(local)'
            print(f"[MOCK DISPLAY] Train {section+1} {line} {express}: {train_data['status']}")
            return
            
        x, y, width, height = self.get_section_coordinates(section)
        
        # Clear both panels for this section
        for i in range(height):
            self.graphics.DrawLine(
                self.matrix, x, y + i, MATRIX_WIDTH - 1, y + i, 
                self.graphics.Color(0, 0, 0)
            )
        
        # Calculate component positions
        circle_x = x + CIRCLE_WIDTH // 2
        circle_y = y + (height // 2)
        line_name_x = x + CIRCLE_WIDTH + FIRST_GAP
        minutes_x = line_name_x + LINE_NAME_WIDTH + SECOND_GAP
        
        # Get train information
        line = train_data['line']
        is_express = train_data['express']
        status = train_data['status']
        
        # Determine line name based on train type
        if line == 'F':
            line_name = "6 Av - Culver Express" if is_express else "6 Av Local"
            circle_color = F_TRAIN_COLOR if self.is_mock else self.f_line_color
        else:  # G train
            line_name = "Crosstown"
            circle_color = G_TRAIN_COLOR if self.is_mock else self.g_line_color
        
        # Draw the train line indicator (circle or diamond)
        circle_radius = CIRCLE_WIDTH // 2
        
        if line == 'F' and is_express:
            self.shape_renderer.draw_diamond(
                circle_x, circle_y, circle_radius, 
                F_TRAIN_COLOR if self.is_mock else circle_color
            )
        else:
            self.shape_renderer.draw_circle(
                circle_x, circle_y, circle_radius, 
                G_TRAIN_COLOR if line == 'G' and self.is_mock else circle_color
            )
        
        # Draw thick letter centered in circle/diamond
        letter_x = x + (CIRCLE_WIDTH - 6) // 2  # Center the 6px wide letter
        letter_y = y + (height - 8) // 2  # Center the 8px tall letter vertically
        text_color_tuple = (255, 255, 255)
        
        if line == 'F':
            self.shape_renderer.draw_thick_F(letter_x, letter_y, text_color_tuple)
        else:  # G train
            self.shape_renderer.draw_thick_G(letter_x, letter_y, text_color_tuple)
        
        # Draw line name with scrolling only if needed (> 72px)
        self.text_renderer.draw_scrolling_text(
            line_name,
            line_name_x,
            y + 7,  # Vertically centered in row
            LINE_NAME_WIDTH,  # 72px as defined in constants
            f'line_name_{section}'
        )
        
        # Draw minutes with scrolling only if needed (> 28px)
        self.text_renderer.draw_scrolling_text(
            status,
            minutes_x,
            y + 7,  # Vertically centered in row
            MINUTES_WIDTH,  # 28px as defined in constants
            f'minutes_{section}'
        )
    
    def render_trains(self, trains: List[Dict[str, Any]]) -> None:
        """Render a list of trains (up to 2).
        
        Args:
            trains: List of train dictionaries to display
        """
        if self.matrix and not self.is_mock:
            self.matrix.Clear()
            
        if len(trains) > 0:
            self.render_train_line(0, trains[0])
        if len(trains) > 1:
            self.render_train_line(1, trains[1]) 