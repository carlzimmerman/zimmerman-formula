#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER XX: Z² UNIVERSAL COORDINATE TRANSFORMER
================================================================================

PURPOSE: Convert all raw astronomical measurements into the unified Z²
Cartesian coordinate system within the 20.6 Gpc fundamental domain.

The key transformation steps:
1. Convert raw measurements (z, parallax, μ) to comoving distance D_c
2. Subtract local topological bulk flow (265 km/s) for cosmological z
3. Integrate Z² geometric Dark Energy equation for D_c(z)
4. Convert (RA, Dec, D_c) to (x, y, z) Cartesian
5. Apply T³ orbifold wrapping: |coordinate| < L_c/2 = 10.3 Gpc

OUTPUT: z2_master_coordinates.bin (Float32Array for WebGL)

Author: Z² Offensive Campaign
Date: 2026-05-24
================================================================================
"""

import numpy as np
import pandas as pd
from pathlib import Path
from datetime import datetime
import json
import struct
import warnings
warnings.filterwarnings('ignore')

from scipy.integrate import quad

OUTPUT_DIR = Path(__file__).parent

# =============================================================================
# Z² COSMOLOGICAL PARAMETERS (LOCKED)
# =============================================================================

# Fundamental constants
C_KMS = 299792.458          # Speed of light in km/s
H0 = 67.4                   # Hubble constant km/s/Mpc

# Z² topological parameters
L_C_MPC = 20600             # Fundamental domain size
L_C_HALF = L_C_MPC / 2      # Half-box (boundary at ±10.3 Gpc)

# Z² matter/energy fractions
OMEGA_M = 6 / 19            # = 0.3158
OMEGA_LAMBDA = 13 / 19      # = 0.6842
OMEGA_R = 5e-5              # Radiation (negligible at low z)

# Topological bulk flow (local motion correction)
V_BULK_KMS = 265            # km/s toward vertex

print("="*70)
print("WORK-ORDER XX: Z² UNIVERSAL COORDINATE TRANSFORMER")
print("="*70)
print(f"\nZ² PARAMETERS:")
print(f"  L_c = {L_C_MPC:,} Mpc")
print(f"  Ω_m = {OMEGA_M:.4f} (6/19)")
print(f"  Ω_Λ = {OMEGA_LAMBDA:.4f} (13/19)")
print(f"  v_bulk = {V_BULK_KMS} km/s")


# =============================================================================
# DISTANCE CALCULATIONS
# =============================================================================

def z2_hubble(z, D_c):
    """
    Z² modified Hubble parameter with geometric Dark Energy.

    H(z) = H₀ √[Ω_m(1+z)³ + Ω_r(1+z)⁴ + Ω_Λ_eff(D_c)]

    where Ω_Λ_eff = (13/19) × [1 - (D_c/L_c)³]
    accounts for the topological boundary.
    """
    # Geometric dark energy correction (diminishes near boundary)
    boundary_factor = 1 - (D_c / L_C_MPC)**3 if D_c < L_C_MPC else 0

    omega_lambda_eff = OMEGA_LAMBDA * max(0, boundary_factor)

    H_squared = OMEGA_M * (1 + z)**3 + OMEGA_R * (1 + z)**4 + omega_lambda_eff

    return H0 * np.sqrt(max(H_squared, 0.01))


def comoving_distance_z2(z_cosmo):
    """
    Compute comoving distance using Z² cosmology.

    D_c = c ∫[0 to z] dz' / H(z')

    Uses iterative integration since H depends on D_c.
    """
    if z_cosmo <= 0:
        return 0

    # For low z, use standard approximation
    if z_cosmo < 0.1:
        return C_KMS * z_cosmo / H0

    # Iterative integration
    D_c = C_KMS * z_cosmo / H0  # Initial guess

    for _ in range(5):  # Converges quickly
        def integrand(z_prime):
            # Estimate D_c at z' by linear interpolation
            D_at_z = D_c * z_prime / z_cosmo
            return 1.0 / z2_hubble(z_prime, D_at_z)

        D_c, _ = quad(integrand, 0, z_cosmo, limit=100)
        D_c *= C_KMS

    return min(D_c, L_C_MPC * 0.99)  # Cap at boundary


def parallax_to_distance(parallax_mas):
    """Convert parallax (mas) to distance (Mpc)."""
    if parallax_mas <= 0:
        return 0
    distance_pc = 1000 / parallax_mas
    distance_mpc = distance_pc / 1e6
    return distance_mpc


def distance_modulus_to_distance(mu):
    """Convert distance modulus to distance (Mpc)."""
    distance_pc = 10 ** ((mu - 25) / 5 + 1)
    distance_mpc = distance_pc / 1e6
    return distance_mpc


def dispersion_measure_to_distance(dm):
    """
    Approximate distance from FRB dispersion measure.
    DM ~ 1000 pc/cm³ corresponds to z ~ 1 (very rough).
    """
    # Simple empirical relation
    z_approx = dm / 1000  # Very approximate
    return comoving_distance_z2(z_approx)


# =============================================================================
# COORDINATE TRANSFORMATIONS
# =============================================================================

def ra_dec_distance_to_cartesian(ra_deg, dec_deg, distance_mpc):
    """Convert (RA, Dec, D_c) to Cartesian (x, y, z)."""
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    x = distance_mpc * np.cos(dec_rad) * np.cos(ra_rad)
    y = distance_mpc * np.cos(dec_rad) * np.sin(ra_rad)
    z = distance_mpc * np.sin(dec_rad)

    return x, y, z


def apply_t3_wrapping(x, y, z):
    """
    Apply T³ fundamental domain boundary condition.

    Coordinates wrap at ±L_c/2 = ±10.3 Gpc using modular arithmetic.
    """
    def wrap(coord):
        # Shift to [0, L_c), then back to [-L_c/2, L_c/2)
        wrapped = ((coord + L_C_HALF) % L_C_MPC) - L_C_HALF
        return wrapped

    return wrap(x), wrap(y), wrap(z)


def correct_bulk_flow(ra_deg, dec_deg, z_obs):
    """
    Correct observed redshift for topological bulk flow.

    The local flow is 265 km/s toward the vertex.
    z_cosmo = z_obs - v_bulk × cos(θ) / c

    where θ is the angle to the flow direction.
    """
    # Flow direction (toward V1 Shapley)
    flow_l, flow_b = 276.4, 29.8

    # Convert to Cartesian for dot product
    flow_ra, flow_dec = galactic_to_equatorial(flow_l, flow_b)

    # Unit vectors
    obs_vec = np.array([
        np.cos(np.radians(dec_deg)) * np.cos(np.radians(ra_deg)),
        np.cos(np.radians(dec_deg)) * np.sin(np.radians(ra_deg)),
        np.sin(np.radians(dec_deg))
    ])

    flow_vec = np.array([
        np.cos(np.radians(flow_dec)) * np.cos(np.radians(flow_ra)),
        np.cos(np.radians(flow_dec)) * np.sin(np.radians(flow_ra)),
        np.sin(np.radians(flow_dec))
    ])

    cos_theta = np.dot(obs_vec, flow_vec)

    # Correction
    delta_z = V_BULK_KMS * cos_theta / C_KMS
    z_cosmo = z_obs - delta_z

    return max(z_cosmo, 0)


def galactic_to_equatorial(l_deg, b_deg):
    """Convert galactic to equatorial coordinates."""
    from astropy.coordinates import SkyCoord
    import astropy.units as u

    coord = SkyCoord(l=l_deg*u.deg, b=b_deg*u.deg, frame='galactic')
    eq = coord.icrs
    return float(eq.ra.deg), float(eq.dec.deg)


# =============================================================================
# MAIN TRANSFORMATION
# =============================================================================

def transform_catalog():
    """Transform universal catalog to Z² coordinates."""
    print("\n" + "-"*60)
    print("LOADING UNIVERSAL CATALOG")
    print("-"*60)

    input_path = OUTPUT_DIR / 'universal_raw_observations.parquet'
    if not input_path.exists():
        print(f"ERROR: {input_path} not found")
        return None

    df = pd.read_parquet(input_path)
    print(f"Loaded {len(df):,} observations")

    print("\n" + "-"*60)
    print("TRANSFORMING TO Z² COORDINATES")
    print("-"*60)

    # Initialize output arrays
    x_coords = np.zeros(len(df), dtype=np.float32)
    y_coords = np.zeros(len(df), dtype=np.float32)
    z_coords = np.zeros(len(df), dtype=np.float32)
    types = np.zeros(len(df), dtype=np.int32)

    # Process each measurement type differently
    for i, row in df.iterrows():
        ra = row['ra']
        dec = row['dec']
        raw = row['raw_measurement']
        mtype = row['measurement_type']
        mtype_id = row['measurement_type_id']

        # Convert raw measurement to comoving distance
        if mtype == 'SPECTROSCOPY':
            # Redshift → correct for bulk flow → comoving distance
            z_cosmo = correct_bulk_flow(ra, dec, raw)
            D_c = comoving_distance_z2(z_cosmo)

        elif mtype == 'PHOTOMETRY':
            # Distance modulus → distance
            D_c = distance_modulus_to_distance(raw)

        elif mtype == 'RADIO':
            # Dispersion measure → approximate distance
            D_c = dispersion_measure_to_distance(raw)

        elif mtype == 'XRAY':
            # Cluster redshift → comoving distance
            z_cosmo = correct_bulk_flow(ra, dec, raw)
            D_c = comoving_distance_z2(z_cosmo)

        elif mtype == 'ASTROMETRY':
            # Parallax → distance (very local, no bulk flow correction)
            D_c = parallax_to_distance(raw)

        elif mtype == 'MICROWAVE':
            # CMB features at last scattering surface
            D_c = L_C_HALF * 0.99  # Just inside boundary

        else:
            D_c = 0

        # Convert to Cartesian
        x, y, z = ra_dec_distance_to_cartesian(ra, dec, D_c)

        # Apply T³ wrapping
        x, y, z = apply_t3_wrapping(x, y, z)

        x_coords[i] = x
        y_coords[i] = y
        z_coords[i] = z
        types[i] = mtype_id

        if (i + 1) % 50000 == 0:
            print(f"  Processed {i+1:,}/{len(df):,} observations...")

    print(f"\nTransformation complete")

    # Statistics
    print(f"\nCoordinate ranges (Mpc):")
    print(f"  x: [{x_coords.min():.0f}, {x_coords.max():.0f}]")
    print(f"  y: [{y_coords.min():.0f}, {y_coords.max():.0f}]")
    print(f"  z: [{z_coords.min():.0f}, {z_coords.max():.0f}]")

    return x_coords, y_coords, z_coords, types


def export_binary(x, y, z, types):
    """Export as binary Float32Array for WebGL."""
    print("\n" + "-"*60)
    print("EXPORTING BINARY DATA")
    print("-"*60)

    n = len(x)

    # Pack as interleaved [x, y, z, type] for each point
    binary_data = bytearray()

    for i in range(n):
        # Pack x, y, z as float32, type as int32
        binary_data.extend(struct.pack('<f', x[i]))
        binary_data.extend(struct.pack('<f', y[i]))
        binary_data.extend(struct.pack('<f', z[i]))
        binary_data.extend(struct.pack('<i', types[i]))

    output_path = OUTPUT_DIR / 'z2_master_coordinates.bin'
    with open(output_path, 'wb') as f:
        f.write(binary_data)

    print(f"Exported: {output_path}")
    print(f"File size: {len(binary_data) / 1e6:.2f} MB")
    print(f"Points: {n:,}")
    print(f"Bytes per point: 16 (4×float32/int32)")

    # Also save JSON metadata
    metadata = {
        'n_points': n,
        'bytes_per_point': 16,
        'format': '[x: f32, y: f32, z: f32, type: i32] interleaved',
        'coordinate_system': 'Z² Cartesian (Mpc)',
        'box_size_mpc': L_C_MPC,
        'half_box_mpc': L_C_HALF,
        'measurement_types': {
            1: 'SPECTROSCOPY',
            2: 'PHOTOMETRY',
            3: 'RADIO',
            4: 'XRAY',
            5: 'ASTROMETRY',
            6: 'MICROWAVE'
        }
    }

    meta_path = OUTPUT_DIR / 'z2_master_coordinates_metadata.json'
    with open(meta_path, 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"Saved: {meta_path}")

    return output_path


def main():
    """Execute Work-Order XX."""

    # Transform catalog
    result = transform_catalog()

    if result is None:
        return None

    x, y, z, types = result

    # Export binary
    binary_path = export_binary(x, y, z, types)

    # Save results
    output = {
        'work_order': 'XX',
        'task': 'Z² Universal Coordinate Transformer',
        'date': datetime.now().isoformat(),
        'z2_parameters': {
            'L_c_Mpc': L_C_MPC,
            'Omega_m': float(OMEGA_M),
            'Omega_Lambda': float(OMEGA_LAMBDA),
            'v_bulk_kms': V_BULK_KMS
        },
        'output': {
            'binary_file': str(binary_path),
            'n_points': len(x),
            'coord_ranges_mpc': {
                'x': [float(x.min()), float(x.max())],
                'y': [float(y.min()), float(y.max())],
                'z': [float(z.min()), float(z.max())]
            }
        }
    }

    json_path = OUTPUT_DIR / 'WORK_ORDER_XX_results.json'
    with open(json_path, 'w') as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved: {json_path}")

    print("\n" + "="*70)
    print("WORK-ORDER XX: COMPLETE")
    print("="*70)
    print(f"""
┌──────────────────────────────────────────────────────────────────────┐
│           WORK-ORDER XX: Z² COORDINATE TRANSFORMER COMPLETE           │
├──────────────────────────────────────────────────────────────────────┤
│                                                                       │
│  TRANSFORMED: {len(x):>10,} observations                                    │
│                                                                       │
│  COORDINATE SYSTEM:                                                   │
│    • Origin: Earth                                                    │
│    • Units: Mpc                                                       │
│    • Box size: {L_C_MPC:,} Mpc = 20.6 Gpc                                │
│    • T³ boundary wrapping: ±{L_C_HALF:,.0f} Mpc                             │
│                                                                       │
│  CORRECTIONS APPLIED:                                                 │
│    • Topological bulk flow: {V_BULK_KMS} km/s                             │
│    • Z² geometric dark energy                                         │
│    • Orbifold boundary wrapping                                       │
│                                                                       │
│  Output: z2_master_coordinates.bin (WebGL ready)                      │
│                                                                       │
└──────────────────────────────────────────────────────────────────────┘
""")

    return output


if __name__ == "__main__":
    main()
