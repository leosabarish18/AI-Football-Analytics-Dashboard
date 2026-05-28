import json
import os

def load_matches(competition_id, season_id):

    folder_path = os.path.join(
        "data",
        "matches",
        str(competition_id)
    )

    if not os.path.exists(folder_path):
        return []

    season_file = os.path.join(
        folder_path,
        f"{season_id}.json"
    )

    if not os.path.exists(season_file):
        return []

    with open(season_file, "r", encoding="utf-8") as f:
        matches = json.load(f)

    return matches