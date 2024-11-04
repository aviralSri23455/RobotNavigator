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
