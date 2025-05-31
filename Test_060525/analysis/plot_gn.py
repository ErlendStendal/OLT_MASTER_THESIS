import pandas as pd
import matplotlib.pyplot as plt

# Load CSV
df = pd.read_csv("main_meter.csv")

# Convert GPS_Time to datetime with milliseconds
df["GPS_Time"] = pd.to_datetime(df["GPS_Time"], format="%H:%M:%S.%f")

# Calculate min and max for Pot3
pot3_min = df["Pot3"].min()
pot3_max = df["Pot3"].max()
print(f"Pot3 (Gooseneck) Min Value: {pot3_min}")
print(f"Pot3 (Gooseneck) Max Value: {pot3_max}")

# Plot Pot3
plt.figure(figsize=(12, 4))
plt.plot(df["GPS_Time"], df["Pot3"], label="Gooseneck", color="tab:green")
plt.ylabel("Potentiometer (Gooseneck)")
plt.xlabel("Time")
plt.title("Pot3 (Gooseneck) Over Time")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
