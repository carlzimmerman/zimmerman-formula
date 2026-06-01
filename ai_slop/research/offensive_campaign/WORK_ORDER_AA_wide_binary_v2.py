#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER AA v2: WIDE BINARY GRAVITY TEST - CORRECTED METHODOLOGY
================================================================================

The proper motion difference in wide binaries includes projection effects
and is not a direct measure of orbital velocity. Following Pittordis &
Sutherland (2023) methodology:

The key observable is the "velocity ratio":
    s = v_sky / v_circ = δμ × d / √(GM/r)

where:
    - δμ is the proper motion difference
    - d is the distance
    - r is the projected separation
    - M is the total mass

For bound Keplerian orbits, the maximum value of s depends on eccentricity
but is always bounded. In MOND/modified gravity, we expect enhanced s values.

The statistical test compares the distribution of s to expectations from:
1. Newtonian gravity
2. MOND
3. Z² topological inertia

Author: Z² Offensive Campaign
Date: 2026-05-24
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json

from astropy.table import Table
from scipy import stats

# =============================================================================
# PHYSICAL CONSTANTS
# =============================================================================

G_SI = 6.67430e-11          # m³/kg/s²
M_SUN_KG = 1.989e30         # kg
AU_M = 1.496e11             # m
PC_M = 3.086e16             # m

# Acceleration scales
A0_MOND = 1.2e-10           # m/s²
L_C_M = 20600 * 3.086e22    # Z² fundamental domain in m
C_MS = 299792458            # m/s
A_TOPO = C_MS**2 / L_C_M    # ~1.4e-10 m/s²

OUTPUT_DIR = Path(__file__).parent
DATA_DIR = OUTPUT_DIR / "data_cache"

print("="*70)
print("WORK-ORDER AA v2: WIDE BINARY GRAVITY TEST (CORRECTED)")
print("="*70)


# =============================================================================
# VELOCITY RATIO METHODOLOGY
# =============================================================================

def estimate_mass(G_abs, bp_rp):
    """Estimate stellar mass from absolute G magnitude."""
    valid = np.isfinite(G_abs) & np.isfinite(bp_rp) & (bp_rp < 5) & (G_abs < 15)
    mass = np.full_like(G_abs, 1.0)

    L_ratio = 10**((4.83 - G_abs[valid]) / 2.5)
    L_ratio = np.clip(L_ratio, 0.001, 100)

    mass[valid] = np.where(
        L_ratio > 0.5,
        L_ratio**0.29,
        0.23 * L_ratio**0.5
    )

    return np.clip(mass, 0.1, 3.0)


def compute_velocity_ratio(sample):
    """
    Compute the velocity ratio s = v_sky / v_circ for each binary.

    v_sky = tangential velocity from proper motion difference
    v_circ = √(GM/r) = Newtonian circular velocity

    For bound orbits, s has a predictable distribution.
    Modified gravity predicts higher s values.
    """
    print("\n" + "-"*60)
    print("COMPUTING VELOCITY RATIOS")
    print("-"*60)

    # Extract data
    plx1 = np.array(sample['parallax1'])
    plx2 = np.array(sample['parallax2'])
    plx = (plx1 + plx2) / 2  # mas

    # Distance in pc
    dist_pc = 1000 / plx

    # Projected separation in AU
    sep_au = np.array(sample['sep_AU'])

    # Separation in meters
    sep_m = sep_au * AU_M

    # Proper motion differences (mas/yr)
    delta_pmra = np.array(sample['pmra1']) - np.array(sample['pmra2'])
    delta_pmdec = np.array(sample['pmdec1']) - np.array(sample['pmdec2'])
    delta_pm = np.sqrt(delta_pmra**2 + delta_pmdec**2)

    # Sky velocity (km/s): v = 4.74 × d(pc) × pm(mas/yr)
    v_sky = 4.74 * dist_pc * delta_pm

    # Estimate masses
    G1 = np.array(sample['phot_g_mean_mag1'])
    G2 = np.array(sample['phot_g_mean_mag2'])
    bp_rp1 = np.array(sample['bp_rp1'])
    bp_rp2 = np.array(sample['bp_rp2'])

    G1_abs = G1 + 5 * np.log10(plx1/100)
    G2_abs = G2 + 5 * np.log10(plx2/100)

    mass1 = estimate_mass(G1_abs, bp_rp1)
    mass2 = estimate_mass(G2_abs, bp_rp2)
    mass_total = mass1 + mass2

    # Newtonian circular velocity (km/s)
    M_kg = mass_total * M_SUN_KG
    v_circ = np.sqrt(G_SI * M_kg / sep_m) / 1000  # km/s

    # Velocity ratio
    s = v_sky / v_circ

    # Newtonian acceleration
    a_newton = G_SI * M_kg / sep_m**2
    a_over_a0 = a_newton / A0_MOND

    print(f"Sample size: {len(s)}")
    print(f"v_sky range: {np.min(v_sky):.2f} - {np.max(v_sky):.2f} km/s")
    print(f"v_circ range: {np.min(v_circ):.3f} - {np.max(v_circ):.3f} km/s")
    print(f"Velocity ratio s: median = {np.median(s):.2f}, 90th = {np.percentile(s, 90):.2f}")

    return {
        'v_sky': v_sky,
        'v_circ': v_circ,
        's': s,
        'mass_total': mass_total,
        'sep_au': sep_au,
        'a_over_a0': a_over_a0
    }


def mond_boost_factor(a_over_a0):
    """
    MOND velocity boost: v_mond / v_newton = (μ)^(-1/2)
    where μ = x / √(1 + x²), x = a_N/a₀
    """
    mu = a_over_a0 / np.sqrt(1 + a_over_a0**2)
    return 1 / np.sqrt(mu)


def z2_boost_factor(a_over_a0):
    """
    Z² velocity boost from topological inertia.
    """
    a_over_aT = a_over_a0 * (A0_MOND / A_TOPO)
    f = np.where(a_over_aT > 0.01, 1 - np.exp(-1/a_over_aT), 1.0)
    enhancement = 1 + (13/6) * f
    return np.sqrt(enhancement)


def analyze_velocity_ratio_distribution(data):
    """
    Analyze the distribution of velocity ratios.

    Key insight: For BOUND orbits with random orientations, the velocity
    ratio s = v_sky / v_circ follows a predictable distribution with
    median ~0.7 and 90th percentile ~1.5 for Newtonian gravity.

    If we see systematically higher s values at low accelerations,
    this indicates modified gravity.
    """
    print("\n" + "-"*60)
    print("ANALYZING VELOCITY RATIO DISTRIBUTION")
    print("-"*60)

    s = data['s']
    a_over_a0 = data['a_over_a0']

    # Split into high-a and low-a regimes
    low_a_mask = a_over_a0 < 0.1
    mid_a_mask = (a_over_a0 >= 0.1) & (a_over_a0 < 1.0)
    high_a_mask = a_over_a0 >= 1.0

    print("\nVelocity ratio statistics by acceleration regime:")

    regimes = [
        ("Low-a (a/a₀ < 0.1)", low_a_mask),
        ("Mid-a (0.1 ≤ a/a₀ < 1)", mid_a_mask),
        ("High-a (a/a₀ ≥ 1)", high_a_mask)
    ]

    results = []
    for name, mask in regimes:
        if np.sum(mask) > 20:
            s_sub = s[mask]
            a_sub = a_over_a0[mask]

            # Expected MOND and Z² boosts
            mond_boost = mond_boost_factor(np.median(a_sub))
            z2_boost = z2_boost_factor(np.median(a_sub))

            median_s = np.median(s_sub)
            pct90 = np.percentile(s_sub, 90)

            print(f"\n  {name}:")
            print(f"    N = {np.sum(mask)}")
            print(f"    median(s) = {median_s:.2f}")
            print(f"    90th percentile = {pct90:.2f}")
            print(f"    Expected MOND boost: {mond_boost:.2f}")
            print(f"    Expected Z² boost: {z2_boost:.2f}")

            results.append({
                'regime': name,
                'n': int(np.sum(mask)),
                'median_a_over_a0': float(np.median(a_sub)),
                'median_s': float(median_s),
                'pct90_s': float(pct90),
                'expected_mond_boost': float(mond_boost),
                'expected_z2_boost': float(z2_boost)
            })

    # Key test: ratio of low-a to high-a velocity ratios
    if np.sum(low_a_mask) > 20 and np.sum(high_a_mask) > 20:
        s_low = np.median(s[low_a_mask])
        s_high = np.median(s[high_a_mask])
        ratio = s_low / s_high

        print(f"\n  CRITICAL TEST: s_low / s_high = {ratio:.3f}")
        print(f"    Expected (Newtonian): ~1.0")
        print(f"    Expected (MOND): ~1.5-2.0")
        print(f"    Expected (Z²): ~1.3-1.6")

    return results


def kolmogorov_smirnov_test(data):
    """
    KS test comparing low-a and high-a distributions.
    """
    print("\n" + "-"*60)
    print("KOLMOGOROV-SMIRNOV TEST")
    print("-"*60)

    s = data['s']
    a_over_a0 = data['a_over_a0']

    # Compare low-a and high-a distributions
    low_a = s[a_over_a0 < 0.1]
    high_a = s[a_over_a0 >= 1.0]

    if len(low_a) > 20 and len(high_a) > 20:
        ks_stat, p_value = stats.ks_2samp(low_a, high_a)

        print(f"\nComparing low-a vs high-a velocity ratio distributions:")
        print(f"  Low-a sample: N = {len(low_a)}")
        print(f"  High-a sample: N = {len(high_a)}")
        print(f"  KS statistic: {ks_stat:.4f}")
        print(f"  p-value: {p_value:.4e}")

        if p_value < 0.01:
            print(f"  → Distributions are SIGNIFICANTLY DIFFERENT (p < 0.01)")
        elif p_value < 0.05:
            print(f"  → Distributions are marginally different (p < 0.05)")
        else:
            print(f"  → Distributions are NOT significantly different")

        return {
            'ks_statistic': float(ks_stat),
            'p_value': float(p_value),
            'n_low': int(len(low_a)),
            'n_high': int(len(high_a))
        }

    return None


def main():
    """Execute corrected wide binary gravity test."""

    # Load catalog
    print("\n" + "-"*60)
    print("LOADING DATA")
    print("-"*60)

    catalog_path = DATA_DIR / "el_badry_wide_binaries.fits.gz"
    if not catalog_path.exists():
        print(f"ERROR: Catalog not found at {catalog_path}")
        return None

    t = Table.read(catalog_path)
    print(f"Loaded {len(t):,} pairs")

    # Selection criteria
    sep = np.array(t['sep_AU'])
    r_chance = np.array(t['R_chance_align'])
    plx1 = np.array(t['parallax1'])
    plx2 = np.array(t['parallax2'])

    # Select wide, clean, nearby binaries
    mask = (
        (sep >= 5000) &
        (sep <= 30000) &  # Tighter range to focus on MOND regime
        (r_chance < 0.001) &  # Very high purity
        (plx1 > 10) &  # Nearby (< 100 pc)
        (plx2 > 10) &
        np.isfinite(t['pmra1']) &
        np.isfinite(t['pmra2']) &
        np.isfinite(t['pmdec1']) &
        np.isfinite(t['pmdec2'])
    )

    sample = t[mask]
    print(f"\nSelected {len(sample):,} high-purity wide binaries")
    print(f"  Separation: 5000-30000 AU")
    print(f"  Chance alignment: < 0.1%")
    print(f"  Distance: < 100 pc")

    if len(sample) < 100:
        print("ERROR: Insufficient sample")
        return None

    # Compute velocity ratios
    data = compute_velocity_ratio(sample)

    # Analyze distribution
    regime_results = analyze_velocity_ratio_distribution(data)

    # KS test
    ks_results = kolmogorov_smirnov_test(data)

    # Final verdict
    print("\n" + "="*70)
    print("WORK-ORDER AA v2: FINAL ASSESSMENT")
    print("="*70)

    s = data['s']
    a_over_a0 = data['a_over_a0']

    low_a_s = np.median(s[a_over_a0 < 0.1]) if np.sum(a_over_a0 < 0.1) > 10 else np.nan
    high_a_s = np.median(s[a_over_a0 >= 1.0]) if np.sum(a_over_a0 >= 1.0) > 10 else np.nan

    if np.isfinite(low_a_s) and np.isfinite(high_a_s):
        ratio = low_a_s / high_a_s

        if ratio > 1.4:
            verdict = "STRONG EVIDENCE for modified gravity in low-acceleration regime"
            model = "MOND/Z²"
        elif ratio > 1.2:
            verdict = "MARGINAL EVIDENCE for velocity enhancement at low acceleration"
            model = "INCONCLUSIVE"
        else:
            verdict = "NO SIGNIFICANT low-acceleration anomaly detected"
            model = "NEWTON"
    else:
        verdict = "INSUFFICIENT DATA for low-a vs high-a comparison"
        model = "INCONCLUSIVE"
        ratio = np.nan

    # Save results
    results = {
        'work_order': 'AA_v2',
        'task': 'Gaia Wide Binary Gravity Test (Corrected Methodology)',
        'date': datetime.now().isoformat(),
        'catalog': 'El-Badry et al. (2021) Gaia eDR3',
        'selection': {
            'n_binaries': len(sample),
            'sep_range_au': [5000, 30000],
            'chance_align_max': 0.001,
            'max_distance_pc': 100
        },
        'velocity_ratio_stats': {
            'overall_median': float(np.median(s)),
            'overall_90th': float(np.percentile(s, 90)),
            'low_a_median': float(low_a_s) if np.isfinite(low_a_s) else None,
            'high_a_median': float(high_a_s) if np.isfinite(high_a_s) else None,
            'low_high_ratio': float(ratio) if np.isfinite(ratio) else None
        },
        'regime_results': regime_results,
        'ks_test': ks_results,
        'favored_model': model,
        'verdict': verdict
    }

    output_file = OUTPUT_DIR / 'WORK_ORDER_AA_v2_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_file}")

    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│            WORK-ORDER AA v2: WIDE BINARY GRAVITY TEST                 │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  High-purity sample: {len(sample):>6,} binaries                              │
│                                                                       │
│  VELOCITY RATIO (s = v_sky / v_circ):                                 │
│    Overall median:    {np.median(s):>8.2f}                                    │
│    Low-a median:      {low_a_s:>8.2f}                                    │
│    High-a median:     {high_a_s:>8.2f}                                    │
│    Ratio (low/high):  {ratio:>8.3f}                                    │
│                                                                       │
│  VERDICT: {verdict:<58} │
│  FAVORED MODEL: {model:<51} │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
""")

    return results


if __name__ == "__main__":
    main()
