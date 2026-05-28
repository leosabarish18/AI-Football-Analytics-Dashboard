import json
import os


def load_matches(competition_id):

    matches_folder = f"backend/data/matches/{competition_id}"

    if not os.path.exists(matches_folder):
        return []

    all_matches = []

    for file in os.listdir(matches_folder):

        if file.endswith(".json"):

            file_path = os.path.join(matches_folder, file)

            try:
                with open(file_path, "r", encoding="utf-8") as f:

                    data = json.load(f)

                    if isinstance(data, list):

                        for match in data:

                            match_id = match.get("match_id")

                            # CHECK EVENT FILE EXISTS
                            event_file = f"backend/data/events/{match_id}.json"

                            if os.path.exists(event_file):

                                all_matches.append(match)

            except Exception as e:
                print("ERROR:", e)

    return all_matches