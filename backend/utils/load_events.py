import json
import os


def load_events(match_id):

    file_path = os.path.join(
        "data",
        "events",
        f"{match_id}.json"
    )

    if not os.path.exists(file_path):
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Ensure correct format
        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print("Error loading events:", e)
        return []