import sys
from PyQt5.QtCore import Qt, QMimeData
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QListWidget,
    QListWidgetItem,
    QGridLayout,
    QLabel,
    QFrame,
    QWidget,
    QHBoxLayout,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QDrag, QColor, QPainter
from PyQt5.QtCore import QSize, Qt, QPoint

from utils.data import initData
from layouts.map import Map
from widgets.line import LineGridWidget


class MainWindow(QMainWindow):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data
        self.setWindowTitle("Robotour gui - Eddie Tang 25'")
        self.setMinimumSize(QSize(200, 200))
        self.setMaximumSize(QSize(400, 400))

        self.map = Map()

        main_layout = QHBoxLayout()

        map_widget = LineGridWidget(self.map, self.json_data)
        main_layout.addWidget(map_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        map_widget.setLinePoints(QPoint(0, 0), QPoint(1, 1))

        self.setCentralWidget(central_widget)


if __name__ == "__main__":
    data = initData()
    app = QApplication(sys.argv)
    window = MainWindow(data)
    window.show()
    sys.exit(app.exec_())
