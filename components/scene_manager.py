import pygame
from services.config_loader import WIN, DRAW_LINES

class Renderer:
    
    # -- Pipe rendering --
    def draw_background(self, background):
        WIN.blit(background.IMAGE, (background.x1, background.y))
        WIN.blit(background.IMAGE, (background.x2, background.y))
    
    # -- Bird rendering --
    def draw_bird(self, bird):
        bird.update_image()
        self.blitRotateCenter(bird.img, (bird.x, bird.y), bird.tilt)
        
    def blitRotateCenter(self, image, topleft, angle):
        rotated_image = pygame.transform.rotate(image, angle)
        new_rect = rotated_image.get_rect(center=image.get_rect(topleft=topleft).center)
        WIN.blit(rotated_image, new_rect.topleft)
        
    def draw_bird_trace(self, bird, pipes):
        # draw lines from bird to pipe
        if DRAW_LINES:
            pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[0].x + pipes[0].PIPE_TOP.get_width()/2, pipes[0].height), 5)
            pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[0].x + pipes[0].PIPE_BOTTOM.get_width()/2, pipes[0].bottom), 5)

            pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[1].x + pipes[1].PIPE_TOP.get_width()/2, pipes[1].height), 5)
            pygame.draw.line(WIN, (255,0,0), (bird.x+bird.img.get_width()/2, bird.y + bird.img.get_height()/2), (pipes[1].x + pipes[1].PIPE_BOTTOM.get_width()/2, pipes[1].bottom), 5)
            
    # -- Floor rendering --
    def draw_floor(self, floor):
        WIN.blit(floor.IMAGE, (floor.x1, floor.y))
        WIN.blit(floor.IMAGE, (floor.x2, floor.y))
        
    # -- State rendering --
    def draw_state(self, state):
        WIN.blit(state.get_render_object(), (state.x, state.y))
        
    # -- Pipe rendering --
    def draw_pipe(self, pipe):
        WIN.blit(pipe.PIPE_TOP, (pipe.x, pipe.top))
        WIN.blit(pipe.PIPE_BOTTOM, (pipe.x, pipe.bottom))