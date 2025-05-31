import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# Load CSV
input_file = "tacks_meter.csv"  # Change to your filename
df = pd.read_csv(input_file)

# Wind direction in degrees (meteorological direction: 0 = from North, 90 = from East, etc)
wind_direction_deg = 317.9  # Example: wind coming from the southeast (135°)

# Convert wind direction to radians (convert to "to" direction)
wind_direction_rad = np.radians((wind_direction_deg + 180) % 360)

# Vector length (in meters, you can adjust this)
vector_length = 200

# Calculate vector end point
x_start = df.loc[df.index[-1], "X_meters"]
y_start = df.loc[df.index[-1], "Y_meters"]
x_end = x_start + vector_length * np.sin(wind_direction_rad)
y_end = y_start + vector_length * np.cos(wind_direction_rad)

# Create scatter plot with hover showing GPS_Time
fig = px.scatter(df, 
                 x="X_meters", 
                 y="Y_meters", 
                 hover_data=["GPS_Time"],
                 title="Lat vs Lon Plot with Timestamp on Hover")

fig.update_layout(
    xaxis_title="[m]",
    yaxis_title="[m]",
    hovermode='closest'
)

fig.update_yaxes(scaleanchor="x", scaleratio=1)

# Add wind direction vector
fig.add_trace(go.Scatter(
    x=[x_start, x_end],
    y=[y_start, y_end],
    mode="lines+markers",
    name=f"Wind Direction ({wind_direction_deg}°)",
    line=dict(color="red", width=3),
    marker=dict(size=8)
))

fig.show()
