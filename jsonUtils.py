import json


def readInJson(fileName: str) -> dict:
    with open(fileName, "r") as f:
        return json.load(f)


def parseJson(fileName: str, newJson: dict) -> None:
    with open(fileName, "w") as f:
        json.dump(newJson, f, indent=4)
