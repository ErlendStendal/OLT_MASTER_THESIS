import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('stepper_mast.csv')
plt.rcParams.update({'font.size': 18})
# Remap Pot3: max -> 0, min -> 250
pot1_max = df['Pot2'].min()
pot1_min = df['Pot2'].max()
df['Pot2_mapped'] = ( (df['Pot2']) +135) * 1.025
potAngle_max = ((2800/ 4095.0 * 3600.0)+135) * 1.025 # Map to 0-3600 degrees for 10 revolutions
potAngle_min = ((1700/ 4095.0 * 3600.0)+135) * 1.025 # Map to 0-3600 degrees for 10 revolutions
# Map specific Pot3 values to the same scale
#pot2250 = 270 * (pot1_max - 2250) / (pot1_max - pot1_min)
#pot1000 = 270 * (pot1_max - 1000) / (pot1_max - pot1_min)
#pot2500 = 270 * (pot1_max - 2500) / (pot1_max - pot1_min)

print(f"pot min: {pot1_min} | pot max: {pot1_max}")
print(f"pot 2800 mapped: {potAngle_max} | pot 1700 mapped: {potAngle_min}") # | pot 1000 mapped: {pot1000} | pot 2500 mapped: {pot2500}")

# Plot remapped Pot3 and StepperAngle
plt.figure(figsize=(10, 5))
plt.plot(df['Pot2_mapped'], label='Potentimeter')
plt.plot(df['StepperAngle'], label='Stepper')

# Add horizontal dotted lines
#plt.axhline(pot2250, color='red', linestyle='--', label='Pot3=2250 (mapped)')
#plt.axhline(pot1000, color='green', linestyle='--', label='Pot3=1000 (mapped)')
#plt.axhline(pot2500, color='blue', linestyle='--', label='Pot3=2500 (mapped)')

# Labels and formatting
plt.xlabel('Sample Index')
plt.ylabel('Angle [deg]')
plt.ylim(top=3900)
#plt.title('Mast and StepperAngle over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
