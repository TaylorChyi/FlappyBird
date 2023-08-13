from abc import ABC, abstractmethod

class GameState(ABC):

    @abstractmethod
    def handle_events(self, controller):
        """Handle game events for the specific state."""
        pass

    @abstractmethod
    def update(self, controller):
        """Update the game state."""
        pass

    @abstractmethod
    def render(self, controller):
        """Render the game state to the screen."""
        pass
