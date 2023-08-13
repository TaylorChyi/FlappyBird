import pygame
import json
import os

# 从配置文件中加载参数
def load_config():
    config_path = os.path.join(os.path.dirname(__file__), 'config.json')
    with open(config_path, 'r') as file:
        config = json.load(file)
        
    return config

CONFIG = load_config()

# 加载配置
WINDOW = CONFIG['WINDOW']
FONT = CONFIG['FONT']
RESOURCE = CONFIG['RESOURCE']

DRAW_LINES = CONFIG['DRAW_LINES']
HUMAN_TRAIN_MODEL_MODE = CONFIG['HUMAN_TRAIN_MODEL_MODE']

# 设置窗口
WIN_WIDTH = WINDOW['WIN_WIDTH']
WIN_HEIGHT = WINDOW['WIN_HEIGHT']
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption(WINDOW['CAPTION'])

# 设置字体
pygame.font.init()
STAT_FONT = pygame.font.SysFont(FONT['STATE']['NAME'], FONT['STATE']['SIZE'])
END_FONT = pygame.font.SysFont(FONT['END']['NAME'], FONT['END']['SIZE'])

# 加载资源
BACKGROUND_IMAGE = pygame.transform.scale(pygame.image.load(os.path.join(RESOURCE['ROOT'], RESOURCE['BACKGROUND']['IMAGE'])).convert_alpha(), (600, 900))
FLOOR_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(RESOURCE['ROOT'], RESOURCE['FLOOR'])).convert_alpha())
BIRDS_IMAGE = [pygame.transform.scale2x(pygame.image.load(os.path.join(RESOURCE['ROOT'], img))) for img in RESOURCE['BIRDS']]
PIPE_IMAGE = pygame.transform.scale2x(pygame.image.load(os.path.join(RESOURCE['ROOT'], RESOURCE['PIPE'])).convert_alpha())

# 文件名
FILE_PATH = CONFIG['FILE_PATH']

# Background
BACKGROUND_VELOCITY = RESOURCE['BACKGROUND']['VELOCITY']

# ORIGIN POINT
ORIGIN_POINT_X = CONFIG['ORIGIN_POINT']['X']
ORIGIN_POINT_Y = CONFIG['ORIGIN_POINT']['Y']

# FITNESS SCORE
FITNESS_LIVE = CONFIG['FITNESS']['LIVE']
FITNESS_FLOOR = CONFIG['FITNESS']['FLOOR']
FITNESS_PIPE = CONFIG['FITNESS']['PIPE']
FITNESS_PASS = CONFIG['FITNESS']['PASS']
