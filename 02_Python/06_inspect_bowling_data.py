import json
import os

# ==========================================
# IPL BOWLING DATA INSPECTION
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "Raw Dataset",
    "All_Player_Stat_Season_wise_2016_to_2025.json"
)

with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

print("=" * 60)
print("IPL BOWLING DATA INSPECTION")
print("=" * 60)

# Find the first player-season record
for player, seasons in data.items():

    if not isinstance(seasons, dict):
        continue

    for season, stats in seasons.items():

        if not isinstance(stats, dict):
            continue

        print("\nPlayer:", player)
        print("Season:", season)

        print("\nBowling-related fields:")

        for key, value in stats.items():

            if "bw" in key.lower() or "bowl" in key.lower():
                print(f"{key}: {value}")

        # Inspect only one record for now
        raise SystemExit

print("No player-season records found.")
