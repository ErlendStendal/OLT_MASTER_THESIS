import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyproj import Transformer
from datetime import timedelta

def plot_gps_drift(file_path):
    # Read the full file and trim to valid GPS data
    full_df = pd.read_csv(file_path)
    df = full_df.iloc[0:].copy()

    # Ensure Lat and Lon are floats
    df['Lat'] = df['Lat'].astype(float)
    df['Lon'] = df['Lon'].astype(float)

    # Filter out invalid GPS data
    df = df[(df['Lat'] != 0.0) & (df['Lon'] != 0.0)].copy()

    # Convert lat/lon to UTM coordinates (zone 32N - modify if needed)
    transformer = Transformer.from_crs("EPSG:4326", "EPSG:32632", always_xy=True)
    df['E'], df['N'] = transformer.transform(df['Lon'].values, df['Lat'].values)

    # Offset from starting point
    df['E_offset'] = df['E'] - df['E'].iloc[0]
    df['N_offset'] = df['N'] - df['N'].iloc[0]

    # Parse GPS_Time column
    df['GPS_Time'] = pd.to_datetime(df['GPS_Time'], format='%H:%M:%S', errors='coerce')
    df = df.dropna(subset=['GPS_Time'])

    # Limit to first 60 minutes
    start_time = df['GPS_Time'].iloc[0]
    df = df[df['GPS_Time'] <= start_time + timedelta(minutes=60)]

    # Select points every 5 minutes
    next_time = start_time + timedelta(minutes=5)
    label_indices = []
    for idx, time in enumerate(df['GPS_Time']):
        if time >= next_time:
            label_indices.append(idx)
            next_time += timedelta(minutes=5)

    # Include first point
    label_indices = [0] + label_indices

    # Prepare axis limits and grid
    x_min, x_max = df['E_offset'].min(), df['E_offset'].max()
    y_min, y_max = df['N_offset'].min(), df['N_offset'].max()
    x_ticks_major = np.arange(np.floor(x_min), np.ceil(x_max) + 1, 1)
    y_ticks_major = np.arange(np.floor(y_min), np.ceil(y_max) + 1, 1)
    x_ticks_minor = np.arange(np.floor(x_min), np.ceil(x_max) + 0.5, 0.5)
    y_ticks_minor = np.arange(np.floor(y_min), np.ceil(y_max) + 0.5, 0.5)

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 8))

    # Plot full path (light blue)
    ax.plot(df['E_offset'], df['N_offset'], marker='o', markersize=2, linestyle='-', linewidth=0.5, color='skyblue')

    # Plot and annotate timestamped points
    for idx in label_indices:
        time_str = df['GPS_Time'].iloc[idx].strftime('%H:%M')
        x = df['E_offset'].iloc[idx]
        y = df['N_offset'].iloc[idx]
        ax.plot(x, y, marker='o', color='steelblue', markersize=5)  # Emphasized point
        ax.annotate(
            time_str,
            (x, y),
            textcoords="offset points",
            xytext=(8, -6),
            ha='left',
            va='top',
            fontsize=7,
            rotation=25,
            bbox=dict(boxstyle="round,pad=0.2", edgecolor='none', facecolor='white', alpha=0.7)
        )

    # Grid and ticks
    ax.set_xticks(x_ticks_major)
    ax.set_yticks(y_ticks_major)
    ax.set_xticks(x_ticks_minor, minor=True)
    ax.set_yticks(y_ticks_minor, minor=True)
    ax.grid(which='major', linestyle='-', linewidth=0.6)
    ax.grid(which='minor', linestyle='--', linewidth=0.3)
    ax.set_xticklabels([str(int(t)) for t in x_ticks_major])
    ax.set_yticklabels([str(int(t)) for t in y_ticks_major])

    # Formatting
    ax.axhline(0, color='gray', linewidth=0.5)
    ax.axvline(0, color='gray', linewidth=0.5)
    ax.set_aspect('equal', adjustable='box')
    ax.set_xlabel('East offset (m)')
    ax.set_ylabel('North offset (m)')
    ax.set_title(f'GPS Drift (first 60 min): Test 3')
    plt.tight_layout()
    plt.show()

# Example usage:
plot_gps_drift("C:/Users/Karen/OLT_Pre_Project/Baseline_test_130425/log_1773.csv")
