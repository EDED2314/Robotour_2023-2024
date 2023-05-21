from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtCore import QSize, Qt
from functools import partial
from utils.data import (
    appendOrDeleteBlocks,
    modifyStartPoint,
    modifyStopPoint,
    appendGate,
    delGate,
    appendOrDeleteMovement,
)


class CellWidget(QFrame):
    def __init__(self, row, col, refreshDataFunction, parent):
        super().__init__()
        self.row = row
        self.col = col
        self.refreshFunction = refreshDataFunction
        self.parent = parent
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
        self.generateSubActionsForMovement(action2)

        action3 = context_menu.addAction("Start/Stop")
        self.generateSubActionsForStartStop(action3)

        action4 = context_menu.addAction("Gates")
        self.generateSubActionsForGates(action4)

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

    def generateSubActionsForGates(self, ctx_action: QAction):
        gate_add_del = QMenu("Gate set un-set menu", self)
        add = gate_add_del.addAction("Set as gate")
        add.triggered.connect(partial(self.gateListener, "set"))
        delete = gate_add_del.addAction("Delete this block's gate")
        delete.triggered.connect(partial(self.gateListener, "del"))
        ctx_action.setMenu(gate_add_del)

    def generateSubActionsForStartStop(self, ctx_action: QAction):
        sides = ["mid", "top", "bottom", "left", "right"]
        start_stop = QMenu("start stop menu", self)
        start = start_stop.addAction("Start")
        stop = start_stop.addAction("Stop")

        start_menu = QMenu("start selector menu", self)
        for side in sides:
            act = start_menu.addAction(side)
            act.triggered.connect(partial(self.startStopListner, "start", side))
        start.setMenu(start_menu)

        stop_menu = QMenu("stop selector menu", self)
        for side in sides:
            act = stop_menu.addAction(side)
            act.triggered.connect(partial(self.startStopListner, "stop", side))
        stop.setMenu(stop_menu)

        ctx_action.setMenu(start_stop)

    def generateSubActionsForMovement(self, ctx_action: QAction):
        locs = ["F", "B", "L", "R"]
        sub_menu = QMenu("Blocks", self)
        for move in locs:
            action = sub_menu.addAction(move)
            action.triggered.connect(
                partial(self.generateSubActionsForMovementListener, move)
            )

        ctx_action.setMenu(sub_menu)

    def generateSubActionsForBlocks(self, ctx_action: QAction):
        locs = ["T", "B", "L", "R"]

        sub_menu = QMenu("Blocks", self)
        for loci in locs:
            action = sub_menu.addAction(loci)
            action.triggered.connect(
                partial(self.generateSubActionsForBlocksListener, loci)
            )

        ctx_action.setMenu(sub_menu)

    def generateSubActionsForMovementListener(self, name):
        move = {"points": [self.row, self.col], "direction": name}
        appendOrDeleteMovement(move)
        self.refreshFunction(self.parent)
        return

    def generateSubActionsForBlocksListener(self, name):
        block = {"points": [], "pos": "T"}
        row = self.row
        col = self.col

        block["points"] = [row, col]
        block["pos"] = name
        appendOrDeleteBlocks(block)
        self.refreshFunction(self.parent)
        return

    def startStopListner(self, name: str, side: str):
        if name == "start":
            modifyStartPoint(self.row, self.col, side)
        elif name == "stop":
            modifyStopPoint(self.row, self.col, side)
        self.refreshFunction(self.parent)
        return

    def gateListener(self, name):
        if name == "set":
            appendGate(self.row, self.col)
        elif name == "del":
            delGate(self.row, self.col)
        self.refreshFunction(self.parent)
        return
