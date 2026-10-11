import pandas as pd
import json
import os

# Find the main project folder
PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Path to the original JSON dataset
file_path = os.path.join(
    PROJECT_DIR,
    "Raw Dataset",
    "All_Player_Stat_Season_wise_2016_to_2025.json"
)

print("=" * 60)
print("IPL DATA UNDERSTANDING")
print("=" * 60)

# Check whether the file exists
if not os.path.exists(file_path):
    print("\nERROR: Dataset file not found!")
    print("Expected location:", file_path)
    raise SystemExit(1)

# Load the original JSON data
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

print("\n1. JSON DATA TYPE")
print(type(data).__name__)

# Convert the JSON data into a DataFrame
if isinstance(data, list):
    df = pd.json_normalize(data)

elif isinstance(data, dict):
    df = pd.json_normalize(
        [{"Player": player, **stats}
         for player, stats in data.items()]
    )

else:
    raise ValueError("Unexpected JSON structure.")

print("\n2. FIRST FIVE ROWS")
print(df.head().to_string())

print("\n3. DATASET SHAPE")
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

print("\n4. COLUMN NAMES")
print(df.columns.tolist())

print("\n5. DATA TYPES")
print(df.dtypes)

print("\n6. MISSING VALUES")
print(df.isnull().sum())

print("\n7. DUPLICATE ROWS")
print("Duplicate player names:", df["Player"].duplicated().sum())

print("\n8. NUMERICAL DESCRIPTIVE STATISTICS")
print(df.describe().T)

print("\n9. DATA UNDERSTANDING COMPLETED")
print("Original JSON file was read without modification.")
