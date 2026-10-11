import os
import pandas as pd

# ==========================================
# INVESTIGATE IPL BOWLING RUNS
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data",
    "IPL_Player_Season_Summary.csv"
)

df = pd.read_csv(INPUT_FILE)

print("=" * 60)
print("INVESTIGATION OF BOWLING RUNS")
print("=" * 60)

# 1. Show the highest bowling-run totals
print("\n1. TOP 15 BOWLING-RUN TOTALS")
print("-" * 40)

top_bowlers = df.sort_values(
    "Total_Bw_Runs",
    ascending=False
)[
    [
        "Player",
        "Season",
        "Total_Bw_Runs",
        "Total_Bw_Balls",
        "Bw_economy",
        "Bw_wicket_per_match"
    ]
].head(15)

print(top_bowlers.to_string(index=False))

# 2. Show the highest batting-run totals
print("\n2. TOP 15 BATTING-RUN TOTALS")
print("-" * 40)

top_batters = df.sort_values(
    "Total_Bt_Runs",
    ascending=False
)[
    [
        "Player",
        "Season",
        "Total_Bt_Runs",
        "Total_Bt_Balls",
        "Bt_Avg",
        "Bt_strike_rate"
    ]
].head(15)

print(top_batters.to_string(index=False))

# 3. Compare bowling and batting runs by season
print("\n3. RUN TOTALS BY SEASON")
print("-" * 40)

season_totals = df.groupby("Season").agg(
    Batting_Runs=("Total_Bt_Runs", "sum"),
    Bowling_Runs=("Total_Bw_Runs", "sum"),
    Bowling_Balls=("Total_Bw_Balls", "sum")
)

season_totals["Run_Difference"] = (
    season_totals["Batting_Runs"]
    - season_totals["Bowling_Runs"]
)

print(season_totals.to_string())

# 4. Check bowling runs when no balls were bowled
print("\n4. BOWLING RUNS WITH ZERO BOWLING BALLS")
print("-" * 40)

unusual = df[
    (df["Total_Bw_Balls"] == 0)
    & (df["Total_Bw_Runs"] > 0)
][
    [
        "Player",
        "Season",
        "Total_Bw_Runs",
        "Total_Bw_Balls",
        "Bw_economy"
    ]
]

print("Number of records:", len(unusual))

if not unusual.empty:
    print(unusual.head(20).to_string(index=False))

print("\nInvestigation completed.")