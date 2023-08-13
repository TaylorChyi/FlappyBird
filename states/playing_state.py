
from states.base_state import GameState

class PlayingState(GameState):

    def handle_events(self, controller):
        # Handle events while the game is playing (like bird jump)
        pass

    def update(self, controller):
        # Update game components like bird, pipes, etc.
        pass

    def render(self, controller):
        # Render game components to the screen
        pass
