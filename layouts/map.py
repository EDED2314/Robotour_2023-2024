from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
)
from PyQt5.QtGui import QDrag, QColor, QPainter, QPen
from widgets.cell import CellWidget


class Map(QGridLayout):
    def __init__(self):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

        self.init()

    def init(self):
        for row in range(4):
            for col in range(4):
                cell_widget = CellWidget(row, col)
                self.addWidget(cell_widget, row, col)
