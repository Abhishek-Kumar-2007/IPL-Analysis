import os
import pandas as pd

# ==========================================
# IPL ANALYSIS DATASET PREPARATION
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data",
    "IPL_Player_Season_Summary.csv"
)

OUTPUT_FILE = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data",
    "IPL_Player_Season_Analysis.csv"
)

print("=" * 60)
print("IPL ANALYSIS DATASET PREPARATION")
print("=" * 60)

# 1. Load the validated dataset
df = pd.read_csv(INPUT_FILE)

# 2. Create additional performance metrics
df["Batting_Runs_Per_Match"] = (
    df["Total_Bt_Runs"]
    / df["Total_Matches"]
)

df["Batting_Balls_Per_Match"] = (
    df["Total_Bt_Balls"]
    / df["Total_Matches"]
)

df["Bowling_Balls_Per_Match"] = (
    df["Total_Bw_Balls"]
    / df["Total_Matches"]
)

# 3. Flag matching batting and bowling run totals
df["Run_Total_Review_Flag"] = (
    df["Total_Bt_Runs"] == df["Total_Bw_Runs"]
).map({
    True: "Review",
    False: "No Match"
})

# 4. Sort the dataset
df = df.sort_values(
    ["Season", "Player"]
).reset_index(drop=True)

# 5. Save the analysis dataset
df.to_csv(OUTPUT_FILE, index=False)

# 6. Display results
print("\nAnalysis dataset created successfully.")

print("Total records:", len(df))
print("Total columns:", len(df.columns))

print("\nRecords flagged for run-total review:")
print(
    (df["Run_Total_Review_Flag"] == "Review").sum()
)

print("\nSample records:")
print(df.head(10).to_string(index=False))

print("\nFile saved at:")
print(OUTPUT_FILE)
