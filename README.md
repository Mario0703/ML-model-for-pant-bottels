# Danish Pant Bottle Classifier

This educational project trains an Ultralytics YOLO classification model to
recognise Danish pant bottles and exposes it through a PyQt6 desktop
application. The app can classify a saved image or show live predictions from
a webcam.

## Features

- Classifies images as `no_pant`, `Pant_a`, `Pant_b`, `Pant_c`, or
  `pant_not_visible`.
- Displays the predicted category and confidence score.
- Supports saved images and live webcam frames.
- Returns `Uncertain` when a prediction is below the requested confidence.
- Includes a repeatable YOLO training entry point.

## Installation

Python 3.10 or newer is required. Create and activate a virtual environment,
then install the package in editable mode:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
python -m pip install -e .
```

For development tools and AVIF dataset preparation support, install the
optional dependency groups:

```bash
python -m pip install -e ".[dev,data]"
```

## Running the application

From the repository root, run either:

```bash
pant-bottle-classifier
```

or:

```bash
python -m pant_bottle_classifier
```

The trained model is expected at
`runs/classify/pant_classifier-2/weights/best.pt`.

## Training

Place class-based image folders under `TraningData/`, then run:

```bash
pant-bottle-train
```

The training command uses 30 epochs, 224-pixel images, a batch size of 8, and
CPU training. Ultralytics writes generated runs beneath `runs/classify/`.

To convert and consistently rename source images before training, use:

```bash
python scripts/prepare_training_images.py
```

## Tests

After installing the development dependencies, run:

```bash
pytest
```

The tests are also compatible with Python's standard-library runner:

```bash
python -m unittest discover
```

## Project structure

```text
ML-model-for-pant-bottels/
├── src/
│   └── pant_bottle_classifier/
│       ├── __init__.py
│       ├── __main__.py
│       ├── main.py
│       ├── gui/
│       ├── inputs/
│       └── model/
├── tests/
├── docs/
├── scripts/
├── pyproject.toml
├── README.md
└── .gitignore
```

Local datasets, model weights, and training runs are excluded from version
control. They remain at the repository root so that large generated artifacts
do not become part of the importable package.

## Model limitations

This is a small learning dataset, so predictions can be sensitive to lighting,
reflections, rotation, distance, background, and class imbalance. The webcam
mode is a demonstration and should not be treated as a production pant scanner.
Improving it requires more balanced examples captured across a wider range of
bottles, viewpoints, and environments.
