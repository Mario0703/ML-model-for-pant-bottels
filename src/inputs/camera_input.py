import cv2
from ..YOLO_model.predict import PantBottlePredictor


class CameraInput:
    def __init__(self, camera_index=0):
        self.camera = cv2.VideoCapture(camera_index)
        self.frame = None
        self.predictor = PantBottlePredictor()

        if not self.camera.isOpened():
            raise RuntimeError("Camera could not be opened")

    def get_video_frame(self):
        ret, self.frame = self.camera.read()

        if not ret:
            return None

        return self.frame

    def predict_image(self, frame=None, certainty=0.5):
        if frame is None:
            frame = self.frame

        return self.predictor.predict_image(frame, certainty)

    def release(self):
        self.camera.release()
