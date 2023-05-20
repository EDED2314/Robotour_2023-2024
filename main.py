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

from utils.data import initData, initRobotdata
from layouts.map import Map
from widgets.line import PaintGridWidget
from utils.export import convertToRobotableJson


class MainWindow(QMainWindow):
    def __init__(self, json_data):
        super().__init__()
        self.json_data = json_data
        self.setWindowTitle("Robotour gui - Eddie Tang 25'")
        self.setMaximumSize(QSize(400, 400))

        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Create the export action
        export_action = QAction("Export To Robot Json", self)
        export_action.triggered.connect(self.exportClicked)
        toolbar.addAction(export_action)

        main_layout = QHBoxLayout()

        map_widget = PaintGridWidget(self.json_data)
        main_layout.addWidget(map_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        map_widget.setLinePoints(QPoint(0, 0), QPoint(1, 1))

        self.setCentralWidget(central_widget)

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
