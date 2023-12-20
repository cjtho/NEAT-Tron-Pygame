class StateManager:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock

        self.states = {}
        self.current_state_key = None
        self.current_state = None

    def add_state(self, state_key, state_class):
        self.states[state_key] = state_class

    def set_state(self, state_key, *args):
        self.current_state_key = state_key
        self.current_state = self.states[self.current_state_key](self.screen,
                                                                 self.clock,
                                                                 self,
                                                                 *args)
        return self.current_state

    def handle_event(self, event):
        self.current_state.handle_event(event)

    def update(self):
        self.current_state.update()

    def draw(self):
        self.current_state.draw()
