from dataclasses import dataclass
from functools import cached_property
from typing import Dict, List, Tuple, Any, TypedDict, Optional, NamedTuple

from matrix_setup import (
    MATRIX_WIDTH, MATRIX_HEIGHT, PANEL_WIDTH,
    PADDING_X, PADDING_Y, CENTER_GAP, ROW_HEIGHT,
    CIRCLE_WIDTH, FIRST_GAP, LINE_NAME_WIDTH, 
    SECOND_GAP, MINUTES_WIDTH
)
from styles import F_TRAIN_COLOR, G_TRAIN_COLOR


@dataclass(frozen=True)
class SectionCoordinates:
    """Immutable coordinates for a section."""
    start_x: int
    start_y: int
    width: int
    height: int
    
    @property
    def end_x(self) -> int:
        return self.start_x + self.width - 1
        
    @property
    def end_y(self) -> int:
        return self.start_y + self.height - 1


@dataclass(frozen=True)
class ComponentCoordinates:
    """Immutable coordinates for rendering components."""
    circle_x: int
    circle_y: int
    circle_radius: int
    letter_x: int
    letter_y: int
    line_name_x: int
    minutes_x: int
    minutes_end_x: int
    text_y: int


@dataclass(frozen=True)
class TrainData:
    """Immutable train data structure."""
    line: str  # 'F' or 'G'
    express: bool
    status: str
    
    @property
    def line_name(self) -> str:
        """Get the full name of the line."""
        if self.line == 'F':
            return "6 Av - Culver Express" if self.express else "6 Av Local"
        return "Crosstown"  # G train


class TrainRenderer:
    """Renders train information on the LED matrix display."""
    
    # Class constants
    MAX_LINE_NAME_LENGTH = 14
    MAX_STATUS_LENGTH = 7
    TEXT_COLOR = (255, 255, 255)
    
    def __init__(
        self, 
        matrix: Any,  # Matrix type not exposed in library
        graphics: Any,  # Graphics type not exposed in library
        text_renderer: Any,
        shape_renderer: Any,
        is_mock: bool = False
    ) -> None:
        """Initialize the train renderer."""
        self.matrix = matrix
        self.graphics = graphics
        self.text_renderer = text_renderer
        self.shape_renderer = shape_renderer
        self.is_mock = is_mock
        
        # Initialize colors once
        if not is_mock:
            self._f_line_color = graphics.Color(*F_TRAIN_COLOR)
            self._g_line_color = graphics.Color(*G_TRAIN_COLOR)
            self._text_color = graphics.Color(*self.TEXT_COLOR)
            self._black_color = graphics.Color(0, 0, 0)
    
    @cached_property
    def _section_coordinates(self) -> Tuple[SectionCoordinates, SectionCoordinates]:
        """Cache the coordinates for both sections."""
        section0 = SectionCoordinates(
            start_x=PADDING_X,
            start_y=PADDING_Y,
            width=MATRIX_WIDTH - (PADDING_X * 2),
            height=ROW_HEIGHT
        )
        section1 = SectionCoordinates(
            start_x=PADDING_X,
            start_y=PADDING_Y + ROW_HEIGHT + CENTER_GAP,
            width=MATRIX_WIDTH - (PADDING_X * 2),
            height=ROW_HEIGHT
        )
        return (section0, section1)
    
    def _get_component_coordinates(self, section_coords: SectionCoordinates) -> ComponentCoordinates:
        """Calculate all component coordinates for a section."""
        x, y = section_coords.start_x, section_coords.start_y
        height = section_coords.height
        
        circle_x = x + CIRCLE_WIDTH // 2
        circle_y = y + (height // 2)
        circle_radius = CIRCLE_WIDTH // 2
        letter_x = x + (CIRCLE_WIDTH - 6) // 2
        letter_y = y + (height - 8) // 2
        line_name_x = x + CIRCLE_WIDTH + FIRST_GAP - 1
        minutes_x = line_name_x + LINE_NAME_WIDTH + SECOND_GAP - 1
        minutes_end_x = minutes_x + MINUTES_WIDTH
        text_y = y + 9
        
        return ComponentCoordinates(
            circle_x=circle_x,
            circle_y=circle_y,
            circle_radius=circle_radius,
            letter_x=letter_x,
            letter_y=letter_y,
            line_name_x=line_name_x,
            minutes_x=minutes_x,
            minutes_end_x=minutes_end_x,
            text_y=text_y
        )
    
    def _get_line_color(self, train: TrainData) -> Any:
        """Get the color for a train line."""
        if train.line == 'F':
            return self._f_line_color if not self.is_mock else F_TRAIN_COLOR
        return self._g_line_color if not self.is_mock else G_TRAIN_COLOR
    
    def _parse_status(self, status: str) -> Tuple[str, Optional[str]]:
        """Parse the status string into variable and fixed parts."""
        if not status or " mins" not in status:
            return (status[:self.MAX_STATUS_LENGTH], None)
        
        parts = status.split(" mins", 1)
        return (parts[0], " mins")
    
    def _clear_section(self, coords: SectionCoordinates) -> None:
        """Clear a section efficiently."""
        if self.is_mock:
            return
            
        # Fill rectangle with black
        for y in range(coords.start_y, coords.end_y + 1):
            self.graphics.DrawLine(
                self.matrix,
                coords.start_x,
                y,
                coords.end_x,
                y,
                self._black_color
            )
    
    def render_train_line(self, section: int, train: TrainData) -> None:
        """Render a train line with its text in the specified section."""
        if self.is_mock:
            express = '(express)' if train.express else '(local)'
            print(f"[MOCK DISPLAY] Train {section+1} {train.line} {express}: {train.status}")
            return
            
        # Get cached section coordinates
        section_coords = self._section_coordinates[section]
        coords = self._get_component_coordinates(section_coords)
        
        # Clear the section
        self._clear_section(section_coords)
        
        # Get line color
        circle_color = self._get_line_color(train)
        
        # Draw train indicator
        if train.line == 'F' and train.express:
            self.shape_renderer.draw_diamond(
                coords.circle_x,
                coords.circle_y,
                coords.circle_radius,
                circle_color
            )
        else:
            self.shape_renderer.draw_circle(
                coords.circle_x,
                coords.circle_y,
                coords.circle_radius,
                circle_color
            )
        
        # Draw line letter
        if train.line == 'F':
            self.shape_renderer.draw_thick_F(
                coords.letter_x,
                coords.letter_y,
                self.TEXT_COLOR
            )
        else:
            self.shape_renderer.draw_thick_G(
                coords.letter_x,
                coords.letter_y,
                self.TEXT_COLOR
            )
        
        # Draw line name (truncated)
        self.text_renderer.draw_text(
            train.line_name[:self.MAX_LINE_NAME_LENGTH],
            coords.line_name_x,
            coords.text_y
        )
        
        # Draw status
        variable_part, fixed_part = self._parse_status(train.status)
        if fixed_part:
            self.text_renderer.draw_text_with_fixed_suffix(
                variable_part,
                fixed_part,
                coords.minutes_end_x,
                coords.text_y
            )
        else:
            self.text_renderer.draw_text(
                variable_part,
                coords.minutes_x,
                coords.text_y
            )

    def render_trains(self, trains: List[TrainData]) -> None:
        """Render a list of trains (up to 2)."""
        if self.matrix and not self.is_mock:
            self.matrix.Clear()
            
        if len(trains) > 0:
            self.render_train_line(0, trains[0])
        if len(trains) > 1:
            self.render_train_line(1, trains[1])