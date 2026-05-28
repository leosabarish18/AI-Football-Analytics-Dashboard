import json
import os

def load_competitions():
    file_path = os.path.join("data", "competitions.json")

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return data