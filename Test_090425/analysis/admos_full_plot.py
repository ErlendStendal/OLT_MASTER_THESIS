import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
plt.rcParams.update({'font.size': 18})

# Load the file
choose_file = 0
if choose_file == 0:
    file_path = "converted_admos_gps_IMU_data_boat.csv"
else:
    file_path = "converted_admos_gps_IMU_data_sailor.csv"
df = pd.read_csv(file_path)

# Ensure datetime is in correct format
df['datetime'] = pd.to_datetime(df['datetime'])

# Set datetime as index
df.set_index('datetime', inplace=True)

# Custom formatter: MM:SS.s
def format_mmss1(x, pos=None):
    dt = mdates.num2date(x)
    total_seconds = dt.minute * 60 + dt.second + dt.microsecond / 1e6
    return f"{int(total_seconds // 60):02}:{total_seconds % 60:04.1f}"

# Calculate total 3D speed from GNSS
df['totalSpeed [m/s]'] = (df[['speedN [m/s]', 'speedE [m/s]', 'speedD [m/s]']] ** 2).sum(axis=1).pow(0.5)

# Create a 4-row subplot
fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(12, 10), sharex=True)
plt.subplots_adjust(hspace=0.4)

# Plot Accelerometer Data
df[['accX [g]', 'accY [g]', 'accZ [g]']].plot(ax=axes[0])
axes[0].set_title('Accelerometer Data')
axes[0].set_ylabel('[g]')
axes[0].set_ylim([-5, 5])  # <- Limit Y-axis
axes[0].xaxis.set_major_formatter(plt.FuncFormatter(format_mmss1))
axes[0].grid(True)

# Plot Gyroscope Data
df[['gyrX [dps]', 'gyrY [dps]', 'gyrZ [dps]']].plot(ax=axes[1])
axes[1].set_title('Gyroscope Data')
axes[1].set_ylabel('[dps]')
axes[1].set_ylim([-170, 170])  # <- Limit Y-axis
axes[1].xaxis.set_major_formatter(plt.FuncFormatter(format_mmss1))
axes[1].grid(True)

# Plot Combined GNSS Speed
df['totalSpeed [m/s]'].plot(ax=axes[2])
axes[2].set_title('GNSS Total Speed')
axes[2].set_ylabel('[m/s]')
axes[2].xaxis.set_major_formatter(plt.FuncFormatter(format_mmss1))
axes[2].grid(True)
"""
# Plot GNSS Altitude
df['altitude [m]'].plot(ax=axes[3])
axes[3].set_title('GNSS Altitude')
axes[3].set_ylabel('[m]')
axes[3].set_xlabel('Time (MM:SS.s)')
axes[3].xaxis.set_major_formatter(plt.FuncFormatter(format_mmss1))
axes[3].grid(True)
"""
plt.tight_layout()
plt.show()

# GNSS Position Plot (optional)
# fig, ax = plt.subplots()
# df.plot(x='lon', y='lat', ax=ax, legend=False)
# ax.set_title('GNSS Position (Latitude vs Longitude)')
# ax.set_xlabel('Longitude')
# ax.set_ylabel('Latitude')
# ax.grid(True)
# plt.show()
