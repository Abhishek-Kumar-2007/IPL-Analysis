import os
import pandas as pd

# ==========================================
# IPL PLAYER-SEASON DATA VALIDATION
# ==========================================

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

INPUT_FILE = os.path.join(
    PROJECT_DIR,
    "03_Cleaned_Data",
    "IPL_Player_Season_Summary.csv"
)

print("=" * 60)
print("IPL PLAYER-SEASON DATA VALIDATION")
print("=" * 60)

# 1. Check whether the CSV exists
if not os.path.exists(INPUT_FILE):
    raise FileNotFoundError(
        f"Dataset not found: {INPUT_FILE}"
    )

# 2. Load the dataset
df = pd.read_csv(INPUT_FILE)

print("\n1. DATASET INFORMATION")
print("-" * 40)
print("Total rows:", len(df))
print("Total columns:", len(df.columns))
print("Column names:", df.columns.tolist())

# 3. Check missing values
print("\n2. MISSING VALUES")
print("-" * 40)
print(df.isnull().sum())

# 4. Check duplicate player-season records
print("\n3. DUPLICATE PLAYER-SEASON RECORDS")
print("-" * 40)

duplicate_count = df.duplicated(
    subset=["Player", "Season"]
).sum()

print("Duplicate records:", duplicate_count)

# 5. Check season range
print("\n4. SEASON RANGE")
print("-" * 40)
print("Earliest season:", df["Season"].min())
print("Latest season:", df["Season"].max())
print("Available seasons:", sorted(df["Season"].unique()))

# 6. Check negative values in numerical statistics
numeric_columns = [
    "Total_Bt_Runs",
    "Total_Bt_Balls",
    "Total_Bw_Runs",
    "Total_Bw_Balls",
    "Bt_Avg",
    "Bt_strike_rate",
    "Bw_economy",
    "Bw_wicket_per_match",
    "Total_Matches"
]

print("\n5. NEGATIVE VALUES")
print("-" * 40)

for column in numeric_columns:
    negative_count = (df[column] < 0).sum()
    print(f"{column}: {negative_count}")

# 7. Check records by season
print("\n6. PLAYER RECORDS BY SEASON")
print("-" * 40)
print(df.groupby("Season")["Player"].count())

# 8. Display basic statistics
print("\n7. NUMERICAL SUMMARY")
print("-" * 40)
print(df[numeric_columns].describe().round(2))

print("\nValidation checks completed.")
