from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QSize, Qt
from functools import partial
from utils.data import appendToBlocks


class CellWidget(QFrame):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.setMinimumSize(QSize(50, 50))
        self.setStyleSheet(
            "border-width: 1;" "border-style: solid;" "border-color: none"
        )
        self.setFrameShape(QFrame.Box)
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.contextMenuEvent)

        self.top_border_color = QColor(255, 0, 0)  # Red

    def mousePressEvent(self, event):
        print(f"Clicked on cell [{self.row}, {self.col}]")

    def contextMenuEvent(self, event):
        context_menu = QMenu(self)
        action1 = context_menu.addAction("Blocks")

        self.generateSubActionsForBlocks(action1)

        action2 = context_menu.addAction("Movement")
        action3 = context_menu.addAction("Start/Stop")
        action4 = context_menu.addAction("Gates")
        # todo: may like hover or rihjt click to get info about it
        action5 = context_menu.addAction("Info")

        context_menu.exec_(self.mapToGlobal(event))

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the border color and opacity
        border_color = QColor(0, 0, 0, 50)  # Black color with 100 opacity

        # Draw the border
        pen = painter.pen()
        pen.setWidth(2)
        pen.setColor(border_color)
        painter.setPen(pen)
        painter.drawRect(self.rect())

    def generateSubActionsForBlocks(self, ctx_action: QAction):
        locs = ["T", "B", "L", "R"]

        sub_menu = QMenu("Blocks", self)
        for loci in locs:
            action = sub_menu.addAction(loci)
            action.triggered.connect(
                partial(self.generateSubActionsForBlocksListener, loci)
            )

        ctx_action.setMenu(sub_menu)

    def generateSubActionsForBlocksListener(self, name):
        block = {"points": [], "pos": "T"}
        row = self.row
        col = self.col
        row1 = row
        col1 = col
        if name == "T":
            col1 = col + 1
        elif name == "B":
            col1 = col + 1
        elif name == "L":
            row1 = row + 1
        elif name == "R":
            row1 = row + 1

        block["points"] = [row, col, row1, col1]
        block["pos"] = name
        appendToBlocks(block)
        return
