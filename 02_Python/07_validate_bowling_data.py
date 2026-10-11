import json
import os
import pandas as pd

# ==========================================
# IPL BOWLING DATA VALIDATION
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

with open(JSON_FILE, "r", encoding="utf-8") as file:
    original_data = json.load(file)

df = pd.read_csv(CSV_FILE)

print("=" * 60)
print("IPL BOWLING DATA VALIDATION")
print("=" * 60)

# 1. Check whether summary values match the original JSON
mismatches = []

for _, row in df.iterrows():

    player = row["Player"]
    season = str(row["Season"])

    stats = original_data.get(player, {}).get(season, {})

    for column in [
        "Total_Bw_Runs",
        "Total_Bw_Balls",
        "Bw_economy",
        "Bw_wicket_per_match"
    ]:
        original_value = stats.get(column)
        csv_value = row[column]

        if original_value is None:
            mismatches.append(
                (player, season, column, "Missing in JSON", csv_value)
            )
        elif abs(float(original_value) - float(csv_value)) > 0.01:
            mismatches.append(
                (player, season, column, original_value, csv_value)
            )

print("\n1. SUMMARY VALUES VS ORIGINAL JSON")
print("-" * 40)
print("Mismatches:", len(mismatches))

for mismatch in mismatches[:10]:
    print(mismatch)

# 2. Count records with no bowling balls
print("\n2. RECORDS WITH ZERO BOWLING BALLS")
print("-" * 40)

zero_balls = (df["Total_Bw_Balls"] == 0).sum()
print("Records with zero bowling balls:", zero_balls)

# 3. Count records with bowling balls but zero runs conceded
print("\n3. BOWLING BALLS BUT ZERO RUNS")
print("-" * 40)

condition = (
    (df["Total_Bw_Balls"] > 0)
    & (df["Total_Bw_Runs"] == 0)
)

print("Records:", condition.sum())

# 4. Compare the overall totals
print("\n4. OVERALL BOWLING TOTALS")
print("-" * 40)

print("Total bowling runs:", df["Total_Bw_Runs"].sum())
print("Total bowling balls:", df["Total_Bw_Balls"].sum())
print("Total batting runs:", df["Total_Bt_Runs"].sum())

print("\nValidation completed.")
