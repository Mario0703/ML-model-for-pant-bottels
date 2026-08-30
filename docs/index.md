# Danish Pant Bottle Classifier

The application uses an Ultralytics YOLO classification model to identify
Danish pant categories from image files or webcam frames. See the project
[README](../README.md) for installation and usage instructions.

## Architecture

- `pant_bottle_classifier.gui` contains the PyQt6 desktop interface.
- `pant_bottle_classifier.inputs` handles saved images and webcam frames.
- `pant_bottle_classifier.model` contains inference and training code.
- `pant_bottle_classifier.paths` defines paths to local data and model files.

Training data and generated weights intentionally remain outside the Python
package because they are local, potentially large artifacts rather than
importable application code.
