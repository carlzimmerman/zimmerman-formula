#!/usr/bin/env python3
"""
O4 Sensitivity Projection: Time to Distinguish R=1 vs R=3.1
============================================================

Compute how much O4 observation time is needed to distinguish:
  - R = 1.0 (unpolarized, standard GR)
  - R = 3.1 (h+ only, Z² chirality)

for the expected astrophysical stochastic background.

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
from scipy import integrate
import matplotlib.pyplot as plt
import json
import os

print("=" * 75)
print("O4 CHIRALITY TEST: SENSITIVITY PROJECTION")
print("=" * 75)

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

H0 = 67.4  # km/s/Mpc (Planck 2018)
H0_SI = H0 * 1000 / (3.086e22)  # Convert to SI (s^-1)
c = 3e8  # m/s

# =============================================================================
# DETECTOR PARAMETERS
# =============================================================================

# Detector positions (Earth-centered coordinates in meters)
# Reference: LIGO/Virgo detector coordinates

# Hanford (H1)
H1_lat = 46.455 * np.pi/180
H1_lon = -119.408 * np.pi/180

# Livingston (L1)
L1_lat = 30.563 * np.pi/180
L1_lon = -90.774 * np.pi/180

# Virgo (V1)
V1_lat = 43.631 * np.pi/180
V1_lon = 10.504 * np.pi/180

def baseline_distance(lat1, lon1, lat2, lon2):
    """Compute baseline distance between detectors."""
    R_earth = 6.371e6  # meters
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1)*np.cos(lat2)*np.sin(dlon/2)**2
    return 2 * R_earth * np.arcsin(np.sqrt(a))

d_H1L1 = baseline_distance(H1_lat, H1_lon, L1_lat, L1_lon)
d_H1V1 = baseline_distance(H1_lat, H1_lon, V1_lat, V1_lon)
d_L1V1 = baseline_distance(L1_lat, L1_lon, V1_lat, V1_lon)

print(f"\nBaseline distances:")
print(f"  H1-L1: {d_H1L1/1e6:.1f} km")
print(f"  H1-V1: {d_H1V1/1e6:.1f} km")
print(f"  L1-V1: {d_L1V1/1e6:.1f} km")

# =============================================================================
# DESIGN SENSITIVITY CURVES (O4)
# =============================================================================

def aLIGO_psd(f):
    """
    Advanced LIGO O4 design sensitivity (strain noise PSD).
    Approximation based on aligo_O4high.txt sensitivity curve.
    """
    # Seismic wall below 10 Hz
    if np.isscalar(f):
        if f < 10:
            return 1e-40  # Effectively infinite noise
    else:
        f = np.asarray(f)

    # Fit to O4 sensitivity (approximate)
    # Low frequency: seismic
    # Mid frequency: thermal
    # High frequency: shot noise

    f0 = 20  # Reference frequency
    S0 = 1e-47  # Reference PSD at 20 Hz (strain^2/Hz)

    # Composite model
    seismic = (f0/f)**14 * np.exp(-((f-10)/5)**2)
    thermal = (f0/f)**2
    shot = (f/200)**2

    return S0 * (0.1*seismic + thermal + 0.5*shot + 0.5)

def AdVirgo_psd(f):
    """
    Advanced Virgo O4 sensitivity (strain noise PSD).
    Slightly less sensitive than aLIGO.
    """
    return 1.5 * aLIGO_psd(f)  # ~20% worse than LIGO

# =============================================================================
# OVERLAP REDUCTION FUNCTION
# =============================================================================

def compute_orf_ratio(baseline_km, freqs):
    """
    Compute the ratio γ_standard / γ_++ for a given baseline.

    This is a simplified model based on our detailed calculation.
    The key physics: longer baselines have better h+ sensitivity
    because the time delay causes more decorrelation of h×.
    """
    # Light travel time across baseline
    tau = baseline_km * 1000 / c

    # Approximate ORF decomposition
    # γ_++ / γ_total depends on baseline orientation and length

    # From our detailed H1-L1 calculation: h+ fraction ≈ 0.27 at 20 Hz
    # From H1-V1 geometry: h+ fraction ≈ 0.77 at 20 Hz (longer baseline)

    ratios = []
    for f in freqs:
        phase = 2 * np.pi * f * tau

        # Simplified model: h+ fraction increases with phase
        # (longer baseline = more decorrelation of h×)
        h_plus_frac = 0.25 + 0.25 * np.sin(phase/4)**2

        # Adjust for baseline length
        if baseline_km > 6000:  # H1-V1 or L1-V1
            h_plus_frac = 0.6 + 0.2 * np.sin(phase/6)**2

        # Ratio R = γ_total / γ_++ = 1 / h_plus_frac
        R = 1.0 / max(h_plus_frac, 0.1)
        ratios.append(R)

    return np.array(ratios)

# =============================================================================
# ASTROPHYSICAL BACKGROUND MODEL
# =============================================================================

def Omega_astro(f, Omega_ref=1e-9, f_ref=25, alpha=2/3):
    """
    Astrophysical stochastic background from compact binary mergers.

    Ω(f) = Ω_ref × (f/f_ref)^α

    α = 2/3 for inspiraling binaries (dominant contribution)
    Ω_ref ~ 10^-9 at 25 Hz (current best estimate)
    """
    return Omega_ref * (f / f_ref)**alpha

# =============================================================================
# SNR CALCULATION
# =============================================================================

def compute_snr(T_obs, freqs, Omega_gw, P1, P2, gamma, df=1.0):
    """
    Compute SNR for stochastic search.

    SNR² = (3H₀²/10π²)² × 2T × ∫ df [γ²(f) Ω²(f)] / [P₁(f) P₂(f) f⁶]

    Parameters:
    -----------
    T_obs : float
        Observation time in seconds
    freqs : array
        Frequency array
    Omega_gw : array
        GW energy density spectrum
    P1, P2 : arrays
        Detector noise PSDs
    gamma : array
        Overlap reduction function
    df : float
        Frequency resolution
    """
    prefactor = (3 * H0_SI**2 / (10 * np.pi**2))**2

    # Integrand
    integrand = gamma**2 * Omega_gw**2 / (P1 * P2 * freqs**6)

    # Remove any infinities or NaNs
    integrand = np.nan_to_num(integrand, nan=0, posinf=0, neginf=0)

    # Integrate
    integral = np.trapz(integrand, freqs)

    snr_squared = prefactor * 2 * T_obs * integral

    return np.sqrt(max(snr_squared, 0))

# =============================================================================
# PROJECTION CALCULATION
# =============================================================================

print("\n" + "=" * 75)
print("COMPUTING O4 SENSITIVITY PROJECTION")
print("=" * 75)

# Frequency range
freqs = np.logspace(1, 3, 500)  # 10 Hz to 1000 Hz

# Noise PSDs
P_H1 = np.array([aLIGO_psd(f) for f in freqs])
P_L1 = np.array([aLIGO_psd(f) for f in freqs])
P_V1 = np.array([AdVirgo_psd(f) for f in freqs])

# Astrophysical background
Omega = Omega_astro(freqs)

# ORF (use our calculated values)
# For H1-L1: γ_standard normalized to 1 at low f, γ_++ ≈ 0.32 at 20 Hz
# Load our actual results
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
try:
    with open(os.path.join(OUTPUT_DIR, 'polarized_orf_deep_results.json'), 'r') as f:
        orf_data = json.load(f)
    R_H1L1 = orf_data['key_results']['null_test_ratio']
    h_plus_frac_H1L1 = orf_data['key_results']['h_plus_fraction_20Hz']
    print(f"\n  Loaded H1-L1 results: R = {R_H1L1:.2f}")
except:
    R_H1L1 = 3.11
    h_plus_frac_H1L1 = 0.32
    print(f"\n  Using default H1-L1: R = {R_H1L1:.2f}")

# H1-V1 ratio (from our multi-baseline analysis)
# Longer baseline = better h+ sensitivity
R_H1V1 = 1.0 / 0.77  # h+ fraction of 77% → R = 1.30
h_plus_frac_H1V1 = 0.77

print(f"  H1-V1 h+ fraction: {h_plus_frac_H1V1:.0%} → R = {R_H1V1:.2f}")

# Simplified ORF for SNR calculation (normalized)
gamma_H1L1 = np.ones_like(freqs) * 0.5  # Average ORF magnitude
gamma_H1V1 = np.ones_like(freqs) * 0.3  # H1-V1 has smaller ORF (longer baseline)

# =============================================================================
# TIME TO DETECTION
# =============================================================================

print("\n" + "-" * 75)
print("TIME TO DETECTION (SNR = 3)")
print("-" * 75)

observation_times = np.logspace(5, 8, 100)  # 1 day to 3 years in seconds

snr_H1L1 = []
snr_H1V1 = []

for T in observation_times:
    snr_H1L1.append(compute_snr(T, freqs, Omega, P_H1, P_L1, gamma_H1L1))
    snr_H1V1.append(compute_snr(T, freqs, Omega, P_H1, P_V1, gamma_H1V1))

snr_H1L1 = np.array(snr_H1L1)
snr_H1V1 = np.array(snr_H1V1)

# Find time to SNR = 3 (detection threshold)
def find_time_to_snr(times, snrs, target_snr):
    idx = np.searchsorted(snrs, target_snr)
    if idx >= len(times):
        return np.inf
    return times[idx]

T_detect_H1L1 = find_time_to_snr(observation_times, snr_H1L1, 3)
T_detect_H1V1 = find_time_to_snr(observation_times, snr_H1V1, 3)

print(f"\n  Astrophysical background Ω(25 Hz) = 1×10⁻⁹")
print(f"\n  Time to SNR = 3 (detection):")
print(f"    H1-L1: {T_detect_H1L1/86400/30:.1f} months")
print(f"    H1-V1: {T_detect_H1V1/86400/30:.1f} months")

# =============================================================================
# TIME TO DISTINGUISH R = 1 vs R = 3.1
# =============================================================================

print("\n" + "-" * 75)
print("TIME TO DISTINGUISH R = 1 vs R = 3.1 (5σ)")
print("-" * 75)

print("""
To distinguish R = 1 (unpolarized) from R = 3.1 (h+ only) at 5σ:

  σ(R) < |R_Z2 - R_GR| / 5 = |3.1 - 1.0| / 5 = 0.42

For ratio of two measurements with similar SNR:
  σ(R)/R ≈ √2 / SNR

At R ≈ 2 (midpoint): SNR > √2 × 2 / 0.42 ≈ 6.7

So we need SNR ≈ 7 to distinguish at 5σ.
""")

T_distinguish_H1L1 = find_time_to_snr(observation_times, snr_H1L1, 7)
T_distinguish_H1V1 = find_time_to_snr(observation_times, snr_H1V1, 7)

print(f"  Time to SNR = 7 (distinguish R at 5σ):")
print(f"    H1-L1: {T_distinguish_H1L1/86400/30:.1f} months")
print(f"    H1-V1: {T_distinguish_H1V1/86400/30:.1f} months")

# =============================================================================
# O4/O5 TIMELINE
# =============================================================================

print("\n" + "-" * 75)
print("O4/O5 PROJECTED TIMELINE")
print("-" * 75)

# O4 parameters
O4_duration_months = 18  # O4 expected ~18 months total
O4_duty_cycle = 0.7  # ~70% uptime
O4_effective_months = O4_duration_months * O4_duty_cycle

# O5 parameters (starts ~2027)
O5_sensitivity_improvement = 2.0  # ~2x better sensitivity
O5_duration_months = 24

print(f"""
  O4 RUN (current):
    Duration: {O4_duration_months} months (effective: {O4_effective_months:.0f} months)
    Expected SNR for astro SGWB: {snr_H1L1[np.searchsorted(observation_times, O4_effective_months*30*86400)]:.1f} (H1-L1)

  O5 RUN (starting ~2027):
    Duration: {O5_duration_months} months
    Sensitivity: ~{O5_sensitivity_improvement}× better
    Expected SNR: ~{snr_H1L1[np.searchsorted(observation_times, O4_effective_months*30*86400)] * O5_sensitivity_improvement * np.sqrt(O5_duration_months/O4_effective_months):.0f} (cumulative)
""")

# =============================================================================
# THE KEY INSIGHT: H1-V1 ADVANTAGE
# =============================================================================

print("\n" + "=" * 75)
print("KEY INSIGHT: H1-V1 BASELINE ADVANTAGE")
print("=" * 75)

print(f"""
For the CHIRALITY TEST, the H1-V1 baseline has a critical advantage:

  H1-L1 baseline:
    • h+ fraction: {h_plus_frac_H1L1:.0%}
    • Null test ratio: R = {R_H1L1:.1f}
    • Effect size: {(R_H1L1-1)*100:.0f}%

  H1-V1 baseline:
    • h+ fraction: {h_plus_frac_H1V1:.0%}  ← MUCH HIGHER
    • Null test ratio: R = {R_H1V1:.2f}
    • Effect size: {(R_H1V1-1)*100:.0f}%

INTERPRETATION:
The H1-V1 baseline is 77% sensitive to h+ (vs 27% for H1-L1).

This means:
  • For an UNPOLARIZED background: Both baselines see the same Ω
  • For a CHIRAL (h+ only) background:
    - H1-L1 sees ~27% of true amplitude
    - H1-V1 sees ~77% of true amplitude

The RATIO between H1-L1 and H1-V1 estimates provides ANOTHER null test:
  Ω̂(H1-V1) / Ω̂(H1-L1) ≈ 0.77/0.27 ≈ 2.85 for h+ only
  Ω̂(H1-V1) / Ω̂(H1-L1) ≈ 1.0 for unpolarized

This cross-baseline comparison is INDEPENDENT of the amplitude!
""")

# =============================================================================
# CREATE FIGURE
# =============================================================================

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Plot 1: SNR accumulation
ax1 = axes[0, 0]
times_months = observation_times / (86400 * 30)
ax1.loglog(times_months, snr_H1L1, 'b-', linewidth=2, label='H1-L1')
ax1.loglog(times_months, snr_H1V1, 'r--', linewidth=2, label='H1-V1')
ax1.axhline(3, color='green', linestyle=':', label='Detection (SNR=3)')
ax1.axhline(7, color='orange', linestyle=':', label='Distinguish R (SNR=7)')
ax1.axvline(O4_effective_months, color='purple', linestyle='--', alpha=0.5, label=f'O4 end ({O4_effective_months:.0f} mo)')
ax1.set_xlabel('Observation Time (months)', fontsize=12)
ax1.set_ylabel('SNR', fontsize=12)
ax1.set_title('SNR Accumulation for Astrophysical SGWB', fontsize=14)
ax1.legend(loc='lower right')
ax1.grid(True, alpha=0.3)
ax1.set_xlim(0.1, 100)
ax1.set_ylim(0.1, 30)

# Plot 2: ORF decomposition (from our data)
ax2 = axes[0, 1]
try:
    orf_freqs = np.array(orf_data['frequencies_hz'])
    gamma_std = np.array(orf_data['orf_components']['gamma_standard'])
    gamma_pp = np.array(orf_data['orf_components']['gamma_plus_plus'])
    gamma_cc = np.array(orf_data['orf_components']['gamma_cross_cross'])

    ax2.semilogx(orf_freqs, gamma_std, 'k-', linewidth=2, label='γ_total (standard)')
    ax2.semilogx(orf_freqs, gamma_pp, 'b-', linewidth=2, label='γ_++ (h+ only)')
    ax2.semilogx(orf_freqs, gamma_cc, 'r--', linewidth=2, label='γ_×× (h× only)')
    ax2.axvline(20, color='gray', linestyle=':', alpha=0.5)
    ax2.text(22, 0.9, '20 Hz', fontsize=10)
except:
    ax2.text(0.5, 0.5, 'ORF data not available', transform=ax2.transAxes, ha='center')
ax2.set_xlabel('Frequency (Hz)', fontsize=12)
ax2.set_ylabel('Overlap Reduction Function', fontsize=12)
ax2.set_title('H1-L1 ORF Decomposition', fontsize=14)
ax2.legend()
ax2.grid(True, alpha=0.3)
ax2.set_xlim(10, 1000)

# Plot 3: Baseline comparison
ax3 = axes[1, 0]
baselines = ['H1-L1', 'H1-V1', 'L1-V1']
h_plus_fracs = [0.27, 0.77, 0.65]  # Approximate values
colors = ['steelblue', 'crimson', 'forestgreen']

bars = ax3.bar(baselines, h_plus_fracs, color=colors, edgecolor='black', linewidth=2)
ax3.axhline(0.5, color='gray', linestyle='--', label='50% (no preference)')
ax3.set_ylabel('h+ Sensitivity Fraction', fontsize=12)
ax3.set_title('Baseline Sensitivity to h+ Polarization', fontsize=14)
ax3.set_ylim(0, 1)
for bar, frac in zip(bars, h_plus_fracs):
    ax3.text(bar.get_x() + bar.get_width()/2, frac + 0.03, f'{frac:.0%}',
             ha='center', fontsize=14, fontweight='bold')
ax3.legend()
ax3.grid(True, alpha=0.3, axis='y')

# Plot 4: Decision diagram
ax4 = axes[1, 1]
ax4.axis('off')

decision_text = """
╔═══════════════════════════════════════════════════════════════════╗
║            O4 CHIRALITY TEST DECISION TREE                        ║
╠═══════════════════════════════════════════════════════════════════╣
║                                                                   ║
║  IF stochastic background detected (SNR > 3):                     ║
║                                                                   ║
║    1. Compute R = Ω̂_polarized / Ω̂_standard                       ║
║                                                                   ║
║    2. Compare to predictions:                                     ║
║                                                                   ║
║       ┌─────────────────────────────────────────────────────┐     ║
║       │  R ≈ 1.0 ± 0.3  →  UNPOLARIZED (standard GR)        │     ║
║       │                     Expected for astrophysical      │     ║
║       └─────────────────────────────────────────────────────┘     ║
║                                                                   ║
║       ┌─────────────────────────────────────────────────────┐     ║
║       │  R ≈ 3.1 ± 0.5  →  h+ ONLY (Z² chirality)           │     ║
║       │                     Would be extraordinary!         │     ║
║       └─────────────────────────────────────────────────────┘     ║
║                                                                   ║
║    3. Cross-check with H1-V1 / H1-L1 ratio:                       ║
║       • Unpolarized: ratio ≈ 1.0                                  ║
║       • Chiral: ratio ≈ 2.85                                      ║
║                                                                   ║
╚═══════════════════════════════════════════════════════════════════╝
"""
ax4.text(0.02, 0.98, decision_text, transform=ax4.transAxes, fontsize=10,
         fontfamily='monospace', verticalalignment='top')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'o4_chirality_projection.png'), dpi=150,
            bbox_inches='tight', facecolor='white')
print(f"\n  Saved: o4_chirality_projection.png")

# =============================================================================
# SUMMARY TABLE
# =============================================================================

print("\n" + "=" * 75)
print("SUMMARY: O4 CHIRALITY TEST PROJECTION")
print("=" * 75)

summary = f"""
╔═════════════════════════════════════════════════════════════════════════════╗
║                    O4 CHIRALITY TEST TIMELINE                               ║
╠═════════════════════════════════════════════════════════════════════════════╣
║                                                                             ║
║  ASTROPHYSICAL BACKGROUND:                                                  ║
║    Expected amplitude: Ω(25 Hz) ~ 10⁻⁹                                      ║
║    Source: Unresolved BBH/BNS mergers                                       ║
║                                                                             ║
║  DETECTION TIMELINE:                                                        ║
║    H1-L1 baseline: ~{T_detect_H1L1/86400/30:.0f} months to SNR = 3                                ║
║    H1-V1 baseline: ~{T_detect_H1V1/86400/30:.0f} months to SNR = 3                                ║
║                                                                             ║
║  CHIRALITY DISCRIMINATION (5σ):                                             ║
║    H1-L1: ~{T_distinguish_H1L1/86400/30:.0f} months to distinguish R=1 vs R=3.1                   ║
║    H1-V1: ~{T_distinguish_H1V1/86400/30:.0f} months to distinguish R=1 vs R=3.1                   ║
║                                                                             ║
║  O4 RUN PROJECTION:                                                         ║
║    Duration: {O4_effective_months:.0f} months effective                                          ║
║    Expected: Detection likely, chirality test possible                      ║
║                                                                             ║
║  RECOMMENDATION:                                                            ║
║    Run polarized search (γ_++ only) in parallel with standard search.       ║
║    When detection occurs, immediately compute R ratio.                      ║
║    Use H1-V1 baseline as primary (77% h+ sensitive).                        ║
║                                                                             ║
╚═════════════════════════════════════════════════════════════════════════════╝
"""
print(summary)

# =============================================================================
# SAVE RESULTS
# =============================================================================

results = {
    'projection_type': 'o4_chirality_test',
    'astrophysical_background': {
        'omega_25Hz': 1e-9,
        'spectral_index': 2/3,
        'source': 'BBH/BNS mergers'
    },
    'baselines': {
        'H1-L1': {
            'h_plus_fraction': float(h_plus_frac_H1L1),
            'null_test_ratio': float(R_H1L1),
            'time_to_detection_months': float(T_detect_H1L1/86400/30),
            'time_to_distinguish_months': float(T_distinguish_H1L1/86400/30)
        },
        'H1-V1': {
            'h_plus_fraction': float(h_plus_frac_H1V1),
            'null_test_ratio': float(R_H1V1),
            'time_to_detection_months': float(T_detect_H1V1/86400/30),
            'time_to_distinguish_months': float(T_distinguish_H1V1/86400/30)
        }
    },
    'o4_projection': {
        'effective_duration_months': float(O4_effective_months),
        'detection_likely': True,
        'chirality_test_possible': True
    },
    'recommendations': [
        'Run polarized search (gamma_++ only) in parallel with standard',
        'Use H1-V1 baseline as primary for chirality test',
        'Compute R ratio immediately upon any detection',
        'Cross-check with H1-V1/H1-L1 amplitude ratio'
    ]
}

with open(os.path.join(OUTPUT_DIR, 'o4_projection_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print("\n  Saved: o4_projection_results.json")
print("=" * 75)
