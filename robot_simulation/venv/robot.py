import numpy as np

class Robot:
    def __init__(self, x=0, y=0, speed=0.1, move_time=0.1, rest_time=2, boundaries=(10, 10)):
        self.position = np.array([x, y])
        self.speed = speed  # Speed in m/s
        self.move_time = move_time  # Movement duration in seconds
        self.rest_time = rest_time  # Rest duration in seconds
        self.boundaries = np.array(boundaries)
        self.path_history = [self.position.copy()]

    def move_towards(self, target_x, target_y, obstacles=[]):
        target_position = np.array([target_x, target_y])
        direction = target_position - self.position
        distance_to_target = np.linalg.norm(direction)

        if distance_to_target < 0.1:
            return True  # Reached target

        direction /= distance_to_target  # Normalize direction

        # Calculate potential new position
        step_distance = min(self.speed * self.move_time, distance_to_target)
        new_position = self.position + direction * step_distance

        # Ensure the new position stays within boundaries
        new_position = np.clip(new_position, [0, 0], self.boundaries)

        # Update position if there's no collision
        if not self.is_collision(new_position, obstacles):
            self.position = new_position
            self.path_history.append(self.position.copy())

        return np.linalg.norm(target_position - self.position) < 0.1

    def is_collision(self, new_position, obstacles):
        """Check if the new position collides with any obstacles."""
        for obs_x, obs_y, radius in obstacles:
            if np.linalg.norm(new_position - np.array([obs_x, obs_y])) < radius:
                return True
        return False
