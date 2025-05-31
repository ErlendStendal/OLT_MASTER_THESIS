import pandas as pd
import numpy as np
import plotly.graph_objs as go

# === CONFIGURATION ===
column = 'Pot2'  # Change to 'Pot2' to analyze Pot2 instead

# Load CSV
df = pd.read_csv("tacks_meter_wind.csv")

# Step 1: Main average
avg_main = df[column].mean()

# Step 2: Split the data
under_df = df[df[column] < avg_main]
over_df = df[df[column] > avg_main]

# Step 3: Sub-averages
avg_under = under_df[column].mean() if not under_df.empty else np.nan
avg_over = over_df[column].mean() if not over_df.empty else np.nan

# Step 4: Average of the sub-averages
avg_final = np.mean([avg_under, avg_over]) if not np.isnan(avg_under) and not np.isnan(avg_over) else np.nan

# Step 5: Plot
fig = go.Figure()

# Raw values
fig.add_trace(go.Scatter(
    y=df[column],
    mode='lines+markers',
    name=column
))

# Main average
fig.add_trace(go.Scatter(
    y=[avg_main] * len(df),
    mode='lines',
    name=f'Main Avg ≈ {avg_main:.2f}',
    line=dict(dash='dash', color='red')
))

# Under average
fig.add_trace(go.Scatter(
    y=[avg_under] * len(df),
    mode='lines',
    name=f'Under Avg ≈ {avg_under:.2f}',
    line=dict(dash='dot', color='blue')
))

# Over average
fig.add_trace(go.Scatter(
    y=[avg_over] * len(df),
    mode='lines',
    name=f'Over Avg ≈ {avg_over:.2f}',
    line=dict(dash='dot', color='green')
))

# Final between-subset average
fig.add_trace(go.Scatter(
    y=[avg_final] * len(df),
    mode='lines',
    name=f'Final Avg ≈ {avg_final:.2f}',
    line=dict(dash='dashdot', color='orange')
))

fig.update_layout(
    title=f"{column} and Subset Averages",
    xaxis_title="Sample Index",
    yaxis_title=f"{column} Value",
    template="plotly_white"
)

fig.show()

# Print results
print(f"Main average {column}: {avg_main:.2f}")
print(f"Under average {column}: {avg_under:.2f}")
print(f"Over average {column}: {avg_over:.2f}")
print(f"Average of under & over averages: {avg_final:.2f}")
