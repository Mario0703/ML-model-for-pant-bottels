"""Convert and consistently name the project's training images.

Run this script from the repository root. It converts every supported image in
TraningData/<category>/ to JPEG and names it bottleNNN_<category>.jpeg.
"""

from pathlib import Path
import shutil

from PIL import Image

try:
    import pillow_avif  # noqa: F401  # Registers AVIF support with Pillow.
except ImportError as error:
    raise SystemExit(
        "AVIF support is required. Install it with: "
        "python -m pip install Pillow pillow-avif-plugin"
    ) from error


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATASET_ROOT = PROJECT_ROOT / "TraningData"
CATEGORIES = ("no_pant", "Pant_a", "Pant_b", "Pant_c", "pant_not_visible")
IMAGE_EXTENSIONS = {".avif", ".jpeg", ".jpg", ".png", ".webp"}
STAGING_DIRECTORY = PROJECT_ROOT / ".training_image_staging"


def convert_to_jpeg(source: Path, destination: Path) -> None:
    """Convert one image to an RGB JPEG, using white behind transparent pixels."""
    with Image.open(source) as image:
        if image.mode in {"RGBA", "LA"} or "transparency" in image.info:
            rgba_image = image.convert("RGBA")
            background = Image.new("RGB", rgba_image.size, "white")
            background.paste(rgba_image, mask=rgba_image.getchannel("A"))
            image = background
        else:
            image = image.convert("RGB")

        image.save(destination, format="JPEG", quality=95)


def main() -> None:
    if not DATASET_ROOT.is_dir():
        raise SystemExit(f"Training-data directory not found: {DATASET_ROOT}")
    if STAGING_DIRECTORY.exists():
        raise SystemExit(
            f"Staging directory already exists: {STAGING_DIRECTORY}. "
            "Remove it only after checking its contents."
        )

    planned_files = []
    for category in CATEGORIES:
        category_directory = DATASET_ROOT / category
        if not category_directory.is_dir():
            raise SystemExit(f"Category directory not found: {category_directory}")

        source_files = sorted(
            (
                path
                for path in category_directory.iterdir()
                if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
            ),
            key=lambda path: path.name.lower(),
        )
        label = category.lower()

        for index, source in enumerate(source_files, start=1):
            destination = category_directory / f"bottle{index:03d}_{label}.jpeg"
            if destination.exists() and destination != source:
                raise SystemExit(
                    f"Refusing to overwrite an existing file: {destination}"
                )
            planned_files.append((source, destination, label, index))

    STAGING_DIRECTORY.mkdir()
    try:
        for source, _, label, index in planned_files:
            staging_file = STAGING_DIRECTORY / f"{label}_{index:03d}.jpeg"
            convert_to_jpeg(source, staging_file)

        for source, destination, label, index in planned_files:
            staging_file = STAGING_DIRECTORY / f"{label}_{index:03d}.jpeg"
            staging_file.replace(destination)
            source.unlink()
    finally:
        if STAGING_DIRECTORY.exists():
            shutil.rmtree(STAGING_DIRECTORY)

    print(f"Converted and renamed {len(planned_files)} images.")


if __name__ == "__main__":
    main()
