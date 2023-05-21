from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint
from layouts.map import Map
from utils.data import initData


class PaintGridWidget(QWidget):
    def __init__(self, json_data, parent=None):
        super().__init__(parent)
        self.layout = Map(self.refreshData, self)
        self.setLayout(self.layout)
        self.json_data = json_data
        self.blocks = self.json_data["blocks"]
        self.start = self.json_data["start"]
        self.stop = self.json_data["stop"]
        self.gates = self.json_data["gates"]
        self.actions = self.json_data["actions"]
        # print(self.blocks)

        self.arrow_size = 15
        self.robot_bounds = 20

    def refreshData(self, paint_grid_object_self):
        paint_grid_object_self.json_data = initData()
        paint_grid_object_self.blocks = paint_grid_object_self.json_data["blocks"]
        paint_grid_object_self.start = paint_grid_object_self.json_data["start"]
        paint_grid_object_self.stop = paint_grid_object_self.json_data["stop"]
        paint_grid_object_self.gates = paint_grid_object_self.json_data["gates"]
        paint_grid_object_self.actions = paint_grid_object_self.json_data["actions"]
        paint_grid_object_self.update()

    def setLinePoints(self, start, end):
        self.line_start = start
        self.line_end = end
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Set the line color and width
        pen = QPen(QColor(255, 0, 0))  # Red color
        pen.setWidth(self.robot_bounds)
        painter.setPen(pen)

        for block in self.blocks:
            p1, p2 = self.paintBlock(block)
            # print(p1, p2)
            painter.drawLine(p1, p2)

        # # Calculate the center points of the widgets
        # center1 = self.getWidgetCenter(self.line_start)
        # center2 = self.getWidgetCenter(self.line_end)
        # # print(center1, center2)

        # # Draw a line between the two center points
        # painter.drawLine(center1, center2)
        # # painter.drawLine(0, 0, 25, 50)
        pen = QPen(QColor(255, 0, 0))
        pen.setWidth(10)
        painter.setPen(pen)
        self.paintCenterPoint(self.stop[0], self.stop[1], 5, painter)
        pen = QPen(QColor(0, 255, 0))
        pen.setWidth(10)
        painter.setPen(pen)
        self.paintCenterPoint(self.start[0], self.start[1], 5, painter)
        pen = QPen(QColor(0, 0, 255))
        pen.setWidth(2)
        painter.setPen(pen)
        for gate in self.gates:
            self.paintCenterPoint(gate[0], gate[1], 10, painter)
        for action in self.actions:
            self.paintArrow(action, painter)

    def getWidgetCenter(self, point: QPoint):
        widget = self.layout.itemAtPosition(point.x(), point.y()).widget()
        rect = widget.geometry()
        center_x = rect.x() + rect.width() // 2
        center_y = rect.y() + rect.height() // 2
        return QPoint(center_x, center_y)

    def getArrowHeadPoints(self, end_point: QPoint, direc):
        # todo: change direction of arrow dybnamically
        return [
            end_point,
            QPoint(end_point.x() + self.arrow_size, end_point.y() + self.arrow_size),
            QPoint(end_point.x() - self.arrow_size, end_point.y() + self.arrow_size),
        ]

    def paintArrow(self, action, painter: QPainter):
        cell = action["points"]
        direc = action["direction"]
        widget = self.layout.itemAtPosition(cell[0], cell[1]).widget()
        rect = widget.geometry()
        center_x = rect.x() + rect.width() // 2
        center_y = rect.y() + rect.height() // 2
        y = rect.y()
        x = rect.x()

        start_point = QPoint(center_x, center_y)
        end_point = QPoint(center_x, center_y)
        if direc == "F":
            start_point = QPoint(center_x, y + rect.height())
            end_point = QPoint(center_x, y)
        elif direc == "B":
            start_point = QPoint(center_x, y)
            end_point = QPoint(center_x, y + rect.height())
        elif direc == "L":
            start_point = QPoint(x + rect.width(), center_y)
            end_point = QPoint(x, center_y)
        elif direc == "R":
            start_point = QPoint(x, center_y)
            end_point = QPoint(x + rect.width(), center_y)

        arrow_points = self.getArrowHeadPoints(end_point, direc)
        painter.drawLine(start_point, end_point)
        painter.drawPolygon(*arrow_points)
        return

    def paintCenterPoint(self, row: int, col: int, rad: int, painter: QPainter):
        p = self.getWidgetCenter(QPoint(row, col))
        painter.drawEllipse(
            p.x() - rad,
            p.y() - rad,
            rad * 2,
            rad * 2,
        )
        return

    def paintBlock(self, block):
        points = block["points"]
        pos = block["pos"]
        widget1 = self.layout.itemAtPosition(points[0], points[1]).widget()
        # widget2 = self.layout.itemAtPosition(points[2], points[3]).widget()
        rect1 = widget1.geometry()

        """
        Its
        suposed to be like row, col in poiunts in nav.json
        so like, i wrote the points incorrectly, because row, col will give a x,y
        """

        x1 = rect1.x()
        y1 = rect1.y()

        p1 = QPoint()
        p2 = QPoint()

        if pos == "T":
            x2 = x1 + rect1.width()
            y2 = y1
            p1 = QPoint(x1, y1)
            p2 = QPoint(x2, y2)

        elif pos == "B":
            x2 = x1 + rect1.width()
            y2 = y1
            p1 = QPoint(x1, y1 + rect1.height())
            p2 = QPoint(x2, y2 + rect1.height())
        elif pos == "L":
            x2 = x1
            y2 = y1 + rect1.height()
            p1 = QPoint(x1, y1)
            p2 = QPoint(x2, y2)
        elif pos == "R":
            x2 = x1
            y2 = y1 + rect1.height()
            p1 = QPoint(x1 + rect1.width(), y1)
            p2 = QPoint(x2 + rect1.width(), y2)

        # print(x1, y1, x2, y2)
        # print("----")
        # print(p1.x(), p1.y(), p2.x(), p2.y())
        # print("~~~~~")
        return (p1, p2)
