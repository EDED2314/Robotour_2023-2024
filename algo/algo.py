import numpy as np
from visualizer import Visualizer


class Algorithm:
    ROBOT_RADIUS = 10 + 10
    SIZE = 200
    VELOCITY = 20

    def __init__(self):
        self.visited = []
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
                [50, 49, 100, 49],
                [100, 0, 100, 50],
                [150, 150, 200, 150],
                [150, 0, 150, 50],
                [100, 100, 150, 100],
                [50, 150, 100, 150],
                [0, 100, 50, 100],
                [100, 100, 100, 150],
            ],
            "gates": [[25, 125], [125, 25], [125, 175]],
            "start": [75, 175],
            "stop": [75, 25],
            "actions": [],
        }

        self.block_lines_form = []
        for block in sample["blocks"]:
            self.block_lines_form.append(
                [
                    (block[i], Algorithm.SIZE - block[i + 1])
                    for i in range(0, len(block) - 1, 2)
                ]
            )

        self.blocks = []
        self.walls_prime = []
        for block in sample["blocks"]:
            result = [
                (block[i], Algorithm.SIZE - block[i + 1])
                for i in range(0, len(block) - 1, 2)
            ]
            outline_points = self.calculate_outline_points(
                result, Algorithm.ROBOT_RADIUS * 2
            )
            outline_points_prime = self.calculate_outline_points(
                result, (Algorithm.ROBOT_RADIUS - 2) * 2
            )
            # print(outline_points)
            for i in range(len(outline_points)):
                for k in range(i, len(outline_points), 1):
                    p1 = outline_points[k]
                    p2 = outline_points[i]
                    p1_prime = outline_points_prime[k]
                    p2_prime = outline_points_prime[i]
                    p1x = p1[0]
                    p1y = p1[1]
                    p2x = p2[0]
                    p2y = p2[1]
                    if (
                        (p1x == p2x or p1y == p2y)
                        and not (p1x == p2x and p1y == p2y)
                        # and (p1x >= 0 and p1y >= 0 and p2x >= 0 and p2y >= 0)
                        # and (
                        #     p1x <= Algorithm.SIZE
                        #     and p1y <= Algorithm.SIZE
                        #     and p2x <= Algorithm.SIZE
                        #     and p2y <= Algorithm.SIZE
                        # )
                    ):
                        self.blocks.append((p1, p2))
                        # self.blocks.append((p1_prime, p2_prime))
                        self.walls_prime.append((p1_prime, p2_prime))

        sample["blocks"] = self.blocks
        self.gates = []
        for gate in sample["gates"]:
            gatex = gate[1]
            gatey = Algorithm.SIZE - gate[0]
            self.gates.append((gatex, gatey))

        sample["gates"] = self.gates

        # sample["gates"] = [
        #     (sample["gates"][i], sample["gates"][i + 1])
        #     for i in range(0, len(sample["gates"]) - 1, 2)
        # ]

        self.map = sample
        return sample

    def init(self):
        self.initSample()
        self.gates = self.map["gates"]
        self.start = (
            self.map["start"][0],
            Algorithm.SIZE - self.map["start"][1],
        )
        self.stop = (
            self.map["stop"][0],
            Algorithm.SIZE - self.map["stop"][1],
        )

    def setSortedNWallLinesToDraw(self, sorted_n_wall_lines, start_point):
        self.sorted_n_wall_lines_to_draw = []
        for n_wall_line in sorted_n_wall_lines:
            p1 = n_wall_line[0]
            p2 = n_wall_line[1]
            p1 += start_point
            p2 += start_point
            self.sorted_n_wall_lines_to_draw.append(np.array([p1, p2]))

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

    def is_intersect(self, line1, line2):
        """
        Checks if two line segments intersect.

        Args:
            line1: A tuple of two points that define the first line segment.
            line2: A tuple of two points that define the second line segment.

        Returns:
            True if the lines intersect, False otherwise.
        """

        # Extract coordinates from the line segments
        x1, y1 = line1[0]
        x2, y2 = line1[1]
        x3, y3 = line2[0]
        x4, y4 = line2[1]

        # Check if the lines are collinear.
        if np.array_equal(line1[0], line2[0]) and np.array_equal(line1[1], line2[1]):
            return None, None

        # Calculate the determinant of the line segments
        det = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)

        # Check if the lines are parallel
        if det == 0:
            return None, None

        # Calculate the intersection point
        intersection_x = (
            (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - y3 * x4)
        ) / det
        intersection_y = (
            (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - y3 * x4)
        ) / det
        """
        This formula is derived from the equations of two lines in the form Ax + By = C. 
        By solving these equations using determinants, we can find the intersection point :DDDD!!
        """

        # Check if the intersection point lies within both line segments
        if (
            min(x1, x2) <= intersection_x <= max(x1, x2)
            and min(y1, y2) <= intersection_y <= max(y1, y2)
            and min(x3, x4) <= intersection_x <= max(x3, x4)
            and min(y3, y4) <= intersection_y <= max(y3, y4)
        ):
            return intersection_x, intersection_y

        return None, None

    def generate_normalized_wall_lines(self, wall_paths, start_point):
        n_wall_lines = np.array(
            [
                (
                    np.subtract(wall_path[0], start_point),
                    np.subtract(wall_path[1], start_point),
                )
                for wall_path in wall_paths
            ]
        )
        return n_wall_lines

    def sort_wall_lines_based_on_min_distance(self, n_wall_lines, travel_path_distance):
        # wall path distaces
        # between each point find the shortest distance
        # use that distance and compare it with other distances found via that method
        dis_arr = []  # tehcniqually just keys lol
        dis_dict = {}
        occur_dis_dict = {}
        sorted_n_wall_lines = []
        # example dict is {dis: [((x1,y1), (x2,y2) ), ....]}
        for line in n_wall_lines:
            # todo - idk why its max its supposed to be min but min gives odd results test with more cases
            dis = min(np.linalg.norm(line[0]), np.linalg.norm(line[1]))
            dis_arr.append(dis)

            if dis not in dis_dict:
                dis_dict[dis] = []
            dis_dict[dis].append(line)

        dis_arr = sorted(dis_arr)

        # print(dis_arr)

        new_keys_for_dis_dict = []
        for the_dis_in_array in dis_arr:
            if the_dis_in_array > travel_path_distance:
                break
            else:
                # the_dis_in_array < travel_path_distance
                new_keys_for_dis_dict.append(the_dis_in_array)

        # print(new_keys_for_dis_dict)

        for dis in new_keys_for_dis_dict:
            if dis not in occur_dis_dict:
                occur_dis_dict[dis] = 0

            lines = dis_dict[dis]
            line = lines[occur_dis_dict[dis]]
            sorted_n_wall_lines.append(line)

            occur_dis_dict[dis] += 1

        return sorted_n_wall_lines

    def checkIntersectionWithBlocks(self, start_point: tuple, end_point: tuple):
        """
        Args

        start_point
            start point (x,y)

        end_point
            end point (x,y)
        """
        # self.init()
        wall_paths = self.blocks

        n_end = np.subtract(end_point, start_point)

        n_wall_lines = self.generate_normalized_wall_lines(wall_paths, start_point)

        travel_path_distance = np.linalg.norm(n_end)

        sorted_n_wall_lines = self.sort_wall_lines_based_on_min_distance(
            n_wall_lines, travel_path_distance
        )

        sorted_wall_lines = np.array(sorted_n_wall_lines)
        # sorted_n_wall_lines = sorted_n_wall_lines_to_put_in_param.tolist()
        self.setSortedNWallLinesToDraw(sorted_wall_lines, start_point)
        #  sorted_n_wall_lines = np.array(sorted_n_wall_lines)

        intersection_points = []
        point_inter_wall_dct = {}
        walls_points_used = []

        for wall_line in sorted_wall_lines:
            # print([start_point, end_point])
            # print(wall_line)
            x, y = self.is_intersect(np.array([start_point, end_point]), wall_line)
            if not (x is None or y is None):
                intersection_points.append((x, y))
                point_inter_wall_dct[(x, y)] = wall_line.tolist()
                walls_points_used.append(wall_line.tolist()[0])
                walls_points_used.append(wall_line.tolist()[1])
        intersection_points = list(set(intersection_points))

        min_dis = 10000000
        dis_inter_point_dict = {}
        for p in intersection_points:
            if list(p) in walls_points_used:
                continue
            dis = np.linalg.norm(np.array(p) - np.array(start_point))
            dis_inter_point_dict[dis] = p
            min_dis = min(min_dis, dis)

        # print("---")
        # print("Line info: [start, stop]", start_point, end_point)
        # print("Line intersection points: ", intersection_points)
        # print(
        #     "[POINT INTER WALL DCT] (key: point, val: the wall's line's points (2)): ",
        #     point_inter_wall_dct,
        # )
        # print("Wall points used: " + str(walls_points_used))
        # print("Distance from inter point dict: ", dis_inter_point_dict)
        # print("Min dis: ", min_dis)

        return (
            dis_inter_point_dict.get(min_dis, (-1, -1)),
            point_inter_wall_dct.get(
                dis_inter_point_dict.get(min_dis, (-1, -1)), ((-1, -1), (-1, -1))
            ),
        )

    # collision detection, detect collision
    def startPointToGates(self):
        start_point = self.start
        gates = self.gates
        for gate in gates:
            # print(start_point, gate)
            inter_point = self.checkIntersectionWithBlocks(start_point, gate)
            # print(inter_point)
            # if inter_point[0] != -1 and inter_point[1] != -1:
            #     pass

    def giveMePathFromStartToEndPoint(
        self, path: list, start_point, end_point, prev_start_point=None
    ):
        if prev_start_point is not None:
            # check startpoint and prev_start_point
            # print("checking previous start point! ", prev_start_point)
            ret = self.checkIntersectionWithBlocks(prev_start_point, start_point)
            if ret[0][0] != -1 and ret[0][1] != -1:
                wall = ret[1]
                ip = ret[0]
                wallp1 = np.array(wall[0])
                wallp2 = np.array(wall[1])
                dis1 = np.linalg.norm(wallp1 - ip)
                dis2 = np.linalg.norm(wallp2 - ip)

                conditionp1 = np.logical_or(wallp1 < 0, wallp1 > Algorithm.SIZE)
                conditionp2 = np.logical_or(wallp2 < 0, wallp2 > Algorithm.SIZE)

                if np.any(conditionp1):
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp2.tolist()), end_point, start_point
                    )
                    return path
                elif np.any(conditionp2):
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp1.tolist()), end_point, start_point
                    )
                    return path

                if dis1 <= dis2:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp1.tolist()), end_point, start_point
                    )
                    return path
                elif dis2 < dis1:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp2.tolist()), end_point, start_point
                    )
                    return path
            else:
                return self.giveMePathFromStartToEndPoint(
                    path, start_point, end_point, None
                )
        else:
            path.append(start_point)
            ret = self.checkIntersectionWithBlocks(start_point, end_point)
            if ret[0][0] != -1 and ret[0][1] != -1:
                wall = ret[1]
                ip = ret[0]
                wallp1 = np.array(wall[0])
                wallp2 = np.array(wall[1])
                dis1 = np.linalg.norm(wallp1 - ip)
                dis2 = np.linalg.norm(wallp2 - ip)

                conditionp1 = np.logical_or(wallp1 < 0, wallp1 > Algorithm.SIZE)
                conditionp2 = np.logical_or(wallp2 < 0, wallp2 > Algorithm.SIZE)

                if np.any(conditionp1):
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp2.tolist()), end_point, start_point
                    )
                    return path
                elif np.any(conditionp2):
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp1.tolist()), end_point, start_point
                    )
                    return path

                wallp1_fail = False
                wallp2_fail = False
                for block_lines in self.block_lines_form:
                    x, y = self.is_intersect(
                        block_lines, (tuple(wallp1.tolist()), end_point)
                    )
                    if x is not None and y is not None:
                        wallp1_fail = True
                    x, y = self.is_intersect(
                        block_lines, (tuple(wallp2.tolist()), end_point)
                    )
                    if x is not None and y is not None:
                        wallp2_fail = True

                if wallp1_fail:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp2.tolist()), end_point, start_point
                    )
                    return path
                elif wallp2_fail:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp1.tolist()), end_point, start_point
                    )
                    return path

                if dis1 <= dis2:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp1.tolist()), end_point, start_point
                    )
                    return path
                elif dis2 < dis1:
                    self.giveMePathFromStartToEndPoint(
                        path, tuple(wallp2.tolist()), end_point, start_point
                    )
                    return path
            else:
                path.append(end_point)

                return path

    def run(self):
        self.init()

        #  line = [(75, 25), (25, 75)]
        # self.startPointToGates()
        # for gate in gates:
        #     print(self.start, gate)
        #     inter_point = self.checkIntersectionWithBlocks(self.start, gate)
        #     print(inter_point)

        path = []
        gate1 = self.gates[2]
        gate2 = self.gates[0]
        gate3 = self.gates[1]
        path = self.giveMePathFromStartToEndPoint(path, self.start, gate1)
        path = path[0 : len(path) - 1]
        path = self.giveMePathFromStartToEndPoint(path, gate1, gate2)
        path = path[0 : len(path) - 1]
        path = self.giveMePathFromStartToEndPoint(path, gate2, gate3)
        path = path[0 : len(path) - 1]
        path = self.giveMePathFromStartToEndPoint(path, gate3, self.stop)

        print(path)
        total_length = 0
        total_angulardistance = 0
        total_time = 0

        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i + 1]

            p1 = np.array(p1)
            p2 = np.array(p2)

            length = np.linalg.norm(p1 - p2)
            total_length += length

        for i in range(len(path) - 2):
            p1 = path[i]
            p2 = path[i + 1]
            p3 = path[i + 2]
            p1 = np.array(p1)
            p2 = np.array(p2)
            p3 = np.array(p3)

            pv1 = p2 - p1
            pv2 = p3 - p2

            angle = np.abs(
                np.arccos(
                    -1 * np.dot(pv1, pv2) / (np.linalg.norm(pv1) * np.linalg.norm(pv2))
                )
            )
            total_angulardistance += angle

        # print(total_length)
        # print(total_angulardistance)

        total_time = (
            total_length / Algorithm.VELOCITY
            + Algorithm.ROBOT_RADIUS
            * total_angulardistance
            / Algorithm.VELOCITY  # we can replace robot radius/velocuty as 1/angular velocity
            # centimeters
        )

        # angular displacement point i, point i+1, point i+2 -> good vectors by doing p1-p2 for each path. pv1 = p i +
        # angle = abs( arccos(-pv1 dot pv2 / length pv1 length pv2))

        # gate_dict = {}
        # gates = self.gates
        # for i in range(len(gates) - 1):
        #     gate1 = gates[i]
        #     gate2 = gates[i + 1]

        #     if i not in gate_dict:
        #         gate_dict[i] = []

        #     path = self.giveMePathFromStartToEndPoint([], self.start, gate1)
        #     path = self.giveMePathFromStartToEndPoint(path, gate1, gate2)
        #     path = self.giveMePathFromStartToEndPoint(path, gate2, self.stop)

        #     gate_dict[i].extend(path)

        # print(gate_dict)

        vis = Visualizer(
            self.blocks,
            self.start,
            self.stop,
            self.gates,
            self.block_lines_form,
            Algorithm.SIZE,
            path,
            total_length,
            total_time,
            total_angulardistance,
            Algorithm.VELOCITY
            # {"line": line},  # , "wall_lines": self.sorted_n_wall_lines_to_draw},
        )
        vis.run()


al = Algorithm()
al.run()
