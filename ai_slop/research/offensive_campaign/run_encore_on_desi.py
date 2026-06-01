#!/usr/bin/env python3
"""
RUN ENCORE ON DESI LRG DATA
===========================

Prepare DESI DR1 LRG catalogs for encore NPCF computation.

Steps:
1. Load DESI LRG catalogs
2. Convert to encore input format (x, y, z, weight)
3. Run encore to compute 4PCF
4. Analyze parity-odd signal

Author: Claude Opus 4.5
Date: May 24, 2026
"""

import numpy as np
from pathlib import Path
import subprocess
import os
from astropy.io import fits
from astropy.coordinates import SkyCoord
import astropy.units as u


def load_desi_catalog(filepath: Path) -> tuple:
    """Load DESI LRG catalog and extract positions/weights."""
    print(f"Loading {filepath.name}...")

    with fits.open(filepath) as hdul:
        data = hdul[1].data
        ra = data['RA']
        dec = data['DEC']
        z = data['Z']

        # Check for weights
        if 'WEIGHT' in data.names:
            weight = data['WEIGHT']
        else:
            weight = np.ones(len(ra))

    return ra, dec, z, weight


def radec_z_to_cartesian(ra, dec, z, H0=70, Om0=0.315):
    """Convert RA/Dec/z to comoving Cartesian coordinates."""
    from astropy.cosmology import FlatLambdaCDM

    cosmo = FlatLambdaCDM(H0=H0, Om0=Om0)

    # Convert to Galactic coordinates
    coords = SkyCoord(ra=ra*u.deg, dec=dec*u.deg, frame='icrs')

    # Comoving distance in Mpc/h
    D_c = cosmo.comoving_distance(z).value * H0 / 100

    # Cartesian (using RA/Dec directly for simplicity)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = D_c * np.cos(dec_rad) * np.cos(ra_rad)
    y = D_c * np.cos(dec_rad) * np.sin(ra_rad)
    z_cart = D_c * np.sin(dec_rad)

    return x, y, z_cart


def write_encore_input(x, y, z, w, output_file: Path, subsample: int = None):
    """Write positions to encore input format (x y z w)."""

    if subsample and len(x) > subsample:
        idx = np.random.choice(len(x), subsample, replace=False)
        x, y, z, w = x[idx], y[idx], z[idx], w[idx]

    print(f"Writing {len(x)} particles to {output_file}...")

    with open(output_file, 'w') as f:
        for i in range(len(x)):
            f.write(f"{x[i]:.6f} {y[i]:.6f} {z[i]:.6f} {w[i]:.6f}\n")

    return len(x)


def compute_box_size(x, y, z):
    """Compute bounding box for the data."""
    x_range = x.max() - x.min()
    y_range = y.max() - y.min()
    z_range = z.max() - z.min()

    # Add padding
    box_size = max(x_range, y_range, z_range) * 1.1

    return box_size


def run_encore(input_file: Path, output_str: str, box_size: float,
               r_min: float = 20, r_max: float = 160):
    """Run encore on the input file."""
    encore_path = Path(__file__).parent / "encore" / "encore"

    if not encore_path.exists():
        print(f"ERROR: encore binary not found at {encore_path}")
        print("Please compile encore first:")
        print("  cd encore && make")
        return False

    # Build command
    cmd = [
        str(encore_path),
        "-in", str(input_file),
        "-outstr", output_str,
        "-box", str(box_size),
        "-rmin", str(r_min),
        "-rmax", str(r_max),
        "-nside", "50"
    ]

    print(f"\nRunning encore...")
    print(f"  Command: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
        print(result.stdout)
        if result.returncode != 0:
            print(f"ERROR: {result.stderr}")
            return False
        return True
    except subprocess.TimeoutExpired:
        print("ERROR: encore timed out")
        return False
    except Exception as e:
        print(f"ERROR: {e}")
        return False


def prepare_desi_for_encore():
    """Main function to prepare DESI data for encore analysis."""
    print("=" * 70)
    print("PREPARING DESI DR1 LRG DATA FOR ENCORE 4PCF")
    print("=" * 70)

    data_dir = Path(__file__).parent

    # Find DESI catalogs
    desi_files = []
    for subdir in [data_dir, data_dir / "desi_data"]:
        for fname in ["LRG_NGC_clustering.dat.fits", "LRG_SGC_clustering.dat.fits"]:
            fpath = subdir / fname
            if fpath.exists():
                desi_files.append(fpath)

    if not desi_files:
        print("ERROR: DESI LRG catalogs not found")
        return None

    print(f"\nFound {len(desi_files)} DESI catalogs")

    # Process each catalog separately (NGC and SGC)
    results = {}

    for fpath in desi_files:
        region = "NGC" if "NGC" in fpath.name else "SGC"
        print(f"\n{'=' * 60}")
        print(f"Processing {region}")
        print("=" * 60)

        # Load data
        ra, dec, z, w = load_desi_catalog(fpath)
        print(f"  Loaded {len(ra)} galaxies")

        # Convert to Cartesian
        print("  Converting to Cartesian...")
        x, y, z_cart = radec_z_to_cartesian(ra, dec, z)

        # Compute box size
        box_size = compute_box_size(x, y, z_cart)
        print(f"  Box size: {box_size:.1f} Mpc/h")

        # For testing, use a subsample
        n_sample = min(100000, len(x))
        print(f"  Using {n_sample} galaxy subsample")

        # Write input file
        input_file = data_dir / f"desi_{region.lower()}_encore_input.dat"
        n_written = write_encore_input(x, y, z_cart, w, input_file, subsample=n_sample)

        results[region] = {
            'input_file': str(input_file),
            'n_galaxies': n_written,
            'box_size': float(box_size)
        }

        # Try to run encore
        print(f"\n  Attempting to run encore on {region}...")
        output_str = f"desi_{region.lower()}"
        success = run_encore(input_file, output_str, box_size)

        if success:
            print(f"  SUCCESS: encore completed for {region}")
            results[region]['encore_success'] = True
        else:
            print(f"  NOTE: encore not available or failed")
            results[region]['encore_success'] = False
            print(f"  Input file ready at: {input_file}")
            print(f"  To run manually:")
            print(f"    ./encore/encore -in {input_file} -outstr {output_str} -box {box_size:.0f}")

    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)

    for region, info in results.items():
        print(f"\n{region}:")
        print(f"  Galaxies: {info['n_galaxies']}")
        print(f"  Input file: {info['input_file']}")
        if info.get('encore_success'):
            print(f"  4PCF computed: output/{info['input_file'].split('/')[-1].replace('_input.dat', '')}_4pcf.txt")

    return results


if __name__ == "__main__":
    results = prepare_desi_for_encore()
