from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
)
from PyQt5.QtCore import Qt
from widgets.cell import CellWidget


class Map(QGridLayout):
    def __init__(self, refreshDataFunction, parent):
        super().__init__()
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)
        self.init(refreshDataFunction, parent)
        # todo: maybe a tool bar to like spice stuff up, help menu, info etc

    def init(self, refreshFunc, parent):
        for row in range(4):
            for col in range(4):
                cell_widget = CellWidget(row, col, refreshFunc, parent)
                # cell_widget.setAttribute(Qt.WA_OpaquePaintEvent)
                self.addWidget(cell_widget, row, col)
