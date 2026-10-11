import json
import os
import pandas as pd

# ==========================================
# IPL PLAYER-SEASON DATASET CREATION
# ==========================================

# 1. Define project paths
PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "Raw Dataset",
    "All_Player_Stat_Season_wise_2016_to_2025.json"
)

OUTPUT_DIR = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data"
)

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "IPL_Player_Season_Summary.csv"
)

print("=" * 60)
print("IPL PLAYER-SEASON DATASET CREATION")
print("=" * 60)

# 2. Check whether the input file exists
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

# 3. Load the original JSON file
with open(INPUT_FILE, "r", encoding="utf-8") as file:
    data = json.load(file)

print("\nOriginal JSON file loaded successfully.")

# 4. Convert the data into player-season records
records = []

for player, seasons in data.items():

    if not isinstance(seasons, dict):
        continue

    for season, stats in seasons.items():

        if not isinstance(stats, dict):
            continue

        # Keep the player name and season
        record = {
            "Player": player,
            "Season": int(season)
        }

        # Keep scalar statistics.
        # List-valued statistics will be handled separately.
        for metric, value in stats.items():

            if not isinstance(value, (list, dict)):
                record[metric] = value

        records.append(record)

# 5. Create a pandas DataFrame
df = pd.DataFrame(records)

if df.empty:
    raise ValueError(
        "No player-season records were created. "
        "Check the structure of the JSON file."
    )

# 6. Sort records
df = df.sort_values(
    by=["Player", "Season"]
).reset_index(drop=True)

# 7. Create the output directory if necessary
os.makedirs(OUTPUT_DIR, exist_ok=True)

# 8. Export the dataset to CSV
df.to_csv(OUTPUT_FILE, index=False)

# 9. Display a summary
print("\nDATASET CREATED SUCCESSFULLY")
print("-" * 40)

print("Total player-season records:", len(df))
print("Total columns:", len(df.columns))

print("\nAvailable columns:")
print(df.columns.tolist())

print("\nFirst 10 records:")
print(df.head(10).to_string(index=False))

print("\nMissing values in the first 15 columns:")
print(df.isnull().sum().head(15))

print("\nCSV file saved at:")
print(OUTPUT_FILE)

print("\nPlayer-season dataset creation completed.")
