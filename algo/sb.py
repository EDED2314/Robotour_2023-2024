import math


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

    def calculate_outline_points(points, l):
        x1, y1, x2, y2 = points
        theta = math.atan2(y2 - y1, x2 - x1)
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        h = l / 2

        x3 = x1 + h * math.sin(theta)
        y3 = y1 - h * math.cos(theta)
        x4 = x1 - h * math.sin(theta)
        y4 = y1 + h * math.cos(theta)

        x5 = x2 + h * math.sin(theta)
        y5 = y2 - h * math.cos(theta)
        x6 = x2 - h * math.sin(theta)
        y6 = y2 + h * math.cos(theta)

        return [(x3, y3), (x4, y4), (x5, y5), (x6, y6)]

    def test(self):
        points = [0, 100, 50, 100]
        l = 10

        outline_points = self.calculate_outline_points(points, l)
        print(outline_points)


s = SourishAlgorithm()
s.test()
