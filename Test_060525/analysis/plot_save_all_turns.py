import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# --- CONFIGURATION ---

input_file = "tacks_meter_wind_VMG2.csv"  # Change this
window_seconds = 5  # +/- seconds for each turn

# Paste your turn list here
turn_list_raw = """
1:13:34:34.000
2:13:35:04.500
3:13:35:58.700
4:13:36:26.900
5:13:37:03.200
6:13:37:35.700
7:13:38:20.700
8:13:38:55.800
9:13:39:35.300
10:13:40:15.300
11:13:41:04.800
12:13:41:36.700
13:13:42:11.200
14:13:42:50.600
15:13:44:02.500
16:13:44:48.500
17:13:45:35.100
18:13:46:24.900
19:13:46:53.400
"""
# --- Create output folder ---
output_folder = "tacks2"
os.makedirs(output_folder, exist_ok=True)

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
