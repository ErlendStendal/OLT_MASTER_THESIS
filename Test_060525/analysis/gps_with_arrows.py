import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# --- Configurable values ---
input_file = "main_meter.csv"  # Replace with your CSV filename

# First section
start_time_1 = "13:16:50.000"
end_time_1 = "13:25:30.000"
estimated_onboard_wind_deg_1 = 308.2
true_wind_deg_1 = 290.3

# Second section
start_time_2 = "13:34:00.000"
end_time_2 = "13:47:30.000"
estimated_onboard_wind_deg_2 = 307.26
true_wind_deg_2 = 279.5

# --- Load data ---
df = pd.read_csv(input_file)
df["GPS_Time"] = df["GPS_Time"].astype(str)

# --- Highlight logic for two sections ---
def highlight_label(time_str):
    if start_time_1 <= time_str <= end_time_1:
        return "section1"
    elif start_time_2 <= time_str <= end_time_2:
        return "section2"
    return None

df["highlight"] = df["GPS_Time"].apply(highlight_label)

# --- Plot base and highlighted points ---
fig, ax = plt.subplots()

# Plot full track
ax.scatter(df[df["highlight"].isnull()]["X_meters"],
           df[df["highlight"].isnull()]["Y_meters"],
           s=10, c='lightgray', label="Complete path")

# Plot highlighted sections
ax.scatter(df[df["highlight"] == "section1"]["X_meters"],
           df[df["highlight"] == "section1"]["Y_meters"],
           s=10, c='orange', label="Selected tacks 1")

ax.scatter(df[df["highlight"] == "section2"]["X_meters"],
           df[df["highlight"] == "section2"]["Y_meters"],
           s=10, c='blue', label="Selected tacks 2")

ax.set_xlabel("X [m]", fontsize=18)
ax.set_ylabel("Y [m]", fontsize=18)
ax.tick_params(axis='both', which='major', labelsize=18)
ax.axis("equal")

# --- Add wind arrows ---
def polar_to_vector(angle_deg_from, length=150):
    angle_to = (angle_deg_from + 180) % 360
    adjusted_angle = 90 - angle_to
    angle_rad = np.radians(adjusted_angle)
    return np.cos(angle_rad) * length, np.sin(angle_rad) * length

# Arrow origins
x_origin_1 = -350
y_origin_1 = 350
x_origin_2 = -350
y_origin_2 = 1950

# Section 1 wind arrows
dx1, dy1 = polar_to_vector(estimated_onboard_wind_deg_1)
ax.arrow(x_origin_1 -50, y_origin_1 -200, dx1, dy1, head_width=6, head_length=12,
         fc='green', ec='green')
ax.text(x_origin_1 -50 + dx1, y_origin_1 + dy1 -200 +20, "EOWD 1", color='green', fontsize=18)

dx2, dy2 = polar_to_vector(true_wind_deg_1)
ax.arrow(x_origin_1 , y_origin_1 -150, dx2, dy2, head_width=6, head_length=12,
         fc='red', ec='red')
ax.text(x_origin_1 + dx2, y_origin_1 + dy2 -150 +20, "MWD 1", color='red', fontsize=18)

# Section 2 wind arrows
dx3, dy3 = polar_to_vector(estimated_onboard_wind_deg_2)
ax.arrow(x_origin_2 -50, y_origin_2 -200, dx3, dy3, head_width=6, head_length=12,
         fc='darkgreen', ec='darkgreen')
ax.text(x_origin_2 -50 + dx3, y_origin_2 + dy3 -200 +20, "EOWD 2", color='darkgreen', fontsize=18)

dx4, dy4 = polar_to_vector(true_wind_deg_2)
ax.arrow(x_origin_2, y_origin_2 -150, dx4, dy4, head_width=6, head_length=12,
         fc='darkred', ec='darkred')
ax.text(x_origin_2 + dx4, y_origin_2 + dy4 -150 +20, "MWD 2", color='darkred', fontsize=18)

ax.legend(fontsize=18)
plt.tight_layout()
plt.show()
