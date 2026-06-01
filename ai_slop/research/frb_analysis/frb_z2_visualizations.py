#!/usr/bin/env python3
"""
FRB Z² Framework Visualizations
================================

Publication-quality plots for FRB analysis.

Author: Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import matplotlib.patches as mpatches

# =============================================================================
# Z² CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321638...
Z = np.sqrt(Z_SQUARED)       # = 5.788810...
OMEGA_M = 6/19
OMEGA_L = 13/19

# =============================================================================
# DATA (from main analysis script)
# =============================================================================

# ASKAP localized FRBs with redshifts
LOCALIZED_FRBS = [
    ("FRB 180924", 361.4, 0.3214),
    ("FRB 181112", 589.3, 0.4755),
    ("FRB 190102", 364.5, 0.291),
    ("FRB 190608", 339.0, 0.1178),
    ("FRB 190611", 321.4, 0.378),
    ("FRB 190711", 593.1, 0.522),
    ("FRB 190714", 504.1, 0.2365),
    ("FRB 191001", 507.9, 0.234),
    ("FRB 191228", 297.5, 0.243),
    ("FRB 200430", 380.0, 0.161),
    ("FRB 200906", 577.8, 0.3688),
    ("FRB 210117", 730.0, 0.214),
    ("FRB 210320", 384.9, 0.279),
    ("FRB 210807", 251.1, 0.122),
    ("FRB 210912", 378.7, 0.196),
    ("FRB 211127", 234.8, 0.0469),
    ("FRB 211212", 206.0, 0.0707),
    ("FRB 220105", 583.0, 0.442),
    ("FRB 220310", 462.3, 0.479),
    ("FRB 220501", 449.0, 0.384),
    ("FRB 220610", 1458.0, 1.016),  # Highest z
    ("FRB 220725", 287.0, 0.193),
    ("FRB 220912", 219.5, 0.0771),
]

# All ASKAP DMs for distribution
ALL_DMS = [609.5, 523.2, 991.7, 235.2, 312.8, 390.6, 463.2, 304.0, 114.1, 618.5,
           158.6, 203.1, 361.4, 589.3, 364.5, 339.0, 321.4, 593.1, 504.1, 507.9,
           297.5, 380.0, 577.8, 730.0, 384.9, 251.1, 378.7, 234.8, 206.0, 583.0,
           462.3, 449.0, 1458.0, 287.0, 219.5, 411.2, 523.7, 287.4, 618.9, 445.3,
           372.6, 556.8]

# =============================================================================
# COSMOLOGY FUNCTIONS
# =============================================================================

def E_z(z):
    return np.sqrt(OMEGA_M * (1 + z)**3 + OMEGA_L)

def DM_cosmic_theory(z, f_IGM=0.84):
    """Theoretical cosmic DM."""
    if z == 0:
        return 0.0
    z_arr = np.linspace(0, z, 1000)
    integrand = (1 + z_arr) / E_z(z_arr)
    integral = np.trapz(integrand, z_arr)
    return 935 * f_IGM * integral

def DM_cosmic_z2(z):
    """Z² modified cosmic DM."""
    if z == 0:
        return 0.0
    a0_ratio = E_z(z)
    f_IGM_z2 = 0.84 / (1 + 0.08 * np.log(max(1, a0_ratio)))
    return DM_cosmic_theory(z, f_IGM=f_IGM_z2)

# =============================================================================
# FIGURE 1: DM-z Relation
# =============================================================================

def plot_dm_z_relation():
    """Plot DM-redshift relation comparing Z² to standard."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Data points
    DM_MW = 50  # Milky Way contribution
    names = [f[0] for f in LOCALIZED_FRBS]
    dms = np.array([f[1] - DM_MW for f in LOCALIZED_FRBS])
    zs = np.array([f[2] for f in LOCALIZED_FRBS])

    # Sort by redshift for plotting
    sort_idx = np.argsort(zs)
    dms = dms[sort_idx]
    zs = zs[sort_idx]
    names = [names[i] for i in sort_idx]

    # Theory curves
    z_theory = np.linspace(0.01, 1.2, 100)
    dm_std = np.array([DM_cosmic_theory(z) for z in z_theory])
    dm_z2 = np.array([DM_cosmic_z2(z) for z in z_theory])

    # Plot theory
    ax.plot(z_theory, dm_std, 'r-', linewidth=2.5, label='Standard ΛCDM (f_IGM = 0.84)')
    ax.plot(z_theory, dm_z2, 'b--', linewidth=2.5, label='Z² Framework (evolving f_IGM)')
    ax.fill_between(z_theory, dm_std, dm_z2, alpha=0.2, color='purple',
                   label=f'Z² deviation ({(1-dm_z2[-1]/dm_std[-1])*100:.1f}% at z=1.2)')

    # Plot data
    ax.scatter(zs, dms, s=100, c='black', marker='o', zorder=5,
              label=f'ASKAP localized FRBs (N={len(zs)})')

    # Highlight highest z FRB
    high_z_idx = np.argmax(zs)
    ax.scatter(zs[high_z_idx], dms[high_z_idx], s=200, c='gold', marker='*',
              edgecolors='black', linewidths=1.5, zorder=6,
              label=f'FRB 220610 (z={zs[high_z_idx]:.3f})')

    # Error bars (typical 50 pc/cm³ + 10% systematic)
    yerr = np.sqrt(50**2 + (0.1 * dms)**2)
    ax.errorbar(zs, dms, yerr=yerr, fmt='none', ecolor='gray', alpha=0.5, capsize=3)

    # Labels
    ax.set_xlabel('Redshift z', fontsize=14)
    ax.set_ylabel('DM$_{extragalactic}$ (pc cm$^{-3}$)', fontsize=14)
    ax.set_title('FRB Dispersion Measure vs Redshift\nASKAP/CRAFT Localized Sample', fontsize=16)
    ax.legend(loc='upper left', fontsize=11)
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, 1.1)
    ax.set_ylim(0, 1600)

    # Add annotation
    textstr = f'Z² = 32π/3 = {Z_SQUARED:.2f}\nΩ_Λ = 13/19 = {OMEGA_L:.4f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.02, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', bbox=props)

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/frb_analysis/frb_dm_z_relation.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: frb_dm_z_relation.png")

# =============================================================================
# FIGURE 2: DM Distribution with Z² Multiples
# =============================================================================

def plot_dm_distribution():
    """Plot DM distribution highlighting Z² multiples."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

    dms = np.array(ALL_DMS)

    # Left panel: Histogram
    bins = np.linspace(0, 1600, 30)
    ax1.hist(dms, bins=bins, color='steelblue', edgecolor='black', alpha=0.7)

    # Mark Z² multiples
    z2_multiples = [n * Z_SQUARED for n in [1, 2, 5, 10, 12, 15, 20, 30, 40]]
    colors = plt.cm.Reds(np.linspace(0.3, 0.9, len(z2_multiples)))

    for i, (mult, color) in enumerate(zip(z2_multiples, colors)):
        if mult < 1600:
            ax1.axvline(mult, color=color, linestyle='--', linewidth=1.5, alpha=0.7)
            if mult < 800:
                ax1.text(mult + 10, ax1.get_ylim()[1] * 0.9 - i*0.8, f'{int(mult/Z_SQUARED)}×Z²',
                        fontsize=9, rotation=90, va='top')

    # Mark median
    dm_median = np.median(dms)
    ax1.axvline(dm_median, color='red', linestyle='-', linewidth=2,
               label=f'Median = {dm_median:.0f} pc/cm³')
    ax1.axvline(12 * Z_SQUARED, color='green', linestyle='-', linewidth=2,
               label=f'12×Z² = {12*Z_SQUARED:.0f} pc/cm³')

    ax1.set_xlabel('DM (pc cm$^{-3}$)', fontsize=12)
    ax1.set_ylabel('Count', fontsize=12)
    ax1.set_title('ASKAP FRB DM Distribution', fontsize=14)
    ax1.legend(fontsize=10)

    # Right panel: DM vs Z² multiple residuals
    ratios = dms / Z_SQUARED
    nearest_int = np.round(ratios)
    residuals = (ratios - nearest_int) * 100 / nearest_int  # Percent deviation

    ax2.scatter(nearest_int, residuals, s=60, c='steelblue', alpha=0.7)
    ax2.axhline(0, color='red', linestyle='-', linewidth=1)
    ax2.axhline(5, color='gray', linestyle='--', alpha=0.5)
    ax2.axhline(-5, color='gray', linestyle='--', alpha=0.5)

    ax2.set_xlabel('Nearest integer n (DM ≈ n × Z²)', fontsize=12)
    ax2.set_ylabel('% deviation from n × Z²', fontsize=12)
    ax2.set_title('DM Residuals from Z² Multiples', fontsize=14)
    ax2.set_xlim(0, 50)
    ax2.set_ylim(-50, 50)
    ax2.grid(True, alpha=0.3)

    # Annotation for the 12×Z² finding
    n12_mask = nearest_int == 12
    if np.any(n12_mask):
        n12_residuals = residuals[n12_mask]
        ax2.scatter(np.ones(np.sum(n12_mask)) * 12, n12_residuals,
                   s=150, c='gold', edgecolors='black', marker='*', zorder=5,
                   label=f'Median at n=12 ({np.mean(n12_residuals):+.1f}%)')
        ax2.legend()

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/frb_analysis/frb_dm_distribution.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: frb_dm_distribution.png")

# =============================================================================
# FIGURE 3: Z² Prediction for Future FRBs
# =============================================================================

def plot_z2_prediction():
    """Plot Z² framework predictions for high-z FRB observations."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))

    # Panel 1: DM-z with Z² prediction bands
    ax1 = axes[0, 0]
    z_arr = np.linspace(0.01, 3, 100)
    dm_std = np.array([DM_cosmic_theory(z) for z in z_arr])
    dm_z2 = np.array([DM_cosmic_z2(z) for z in z_arr])

    ax1.fill_between(z_arr, dm_std * 0.8, dm_std * 1.2, alpha=0.3, color='red',
                    label='Standard ±20%')
    ax1.fill_between(z_arr, dm_z2 * 0.8, dm_z2 * 1.2, alpha=0.3, color='blue',
                    label='Z² ±20%')
    ax1.plot(z_arr, dm_std, 'r-', linewidth=2)
    ax1.plot(z_arr, dm_z2, 'b--', linewidth=2)

    # Current data
    zs_data = np.array([f[2] for f in LOCALIZED_FRBS])
    dms_data = np.array([f[1] - 50 for f in LOCALIZED_FRBS])
    ax1.scatter(zs_data, dms_data, s=50, c='black', zorder=5)

    ax1.set_xlabel('Redshift z', fontsize=12)
    ax1.set_ylabel('DM$_{cosmic}$ (pc cm$^{-3}$)', fontsize=12)
    ax1.set_title('DM-z Relation: Standard vs Z²', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)

    # Panel 2: Percent difference
    ax2 = axes[0, 1]
    diff_pct = 100 * (dm_z2 - dm_std) / dm_std
    ax2.plot(z_arr, diff_pct, 'purple', linewidth=2)
    ax2.fill_between(z_arr, diff_pct, 0, alpha=0.3, color='purple')
    ax2.axhline(0, color='black', linestyle='-')
    ax2.axhline(-5, color='red', linestyle='--', alpha=0.5, label='-5% threshold')

    ax2.set_xlabel('Redshift z', fontsize=12)
    ax2.set_ylabel('(DM$_{Z²}$ - DM$_{std}$) / DM$_{std}$ (%)', fontsize=12)
    ax2.set_title('Z² Deviation from Standard Model', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim(-10, 2)

    # Panel 3: a₀ evolution with redshift
    ax3 = axes[1, 0]
    a0_ratio = np.array([E_z(z) for z in z_arr])
    ax3.plot(z_arr, a0_ratio, 'g-', linewidth=2)
    ax3.axhline(1, color='black', linestyle='--', alpha=0.5)

    ax3.set_xlabel('Redshift z', fontsize=12)
    ax3.set_ylabel('a₀(z) / a₀(0) = H(z)/H₀', fontsize=12)
    ax3.set_title('MOND Acceleration Scale Evolution (Z² Framework)', fontsize=14)
    ax3.grid(True, alpha=0.3)

    # Mark key redshifts
    for z_mark, label in [(0.5, 'z=0.5'), (1.0, 'z=1'), (2.0, 'z=2')]:
        a0_mark = E_z(z_mark)
        ax3.scatter([z_mark], [a0_mark], s=100, c='red', zorder=5)
        ax3.annotate(f'{label}\na₀={a0_mark:.2f}×', (z_mark, a0_mark),
                    textcoords="offset points", xytext=(10, 0), fontsize=10)

    # Panel 4: Summary of key Z² predictions
    ax4 = axes[1, 1]
    ax4.axis('off')

    predictions = """
    ┌────────────────────────────────────────────────────────────────┐
    │              Z² FRAMEWORK PREDICTIONS FOR FRBs                 │
    ├────────────────────────────────────────────────────────────────┤
    │                                                                │
    │  TESTABLE PREDICTIONS:                                         │
    │                                                                │
    │  1. DM-z Relation at z > 1:                                    │
    │     • Z² predicts 3-5% LOWER DM at fixed z                    │
    │     • Due to enhanced structure formation                     │
    │     • Testable with >100 localized FRBs at z > 0.5            │
    │                                                                │
    │  2. Host Galaxy Dynamics:                                      │
    │     • σ = v_flat / Z for FRB host galaxies                    │
    │     • Mass discrepancy ∝ √(a₀(z))                             │
    │     • Testable with IFU spectroscopy                          │
    │                                                                │
    │  3. CGM Probing:                                               │
    │     • MOND phantom DM profile ≠ NFW halo                      │
    │     • Different DM vs impact parameter shape                  │
    │                                                                │
    │  CURRENT STATUS:                                               │
    │     • 23 ASKAP localized FRBs analyzed                        │
    │     • Z² and standard models currently indistinguishable      │
    │     • Need more z > 0.5 FRBs for definitive test              │
    │                                                                │
    │  TIMELINE:                                                     │
    │     • DSA-2000 (2027+): ~1000 localized FRBs/year            │
    │     • CHORD (2026+): High-z FRB localizations                 │
    │     • Definitive test possible by 2028-2030                   │
    │                                                                │
    └────────────────────────────────────────────────────────────────┘
    """
    ax4.text(0.05, 0.95, predictions, transform=ax4.transAxes,
             fontsize=10, family='monospace', verticalalignment='top')

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/frb_analysis/frb_z2_predictions.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: frb_z2_predictions.png")

# =============================================================================
# FIGURE 4: Integer Multiple Analysis
# =============================================================================

def plot_integer_analysis():
    """Detailed analysis of DM = 12 × Z² finding."""
    fig, ax = plt.subplots(figsize=(10, 8))

    dms = np.array(ALL_DMS)
    dm_median = np.median(dms)

    # Calculate ratios to Z²
    n_range = np.arange(1, 50)
    theoretical_dms = n_range * Z_SQUARED

    # For each FRB, find closest integer multiple
    closest_n = np.round(dms / Z_SQUARED).astype(int)

    # Count how many FRBs are near each integer
    counts = np.array([np.sum(closest_n == n) for n in n_range])

    # Expected from uniform distribution in DM range
    dm_min, dm_max = dms.min(), dms.max()
    expected_uniform = len(dms) / ((dm_max - dm_min) / Z_SQUARED)

    # Plot
    ax.bar(n_range, counts, color='steelblue', alpha=0.7, edgecolor='black',
          label='Observed')
    ax.axhline(expected_uniform, color='red', linestyle='--', linewidth=2,
              label=f'Expected (uniform): {expected_uniform:.1f}')

    # Highlight n=12 (median)
    n12_idx = np.where(n_range == 12)[0][0]
    ax.bar(12, counts[n12_idx], color='gold', edgecolor='black', linewidth=2,
          label=f'n=12: {counts[n12_idx]} FRBs')

    # Poisson significance
    from scipy.stats import poisson
    p_value = 1 - poisson.cdf(counts[n12_idx] - 1, expected_uniform)

    ax.set_xlabel('Integer n (DM ≈ n × Z²)', fontsize=12)
    ax.set_ylabel('Number of FRBs', fontsize=12)
    ax.set_title(f'FRB DM Distribution in Z² Units\nMedian DM = {dm_median:.0f} ≈ 12 × Z² = {12*Z_SQUARED:.0f}',
                fontsize=14)
    ax.legend(fontsize=11)
    ax.set_xlim(0, 50)
    ax.grid(True, alpha=0.3, axis='y')

    # Annotation
    textstr = f'Z² = 32π/3 = {Z_SQUARED:.2f}\n12 × Z² = {12*Z_SQUARED:.1f}\nDM median = {dm_median:.1f}\nRatio = {dm_median/(12*Z_SQUARED):.3f}'
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(0.98, 0.98, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right', bbox=props)

    plt.tight_layout()
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/frb_analysis/frb_integer_analysis.png',
                dpi=150, bbox_inches='tight')
    plt.close()
    print("Saved: frb_integer_analysis.png")

# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    print("Generating FRB Z² visualizations...")
    print(f"Z² = {Z_SQUARED:.6f}, Z = {Z:.6f}")
    print()

    plot_dm_z_relation()
    plot_dm_distribution()
    plot_z2_prediction()
    plot_integer_analysis()

    print("\nAll visualizations saved to research/frb_analysis/")
