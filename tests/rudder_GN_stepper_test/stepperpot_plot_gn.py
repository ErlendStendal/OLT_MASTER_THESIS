import pandas as pd
import matplotlib.pyplot as plt

# Load data from CSV file
df = pd.read_csv('stepper_gn.csv')
plt.rcParams.update({'font.size': 18})
# Remap Pot3: max -> 0, min -> 250
pot1_min = df['Pot3'].max()
pot1_max = df['Pot3'].min()
df['Pot3_mapped'] = 270 * (pot1_max - df['Pot3']) / (pot1_max - pot1_min)

# Map specific Pot3 values to the same scale
pot2250 = 270 * (pot1_max - 2250) / (pot1_max - pot1_min)
pot1000 = 270 * (pot1_max - 1000) / (pot1_max - pot1_min)
pot2500 = 270 * (pot1_max - 2500) / (pot1_max - pot1_min)

print(f"pot min: {pot1_min} | pot max: {pot1_max}")
print(f"pot 2250 mapped: {pot2250} | pot 1000 mapped: {pot1000} | pot 2500 mapped: {pot2500}")

# Plot remapped Pot3 and StepperAngle
plt.figure(figsize=(10, 5))
plt.plot(df['Pot3_mapped'], label='Potentiometer')
plt.plot(df['StepperAngle'], label='Stepper')

# Add horizontal dotted lines
#plt.axhline(pot2250, color='red', linestyle='--', label='Pot3=2250 (mapped)')
#plt.axhline(pot1000, color='green', linestyle='--', label='Pot3=1000 (mapped)')
#plt.axhline(pot2500, color='blue', linestyle='--', label='Pot3=2500 (mapped)')

# Labels and formatting
plt.xlabel('Sample Index')
plt.ylabel('Angle [deg]')
#plt.title('Mapped Pot3 and StepperAngle over Time')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
