import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
