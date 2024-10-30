import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation


class Robot:
    def __init__(self, x=0, y=0, speed=0.1, move_time=0.1, rest_time=2.0):
        self.x = x
        self.y = y
        self.speed = speed
        self.move_time = move_time
        self.rest_time = rest_time

    @staticmethod
    def distance(x1, y1, x2, y2):
        return np.hypot(x2 - x1, y2 - y1)

    def move_towards(self, target_x, target_y, obstacles=None):
        direction_x, direction_y = target_x - self.x, target_y - self.y
        distance_to_target = self.distance(self.x, self.y, target_x, target_y)

        if distance_to_target < self.speed:
            return True  # Target reached

        # Normalize direction to a unit vector
        norm = np.hypot(direction_x, direction_y)
        direction_x, direction_y = direction_x / norm, direction_y / norm

        new_x = self.x + direction_x * self.speed
        new_y = self.y + direction_y * self.speed

        # Check for obstacles
        if obstacles and self.check_obstacles(new_x, new_y, obstacles):
            new_x, new_y = self.avoid_obstacles(direction_x, direction_y)

        self.x, self.y = new_x, new_y
        return False  # Target not yet reached

    def check_obstacles(self, new_x, new_y, obstacles):
        for (obs_x, obs_y, radius) in obstacles:
            if self.distance(new_x, new_y, obs_x, obs_y) < radius + 0.1:
                return True
        return False

    def avoid_obstacles(self, direction_x, direction_y):
        angle_offset = np.pi / 4  # 45 degrees
        direction_x, direction_y = (
            np.cos(angle_offset) * direction_x - np.sin(angle_offset) * direction_y,
            np.sin(angle_offset) * direction_x + np.cos(angle_offset) * direction_y
        )
        new_x = self.x + direction_x * self.speed
        new_y = self.y + direction_y * self.speed
        return new_x, new_y


class Simulation:
    def __init__(self, warehouse_size=(10, 10), target=(7, 9), obstacles=None):
        self.warehouse_width, self.warehouse_height = warehouse_size
        self.target = target
        self.robot = Robot()
        self.obstacles = obstacles or [(3, 3, 0.5), (6, 5, 0.5)]

        self.setup_plot()
        self.path_trace = []
        self.stop_points = []

    def setup_plot(self):
        """Set up the plot for the simulation."""
        self.fig, self.ax = plt.subplots()
        self.ln, = self.ax.plot([], [], 'b-', alpha=0.5, label='Robot Path')
        self.robot_point, = self.ax.plot([], [], 'ro', markersize=10, label='Robot')
        self.target_point, = self.ax.plot([self.target[0]], [self.target[1]], 'g*', markersize=15, label='Target')
        self.stopping_points, = self.ax.plot([], [], 'yo', markersize=5, label='Stop Points')

        for (obs_x, obs_y, radius) in self.obstacles:
            obstacle_circle = plt.Circle((obs_x, obs_y), radius, color='gray', alpha=0.5)
            self.ax.add_patch(obstacle_circle)

    def init_animation(self):
        """Initialize the animation."""
        self.ax.set_xlim(-1, self.warehouse_width + 1)
        self.ax.set_ylim(-1, self.warehouse_height + 1)
        self.ax.grid(True)
        self.ax.set_title('Robot Navigation Simulation')
        self.ax.set_xlabel('X (meters)')
        self.ax.set_ylabel('Y (meters)')
        self.ax.legend()
        return self.ln, self.robot_point, self.target_point, self.stopping_points

    def update(self, frame):
        """Update the state of the simulation for each frame."""
        reached_target = self.robot.move_towards(*self.target, obstacles=self.obstacles)
        self.path_trace.append((self.robot.x, self.robot.y))

        if self.should_record_stop():
            self.stop_points.append((self.robot.x, self.robot.y))

        self.limit_trace_length()
        self.update_plot_data()

        # Change robot color based on motion state
        self.robot_point.set_color('blue' if reached_target or self.should_pause() else 'red')
        self.robot_point.set_data([self.robot.x], [self.robot.y])
        
        return self.ln, self.robot_point, self.target_point, self.stopping_points

    def should_record_stop(self):
        """Check if the robot should record a stop point."""
        return len(self.path_trace) > 1 and np.hypot(
            self.path_trace[-1][0] - self.path_trace[-2][0],
            self.path_trace[-1][1] - self.path_trace[-2][1]
        ) < 0.01

    def limit_trace_length(self):
        """Limit the length of the path trace for fading effect."""
        if len(self.path_trace) > 100:
            self.path_trace.pop(0)

    def update_plot_data(self):
        """Update the data for the plot."""
        path = list(zip(*self.path_trace))
        if path:
            self.ln.set_data(*path)

        stop_points_x, stop_points_y = zip(*self.stop_points) if self.stop_points else ([], [])
        self.stopping_points.set_data(stop_points_x, stop_points_y)

    def should_pause(self):
        """Determine if the robot should pause."""
        return len(self.path_trace) % int(self.robot.rest_time / self.robot.move_time) == 0

    def run(self):
        """Run the simulation."""
        try:
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
        except KeyboardInterrupt:
            plt.close()  # Close the plot on interruption


# Execution block
if __name__ == "__main__":
    sim = Simulation()
    sim.run()
