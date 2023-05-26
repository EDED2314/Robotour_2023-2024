import numpy as np


class Algorithm:
    ROBOT_RADIUS = 20

    def __init__(self):
        return

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

    def initSample(self):
        sample = {
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

        self.blocks = []
        for block in sample["blocks"]:
            result = [(block[i], block[i + 1]) for i in range(0, len(block) - 1, 2)]
            outline_points = self.calculate_outline_points(
                result, Algorithm.ROBOT_RADIUS * 2
            )
            for i in range(len(outline_points)):
                for k in range(i, len(outline_points), 1):
                    p1 = outline_points[k]
                    p2 = outline_points[i]
                    p1x = p1[0]
                    p1y = p1[1]
                    p2x = p2[0]
                    p2y = p2[1]
                    if (p1x == p2x or p1y == p2y) and not (p1x == p2x and p2y == p2y):
                        self.blocks.append((p1, p2))

        sample["blocks"] = self.blocks
        sample["gates"] = [
            (sample["gates"][i], sample["gates"][i + 1])
            for i in range(0, len(sample["gates"]) - 1, 2)
        ]

        self.map = sample
        return sample

    def calc_gates(self):
        gates = self.map["gates"]
        for gate in gates:
            x = gate[0]
            y = gate[1]

    def init(self):
        self.initSample()
        self.gates = self.map["gates"]
        self.start = (self.map["start"][0], self.map["start"][1])
        self.stop = (self.map["stop"][0], self.map["stop"][1])

    def test(self):
        return

    # path arrays with start path
    def createpath(self, startpoint, endpoint):
        array = [startpoint, endpoint]
        return array

    # start paths
    def startpaths(self, startpoint, gatepoints):
        start_paths = []

        for g in gatepoints:
            start_paths.append(self.createpath(startpoint, g))

        return start_paths

    def stoppaths(self, endpoint, gatepoints):
        stoppaths = []

        for g in gatepoints:
            stoppaths.append(self.createpath(endpoint, g))

        return stoppaths

    def checkIntersection(self, start_point: tuple, end_point: tuple):
        """
        normalize wall paths by subtracting the start point in the path to the array
        assign wall_paths variable to the new array
        normalize end by subtracting startpoint from end point
        start the new path from 0,0 to normalized end -> travel path

        calculating the distance r of travel_path (start to end) using pythag, start to end
        start by ordering from wall_paths with the smallest radius to greatest  radius. |p1|, |p2|

        if wall_paths have both points with distance greater than r, disclude them from checkable locations -> pop from array.

        find the start and end angles of the wall path using atan (remember the difference be greater than 180, if it is greater than 180, reverse the start and end angles)
        special cases, vertical cases, 90* and 270*
        check if travel path angle (atan(y/x)) resides between the start and end angles of the wall paths
        if it does, count that as the intersection, record the wall path point with the smallest possible distance to it, return

        parameters
        -------
        start_point - start point (x,y)
        end_point - end point (x,y)
        """
        self.init()
        wall_paths = self.blocks

        n_end = np.subtract(end_point, start_point)
        n_start = np.array((0, 0))
        print(n_end, n_start)

        n_wall_lines = np.array(
            [
                (
                    np.subtract(wall_path[0], start_point),
                    np.subtract(wall_path[1], start_point),
                )
                for wall_path in wall_paths
            ]
        )

        print(n_wall_lines)
        travel_path_distance = np.linalg.norm(n_end)
        print(travel_path_distance)

        # wall path distaces
        # between each point find the shortest distance
        # use that distance and compare it with other distances found via that method

        dis_arr = []
        dis_dict = {}
        occur_dis_dict = {}
        sorted_n_wall_lines = {}
        # example dict is {dis: [((x1,y1), (x2,y2) ), ....]}
        for line in n_wall_lines:
            dis = max(np.linalg.norm(line[0]), np.linalg.norm(line[1]))
            dis_arr.append(dis)
            if dis not in dis_dict:
                dis_dict[dis] = []
            dis_dict[dis].append(line)

        dis_arr = sorted(dis_arr)
        for dis in dis_arr:
            if dis not in occur_dis_dict:
                occur_dis_dict[dis] = 0

            lines = dis_dict[dis]
            line = lines[occur_dis_dict[dis]]
            sorted_n_wall_lines.append(line)

            occur_dis_dict[dis] += 1

        # print(sorted_n_wall_lines)
        # collision detection, detect collision

    def run(self):
        self.init()
        # print(self.blocks)
        self.checkIntersection((50, 50), (100, 100))


al = Algorithm()
al.run()
