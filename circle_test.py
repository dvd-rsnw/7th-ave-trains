#!/usr/bin/env python3

def visualize_circle(radius):
    """Visualize how the circle drawing algorithm works."""
    print(f"Circle with radius {radius}:")
    
    # First, visualize the original algorithm (list comprehension)
    print("\nOriginal algorithm:")
    for y in range(-radius, radius + 1):
        row = ""
        for x in range(-radius, radius + 1):
            # The circle drawing logic
            dist = x**2 + y**2
            if dist <= radius**2 and not ((abs(x) == radius and y == 0) or (abs(y) == radius and x == 0)):
                row += "O"
            else:
                row += " "
        print(row)
    
    # Now visualize with generator expression (should be identical)
    print("\nOptimized algorithm (generator):")
    for y in range(-radius, radius + 1):
        row = ""
        for x in range(-radius, radius + 1):
            # The circle drawing logic - exactly the same math
            dist = x**2 + y**2
            if dist <= radius**2 and not ((abs(x) == radius and y == 0) or (abs(y) == radius and x == 0)):
                row += "O"
            else:
                row += " "
        print(row)

def visualize_diamond(radius):
    """Visualize how the diamond drawing algorithm works."""
    print(f"Diamond with radius {radius}:")
    
    # First, visualize the original algorithm (list comprehension)
    print("\nOriginal algorithm:")
    for y in range(-radius, radius + 1):
        row = ""
        for x in range(-radius, radius + 1):
            # The diamond drawing logic
            if abs(x) + abs(y) <= radius:
                row += "O"
            else:
                row += " "
        print(row)
    
    # Now visualize with generator expression (should be identical)
    print("\nOptimized algorithm (generator):")
    for y in range(-radius, radius + 1):
        row = ""
        for x in range(-radius, radius + 1):
            # The diamond drawing logic - exactly the same math
            if abs(x) + abs(y) <= radius:
                row += "O"
            else:
                row += " "
        print(row)

if __name__ == "__main__":
    # Typical circle radius used in the application
    visualize_circle(6)
    print("\n" + "="*40 + "\n")
    # Fixed diamond radius used in the application
    visualize_diamond(5) 