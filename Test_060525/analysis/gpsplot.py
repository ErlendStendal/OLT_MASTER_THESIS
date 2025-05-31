import pandas as pd
import matplotlib.pyplot as plt
from pyproj import Proj, Transformer
plt.rcParams.update({'font.size': 18})
# Load CSV
file_path = "test_060525.csv"  # <-- Replace with your actual file path
df = pd.read_csv(file_path)

# Reference lat/lon (first row) for local conversion
ref_lat = df["Lat"].iloc[0]
ref_lon = df["Lon"].iloc[0]

# Set up transformer: WGS84 to local East/North (meters) using UTM projection
proj = Proj(proj='utm', zone=32, ellps='WGS84', south=False)  # Adjust zone if needed
transformer = Transformer.from_crs("epsg:4326", proj.srs, always_xy=True)

# Convert lat/lon to meters
df["x_m"], df["y_m"] = transformer.transform(df["Lon"].values, df["Lat"].values)

# Offset to relative origin
df["x_m"] -= df["x_m"].iloc[0]
df["y_m"] -= df["y_m"].iloc[0]

# Plotting
plt.figure(figsize=(10, 8))
plt.plot(df["x_m"], df["y_m"],label="Path", linestyle='-')
#plt.title("GPS Trajectory in Meters")
plt.legend()
plt.xlabel("[m]")
plt.ylabel("[m]")
plt.grid(True)
plt.axis("equal")
plt.tight_layout()
plt.show()
