import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configurable values ---
input_file = "gps_meter.csv"  # Replace with your CSV filename
start_time = "09:32:07.000"
end_time = "09:36:46.800"
estimated_onboard_wind_deg = 317.9
true_wind_deg = 340

# --- Load data ---
df = pd.read_csv(input_file)
df["GPS_Time"] = df["GPS_Time"].astype(str)

# --- Highlight logic ---
def highlight_row(time_str):
    return start_time <= time_str <= end_time

df["highlight"] = df["GPS_Time"].apply(highlight_row)

# --- Plot base and highlighted points ---
fig, ax = plt.subplots()

# Plot full track
ax.scatter(df[~df["highlight"]]["X_meters"],
           df[~df["highlight"]]["Y_meters"],
           s=10, c='lightgray', label="Complete path")

# Plot highlighted section
ax.scatter(df[df["highlight"]]["X_meters"],
           df[df["highlight"]]["Y_meters"],
           s=10, c='orange', label="Selected tacks")

ax.set_xlabel("X [m]", fontsize=18)
ax.set_ylabel("Y [m]", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
ax.axis("equal")

# --- Add wind arrows ---
def polar_to_vector(angle_deg_from, length=150):
    # Convert 'from' direction to 'to' direction
    angle_to = (angle_deg_from + 180) % 360
    # Adjust to standard unit circle (0° = east, so 90 - angle for 0° = north)
    adjusted_angle = 90 - angle_to
    angle_rad = np.radians(adjusted_angle)
    return np.cos(angle_rad) * length, np.sin(angle_rad) * length

# Arrow origin
x_origin = -600
y_origin = 400

# Estimated onboard wind direction
dx1, dy1 = polar_to_vector(estimated_onboard_wind_deg)
ax.arrow(x_origin - 100, y_origin - 200, dx1, dy1, head_width=6, head_length=12,
         fc='green', ec='green')
ax.text(x_origin + dx1 + 10 - 100, y_origin + dy1 - 200, "EOWD", color='green', fontsize=18)

# Measured wind direction
dx2, dy2 = polar_to_vector(true_wind_deg)
ax.arrow(x_origin - 250, y_origin + 30 - 240, dx2, dy2, head_width=6, head_length=12,
         fc='red', ec='red')
ax.text(x_origin - 250 + dx2 + 10, y_origin + dy2 + 30 - 240, "MWD", color='red', fontsize=18)

ax.legend(fontsize=18)
plt.tight_layout()
plt.show()
