from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt, QPoint


class LineGridWidget(QWidget):
    def __init__(self, layout: QGridLayout, json_data, parent=None):
        super().__init__(parent)
        self.layout = layout
        self.setLayout(self.layout)
        self.json_data = json_data

        self.line_start = QPoint()
        self.line_end = QPoint()

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
        pen.setWidth(2)
        painter.setPen(pen)

        # Calculate the center points of the widgets
        center1 = self.getWidgetCenter(self.line_start)
        center2 = self.getWidgetCenter(self.line_end)

        # Draw a line between the two center points
        painter.drawLine(center1, center2)

    def getWidgetCenter(self, point: QPoint):
        widget = self.layout.itemAtPosition(point.x(), point.y()).widget()
        rect = widget.geometry()
        center_x = rect.x() + rect.width() // 2
        center_y = rect.y() + rect.height() // 2
        return QPoint(center_x, center_y)

    def initBlocks(self):
        blocks = self.json_data["blocks"]
        for block in blocks:
            pass
