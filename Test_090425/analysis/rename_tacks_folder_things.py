import os
import pandas as pd

# Define input and output folders
input_folder = 'tacks'
output_folder = 'tacks_renamed'

# Create the output folder if it doesn't exist
os.makedirs(output_folder, exist_ok=True)

# Columns to rename
rename_map = {
    'Pot1': 'Rudder angle',
    'Pot2': 'Mast angle',
    'Speed': 'SOG'
}

# Process files Turn_01.csv to Turn_14.csv
for i in range(1, 15):
    file_name = f'Turn_{i:02d}.csv'
    input_path = os.path.join(input_folder, file_name)
    output_path = os.path.join(output_folder, file_name)

    # Read, rename, and save the file
    df = pd.read_csv(input_path)
    df.rename(columns=rename_map, inplace=True)
    df.to_csv(output_path, index=False)

print("All files processed and saved to 'tacks_renamed' folder.")
