import pandas as pd
import plotly.graph_objects as go

# User-defined time filter (EDIT THESE)
start_time = "2025-04-09 09:32:07"
end_time = "2025-04-09 09:36:46"

# Load wind direction CSV
wind_dir_file = "Wind_direction-data-2025-04-09_11_09_12.csv"
df_dir = pd.read_csv(wind_dir_file)

# Clean wind direction (remove " °" and convert to integer)
df_dir["meteo_wind_direction_munkholmen.mean"] = df_dir["meteo_wind_direction_munkholmen.mean"].str.replace(" °", "").astype(int)

# Load wind speed CSV
wind_speed_file = "Wind_speed-data-2025-04-09_11_07_13.csv"
df_speed = pd.read_csv(wind_speed_file)

# Merge the two dataframes on Time (outer join to keep all data)
df = pd.merge(df_speed, df_dir, on="Time", how="outer").sort_values("Time")

# Convert Time to datetime for filtering
df["Time"] = pd.to_datetime(df["Time"])
start_time = pd.to_datetime(start_time)
end_time = pd.to_datetime(end_time)

# Filter by time range
df_filtered = df[(df["Time"] >= start_time) & (df["Time"] <= end_time)]

# Create the plot
fig = go.Figure()

# Add wind speed trace
fig.add_trace(go.Scatter(
    x=df_filtered["Time"],
    y=df_filtered["Mean"],
    name="Wind Speed",
    yaxis="y1",
    mode='lines+markers'
))

# Add wind direction trace
fig.add_trace(go.Scatter(
    x=df_filtered["Time"],
    y=df_filtered["meteo_wind_direction_munkholmen.mean"],
    name="Wind Direction",
    yaxis="y2",
    mode='lines+markers'
))

# Update layout with two y-axes
fig.update_layout(
    title=f"Wind Speed and Direction ({start_time} to {end_time})",
    xaxis_title="Time",
    yaxis=dict(
        title="Wind Speed",
        side="left"
    ),
    yaxis2=dict(
        title="Wind Direction (deg)",
        overlaying="y",
        side="right"
    ),
    legend=dict(x=0.01, y=0.99),
    hovermode='x unified'
)

fig.show()
