from services.config_loader import BACKGROUND_IMAGE, BACKGROUND_VELOCITY

class Background:
    """Class to represent the scrolling background of the game.
    
    Attributes:
        VEL (int): Speed at which the background moves.
        IMAGE (pygame.Surface): Surface object of the background image.
        WIDTH (int): Width of the background image.
        y (int): Vertical position of the background.
        x1 (int): Horizontal position of the first background image.
        x2 (int): Horizontal position of the second background image.
    """
    
    def __init__(self, image=BACKGROUND_IMAGE, velocity=BACKGROUND_VELOCITY, y_position=0):
        """Initialize the Background object by setting the velocities, loading the image, 
        and setting the initial positions.
        
        Args:
            image (pygame.Surface): Image to be used as the background.
            velocity (int): Speed at which the background moves.
            y_position (int): Vertical position of the background.
        """
        self.VEL = velocity
        self.IMAGE = image
        self.WIDTH = self.IMAGE.get_width()
        self.y = y_position
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, delta_time):
        """Move the background images to create a scrolling effect. If an image goes off screen,
        it's repositioned to the right to create a continuous loop.
        
        Args:
            delta_time (float): Time since the last frame.
        """
        self.x1 -= self.VEL * delta_time
        self.x2 -= self.VEL * delta_time
        
        # Adjust the backgrounds if they go off screen
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
