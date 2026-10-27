import os
import random
import select
import sys
import time

# Conway's Game of Life: a cellular automaton where each cell evolves based on
# the state of its neighbors according to a small set of rules.
# This version is closer to the classic game by using a finite field with dead
# cells at the edges, and it also includes a few known life patterns.

WIDTH = 60
HEIGHT = 24
ALIVE = '█'
DEAD = ' '
FRAME_DELAY = 0.12
MIN_FRAME_DELAY = 0.03
MAX_FRAME_DELAY = 0.5
CHALLENGE_TARGET = 100
CHALLENGE_GENERATIONS = 30


def create_empty_grid():
    """Return a new grid with every cell dead."""
    return [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]


def count_population(grid):
    """Count all living cells on the board."""
    return sum(sum(row) for row in grid)


def place_pattern(grid, pattern, start_x, start_y):
    """Add a pattern to the grid starting at (start_x, start_y)."""
    for y, row in enumerate(pattern):
        for x, cell in enumerate(row):
            if cell == 1:
                grid_y = start_y + y
                grid_x = start_x + x
                if 0 <= grid_y < HEIGHT and 0 <= grid_x < WIDTH:
                    grid[grid_y][grid_x] = 1


def make_random_grid(density=0.2):
    """Create a grid with a random number of living cells."""
    grid = create_empty_grid()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if random.random() < density:
                grid[y][x] = 1
    return grid


def create_pattern_library():
    """Return a dictionary of famous small patterns from Conway's Game of Life."""
    return {
        'glider': [
            [0, 1, 0],
            [0, 0, 1],
            [1, 1, 1],
        ],
        'blinker': [
            [1, 1, 1],
        ],
        'toad': [
            [0, 1, 1, 1],
            [1, 1, 1, 0],
        ],
        'beacon': [
            [1, 1, 0, 0],
            [1, 1, 0, 0],
            [0, 0, 1, 1],
            [0, 0, 1, 1],
        ],
        'pulsar': [
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0],
        ],
    }


def create_grid(mode='random', density=0.18):
    """Create the starting state for the simulation.

    Modes:
    - 'random': a field with a moderate amount of live cells
    - 'glider': a single glider near the middle
    - 'mixed': several small patterns placed together
    """
    grid = create_empty_grid()

    if mode == 'random':
        return make_random_grid(density)

    patterns = create_pattern_library()

    if mode == 'glider':
        place_pattern(grid, patterns['glider'], WIDTH // 2 - 2, HEIGHT // 2)
        return grid

    if mode == 'mixed':
        pattern_names = ['glider', 'blinker', 'toad', 'beacon']
        for index, name in enumerate(pattern_names):
            pattern = patterns[name]
            start_x = 5 + index * 12
            start_y = 3 + (index % 2) * 7
            place_pattern(grid, pattern, start_x, start_y)
        return grid

    return make_random_grid(density)


def print_grid(
    grid, generation, cursor_x, cursor_y, running, mode, score,
    peak_population, frame_delay, outcome=None
):
    """Draw the board, game stats, objective, and keyboard controls."""
    # ANSI escape codes clear and reposition the terminal without starting a
    # separate shell process for every frame.
    print('\033[2J\033[H', end='')
    state = 'Running' if running else 'Paused'
    population = count_population(grid)
    mode_name = 'Challenge' if mode == 'challenge' else 'Sandbox'
    print(f"CONWAY'S GAME OF LIFE  |  {mode_name}  |  {state}")
    print(
        f"Generation: {generation}  |  Living cells: {population}"
        f"  |  Peak: {peak_population}  |  Score: {score}"
        f"  |  Frame: {frame_delay:.2f}s"
    )

    if mode == 'challenge':
        progress = min(population / CHALLENGE_TARGET, 1)
        filled = int(progress * 20)
        progress_bar = '#' * filled + '-' * (20 - filled)
        print(
            f"MISSION: reach {CHALLENGE_TARGET} living cells by generation "
            f"{CHALLENGE_GENERATIONS}  [{progress_bar}]"
        )

    if outcome == 'won':
        print("CHALLENGE COMPLETE! You reached the population goal.")
    elif outcome == 'lost':
        print("CHALLENGE OVER: the generation limit was reached.")

    for y, row in enumerate(grid):
        display_row = []
        for x, cell in enumerate(row):
            if x == cursor_x and y == cursor_y:
                display_row.append('@')
            else:
                display_row.append(ALIVE if cell else DEAD)
        print(''.join(display_row))

    if outcome:
        print("\nR: restart challenge | M: main menu | Q: quit")
    else:
        print("\nWASD: move | Space: toggle cell | P/Enter: run or pause")
        print("N: step | 1-5: place pattern | +/-: speed | G: randomize")
        print("C: clear | R: restart | M: main menu | Q: quit")
        print("Patterns: 1 Glider, 2 Blinker, 3 Toad, 4 Beacon, 5 Pulsar")
    sys.stdout.flush()


def read_key(timeout=None):
    """Read one key, optionally waiting for at most timeout seconds."""
    if os.name == 'nt':
        import msvcrt

        if timeout is None:
            while not msvcrt.kbhit():
                time.sleep(0.05)
        elif not msvcrt.kbhit():
            time.sleep(timeout)
            return None
        return msvcrt.getwch()

    ready, _, _ = select.select([sys.stdin], [], [], timeout)
    return sys.stdin.read(1) if ready else None


class TerminalInput:
    """Enable single-key input without requiring the user to press Enter."""

    def __enter__(self):
        if os.name != 'nt':
            import termios
            import tty

            self.termios = termios
            self.previous_settings = termios.tcgetattr(sys.stdin)
            tty.setcbreak(sys.stdin.fileno())
        return self

    def __exit__(self, exception_type, exception, traceback):
        if os.name != 'nt':
            self.termios.tcsetattr(
                sys.stdin, self.termios.TCSADRAIN, self.previous_settings
            )


def count_neighbors(grid, x, y):
    """Count how many neighboring cells are alive.

    This version uses a finite grid: cells outside the visible field are treated
    as dead, which is closer to the original mathematical concept of Conway's
    Game of Life than wrapping the grid around edges.
    """
    count = 0

    for offset_y in (-1, 0, 1):
        for offset_x in (-1, 0, 1):
            if offset_x == 0 and offset_y == 0:
                continue

            neighbor_x = x + offset_x
            neighbor_y = y + offset_y

            if 0 <= neighbor_x < WIDTH and 0 <= neighbor_y < HEIGHT:
                count += grid[neighbor_y][neighbor_x]

    return count


def next_generation(grid):
    """Calculate the next generation using Conway's rules."""
    new_grid = create_empty_grid()

    for y in range(HEIGHT):
        for x in range(WIDTH):
            neighbors = count_neighbors(grid, x, y)
            cell_is_alive = grid[y][x] == 1

            # Rule 1: A live cell survives if it has exactly 2 or 3 neighbors.
            # Rule 2: A dead cell becomes alive if it has exactly 3 neighbors.
            # Rule 3: All other cells die or stay dead.
            if cell_is_alive and neighbors in (2, 3):
                new_grid[y][x] = 1
            elif not cell_is_alive and neighbors == 3:
                new_grid[y][x] = 1

    return new_grid


def check_challenge(mode, population, generation):
    """Return the challenge result after a generation, if it has ended."""
    if mode != 'challenge':
        return None
    if population >= CHALLENGE_TARGET:
        return 'won'
    if generation >= CHALLENGE_GENERATIONS:
        return 'lost'
    return None


def run_game(mode):
    """Run one sandbox or timed population-challenge session."""
    grid = create_grid(mode='mixed')
    generation = 0
    cursor_x = WIDTH // 2
    cursor_y = HEIGHT // 2
    running = False
    score = 0
    peak_population = count_population(grid)
    frame_delay = FRAME_DELAY
    outcome = None
    patterns = create_pattern_library()
    pattern_keys = {
        '1': 'glider',
        '2': 'blinker',
        '3': 'toad',
        '4': 'beacon',
        '5': 'pulsar',
    }

    while True:
        print_grid(
            grid, generation, cursor_x, cursor_y, running, mode,
            score, peak_population, frame_delay, outcome
        )
        key = read_key(frame_delay if running and not outcome else None)

        if key is None:
            grid = next_generation(grid)
            generation += 1
            population = count_population(grid)
            # Score rewards the total number of living cells across generations.
            score += population
            peak_population = max(peak_population, population)

            outcome = check_challenge(mode, population, generation)
            if outcome:
                running = False
            continue

        key = key.lower()
        if key == 'q':
            return True
        if key == 'm':
            return False

        if outcome and key != 'r':
            continue

        if key == 'w':
            cursor_y = max(0, cursor_y - 1)
        elif key == 's':
            cursor_y = min(HEIGHT - 1, cursor_y + 1)
        elif key == 'a':
            cursor_x = max(0, cursor_x - 1)
        elif key == 'd':
            cursor_x = min(WIDTH - 1, cursor_x + 1)
        elif key == ' ':
            grid[cursor_y][cursor_x] = 1 - grid[cursor_y][cursor_x]
            peak_population = max(peak_population, count_population(grid))
        elif key in ('p', '\r', '\n'):
            running = not running
        elif key == 'n':
            running = False
            grid = next_generation(grid)
            generation += 1
            population = count_population(grid)
            score += population
            peak_population = max(peak_population, population)
            outcome = check_challenge(mode, population, generation)
        elif key in pattern_keys:
            # Center patterns on the cursor so they are easy to position.
            pattern = patterns[pattern_keys[key]]
            place_pattern(
                grid,
                pattern,
                cursor_x - len(pattern[0]) // 2,
                cursor_y - len(pattern) // 2,
            )
            peak_population = max(peak_population, count_population(grid))
        elif key == '+':
            frame_delay = max(MIN_FRAME_DELAY, frame_delay * 0.8)
        elif key == '-':
            frame_delay = min(MAX_FRAME_DELAY, frame_delay / 0.8)
        elif key == 'g':
            grid = make_random_grid()
            generation = 0
            score = 0
            peak_population = count_population(grid)
            running = False
            outcome = None
        elif key == 'c':
            grid = create_empty_grid()
            generation = 0
            score = 0
            peak_population = 0
            running = False
            outcome = None
        elif key == 'r':
            grid = create_grid(mode='mixed')
            generation = 0
            score = 0
            peak_population = count_population(grid)
            frame_delay = FRAME_DELAY
            running = False
            outcome = None


def print_menu():
    """Show the mode selection screen."""
    print('\033[2J\033[H', end='')
    print("CONWAY'S GAME OF LIFE")
    print("\n1: Sandbox - experiment without a win condition")
    print(
        f"2: Population Challenge - reach {CHALLENGE_TARGET} living cells "
        f"within {CHALLENGE_GENERATIONS} generations"
    )
    print("Q: quit")
    sys.stdout.flush()


def main():
    """Show the menu and run the selected game mode."""
    try:
        with TerminalInput():
            while True:
                print_menu()
                key = read_key()
                if key is None:
                    continue
                key = key.lower()
                if key == 'q':
                    break
                if key == '1':
                    if run_game('sandbox'):
                        break
                elif key == '2':
                    if run_game('challenge'):
                        break
    except KeyboardInterrupt:
        pass
    finally:
        print('\033[2J\033[HThanks for playing!')


if __name__ == '__main__':
    main()