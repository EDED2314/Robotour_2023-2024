import math, sys
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
    QToolBar,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QDrag, QColor, QPainter, QPen
from PyQt5.QtCore import QSize, Qt, QPoint, QRectF

ROBOT_RADIUS = 20


class SourishAlgorithm:
    def __init__(self):
        return

    def initSample(self):
        {
            "blocks": [
                [0, 100, 50, 100],  # x1,y1,x2,y2
                [50, 50, 50, 100],
                [100, 200, 150, 200],
                [50, 100, 50, 150],
                [100, 100, 150, 100],
                [100, 100, 150, 100],
                [100, 0, 150, 0],
                [100, 100, 100, 150],
            ],
            "gates": [25, 125],
            "start": [75, 175],
            "stop": [75, 25],
            "actions": [],
        }

    def calculate_outline_points(self, pointss, l):
        outline_points = []

        for i in range(0, len(pointss), 2):
            x1, y1 = pointss[i]
            x2, y2 = pointss[i + 1]

            if x1 == x2:  # Vertical line
                x3 = x1 - l / 2
                y3 = min(y1, y2) - l / 2
                x4 = x1 + l / 2
                y4 = max(y1, y2) + l / 2

                outline_points.extend([(x3, y3), (x4, y3), (x4, y4), (x3, y4)])
            elif y1 == y2:  # Horizontal line
                x3 = min(x1, x2) - l / 2
                y3 = y1 - l / 2
                x4 = max(x1, x2) + l / 2
                y4 = y1 + l / 2

                outline_points.extend([(x3, y3), (x4, y3), (x4, y4), (x3, y4)])

        return outline_points

    def test(self):
        # result = [(array[i], array[i+1]) for i in range(0, len(array)-1, 2)]
        points = [(0, 100), (50, 100)]
        points = [(100, 200), (150, 200)]
        points = [(100, 100), (100, 150)]
        # points = [(100, 100), (100, 150), (100, 150), (150, 150)]
        l = ROBOT_RADIUS * 2

        outline_points = self.calculate_outline_points(points, l)
        print(outline_points)

        app = QApplication(sys.argv)
        vis = Visualizer({"rect": outline_points, "line": points})
        vis.show()
        sys.exit(app.exec_())


class Visualizer(QMainWindow):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setFixedSize(QSize(400, 400))
        self.setWindowTitle("algo vis")

    def paintEvent(self, event):
        painter = QPainter(self)
        pen = QPen()
        pen.setWidth(2)
        pen.setColor(QColor(255, 0, 0))  # Red color
        painter.setPen(pen)

        # Draw the rectangle
        rect_points = [QPoint(int(s[0]), int(s[1])) for s in self.data["rect"]]
        # print(rect_points)
        painter.drawPolygon(*rect_points)
        # painter.drawRect(*rect_points)
        line = [QPoint(int(s[0]), int(s[1])) for s in self.data["line"]]

        painter.drawLine(line[0], line[1])
        # painter.drawRect(50, 50, 200, 100)


s = SourishAlgorithm()
s.test()
