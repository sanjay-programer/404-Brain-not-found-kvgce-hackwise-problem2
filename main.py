import math
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

# === Simulation Parameters ===
TIME_STEP = 0.1  # Time increment in seconds
MAX_TIME = 10.0  # Total simulation run time in seconds
GRID_CELL_SIZE = 50  # Size of each cell for spatial hashing (used for optimizing collision checks)


# === Step 1: Read Asteroid Data from File ===
def read_asteroids(file_path):
    """
    Reads asteroid data from a text file.
    Each line should have either:
    - 5 values: x, y, radius, vx, vy  (auto-generated ID will be assigned)
    - 6 values: id, x, y, radius, vx, vy

    Returns:
        List of tuples: (id, x, y, r, vx, vy)
    """
    asteroids = []
    with open(file_path) as f:
        for line_num, line in enumerate(f, start=1):
            parts = line.strip().split()
            if len(parts) not in [5, 6]:
                print(f"Invalid input at line {line_num}. Skipping.")
                continue

            try:
                if len(parts) == 5:
                    id_ = line_num
                    x, y, r, vx, vy = map(float, parts)
                else:
                    id_ = int(parts[0])
                    x, y, r, vx, vy = map(float, parts[1:])

                asteroids.append((id_, x, y, r, vx, vy))
            except ValueError:
                print(f"Invalid number format at line {line_num}. Skipping.")
    return asteroids


# === Step 2: Spatial Hashing Utility ===
def get_hash_cell(x, y, cell_size):
    """
    Calculates which grid cell (as a tuple) a point belongs to based on its x, y coordinates.
    """
    return (int(x // cell_size), int(y // cell_size))


# === Step 3: Simulate Asteroid Motion and Track Collisions ===
def simulate_motion(asteroids, time_step, max_time):
    """
    Simulates the motion of asteroids over time and detects collisions using spatial hashing.

    Returns:
        Sorted list of collisions as (time, id1, id2)
    """
    grid = defaultdict(list)  # Hash grid to store asteroids by their grid cell
    collisions = set()  # Set to store detected collisions (to avoid duplicates)
    time_steps = int(max_time / time_step)

    for step in range(time_steps + 1):
        t = round(step * time_step, 1)
        grid.clear()  # Reset grid at each time step

        # Update asteroid positions and assign them to appropriate grid cells
        for asteroid in asteroids:
            id_, x, y, r, vx, vy = asteroid
            new_x, new_y = x + vx * t, y + vy * t
            cell = get_hash_cell(new_x, new_y, GRID_CELL_SIZE)
            grid[cell].append((id_, new_x, new_y, r))

        # Parallel collision detection for each cell and its neighbors
        with ThreadPoolExecutor() as executor:
            future_to_cell = {
                executor.submit(check_collisions_in_cell, cell, grid, t): cell for cell in grid
            }
            for future in future_to_cell:
                collisions.update(future.result())

    return sorted(collisions)


# === Step 4: Check for Collisions within and Around a Grid Cell ===
def check_collisions_in_cell(cell, grid, t):
    """
    Checks for collisions among asteroids within a specific cell and its 8 neighboring cells.

    Returns:
        Set of collisions as (time, id1, id2)
    """
    local_collisions = set()
    asteroids_in_cell = grid[cell]

    # Identify neighboring cells (including the current cell itself)
    neighbors = [
        cell,
        (cell[0] - 1, cell[1] - 1), (cell[0], cell[1] - 1), (cell[0] + 1, cell[1] - 1),
        (cell[0] - 1, cell[1]), (cell[0] + 1, cell[1]),
        (cell[0] - 1, cell[1] + 1), (cell[0], cell[1] + 1), (cell[0] + 1, cell[1] + 1),
    ]

    seen_collisions = set()

    # Compare each asteroid with others in neighboring cells
    for neighbor in neighbors:
        if neighbor not in grid:
            continue
        for asteroid1 in asteroids_in_cell:
            for asteroid2 in grid[neighbor]:
                id1, x1, y1, r1 = asteroid1
                id2, x2, y2, r2 = asteroid2

                if id1 >= id2:
                    continue  # Avoid duplicate or self-collisions

                dist = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
                if dist < r1 + r2:
                    collision_key = tuple(sorted((id1, id2)))
                    if collision_key not in seen_collisions:
                        local_collisions.add((t, id1, id2))
                        seen_collisions.add(collision_key)

    return local_collisions


# === Step 5: Write Detected Collisions to Output File ===
def write_collisions_to_file(collisions, output_path):
    """
    Writes the list of detected collisions to a text file in the format:
    time id1 id2
    """
    with open(output_path, 'w') as f:
        for collision in collisions:
            t, id1, id2 = collision
            f.write(f"{t:.1f} {id1} {id2}\n")


# === Main Execution Function ===
def main(input_file, output_file):
    """
    Main driver function to run the asteroid collision simulation.
    """
    asteroids = read_asteroids(input_file)
    collisions = simulate_motion(asteroids, TIME_STEP, MAX_TIME)
    write_collisions_to_file(collisions, output_file)
    print(f"Collision detection complete. Results saved to {output_file}.")


# === Execute Simulation ===
# Replace 'asteroids_test.txt' and 'collisions_test.txt' with your actual file paths if needed
input_file = "sample_output/asteroids.txt"
output_file = "sample_output/collisions.txt"
main(input_file, output_file)