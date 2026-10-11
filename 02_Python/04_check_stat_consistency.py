import json
import os
import pandas as pd

# ==========================================
# IPL STATISTICAL CONSISTENCY CHECK
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

JSON_FILE = os.path.join(
    PROJECT_DIR,
    "Raw Dataset",
    "All_Player_Stat_Season_wise_2016_to_2025.json"
)

CSV_FILE = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data",
    "IPL_Player_Season_Summary.csv"
)

# Load original JSON
with open(JSON_FILE, "r", encoding="utf-8") as file:
    original_data = json.load(file)

# Load player-season CSV
df = pd.read_csv(CSV_FILE)

print("=" * 60)
print("IPL STATISTICAL CONSISTENCY CHECK")
print("=" * 60)

# 1. Compare batting runs and bowling runs
print("\n1. BATING RUNS VS BOWLING RUNS")
print("-" * 40)

print(
    "Total batting runs:",
    df["Total_Bt_Runs"].sum()
)

print(
    "Total bowling runs:",
    df["Total_Bw_Runs"].sum()
)

print(
    "Rows where both values are equal:",
    (
        df["Total_Bt_Runs"]
        == df["Total_Bw_Runs"]
    ).sum()
)

# 2. Inspect the original JSON for selected players
print("\n2. ORIGINAL JSON RECORDS")
print("-" * 40)

sample_players = [
    "A Ashish Reddy",
    "A Badoni",
    "A Choudhary"
]

for player in sample_players:

    if player not in original_data:
        print(f"\nPlayer not found: {player}")
        continue

    print(f"\nPlayer: {player}")

    player_seasons = original_data[player]

    for season, stats in player_seasons.items():

        if not isinstance(stats, dict):
            continue

        print(f"Season: {season}")

        for key in [
            "Total_Bt_Runs",
            "Total_Bt_Balls",
            "Total_Bw_Runs",
            "Total_Bw_Balls",
            "Total_Matches"
        ]:
            print(f"  {key}: {stats.get(key, 'Not available')}")

# 3. Check batting averages and strike rates
print("\n3. BATTING METRIC CHECK")
print("-" * 40)

print(
    "Rows with positive balls but zero runs:",
    (
        (df["Total_Bt_Balls"] > 0)
        & (df["Total_Bt_Runs"] == 0)
    ).sum()
)

print(
    "Rows with positive runs but zero balls:",
    (
        (df["Total_Bt_Runs"] > 0)
        & (df["Total_Bt_Balls"] == 0)
    ).sum()
)

print(
    "Rows with strike rate above 300:",
    (df["Bt_strike_rate"] > 300).sum()
)

print("\nCheck completed.")

