from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QFrame,
    QMenu,
    QAction,
)
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QSize, Qt


class CellWidget(QFrame):
    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col
        self.setMinimumSize(QSize(50, 50))
        self.setStyleSheet(
            "border-width: 1;" "border-style: solid;" "border-color: rgb(0, 0, 0)"
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

        action = context_menu.exec_(self.mapToGlobal(event))

        if action == action1:
            print(f"Action 1 selected for cell [{self.row}, {self.col}]")
        # elif action == sub_action1:
        #     print(f"Sub-Action 1 selected for cell [{self.row}, {self.col}]")
        # elif action == sub_action2:
        #     print(f"Sub-Action 2 selected for cell [{self.row}, {self.col}]")
        elif action == action2:
            print(f"Action 2 selected for cell [{self.row}, {self.col}]")

    def generateSubActionsForBlocks(self, ctx_action: QAction):
        locs = ["T", "B", "L", "R"]

        sub_one = QMenu("Num Blocks 1", self)
        sub_two = QMenu("Num Blocks 2", self)
        sub_three = QMenu("Num Blocks 3", self)

        for loci in locs:
            sub_one.addAction(loci)
            for locj in locs:
                if loci != locj:
                    combo = loci + locj
                    sub_two.addAction(combo)
                    for lock in locs:
                        if loci != lock and locj != lock:
                            comboo = loci + locj + lock
                            sub_three.addAction(comboo)

        sub_menu = QMenu("Num Blocks", self)
        sub_action1 = sub_menu.addAction("One block")
        sub_action2 = sub_menu.addAction("Two blocks")
        sub_action3 = sub_menu.addAction("Three blocks")

        sub_action1.setMenu(sub_one)
        sub_action2.setMenu(sub_two)
        sub_action3.setMenu(sub_three)

        ctx_action.setMenu(sub_menu)
