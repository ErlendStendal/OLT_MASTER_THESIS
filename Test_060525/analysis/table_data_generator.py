import os
import pandas as pd
import numpy as np
from numpy import radians, degrees, sin, cos, arctan2

# Folder containing CSV files
folder_path = "tacks_converted_deg_ms"
output_csv = "tack_summary.csv"

# Define the custom processing order
file_order = [f"Turn_{i:02d}.csv" for i in [1, 3, 5, 7, 9, 11, 2, 4, 6, 8, 10, 12]]

# Function to calculate circular mean of angles (in degrees)
def circular_mean(degrees_array):
    radians_array = radians(degrees_array)
    sin_sum = np.mean(np.sin(radians_array))
    cos_sum = np.mean(np.cos(radians_array))
    mean_angle = np.arctan2(sin_sum, cos_sum)
    mean_deg = np.degrees(mean_angle) % 360
    return round(mean_deg)

# Function to process a single file
def process_file(file_path, tack_number, tack_side):
    df = pd.read_csv(file_path)

    df['Relative_Time'] = pd.to_numeric(df['Relative_Time'], errors='coerce')
    df = df.dropna(subset=['Relative_Time', 'SOG', 'Course', 'VMG', 'Rudder angle', 'Mast angle'])

    entry_window = df[df['Relative_Time'] <= 2]
    exit_window = df[df['Relative_Time'] >= df['Relative_Time'].max() - 2]

    entry_sog = round(entry_window['SOG'].mean(), 1)
    exit_sog = round(exit_window['SOG'].mean(), 1)

    entry_course = circular_mean(entry_window[entry_window['Relative_Time'] <= 1]['Course'])
    exit_course = circular_mean(exit_window[exit_window['Relative_Time'] >= df['Relative_Time'].max() - 1]['Course'])

    # Time from start until SOG reaches 80% of exit SOG, but only after min SOG
    sog_threshold = 0.8 * entry_sog
    sog_min_idx = df['SOG'].idxmin()
    sog_after_min = df.loc[sog_min_idx:]
    sog_80 = sog_after_min[sog_after_min['SOG'] >= sog_threshold]
    if not sog_80.empty:
        time_80 = sog_80['Relative_Time'].iloc[0]
        time_start = df['Relative_Time'].iloc[0]
        time_to_80 = round(time_80 - time_start, 1)
    else:
        time_to_80 = np.nan

    avg_sog = round(df['SOG'].mean(), 1)
    avg_vmg = round(df['VMG'].mean(), 1)

    rudder_delta = round(df['Rudder angle'].max() - df['Rudder angle'].min())
    mast_delta = round(df['Mast angle'].max() - df['Mast angle'].min())

    return {
        "Tack number": tack_number,
        "Tack side": tack_side,
        "Entry SOG": entry_sog,
        "Exit SOG": exit_sog,
        "Entry course": entry_course,
        "Exit course": exit_course,
        "Time until 80% SOG": time_to_80,
        "Avg SOG": avg_sog,
        "Avg VMG": avg_vmg,
        "Rudder angle delta": rudder_delta,
        "Mast angle delta": mast_delta
    }

# Process all files and store results
summary = []

for i, filename in enumerate(file_order):
    tack_number = int(filename.split("_")[1].split(".")[0])
    tack_side = "Starboard" if i < 6 else "Port"
    file_path = os.path.join(folder_path, filename)
    
    if os.path.exists(file_path):
        result = process_file(file_path, tack_number, tack_side)
        summary.append(result)
    else:
        print(f"Warning: File {filename} not found.")

# Create output DataFrame and export to CSV
summary_df = pd.DataFrame(summary)
summary_df.to_csv(output_csv, index=False)
print(f"Summary exported to '{output_csv}'")
