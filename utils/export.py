from utils.data import read_json_file, write_json_file, initRobotdata, initData
from constants import *

# 50 cm per square
# 4 x 4 squares


def convertToRobotableJson(path):
    initRobotdata()
    robo = initData()
    robo.__delitem__("gates")  # probably want to add it back
    # todo: implement actions
    blocks = robo.get("blocks", [])  # [x1,x2,y1,y2]
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
        real_x = points[0] * SQUARE_SIZE
        real_y = points[1] * SQUARE_SIZE
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

        new_blks.append([real_x, real_y, mod_x, mod_y])

    robo["start"] = [s * SQUARE_SIZE for s in robo["start"]]
    robo["stop"] = [s * SQUARE_SIZE for s in robo["stop"]]
    robo["blocks"] = new_blks
    robo["actions"] = new_actions

    boo = write_json_file(robo, path)

    return boo
