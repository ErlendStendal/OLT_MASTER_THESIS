"""
This script opens up a browser window with the gps plot,
if you hover the mouse over the path the timestamp will show.
"""

import pandas as pd
import plotly.express as px

# Load CSV
input_file = "main_meter.csv"  # Change to your filename
df = pd.read_csv(input_file)

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

fig.show()
