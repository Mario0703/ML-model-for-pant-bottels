import sys

from PyQt6.QtWidgets import QApplication, QWidget


def run_gui():
    app = QApplication(sys.argv)

    window = QWidget()
    window.setWindowTitle("Pant Bottle Recognition")
    window.resize(800, 600)
    window.show()

    return app.exec()
