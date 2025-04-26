Team Name: 404 Brain Not Found
Team ID: 19

Problem Number: 2
Title: Asteroid Collision Detection in 2D Space

How to Run:
    Install Dependencies:
        No external dependencies. Uses only Python’s built-in math and concurrent.futures libraries.
    Run the Simulation:
        Open terminal in project folder.
        Run:python main.py

Expected Input:
    Input File: asteroids.txt
    Each line should contain:
    ID x y vx vy radius
    Example:
        1 100 200 1.5 -0.5 20
        2 300 400 -1.0 1.2 15

Output:
    Output File: collisions.txt
    Each line format:
    time_step asteroid1_id asteroid2_id
    Example:
        2.1 1 2
        2.3 3 5

Notes
    Keep asteroids.txt in the same directory as main.py.
    Collision results will be saved to collisions.txt in the same folder.