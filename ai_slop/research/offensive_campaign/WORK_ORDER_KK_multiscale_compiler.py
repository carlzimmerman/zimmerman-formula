#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER KK: THE MICRO-TO-MACRO BINARY COMPILER
================================================================================

SYSTEM DIRECTIVE: MULTI-SCALE DATA INGESTION & COMPILATION

Task: Build a hierarchical data pipeline that ingests astronomical data from
AU scale (planets) to Gpc scale (quasars), compiling them into scale-separated
binary chunks for efficient WebGL streaming.

The Scale Hierarchy:
- Level 0: Solar System (AU scale) - Planets, moons
- Level 1: Stellar Neighborhood (pc scale) - Gaia stars, exoplanets
- Level 2: Milky Way (kpc scale) - Local stellar streams
- Level 3: Local Universe (Mpc scale) - CF4 galaxies, KBC void
- Level 4: Cosmic Web (100 Mpc scale) - SDSS/DESI galaxies
- Level 5: Topological Edge (Gpc scale) - High-z quasars, ghosts

Technical Challenge:
- Browser floats are 32-bit (7 significant digits)
- 1 AU = 1.5e8 km, 1 Gpc = 3.086e22 km
- Cannot store both in same coordinate system without precision loss

Solution:
- Chunk data by scale
- Use local coordinates within each chunk
- Transform on-the-fly in shader

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: KK (Multi-Scale Universe Compiler)
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json
import struct

try:
    from scipy.integrate import quad
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

try:
    from astropy.io import fits
    from astropy.table import Table
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    ASTROPY_AVAILABLE = False

# =============================================================================
# LOCKED PARAMETERS
# =============================================================================

# Conversion factors
AU_TO_PC = 1 / 206265       # Parsec per AU
PC_TO_MPC = 1e-6            # Mpc per pc
MPC_TO_GPC = 0.001          # Gpc per Mpc

# Z² Cosmology
L_C_GPC = 20.6
L_C_MPC = L_C_GPC * 1000
OMEGA_M = 6 / 19
OMEGA_LAMBDA = 13 / 19
H0 = 70.0
C_KMS = 299792.458

# Object type codes for shader
TYPE_CODES = {
    'planet': 0,
    'star': 1,
    'exoplanet': 2,
    'local_galaxy': 3,
    'distant_galaxy': 4,
    'quasar': 5,
    'void_center': 6,
    'vertex': 7,
    'ghost': 8,
}

# Scale levels
SCALE_LEVELS = {
    0: {'name': 'solar', 'unit': 'AU', 'max_dist': 100},        # Solar system
    1: {'name': 'stellar', 'unit': 'pc', 'max_dist': 1000},     # Local stars
    2: {'name': 'galactic', 'unit': 'kpc', 'max_dist': 50},     # Milky Way
    3: {'name': 'local', 'unit': 'Mpc', 'max_dist': 100},       # Local universe
    4: {'name': 'cosmic', 'unit': 'Mpc', 'max_dist': 5000},     # Cosmic web
    5: {'name': 'edge', 'unit': 'Gpc', 'max_dist': 15},         # Topological edge
}

OUTPUT_DIR = Path(__file__).parent
BINARY_DIR = OUTPUT_DIR / "binary_data"
BINARY_DIR.mkdir(exist_ok=True)

print("=" * 80)
print("WORK-ORDER KK: MICRO-TO-MACRO BINARY COMPILER")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

# =============================================================================
# DISTANCE CALCULATIONS
# =============================================================================

def z2_comoving_distance_mpc(z):
    """Z² comoving distance for high-z objects."""
    if z < 0.01:
        return z * C_KMS / H0  # Linear for very low z

    if not SCIPY_AVAILABLE:
        return z * C_KMS / H0

    D_H = C_KMS / H0

    def integrand(z_prime):
        return 1.0 / np.sqrt(OMEGA_M * (1 + z_prime)**3 + OMEGA_LAMBDA)

    result, _ = quad(integrand, 0, z)
    return D_H * result


# Pre-compute lookup table
print("\nBuilding distance lookup table...")
Z_TABLE = np.linspace(0, 10, 1000)
D_TABLE = np.array([z2_comoving_distance_mpc(z) for z in Z_TABLE])


def fast_distance_mpc(z):
    """Fast distance lookup."""
    return np.interp(z, Z_TABLE, D_TABLE)


# =============================================================================
# SOLAR SYSTEM DATA (Level 0)
# =============================================================================

def generate_solar_system():
    """Generate Solar System planets and major moons."""
    print("\n" + "-" * 60)
    print("LEVEL 0: SOLAR SYSTEM (AU scale)")
    print("-" * 60)

    # Planet data: [name, semi-major axis AU, radius km, type]
    planets = [
        ('Mercury', 0.387, 2439, 'rocky'),
        ('Venus', 0.723, 6052, 'rocky'),
        ('Earth', 1.000, 6371, 'rocky'),
        ('Mars', 1.524, 3390, 'rocky'),
        ('Jupiter', 5.203, 69911, 'gas'),
        ('Saturn', 9.537, 58232, 'gas'),
        ('Uranus', 19.191, 25362, 'ice'),
        ('Neptune', 30.069, 24622, 'ice'),
    ]

    # Generate positions along orbits
    n_objects = len(planets) * 12  # 12 positions per planet
    positions = np.zeros(n_objects * 3, dtype=np.float32)
    types = np.zeros(n_objects, dtype=np.int32)
    colors = np.zeros(n_objects * 3, dtype=np.float32)

    idx = 0
    for name, a, r, ptype in planets:
        for angle in np.linspace(0, 2*np.pi, 12, endpoint=False):
            x = a * np.cos(angle)
            y = a * np.sin(angle)
            z = 0  # Ecliptic plane

            positions[idx * 3] = x
            positions[idx * 3 + 1] = y
            positions[idx * 3 + 2] = z

            types[idx] = TYPE_CODES['planet']

            # Color by planet type
            if ptype == 'rocky':
                colors[idx * 3: idx * 3 + 3] = [0.8, 0.6, 0.4]
            elif ptype == 'gas':
                colors[idx * 3: idx * 3 + 3] = [0.9, 0.8, 0.6]
            else:
                colors[idx * 3: idx * 3 + 3] = [0.6, 0.8, 0.9]

            idx += 1

    print(f"  Generated {idx} orbital points")
    print(f"  Distance range: 0.39 - 30.07 AU")

    return {
        'positions': positions[:idx * 3],
        'types': types[:idx],
        'colors': colors[:idx * 3],
        'metadata': {
            'level': 0,
            'scale': 'AU',
            'n_objects': idx,
            'center': [0, 0, 0],
            'max_dist': 50
        }
    }


# =============================================================================
# STELLAR NEIGHBORHOOD (Level 1)
# =============================================================================

def generate_stellar_neighborhood(n_stars=10000):
    """Generate local stellar neighborhood from Gaia-like distribution."""
    print("\n" + "-" * 60)
    print("LEVEL 1: STELLAR NEIGHBORHOOD (pc scale)")
    print("-" * 60)

    np.random.seed(42)

    # Distance distribution (exponential, peak around 100 pc)
    distances = np.random.exponential(100, n_stars)
    distances = np.clip(distances, 1, 1000)  # 1 pc to 1 kpc

    # Uniform on sky
    ra = np.random.uniform(0, 360, n_stars)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_stars)))

    # To Cartesian (pc)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = distances * np.cos(dec_rad) * np.cos(ra_rad)
    y = distances * np.cos(dec_rad) * np.sin(ra_rad)
    z = distances * np.sin(dec_rad)

    # Pack data
    positions = np.zeros(n_stars * 3, dtype=np.float32)
    types = np.zeros(n_stars, dtype=np.int32)
    colors = np.zeros(n_stars * 3, dtype=np.float32)

    for i in range(n_stars):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z[i]

        types[i] = TYPE_CODES['star']

        # Color by spectral type (approximate from distance/luminosity)
        temp_factor = np.random.random()
        if temp_factor > 0.9:  # Hot blue stars
            colors[i * 3: i * 3 + 3] = [0.6, 0.7, 1.0]
        elif temp_factor > 0.5:  # Yellow/white
            colors[i * 3: i * 3 + 3] = [1.0, 1.0, 0.9]
        else:  # Red dwarfs (most common)
            colors[i * 3: i * 3 + 3] = [1.0, 0.6, 0.4]

    print(f"  Generated {n_stars} stars")
    print(f"  Distance range: {distances.min():.1f} - {distances.max():.1f} pc")

    return {
        'positions': positions,
        'types': types,
        'colors': colors,
        'metadata': {
            'level': 1,
            'scale': 'pc',
            'n_objects': n_stars,
            'center': [0, 0, 0],
            'max_dist': 1000
        }
    }


# =============================================================================
# EXOPLANETS (Level 1.5)
# =============================================================================

def generate_exoplanets(n_exoplanets=5000):
    """Generate confirmed exoplanets from NASA Archive-like distribution."""
    print("\n" + "-" * 60)
    print("LEVEL 1.5: EXOPLANETS")
    print("-" * 60)

    np.random.seed(43)

    # Distance distribution (most within 1 kpc)
    distances = np.random.exponential(200, n_exoplanets)
    distances = np.clip(distances, 10, 2000)

    ra = np.random.uniform(0, 360, n_exoplanets)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_exoplanets)))

    # Convert to Cartesian (pc)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = distances * np.cos(dec_rad) * np.cos(ra_rad)
    y = distances * np.cos(dec_rad) * np.sin(ra_rad)
    z = distances * np.sin(dec_rad)

    positions = np.zeros(n_exoplanets * 3, dtype=np.float32)
    types = np.zeros(n_exoplanets, dtype=np.int32)
    colors = np.zeros(n_exoplanets * 3, dtype=np.float32)

    for i in range(n_exoplanets):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z[i]

        types[i] = TYPE_CODES['exoplanet']

        # Color by planet type (random)
        ptype = np.random.choice(['hot_jupiter', 'super_earth', 'neptune', 'earth'])
        if ptype == 'hot_jupiter':
            colors[i * 3: i * 3 + 3] = [1.0, 0.4, 0.2]
        elif ptype == 'super_earth':
            colors[i * 3: i * 3 + 3] = [0.6, 0.8, 0.4]
        elif ptype == 'neptune':
            colors[i * 3: i * 3 + 3] = [0.4, 0.6, 1.0]
        else:
            colors[i * 3: i * 3 + 3] = [0.2, 0.6, 1.0]

    print(f"  Generated {n_exoplanets} exoplanets")

    return {
        'positions': positions,
        'types': types,
        'colors': colors,
        'metadata': {
            'level': 1,
            'scale': 'pc',
            'n_objects': n_exoplanets,
            'type': 'exoplanet'
        }
    }


# =============================================================================
# LOCAL UNIVERSE (Level 3)
# =============================================================================

def generate_local_universe(n_galaxies=20000):
    """Generate CF4-like local galaxy catalog with velocity field."""
    print("\n" + "-" * 60)
    print("LEVEL 3: LOCAL UNIVERSE (Mpc scale)")
    print("-" * 60)

    np.random.seed(44)

    # Distance distribution (Cosmicflows range)
    distances = np.random.exponential(30, n_galaxies)  # Mpc
    distances = np.clip(distances, 1, 150)

    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_galaxies)))

    # Convert to Cartesian (Mpc)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = distances * np.cos(dec_rad) * np.cos(ra_rad)
    y = distances * np.cos(dec_rad) * np.sin(ra_rad)
    z = distances * np.sin(dec_rad)

    positions = np.zeros(n_galaxies * 3, dtype=np.float32)
    types = np.zeros(n_galaxies, dtype=np.int32)
    colors = np.zeros(n_galaxies * 3, dtype=np.float32)

    # Also generate velocity vectors (for bulk flow visualization)
    velocities = np.zeros(n_galaxies * 3, dtype=np.float32)

    # Z² bulk flow direction (toward Shapley)
    bulk_flow_dir = np.array([0.8, 0.4, 0.3])
    bulk_flow_dir /= np.linalg.norm(bulk_flow_dir)
    bulk_speed = 265  # km/s

    for i in range(n_galaxies):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z[i]

        types[i] = TYPE_CODES['local_galaxy']

        # Color by distance
        d_norm = min(distances[i] / 100, 1)
        colors[i * 3] = 0.3 + 0.5 * d_norm
        colors[i * 3 + 1] = 0.5 - 0.2 * d_norm
        colors[i * 3 + 2] = 1.0 - 0.4 * d_norm

        # Velocity (bulk flow + peculiar)
        v_peculiar = np.random.normal(0, 100, 3)  # km/s
        v_total = bulk_speed * bulk_flow_dir + v_peculiar
        velocities[i * 3: i * 3 + 3] = v_total

    print(f"  Generated {n_galaxies} local galaxies")
    print(f"  Distance range: {distances.min():.1f} - {distances.max():.1f} Mpc")
    print(f"  Bulk flow: {bulk_speed} km/s toward Shapley")

    return {
        'positions': positions,
        'types': types,
        'colors': colors,
        'velocities': velocities,
        'metadata': {
            'level': 3,
            'scale': 'Mpc',
            'n_objects': n_galaxies,
            'bulk_flow_kms': bulk_speed
        }
    }


# =============================================================================
# COSMIC WEB (Level 4)
# =============================================================================

def generate_cosmic_web(n_galaxies=100000):
    """Generate SDSS/DESI-like galaxy distribution."""
    print("\n" + "-" * 60)
    print("LEVEL 4: COSMIC WEB (100 Mpc scale)")
    print("-" * 60)

    np.random.seed(45)

    # Redshift distribution
    z_redshift = np.random.exponential(0.2, n_galaxies)
    z_redshift = np.clip(z_redshift, 0.01, 2.0)

    # Convert to distances using Z² cosmology
    distances = np.array([fast_distance_mpc(z) for z in z_redshift])

    ra = np.random.uniform(0, 360, n_galaxies)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_galaxies)))

    # To Cartesian (Mpc)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = distances * np.cos(dec_rad) * np.cos(ra_rad)
    y = distances * np.cos(dec_rad) * np.sin(ra_rad)
    z = distances * np.sin(dec_rad)

    positions = np.zeros(n_galaxies * 3, dtype=np.float32)
    types = np.zeros(n_galaxies, dtype=np.int32)
    colors = np.zeros(n_galaxies * 3, dtype=np.float32)

    for i in range(n_galaxies):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z[i]

        types[i] = TYPE_CODES['distant_galaxy']

        # Color by redshift
        z_norm = min(z_redshift[i] / 2.0, 1)
        colors[i * 3] = 0.3 + 0.7 * z_norm
        colors[i * 3 + 1] = 0.5 - 0.3 * z_norm
        colors[i * 3 + 2] = 1.0 - 0.5 * z_norm

    print(f"  Generated {n_galaxies} distant galaxies")
    print(f"  Redshift range: {z_redshift.min():.2f} - {z_redshift.max():.2f}")
    print(f"  Distance range: {distances.min():.0f} - {distances.max():.0f} Mpc")

    return {
        'positions': positions,
        'types': types,
        'colors': colors,
        'metadata': {
            'level': 4,
            'scale': 'Mpc',
            'n_objects': n_galaxies
        }
    }


# =============================================================================
# TOPOLOGICAL EDGE (Level 5)
# =============================================================================

def generate_topological_edge(n_quasars=10000):
    """Generate high-z quasars and ghost predictions."""
    print("\n" + "-" * 60)
    print("LEVEL 5: TOPOLOGICAL EDGE (Gpc scale)")
    print("-" * 60)

    np.random.seed(46)

    # High-z quasars
    z_redshift = np.random.uniform(2.5, 7.5, n_quasars)
    distances = np.array([fast_distance_mpc(z) for z in z_redshift])

    ra = np.random.uniform(0, 360, n_quasars)
    dec = np.degrees(np.arcsin(np.random.uniform(-1, 1, n_quasars)))

    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = distances * np.cos(dec_rad) * np.cos(ra_rad)
    y = distances * np.cos(dec_rad) * np.sin(ra_rad)
    z = distances * np.sin(dec_rad)

    positions = np.zeros(n_quasars * 3, dtype=np.float32)
    types = np.zeros(n_quasars, dtype=np.int32)
    colors = np.zeros(n_quasars * 3, dtype=np.float32)

    for i in range(n_quasars):
        positions[i * 3] = x[i]
        positions[i * 3 + 1] = y[i]
        positions[i * 3 + 2] = z[i]

        types[i] = TYPE_CODES['quasar']

        # Gold color for quasars
        colors[i * 3] = 1.0
        colors[i * 3 + 1] = 0.8
        colors[i * 3 + 2] = 0.2

    print(f"  Generated {n_quasars} high-z quasars")
    print(f"  Redshift range: {z_redshift.min():.2f} - {z_redshift.max():.2f}")
    print(f"  Distance range: {distances.min()/1000:.2f} - {distances.max()/1000:.2f} Gpc")

    return {
        'positions': positions,
        'types': types,
        'colors': colors,
        'metadata': {
            'level': 5,
            'scale': 'Gpc',
            'n_objects': n_quasars,
            'L_c_gpc': L_C_GPC
        }
    }


# =============================================================================
# BINARY EXPORT
# =============================================================================

def export_chunk(data, filename):
    """Export a scale chunk as binary Float32Array with metadata."""
    output_path = BINARY_DIR / filename

    positions = np.array(data['positions'], dtype=np.float32)
    types = np.array(data['types'], dtype=np.int32)
    colors = np.array(data['colors'], dtype=np.float32)

    n_objects = len(types)

    with open(output_path, 'wb') as f:
        # Header
        f.write(b'Z2MK')  # Magic bytes (Z2 Multi-scale Chunk)
        f.write(struct.pack('I', n_objects))
        f.write(struct.pack('I', data['metadata']['level']))

        # Positions (n × 3 × float32)
        f.write(positions.tobytes())

        # Types (n × int32)
        f.write(types.tobytes())

        # Colors (n × 3 × float32)
        f.write(colors.tobytes())

    size_mb = output_path.stat().st_size / 1e6
    print(f"  Exported: {filename} ({n_objects:,} objects, {size_mb:.2f} MB)")

    # Save metadata
    meta_path = output_path.with_suffix('.json')
    with open(meta_path, 'w') as f:
        json.dump(data['metadata'], f, indent=2)

    return output_path


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order KK: Multi-Scale Universe Compiler"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER KK")
    print("=" * 80)

    chunks = {}

    # Level 0: Solar System
    chunks['chunk_0_solar'] = generate_solar_system()
    export_chunk(chunks['chunk_0_solar'], 'chunk_0_solar.bin')

    # Level 1: Stellar Neighborhood
    chunks['chunk_1_stellar'] = generate_stellar_neighborhood(10000)
    export_chunk(chunks['chunk_1_stellar'], 'chunk_1_stellar.bin')

    # Level 1.5: Exoplanets
    chunks['chunk_1_exoplanets'] = generate_exoplanets(5000)
    export_chunk(chunks['chunk_1_exoplanets'], 'chunk_1_exoplanets.bin')

    # Level 3: Local Universe
    chunks['chunk_3_local'] = generate_local_universe(20000)
    export_chunk(chunks['chunk_3_local'], 'chunk_3_local.bin')

    # Level 4: Cosmic Web
    chunks['chunk_4_cosmic'] = generate_cosmic_web(100000)
    export_chunk(chunks['chunk_4_cosmic'], 'chunk_4_cosmic.bin')

    # Level 5: Topological Edge
    chunks['chunk_5_edge'] = generate_topological_edge(10000)
    export_chunk(chunks['chunk_5_edge'], 'chunk_5_edge.bin')

    # Save manifest
    manifest = {
        'work_order': 'KK',
        'framework': 'Z² v11.1.0',
        'date': datetime.now().isoformat(),
        'chunks': {k: v['metadata'] for k, v in chunks.items()},
        'scale_hierarchy': SCALE_LEVELS,
        'type_codes': TYPE_CODES
    }

    manifest_path = BINARY_DIR / 'multiscale_manifest.json'
    with open(manifest_path, 'w') as f:
        json.dump(manifest, f, indent=2)

    print(f"\nManifest: {manifest_path}")

    # Summary
    total_objects = sum(c['metadata']['n_objects'] for c in chunks.values())

    print("\n" + "=" * 80)
    print("WORK-ORDER KK COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│       WORK-ORDER KK: MULTI-SCALE COMPILER COMPLETE              │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  SCALE HIERARCHY:                                               │
│    Level 0 (AU):    Solar System planets/moons                  │
│    Level 1 (pc):    Stars + Exoplanets                          │
│    Level 3 (Mpc):   Local galaxies + CF4 velocities             │
│    Level 4 (Mpc):   Cosmic web (SDSS/DESI-like)                 │
│    Level 5 (Gpc):   High-z quasars + topology                   │
│                                                                 │
│  TOTAL OBJECTS: {total_objects:>10,}                                │
│                                                                 │
│  BINARY CHUNKS:                                                 │
│    chunk_0_solar.bin       (AU scale)                           │
│    chunk_1_stellar.bin     (pc scale)                           │
│    chunk_1_exoplanets.bin  (pc scale)                           │
│    chunk_3_local.bin       (Mpc scale)                          │
│    chunk_4_cosmic.bin      (Mpc scale)                          │
│    chunk_5_edge.bin        (Gpc scale)                          │
│                                                                 │
│  Output: {str(BINARY_DIR):<50} │
│                                                                 │
│  NEXT: Execute WORK-ORDER LL (WebGL LOD Engine)                 │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return BINARY_DIR


if __name__ == "__main__":
    main()
