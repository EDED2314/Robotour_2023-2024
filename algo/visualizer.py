import matplotlib.pyplot as plt
import matplotlib.patches as patch


class Visualizer:
    def __init__(
        self,
        wall_lines: list,
        start: tuple,
        stop: tuple,
        gates: list,
        wall_actually_lines: list,
        mapsize: int,
        other=None,
    ):
        self.wall_lines = wall_lines
        self.start = start
        self.stop = stop
        self.gates = gates
        self.other = other
        self.wall_actually_lines = wall_actually_lines
        super().__init__()

        self.size = mapsize
        self.fig, self.ax = plt.subplots()

    def init(self):
        self.ax.set_xlim(0, self.size)
        self.ax.set_ylim(0, self.size)
        self.ax.axhline(0, color="black", linewidth=0.5)
        self.ax.axvline(0, color="black", linewidth=0.5)
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.grid(True, linewidth=0.5, linestyle="--", color="gray")

    def initDrawings(self):
        self.drawCircle(self.start, 5, color="green")
        self.drawCircle(self.stop, 5)
        for line in self.wall_lines:
            self.drawLine(line[0], line[1])

        for gate in self.gates:
            self.drawCircle(gate, 5, "blue")

        # print(self.wall_actually_lines)
        for line in self.wall_actually_lines:
            self.drawLine(line[0], line[1], color="red")

        self.drawLine(
            self.other["line"][0], self.other["line"][1], color="green", linewidth=3
        )
        # for line in self.other["wall_lines"]:
        #     self.drawLine(line[0], line[1], color="yellow")

    def drawLine(
        self, point1: tuple, point2: tuple, color: str = "blue", linewidth: int = 2
    ):
        self.ax.plot(
            (point1[0], point2[0]),
            (point1[1], point2[1]),
            color=color,
            linewidth=linewidth,
        )
        return

    def drawCircle(self, center: tuple, radius: int, color: str = "red", fill=False):
        circle = patch.Circle(center, radius, color=color, fill=fill)
        self.ax.add_artist(circle)

    def drawRectangle(self, xy: tuple, height, width, color="green", fill=False):
        rectangle = patch.Rectangle(xy, width=width, height=height)
        self.ax.add_artist(rectangle)

    def run(self):
        self.init()
        self.initDrawings()
        plt.show()

    def tryi(self):
        x1, y1 = 2, 3
        x2, y2 = 5, 7

        # Create figure and axis
        fig, ax = plt.subplots()

        # Draw the line using plt.plot()
        ax.plot([x1, x2], [y1, y2], color="blue", linewidth=2)

        # Set limits for x and y axes
        ax.set_xlim(min(x1, x2), max(x1, x2))
        ax.set_ylim(min(y1, y2), max(y1, y2))

        # Add labels to x and y axes
        ax.set_xlabel("X")
        ax.set_ylabel("Y")

        # Show the plot
        plt.show()
