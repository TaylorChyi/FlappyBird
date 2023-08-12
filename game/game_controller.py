import pygame
import random
from collections import deque
import pickle
import os

from components.bird import Bird
from components.pipe import Pipe
from components.floor import Floor
from components.background import Background
from components.state import State

from view.renderer import Renderer
from config.config_loader import WIN_WIDTH, WIN_HEIGHT, FLOOR_IMAGE, FITNESS_PIPE, FITNESS_FLOOR, FITNESS_LIVE, FITNESS_PASS, DRAW_LINES

from utils.file_loader import file_path

from game.collision_manager import CollisionManager

import neat

class GameController:

    def __init__(self, mode):
        self.mode = mode
        
        if (self.mode == "HUMAN"):
            self.birds = [Bird(230, (WIN_HEIGHT - FLOOR_IMAGE.get_height()) // 2)]  # Start with one bird for simplicity
        elif (self.mode == "TRAIN"):
            self.birds = []
        self.pipes = deque([Pipe(WIN_WIDTH)])  # Start with one pipe for simplicity
        self.floor = Floor(WIN_HEIGHT - FLOOR_IMAGE.get_height())
        self.background = Background()
        self.score = State("score", 0)
        
        
        if (self.mode == "TRAIN"):
            self.generation = State("generation", 0)
            self.fitness = State("fitness")
            
            
        self.renderer = Renderer()  # Create an instance of our Renderer class
        self.clock = pygame.time.Clock()
        
        self.previous_time = pygame.time.get_ticks()
        
    def reset(self):
        self.birds = []
        self.pipes = deque([Pipe(WIN_WIDTH)])   # Start with one pipe for simplicity
        self.score.reset()
        self.previous_time = pygame.time.get_ticks()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over()
            
            if (self.mode == "HUMAN"):
                is_mouse_click = event.type == pygame.MOUSEBUTTONDOWN
                is_space_press = event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE

                if is_mouse_click or is_space_press:
                    for bird in self.birds:
                        bird.jump()

                is_escape_press = event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                
                if is_escape_press:
                    self.game_over()
                
    def game_over(self):
        pygame.quit()
        exit()

    def update_game_state_human(self):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.previous_time) / 1000.0  # Convert to seconds

        for bird in self.birds:
            bird.move(delta_time)
            for pipe in self.pipes:
                if CollisionManager.check_pipe_collision(bird, pipe):
                    self.birds.remove(bird)
                    
            if CollisionManager.check_floor_collision(bird, self.floor):
                self.birds.remove(bird)
                
            if len(self.birds) == 0:
                self.game_over()

        # Update pipe positions and add new pipes or remove off-screen pipes
        for pipe in list(self.pipes):
            pipe.move(delta_time)
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                self.pipes.popleft()  # Remove the leftmost pipe
            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                self.score.increase()
        
        # 判断是否应该添加新的管道
        if random.uniform(0, 1) < 0.05:
            if len(self.pipes) == 0 or (self.pipes[-1].x <= WIN_WIDTH - 300):  # Check the position of the last pipe
                self.pipes.append(Pipe(WIN_WIDTH))  # Add a new pipe to the right end

        # Move the floor and the background
        self.floor.move(delta_time)
        self.background.move(delta_time)
        
        self.previous_time = current_time

    def render(self):
        self.renderer.draw_background(self.background)
        
        for pipe in self.pipes:
            self.renderer.draw_pipe(pipe)
            
        self.renderer.draw_floor(self.floor)
        
        for bird in self.birds:
            self.renderer.draw_bird(bird)
            self.renderer.draw_bird_trace(bird, self.pipes)
        
        self.renderer.draw_state(self.score)
        if (self.mode == "TRAIN"):
            self.renderer.draw_state(self.generation)
            self.renderer.draw_state(self.fitness)
        
        pygame.display.update()

    def run_human(self):
        while True:
            self.handle_events()
            self.update_game_state_human()
            self.render()
            self.clock.tick(60)
    
    def update_game_state_train(self, nets, generation):
        current_time = pygame.time.get_ticks()
        delta_time = (current_time - self.previous_time) / 1000.0  # Convert to seconds

        for bird_index, bird in enumerate(self.birds):
            generation[bird_index].fitness += FITNESS_LIVE
            self.fitness.increase(FITNESS_LIVE)
                    
            # send bird location, top pipe location and bottom pipe location and determine from network whether to jump or not
            output = nets[self.birds.index(bird)].activate((bird.y, 
                                                            int(bird.y - self.pipes[0].height) if len(self.pipes) > 0 else 300,
                                                            int(bird.y - self.pipes[0].bottom) if len(self.pipes) > 0 else -300,
                                                            int(bird.y - self.pipes[1].height) if len(self.pipes) > 1 else 300, 
                                                            int(bird.y - self.pipes[1].bottom) if len(self.pipes) > 1 else -300,
                                                            int(self.pipes[0].x - bird.x) if len(self.pipes) > 0 else 300,
                                                            int(self.pipes[1].x - bird.x) if len(self.pipes) > 1 else 300,
                                                            int(self.pipes[0].center - self.pipes[1].center) if len(self.pipes) > 2 else 0))
                
            if output[0] > 0.9:  # we use a tanh activation function so result will be between -1 and 1. if over 0.5 jump
                bird.jump()
                
            bird.move(delta_time)
            for pipe in self.pipes:
                if CollisionManager.check_pipe_collision(bird, pipe):
                    try:
                        self.birds.remove(bird)
                    except ValueError:
                        continue
                    nets.pop(bird_index)
                    generation[bird_index].fitness -= FITNESS_PIPE
                    generation.pop(bird_index)
                    self.fitness.decrease(FITNESS_PIPE)
                    
                    
            if CollisionManager.check_floor_collision(bird, self.floor):
                try:
                    self.birds.remove(bird)
                except ValueError:
                    continue
                nets.pop(bird_index)
                generation[bird_index].fitness -= FITNESS_FLOOR
                generation.pop(bird_index)
                self.fitness.decrease(FITNESS_FLOOR)

        # Update pipe positions and add new pipes or remove off-screen pipes
        for pipe in list(self.pipes):
            pipe.move(delta_time)
            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                self.pipes.popleft()
            if not pipe.passed and pipe.x < bird.x and len(self.pipes) > 1:
                pipe.passed = True
                self.score.increase()
                for genome in generation:
                    genome.fitness += FITNESS_PASS
                    self.fitness.increase(FITNESS_PASS)
        
        # 判断是否应该添加新的管道
        if random.uniform(0, 1) < 0.05 or len(self.pipes) < 2:  
            # 检查最后一个管道的位置
            if (self.pipes[-1].x <= WIN_WIDTH - 350):
                self.pipes.append(Pipe(WIN_WIDTH))

        # Move the floor and the background
        self.floor.move(delta_time)
        self.background.move(delta_time)
        
        self.previous_time = current_time
               
    def run_train(self):        
        training_config_file = file_path("TRAINING_CONFIG")
        config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         training_config_file)

        # 1. 在训练开始时加载模型（如果存在）
        if os.path.exists("model/checkpoint"):
            print("Model loaded from checkpoint")
            
            population = neat.Checkpointer.restore_checkpoint("model/checkpoint")
        elif os.path.exists("model/best_51.pkl"):
            print("Model loaded from best_1.pkl")
            with open("model/best_1.pkl", "rb") as f:
                population = pickle.load(f)
        else:
            print("Model not loaded, creating new population")
            population = neat.Population(config)
            
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        # 添加一个CheckpointReporter，使其每经过5代保存一次状态
        population.add_reporter(neat.Checkpointer(5, filename_prefix='model/checkpoint'))
      
        winner = population.run(self.eval_genomes, 10000)
        
        # Here, you can save the winner network or do other post-training tasks
        with open("model/best_1.pkl", "wb") as f:
            pickle.dump(population, f)
            
        return winner
    
    def eval_genomes(self, genomes, config):
        
        self.generation.increase()

        nets = []
        generation = []
        
        for genome_id, genome in genomes:
            genome.fitness = 0  # start with fitness level of 0
            net = neat.nn.FeedForwardNetwork.create(genome, config)
            nets.append(net)
            self.birds.append(Bird((WIN_HEIGHT - FLOOR_IMAGE.get_height()) // 2))
            generation.append(genome)

        self.fitness.set_number(genome.fitness)
        
        while len(self.birds) > 0:
            self.handle_events()
            self.update_game_state_train(nets, generation)
            self.render()
            self.clock.tick(60)
            
        self.reset()

    def run_model(self):
        model_path = file_path("MODEL")
