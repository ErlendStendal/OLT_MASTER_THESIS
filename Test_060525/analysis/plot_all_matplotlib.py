import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("tacks_meter_wind_VMG_deg2.csv")

# Convert GPS_Time to datetime with milliseconds
df["GPS_Time"] = pd.to_datetime(df["GPS_Time"], format="%H:%M:%S.%f")

# Plotting
fig, axs = plt.subplots(5, 1, figsize=(12, 18), sharex=True)
#fig, axs = plt.subplots(6, 1, figsize=(12, 18), sharex=True)
# Potentiometers
axs[0].plot(df["GPS_Time"], df["Rudder angle"], label="Rudder angle")
axs[0].plot(df["GPS_Time"], df["GN angle"], label="GN angle")
axs[0].set_ylabel("Angle [deg]")
axs[0].legend()
axs[0].grid(True)

# Speed
axs[1].plot(df["GPS_Time"], df["SOG"], label="SOG", color="tab:blue")
axs[1].set_ylabel("velocity [m/s]")
axs[1].legend()
axs[1].grid(True)

# Normalize Course to range [-180, 180]
df["Course_normalized"] = (df["Course"] + 180) % 360 - 180

# Course
axs[2].plot(df["GPS_Time"], df["Course_normalized"], label="Course", color="tab:orange")
axs[2].set_ylabel("Course [deg]]")
axs[2].legend()
axs[2].grid(True)


# Accelerometer
axs[3].plot(df["GPS_Time"], df["AccelX"], label="X")
axs[3].plot(df["GPS_Time"], df["AccelY"], label="Y")
axs[3].plot(df["GPS_Time"], df["AccelZ"], label="Z")
axs[3].set_ylabel("Acceleration [m/s^2]")
axs[3].legend()
axs[3].grid(True)

# Gyroscope
axs[4].plot(df["GPS_Time"], df["GyroX"], label="X")
axs[4].plot(df["GPS_Time"], df["GyroY"], label="Y")
axs[4].plot(df["GPS_Time"], df["GyroZ"], label="Z")
axs[4].set_ylabel("Gyroscope [rad/s]")
axs[4].legend()
axs[4].grid(True)
"""
# Magnetometer
axs[5].plot(df["GPS_Time"], df["MagX"], label="MagX")
axs[5].plot(df["GPS_Time"], df["MagY"], label="MagY")
axs[5].plot(df["GPS_Time"], df["MagZ"], label="MagZ")
axs[5].set_ylabel("Magnetometer (µT)")
axs[5].set_xlabel("Time")
axs[5].legend()
axs[5].grid(True)
"""
plt.tight_layout()
plt.show()
