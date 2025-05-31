"""
This scripts adds milliseconds to the complete log csv file
Should be run before analyzing data.
"""

import pandas as pd
from datetime import datetime, timedelta

# Load CSV
input_file = "MAIN_complete_log_copy.csv"  # Change to your filename
output_file = "time_transformed_main_log_copy.csv"

# Read the CSV
df = pd.read_csv(input_file)

# Group by GPS_Time
grouped = df.groupby("GPS_Time")

new_times = []

# Process each group
for gps_time, group in grouped:
    count = len(group)
    
    # Calculate step in milliseconds (1000 ms total)
    if count == 1:
        steps = [0]
    else:
        steps = [int(round(i * 1000 / count)) for i in range(count)]
    
    for idx, step in enumerate(steps):
        # Create new timestamp with milliseconds
        time_obj = datetime.strptime(gps_time, "%H:%M:%S") + timedelta(milliseconds=step)
        new_time_str = time_obj.strftime("%H:%M:%S.%f")[:-3]  # Format to HH:MM:SS.mmm
        new_times.append(new_time_str)

# Replace GPS_Time with new times
df["GPS_Time"] = new_times

# Save to new CSV
df.to_csv(output_file, index=False)

print(f"Done! Saved with milliseconds to {output_file}")
