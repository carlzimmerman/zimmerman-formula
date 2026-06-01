#!/bin/bash
#
# Run encore in Docker container on Mac
#
# This script:
# 1. Builds a Docker container with encore compiled for Linux
# 2. Mounts the DESI data
# 3. Runs the 4PCF computation
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "ENCORE IN DOCKER"
echo "========================================"

# Check Docker is available
if ! command -v docker &> /dev/null; then
    echo "ERROR: Docker not found"
    echo "Please install Docker Desktop for Mac"
    exit 1
fi

# Build the container
echo ""
echo "Building Docker container..."
docker build -f Dockerfile.encore -t encore-z2 .

# Prepare input data
echo ""
echo "Preparing DESI data for encore..."

# Create input file from DESI catalog
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

            # Subsample to 100k
            n = min(100000, len(ra))
            idx = np.random.choice(len(ra), n, replace=False)
            ra, dec, z = ra[idx], dec[idx], z[idx]

            # Convert to Cartesian
            D_c = cosmo.comoving_distance(z).value
            ra_rad = np.radians(ra)
            dec_rad = np.radians(dec)

            x = D_c * np.cos(dec_rad) * np.cos(ra_rad)
            y = D_c * np.cos(dec_rad) * np.sin(ra_rad)
            z_cart = D_c * np.sin(dec_rad)

            # Write encore input
            output = f"desi_{region.lower()}_input.dat"
            with open(output, 'w') as f:
                for i in range(len(x)):
                    f.write(f"{x[i]:.6f} {y[i]:.6f} {z_cart[i]:.6f} 1.0\n")

            print(f"  Wrote {len(x)} galaxies to {output}")
            break

print("Data preparation complete!")
PYTHON_SCRIPT

# Compute box size
BOX_SIZE=4000  # Mpc/h, conservative for z~0.5 LRGs

# Run encore in container
echo ""
echo "Running encore on NGC..."
docker run --rm -v "$SCRIPT_DIR:/work" encore-z2 \
    /work/encore/encore \
    -in /work/desi_ngc_input.dat \
    -outstr desi_ngc \
    -box $BOX_SIZE \
    -rmin 20 \
    -rmax 160 \
    -nside 30

echo ""
echo "Running encore on SGC..."
docker run --rm -v "$SCRIPT_DIR:/work" encore-z2 \
    /work/encore/encore \
    -in /work/desi_sgc_input.dat \
    -outstr desi_sgc \
    -box $BOX_SIZE \
    -rmin 20 \
    -rmax 160 \
    -nside 30

echo ""
echo "========================================"
echo "ENCORE COMPLETE"
echo "========================================"
echo ""
echo "Output files:"
echo "  output/desi_ngc_4pcf.txt"
echo "  output/desi_sgc_4pcf.txt"
echo ""
echo "Run the analysis:"
echo "  python3 proper_parity_odd_4pcf_analysis.py"
