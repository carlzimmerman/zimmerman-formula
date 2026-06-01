#!/usr/bin/env python3
"""
Prepare full DESI sample for encore.
"""

import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM

data_dir = Path(__file__).parent
cosmo = FlatLambdaCDM(H0=70, Om0=0.315)

# Use larger samples - 200k each for better statistics
N_SAMPLE = 200000

for region in ["NGC", "SGC"]:
    for subdir in [data_dir, data_dir / "desi_data"]:
        fpath = subdir / f"LRG_{region}_clustering.dat.fits"
        if fpath.exists():
            print(f"Processing {fpath.name}...")

            with fits.open(fpath) as hdul:
                data = hdul[1].data
                ra = data['RA']
                dec = data['DEC']
                z = data['Z']

            print(f"  Total galaxies: {len(ra)}")

            # Subsample
            n = min(N_SAMPLE, len(ra))
            print(f"  Using {n} galaxies")

            np.random.seed(42 if region == "NGC" else 43)
            idx = np.random.choice(len(ra), n, replace=False)
            ra, dec, z = ra[idx], dec[idx], z[idx]

            # Convert to Cartesian
            print("  Computing comoving distances...")
            D_c = cosmo.comoving_distance(z).value
            ra_rad = np.radians(ra)
            dec_rad = np.radians(dec)

            x = D_c * np.cos(dec_rad) * np.cos(ra_rad)
            y = D_c * np.cos(dec_rad) * np.sin(ra_rad)
            z_cart = D_c * np.sin(dec_rad)

            # Shift to positive
            x = x - x.min() + 10
            y = y - y.min() + 10
            z_cart = z_cart - z_cart.min() + 10

            # Compute box
            box = max(x.max(), y.max(), z_cart.max()) + 10
            print(f"  Box size: {box:.0f} Mpc/h")

            # Write
            output = data_dir / f"desi_{region.lower()}_full_input.dat"
            print(f"  Writing to {output}...")
            with open(output, 'w') as f:
                for i in range(len(x)):
                    f.write(f"{x[i]:.6f} {y[i]:.6f} {z_cart[i]:.6f} 1.0\n")

            print(f"  Done: {n} galaxies")
            break

print("\nData preparation complete!")
print("Run encore with:")
print("  ./encore_macos -in ../desi_ngc_full_input.dat -outstr desi_ngc_full -box 6500 -rmin 20 -rmax 160 -nside 40")
