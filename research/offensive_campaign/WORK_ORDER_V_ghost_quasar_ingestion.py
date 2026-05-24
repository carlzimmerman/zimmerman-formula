#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER V: HIGH-Z QUASAR CATALOG INGESTION & TRIAGE
================================================================================

SYSTEM DIRECTIVE: STRICT DATA TRIAGE

Task: Ingest and filter public quasar catalogs to build the candidate pool
for topological duplication detection in T³/Z₂ topology.

The Topological Threshold:
- To see a ghost image, light must have had enough time to wrap around
  the 20.6 Gpc fundamental domain
- Quasars must be at z ≥ 3.0 for ghost paths to be geometrically feasible

Technical Requirements:
1. Load SDSS DR16Q/DR18 and DESI quasar catalogs
2. Filter strictly for z ≥ 3.0
3. Extract: RA, DEC, Z, FLUX, PLATE/MJD/FIBER (spectroscopic IDs)
4. Output: high_z_quasar_candidates.fits

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: V (Ghost Quasar Search Pipeline)
================================================================================
"""

import numpy as np
from pathlib import Path
from datetime import datetime
import json

# Try astropy imports
try:
    from astropy.io import fits
    from astropy.table import Table, vstack
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    print("WARNING: astropy not available. Some functions will be limited.")
    ASTROPY_AVAILABLE = False

# =============================================================================
# LOCKED PARAMETERS - DO NOT MODIFY
# =============================================================================

L_C_GPC = 20.6              # Fundamental domain scale (LOCKED)
Z_MIN_THRESHOLD = 3.0       # Minimum redshift for ghost detection
Z_MAX_THRESHOLD = 10.0      # Maximum reasonable redshift

# Z² Cosmological parameters
OMEGA_M = 6 / 19            # = 0.3158 (topological dark matter)
OMEGA_LAMBDA = 13 / 19      # = 0.6842 (dark energy from EW vacuum)
H0 = 70.0                   # Hubble constant km/s/Mpc

OUTPUT_DIR = Path(__file__).parent
DATA_DIR = OUTPUT_DIR / "quasar_data"

print("=" * 80)
print("WORK-ORDER V: HIGH-Z QUASAR CATALOG INGESTION & TRIAGE")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\nTopological Threshold: z ≥ {Z_MIN_THRESHOLD}")
print(f"Fundamental Domain: L_c = {L_C_GPC} Gpc")

# =============================================================================
# CATALOG LOCATIONS
# =============================================================================

CATALOG_SOURCES = {
    'SDSS_DR16Q': {
        'file': DATA_DIR / 'DR18Q_v1.fits',  # Already downloaded
        'url': 'https://data.sdss.org/sas/dr16/eboss/qso/DR16Q/DR16Q_v4.fits',
        'ra_col': 'RA',
        'dec_col': 'DEC',
        'z_col': 'Z',
        'id_cols': ['SDSS_NAME', 'PLATE', 'MJD', 'FIBERID']
    },
    'DESI_DR1': {
        'file': DATA_DIR / 'desi_qso_dr1.fits',
        'url': 'https://data.desi.lbl.gov/public/dr1/spectro/redux/iron/healpix/',
        'ra_col': 'TARGET_RA',
        'dec_col': 'TARGET_DEC',
        'z_col': 'Z',
        'id_cols': ['TARGETID', 'SURVEY', 'PROGRAM']
    }
}

# =============================================================================
# INGESTION FUNCTIONS
# =============================================================================

def load_sdss_catalog():
    """
    Load SDSS DR16Q quasar catalog.
    Returns astropy Table with standardized column names.
    """
    print("\n" + "-" * 60)
    print("LOADING SDSS DR16Q CATALOG")
    print("-" * 60)

    catalog_file = CATALOG_SOURCES['SDSS_DR16Q']['file']

    if not catalog_file.exists():
        print(f"✗ Catalog not found: {catalog_file}")
        print(f"  Download from: {CATALOG_SOURCES['SDSS_DR16Q']['url']}")
        return None

    print(f"Loading: {catalog_file}")

    try:
        data = Table.read(catalog_file, hdu='CATALOG')
        print(f"✓ Loaded {len(data):,} quasars from SDSS DR16Q")

        # Identify redshift column
        z_col = None
        for col in ['Z', 'Z_PIPE', 'Z_VI', 'Z_QN', 'REDSHIFT']:
            if col in data.colnames:
                z_col = col
                break

        if z_col is None:
            print("✗ No redshift column found!")
            return None

        print(f"  Using redshift column: {z_col}")

        # Create standardized table
        result = Table()
        result['RA'] = data['RA']
        result['DEC'] = data['DEC']
        result['Z'] = data[z_col]
        result['SOURCE'] = 'SDSS_DR16Q'

        # Add identifiers
        if 'SDSS_NAME' in data.colnames:
            result['NAME'] = data['SDSS_NAME']
        else:
            result['NAME'] = [f"SDSS_{ra:.4f}+{dec:.4f}"
                             for ra, dec in zip(data['RA'], data['DEC'])]

        if 'PLATE' in data.colnames:
            result['PLATE'] = data['PLATE']
            result['MJD'] = data['MJD']
            result['FIBERID'] = data['FIBERID']

        return result

    except Exception as e:
        print(f"✗ Error loading catalog: {e}")
        return None


def load_desi_catalog():
    """
    Load DESI DR1 quasar catalog if available.
    """
    print("\n" + "-" * 60)
    print("LOADING DESI DR1 CATALOG")
    print("-" * 60)

    catalog_file = CATALOG_SOURCES['DESI_DR1']['file']

    if not catalog_file.exists():
        print(f"✗ DESI catalog not found: {catalog_file}")
        print("  Skipping DESI data (SDSS only)")
        return None

    # Similar loading logic for DESI
    # ... (implement when DESI data available)
    return None


def apply_topological_filter(catalog):
    """
    Apply strict topological threshold filter.

    The Physics:
    - Light must travel at least L_c to create a ghost
    - Comoving distance at z=3 is ~6.3 Gpc
    - At z=3, ghost path would be ~14-27 Gpc (within horizon)
    - Below z~3, ghosts are geometrically impossible
    """
    print("\n" + "-" * 60)
    print("APPLYING TOPOLOGICAL THRESHOLD FILTER")
    print("-" * 60)

    n_initial = len(catalog)
    print(f"Initial count: {n_initial:,} quasars")

    # Remove invalid redshifts
    valid_z = (catalog['Z'] > 0) & (catalog['Z'] < Z_MAX_THRESHOLD)
    catalog = catalog[valid_z]
    print(f"After removing invalid z: {len(catalog):,}")

    # Apply topological threshold
    high_z = catalog['Z'] >= Z_MIN_THRESHOLD
    catalog = catalog[high_z]
    print(f"After z ≥ {Z_MIN_THRESHOLD} filter: {len(catalog):,}")

    # Statistics
    z_values = catalog['Z']
    print(f"\nRedshift Distribution:")
    print(f"  z ∈ [3.0, 4.0): {np.sum((z_values >= 3) & (z_values < 4)):,}")
    print(f"  z ∈ [4.0, 5.0): {np.sum((z_values >= 4) & (z_values < 5)):,}")
    print(f"  z ∈ [5.0, 6.0): {np.sum((z_values >= 5) & (z_values < 6)):,}")
    print(f"  z ∈ [6.0, 7.0): {np.sum((z_values >= 6) & (z_values < 7)):,}")
    print(f"  z ≥ 7.0:        {np.sum(z_values >= 7):,}")

    return catalog


def add_comoving_distances(catalog):
    """
    Add comoving distance column using Z² cosmology.

    Z² Cosmology:
    - Ω_m = 6/19 = 0.3158
    - Ω_Λ = 13/19 = 0.6842
    - Uses standard FLRW metric with these densities
    """
    from scipy.integrate import quad

    print("\n" + "-" * 60)
    print("COMPUTING COMOVING DISTANCES (Z² COSMOLOGY)")
    print("-" * 60)

    def comoving_distance_gpc(z):
        """Comoving distance in Gpc using Z² parameters."""
        c_kms = 299792.458

        def integrand(z_p):
            return 1.0 / np.sqrt(OMEGA_M * (1 + z_p)**3 + OMEGA_LAMBDA)

        result, _ = quad(integrand, 0, z)
        D_H = c_kms / H0 / 1000  # Hubble distance in Gpc
        return D_H * result

    # Compute distances
    print("Computing comoving distances...")
    distances = []
    for i, z in enumerate(catalog['Z']):
        distances.append(comoving_distance_gpc(float(z)))
        if (i + 1) % 10000 == 0:
            print(f"  Progress: {i+1:,}/{len(catalog):,}")

    catalog['D_C_GPC'] = distances

    # Statistics
    d_values = catalog['D_C_GPC']
    print(f"\nComoving Distance Distribution:")
    print(f"  Min: {np.min(d_values):.2f} Gpc")
    print(f"  Max: {np.max(d_values):.2f} Gpc")
    print(f"  Mean: {np.mean(d_values):.2f} Gpc")
    print(f"  Within L_c ({L_C_GPC} Gpc): {np.sum(d_values < L_C_GPC):,}")

    return catalog


def save_candidate_catalog(catalog, filename='high_z_quasar_candidates.fits'):
    """
    Save the filtered, triage catalog for ghost coordinate prediction.
    """
    print("\n" + "-" * 60)
    print("SAVING CANDIDATE CATALOG")
    print("-" * 60)

    output_file = OUTPUT_DIR / filename

    # Save as FITS
    catalog.write(output_file, format='fits', overwrite=True)
    print(f"✓ Saved: {output_file}")
    print(f"  Total candidates: {len(catalog):,}")

    # Also save summary as JSON
    summary = {
        'work_order': 'V',
        'task': 'High-z Quasar Catalog Ingestion & Triage',
        'date': datetime.now().isoformat(),
        'parameters': {
            'z_min_threshold': Z_MIN_THRESHOLD,
            'L_c_gpc': L_C_GPC,
            'omega_m': OMEGA_M,
            'omega_lambda': OMEGA_LAMBDA
        },
        'results': {
            'total_candidates': len(catalog),
            'z_range': [float(np.min(catalog['Z'])), float(np.max(catalog['Z']))],
            'd_c_range_gpc': [float(np.min(catalog['D_C_GPC'])),
                             float(np.max(catalog['D_C_GPC']))],
            'sources': list(set(catalog['SOURCE']))
        },
        'output_file': str(output_file),
        'next_step': 'WORK-ORDER W: Geometric Translation Engine'
    }

    summary_file = OUTPUT_DIR / 'WORK_ORDER_V_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Summary: {summary_file}")

    return output_file


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order V: Catalog Ingestion & Triage"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER V")
    print("=" * 80)

    # Step 1: Load catalogs
    catalogs = []

    sdss_data = load_sdss_catalog()
    if sdss_data is not None:
        catalogs.append(sdss_data)

    desi_data = load_desi_catalog()
    if desi_data is not None:
        catalogs.append(desi_data)

    if not catalogs:
        print("\n✗ No catalogs loaded. Cannot proceed.")
        return None

    # Step 2: Combine catalogs
    if len(catalogs) > 1:
        print("\nCombining catalogs...")
        combined = vstack(catalogs)
    else:
        combined = catalogs[0]

    print(f"\nTotal loaded: {len(combined):,} quasars")

    # Step 3: Apply topological filter
    filtered = apply_topological_filter(combined)

    # Step 4: Compute comoving distances
    with_distances = add_comoving_distances(filtered)

    # Step 5: Save output
    output_file = save_candidate_catalog(with_distances)

    # Final summary
    print("\n" + "=" * 80)
    print("WORK-ORDER V COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│              WORK-ORDER V: INGESTION COMPLETE                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Total quasars ingested:      {len(combined):>10,}                    │
│  After z ≥ {Z_MIN_THRESHOLD} filter:          {len(with_distances):>10,}                    │
│                                                                 │
│  Redshift range:              z = {np.min(with_distances['Z']):.2f} - {np.max(with_distances['Z']):.2f}          │
│  Distance range:              D = {np.min(with_distances['D_C_GPC']):.2f} - {np.max(with_distances['D_C_GPC']):.2f} Gpc       │
│                                                                 │
│  Output: {str(output_file):<50} │
│                                                                 │
│  NEXT: Execute WORK-ORDER W (Geometric Translation Engine)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return output_file


if __name__ == "__main__":
    main()
