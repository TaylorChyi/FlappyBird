import pygame
from services.config_loader import BIRDS_IMAGE

class Bird:
    """Class representing the flappy bird in the game.
    
    Attributes:
        MAX_ROTATION (int): Maximum rotation angle.
        IMGS (list): List of bird images for animation.
        ROT_VEL (int): Rotation velocity.
        ANIMATION_TIME (int): Time for each bird animation frame.
        JUMP_VELOCITY (int): Upward velocity applied when the bird jumps.
        GRAVITY_ACCEL (float): Acceleration due to gravity.
        MAX_DISPLACEMENT (int): Maximum displacement per frame.
        TILT_DOWN_ANGLE (int): Angle to tilt downwards.
    """
    
    MAX_ROTATION = 25
    IMGS = BIRDS_IMAGE
    ROT_VEL = 7
    ANIMATION_TIME = 8
    JUMP_VELOCITY = -150
    GRAVITY_ACCEL = 1.3
    MAX_DISPLACEMENT = 16
    TILT_DOWN_ANGLE = -80
    x = 150


    def __init__(self, y):
        """Initialize the bird object.
        
        Args:
            x (int): Starting x position.
            y (int): Starting y position.
        """
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.image_count = 0
        self.image = self.IMGS[0]

    def jump(self):
        """Make the bird jump by setting its velocity to a predefined upward value."""
        self.vel = self.JUMP_VELOCITY
        self.tick_count = 0
        self.height = self.y

    def move(self, delta_time):
        """Calculate and update the bird's position based on its velocity and gravitational acceleration.
        Adjust the bird's tilt based on its movement."""
        self.tick_count += 1

        # Calculate displacement
        displacement = self.vel * delta_time +  self.GRAVITY_ACCEL * (self.tick_count**2) * delta_time
        if displacement >= self.MAX_DISPLACEMENT:
            displacement = (displacement/abs(displacement)) * self.MAX_DISPLACEMENT
        if displacement < 0:
            displacement -= 2

        # Update position
        self.y += displacement

        # Adjust tilt
        if displacement < 0 or self.y < self.height + 50:
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION
        elif self.tilt > self.TILT_DOWN_ANGLE:
            self.tilt -= self.ROT_VEL

    def update_image(self):
        """Update the bird's image for animation.
        
        Cycle through the bird images to create a flapping effect."""
        self.image_count = (self.image_count + 1) % (len(self.IMGS) * self.ANIMATION_TIME)
        idx = self.image_count // self.ANIMATION_TIME
        self.img = self.IMGS[idx]

        if self.tilt <= self.TILT_DOWN_ANGLE:
            self.img = self.IMGS[1]
