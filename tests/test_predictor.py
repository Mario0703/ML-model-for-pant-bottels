from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import MagicMock, patch

from pant_bottle_classifier.model.predict import PantBottlePredictor


class PantBottlePredictorTests(unittest.TestCase):
    @patch("pant_bottle_classifier.model.predict.YOLO")
    def test_prediction_returns_label_and_confidence(self, yolo_class):
        result = MagicMock()
        result.probs.top1 = 1
        result.probs.top1conf = 0.75
        result.names = {1: "Pant_b"}
        yolo_class.return_value.return_value = [result]

        with TemporaryDirectory() as temporary_directory:
            model_path = Path(temporary_directory) / "model.pt"
            model_path.touch()
            predictor = PantBottlePredictor(model_path=model_path)

            self.assertEqual(predictor.predict_image(object()), "Pant_b")
            self.assertEqual(
                predictor.prediction(),
                {"label": "Pant_b", "confidence": 0.75, "class_id": 1},
            )
            self.assertEqual(
                predictor.predict_image(object(), certainty=0.8),
                "Uncertain",
            )

    def test_missing_model_is_rejected(self):
        with TemporaryDirectory() as temporary_directory:
            missing_model = Path(temporary_directory) / "missing.pt"

            with self.assertRaisesRegex(FileNotFoundError, "Model not found"):
                PantBottlePredictor(model_path=missing_model)


if __name__ == "__main__":
    unittest.main()
