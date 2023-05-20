from utils.data import read_json_file, write_json_file, initRobotdata, initData

SQUARE_SIZE = 50  # 50 cm per square
# 4 x 4 squares


def convertToRobotableJson():
    initRobotdata()
    robo = initData()
    blocks = robo.get("blocks", [])  # [x1,x2,y1,y2]
    new_blks = []
    for block in blocks:
        points = block["points"]
        pos = block["pos"]
        real_x = points[0] * SQUARE_SIZE
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

        new_blks.append([real_x, real_y, mod_x, mod_y])

    robo["start"] = [s * SQUARE_SIZE for s in robo["start"]]
    robo["stop"] = [s * SQUARE_SIZE for s in robo["stop"]]
    robo["points"] = new_blks

    write_json_file(robo, "robo.json")

    return
