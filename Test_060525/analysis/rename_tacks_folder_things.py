import os
import pandas as pd

# Define input and output folders
input_folder = 'tacks2'
output_folder = 'tacks_renamed2'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Columns to rename
rename_map = {
    'Pot1': 'Rudder angle',
    'Pot3': 'GN angle',
    'Speed': 'SOG'
}

# Process all CSV files in the input folder
for file_name in os.listdir(input_folder):
    if file_name.lower().endswith('.csv'):
        input_path = os.path.join(input_folder, file_name)
        output_path = os.path.join(output_folder, file_name)

        # Read, rename, and save the file
        df = pd.read_csv(input_path)
        df.rename(columns=rename_map, inplace=True)
        df.to_csv(output_path, index=False)

print("All CSV files processed and saved to 'tacks_renamed2' folder.")
