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
    image_title.setStyleSheet("font-size: 28px; font-weight: bold;")

    image_path_input = QLineEdit()
    image_path_input.setPlaceholderText("Enter or select the path to an image")
    image_path_input.setFixedWidth(400)

    select_image_button = QPushButton("Select image")
    back_button = QPushButton("Back")

    def select_image():
        image_path, _ = QFileDialog.getOpenFileName(
            window,
            "Select a bottle image",
            "",
            "Image files (*.png *.jpg *.jpeg *.bmp *.webp)",
        )
        if image_path:
            image_path_input.setText(image_path)

    image_layout.addWidget(image_title)
    image_layout.addStretch()
    image_layout.addWidget(
        image_path_input,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )
    image_layout.addWidget(
        select_image_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )
    image_layout.addWidget(
        back_button,
        alignment=Qt.AlignmentFlag.AlignHCenter,
    )

    # Add pages to the stacked layout
    stacked_layout.addWidget(main_menu)  # Index 0
    stacked_layout.addWidget(image_menu)  # Index 1

    # Switch between pages
    bottle_image_button.clicked.connect(lambda: stacked_layout.setCurrentIndex(1))
    select_image_button.clicked.connect(select_image)
    back_button.clicked.connect(lambda: stacked_layout.setCurrentIndex(0))

    window.setLayout(stacked_layout)
    window.show()

    return app.exec()
