import pandas as pd
import numpy as np
import plotly.graph_objects as go

def remove_outliers(series):
    """
    Remove outliers using IQR method.
    """
    Q1 = series.quantile(0.25)
    Q3 = series.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 2.5 * IQR
    upper_bound = Q3 + 2.5 * IQR
    return series[(series >= lower_bound) & (series <= upper_bound)]

# User defined timestamps
start_time = "2025-04-09 09:32:07"
end_time = "2025-04-09 09:36:46"

# Load wind direction CSV
wind_dir_file = "Wind_direction-data-2025-04-09_11_09_12.csv"
df = pd.read_csv(wind_dir_file)

# Clean wind direction (remove " °" and convert to integer)
df["Wind_Direction"] = df["meteo_wind_direction_munkholmen.mean"].str.replace(" °", "").astype(int)

# Convert Time to datetime
df["Time"] = pd.to_datetime(df["Time"])

# Filter by time range
start_time_dt = pd.to_datetime(start_time)
end_time_dt = pd.to_datetime(end_time)
df_filtered = df[(df["Time"] >= start_time_dt) & (df["Time"] <= end_time_dt)].copy()

# Calculate average of wind direction (after removing outliers)
original_values = df_filtered["Wind_Direction"]
wind_direction_no_outliers = remove_outliers(original_values)
average_direction = wind_direction_no_outliers.mean()

# Identify and print outliers removed
outliers_removed = original_values[~original_values.isin(wind_direction_no_outliers)]
print(f"Average Wind Direction (no outliers): {average_direction:.2f} degrees")
print("Outliers removed from average calculation:")
print(outliers_removed.to_string(index=False))

# Calculate median of wind direction (with outliers)
median_direction = original_values.median()
print(f"Median Wind Direction (with outliers): {median_direction:.2f} degrees")

# Plot
fig = go.Figure()

# Plot raw wind direction (without outlier removal)
fig.add_trace(go.Scatter(
    x=df_filtered["Time"],
    y=df_filtered["Wind_Direction"],
    mode='lines+markers',
    name='Raw Wind Direction'
))

# Plot average as horizontal line
fig.add_trace(go.Scatter(
    x=[df_filtered["Time"].min(), df_filtered["Time"].max()],
    y=[average_direction, average_direction],
    mode='lines',
    name='Average Wind Direction (No Outliers)',
    line=dict(dash='dash', color='red')
))

# Plot median as horizontal line
fig.add_trace(go.Scatter(
    x=[df_filtered["Time"].min(), df_filtered["Time"].max()],
    y=[median_direction, median_direction],
    mode='lines',
    name='Median Wind Direction (With Outliers)',
    line=dict(dash='dot', color='green')
))

fig.update_layout(
    title="Wind Direction with Average (Outliers Removed for Average Only)",
    xaxis_title="Time",
    yaxis_title="Wind Direction (degrees)",
    hovermode='x unified'
)

fig.show()
