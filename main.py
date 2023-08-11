from config.config_loader import HUMAN_TRAIN_MODEL_MODE
from game.game_controller import GameController
import argparse

# 自定义的模式类型函数，将输入转换为大写并验证是否有效
# Custom mode type function, converting input to uppercase and validating if it's valid
def mode_type(value):
    value_upper = value.upper()
    if value_upper not in ['HUMAN', 'TRAIN', 'MODEL']:
        raise argparse.ArgumentTypeError('Invalid mode selected. Choose "HUMAN", "TRAIN", or "MODEL".')
    return value_upper

# 主函数，根据输入的模式执行相应的逻辑
# Main function, executing the corresponding logic based on the input mode
def main(mode=None):
    # 如果模式未提供，则解析命令行参数
    # If mode is not provided, parse command-line arguments
    if mode is None:
        parser = argparse.ArgumentParser(description='Flappy Bird mode selection.')
        parser.add_argument('--mode', type=mode_type, choices=['HUMAN', 'TRAIN', 'MODEL'], default=HUMAN_TRAIN_MODEL_MODE,
                            help='Select the running mode: HUMAN, TRAIN or MODEL.')
        args = parser.parse_args()
        mode = args.mode
        
    # 验证模式是否有效
    # Validate if the mode is valid
    elif mode not in ['HUMAN', 'TRAIN', 'MODEL']:
        raise ValueError('Invalid mode selected. Choose "HUMAN", "TRAIN" or "MODEL".')
    
    # 根据选定的模式执行逻辑
    # Execute logic based on the selected mode
    if mode == "HUMAN":
        print("Human mode selected.")
        GameController("HUMAN").run_human()
    elif mode == "TRAIN":
        print("Training mode selected.")
        GameController("TRAIN").run_train()
    else:
        print("Model mode selected.")
        GameController("MODEL").run_model()

# 程序入口点
# Program entry point
if __name__ == '__main__':
    # main(None)
    # main("HUMAN")
    main("TRAIN")
    # main("MODEL")
