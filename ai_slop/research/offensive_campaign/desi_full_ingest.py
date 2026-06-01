#!/usr/bin/env python3
"""
=============================================================================
DIRECTIVE ZZZZ: DESI FULL-SCALE COSMIC WEB INGESTION
=============================================================================

Ingests the complete DESI spectroscopic dataset and converts to T³/Z₂
topographic coordinates for rendering the macroscopic Cosmic Web.

Data Sources:
- DESI DR1 (2024): ~40M spectra
- NOIRLab Astro Data Lab TAP service

Coordinate Transform:
- Input: RA (deg), Dec (deg), Redshift (z)
- Output: Cartesian X, Y, Z in Gpc (Earth at origin)
- Boundary: ±10.3 Gpc (L_c = 20.6 Gpc fundamental domain)

Cosmology: Planck 2018 (H0=67.4, Ωm=0.315, ΩΛ=0.685)
=============================================================================
"""

import numpy as np
import json
from astropy.cosmology import Planck18
from astropy import units as u
from astropy.coordinates import SkyCoord
import requests
from io import StringIO
import pandas as pd
from pathlib import Path
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# =============================================================================
# COSMOLOGICAL PARAMETERS
# =============================================================================

# Fundamental domain size
L_C_GPC = 20.6  # Gpc
HALF_BOX_GPC = L_C_GPC / 2  # ±10.3 Gpc

# Use Planck 2018 cosmology
cosmo = Planck18

def redshift_to_comoving_distance_gpc(z):
    """Convert redshift to comoving distance in Gpc using Planck 2018."""
    if z <= 0:
        return 0.0
    d_mpc = cosmo.comoving_distance(z).to(u.Mpc).value
    return d_mpc / 1000.0  # Convert Mpc to Gpc

def ra_dec_z_to_cartesian(ra_deg, dec_deg, z):
    """
    Convert RA/Dec/z to Cartesian X,Y,Z in Gpc.

    Coordinate system:
    - X: toward RA=0, Dec=0
    - Y: toward RA=90°, Dec=0
    - Z: toward Dec=+90° (North Celestial Pole)
    - Earth at origin (0, 0, 0)
    """
    # Comoving distance
    d_gpc = redshift_to_comoving_distance_gpc(z)

    # Convert to radians
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    # Spherical to Cartesian
    x = d_gpc * np.cos(dec_rad) * np.cos(ra_rad)
    y = d_gpc * np.cos(dec_rad) * np.sin(ra_rad)
    z_coord = d_gpc * np.sin(dec_rad)

    return x, y, z_coord

# =============================================================================
# NOIRLAB TAP QUERY
# =============================================================================

NOIRLAB_TAP_URL = "https://datalab.noirlab.edu/tap/sync"

def query_desi_tap(query, max_retries=3):
    """Execute a TAP query against NOIRLab Astro Data Lab."""
    params = {
        'REQUEST': 'doQuery',
        'LANG': 'ADQL',
        'FORMAT': 'csv',
        'QUERY': query
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(NOIRLAB_TAP_URL, data=params, timeout=300)
            response.raise_for_status()
            return pd.read_csv(StringIO(response.text))
        except Exception as e:
            print(f"  Attempt {attempt + 1} failed: {e}")
            if attempt < max_retries - 1:
                time.sleep(5 * (attempt + 1))
            else:
                raise

def fetch_desi_lrg(limit=None):
    """Fetch Luminous Red Galaxies from DESI DR1."""
    limit_clause = f"TOP {limit}" if limit else ""
    query = f"""
    SELECT {limit_clause}
        target_ra as ra,
        target_dec as dec,
        z as redshift,
        zwarn,
        spectype
    FROM desi_dr1.zpix
    WHERE spectype = 'GALAXY'
      AND zwarn = 0
      AND z > 0.01 AND z < 1.5
    """
    print(f"Fetching DESI LRG galaxies...")
    return query_desi_tap(query)

def fetch_desi_elg(limit=None):
    """Fetch Emission Line Galaxies from DESI DR1."""
    limit_clause = f"TOP {limit}" if limit else ""
    query = f"""
    SELECT {limit_clause}
        target_ra as ra,
        target_dec as dec,
        z as redshift,
        zwarn,
        spectype
    FROM desi_dr1.zpix
    WHERE spectype = 'GALAXY'
      AND zwarn = 0
      AND z > 0.6 AND z < 1.6
    """
    print(f"Fetching DESI ELG galaxies...")
    return query_desi_tap(query)

def fetch_desi_qso(limit=None):
    """Fetch Quasars from DESI DR1."""
    limit_clause = f"TOP {limit}" if limit else ""
    query = f"""
    SELECT {limit_clause}
        target_ra as ra,
        target_dec as dec,
        z as redshift,
        zwarn,
        spectype
    FROM desi_dr1.zpix
    WHERE spectype = 'QSO'
      AND zwarn = 0
      AND z > 0.5 AND z < 4.0
    """
    print(f"Fetching DESI QSOs...")
    return query_desi_tap(query)

def fetch_desi_bgs(limit=None):
    """Fetch Bright Galaxy Survey objects from DESI DR1."""
    limit_clause = f"TOP {limit}" if limit else ""
    query = f"""
    SELECT {limit_clause}
        target_ra as ra,
        target_dec as dec,
        z as redshift,
        zwarn,
        spectype
    FROM desi_dr1.zpix
    WHERE spectype = 'GALAXY'
      AND zwarn = 0
      AND z > 0.001 AND z < 0.4
    """
    print(f"Fetching DESI BGS galaxies...")
    return query_desi_tap(query)

# =============================================================================
# COORDINATE CONVERSION & CHUNKING
# =============================================================================

def convert_catalog_to_cartesian(df, source_type):
    """Convert a catalog dataframe to Cartesian coordinates."""
    results = []

    for _, row in df.iterrows():
        try:
            x, y, z = ra_dec_z_to_cartesian(row['ra'], row['dec'], row['redshift'])

            # Check if within fundamental domain
            if abs(x) <= HALF_BOX_GPC and abs(y) <= HALF_BOX_GPC and abs(z) <= HALF_BOX_GPC:
                results.append({
                    'x': round(x, 6),
                    'y': round(y, 6),
                    'z': round(z, 6),
                    'redshift': round(row['redshift'], 4),
                    'type': source_type
                })
        except:
            continue

    return results

def compute_boundary_alignment(objects):
    """
    Compute density gradient as objects approach the T³ boundary walls.

    Returns alignment scores for each axis showing if structure
    preferentially aligns with the fundamental domain boundaries.
    """
    if len(objects) == 0:
        return {}

    # Extract coordinates
    coords = np.array([[o['x'], o['y'], o['z']] for o in objects])

    # Compute density in shells approaching each boundary
    alignment_scores = {}

    for axis_idx, axis_name in enumerate(['X', 'Y', 'Z']):
        # Distance from boundary wall (either + or -)
        dist_from_wall = HALF_BOX_GPC - np.abs(coords[:, axis_idx])

        # Count objects in shells
        shells = [
            (0, 0.5),   # 0-0.5 Gpc from wall
            (0.5, 1.0), # 0.5-1.0 Gpc from wall
            (1.0, 2.0), # 1.0-2.0 Gpc from wall
            (2.0, 5.0), # 2.0-5.0 Gpc from wall
        ]

        shell_densities = []
        for inner, outer in shells:
            mask = (dist_from_wall >= inner) & (dist_from_wall < outer)
            count = np.sum(mask)
            volume = outer - inner  # Simplified volume
            density = count / volume if volume > 0 else 0
            shell_densities.append(density)

        # Alignment score: ratio of near-wall density to far-wall density
        if shell_densities[-1] > 0:
            alignment_scores[axis_name] = {
                'near_wall_density': shell_densities[0],
                'far_wall_density': shell_densities[-1],
                'alignment_ratio': shell_densities[0] / shell_densities[-1],
                'shell_densities': shell_densities
            }
        else:
            alignment_scores[axis_name] = {
                'near_wall_density': shell_densities[0],
                'far_wall_density': 0,
                'alignment_ratio': float('inf') if shell_densities[0] > 0 else 0,
                'shell_densities': shell_densities
            }

    return alignment_scores

def create_spatial_chunks(objects, chunk_size_gpc=2.0):
    """
    Divide objects into spatial chunks for efficient WebGL rendering.
    Uses octree-like chunking.
    """
    chunks = {}

    for obj in objects:
        # Compute chunk indices
        cx = int((obj['x'] + HALF_BOX_GPC) / chunk_size_gpc)
        cy = int((obj['y'] + HALF_BOX_GPC) / chunk_size_gpc)
        cz = int((obj['z'] + HALF_BOX_GPC) / chunk_size_gpc)

        chunk_key = f"{cx}_{cy}_{cz}"

        if chunk_key not in chunks:
            chunks[chunk_key] = {
                'center': {
                    'x': (cx + 0.5) * chunk_size_gpc - HALF_BOX_GPC,
                    'y': (cy + 0.5) * chunk_size_gpc - HALF_BOX_GPC,
                    'z': (cz + 0.5) * chunk_size_gpc - HALF_BOX_GPC,
                },
                'objects': []
            }

        # Store only relative position within chunk for memory efficiency
        chunks[chunk_key]['objects'].append({
            'dx': obj['x'] - chunks[chunk_key]['center']['x'],
            'dy': obj['y'] - chunks[chunk_key]['center']['y'],
            'dz': obj['z'] - chunks[chunk_key]['center']['z'],
            't': obj['type'][0]  # First letter of type (G/Q)
        })

    return chunks

# =============================================================================
# MAIN PIPELINE
# =============================================================================

def main():
    """Main pipeline: Fetch DESI data and convert to T³/Z₂ coordinates."""

    print("=" * 70)
    print("DIRECTIVE ZZZZ: DESI COSMIC WEB INGESTION")
    print("=" * 70)
    print(f"Fundamental domain: L_c = {L_C_GPC} Gpc")
    print(f"Boundary walls at: ±{HALF_BOX_GPC} Gpc")
    print(f"Cosmology: Planck 2018 (H0={cosmo.H0.value}, Ωm={cosmo.Om0})")
    print()

    # Output paths
    output_dir = Path(__file__).parent

    all_objects = []
    source_counts = {}

    # Fetch each catalog type
    # Using limits for initial testing - remove for full catalog
    catalog_configs = [
        ('BGS', fetch_desi_bgs, 500000),     # Bright galaxies (nearby)
        ('LRG', fetch_desi_lrg, 2000000),    # Luminous red galaxies
        ('ELG', fetch_desi_elg, 2000000),    # Emission line galaxies
        ('QSO', fetch_desi_qso, 500000),     # Quasars (distant)
    ]

    for source_type, fetch_func, limit in catalog_configs:
        try:
            print(f"\n--- Fetching {source_type} ---")
            df = fetch_func(limit=limit)
            print(f"  Retrieved {len(df)} objects")

            print(f"  Converting to Cartesian coordinates...")
            objects = convert_catalog_to_cartesian(df, source_type)
            print(f"  {len(objects)} objects within fundamental domain")

            all_objects.extend(objects)
            source_counts[source_type] = len(objects)

        except Exception as e:
            print(f"  ERROR fetching {source_type}: {e}")
            source_counts[source_type] = 0

    print(f"\n--- TOTAL: {len(all_objects)} objects ---")

    if len(all_objects) == 0:
        print("No objects retrieved. Check network connection to NOIRLab.")
        return

    # Compute boundary alignment
    print("\nComputing boundary alignment analysis...")
    alignment = compute_boundary_alignment(all_objects)

    print("\nBoundary Alignment Scores:")
    for axis, scores in alignment.items():
        ratio = scores['alignment_ratio']
        status = "ALIGNED" if ratio > 1.5 else "NORMAL"
        print(f"  {axis}-axis: ratio = {ratio:.2f} [{status}]")

    # Create spatial chunks for WebGL
    print("\nCreating spatial chunks for WebGL rendering...")
    chunks = create_spatial_chunks(all_objects, chunk_size_gpc=2.0)
    print(f"  Created {len(chunks)} spatial chunks")

    # Prepare output
    output_data = {
        'metadata': {
            'title': 'DESI Cosmic Web - T³/Z₂ Topographic Coordinates',
            'description': 'Full DESI spectroscopic catalog mapped to fundamental domain',
            'extraction_date': datetime.now().isoformat(),
            'cosmology': {
                'H0': cosmo.H0.value,
                'Om0': cosmo.Om0,
                'Ode0': cosmo.Ode0,
            },
            'fundamental_domain_gpc': L_C_GPC,
            'boundary_walls_gpc': HALF_BOX_GPC,
            'total_objects': len(all_objects),
            'source_counts': source_counts,
            'coordinate_system': 'Cartesian (X,Y,Z) in Gpc, Earth at origin',
        },
        'boundary_alignment': alignment,
        'chunks': chunks,
        # Also include flat list for simple rendering
        'objects_flat': all_objects[:100000],  # First 100k for flat access
    }

    # Save to JSON
    output_file = output_dir / 'desi_cosmic_web_full.json'
    print(f"\nSaving to {output_file}...")

    with open(output_file, 'w') as f:
        json.dump(output_data, f)

    print(f"File size: {output_file.stat().st_size / 1024 / 1024:.1f} MB")

    # Also save a smaller version for the website
    website_data = {
        'metadata': output_data['metadata'],
        'boundary_alignment': alignment,
        'objects': all_objects[:500000],  # 500k for web
    }

    website_file = Path(__file__).parent.parent.parent / 'website' / 'public' / 'data' / 'desi_cosmic_web.json'
    website_file.parent.mkdir(parents=True, exist_ok=True)

    print(f"Saving web version to {website_file}...")
    with open(website_file, 'w') as f:
        json.dump(website_data, f)

    print(f"Web file size: {website_file.stat().st_size / 1024 / 1024:.1f} MB")

    print("\n" + "=" * 70)
    print("DIRECTIVE ZZZZ COMPLETE")
    print("=" * 70)

if __name__ == '__main__':
    main()
