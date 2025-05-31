import pandas as pd
import plotly.express as px

# --- Configurable values ---
input_file = "gps_meter.csv"  # Change to your CSV filename

# Define the time window for highlighting (format: HH:MM:SS or HH:MM:SS.mmm if needed)
start_time = "09:32:07.000"
end_time = "09:36:46.800"

# --- Load data ---
df = pd.read_csv(input_file)

# Ensure GPS_Time is treated as string for easy comparison
df["GPS_Time"] = df["GPS_Time"].astype(str)

# Create a new column for color tagging
def highlight_row(time_str):
    if start_time <= time_str <= end_time:
        return "Highlighted"
    else:
        return "Normal"

df["ColorGroup"] = df["GPS_Time"].apply(highlight_row)

# --- Plot using Plotly ---
fig = px.scatter(df, 
                 x="Lon", 
                 y="Lat", 
                 color="ColorGroup", 
                 hover_data=["GPS_Time"],
                 title=f"Lat vs Lon (highlighting from {start_time} to {end_time})")

fig.update_layout(
    xaxis_title="Longitude",
    yaxis_title="Latitude",
    hovermode='closest'
)

fig.show()
