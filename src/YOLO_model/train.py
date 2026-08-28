from pathlib import Path
from ultralytics import YOLO

dataset_path = Path(__file__).resolve().parents[2] / "TraningData"

model = YOLO("yolo26n-cls.pt")

model.train(
    data=str(dataset_path),
    epochs=30,
    imgsz=224,
    batch=8,
    device="cpu",
    name="pant_classifier",
)