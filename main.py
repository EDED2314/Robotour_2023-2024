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
    QToolBar,
    QFileDialog,
    QMessageBox,
)
from PyQt5.QtGui import QDrag, QColor, QPainter
from PyQt5.QtCore import QSize, Qt, QPoint

from utils.data import initData, initRobotdata, clearMovements
from layouts.map import Map
from widgets.paint import PaintGridWidget
from utils.export import convertToRobotableJson


class MainWindow(QMainWindow):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data
        self.setWindowTitle("Robotour gui - Eddie Tang 25'")
        self.setMaximumSize(QSize(400, 400))

        self.initToolBar()

        main_layout = QHBoxLayout()

        self.map_widget = PaintGridWidget(self.json_data)
        main_layout.addWidget(self.map_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def initToolBar(self):
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        export_action = QAction("Export To Robot Json", self)
        export_action.triggered.connect(self.exportClicked)
        clear_movements = QAction("Clear Movements", self)
        clear_movements.triggered.connect(self.clear)
        toolbar.addAction(export_action)
        toolbar.addAction(clear_movements)

    def clear(self):
        clearMovements()
        self.map_widget.refreshData(self.map_widget)

    def exportClicked(self):
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getSaveFileName(
            self, "Save File", "", "JSON Files (*.json)"
        )
        if file_path:
            suc = convertToRobotableJson(file_path)
            if suc:
                QMessageBox.information(
                    self, "Export Successful", "Export completed successfully!"
                )


if __name__ == "__main__":
    initRobotdata()
    data = initData()
    app = QApplication(sys.argv)
    window = MainWindow(data)
    window.show()
    sys.exit(app.exec_())
