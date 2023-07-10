from audioop import avg

from PyQt5.QtCore import QSize, Qt, pyqtSignal
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QMainWindow, QVBoxLayout, QHBoxLayout, QMenu, QMenuBar,\
    QLabel
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.figure import Figure
import time
import sys


class Window(QMainWindow):

    trigger = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.num = 0
        self.label = QLabel(f"{self.num}")
        self.button = QPushButton("Click me!")
        self.button.clicked.connect(lambda: self._emitter())

        layout = QHBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)


        widget = QWidget()
        widget.setLayout(layout)


        self.setCentralWidget(widget)


        self.trigger.connect(self._handler)


    def _handler(self):
         self.num += 1
    def _emitter(self):
        self.trigger.emit()
        print("something emited!")
        self.trigger.connect(self._handler)

if __name__ == '__main__':
    app = QApplication([])
    main_window = Window()
    main_window.show()
    app.exec()

