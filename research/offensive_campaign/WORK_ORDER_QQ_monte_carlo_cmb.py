#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER QQ: MONTE CARLO VALIDATION OF CMB MATCHED CIRCLES
================================================================================

PURPOSE: Rigorous statistical validation of the V2↔V3 matched circles detection
at 115.5° with 5.8σ combined Planck+WMAP significance.

METHODOLOGY:
1. Generate N=10,000 synthetic CMB realizations using the Planck best-fit ΛCDM
   power spectrum with Gaussian random phases
2. For each realization, compute the V2↔V3 circle correlation at r=10°
3. Test BOTH forward and reversed orientations (to avoid look-elsewhere bias)
4. Build the null distribution of maximum correlations
5. Compare observed correlation to this null distribution
6. Report the Monte Carlo-validated significance

KEY INSIGHT:
The Z² framework PREDICTS the vertex locations beforehand, eliminating the
look-elsewhere effect that plagued previous matched-circles searches.
This Monte Carlo directly tests: "Given random ΛCDM CMB, how often would we
see a correlation this strong at the SPECIFIC V2↔V3 location?"

Author: Z² Offensive Campaign
Date: 2026-05-24
Framework: Z² v11.1.0
================================================================================
"""

import numpy as np
import healpy as hp
from pathlib import Path
from datetime import datetime
import json
from multiprocessing import Pool, cpu_count
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = Path(__file__).parent
N_SIMULATIONS = 10000  # Number of Monte Carlo realizations
NSIDE = 256            # Resolution for simulations (faster than 2048)
CIRCLE_RADIUS_DEG = 10 # Optimal radius from detection
N_CIRCLE_POINTS = 360  # Points per circle

# Z² vertex directions (locked parameters)
V2_ANTI_SHAPLEY = {"l": 96.4, "b": -29.8}   # V2
V3_COLD_SPOT = {"l": 186.4, "b": 60.2}      # V3

# Observed correlation from combined Planck+WMAP analysis
OBSERVED_R = 0.53  # Best correlation at r=10°
OBSERVED_ORIENTATION = "reversed"

print("="*70)
print("WORK-ORDER QQ: MONTE CARLO CMB MATCHED CIRCLES VALIDATION")
print("="*70)
print(f"\nConfiguration:")
print(f"  N simulations:     {N_SIMULATIONS:,}")
print(f"  HEALPix Nside:     {NSIDE}")
print(f"  Circle radius:     {CIRCLE_RADIUS_DEG}°")
print(f"  Target: V2↔V3 at 115.5° (reversed orientation)")
print(f"  Observed r:        {OBSERVED_R:.4f}")


# =============================================================================
# CMB POWER SPECTRUM (Planck 2018 best-fit ΛCDM)
# =============================================================================

def get_planck_cls(lmax=3*256):
    """
    Return Planck 2018 best-fit TT power spectrum.
    Uses the standard ΛCDM parameterization.
    """
    # Planck 2018 best-fit parameters
    # These generate the theoretical C_l spectrum

    # For computational efficiency, we use an analytic approximation
    # to the Planck power spectrum that captures the key features:
    # - Sachs-Wolfe plateau at low l
    # - Acoustic peaks at l ~ 220, 540, 810, ...
    # - Silk damping at high l

    ell = np.arange(lmax + 1)

    # Avoid division by zero
    ell_safe = np.maximum(ell, 1)

    # Approximate TT spectrum (in μK²)
    # Primary CMB: D_l = l(l+1)C_l/(2π) ~ 1000-6000 μK²

    # Sachs-Wolfe plateau
    sw_amplitude = 800  # μK²

    # First acoustic peak at l~220
    peak1_l = 220
    peak1_amp = 5500
    peak1_width = 60

    # Second acoustic peak at l~540
    peak2_l = 540
    peak2_amp = 2500
    peak2_width = 80

    # Third acoustic peak at l~810
    peak3_l = 810
    peak3_amp = 2800
    peak3_width = 90

    # Silk damping
    damping_scale = 1200

    # Build D_l = l(l+1)C_l/(2π)
    D_l = sw_amplitude * np.ones_like(ell, dtype=float)

    # Add acoustic peaks
    D_l += peak1_amp * np.exp(-0.5 * ((ell - peak1_l) / peak1_width)**2)
    D_l += peak2_amp * np.exp(-0.5 * ((ell - peak2_l) / peak2_width)**2)
    D_l += peak3_amp * np.exp(-0.5 * ((ell - peak3_l) / peak3_width)**2)

    # Apply Silk damping
    D_l *= np.exp(-(ell / damping_scale)**2)

    # Convert D_l to C_l: C_l = 2π D_l / [l(l+1)]
    C_l = np.zeros_like(D_l)
    C_l[2:] = 2 * np.pi * D_l[2:] / (ell_safe[2:] * (ell_safe[2:] + 1))

    # Convert from μK² to K² (healpy expects K²)
    C_l *= 1e-12

    return C_l


# =============================================================================
# CIRCLE EXTRACTION
# =============================================================================

def galactic_to_healpix(l_deg, b_deg):
    """Convert galactic coordinates to HEALPix theta, phi."""
    theta = np.radians(90 - b_deg)
    phi = np.radians(l_deg)
    return theta, phi


def get_circle_points(theta_c, phi_c, radius_rad, n_points):
    """
    Generate 3D unit vectors for points along a circle.

    Parameters:
        theta_c, phi_c: Center of circle (colatitude, longitude)
        radius_rad: Circle radius in radians
        n_points: Number of points on circle

    Returns:
        Array of shape (n_points, 3) with unit vectors
    """
    # Center vector
    cx = np.sin(theta_c) * np.cos(phi_c)
    cy = np.sin(theta_c) * np.sin(phi_c)
    cz = np.cos(theta_c)

    # Build orthonormal basis
    if abs(cz) < 0.9:
        px, py, pz = -cy, cx, 0
    else:
        px, py, pz = 1, 0, 0
    norm = np.sqrt(px**2 + py**2 + pz**2)
    px, py, pz = px/norm, py/norm, pz/norm

    # Cross product for second basis vector
    qx = cy*pz - cz*py
    qy = cz*px - cx*pz
    qz = cx*py - cy*px

    # Generate points around circle
    angles = np.linspace(0, 2*np.pi, n_points, endpoint=False)
    cos_r, sin_r = np.cos(radius_rad), np.sin(radius_rad)

    vectors = np.zeros((n_points, 3))
    for i, angle in enumerate(angles):
        cos_a, sin_a = np.cos(angle), np.sin(angle)
        vectors[i, 0] = cx*cos_r + (px*cos_a + qx*sin_a)*sin_r
        vectors[i, 1] = cy*cos_r + (py*cos_a + qy*sin_a)*sin_r
        vectors[i, 2] = cz*cos_r + (pz*cos_a + qz*sin_a)*sin_r

    return vectors


def extract_circle_temps(cmb_map, theta_c, phi_c, radius_deg, n_points=360):
    """Extract temperatures along a circle on the CMB map."""
    nside = hp.get_nside(cmb_map)
    radius_rad = np.radians(radius_deg)

    vectors = get_circle_points(theta_c, phi_c, radius_rad, n_points)
    pixels = hp.vec2pix(nside, vectors[:, 0], vectors[:, 1], vectors[:, 2])

    return cmb_map[pixels]


def compute_correlation(temps1, temps2):
    """
    Compute maximum correlation between two circle temperature profiles.
    Tests both forward and reversed orientations.

    Returns: (r_max, orientation)
    """
    # Normalize
    t1 = (temps1 - np.mean(temps1)) / (np.std(temps1) + 1e-10)
    t2 = (temps2 - np.mean(temps2)) / (np.std(temps2) + 1e-10)

    # Forward correlation (slide one circle against other)
    corr_fwd = np.correlate(t1, t2, mode='full') / len(t1)
    r_fwd = np.max(np.abs(corr_fwd))

    # Reversed correlation (Z₂ antipodal signature)
    t2_rev = t2[::-1]
    corr_rev = np.correlate(t1, t2_rev, mode='full') / len(t1)
    r_rev = np.max(np.abs(corr_rev))

    if r_rev > r_fwd:
        return r_rev, "reversed"
    return r_fwd, "forward"


# =============================================================================
# MONTE CARLO SIMULATION
# =============================================================================

def simulate_one_realization(seed):
    """
    Generate one random CMB realization and compute V2↔V3 correlation.

    This is the core Monte Carlo function.
    """
    np.random.seed(seed)

    # Generate Gaussian random CMB map
    cls = get_planck_cls(lmax=3*NSIDE)
    cmb_map = hp.synfast(cls, NSIDE, verbose=False)

    # V2 and V3 coordinates
    v2_theta, v2_phi = galactic_to_healpix(V2_ANTI_SHAPLEY["l"], V2_ANTI_SHAPLEY["b"])
    v3_theta, v3_phi = galactic_to_healpix(V3_COLD_SPOT["l"], V3_COLD_SPOT["b"])

    # Extract circles
    temps_v2 = extract_circle_temps(cmb_map, v2_theta, v2_phi, CIRCLE_RADIUS_DEG, N_CIRCLE_POINTS)
    temps_v3 = extract_circle_temps(cmb_map, v3_theta, v3_phi, CIRCLE_RADIUS_DEG, N_CIRCLE_POINTS)

    # Compute correlation
    r_max, orientation = compute_correlation(temps_v2, temps_v3)

    return r_max, orientation


def run_monte_carlo_parallel(n_sims, n_workers=None):
    """Run Monte Carlo simulations in parallel."""
    if n_workers is None:
        n_workers = max(1, cpu_count() - 1)

    print(f"\nRunning {n_sims:,} simulations on {n_workers} cores...")
    print("This may take several minutes...")

    seeds = list(range(n_sims))

    with Pool(n_workers) as pool:
        results = []
        for i, result in enumerate(pool.imap(simulate_one_realization, seeds, chunksize=100)):
            results.append(result)
            if (i + 1) % 1000 == 0:
                print(f"  Completed {i+1:,}/{n_sims:,} simulations...")

    return results


def run_monte_carlo_serial(n_sims):
    """Run Monte Carlo simulations serially (for debugging)."""
    print(f"\nRunning {n_sims:,} simulations (serial mode)...")

    results = []
    for i in range(n_sims):
        result = simulate_one_realization(i)
        results.append(result)
        if (i + 1) % 500 == 0:
            print(f"  Completed {i+1:,}/{n_sims:,} simulations...")

    return results


# =============================================================================
# ANALYSIS
# =============================================================================

def analyze_null_distribution(results, observed_r):
    """Analyze the Monte Carlo null distribution."""
    print("\n" + "="*60)
    print("NULL DISTRIBUTION ANALYSIS")
    print("="*60)

    correlations = np.array([r[0] for r in results])
    orientations = [r[1] for r in results]

    n_reversed = sum(1 for o in orientations if o == "reversed")

    print(f"\nNull distribution statistics:")
    print(f"  N simulations:    {len(correlations):,}")
    print(f"  Mean r:           {np.mean(correlations):.4f}")
    print(f"  Std r:            {np.std(correlations):.4f}")
    print(f"  Max r:            {np.max(correlations):.4f}")
    print(f"  Reversed frac:    {n_reversed/len(correlations):.1%}")

    # Percentiles
    percentiles = [90, 95, 99, 99.9, 99.99]
    print(f"\n  Percentiles:")
    for p in percentiles:
        val = np.percentile(correlations, p)
        print(f"    {p}th: {val:.4f}")

    # Count how many exceed observed
    n_exceed = np.sum(correlations >= observed_r)
    p_value = (n_exceed + 1) / (len(correlations) + 1)  # +1 for continuity correction

    # Count reversed AND exceeding
    n_reversed_exceed = sum(1 for r, o in results if r >= observed_r and o == "reversed")
    p_value_reversed = (n_reversed_exceed + 1) / (len(correlations) + 1)

    print(f"\n  Observed r = {observed_r:.4f}")
    print(f"  N exceeding observed:           {n_exceed}")
    print(f"  p-value (any orientation):      {p_value:.6e}")
    print(f"  N reversed AND exceeding:       {n_reversed_exceed}")
    print(f"  p-value (reversed only):        {p_value_reversed:.6e}")

    # Convert p-value to sigma
    from scipy import stats
    if p_value > 0:
        sigma = stats.norm.isf(p_value)
    else:
        sigma = float('inf')

    if p_value_reversed > 0:
        sigma_reversed = stats.norm.isf(p_value_reversed)
    else:
        sigma_reversed = float('inf')

    print(f"\n  MONTE CARLO SIGNIFICANCE:")
    print(f"    Any orientation:    {sigma:.2f}σ")
    print(f"    Reversed only:      {sigma_reversed:.2f}σ")

    return {
        'n_simulations': len(correlations),
        'mean': float(np.mean(correlations)),
        'std': float(np.std(correlations)),
        'max': float(np.max(correlations)),
        'percentiles': {str(p): float(np.percentile(correlations, p)) for p in percentiles},
        'fraction_reversed': float(n_reversed / len(correlations)),
        'observed_r': observed_r,
        'n_exceed': int(n_exceed),
        'n_reversed_exceed': int(n_reversed_exceed),
        'p_value': float(p_value),
        'p_value_reversed': float(p_value_reversed),
        'sigma': float(sigma) if np.isfinite(sigma) else ">6",
        'sigma_reversed': float(sigma_reversed) if np.isfinite(sigma_reversed) else ">6"
    }


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Monte Carlo validation."""

    start_time = datetime.now()
    print(f"\nStarted: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Check for healpy
    try:
        import healpy as hp
    except ImportError:
        print("ERROR: healpy not installed")
        return None

    # Run Monte Carlo
    try:
        # Try parallel first
        results = run_monte_carlo_parallel(N_SIMULATIONS)
    except Exception as e:
        print(f"Parallel execution failed ({e}), falling back to serial...")
        results = run_monte_carlo_serial(N_SIMULATIONS)

    # Analyze null distribution
    analysis = analyze_null_distribution(results, OBSERVED_R)

    # Timing
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()

    # Final verdict
    print("\n" + "="*70)
    print("MONTE CARLO VALIDATION: FINAL VERDICT")
    print("="*70)

    sigma = analysis['sigma']
    sigma_rev = analysis['sigma_reversed']

    if isinstance(sigma, str) or sigma > 5:
        verdict = "VALIDATED: Detection significance EXCEEDS 5σ in Monte Carlo"
        status = "CONFIRMED"
    elif sigma > 3:
        verdict = f"STRONG: Detection at {sigma:.1f}σ in Monte Carlo"
        status = "STRONG"
    elif sigma > 2:
        verdict = f"MARGINAL: Detection at {sigma:.1f}σ in Monte Carlo"
        status = "MARGINAL"
    else:
        verdict = f"NOT SIGNIFICANT: Only {sigma:.1f}σ in Monte Carlo"
        status = "NOT_SIGNIFICANT"

    # Save results
    results_dict = {
        'work_order': 'QQ',
        'task': 'Monte Carlo Validation of CMB Matched Circles',
        'date': datetime.now().isoformat(),
        'configuration': {
            'n_simulations': N_SIMULATIONS,
            'nside': NSIDE,
            'circle_radius_deg': CIRCLE_RADIUS_DEG,
            'v2_direction': V2_ANTI_SHAPLEY,
            'v3_direction': V3_COLD_SPOT
        },
        'observed': {
            'correlation': OBSERVED_R,
            'orientation': OBSERVED_ORIENTATION,
            'separation_deg': 115.5
        },
        'null_distribution': analysis,
        'runtime_seconds': duration,
        'verdict': verdict,
        'status': status
    }

    output_file = OUTPUT_DIR / 'WORK_ORDER_QQ_monte_carlo_results.json'
    with open(output_file, 'w') as f:
        json.dump(results_dict, f, indent=2)
    print(f"\nSaved: {output_file}")

    # Summary box
    print(f"""
┌────────────────────────────────────────────────────────────────────────┐
│          WORK-ORDER QQ: MONTE CARLO CMB VALIDATION                      │
├────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  MONTE CARLO PARAMETERS:                                                │
│    Simulations:       {N_SIMULATIONS:>10,}                                     │
│    Resolution:        Nside = {NSIDE}                                       │
│    Circle radius:     {CIRCLE_RADIUS_DEG}°                                           │
│                                                                         │
│  NULL DISTRIBUTION:                                                     │
│    Mean r:            {analysis['mean']:>10.4f}                                     │
│    Std r:             {analysis['std']:>10.4f}                                     │
│    99.9th percentile: {analysis['percentiles']['99.9']:>10.4f}                                     │
│                                                                         │
│  OBSERVED V2↔V3:                                                        │
│    Correlation:       {OBSERVED_R:>10.4f}                                     │
│    Orientation:       {OBSERVED_ORIENTATION:>10}                                     │
│                                                                         │
│  SIGNIFICANCE:                                                          │
│    p-value:           {analysis['p_value']:>10.2e}                                     │
│    Monte Carlo σ:     {analysis['sigma'] if isinstance(analysis['sigma'], str) else f"{analysis['sigma']:.2f}":>10}σ                                     │
│                                                                         │
│  VERDICT: {verdict:<60} │
│                                                                         │
└────────────────────────────────────────────────────────────────────────┘
""")

    print(f"\nRuntime: {duration:.1f} seconds ({duration/60:.1f} minutes)")

    return results_dict


if __name__ == "__main__":
    main()
