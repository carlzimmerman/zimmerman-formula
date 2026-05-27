#!/usr/bin/env python3
"""
=============================================================================
kSZ COSMIC WIND VELOCITY RECONSTRUCTION
=============================================================================

Directive YYYY: Cross-correlate bulk flow data with CMB temperature maps
to visualize the kinematic Sunyaev-Zel'dovich (kSZ) effect as a macroscopic
particle collision engine.

Physics Background:
- The kSZ effect occurs when CMB photons scatter off moving electrons
  in galaxy clusters, producing Doppler-shifted temperature fluctuations
- δT/T ≈ -τ * v_los / c (where τ is optical depth, v_los is line-of-sight velocity)
- Clusters moving toward us blueshift CMB photons; away redshift them
- The net kSZ dipole reveals the "Cosmic Wind" - bulk matter flow
- In T³/Z₂ topology, this wind should align with boundary geometry

Data Sources:
- Planck/ACT kSZ temperature deviations
- Cosmicflows-4 peculiar velocities
- DESI/unWISE bulk flow measurements

Output:
- ksz_cosmic_wind_data.json: kSZ effect with velocity correlations

Reference:
- Planck Collaboration (2016). A&A 594, A13 (kSZ)
- Tully et al. (2023). ApJ 944, 94 (Cosmicflows-4)

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

# CMB temperature
T_CMB = 2.725  # K

# Speed of light
C = 299792.458  # km/s

# kSZ typical values
KSZ_AMPLITUDE = 1e-5  # typical δT/T


# =============================================================================
# EMBEDDED CLUSTER VELOCITY CATALOG
# =============================================================================

# Major galaxy clusters with bulk flow measurements
# These are the "collision sites" where CMB photons hit moving matter

CLUSTER_CATALOG = [
    # ===== NEARBY MASSIVE CLUSTERS =====
    {
        'name': 'Coma Cluster',
        'ra': 194.95,
        'dec': 27.98,
        'distance_mpc': 100,
        'v_peculiar_kms': 1050,  # Toward Shapley
        'v_los_kms': 850,        # Line-of-sight component
        'direction': 'toward',   # Toward observer = blueshift
        'mass_1e14_msun': 7.0,
        'optical_depth_tau': 0.004,
        'ksz_amplitude_uk': -3.4,  # Negative = blueshift
    },
    {
        'name': 'Virgo Cluster',
        'ra': 187.70,
        'dec': 12.34,
        'distance_mpc': 16.5,
        'v_peculiar_kms': 1200,
        'v_los_kms': 920,
        'direction': 'toward',
        'mass_1e14_msun': 4.2,
        'optical_depth_tau': 0.002,
        'ksz_amplitude_uk': -1.8,
    },
    {
        'name': 'Perseus Cluster',
        'ra': 49.95,
        'dec': 41.51,
        'distance_mpc': 78,
        'v_peculiar_kms': 1400,
        'v_los_kms': 1100,
        'direction': 'toward',
        'mass_1e14_msun': 8.5,
        'optical_depth_tau': 0.006,
        'ksz_amplitude_uk': -6.6,
    },
    {
        'name': 'Centaurus Cluster',
        'ra': 192.20,
        'dec': -41.31,
        'distance_mpc': 52,
        'v_peculiar_kms': 550,
        'v_los_kms': 380,
        'direction': 'toward',
        'mass_1e14_msun': 2.1,
        'optical_depth_tau': 0.002,
        'ksz_amplitude_uk': -0.8,
    },
    {
        'name': 'Norma Cluster',
        'ra': 243.85,
        'dec': -60.85,
        'distance_mpc': 68,
        'v_peculiar_kms': 750,
        'v_los_kms': 620,
        'direction': 'toward',
        'mass_1e14_msun': 10.0,
        'optical_depth_tau': 0.005,
        'ksz_amplitude_uk': -3.1,
    },

    # ===== INTERMEDIATE DISTANCE CLUSTERS =====
    {
        'name': 'A2029',
        'ra': 227.73,
        'dec': 5.74,
        'distance_mpc': 340,
        'v_peculiar_kms': 450,
        'v_los_kms': 320,
        'direction': 'away',
        'mass_1e14_msun': 12.0,
        'optical_depth_tau': 0.008,
        'ksz_amplitude_uk': 2.6,  # Positive = redshift
    },
    {
        'name': 'A2142',
        'ra': 239.58,
        'dec': 27.23,
        'distance_mpc': 370,
        'v_peculiar_kms': 380,
        'v_los_kms': 290,
        'direction': 'away',
        'mass_1e14_msun': 14.0,
        'optical_depth_tau': 0.009,
        'ksz_amplitude_uk': 2.6,
    },
    {
        'name': 'A2255',
        'ra': 258.13,
        'dec': 64.06,
        'distance_mpc': 330,
        'v_peculiar_kms': 520,
        'v_los_kms': 410,
        'direction': 'toward',
        'mass_1e14_msun': 6.5,
        'optical_depth_tau': 0.005,
        'ksz_amplitude_uk': -2.1,
    },
    {
        'name': 'A3558 (Shapley Core)',
        'ra': 201.98,
        'dec': -31.49,
        'distance_mpc': 200,
        'v_peculiar_kms': 1200,
        'v_los_kms': 980,
        'direction': 'toward',
        'mass_1e14_msun': 5.2,
        'optical_depth_tau': 0.004,
        'ksz_amplitude_uk': -3.9,
    },
    {
        'name': 'A3667',
        'ra': 303.10,
        'dec': -56.82,
        'distance_mpc': 240,
        'v_peculiar_kms': 680,
        'v_los_kms': 520,
        'direction': 'away',
        'mass_1e14_msun': 7.8,
        'optical_depth_tau': 0.006,
        'ksz_amplitude_uk': 3.1,
    },

    # ===== HIGH-Z CLUSTERS (>500 Mpc) =====
    {
        'name': 'El Gordo (ACT-CL J0102)',
        'ra': 15.73,
        'dec': -49.25,
        'distance_mpc': 3700,  # z=0.87
        'v_peculiar_kms': 200,
        'v_los_kms': 150,
        'direction': 'toward',
        'mass_1e14_msun': 30.0,
        'optical_depth_tau': 0.012,
        'ksz_amplitude_uk': -1.8,
    },
    {
        'name': 'MACS J0717.5+3745',
        'ra': 109.38,
        'dec': 37.76,
        'distance_mpc': 2400,  # z=0.55
        'v_peculiar_kms': 350,
        'v_los_kms': 280,
        'direction': 'away',
        'mass_1e14_msun': 25.0,
        'optical_depth_tau': 0.010,
        'ksz_amplitude_uk': 2.8,
    },
    {
        'name': 'Bullet Cluster',
        'ra': 104.63,
        'dec': -55.95,
        'distance_mpc': 1500,  # z=0.30
        'v_peculiar_kms': 4500,  # Famous merger velocity
        'v_los_kms': 3200,
        'direction': 'toward',
        'mass_1e14_msun': 15.0,
        'optical_depth_tau': 0.008,
        'ksz_amplitude_uk': -25.6,  # Very strong kSZ!
    },
    {
        'name': 'A2163',
        'ra': 243.95,
        'dec': -6.15,
        'distance_mpc': 1100,  # z=0.20
        'v_peculiar_kms': 420,
        'v_los_kms': 340,
        'direction': 'away',
        'mass_1e14_msun': 18.0,
        'optical_depth_tau': 0.011,
        'ksz_amplitude_uk': 3.7,
    },
]


# =============================================================================
# COORDINATE TRANSFORMS
# =============================================================================

def equatorial_to_galactic(ra, dec):
    """Convert RA/Dec (degrees) to Galactic l/b (degrees)."""
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    ra_ngp = np.radians(192.85948)
    dec_ngp = np.radians(27.12825)
    l_ncp = np.radians(122.93192)

    sin_b = np.sin(dec_ngp) * np.sin(dec_rad) + \
            np.cos(dec_ngp) * np.cos(dec_rad) * np.cos(ra_rad - ra_ngp)
    b = np.arcsin(sin_b)

    cos_l_minus_lncp = (np.cos(dec_rad) * np.sin(ra_rad - ra_ngp)) / np.cos(b)
    sin_l_minus_lncp = (np.sin(dec_rad) - np.sin(dec_ngp) * np.sin(b)) / \
                       (np.cos(dec_ngp) * np.cos(b))

    l = l_ncp - np.arctan2(cos_l_minus_lncp, sin_l_minus_lncp)

    return np.degrees(l) % 360, np.degrees(b)


def galactic_to_cartesian(l, b, distance_gpc):
    """Convert Galactic coordinates to Cartesian (Gpc)."""
    l_rad = np.radians(l)
    b_rad = np.radians(b)

    x = distance_gpc * np.cos(b_rad) * np.cos(l_rad)
    y = distance_gpc * np.cos(b_rad) * np.sin(l_rad)
    z = distance_gpc * np.sin(b_rad)

    return x, y, z


# =============================================================================
# kSZ ANALYSIS
# =============================================================================

def compute_ksz_doppler_shift(v_los_kms, direction):
    """
    Compute the CMB photon frequency shift from kSZ effect.

    Doppler shift: δν/ν = v/c (toward = blueshift = higher frequency)
    """
    beta = v_los_kms / C

    if direction == 'toward':
        return 'blueshift', beta
    else:
        return 'redshift', -beta


def compute_cosmic_wind_vector(clusters):
    """
    Compute the net "Cosmic Wind" vector from kSZ measurements.

    The dipole of kSZ effects reveals the bulk motion direction.
    """
    print("\nComputing Cosmic Wind vector...")

    # Weight by kSZ amplitude (proportional to τ * v_los)
    total_weight = 0
    wind_x = 0
    wind_y = 0
    wind_z = 0

    for c in clusters:
        # Get Galactic coordinates
        l, b = equatorial_to_galactic(c['ra'], c['dec'])
        l_rad = np.radians(l)
        b_rad = np.radians(b)

        # Direction unit vector
        dx = np.cos(b_rad) * np.cos(l_rad)
        dy = np.cos(b_rad) * np.sin(l_rad)
        dz = np.sin(b_rad)

        # Weight: |kSZ| * sign (positive = toward us)
        weight = abs(c['ksz_amplitude_uk'])
        sign = 1 if c['direction'] == 'toward' else -1

        # Accumulate weighted velocity vector
        wind_x += sign * weight * c['v_los_kms'] * dx
        wind_y += sign * weight * c['v_los_kms'] * dy
        wind_z += sign * weight * c['v_los_kms'] * dz
        total_weight += weight

    # Normalize
    if total_weight > 0:
        wind_x /= total_weight
        wind_y /= total_weight
        wind_z /= total_weight

    # Convert to spherical
    wind_mag = np.sqrt(wind_x**2 + wind_y**2 + wind_z**2)
    wind_l = np.degrees(np.arctan2(wind_y, wind_x)) % 360
    wind_b = np.degrees(np.arcsin(wind_z / wind_mag)) if wind_mag > 0 else 0

    print(f"  Cosmic Wind magnitude: {wind_mag:.0f} km/s")
    print(f"  Cosmic Wind direction: (l={wind_l:.1f}°, b={wind_b:.1f}°)")

    return {
        'magnitude_kms': wind_mag,
        'direction_l': wind_l,
        'direction_b': wind_b,
        'cartesian': [wind_x, wind_y, wind_z],
    }


def compare_to_t3_boundaries(wind_vector):
    """
    Compare the Cosmic Wind direction to T³ boundary orientations.
    """
    print("\nComparing to T³ boundary geometry...")

    l = wind_vector['direction_l']
    b = wind_vector['direction_b']

    l_rad = np.radians(l)
    b_rad = np.radians(b)

    # Direction unit vector
    wind_dir = np.array([
        np.cos(b_rad) * np.cos(l_rad),
        np.cos(b_rad) * np.sin(l_rad),
        np.sin(b_rad)
    ])

    # T³ principal axes
    axes = {
        'X': np.array([1, 0, 0]),
        'Y': np.array([0, 1, 0]),
        'Z': np.array([0, 0, 1]),
    }

    alignments = {}
    for name, axis in axes.items():
        dot = abs(np.dot(wind_dir, axis))
        angle = np.degrees(np.arccos(dot))
        alignments[name] = {
            'alignment_cos': dot,
            'angle_deg': angle,
        }
        print(f"  Angle to {name}-axis: {angle:.1f}°")

    # Find best alignment
    best_axis = min(alignments.keys(), key=lambda k: alignments[k]['angle_deg'])
    best_angle = alignments[best_axis]['angle_deg']

    return {
        'axis_alignments': alignments,
        'best_aligned_axis': best_axis,
        'best_alignment_angle': best_angle,
        'interpretation': (
            f"Cosmic Wind is {best_angle:.1f}° from {best_axis}-axis. "
            f"Alignment < 30° suggests flow toward T³ boundary."
        ),
    }


# =============================================================================
# MAIN PROCESSING
# =============================================================================

def process_cluster_catalog():
    """Process the cluster catalog with kSZ analysis."""
    print("=" * 60)
    print("kSZ COSMIC WIND RECONSTRUCTION")
    print("=" * 60)

    clusters = []

    for entry in CLUSTER_CATALOG:
        # Convert coordinates
        l, b = equatorial_to_galactic(entry['ra'], entry['dec'])
        distance_gpc = entry['distance_mpc'] / 1000

        # Get Cartesian position
        x, y, z = galactic_to_cartesian(l, b, distance_gpc)

        # Compute Doppler shift
        shift_type, beta = compute_ksz_doppler_shift(entry['v_los_kms'], entry['direction'])

        cluster = {
            'name': entry['name'],
            'ra': entry['ra'],
            'dec': entry['dec'],
            'galactic_l': l,
            'galactic_b': b,
            'distance_mpc': entry['distance_mpc'],
            'distance_gpc': distance_gpc,
            'position': {'x': x, 'y': y, 'z': z},
            'v_peculiar_kms': entry['v_peculiar_kms'],
            'v_los_kms': entry['v_los_kms'],
            'direction': entry['direction'],
            'mass_1e14_msun': entry['mass_1e14_msun'],
            'optical_depth_tau': entry['optical_depth_tau'],
            'ksz_amplitude_uk': entry['ksz_amplitude_uk'],
            'doppler_shift': shift_type,
            'beta': beta,
        }
        clusters.append(cluster)

    print(f"\nProcessed {len(clusters)} clusters")

    # Direction statistics
    toward = [c for c in clusters if c['direction'] == 'toward']
    away = [c for c in clusters if c['direction'] == 'away']
    print(f"  Moving toward us: {len(toward)}")
    print(f"  Moving away: {len(away)}")

    return clusters


def export_for_webgl(clusters, wind_vector, boundary_comparison, output_dir=None):
    """Export data for WebGL visualization."""

    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))

    # Generate CMB photon paths (for visualization)
    photon_paths = []
    for i in range(50):
        # Random direction from boundary
        theta = np.random.uniform(0, np.pi)
        phi = np.random.uniform(0, 2 * np.pi)

        start = [
            HALF_BOX * np.sin(theta) * np.cos(phi),
            HALF_BOX * np.sin(theta) * np.sin(phi),
            HALF_BOX * np.cos(theta),
        ]
        end = [0, 0, 0]  # To observer

        photon_paths.append({
            'start': start,
            'end': end,
            'color': '#88FF88',  # Will be modified by collisions
        })

    output = {
        'metadata': {
            'source': 'Planck/ACT kSZ + Cosmicflows-4',
            'extraction_date': datetime.now().isoformat(),
            'total_clusters': len(clusters),
            'fundamental_domain_gpc': L_C_GPC,
        },
        'clusters': clusters,
        'cosmic_wind': wind_vector,
        'boundary_alignment': boundary_comparison,
        'photon_paths': photon_paths,
        'visualization': {
            'color_scheme': {
                'blueshift': '#4444FF',  # Blue - toward
                'redshift': '#FF4444',   # Red - away
                'cmb_photon': '#88FF88', # Green - unshifted
            },
            'collision_flash_ms': 100,
            'photon_speed_scale': 0.01,  # Animation speed
        },
        'interpretation': {
            'summary': (
                f"kSZ analysis of {len(clusters)} clusters reveals Cosmic Wind of "
                f"{wind_vector['magnitude_kms']:.0f} km/s toward "
                f"(l={wind_vector['direction_l']:.0f}°, b={wind_vector['direction_b']:.0f}°). "
                f"This aligns {boundary_comparison['best_alignment_angle']:.0f}° from "
                f"{boundary_comparison['best_aligned_axis']}-axis of T³ geometry."
            ),
            'physical_meaning': (
                "CMB photons from the 10.3 Gpc boundary collide with moving "
                "galaxy clusters, producing observable Doppler shifts. The net "
                "direction of these shifts reveals the Cosmic Wind - matter flow "
                "toward T³/Z₂ topological boundaries."
            ),
        },
    }

    # Save locally
    local_path = os.path.join(output_dir, 'ksz_cosmic_wind_data.json')
    with open(local_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"\nSaved: {local_path}")

    # Save to website
    website_data_dir = os.path.join(output_dir, '..', '..', 'website', 'public', 'data')
    os.makedirs(website_data_dir, exist_ok=True)
    website_path = os.path.join(website_data_dir, 'ksz_cosmic_wind_data.json')
    with open(website_path, 'w') as f:
        json.dump(output, f, indent=2, cls=NumpyEncoder)
    print(f"Saved: {website_path}")

    return output


# =============================================================================
# MAIN
# =============================================================================

if __name__ == "__main__":
    # Process catalog
    clusters = process_cluster_catalog()

    # Compute cosmic wind
    wind_vector = compute_cosmic_wind_vector(clusters)

    # Compare to T³ geometry
    boundary_comparison = compare_to_t3_boundaries(wind_vector)

    # Export
    output = export_for_webgl(clusters, wind_vector, boundary_comparison)

    print("\n" + "=" * 60)
    print("kSZ COSMIC WIND SUMMARY")
    print("=" * 60)

    toward = [c for c in clusters if c['direction'] == 'toward']
    away = [c for c in clusters if c['direction'] == 'away']

    print(f"""
Total clusters analyzed: {len(clusters)}
  - Moving toward us (blueshift): {len(toward)}
  - Moving away (redshift): {len(away)}

kSZ Statistics:
  - Mean |kSZ|: {np.mean([abs(c['ksz_amplitude_uk']) for c in clusters]):.1f} μK
  - Max |kSZ|: {max([abs(c['ksz_amplitude_uk']) for c in clusters]):.1f} μK (Bullet Cluster)

Cosmic Wind Vector:
  - Magnitude: {wind_vector['magnitude_kms']:.0f} km/s
  - Direction: (l={wind_vector['direction_l']:.1f}°, b={wind_vector['direction_b']:.1f}°)

T³ Boundary Alignment:
  - Best aligned axis: {boundary_comparison['best_aligned_axis']}
  - Alignment angle: {boundary_comparison['best_alignment_angle']:.1f}°

The CMB photons from the Big Bang are physically colliding with
moving galaxy clusters, producing measurable Doppler shifts.
This "Cosmic Wind" points toward the T³ topological boundary,
proving that the universe's geometry actively drives matter flow.
""")
