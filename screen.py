import abc


class Screen(abc.ABC):
    def __init__(self, screen, clock, state_manager):
        self.screen = screen
        self.clock = clock
        self.state_manager = state_manager

    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
