import pandas as pd
import os

# Input and output file paths
input_file = 'tacks_meter_wind_VMG_re1.csv'  # Replace with your actual file path
output_file = 'tacks_meter_wind_VMG_deg1.csv'  # Adjust as needed


# Conversion parameters
rudder_center = 1800
rudder_scale = 4095 / 270
gn_center = 2104.5
gn_scale = 4095 / 270

# Read the CSV file
df = pd.read_csv(input_file)

# Convert Rudder and GN angles if present
if 'Rudder angle' in df.columns:
    df['Rudder angle'] = (df['Rudder angle'] - rudder_center) / rudder_scale
if 'GN angle' in df.columns:
    df['GN angle'] = (df['GN angle'] - gn_center) / gn_scale

# Save the modified CSV
df.to_csv(output_file, index=False)

print(f"Processed file saved as: '{output_file}'")
