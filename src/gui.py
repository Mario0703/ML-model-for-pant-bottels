import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt


def run_gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Pant Bottle Recognition")
    window.resize(800, 600)
    layout = QVBoxLayout()
    width, height = 400, 60

    bottle_image_button = QPushButton("Import image of a bottle")
    bottle_camera_button = QPushButton(
        "Use the camera to determine if a bottle has pant"
    )
    title = QLabel("Pant Bottle Recognition")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("""
        font-size: 28px;
        font-weight: bold;
    """)

    bottle_image_button.setFixedSize(width, height)
    bottle_camera_button.setFixedSize(width, height)
    layout.addWidget(title)
    layout.addStretch()
    layout.addWidget(
        bottle_image_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )
    layout.addWidget(
        bottle_camera_button,
        alignment=Qt.AlignmentFlag.AlignHCenter)


    window.setLayout(layout)

    window.show()

    return app.exec()
