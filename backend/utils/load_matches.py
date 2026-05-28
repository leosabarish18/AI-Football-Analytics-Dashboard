import json
import os


def load_matches(competition_id, season_id):

    file_path = f"backend/data/matches/{competition_id}/{season_id}.json"

    # DEBUG
    print("Loading:", file_path)

    if not os.path.exists(file_path):
        print("FILE NOT FOUND")
        return []

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data

        return []

    except Exception as e:
        print("MATCH LOAD ERROR:", e)
        return []