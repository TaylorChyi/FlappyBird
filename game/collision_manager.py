import pygame
from services.config_loader import WIN_HEIGHT

class CollisionManager:
    
    @staticmethod
    def check_floor_collision(bird, floor):
        return bird.y + bird.image.get_height() >= WIN_HEIGHT - floor.IMAGE.get_height() or bird.y < 0

    
    @staticmethod
    def check_pipe_collision(bird, pipe):

        original_bird_mask = CollisionManager._get_image_mask(bird.image)
        width, height = original_bird_mask.get_size()
        bird_mask = original_bird_mask.scale((int(width * 0.9), int(height * 0.9)))

        pipe_top_mask = CollisionManager._get_image_mask(pipe.PIPE_TOP)
        pipe_bottom_mask = CollisionManager._get_image_mask(pipe.PIPE_BOTTOM)
        

        top_offset_x = pipe.get_top_pipe_position()[0] - bird.x
        top_offset_y = round(pipe.get_top_pipe_position()[1] - bird.y)

        top_collision_point = bird_mask.overlap(pipe_top_mask, (top_offset_x, top_offset_y))
        
        
        bottom_offset_x = pipe.get_bottom_pipe_position()[0] - bird.x
        bottom_offset_y = round(pipe.get_bottom_pipe_position()[1] - bird.y)
        
        bottom_collision_point = bird_mask.overlap(pipe_bottom_mask, (bottom_offset_x, bottom_offset_y))
        return (top_collision_point is not None) or (bottom_collision_point is not None)

    @staticmethod
    def _get_image_mask(image):
        """
        Gets the mask for a given image.

        Args:
            image (pygame.Surface): The image for which the mask is to be generated.

        Returns:
            pygame.mask.Mask: The mask of the provided image.
        """
        return pygame.mask.from_surface(image)
