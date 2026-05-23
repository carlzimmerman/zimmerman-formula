#!/bin/bash
#
# Build encore from source and run on DESI data
#

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================"
echo "BUILD AND RUN ENCORE"
echo "========================================"

# Prepare input data first
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

            # Subsample to 30k for speed
            n = min(30000, len(ra))
            idx = np.random.choice(len(ra), n, replace=False)
            ra, dec, z = ra[idx], dec[idx], z[idx]

            # Convert to Cartesian
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

            # Write
            output = f"desi_{region.lower()}_input.dat"
            with open(output, 'w') as f:
                for i in range(len(x)):
                    f.write(f"{x[i]:.6f} {y[i]:.6f} {z_cart[i]:.6f} 1.0\n")

            print(f"  Wrote {len(x)} galaxies to {output}")
            break

print("Data preparation complete!")
PYTHON_SCRIPT

# Create a Dockerfile that builds encore
echo ""
echo "Building Docker image with encore..."

cat > Dockerfile.build << 'EOF'
FROM --platform=linux/amd64 ubuntu:22.04

RUN apt-get update && apt-get install -y \
    build-essential \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy encore source
COPY encore/ /build/encore/

WORKDIR /build/encore

# Create a CPU-only Makefile
RUN echo 'CXX = g++ -std=c++0x -ffast-math -fopenmp -Wall' > Makefile.cpu && \
    echo 'CXXFLAGS = -O3 -DOPENMP -DFOURPCF -DALLPARITY' >> Makefile.cpu && \
    echo '' >> Makefile.cpu && \
    echo 'encore: encore.cpp' >> Makefile.cpu && \
    echo '	$(CXX) $(CXXFLAGS) encore.cpp -o encore' >> Makefile.cpu

# Try to build (may fail due to missing CMASM.o, but try anyway)
RUN make -f Makefile.cpu 2>&1 || echo "Build may have issues, checking..."
RUN ls -la encore 2>/dev/null || echo "encore binary not created"

WORKDIR /work
EOF

docker build --platform linux/amd64 -f Dockerfile.build -t encore-build . 2>&1 | tail -20

# Check if build succeeded
echo ""
echo "Checking build result..."
docker run --rm --platform linux/amd64 encore-build ls -la /build/encore/encore 2>&1 || echo "Build failed, trying alternative..."

# If build fails, try running the original with dummy CUDA libs
echo ""
echo "Attempting to run with library stubs..."

cat > Dockerfile.run << 'EOF'
FROM --platform=linux/amd64 ubuntu:22.04

RUN apt-get update && apt-get install -y libgomp1 && rm -rf /var/lib/apt/lists/*

# Create dummy CUDA runtime
RUN mkdir -p /usr/local/cuda/lib64 && \
    touch /usr/local/cuda/lib64/libcudart.so.11.0 && \
    ldconfig /usr/local/cuda/lib64 2>/dev/null || true

WORKDIR /work
EOF

docker build --platform linux/amd64 -f Dockerfile.run -t encore-run . 2>&1

echo ""
echo "Attempting to run encore..."
docker run --rm --platform linux/amd64 \
    -v "$SCRIPT_DIR/encore:/encore:ro" \
    -v "$SCRIPT_DIR:/data" \
    -w /data \
    encore-run \
    bash -c "export LD_LIBRARY_PATH=/usr/local/cuda/lib64:\$LD_LIBRARY_PATH && /encore/encore -def 2>&1 || echo 'Encore failed - needs recompilation'"

echo ""
echo "========================================"
echo "If encore runs, output will be in output/"
echo "========================================"
