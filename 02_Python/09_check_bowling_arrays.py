import json
import os

# ==========================================
# IPL BOWLING ARRAY VALIDATION
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
print("IPL BOWLING ARRAY VALIDATION")
print("=" * 60)

records_checked = 0
runs_match = 0
balls_match = 0
examples = []

for player, seasons in data.items():

    if not isinstance(seasons, dict):
        continue

    for season, stats in seasons.items():

        if not isinstance(stats, dict):
            continue

        runs_array = stats.get("Bw_Runs")
        balls_array = stats.get("Bw_Balls")

        if not isinstance(runs_array, list):
            continue

        if not isinstance(balls_array, list):
            continue

        records_checked += 1

        # Compare list sums with summary fields
        runs_sum = sum(runs_array)
        balls_sum = sum(balls_array)

        summary_runs = stats.get("Total_Bw_Runs")
        summary_balls = stats.get("Total_Bw_Balls")

        run_match = (
            summary_runs is not None
            and runs_sum == summary_runs
        )

        ball_match = (
            summary_balls is not None
            and balls_sum == summary_balls
        )

        if run_match:
            runs_match += 1

        if ball_match:
            balls_match += 1

        # Save a few examples for inspection
        if len(examples) < 10:
            examples.append({
                "Player": player,
                "Season": season,
                "Bw_Runs": runs_array,
                "Sum_Bw_Runs": runs_sum,
                "Total_Bw_Runs": summary_runs,
                "Bw_Balls": balls_array,
                "Sum_Bw_Balls": balls_sum,
                "Total_Bw_Balls": summary_balls
            })

print("\nRecords checked:", records_checked)
print("Bowling-run sums matching summary:", runs_match)
print("Bowling-ball sums matching summary:", balls_match)

print("\nSAMPLE RECORDS")
print("-" * 40)

for record in examples:
    print(record)

print("\nArray validation completed.")
