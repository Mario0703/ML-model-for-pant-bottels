import sys

import cv2
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from ..inputs.camera_input import CameraInput
from ..inputs.image_input import UserImageLoader
from ..model.predict import PantBottlePredictor


class PantBottleRecognitionWindow(QWidget):
    """Main application window for selecting a bottle image or camera input."""

    def __init__(self):
        super().__init__()
        width, height = 800, 600

        self.setWindowTitle("Pant Bottle Recognition")
        self.resize(width, height)
        self.image_loader = UserImageLoader()
        self.saved_image_path = None
        self.user_loaded_image = None
        self.camera = CameraInput()

        self.stacked_layout = QStackedLayout()
        self._create_main_menu()
        self._create_image_menu()
        self._create_image_list_menu()
        self._create_camera_menu()
        self._create_predict_bottle_menu()

        self.stacked_layout.addWidget(self.main_menu)
        self.stacked_layout.addWidget(self.image_menu)
        self.stacked_layout.addWidget(self.image_list_menu)
        self.stacked_layout.addWidget(self.camera_menu)
        self.stacked_layout.addWidget(self.show_and_predict_image_menu)
        self.setLayout(self.stacked_layout)

    def _create_main_menu(self):
        """Build the application's main menu page."""
        self.main_menu = QWidget()
        main_layout = QVBoxLayout(self.main_menu)

        title = QLabel("Pant Bottle Recognition")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.bottle_image_button = QPushButton("Import image of a bottle")
        self.list_images_button = QPushButton("List loaded images")
        self.bottle_camera_button = QPushButton(
            "Use the camera to determine if a bottle has pant"
        )

        main_layout.addWidget(title)
        main_layout.addStretch()
        main_layout.addWidget(
            self.bottle_image_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        main_layout.addWidget(
            self.list_images_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        main_layout.addWidget(
            self.bottle_camera_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        self.bottle_image_button.clicked.connect(self.show_image_menu)
        self.list_images_button.clicked.connect(self.show_image_list_menu)
        self.bottle_camera_button.clicked.connect(self.show_camera_menu)

    def _create_image_menu(self):
        """Build the image-selection page."""
        self.image_menu = QWidget()
        image_layout = QVBoxLayout(self.image_menu)

        image_title = QLabel("Import a bottle image")
        image_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        image_title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.image_path_input = QLineEdit()
        self.image_path_input.setPlaceholderText("Enter or select the path to an image")
        self.image_path_input.setFixedWidth(400)

        self.select_image_button = QPushButton("Select image")
        self.load_image_button = QPushButton("Load image")
        self.back_button = QPushButton("Back")
        self.load_status = QLabel()
        self.load_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_layout.addWidget(image_title)
        image_layout.addStretch()
        image_layout.addWidget(
            self.image_path_input,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        image_layout.addWidget(
            self.select_image_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        image_layout.addWidget(
            self.load_image_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        image_layout.addWidget(self.load_status)
        image_layout.addWidget(
            self.back_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        self.select_image_button.clicked.connect(self.select_image)
        self.load_image_button.clicked.connect(self.load_image_into_directory)
        self.back_button.clicked.connect(self.show_main_menu)

    def _create_image_list_menu(self):
        """Build the page showing saved images in a two-column grid."""
        self.image_list_menu = QWidget()
        layout = QVBoxLayout(self.image_list_menu)

        title = QLabel("Loaded images")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.image_grid_container = QWidget()
        self.image_grid = QGridLayout(self.image_grid_container)
        self.image_grid.setSpacing(16)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(self.image_grid_container)

        back_button = QPushButton("Back")
        back_button.clicked.connect(self.show_main_menu)

        layout.addWidget(title)
        layout.addWidget(scroll_area)
        layout.addWidget(back_button, alignment=Qt.AlignmentFlag.AlignHCenter)

    def _create_camera_menu(self):
        """Build the camera page. Frames come from CameraInput."""
        self.camera_menu = QWidget()
        layout = QVBoxLayout(self.camera_menu)

        self.camera_output = QLabel("Camera is not running")
        self.camera_output.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_output.setMinimumSize(640, 480)

        self.camera_prediction = QLabel("Prediction: waiting for camera")
        self.camera_prediction.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.camera_prediction.setStyleSheet("font-size: 20px; font-weight: bold;")

        self.camera_back_button = QPushButton("Exit camera")
        self.camera_back_button.clicked.connect(self.close_camera)

        layout.addWidget(self.camera_output)
        layout.addWidget(self.camera_prediction)
        layout.addWidget(
            self.camera_back_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        self.camera_timer = QTimer(self)
        self.camera_timer.timeout.connect(self._update_camera_output)

    def _update_camera_output(self):
        frame = self.camera.get_video_frame()
        if frame is None:
            self.camera_prediction.setText("Prediction: no camera frame")
            return

        prediction = self.camera.predict_image(frame, certainty=0.95)
        self.camera_prediction.setText(f"Prediction: {prediction}")

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channels = frame_rgb.shape
        bytes_per_line = channels * width

        image = QImage(
            frame_rgb.data,
            width,
            height,
            bytes_per_line,
            QImage.Format.Format_RGB888,
        ).copy()

        self.camera_output.setPixmap(
            QPixmap.fromImage(image).scaled(
                self.camera_output.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
        )

    def _create_predict_bottle_menu(self):
        self.show_and_predict_image_menu = QWidget()
        layout = QVBoxLayout(self.show_and_predict_image_menu)

        title = QLabel("Bottle prediction")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.loaded_image_label = QLabel("No image loaded")
        self.loaded_image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loaded_image_label.setFixedSize(500, 400)

        self.predict_button = QPushButton("Predict bottle")
        self.predict_back_button = QPushButton("Back")
        self.prediction_result_label = QLabel("Prediction not run")
        self.prediction_result_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.prediction_result_label.setStyleSheet(
            "font-size: 18px; font-weight: bold;"
        )

        layout.addWidget(title)
        layout.addWidget(
            self.loaded_image_label,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        layout.addWidget(
            self.predict_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )
        layout.addWidget(self.prediction_result_label)
        layout.addWidget(
            self.predict_back_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        self.predict_button.clicked.connect(self.predict_loaded_image)
        self.predict_back_button.clicked.connect(self.show_image_list_menu)

    def select_image(self):
        """Prompt for an image file and display its path in the input field."""
        image_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select a bottle image",
            "",
            "Image files (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if image_path:
            self.image_path_input.setText(image_path)

    def load_image_into_directory(self):

        image_path = self.get_image_path().strip()
        if not image_path:
            self.load_status.setText("Select an image first.")
            return

        try:
            self.saved_image_path, self.user_loaded_image = (
                self.image_loader.copy_and_load(image_path)
            )
        except (FileNotFoundError, OSError) as error:
            self.load_status.setText(f"Could not load image: {error}")
            return

        self.load_status.setText(f"Image loaded: {self.saved_image_path.name}")

    def show_image_list_menu(self):
        """Refresh the saved-image grid and display it."""
        self._clear_image_grid()

        image_extensions = {".png", ".jpg", ".jpeg", ".bmp", ".webp"}
        image_paths = []
        
        for path in self.image_loader.destination_directory.iterdir():
            if path.is_file() and path.suffix.lower() in image_extensions:
                image_paths.append(path)

        image_paths.sort()

        if not image_paths:
            self.image_grid.addWidget(QLabel("No images have been loaded yet."), 0, 0)
        else:
            for index, image_path in enumerate(image_paths):
                self._add_image_card(image_path, index)

        self.stacked_layout.setCurrentWidget(self.image_list_menu)

    def _clear_image_grid(self):
        while self.image_grid.count():
            item = self.image_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def _add_image_card(self, image_path, index):
        """Add an image name and its Predict button to one grid cell."""
        card = QWidget()
        card_layout = QVBoxLayout(card)

        image_name = QLabel(image_path.name)
        image_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        predict_button = QPushButton("Predict")
        predict_button.clicked.connect(
            lambda _=False, path=image_path: self.show_predict_bottle_menu(path)
        )

        card_layout.addWidget(image_name)
        card_layout.addWidget(predict_button)
        self.image_grid.addWidget(card, index // 2, index % 2)

    def get_image_path(self):
        """Return the image path currently entered by the user."""
        return self.image_path_input.text()

    def show_main_menu(self):
        self.stacked_layout.setCurrentWidget(self.main_menu)

    def show_image_menu(self):
        self.stacked_layout.setCurrentWidget(self.image_menu)

    def show_camera_menu(self):
        self.stacked_layout.setCurrentWidget(self.camera_menu)
        self.camera_timer.start(30)

    # Keep the old spelling working if it is used elsewhere in the project.
    def show_camerea_menu(self):
        self.show_camera_menu()

    def close_camera(self):
        self.camera_timer.stop()
        self.camera_output.clear()
        self.camera_output.setText("Camera is closed")
        self.show_main_menu()

    def closeEvent(self, event):
        self.camera_timer.stop()
        self.camera.release()
        event.accept()

    def keyPressEvent(self, event):
        if self.stacked_layout.currentWidget() == self.camera_menu and event.key() in (
            Qt.Key.Key_Escape,
            Qt.Key.Key_Q,
        ):
            self.close_camera()
            return

        super().keyPressEvent(event)

    def show_predict_bottle_menu(self, image_path=None):
        if image_path is not None:
            try:
                self.saved_image_path = image_path
                self.user_loaded_image = self.image_loader.load_user_file(image_path)
            except (FileNotFoundError, OSError) as error:
                self.load_status.setText(f"Could not load image: {error}")
                return

        if self.saved_image_path is None:
            self.load_status.setText("Load an image first.")
            return

        pixmap = QPixmap(str(self.saved_image_path))
        if pixmap.isNull():
            self.loaded_image_label.setText("Could not display this image.")
        else:
            self.loaded_image_label.setPixmap(
                pixmap.scaled(
                    self.loaded_image_label.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
            )
        self.prediction_result_label.setText("Prediction not run")
        self.stacked_layout.setCurrentWidget(self.show_and_predict_image_menu)

    def predict_loaded_image(self):

        if self.saved_image_path is None:
            self.prediction_result_label.setText("No image selected")
            return
        try:
            predictor = PantBottlePredictor(self.saved_image_path)
        except (FileNotFoundError, OSError, ValueError) as error:
            self.prediction_result_label.setText(f"Prediction failed: {error}")
            return

        self.prediction_result_label.setText(
            f"Category: {predictor.label}\n"
            f"Confidence: {predictor.confidence * 100:.2f}%"
        )


def run_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    window = PantBottleRecognitionWindow()
    window.show()

    return app.exec()
