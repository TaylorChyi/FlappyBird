import pygame
from patterns.singleton import Singleton

class InputManager(Singleton):
    def __init__(self):
        self.jump_request = False   # Indicates if the player has requested the bird to jump
        self.pause_request = False  # Indicates if the player has requested to pause the game
        self.quit_request = False # Indicates if the player has requested to quit the game

    def handle_events(self):
        """Process all input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.request_quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.request_jump()
                elif event.key == pygame.K_p:
                    self.request_pause()
                elif event.key == pygame.K_ESCAPE:
                    self.request_quit()

    def reset_all(self):
        """Reset all input requests."""
        self.jump_request = False
        self.pause_request = False
        self.quit_request = False
    
    def reset_jump(self):
        """Reset the jump request."""
        self.jump_request = False
        
    def reset_pause(self):
        """Reset the pause request."""
        self.pause_request = False
        
    def reset_quit(self):
        """Reset the quit request."""
        self.quit_request = False
        
    def request_jump(self):
        """Request the bird to jump."""
        self.jump_request = True

    def is_jump_requested(self):
        """Check if the player has requested the bird to jump."""
        return self.jump_request
    
    def request_pause(self):
        """Request to pause the game."""
        self.pause_request = not self.pause_request
    
    def is_pause_requested(self):
        """Check if the player has requested to pause the game."""
        return self.pause_request
    
    def request_quit(self):
        """Request to quit the game."""
        self.quit_request = True

    def is_quit_requested(self):
        """Check if the player has requested to quit the game."""
        return self.quit_request