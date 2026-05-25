#!/usr/bin/env python3
"""
=============================================================================
CMB CIRCLES-IN-THE-SKY ANALYSIS (T³/Z₂ Topology)
=============================================================================
Searches for matched circles in the CMB that would indicate the universe
has T³/Z₂ orbifold topology with L_c = 20.6 Gpc.

In T³/Z₂:
- The Z₂ involution maps antipodal points: (θ,φ) → (π-θ, φ+π)
- Matched circles appear at EXACTLY 180° separation
- Circle angular radius α = 37.5° (from Z² metric calculation)
- Temperature patterns should match with Z₂ parity (reflection)

Method:
1. Extract temperature profile along circles of radius 37.5°
2. Compare each circle to its antipodal counterpart
3. Calculate correlation with and without Z₂ parity flip
4. Statistical significance via Monte Carlo

Author: Carl Zimmerman / Claude
Based on: Cornish, Spergel, Starkman (1998) - Circles in the Sky
=============================================================================
"""

import numpy as np
import healpy as hp
from pathlib import Path
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
import json
import sys

# Force unbuffered output
sys.stdout.reconfigure(line_buffering=True)

# =============================================================================
# T³/Z₂ TOPOLOGY PARAMETERS (from Z² metric calculation)
# =============================================================================

L_C_GPC = 20.6          # Fundamental domain size
D_LSS_GPC = 12.983      # Distance to last scattering surface (Z² metric)
ALPHA_DEG = 37.5        # Matched circle angular radius
ALPHA_RAD = np.radians(ALPHA_DEG)

# Number of points to sample along each circle
N_CIRCLE_POINTS = 360   # 1° resolution

# Statistical thresholds
CORRELATION_THRESHOLD = 0.7  # Minimum correlation for a "match"


# =============================================================================
# CMB MAP LOADING
# =============================================================================

def load_cmb_map(fits_path: Path, field: int = 0) -> Tuple[np.ndarray, int]:
    """
    Load a CMB temperature map from FITS file.

    Args:
        fits_path: Path to the FITS file
        field: Which field to read (0 = temperature for most maps)

    Returns:
        (temperature_map, nside)
    """
    print(f"Loading CMB map: {fits_path.name}")

    # Read the map
    cmb_map = hp.read_map(fits_path, field=field, verbose=False)

    # Get NSIDE (resolution parameter)
    nside = hp.npix2nside(len(cmb_map))

    print(f"  NSIDE: {nside}")
    print(f"  Resolution: {hp.nside2resol(nside, arcmin=True):.2f} arcmin")
    print(f"  N_pixels: {len(cmb_map):,}")

    # Check for bad values
    good_pixels = np.isfinite(cmb_map)
    bad_frac = 1 - np.sum(good_pixels) / len(cmb_map)
    print(f"  Bad pixels: {bad_frac*100:.2f}%")

    # Replace bad values with local mean (simple inpainting)
    if bad_frac > 0:
        cmb_map[~good_pixels] = np.nanmean(cmb_map)

    return cmb_map, nside


# =============================================================================
# CIRCLE EXTRACTION
# =============================================================================

def get_circle_pixels(
    theta_center: float,
    phi_center: float,
    alpha: float,
    nside: int,
    n_points: int = N_CIRCLE_POINTS
) -> Tuple[np.ndarray, np.ndarray]:
    """
    Get the pixel indices and angular positions along a circle.

    Args:
        theta_center: Colatitude of circle center (radians, 0=North pole)
        phi_center: Longitude of circle center (radians)
        alpha: Angular radius of circle (radians)
        nside: HEALPix resolution parameter
        n_points: Number of points to sample along circle

    Returns:
        (pixel_indices, azimuthal_angles)
    """
    # Create points along the circle
    # The circle is parameterized by angle β going from 0 to 2π
    beta = np.linspace(0, 2*np.pi, n_points, endpoint=False)

    # Convert circle points to (theta, phi) on the sphere
    # Using spherical geometry rotation

    # First, create circle at north pole with radius alpha
    theta_circ = np.full(n_points, alpha)
    phi_circ = beta

    # Then rotate to the actual center position
    # This requires spherical rotation

    # Convert to Cartesian
    x = np.sin(theta_circ) * np.cos(phi_circ)
    y = np.sin(theta_circ) * np.sin(phi_circ)
    z = np.cos(theta_circ)

    # Rotate around y-axis by theta_center
    cos_t = np.cos(theta_center)
    sin_t = np.sin(theta_center)

    x_rot = cos_t * x + sin_t * z
    z_rot = -sin_t * x + cos_t * z
    y_rot = y

    # Then rotate around z-axis by phi_center
    cos_p = np.cos(phi_center)
    sin_p = np.sin(phi_center)

    x_final = cos_p * x_rot - sin_p * y_rot
    y_final = sin_p * x_rot + cos_p * y_rot
    z_final = z_rot

    # Convert back to spherical
    theta_final = np.arccos(np.clip(z_final, -1, 1))
    phi_final = np.arctan2(y_final, x_final) % (2 * np.pi)

    # Get HEALPix pixel indices
    pixels = hp.ang2pix(nside, theta_final, phi_final)

    return pixels, beta


def extract_circle_temperature(
    cmb_map: np.ndarray,
    theta_center: float,
    phi_center: float,
    alpha: float,
    nside: int,
    n_points: int = N_CIRCLE_POINTS
) -> np.ndarray:
    """
    Extract temperature values along a circle.

    Args:
        cmb_map: The CMB temperature map
        theta_center, phi_center: Circle center (radians)
        alpha: Circle radius (radians)
        nside: HEALPix resolution
        n_points: Sampling points

    Returns:
        Array of temperature values along the circle
    """
    pixels, _ = get_circle_pixels(theta_center, phi_center, alpha, nside, n_points)
    return cmb_map[pixels]


# =============================================================================
# ANTIPODAL CIRCLE COMPARISON
# =============================================================================

def antipodal_coordinates(theta: float, phi: float) -> Tuple[float, float]:
    """
    Calculate the antipodal (Z₂ inverted) coordinates.

    Z₂ involution: (θ, φ) → (π - θ, φ + π)

    Args:
        theta: Colatitude (radians)
        phi: Longitude (radians)

    Returns:
        (theta_anti, phi_anti)
    """
    theta_anti = np.pi - theta
    phi_anti = (phi + np.pi) % (2 * np.pi)
    return theta_anti, phi_anti


def compare_circles(
    temp1: np.ndarray,
    temp2: np.ndarray,
    apply_parity: bool = False
) -> float:
    """
    Compare two circle temperature profiles.

    Args:
        temp1: Temperature profile of circle 1
        temp2: Temperature profile of circle 2
        apply_parity: If True, flip circle 2 (Z₂ parity)

    Returns:
        Pearson correlation coefficient
    """
    # Normalize (subtract mean, divide by std)
    t1 = (temp1 - np.mean(temp1)) / (np.std(temp1) + 1e-10)
    t2 = (temp2 - np.mean(temp2)) / (np.std(temp2) + 1e-10)

    if apply_parity:
        # Z₂ parity: flip the circle direction
        t2 = t2[::-1]

    # Try all possible phase shifts (rotation around circle)
    n = len(t1)
    correlations = []

    for shift in range(n):
        t2_shifted = np.roll(t2, shift)
        corr = np.corrcoef(t1, t2_shifted)[0, 1]
        correlations.append(corr)

    # Return maximum correlation (best alignment)
    return max(correlations)


def analyze_circle_pair(
    cmb_map: np.ndarray,
    theta: float,
    phi: float,
    nside: int,
    alpha: float = ALPHA_RAD
) -> Dict:
    """
    Analyze a pair of antipodal circles.

    Args:
        cmb_map: CMB temperature map
        theta, phi: Center of first circle (radians)
        nside: HEALPix resolution
        alpha: Circle radius (radians)

    Returns:
        Dictionary with analysis results
    """
    # Get antipodal center
    theta_anti, phi_anti = antipodal_coordinates(theta, phi)

    # Extract both circles
    temp1 = extract_circle_temperature(cmb_map, theta, phi, alpha, nside)
    temp2 = extract_circle_temperature(cmb_map, theta_anti, phi_anti, alpha, nside)

    # Compare without parity
    corr_direct = compare_circles(temp1, temp2, apply_parity=False)

    # Compare with Z₂ parity (flip)
    corr_parity = compare_circles(temp1, temp2, apply_parity=True)

    return {
        "theta_deg": np.degrees(theta),
        "phi_deg": np.degrees(phi),
        "theta_anti_deg": np.degrees(theta_anti),
        "phi_anti_deg": np.degrees(phi_anti),
        "correlation_direct": corr_direct,
        "correlation_parity": corr_parity,
        "best_correlation": max(corr_direct, corr_parity),
        "parity_preferred": corr_parity > corr_direct
    }


# =============================================================================
# FULL SKY SEARCH
# =============================================================================

def search_all_antipodal_circles(
    cmb_map: np.ndarray,
    nside: int,
    alpha: float = ALPHA_RAD,
    n_theta: int = 30,
    n_phi: int = 60
) -> List[Dict]:
    """
    Search the full sky for matched antipodal circles.

    Only searches one hemisphere (the antipodes are automatically tested).

    Args:
        cmb_map: CMB temperature map
        nside: HEALPix resolution
        alpha: Circle radius (radians)
        n_theta: Number of colatitude samples
        n_phi: Number of longitude samples

    Returns:
        List of results for each circle pair
    """
    results = []

    # Only search one hemisphere (theta from 0 to π/2)
    # The antipodes are in the other hemisphere
    thetas = np.linspace(alpha, np.pi/2, n_theta)  # Avoid poles
    phis = np.linspace(0, 2*np.pi, n_phi, endpoint=False)

    total = len(thetas) * len(phis)
    print(f"Searching {total} circle pairs...")

    count = 0
    for theta in thetas:
        for phi in phis:
            result = analyze_circle_pair(cmb_map, theta, phi, nside, alpha)
            results.append(result)

            count += 1
            if count % 100 == 0:
                print(f"  Progress: {count}/{total} ({100*count/total:.1f}%)")

    return results


def find_best_matches(results: List[Dict], top_n: int = 10) -> List[Dict]:
    """
    Find the best matching circle pairs.

    Args:
        results: List of analysis results
        top_n: Number of top matches to return

    Returns:
        Top N results sorted by correlation
    """
    # Sort by best correlation
    sorted_results = sorted(results, key=lambda x: x["best_correlation"], reverse=True)
    return sorted_results[:top_n]


# =============================================================================
# STATISTICAL SIGNIFICANCE
# =============================================================================

def monte_carlo_significance(
    cmb_map: np.ndarray,
    nside: int,
    observed_corr: float,
    n_random: int = 1000,
    alpha: float = ALPHA_RAD
) -> Tuple[float, float]:
    """
    Estimate statistical significance via Monte Carlo.

    Compares observed correlation to random circle pairs
    (not antipodal - just random positions).

    Args:
        cmb_map: CMB temperature map
        nside: HEALPix resolution
        observed_corr: The observed correlation to test
        n_random: Number of random comparisons
        alpha: Circle radius

    Returns:
        (p_value, z_score)
    """
    print(f"Running Monte Carlo significance test ({n_random} random pairs)...")

    random_corrs = []

    for i in range(n_random):
        # Random circle centers (not antipodal)
        theta1 = np.arccos(1 - 2*np.random.random())  # Uniform on sphere
        phi1 = 2 * np.pi * np.random.random()

        theta2 = np.arccos(1 - 2*np.random.random())
        phi2 = 2 * np.pi * np.random.random()

        # Extract and compare
        temp1 = extract_circle_temperature(cmb_map, theta1, phi1, alpha, nside)
        temp2 = extract_circle_temperature(cmb_map, theta2, phi2, alpha, nside)

        corr = compare_circles(temp1, temp2, apply_parity=False)
        random_corrs.append(corr)

        if (i + 1) % 200 == 0:
            print(f"  Progress: {i+1}/{n_random}")

    random_corrs = np.array(random_corrs)

    # P-value: fraction of random correlations >= observed
    p_value = np.sum(random_corrs >= observed_corr) / n_random

    # Z-score
    mean_random = np.mean(random_corrs)
    std_random = np.std(random_corrs)
    z_score = (observed_corr - mean_random) / (std_random + 1e-10)

    print(f"  Random correlations: mean={mean_random:.4f}, std={std_random:.4f}")
    print(f"  Observed: {observed_corr:.4f}")
    print(f"  P-value: {p_value:.6f}")
    print(f"  Z-score: {z_score:.2f}σ")

    return p_value, z_score


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def main():
    """Run the full CMB circles analysis"""

    print("\n" + "="*70)
    print("CMB CIRCLES-IN-THE-SKY ANALYSIS")
    print("Searching for T³/Z₂ topology signature")
    print("="*70 + "\n")

    print(f"Expected circle radius: α = {ALPHA_DEG:.2f}°")
    print(f"Topology: T³/Z₂ with L_c = {L_C_GPC} Gpc")
    print(f"D_LSS = {D_LSS_GPC:.3f} Gpc (Z² metric)")
    print()

    # Try to load CMB map
    # First try WMAP (smaller, faster for testing)
    wmap_path = Path(__file__).parent.parent / "offensive_campaign" / "wmap_ilc_9yr.fits"
    planck_path = Path(__file__).parent.parent / "offensive_campaign" / "planck_cmb_smica.fits"

    if wmap_path.exists():
        cmb_map, nside = load_cmb_map(wmap_path)
        map_name = "WMAP ILC 9yr"
    elif planck_path.exists():
        cmb_map, nside = load_cmb_map(planck_path)
        map_name = "Planck SMICA"
    else:
        print("ERROR: No CMB map found!")
        print(f"  Tried: {wmap_path}")
        print(f"  Tried: {planck_path}")
        return

    print(f"\nUsing: {map_name}")
    print()

    # Run full sky search
    print("="*70)
    print("FULL SKY SEARCH FOR MATCHED ANTIPODAL CIRCLES")
    print("="*70 + "\n")

    results = search_all_antipodal_circles(
        cmb_map, nside,
        alpha=ALPHA_RAD,
        n_theta=20,  # Coarse search first
        n_phi=40
    )

    # Find best matches
    print("\n" + "="*70)
    print("TOP 10 BEST MATCHING ANTIPODAL CIRCLE PAIRS")
    print("="*70 + "\n")

    best = find_best_matches(results, top_n=10)

    print(f"{'Rank':<6} {'θ (°)':<10} {'φ (°)':<10} {'Corr (direct)':<15} {'Corr (parity)':<15} {'Best':<10}")
    print("-"*70)

    for i, r in enumerate(best, 1):
        print(f"{i:<6} {r['theta_deg']:<10.2f} {r['phi_deg']:<10.2f} "
              f"{r['correlation_direct']:<15.4f} {r['correlation_parity']:<15.4f} "
              f"{r['best_correlation']:<10.4f}")

    # Statistical significance of best match
    if best:
        print("\n" + "="*70)
        print("STATISTICAL SIGNIFICANCE TEST")
        print("="*70 + "\n")

        best_corr = best[0]["best_correlation"]
        p_value, z_score = monte_carlo_significance(
            cmb_map, nside,
            observed_corr=best_corr,
            n_random=500,
            alpha=ALPHA_RAD
        )

        print("\n" + "="*70)
        print("SUMMARY")
        print("="*70)
        print(f"Best antipodal circle correlation: {best_corr:.4f}")
        print(f"Statistical significance: {z_score:.2f}σ (p = {p_value:.6f})")

        if z_score > 3:
            print("\n★★★ SIGNIFICANT TOPOLOGY SIGNAL DETECTED! ★★★")
        elif z_score > 2:
            print("\n★★ Moderate evidence for topology (2-3σ)")
        else:
            print("\n○ No significant topology signal in this search")

    # Save results (convert numpy types to Python native)
    output_file = Path(__file__).parent / "cmb_circles_results.json"

    def to_native(obj):
        """Convert numpy types to Python native for JSON serialization"""
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif isinstance(obj, dict):
            return {k: to_native(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [to_native(v) for v in obj]
        return obj

    with open(output_file, 'w') as f:
        json.dump(to_native({
            "map_name": map_name,
            "alpha_deg": ALPHA_DEG,
            "n_pairs_searched": len(results),
            "best_correlation": best[0]["best_correlation"] if best else 0,
            "z_score": z_score if 'z_score' in dir() else None,
            "p_value": p_value if 'p_value' in dir() else None,
            "top_10_matches": best,
            "all_correlations": [r["best_correlation"] for r in results]
        }), f, indent=2)

    print(f"\nResults saved to: {output_file}")
    print("="*70 + "\n")


if __name__ == "__main__":
    main()
