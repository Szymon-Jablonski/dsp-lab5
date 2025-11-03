import re
import numpy as np
import matplotlib.pyplot as plt


# === CONFIGURATION ===
filename = "40kHz.txt" # your exported STM32 data
sampling_frequency = 50000 # Sampling frequency in Hz (TIM3 trigger = 50 kHz)

# === PARSE FILE ===
values = []
with open(filename, 'r') as f:
    for line in f:
        # Extract the integer after 'uint32_t' if present
        match = re.search(r'uint32_t\s+(\d+)', line)
        if match:
            values.append(int(match.group(1)))

data = np.array(values, dtype=float)
N = len(data)
print(f"Loaded {N} samples")

# === TIME VECTOR ===
t = np.arange(N) / sampling_frequency

# === TIME DOMAIN PLOT ===
plt.figure(figsize=(10,5))
plt.plot(t*1000, data, 'b.-')
plt.title("STM32 ADC Samples (Time Domain)")
plt.xlabel("Time [ms]")
plt.ylabel("ADC Value")
plt.grid(True)
plt.tight_layout()
plt.show()