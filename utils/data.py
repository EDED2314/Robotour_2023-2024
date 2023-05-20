import json
import os


def read_json_file(file_path):
    try:
        with open(file_path, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")
        return None
    except json.JSONDecodeError:
        print(f"Error decoding JSON data from '{file_path}'.")
        return None


def write_json_file(data, file_path):
    try:
        with open(file_path, "w+") as file:
            json.dump(data, file, indent=4)
        print(f"Data written to '{file_path}' successfully.")
    except:
        print(f"Error writing data to '{file_path}'.")


def initData():
    data = {}
    if not os.path.exists("nav.json"):
        data = {"blocks": [], "gates": [], "start": [0, 0], "stop": [0, 0]}
        write_json_file(data, "nav.json")
    else:
        data = read_json_file("nav.json")
    return data


def appendToBlocks(block):
    """Append block to blocks in nav.json

    Keyword arguments:
    block -- {
            "points" (In row, col format): [
                0,
                0,
                0,
                1
            ],
            "pos": "B"
        },
    Return: void
    """
    j = read_json_file("nav.json")
    j["blocks"].append(block)
    write_json_file(j, "nav.json")
    return


def modifyStartPoint(row, col):
    j = read_json_file("nav.json")
    j["start"] = [row, col]
    write_json_file(j, "nav.json")
    return


def modifyStopPoint(row, col):
    j = read_json_file("nav.json")
    j["stop"] = [row, col]
    write_json_file(j, "nav.json")
    return


def appendGate(row, col):
    j = read_json_file("nav.json")
    j["gates"].append([row, col])
    write_json_file(j, "nav.json")
    return


def delGate(row, col):
    j = read_json_file("nav.json")
    try:
        j["gates"].remove([row, col])
    except:
        print(
            f"[delGate() ERROR]: Couldn't remove [{row}, {col}]'s gate, probably does not exist."
        )
    write_json_file(j, "nav.json")
    return
