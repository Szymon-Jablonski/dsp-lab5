import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import fft, fftfreq

def plot_frequency_spectrum(signal, fs, title):
    # Needed to remove the DC offset
    signal = np.array(signal) - np.mean(signal)
    N = len(signal)
     
    window = np.hanning(N)
    signal = signal * window
  
    fft_vals = fft(signal)
    fft_freq = fftfreq(N, 1/fs)# Plot magnitude spectrum (positive frequencies only)
    
    # Single-sided spectrum
    mag = np.abs(fft_vals[:N//2])

    # Normalize (optional but recommended)

    # Convert to dB (add small value to avoid log(0))
    mag_db = 20 * np.log10(mag + 1e-12)

    plt.figure(figsize=(10, 5))
    # :N//2 - return only first half - the positive frequencies
    # 2/N * np.abs(...) - normalize the amplitude, factor of 2 for single-sided spectrum
    plt.plot(fft_freq[:N//2], mag_db)
    plt.title(title)
    plt.xlabel('Frequency (Hz)')
    plt.ylabel('Magnitude')
    plt.grid(True)
    plt.xlim(0, fs/2)
    plt.show()

def process_adc_vals(filenames, sampling_rate):
    for filename in filenames:
        adc_values = []

        # Parse the text file and put values into the variable
        with open(filename, 'r') as f:
            for line in f:
                match = re.search(r'uint32_t\s+(\d+)', line)
                if match:
                    adc_values.append(int(match.group(1)))
        
        t = np.arange(len(adc_values)) / sampling_rate
        
        plt.figure(figsize=(10, 5))
        plt.plot(t*1000, adc_values, 'b.-')
        plt.title("Signal from " + filename)
        plt.xlabel("Time [ms]")
        plt.ylabel("ADC Value")
        plt.grid(True)
        plt.show()

        plot_frequency_spectrum(adc_values, sampling_rate, "FFT for signal from " + filename)
        
files = ["1khz.txt", "10khz.txt", "40khz.txt", "1khz-t2.txt", "10khz-t2.txt", "my-1khz-t2.txt", "my-10khz-t2.txt", "my-40khz-t2.txt"]
process_adc_vals(files, 50000)
