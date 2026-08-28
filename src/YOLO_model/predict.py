from pathlib import Path

from ultralytics import YOLO

project_root = Path(__file__).resolve().parents[2]

model_path = (
    project_root
    / "runs"
    / "classify"
    / "pant_classifier-2"
    / "weights"
    / "best.pt"
)

image_path = project_root / "src" / "user_loaded_image" / "image.png"

model = YOLO(model_path)
result = model(image_path)[0]

class_id = result.probs.top1
confidence = float(result.probs.top1conf)
label = result.names[class_id]

print(f"Prediction: {label}")
print(f"Confidence: {confidence:.1%}")