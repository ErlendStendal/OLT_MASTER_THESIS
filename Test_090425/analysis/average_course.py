import pandas as pd
import numpy as np
import plotly.graph_objs as go

def circular_mean(degrees):
    radians = np.deg2rad(degrees)
    mean_sin = np.mean(np.sin(radians))
    mean_cos = np.mean(np.cos(radians))
    mean_rad = np.arctan2(mean_sin, mean_cos)
    mean_deg = np.rad2deg(mean_rad)
    return ((mean_deg + 180) % 360) - 180  # Normalize to [-180, 180]

# Load CSV
df = pd.read_csv("tacks_meter_wind.csv")

# Convert Course to [-180, 180]
df['Course_deg'] = ((df['Course'] + 180) % 360) - 180

# Step 1: Main average
avg_main = circular_mean(df['Course_deg'])

# Step 2: Split the data
under_df = df[df['Course_deg'] < avg_main]
over_df = df[df['Course_deg'] > avg_main]

# Step 3: Sub-averages
avg_under = circular_mean(under_df['Course_deg']) if not under_df.empty else np.nan
avg_over = circular_mean(over_df['Course_deg']) if not over_df.empty else np.nan

# Step 4: Average of the sub-averages
avg_final = circular_mean([avg_under, avg_over]) if not np.isnan(avg_under) and not np.isnan(avg_over) else np.nan

# Step 5: Plot
fig = go.Figure()

# Raw course
fig.add_trace(go.Scatter(
    y=df['Course_deg'],
    mode='lines+markers',
    name='Course [-180°, 180°]'
))

# Main average
fig.add_trace(go.Scatter(
    y=[avg_main] * len(df),
    mode='lines',
    name=f'Main Avg ≈ {avg_main:.2f}°',
    line=dict(dash='dash', color='red')
))

# Under average
fig.add_trace(go.Scatter(
    y=[avg_under] * len(df),
    mode='lines',
    name=f'Under Avg ≈ {avg_under:.2f}°',
    line=dict(dash='dot', color='blue')
))

# Over average
fig.add_trace(go.Scatter(
    y=[avg_over] * len(df),
    mode='lines',
    name=f'Over Avg ≈ {avg_over:.2f}°',
    line=dict(dash='dot', color='green')
))

# Final between-subset average
fig.add_trace(go.Scatter(
    y=[avg_final] * len(df),
    mode='lines',
    name=f'Final Avg ≈ {avg_final:.2f}°',
    line=dict(dash='dashdot', color='orange')
))

fig.update_layout(
    title="Course and Circular Averages",
    xaxis_title="Sample Index",
    yaxis_title="Course (°)",
    yaxis=dict(range=[-180, 180]),
    template="plotly_white"
)

fig.show()

# Print results
print(f"Main average course: {avg_main:.2f}°")
print(f"Under average course: {avg_under:.2f}°")
print(f"Over average course: {avg_over:.2f}°")
print(f"Average of under & over averages: {avg_final:.2f}°")
