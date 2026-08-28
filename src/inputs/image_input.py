from pathlib import Path

import matplotlib.pyplot as plt
from PIL import Image


class UserImageLoader:
    """Save user-selected images locally and load them as NumPy arrays."""

    def __init__(self, destination_directory=None):
        self.destination_directory = (
            Path(destination_directory)
            if destination_directory
            else Path(__file__).resolve().parents[1] / "user_loaded_image"
        )

    def copy_and_load(self, image_path):
        """Copy an image to the destination folder and return its pixel array."""
        source = Path(image_path)
        if not source.is_file():
            raise FileNotFoundError(f"Image file not found: {source}")

        destination = self.destination_directory / source.name

        with Image.open(source) as image:
            image.save(destination)

        return destination, self.load(destination)

    def load(self, image_path):
        """Return the pixel data for an image already stored on disk."""
        source = Path(image_path)
        if not source.is_file():
            raise FileNotFoundError(f"Image file not found: {source}")

        return plt.imread(source)
