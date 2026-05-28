import json
import os


def load_events(match_id):

    file_path = f"backend/data/events/{match_id}.json"

    print("Loading events:", file_path)

    if not os.path.exists(file_path):
        print("EVENT FILE NOT FOUND")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print("EVENT LOAD ERROR:", e)
        return []