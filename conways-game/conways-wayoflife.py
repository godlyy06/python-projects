import os
import time
import random

# Set the dimensions and visual representation of the grid
WIDTH = 60
HEIGHT = 20
ALIVE = '█'
DEAD = ' '

def create_grid():
    # Generate a 2D array filled with random 0s (dead) and 1s (alive)
    return [[random.choice([0, 1]) for _ in range(WIDTH)] for _ in range(HEIGHT)]

def print_grid(grid):
    # Clear the terminal screen (works on Windows 'nt' and Linux/Mac 'clear')
    os.system('cls' if os.name == 'nt' else 'clear')
    
    # Iterate through the grid and print the corresponding characters
    for row in grid:
        print("".join([ALIVE if cell else DEAD for cell in row]))

def count_neighbors(grid, x, y):
    count = 0
    # Loop through the 3x3 area surrounding the current cell
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
                
            # Use modulo to wrap around the edges (creates a toroidal/seamless grid)
            row = (y + i) % HEIGHT
            col = (x + j) % WIDTH
            count += grid[row][col]
            
    return count

def next_generation(grid):
    # Create an empty grid for the next frame
    new_grid = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
    
    # Apply Conway's rules to every cell
    for y in range(HEIGHT):
        for x in range(WIDTH):
            neighbors = count_neighbors(grid, x, y)
            
            # Rule 1 & 2: Any live cell with 2 or 3 neighbors survives
            if grid[y][x] == 1 and neighbors in [2, 3]:
                new_grid[y][x] = 1
            # Rule 3: Any dead cell with exactly 3 neighbors becomes a live cell
            elif grid[y][x] == 0 and neighbors == 3:
                new_grid[y][x] = 1
                
    return new_grid

def main():
    # Initialize the starting state
    grid = create_grid()
    
    try:
        # Create an infinite loop to animate the simulation
        while True:
            print_grid(grid)
            grid = next_generation(grid)
            time.sleep(0.1) # Pause briefly to make the animation viewable
            
    except KeyboardInterrupt:
        # Gracefully handle user exit when Ctrl+C is pressed
        print("\nSimulation stopped.")

if __name__ == "__main__":
    main()