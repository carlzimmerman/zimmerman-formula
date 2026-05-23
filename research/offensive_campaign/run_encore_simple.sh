#!/bin/bash
#
# Run pre-compiled encore in Docker
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "RUNNING ENCORE IN LINUX CONTAINER"
echo "========================================"

# Prepare input data
echo ""
echo "Preparing DESI data..."

python3 << 'PYTHON_SCRIPT'
import numpy as np
from pathlib import Path
from astropy.io import fits
from astropy.cosmology import FlatLambdaCDM

data_dir = Path(".")
cosmo = FlatLambdaCDM(H0=70, Om0=0.315)

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

            # Subsample to 50k for speed
            n = min(50000, len(ra))
            idx = np.random.choice(len(ra), n, replace=False)
            ra, dec, z = ra[idx], dec[idx], z[idx]

            # Convert to Cartesian
            D_c = cosmo.comoving_distance(z).value
            ra_rad = np.radians(ra)
            dec_rad = np.radians(dec)

            x = D_c * np.cos(dec_rad) * np.cos(ra_rad)
            y = D_c * np.cos(dec_rad) * np.sin(ra_rad)
            z_cart = D_c * np.sin(dec_rad)

            # Compute box size
            box_x = x.max() - x.min()
            box_y = y.max() - y.min()
            box_z = z_cart.max() - z_cart.min()
            box_size = max(box_x, box_y, box_z) * 1.2

            # Shift to positive coordinates
            x = x - x.min() + 10
            y = y - y.min() + 10
            z_cart = z_cart - z_cart.min() + 10

            # Write encore input
            output = f"desi_{region.lower()}_input.dat"
            with open(output, 'w') as f:
                for i in range(len(x)):
                    f.write(f"{x[i]:.6f} {y[i]:.6f} {z_cart[i]:.6f} 1.0\n")

            print(f"  Wrote {len(x)} galaxies to {output}")
            print(f"  Box size: {box_size:.0f} Mpc/h")
            break

print("Data preparation complete!")
PYTHON_SCRIPT

# Run using Docker with Ubuntu and the pre-built binary
echo ""
echo "Running encore on NGC in Docker..."

docker run --rm --platform linux/amd64 \
    -v "$SCRIPT_DIR/encore:/encore:ro" \
    -v "$SCRIPT_DIR:/data" \
    -w /data \
    ubuntu:22.04 \
    /encore/encore \
    -in /data/desi_ngc_input.dat \
    -outstr desi_ngc \
    -box 3500 \
    -rmin 20 \
    -rmax 160 \
    -nside 25

echo ""
echo "Running encore on SGC in Docker..."

docker run --rm --platform linux/amd64 \
    -v "$SCRIPT_DIR/encore:/encore:ro" \
    -v "$SCRIPT_DIR:/data" \
    -w /data \
    ubuntu:22.04 \
    /encore/encore \
    -in /data/desi_sgc_input.dat \
    -outstr desi_sgc \
    -box 3500 \
    -rmin 20 \
    -rmax 160 \
    -nside 25

echo ""
echo "========================================"
echo "ENCORE COMPLETE"
echo "========================================"
ls -la output/*.txt 2>/dev/null || echo "Check output/ directory"
