import pandas as pd

# --- User settings ---

input_file = "tacks.csv"            # Input CSV file
output_file = "tacks_meter_wind.csv"  # Output CSV file
wind_direction_value = 317.9        # Fixed wind direction you want to add egnt ewod men blir lettere.

# ----------------------

# Load CSV
df = pd.read_csv(input_file)

# Add wind direction column
df["Wind_Direction"] = wind_direction_value

# Save to new CSV
df.to_csv(output_file, index=False)

print(f"Saved new CSV with wind direction to {output_file}")
