# Preliminary-EEG-Device-Comparison
Preliminary comparison of EEG signals recorded using Muse and the Upside Down Labs Neuroscience Kit using signal amplitude statistics and frequency-domain characteristics.

## Overview

This project performs a preliminary comparison of EEG signals recorded using two devices:

- **Muse EEG headband**
- **Upside Down Labs Neuroscience Kit**

The analysis examines signal amplitude statistics and frequency-domain characteristics to describe the recorded signals.

The recordings were collected separately and were not acquired simultaneously.

## Objectives

- Compare basic statistical characteristics of EEG signals.
- Examine the distribution of relative power across EEG frequency bands.
- Identify the strongest spectral peaks in each recording.
- Generate a CSV report containing the comparison results.

## Methodology

### 1. Data Selection

The analysis uses:
- Muse: AF7 channel
- Upside Down Labs: Channel1

### 2. Sampling Rates

- Muse: 256 Hz
- Upside Down Labs: 500 Hz

### 3. Duration Matching

The shorter recording duration is used to determine the comparison duration. The corresponding samples are selected from the end of each recording.

### 4. Signal Filtering

A fourth-order Butterworth bandpass filter from 0.5 Hz to 45 Hz is applied using zero-phase forward-backward filtering.

### 5. Calculated Parameters

**Amplitude statistics**
- Minimum amplitude
- Maximum amplitude
- Peak-to-peak amplitude
- Standard deviation
- Root mean square (RMS) amplitude

**Frequency-domain analysis**
- Relative Delta power (0.5–4 Hz)
- Relative Theta power (4–8 Hz)
- Relative Alpha power (8–13 Hz)
- Relative Beta power (13–30 Hz)
- Relative Gamma power (30–45 Hz)
- Five strongest spectral peaks

Welch's method is used to estimate the power spectral density (PSD).

## Technologies Used

- Python
- NumPy
- pandas
- SciPy

## How to Run

1. Install Python.
2. Install the required libraries:

   `pip install numpy pandas scipy`

3. Place the input CSV files in the same directory as the Python script:
   - `muse_post_baseline.csv`
   - `udl.csv`

4. Ensure that the CSV files contain the expected columns:
   - Muse: `AF7`
   - Upside Down Labs: `Channel1`

5. Run the script:

   `python preliminary_eeg_device_comparison.py`

## Output

The script prints a comparison table and saves the results to:

`final_device_comparison.csv`

## Limitations

- The recordings were collected separately rather than simultaneously.
- Only one selected channel from each device is analysed.
- Differences in electrode placement, reference configuration, hardware gain, units, and recording conditions may influence the results.
- Relative band power describes the distribution of power within the analysed frequency range; it does not independently establish signal quality.
- The analysis does not calculate signal-to-noise ratio (SNR).
- The analysis does not establish which device is more accurate or clinically superior.

## Project Status

Preliminary analysis completed. Further validation using suitable reference recordings and additional signal-quality measures may be required.

## Disclaimer

This project is intended for educational and research purposes. It is not intended for clinical diagnosis or medical decision-making.
