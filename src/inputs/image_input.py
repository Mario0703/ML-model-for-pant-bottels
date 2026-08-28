from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


class UserImageLoader:
    """Save user-selected images locally and load them as NumPy arrays."""

    def __init__(self, destination_directory=None):
        default_directory = Path(__file__).resolve().parents[1] / "user_loaded_image"
        self.destination_directory = Path(destination_directory or default_directory)

    def copy_and_load(self, image_path):

        source = Path(image_path)
        destination = self.destination_directory / source.name
        
        if not source.is_file():
            raise FileNotFoundError(f"Image file not found: {source}")

        with Image.open(source) as image:
            image.save(destination)

        return destination, self.load_user_file(destination)

    def load_user_file(self, image_path):
        source = Path(image_path)
        
        if not source.is_file():
            raise FileNotFoundError(f"Image file not found: {source}")
        
        return plt.imread(source)
