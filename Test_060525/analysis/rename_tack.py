import os
import pandas as pd

# Define input and output file paths
input_file = 'tacks_meter_wind_VMG2.csv'      # Replace with your actual input file path
output_file = 'tacks_meter_wind_VMG_re2.csv'  # Adjust the output path and name as needed


# Columns to rename
rename_map = {
    'Pot1': 'Rudder angle',
    'Pot3': 'GN angle',
    'Speed': 'SOG'
}

# Read the CSV file
df = pd.read_csv(input_file)

# Rename columns
df.rename(columns=rename_map, inplace=True)

# Save the modified CSV
df.to_csv(output_file, index=False)

print(f"Processed file saved as: '{output_file}'")
