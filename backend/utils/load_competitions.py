import json
import os


def load_competitions():
    current_dir = os.path.dirname(__file__)

    file_path = os.path.join(
        current_dir,
        "..",
        "data",
        "competitions.json"
    )

    file_path = os.path.abspath(file_path)

    with open(file_path, "r", encoding="utf-8") as f:
        competitions = json.load(f)

    return competitions