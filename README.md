# Danish Pant Bottle Classifier

This project explores how machine learning can be used to recognise Danish
pant bottles. A YOLO classification model is trained on labelled bottle
images and used through a simple desktop application. The application can
analyse a saved image or make predictions from a webcam.

The aim is to experiment with the complete machine-learning workflow: using a
dataset, training a model, evaluating predictions, and connecting the model to
a user interface.

## What the project can do

- Classify an image into one of the available labels:
  `no_pant`, `Pant_a`, `Pant_b`, `Pant_c`, or `pant_not_visible`.
- Let the user select an image and display the predicted category and
  confidence score.
- Read frames from a webcam and show a live prediction when the model is
  sufficiently confident.
- Return `Uncertain` when the prediction does not reach the configured
  confidence threshold.
- Train a YOLO classification model using the images in `TraningData`.

## Learning goals

By working on this project, you can practise:

- organising images into class-based folders for supervised learning;
- preparing and splitting image data into training and validation sets;
- training an image-classification model with Ultralytics YOLO;
- understanding confidence scores and uncertainty in model predictions;
- using Python, OpenCV, and PyQt6 to build a machine-learning application;
- integrating a trained model into both file-based and live-camera input;
- identifying how dataset quality affects real-world model performance.

## Dataset

The current dataset is organised into these classes:

```text
TraningData/
├── no_pant/
├── Pant_a/
├── Pant_b/
├── Pant_c/
└── pant_not_visible/
```

The dataset is intentionally a small learning dataset. It contains only a
limited number of examples for `no_pant` and the `Pant_*` classes, while
`pant_not_visible` has considerably more images. This imbalance and the
limited variation in bottle shape, angle, lighting, background, and camera
distance affect what the model can learn.

## Webcam limitation

The webcam feature is included as a demonstration of live inference, but it
should not be treated as a reliable production scanner. The model can only
recognise visual patterns represented in the current dataset. A webcam image
may look very different from the training images because of lighting,
reflections, rotation, distance, background, or partial visibility. As a
result, live predictions may be incorrect or frequently be reported as
`Uncertain`.

Improving webcam performance would require a larger and more balanced
dataset containing real webcam-style images, more bottle examples, and a
broader range of environments and viewpoints.

## Running the application

Install the project dependencies in a Python environment, then run:

```bash
python main.py
```

The application provides options for selecting an image and for opening the
webcam. A trained model is expected at:

```text
runs/classify/pant_classifier-2/weights/best.pt
```

## Training the model

To train the classifier again using the dataset in `TraningData`, run:

```bash
python src/YOLO_model/train.py
```

The training script uses the YOLO classification model, 30 epochs, an image
size of 224 pixels, a batch size of 8, and CPU training. Training creates a
new run under `runs/classify/`.

## Project structure

```text
main.py                      Start the desktop application
src/gui/                     PyQt6 user interface
src/inputs/                  Image and webcam input handling
src/YOLO_model/train.py      Model training script
src/YOLO_model/predict.py    Prediction and confidence handling
scripts/                     Dataset preparation utilities
TraningData/                 Training images organised by class
runs/                        Training outputs and model weights
```

## Project status

This is an educational prototype rather than a finished recycling or pant-
return solution. Its main value is demonstrating how a trained computer
vision model can be connected to an interactive application, while making the
limitations of a small dataset visible.
