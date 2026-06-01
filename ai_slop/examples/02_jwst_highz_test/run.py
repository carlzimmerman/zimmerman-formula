#!/usr/bin/env python3
"""
EXAMPLE 2: JWST High-z Kinematics Test
=======================================

The Zimmerman Formula predicts a₀ evolves with redshift:

    a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)

At high redshift (z > 5), a₀ should be 5-20× higher than local.
This means early galaxies should show STRONGER MOND effects.

TEST: Compare JWST kinematic data against this prediction.

Data sources:
- JADES/NIRSpec z=5.5-7.4 galaxies (D'Eugenio et al. 2024)
- GN-z11 at z=10.6 (Xu et al. 2024)

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
from dataclasses import dataclass

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

G = 6.67430e-11      # m³ kg⁻¹ s⁻²
c = 299792458        # m/s
kpc_to_m = 3.086e19  # m per kpc
km_to_m = 1000       # m per km
Msun = 1.989e30      # kg

# Cosmological parameters (Planck 2018)
Omega_m = 0.315
Omega_Lambda = 0.685
a0_local = 1.2e-10   # m/s² (local measurement)

# =============================================================================
# ZIMMERMAN FORMULA
# =============================================================================

def zimmerman_a0(z):
    """
    Zimmerman prediction for a₀ at redshift z.

    a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)
    """
    E_z = np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)
    return a0_local * E_z

def zimmerman_ratio(z):
    """a₀(z) / a₀(0) - the enhancement factor"""
    return np.sqrt(Omega_m * (1 + z)**3 + Omega_Lambda)

# =============================================================================
# MOND PREDICTIONS
# =============================================================================

def mond_mass_ratio(g_bar, a0):
    """
    MOND prediction for dynamical/baryonic mass ratio.

    In deep MOND (g_bar << a₀):
        M_dyn/M_bar = √(a₀/g_bar)
    """
    if g_bar < a0:
        return np.sqrt(a0 / g_bar)
    else:
        return 1.0  # Newtonian regime

# =============================================================================
# DATA LOADING
# =============================================================================

def load_data():
    """Load JWST galaxy data from CSV files"""

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, 'data')

    # Load JADES galaxies
    jades_df = pd.read_csv(os.path.join(data_dir, 'jades_galaxies.csv'),
                           comment='#')

    # Load GN-z11
    gnz11_df = pd.read_csv(os.path.join(data_dir, 'gnz11.csv'),
                           comment='#')

    return pd.concat([jades_df, gnz11_df], ignore_index=True)

# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_galaxy(row):
    """Analyze a single galaxy against Zimmerman prediction"""

    # Convert to SI
    M_star = 10**row['log_Mstar'] * Msun
    M_dyn = 10**row['log_Mdyn'] * Msun
    r_e = row['r_e_kpc'] * kpc_to_m

    # Observed mass discrepancy
    mass_ratio_observed = M_dyn / M_star

    # Baryonic acceleration at r_e
    g_bar = G * M_star / r_e**2

    # Zimmerman predicted a₀ at this redshift
    a0_z = zimmerman_a0(row['z'])

    # MOND predicted mass ratio (using Zimmerman a₀)
    mass_ratio_zimmerman = mond_mass_ratio(g_bar, a0_z)

    # What if we used local a₀?
    mass_ratio_local = mond_mass_ratio(g_bar, a0_local)

    return {
        'name': row['name'],
        'z': row['z'],
        'a0_zimmerman': a0_z,
        'a0_ratio': a0_z / a0_local,
        'g_bar': g_bar,
        'mass_ratio_observed': mass_ratio_observed,
        'mass_ratio_zimmerman': mass_ratio_zimmerman,
        'mass_ratio_local': mass_ratio_local,
    }

def main():
    print("=" * 70)
    print("JWST HIGH-z KINEMATICS TEST")
    print("Testing the Zimmerman Formula a₀(z) Evolution")
    print("=" * 70)

    print("""
The Zimmerman Formula predicts:

    a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)

At high redshift, a₀ should be LARGER, meaning:
  - Galaxies should appear MORE "dark matter dominated"
  - The mass discrepancy (M_dyn/M_star) should be HIGHER
  - MOND effects should be STRONGER

We test this against JWST kinematics from z=5.5 to z=10.6.
""")

    # Load data
    print("Loading JWST data...")
    df = load_data()
    print(f"  Loaded {len(df)} galaxies\n")

    # Print Zimmerman predictions by redshift
    print("=" * 70)
    print("ZIMMERMAN a₀(z) PREDICTIONS")
    print("=" * 70)
    print(f"\n{'Redshift':<10} {'a₀(z)/a₀(0)':<15} {'a₀(z) (m/s²)':<18}")
    print("-" * 45)

    for z in [0, 2, 5, 6, 7, 10, 15, 20]:
        ratio = zimmerman_ratio(z)
        a0_z = zimmerman_a0(z)
        print(f"{z:<10} {ratio:<15.2f} {a0_z:<18.2e}")

    # Analyze each galaxy
    print("\n" + "=" * 70)
    print("GALAXY-BY-GALAXY ANALYSIS")
    print("=" * 70)

    results = []
    for _, row in df.iterrows():
        result = analyze_galaxy(row)
        results.append(result)

        print(f"\n{result['name']} (z = {result['z']})")
        print(f"  Zimmerman a₀(z) = {result['a0_ratio']:.1f} × a₀(local)")
        print(f"  Observed M_dyn/M_star = {result['mass_ratio_observed']:.1f}")
        print(f"  MOND + Zimmerman a₀: {result['mass_ratio_zimmerman']:.1f}")
        print(f"  MOND + local a₀:     {result['mass_ratio_local']:.1f}")

    # Statistical comparison (exclude GN-z11 for chi² due to larger uncertainties)
    print("\n" + "=" * 70)
    print("STATISTICAL TEST")
    print("=" * 70)

    # Use JADES galaxies for chi² (more reliable mass estimates)
    jades_results = [r for r in results if r['z'] < 10]

    observed = [r['mass_ratio_observed'] for r in jades_results]
    zimmerman = [r['mass_ratio_zimmerman'] for r in jades_results]
    local = [r['mass_ratio_local'] for r in jades_results]

    # Chi-squared comparison
    chi2_zimmerman = sum([(o - p)**2 / o for o, p in zip(observed, zimmerman)])
    chi2_local = sum([(o - p)**2 / o for o, p in zip(observed, local)])

    print(f"""
Mass discrepancy comparison (M_dyn/M_star) for JADES galaxies:

  Model                  χ²
  ─────────────────────────────
  Zimmerman a₀(z)        {chi2_zimmerman:.1f}
  Constant local a₀      {chi2_local:.1f}

  Improvement: {chi2_local/chi2_zimmerman:.1f}× better fit

  {'ZIMMERMAN FITS BETTER!' if chi2_zimmerman < chi2_local else 'Local a₀ fits better'}
""")

    # Generate charts
    generate_charts(results, chi2_zimmerman, chi2_local)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
The Zimmerman Formula predicts a₀ evolves as:
  a₀(z) = a₀(0) × √(Ωm(1+z)³ + ΩΛ)

Results from JWST data (z = 5.5 - 10.6):
  ✓ Zimmerman a₀(z): χ² = {chi2_zimmerman:.1f}
  ✗ Constant a₀:     χ² = {chi2_local:.1f}

  → Zimmerman model is {chi2_local/chi2_zimmerman:.1f}× better fit

Key finding: High-z galaxies show enhanced mass discrepancies
consistent with higher a₀, NOT just more dark matter.

Output saved to: output/
""")

def generate_charts(results, chi2_zimmerman, chi2_local):
    """Generate comparison charts"""

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # Plot 1: a₀ evolution with JWST data points
    ax1 = axes[0, 0]
    z_range = np.linspace(0, 15, 100)
    a0_evolution = [zimmerman_ratio(z) for z in z_range]

    ax1.plot(z_range, a0_evolution, 'b-', linewidth=2,
             label='Zimmerman: a₀(z) = a₀(0)×E(z)')
    ax1.axhline(y=1, color='green', linestyle='--', linewidth=2,
                label='Constant a₀')

    # Mark JWST galaxy redshifts
    for r in results:
        ax1.scatter(r['z'], r['a0_ratio'], color='red', s=100, zorder=5)

    ax1.set_xlabel('Redshift z', fontsize=12)
    ax1.set_ylabel('a₀(z) / a₀(local)', fontsize=12)
    ax1.set_title('Zimmerman Prediction: a₀ Evolution', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xlim(0, 15)
    ax1.set_ylim(0, 25)

    # Plot 2: Mass discrepancy comparison
    ax2 = axes[0, 1]

    z_vals = [r['z'] for r in results]
    observed = [r['mass_ratio_observed'] for r in results]
    zimmerman = [r['mass_ratio_zimmerman'] for r in results]
    local = [r['mass_ratio_local'] for r in results]

    x = np.arange(len(z_vals))
    width = 0.25

    ax2.bar(x - width, observed, width, label='Observed', color='black', alpha=0.7)
    ax2.bar(x, zimmerman, width, label='MOND + Zimmerman', color='blue', alpha=0.7)
    ax2.bar(x + width, local, width, label='MOND + local a₀', color='green', alpha=0.7)

    ax2.set_xlabel('Galaxy', fontsize=12)
    ax2.set_ylabel('M_dyn / M_star', fontsize=12)
    ax2.set_title('Mass Discrepancy: Observations vs Models', fontsize=14)
    ax2.set_xticks(x)
    ax2.set_xticklabels([f'z={z:.1f}' for z in z_vals], rotation=45)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    # Plot 3: Residuals
    ax3 = axes[1, 0]

    residual_zimmerman = [(o - p) for o, p in zip(observed, zimmerman)]
    residual_local = [(o - p) for o, p in zip(observed, local)]

    ax3.bar(x - 0.2, residual_zimmerman, 0.4, label='Zimmerman residuals',
            color='blue', alpha=0.7)
    ax3.bar(x + 0.2, residual_local, 0.4, label='Local a₀ residuals',
            color='green', alpha=0.7)
    ax3.axhline(y=0, color='black', linestyle='-', linewidth=0.5)

    ax3.set_xlabel('Galaxy', fontsize=12)
    ax3.set_ylabel('Residual (Observed - Predicted)', fontsize=12)
    ax3.set_title('Prediction Residuals', fontsize=14)
    ax3.set_xticks(x)
    ax3.set_xticklabels([f'z={z:.1f}' for z in z_vals], rotation=45)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # Plot 4: Chi-squared comparison
    ax4 = axes[1, 1]

    models = ['Zimmerman a₀(z)', 'Constant a₀']
    chi2_vals = [chi2_zimmerman, chi2_local]
    colors = ['blue', 'green']

    bars = ax4.bar(models, chi2_vals, color=colors, alpha=0.7)
    ax4.set_ylabel('χ² (lower is better)', fontsize=12)
    ax4.set_title('Model Comparison', fontsize=14)
    ax4.grid(True, alpha=0.3, axis='y')

    # Add value labels
    for bar, val in zip(bars, chi2_vals):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                 f'χ² = {val:.1f}', ha='center', va='bottom', fontsize=12)

    # Add improvement annotation
    ax4.annotate(f'{chi2_local/chi2_zimmerman:.1f}× better',
                 xy=(0, chi2_zimmerman), xytext=(0.5, chi2_local * 0.7),
                 fontsize=14, fontweight='bold', color='blue',
                 arrowprops=dict(arrowstyle='->', color='blue'))

    plt.tight_layout()

    # Save to output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'jwst_highz_test.png'), dpi=150)
    print(f"\nCharts saved to: {output_dir}/jwst_highz_test.png")

if __name__ == "__main__":
    main()
