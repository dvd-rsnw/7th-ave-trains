import asyncio
import platform
import time
from typing import Tuple, Dict
from styles import F_TRAIN_COLOR, G_TRAIN_COLOR
import sys

# Constants for layout
PANEL_WIDTH = 64  # Width of a single panel
MATRIX_WIDTH = PANEL_WIDTH * 2  # Two panels chained
MATRIX_HEIGHT = 32
PADDING_X = 2
PADDING_Y = 4
CENTER_GAP = 4
ROW_HEIGHT = 10

# Row component measurements
CIRCLE_WIDTH = 10
FIRST_GAP = 3
LINE_NAME_WIDTH = 72  # Exact width for line name
SECOND_GAP = 11
MINUTES_WIDTH = 28  # Remaining space: 128 - (2 + 10 + 3 + 72 + 11 + 2) = 28px

# Scrolling configuration
SCROLL_SPEED = 2  # pixels per second
SCROLL_UPDATE_INTERVAL = 15  # seconds (matches polling interval)

# Use actual display only on Raspberry Pi
if platform.system() == "Linux":
    from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

    options = RGBMatrixOptions()
    options.rows = 16  # Each panel is 16 rows high
    options.cols = 64  # Each panel is 64 columns wide
    options.chain_length = 2  # Two panels chained horizontally
    options.parallel = 1
    options.hardware_mapping = 'adafruit-hat'
    
    # Additional recommended options for better performance
    options.gpio_slowdown = 4  # Slow down GPIO for stability
    options.brightness = 50    # Mid brightness to prevent overheating
    options.pwm_bits = 7      # Lower PWM bits for better refresh
    options.pwm_lsb_nanoseconds = 130  # Tune PWM timing
    options.limit_refresh_rate_hz = 100  # Cap refresh for stability
    # No pixel mapper needed for horizontal arrangement

    matrix = RGBMatrix(options=options)
    font = graphics.Font()
    font.LoadFont("/home/pi/rpi-rgb-led-matrix/fonts/6x10.bdf")

    f_line_color = graphics.Color(*F_TRAIN_COLOR)
    g_line_color = graphics.Color(*G_TRAIN_COLOR)
    text_color = graphics.Color(255, 255, 255)

    # Global variables for scroll positions and timestamps
    scroll_positions = {}
    scroll_timestamps = {}  # New dict to track individual timestamps

    def get_text_width(text: str) -> int:
        """Get the pixel width of text using the current font"""
        return sum(font.CharacterWidth(ord(c)) for c in text)

    def get_section_coordinates(section: int) -> Tuple[int, int, int, int]:
        """Get the coordinates for a section (0=top, 1=bottom)
        Returns: (start_x, start_y, width, height)"""
        start_x = PADDING_X
        start_y = PADDING_Y if section == 0 else PADDING_Y + ROW_HEIGHT + CENTER_GAP
        return (start_x, start_y, MATRIX_WIDTH - (PADDING_X * 2), ROW_HEIGHT)

    def draw_scrolling_text(text: str, x: int, y: int, max_width: int, scroll_key: str):
        """Draw text with scrolling if it exceeds max_width"""
        text_width = get_text_width(text)
        
        if text_width <= max_width:
            # Text fits, no scrolling needed
            graphics.DrawText(matrix, font, x, y, text_color, text)
            scroll_positions[scroll_key] = 0  # Reset scroll position
            scroll_timestamps[scroll_key] = time.time()  # Reset timestamp
        else:
            # Calculate scroll position using individual timestamp
            current_time = time.time()
            if scroll_key not in scroll_timestamps:
                scroll_timestamps[scroll_key] = current_time
            
            time_diff = current_time - scroll_timestamps[scroll_key]
            scroll_amount = int(SCROLL_SPEED * time_diff)
            
            # Update scroll position
            if scroll_key not in scroll_positions:
                scroll_positions[scroll_key] = 0
            scroll_positions[scroll_key] = (scroll_positions[scroll_key] + scroll_amount) % text_width
            
            # Update timestamp
            scroll_timestamps[scroll_key] = current_time
            
            # Draw scrolled text
            offset_x = x - scroll_positions[scroll_key]
            graphics.DrawText(matrix, font, offset_x, y, text_color, text)
            # Draw text again if it's scrolled partially off
            if offset_x + text_width < x + max_width:
                graphics.DrawText(matrix, font, offset_x + text_width, y, text_color, text)

    def draw_circle(x: int, y: int, radius: int, color):
        """Draw a filled circle"""
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if i*i + j*j <= radius*radius:
                    graphics.DrawPixel(matrix, x + i, y + j, color)

    def draw_diamond(x: int, y: int, radius: int, color):
        """Draw a filled diamond"""
        for i in range(-radius, radius + 1):
            for j in range(-radius, radius + 1):
                if abs(i) + abs(j) <= radius:
                    graphics.DrawPixel(matrix, x + i, y + j, color)

    def draw_thick_F(x: int, y: int, color):
        """Draw a 2px thick F letter"""
        # Vertical line
        for i in range(6):  # Height of 6px
            graphics.DrawPixel(matrix, x, y + i, color)
            graphics.DrawPixel(matrix, x + 1, y + i, color)
        
        # Top horizontal line
        for i in range(4):  # Width of 4px
            graphics.DrawPixel(matrix, x + i, y, color)
            graphics.DrawPixel(matrix, x + i, y + 1, color)
        
        # Middle horizontal line
        for i in range(3):  # Width of 3px
            graphics.DrawPixel(matrix, x + i, y + 3, color)
            graphics.DrawPixel(matrix, x + i, y + 4, color)

    def draw_thick_G(x: int, y: int, color):
        """Draw a 2px thick G letter"""
        # Top curve
        for i in range(4):  # Width of 4px
            graphics.DrawPixel(matrix, x + 1 + i, y, color)
            graphics.DrawPixel(matrix, x + 1 + i, y + 1, color)
        
        # Left vertical line
        for i in range(6):  # Height of 6px
            graphics.DrawPixel(matrix, x, y + 1 + i, color)
            graphics.DrawPixel(matrix, x + 1, y + 1 + i, color)
        
        # Bottom curve
        for i in range(4):  # Width of 4px
            graphics.DrawPixel(matrix, x + 1 + i, y + 6, color)
            graphics.DrawPixel(matrix, x + 1 + i, y + 7, color)
        
        # Right vertical stub
        for i in range(3):  # Height of 3px
            graphics.DrawPixel(matrix, x + 4, y + 4 + i, color)
            graphics.DrawPixel(matrix, x + 5, y + 4 + i, color)
        
        # Middle horizontal line
        for i in range(2):  # Width of 2px
            graphics.DrawPixel(matrix, x + 3, y + 4, color)
            graphics.DrawPixel(matrix, x + 3, y + 5, color)

    def render_train_line(section: int, train_data: dict):
        """Render a train line with its text in the specified section"""
        x, y, width, height = get_section_coordinates(section)
        
        # Clear both panels for this section
        for i in range(height):
            graphics.DrawLine(matrix, x, y + i, MATRIX_WIDTH - 1, y + i, graphics.Color(0, 0, 0))
        
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
        else:  # G train
            line_name = "Crosstown"
        
        # Draw the train line indicator (circle or diamond)
        circle_color = f_line_color if line == 'F' else g_line_color
        circle_radius = CIRCLE_WIDTH // 2
        
        if line == 'F' and is_express:
            draw_diamond(circle_x, circle_y, circle_radius, circle_color)
        else:
            draw_circle(circle_x, circle_y, circle_radius, circle_color)
        
        # Draw thick letter centered in circle/diamond
        letter_x = x + (CIRCLE_WIDTH - 6) // 2  # Center the 6px wide letter
        letter_y = y + (height - 8) // 2  # Center the 8px tall letter vertically
        if line == 'F':
            draw_thick_F(letter_x, letter_y, text_color)
        else:  # G train
            draw_thick_G(letter_x, letter_y, text_color)
        
        # Draw line name with scrolling only if needed (> 72px)
        draw_scrolling_text(
            line_name,
            line_name_x,
            y + 7,  # Vertically centered in row
            LINE_NAME_WIDTH,  # 72px as defined in constants
            f'line_name_{section}'
        )
        
        # Draw minutes with scrolling only if needed (> 28px)
        draw_scrolling_text(
            status,
            minutes_x,
            y + 7,  # Vertically centered in row
            MINUTES_WIDTH,  # 28px as defined in constants
            f'minutes_{section}'
        )

    def render_train_1(train_data: dict):
        """Render the first train in the top section"""
        render_train_line(0, train_data)

    def render_train_2(train_data: dict):
        """Render the second train in the bottom section"""
        render_train_line(1, train_data)

    def display_trains(trains: list):
        global last_update_time
        matrix.Clear()
        last_update_time = time.time()  # Update timestamp for scroll calculations
        
        if len(trains) > 0:
            render_train_1(trains[0])
        if len(trains) > 1:
            render_train_2(trains[1])

else:
    # Mac-safe mock functions
    def render_train_1(train_data: dict):
        line = train_data['line']
        express = '(express)' if train_data['express'] else '(local)'
        print(f"[MOCK DISPLAY] Train 1 {line} {express}: {train_data['status']}")

    def render_train_2(train_data: dict):
        line = train_data['line']
        express = '(express)' if train_data['express'] else '(local)'
        print(f"[MOCK DISPLAY] Train 2 {line} {express}: {train_data['status']}")

    def display_trains(trains: list):
        if len(trains) > 0:
            render_train_1(trains[0])
        if len(trains) > 1:
            render_train_2(trains[1])

# Polling loop (shared for both real & mock)
async def poll_and_display():
    import httpx  # imported here so it doesn't crash early on macOS
    while True:
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get("http://127.0.0.1:8000/fg-trains-northbound-next", timeout=5.0)
                if resp.status_code == 200:
                    trains = resp.json()
                    display_trains(trains[:2])  # Display first two trains
                else:
                    display_trains([
                        {"line": "?", "status": "Bad response", "express": False},
                        {"line": "?", "status": "Bad response", "express": False}
                    ])
        except Exception as e:
            display_trains([
                {"line": "?", "status": str(e), "express": False}
            ])
        await asyncio.sleep(15)

# Start the polling loop when script runs
if __name__ == "__main__":
    try:
        asyncio.run(poll_and_display())
    except KeyboardInterrupt:
        print("Exiting...")
        if platform.system() == "Linux":
            matrix.Clear()
            sys.exit(0)
