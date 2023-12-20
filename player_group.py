from player import Player


class PlayerGroup:
    def __init__(self, data):
        self.data = data
        self.players = {i: Player(**val) for i, val in self.data.items()}

    def keys(self):
        return self.players.keys()

    def values(self):
        return self.players.values()

    def items(self):
        return self.players.items()

    def __iter__(self):
        return self.players.__iter__()

    def __getitem__(self, item):
        return self.players.__getitem__(item)

    def __contains__(self, item):
        return self.players.__contains__(item)

    def __len__(self):
        return self.players.__len__()

    def __repr__(self):
        return "\n" + "\n".join(player.__repr__() for player in self.players.values())

    def reset_players(self):
        for player in self.values():
            player.reset()

    def move_all(self):
        for player in self.values():
            player.move()

    def self_collisions(self):
        """Detects self-collisions for players."""
        players_with_self_collision = []

        for player in self.players.values():
            # Check for self-collision, excluding the head
            if player.head in player.path[:-1]:
                players_with_self_collision.append(player)

        return players_with_self_collision

    def collisions_with_others(self):
        """Detects collisions of a player with other players' paths."""
        players_with_other_collision = []

        for player1 in self.values():
            for player2 in self.values():
                if (not (player1 is player2)) and player1.head in player2.path:
                    players_with_other_collision.append((player1, player2))

        return players_with_other_collision

    def head_on_collisions(self):
        """Detects head-on collisions between players based on mutual collisions."""
        players_who_head_on_collision = set()

        # First, get all collisions with others
        collisions = self.collisions_with_others()

        # Create a set for easier lookup
        collision_set = set(collisions)

        # Check for mutual collisions indicating head-on collisions
        for player1, player2 in collisions:
            if (player2, player1) in collision_set:
                players_who_head_on_collision.add(player1)
                players_who_head_on_collision.add(player2)

        return list(players_who_head_on_collision)

    def all_collisions(self):
        """Detects any type of collision and returns a list of player IDs involved."""
        collision_players = set()

        # Add all players involved in any type of collision
        collision_players.update(self.self_collisions())
        collision_players.update([pair[0] for pair in self.collisions_with_others()])
        collision_players.update(self.head_on_collisions())

        return list(collision_players)

    def determine_win_condition(self):
        # Get collision information
        players_who_head_on_collisions = self.head_on_collisions()

        # Determine alive players
        alive_players = set(player for player in self.values() if player.alive)

        if len(alive_players) == 1:  # Only one alive player is the winner
            winner = alive_players.pop()
            winner.win()
            alive_players.add(winner)  # ugh
        elif len(alive_players) > 1:
            return {player_id: () for player_id in self.keys()}

        for player in self.values():
            if player in players_who_head_on_collisions:
                player.tie()
            elif player in alive_players:
                pass
            else:
                player.lose()

        return {player_id: player.score_history[-1] for player_id, player in self.items()}
