import os
import pandas as pd
from datetime import datetime

# Input folder (already contains renamed files)
input_folder = 'tacks_renamed'

# New output folder with timestamp
#timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_folder = 'tacks_converted_deg'
os.makedirs(output_folder, exist_ok=True)

# Conversion parameters
rudder_center = 2184
rudder_scale = 15.5
mast_center = 2192
mast_scale = 6.258

# Process all CSV files in the folder
for file_name in os.listdir(input_folder):
    if file_name.endswith('.csv'):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Read CSV
        df = pd.read_csv(input_path)

        # Check and convert Rudder and Mast angles
        if 'Rudder angle' in df.columns:
            df['Rudder angle'] = (df['Rudder angle'] - rudder_center) / rudder_scale
        if 'Mast angle' in df.columns:
            df['Mast angle'] = (df['Mast angle'] - mast_center) / mast_scale

        # Save modified file
        df.to_csv(output_path, index=False)

print(f"Processed files saved in: '{output_folder}'")
