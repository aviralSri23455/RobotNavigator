# Autonomous Robot Warehouse Simulation

## Project Setup

### Step 1: Install Required Libraries

To set up the project environment, open a terminal or command prompt and use the following command to install the necessary Python libraries:

```bash
**pip install numpy matplotlib**

```
- **numpy** is used for mathematical calculations.
- **matplotlib** is used to visualize the robot's movements in a 2D environment.

### Step 2: Project Structure

- Create a new folder named Robot.
- Inside this folder, create two Python files:
- **robot.py:** Contains the Robot class, which represents the robot's movements and obstacle avoidance.
- **simulation.py:** Contains the Simulation class, which sets up the environment, defines obstacles, and animates the robot's movement

```bash
Folder structure:
Robot/
├── robot.py
├── simulation.py
└── README.md
```

### Step 3: Writing the Code
- Part 1: Define the Robot Class in robot.py
- The Robot class represents the autonomous robot, managing its movements, speed, and obstacle avoidance.

```python
import numpy as np

class Robot:
    def __init__(self, x=0, y=0, speed=0.1, move_time=0.1, rest_time=2.0):
        self.position = np.array([x, y])
        self.speed = speed
        self.move_time = move_time
        self.rest_time = rest_time
        self.time_elapsed = 0
        self.moving = True  # Start with moving
        self.path_history = [self.position.copy()]

    def move_towards(self, target_x, target_y, delta_time, obstacles=[]):
        """Move the robot towards the target position, with pauses every move_time."""
        
        # If in resting phase, increment time and check if rest is over
        if not self.moving:
            self.time_elapsed += delta_time
            if self.time_elapsed >= self.rest_time:
                # Reset to moving state
                self.time_elapsed = 0
                self.moving = True
            return False  # Still resting

        # If moving, calculate movement towards the target
        target_position = np.array([target_x, target_y])
        direction = target_position - self.position
        distance_to_target = np.linalg.norm(direction)
        
        if distance_to_target < self.speed * delta_time:
            return True  # Reached target

        # Normalize direction and calculate step distance
        direction /= distance_to_target
        step_distance = self.speed * delta_time
        new_position = self.position + direction * step_distance

        # Check for obstacle collisions before updating position
        if not self.is_collision(new_position, obstacles):
            self.position = new_position
            self.path_history.append(self.position.copy())
        
        # Increment time, switch to rest if move_time is reached
        self.time_elapsed += delta_time
        if self.time_elapsed >= self.move_time:
            self.time_elapsed = 0
            self.moving = False
        
        return False  # Target not reached

    def is_collision(self, new_position, obstacles):
        """Check if new position collides with obstacles."""
        for obs_x, obs_y, radius in obstacles:
            if np.linalg.norm(new_position - np.array([obs_x, obs_y])) < radius:
                return True
        return False

```

- Attributes:

- **position:** Current position of the robot.
- **speed:** Speed of the robot (0.1 m/s).
- **move_time:** Duration of each movement (0.1 seconds).
- **rest_time:** Duration of each rest period (2 seconds).

- Methods:

- **distance:** Calculates distance to a target point.
- **move_towards:** Moves the robot toward the target while checking for obstacles.
- **check_obstacles:** Detects if the robot is close to an obstacle.
- **avoid_obstacles:** Alters the robot’s path to avoid obstacles.

### Part 2: Define the Simulation Class in simulation.py

- The Simulation class sets up the environment and animates the robot’s movements in a 10x10 warehouse.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from robot import Robot

class Simulation:
    def __init__(self, warehouse_size=(10, 10), target=(7, 9), obstacles=None):
        # Initialization logic
        # ...

    def setup_plot(self):
        """Set up the plot for the simulation."""
        # Plotting logic

    def update(self, frame):
        """Update robot's state per frame."""
        # Update logic for robot movements

    def run(self):
        """Run the simulation."""
        anim = FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init_animation,
            frames=None,
            interval=100,
            blit=True,
            repeat=False,
            cache_frame_data=False
        )
        plt.show()

# Execution
if __name__ == "__main__":
    sim = Simulation()
    sim.run()

```

- Attributes:

- **warehouse_size:** Sets the warehouse dimensions to 10x10 meters.
- **target:** Destination of the robot (7, 9).
- **robot:** Instance of the Robot class.
- **obstacles:** List of obstacle positions.
- Methods:

- **setup_plot:** Configures the simulation plot.
- **update:**  Updates the robot's position, checks for movement/rest periods.
- **run:** Runs the simulation.

### Step 4: Running the Simulation

- To run the simulation, create an entry function in simulation.py:

```python
from simulation import Simulation

def main():
    sim = Simulation()
    sim.run()

if __name__ == "__main__":
    main()

```