import os
import pandas as pd

# Define folder paths
input_folder = "tacks_converted_deg"
output_folder = "tacks_converted_deg_ms"

# Create output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Conversion factor from km/h to m/s
KMH_TO_MS = 1000 / 3600  # 1 km/h = 0.2777777778 m/s

# Process each file
for i in range(1, 13):
    filename = f"Turn_{i:02d}.csv"
    input_path = os.path.join(input_folder, filename)
    output_path = os.path.join(output_folder, filename)

    if os.path.exists(input_path):
        # Read the CSV file
        df = pd.read_csv(input_path)

        # Convert SOG and VMG from km/h to m/s
        df["SOG"] = df["SOG"] * KMH_TO_MS
        df["VMG"] = df["VMG"] * KMH_TO_MS

        # Save to the output folder
        df.to_csv(output_path, index=False)
        print(f"Processed and saved: {output_path}")
    else:
        print(f"File not found: {input_path}")
