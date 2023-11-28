from services.config_loader import FLOOR_IMAGE

class Floor:
    """
    Represnts the moving floor of the game
    """
    VEL = 150
    IMAGE = FLOOR_IMAGE
    WIDTH = IMAGE.get_width()
    
    def __init__(self, y):
        """
        Initialize the object
        :param y: int
        :return: None
        """
        self.y = y
        self.x1 = 0
        self.x2 = self.WIDTH

    def move(self, delta_time):
        """
        move floor so it looks like its scrolling
        :return: None
        """
        self.x1 -= self.VEL * delta_time
        self.x2 -= self.VEL * delta_time
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH
