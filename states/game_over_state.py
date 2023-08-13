from states.base_state import GameState

class GameOverState(GameState):

    def handle_events(self, controller):
        # Handle events for game over screen (like restart button click)
        pass

    def update(self, controller):
        # Update any animations or highlights in game over screen
        pass

    def render(self, controller):
        # Render game over screen to the screen
        pass
