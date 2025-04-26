Team Name: 404 Brain Not Found<br>
Team ID: 19<br>

Problem Number: 2<br>
Title: Asteroid Collision Detection in 2D Space<br>

How to Run:<br>
    Install Dependencies:<br>
        No external dependencies. Uses only Python’s built-in math and concurrent.futures libraries.<br>
    Run the Simulation:<br>
        Open terminal in project folder.<br>
        Run:python main.py<br>

Expected Input:<br>
    Input File: asteroids.txt<br>
    Each line should contain:<br>
    ID x y vx vy radius<br>
    Example:<br>
        1 100 200 1.5 -0.5 20<br>
        2 300 400 -1.0 1.2 15<br>

Output:<br>
    Output File: collisions.txt<br>
    Each line format:<br>
    time_step asteroid1_id asteroid2_id<br>
    Example:<br>
        2.1 1 2<br>
        2.3 3 5<br>

Notes<br>
    Keep asteroids.txt in the same directory as main.py.<br>
    Collision results will be saved to collisions.txt in the same folder.<br>
