from utils.data import read_json_file, write_json_file, initRobotdata, initData
from constants import *

# 50 cm per square
# 4 x 4 squares


def convertToRobotableJson(path):
    initRobotdata()
    robo = initData()  # (dict[str, Any] | Any | None)
    gates = robo.get("gates", [])
    new_gates = []
    for gate in gates:
        x = gate[0] * SQUARE_SIZE
        y = gate[1] * SQUARE_SIZE
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2

        new_gates.append([center_x, center_y])

    blocks = robo.get("blocks", [])
    new_blks = []
    actions = robo.get("actions", [])
    new_actions = []
    for action in actions:
        act = {"start": [], "stop": []}
        cell = action["points"]
        d = action["direction"]
        x = cell[0] * SQUARE_SIZE
        y = cell[1] * SQUARE_SIZE
        center_x = x + SQUARE_SIZE // 2
        center_y = y + SQUARE_SIZE // 2
        if d == "F":
            act["start"] = [center_x, y + SQUARE_SIZE]
            act["stop"] = [center_x, y]
        elif d == "B":
            act["start"] = [center_x, y]
            act["stop"] = [center_x, y + SQUARE_SIZE]
        elif d == "L":
            act["start"] = [x + SQUARE_SIZE, center_y]
            act["stop"] = [x, center_y]
        elif d == "R":
            act["start"] = [x, center_y]
            act["stop"] = [x + SQUARE_SIZE, center_y]

        new_actions.append(act)

    for block in blocks:
        points = block["points"]
        pos = block["pos"]
        real_x = points[1] * SQUARE_SIZE
        real_y = points[0] * SQUARE_SIZE
        mod_x = real_x
        mod_y = real_y

        if pos == "T":
            mod_x = real_x + SQUARE_SIZE
        elif pos == "B":
            mod_x = real_x + SQUARE_SIZE
            real_y += SQUARE_SIZE
            mod_y += SQUARE_SIZE
        elif pos == "L":
            mod_y = real_y + SQUARE_SIZE
        elif pos == "R":
            mod_y = real_y + SQUARE_SIZE
            real_x += SQUARE_SIZE
            mod_x += SQUARE_SIZE

        print(block)
        print([real_x, real_y, mod_x, mod_y])
        new_blks.append([real_x, real_y, mod_x, mod_y])

    start_x = robo["start"][0] * SQUARE_SIZE
    start_y = robo["start"][1] * SQUARE_SIZE
    start_side = robo["start"][2]

    start_center_x = start_x + SQUARE_SIZE // 2
    start_center_y = start_y + SQUARE_SIZE // 2

    actual_start_x = start_x
    actual_start_y = start_y

    if start_side == "mid":
        actual_start_x, actual_start_y = start_center_x, start_center_y
    elif start_side == "top":
        actual_start_x, actual_start_y = start_center_x, start_y
    elif start_side == "bottom":
        actual_start_x, actual_start_y = start_center_x, start_y + SQUARE_SIZE
    elif start_side == "left":
        actual_start_x, actual_start_y = start_x, start_center_y
    elif start_side == "right":
        actual_start_x, actual_start_y = start_x + SQUARE_SIZE, start_center_y

    stop_x = robo["stop"][0] * SQUARE_SIZE
    stop_y = robo["stop"][1] * SQUARE_SIZE
    stop_side = robo["stop"][2]

    stop_center_x = stop_x + SQUARE_SIZE // 2
    stop_center_y = stop_y + SQUARE_SIZE // 2

    actual_stop_x = stop_x
    actual_stop_y = stop_y

    if stop_side == "mid":
        actual_stop_x, actual_stop_y = stop_center_x, stop_center_y
    elif stop_side == "top":
        actual_stop_x, actual_stop_y = stop_center_x, stop_y
    elif stop_side == "bottom":
        actual_stop_x, actual_stop_y = stop_center_x, stop_y + SQUARE_SIZE
    elif stop_side == "left":
        actual_stop_x, actual_stop_y = stop_x, start_center_y
    elif stop_side == "right":
        actual_stop_x, actual_stop_y = stop_x + SQUARE_SIZE, stop_center_y

    robo["start"] = [actual_start_y, actual_start_x]
    robo["stop"] = [actual_stop_y, actual_stop_x]
    robo["blocks"] = new_blks
    robo["actions"] = new_actions
    robo["gates"] = new_gates

    boo = write_json_file(robo, path)

    return boo
