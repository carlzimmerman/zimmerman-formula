#!/usr/bin/env python3
"""
================================================================================
WORK-ORDER W: THE GEOMETRIC TRANSLATION ENGINE
================================================================================

SYSTEM DIRECTIVE: STRICT TOPOLOGICAL GEOMETRY (LOCKED PARAMETERS)

Task: Calculate the predicted ghost coordinates for every high-z quasar
candidate using T³/Z₂ topology with L_c = 20.6 Gpc.

STRICT CONSTRAINTS (HARD STOP PROTOCOL):
- Do NOT alter the fundamental domain: L_c = 20.6 Gpc
- Use Z² native distance integral with Ω_m = 6/19, Ω_Λ = 13/19

The Mathematics:
1. Convert (RA, Dec, z) → Cartesian (x, y, z) using comoving distance
2. Apply Z₂ lattice translations: x_ghost = x_true ± L_c * ê_i
3. Convert back to (RA_ghost, Dec_ghost, z_ghost)

Output: predicted_ghost_coordinates.fits

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: Z² Unified Action v11.1.0
Work-Order: W (Ghost Quasar Search Pipeline)
================================================================================
"""

import numpy as np
from scipy.integrate import quad
from scipy.optimize import brentq
from pathlib import Path
from datetime import datetime
import json

try:
    from astropy.io import fits
    from astropy.table import Table
    from astropy.coordinates import SkyCoord
    import astropy.units as u
    ASTROPY_AVAILABLE = True
except ImportError:
    print("WARNING: astropy not available.")
    ASTROPY_AVAILABLE = False

# =============================================================================
# LOCKED PARAMETERS - DO NOT MODIFY (HARD STOP PROTOCOL)
# =============================================================================

L_C_GPC = 20.6              # Fundamental domain scale - LOCKED
L_C_MPC = L_C_GPC * 1000    # in Mpc

# Z² Cosmological parameters - LOCKED
OMEGA_M = 6 / 19            # = 0.3158 (topological dark matter)
OMEGA_LAMBDA = 13 / 19      # = 0.6842 (dark energy from EW vacuum)
H0 = 70.0                   # Hubble constant km/s/Mpc
C_KMS = 299792.458          # Speed of light km/s

# Derived constants
D_H_GPC = C_KMS / H0 / 1000  # Hubble distance in Gpc = 4.283 Gpc

OUTPUT_DIR = Path(__file__).parent

print("=" * 80)
print("WORK-ORDER W: GEOMETRIC TRANSLATION ENGINE")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"\n*** LOCKED PARAMETERS ***")
print(f"  L_c = {L_C_GPC} Gpc (fundamental domain)")
print(f"  Ω_m = {OMEGA_M:.4f} = 6/19")
print(f"  Ω_Λ = {OMEGA_LAMBDA:.4f} = 13/19")

# =============================================================================
# Z² COSMOLOGY FUNCTIONS
# =============================================================================

def z2_comoving_distance_gpc(z):
    """
    Comoving distance in Gpc using EXACT Z² cosmological parameters.

    The integral:
    D_c(z) = D_H ∫₀ᶻ dz' / √[Ω_m(1+z')³ + Ω_Λ]

    where D_H = c/H₀ is the Hubble distance.
    """
    def integrand(z_prime):
        return 1.0 / np.sqrt(OMEGA_M * (1 + z_prime)**3 + OMEGA_LAMBDA)

    result, _ = quad(integrand, 0, z)
    return D_H_GPC * result


def z2_redshift_from_distance(d_gpc):
    """
    Inverse function: find z given comoving distance.
    Uses root-finding on the distance integral.
    """
    if d_gpc <= 0:
        return 0.0

    # Maximum redshift to search
    z_max = 20.0

    def func(z):
        return z2_comoving_distance_gpc(z) - d_gpc

    # Check if distance is within range
    d_max = z2_comoving_distance_gpc(z_max)
    if d_gpc > d_max:
        return z_max  # Saturate at z_max

    try:
        z = brentq(func, 0, z_max)
        return z
    except:
        return z_max


# Pre-compute distance-redshift table for speed
print("\nPre-computing distance-redshift lookup table...")
Z_TABLE = np.linspace(0, 15, 1000)
D_TABLE = np.array([z2_comoving_distance_gpc(z) for z in Z_TABLE])
print(f"  z range: 0 - {Z_TABLE[-1]:.1f}")
print(f"  D range: 0 - {D_TABLE[-1]:.2f} Gpc")


def fast_redshift_from_distance(d_gpc):
    """Fast lookup using pre-computed table."""
    if d_gpc <= 0:
        return 0.0
    if d_gpc >= D_TABLE[-1]:
        return Z_TABLE[-1]
    return np.interp(d_gpc, D_TABLE, Z_TABLE)

# =============================================================================
# COORDINATE TRANSFORMATIONS
# =============================================================================

def spherical_to_cartesian(ra_deg, dec_deg, d_gpc):
    """
    Convert spherical coordinates (RA, Dec, D) to Cartesian (x, y, z).

    Convention:
    - x points toward (RA=0, Dec=0)
    - y points toward (RA=90, Dec=0)
    - z points toward Dec=+90 (North Celestial Pole)
    """
    ra_rad = np.radians(ra_deg)
    dec_rad = np.radians(dec_deg)

    x = d_gpc * np.cos(dec_rad) * np.cos(ra_rad)
    y = d_gpc * np.cos(dec_rad) * np.sin(ra_rad)
    z = d_gpc * np.sin(dec_rad)

    return x, y, z


def cartesian_to_spherical(x, y, z):
    """
    Convert Cartesian (x, y, z) to spherical coordinates (RA, Dec, D).

    Returns:
    - ra_deg: Right Ascension in degrees [0, 360)
    - dec_deg: Declination in degrees [-90, +90]
    - d_gpc: Distance in Gpc
    """
    d = np.sqrt(x**2 + y**2 + z**2)

    if d == 0:
        return 0.0, 0.0, 0.0

    dec_rad = np.arcsin(z / d)
    ra_rad = np.arctan2(y, x)

    ra_deg = np.degrees(ra_rad)
    if ra_deg < 0:
        ra_deg += 360.0

    dec_deg = np.degrees(dec_rad)

    return ra_deg, dec_deg, d

# =============================================================================
# T³/Z₂ TOPOLOGICAL TRANSLATIONS
# =============================================================================

def compute_ghost_coordinates(ra, dec, z_obs):
    """
    Compute the 6 primary face-ghost coordinates for a quasar.

    In T³/Z₂ topology, a quasar at position r = (x, y, z) has ghost images at:
    r_ghost = r ± L_c * ê_i for i = 1, 2, 3

    The Z₂ identification x ~ -x creates additional symmetry, but we focus
    on the primary face ghosts which are most detectable.

    Returns list of 6 ghost predictions:
    [(RA, Dec, z_predicted, ghost_type, path_length), ...]
    """
    # Get true comoving position
    d_true = z2_comoving_distance_gpc(z_obs)
    x, y, z = spherical_to_cartesian(ra, dec, d_true)

    ghosts = []

    # The 6 translation vectors (face-centered ghosts)
    translations = [
        ('+X', L_C_GPC, 0, 0),
        ('-X', -L_C_GPC, 0, 0),
        ('+Y', 0, L_C_GPC, 0),
        ('-Y', 0, -L_C_GPC, 0),
        ('+Z', 0, 0, L_C_GPC),
        ('-Z', 0, 0, -L_C_GPC),
    ]

    for label, dx, dy, dz in translations:
        # Ghost position in Cartesian
        x_ghost = x + dx
        y_ghost = y + dy
        z_ghost = z + dz

        # Convert back to spherical
        ra_ghost, dec_ghost, d_ghost = cartesian_to_spherical(
            x_ghost, y_ghost, z_ghost
        )

        # Skip if ghost is behind us (negative distance) or too close
        if d_ghost < 1.0:  # Less than 1 Gpc
            continue

        # Convert distance to redshift
        z_ghost = fast_redshift_from_distance(d_ghost)

        # Calculate angular separation
        sep = angular_separation(ra, dec, ra_ghost, dec_ghost)

        # Calculate flux ratio (inverse square law)
        flux_ratio = (d_true / d_ghost)**2 if d_ghost > d_true else (d_ghost / d_true)**2

        # Time delay (path length difference in Myr)
        # Light travel time difference: Δt = (D_ghost - D_true) / c
        # In Gpc/c ≈ 3.26 Gyr per Gpc
        time_delay_myr = (d_ghost - d_true) * 3260  # Myr

        ghosts.append({
            'RA_ghost': ra_ghost,
            'Dec_ghost': dec_ghost,
            'z_ghost': z_ghost,
            'D_ghost_gpc': d_ghost,
            'ghost_type': f'face_{label}',
            'separation_deg': sep,
            'flux_ratio': flux_ratio,
            'time_delay_myr': time_delay_myr
        })

    return ghosts


def angular_separation(ra1, dec1, ra2, dec2):
    """Angular separation in degrees using Vincenty formula."""
    ra1, dec1, ra2, dec2 = map(np.radians, [ra1, dec1, ra2, dec2])

    cos_sep = (np.sin(dec1) * np.sin(dec2) +
               np.cos(dec1) * np.cos(dec2) * np.cos(ra1 - ra2))
    cos_sep = np.clip(cos_sep, -1, 1)

    return np.degrees(np.arccos(cos_sep))

# =============================================================================
# MAIN PROCESSING
# =============================================================================

def process_candidates(input_file):
    """
    Process all high-z quasar candidates and compute ghost predictions.
    """
    print("\n" + "-" * 60)
    print("LOADING CANDIDATE CATALOG")
    print("-" * 60)

    # Load input from Work-Order V
    if not Path(input_file).exists():
        print(f"✗ Input file not found: {input_file}")
        print("  Run WORK-ORDER V first to generate candidates.")
        return None

    candidates = Table.read(input_file)
    print(f"✓ Loaded {len(candidates):,} candidates")

    # Process each candidate
    print("\n" + "-" * 60)
    print("COMPUTING GHOST COORDINATES")
    print("-" * 60)

    all_ghosts = []

    for i, cand in enumerate(candidates):
        ra = float(cand['RA'])
        dec = float(cand['DEC'])
        z_obs = float(cand['Z'])

        # Get ghost predictions
        ghosts = compute_ghost_coordinates(ra, dec, z_obs)

        for ghost in ghosts:
            all_ghosts.append({
                'PRIMARY_NAME': str(cand['NAME']) if 'NAME' in cand.colnames else f"Q{i}",
                'PRIMARY_RA': ra,
                'PRIMARY_DEC': dec,
                'PRIMARY_Z': z_obs,
                'PRIMARY_D_GPC': float(cand['D_C_GPC']) if 'D_C_GPC' in cand.colnames else z2_comoving_distance_gpc(z_obs),
                **ghost
            })

        if (i + 1) % 5000 == 0:
            print(f"  Progress: {i+1:,}/{len(candidates):,} ({100*(i+1)/len(candidates):.1f}%)")

    print(f"\n✓ Generated {len(all_ghosts):,} ghost predictions")
    print(f"  ({len(all_ghosts)/len(candidates):.1f} ghosts per quasar on average)")

    return all_ghosts


def save_ghost_predictions(ghosts, filename='predicted_ghost_coordinates.fits'):
    """
    Save ghost coordinate predictions to FITS file.
    """
    print("\n" + "-" * 60)
    print("SAVING GHOST PREDICTIONS")
    print("-" * 60)

    # Create table
    t = Table()

    cols = ['PRIMARY_NAME', 'PRIMARY_RA', 'PRIMARY_DEC', 'PRIMARY_Z', 'PRIMARY_D_GPC',
            'RA_ghost', 'Dec_ghost', 'z_ghost', 'D_ghost_gpc', 'ghost_type',
            'separation_deg', 'flux_ratio', 'time_delay_myr']

    for col in cols:
        t[col] = [g[col] for g in ghosts]

    output_file = OUTPUT_DIR / filename
    t.write(output_file, format='fits', overwrite=True)
    print(f"✓ Saved: {output_file}")

    # Summary JSON
    summary = {
        'work_order': 'W',
        'task': 'Geometric Translation Engine',
        'date': datetime.now().isoformat(),
        'parameters': {
            'L_c_gpc': L_C_GPC,
            'omega_m': OMEGA_M,
            'omega_lambda': OMEGA_LAMBDA
        },
        'results': {
            'total_ghosts': len(ghosts),
            'unique_primaries': len(set(g['PRIMARY_NAME'] for g in ghosts)),
            'z_ghost_range': [float(min(g['z_ghost'] for g in ghosts)),
                              float(max(g['z_ghost'] for g in ghosts))],
            'separation_range': [float(min(g['separation_deg'] for g in ghosts)),
                                float(max(g['separation_deg'] for g in ghosts))]
        },
        'output_file': str(output_file),
        'next_step': 'WORK-ORDER X: Spectroscopic Cross-Match'
    }

    summary_file = OUTPUT_DIR / 'WORK_ORDER_W_summary.json'
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2)
    print(f"✓ Summary: {summary_file}")

    return output_file


# =============================================================================
# MAIN EXECUTION
# =============================================================================

def main():
    """Execute Work-Order W: Geometric Translation Engine"""

    print("\n" + "=" * 80)
    print("EXECUTING WORK-ORDER W")
    print("=" * 80)

    # Input from Work-Order V
    input_file = OUTPUT_DIR / 'high_z_quasar_candidates.fits'

    # Process candidates
    ghosts = process_candidates(input_file)

    if ghosts is None:
        print("\n✗ Work-Order W failed. Missing input from Work-Order V.")
        return None

    # Save predictions
    output_file = save_ghost_predictions(ghosts)

    # Statistics
    separations = [g['separation_deg'] for g in ghosts]
    z_ghosts = [g['z_ghost'] for g in ghosts]

    print("\n" + "=" * 80)
    print("WORK-ORDER W COMPLETE")
    print("=" * 80)
    print(f"""
┌─────────────────────────────────────────────────────────────────┐
│            WORK-ORDER W: GEOMETRIC ENGINE COMPLETE               │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Primary quasars processed:   {len(set(g['PRIMARY_NAME'] for g in ghosts)):>10,}                    │
│  Ghost predictions generated: {len(ghosts):>10,}                    │
│                                                                 │
│  Ghost redshift range:        z = {min(z_ghosts):.2f} - {max(z_ghosts):.2f}          │
│  Angular separation range:    {min(separations):.1f}° - {max(separations):.1f}°             │
│                                                                 │
│  Output: predicted_ghost_coordinates.fits                       │
│                                                                 │
│  NEXT: Execute WORK-ORDER X (Spectroscopic Cross-Match)         │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

    return output_file


if __name__ == "__main__":
    main()
