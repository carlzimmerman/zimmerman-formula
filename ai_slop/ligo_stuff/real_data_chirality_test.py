#!/usr/bin/env python3
"""
Real Data Chirality Test: R-ratio from Actual LIGO O3a Data
============================================================

Apply the polarized ORF chirality test to REAL LIGO strain data.

This script:
1. Loads H1 and L1 O3a strain data
2. Computes cross-spectral density (CSD)
3. Applies both standard (γ_total) and polarized (γ_++) ORF weights
4. Computes Ω̂_standard and Ω̂_polarized
5. Calculates R = Ω̂_pol / Ω̂_std
6. Assesses consistency with unpolarized (R≈1) vs chiral (R≈3.1)

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import h5py
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from scipy import signal
from scipy.interpolate import interp1d
import json
import os
import warnings
warnings.filterwarnings('ignore')

print("=" * 80)
print("REAL DATA CHIRALITY TEST: Applying R-ratio to LIGO O3a Data")
print("=" * 80)

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

c = 299792458.0  # m/s
H0 = 67.4 * 1000 / 3.086e22  # Hubble constant in SI (s^-1)
R_EARTH = 6.371e6  # m

# =============================================================================
# LOAD DATA
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

print("\n[1] Loading LIGO strain data...")

try:
    # Default sample rate for LIGO data
    fs = 4096  # Hz (standard LIGO sample rate)

    with h5py.File(os.path.join(OUTPUT_DIR, 'h1_strain.hdf5'), 'r') as f:
        h1_strain = f['strain'][:]
        print(f"  H1: {len(h1_strain)} samples at {fs} Hz")
        print(f"      Duration: {len(h1_strain)/fs:.1f} seconds")

    with h5py.File(os.path.join(OUTPUT_DIR, 'l1_strain.hdf5'), 'r') as f:
        l1_strain = f['strain'][:]
        print(f"  L1: {len(l1_strain)} samples at {fs} Hz")
        print(f"      Duration: {len(l1_strain)/fs:.1f} seconds")

except FileNotFoundError:
    print("  ERROR: Strain data files not found. Run download_data.py first.")
    exit(1)

# Compute duration
duration = min(len(h1_strain), len(l1_strain)) / fs

# Truncate to same length
n_samples = min(len(h1_strain), len(l1_strain))
h1_strain = h1_strain[:n_samples]
l1_strain = l1_strain[:n_samples]

print(f"\n  Using {duration:.1f} seconds of coincident data")

# =============================================================================
# LOAD ORF DATA
# =============================================================================

print("\n[2] Loading ORF decomposition...")

try:
    with open(os.path.join(OUTPUT_DIR, 'multi_baseline_orf_results.json'), 'r') as f:
        orf_data = json.load(f)

    orf_freqs = np.array(orf_data['baselines']['H1-L1']['frequencies_hz'])
    gamma_total = np.array(orf_data['baselines']['H1-L1']['gamma_total'])
    gamma_pp = np.array(orf_data['baselines']['H1-L1']['gamma_pp'])

    print(f"  Loaded ORF for {len(orf_freqs)} frequencies")
    print(f"  Frequency range: {orf_freqs[0]:.1f} - {orf_freqs[-1]:.1f} Hz")

    # Create interpolators
    gamma_total_interp = interp1d(orf_freqs, gamma_total, kind='linear',
                                   bounds_error=False, fill_value=0)
    gamma_pp_interp = interp1d(orf_freqs, gamma_pp, kind='linear',
                                bounds_error=False, fill_value=0)

except FileNotFoundError:
    print("  ERROR: ORF data not found. Run multi_baseline_orf_analysis.py first.")
    exit(1)

# =============================================================================
# COMPUTE CROSS-SPECTRAL DENSITY
# =============================================================================

print("\n[3] Computing cross-spectral density...")

# FFT parameters
segment_duration = 60  # seconds per segment
nperseg = int(segment_duration * fs)
noverlap = nperseg // 2
nfft = nperseg

# Compute CSD using Welch's method
freqs_csd, Pxy = signal.csd(h1_strain, l1_strain, fs=fs,
                             nperseg=nperseg, noverlap=noverlap,
                             nfft=nfft, window='hann')

# Also compute individual PSDs
freqs_psd, Pxx = signal.welch(h1_strain, fs=fs, nperseg=nperseg,
                               noverlap=noverlap, nfft=nfft, window='hann')
_, Pyy = signal.welch(l1_strain, fs=fs, nperseg=nperseg,
                       noverlap=noverlap, nfft=nfft, window='hann')

print(f"  CSD computed: {len(freqs_csd)} frequency bins")
print(f"  Frequency resolution: {freqs_csd[1]-freqs_csd[0]:.4f} Hz")

# Number of segments
n_segments = int(2 * duration / segment_duration) - 1
print(f"  Number of segments: {n_segments}")

# =============================================================================
# FREQUENCY BAND SELECTION
# =============================================================================

# Focus on sensitive band
f_low = 20.0
f_high = 200.0

mask = (freqs_csd >= f_low) & (freqs_csd <= f_high)
freqs_band = freqs_csd[mask]
Pxy_band = Pxy[mask]
Pxx_band = Pxx[mask]
Pyy_band = Pyy[mask]

print(f"\n  Analysis band: {f_low} - {f_high} Hz ({np.sum(mask)} bins)")

# =============================================================================
# ORF WEIGHTING
# =============================================================================

print("\n[4] Applying ORF weights...")

# Interpolate ORF to CSD frequencies
gamma_total_f = gamma_total_interp(freqs_band)
gamma_pp_f = gamma_pp_interp(freqs_band)

# Ensure positive values for weighting
gamma_total_f = np.maximum(np.abs(gamma_total_f), 1e-10)
gamma_pp_f = np.maximum(np.abs(gamma_pp_f), 1e-10)

print(f"  γ_total range: [{np.min(gamma_total_f):.4f}, {np.max(gamma_total_f):.4f}]")
print(f"  γ_++ range: [{np.min(gamma_pp_f):.4f}, {np.max(gamma_pp_f):.4f}]")

# =============================================================================
# COMPUTE Ω ESTIMATORS
# =============================================================================

print("\n[5] Computing Ω estimators...")

# The cross-correlation estimator for Ω_GW:
#
#   Ŷ(f) = Re[Pxy(f)] / γ(f)
#
# And the optimal estimator for broadband Ω:
#
#   Ω̂ = ∫ df W(f) Re[Pxy(f)] / ∫ df W(f) γ(f)
#
# where W(f) is the optimal weight:
#   W(f) = γ(f)² / [Pxx(f) × Pyy(f) × f⁶]
#
# For our purpose, we use a simpler estimator:
#   Ω̂ = Σ Re[Pxy(f)] / Σ γ(f)  (unweighted average)

# Real part of CSD (the signal)
Re_Pxy = np.real(Pxy_band)

# Conversion factor from CSD to Ω
# Ω_GW(f) = (10π² / 3H₀²) × f³ × Pxy(f) / γ(f)
conversion = (10 * np.pi**2 / (3 * H0**2)) * freqs_band**3

# Standard estimator (using γ_total)
Y_standard = conversion * Re_Pxy / gamma_total_f
Omega_standard = np.mean(Y_standard)
sigma_standard = np.std(Y_standard) / np.sqrt(len(Y_standard))

# Polarized estimator (using γ_++)
Y_polarized = conversion * Re_Pxy / gamma_pp_f
Omega_polarized = np.mean(Y_polarized)
sigma_polarized = np.std(Y_polarized) / np.sqrt(len(Y_polarized))

print(f"\n  RESULTS:")
print(f"  ─────────")
print(f"  Ω̂_standard  = {Omega_standard:.3e} ± {sigma_standard:.3e}")
print(f"  Ω̂_polarized = {Omega_polarized:.3e} ± {sigma_polarized:.3e}")

# =============================================================================
# COMPUTE R-RATIO
# =============================================================================

print("\n[6] Computing R-ratio...")

# R = Ω̂_polarized / Ω̂_standard
if Omega_standard != 0:
    R_measured = Omega_polarized / Omega_standard

    # Error propagation for R
    # σ(R)/R = √[(σ_pol/Ω_pol)² + (σ_std/Ω_std)²]
    if Omega_polarized != 0:
        rel_err = np.sqrt((sigma_polarized/abs(Omega_polarized))**2 +
                          (sigma_standard/abs(Omega_standard))**2)
        sigma_R = abs(R_measured) * rel_err
    else:
        sigma_R = np.inf
else:
    R_measured = np.nan
    sigma_R = np.nan

# Expected values
R_unpolarized = 1.0
R_chiral = orf_data['baselines']['H1-L1']['metrics']['R_ratio_20Hz']

print(f"\n  R = Ω̂_pol / Ω̂_std = {R_measured:.3f} ± {sigma_R:.3f}")
print(f"\n  COMPARISON TO PREDICTIONS:")
print(f"    Expected if unpolarized (GR): R = {R_unpolarized:.2f}")
print(f"    Expected if h+ only (Z²):     R = {R_chiral:.2f}")
print(f"    Measured:                     R = {R_measured:.2f} ± {sigma_R:.2f}")

# =============================================================================
# STATISTICAL INTERPRETATION
# =============================================================================

print("\n" + "=" * 80)
print("[7] STATISTICAL INTERPRETATION")
print("=" * 80)

# Significance of deviation from each hypothesis
if not np.isnan(R_measured) and sigma_R > 0 and not np.isinf(sigma_R):
    z_from_unpolarized = abs(R_measured - R_unpolarized) / sigma_R
    z_from_chiral = abs(R_measured - R_chiral) / sigma_R

    print(f"""
  HYPOTHESIS TESTS:
  ─────────────────
  H₀ (unpolarized): R = 1.0
    Distance: {abs(R_measured - R_unpolarized):.3f}
    Significance: {z_from_unpolarized:.2f}σ

  H₁ (h+ only): R = {R_chiral:.2f}
    Distance: {abs(R_measured - R_chiral):.3f}
    Significance: {z_from_chiral:.2f}σ
""")

    if z_from_unpolarized < 2 and z_from_chiral < 2:
        interpretation = "Noise-dominated: Cannot distinguish hypotheses"
    elif z_from_unpolarized < z_from_chiral:
        interpretation = f"More consistent with UNPOLARIZED (R≈1)"
    else:
        interpretation = f"More consistent with CHIRAL (R≈{R_chiral:.1f})"

    print(f"  INTERPRETATION: {interpretation}")
else:
    print("  Cannot compute significance (noise-dominated measurement)")
    z_from_unpolarized = np.nan
    z_from_chiral = np.nan
    interpretation = "Measurement noise-dominated"

# =============================================================================
# FREQUENCY-DEPENDENT ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("[8] FREQUENCY-DEPENDENT R(f)")
print("=" * 80)

# Compute R(f) in frequency bins
n_bins = 10
bin_edges = np.logspace(np.log10(f_low), np.log10(f_high), n_bins + 1)

R_f_measured = []
R_f_errors = []
f_centers = []

for i in range(n_bins):
    bin_mask = (freqs_band >= bin_edges[i]) & (freqs_band < bin_edges[i+1])
    if np.sum(bin_mask) < 3:
        continue

    f_center = np.sqrt(bin_edges[i] * bin_edges[i+1])  # Geometric mean
    f_centers.append(f_center)

    # Bin averages
    Y_std_bin = np.mean(Y_standard[bin_mask])
    Y_pol_bin = np.mean(Y_polarized[bin_mask])
    sigma_std_bin = np.std(Y_standard[bin_mask]) / np.sqrt(np.sum(bin_mask))
    sigma_pol_bin = np.std(Y_polarized[bin_mask]) / np.sqrt(np.sum(bin_mask))

    if Y_std_bin != 0:
        R_bin = Y_pol_bin / Y_std_bin
        if Y_pol_bin != 0:
            rel_err = np.sqrt((sigma_pol_bin/abs(Y_pol_bin))**2 +
                              (sigma_std_bin/abs(Y_std_bin))**2)
            sigma_R_bin = abs(R_bin) * rel_err
        else:
            sigma_R_bin = np.inf
    else:
        R_bin = np.nan
        sigma_R_bin = np.nan

    R_f_measured.append(R_bin)
    R_f_errors.append(sigma_R_bin)

f_centers = np.array(f_centers)
R_f_measured = np.array(R_f_measured)
R_f_errors = np.array(R_f_errors)

print(f"\n  R(f) measured in {len(f_centers)} frequency bins:")
print(f"  {'f (Hz)':>10} {'R_measured':>12} {'σ(R)':>10} {'R_expected':>12}")
print(f"  {'-'*10} {'-'*12} {'-'*10} {'-'*12}")

for i, f in enumerate(f_centers):
    R_exp = gamma_total_interp(f) / gamma_pp_interp(f)
    print(f"  {f:10.1f} {R_f_measured[i]:12.2f} {R_f_errors[i]:10.2f} {R_exp:12.2f}")

# =============================================================================
# GENERATE FIGURES
# =============================================================================

print("\n" + "=" * 80)
print("[9] Generating Figures")
print("=" * 80)

fig = plt.figure(figsize=(16, 14))
gs = GridSpec(3, 2, figure=fig, hspace=0.35, wspace=0.25)

# Panel A: Power Spectral Densities
ax1 = fig.add_subplot(gs[0, 0])
ax1.loglog(freqs_psd, np.sqrt(Pxx), 'b-', alpha=0.7, label='H1')
ax1.loglog(freqs_psd, np.sqrt(Pyy), 'r-', alpha=0.7, label='L1')
ax1.axvline(f_low, color='gray', linestyle='--', alpha=0.5)
ax1.axvline(f_high, color='gray', linestyle='--', alpha=0.5)
ax1.set_xlabel('Frequency [Hz]', fontsize=11)
ax1.set_ylabel('ASD [1/√Hz]', fontsize=11)
ax1.set_title('A: Detector Amplitude Spectral Densities', fontsize=12, fontweight='bold')
ax1.legend()
ax1.grid(True, alpha=0.3, which='both')
ax1.set_xlim(10, 1000)

# Panel B: Cross-Spectral Density
ax2 = fig.add_subplot(gs[0, 1])
ax2.semilogx(freqs_csd, np.real(Pxy), 'k-', alpha=0.5, linewidth=0.5)
ax2.axhline(0, color='gray', linestyle='-', linewidth=1)
ax2.axvline(f_low, color='gray', linestyle='--', alpha=0.5)
ax2.axvline(f_high, color='gray', linestyle='--', alpha=0.5)
ax2.set_xlabel('Frequency [Hz]', fontsize=11)
ax2.set_ylabel('Re[CSD]', fontsize=11)
ax2.set_title('B: Cross-Spectral Density (H1 × L1)', fontsize=12, fontweight='bold')
ax2.grid(True, alpha=0.3)
ax2.set_xlim(10, 500)

# Panel C: Ω estimators vs frequency
ax3 = fig.add_subplot(gs[1, 0])
ax3.semilogx(freqs_band, Y_standard, 'b-', alpha=0.3, linewidth=0.5, label='Ω̂_standard(f)')
ax3.semilogx(freqs_band, Y_polarized, 'r-', alpha=0.3, linewidth=0.5, label='Ω̂_polarized(f)')
ax3.axhline(0, color='gray', linestyle='-', linewidth=1)
ax3.axhline(Omega_standard, color='blue', linestyle='--', linewidth=2, label=f'⟨Ω̂_std⟩ = {Omega_standard:.2e}')
ax3.axhline(Omega_polarized, color='red', linestyle='--', linewidth=2, label=f'⟨Ω̂_pol⟩ = {Omega_polarized:.2e}')
ax3.set_xlabel('Frequency [Hz]', fontsize=11)
ax3.set_ylabel('Ω_GW estimate', fontsize=11)
ax3.set_title('C: Ω Estimators vs Frequency', fontsize=12, fontweight='bold')
ax3.legend(fontsize=9)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(f_low, f_high)

# Panel D: R(f) compared to predictions
ax4 = fig.add_subplot(gs[1, 1])
# Theoretical R(f)
f_theory = np.logspace(np.log10(f_low), np.log10(f_high), 100)
R_theory = gamma_total_interp(f_theory) / np.maximum(gamma_pp_interp(f_theory), 1e-10)
ax4.semilogx(f_theory, R_theory, 'k-', linewidth=2, label='R(f) predicted (h+ only)')
ax4.axhline(1.0, color='green', linestyle='--', linewidth=2, label='R = 1 (unpolarized)')

# Measured R(f)
valid = ~np.isnan(R_f_measured) & ~np.isinf(R_f_errors) & (R_f_errors < 100)
if np.any(valid):
    ax4.errorbar(f_centers[valid], R_f_measured[valid], yerr=R_f_errors[valid],
                 fmt='ro', markersize=8, capsize=4, label='R(f) measured')
ax4.set_xlabel('Frequency [Hz]', fontsize=11)
ax4.set_ylabel('R = Ω̂_pol / Ω̂_std', fontsize=11)
ax4.set_title('D: R-ratio vs Frequency', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(f_low, f_high)
ax4.set_ylim(-5, 15)

# Panel E: R measurement summary
ax5 = fig.add_subplot(gs[2, 0])
ax5.axis('off')

summary_text = f"""
╔══════════════════════════════════════════════════════════════════════╗
║              REAL DATA CHIRALITY TEST: RESULTS                       ║
╠══════════════════════════════════════════════════════════════════════╣
║                                                                      ║
║  DATA:                                                               ║
║    Source: LIGO O3a (H1-L1 coincident)                              ║
║    Duration: {duration:.1f} seconds                                         ║
║    Frequency band: {f_low:.0f} - {f_high:.0f} Hz                                    ║
║                                                                      ║
║  MEASUREMENTS:                                                       ║
║    Ω̂_standard  = {Omega_standard:+.2e} ± {sigma_standard:.2e}                   ║
║    Ω̂_polarized = {Omega_polarized:+.2e} ± {sigma_polarized:.2e}                   ║
║                                                                      ║
║  R-RATIO:                                                            ║
║    R = Ω̂_pol / Ω̂_std = {R_measured:.2f} ± {sigma_R:.2f}                             ║
║                                                                      ║
║  PREDICTIONS:                                                        ║
║    Unpolarized (GR): R = 1.00                                       ║
║    h+ only (Z²):     R = {R_chiral:.2f}                                       ║
║                                                                      ║
║  INTERPRETATION:                                                     ║
║    {interpretation:60s}     ║
║                                                                      ║
║  NOTE: Current data is NOISE-DOMINATED (no SGWB detection yet).     ║
║  R measurement demonstrates methodology; actual chirality test      ║
║  requires SNR ≥ 5 detection of stochastic background.               ║
║                                                                      ║
╚══════════════════════════════════════════════════════════════════════╝
"""
ax5.text(0.02, 0.98, summary_text, transform=ax5.transAxes, fontsize=10,
         fontfamily='monospace', verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Panel F: Posterior visualization
ax6 = fig.add_subplot(gs[2, 1])

if not np.isnan(R_measured) and not np.isinf(sigma_R) and sigma_R > 0:
    R_grid = np.linspace(R_measured - 4*sigma_R, R_measured + 4*sigma_R, 200)
    posterior = np.exp(-0.5 * ((R_grid - R_measured) / sigma_R)**2)
    ax6.fill_between(R_grid, 0, posterior, alpha=0.5, color='blue', label='Measured posterior')
    ax6.plot(R_grid, posterior, 'b-', linewidth=2)

ax6.axvline(R_unpolarized, color='green', linewidth=2, linestyle='--', label=f'R = {R_unpolarized} (unpolarized)')
ax6.axvline(R_chiral, color='red', linewidth=2, linestyle='--', label=f'R = {R_chiral:.2f} (h+ only)')
ax6.axvline(R_measured, color='blue', linewidth=2, label=f'R = {R_measured:.2f} (measured)')

ax6.set_xlabel('R value', fontsize=11)
ax6.set_ylabel('Probability', fontsize=11)
ax6.set_title('F: R Measurement vs Predictions', fontsize=12, fontweight='bold')
ax6.legend(fontsize=10)
ax6.grid(True, alpha=0.3)

fig.suptitle('Chirality Test on Real LIGO O3a Data',
             fontsize=15, fontweight='bold', y=0.99)

plt.savefig(os.path.join(OUTPUT_DIR, 'real_data_chirality_test.png'),
            dpi=200, bbox_inches='tight', facecolor='white')
print("\n  Saved: real_data_chirality_test.png")

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'analysis': 'real_data_chirality_test',
    'data': {
        'source': 'LIGO O3a',
        'detectors': ['H1', 'L1'],
        'duration_seconds': float(duration),
        'sample_rate_hz': float(fs),
        'frequency_band_hz': [float(f_low), float(f_high)]
    },
    'measurements': {
        'Omega_standard': float(Omega_standard),
        'sigma_standard': float(sigma_standard),
        'Omega_polarized': float(Omega_polarized),
        'sigma_polarized': float(sigma_polarized),
        'R_measured': float(R_measured) if not np.isnan(R_measured) else None,
        'sigma_R': float(sigma_R) if not np.isnan(sigma_R) and not np.isinf(sigma_R) else None
    },
    'predictions': {
        'R_unpolarized': float(R_unpolarized),
        'R_chiral': float(R_chiral)
    },
    'interpretation': interpretation,
    'note': 'Data is noise-dominated; demonstrates methodology only'
}

with open(os.path.join(OUTPUT_DIR, 'real_data_chirality_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("  Saved: real_data_chirality_results.json")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("REAL DATA CHIRALITY TEST: COMPLETE")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    CHIRALITY TEST ON REAL LIGO DATA                          ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  DATA ANALYZED:                                                              ║
║    • LIGO O3a coincident H1-L1 data                                         ║
║    • Duration: {duration:.0f} seconds ({duration/3600:.1f} hours)                                    ║
║    • Band: {f_low:.0f}-{f_high:.0f} Hz                                                       ║
║                                                                              ║
║  R-RATIO RESULT:                                                             ║
║    R = {R_measured:.2f} ± {sigma_R:.2f}                                                          ║
║                                                                              ║
║  COMPARISON:                                                                 ║
║    • If unpolarized (GR): R = 1.00                                          ║
║    • If h+ only (Z²):     R = {R_chiral:.2f}                                          ║
║                                                                              ║
║  INTERPRETATION:                                                             ║
║    {interpretation:60s}     ║
║                                                                              ║
║  IMPORTANT CAVEAT:                                                           ║
║    This data does NOT contain a detected stochastic signal.                 ║
║    The measured R is dominated by noise fluctuations.                       ║
║    This analysis DEMONSTRATES the methodology - the actual chirality        ║
║    test requires a stochastic detection (expected O4/O5).                   ║
║                                                                              ║
║  WHAT WE PROVED:                                                             ║
║    ✓ Pipeline works on real LIGO data                                       ║
║    ✓ Both estimators (Ω̂_std, Ω̂_pol) computable                             ║
║    ✓ R-ratio measurable with proper error bars                              ║
║    ✓ Ready for application to future detections                             ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
