import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# --- CONFIGURATION ---

input_file = "tacks_meter_wind_VMG.csv"  # Change this
window_seconds = 5  # +/- seconds for each turn

# Paste your turn list here
turn_list_raw = """
1:09:32:10.857
2:09:32:20.571
3:09:32:38.857
4:09:32:53.000
5:09:33:16.500
6:09:33:27.167
7:09:33:46.667
8:09:34:10.000
9:09:35:11.400
10:09:35:39.667
11:09:36:02.429
12:09:36:17.286
13:09:36:36.167
14:09:36:42.600
"""

# --- Parse turn list ---
turn_times = []
for line in turn_list_raw.strip().splitlines():
    parts = line.strip().split(":")
    if len(parts) >= 2:
        time_str = ":".join(parts[1:])  # skip the number part
        turn_times.append(time_str)

turn_times_dt = [datetime.strptime(t, "%H:%M:%S.%f") for t in turn_times]

# --- Load CSV ---
df = pd.read_csv(input_file)

# Ensure GPS_Time is formatted
df["GPS_Time"] = df["GPS_Time"].astype(str)

# Convert GPS_Time to datetime
def to_datetime(t):
    try:
        return datetime.strptime(t, "%H:%M:%S.%f")
    except:
        return datetime.strptime(t, "%H:%M:%S")

df["GPS_Time_dt"] = df["GPS_Time"].apply(to_datetime)

# --- Create output folder ---
output_folder = "tacks"
os.makedirs(output_folder, exist_ok=True)

# --- Plotting ---
fig = go.Figure()

for idx, turn_time in enumerate(turn_times_dt):
    
    start_time = turn_time - timedelta(seconds=window_seconds)
    end_time = turn_time + timedelta(seconds=window_seconds)
    
    # Extract data within window
    mask = (df["GPS_Time_dt"] >= start_time) & (df["GPS_Time_dt"] <= end_time)
    turn_df = df[mask].copy()

    # Find the lat/lon at the EXACT turn timestamp (closest point)
    turn_point_row = df.loc[(df["GPS_Time_dt"] - turn_time).abs().idxmin()]
    lat_turn = turn_point_row["Lat"]
    lon_turn = turn_point_row["Lon"]

    # Normalize relative to turn point
    turn_df["Lat_Normalized"] = turn_df["Lat"] - lat_turn
    turn_df["Lon_Normalized"] = turn_df["Lon"] - lon_turn
    turn_df["Relative_Time"] = (turn_df["GPS_Time_dt"] - turn_time).dt.total_seconds()

    # --- Save to CSV (with ALL raw columns + normalized + relative time) ---
    output_file = os.path.join(output_folder, f"Turn_{idx+1:02d}.csv")
    turn_df.to_csv(output_file, index=False)

    # --- Plot ---
    fig.add_trace(go.Scatter(
        x=turn_df["Lon_Normalized"],
        y=turn_df["Lat_Normalized"],
        mode="lines+markers",
        name=f"Turn {idx + 1}",
        hovertext=turn_df["GPS_Time"]
    ))

fig.update_layout(
    title="Overlay of Turns (Lat vs Lon, aligned at turn point)",
    xaxis_title="Longitude (relative to turn point)",
    yaxis_title="Latitude (relative to turn point)",
    hovermode="closest",
    showlegend=True
)

fig.show()

print("All turns exported to folder:", output_folder)
