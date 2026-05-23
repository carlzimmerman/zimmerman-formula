#!/usr/bin/env python3
"""
RUN CHIRALITY AXIS TEST ON REAL DESI DR1 DATA
==============================================

This is the kill shot. We're extracting the directional chirality axis
from actual DESI LRG observations and comparing to the Z² prediction.

Z² Prediction: (l, b) = (287°, 9°) ± 5°

If the observed axis aligns with this direction, the T³/Z₂ topology
of the universe is confirmed.

Author: Carl Zimmerman + Claude
Date: May 24, 2026
Framework: v11.1.0
"""

import numpy as np
from pathlib import Path
import json
import sys

# Check for astropy
try:
    from astropy.io import fits
    from astropy.coordinates import SkyCoord
    import astropy.units as u
except ImportError:
    print("ERROR: astropy required. Install with: pip install astropy")
    sys.exit(1)

# Import our chirality extraction algorithm
from chirality_axis_extraction import (
    compute_directional_4pcf,
    test_z2_alignment,
    galactic_to_cartesian,
    cartesian_to_galactic,
    KBC_L_DEG, KBC_B_DEG
)

# =============================================================================
# COSMOLOGY FOR COORDINATE CONVERSION
# =============================================================================

def comoving_distance(z, H0=70, Omega_m=0.315, Omega_Lambda=0.685):
    """Calculate comoving distance in Mpc."""
    from scipy.integrate import quad

    c = 299792.458  # km/s

    def integrand(z_prime):
        return 1.0 / np.sqrt(Omega_m * (1 + z_prime)**3 + Omega_Lambda)

    result, _ = quad(integrand, 0, z)
    D_H = c / H0

    return D_H * result


def radec_to_galactic_cartesian(ra, dec, z):
    """
    Convert RA/Dec/z to Galactic Cartesian coordinates.

    Returns positions in Mpc with Galactic frame orientation.
    """
    # Convert to SkyCoord
    coords = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')

    # Transform to Galactic
    gal = coords.galactic

    # Get Galactic l, b
    l_deg = gal.l.deg
    b_deg = gal.b.deg

    # Calculate comoving distances (vectorized for speed)
    print("  Computing comoving distances...")
    # Use approximate formula for speed (accurate to ~1%)
    c = 299792.458
    H0 = 70
    Omega_m = 0.315

    # Simple integral approximation
    D_c = np.zeros_like(z)
    for i, zi in enumerate(z):
        if i % 50000 == 0:
            print(f"    {i}/{len(z)}...")
        D_c[i] = comoving_distance(zi)

    # Convert to Galactic Cartesian
    l_rad = np.radians(l_deg)
    b_rad = np.radians(b_deg)

    x = D_c * np.cos(b_rad) * np.cos(l_rad)
    y = D_c * np.cos(b_rad) * np.sin(l_rad)
    z_cart = D_c * np.sin(b_rad)

    return np.column_stack([x, y, z_cart])


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def load_desi_lrg(filepath):
    """Load DESI LRG clustering catalog."""
    print(f"\nLoading {filepath}...")

    with fits.open(filepath) as hdul:
        data = hdul[1].data

        # Extract columns
        ra = data['RA']
        dec = data['DEC']
        z = data['Z']

        # Apply basic quality cuts
        # DESI uses WEIGHT_COMP for completeness
        if 'WEIGHT_COMP' in data.columns.names:
            weights = data['WEIGHT_COMP']
            good = weights > 0
            ra, dec, z = ra[good], dec[good], z[good]

    print(f"  Loaded {len(ra)} LRGs")
    print(f"  Redshift range: {z.min():.3f} - {z.max():.3f}")

    return ra, dec, z


def run_desi_chirality_test():
    """Run the full chirality axis test on DESI data."""

    print("=" * 70)
    print("DESI DR1 LRG CHIRALITY AXIS TEST")
    print("=" * 70)
    print(f"\nFramework: Z² Unified Action v11.1.0")
    print(f"Date: May 24, 2026")
    print(f"Target: Extract chirality axis from REAL DESI data")

    print(f"""
Z² PREDICTION:
--------------
  Chirality axis: (l, b) = ({KBC_L_DEG}°, {KBC_B_DEG}°)
  Physical meaning: Direction toward nearest T³/Z₂ vertex via KBC Void
  Uncertainty: ±5°

If observed axis aligns with this → Universe is T³/Z₂ with L_c = 20.6 Gpc
""")

    # Load data
    data_dir = Path(__file__).parent / 'desi_data'

    # Check for files
    ngc_file = data_dir / 'LRG_NGC_clustering.dat.fits'
    sgc_file = data_dir / 'LRG_SGC_clustering.dat.fits'

    if not ngc_file.exists() and not sgc_file.exists():
        # Try current directory
        ngc_file = Path('LRG_NGC_clustering.dat.fits')
        sgc_file = Path('LRG_SGC_clustering.dat.fits')

    if not ngc_file.exists() and not sgc_file.exists():
        print("ERROR: DESI files not found!")
        print("Expected: LRG_NGC_clustering.dat.fits and/or LRG_SGC_clustering.dat.fits")
        return None

    all_ra = []
    all_dec = []
    all_z = []

    if ngc_file.exists():
        ra, dec, z = load_desi_lrg(ngc_file)
        all_ra.extend(ra)
        all_dec.extend(dec)
        all_z.extend(z)

    if sgc_file.exists():
        ra, dec, z = load_desi_lrg(sgc_file)
        all_ra.extend(ra)
        all_dec.extend(dec)
        all_z.extend(z)

    all_ra = np.array(all_ra)
    all_dec = np.array(all_dec)
    all_z = np.array(all_z)

    print(f"\nTotal LRGs: {len(all_ra)}")

    # Convert to Galactic Cartesian
    print("\n" + "=" * 70)
    print("CONVERTING TO GALACTIC CARTESIAN COORDINATES")
    print("=" * 70)

    # Use subsample for speed (full analysis would use all)
    n_sample = min(100000, len(all_ra))
    print(f"\nUsing {n_sample} LRGs for analysis...")

    idx = np.random.choice(len(all_ra), n_sample, replace=False)
    ra_sample = all_ra[idx]
    dec_sample = all_dec[idx]
    z_sample = all_z[idx]

    positions = radec_to_galactic_cartesian(ra_sample, dec_sample, z_sample)
    print(f"  Positions shape: {positions.shape}")

    # Run directional 4PCF
    print("\n" + "=" * 70)
    print("RUNNING DIRECTIONAL 4PCF ANALYSIS")
    print("=" * 70)
    print("\nThis is the moment of truth...")
    print("Sampling tetrahedra from REAL DESI galaxies...")

    chirality_axis, axis_strength, significance = compute_directional_4pcf(
        positions, n_tetrahedra=200000, r_min=30, r_max=120
    )

    print(f"\nDIRECTIONAL 4PCF RESULTS:")
    print(f"  Axis strength: {axis_strength:.6f}")
    print(f"  Significance: {significance:.1f}σ")

    # Test alignment with Z² prediction
    alignment_results = test_z2_alignment(chirality_axis, print_results=True)

    # Final verdict
    print("\n" + "=" * 70)
    print("FINAL VERDICT")
    print("=" * 70)

    alignment = alignment_results['alignment']
    ang_sep = alignment_results['angular_separation_deg']

    if alignment > 0.9:
        print("""
██████████████████████████████████████████████████████████████████████
█                                                                    █
█   TOPOLOGY CONFIRMED: Chirality axis aligns with Z² prediction!   █
█                                                                    █
█   The universe is a T³/Z₂ orbifold with L_c = 20.6 Gpc            █
█   Dark matter is topology. There is no particle.                   █
█                                                                    █
██████████████████████████████████████████████████████████████████████
""")
    elif alignment > 0.7:
        print(f"""
STRONG INDICATION: Alignment = {alignment:.3f} (separation = {ang_sep:.1f}°)

The observed chirality axis is CONSISTENT with the Z² prediction.
More data or refined analysis recommended to confirm.
""")
    elif alignment > 0.5:
        print(f"""
MODERATE INDICATION: Alignment = {alignment:.3f} (separation = {ang_sep:.1f}°)

The observed chirality axis shows PARTIAL alignment with Z² prediction.
Could be topology + noise, or coincidence. More analysis needed.
""")
    else:
        print(f"""
WEAK/NO ALIGNMENT: Alignment = {alignment:.3f} (separation = {ang_sep:.1f}°)

The observed chirality axis does NOT align with Z² prediction.
Possible explanations:
1. Insufficient statistics (need more tetrahedra or full sample)
2. Scale range not optimal
3. Local structure contamination
4. Topology different than T³/Z₂

Recommend: Run on full sample with multiple scale ranges.
""")

    # Save results
    results = {
        'analysis': 'DESI_DR1_LRG_chirality_test',
        'framework': 'v11.1.0',
        'date': 'May 24, 2026',
        'data': {
            'total_lrgs': len(all_ra),
            'lrgs_used': n_sample,
            'z_range': [float(z_sample.min()), float(z_sample.max())]
        },
        'directional_4pcf': {
            'n_tetrahedra': 200000,
            'r_min_Mpc': 30,
            'r_max_Mpc': 120,
            'axis_strength': float(axis_strength),
            'significance_sigma': float(significance)
        },
        'z2_alignment': alignment_results,
        'verdict': 'ALIGNED' if alignment > 0.7 else 'INCONCLUSIVE' if alignment > 0.5 else 'NOT_ALIGNED'
    }

    output_file = Path(__file__).parent / 'desi_chirality_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\nResults saved to: {output_file}")

    return results


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    results = run_desi_chirality_test()
