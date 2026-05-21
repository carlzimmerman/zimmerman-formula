#!/usr/bin/env python3
"""
Standard Isotropic Stochastic Gravitational Wave Background Search
===================================================================

Performs a standard stochastic background search using H1-L1 cross-correlation.
This is the baseline analysis assuming an unpolarized isotropic background.

Method:
- Cross-power spectral density (CPSD) between H1 and L1
- Standard overlap reduction function (ORF) for isotropic, unpolarized background
- Optimal filter weighting for Ω_GW(f)

Author: Carl Zimmerman
Date: May 2026
"""

import os
import json
import numpy as np
import h5py
from scipy import signal
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt

print("=" * 70)
print("STANDARD STOCHASTIC SEARCH - Isotropic Unpolarized Background")
print("=" * 70)

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
H1_FILE = os.path.join(OUTPUT_DIR, 'h1_strain.hdf5')
L1_FILE = os.path.join(OUTPUT_DIR, 'l1_strain.hdf5')
PLOT_FILE = os.path.join(OUTPUT_DIR, 'standard_search_results.png')
JSON_FILE = os.path.join(OUTPUT_DIR, 'standard_search_results.json')

# Analysis parameters
F_LOW = 20.0       # Hz - lower frequency bound
F_HIGH = 1726.0    # Hz - upper frequency bound (standard LIGO stochastic band)
SEGMENT_DURATION = 60  # seconds for Welch method
OVERLAP_FRACTION = 0.5

# Physical constants
H0 = 67.4e3 / 3.086e22  # Hubble constant in SI (s^-1)
c = 299792458.0         # Speed of light (m/s)

# Detector positions (geocentric, meters)
# These are approximate - for accurate ORF need precise positions
H1_LAT = np.radians(46.455)
H1_LON = np.radians(-119.408)
L1_LAT = np.radians(30.563)
L1_LON = np.radians(-90.774)

# Detector arm orientations (degrees from North, clockwise)
H1_ARM_ANGLE = np.radians(125.999)
L1_ARM_ANGLE = np.radians(197.716)

# Earth radius
R_EARTH = 6.371e6  # meters

# =============================================================================
# STEP 1: Load strain data
# =============================================================================

print("\n[1] Loading strain data...")

data = {}
for name, filepath in [('H1', H1_FILE), ('L1', L1_FILE)]:
    print(f"  Loading {name}...")
    with h5py.File(filepath, 'r') as f:
        data[name] = {
            'strain': f['strain'][:],
            'sample_rate': f.attrs['sample_rate'],
            'gps_start': f.attrs['gps_start'],
            'duration': f.attrs['duration']
        }
    print(f"    Samples: {len(data[name]['strain']):,}")
    print(f"    Sample rate: {data[name]['sample_rate']} Hz")
    print(f"    Duration: {data[name]['duration']}s")

# Verify consistency
assert data['H1']['sample_rate'] == data['L1']['sample_rate'], "Sample rates must match"
assert data['H1']['duration'] == data['L1']['duration'], "Durations must match"

fs = data['H1']['sample_rate']
duration = data['H1']['duration']
n_samples = len(data['H1']['strain'])

print(f"\n  Data verified: {duration}s at {fs} Hz")

# =============================================================================
# STEP 2: Bandpass filter
# =============================================================================

print("\n[2] Applying bandpass filter ({:.0f}-{:.0f} Hz)...".format(F_LOW, F_HIGH))

# Design bandpass filter
nyquist = fs / 2
low = F_LOW / nyquist
high = F_HIGH / nyquist

# Use 8th order Butterworth filter
b, a = signal.butter(8, [low, high], btype='band')

for name in ['H1', 'L1']:
    print(f"  Filtering {name}...")
    data[name]['filtered'] = signal.filtfilt(b, a, data[name]['strain'])

print("  Filtering complete.")

# =============================================================================
# STEP 3: Compute Cross-Power Spectral Density (CPSD)
# =============================================================================

print("\n[3] Computing Cross-Power Spectral Density...")

# Welch method parameters
nperseg = int(SEGMENT_DURATION * fs)
noverlap = int(nperseg * OVERLAP_FRACTION)

print(f"  Segment length: {nperseg} samples ({SEGMENT_DURATION}s)")
print(f"  Overlap: {noverlap} samples ({OVERLAP_FRACTION*100:.0f}%)")

# Compute CPSD
freqs, Pxy = signal.csd(
    data['H1']['filtered'],
    data['L1']['filtered'],
    fs=fs,
    nperseg=nperseg,
    noverlap=noverlap,
    window='hann',
    detrend='constant'
)

# Compute individual PSDs for normalization
_, Pxx_H1 = signal.welch(
    data['H1']['filtered'],
    fs=fs,
    nperseg=nperseg,
    noverlap=noverlap,
    window='hann',
    detrend='constant'
)

_, Pxx_L1 = signal.welch(
    data['L1']['filtered'],
    fs=fs,
    nperseg=nperseg,
    noverlap=noverlap,
    window='hann',
    detrend='constant'
)

# Select frequency range
freq_mask = (freqs >= F_LOW) & (freqs <= F_HIGH)
freqs = freqs[freq_mask]
Pxy = Pxy[freq_mask]
Pxx_H1 = Pxx_H1[freq_mask]
Pxx_L1 = Pxx_L1[freq_mask]

print(f"  Frequency range: {freqs[0]:.1f} - {freqs[-1]:.1f} Hz")
print(f"  Frequency bins: {len(freqs)}")

# =============================================================================
# STEP 4: Compute Overlap Reduction Function (ORF)
# =============================================================================

print("\n[4] Computing Overlap Reduction Function γ(f)...")

def compute_orf_standard(freqs, det1_lat, det1_lon, det1_arm,
                         det2_lat, det2_lon, det2_arm, n_sky=1000):
    """
    Compute the standard overlap reduction function for an isotropic,
    unpolarized gravitational wave background.

    For the H1-L1 baseline, γ(f) ≈ 1 at low frequencies and oscillates
    at higher frequencies due to the baseline length.
    """
    # Baseline vector between detectors
    # Convert lat/lon to Cartesian
    def latlon_to_xyz(lat, lon, R=R_EARTH):
        x = R * np.cos(lat) * np.cos(lon)
        y = R * np.cos(lat) * np.sin(lon)
        z = R * np.sin(lat)
        return np.array([x, y, z])

    pos_H1 = latlon_to_xyz(det1_lat, det1_lon)
    pos_L1 = latlon_to_xyz(det2_lat, det2_lon)
    baseline = pos_L1 - pos_H1
    baseline_length = np.linalg.norm(baseline)
    baseline_unit = baseline / baseline_length

    print(f"    Baseline length: {baseline_length/1000:.1f} km")

    # Light travel time along baseline
    tau_baseline = baseline_length / c
    print(f"    Light travel time: {tau_baseline*1000:.2f} ms")

    # For each frequency, compute the ORF
    # The analytic expression for aligned detectors is:
    # γ(f) = (5/2) * [j0(x) - j1(x)/x - j2(x)/3 + ...]
    # where x = 2πf * d/c and jn are spherical Bessel functions

    # Simpler approximation using sinc function for co-aligned detectors
    # For misaligned detectors, we need numerical integration over sky

    # Numerical sky integration
    gamma = np.zeros(len(freqs))

    # Generate sky directions (uniform on sphere)
    np.random.seed(42)  # Reproducibility
    phi_sky = np.random.uniform(0, 2*np.pi, n_sky)
    cos_theta = np.random.uniform(-1, 1, n_sky)
    theta_sky = np.arccos(cos_theta)

    for i, f in enumerate(freqs):
        omega = 2 * np.pi * f

        # Sky-averaged product of antenna patterns
        sum_val = 0.0
        for j in range(n_sky):
            theta = theta_sky[j]
            phi = phi_sky[j]

            # Sky direction unit vector
            n_hat = np.array([
                np.sin(theta) * np.cos(phi),
                np.sin(theta) * np.sin(phi),
                np.cos(theta)
            ])

            # Time delay for this sky direction
            delta_t = np.dot(baseline, n_hat) / c

            # Antenna pattern functions (simplified - assumes arms along local x, y)
            # F+ = (1 + cos²θ)/2 * cos(2φ - 2ψ) for optimal orientation
            # Fx = cosθ * sin(2φ - 2ψ)
            # For simplicity, use scalar approximation

            # Phase factor
            phase = np.exp(2j * np.pi * f * delta_t)

            # Combine (F+² + Fx²) averaged over polarization angle
            # For aligned detectors: ≈ 1
            # For H1-L1 (roughly aligned): use geometric factor
            cos_opening = np.abs(np.cos(det1_arm - det2_arm))
            antenna_product = 0.5 * (1 + cos_opening)

            sum_val += antenna_product * phase

        gamma[i] = np.abs(sum_val) / n_sky

    # Normalize so γ(0) ≈ 1 for aligned detectors
    gamma = gamma / gamma[0] if gamma[0] > 0 else gamma

    return gamma


# Compute ORF
gamma = compute_orf_standard(
    freqs, H1_LAT, H1_LON, H1_ARM_ANGLE,
    L1_LAT, L1_LON, L1_ARM_ANGLE, n_sky=2000
)

print(f"  γ(20 Hz) = {gamma[0]:.4f}")
print(f"  γ(100 Hz) = {gamma[np.argmin(np.abs(freqs-100))]:.4f}")
print(f"  γ(1000 Hz) = {gamma[np.argmin(np.abs(freqs-1000))]:.4f}")

# =============================================================================
# STEP 5: Compute Ω_GW(f) Optimal Estimator
# =============================================================================

print("\n[5] Computing Ω_GW(f) optimal estimator...")

# The optimal estimator for Ω_GW is:
# Ŷ(f) = Re[Pxy(f)] / γ(f)
# Ω_GW(f) = (10π² / 3H0²) * f³ * Ŷ(f)

# Normalization factor
norm_factor = (10 * np.pi**2) / (3 * H0**2)

# Avoid division by zero
gamma_safe = np.maximum(np.abs(gamma), 1e-10)

# Cross-correlation estimator (real part)
Y_hat = np.real(Pxy) / gamma_safe

# Ω_GW(f) estimator
Omega_GW = norm_factor * freqs**3 * Y_hat

# Compute variance/uncertainty
# σ²(f) ∝ P_H1(f) * P_L1(f) / (T * Δf * γ²(f))
T_obs = duration
delta_f = freqs[1] - freqs[0]
n_segments = duration / SEGMENT_DURATION

# Variance of the estimator
variance_Y = (Pxx_H1 * Pxx_L1) / (2 * T_obs * delta_f * gamma_safe**2)
sigma_Omega = norm_factor * freqs**3 * np.sqrt(variance_Y)

# Print some statistics
print(f"  Frequency resolution: {delta_f:.4f} Hz")
print(f"  Number of segments: {n_segments:.0f}")
print(f"  Observation time: {T_obs:.0f}s")

# =============================================================================
# STEP 6: Broadband Integration
# =============================================================================

print("\n[6] Computing broadband Ω_GW estimate...")

# Optimal filter for flat Ω_GW spectrum
# Weight by 1/σ²
weights = 1.0 / (sigma_Omega**2 + 1e-100)
weights = weights / np.sum(weights)

# Weighted average
Omega_GW_broadband = np.sum(weights * Omega_GW)
sigma_broadband = 1.0 / np.sqrt(np.sum(1.0 / (sigma_Omega**2 + 1e-100)))

print(f"  Broadband Ω_GW = {Omega_GW_broadband:.2e}")
print(f"  Uncertainty σ = {sigma_broadband:.2e}")

# 95% upper limit (assuming Gaussian statistics)
upper_limit_95 = Omega_GW_broadband + 1.645 * sigma_broadband
if Omega_GW_broadband < 0:
    upper_limit_95 = 1.645 * sigma_broadband

print(f"\n  95% Upper Limit: Ω_GW < {upper_limit_95:.2e}")

# =============================================================================
# STEP 7: Generate Plots
# =============================================================================

print("\n[7] Generating plots...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Overlap Reduction Function
ax1 = axes[0, 0]
ax1.semilogx(freqs, gamma, 'b-', linewidth=1.5, label='γ(f) H1-L1')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Overlap Reduction Function γ(f)')
ax1.set_title('Standard ORF (Isotropic Unpolarized)')
ax1.set_xlim(F_LOW, F_HIGH)
ax1.set_ylim(0, 1.2)
ax1.grid(True, alpha=0.3)
ax1.legend()

# Panel 2: Cross-power spectrum
ax2 = axes[0, 1]
ax2.loglog(freqs, np.abs(Pxy), 'g-', linewidth=0.8, alpha=0.7)
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('|CPSD| [strain²/Hz]')
ax2.set_title('H1-L1 Cross-Power Spectral Density')
ax2.set_xlim(F_LOW, F_HIGH)
ax2.grid(True, alpha=0.3, which='both')

# Panel 3: Ω_GW(f) spectrum
ax3 = axes[1, 0]
# Plot with uncertainty band
ax3.fill_between(freqs, (Omega_GW - sigma_Omega), (Omega_GW + sigma_Omega),
                  alpha=0.3, color='blue', label='1σ uncertainty')
ax3.semilogx(freqs, Omega_GW, 'b-', linewidth=1, label='Ω_GW(f)')
ax3.axhline(0, color='gray', linestyle='--', linewidth=0.5)
ax3.axhline(upper_limit_95, color='red', linestyle='--', linewidth=1.5,
            label=f'95% UL = {upper_limit_95:.1e}')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Ω_GW(f)')
ax3.set_title('Gravitational Wave Energy Density Spectrum')
ax3.set_xlim(F_LOW, F_HIGH)
ax3.legend()
ax3.grid(True, alpha=0.3)

# Panel 4: Sensitivity curve
ax4 = axes[1, 1]
# PI curve (Power-law Integrated) sensitivity
ax4.loglog(freqs, sigma_Omega, 'b-', linewidth=1.5, label='Sensitivity σ(f)')
ax4.axhline(upper_limit_95, color='red', linestyle='--', linewidth=1.5,
            label=f'95% UL = {upper_limit_95:.1e}')
ax4.set_xlabel('Frequency [Hz]')
ax4.set_ylabel('Ω_GW sensitivity')
ax4.set_title('Stochastic Search Sensitivity')
ax4.set_xlim(F_LOW, F_HIGH)
ax4.legend()
ax4.grid(True, alpha=0.3, which='both')

fig.suptitle('Standard Isotropic Stochastic GW Background Search (H1-L1)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150, bbox_inches='tight', facecolor='white')
print(f"  Saved plot to: {os.path.basename(PLOT_FILE)}")

# =============================================================================
# STEP 8: Save Results
# =============================================================================

print("\n[8] Saving results...")

results = {
    'analysis': 'standard_isotropic_unpolarized',
    'gps_start': int(data['H1']['gps_start']),
    'gps_end': int(data['H1']['gps_start'] + duration),
    'duration_seconds': float(duration),
    'frequency_range_hz': [float(F_LOW), float(F_HIGH)],
    'segment_duration_s': SEGMENT_DURATION,
    'broadband_omega_gw': float(Omega_GW_broadband),
    'broadband_sigma': float(sigma_broadband),
    'upper_limit_95_percent': float(upper_limit_95),
    'gamma_f': {
        'frequencies_hz': freqs.tolist(),
        'gamma': gamma.tolist()
    },
    'omega_gw_spectrum': {
        'frequencies_hz': freqs.tolist(),
        'omega_gw': Omega_GW.tolist(),
        'sigma': sigma_Omega.tolist()
    }
}

with open(JSON_FILE, 'w') as f:
    json.dump(results, f, indent=2)

print(f"  Saved results to: {os.path.basename(JSON_FILE)}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("STANDARD STOCHASTIC SEARCH COMPLETE")
print("=" * 70)

print(f"""
  Analysis: Isotropic Unpolarized Background
  Observation Time: {duration/3600:.2f} hours
  Frequency Band: {F_LOW:.0f} - {F_HIGH:.0f} Hz

  Results:
    Broadband Ω_GW = {Omega_GW_broadband:.2e} ± {sigma_broadband:.2e}

    ╔══════════════════════════════════════════╗
    ║  95% Upper Limit: Ω_GW < {upper_limit_95:.2e}    ║
    ╚══════════════════════════════════════════╝

  Files Created:
    - standard_search_results.png
    - standard_search_results.json
""")

print("=" * 70)
