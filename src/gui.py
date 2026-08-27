import sys

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel, QStackedLayout
from PyQt6.QtCore import Qt


def run_gui():
    app = QApplication.instance() or QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Pant Bottle Recognition")
    window.resize(800, 600)

    stacked_layout = QStackedLayout()

    # Main menu
    main_menu = QWidget()
    main_layout = QVBoxLayout(main_menu)

    title = QLabel("Pant Bottle Recognition")
    title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    title.setStyleSheet("font-size: 28px; font-weight: bold;")

    bottle_image_button = QPushButton("Import image of a bottle")
    bottle_camera_button = QPushButton(
        "Use the camera to determine if a bottle has pant"
    )

    main_layout.addWidget(title)
    main_layout.addStretch()
    main_layout.addWidget(
        bottle_image_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )
    main_layout.addWidget(
        bottle_camera_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )

    # Image menu
    image_menu = QWidget()
    image_layout = QVBoxLayout(image_menu)

    image_title = QLabel("Import a bottle image")
    image_title.setAlignment(Qt.AlignmentFlag.AlignCenter)
    

    select_image_button = QPushButton("Select image")
    back_button = QPushButton("Back")

    image_layout.addWidget(image_title)
    image_layout.addStretch()
    image_layout.addWidget(
        select_image_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )
    image_layout.addWidget(
        back_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )

    # Add pages to the stacked layout
    stacked_layout.addWidget(main_menu)   # Index 0
    stacked_layout.addWidget(image_menu)  # Index 1

    # Switch between pages
    bottle_image_button.clicked.connect(
        lambda: stacked_layout.setCurrentIndex(1)
    )
    back_button.clicked.connect(
        lambda: stacked_layout.setCurrentIndex(0)
    )

    window.setLayout(stacked_layout)
    window.show()

    return app.exec()
