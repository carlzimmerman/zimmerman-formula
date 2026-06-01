#!/usr/bin/env python3
"""
=============================================================================
DESI DATA EXPORTER - Convert Real DESI LRG Data for Digital Twin
=============================================================================

Converts DESI DR1 Luminous Red Galaxy (LRG) coordinates to JSON format
for precise visualization in the T³/Z₂ Digital Twin.

Input: DESI encore-format .dat files (X, Y, Z in Mpc/h, weight)
Output: JSON with coordinates in Gpc for WebGL rendering

=============================================================================
"""

import numpy as np
import json
import os
from datetime import datetime

# =============================================================================
# CONSTANTS
# =============================================================================

# Planck 2018 cosmology
H0 = 67.4  # km/s/Mpc
h = H0 / 100  # = 0.674

# Fundamental domain
L_C_GPC = 20.6
HALF_BOX = L_C_GPC / 2

# =============================================================================
# DATA LOADING
# =============================================================================

def load_desi_dat(filepath, max_galaxies=None):
    """
    Load DESI encore-format .dat file.

    Format: X Y Z weight (in Mpc/h)

    Returns coordinates in Gpc (physical, not comoving/h).
    """
    print(f"Loading {filepath}...")

    data = np.loadtxt(filepath)

    if max_galaxies and len(data) > max_galaxies:
        # Random sample to reduce size
        indices = np.random.choice(len(data), max_galaxies, replace=False)
        data = data[indices]

    # Extract coordinates (Mpc/h)
    x_mpc_h = data[:, 0]
    y_mpc_h = data[:, 1]
    z_mpc_h = data[:, 2]
    weights = data[:, 3] if data.shape[1] > 3 else np.ones(len(data))

    # Convert Mpc/h to Gpc (physical)
    # Mpc/h → Mpc → Gpc: divide by h, then divide by 1000
    x_gpc = x_mpc_h / h / 1000
    y_gpc = y_mpc_h / h / 1000
    z_gpc = z_mpc_h / h / 1000

    print(f"  Loaded {len(x_gpc)} galaxies")
    print(f"  X range: [{x_gpc.min():.3f}, {x_gpc.max():.3f}] Gpc")
    print(f"  Y range: [{y_gpc.min():.3f}, {y_gpc.max():.3f}] Gpc")
    print(f"  Z range: [{z_gpc.min():.3f}, {z_gpc.max():.3f}] Gpc")

    return {
        'x': x_gpc,
        'y': y_gpc,
        'z': z_gpc,
        'weights': weights,
        'count': len(x_gpc)
    }


def apply_t3_wrapping(x, y, z):
    """
    Apply T³ topology wrapping to keep coordinates within fundamental domain.
    """
    def wrap(val):
        return ((val + HALF_BOX) % L_C_GPC + L_C_GPC) % L_C_GPC - HALF_BOX

    return wrap(x), wrap(y), wrap(z)


def compute_statistics(data):
    """
    Compute statistics for the dataset.
    """
    x, y, z = data['x'], data['y'], data['z']

    # Distance from origin
    r = np.sqrt(x**2 + y**2 + z**2)

    return {
        'count': int(data['count']),
        'x_range_gpc': [float(x.min()), float(x.max())],
        'y_range_gpc': [float(y.min()), float(y.max())],
        'z_range_gpc': [float(z.min()), float(z.max())],
        'r_range_gpc': [float(r.min()), float(r.max())],
        'r_mean_gpc': float(r.mean()),
        'r_std_gpc': float(r.std()),
    }


# =============================================================================
# EXPORT FUNCTIONS
# =============================================================================

def export_for_webgl(ngc_data, sgc_data, output_path, downsample_factor=1):
    """
    Export DESI data in WebGL-friendly JSON format.

    Parameters:
    -----------
    downsample_factor : int
        Keep every Nth galaxy (1 = all, 10 = 10%)
    """
    # Combine NGC and SGC
    x = np.concatenate([ngc_data['x'], sgc_data['x']])
    y = np.concatenate([ngc_data['y'], sgc_data['y']])
    z = np.concatenate([ngc_data['z'], sgc_data['z']])

    # Downsample if needed
    if downsample_factor > 1:
        indices = np.arange(0, len(x), downsample_factor)
        x, y, z = x[indices], y[indices], z[indices]

    # Apply T³ wrapping
    x, y, z = apply_t3_wrapping(x, y, z)

    print(f"\nExporting {len(x)} galaxies...")

    # Create output structure
    output = {
        'metadata': {
            'source': 'DESI DR1 LRG Catalog',
            'regions': ['NGC', 'SGC'],
            'extraction_date': datetime.now().isoformat(),
            'cosmology': {
                'h': h,
                'H0_km_s_Mpc': H0,
            },
            'topology': {
                'fundamental_domain_gpc': L_C_GPC,
                'half_box_gpc': HALF_BOX,
                't3_wrapping_applied': True,
            },
            'downsample_factor': downsample_factor,
        },
        'statistics': {
            'total_count': int(len(x)),
            'ngc_count': int(ngc_data['count']),
            'sgc_count': int(sgc_data['count']),
            'x_range_gpc': [float(x.min()), float(x.max())],
            'y_range_gpc': [float(y.min()), float(y.max())],
            'z_range_gpc': [float(z.min()), float(z.max())],
        },
        'galaxies': {
            'x': x.tolist(),
            'y': y.tolist(),
            'z': z.tolist(),
        }
    }

    # Save
    with open(output_path, 'w') as f:
        json.dump(output, f)

    file_size_mb = os.path.getsize(output_path) / 1024 / 1024
    print(f"Saved: {output_path} ({file_size_mb:.1f} MB)")

    return output


def export_binary_for_webgl(ngc_data, sgc_data, output_dir, downsample_factor=1):
    """
    Export DESI data in binary format for faster WebGL loading.
    Creates Float32Array-compatible .bin file.
    """
    # Combine NGC and SGC
    x = np.concatenate([ngc_data['x'], sgc_data['x']])
    y = np.concatenate([ngc_data['y'], sgc_data['y']])
    z = np.concatenate([ngc_data['z'], sgc_data['z']])

    # Downsample if needed
    if downsample_factor > 1:
        indices = np.arange(0, len(x), downsample_factor)
        x, y, z = x[indices], y[indices], z[indices]

    # Apply T³ wrapping
    x, y, z = apply_t3_wrapping(x, y, z)

    # Interleave as [x0,y0,z0, x1,y1,z1, ...]
    positions = np.zeros(len(x) * 3, dtype=np.float32)
    positions[0::3] = x
    positions[1::3] = y
    positions[2::3] = z

    # Save binary
    bin_path = os.path.join(output_dir, 'desi_galaxies.bin')
    positions.tofile(bin_path)

    # Save metadata JSON
    meta = {
        'format': 'Float32Array',
        'stride': 3,
        'count': len(x),
        'total_bytes': len(positions) * 4,
        'source': 'DESI DR1 LRG',
        't3_wrapping_applied': True,
    }
    meta_path = os.path.join(output_dir, 'desi_galaxies.json')
    with open(meta_path, 'w') as f:
        json.dump(meta, f, indent=2)

    print(f"Saved binary: {bin_path} ({len(positions) * 4 / 1024 / 1024:.1f} MB)")
    print(f"Saved metadata: {meta_path}")

    return meta


# =============================================================================
# MAIN
# =============================================================================

def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))

    print("=" * 60)
    print("DESI DATA EXPORT FOR T³/Z₂ DIGITAL TWIN")
    print("=" * 60)

    # Load NGC and SGC data
    # Use full samples for best precision
    ngc_path = os.path.join(base_dir, 'desi_ngc_full_input.dat')
    sgc_path = os.path.join(base_dir, 'desi_sgc_full_input.dat')

    # Check if full files exist, otherwise use smaller samples
    if not os.path.exists(ngc_path):
        ngc_path = os.path.join(base_dir, 'desi_ngc_input.dat')
        sgc_path = os.path.join(base_dir, 'desi_sgc_input.dat')

    ngc_data = load_desi_dat(ngc_path)
    sgc_data = load_desi_dat(sgc_path)

    # Export for website (downsampled for performance)
    website_data_dir = os.path.join(base_dir, '..', '..', 'website', 'public', 'data')
    os.makedirs(website_data_dir, exist_ok=True)

    # Full JSON (for detailed analysis)
    json_path = os.path.join(website_data_dir, 'desi_galaxies.json')
    export_for_webgl(ngc_data, sgc_data, json_path, downsample_factor=4)

    # Binary format (for fast WebGL loading)
    export_binary_for_webgl(ngc_data, sgc_data, website_data_dir, downsample_factor=4)

    print("\n" + "=" * 60)
    print("EXPORT COMPLETE")
    print("=" * 60)
    print(f"""
Real DESI DR1 LRG galaxies exported for Digital Twin:
- JSON format: {json_path}
- Binary format: {website_data_dir}/desi_galaxies.bin

Total galaxies: {ngc_data['count'] + sgc_data['count']}
Exported (downsampled 4x): {(ngc_data['count'] + sgc_data['count']) // 4}

These are REAL observed galaxy positions from DESI,
not procedurally generated data.
""")


if __name__ == "__main__":
    main()
