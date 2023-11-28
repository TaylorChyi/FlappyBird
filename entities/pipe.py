import pygame
import random
from services.config_loader import PIPE_IMAGE

class Pipe:
    
    MIN_GAP = 200
    VEL = 150

    def __init__(self, x):
        self.x = x
        self.height = 0
        
        self.gap = self.MIN_GAP + random.randrange(0, 100)

        # y position for the top and bottom of the pipe
        self.top = 0
        self.bottom = 0

        # Flip the PIPE_IMG for a top pipe
        self.PIPE_TOP = pygame.transform.flip(PIPE_IMAGE, False, True)
        self.PIPE_BOTTOM = PIPE_IMAGE

        self.passed = False  # Check if the bird has passed the pipe

        self.set_height()

    def set_height(self):
        self.height = random.randrange(50, 450)
        self.top = self.height - self.PIPE_TOP.get_height()
        self.bottom = self.height + self.gap
        self.center = self.height + self.gap / 2

    def move(self, delta_time):
        self.x -= self.VEL * delta_time
        
    def get_top_pipe_position(self):
        return (self.x, self.height - self.PIPE_TOP.get_height())

    def get_bottom_pipe_position(self):
        return (self.x, self.height + self.gap)
