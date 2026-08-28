import cv2
from ..YOLO_model.predict import PantBottlePredictor


class CameraInput:
    def __init__(self, camera_index=0):
        self.cam = cv2.VideoCapture(camera_index)
        self.frame = None
        self.predictor = PantBottlePredictor()

        if not self.cam.isOpened():
            raise RuntimeError("Camera could not be opened")

    def get_video_frame(self):
        ret, self.frame = self.cam.read()

        if not ret:
            return None

        return self.frame

    def predict_image(self, frame=None, certainty=0.5):
        """Predict a frame and return a GUI-ready label string."""
        frame = frame if frame is not None else self.frame

        if frame is None:
            return "No frame available"

        return self.predictor.predict_image(frame, certainty)

    def release(self):
        self.cam.release()
