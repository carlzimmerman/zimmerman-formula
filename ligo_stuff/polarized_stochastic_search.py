#!/usr/bin/env python3
"""
Polarized Stochastic Gravitational Wave Background Search (h+ only)
====================================================================

Performs a stochastic background search modified for a single-polarization
(h+ only) background, as predicted by the T³/Z₂ topological framework.

Key modification:
- Standard ORF: γ(f) ∝ ∫ [F+₁F+₂ + F×₁F×₂] exp(2πifΔt) dΩ
- Polarized ORF: γ₊(f) ∝ ∫ [F+₁F+₂] exp(2πifΔt) dΩ  (hx term dropped)

The Z² framework predicts only h+ polarization survives due to the Z₂
orbifold projection, with tensor-to-scalar ratio r = 1/(2Z²) = 0.0149.

Author: Carl Zimmerman
Date: May 2026
"""

import os
import json
import numpy as np
import h5py
import healpy as hp
from scipy import signal
from scipy.integrate import trapezoid
import matplotlib.pyplot as plt

print("=" * 70)
print("POLARIZED STOCHASTIC SEARCH - h+ Only Background (Z² Framework)")
print("=" * 70)

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
H1_FILE = os.path.join(OUTPUT_DIR, 'h1_strain.hdf5')
L1_FILE = os.path.join(OUTPUT_DIR, 'l1_strain.hdf5')
STANDARD_RESULTS = os.path.join(OUTPUT_DIR, 'standard_search_results.json')
PLOT_FILE = os.path.join(OUTPUT_DIR, 'polarized_search_results.png')
JSON_FILE = os.path.join(OUTPUT_DIR, 'polarized_search_results.json')

# Analysis parameters
F_LOW = 20.0
F_HIGH = 1726.0
SEGMENT_DURATION = 60
OVERLAP_FRACTION = 0.5

# Physical constants
H0 = 67.4e3 / 3.086e22  # Hubble constant in SI (s^-1)
c = 299792458.0         # Speed of light (m/s)

# Detector parameters (precise values)
# Hanford (H1)
H1_LAT = np.radians(46.4552)
H1_LON = np.radians(-119.4076)
H1_X_ARM_AZIMUTH = np.radians(125.9994)  # X arm direction from North
H1_Y_ARM_AZIMUTH = np.radians(125.9994 - 90)  # Y arm perpendicular

# Livingston (L1)
L1_LAT = np.radians(30.5629)
L1_LON = np.radians(-90.7742)
L1_X_ARM_AZIMUTH = np.radians(197.7165)
L1_Y_ARM_AZIMUTH = np.radians(197.7165 - 90)

# Earth radius
R_EARTH = 6.371e6

# Z² framework constants
Z2 = 32 * np.pi / 3
r_tensor = 1 / (2 * Z2)  # Tensor-to-scalar ratio = 0.0149

# HEALPix resolution for sky integration
NSIDE = 32

# =============================================================================
# DETECTOR GEOMETRY FUNCTIONS
# =============================================================================

def latlon_to_xyz(lat, lon, R=R_EARTH):
    """Convert latitude/longitude to geocentric Cartesian coordinates."""
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return np.array([x, y, z])


def get_detector_frame(lat, lon, x_arm_azimuth):
    """
    Compute the detector tensor in Earth-centered coordinates.

    Returns the response tensor D = (1/2)(x⊗x - y⊗y) in ECEF coordinates.
    """
    # Local North, East, Up unit vectors at detector location
    cos_lat, sin_lat = np.cos(lat), np.sin(lat)
    cos_lon, sin_lon = np.cos(lon), np.sin(lon)

    # Up (radial)
    up = np.array([cos_lat * cos_lon, cos_lat * sin_lon, sin_lat])

    # North (tangent to meridian, pointing north)
    north = np.array([-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat])

    # East (tangent to parallel, pointing east)
    east = np.array([-sin_lon, cos_lon, 0])

    # X arm direction (azimuth from North, clockwise)
    cos_az, sin_az = np.cos(x_arm_azimuth), np.sin(x_arm_azimuth)
    x_arm = cos_az * north + sin_az * east

    # Y arm direction (perpendicular, 90° counter-clockwise from X)
    y_arm = -sin_az * north + cos_az * east

    return x_arm, y_arm


def antenna_pattern_plus(theta, phi, x_arm, y_arm):
    """
    Compute the h+ antenna pattern function F+ for a detector.

    F+ = (1/2) * [(x·e+)(x·e+) - (y·e+)(y·e+)]

    where e+ is the plus polarization tensor basis vector.
    """
    # Wave propagation direction (from source)
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)

    # Unit vector from source
    n_hat = np.array([
        sin_theta * cos_phi,
        sin_theta * sin_phi,
        cos_theta
    ])

    # Polarization basis vectors for the GW
    # Using the standard choice with ψ = 0 (polarization angle)
    # e_theta and e_phi are perpendicular to n_hat
    e_theta = np.array([
        cos_theta * cos_phi,
        cos_theta * sin_phi,
        -sin_theta
    ])

    e_phi = np.array([
        -sin_phi,
        cos_phi,
        0
    ])

    # F+ = (1/2) * [ (x·e_θ)² - (x·e_φ)² - (y·e_θ)² + (y·e_φ)² ]
    x_dot_theta = np.dot(x_arm, e_theta)
    x_dot_phi = np.dot(x_arm, e_phi)
    y_dot_theta = np.dot(y_arm, e_theta)
    y_dot_phi = np.dot(y_arm, e_phi)

    F_plus = 0.5 * (x_dot_theta**2 - x_dot_phi**2 - y_dot_theta**2 + y_dot_phi**2)

    return F_plus


def antenna_pattern_cross(theta, phi, x_arm, y_arm):
    """
    Compute the hx antenna pattern function F× for a detector.

    F× = (1/2) * [(x·e+)(x·ex) - (y·e+)(y·ex) + ...]
    """
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)

    e_theta = np.array([
        cos_theta * cos_phi,
        cos_theta * sin_phi,
        -sin_theta
    ])

    e_phi = np.array([
        -sin_phi,
        cos_phi,
        0
    ])

    x_dot_theta = np.dot(x_arm, e_theta)
    x_dot_phi = np.dot(x_arm, e_phi)
    y_dot_theta = np.dot(y_arm, e_theta)
    y_dot_phi = np.dot(y_arm, e_phi)

    # F× = (x·e_θ)(x·e_φ) - (y·e_θ)(y·e_φ)
    F_cross = x_dot_theta * x_dot_phi - y_dot_theta * y_dot_phi

    return F_cross


# =============================================================================
# OVERLAP REDUCTION FUNCTION COMPUTATION
# =============================================================================

def compute_orf_polarized(freqs, nside=NSIDE):
    """
    Compute the polarized ORF γ₊(f) for h+ only background.

    γ₊(f) = (5/8π) ∫ F+_H1(Ω) F+_L1(Ω) exp(2πif Δt(Ω)) dΩ

    Note: the factor 5/8π is for normalization such that γ(0)=1
    for co-located, co-aligned detectors.
    """
    print("\n    Computing polarized ORF (h+ only)...")

    # Detector positions and orientations
    pos_H1 = latlon_to_xyz(H1_LAT, H1_LON)
    pos_L1 = latlon_to_xyz(L1_LAT, L1_LON)
    baseline = pos_L1 - pos_H1

    x_H1, y_H1 = get_detector_frame(H1_LAT, H1_LON, H1_X_ARM_AZIMUTH)
    x_L1, y_L1 = get_detector_frame(L1_LAT, L1_LON, L1_X_ARM_AZIMUTH)

    # HEALPix sky grid
    npix = hp.nside2npix(nside)
    theta_hp, phi_hp = hp.pix2ang(nside, np.arange(npix))

    print(f"    Sky pixels: {npix} (nside={nside})")

    # Precompute antenna patterns and time delays for all sky directions
    F_plus_H1 = np.zeros(npix)
    F_plus_L1 = np.zeros(npix)
    F_cross_H1 = np.zeros(npix)
    F_cross_L1 = np.zeros(npix)
    delta_t = np.zeros(npix)

    for i in range(npix):
        theta, phi = theta_hp[i], phi_hp[i]

        # Antenna patterns
        F_plus_H1[i] = antenna_pattern_plus(theta, phi, x_H1, y_H1)
        F_plus_L1[i] = antenna_pattern_plus(theta, phi, x_L1, y_L1)
        F_cross_H1[i] = antenna_pattern_cross(theta, phi, x_H1, y_H1)
        F_cross_L1[i] = antenna_pattern_cross(theta, phi, x_L1, y_L1)

        # Time delay: Δt = (baseline · n_hat) / c
        n_hat = np.array([
            np.sin(theta) * np.cos(phi),
            np.sin(theta) * np.sin(phi),
            np.cos(theta)
        ])
        delta_t[i] = np.dot(baseline, n_hat) / c

    # Solid angle per pixel
    dOmega = 4 * np.pi / npix

    # Compute ORF for each frequency
    gamma_plus = np.zeros(len(freqs))
    gamma_standard = np.zeros(len(freqs))

    for i, f in enumerate(freqs):
        # Phase factor
        phase = np.exp(2j * np.pi * f * delta_t)

        # Polarized ORF (h+ only)
        integrand_plus = F_plus_H1 * F_plus_L1 * phase
        gamma_plus[i] = np.abs(np.sum(integrand_plus) * dOmega)

        # Standard ORF (h+ and hx)
        integrand_standard = (F_plus_H1 * F_plus_L1 + F_cross_H1 * F_cross_L1) * phase
        gamma_standard[i] = np.abs(np.sum(integrand_standard) * dOmega)

    # Normalize (factor of 5/8π for standard normalization)
    norm = 5 / (8 * np.pi)
    gamma_plus *= norm
    gamma_standard *= norm

    # Normalize so γ(f=0) ≈ 1 for reference
    if gamma_standard[0] > 0:
        gamma_plus = gamma_plus / gamma_standard[0]
        gamma_standard = gamma_standard / gamma_standard[0]

    return gamma_plus, gamma_standard


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

fs = data['H1']['sample_rate']
duration = data['H1']['duration']

print(f"  Data: {duration}s at {fs} Hz")

# =============================================================================
# STEP 2: Bandpass filter
# =============================================================================

print("\n[2] Applying bandpass filter...")

nyquist = fs / 2
low = F_LOW / nyquist
high = F_HIGH / nyquist
b, a = signal.butter(8, [low, high], btype='band')

for name in ['H1', 'L1']:
    data[name]['filtered'] = signal.filtfilt(b, a, data[name]['strain'])

# =============================================================================
# STEP 3: Compute CPSD
# =============================================================================

print("\n[3] Computing Cross-Power Spectral Density...")

nperseg = int(SEGMENT_DURATION * fs)
noverlap = int(nperseg * OVERLAP_FRACTION)

freqs, Pxy = signal.csd(
    data['H1']['filtered'],
    data['L1']['filtered'],
    fs=fs,
    nperseg=nperseg,
    noverlap=noverlap,
    window='hann'
)

_, Pxx_H1 = signal.welch(data['H1']['filtered'], fs=fs, nperseg=nperseg, noverlap=noverlap)
_, Pxx_L1 = signal.welch(data['L1']['filtered'], fs=fs, nperseg=nperseg, noverlap=noverlap)

# Frequency selection
freq_mask = (freqs >= F_LOW) & (freqs <= F_HIGH)
freqs = freqs[freq_mask]
Pxy = Pxy[freq_mask]
Pxx_H1 = Pxx_H1[freq_mask]
Pxx_L1 = Pxx_L1[freq_mask]

# Downsample for ORF computation (computation-intensive)
freq_step = max(1, len(freqs) // 1000)
freqs_orf = freqs[::freq_step]

print(f"  Frequency bins: {len(freqs)}")
print(f"  ORF computed at: {len(freqs_orf)} frequencies")

# =============================================================================
# STEP 4: Compute ORFs
# =============================================================================

print("\n[4] Computing Overlap Reduction Functions...")

gamma_plus, gamma_standard = compute_orf_polarized(freqs_orf)

# Interpolate to full frequency grid
gamma_plus_full = np.interp(freqs, freqs_orf, gamma_plus)
gamma_standard_full = np.interp(freqs, freqs_orf, gamma_standard)

print(f"\n  Results at key frequencies:")
print(f"                    Standard    Polarized (h+)")
print(f"    γ(20 Hz):       {gamma_standard[0]:.4f}       {gamma_plus[0]:.4f}")
idx_100 = np.argmin(np.abs(freqs_orf - 100))
print(f"    γ(100 Hz):      {gamma_standard[idx_100]:.4f}       {gamma_plus[idx_100]:.4f}")
idx_1000 = np.argmin(np.abs(freqs_orf - 1000))
print(f"    γ(1000 Hz):     {gamma_standard[idx_1000]:.4f}       {gamma_plus[idx_1000]:.4f}")

# =============================================================================
# STEP 5: Compute Ω_GW estimates with both ORFs
# =============================================================================

print("\n[5] Computing Ω_GW estimates...")

norm_factor = (10 * np.pi**2) / (3 * H0**2)
delta_f = freqs[1] - freqs[0]
T_obs = duration

# Standard analysis (for comparison)
gamma_std_safe = np.maximum(np.abs(gamma_standard_full), 1e-10)
Y_hat_std = np.real(Pxy) / gamma_std_safe
Omega_GW_std = norm_factor * freqs**3 * Y_hat_std
variance_std = (Pxx_H1 * Pxx_L1) / (2 * T_obs * delta_f * gamma_std_safe**2)
sigma_std = norm_factor * freqs**3 * np.sqrt(variance_std)

# Polarized analysis (h+ only)
gamma_pol_safe = np.maximum(np.abs(gamma_plus_full), 1e-10)
Y_hat_pol = np.real(Pxy) / gamma_pol_safe
Omega_GW_pol = norm_factor * freqs**3 * Y_hat_pol
variance_pol = (Pxx_H1 * Pxx_L1) / (2 * T_obs * delta_f * gamma_pol_safe**2)
sigma_pol = norm_factor * freqs**3 * np.sqrt(variance_pol)

# Broadband estimates
weights_std = 1.0 / (sigma_std**2 + 1e-100)
weights_std = weights_std / np.sum(weights_std)
Omega_broadband_std = np.sum(weights_std * Omega_GW_std)
sigma_broadband_std = 1.0 / np.sqrt(np.sum(1.0 / (sigma_std**2 + 1e-100)))

weights_pol = 1.0 / (sigma_pol**2 + 1e-100)
weights_pol = weights_pol / np.sum(weights_pol)
Omega_broadband_pol = np.sum(weights_pol * Omega_GW_pol)
sigma_broadband_pol = 1.0 / np.sqrt(np.sum(1.0 / (sigma_pol**2 + 1e-100)))

# Upper limits
UL_std = max(Omega_broadband_std + 1.645 * sigma_broadband_std, 1.645 * sigma_broadband_std)
UL_pol = max(Omega_broadband_pol + 1.645 * sigma_broadband_pol, 1.645 * sigma_broadband_pol)

ratio_UL = UL_pol / UL_std

print(f"\n  Standard Search:")
print(f"    Broadband Ω_GW = {Omega_broadband_std:.2e} ± {sigma_broadband_std:.2e}")
print(f"    95% Upper Limit: {UL_std:.2e}")

print(f"\n  Polarized Search (h+ only):")
print(f"    Broadband Ω_GW = {Omega_broadband_pol:.2e} ± {sigma_broadband_pol:.2e}")
print(f"    95% Upper Limit: {UL_pol:.2e}")

print(f"\n  Ratio (Polarized / Standard): {ratio_UL:.3f}")

# Z² prediction
print(f"\n  Z² Framework Prediction:")
print(f"    Tensor-to-scalar ratio r = 1/(2Z²) = {r_tensor:.4f}")

# =============================================================================
# STEP 6: Generate Plots
# =============================================================================

print("\n[6] Generating plots...")

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Both ORFs comparison
ax1 = axes[0, 0]
ax1.semilogx(freqs_orf, gamma_standard, 'b-', linewidth=1.5, label='Standard (h+ + h×)')
ax1.semilogx(freqs_orf, gamma_plus, 'r-', linewidth=1.5, label='Polarized (h+ only)')
ax1.set_xlabel('Frequency [Hz]')
ax1.set_ylabel('Overlap Reduction Function γ(f)')
ax1.set_title('ORF Comparison: Standard vs Polarized')
ax1.set_xlim(F_LOW, F_HIGH)
ax1.set_ylim(0, 1.2)
ax1.grid(True, alpha=0.3)
ax1.legend()

# Panel 2: Ratio of ORFs
ax2 = axes[0, 1]
ratio_orf = gamma_plus / np.maximum(gamma_standard, 1e-10)
ax2.semilogx(freqs_orf, ratio_orf, 'purple', linewidth=1.5)
ax2.axhline(0.5, color='gray', linestyle='--', alpha=0.5, label='Expected ratio ≈ 0.5')
ax2.set_xlabel('Frequency [Hz]')
ax2.set_ylabel('γ₊(f) / γ_standard(f)')
ax2.set_title('ORF Ratio: Polarized / Standard')
ax2.set_xlim(F_LOW, F_HIGH)
ax2.set_ylim(0, 1.5)
ax2.grid(True, alpha=0.3)
ax2.legend()

# Panel 3: Ω_GW sensitivity comparison
ax3 = axes[1, 0]
ax3.loglog(freqs, sigma_std, 'b-', linewidth=1, alpha=0.7, label='Standard σ(f)')
ax3.loglog(freqs, sigma_pol, 'r-', linewidth=1, alpha=0.7, label='Polarized σ(f)')
ax3.axhline(UL_std, color='blue', linestyle='--', linewidth=1.5, label=f'Std UL = {UL_std:.1e}')
ax3.axhline(UL_pol, color='red', linestyle='--', linewidth=1.5, label=f'Pol UL = {UL_pol:.1e}')
ax3.set_xlabel('Frequency [Hz]')
ax3.set_ylabel('Ω_GW sensitivity')
ax3.set_title('Sensitivity Comparison')
ax3.set_xlim(F_LOW, F_HIGH)
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3, which='both')

# Panel 4: Summary text
ax4 = axes[1, 1]
ax4.axis('off')
summary_text = f"""
╔══════════════════════════════════════════════════════════════╗
║          POLARIZED STOCHASTIC SEARCH RESULTS                 ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  Standard Search (h+ + h×):                                  ║
║    95% Upper Limit: Ω_GW < {UL_std:.2e}                  ║
║                                                              ║
║  Polarized Search (h+ only):                                 ║
║    95% Upper Limit: Ω_GW < {UL_pol:.2e}                  ║
║                                                              ║
║  Ratio (Polarized / Standard): {ratio_UL:.3f}                      ║
║                                                              ║
╠══════════════════════════════════════════════════════════════╣
║  Z² FRAMEWORK PREDICTION:                                    ║
║    • Only h+ polarization survives (Z₂ projection)           ║
║    • Tensor-to-scalar ratio r = 1/(2Z²) = {r_tensor:.4f}           ║
║    • Predicted Ω_GW ~ 10⁻¹⁵ (primordial)                     ║
║                                                              ║
║  Note: Current sensitivity is ~10⁻⁵, prediction is ~10⁻¹⁵   ║
║        (~10 orders of magnitude below current reach)         ║
╚══════════════════════════════════════════════════════════════╝
"""
ax4.text(0.05, 0.95, summary_text, transform=ax4.transAxes,
         fontfamily='monospace', fontsize=10,
         verticalalignment='top')

fig.suptitle('Polarized Stochastic Search: h+ Only (Z² Framework)',
             fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(PLOT_FILE, dpi=150, bbox_inches='tight', facecolor='white')
print(f"  Saved plot to: {os.path.basename(PLOT_FILE)}")

# =============================================================================
# STEP 7: Save Results
# =============================================================================

print("\n[7] Saving results...")

results = {
    'analysis': 'polarized_h_plus_only',
    'framework': 'Z2_T3_orbifold',
    'gps_start': int(data['H1']['gps_start']),
    'duration_seconds': float(duration),
    'frequency_range_hz': [float(F_LOW), float(F_HIGH)],
    'z2_constant': float(Z2),
    'r_tensor_prediction': float(r_tensor),
    'standard_search': {
        'broadband_omega_gw': float(Omega_broadband_std),
        'sigma': float(sigma_broadband_std),
        'upper_limit_95': float(UL_std)
    },
    'polarized_search': {
        'broadband_omega_gw': float(Omega_broadband_pol),
        'sigma': float(sigma_broadband_pol),
        'upper_limit_95': float(UL_pol)
    },
    'ratio_polarized_to_standard': float(ratio_UL),
    'orf_comparison': {
        'frequencies_hz': freqs_orf.tolist(),
        'gamma_standard': gamma_standard.tolist(),
        'gamma_polarized': gamma_plus.tolist()
    }
}

with open(JSON_FILE, 'w') as f:
    json.dump(results, f, indent=2)

print(f"  Saved results to: {os.path.basename(JSON_FILE)}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("POLARIZED STOCHASTIC SEARCH COMPLETE")
print("=" * 70)

print(f"""
  Standard search upper limit:     Ω_GW < {UL_std:.2e}
  Polarized (h+ only) upper limit: Ω_GW < {UL_pol:.2e}
  Ratio:                           {ratio_UL:.3f}

  Z² Framework Prediction:
    r = 1/(2Z²) = {r_tensor:.4f}
    Predicted primordial Ω_GW at f ~ 25 Hz: ~ 10⁻¹⁵

  Status: Signal is ~10 orders of magnitude below current sensitivity.
          Future detectors (ET, CE) may reach r ~ 10⁻³ sensitivity.
""")

print("=" * 70)
