import sys


class PathFinder:
    def __init__(self, map_data):
        self.map = map_data["map"]
        self.blocks = map_data["blocks"]
        self.gates = map_data["gates"]
        self.start = map_data["start"]
        self.end = map_data["stop"]
        self.visited = set()
        self.max_gates = 0
        self.best_path = None

    def find_path(self):
        self.dfs(self.start, 0, 0, [])
        return self.best_path

    # def dfs(self, current, current_time, num_gates, path):
    #     if current_time > 60:
    #         return
    #     if current == tuple(self.end) and 50 <= current_time <= 60:
    #         if num_gates > self.max_gates:
    #             self.max_gates = num_gates
    #             self.best_path = path[:]
    #         return

    #     self.visited.add(tuple(current))
    #     for next_pos in self.get_neighbors(current):
    #         if tuple(next_pos) not in self.visited:
    #             next_time = current_time + self.get_travel_time(current, next_pos)
    #             next_gates = num_gates + self.get_gate_incentive(next_pos)
    #             self.dfs(next_pos, next_time, next_gates, path + [next_pos])
    #     self.visited.remove(tuple(current))

    def dfs(self, current, current_time, num_gates, path):
        if current == tuple(self.end):
            self.best_path = path[:]
            return

        self.visited.add(tuple(current))
        for next_pos in self.get_neighbors(current):
            if tuple(next_pos) not in self.visited:
                next_time = current_time + self.get_travel_time(current, next_pos)
                next_gates = num_gates + self.get_gate_incentive(next_pos)
                self.dfs(next_pos, next_time, next_gates, path + [next_pos])

    def get_neighbors(self, pos):
        x, y = pos
        neighbors = []
        if x > 0:
            neighbors.append((x - 1, y))
        if x < len(self.map) - 1:
            neighbors.append((x + 1, y))
        if y > 0:
            neighbors.append((x, y - 1))
        if y < len(self.map[0]) - 1:
            neighbors.append((x, y + 1))
        return neighbors

    def get_travel_time(self, pos1, pos2):
        x1, y1 = pos1
        x2, y2 = pos2
        block = self.get_block((x1, y1), (x2, y2))
        if block:
            return 5  # Travel time for a block
        return 1  # Travel time for an empty cell

    def get_gate_incentive(self, pos):
        x, y = pos
        if (x, y) in self.gates:
            return 1  # Increment for passing through a gate
        return 0

    def get_block(self, pos1, pos2):
        for block in self.blocks:
            points = block["points"]
            if (
                pos1[0] == points[0]
                and pos1[1] == points[1]
                and pos2[0] == points[2]
                and pos2[1] == points[3]
            ) or (
                pos1[0] == points[2]
                and pos1[1] == points[3]
                and pos2[0] == points[0]
                and pos2[1] == points[1]
            ):
                return block
        return None


# Example usage
map_data = {
    "map": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
    "blocks": [
        {"points": [1, 1, 2, 1], "pos": "L"},
        {"points": [2, 2, 3, 2], "pos": "R"},
        {"points": [1, 2, 1, 3], "pos": "B"},
    ],
    "gates": [[3, 3], [1, 2]],
    "start": [0, 2],
    "stop": [0, 1],
}

path_finder = PathFinder(map_data)
path = path_finder.find_path()
if path:
    print("Path found:")
    print(path)
else:
    print("No valid path found.")
