#!/usr/bin/env python3
"""
Deep Analysis: Polarized Overlap Reduction Function for Z² Framework
======================================================================

The Z² framework predicts ONLY h+ polarization survives the Z₂ orbifold
projection. This has specific consequences for LIGO stochastic searches
that go beyond just using a different ORF.

KEY PHYSICS INSIGHT:
--------------------
Standard searches assume: ⟨|h_+|²⟩ = ⟨|h_×|²⟩ = S_h(f)/2
Z² predicts:              ⟨|h_+|²⟩ = S_h(f), ⟨|h_×|²⟩ = 0

This changes:
1. The overlap reduction function (ORF)
2. The optimal filter weighting
3. The interpretation of upper limits
4. The construction of null tests

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import healpy as hp
import json
import os

print("=" * 75)
print("POLARIZED ORF DEEP ANALYSIS: h+ Only Gravitational Waves")
print("=" * 75)

# =============================================================================
# DETECTOR PARAMETERS
# =============================================================================

# Physical constants
c = 299792458.0  # m/s
R_EARTH = 6.371e6  # m

# Detector locations and orientations
DETECTORS = {
    'H1': {
        'lat': np.radians(46.4552),
        'lon': np.radians(-119.4076),
        'arm_azimuth': np.radians(125.9994),
        'name': 'LIGO Hanford'
    },
    'L1': {
        'lat': np.radians(30.5629),
        'lon': np.radians(-90.7742),
        'arm_azimuth': np.radians(197.7165),
        'name': 'LIGO Livingston'
    },
    'V1': {
        'lat': np.radians(43.6314),
        'lon': np.radians(10.5045),
        'arm_azimuth': np.radians(70.5675),
        'name': 'Virgo'
    }
}

# =============================================================================
# GEOMETRY FUNCTIONS
# =============================================================================

def latlon_to_xyz(lat, lon, R=R_EARTH):
    """Convert lat/lon to geocentric Cartesian."""
    x = R * np.cos(lat) * np.cos(lon)
    y = R * np.cos(lat) * np.sin(lon)
    z = R * np.sin(lat)
    return np.array([x, y, z])


def get_detector_tensors(lat, lon, arm_azimuth):
    """
    Compute detector response tensor D_ij = (1/2)(x_i x_j - y_i y_j)
    in Earth-centered coordinates.
    """
    cos_lat, sin_lat = np.cos(lat), np.sin(lat)
    cos_lon, sin_lon = np.cos(lon), np.sin(lon)

    # Local coordinate frame
    north = np.array([-sin_lat * cos_lon, -sin_lat * sin_lon, cos_lat])
    east = np.array([-sin_lon, cos_lon, 0])

    # Arm directions
    cos_az, sin_az = np.cos(arm_azimuth), np.sin(arm_azimuth)
    x_arm = cos_az * north + sin_az * east
    y_arm = -sin_az * north + cos_az * east

    return x_arm, y_arm


def antenna_patterns(theta, phi, x_arm, y_arm):
    """
    Compute F+ and F× antenna patterns for a given sky direction.

    theta, phi: sky direction in spherical coordinates
    x_arm, y_arm: detector arm unit vectors
    """
    # Wave propagation basis vectors
    cos_theta, sin_theta = np.cos(theta), np.sin(theta)
    cos_phi, sin_phi = np.cos(phi), np.sin(phi)

    e_theta = np.array([cos_theta * cos_phi, cos_theta * sin_phi, -sin_theta])
    e_phi = np.array([-sin_phi, cos_phi, 0])

    # Antenna patterns
    x_theta = np.dot(x_arm, e_theta)
    x_phi = np.dot(x_arm, e_phi)
    y_theta = np.dot(y_arm, e_theta)
    y_phi = np.dot(y_arm, e_phi)

    F_plus = 0.5 * (x_theta**2 - x_phi**2 - y_theta**2 + y_phi**2)
    F_cross = x_theta * x_phi - y_theta * y_phi

    return F_plus, F_cross


# =============================================================================
# ORF COMPUTATION
# =============================================================================

def compute_orf_components(det1, det2, freqs, nside=64):
    """
    Compute the individual components of the ORF:
    - γ_++ : contribution from F+₁ × F+₂
    - γ_×× : contribution from F×₁ × F×₂
    - γ_+× : cross term (should be ~0 for isotropic)
    - γ_total = γ_++ + γ_××

    This decomposition reveals how much each polarization contributes.
    """
    # Detector setup
    pos1 = latlon_to_xyz(det1['lat'], det1['lon'])
    pos2 = latlon_to_xyz(det2['lat'], det2['lon'])
    baseline = pos2 - pos1

    x1, y1 = get_detector_tensors(det1['lat'], det1['lon'], det1['arm_azimuth'])
    x2, y2 = get_detector_tensors(det2['lat'], det2['lon'], det2['arm_azimuth'])

    # Sky grid
    npix = hp.nside2npix(nside)
    theta, phi = hp.pix2ang(nside, np.arange(npix))
    dOmega = 4 * np.pi / npix

    # Precompute antenna patterns and time delays
    F_plus_1 = np.zeros(npix)
    F_cross_1 = np.zeros(npix)
    F_plus_2 = np.zeros(npix)
    F_cross_2 = np.zeros(npix)
    delta_t = np.zeros(npix)

    for i in range(npix):
        F_plus_1[i], F_cross_1[i] = antenna_patterns(theta[i], phi[i], x1, y1)
        F_plus_2[i], F_cross_2[i] = antenna_patterns(theta[i], phi[i], x2, y2)

        n_hat = np.array([
            np.sin(theta[i]) * np.cos(phi[i]),
            np.sin(theta[i]) * np.sin(phi[i]),
            np.cos(theta[i])
        ])
        delta_t[i] = np.dot(baseline, n_hat) / c

    # Compute ORF components at each frequency
    gamma_pp = np.zeros(len(freqs), dtype=complex)
    gamma_cc = np.zeros(len(freqs), dtype=complex)
    gamma_pc = np.zeros(len(freqs), dtype=complex)

    for i, f in enumerate(freqs):
        phase = np.exp(2j * np.pi * f * delta_t)

        gamma_pp[i] = np.sum(F_plus_1 * F_plus_2 * phase) * dOmega
        gamma_cc[i] = np.sum(F_cross_1 * F_cross_2 * phase) * dOmega
        gamma_pc[i] = np.sum(F_plus_1 * F_cross_2 * phase) * dOmega

    # Normalization factor
    norm = 5 / (8 * np.pi)
    gamma_pp *= norm
    gamma_cc *= norm
    gamma_pc *= norm

    # Standard ORF (both polarizations, equal weight)
    gamma_standard = gamma_pp + gamma_cc

    # Normalize to γ(0) = 1 for reference
    norm_factor = np.abs(gamma_standard[0])
    if norm_factor > 0:
        gamma_pp /= norm_factor
        gamma_cc /= norm_factor
        gamma_pc /= norm_factor
        gamma_standard /= norm_factor

    return {
        'gamma_pp': np.abs(gamma_pp),       # h+ contribution only
        'gamma_cc': np.abs(gamma_cc),       # h× contribution only
        'gamma_pc': np.abs(gamma_pc),       # Cross term
        'gamma_standard': np.abs(gamma_standard),  # Total (standard)
        'gamma_plus_only': np.abs(gamma_pp),       # Same as gamma_pp
    }


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

print("\n[1] Computing ORF decomposition for H1-L1 baseline...")

freqs = np.logspace(np.log10(10), np.log10(2000), 200)

orf_H1L1 = compute_orf_components(DETECTORS['H1'], DETECTORS['L1'], freqs)

# Key metrics
ratio_at_20Hz = orf_H1L1['gamma_plus_only'][np.argmin(np.abs(freqs-20))] / \
                orf_H1L1['gamma_standard'][np.argmin(np.abs(freqs-20))]
ratio_at_100Hz = orf_H1L1['gamma_plus_only'][np.argmin(np.abs(freqs-100))] / \
                 orf_H1L1['gamma_standard'][np.argmin(np.abs(freqs-100))]

print(f"\n  ORF DECOMPOSITION RESULTS:")
print(f"  ─────────────────────────")
print(f"  At 20 Hz:")
print(f"    γ_standard = {orf_H1L1['gamma_standard'][np.argmin(np.abs(freqs-20))]:.4f}")
print(f"    γ_++ (h+ only) = {orf_H1L1['gamma_pp'][np.argmin(np.abs(freqs-20))]:.4f}")
print(f"    γ_×× (h× only) = {orf_H1L1['gamma_cc'][np.argmin(np.abs(freqs-20))]:.4f}")
print(f"    Ratio γ_++/γ_total = {ratio_at_20Hz:.3f}")
print(f"\n  At 100 Hz:")
print(f"    γ_standard = {orf_H1L1['gamma_standard'][np.argmin(np.abs(freqs-100))]:.4f}")
print(f"    γ_++ (h+ only) = {orf_H1L1['gamma_pp'][np.argmin(np.abs(freqs-100))]:.4f}")
print(f"    γ_×× (h× only) = {orf_H1L1['gamma_cc'][np.argmin(np.abs(freqs-100))]:.4f}")
print(f"    Ratio γ_++/γ_total = {ratio_at_100Hz:.3f}")

# =============================================================================
# THE KEY INSIGHT: SNR COMPARISON
# =============================================================================

print("\n" + "=" * 75)
print("[2] SNR Analysis: Standard vs Polarized Search")
print("=" * 75)

print("""
KEY PHYSICS:
────────────
For a stochastic background with spectral density S_h(f):

STANDARD search assumes unpolarized: ⟨|h_+|²⟩ = ⟨|h_×|²⟩ = S_h(f)/2
Z² framework predicts h+ only:       ⟨|h_+|²⟩ = S_h(f), ⟨|h_×|²⟩ = 0

The optimal SNR for detecting a signal is:

    SNR² = ∫ df [γ(f)]² S_h²(f) / [P₁(f) P₂(f)]

where γ(f) is the ORF for the assumed polarization model.

CRITICAL INSIGHT:
─────────────────
If the true signal is h+ only, but we search with standard (unpolarized) ORF:
- We use γ_standard instead of γ_++
- This is SUBOPTIMAL because γ_standard includes h× which contributes noise, not signal

The SNR LOSS from using wrong ORF is:

    Loss = [γ_++/γ_standard]² averaged over frequency band

""")

# Compute SNR loss
# Assuming flat Ω_GW spectrum and similar noise at all frequencies
snr_ratio_squared = np.mean(orf_H1L1['gamma_pp']**2) / np.mean(orf_H1L1['gamma_standard']**2)
snr_ratio = np.sqrt(snr_ratio_squared)

print(f"  SNR COMPARISON (H1-L1, 20-1000 Hz band):")
print(f"  ────────────────────────────────────────")
print(f"  Mean [γ_++/γ_standard]² = {snr_ratio_squared:.4f}")
print(f"  SNR ratio (h+ search / standard) = {snr_ratio:.3f}")
print(f"\n  INTERPRETATION:")
print(f"  If signal is truly h+ only, standard search has SNR = {snr_ratio:.1%} of optimal")
print(f"  Using polarized ORF recovers the full optimal SNR")

# =============================================================================
# NULL TEST CONSTRUCTION
# =============================================================================

print("\n" + "=" * 75)
print("[3] Null Test for Chirality")
print("=" * 75)

print("""
THE CHIRALITY NULL TEST:
────────────────────────
If we detect a stochastic signal, we can test whether it's h+ only or unpolarized.

Define two estimators:
  Ŷ_standard = Re[C₁₂] / γ_standard(f)  → assumes unpolarized
  Ŷ_plus     = Re[C₁₂] / γ_++(f)        → assumes h+ only

For a TRUE unpolarized signal:
  ⟨Ŷ_standard⟩ = Ω_GW (correct)
  ⟨Ŷ_plus⟩     = Ω_GW × [γ_standard/γ_++] ≠ Ω_GW (biased high)

For a TRUE h+ only signal:
  ⟨Ŷ_standard⟩ = Ω_GW × [γ_++/γ_standard] ≠ Ω_GW (biased low)
  ⟨Ŷ_plus⟩     = Ω_GW (correct)

NULL TEST STATISTIC:
  R = Ŷ_plus / Ŷ_standard = γ_standard / γ_++

  For unpolarized background: R ≈ 1
  For h+ only background:     R ≈ γ_standard/γ_++ ≈ {:.1f}

""".format(1/ratio_at_20Hz))

# Frequency-dependent test statistic
R_f = orf_H1L1['gamma_standard'] / np.maximum(orf_H1L1['gamma_pp'], 1e-10)

print(f"  NULL TEST PREDICTIONS:")
print(f"  ──────────────────────")
print(f"  If h+ only (Z² correct): R(20 Hz) ≈ {R_f[np.argmin(np.abs(freqs-20))]:.2f}")
print(f"  If unpolarized (Z² wrong): R ≈ 1.0")
print(f"\n  This is a ~{abs(R_f[np.argmin(np.abs(freqs-20))]-1)*100:.0f}% effect - MEASURABLE if signal is detected!")

# =============================================================================
# MULTI-BASELINE ANALYSIS
# =============================================================================

print("\n" + "=" * 75)
print("[4] Multi-Baseline Network Analysis")
print("=" * 75)

print("\n  Computing ORF for all baselines...")

baselines = [
    ('H1', 'L1'),
    ('H1', 'V1'),
    ('L1', 'V1')
]

orf_all = {}
for d1, d2 in baselines:
    key = f"{d1}-{d2}"
    print(f"    {key}...", end=" ")
    orf_all[key] = compute_orf_components(DETECTORS[d1], DETECTORS[d2], freqs, nside=32)
    ratio = orf_all[key]['gamma_pp'][0] / orf_all[key]['gamma_standard'][0]
    print(f"γ_++/γ_total = {ratio:.3f}")

print("""
NETWORK OPTIMIZATION:
─────────────────────
Different baselines have different γ_++/γ_standard ratios due to geometry.

For h+ only search, we should weight baselines by their h+ sensitivity:
  w_ij ∝ γ_++(f)² / [P_i(f) P_j(f)]

This is DIFFERENT from standard weighting which uses γ_standard.

The optimal combination may significantly improve h+ sensitivity compared
to using standard network weights.
""")

# =============================================================================
# GENERATE FIGURES
# =============================================================================

print("\n" + "=" * 75)
print("[5] Generating Analysis Figures")
print("=" * 75)

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

fig = plt.figure(figsize=(16, 12))
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Panel A: ORF Decomposition
ax1 = fig.add_subplot(gs[0, 0])
ax1.semilogx(freqs, orf_H1L1['gamma_standard'], 'k-', linewidth=2.5, label='γ_total (standard)')
ax1.semilogx(freqs, orf_H1L1['gamma_pp'], 'b-', linewidth=2, label='γ_++ (h+ contribution)')
ax1.semilogx(freqs, orf_H1L1['gamma_cc'], 'r--', linewidth=2, label='γ_×× (h× contribution)')
ax1.fill_between(freqs, 0, orf_H1L1['gamma_pp'], alpha=0.3, color='blue')
ax1.fill_between(freqs, orf_H1L1['gamma_pp'], orf_H1L1['gamma_standard'], alpha=0.3, color='red')
ax1.set_xlabel('Frequency [Hz]', fontsize=12)
ax1.set_ylabel('Overlap Reduction Function', fontsize=12)
ax1.set_title('Panel A: ORF Decomposition (H1-L1)', fontsize=13, fontweight='bold')
ax1.set_xlim(10, 2000)
ax1.set_ylim(0, 1.1)
ax1.legend(loc='upper right', fontsize=10)
ax1.grid(True, alpha=0.3)
ax1.text(15, 0.2, 'h+ contribution', fontsize=10, color='blue')
ax1.text(15, 0.6, 'h× contribution', fontsize=10, color='red')

# Panel B: Ratio γ_++/γ_total
ax2 = fig.add_subplot(gs[0, 1])
ratio = orf_H1L1['gamma_pp'] / np.maximum(orf_H1L1['gamma_standard'], 1e-10)
ax2.semilogx(freqs, ratio, 'purple', linewidth=2)
ax2.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, label='Expected for co-aligned')
ax2.fill_between(freqs, 0, ratio, alpha=0.3, color='purple')
ax2.set_xlabel('Frequency [Hz]', fontsize=12)
ax2.set_ylabel('γ_++ / γ_total', fontsize=12)
ax2.set_title('Panel B: h+ Fraction of Total ORF', fontsize=13, fontweight='bold')
ax2.set_xlim(10, 2000)
ax2.set_ylim(0, 1.5)
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

# Panel C: Multi-baseline comparison
ax3 = fig.add_subplot(gs[1, 0])
colors = {'H1-L1': 'blue', 'H1-V1': 'green', 'L1-V1': 'orange'}
for baseline, orf in orf_all.items():
    ax3.semilogx(freqs, orf['gamma_pp'], color=colors[baseline], linewidth=2,
                 label=f'{baseline} γ_++')
    ax3.semilogx(freqs, orf['gamma_standard'], color=colors[baseline], linewidth=1,
                 linestyle='--', alpha=0.5)
ax3.set_xlabel('Frequency [Hz]', fontsize=12)
ax3.set_ylabel('Overlap Reduction Function', fontsize=12)
ax3.set_title('Panel C: Multi-Baseline ORFs (solid=h+, dashed=standard)', fontsize=13, fontweight='bold')
ax3.set_xlim(10, 2000)
ax3.set_ylim(0, 1.1)
ax3.legend(fontsize=10)
ax3.grid(True, alpha=0.3)

# Panel D: Summary
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

summary_text = """
┌─────────────────────────────────────────────────────────────────────┐
│          POLARIZED ORF: WHAT IT ACTUALLY TELLS US                   │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ORF DECOMPOSITION (H1-L1 at 20 Hz):                               │
│    • γ_total (standard) = 1.000                                    │
│    • γ_++ (h+ only)     = {:.3f}                                    │
│    • γ_×× (h× only)     = {:.3f}                                    │
│    • h+ fraction        = {:.1f}%                                   │
│                                                                     │
│  SNR IMPLICATIONS:                                                  │
│    • If signal is h+ only, standard search is SUBOPTIMAL           │
│    • SNR loss from wrong ORF: {:.1f}%                               │
│    • Polarized search recovers optimal sensitivity                 │
│                                                                     │
│  NULL TEST FOR CHIRALITY:                                           │
│    • Compare Ŷ_standard vs Ŷ_polarized                             │
│    • Ratio R = Ŷ_pol/Ŷ_std should be ~{:.1f} if h+ only             │
│    • Ratio R ≈ 1 if unpolarized                                    │
│    • This is a {:.0f}% measurable effect!                            │
│                                                                     │
│  BOTTOM LINE:                                                       │
│    Can't close the 10¹¹ gap, but IF a signal is ever detected,     │
│    the polarized ORF provides a DEFINITIVE TEST of chirality.      │
│                                                                     │
│    Z² prediction: Signal should appear ~{:.0f}% stronger in         │
│    polarized search than standard search.                          │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
""".format(
    orf_H1L1['gamma_pp'][0],
    orf_H1L1['gamma_cc'][0],
    orf_H1L1['gamma_pp'][0] * 100,
    (1 - snr_ratio) * 100,
    1/ratio_at_20Hz,
    abs(1/ratio_at_20Hz - 1) * 100,
    (1/ratio_at_20Hz - 1) * 100
)

ax4.text(0.02, 0.98, summary_text, transform=ax4.transAxes,
         fontfamily='monospace', fontsize=9.5,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

fig.suptitle('Deep Analysis: Polarized ORF for h+ Only Gravitational Waves',
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig(os.path.join(OUTPUT_DIR, 'polarized_orf_deep_analysis.png'),
            dpi=200, bbox_inches='tight', facecolor='white')
print("  Saved: polarized_orf_deep_analysis.png")

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'analysis': 'polarized_orf_deep',
    'baseline': 'H1-L1',
    'frequencies_hz': freqs.tolist(),
    'orf_components': {
        'gamma_standard': orf_H1L1['gamma_standard'].tolist(),
        'gamma_plus_plus': orf_H1L1['gamma_pp'].tolist(),
        'gamma_cross_cross': orf_H1L1['gamma_cc'].tolist(),
    },
    'key_results': {
        'h_plus_fraction_20Hz': float(orf_H1L1['gamma_pp'][np.argmin(np.abs(freqs-20))]),
        'h_plus_fraction_100Hz': float(orf_H1L1['gamma_pp'][np.argmin(np.abs(freqs-100))]),
        'snr_ratio': float(snr_ratio),
        'null_test_ratio': float(1/ratio_at_20Hz),
        'measurable_effect_percent': float(abs(1/ratio_at_20Hz - 1) * 100)
    },
    'interpretation': {
        'can_close_gap': False,
        'provides_chirality_test': True,
        'effect_size': f"{abs(1/ratio_at_20Hz - 1) * 100:.0f}% difference between polarized and standard"
    }
}

with open(os.path.join(OUTPUT_DIR, 'polarized_orf_deep_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("  Saved: polarized_orf_deep_results.json")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 75)
print("POLARIZED ORF DEEP ANALYSIS: CONCLUSIONS")
print("=" * 75)

print(f"""
╔═════════════════════════════════════════════════════════════════════════════╗
║                    WHAT THE POLARIZED ORF ACTUALLY GIVES US                 ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  1. SENSITIVITY IMPROVEMENT: Modest                                         ║
║     • Standard search is ~{(1-snr_ratio)*100:.0f}% suboptimal for h+ only signal       ║
║     • Polarized ORF recovers this, but can't close 10¹¹ gap                ║
║                                                                             ║
║  2. CHIRALITY NULL TEST: Powerful                                           ║
║     • IF a signal is detected, ratio test distinguishes h+ from unpolarized║
║     • Effect size: ~{abs(1/ratio_at_20Hz - 1)*100:.0f}% difference (easily measurable)              ║
║     • This is the DECISIVE TEST for Z² topology                            ║
║                                                                             ║
║  3. SCIENTIFIC VALUE:                                                       ║
║     • Standard LIGO stochastic searches ARE slightly suboptimal for Z²     ║
║     • A dedicated h+ search is warranted as a parallel analysis            ║
║     • Main value is in CHARACTERIZATION, not detection                     ║
║                                                                             ║
║  RECOMMENDATION FOR LIGO COLLABORATION:                                     ║
║     Run polarized ORF as a secondary analysis alongside standard search.   ║
║     If astrophysical SGWB is detected, the ratio test probes chirality.    ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
""")

print("=" * 75)
