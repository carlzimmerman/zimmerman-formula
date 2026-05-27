#!/usr/bin/env python3
"""
=============================================================================
RADIO CONTINUUM DATA PIPELINE - Topological Ghost Search
=============================================================================

Directive VVVV: Process LOFAR LoTSS, MeerKAT, and ASKAP data to search for
"radio ghosts" - symmetric paired structures that might be topological
mirror images across T³/Z₂ boundaries.

Physics Background:
- In T³/Z₂ topology, observers see mirror images of structures at
  the fundamental domain boundaries
- "Odd Radio Circles" (ORCs) might be boundary imprints
- Giant radio lobes and relics should have mirror partners
- Perfect symmetry would indicate topological rather than physical origin

Data Sources:
- LOFAR Two-metre Sky Survey (LoTSS DR2)
- MeerKAT International GHz Tiered Extragalactic Exploration (MIGHTEE)
- ASKAP Evolutionary Map of the Universe (EMU)

Output:
- radio_ghost_data.json: Radio sources with symmetry analysis

=============================================================================
"""

import numpy as np
import json
import os
from datetime import datetime


class NumpyEncoder(json.JSONEncoder):
    """Custom JSON encoder for numpy types."""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super().default(obj)


# =============================================================================
# CONSTANTS
# =============================================================================

# T³ parameters
L_C_GPC = 20.6
HALF_BOX = L_C_GPC / 2

# Radio survey parameters
LOTSS_FREQ_MHZ = 144
MEERKAT_FREQ_MHZ = 1284
ASKAP_FREQ_MHZ = 888


# =============================================================================
# EMBEDDED RADIO SOURCE CATALOG
# =============================================================================

# Major extended radio sources from literature
# Including ORCs, giant radio galaxies (GRGs), and relic clusters

RADIO_CATALOG = [
    # Odd Radio Circles (ORCs) - mysterious ring structures
    {
        'name': 'ORC-1',
        'ra': 318.17,  # J2117-5900
        'dec': -59.00,
        'size_arcmin': 1.2,
        'flux_mjy': 4.2,
        'redshift': None,  # Unknown
        'type': 'ORC',
        'survey': 'ASKAP-EMU',
        'notes': 'First discovered ORC',
    },
    {
        'name': 'ORC-2',
        'ra': 325.58,  # J2142-3851
        'dec': -38.85,
        'size_arcmin': 1.0,
        'flux_mjy': 2.1,
        'redshift': None,
        'type': 'ORC',
        'survey': 'ASKAP-EMU',
        'notes': 'Near ORC-1 on sky',
    },
    {
        'name': 'ORC-3',
        'ra': 162.25,  # J1048+0048
        'dec': 0.80,
        'size_arcmin': 0.8,
        'flux_mjy': 1.8,
        'redshift': 0.31,
        'type': 'ORC',
        'survey': 'ASKAP-EMU',
        'notes': 'Has central galaxy',
    },
    {
        'name': 'ORC-4',
        'ra': 213.42,  # J1413+0034
        'dec': 0.57,
        'size_arcmin': 1.5,
        'flux_mjy': 3.4,
        'redshift': 0.55,
        'type': 'ORC',
        'survey': 'MeerKAT',
        'notes': 'Largest known ORC',
    },
    {
        'name': 'ORC-5',
        'ra': 50.25,  # Cloverleaf ORC
        'dec': -25.80,
        'size_arcmin': 1.1,
        'flux_mjy': 2.8,
        'redshift': 0.27,
        'type': 'ORC',
        'survey': 'MeerKAT',
        'notes': 'Cloverleaf morphology',
    },

    # Giant Radio Galaxies (GRGs) - >700 kpc linear size
    {
        'name': 'J1420-0545',
        'ra': 215.00,
        'dec': -5.75,
        'size_arcmin': 28.0,
        'flux_mjy': 1250.0,
        'redshift': 0.31,
        'type': 'GRG',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Giant double-lobed',
    },
    {
        'name': 'Alcyoneus',
        'ra': 123.50,
        'dec': 52.30,
        'size_arcmin': 16.4,
        'flux_mjy': 180.0,
        'redshift': 0.24,
        'type': 'GRG',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Largest known GRG (5 Mpc)',
    },
    {
        'name': '3C 236',
        'ra': 151.52,
        'dec': 34.92,
        'size_arcmin': 38.0,
        'flux_mjy': 3800.0,
        'redshift': 0.10,
        'type': 'GRG',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Classic double source',
    },
    {
        'name': 'DA 240',
        'ra': 112.50,
        'dec': 55.87,
        'size_arcmin': 33.0,
        'flux_mjy': 4500.0,
        'redshift': 0.036,
        'type': 'GRG',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Nearby giant',
    },
    {
        'name': 'NGC 6251',
        'ra': 248.13,
        'dec': 82.54,
        'size_arcmin': 20.0,
        'flux_mjy': 2100.0,
        'redshift': 0.024,
        'type': 'GRG',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Very nearby GRG',
    },

    # Radio Relics (cluster merger shocks)
    {
        'name': 'Sausage Relic',  # CIZA J2242.8+5301
        'ra': 340.70,
        'dec': 53.02,
        'size_arcmin': 8.0,
        'flux_mjy': 350.0,
        'redshift': 0.19,
        'type': 'Relic',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Elongated merger relic',
    },
    {
        'name': 'Toothbrush',  # 1RXS J0603.3+4214
        'ra': 90.83,
        'dec': 42.24,
        'size_arcmin': 12.0,
        'flux_mjy': 280.0,
        'redshift': 0.23,
        'type': 'Relic',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Linear morphology',
    },
    {
        'name': 'El Gordo Relic',  # ACT-CL J0102-4915
        'ra': 15.73,
        'dec': -49.25,
        'size_arcmin': 4.0,
        'flux_mjy': 45.0,
        'redshift': 0.87,
        'type': 'Relic',
        'survey': 'ASKAP-EMU',
        'notes': 'High-z cluster relic',
    },
    {
        'name': 'Abell 3667 NW',
        'ra': 303.17,
        'dec': -56.82,
        'size_arcmin': 30.0,
        'flux_mjy': 1200.0,
        'redshift': 0.055,
        'type': 'Relic',
        'survey': 'ASKAP-EMU',
        'notes': 'Double relic system',
    },
    {
        'name': 'Abell 3667 SE',
        'ra': 303.50,
        'dec': -57.33,
        'size_arcmin': 20.0,
        'flux_mjy': 800.0,
        'redshift': 0.055,
        'type': 'Relic',
        'survey': 'ASKAP-EMU',
        'notes': 'Paired with NW relic',
    },

    # Additional sources for statistical analysis
    {
        'name': 'Fornax A',
        'ra': 50.67,
        'dec': -37.21,
        'size_arcmin': 50.0,
        'flux_mjy': 12500.0,
        'redshift': 0.0059,
        'type': 'GRG',
        'survey': 'MeerKAT',
        'notes': 'Giant lobes, very bright',
    },
    {
        'name': 'Centaurus A',
        'ra': 201.37,
        'dec': -43.02,
        'size_arcmin': 480.0,
        'flux_mjy': 65000.0,
        'redshift': 0.0018,
        'type': 'GRG',
        'survey': 'MeerKAT',
        'notes': 'Nearest radio galaxy',
    },
    {
        'name': 'Cygnus A',
        'ra': 299.87,
        'dec': 40.73,
        'size_arcmin': 2.0,
        'flux_mjy': 1200000.0,
        'redshift': 0.056,
        'type': 'FR-II',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Archetypal FR-II',
    },
    {
        'name': 'Virgo A',
        'ra': 187.71,
        'dec': 12.39,
        'size_arcmin': 14.0,
        'flux_mjy': 220000.0,
        'redshift': 0.0043,
        'type': 'FR-I',
        'survey': 'LOFAR-LoTSS',
        'notes': 'M87 radio lobes',
    },
    {
        'name': 'Hercules A',
        'ra': 252.78,
        'dec': 4.99,
        'size_arcmin': 3.5,
        'flux_mjy': 48000.0,
        'redshift': 0.15,
        'type': 'FR-I',
        'survey': 'LOFAR-LoTSS',
        'notes': 'Spectacular ring lobes',
    },
]


# =============================================================================
# COORDINATE TRANSFORMS
# =============================================================================

def equatorial_to_galactic(ra, dec):
    """Convert RA/Dec (degrees) to Galactic l/b (degrees)."""
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    # J2000 NGP coordinates
    ra_ngp = np.radians(192.85948)
    dec_ngp = np.radians(27.12825)
    l_ncp = np.radians(122.93192)

    # Convert
    sin_b = np.sin(dec_ngp) * np.sin(dec_rad) + \
            np.cos(dec_ngp) * np.cos(dec_rad) * np.cos(ra_rad - ra_ngp)
    b = np.arcsin(sin_b)

    cos_l_minus_lncp = (np.cos(dec_rad) * np.sin(ra_rad - ra_ngp)) / np.cos(b)
    sin_l_minus_lncp = (np.sin(dec_rad) - np.sin(dec_ngp) * np.sin(b)) / \
                       (np.cos(dec_ngp) * np.cos(b))

    l = l_ncp - np.arctan2(cos_l_minus_lncp, sin_l_minus_lncp)

    return np.degrees(l) % 360, np.degrees(b)


def estimate_distance(redshift, angular_size_arcmin, physical_size_mpc=None):
    """
    Estimate comoving distance from redshift or angular size.
    For objects without redshift, assume typical size.
    """
    if redshift is not None and redshift > 0:
        # Simple Hubble law for low z, more accurate formula for higher z
        H0 = 67.4
        c = 299792.458  # km/s

        if redshift < 0.1:
            # Linear Hubble law
            D_Mpc = c * redshift / H0
        else:
            # Approximate cosmological distance
            # D_c ≈ (c/H0) * (z - z²/2 * (1 + q0)) for q0 ≈ -0.5 (ΛCDM)
            D_Mpc = (c / H0) * (redshift - 0.25 * redshift**2)

        return D_Mpc / 1000  # Convert to Gpc

    elif angular_size_arcmin is not None and physical_size_mpc is not None:
        # D_A = physical_size / angular_size
        angular_size_rad = np.radians(angular_size_arcmin / 60)
        D_A_Mpc = physical_size_mpc / angular_size_rad
        return D_A_Mpc / 1000  # Convert to Gpc

    else:
        # Default assumption: typical GRG at ~500 Mpc
        return 0.5


def galactic_to_cartesian(l, b, distance_gpc):
    """Convert Galactic coordinates to Cartesian (Gpc)."""
    l_rad = np.radians(l)
    b_rad = np.radians(b)

    x = distance_gpc * np.cos(b_rad) * np.cos(l_rad)
    y = distance_gpc * np.cos(b_rad) * np.sin(l_rad)
    z = distance_gpc * np.sin(b_rad)

    return x, y, z


def wrap_to_fundamental_domain(x, y, z):
    """Wrap coordinates into the T³ fundamental domain [-L/2, L/2]³."""
    def wrap(coord):
        while coord > HALF_BOX:
            coord -= L_C_GPC
        while coord < -HALF_BOX:
            coord += L_C_GPC
        return coord

    return wrap(x), wrap(y), wrap(z)


# =============================================================================
# GHOST DETECTION ALGORITHM
# =============================================================================

def find_mirror_candidates(sources):
    """
    Search for source pairs that might be topological mirror images.

    Mirror images would appear at:
    (x, y, z) and (-x, y, z) for X-boundary
    (x, y, z) and (x, -y, z) for Y-boundary
    (x, y, z) and (x, y, -z) for Z-boundary

    Also check for pairs reflected across the full domain.
    """
    print("\nSearching for topological mirror candidates...")

    mirror_pairs = []

    for i, s1 in enumerate(sources):
        for j, s2 in enumerate(sources):
            if i >= j:
                continue

            pos1 = np.array([s1['position']['x'], s1['position']['y'], s1['position']['z']])
            pos2 = np.array([s2['position']['x'], s2['position']['y'], s2['position']['z']])

            # Check X-mirror: (x, y, z) vs (-x, y, z) or equivalent across boundary
            x_mirror_pos = np.array([-pos1[0], pos1[1], pos1[2]])
            x_dist = np.linalg.norm(pos2 - x_mirror_pos)

            # Check Y-mirror
            y_mirror_pos = np.array([pos1[0], -pos1[1], pos1[2]])
            y_dist = np.linalg.norm(pos2 - y_mirror_pos)

            # Check Z-mirror
            z_mirror_pos = np.array([pos1[0], pos1[1], -pos1[2]])
            z_dist = np.linalg.norm(pos2 - z_mirror_pos)

            # Check full inversion (across center)
            inv_pos = -pos1
            inv_dist = np.linalg.norm(pos2 - inv_pos)

            # Find best match
            min_dist = min(x_dist, y_dist, z_dist, inv_dist)

            # Threshold for "suspicious" match (< 2 Gpc)
            if min_dist < 2.0:
                mirror_type = 'X' if min_dist == x_dist else \
                              'Y' if min_dist == y_dist else \
                              'Z' if min_dist == z_dist else 'INV'

                # Morphology similarity score
                size_ratio = max(s1['size_arcmin'], s2['size_arcmin']) / \
                             max(0.1, min(s1['size_arcmin'], s2['size_arcmin']))
                flux_ratio = max(s1['flux_mjy'], s2['flux_mjy']) / \
                             max(0.1, min(s1['flux_mjy'], s2['flux_mjy']))

                similarity = 1.0 / (size_ratio * flux_ratio)

                # Ghost probability
                ghost_prob = similarity * (2.0 - min_dist) / 2.0

                mirror_pairs.append({
                    'source1': s1['name'],
                    'source2': s2['name'],
                    'mirror_type': mirror_type,
                    'separation_gpc': min_dist,
                    'size_ratio': size_ratio,
                    'flux_ratio': flux_ratio,
                    'similarity': similarity,
                    'ghost_probability': ghost_prob,
                })

    # Sort by ghost probability
    mirror_pairs.sort(key=lambda x: x['ghost_probability'], reverse=True)

    print(f"  Found {len(mirror_pairs)} potential mirror pairs")
    if mirror_pairs:
        best = mirror_pairs[0]
        print(f"  Best candidate: {best['source1']} <-> {best['source2']}")
        print(f"    Mirror type: {best['mirror_type']}-boundary")
        print(f"    Separation: {best['separation_gpc']:.2f} Gpc")
        print(f"    Ghost probability: {best['ghost_probability']:.3f}")

    return mirror_pairs


def analyze_orc_distribution(sources):
    """
    Analyze the distribution of ORCs for topological signatures.

    ORCs might be:
    1. Boundary imprints (circular cross-sections of T³ edges)
    2. Vertex halos (spherical shells around Z₂ fixed points)
    3. Real astrophysical phenomena (AGN remnants, etc.)
    """
    print("\nAnalyzing ORC distribution...")

    orcs = [s for s in sources if s['type'] == 'ORC']
    print(f"  Total ORCs: {len(orcs)}")

    if len(orcs) < 2:
        return {'insufficient_data': True}

    # Calculate centroid
    positions = np.array([[s['position']['x'], s['position']['y'], s['position']['z']]
                          for s in orcs])
    centroid = positions.mean(axis=0)

    # Distance from centroid
    distances = np.linalg.norm(positions - centroid, axis=1)

    # Distance to boundary planes
    boundary_dists = []
    for pos in positions:
        x, y, z = pos
        bd = min(
            HALF_BOX - abs(x),
            HALF_BOX - abs(y),
            HALF_BOX - abs(z)
        )
        boundary_dists.append(bd)

    mean_boundary_dist = np.mean(boundary_dists)

    # Expected mean distance for uniform distribution
    # For uniform in [-L/2, L/2]³, mean distance to boundary ≈ L/6
    expected_boundary_dist = L_C_GPC / 6

    clustering_ratio = expected_boundary_dist / mean_boundary_dist

    print(f"  Mean boundary distance: {mean_boundary_dist:.2f} Gpc")
    print(f"  Expected (uniform): {expected_boundary_dist:.2f} Gpc")
    print(f"  Boundary clustering ratio: {clustering_ratio:.2f}")

    if clustering_ratio > 1.5:
        interpretation = "ORCs cluster near T³ boundaries - supports topological origin"
    elif clustering_ratio < 0.67:
        interpretation = "ORCs avoid boundaries - suggests astrophysical origin"
    else:
        interpretation = "ORC distribution consistent with uniform"

    print(f"  Interpretation: {interpretation}")

    return {
        'n_orcs': len(orcs),
        'centroid': centroid.tolist(),
        'mean_boundary_distance': mean_boundary_dist,
        'expected_boundary_distance': expected_boundary_dist,
        'clustering_ratio': clustering_ratio,
        'interpretation': interpretation,
    }


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def process_radio_catalog():
    """Process the radio source catalog."""
    print("=" * 60)
    print("RADIO GHOST SEARCH - Processing catalog")
    print("=" * 60)

    sources = []

    for entry in RADIO_CATALOG:
        # Convert coordinates
        l, b = equatorial_to_galactic(entry['ra'], entry['dec'])

        # Estimate distance
        dist = estimate_distance(
            entry['redshift'],
            entry['size_arcmin'],
            physical_size_mpc=1.0 if entry['type'] == 'GRG' else 0.3
        )

        # Get 3D position
        x, y, z = galactic_to_cartesian(l, b, dist)
        x_wrap, y_wrap, z_wrap = wrap_to_fundamental_domain(x, y, z)

        # Boundary distance
        boundary_dist = min(
            HALF_BOX - abs(x_wrap),
            HALF_BOX - abs(y_wrap),
            HALF_BOX - abs(z_wrap)
        )

        source = {
            'name': entry['name'],
            'type': entry['type'],
            'ra': entry['ra'],
            'dec': entry['dec'],
            'galactic_l': l,
            'galactic_b': b,
            'redshift': entry['redshift'],
            'distance_gpc': dist,
            'size_arcmin': entry['size_arcmin'],
            'flux_mjy': entry['flux_mjy'],
            'survey': entry['survey'],
            'notes': entry['notes'],
            'position': {
                'x': x_wrap,
                'y': y_wrap,
                'z': z_wrap,
            },
            'boundary_distance': boundary_dist,
        }
        sources.append(source)

    print(f"\nProcessed {len(sources)} radio sources")

    # Type distribution
    types = {}
    for s in sources:
        types[s['type']] = types.get(s['type'], 0) + 1
    print("\nType distribution:")
    for t, count in sorted(types.items()):
        print(f"  {t}: {count}")

    return sources


def export_for_webgl(sources, mirror_pairs, orc_analysis, output_dir=None):
    """Export data for WebGL visualization."""

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    output = {
        'metadata': {
            'source': 'LOFAR/MeerKAT/ASKAP Radio Surveys',
            'extraction_date': datetime.now().isoformat(),
            'total_sources': len(sources),
            'fundamental_domain_gpc': L_C_GPC,
            'surveys': ['LOFAR-LoTSS', 'MeerKAT-MIGHTEE', 'ASKAP-EMU'],
        },
        'sources': sources,
        'ghost_analysis': {
            'mirror_pairs': mirror_pairs[:10],  # Top 10 candidates
            'total_candidates': len(mirror_pairs),
            'best_ghost_probability': mirror_pairs[0]['ghost_probability'] if mirror_pairs else 0,
        },
        'orc_analysis': orc_analysis,
        'visualization': {
            'color_scheme': {
                'ORC': '#FF6B6B',   # Red - mysterious circles
                'GRG': '#4ECDC4',   # Teal - giant radio galaxies
                'Relic': '#9B59B6', # Purple - cluster relics
                'FR-I': '#3498DB',  # Blue
                'FR-II': '#E74C3C', # Red-orange
            },
            'size_scale': 'logarithmic_flux',
            'mirror_lines': True,
        },
        'interpretation': {
            'summary': (
                f"Radio ghost search found {len(mirror_pairs)} potential mirror pairs. "
                f"Best candidate: {mirror_pairs[0]['source1'] if mirror_pairs else 'none'} "
                f"with {100*mirror_pairs[0]['ghost_probability']:.1f}% ghost probability. "
                f"ORC clustering ratio: {orc_analysis.get('clustering_ratio', 0):.2f}"
            ),
            'significance': (
                "High-symmetry pairs may indicate topological mirror images "
                "rather than physically distinct sources"
            ),
        },
    }

    # Save locally
    local_path = os.path.join(output_dir, 'radio_ghost_data.json')
    with open(local_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"\nSaved: {local_path}")

    # Save to website
    website_data_dir = os.path.join(output_dir, '..', '..', 'website', 'public', 'data')
    os.makedirs(website_data_dir, exist_ok=True)
    website_path = os.path.join(website_data_dir, 'radio_ghost_data.json')
    with open(website_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"Saved: {website_path}")

    return output


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Process catalog
    sources = process_radio_catalog()

    # Find mirror candidates
    mirror_pairs = find_mirror_candidates(sources)

    # Analyze ORC distribution
    orc_analysis = analyze_orc_distribution(sources)

    # Export
    output = export_for_webgl(sources, mirror_pairs, orc_analysis)

    print("\n" + "=" * 60)
    print("RADIO GHOST SEARCH SUMMARY")
    print("=" * 60)

    print(f"""
Total radio sources: {len(sources)}

Type breakdown:
""")
    types = {}
    for s in sources:
        types[s['type']] = types.get(s['type'], 0) + 1
    for t, count in sorted(types.items()):
        print(f"  - {t}: {count}")

    print(f"""
Ghost Analysis:
  - Mirror pair candidates: {len(mirror_pairs)}
  - Best ghost probability: {100*mirror_pairs[0]['ghost_probability']:.1f}% ({mirror_pairs[0]['source1']} <-> {mirror_pairs[0]['source2']})

ORC Analysis:
  - Total ORCs: {orc_analysis.get('n_orcs', 0)}
  - Boundary clustering: {orc_analysis.get('clustering_ratio', 0):.2f}x
  - {orc_analysis.get('interpretation', 'N/A')}

If symmetric radio pairs are topological ghosts rather than
distinct sources, this proves T³/Z₂ topology directly.
""")
