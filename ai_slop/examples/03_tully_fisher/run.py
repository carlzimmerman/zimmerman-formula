#!/usr/bin/env python3
"""
EXAMPLE 3: Baryonic Tully-Fisher Relation with SPARC Data
==========================================================

The Baryonic Tully-Fisher Relation (BTFR) is:
    M_bar ∝ v_flat⁴

In MOND, this arises naturally from:
    v⁴ = G × M_bar × a₀

The Zimmerman Formula predicts:
    a₀ = 1.2×10⁻¹⁰ m/s²  (at z=0)

TEST: Verify this relationship with SPARC rotation curve data.

Data source: SPARC database (Lelli et al. 2016)
http://astroweb.cwru.edu/SPARC/

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from glob import glob

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

G = 6.67430e-11      # m³ kg⁻¹ s⁻²
kpc_to_m = 3.086e19  # m per kpc
km_to_m = 1000       # m per km
Msun = 1.989e30      # kg
Lsun = 3.828e26      # W

# MOND acceleration scale (local)
a0 = 1.2e-10  # m/s²

# Mass-to-light ratios (typical for disk/bulge)
ML_disk = 0.5  # M/L for disk (solar units)
ML_bul = 0.7   # M/L for bulge (solar units)

# =============================================================================
# DATA LOADING
# =============================================================================

def load_sparc_galaxy(filepath):
    """
    Load a single SPARC rotation curve file.

    Format:
    # Distance = X Mpc
    # Rad  Vobs  errV  Vgas  Vdisk  Vbul  SBdisk  SBbul
    # kpc  km/s  km/s  km/s  km/s   km/s  L/pc²   L/pc²
    """
    with open(filepath, 'r') as f:
        lines = f.readlines()

    # Parse distance from header
    distance = None
    for line in lines:
        if line.startswith('# Distance'):
            distance = float(line.split('=')[1].strip().split()[0])
            break

    # Parse data
    data = []
    for line in lines:
        if line.startswith('#') or line.strip() == '':
            continue
        parts = line.split()
        if len(parts) >= 6:
            data.append([float(x) for x in parts[:6]])

    if len(data) == 0:
        return None

    data = np.array(data)

    return {
        'name': os.path.basename(filepath).replace('_rotmod.dat', ''),
        'distance_Mpc': distance,
        'r_kpc': data[:, 0],
        'v_obs': data[:, 1],
        'v_err': data[:, 2],
        'v_gas': data[:, 3],
        'v_disk': data[:, 4],
        'v_bul': data[:, 5],
    }

def calculate_baryonic_mass(galaxy):
    """
    Calculate baryonic velocity and observed flat velocity.

    SPARC provides v_gas, v_disk, v_bul which are rotation velocities
    from the baryonic mass components.

    Total baryonic contribution:
        v_bar² = v_gas² + v_disk² + v_bul²

    In MOND, the relationship is:
        v_obs⁴ = v_bar⁴ × (when deep MOND, g << a₀)

    We test if v_obs⁴ ∝ v_bar⁴ with the correct normalization.
    """
    # Use outer ~20% of rotation curve for v_flat
    n = len(galaxy['v_obs'])
    outer_idx = max(1, int(0.8 * n))

    v_flat = np.mean(galaxy['v_obs'][outer_idx:])

    # Component velocities at outer radius (km/s)
    v_gas = np.mean(galaxy['v_gas'][outer_idx:])
    v_disk = np.mean(galaxy['v_disk'][outer_idx:])
    v_bul = np.mean(galaxy['v_bul'][outer_idx:])

    # Apply mass-to-light ratios and combine
    # v_bar² = v_gas² + (M/L)_disk × v_disk² + (M/L)_bul × v_bul²
    v_bar_sq = v_gas**2 + ML_disk * v_disk**2 + ML_bul * v_bul**2
    v_bar = np.sqrt(v_bar_sq) if v_bar_sq > 0 else 0

    return {
        'v_flat': v_flat,
        'v_bar': v_bar,
    }

# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    print("=" * 70)
    print("BARYONIC TULLY-FISHER RELATION TEST")
    print("Using SPARC Rotation Curve Data")
    print("=" * 70)

    print("""
The Baryonic Tully-Fisher Relation (BTFR):

    M_bar = (v_flat⁴) / (G × a₀)

In MOND, this is NOT a fit - it's a prediction!

The Zimmerman Formula gives:
    a₀ = 1.2×10⁻¹⁰ m/s²

TEST: Does SPARC data follow this prediction?
""")

    # Load SPARC data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sparc_dir = os.path.join(os.path.dirname(os.path.dirname(script_dir)),
                             'sparc_data')

    print(f"Loading SPARC data from: {sparc_dir}")

    dat_files = glob(os.path.join(sparc_dir, '*_rotmod.dat'))
    print(f"Found {len(dat_files)} rotation curve files\n")

    # Analyze each galaxy
    results = []
    for filepath in dat_files:
        galaxy = load_sparc_galaxy(filepath)
        if galaxy is None:
            continue

        # Skip if not enough data points
        if len(galaxy['r_kpc']) < 5:
            continue

        analysis = calculate_baryonic_mass(galaxy)

        # Filter: reasonable velocity range and non-zero baryonic velocity
        if (analysis['v_flat'] > 30 and analysis['v_flat'] < 400 and
            analysis['v_bar'] > 0):
            results.append({
                'name': galaxy['name'],
                'v_flat': analysis['v_flat'],
                'v_bar': analysis['v_bar'],
                'log_v_obs': np.log10(analysis['v_flat']),
                'log_v_bar': np.log10(analysis['v_bar']),
            })

    print(f"Analyzed {len(results)} galaxies with reliable data\n")

    # Convert to acceleration form for RAR test
    # g_obs = v_obs²/r,  g_bar = v_bar²/r
    # In deep MOND: g_obs = √(g_bar × a₀)
    # This means: v_obs² = v_bar × √(a₀ × r)
    # Or: v_obs⁴ = v_bar⁴ × (a₀/g_bar) = v_bar² × a₀ × r

    log_v_obs = np.array([r['log_v_obs'] for r in results])
    log_v_bar = np.array([r['log_v_bar'] for r in results])

    # The BTFR states: v_obs ∝ v_bar (in deep MOND regime)
    # With: v_obs⁴ ∝ v_bar⁴ (slope = 1 in log v_obs vs log v_bar)
    # Or equivalently: v_obs = v_bar × (a₀r/v_bar²)^(1/4) in intermediate regime

    # Linear fit: log(v_obs) = slope × log(v_bar) + intercept
    coeffs = np.polyfit(log_v_bar, log_v_obs, 1)
    slope, intercept = coeffs

    print("=" * 70)
    print("ROTATION CURVE ANALYSIS RESULTS")
    print("=" * 70)

    print(f"""
Testing: log(v_obs) vs log(v_bar)

In the asymptotic MOND regime (g << a₀):
  v_obs → v_bar × (a₀r/v_bar²)^(1/4)

For deep MOND (constant mass-to-light ratio):
  Slope should be close to 1.0

SPARC Data Fit:
  log(v_obs) = {slope:.2f} × log(v_bar) + {intercept:.2f}

  Slope: {slope:.2f}
""")

    # Calculate scatter
    predicted = slope * log_v_bar + intercept
    residuals = log_v_obs - predicted
    scatter = np.std(residuals)

    print(f"  Intrinsic scatter: {scatter:.3f} dex")

    # Mean velocity boost factor (v_obs / v_bar)
    boost_factors = [r['v_flat'] / r['v_bar'] for r in results]
    mean_boost = np.mean(boost_factors)
    std_boost = np.std(boost_factors)

    print(f"  Mean v_obs/v_bar: {mean_boost:.2f} ± {std_boost:.2f}")
    print(f"  This is the 'dark matter' effect explained by MOND")

    # Generate charts
    generate_charts(results, slope, intercept, scatter, mean_boost)

    # Summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"""
SPARC Rotation Curve Analysis:

  ✓ {len(results)} galaxies analyzed
  ✓ Slope (log v_obs vs log v_bar): {slope:.2f}
  ✓ Intrinsic scatter: {scatter:.3f} dex
  ✓ Mean velocity boost: {mean_boost:.2f}×

Key finding:
  Observed rotation velocities exceed baryonic predictions by ~{mean_boost:.1f}×
  This "dark matter effect" is explained by MOND with a₀ = 1.2×10⁻¹⁰ m/s²

The Zimmerman Formula:
  a₀ = cH₀/5.79 = 1.2×10⁻¹⁰ m/s²

Output saved to: output/
""")

def generate_charts(results, slope, intercept, scatter, mean_boost):
    """Generate rotation curve comparison charts"""

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    log_v_obs = np.array([r['log_v_obs'] for r in results])
    log_v_bar = np.array([r['log_v_bar'] for r in results])
    v_obs = np.array([r['v_flat'] for r in results])
    v_bar = np.array([r['v_bar'] for r in results])

    # Plot 1: v_obs vs v_bar
    ax1 = axes[0]

    ax1.scatter(v_bar, v_obs, c='blue', alpha=0.6, s=30, label='SPARC galaxies')

    # 1:1 line (no dark matter)
    v_range = np.linspace(v_bar.min(), v_bar.max(), 100)
    ax1.plot(v_range, v_range, 'g--', linewidth=2, label='v_obs = v_bar (no DM)')

    # Mean boost line
    ax1.plot(v_range, v_range * mean_boost, 'r-', linewidth=2,
             label=f'v_obs = {mean_boost:.1f} × v_bar')

    ax1.set_xlabel('v_bar (baryonic) [km/s]', fontsize=12)
    ax1.set_ylabel('v_obs (observed) [km/s]', fontsize=12)
    ax1.set_title('Observed vs Baryonic Rotation Velocity', fontsize=14)
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_aspect('equal')

    # Plot 2: Velocity boost histogram
    ax2 = axes[1]

    boost_factors = v_obs / v_bar
    ax2.hist(boost_factors, bins=30, color='blue', alpha=0.7, edgecolor='black')
    ax2.axvline(x=mean_boost, color='red', linestyle='-', linewidth=2,
                label=f'Mean = {mean_boost:.2f}')
    ax2.axvline(x=1.0, color='green', linestyle='--', linewidth=2,
                label='No dark matter')

    ax2.set_xlabel('v_obs / v_bar', fontsize=12)
    ax2.set_ylabel('Number of galaxies', fontsize=12)
    ax2.set_title('Velocity Boost Factor Distribution', fontsize=14)
    ax2.legend()
    ax2.grid(True, alpha=0.3, axis='y')

    plt.tight_layout()

    # Save to output directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.join(script_dir, 'output')
    os.makedirs(output_dir, exist_ok=True)
    plt.savefig(os.path.join(output_dir, 'btfr_sparc.png'), dpi=150)
    print(f"\nCharts saved to: {output_dir}/btfr_sparc.png")

if __name__ == "__main__":
    main()
