import pandas as pd
from scipy.stats import zscore

# Load CSV
file_path = "test_090425.csv"  # <-- Replace with your file
df = pd.read_csv(file_path)

# Convert GPS time to datetime (if needed)
df["GPS_Time"] = pd.to_datetime(df["GPS_Time"], format="%H:%M:%S.%f")

# --- Choose column(s) to check for outliers ---
target_column = "Lon"  # Change to e.g. 'Speed', 'Pot1', 'GyroX', etc.

# Compute z-scores
df["z_score"] = zscore(df[target_column])

# Mark outliers where abs(z-score) > threshold (common threshold = 3)
threshold = 30
outliers = df[abs(df["z_score"]) > threshold]

# Print results
if not outliers.empty:
    print(f"Outliers found in column '{target_column}':")
    print(outliers[["GPS_Time", target_column, "z_score"]])
else:
    print(f"No outliers detected in '{target_column}'.")

# Optional: Save outliers to CSV
# outliers.to_csv("outliers_detected.csv", index=False)
