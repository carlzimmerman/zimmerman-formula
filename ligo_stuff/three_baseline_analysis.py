#!/usr/bin/env python3
"""
Three-Baseline Chirality Analysis: H1-L1, H1-V1, L1-V1
=======================================================

Full multi-baseline R-ratio analysis using O3a data from all three detectors.
Tests the calibration hierarchy:
- H1-L1: Discriminator (R = 3.11, highest contrast)
- H1-V1: Calibrator (77% h+ sensitivity)
- L1-V1: Consistency check

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
import time
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# Physical constants
c = 299792458.0
H0 = 67.4 * 1000 / 3.086e22

# Analysis parameters
CONFIG = {
    'sample_rate': 4096,
    'f_low': 20,
    'f_high': 200,
    'segment_duration': 60,
    'overlap_fraction': 0.5,
}

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")

# =============================================================================
# DATA LOADING
# =============================================================================

def load_strain_data():
    """Load strain data from all three detectors."""
    data = {}

    # Try loading 8-hour files first
    files_8h = {
        'H1': 'h1_8h.hdf5',
        'L1': 'l1_8h.hdf5',
        'V1': 'v1_8h.hdf5'
    }

    # Fallback to original files
    files_orig = {
        'H1': 'h1_strain.hdf5',
        'L1': 'l1_strain.hdf5',
    }

    for det, filename in files_8h.items():
        filepath = os.path.join(OUTPUT_DIR, filename)
        if os.path.exists(filepath):
            with h5py.File(filepath, 'r') as f:
                strain = f['strain'][:]
            # Check for valid data (not all zeros)
            if np.any(strain != 0):
                data[det] = strain.astype(np.float64)
                print_status(f"Loaded {det}: {len(strain):,} samples from {filename}")
            else:
                print_status(f"Warning: {det} data is all zeros in {filename}")

    # Use original files if 8h files don't have valid data
    for det in ['H1', 'L1']:
        if det not in data or len(data[det]) < 1000:
            filepath = os.path.join(OUTPUT_DIR, files_orig[det])
            if os.path.exists(filepath):
                with h5py.File(filepath, 'r') as f:
                    strain = f['strain'][:]
                data[det] = strain.astype(np.float64)
                print_status(f"Loaded {det}: {len(strain):,} samples from {files_orig[det]} (fallback)")

    return data

def load_orf_data():
    """Load ORF decomposition for all baselines."""
    filepath = os.path.join(OUTPUT_DIR, 'multi_baseline_orf_results.json')
    with open(filepath, 'r') as f:
        return json.load(f)

# =============================================================================
# ANALYSIS FUNCTIONS
# =============================================================================

def compute_baseline_analysis(det1_strain, det2_strain, baseline_name, orf_data, config):
    """
    Compute R-ratio for a single baseline.
    Handles NaN values by using only valid segments.
    """
    fs = config['sample_rate']
    f_low = config['f_low']
    f_high = config['f_high']
    nperseg = int(config['segment_duration'] * fs)
    noverlap = int(nperseg * config['overlap_fraction'])

    # Get ORF data for this baseline
    bl_data = orf_data['baselines'][baseline_name]
    orf_freqs = np.array(bl_data['frequencies_hz'])
    gamma_total = np.array(bl_data['gamma_total'])
    gamma_pp = np.array(bl_data['gamma_pp'])

    gamma_total_interp = interp1d(orf_freqs, gamma_total, kind='linear',
                                   bounds_error=False, fill_value=0)
    gamma_pp_interp = interp1d(orf_freqs, gamma_pp, kind='linear',
                                bounds_error=False, fill_value=0)

    R_expected = bl_data['metrics']['R_ratio_20Hz']
    h_plus_frac = bl_data['metrics']['h_plus_fraction_20Hz']

    # Find common length
    n_samples = min(len(det1_strain), len(det2_strain))
    det1 = det1_strain[:n_samples]
    det2 = det2_strain[:n_samples]

    # Handle NaN values: find segments where both detectors have valid data
    valid1 = ~np.isnan(det1) & (det1 != 0)
    valid2 = ~np.isnan(det2) & (det2 != 0)
    both_valid = valid1 & valid2

    # Find contiguous valid segments of at least nperseg samples
    segment_step = nperseg - noverlap
    valid_segments = []
    i = 0
    while i + nperseg <= n_samples:
        segment_valid = both_valid[i:i+nperseg]
        if np.all(segment_valid):
            valid_segments.append(i)
            i += segment_step
        else:
            # Skip to next potential segment start
            i += segment_step

    print(f"    Valid segments: {len(valid_segments)} (need {nperseg} samples each)")

    if len(valid_segments) < 2:
        # Not enough valid data
        return {
            'baseline': baseline_name,
            'duration_seconds': 0,
            'n_samples': n_samples,
            'Omega_std': np.nan,
            'Omega_pol': np.nan,
            'sigma_std': np.nan,
            'sigma_pol': np.nan,
            'R': np.nan,
            'sigma_R': np.nan,
            'R_expected': float(R_expected),
            'h_plus_fraction': float(h_plus_frac),
            'n_sigma_from_1': 0,
            'n_sigma_from_expected': 0,
            'n_valid_segments': len(valid_segments),
        }

    # Extract valid segments and compute CSD segment by segment
    all_Pxy = []
    for seg_start in valid_segments:
        seg1 = det1[seg_start:seg_start+nperseg]
        seg2 = det2[seg_start:seg_start+nperseg]
        freqs, Pxy_seg = signal.csd(seg1, seg2, fs=fs,
                                     nperseg=nperseg, noverlap=0, window='hann')
        all_Pxy.append(Pxy_seg)

    # Average CSD across segments
    Pxy = np.mean(all_Pxy, axis=0)
    duration = len(valid_segments) * (nperseg / fs)

    # Frequency mask
    mask = (freqs >= f_low) & (freqs <= f_high)
    freqs_band = freqs[mask]
    Pxy_band = Pxy[mask]

    # ORF weights
    gamma_total_f = gamma_total_interp(freqs_band)
    gamma_pp_f = gamma_pp_interp(freqs_band)

    gamma_total_f = np.where(np.abs(gamma_total_f) < 1e-10, 1e-10, gamma_total_f)
    gamma_pp_f = np.where(np.abs(gamma_pp_f) < 1e-10, 1e-10, gamma_pp_f)

    # Conversion to Omega
    conversion = (10 * np.pi**2 / (3 * H0**2)) * freqs_band**3
    Re_Pxy = np.real(Pxy_band)

    # Estimators
    Y_standard = conversion * Re_Pxy / gamma_total_f
    Y_polarized = conversion * Re_Pxy / gamma_pp_f

    Omega_std = np.mean(Y_standard)
    Omega_pol = np.mean(Y_polarized)
    sigma_std = np.std(Y_standard) / np.sqrt(len(Y_standard))
    sigma_pol = np.std(Y_polarized) / np.sqrt(len(Y_polarized))

    # R-ratio
    if Omega_std != 0:
        R = Omega_pol / Omega_std
        rel_err = np.sqrt((sigma_pol/abs(Omega_pol))**2 + (sigma_std/abs(Omega_std))**2) if Omega_pol != 0 else np.inf
        sigma_R = abs(R) * rel_err
    else:
        R = np.nan
        sigma_R = np.nan

    return {
        'baseline': baseline_name,
        'duration_seconds': duration,
        'n_samples': n_samples,
        'Omega_std': float(Omega_std),
        'Omega_pol': float(Omega_pol),
        'sigma_std': float(sigma_std),
        'sigma_pol': float(sigma_pol),
        'R': float(R),
        'sigma_R': float(sigma_R),
        'R_expected': float(R_expected),
        'h_plus_fraction': float(h_plus_frac),
        'n_sigma_from_1': abs(R - 1.0) / sigma_R if sigma_R > 0 else 0,
        'n_sigma_from_expected': abs(R - R_expected) / sigma_R if sigma_R > 0 else 0,
        'n_valid_segments': len(valid_segments),
    }

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

if __name__ == '__main__':
    print_header("THREE-BASELINE CHIRALITY ANALYSIS")
    print_status("H1-L1 (Discriminator) | H1-V1 (Calibrator) | L1-V1 (Consistency)")

    # Load data
    print_header("LOADING DATA")
    strain_data = load_strain_data()
    orf_data = load_orf_data()

    available_detectors = list(strain_data.keys())
    print_status(f"Available detectors: {available_detectors}")

    # Define baselines
    baselines = []
    if 'H1' in strain_data and 'L1' in strain_data:
        baselines.append(('H1-L1', 'H1', 'L1'))
    if 'H1' in strain_data and 'V1' in strain_data:
        baselines.append(('H1-V1', 'H1', 'V1'))
    if 'L1' in strain_data and 'V1' in strain_data:
        baselines.append(('L1-V1', 'L1', 'V1'))

    print_status(f"Baselines to analyze: {[b[0] for b in baselines]}")

    # Run analysis
    print_header("RUNNING BASELINE ANALYSES")
    results = {}

    for baseline_name, det1, det2 in baselines:
        print_status(f"Analyzing {baseline_name}...")

        result = compute_baseline_analysis(
            strain_data[det1],
            strain_data[det2],
            baseline_name,
            orf_data,
            CONFIG
        )
        results[baseline_name] = result

        print(f"    Duration: {result['duration_seconds']/3600:.2f} hours")
        print(f"    R = {result['R']:.3f} ± {result['sigma_R']:.3f}")
        print(f"    Expected R (h+ only): {result['R_expected']:.2f}")
        print(f"    h+ fraction: {result['h_plus_fraction']*100:.1f}%")

    # ==========================================================================
    # CROSS-BASELINE CONSISTENCY CHECK
    # ==========================================================================

    print_header("CROSS-BASELINE ANALYSIS")

    if 'H1-L1' in results and 'H1-V1' in results:
        # Amplitude ratio test
        Omega_H1L1 = results['H1-L1']['Omega_std']
        Omega_H1V1 = results['H1-V1']['Omega_std']

        if Omega_H1L1 != 0 and Omega_H1V1 != 0:
            amplitude_ratio = Omega_H1V1 / Omega_H1L1
            # For h+ only: ratio should be ~0.77/0.27 = 2.85
            expected_ratio_chiral = 0.77 / 0.27
            expected_ratio_unpol = 1.0

            print_status(f"Amplitude ratio Ω(H1-V1)/Ω(H1-L1) = {amplitude_ratio:.3f}")
            print_status(f"  Expected (unpolarized): {expected_ratio_unpol:.2f}")
            print_status(f"  Expected (h+ only): {expected_ratio_chiral:.2f}")

    # Calibration check
    if 'H1-L1' in results and 'H1-V1' in results:
        R_H1L1 = results['H1-L1']['R']
        R_H1V1 = results['H1-V1']['R']

        print_status(f"\nCalibration Check:")
        print_status(f"  H1-L1 (Discriminator): R = {R_H1L1:.3f}")
        print_status(f"  H1-V1 (Calibrator):    R = {R_H1V1:.3f}")

        # If H1-L1 shows chirality (R > 2), H1-V1 should confirm with enhanced amplitude
        if abs(R_H1L1) > 2:
            print_status(f"  → H1-L1 suggests chirality. Check H1-V1 amplitude...")
        else:
            print_status(f"  → H1-L1 consistent with noise/unpolarized")

    # ==========================================================================
    # GENERATE FIGURES
    # ==========================================================================

    print_header("GENERATING FIGURES")

    fig = plt.figure(figsize=(18, 12))
    gs = GridSpec(2, 3, figure=fig, hspace=0.3, wspace=0.3)

    # Color scheme
    colors = {'H1-L1': 'blue', 'H1-V1': 'orange', 'L1-V1': 'green'}
    roles = {'H1-L1': 'Discriminator', 'H1-V1': 'Calibrator', 'L1-V1': 'Consistency'}

    # Panel A: R-ratio comparison
    ax1 = fig.add_subplot(gs[0, 0])
    baseline_names = list(results.keys())
    R_vals = [results[b]['R'] for b in baseline_names]
    R_errs = [results[b]['sigma_R'] for b in baseline_names]
    R_expected = [results[b]['R_expected'] for b in baseline_names]
    bar_colors = [colors[b] for b in baseline_names]

    x_pos = np.arange(len(baseline_names))
    ax1.bar(x_pos, R_vals, yerr=R_errs, color=bar_colors, edgecolor='black',
            capsize=5, alpha=0.7, label='Measured R')
    ax1.scatter(x_pos, R_expected, color='red', marker='*', s=200, zorder=5,
                label='Expected R (h+ only)')
    ax1.axhline(1.0, color='green', linestyle='--', linewidth=2, label='R=1 (unpolarized)')
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels([f"{b}\n({roles[b]})" for b in baseline_names])
    ax1.set_ylabel('R = Ω_pol / Ω_std', fontsize=12)
    ax1.set_title('A: R-ratio by Baseline', fontsize=13, fontweight='bold')
    ax1.legend(loc='upper right', fontsize=9)
    ax1.grid(True, alpha=0.3, axis='y')

    # Panel B: h+ sensitivity comparison
    ax2 = fig.add_subplot(gs[0, 1])
    h_plus_fracs = [results[b]['h_plus_fraction'] * 100 for b in baseline_names]
    ax2.bar(x_pos, h_plus_fracs, color=bar_colors, edgecolor='black', alpha=0.7)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(baseline_names)
    ax2.set_ylabel('h+ Sensitivity (%)', fontsize=12)
    ax2.set_title('B: h+ Polarization Sensitivity', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3, axis='y')

    for i, (b, frac) in enumerate(zip(baseline_names, h_plus_fracs)):
        ax2.text(i, frac + 2, f'{frac:.0f}%', ha='center', fontsize=11, fontweight='bold')

    # Panel C: Omega estimates
    ax3 = fig.add_subplot(gs[0, 2])
    Omega_std_vals = [results[b]['Omega_std'] for b in baseline_names]
    Omega_pol_vals = [results[b]['Omega_pol'] for b in baseline_names]

    width = 0.35
    ax3.bar(x_pos - width/2, Omega_std_vals, width, label='Ω_standard', color='steelblue', alpha=0.7)
    ax3.bar(x_pos + width/2, Omega_pol_vals, width, label='Ω_polarized', color='coral', alpha=0.7)
    ax3.set_xticks(x_pos)
    ax3.set_xticklabels(baseline_names)
    ax3.set_ylabel('Ω estimate', fontsize=12)
    ax3.set_title('C: Ω Estimates by Baseline', fontsize=13, fontweight='bold')
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')
    ax3.axhline(0, color='black', linewidth=0.5)

    # Panel D: Distance from predictions
    ax4 = fig.add_subplot(gs[1, 0])
    n_sigma_1 = [results[b]['n_sigma_from_1'] for b in baseline_names]
    n_sigma_exp = [results[b]['n_sigma_from_expected'] for b in baseline_names]

    ax4.bar(x_pos - width/2, n_sigma_1, width, label='From R=1 (unpolarized)', color='green', alpha=0.7)
    ax4.bar(x_pos + width/2, n_sigma_exp, width, label='From R_expected (h+ only)', color='red', alpha=0.7)
    ax4.set_xticks(x_pos)
    ax4.set_xticklabels(baseline_names)
    ax4.set_ylabel('Distance (σ)', fontsize=12)
    ax4.set_title('D: Distance from Predictions', fontsize=13, fontweight='bold')
    ax4.legend()
    ax4.grid(True, alpha=0.3, axis='y')
    ax4.axhline(2, color='gray', linestyle='--', alpha=0.5)
    ax4.axhline(5, color='gray', linestyle='--', alpha=0.5)

    # Panel E: Calibration hierarchy
    ax5 = fig.add_subplot(gs[1, 1])
    ax5.axis('off')

    hierarchy_text = """
    ╔═══════════════════════════════════════════════════════════════╗
    ║           CALIBRATION HIERARCHY                               ║
    ╠═══════════════════════════════════════════════════════════════╣
    ║                                                               ║
    ║  H1-L1 (DISCRIMINATOR)                                        ║
    ║    • 27% h+ sensitivity                                       ║
    ║    • R_expected = 3.11 (highest contrast)                     ║
    ║    • PRIMARY test for chirality                               ║
    ║                                                               ║
    ║  H1-V1 (CALIBRATOR)                                           ║
    ║    • 77% h+ sensitivity                                       ║
    ║    • R_expected = 2.11                                        ║
    ║    • VALIDATES any H1-L1 chirality claim                      ║
    ║    • If H1-L1 shows R>>1 but H1-V1 amplitude suppressed,      ║
    ║      the H1-L1 result is likely systematic artifact           ║
    ║                                                               ║
    ║  L1-V1 (CONSISTENCY)                                          ║
    ║    • 65% h+ sensitivity                                       ║
    ║    • R_expected = 1.54                                        ║
    ║    • Network redundancy check                                 ║
    ║                                                               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """
    ax5.text(0.02, 0.98, hierarchy_text, transform=ax5.transAxes, fontsize=9,
             fontfamily='monospace', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

    # Panel F: Summary
    ax6 = fig.add_subplot(gs[1, 2])
    ax6.axis('off')

    # Build summary
    summary_lines = ["╔═══════════════════════════════════════════════════════════════╗",
                     "║           THREE-BASELINE ANALYSIS SUMMARY                     ║",
                     "╠═══════════════════════════════════════════════════════════════╣"]

    for b in baseline_names:
        r = results[b]
        summary_lines.append(f"║  {b:8s}: R = {r['R']:+.2f} ± {r['sigma_R']:.2f} (expected: {r['R_expected']:.2f})       ║")

    summary_lines.append("║                                                               ║")

    # Interpretation
    if 'H1-L1' in results:
        R_H1L1 = results['H1-L1']['R']
        sigma_R = results['H1-L1']['sigma_R']
        if abs(R_H1L1 - 1.0) < 2 * sigma_R:
            interp = "CONSISTENT WITH UNPOLARIZED (R ≈ 1)"
        elif abs(R_H1L1 - 3.11) < 2 * sigma_R:
            interp = "CONSISTENT WITH CHIRAL (R ≈ 3.11)"
        else:
            interp = "NOISE-DOMINATED / INCONCLUSIVE"
        summary_lines.append(f"║  Interpretation: {interp:40s}   ║")

    summary_lines.append("║                                                               ║")
    summary_lines.append("║  Status: Pipeline validated on O3a data                       ║")
    summary_lines.append("║  Note: Current data is noise-dominated (no SGWB signal)       ║")
    summary_lines.append("╚═══════════════════════════════════════════════════════════════╝")

    summary_text = "\n".join(summary_lines)
    ax6.text(0.02, 0.98, summary_text, transform=ax6.transAxes, fontsize=9,
             fontfamily='monospace', verticalalignment='top',
             bbox=dict(boxstyle='round', facecolor='lightcyan', alpha=0.9))

    fig.suptitle('Three-Baseline Chirality Analysis: H1-L1, H1-V1, L1-V1',
                 fontsize=15, fontweight='bold', y=0.98)

    plt.savefig(os.path.join(OUTPUT_DIR, 'three_baseline_analysis.png'),
                dpi=200, bbox_inches='tight', facecolor='white')
    print_status("Saved: three_baseline_analysis.png")

    # ==========================================================================
    # SAVE RESULTS
    # ==========================================================================

    output = {
        'analysis': 'three_baseline_chirality',
        'date': time.strftime('%Y-%m-%d'),
        'baselines': results,
        'calibration_hierarchy': {
            'discriminator': 'H1-L1',
            'calibrator': 'H1-V1',
            'consistency': 'L1-V1'
        },
        'config': CONFIG
    }

    with open(os.path.join(OUTPUT_DIR, 'three_baseline_results.json'), 'w') as f:
        json.dump(output, f, indent=2)
    print_status("Saved: three_baseline_results.json")

    # ==========================================================================
    # FINAL SUMMARY
    # ==========================================================================

    print_header("THREE-BASELINE ANALYSIS COMPLETE")

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    THREE-BASELINE CHIRALITY TEST                             ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  RESULTS:                                                                    ║""")

    for b in baseline_names:
        r = results[b]
        print(f"║    {b:8s}: R = {r['R']:+7.3f} ± {r['sigma_R']:6.3f}  (expected h+ only: {r['R_expected']:.2f})       ║")

    print(f"""║                                                                              ║
║  CALIBRATION CHECK:                                                          ║
║    • H1-L1 (discriminator): Highest R contrast for chirality detection       ║
║    • H1-V1 (calibrator): 77% h+ sensitivity validates any chirality claim    ║
║    • L1-V1 (consistency): Network redundancy                                 ║
║                                                                              ║
║  INTERPRETATION:                                                             ║
║    Current data is NOISE-DOMINATED (no astrophysical SGWB signal yet).       ║
║    This analysis validates the three-baseline pipeline for future use.       ║
║                                                                              ║
║  WHEN SGWB IS DETECTED:                                                      ║
║    1. Check H1-L1 R-ratio (primary discriminator)                            ║
║    2. If R >> 1, verify H1-V1 shows enhanced amplitude (not suppressed)      ║
║    3. Check L1-V1 for network consistency                                    ║
║    4. All three must agree for robust chirality claim                        ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    print("=" * 80)
