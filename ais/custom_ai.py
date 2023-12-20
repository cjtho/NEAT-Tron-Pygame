import random


class CustomAI:
    def __init__(self, player, rows, cols):
        self.player = player
        self.rows = rows
        self.cols = cols
        self.padding = 2
        self.reaction_time = 0.9  # essentially it's difficulty parameter
        self.current_step = 0
        self.reach_limit = 100
        self.set_random_target()

    def set_random_target(self, opponent_position=None):
        area_range = 7  # Range for area around the opponent

        if opponent_position and random.choice([True, False]):
            # Set target within 10x10 area around the opponent
            min_row, max_row = (max(self.padding, opponent_position[0] - area_range),
                                min(self.rows - self.padding, opponent_position[0] + area_range))
            min_col, max_col = (max(self.padding, opponent_position[1] - area_range),
                                min(self.cols - self.padding, opponent_position[1] + area_range))
            self.target_location = (random.randint(min_row, max_row), random.randint(min_col, max_col))
        else:
            # Set target randomly anywhere in the grid
            self.target_location = (random.randint(self.padding, self.rows - self.padding),
                                    random.randint(self.padding, self.cols - self.padding))

            self.current_step = 0

    def update_player(self, player_group, game_logic):
        current_position = self.player.head
        if self.current_step >= self.reach_limit or current_position == self.target_location:
            players = list(player_group.values())
            players.remove(self.player)
            other_player = players.pop()
            self.set_random_target(other_player.head)

        direction = None
        ideal_directions = self.get_optimal_directions(current_position)
        while ideal_directions:
            ideal_direction = ideal_directions.pop()
            if self.is_safe_direction(self.player.head, ideal_direction, player_group):
                direction = ideal_direction
                break

        safe_options = self.get_safe_directions(self.player.head, player_group)
        if direction is None and safe_options:
            safe_option = safe_options.pop()
            direction = safe_option

        if random.random() <= self.reaction_time:
            self.player.change_direction(direction)
        self.current_step += 1

    def get_optimal_directions(self, current_position):
        directions = []
        row_diff, col_diff = (self.target_location[0] - current_position[0],
                              self.target_location[1] - current_position[1])
        if row_diff > 0:
            directions.append("down")
        elif row_diff < 0:
            directions.append("up")
        if col_diff > 0:
            directions.append("right")
        elif col_diff < 0:
            directions.append("left")
        return directions

    def choose_direction(self, current_position, player_group, optimal_directions):
        safe_directions = self.get_safe_directions(current_position, player_group)
        return min(safe_directions,
                   key=lambda direction: self.manhattan_distance(self.get_next_position(current_position, direction)),
                   default=None)

    def get_safe_directions(self, current_position, player_group):
        return [direction for direction in ["up", "down", "left", "right"] if
                self.is_safe_direction(current_position, direction, player_group)]

    def manhattan_distance(self, position):
        return abs(position[0] - self.target_location[0]) + abs(position[1] - self.target_location[1])

    def is_safe_direction(self, current_position, direction, player_group):
        next_position = self.get_next_position(current_position, direction)
        if not (self.padding <= next_position[0] < self.rows - self.padding and self.padding <= next_position[
            1] < self.cols - self.padding):
            return False
        return all(next_position not in player.path for player in player_group.values())

    @staticmethod
    def get_next_position(position, direction):
        if direction == "up":
            return position[0] - 1, position[1]
        elif direction == "down":
            return position[0] + 1, position[1]
        elif direction == "left":
            return position[0], position[1] - 1
        elif direction == "right":
            return position[0], position[1] + 1

    def eval_fitness(self, *args):
        pass