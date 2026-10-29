
import pandas as pd
import numpy as np
from scipy.signal import butter, sosfiltfilt, welch, find_peaks

# Folder and input files
folder = r"D:\EEG_Device_Comparison"

muse = pd.read_csv(folder + r"\muse_post_baseline.csv")
udl = pd.read_csv(folder + r"\udl.csv")

# Sampling rates
muse_fs = 256
udl_fs = 500

# Select signals
muse_raw = pd.to_numeric(muse["AF7"], errors="coerce").dropna().to_numpy()
udl_raw = pd.to_numeric(udl["Channel1"], errors="coerce").dropna().to_numpy()

# Match recording duration using the shorter recording
duration = min(len(muse_raw) / muse_fs, len(udl_raw) / udl_fs)

muse_samples = int(duration * muse_fs)
udl_samples = int(duration * udl_fs)

muse_raw = muse_raw[-muse_samples:]
udl_raw = udl_raw[-udl_samples:]

print(f"Matched duration: {duration:.2f} seconds")

# Bandpass filtering: 0.5-45 Hz
def filter_signal(signal, fs):
    sos = butter(
        4, [0.5, 45],
        btype="bandpass",
        fs=fs,
        output="sos"
    )
    return sosfiltfilt(sos, signal)

muse_signal = filter_signal(muse_raw, muse_fs)
udl_signal = filter_signal(udl_raw, udl_fs)

# Frequency bands
bands = {
    "Delta": (0.5, 4),
    "Theta": (4, 8),
    "Alpha": (8, 13),
    "Beta": (13, 30),
    "Gamma": (30, 45)
}

# Calculate metrics
def calculate_metrics(signal, fs):
    rms = np.sqrt(np.mean(signal ** 2))

    result = {
        "Minimum": np.min(signal),
        "Maximum": np.max(signal),
        "Peak_to_peak": np.ptp(signal),
        "Standard_deviation": np.std(signal),
        "RMS_amplitude": rms
    }

    frequencies, psd = welch(
        signal,
        fs=fs,
        nperseg=fs * 2
    )

    valid = (frequencies >= 0.5) & (frequencies <= 45)
    total_power = np.trapezoid(psd[valid], frequencies[valid])

    for band, (low, high) in bands.items():
        mask = (frequencies >= low) & (frequencies <= high)
        power = np.trapezoid(psd[mask], frequencies[mask])

        result[band + "_relative_power_percent"] = (
            power / total_power * 100 if total_power > 0 else 0
        )

    # Strongest spectral peaks
    peaks, _ = find_peaks(psd)
    peaks = peaks[valid[peaks]]

    strongest = peaks[np.argsort(psd[peaks])[-5:][::-1]]

    for i in range(5):
        result[f"Peak_{i+1}_Hz"] = (
            frequencies[strongest[i]] if i < len(strongest) else np.nan
        )

    return result

# Build comparison report
results = pd.DataFrame({
    "Metric": calculate_metrics(muse_signal, muse_fs).keys(),
    "Muse_AF7": calculate_metrics(muse_signal, muse_fs).values(),
    "UDL_Channel1": calculate_metrics(udl_signal, udl_fs).values()
})

print("\nFINAL EEG DEVICE COMPARISON")
print(results.round(4).to_string(index=False))

# Save report
output_path = folder + r"\final_device_comparison.csv"
results.to_csv(output_path, index=False)

print("\nReport saved to:", output_path)
