import pandas as pd

# --- Configurable values ---
input_file = "gps_meter.csv"  # Change to your filename
output_file = "tacks.csv"

# Define time range (format HH:MM:SS or HH:MM:SS.mmm if needed)
start_time = "09:32:01.000"
end_time = "09:36:49.800"
# --- Load CSV ---
df = pd.read_csv(input_file)

# Ensure GPS_Time is string (important if has milliseconds)
df["GPS_Time"] = df["GPS_Time"].astype(str)

# --- Filter rows ---
filtered_df = df[(df["GPS_Time"] >= start_time) & (df["GPS_Time"] <= end_time)]

# --- Save to new CSV ---
filtered_df.to_csv(output_file, index=False)

print(f"Filtered data saved to {output_file}. Number of rows: {len(filtered_df)}")
