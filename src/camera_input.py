import cv2


class CameraInput:
    def __init__(self, camera_index=0):
        self.cam = cv2.VideoCapture(camera_index, cv2.CAP_DSHOW)

        if not self.cam.isOpened():
            raise RuntimeError("Camera could not be opened")

    def get_video_frame(self):
        ret, frame = self.cam.read()

        if not ret:
            return None

        return frame

    def release(self):
        self.cam.release()
