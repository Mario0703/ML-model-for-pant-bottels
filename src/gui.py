import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QApplication,
    QFileDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QStackedLayout,
    QVBoxLayout,
    QWidget,
)
from src.image_input import UserImageLoader


class PantBottleRecognitionWindow(QWidget):
    """Main application window for selecting a bottle image or camera input."""

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pant Bottle Recognition")
        self.resize(800, 600)
        self.image_loader = UserImageLoader()
        self.saved_image_path = None
        self.user_loaded_image = None

        self.stacked_layout = QStackedLayout()
        self._create_main_menu()
        self._create_image_menu()

        self.stacked_layout.addWidget(self.main_menu)
        self.stacked_layout.addWidget(self.image_menu)
        self.setLayout(self.stacked_layout)

    def _create_main_menu(self):
        """Build the application's landing page."""
        self.main_menu = QWidget()
        main_layout = QVBoxLayout(self.main_menu)

        title = QLabel("Pant Bottle Recognition")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold;")

        self.bottle_image_button = QPushButton("Import image of a bottle")
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
            self.bottle_camera_button,
            alignment=Qt.AlignmentFlag.AlignHCenter,
        )

        self.bottle_image_button.clicked.connect(self.show_image_menu)

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
        """Copy the entered image to the project and load its pixel data."""
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

    def get_image_path(self):
        """Return the image path currently entered by the user."""
        return self.image_path_input.text()

    def show_main_menu(self):
        self.stacked_layout.setCurrentWidget(self.main_menu)

    def show_image_menu(self):
        self.stacked_layout.setCurrentWidget(self.image_menu)


def run_gui():
    app = QApplication.instance() or QApplication(sys.argv)
    window = PantBottleRecognitionWindow()
    window.show()

    return app.exec()
