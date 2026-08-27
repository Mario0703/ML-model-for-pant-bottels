import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


def run_gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Pant Bottle Recognition")
    window.resize(800, 600)
    layout = QVBoxLayout()
    width, height = 200, 60

    bottle_image_button = QPushButton("Import image of a bottle")
    bottle_camera_button = QPushButton(
        "Use the camera to determine if a bottle has pant"
    )

    bottle_image_button.setFixedSize(width, height)
    bottle_camera_button.setFixedSize(width, height)

    layout.addWidget(bottle_image_button)
    layout.addWidget(bottle_camera_button)

    window.setLayout(layout)

    window.show()

    return app.exec()
