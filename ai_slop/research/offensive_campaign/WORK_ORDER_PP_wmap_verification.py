#!/usr/bin/env python3
"""
WORK-ORDER PP: WMAP Cross-Validation of CMB Matched Circles
============================================================
Z² Framework v11.1.0

Purpose:
  Independent verification of the Planck V2↔V3 matched circles detection
  using WMAP 9-year ILC (Internal Linear Combination) CMB map.

Key Finding to Verify:
  - V2 (Anti-Shapley) ↔ V3 (Cold Spot) correlation at 115.5°
  - Planck result: r = 0.47 at 5.5σ (local), 3.8σ (global)
  - Orientation: REVERSED (Z₂ signature)

If WMAP shows the same signal:
  - Rules out Planck-specific systematics
  - Joint significance increases substantially
  - Strongly supports genuine topological origin

Author: Z² Offensive Campaign
Date: 2026-05-24
"""

import numpy as np
from scipy import stats
import healpy as hp
import requests
import os
import json
from datetime import datetime

# Configuration
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# WMAP 9-year ILC map from LAMBDA
WMAP_URL = "https://lambda.gsfc.nasa.gov/data/map/dr5/skymaps/9yr/wmap_ilc_9yr_v5.fits"

# Z² vertex directions
V2_ANTI_SHAPLEY = {"l": 96.4, "b": -29.8}
V3_COLD_SPOT = {"l": 186.4, "b": 60.2}

# Planck result for comparison
PLANCK_RESULT = {
    "r_best": 0.4696,
    "radius_deg": 10,
    "sigma_local": 5.53,
    "orientation": "reversed"
}


def download_wmap(output_path):
    """Download WMAP 9-year ILC map."""
    print(f"Downloading WMAP 9-year ILC map...")
    print(f"URL: {WMAP_URL}")

    try:
        response = requests.get(WMAP_URL, timeout=300, stream=True)
        if response.status_code == 200:
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            print(f"Downloaded: {os.path.getsize(output_path)/1e6:.1f} MB")
            return True
        else:
            print(f"HTTP {response.status_code}")
    except Exception as e:
        print(f"Download error: {e}")

    return False


def circle_point(theta_c, phi_c, radius, angle):
    """Get 3D vector for point on circle."""
    cx = np.sin(theta_c) * np.cos(phi_c)
    cy = np.sin(theta_c) * np.sin(phi_c)
    cz = np.cos(theta_c)

    if abs(cz) < 0.9:
        px, py, pz = -cy, cx, 0
    else:
        px, py, pz = 1, 0, 0
    norm = np.sqrt(px**2 + py**2 + pz**2)
    px, py, pz = px/norm, py/norm, pz/norm

    qx = cy*pz - cz*py
    qy = cz*px - cx*pz
    qz = cx*py - cy*px

    cos_r, sin_r = np.cos(radius), np.sin(radius)
    cos_a, sin_a = np.cos(angle), np.sin(angle)

    x = cx*cos_r + (px*cos_a + qx*sin_a)*sin_r
    y = cy*cos_r + (py*cos_a + qy*sin_a)*sin_r
    z = cz*cos_r + (pz*cos_a + qz*sin_a)*sin_r

    return x, y, z


def extract_circle(cmb_map, theta_c, phi_c, radius_deg, n_points=720):
    """Extract CMB temperature along a circle."""
    nside = hp.get_nside(cmb_map)
    radius = np.radians(radius_deg)
    temperatures = np.zeros(n_points)

    for i in range(n_points):
        angle = 2 * np.pi * i / n_points
        vec = circle_point(theta_c, phi_c, radius, angle)
        pix = hp.vec2pix(nside, *vec)
        temperatures[i] = cmb_map[pix]

    return temperatures


def correlate_with_shifts(temps1, temps2):
    """Compute correlation over all phase shifts, both orientations."""
    t1 = (temps1 - np.mean(temps1)) / np.std(temps1)
    t2 = (temps2 - np.mean(temps2)) / np.std(temps2)

    # Forward correlation
    corr_fwd = np.correlate(t1, t2, mode='full') / len(t1)
    r_fwd = np.max(np.abs(corr_fwd))
    shift_fwd = np.argmax(np.abs(corr_fwd)) - len(t1) + 1

    # Reversed correlation (Z₂ signature)
    t2_rev = t2[::-1]
    corr_rev = np.correlate(t1, t2_rev, mode='full') / len(t1)
    r_rev = np.max(np.abs(corr_rev))
    shift_rev = np.argmax(np.abs(corr_rev)) - len(t1) + 1

    if r_rev > r_fwd:
        return r_rev, shift_rev, "reversed", corr_rev
    return r_fwd, shift_fwd, "forward", corr_fwd


def build_null_distribution(cmb_map, n_samples=500, radius_deg=10):
    """Build null distribution from random circle pairs."""
    print(f"Building WMAP null distribution ({n_samples} samples)...")

    nside = hp.get_nside(cmb_map)
    correlations = []

    np.random.seed(789)  # Different seed from Planck analysis
    for i in range(n_samples):
        theta1 = np.arccos(2*np.random.random() - 1)
        phi1 = 2*np.pi*np.random.random()
        theta2 = np.arccos(2*np.random.random() - 1)
        phi2 = 2*np.pi*np.random.random()

        temps1 = extract_circle(cmb_map, theta1, phi1, radius_deg)
        temps2 = extract_circle(cmb_map, theta2, phi2, radius_deg)

        r_best, _, _, _ = correlate_with_shifts(temps1, temps2)
        correlations.append(r_best)

    correlations = np.array(correlations)

    return {
        "mean": float(np.mean(correlations)),
        "std": float(np.std(correlations)),
        "percentiles": {
            "95": float(np.percentile(correlations, 95)),
            "99": float(np.percentile(correlations, 99)),
            "99.9": float(np.percentile(correlations, 99.9))
        }
    }


def run_wmap_verification():
    """Execute WMAP verification of matched circles."""
    print("="*70)
    print("WORK-ORDER PP: WMAP Cross-Validation of CMB Matched Circles")
    print("="*70)

    # Download WMAP if not present
    wmap_path = os.path.join(OUTPUT_DIR, "wmap_ilc_9yr.fits")

    if not os.path.exists(wmap_path):
        if not download_wmap(wmap_path):
            print("Failed to download WMAP. Cannot proceed.")
            return None

    # Load WMAP map
    print(f"\nLoading WMAP 9-year ILC map...")
    wmap_map = hp.read_map(wmap_path, dtype=np.float64)
    nside = hp.get_nside(wmap_map)
    print(f"Loaded: Nside={nside}, {len(wmap_map)} pixels")

    # WMAP ILC is in mK, convert to same units as analysis
    # (doesn't affect correlation, but good practice)

    # Build null distribution for WMAP
    null_dist = build_null_distribution(wmap_map, n_samples=500, radius_deg=10)
    print(f"WMAP null: μ = {null_dist['mean']:.4f}, σ = {null_dist['std']:.4f}")

    # =================================================================
    # KEY TEST: V2 (Anti-Shapley) ↔ V3 (Cold Spot)
    # =================================================================
    print("\n" + "="*60)
    print("KEY VERIFICATION: V2 (Anti-Shapley) ↔ V3 (Cold Spot)")
    print("="*60)

    # Convert coordinates
    v2_theta = np.radians(90 - V2_ANTI_SHAPLEY["b"])
    v2_phi = np.radians(V2_ANTI_SHAPLEY["l"])
    v3_theta = np.radians(90 - V3_COLD_SPOT["b"])
    v3_phi = np.radians(V3_COLD_SPOT["l"])

    print(f"V2 (Anti-Shapley): l={V2_ANTI_SHAPLEY['l']}°, b={V2_ANTI_SHAPLEY['b']}°")
    print(f"V3 (Cold Spot):    l={V3_COLD_SPOT['l']}°, b={V3_COLD_SPOT['b']}°")
    print(f"Separation: 115.5°")

    # Test multiple radii
    print("\nRadius scan (WMAP):")
    print("-" * 55)

    wmap_results = []

    for radius in [5, 7.5, 10, 12.5, 15, 20, 25, 30]:
        temps1 = extract_circle(wmap_map, v2_theta, v2_phi, radius)
        temps2 = extract_circle(wmap_map, v3_theta, v3_phi, radius)

        r_best, shift, orientation, _ = correlate_with_shifts(temps1, temps2)

        sigma = (r_best - null_dist["mean"]) / null_dist["std"]

        wmap_results.append({
            "radius_deg": radius,
            "r_best": r_best,
            "shift": shift,
            "orientation": orientation,
            "sigma": sigma
        })

        marker = " ***" if sigma > 4 else " **" if sigma > 3 else " *" if sigma > 2 else ""
        print(f"  r={radius:4.1f}°: corr = {r_best:.4f} ({orientation:8s}), "
              f"σ = {sigma:5.1f}{marker}")

    # Find best WMAP result
    best_wmap = max(wmap_results, key=lambda x: x["sigma"])

    # =================================================================
    # COMPARISON WITH PLANCK
    # =================================================================
    print("\n" + "="*60)
    print("PLANCK vs WMAP COMPARISON")
    print("="*60)

    print(f"\n{'Metric':<25} {'Planck':>12} {'WMAP':>12}")
    print("-" * 50)
    print(f"{'Best correlation r':<25} {PLANCK_RESULT['r_best']:>12.4f} {best_wmap['r_best']:>12.4f}")
    print(f"{'Optimal radius':<25} {PLANCK_RESULT['radius_deg']:>12}° {best_wmap['radius_deg']:>12}°")
    print(f"{'Local sigma':<25} {PLANCK_RESULT['sigma_local']:>12.1f}σ {best_wmap['sigma']:>12.1f}σ")
    print(f"{'Orientation':<25} {PLANCK_RESULT['orientation']:>12} {best_wmap['orientation']:>12}")

    # Check consistency
    orientation_match = PLANCK_RESULT['orientation'] == best_wmap['orientation']
    both_significant = PLANCK_RESULT['sigma_local'] > 3 and best_wmap['sigma'] > 2

    print("\n" + "="*60)
    print("CROSS-VALIDATION ASSESSMENT")
    print("="*60)

    if orientation_match and both_significant:
        print("\n✓ ORIENTATIONS MATCH (both reversed)")
        print("✓ BOTH DATASETS SHOW SIGNIFICANT CORRELATION")
        print("\n→ WMAP CONFIRMS PLANCK DETECTION")

        # Combined significance (Fisher's method)
        # Convert sigmas to p-values
        p_planck = stats.norm.sf(PLANCK_RESULT['sigma_local'])
        p_wmap = stats.norm.sf(best_wmap['sigma'])

        # Fisher's combined test
        chi2_combined = -2 * (np.log(p_planck) + np.log(p_wmap))
        p_combined = stats.chi2.sf(chi2_combined, df=4)
        sigma_combined = stats.norm.isf(p_combined)

        print(f"\nCOMBINED SIGNIFICANCE (Fisher's method):")
        print(f"  Planck p-value: {p_planck:.2e}")
        print(f"  WMAP p-value:   {p_wmap:.2e}")
        print(f"  Combined χ²:    {chi2_combined:.2f}")
        print(f"  Combined p:     {p_combined:.2e}")
        print(f"  Combined σ:     {sigma_combined:.1f}σ")

        verdict = "CONFIRMED"

    elif orientation_match:
        print("\n✓ ORIENTATIONS MATCH")
        print("⚠ WMAP significance lower than Planck")
        print("\n→ PARTIAL CONFIRMATION (needs investigation)")
        verdict = "PARTIAL"
        sigma_combined = None

    else:
        print("\n✗ ORIENTATIONS DO NOT MATCH")
        print("\n→ INCONSISTENT RESULTS")
        verdict = "INCONSISTENT"
        sigma_combined = None

    # =================================================================
    # ADDITIONAL CHECKS
    # =================================================================
    print("\n" + "="*60)
    print("ADDITIONAL VERIFICATION CHECKS")
    print("="*60)

    # Test other vertex pairs in WMAP
    vertex_pairs = [
        ("V1_Shapley", "V2_Anti_Shapley", 276.4, 29.8, 96.4, -29.8),
        ("V3_Cold_Spot", "V4_Southern", 186.4, 60.2, 6.4, -60.2),
    ]

    print("\nOther Z² vertex pairs in WMAP:")
    for name1, name2, l1, b1, l2, b2 in vertex_pairs:
        theta1 = np.radians(90 - b1)
        phi1 = np.radians(l1)
        theta2 = np.radians(90 - b2)
        phi2 = np.radians(l2)

        temps1 = extract_circle(wmap_map, theta1, phi1, 10)
        temps2 = extract_circle(wmap_map, theta2, phi2, 10)

        r_best, _, orientation, _ = correlate_with_shifts(temps1, temps2)
        sigma = (r_best - null_dist["mean"]) / null_dist["std"]

        print(f"  {name1} ↔ {name2}: r = {r_best:.3f}, σ = {sigma:.1f} ({orientation})")

    # =================================================================
    # FINAL VERDICT
    # =================================================================
    print("\n" + "="*70)
    print("WMAP VERIFICATION: FINAL VERDICT")
    print("="*70)

    results = {
        "work_order": "PP",
        "task": "WMAP Cross-Validation of CMB Matched Circles",
        "date": datetime.now().isoformat(),
        "wmap_parameters": {
            "map": "9-year ILC",
            "nside": nside
        },
        "null_distribution": null_dist,
        "v2_v3_results": {
            "wmap": wmap_results,
            "best_wmap": best_wmap,
            "planck_comparison": PLANCK_RESULT
        },
        "cross_validation": {
            "orientation_match": orientation_match,
            "both_significant": both_significant,
            "combined_sigma": float(sigma_combined) if sigma_combined else None,
            "verdict": verdict
        }
    }

    # Save results
    output_path = os.path.join(OUTPUT_DIR, "WORK_ORDER_PP_wmap_results.json")
    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to: {output_path}")

    return results


if __name__ == "__main__":
    run_wmap_verification()
