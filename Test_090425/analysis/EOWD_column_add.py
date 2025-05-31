import os
import pandas as pd

# Folder with renamed files
folder_path = 'tacks_renamed'

# Value to assign to the new column
eowd_value = 317.9

# Add EOWD column to each CSV file
for file_name in os.listdir(folder_path):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)

        # Read the CSV file
        df = pd.read_csv(file_path)

        # Add the new column with the specified value
        df['EOWD'] = eowd_value

        # Save it back to the same file
        df.to_csv(file_path, index=False)

print("EOWD column added to all files in 'tacks_renamed'.")
