import os
import pandas as pd

# ==========================================
# IPL BATTING METRICS VALIDATION
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
print("IPL BATTING METRICS VALIDATION")
print("=" * 60)

# 1. Calculate strike rate independently
df["Calculated_Strike_Rate"] = (
    df["Total_Bt_Runs"]
    .div(df["Total_Bt_Balls"].replace(0, float("nan")))
    * 100
)

# 2. Compare calculated and original strike rates
df["Strike_Rate_Difference"] = (
    df["Bt_strike_rate"] - df["Calculated_Strike_Rate"]
).abs()

print("\n1. STRIKE RATE COMPARISON")
print("-" * 40)

print(
    "Records differing by more than 1 point:",
    (df["Strike_Rate_Difference"] > 1).sum()
)

print("\n2. STRIKE RATES ABOVE 300")
print("-" * 40)

high_strike_rates = df[
    df["Bt_strike_rate"] > 300
][
    [
        "Player",
        "Season",
        "Total_Bt_Runs",
        "Total_Bt_Balls",
        "Bt_strike_rate",
        "Calculated_Strike_Rate"
    ]
]

if high_strike_rates.empty:
    print("No records found.")
else:
    print(high_strike_rates.to_string(index=False))

# 3. Inspect the batting and bowling run totals
print("\n3. ROWS WHERE BATTING AND BOWLING RUNS MATCH")
print("-" * 40)

matching_runs = df[
    df["Total_Bt_Runs"] == df["Total_Bw_Runs"]
][
    [
        "Player",
        "Season",
        "Total_Bt_Runs",
        "Total_Bw_Runs"
    ]
]

print(matching_runs.to_string(index=False))

print("\nMetric checks completed.")
