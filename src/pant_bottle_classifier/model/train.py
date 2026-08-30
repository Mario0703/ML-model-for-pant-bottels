"""Train the pant-bottle image classifier."""

from ultralytics import YOLO

from ..paths import TRAINING_DATA_DIRECTORY


def main() -> None:
    """Train the classifier using the repository's training dataset."""
    model = YOLO("yolo26n-cls.pt")
    model.train(
        data=str(TRAINING_DATA_DIRECTORY),
        epochs=30,
        imgsz=224,
        batch=8,
        device="cpu",
        name="pant_classifier",
    )


if __name__ == "__main__":
    main()
