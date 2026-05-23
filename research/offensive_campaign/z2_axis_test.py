#!/usr/bin/env python3
"""
Z² CHIRALITY AXIS ALIGNMENT TEST
=================================

Work-Order T & U - Simplified Approach

Key Insight:
The August 2025 DESI paper found:
- Strong auto-correlation (4-10σ parity-odd signal)
- Null cross-correlation between sky patches

This means: The parity signal is UNIFORM across the sky.
The question is: Does the AXIS of this signal align with the Z² prediction?

Test Strategy:
1. For each tetrahedron, compute its "chirality vector" (normal to handedness)
2. Correlate these vectors with the Z² predicted axis
3. If the correlation is statistically significant → topology confirmed

Z² Prediction: (l, b) = (287°, 9°) - the KBC Void center / Vertex #6

Author: Claude Opus 4.5
Date: May 24, 2026
"""

import numpy as np
from pathlib import Path
import json
from scipy.stats import pearsonr, spearmanr
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u

# Z² prediction
Z2_L, Z2_B = 287.0, 9.0  # Galactic coordinates in degrees


def z2_axis_cartesian():
    """Get Z² chirality axis as unit vector."""
    l_rad = np.radians(Z2_L)
    b_rad = np.radians(Z2_B)
    return np.array([
        np.cos(b_rad) * np.cos(l_rad),
        np.cos(b_rad) * np.sin(l_rad),
        np.sin(b_rad)
    ])


def random_axis():
    """Generate random unit vector for null test."""
    v = np.random.randn(3)
    return v / np.linalg.norm(v)


def tetrahedron_chirality_vector(p0, p1, p2, p3):
    """
    Compute chirality vector for a tetrahedron.

    The chirality vector is perpendicular to the plane defined by
    the tetrahedron's three "arms" and has magnitude = signed volume.

    For a tetrahedron with vertices p0, p1, p2, p3:
    - Form vectors v1 = p1-p0, v2 = p2-p0, v3 = p3-p0
    - Chirality vector = v1 × v2 (cross product)
    - Sign determined by dot with v3
    """
    v1 = p1 - p0
    v2 = p2 - p0
    v3 = p3 - p0

    # Cross product gives normal direction
    normal = np.cross(v1, v2)

    # Sign determined by v3 dot normal
    sign = np.sign(np.dot(v3, normal))

    # Normalize to unit vector, keep sign
    norm = np.linalg.norm(normal)
    if norm < 1e-10:
        return np.zeros(3)

    return sign * normal / norm


def compute_axis_correlation(positions, axis, n_samples=100000, r_min=30.0, r_max=120.0):
    """
    Compute correlation between tetrahedron chirality vectors and a test axis.

    Returns the mean alignment: <v·â> where v is chirality vector, â is test axis.
    For random data, this should be ~0.
    For data with preferred chirality along axis, this will be non-zero.
    """
    from scipy.spatial import cKDTree

    n_galaxies = len(positions)
    tree = cKDTree(positions)

    alignments = []
    n_valid = 0

    for attempt in range(n_samples * 10):
        if n_valid >= n_samples:
            break

        # Pick random primary
        i0 = np.random.randint(n_galaxies)
        p0 = positions[i0]

        # Find neighbors
        neighbors = tree.query_ball_point(p0, r_max)
        neighbors = [n for n in neighbors if n != i0]

        if len(neighbors) < 3:
            continue

        # Pick 3 neighbors
        chosen = np.random.choice(neighbors, 3, replace=False)
        p1, p2, p3 = positions[chosen]

        # Check distances
        dists = [
            np.linalg.norm(p1 - p0),
            np.linalg.norm(p2 - p0),
            np.linalg.norm(p3 - p0),
            np.linalg.norm(p2 - p1),
            np.linalg.norm(p3 - p1),
            np.linalg.norm(p3 - p2),
        ]

        if any(d < r_min or d > r_max for d in dists):
            continue

        # Compute chirality vector
        chi_vec = tetrahedron_chirality_vector(p0, p1, p2, p3)

        if np.linalg.norm(chi_vec) < 0.5:
            continue

        # Compute alignment with axis
        alignment = np.dot(chi_vec, axis)
        alignments.append(alignment)
        n_valid += 1

    alignments = np.array(alignments)

    return alignments


def run_axis_test(positions, n_samples=100000, n_null=10):
    """
    Test alignment with Z² axis vs random null axes.

    Returns statistics comparing Z² alignment to null distribution.
    """
    print(f"\nTesting {n_samples} tetrahedra...")

    # Z² prediction
    z2_axis = z2_axis_cartesian()
    print(f"Z² axis: (l, b) = ({Z2_L}°, {Z2_B}°)")

    # Compute Z² alignment
    print("Computing alignment with Z² axis...")
    z2_alignments = compute_axis_correlation(positions, z2_axis, n_samples)
    z2_mean = np.mean(z2_alignments)
    z2_std = np.std(z2_alignments) / np.sqrt(len(z2_alignments))

    print(f"  Z² alignment: {z2_mean:.6f} ± {z2_std:.6f}")

    # Null tests with random axes
    print(f"\nRunning {n_null} null tests with random axes...")
    null_means = []
    for i in range(n_null):
        rand_axis = random_axis()
        null_alignments = compute_axis_correlation(positions, rand_axis, n_samples)
        null_means.append(np.mean(null_alignments))
        print(f"  Null {i+1}: {null_means[-1]:.6f}")

    null_means = np.array(null_means)
    null_mean = np.mean(null_means)
    null_std = np.std(null_means)

    # Significance
    z_score = (z2_mean - null_mean) / (null_std + 1e-10)

    # Anti-aligned test (reflection symmetry)
    anti_z2 = -z2_axis
    anti_alignments = compute_axis_correlation(positions, anti_z2, n_samples)
    anti_mean = np.mean(anti_alignments)

    # Total alignment (absolute value)
    total_alignment = abs(z2_mean) + abs(anti_mean)

    results = {
        'z2_axis': {
            'galactic': [Z2_L, Z2_B],
            'cartesian': z2_axis.tolist()
        },
        'z2_alignment': {
            'mean': float(z2_mean),
            'std_error': float(z2_std),
            'n_samples': len(z2_alignments)
        },
        'anti_z2_alignment': {
            'mean': float(anti_mean)
        },
        'null_distribution': {
            'mean': float(null_mean),
            'std': float(null_std),
            'n_tests': n_null
        },
        'z_score': float(z_score),
        'total_alignment': float(total_alignment),
        'significant': bool(abs(z_score) > 2.0)
    }

    print("\n" + "=" * 60)
    print("RESULTS")
    print("=" * 60)
    print(f"Z² axis alignment:      {z2_mean:+.6f} ± {z2_std:.6f}")
    print(f"Anti-Z² alignment:      {anti_mean:+.6f}")
    print(f"Null distribution:      {null_mean:+.6f} ± {null_std:.6f}")
    print(f"Z-score vs null:        {z_score:+.2f}")

    if abs(z_score) > 3:
        print("\n*** HIGHLY SIGNIFICANT Z² AXIS ALIGNMENT ***")
        print("*** p < 0.003 - TOPOLOGY SIGNAL DETECTED ***")
    elif abs(z_score) > 2:
        print("\n** Significant Z² axis alignment (p < 0.05) **")
    else:
        print("\nNo significant alignment detected")
        print("(Need more statistics or better estimator)")

    return results


def load_desi_positions():
    """Load DESI data and convert to Cartesian positions."""
    from astropy.cosmology import FlatLambdaCDM

    data_dir = Path(__file__).parent

    print("\nLoading DESI DR1 LRG data...")

    all_ra, all_dec, all_z = [], [], []

    for fname in ['LRG_NGC_clustering.dat.fits', 'LRG_SGC_clustering.dat.fits']:
        for try_dir in [data_dir, data_dir / 'desi_data']:
            fpath = try_dir / fname
            if fpath.exists():
                print(f"  Loading {fname}...")
                with fits.open(fpath) as hdul:
                    data = hdul[1].data
                    all_ra.extend(data['RA'])
                    all_dec.extend(data['DEC'])
                    all_z.extend(data['Z'])
                break

    all_ra = np.array(all_ra)
    all_dec = np.array(all_dec)
    all_z = np.array(all_z)

    print(f"  Total galaxies: {len(all_ra)}")

    # Convert to Galactic Cartesian
    print("  Converting coordinates...")
    cosmo = FlatLambdaCDM(H0=70, Om0=0.315)

    coords = SkyCoord(ra=all_ra*u.deg, dec=all_dec*u.deg, frame='icrs')
    gal = coords.galactic

    l_rad = np.radians(gal.l.deg)
    b_rad = np.radians(gal.b.deg)

    print("  Computing comoving distances...")
    D_c = cosmo.comoving_distance(all_z).value  # Mpc

    x = D_c * np.cos(b_rad) * np.cos(l_rad)
    y = D_c * np.cos(b_rad) * np.sin(l_rad)
    z = D_c * np.sin(b_rad)

    return np.column_stack([x, y, z])


def main():
    print("=" * 70)
    print("Z² CHIRALITY AXIS ALIGNMENT TEST")
    print("=" * 70)
    print()
    print(f"Testing if galaxy chirality aligns with Z² prediction:")
    print(f"  Predicted axis: (l, b) = ({Z2_L}°, {Z2_B}°)")
    print()
    print("Method: Compare tetrahedron chirality correlation with Z² axis")
    print("        vs correlation with random null axes")

    # Load data
    positions = load_desi_positions()

    # Subsample for speed
    n_use = min(300000, len(positions))
    print(f"\nUsing {n_use} galaxy subsample...")
    idx = np.random.choice(len(positions), n_use, replace=False)
    positions = positions[idx]

    # Run test
    results = run_axis_test(positions, n_samples=100000, n_null=20)

    # Save results
    output_file = Path(__file__).parent / 'z2_axis_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    print("\n" + "=" * 70)
    print("INTERPRETATION")
    print("=" * 70)
    print()
    print("The August 2025 DESI paper found 4-10σ parity-odd signal.")
    print("If this is T³/Z₂ topology, the signal axis should align with")
    print(f"the Z₂ vertex at (l, b) = ({Z2_L}°, {Z2_B}°).")
    print()
    print("Our simple estimator may not capture the full signal.")
    print("The proper test requires the Philcox encore algorithm with")
    print("directional multipole output.")

    return results


if __name__ == "__main__":
    np.random.seed(42)
    main()
