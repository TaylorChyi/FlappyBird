from services.config_loader import HUMAN_TRAIN_MODEL_MODE
from game.game_controller import GameController
import argparse

MODES = ['HUMAN', 'TRAIN', 'MODEL']

def parse_arguments():
    """Parse and validate command-line arguments."""
    parser = argparse.ArgumentParser(description="Flappy Bird Game Modes")
    parser.add_argument("--mode", 
                        choices=MODES,
                        type=mode_type, 
                        default=MODES[0],
                        help=f"The game mode: {','.join(MODES)})")
    return parser.parse_args()

def mode_type(mode_str):
    """Validate the mode input."""
    mode_upper_str = mode_str.upper()
    if mode_upper_str not in MODES:
        raise argparse.ArgumentTypeError(f"Mode '{mode_upper_str}' is not valid. Choose from {', '.join(MODES)}")
    return mode_upper_str

def main():
    mode = parse_arguments().mode
    
    print(f"Starting Flappy Bird in {mode} mode...")
    
    controller = GameController(mode)
    
    controller.run()

    print(f"Exiting {mode} mode.")

if __name__ == "__main__":
    main()

