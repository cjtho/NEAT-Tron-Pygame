import random


class GameLogic:
    def __init__(self, player_group):
        self.player_group = player_group
        self.running = True
        self.iterations = 0
        self.rows = 65
        self.cols = 100

        self.place_players()

    def reset_game(self):
        self.running = True
        self.player_group.reset_players()
        self.place_players()

    def place_players(self):
        num_players = len(self.player_group)
        padding = min(self.rows, self.cols) // 10

        if num_players == 1:
            player_positions = [
                (self.rows // 2, self.cols // 2)
            ]
        elif num_players == 2:
            middle_row = self.rows // 2
            player_positions = [
                (middle_row, padding),
                (middle_row, self.cols - padding - 1)
            ]
        elif num_players <= 4:
            player_positions = [
                (padding, padding),
                (self.rows - padding - 1, padding),
                (padding, self.cols - padding - 1),
                (self.rows - padding - 1, self.cols - padding - 1)
            ]
        else:
            raise ValueError("This algorithm supports up to 4 players (exceeded).")

        player_positions = player_positions[:num_players]

        if random.choice([False, False]):
            player_positions = player_positions[::-1]

        for player_pos, player_id in zip(player_positions, self.player_group):
            player = self.player_group[player_id]
            player.origin = player_pos
            player.head = player_pos

            if player_pos[1] < self.cols // 2:
                player.direction = "right"
                # player.path.set_direction("right")
            else:
                player.direction = "left"
                # player.path.set_direction("left")

            player.path.add(player_pos)

    def update(self):
        if not self.running:
            return

        self.player_group.move_all()

        for player in self.player_group.all_collisions():
            player.alive = False

        for player in self.player_group.values():
            if self.hit_wall(player.head):
                player.alive = False

        self.running = not self.is_game_over()

        self.iterations += 1

        if not self.running:
            self.player_group.determine_win_condition()

    def hit_wall(self, pos):
        return not (0 < pos[0] < self.rows - 1 and 0 < pos[1] < self.cols - 1)

    def is_game_over(self):
        # at least two players remain
        return sum(player.alive for player in self.player_group.values()) <= 1
