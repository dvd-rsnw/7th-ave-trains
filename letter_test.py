#!/usr/bin/env python3

def visualize_letter_F():
    """Visualize the F letter drawing algorithm."""
    width = 8
    height = 9
    f_grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Vertical line (2px thick)
    for i in range(height):
        f_grid[i][1] = 'F'
        f_grid[i][2] = 'F'
    
    # Top horizontal line (2px thick)
    for i in range(2):
        for j in range(5):  # Top width is 5px
            f_grid[i][j+1] = 'F'
    
    # Middle horizontal line (2px thick)
    for i in range(2):
        for j in range(4):  # Mid width is 4px
            f_grid[i+4][j+1] = 'F'
    
    print("F Letter:")
    for row in f_grid:
        print(''.join(row))


def visualize_letter_G():
    """Visualize the G letter drawing algorithm."""
    width = 8
    height = 9
    g_grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Define the G shape as a list of ranges for each row
    g_shape = [
        (1, 6),    # Row 0: Top row (xooooo)
        (0, 6),    # Row 1: Second row (oooooo)
        (0, 2),    # Row 2: Third row left (oo)
        (0, 2),    # Row 3: Fourth row left (oo)
        (0, 2, 3, 6),  # Row 4: Fifth row (ooxooo)
        (0, 2, 3, 6),  # Row 5: Sixth row (ooxooo)
        (0, 2, 4, 6),  # Row 6: Seventh row (ooxxoo)
        (0, 6),    # Row 7: Eighth row (oooooo)
        (1, 6),    # Row 8: Ninth row (xooooo)
    ]
    
    # Fill in the grid based on the G shape
    for row, ranges in enumerate(g_shape):
        if len(ranges) == 2:
            start, end = ranges
            for col in range(start, end):
                g_grid[row][col] = 'G'
        else:  # Split ranges for rows with gaps
            start1, end1, start2, end2 = ranges
            for col in range(start1, end1):
                g_grid[row][col] = 'G'
            for col in range(start2, end2):
                g_grid[row][col] = 'G'
    
    print("G Letter:")
    for row in g_grid:
        print(''.join(row))


def visualize_train_display():
    """Visualize the complete train display with circle/diamond and letters."""
    # F-train express in diamond
    width = 20
    height = 10
    f_express_grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw diamond at position (5, 5) with radius 3
    for y in range(-3, 4):
        for x in range(-3, 4):
            if abs(x) + abs(y) <= 3:
                f_express_grid[y+5][x+5] = 'O'
    
    # Place F in the center
    f_express_grid[4][5] = 'F'
    f_express_grid[5][5] = 'F'
    f_express_grid[6][5] = 'F'
    
    # Add some train information
    f_express_grid[2][10] = 'E'
    f_express_grid[2][11] = 'x'
    f_express_grid[2][12] = 'p'
    f_express_grid[2][13] = 'r'
    f_express_grid[2][14] = 'e'
    f_express_grid[2][15] = 's'
    f_express_grid[2][16] = 's'
    
    print("F Train Express:")
    for row in f_express_grid:
        print(''.join(row))
    
    # G-train in circle
    g_train_grid = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw circle at position (5, 5) with radius 3
    for y in range(-3, 4):
        for x in range(-3, 4):
            dist = x**2 + y**2
            if dist <= 9:  # 3*3 = radius squared
                g_train_grid[y+5][x+5] = 'O'
    
    # Place G in the center
    g_train_grid[4][5] = 'G'
    g_train_grid[5][5] = 'G'
    g_train_grid[6][5] = 'G'
    
    # Add some train information
    g_train_grid[2][10] = 'C'
    g_train_grid[2][11] = 'r'
    g_train_grid[2][12] = 'o'
    g_train_grid[2][13] = 's'
    g_train_grid[2][14] = 's'
    g_train_grid[2][15] = 't'
    g_train_grid[2][16] = 'o'
    g_train_grid[2][17] = 'w'
    g_train_grid[2][18] = 'n'
    
    print("\nG Train:")
    for row in g_train_grid:
        print(''.join(row))


if __name__ == "__main__":
    visualize_letter_F()
    print("\n" + "="*30 + "\n")
    visualize_letter_G()
    print("\n" + "="*30 + "\n")
    visualize_train_display() 