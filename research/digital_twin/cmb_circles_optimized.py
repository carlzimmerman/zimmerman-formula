#!/usr/bin/env python3
"""
=============================================================================
OPTIMIZED CMB CIRCLES ANALYSIS (Directives KKKK, LLLL, MMMM)
=============================================================================
High-resolution Planck analysis with:
1. Memory-efficient map loading (memmap)
2. Spherical harmonic filtering (ℓ=2-20) to isolate topology signal
3. Gradient descent optimization around WMAP hit coordinates

Author: Carl Zimmerman / Claude
=============================================================================
"""

import numpy as np
import healpy as hp
from pathlib import Path
from typing import Tuple, Dict, Optional
from scipy.optimize import minimize
import json
import sys

sys.stdout.reconfigure(line_buffering=True)

# =============================================================================
# T³/Z₂ TOPOLOGY PARAMETERS
# =============================================================================

L_C_GPC = 20.6
D_LSS_GPC = 12.983
ALPHA_DEG = 37.5
ALPHA_RAD = np.radians(ALPHA_DEG)
N_CIRCLE_POINTS = 360

# WMAP best hit coordinates (from previous analysis)
WMAP_BEST_THETA = 67.89  # degrees
WMAP_BEST_PHI = 9.0      # degrees


# =============================================================================
# SPHERICAL HARMONIC FILTERING (Directive LLLL)
# =============================================================================

def filter_multipoles(cmb_map: np.ndarray, nside: int,
                      l_min: int = 2, l_max: int = 20) -> np.ndarray:
    """
    Apply spherical harmonic bandpass filter to isolate large-scale structure.

    Topology signatures are macroscopic (37.5° circles). Filter out:
    - ℓ < 2: Removes dipole (Earth's motion)
    - ℓ > 20: Removes small-scale acoustic peaks and noise

    Args:
        cmb_map: Input CMB temperature map
        nside: HEALPix resolution
        l_min: Minimum multipole to keep
        l_max: Maximum multipole to keep

    Returns:
        Filtered map with only ℓ=l_min to l_max
    """
    print(f"Applying multipole filter: ℓ = {l_min} to {l_max}")

    # Decompose into spherical harmonics
    print("  Computing alm coefficients...")
    lmax = 3 * nside - 1  # Standard lmax for nside
    alm = hp.map2alm(cmb_map, lmax=lmax)

    # Create filtered alm
    alm_filtered = np.zeros_like(alm)

    # Copy only desired multipoles
    print(f"  Filtering to ℓ = [{l_min}, {l_max}]...")
    for l in range(l_min, min(l_max + 1, lmax + 1)):
        for m in range(0, l + 1):
            idx = hp.Alm.getidx(lmax, l, m)
            alm_filtered[idx] = alm[idx]

    # Reconstruct filtered map
    print("  Reconstructing filtered map...")
    filtered_map = hp.alm2map(alm_filtered, nside, verbose=False)

    print(f"  Original RMS: {np.std(cmb_map):.2e}")
    print(f"  Filtered RMS: {np.std(filtered_map):.2e}")

    return filtered_map


# =============================================================================
# CIRCLE EXTRACTION (optimized)
# =============================================================================

def get_circle_temperatures(cmb_map: np.ndarray, nside: int,
                           theta: float, phi: float,
                           alpha: float = ALPHA_RAD,
                           n_points: int = N_CIRCLE_POINTS) -> np.ndarray:
    """
    Extract temperature values along a circle on the CMB sphere.

    Args:
        cmb_map: CMB temperature map
        nside: HEALPix resolution
        theta: Colatitude of center (radians)
        phi: Longitude of center (radians)
        alpha: Angular radius (radians)
        n_points: Number of samples

    Returns:
        Array of temperature values
    """
    beta = np.linspace(0, 2*np.pi, n_points, endpoint=False)

    # Circle at north pole
    theta_circ = np.full(n_points, alpha)
    phi_circ = beta

    # Convert to Cartesian
    x = np.sin(theta_circ) * np.cos(phi_circ)
    y = np.sin(theta_circ) * np.sin(phi_circ)
    z = np.cos(theta_circ)

    # Rotate around y-axis by theta
    cos_t, sin_t = np.cos(theta), np.sin(theta)
    x_rot = cos_t * x + sin_t * z
    z_rot = -sin_t * x + cos_t * z
    y_rot = y

    # Rotate around z-axis by phi
    cos_p, sin_p = np.cos(phi), np.sin(phi)
    x_final = cos_p * x_rot - sin_p * y_rot
    y_final = sin_p * x_rot + cos_p * y_rot
    z_final = z_rot

    # Back to spherical
    theta_final = np.arccos(np.clip(z_final, -1, 1))
    phi_final = np.arctan2(y_final, x_final) % (2 * np.pi)

    # Get pixel values
    pixels = hp.ang2pix(nside, theta_final, phi_final)
    return cmb_map[pixels]


def correlation_with_parity(temp1: np.ndarray, temp2: np.ndarray,
                           apply_parity: bool = True) -> Tuple[float, int]:
    """
    Compute best correlation between two circle profiles.

    Args:
        temp1, temp2: Temperature profiles
        apply_parity: If True, flip temp2 for Z₂ parity

    Returns:
        (best_correlation, best_shift)
    """
    t1 = (temp1 - np.mean(temp1)) / (np.std(temp1) + 1e-10)
    t2 = (temp2 - np.mean(temp2)) / (np.std(temp2) + 1e-10)

    if apply_parity:
        t2 = t2[::-1]  # Z₂ parity: reverse direction

    # Find best rotation alignment using FFT cross-correlation
    n = len(t1)
    corr = np.fft.ifft(np.fft.fft(t1) * np.conj(np.fft.fft(t2))).real / n

    best_shift = np.argmax(corr)
    best_corr = corr[best_shift]

    return best_corr, best_shift


# =============================================================================
# GRADIENT DESCENT OPTIMIZATION (Directive MMMM)
# =============================================================================

def optimize_circle_center(cmb_map: np.ndarray, nside: int,
                          theta0: float, phi0: float, alpha0: float,
                          search_radius: float = 5.0) -> Dict:
    """
    Refine circle center using gradient descent optimization.

    Args:
        cmb_map: Filtered CMB map
        nside: HEALPix resolution
        theta0, phi0: Initial center (degrees)
        alpha0: Initial radius (degrees)
        search_radius: Search range (degrees)

    Returns:
        Optimization results
    """
    print(f"\nOptimizing around θ={theta0:.2f}°, φ={phi0:.2f}°, α={alpha0:.2f}°")

    theta0_rad = np.radians(theta0)
    phi0_rad = np.radians(phi0)
    alpha0_rad = np.radians(alpha0)
    search_rad = np.radians(search_radius)

    def negative_correlation(params):
        """Objective function to minimize (negative correlation)"""
        theta, phi, alpha = params

        # Bounds check
        if theta < 0.1 or theta > np.pi - 0.1:
            return 1.0
        if alpha < 0.1 or alpha > np.pi/2:
            return 1.0

        # Get antipodal position
        theta_anti = np.pi - theta
        phi_anti = (phi + np.pi) % (2 * np.pi)

        # Extract circles
        temp1 = get_circle_temperatures(cmb_map, nside, theta, phi, alpha)
        temp2 = get_circle_temperatures(cmb_map, nside, theta_anti, phi_anti, alpha)

        # Compute correlation with Z₂ parity
        corr_parity, _ = correlation_with_parity(temp1, temp2, apply_parity=True)
        corr_direct, _ = correlation_with_parity(temp1, temp2, apply_parity=False)

        return -max(corr_parity, corr_direct)

    # Initial guess
    x0 = [theta0_rad, phi0_rad, alpha0_rad]

    # Bounds
    bounds = [
        (theta0_rad - search_rad, theta0_rad + search_rad),
        (phi0_rad - search_rad, phi0_rad + search_rad),
        (alpha0_rad - np.radians(5), alpha0_rad + np.radians(5))
    ]

    # Optimize
    print("  Running Nelder-Mead optimization...")
    result = minimize(
        negative_correlation,
        x0,
        method='Nelder-Mead',
        options={'maxiter': 200, 'xatol': 0.001, 'fatol': 0.0001}
    )

    theta_opt, phi_opt, alpha_opt = result.x
    best_corr = -result.fun

    print(f"  Optimized: θ={np.degrees(theta_opt):.3f}°, φ={np.degrees(phi_opt):.3f}°")
    print(f"  Optimized α={np.degrees(alpha_opt):.3f}°")
    print(f"  Best correlation: {best_corr:.4f}")

    return {
        "theta_deg": np.degrees(theta_opt),
        "phi_deg": np.degrees(phi_opt),
        "alpha_deg": np.degrees(alpha_opt),
        "theta_anti_deg": np.degrees(np.pi - theta_opt),
        "phi_anti_deg": np.degrees((phi_opt + np.pi) % (2*np.pi)),
        "correlation": best_corr,
        "optimization_success": result.success,
        "n_iterations": result.nit
    }


# =============================================================================
# MONTE CARLO SIGNIFICANCE
# =============================================================================

def monte_carlo_significance(cmb_map: np.ndarray, nside: int,
                            observed_corr: float, n_random: int = 1000,
                            alpha: float = ALPHA_RAD) -> Tuple[float, float]:
    """
    Estimate statistical significance via Monte Carlo.
    """
    print(f"\nRunning Monte Carlo ({n_random} random pairs)...")

    random_corrs = []

    for i in range(n_random):
        # Random non-antipodal circles
        theta1 = np.arccos(1 - 2*np.random.random())
        phi1 = 2 * np.pi * np.random.random()
        theta2 = np.arccos(1 - 2*np.random.random())
        phi2 = 2 * np.pi * np.random.random()

        temp1 = get_circle_temperatures(cmb_map, nside, theta1, phi1, alpha)
        temp2 = get_circle_temperatures(cmb_map, nside, theta2, phi2, alpha)

        corr, _ = correlation_with_parity(temp1, temp2, apply_parity=False)
        random_corrs.append(corr)

        if (i + 1) % 200 == 0:
            print(f"  Progress: {i+1}/{n_random}")

    random_corrs = np.array(random_corrs)

    p_value = np.sum(random_corrs >= observed_corr) / n_random
    z_score = (observed_corr - np.mean(random_corrs)) / (np.std(random_corrs) + 1e-10)

    print(f"  Random: mean={np.mean(random_corrs):.4f}, std={np.std(random_corrs):.4f}")
    print(f"  Observed: {observed_corr:.4f}")
    print(f"  Z-score: {z_score:.2f}σ, P-value: {p_value:.6f}")

    return p_value, z_score


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "="*70)
    print("OPTIMIZED CMB CIRCLES ANALYSIS")
    print("Planck SMICA with ℓ=2-20 filtering + gradient optimization")
    print("="*70 + "\n")

    # Load Planck map
    planck_path = Path(__file__).parent.parent / "offensive_campaign" / "planck_cmb_smica.fits"

    if not planck_path.exists():
        print(f"ERROR: Planck map not found at {planck_path}")
        return

    print("Loading Planck SMICA map...")
    cmb_map = hp.read_map(planck_path, field=0, verbose=False)
    nside = hp.npix2nside(len(cmb_map))
    print(f"  NSIDE: {nside}")
    print(f"  Resolution: {hp.nside2resol(nside, arcmin=True):.2f} arcmin")

    # Optional: downsample for speed (comment out for full resolution)
    if nside > 512:
        print(f"\nDownsampling from NSIDE={nside} to 512 for speed...")
        cmb_map = hp.ud_grade(cmb_map, 512)
        nside = 512
        print(f"  New NSIDE: {nside}")

    # Apply multipole filter (ℓ=2-20)
    print("\n" + "="*70)
    print("MULTIPOLE FILTERING (Directive LLLL)")
    print("="*70)
    filtered_map = filter_multipoles(cmb_map, nside, l_min=2, l_max=20)

    # Load WMAP results for optimization seed
    wmap_results_path = Path(__file__).parent / "cmb_circles_results.json"
    if wmap_results_path.exists():
        with open(wmap_results_path) as f:
            wmap_data = json.load(f)
        print(f"\nLoaded WMAP seed from {wmap_results_path.name}")
        best_hits = wmap_data.get("top_10_matches", [])
    else:
        best_hits = [{"theta_deg": WMAP_BEST_THETA, "phi_deg": WMAP_BEST_PHI}]

    # Optimize around top WMAP hits
    print("\n" + "="*70)
    print("GRADIENT DESCENT OPTIMIZATION (Directive MMMM)")
    print("="*70)

    optimized_results = []

    for i, hit in enumerate(best_hits[:5]):  # Top 5 WMAP hits
        print(f"\n--- Optimizing WMAP hit #{i+1} ---")
        result = optimize_circle_center(
            filtered_map, nside,
            theta0=hit["theta_deg"],
            phi0=hit["phi_deg"],
            alpha0=ALPHA_DEG,
            search_radius=10.0
        )
        optimized_results.append(result)

    # Sort by correlation
    optimized_results.sort(key=lambda x: x["correlation"], reverse=True)

    # Print results
    print("\n" + "="*70)
    print("OPTIMIZED RESULTS (Planck + ℓ=2-20 filter)")
    print("="*70)
    print(f"\n{'Rank':<6} {'θ (°)':<10} {'φ (°)':<10} {'α (°)':<10} {'Correlation':<12}")
    print("-"*60)

    for i, r in enumerate(optimized_results, 1):
        print(f"{i:<6} {r['theta_deg']:<10.3f} {r['phi_deg']:<10.3f} "
              f"{r['alpha_deg']:<10.3f} {r['correlation']:<12.4f}")

    # Statistical significance of best result
    if optimized_results:
        best = optimized_results[0]
        print("\n" + "="*70)
        print("STATISTICAL SIGNIFICANCE")
        print("="*70)

        p_value, z_score = monte_carlo_significance(
            filtered_map, nside,
            observed_corr=best["correlation"],
            n_random=1000,
            alpha=np.radians(best["alpha_deg"])
        )

        best["p_value"] = p_value
        best["z_score"] = z_score

        print("\n" + "="*70)
        print("FINAL RESULT")
        print("="*70)
        print(f"Best circle center: θ={best['theta_deg']:.3f}°, φ={best['phi_deg']:.3f}°")
        print(f"Circle radius: α={best['alpha_deg']:.3f}°")
        print(f"Antipodal center: θ={best['theta_anti_deg']:.3f}°, φ={best['phi_anti_deg']:.3f}°")
        print(f"Correlation: {best['correlation']:.4f}")
        print(f"Z-score: {z_score:.2f}σ")
        print(f"P-value: {p_value:.6f}")

        if z_score > 5:
            print("\n★★★★★ HIGHLY SIGNIFICANT TOPOLOGY DETECTION (>5σ)! ★★★★★")
        elif z_score > 4:
            print("\n★★★★ STRONG TOPOLOGY SIGNAL (>4σ)! ★★★★")
        elif z_score > 3:
            print("\n★★★ SIGNIFICANT TOPOLOGY SIGNAL (>3σ)! ★★★")

        # Save results
        output_file = Path(__file__).parent / "cmb_circles_planck_optimized.json"
        with open(output_file, 'w') as f:
            json.dump({
                "map": "Planck SMICA",
                "filter": "l=2-20",
                "nside_used": nside,
                "best_result": best,
                "all_optimized": optimized_results
            }, f, indent=2)

        print(f"\nResults saved to: {output_file}")


if __name__ == "__main__":
    main()
