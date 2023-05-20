import heapq


def heuristic(start, goal):
    return abs(goal[0] - start[0]) + abs(goal[1] - start[1])


def get_neighbors(node, map_data):
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    neighbors = []
    for direction in directions:
        neighbor = (node[0] + direction[0], node[1] + direction[1])
        if is_valid_neighbor(neighbor, map_data):
            neighbors.append(neighbor)
    return neighbors


def is_valid_neighbor(neighbor, map_data):
    x, y = neighbor
    for block in map_data["blocks"]:
        points = block["points"]
        if points[0] <= x <= points[1] and points[0] <= y <= points[1]:
            return False
    return True


def find_path(map_data):
    start = tuple(map_data["start"])
    goal = tuple(map_data["stop"])

    open_list = [(0, start)]
    closed_set = set()
    g_score = {start: 0}
    f_score = {start: heuristic(start, goal)}
    came_from = {}

    while open_list:
        current = heapq.heappop(open_list)[1]

        if current == goal:
            return reconstruct_path(start, current, came_from)

        closed_set.add(current)

        for neighbor in get_neighbors(current, map_data):
            if neighbor in closed_set:
                continue

            tentative_g_score = g_score[current] + 5

            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score[neighbor], neighbor))

    return None


def reconstruct_path(start, current, came_from):
    path = [current]
    while current != start:
        current = came_from[current]
        path.append(current)
    return path[::-1]


def find_paths(map_data):
    paths = []
    gates = map_data["gates"]
    if len(gates) < 2:
        return paths

    for i in range(len(gates) - 1):
        new_map_data = map_data.copy()
        new_map_data["stop"] = gates[i]
        path = find_path(new_map_data)
        if path:
            paths.append(path)
            if len(paths) == 2:
                break
        new_map_data["start"] = gates[i]
        new_map_data["stop"] = gates[i + 1]
        path = find_path(new_map_data)
        if path:
            paths.append(path)
            if len(paths) == 2:
                break

    return paths


map_data = {
    "blocks": [
        {"points": [0, 1], "pos": "B"},
        {"points": [0, 1], "pos": "R"},
        {"points": [2, 3], "pos": "B"},
        {"points": [0, 2], "pos": "R"},
        {"points": [2, 2], "pos": "T"},
        {"points": [2, 2], "pos": "L"},
        {"points": [2, 1], "pos": "B"},
        {"points": [2, 0], "pos": "T"},
    ],
    "gates": [[0, 2], [2, 0], [2, 3]],
    "start": [3, 1],
    "stop": [0, 1],
}
paths = find_paths(map_data)
if paths:
    for i, path in enumerate(paths):
        time = (len(path) - 1) * 5
        print(f"Path {i+1}: {path}, Time: {time} seconds")
else:
    print("No viable paths found.")
