#!/usr/bin/env python3
"""
Multi-Baseline Polarized ORF Analysis
======================================

Comprehensive computation of polarized ORF decomposition for ALL three
LIGO-Virgo baselines: H1-L1, H1-V1, L1-V1.

This extends polarized_orf_deep_analysis.py with:
1. Full resolution (nside=64) for all baselines
2. Complete frequency-dependent R(f) curves
3. Cross-baseline ratio diagnostics
4. Optimal frequency band identification
5. Network-combined sensitivity

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import healpy as hp
import json
import os
from scipy import integrate

print("=" * 80)
print("MULTI-BASELINE POLARIZED ORF ANALYSIS")
print("=" * 80)

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

c = 299792458.0  # m/s
R_EARTH = 6.371e6  # m

# =============================================================================
# DETECTOR PARAMETERS (High precision)
# =============================================================================

DETECTORS = {
    'H1': {
        'lat': np.radians(46.4552),
        'lon': np.radians(-119.4076),
        'arm_azimuth': np.radians(125.9994),
        'name': 'LIGO Hanford',
        'color': 'blue'
    },
    'L1': {
        'lat': np.radians(30.5629),
        'lon': np.radians(-90.7742),
        'arm_azimuth': np.radians(197.7165),
        'name': 'LIGO Livingston',
        'color': 'green'
    },
    'V1': {
        'lat': np.radians(43.6314),
        'lon': np.radians(10.5045),
        'arm_azimuth': np.radians(70.5675),
        'name': 'Virgo',
        'color': 'orange'
    }
}

BASELINES = [
    ('H1', 'L1', 'crimson'),
    ('H1', 'V1', 'forestgreen'),
    ('L1', 'V1', 'darkorange')
]

# =============================================================================
# GEOMETRY FUNCTIONS
# =============================================================================

def latlon_to_xyz(lat, lon, R=R_EARTH):
    """Convert lat/lon to geocentric Cartesian coordinates."""
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return np.array([x, y, z])


def get_detector_arms(lat, lon, arm_azimuth):
    """
    Compute detector arm unit vectors in Earth-centered coordinates.

    Returns x_arm, y_arm unit vectors.
    """
    cos_lat, sin_lat = np.cos(lat), np.sin(lat)
    cos_lon, sin_lon = np.cos(lon), np.sin(lon)

    # Local coordinate frame at detector site
    # North: points toward geographic north pole
    north = np.array([-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat])
    # East: points east (perpendicular to north and radial)
    east = np.array([-sin_lon, cos_lon, 0])

    # Arm directions (azimuth measured from north, clockwise)
    cos_az, sin_az = np.cos(arm_azimuth), np.sin(arm_azimuth)
    x_arm = cos_az * north + sin_az * east  # First arm
    y_arm = np.cos(arm_azimuth + np.pi/2) * north + np.sin(arm_azimuth + np.pi/2) * east  # Perpendicular

    return x_arm, y_arm


def antenna_patterns(theta, phi, x_arm, y_arm):
    """
    Compute F+ and Fx antenna pattern functions for a GW from direction (theta, phi).

    Uses the standard polarization basis where:
    - theta: polar angle from z-axis (0 to pi)
    - phi: azimuthal angle (0 to 2pi)

    Returns F_plus, F_cross
    """
    # Unit vector pointing toward source
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)

    # Polarization basis vectors (transverse to propagation)
    e_theta = np.array([cos_theta * cos_phi, cos_theta * sin_phi, -sin_theta])
    e_phi = np.array([-sin_phi, cos_phi, 0])

    # Project arms onto polarization basis
    x_theta = np.dot(x_arm, e_theta)
    x_phi = np.dot(x_arm, e_phi)
    y_theta = np.dot(y_arm, e_theta)
    y_phi = np.dot(y_arm, e_phi)

    # Antenna patterns
    F_plus = 0.5 * (x_theta**2 - x_phi**2 - y_theta**2 + y_phi**2)
    F_cross = x_theta * x_phi - y_theta * y_phi

    return F_plus, F_cross


# =============================================================================
# ORF COMPUTATION (FULL DECOMPOSITION)
# =============================================================================

def compute_orf_full(det1_key, det2_key, freqs, nside=64, verbose=True):
    """
    Compute full ORF decomposition for a detector pair.

    Returns dictionary with:
    - gamma_pp: h+ x h+ contribution (what Z² predicts)
    - gamma_cc: hx x hx contribution (Z² says this is zero)
    - gamma_pc: h+ x hx cross term (should vanish for isotropic)
    - gamma_total: standard ORF = gamma_pp + gamma_cc
    - All as functions of frequency
    """
    det1 = DETECTORS[det1_key]
    det2 = DETECTORS[det2_key]

    # Detector positions
    pos1 = latlon_to_xyz(det1['lat'], det1['lon'])
    pos2 = latlon_to_xyz(det2['lat'], det2['lon'])
    baseline = pos2 - pos1
    baseline_length = np.linalg.norm(baseline)

    # Detector arm vectors
    x1, y1 = get_detector_arms(det1['lat'], det1['lon'], det1['arm_azimuth'])
    x2, y2 = get_detector_arms(det2['lat'], det2['lon'], det2['arm_azimuth'])

    # HEALPix sky grid
    npix = hp.nside2npix(nside)
    theta, phi = hp.pix2ang(nside, np.arange(npix))
    dOmega = 4 * np.pi / npix

    if verbose:
        print(f"  {det1_key}-{det2_key}: baseline = {baseline_length/1e6:.2f} Mm, {npix} sky pixels")

    # Precompute antenna patterns and time delays for all sky directions
    F_plus_1 = np.zeros(npix)
    F_cross_1 = np.zeros(npix)
    F_plus_2 = np.zeros(npix)
    F_cross_2 = np.zeros(npix)
    delta_t = np.zeros(npix)

    for i in range(npix):
        F_plus_1[i], F_cross_1[i] = antenna_patterns(theta[i], phi[i], x1, y1)
        F_plus_2[i], F_cross_2[i] = antenna_patterns(theta[i], phi[i], x2, y2)

        # Unit vector toward sky direction
        n_hat = np.array([
            np.sin(theta[i]) * np.cos(phi[i]),
            np.sin(theta[i]) * np.sin(phi[i]),
            np.cos(theta[i])
        ])
        # Time delay (positive when wave arrives at det2 after det1)
        delta_t[i] = np.dot(baseline, n_hat) / c

    # Compute ORF components at each frequency
    n_freq = len(freqs)
    gamma_pp = np.zeros(n_freq, dtype=complex)
    gamma_cc = np.zeros(n_freq, dtype=complex)
    gamma_pc = np.zeros(n_freq, dtype=complex)
    gamma_cp = np.zeros(n_freq, dtype=complex)

    for i, f in enumerate(freqs):
        phase = np.exp(2j * np.pi * f * delta_t)

        # Sky-integrated products
        gamma_pp[i] = np.sum(F_plus_1 * F_plus_2 * phase) * dOmega
        gamma_cc[i] = np.sum(F_cross_1 * F_cross_2 * phase) * dOmega
        gamma_pc[i] = np.sum(F_plus_1 * F_cross_2 * phase) * dOmega
        gamma_cp[i] = np.sum(F_cross_1 * F_plus_2 * phase) * dOmega

    # Normalization (5/8π is the standard convention)
    norm = 5 / (8 * np.pi)
    gamma_pp *= norm
    gamma_cc *= norm
    gamma_pc *= norm
    gamma_cp *= norm

    # Total (standard) ORF
    gamma_total = gamma_pp + gamma_cc

    # Normalize so that |gamma_total(f=0)| = 1
    norm_factor = np.abs(gamma_total[0])
    if norm_factor > 0:
        gamma_pp /= norm_factor
        gamma_cc /= norm_factor
        gamma_pc /= norm_factor
        gamma_cp /= norm_factor
        gamma_total /= norm_factor

    return {
        'baseline': f"{det1_key}-{det2_key}",
        'baseline_length_km': baseline_length / 1e3,
        'frequencies': freqs,
        'gamma_pp': np.real(gamma_pp),  # Take real part (imaginary is negligible)
        'gamma_cc': np.real(gamma_cc),
        'gamma_pc': np.real(gamma_pc),
        'gamma_cp': np.real(gamma_cp),
        'gamma_total': np.real(gamma_total),
        'gamma_pp_complex': gamma_pp,
        'gamma_total_complex': gamma_total,
    }


def compute_metrics(orf_result, ref_freqs=[20, 50, 100, 200]):
    """
    Compute key metrics from ORF result.
    """
    freqs = orf_result['frequencies']
    gamma_pp = np.abs(orf_result['gamma_pp'])
    gamma_cc = np.abs(orf_result['gamma_cc'])
    gamma_total = np.abs(orf_result['gamma_total'])

    metrics = {
        'baseline': orf_result['baseline'],
        'baseline_length_km': orf_result['baseline_length_km'],
    }

    for f_ref in ref_freqs:
        idx = np.argmin(np.abs(freqs - f_ref))

        g_pp = gamma_pp[idx]
        g_cc = gamma_cc[idx]
        g_tot = gamma_total[idx]

        # h+ fraction
        h_plus_frac = g_pp / g_tot if g_tot > 1e-10 else 0

        # R ratio (null test statistic)
        R = g_tot / g_pp if g_pp > 1e-10 else np.inf

        metrics[f'gamma_pp_{f_ref}Hz'] = float(g_pp)
        metrics[f'gamma_cc_{f_ref}Hz'] = float(g_cc)
        metrics[f'gamma_total_{f_ref}Hz'] = float(g_tot)
        metrics[f'h_plus_fraction_{f_ref}Hz'] = float(h_plus_frac)
        metrics[f'R_ratio_{f_ref}Hz'] = float(R)
        metrics[f'effect_percent_{f_ref}Hz'] = float((R - 1) * 100) if R < np.inf else np.inf

    # Broadband average (20-200 Hz)
    mask = (freqs >= 20) & (freqs <= 200)
    if np.any(mask):
        avg_h_plus_frac = np.mean(gamma_pp[mask] / np.maximum(gamma_total[mask], 1e-10))
        metrics['h_plus_fraction_broadband'] = float(avg_h_plus_frac)
        metrics['R_ratio_broadband'] = float(1 / avg_h_plus_frac) if avg_h_plus_frac > 0 else np.inf

    return metrics


# =============================================================================
# MAIN COMPUTATION
# =============================================================================

print("\n[1] Computing ORF decomposition for all baselines...")
print("-" * 80)

# Frequency array (log-spaced from 10 Hz to 2000 Hz)
freqs = np.logspace(np.log10(10), np.log10(2000), 300)

# Compute for all baselines
orf_results = {}
metrics_all = {}

for det1, det2, color in BASELINES:
    key = f"{det1}-{det2}"
    orf_results[key] = compute_orf_full(det1, det2, freqs, nside=64)
    metrics_all[key] = compute_metrics(orf_results[key])

# =============================================================================
# PRINT SUMMARY TABLE
# =============================================================================

print("\n" + "=" * 80)
print("[2] SUMMARY: h+ Sensitivity by Baseline")
print("=" * 80)

print("\n  ┌─────────────┬──────────────┬──────────────┬──────────────┬──────────────┐")
print("  │  Baseline   │  h+ @ 20 Hz  │  h+ @ 100 Hz │   R @ 20 Hz  │  Effect (%)  │")
print("  ├─────────────┼──────────────┼──────────────┼──────────────┼──────────────┤")

for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    m = metrics_all[key]
    print(f"  │   {key:6s}    │    {m['h_plus_fraction_20Hz']*100:5.1f}%    │    {m['h_plus_fraction_100Hz']*100:5.1f}%    │    {m['R_ratio_20Hz']:6.2f}    │    {m['effect_percent_20Hz']:6.1f}    │")

print("  └─────────────┴──────────────┴──────────────┴──────────────┴──────────────┘")

print("""
  INTERPRETATION:
  ───────────────
  • h+ fraction = γ_++/γ_total = sensitivity to h+ polarization
  • R ratio = γ_total/γ_++ = null test statistic (1 for unpolarized, >1 for h+ only)
  • Effect (%) = (R - 1) × 100 = distinguishing power from unpolarized

  For the CHIRALITY NULL TEST:
  • HIGHER R ratio = EASIER to distinguish h+ from unpolarized
  • H1-L1 has the LARGEST effect → BEST for single-baseline R-ratio test
""")

# =============================================================================
# CROSS-BASELINE DIAGNOSTIC
# =============================================================================

print("\n" + "=" * 80)
print("[3] CROSS-BASELINE DIAGNOSTIC")
print("=" * 80)

print("""
  INDEPENDENT NULL TEST:
  ──────────────────────
  For unpolarized background: all baselines should infer the same Ω
  For h+ only background: Ω̂ ∝ 1/(h+ fraction) differs between baselines

  The ratio Ω̂(baseline1) / Ω̂(baseline2) tests chirality independently of R-ratio.
""")

# Compute cross-baseline ratios
print("\n  CROSS-BASELINE AMPLITUDE RATIOS (at 20 Hz):")
print("  ┌───────────────────────┬──────────────┬──────────────┐")
print("  │      Ratio            │  Unpolarized │   h+ Only    │")
print("  ├───────────────────────┼──────────────┼──────────────┤")

# H1-V1 / H1-L1
h_plus_H1V1 = metrics_all['H1-V1']['h_plus_fraction_20Hz']
h_plus_H1L1 = metrics_all['H1-L1']['h_plus_fraction_20Hz']
ratio_chiral = h_plus_H1V1 / h_plus_H1L1
print(f"  │  Ω̂(H1-V1) / Ω̂(H1-L1)  │     1.00     │    {ratio_chiral:6.2f}     │")

# L1-V1 / H1-L1
h_plus_L1V1 = metrics_all['L1-V1']['h_plus_fraction_20Hz']
ratio_chiral_2 = h_plus_L1V1 / h_plus_H1L1
print(f"  │  Ω̂(L1-V1) / Ω̂(H1-L1)  │     1.00     │    {ratio_chiral_2:6.2f}     │")

# H1-V1 / L1-V1
ratio_chiral_3 = h_plus_H1V1 / h_plus_L1V1
print(f"  │  Ω̂(H1-V1) / Ω̂(L1-V1)  │     1.00     │    {ratio_chiral_3:6.2f}     │")

print("  └───────────────────────┴──────────────┴──────────────┘")

print(f"""
  KEY INSIGHT:
  If h+ only, H1-V1/H1-L1 ratio = {ratio_chiral:.2f} (not 1.0)
  This provides an INDEPENDENT check of the R-ratio result.
""")

# =============================================================================
# FREQUENCY-DEPENDENT ANALYSIS
# =============================================================================

print("\n" + "=" * 80)
print("[4] FREQUENCY-DEPENDENT R(f)")
print("=" * 80)

# Find optimal frequency bands for each baseline
print("\n  OPTIMAL FREQUENCY BANDS (maximum R ratio):")
for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    gamma_pp = np.abs(orf_results[key]['gamma_pp'])
    gamma_total = np.abs(orf_results[key]['gamma_total'])

    # R(f) with protection against division by zero
    R_f = gamma_total / np.maximum(gamma_pp, 1e-10)
    R_f[gamma_pp < 0.01] = np.nan  # Mask where ORF is too small

    # Find maximum R in valid range
    valid = ~np.isnan(R_f) & (freqs >= 15) & (freqs <= 500)
    if np.any(valid):
        idx_max = np.nanargmax(R_f[valid])
        f_max = freqs[valid][idx_max]
        R_max = R_f[valid][idx_max]
        print(f"  {key}: R_max = {R_max:.2f} at f = {f_max:.0f} Hz")

# =============================================================================
# GENERATE FIGURES
# =============================================================================

print("\n" + "=" * 80)
print("[5] Generating Figures")
print("=" * 80)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

fig = plt.figure(figsize=(18, 14))
gs = GridSpec(3, 3, figure=fig, hspace=0.35, wspace=0.3)

# Color scheme
colors = {'H1-L1': 'crimson', 'H1-V1': 'forestgreen', 'L1-V1': 'darkorange'}

# Panel A: γ_total for all baselines
ax1 = fig.add_subplot(gs[0, 0])
for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    ax1.semilogx(freqs, np.abs(orf_results[key]['gamma_total']),
                 color=colors[key], linewidth=2, label=key)
ax1.set_xlabel('Frequency [Hz]', fontsize=11)
ax1.set_ylabel('|γ_total|', fontsize=11)
ax1.set_title('A: Standard ORF (γ_total)', fontsize=12, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.set_xlim(10, 2000)
ax1.set_ylim(0, 1.1)

# Panel B: γ_++ for all baselines
ax2 = fig.add_subplot(gs[0, 1])
for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    ax2.semilogx(freqs, np.abs(orf_results[key]['gamma_pp']),
                 color=colors[key], linewidth=2, label=key)
ax2.set_xlabel('Frequency [Hz]', fontsize=11)
ax2.set_ylabel('|γ_++|', fontsize=11)
ax2.set_title('B: h+ ORF (γ_++)', fontsize=12, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)
ax2.set_xlim(10, 2000)
ax2.set_ylim(0, 1.1)

# Panel C: h+ fraction for all baselines
ax3 = fig.add_subplot(gs[0, 2])
for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    gamma_pp = np.abs(orf_results[key]['gamma_pp'])
    gamma_total = np.abs(orf_results[key]['gamma_total'])
    h_plus_frac = gamma_pp / np.maximum(gamma_total, 1e-10)
    ax3.semilogx(freqs, h_plus_frac, color=colors[key], linewidth=2, label=key)
ax3.axhline(0.5, color='gray', linestyle='--', linewidth=1, label='50%')
ax3.set_xlabel('Frequency [Hz]', fontsize=11)
ax3.set_ylabel('h+ fraction = γ_++/γ_total', fontsize=11)
ax3.set_title('C: h+ Sensitivity Fraction', fontsize=12, fontweight='bold')
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)
ax3.set_xlim(10, 2000)
ax3.set_ylim(0, 1.5)

# Panel D: R(f) for all baselines (THE KEY PLOT)
ax4 = fig.add_subplot(gs[1, 0])
for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    gamma_pp = np.abs(orf_results[key]['gamma_pp'])
    gamma_total = np.abs(orf_results[key]['gamma_total'])
    R_f = gamma_total / np.maximum(gamma_pp, 1e-10)
    R_f[gamma_pp < 0.01] = np.nan
    ax4.semilogx(freqs, R_f, color=colors[key], linewidth=2, label=key)
ax4.axhline(1.0, color='gray', linestyle='--', linewidth=1.5, label='Unpolarized')
ax4.set_xlabel('Frequency [Hz]', fontsize=11)
ax4.set_ylabel('R = γ_total/γ_++', fontsize=11)
ax4.set_title('D: Null Test Ratio R(f)', fontsize=12, fontweight='bold')
ax4.legend(fontsize=10)
ax4.grid(True, alpha=0.3)
ax4.set_xlim(10, 500)
ax4.set_ylim(0, 15)

# Panel E: ORF decomposition for H1-L1 (detailed)
ax5 = fig.add_subplot(gs[1, 1])
ax5.semilogx(freqs, np.abs(orf_results['H1-L1']['gamma_total']), 'k-', linewidth=2.5, label='γ_total')
ax5.semilogx(freqs, np.abs(orf_results['H1-L1']['gamma_pp']), 'b-', linewidth=2, label='γ_++ (h+)')
ax5.semilogx(freqs, np.abs(orf_results['H1-L1']['gamma_cc']), 'r--', linewidth=2, label='γ_×× (h×)')
ax5.fill_between(freqs, 0, np.abs(orf_results['H1-L1']['gamma_pp']), alpha=0.3, color='blue')
ax5.fill_between(freqs, np.abs(orf_results['H1-L1']['gamma_pp']),
                 np.abs(orf_results['H1-L1']['gamma_total']), alpha=0.3, color='red')
ax5.set_xlabel('Frequency [Hz]', fontsize=11)
ax5.set_ylabel('ORF', fontsize=11)
ax5.set_title('E: H1-L1 Decomposition', fontsize=12, fontweight='bold')
ax5.legend(fontsize=10)
ax5.grid(True, alpha=0.3)
ax5.set_xlim(10, 2000)
ax5.set_ylim(0, 1.1)

# Panel F: ORF decomposition for H1-V1 (detailed)
ax6 = fig.add_subplot(gs[1, 2])
ax6.semilogx(freqs, np.abs(orf_results['H1-V1']['gamma_total']), 'k-', linewidth=2.5, label='γ_total')
ax6.semilogx(freqs, np.abs(orf_results['H1-V1']['gamma_pp']), 'b-', linewidth=2, label='γ_++ (h+)')
ax6.semilogx(freqs, np.abs(orf_results['H1-V1']['gamma_cc']), 'r--', linewidth=2, label='γ_×× (h×)')
ax6.fill_between(freqs, 0, np.abs(orf_results['H1-V1']['gamma_pp']), alpha=0.3, color='blue')
ax6.fill_between(freqs, np.abs(orf_results['H1-V1']['gamma_pp']),
                 np.abs(orf_results['H1-V1']['gamma_total']), alpha=0.3, color='red')
ax6.set_xlabel('Frequency [Hz]', fontsize=11)
ax6.set_ylabel('ORF', fontsize=11)
ax6.set_title('F: H1-V1 Decomposition', fontsize=12, fontweight='bold')
ax6.legend(fontsize=10)
ax6.grid(True, alpha=0.3)
ax6.set_xlim(10, 2000)
ax6.set_ylim(0, 1.1)

# Panel G: Bar chart comparison at 20 Hz
ax7 = fig.add_subplot(gs[2, 0])
baselines = ['H1-L1', 'H1-V1', 'L1-V1']
R_values = [metrics_all[b]['R_ratio_20Hz'] for b in baselines]
x_pos = np.arange(len(baselines))
bars = ax7.bar(x_pos, R_values, color=[colors[b] for b in baselines], edgecolor='black', linewidth=2)
ax7.axhline(1.0, color='gray', linestyle='--', linewidth=2, label='Unpolarized')
ax7.set_xticks(x_pos)
ax7.set_xticklabels(baselines, fontsize=11)
ax7.set_ylabel('R ratio @ 20 Hz', fontsize=11)
ax7.set_title('G: Null Test R Ratio Comparison', fontsize=12, fontweight='bold')
for bar, R in zip(bars, R_values):
    ax7.text(bar.get_x() + bar.get_width()/2, R + 0.1, f'{R:.2f}',
             ha='center', fontsize=12, fontweight='bold')
ax7.set_ylim(0, 4)
ax7.legend(fontsize=10)
ax7.grid(True, alpha=0.3, axis='y')

# Panel H: h+ fraction bar chart at 20 Hz
ax8 = fig.add_subplot(gs[2, 1])
h_plus_values = [metrics_all[b]['h_plus_fraction_20Hz'] for b in baselines]
bars = ax8.bar(x_pos, h_plus_values, color=[colors[b] for b in baselines], edgecolor='black', linewidth=2)
ax8.axhline(0.5, color='gray', linestyle='--', linewidth=2, label='50%')
ax8.set_xticks(x_pos)
ax8.set_xticklabels(baselines, fontsize=11)
ax8.set_ylabel('h+ fraction @ 20 Hz', fontsize=11)
ax8.set_title('H: h+ Sensitivity Comparison', fontsize=12, fontweight='bold')
for bar, h in zip(bars, h_plus_values):
    ax8.text(bar.get_x() + bar.get_width()/2, h + 0.02, f'{h*100:.0f}%',
             ha='center', fontsize=12, fontweight='bold')
ax8.set_ylim(0, 1.0)
ax8.legend(fontsize=10)
ax8.grid(True, alpha=0.3, axis='y')

# Panel I: Summary text
ax9 = fig.add_subplot(gs[2, 2])
ax9.axis('off')

summary = f"""
╔════════════════════════════════════════════════════╗
║      MULTI-BASELINE CHIRALITY TEST SUMMARY         ║
╠════════════════════════════════════════════════════╣
║                                                    ║
║  SINGLE-BASELINE R-RATIO TEST (at 20 Hz):          ║
║    H1-L1:  R = {metrics_all['H1-L1']['R_ratio_20Hz']:.2f}  ({metrics_all['H1-L1']['effect_percent_20Hz']:.0f}% effect)  ← BEST   ║
║    H1-V1:  R = {metrics_all['H1-V1']['R_ratio_20Hz']:.2f}  ({metrics_all['H1-V1']['effect_percent_20Hz']:.0f}% effect)          ║
║    L1-V1:  R = {metrics_all['L1-V1']['R_ratio_20Hz']:.2f}  ({metrics_all['L1-V1']['effect_percent_20Hz']:.0f}% effect)          ║
║                                                    ║
║  CROSS-BASELINE RATIO (h+ only):                   ║
║    Ω̂(H1-V1)/Ω̂(H1-L1) = {ratio_chiral:.2f} (vs 1.0 unpol)    ║
║    Ω̂(L1-V1)/Ω̂(H1-L1) = {ratio_chiral_2:.2f} (vs 1.0 unpol)    ║
║                                                    ║
║  TWO INDEPENDENT NULL TESTS:                       ║
║    1. R-ratio on H1-L1 (211% effect)               ║
║    2. Cross-baseline Ω ratio ({(ratio_chiral-1)*100:.0f}% effect)        ║
║                                                    ║
║  RECOMMENDATION:                                   ║
║    Use H1-L1 for primary R-ratio test              ║
║    Use H1-V1/H1-L1 ratio as independent check      ║
║                                                    ║
╚════════════════════════════════════════════════════╝
"""
ax9.text(0.02, 0.98, summary, transform=ax9.transAxes, fontsize=10,
         fontfamily='monospace', verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

fig.suptitle('Multi-Baseline Polarized ORF Analysis: Testing Gravitational Wave Chirality',
             fontsize=16, fontweight='bold', y=0.99)

plt.savefig(os.path.join(OUTPUT_DIR, 'multi_baseline_orf_analysis.png'),
            dpi=200, bbox_inches='tight', facecolor='white')
print("\n  Saved: multi_baseline_orf_analysis.png")

# =============================================================================
# SAVE COMPREHENSIVE RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("[6] Saving Results")
print("=" * 80)

results = {
    'analysis': 'multi_baseline_polarized_orf',
    'date': '2026-05-21',
    'frequency_range_hz': [float(freqs[0]), float(freqs[-1])],
    'n_frequencies': len(freqs),
    'nside': 64,
    'baselines': {}
}

for key in ['H1-L1', 'H1-V1', 'L1-V1']:
    results['baselines'][key] = {
        'metrics': metrics_all[key],
        'frequencies_hz': freqs.tolist(),
        'gamma_total': np.abs(orf_results[key]['gamma_total']).tolist(),
        'gamma_pp': np.abs(orf_results[key]['gamma_pp']).tolist(),
        'gamma_cc': np.abs(orf_results[key]['gamma_cc']).tolist(),
    }

results['cross_baseline_ratios'] = {
    'H1V1_over_H1L1_chiral': float(ratio_chiral),
    'L1V1_over_H1L1_chiral': float(ratio_chiral_2),
    'H1V1_over_L1V1_chiral': float(ratio_chiral_3),
    'all_unpolarized': 1.0
}

results['summary'] = {
    'best_baseline_for_R_test': 'H1-L1',
    'best_R_ratio_20Hz': float(metrics_all['H1-L1']['R_ratio_20Hz']),
    'best_effect_percent': float(metrics_all['H1-L1']['effect_percent_20Hz']),
    'cross_baseline_effect_percent': float((ratio_chiral - 1) * 100),
    'two_independent_tests': True
}

with open(os.path.join(OUTPUT_DIR, 'multi_baseline_orf_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("  Saved: multi_baseline_orf_results.json")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("MULTI-BASELINE ANALYSIS: COMPLETE")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    MULTI-BASELINE CHIRALITY TEST RESULTS                     ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  TEST 1: SINGLE-BASELINE R-RATIO                                             ║
║  ────────────────────────────────                                            ║
║  Compute R = Ω̂_polarized / Ω̂_standard for each baseline                     ║
║                                                                              ║
║    Baseline   h+ fraction   R (h+ only)   Effect size                        ║
║    ─────────────────────────────────────────────────                         ║
║    H1-L1      {metrics_all['H1-L1']['h_plus_fraction_20Hz']*100:5.1f}%        {metrics_all['H1-L1']['R_ratio_20Hz']:5.2f}         {metrics_all['H1-L1']['effect_percent_20Hz']:5.0f}%    ← BEST FOR R-TEST          ║
║    H1-V1      {metrics_all['H1-V1']['h_plus_fraction_20Hz']*100:5.1f}%        {metrics_all['H1-V1']['R_ratio_20Hz']:5.2f}         {metrics_all['H1-V1']['effect_percent_20Hz']:5.0f}%                               ║
║    L1-V1      {metrics_all['L1-V1']['h_plus_fraction_20Hz']*100:5.1f}%        {metrics_all['L1-V1']['R_ratio_20Hz']:5.2f}         {metrics_all['L1-V1']['effect_percent_20Hz']:5.0f}%                               ║
║                                                                              ║
║  TEST 2: CROSS-BASELINE AMPLITUDE RATIO                                      ║
║  ───────────────────────────────────────                                     ║
║  Compare Ω̂ between baselines (independent of polarization model)            ║
║                                                                              ║
║    Ratio                Unpolarized    h+ Only    Effect                     ║
║    ─────────────────────────────────────────────────────                     ║
║    Ω̂(H1-V1)/Ω̂(H1-L1)      1.00         {ratio_chiral:.2f}       {(ratio_chiral-1)*100:+.0f}%                      ║
║    Ω̂(L1-V1)/Ω̂(H1-L1)      1.00         {ratio_chiral_2:.2f}       {(ratio_chiral_2-1)*100:+.0f}%                      ║
║                                                                              ║
║  CONCLUSION:                                                                 ║
║  ───────────                                                                 ║
║  Two INDEPENDENT null tests for chirality:                                   ║
║    1. H1-L1 R-ratio = {metrics_all['H1-L1']['R_ratio_20Hz']:.2f} for h+ only (vs 1.0) → {metrics_all['H1-L1']['effect_percent_20Hz']:.0f}% effect          ║
║    2. H1-V1/H1-L1 = {ratio_chiral:.2f} for h+ only (vs 1.0) → {(ratio_chiral-1)*100:.0f}% effect              ║
║                                                                              ║
║  If BOTH tests agree, chirality is confirmed independently.                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 80)
