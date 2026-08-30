"""Filesystem paths used by the local application and training tools."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TRAINING_DATA_DIRECTORY = PROJECT_ROOT / "TraningData"
USER_IMAGE_DIRECTORY = PROJECT_ROOT / "user_loaded_images"
DEFAULT_MODEL_PATH = (
    PROJECT_ROOT
    / "runs"
    / "classify"
    / "pant_classifier-2"
    / "weights"
    / "best.pt"
)
