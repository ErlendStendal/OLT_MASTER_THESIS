import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("tacks_meter_wind_VMG_deg1.csv")

# Convert GPS_Time to datetime with milliseconds
df["GPS_Time"] = pd.to_datetime(df["GPS_Time"], format="%H:%M:%S.%f")

# Plotting
fig, axs = plt.subplots(5, 1, figsize=(12, 18), sharex=True)
#fig, axs = plt.subplots(6, 1, figsize=(12, 18), sharex=True)
# Potentiometers
axs[0].plot(df["GPS_Time"], df["Pot1"], label="Rudder")
axs[0].plot(df["GPS_Time"], df["Pot3"], label="Gooseneck")
axs[0].set_ylabel("Potentiometers")
axs[0].legend()
axs[0].grid(True)

# Speed
axs[1].plot(df["GPS_Time"], df["Speed"], label="Speed", color="tab:blue")
axs[1].set_ylabel("Speed")
axs[1].legend()
axs[1].grid(True)

# Normalize Course to range [-180, 180]
df["Course_normalized"] = (df["Course"] + 180) % 360 - 180

# Course
axs[2].plot(df["GPS_Time"], df["Course_normalized"], label="Course (±180°)", color="tab:orange")
axs[2].set_ylabel("Course (±180°)")
axs[2].legend()
axs[2].grid(True)


# Accelerometer
axs[3].plot(df["GPS_Time"], df["AccelX"], label="AccelX")
axs[3].plot(df["GPS_Time"], df["AccelY"], label="AccelY")
axs[3].plot(df["GPS_Time"], df["AccelZ"], label="AccelZ")
axs[3].set_ylabel("Acceleration (g)")
axs[3].legend()
axs[3].grid(True)

# Gyroscope
axs[4].plot(df["GPS_Time"], df["GyroX"], label="GyroX")
axs[4].plot(df["GPS_Time"], df["GyroY"], label="GyroY")
axs[4].plot(df["GPS_Time"], df["GyroZ"], label="GyroZ")
axs[4].set_ylabel("Gyroscope (°/s)")
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
