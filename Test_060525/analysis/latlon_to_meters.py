import pandas as pd
import numpy as np

# Function to convert lat/lon to meters
def latlon_to_meters(lat, lon, lat0, lon0):
    """
    Convert lat/lon to meters relative to a reference point (lat0, lon0).
    """
    # Earth radius in meters
    R = 6378137

    # Convert degrees to radians
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    lat0_rad = np.radians(lat0)
    lon0_rad = np.radians(lon0)

    # Calculate differences
    dlat = lat_rad - lat0_rad
    dlon = lon_rad - lon0_rad

    # Calculate meters
    x = dlon * R * np.cos(lat0_rad)
    y = dlat * R

    return x, y

def process_csv(input_file, output_file):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Use the first Lat/Lon as the reference point
    lat0 = df['Lat'].iloc[0]
    lon0 = df['Lon'].iloc[0]

    # Convert all lat/lon to meters
    x_meters, y_meters = latlon_to_meters(df['Lat'].values, df['Lon'].values, lat0, lon0)

    # Add to dataframe
    df['X_meters'] = x_meters
    df['Y_meters'] = y_meters

    # Save to new CSV
    df.to_csv(output_file, index=False)
    print(f"Saved output to {output_file}")

# Example usage
input_csv = 'MAIN_log.csv'  # Change this to your input CSV filename
output_csv = 'main_meter.csv'

process_csv(input_csv, output_csv)
