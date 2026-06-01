#!/usr/bin/env python3
"""
Z² Framework vs LIGO Comparison
================================

Overlays the Z² framework prediction on the stochastic search results
and produces a final publication-quality comparison figure.

Z² Prediction:
- Tensor-to-scalar ratio r = 1/(2Z²) = 0.01492
- Only h+ polarization survives the Z₂ orbifold projection
- Ω_GW(f) = (3/128) × r × (H₀²/π²) × (f/f_ref)^(n_t)
- where n_t = -r/8 ≈ -0.00187 (inflationary consistency relation)

Author: Carl Zimmerman
Date: May 2026
"""

import os
import json
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

print("=" * 70)
print("Z² FRAMEWORK vs LIGO COMPARISON")
print("=" * 70)

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
STANDARD_FILE = os.path.join(OUTPUT_DIR, 'standard_search_results.json')
POLARIZED_FILE = os.path.join(OUTPUT_DIR, 'polarized_search_results.json')
PLOT_FILE = os.path.join(OUTPUT_DIR, 'z2_framework_ligo_comparison.png')

# Physical constants
H0_SI = 67.4e3 / 3.086e22  # Hubble constant in SI (s^-1)
H0_100 = 67.4 / 100        # h = H0 / (100 km/s/Mpc)
c = 299792458.0

# Z² framework constants
Z2 = 32 * np.pi / 3          # = 33.51
r_Z2 = 1 / (2 * Z2)          # = 0.01492
n_t = -r_Z2 / 8              # tensor spectral index = -0.00187
f_ref = 0.01                 # Reference frequency (Hz) for CMB normalization

# Analysis frequency range
F_LOW = 20.0
F_HIGH = 1726.0

# =============================================================================
# STEP 1: Load search results
# =============================================================================

print("\n[1] Loading search results...")

with open(STANDARD_FILE, 'r') as f:
    standard_results = json.load(f)

with open(POLARIZED_FILE, 'r') as f:
    polarized_results = json.load(f)

print(f"  Standard search loaded: UL = {standard_results['upper_limit_95_percent']:.2e}")
print(f"  Polarized search loaded: UL = {polarized_results['polarized_search']['upper_limit_95']:.2e}")

# Extract ORF data
freqs_orf = np.array(polarized_results['orf_comparison']['frequencies_hz'])
gamma_standard = np.array(polarized_results['orf_comparison']['gamma_standard'])
gamma_polarized = np.array(polarized_results['orf_comparison']['gamma_polarized'])

# Get sensitivity data
freqs_spec = np.array(standard_results['omega_gw_spectrum']['frequencies_hz'])
sigma_standard = np.array(standard_results['omega_gw_spectrum']['sigma'])

# =============================================================================
# STEP 2: Compute Z² predicted Ω_GW spectrum
# =============================================================================

print("\n[2] Computing Z² framework prediction...")

def omega_gw_primordial(f, r, H0_100, n_t, f_ref=0.01):
    """
    Compute the primordial gravitational wave background energy density.

    Ω_GW(f) h² = (3/128) × r × (f/f_pivot)^n_t × Δ_R²

    For standard slow-roll inflation with Δ_R² ≈ 2.1×10⁻⁹ at k = 0.05 Mpc⁻¹.

    The transfer function from CMB scales to LIGO frequencies includes:
    - Reentry during radiation era: factor of 0.83
    - Matter-radiation equality suppression
    """
    # CMB scalar amplitude
    A_s = 2.1e-9  # Planck 2018

    # Tensor amplitude at CMB scales
    A_t = r * A_s

    # Frequency of horizon entry for CMB pivot scale (k = 0.05 Mpc⁻¹)
    # f_CMB ≈ 3×10⁻¹⁸ Hz

    # Transfer function for modes that re-entered during radiation era
    # These modes get suppressed by a factor compared to CMB
    # T(f)² ≈ 0.83 × (f_eq/f)² for f >> f_eq
    # where f_eq ≈ 2×10⁻¹⁷ Hz is matter-radiation equality frequency

    # Simplified expression valid for LIGO frequencies:
    # Ω_GW(f) h² ≈ (3/128) × r × Ω_r × (f/f_ref)^n_t

    # Radiation density parameter
    Omega_r = 9.15e-5  # Ω_r h²

    # At LIGO frequencies, the GW background that re-entered during RD era:
    # Ω_GW h² ≈ (3/128) × r × Ω_r × A_s^(1/2) × (f/f_pivot)^n_t

    # More accurate formula from Maggiore (2000):
    # Ω_GW(f) h² = (3.6×10⁻¹⁵) × r × (f/f_*)^n_t
    # where f_* = 7.7×10⁻¹⁷ Hz

    f_star = 7.7e-17  # Hz

    # This gives the spectrum
    Omega_h2 = 3.6e-15 * r * (f / f_star)**n_t

    # Convert to Ω_GW (divide by h²)
    Omega_GW = Omega_h2 / H0_100**2

    return Omega_GW


# Compute prediction across LIGO band
freqs_pred = np.logspace(np.log10(F_LOW), np.log10(F_HIGH), 500)
Omega_Z2 = omega_gw_primordial(freqs_pred, r_Z2, H0_100, n_t)

# Also compute for other values of r for comparison
Omega_r001 = omega_gw_primordial(freqs_pred, 0.01, H0_100, -0.01/8)
Omega_r01 = omega_gw_primordial(freqs_pred, 0.1, H0_100, -0.1/8)

print(f"  Z² prediction at 25 Hz: Ω_GW = {omega_gw_primordial(25, r_Z2, H0_100, n_t):.2e}")
print(f"  Z² prediction at 100 Hz: Ω_GW = {omega_gw_primordial(100, r_Z2, H0_100, n_t):.2e}")
print(f"  Z² prediction at 1000 Hz: Ω_GW = {omega_gw_primordial(1000, r_Z2, H0_100, n_t):.2e}")

# =============================================================================
# STEP 3: Calculate the gap to detection
# =============================================================================

print("\n[3] Calculating sensitivity gap...")

UL_standard = standard_results['upper_limit_95_percent']
UL_polarized = polarized_results['polarized_search']['upper_limit_95']

# Z² prediction at typical LIGO frequency
Omega_Z2_100Hz = omega_gw_primordial(100, r_Z2, H0_100, n_t)

gap_orders = np.log10(UL_standard / Omega_Z2_100Hz)
improvement_needed = UL_standard / Omega_Z2_100Hz

print(f"  Current 95% UL: {UL_standard:.2e}")
print(f"  Z² prediction: {Omega_Z2_100Hz:.2e}")
print(f"  Gap: {gap_orders:.1f} orders of magnitude")
print(f"  Improvement factor needed: {improvement_needed:.2e}")

# Future detector projections
# Einstein Telescope / Cosmic Explorer target sensitivity
ET_sensitivity = 1e-12  # approximate at 100 Hz
CE_sensitivity = 1e-13
gap_to_ET = np.log10(ET_sensitivity / Omega_Z2_100Hz)
gap_to_CE = np.log10(CE_sensitivity / Omega_Z2_100Hz)

print(f"\n  Einstein Telescope gap: {gap_to_ET:.1f} orders of magnitude")
print(f"  Cosmic Explorer gap: {gap_to_CE:.1f} orders of magnitude")

# =============================================================================
# STEP 4: Generate 4-panel comparison figure
# =============================================================================

print("\n[4] Generating comparison figure...")

fig = plt.figure(figsize=(16, 12))

# Use gridspec for custom layout
from matplotlib.gridspec import GridSpec
gs = GridSpec(2, 2, figure=fig, hspace=0.3, wspace=0.3)

# Panel 1: Both ORFs
ax1 = fig.add_subplot(gs[0, 0])
ax1.semilogx(freqs_orf, gamma_standard, 'b-', linewidth=2, label='Standard (h+ + h×)')
ax1.semilogx(freqs_orf, gamma_polarized, 'r-', linewidth=2, label='Polarized (h+ only)')
ax1.fill_between(freqs_orf, gamma_polarized, gamma_standard, alpha=0.2, color='purple')
ax1.set_xlabel('Frequency [Hz]', fontsize=12)
ax1.set_ylabel('Overlap Reduction Function γ(f)', fontsize=12)
ax1.set_title('Panel A: Overlap Reduction Functions', fontsize=13, fontweight='bold')
ax1.set_xlim(F_LOW, F_HIGH)
ax1.set_ylim(0, 1.2)
ax1.grid(True, alpha=0.3)
ax1.legend(loc='upper right', fontsize=10)

# Panel 2: Ω_GW sensitivity with Z² prediction
ax2 = fig.add_subplot(gs[0, 1])

# Downsample sensitivity for cleaner plot
step = max(1, len(freqs_spec) // 500)
freqs_plot = freqs_spec[::step]
sigma_plot = sigma_standard[::step]

# Sensitivity curves
ax2.loglog(freqs_plot, sigma_plot, 'b-', linewidth=1.5, alpha=0.7, label='LIGO O3 sensitivity')
ax2.axhline(UL_standard, color='blue', linestyle='--', linewidth=2,
            label=f'Standard UL = {UL_standard:.1e}')
ax2.axhline(UL_polarized, color='red', linestyle=':', linewidth=2,
            label=f'Polarized UL = {UL_polarized:.1e}')

# Z² prediction
ax2.loglog(freqs_pred, Omega_Z2, 'darkgreen', linewidth=2.5,
           label=f'Z² prediction (r = {r_Z2:.4f})')

# Other r values for context
ax2.loglog(freqs_pred, Omega_r01, 'green', linewidth=1, alpha=0.5,
           linestyle='-.', label='r = 0.1 (excluded)')
ax2.loglog(freqs_pred, Omega_r001, 'lightgreen', linewidth=1, alpha=0.5,
           linestyle=':', label='r = 0.01')

# Future detector projections
ax2.axhline(ET_sensitivity, color='orange', linestyle='--', linewidth=1.5, alpha=0.7,
            label='Einstein Telescope (projected)')
ax2.axhline(CE_sensitivity, color='purple', linestyle='--', linewidth=1.5, alpha=0.7,
            label='Cosmic Explorer (projected)')

ax2.set_xlabel('Frequency [Hz]', fontsize=12)
ax2.set_ylabel('Ω_GW', fontsize=12)
ax2.set_title('Panel B: Sensitivity vs Z² Prediction', fontsize=13, fontweight='bold')
ax2.set_xlim(F_LOW, F_HIGH)
ax2.set_ylim(1e-18, 1e-3)
ax2.legend(loc='upper left', fontsize=8, ncol=2)
ax2.grid(True, alpha=0.3, which='both')

# Panel 3: ORF ratio
ax3 = fig.add_subplot(gs[1, 0])
ratio_orf = gamma_polarized / np.maximum(gamma_standard, 1e-10)
ax3.semilogx(freqs_orf, ratio_orf, 'purple', linewidth=2)
ax3.axhline(0.5, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
            label='Theoretical: 0.5 for aligned detectors')
ax3.fill_between(freqs_orf, 0, ratio_orf, alpha=0.3, color='purple')
ax3.set_xlabel('Frequency [Hz]', fontsize=12)
ax3.set_ylabel('γ_polarized / γ_standard', fontsize=12)
ax3.set_title('Panel C: ORF Ratio (h+ only / Standard)', fontsize=13, fontweight='bold')
ax3.set_xlim(F_LOW, F_HIGH)
ax3.set_ylim(0, 1.5)
ax3.grid(True, alpha=0.3)
ax3.legend(loc='upper right', fontsize=10)

# Panel 4: Summary text box
ax4 = fig.add_subplot(gs[1, 1])
ax4.axis('off')

summary = f"""
┌─────────────────────────────────────────────────────────────────────┐
│                    Z² FRAMEWORK LIGO COMPARISON                     │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  Z² FRAMEWORK PREDICTION:                                           │
│    • Z² = 32π/3 = {Z2:.4f}                                          │
│    • Tensor-to-scalar ratio: r = 1/(2Z²) = {r_Z2:.5f}              │
│    • Tensor spectral index: n_t = -r/8 = {n_t:.5f}                 │
│    • Polarization: h+ only (h× projected out by Z₂ orbifold)       │
│                                                                     │
│  PREDICTED SIGNAL:                                                  │
│    • Ω_GW(25 Hz)  = {omega_gw_primordial(25, r_Z2, H0_100, n_t):.2e}                           │
│    • Ω_GW(100 Hz) = {omega_gw_primordial(100, r_Z2, H0_100, n_t):.2e}                          │
│    • Ω_GW(1 kHz)  = {omega_gw_primordial(1000, r_Z2, H0_100, n_t):.2e}                         │
│                                                                     │
│  CURRENT LIGO SENSITIVITY (this analysis):                          │
│    • Standard search 95% UL:  Ω_GW < {UL_standard:.2e}               │
│    • Polarized search 95% UL: Ω_GW < {UL_polarized:.2e}              │
│                                                                     │
│  GAP TO DETECTION:                                                  │
│    • Current gap: {gap_orders:.1f} orders of magnitude                      │
│    • Einstein Telescope: {gap_to_ET:.1f} orders below prediction            │
│    • Cosmic Explorer: {gap_to_CE:.1f} orders below prediction               │
│                                                                     │
│  HONEST ASSESSMENT:                                                 │
│    The Z² primordial GW prediction is ~{int(gap_orders)} orders of magnitude    │
│    below current LIGO sensitivity. Even next-generation ground      │
│    detectors (ET, CE) won't reach r ~ 0.01 for direct detection.    │
│                                                                     │
│    The prediction IS testable via:                                  │
│    1. CMB B-mode polarization (LiteBIRD, CMB-S4): r ~ 0.001-0.01   │
│    2. Pulsar timing arrays: different frequency band                │
│    3. Future space detectors (LISA, BBO): μHz-Hz band              │
│                                                                     │
│  DATA: O3a, 4 hours, H1-L1 cross-correlation                       │
│  DATE: May 2026                                                     │
└─────────────────────────────────────────────────────────────────────┘
"""

ax4.text(0.02, 0.98, summary, transform=ax4.transAxes,
         fontfamily='monospace', fontsize=9,
         verticalalignment='top',
         bbox=dict(boxstyle='round', facecolor='lightgray', alpha=0.3))

fig.suptitle('Z² Framework Gravitational Wave Prediction vs LIGO Sensitivity',
             fontsize=16, fontweight='bold', y=0.98)

plt.savefig(PLOT_FILE, dpi=200, bbox_inches='tight', facecolor='white')
print(f"  Saved figure to: {os.path.basename(PLOT_FILE)}")

# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("\n" + "=" * 70)
print("Z² FRAMEWORK LIGO COMPARISON - FINAL ASSESSMENT")
print("=" * 70)

print(f"""
╔══════════════════════════════════════════════════════════════════════════╗
║                         EXECUTIVE SUMMARY                                ║
╠══════════════════════════════════════════════════════════════════════════╣
║                                                                          ║
║  Z² PREDICTION:                                                          ║
║    • r = 1/(2Z²) = {r_Z2:.5f}                                             ║
║    • h+ polarization only (Z₂ projection)                                ║
║    • Ω_GW ~ 10⁻¹⁵ at LIGO frequencies                                    ║
║                                                                          ║
║  CURRENT SENSITIVITY:                                                    ║
║    • LIGO O3 (this analysis): Ω_GW ~ 10⁻⁵                                ║
║    • Published O3 stochastic limits: Ω_GW ~ 10⁻⁸ to 10⁻⁹                 ║
║                                                                          ║
║  SENSITIVITY GAP: ~{int(gap_orders)} ORDERS OF MAGNITUDE                           ║
║                                                                          ║
║  FUTURE PROSPECTS:                                                       ║
║    • LiteBIRD (2028-2031): Can test r = 0.015 via CMB B-modes           ║
║    • CMB-S4 (~2030): r ~ 0.001 sensitivity                              ║
║    • Einstein Telescope: Still ~4 orders below Z² prediction            ║
║    • Cosmic Explorer: Still ~3 orders below Z² prediction               ║
║                                                                          ║
║  BOTTOM LINE:                                                            ║
║    The Z² prediction r = 0.0149 is NOT testable with LIGO.              ║
║    It IS testable with upcoming CMB B-mode experiments.                  ║
║    LiteBIRD will provide the definitive test in 2028-2031.               ║
║                                                                          ║
╚══════════════════════════════════════════════════════════════════════════╝
""")

print("  Output files:")
print(f"    - {os.path.basename(PLOT_FILE)}")
print(f"    - standard_search_results.json")
print(f"    - polarized_search_results.json")

print("\n" + "=" * 70)
