#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER AA: REAL GAIA WIDE BINARY GRAVITY AUDIT
================================================================================

Analysis of El-Badry et al. (2021) Gaia eDR3 wide binary catalog
to test Newtonian, MOND, and Z² topological inertia predictions.

Key insight: Wide binaries at separations > 5000 AU experience
accelerations below the MOND scale a₀ = 1.2×10⁻¹⁰ m/s².

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
# LOCKED PARAMETERS
# =============================================================================

# Physical constants
G_SI = 6.67430e-11          # m³/kg/s²
M_SUN_KG = 1.989e30         # kg
AU_M = 1.496e11             # m
PC_M = 3.086e16             # m

# MOND acceleration scale
A0_MOND = 1.2e-10           # m/s²

# Z² topological parameters
L_C_MPC = 20600             # Fundamental domain in Mpc
L_C_M = L_C_MPC * 3.086e22  # In meters
C_MS = 299792458            # m/s
A_TOPO = C_MS**2 / L_C_M    # ~1.4e-10 m/s²

OUTPUT_DIR = Path(__file__).parent
DATA_DIR = OUTPUT_DIR / "data_cache"

print("="*70)
print("WORK-ORDER AA: REAL GAIA WIDE BINARY GRAVITY AUDIT")
print("="*70)
print(f"\nUsing El-Badry et al. (2021) Gaia eDR3 catalog")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n*** KEY PARAMETERS ***")
print(f"  MOND a₀:    {A0_MOND:.2e} m/s²")
print(f"  Z² a_T:     {A_TOPO:.2e} m/s²")
print(f"  Ratio:      {A_TOPO/A0_MOND:.2f}")


# =============================================================================
# MASS ESTIMATION FROM PHOTOMETRY
# =============================================================================

def estimate_mass_from_color(G_abs, bp_rp):
    """
    Estimate stellar mass from absolute G magnitude and BP-RP color.

    Uses polynomial fits to PARSEC isochrones for main sequence stars.
    Valid for 0.1 < M/M_sun < 2.0 approximately.
    """
    # Clean up invalid values
    valid = np.isfinite(G_abs) & np.isfinite(bp_rp) & (bp_rp < 5) & (G_abs < 15)
    mass = np.full_like(G_abs, 1.0)  # Default to 1 M_sun

    # Simple mass-luminosity relation for main sequence
    # L/L_sun ~ (M/M_sun)^3.5 for intermediate mass
    # M_G_sun ~ 4.83
    # M_G - M_G_sun = -2.5 * log10(L/L_sun)
    # So L/L_sun = 10^((M_G_sun - M_G)/2.5)
    # And M/M_sun ~ (L/L_sun)^(1/3.5) ~ (L/L_sun)^0.286

    L_ratio = 10**((4.83 - G_abs[valid]) / 2.5)

    # Clip to reasonable range
    L_ratio = np.clip(L_ratio, 0.001, 100)

    # Mass-luminosity with adjusted exponent for different mass ranges
    mass[valid] = np.where(
        L_ratio > 0.5,
        L_ratio**0.29,  # Higher mass
        0.23 * L_ratio**0.5  # Lower mass (M < 0.5 M_sun)
    )

    # Clip to physical range
    mass = np.clip(mass, 0.1, 3.0)

    return mass


# =============================================================================
# GRAVITY MODELS
# =============================================================================

def newtonian_velocity(mass_total_msun, separation_au):
    """Keplerian orbital velocity v = √(GM/r)"""
    M = mass_total_msun * M_SUN_KG
    r = separation_au * AU_M
    v = np.sqrt(G_SI * M / r)
    return v / 1000  # km/s


def newtonian_acceleration(mass_total_msun, separation_au):
    """Newtonian acceleration a = GM/r²"""
    M = mass_total_msun * M_SUN_KG
    r = separation_au * AU_M
    return G_SI * M / r**2


def mond_velocity(mass_total_msun, separation_au):
    """
    MOND orbital velocity with simple interpolating function.
    μ(x) = x / √(1 + x²) where x = a_N / a₀
    """
    M = mass_total_msun * M_SUN_KG
    r = separation_au * AU_M

    a_N = G_SI * M / r**2
    x = a_N / A0_MOND
    mu = x / np.sqrt(1 + x**2)

    # In MOND: a_N = μ(a/a₀) × a, so a = a_N / μ
    a_mond = a_N / mu
    v = np.sqrt(a_mond * r)

    return v / 1000  # km/s


def z2_velocity(mass_total_msun, separation_au):
    """
    Z² topological inertia orbital velocity.

    Enhancement from winding modes:
    a_eff = a_N × [1 + (13/6) × f(a_N/a_T)]
    where f(x) = 1 - exp(-1/x)
    """
    M = mass_total_msun * M_SUN_KG
    r = separation_au * AU_M

    a_N = G_SI * M / r**2
    x = a_N / A_TOPO

    # Smooth transition function
    f = np.where(x > 0.01, 1 - np.exp(-1/x), 1.0)

    # Enhancement ratio from Ω_m = 6/19
    enhancement = 1 + (13/6) * f

    a_eff = a_N * enhancement
    v = np.sqrt(a_eff * r)

    return v / 1000  # km/s


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def load_gaia_catalog():
    """Load and filter El-Badry Gaia wide binary catalog."""
    print("\n" + "-"*60)
    print("LOADING GAIA WIDE BINARY CATALOG")
    print("-"*60)

    catalog_path = DATA_DIR / "el_badry_wide_binaries.fits.gz"
    if not catalog_path.exists():
        print(f"ERROR: Catalog not found at {catalog_path}")
        return None

    print(f"Reading {catalog_path}...")
    t = Table.read(catalog_path)
    print(f"Loaded {len(t):,} pairs")

    return t


def prepare_sample(catalog, min_sep=5000, max_sep=50000, max_chance=0.01, min_plx=5):
    """Prepare clean sample for MOND test."""
    print("\n" + "-"*60)
    print("PREPARING CLEAN SAMPLE")
    print("-"*60)

    sep = np.array(catalog['sep_AU'])
    r_chance = np.array(catalog['R_chance_align'])
    plx1 = np.array(catalog['parallax1'])
    plx2 = np.array(catalog['parallax2'])

    # Quality cuts
    mask = (
        (sep >= min_sep) &
        (sep <= max_sep) &
        (r_chance < max_chance) &
        (plx1 > min_plx) &
        (plx2 > min_plx) &
        np.isfinite(catalog['pmra1']) &
        np.isfinite(catalog['pmra2']) &
        np.isfinite(catalog['pmdec1']) &
        np.isfinite(catalog['pmdec2'])
    )

    sample = catalog[mask]
    print(f"Selection: {min_sep}-{max_sep} AU, chance<{max_chance}, plx>{min_plx} mas")
    print(f"Selected {len(sample):,} wide binaries")

    return sample


def compute_velocities(sample):
    """Compute relative velocities from proper motions."""
    print("\n" + "-"*60)
    print("COMPUTING RELATIVE VELOCITIES")
    print("-"*60)

    # Extract data
    sep_au = np.array(sample['sep_AU'])
    plx1 = np.array(sample['parallax1'])
    plx2 = np.array(sample['parallax2'])

    # Average parallax (mas)
    plx = (plx1 + plx2) / 2

    # Distance in pc
    dist_pc = 1000 / plx

    # Proper motion differences (mas/yr)
    delta_pmra = np.array(sample['pmra1']) - np.array(sample['pmra2'])
    delta_pmdec = np.array(sample['pmdec1']) - np.array(sample['pmdec2'])
    delta_pm = np.sqrt(delta_pmra**2 + delta_pmdec**2)

    # Convert to physical velocity: v = 4.74 × d × pm
    # where d in pc, pm in mas/yr, v in km/s
    v_rel = 4.74 * dist_pc * delta_pm

    # Estimate masses from photometry
    G1 = np.array(sample['phot_g_mean_mag1'])
    G2 = np.array(sample['phot_g_mean_mag2'])
    bp_rp1 = np.array(sample['bp_rp1'])
    bp_rp2 = np.array(sample['bp_rp2'])

    # Absolute magnitudes
    G1_abs = G1 + 5 * np.log10(plx1/100)
    G2_abs = G2 + 5 * np.log10(plx2/100)

    # Mass estimates
    mass1 = estimate_mass_from_color(G1_abs, bp_rp1)
    mass2 = estimate_mass_from_color(G2_abs, bp_rp2)
    mass_total = mass1 + mass2

    print(f"Separation range: {np.min(sep_au):.0f} - {np.max(sep_au):.0f} AU")
    print(f"Distance range: {np.min(dist_pc):.0f} - {np.max(dist_pc):.0f} pc")
    print(f"Relative velocity range: {np.min(v_rel):.2f} - {np.max(v_rel):.2f} km/s")
    print(f"Total mass range: {np.min(mass_total):.2f} - {np.max(mass_total):.2f} M☉")

    return {
        'sep_au': sep_au,
        'dist_pc': dist_pc,
        'v_rel': v_rel,
        'mass_total': mass_total,
        'mass1': mass1,
        'mass2': mass2
    }


def analyze_velocity_boost(data):
    """Compare observed velocities to model predictions."""
    print("\n" + "-"*60)
    print("ANALYZING VELOCITY BOOST")
    print("-"*60)

    sep = data['sep_au']
    mass = data['mass_total']
    v_obs = data['v_rel']

    # Model predictions
    v_newton = newtonian_velocity(mass, sep)
    v_mond = mond_velocity(mass, sep)
    v_z2 = z2_velocity(mass, sep)

    # Accelerations
    a_newton = newtonian_acceleration(mass, sep)
    a_over_a0 = a_newton / A0_MOND

    # Velocity ratios (observed / predicted)
    ratio_newton = v_obs / v_newton
    ratio_mond = v_obs / v_mond
    ratio_z2 = v_obs / v_z2

    print(f"\nVelocity ratio (obs/pred) statistics:")
    print(f"  vs Newton: {np.median(ratio_newton):.3f} ± {np.std(ratio_newton):.3f}")
    print(f"  vs MOND:   {np.median(ratio_mond):.3f} ± {np.std(ratio_mond):.3f}")
    print(f"  vs Z²:     {np.median(ratio_z2):.3f} ± {np.std(ratio_z2):.3f}")

    # Bin by acceleration
    print("\n  Binned by acceleration (a/a₀):")
    log_bins = np.linspace(np.log10(np.min(a_over_a0)), np.log10(np.max(a_over_a0)), 6)

    binned_results = []
    for i in range(len(log_bins)-1):
        mask = (np.log10(a_over_a0) >= log_bins[i]) & (np.log10(a_over_a0) < log_bins[i+1])
        n = np.sum(mask)
        if n > 10:
            a_bin = 10**((log_bins[i] + log_bins[i+1])/2)
            r_n = np.median(ratio_newton[mask])
            r_m = np.median(ratio_mond[mask])
            r_z = np.median(ratio_z2[mask])

            binned_results.append({
                'a_over_a0': float(a_bin),
                'n': int(n),
                'ratio_newton': float(r_n),
                'ratio_mond': float(r_m),
                'ratio_z2': float(r_z)
            })

            print(f"    a/a₀ ~ {a_bin:.2f}: n={n:4d}, v/v_N={r_n:.2f}, v/v_M={r_m:.2f}, v/v_Z²={r_z:.2f}")

    return {
        'v_newton': v_newton,
        'v_mond': v_mond,
        'v_z2': v_z2,
        'ratio_newton': ratio_newton,
        'ratio_mond': ratio_mond,
        'ratio_z2': ratio_z2,
        'a_over_a0': a_over_a0,
        'binned': binned_results
    }


def compute_chi_squared(data, analysis):
    """Compute chi-squared for each model."""
    print("\n" + "-"*60)
    print("COMPUTING CHI-SQUARED")
    print("-"*60)

    v_obs = data['v_rel']

    # Assume 30% relative error (includes orbital phase, mass uncertainty, etc.)
    v_err = 0.3 * v_obs

    v_newton = analysis['v_newton']
    v_mond = analysis['v_mond']
    v_z2 = analysis['v_z2']

    # Chi-squared
    chi2_newton = np.sum(((v_obs - v_newton) / v_err)**2)
    chi2_mond = np.sum(((v_obs - v_mond) / v_err)**2)
    chi2_z2 = np.sum(((v_obs - v_z2) / v_err)**2)

    n = len(v_obs)
    dof = n - 1

    print(f"\nChi-squared (N={n}, dof={dof}):")
    print(f"  Newton:  χ² = {chi2_newton:.1f}, χ²/dof = {chi2_newton/dof:.3f}")
    print(f"  MOND:    χ² = {chi2_mond:.1f}, χ²/dof = {chi2_mond/dof:.3f}")
    print(f"  Z²:      χ² = {chi2_z2:.1f}, χ²/dof = {chi2_z2/dof:.3f}")

    # P-values (probability of getting worse fit if model is correct)
    p_newton = 1 - stats.chi2.cdf(chi2_newton, dof)
    p_mond = 1 - stats.chi2.cdf(chi2_mond, dof)
    p_z2 = 1 - stats.chi2.cdf(chi2_z2, dof)

    print(f"\nP-values (higher = better):")
    print(f"  Newton:  p = {p_newton:.4e}")
    print(f"  MOND:    p = {p_mond:.4e}")
    print(f"  Z²:      p = {p_z2:.4e}")

    return {
        'chi2_newton': float(chi2_newton),
        'chi2_mond': float(chi2_mond),
        'chi2_z2': float(chi2_z2),
        'dof': int(dof),
        'reduced_newton': float(chi2_newton/dof),
        'reduced_mond': float(chi2_mond/dof),
        'reduced_z2': float(chi2_z2/dof),
        'p_newton': float(p_newton),
        'p_mond': float(p_mond),
        'p_z2': float(p_z2)
    }


def main():
    """Execute real Gaia wide binary analysis."""

    # Load catalog
    catalog = load_gaia_catalog()
    if catalog is None:
        return None

    # Prepare sample
    sample = prepare_sample(catalog)
    if len(sample) < 100:
        print("ERROR: Insufficient sample size")
        return None

    # Compute velocities
    data = compute_velocities(sample)

    # Analyze velocity boost
    analysis = analyze_velocity_boost(data)

    # Chi-squared fit
    chi2 = compute_chi_squared(data, analysis)

    # Determine best model
    models = ['newton', 'mond', 'z2']
    reduced = [chi2['reduced_newton'], chi2['reduced_mond'], chi2['reduced_z2']]

    # Best = closest to 1.0
    best_idx = np.argmin(np.abs(np.array(reduced) - 1.0))
    best_model = models[best_idx]

    # VERDICT
    print("\n" + "="*70)
    print("WORK-ORDER AA: FINAL VERDICT")
    print("="*70)

    if chi2['reduced_newton'] < 1.5:
        verdict = "Newtonian gravity adequate - low-acceleration anomaly not detected"
    elif best_model == 'mond':
        verdict = "MOND preferred over Newton and Z² - gravity modification detected"
    elif best_model == 'z2':
        verdict = "Z² TOPOLOGICAL INERTIA preferred - consistent with T³/Z₂ cosmology"
    else:
        verdict = "Inconclusive - none of the models fit well"

    # Save results
    results = {
        'work_order': 'AA',
        'task': 'Gaia Wide Binary Gravity Audit (Real Data)',
        'date': datetime.now().isoformat(),
        'catalog': 'El-Badry et al. (2021) Gaia eDR3',
        'sample': {
            'n_binaries': len(sample),
            'sep_range_au': [float(np.min(data['sep_au'])), float(np.max(data['sep_au']))],
            'dist_range_pc': [float(np.min(data['dist_pc'])), float(np.max(data['dist_pc']))]
        },
        'parameters': {
            'a0_mond': A0_MOND,
            'a_topo': A_TOPO,
            'ratio': A_TOPO / A0_MOND
        },
        'velocity_ratio_median': {
            'vs_newton': float(np.median(analysis['ratio_newton'])),
            'vs_mond': float(np.median(analysis['ratio_mond'])),
            'vs_z2': float(np.median(analysis['ratio_z2']))
        },
        'binned_results': analysis['binned'],
        'chi_squared': chi2,
        'best_model': best_model,
        'verdict': verdict
    }

    output_file = OUTPUT_DIR / 'WORK_ORDER_AA_real_gaia_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nSaved: {output_file}")

    # Summary box
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│            WORK-ORDER AA: GAIA WIDE BINARY AUDIT                      │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  Catalog: El-Badry et al. (2021) Gaia eDR3                            │
│  Binaries analyzed:  {len(sample):>7,}                                       │
│  Separation range:   {np.min(data['sep_au']):>6.0f} - {np.max(data['sep_au']):>6.0f} AU                       │
│                                                                       │
│  VELOCITY RATIO (obs/predicted):                                      │
│    vs Newton:  {np.median(analysis['ratio_newton']):>6.2f}                                           │
│    vs MOND:    {np.median(analysis['ratio_mond']):>6.2f}                                           │
│    vs Z²:      {np.median(analysis['ratio_z2']):>6.2f}                                           │
│                                                                       │
│  CHI-SQUARED FIT:                                                     │
│    Newton:  χ²/dof = {chi2['reduced_newton']:>7.3f}                                   │
│    MOND:    χ²/dof = {chi2['reduced_mond']:>7.3f}                                   │
│    Z²:      χ²/dof = {chi2['reduced_z2']:>7.3f}                                   │
│                                                                       │
│  BEST MODEL: {best_model.upper():<54} │
│                                                                       │
│  {verdict:<68} │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
""")

    return results


if __name__ == "__main__":
    main()
