import pandas as pd
import numpy as np

def calculate_vmg(speed, course, wind_direction):
    # Convert angle difference to radians
    angle_diff = np.radians(course - wind_direction)
    # VMG is positive if heading toward the wind
    return speed * np.cos(angle_diff)
    

def add_vmg_to_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Ensure required columns are present
    if not {'Speed', 'Course', 'Wind_Direction'}.issubset(df.columns):
        raise ValueError("CSV must contain 'Speed', 'Course', and 'Wind_Direction' columns.")

    # Calculate VMG
    df['VMG'] = df.apply(lambda row: calculate_vmg(row['Speed'], row['Course'], row['Wind_Direction']), axis=1)

    # Save the new CSV with VMG column
    df.to_csv(output_file, index=False)
    print(f"VMG column added and saved to {output_file}")

# Example usage:
add_vmg_to_csv("tacks_meter_wind.csv", "tacks_meter_wind_VMG.csv")
