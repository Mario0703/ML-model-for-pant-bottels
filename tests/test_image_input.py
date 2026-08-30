from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from PIL import Image

from pant_bottle_classifier.inputs.image_input import UserImageLoader


class UserImageLoaderTests(unittest.TestCase):
    def test_copy_and_load_creates_destination_directory(self):
        with TemporaryDirectory() as temporary_directory:
            temporary_path = Path(temporary_directory)
            source = temporary_path / "source.png"
            destination_directory = temporary_path / "loaded"
            Image.new("RGB", (2, 3), color="red").save(source)

            loader = UserImageLoader(destination_directory)
            destination, pixels = loader.copy_and_load(source)

            self.assertEqual(destination, destination_directory / source.name)
            self.assertTrue(destination.is_file())
            self.assertEqual(pixels.shape[:2], (3, 2))

    def test_load_user_file_rejects_missing_file(self):
        with TemporaryDirectory() as temporary_directory:
            missing_file = Path(temporary_directory) / "missing.png"
            loader = UserImageLoader()

            with self.assertRaisesRegex(FileNotFoundError, "Image file not found"):
                loader.load_user_file(missing_file)


if __name__ == "__main__":
    unittest.main()
