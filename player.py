import colorsys
from path import Path
import joblib


class Player:
    def __init__(self, origin=None, head_colour=None):
        self.origin = origin
        self.head_colour = (255, 255, 255) if head_colour is None else head_colour
        self.path_colour = self.lighten_color(head_colour)
        self.head = (0, 0) if origin is None else origin
        self.path = Path()
        self.score_history = []
        self.alive = True
        self.direction = "up"
        self.movement_queue = []
        self.boosts = 3

        self.direction_mapping = {
            "up": (-1, 0),
            "down": (1, 0),
            "left": (0, -1),
            "right": (0, 1),
        }

        self.opposite_directions = {
            "up": "down",
            "down": "up",
            "left": "right",
            "right": "left",
        }

        self.rgb_to_name = self.setup_rgb_func()
        self.name = ""#self.rgb_to_name(head_colour)

    @staticmethod
    def lighten_color(rgb, increase=0.1):
        r, g, b = [x / 255.0 for x in rgb]
        h, l, s = colorsys.rgb_to_hls(r, g, b)
        l = min(1.0, l + increase)
        r, g, b = colorsys.hls_to_rgb(h, l, s)
        return int(r * 255), int(g * 255), int(b * 255)

    @staticmethod
    def setup_rgb_func():
        """Applies an SVM to the WEBCOLORS module."""

        data = joblib.load("rgb_to_name_predictor.joblib")
        model, label_encoder = data["model"], data["encoder"]
        return lambda rgb_val: label_encoder.inverse_transform(model.predict([rgb_val]))[0]

    def move(self, teleport=False):
        if not self.alive:
            return

        if self.movement_queue:
            new_direction = self.movement_queue.pop(0)
            if new_direction != self.opposite_directions[self.direction]:
                self.direction = new_direction

        dr, dc = self.direction_mapping[self.direction]
        r, c = self.head
        nr, nc = (r + dr, c + dc)
        self.head = (nr, nc)
        if teleport is False:
            self.path.add(self.head)

    def change_direction(self, new_direction):
        if new_direction is None:
            return
        if not self.alive:
            return
        if new_direction != self.direction and new_direction != self.opposite_directions[self.direction]:
            self.movement_queue.append(new_direction)

    def reset(self):
        self.head = (0, 0) if self.origin is None else self.origin
        self.path = Path()
        self.alive = True
        self.movement_queue.clear()

    def win(self):
        self.score_history.append(("win", 1))

    def tie(self):
        self.score_history.append(("tie", 0.5))

    def lose(self):
        self.score_history.append(("lose", 0))

    def __repr__(self):
        return f"Player(origin={self.origin}, head_colour={self.head_colour}, head={self.head}, score_history={self.score_history[-3:]}, alive={self.alive}, direction={self.direction})"
