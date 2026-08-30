from pathlib import Path

from ultralytics import YOLO

from ..paths import DEFAULT_MODEL_PATH


class PantBottlePredictor:
    """Classify one arbitrary image using the trained pant-bottle model."""

    def __init__(self, image_path=None, model_path=None):
        self.model_path = Path(model_path) if model_path else self._default_model_path()
        if not self.model_path.is_file():
            raise FileNotFoundError(f"Model not found: {self.model_path}")

        self.model = YOLO(self.model_path)
        self.result = None
        self.image_path = None

        if image_path is not None:
            self.predict_image(image_path)

    def predict_image(self, image, certainty=0.5):
        """Return the predicted label when confidence reaches ``certainty``."""
        if not 0 <= certainty <= 1:
            raise ValueError("certainty must be between 0 and 1")

        if isinstance(image, (str, Path)):
            image = Path(image)
            if not image.is_file():
                raise FileNotFoundError(f"Image not found: {image}")
            self.image_path = image
        else:
            self.image_path = None

        self.result = self.model(image)[0]

        self.class_id = self.result.probs.top1
        self.confidence = float(self.result.probs.top1conf)
        self.label = str(self.result.names[self.class_id])

        return self.label if self.confidence >= certainty else "Uncertain"

    def _default_model_path(self):
        return DEFAULT_MODEL_PATH

    def prediction(self):
        """Return the prediction in a convenient dictionary."""
        if self.result is None:
            return None

        return {
            "label": self.label,
            "confidence": self.confidence,
            "class_id": self.class_id,
        }
