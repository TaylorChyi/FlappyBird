import os
from services.config_loader import FILE_PATH

def file_path(filename):
    """
    :return: the path of the current file
    """
    root_dir = os.path.dirname(os.path.dirname(__file__))
    return os.path.join(root_dir, FILE_PATH[filename]["FOLDER"], FILE_PATH[filename]["FILENAME"])
    