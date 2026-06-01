#!/usr/bin/env python3
"""
Octupole Fixed-Point Sky Search: The T³/Z₂ Topological Fingerprint
====================================================================

The T³/Z₂ orbifold has 8 fixed points at vertices of a cube in the internal space.
If these fixed points anchor the vacuum structure, there may be measurable
anisotropies in the GW background correlated with these 8 directions.

This analysis:
1. Maps the 8 orbifold fixed points to celestial coordinates
2. Computes targeted cross-correlation at these 8 sky positions
3. Compares against isotropic expectation and random directions
4. Tests multiple alignment hypotheses (CMB, Galactic, Ecliptic)

Physics:
- Standard GR: Isotropic SGWB, no preferred directions
- Z² prediction: Enhanced correlation at 8 fixed-point directions

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal
from scipy.interpolate import interp1d
import healpy as hp
import h5py
import json
import os
import time
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# CONFIGURATION
# =============================================================================

OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))

# HEALPix resolution
NSIDE = 64
NPIX = hp.nside2npix(NSIDE)

# Analysis parameters
CONFIG = {
    'sample_rate': 4096,
    'f_low': 20,
    'f_high': 200,
    'segment_duration': 60,
}

# Physical constants
c = 299792458.0
H0 = 67.4 * 1000 / 3.086e22

def print_header(text):
    print("\n" + "=" * 80)
    print(f"  {text}")
    print("=" * 80)

def print_status(text):
    print(f"  [{time.strftime('%H:%M:%S')}] {text}")


# =============================================================================
# ORBIFOLD FIXED POINT GEOMETRY
# =============================================================================

def get_cube_vertices():
    """
    The 8 fixed points of T³/Z₂ correspond to the vertices of a unit cube.
    In internal coordinates: (y₁, y₂, y₃) ∈ {0, 1}³
    """
    vertices = []
    for i in [0, 1]:
        for j in [0, 1]:
            for k in [0, 1]:
                vertices.append((i, j, k))
    return np.array(vertices)


def cube_to_unit_sphere(vertices):
    """
    Map cube vertices to unit sphere.
    Center cube at origin, then project onto sphere.
    """
    # Shift to center at origin: {0,1} -> {-1,1}
    centered = 2 * vertices - 1

    # Normalize to unit sphere
    norms = np.linalg.norm(centered, axis=1, keepdims=True)
    unit_vectors = centered / norms

    return unit_vectors


def unit_vectors_to_sky_coords(unit_vectors, frame='galactic'):
    """
    Convert unit vectors to sky coordinates (theta, phi) in specified frame.

    Returns: (theta, phi) where theta ∈ [0, π], phi ∈ [0, 2π)
    """
    x, y, z = unit_vectors[:, 0], unit_vectors[:, 1], unit_vectors[:, 2]

    theta = np.arccos(z)  # Polar angle from +z
    phi = np.arctan2(y, x) % (2 * np.pi)  # Azimuthal angle

    return theta, phi


def rotate_to_frame(unit_vectors, from_frame='internal', to_frame='galactic'):
    """
    Apply rotation to align internal cube with specified astronomical frame.

    Alignment hypotheses:
    - 'galactic': Cube aligned with Galactic coordinate axes
    - 'cmb_dipole': One vertex points toward CMB dipole (l=264°, b=48°)
    - 'ecliptic': Cube aligned with ecliptic plane
    - 'cmb_octupole': Aligned with observed CMB octupole axis
    """
    if to_frame == 'galactic':
        # No rotation - cube axes aligned with Galactic (l, b) axes
        rotation = np.eye(3)

    elif to_frame == 'cmb_dipole':
        # Rotate so one vertex points toward CMB dipole
        # CMB dipole: (l, b) = (264°, 48°) in Galactic coordinates
        l_dip, b_dip = np.radians(264), np.radians(48)

        # Target direction
        target = np.array([
            np.cos(b_dip) * np.cos(l_dip),
            np.cos(b_dip) * np.sin(l_dip),
            np.sin(b_dip)
        ])

        # Rotate (1,1,1)/√3 vertex to target
        source = np.array([1, 1, 1]) / np.sqrt(3)
        rotation = rotation_matrix_between_vectors(source, target)

    elif to_frame == 'ecliptic':
        # Rotate from Galactic to Ecliptic
        # Ecliptic pole in Galactic: (l, b) ≈ (96°, 30°)
        rotation = galactic_to_ecliptic_rotation()

    elif to_frame == 'cmb_octupole':
        # Align with observed CMB octupole axis
        # CMB quadrupole-octupole alignment axis: (l, b) ≈ (240°, 63°)
        l_oct, b_oct = np.radians(240), np.radians(63)

        target = np.array([
            np.cos(b_oct) * np.cos(l_oct),
            np.cos(b_oct) * np.sin(l_oct),
            np.sin(b_oct)
        ])

        source = np.array([0, 0, 1])  # Align z-axis with octupole
        rotation = rotation_matrix_between_vectors(source, target)

    else:
        rotation = np.eye(3)

    return (rotation @ unit_vectors.T).T


def rotation_matrix_between_vectors(a, b):
    """Compute rotation matrix that rotates unit vector a to unit vector b."""
    a = a / np.linalg.norm(a)
    b = b / np.linalg.norm(b)

    v = np.cross(a, b)
    c = np.dot(a, b)
    s = np.linalg.norm(v)

    if s < 1e-10:  # Parallel or anti-parallel
        if c > 0:
            return np.eye(3)
        else:
            # 180° rotation around any perpendicular axis
            perp = np.array([1, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1, 0])
            perp = perp - np.dot(perp, a) * a
            perp = perp / np.linalg.norm(perp)
            return 2 * np.outer(perp, perp) - np.eye(3)

    vx = np.array([
        [0, -v[2], v[1]],
        [v[2], 0, -v[0]],
        [-v[1], v[0], 0]
    ])

    R = np.eye(3) + vx + vx @ vx * (1 - c) / (s * s)
    return R


def galactic_to_ecliptic_rotation():
    """Rotation matrix from Galactic to Ecliptic coordinates."""
    # Approximate transformation
    # Ecliptic pole in Galactic: (l, b) ≈ (96.4°, 29.8°)
    l_pole = np.radians(96.4)
    b_pole = np.radians(29.8)

    # This is a simplified rotation
    return rotation_matrix_between_vectors(
        np.array([0, 0, 1]),  # Galactic pole
        np.array([np.cos(b_pole)*np.cos(l_pole),
                  np.cos(b_pole)*np.sin(l_pole),
                  np.sin(b_pole)])
    )


def get_fixed_point_sky_positions(alignment='galactic'):
    """
    Get the 8 orbifold fixed point positions in sky coordinates.

    Returns: (theta, phi, l, b) arrays for 8 fixed points
    """
    # Get cube vertices
    vertices = get_cube_vertices()

    # Map to unit sphere
    unit_vectors = cube_to_unit_sphere(vertices)

    # Rotate to astronomical frame
    rotated = rotate_to_frame(unit_vectors, to_frame=alignment)

    # Convert to sky coordinates
    theta, phi = unit_vectors_to_sky_coords(rotated)

    # Convert to Galactic (l, b)
    l = np.degrees(phi)
    b = 90 - np.degrees(theta)

    return theta, phi, l, b


# =============================================================================
# DETECTOR RESPONSE AT FIXED POINTS
# =============================================================================

def antenna_pattern_pixel(theta, phi, det='H1'):
    """
    Compute antenna pattern F+ and F× for a single sky direction.
    """
    # Detector parameters (approximate)
    if det == 'H1':
        lat = np.radians(46.45)
        lon = np.radians(-119.41)
        arm_angle = np.radians(171.8)
    elif det == 'L1':
        lat = np.radians(30.56)
        lon = np.radians(-90.77)
        arm_angle = np.radians(243.0)
    elif det == 'V1':
        lat = np.radians(43.63)
        lon = np.radians(10.50)
        arm_angle = np.radians(116.5)
    else:
        raise ValueError(f"Unknown detector: {det}")

    # Simplified antenna pattern
    # This is an approximation - full calculation requires detector tensor

    cos_theta = np.cos(theta)
    sin_theta = np.sin(theta)
    cos_phi = np.cos(phi)
    sin_phi = np.sin(phi)

    # Approximate F+ and F×
    F_plus = 0.5 * (1 + cos_theta**2) * np.cos(2*phi)
    F_cross = cos_theta * np.sin(2*phi)

    return F_plus, F_cross


def compute_orf_at_direction(theta, phi, freq, baseline='H1-L1'):
    """
    Compute overlap reduction function for a specific sky direction.
    """
    det1, det2 = baseline.split('-')

    # Antenna patterns
    F1p, F1c = antenna_pattern_pixel(theta, phi, det1)
    F2p, F2c = antenna_pattern_pixel(theta, phi, det2)

    # ORF components
    gamma_pp = F1p * F2p
    gamma_cc = F1c * F2c
    gamma_total = gamma_pp + gamma_cc

    return gamma_pp, gamma_cc, gamma_total


# =============================================================================
# CROSS-CORRELATION ANALYSIS
# =============================================================================

def load_strain_data():
    """Load available strain data."""
    data = {}
    for det, fname in [('H1', 'h1_strain.hdf5'), ('L1', 'l1_strain.hdf5')]:
        filepath = os.path.join(OUTPUT_DIR, fname)
        if os.path.exists(filepath):
            with h5py.File(filepath, 'r') as f:
                data[det] = f['strain'][:].astype(np.float64)
            print_status(f"Loaded {det}: {len(data[det]):,} samples")
    return data


def compute_directional_correlation(h1_strain, l1_strain, theta, phi, config):
    """
    Compute cross-correlation weighted by antenna pattern for a specific direction.
    """
    fs = config['sample_rate']
    f_low = config['f_low']
    f_high = config['f_high']
    nperseg = int(config['segment_duration'] * fs)

    # Get antenna patterns at this direction
    F1p, F1c = antenna_pattern_pixel(theta, phi, 'H1')
    F2p, F2c = antenna_pattern_pixel(theta, phi, 'L1')

    # ORF for this direction
    gamma_pp = F1p * F2p
    gamma_total = F1p * F2p + F1c * F2c

    # Common length
    n_samples = min(len(h1_strain), len(l1_strain))
    h1 = h1_strain[:n_samples]
    l1 = l1_strain[:n_samples]

    # CSD
    freqs, Pxy = signal.csd(h1, l1, fs=fs, nperseg=nperseg)

    # Band selection
    mask = (freqs >= f_low) & (freqs <= f_high)
    freqs_band = freqs[mask]
    Pxy_band = Pxy[mask]

    # Directional correlation statistic
    # Weight by antenna pattern product
    weight = np.abs(gamma_total) if gamma_total != 0 else 1e-10

    # Mean correlation (real part)
    C = np.mean(np.real(Pxy_band)) * weight

    # R-ratio for this direction (if we could isolate it)
    gamma_pp_safe = gamma_pp if abs(gamma_pp) > 1e-10 else 1e-10
    gamma_total_safe = gamma_total if abs(gamma_total) > 1e-10 else 1e-10

    R_direction = gamma_total_safe / gamma_pp_safe

    return {
        'theta': theta,
        'phi': phi,
        'correlation': float(C),
        'gamma_pp': float(gamma_pp),
        'gamma_total': float(gamma_total),
        'R_direction': float(R_direction),
        'weight': float(weight),
    }


def generate_random_directions(n_directions, seed=42):
    """Generate uniformly distributed random sky directions."""
    np.random.seed(seed)
    phi = np.random.uniform(0, 2*np.pi, n_directions)
    cos_theta = np.random.uniform(-1, 1, n_directions)
    theta = np.arccos(cos_theta)
    return theta, phi


# =============================================================================
# MAIN ANALYSIS
# =============================================================================

def run_octupole_search():
    print_header("OCTUPOLE FIXED-POINT SKY SEARCH")
    print_status("Testing for T³/Z₂ topological fingerprint in GW correlations")

    # Load data
    print_header("LOADING DATA")
    strain_data = load_strain_data()

    if 'H1' not in strain_data or 'L1' not in strain_data:
        print_status("ERROR: Need both H1 and L1 data")
        return None

    # Test multiple alignment hypotheses
    alignments = ['galactic', 'cmb_dipole', 'cmb_octupole', 'ecliptic']

    results = {}

    for alignment in alignments:
        print_header(f"ALIGNMENT: {alignment.upper()}")

        # Get fixed point positions
        theta_fp, phi_fp, l_fp, b_fp = get_fixed_point_sky_positions(alignment)

        print_status("8 Fixed Point Positions (Galactic l, b):")
        for i in range(8):
            print(f"    FP{i+1}: (l={l_fp[i]:6.1f}°, b={b_fp[i]:+6.1f}°)")

        # Compute correlations at fixed points
        print_status("\nComputing correlations at fixed points...")
        fp_correlations = []

        for i in range(8):
            corr = compute_directional_correlation(
                strain_data['H1'], strain_data['L1'],
                theta_fp[i], phi_fp[i], CONFIG
            )
            fp_correlations.append(corr)
            print(f"    FP{i+1}: C = {corr['correlation']:+.2e}, γ_total = {corr['gamma_total']:+.3f}")

        # Generate random control directions
        print_status("\nComputing correlations at 100 random directions...")
        theta_rand, phi_rand = generate_random_directions(100)
        rand_correlations = []

        for i in range(100):
            corr = compute_directional_correlation(
                strain_data['H1'], strain_data['L1'],
                theta_rand[i], phi_rand[i], CONFIG
            )
            rand_correlations.append(corr)

        # Statistical comparison
        fp_C = np.array([c['correlation'] for c in fp_correlations])
        rand_C = np.array([c['correlation'] for c in rand_correlations])

        mean_fp = np.mean(np.abs(fp_C))
        std_fp = np.std(np.abs(fp_C))
        mean_rand = np.mean(np.abs(rand_C))
        std_rand = np.std(np.abs(rand_C))

        # Z-score: how many σ are fixed points above random?
        z_score = (mean_fp - mean_rand) / (std_rand / np.sqrt(100)) if std_rand > 0 else 0

        print_status(f"\nStatistical Comparison:")
        print_status(f"  Fixed Points: |C| = {mean_fp:.2e} ± {std_fp:.2e}")
        print_status(f"  Random Dirs:  |C| = {mean_rand:.2e} ± {std_rand:.2e}")
        print_status(f"  Z-score (FP vs Random): {z_score:+.2f}σ")

        results[alignment] = {
            'fixed_points': {
                'positions': [(float(l_fp[i]), float(b_fp[i])) for i in range(8)],
                'correlations': [float(c) for c in fp_C],
                'mean': float(mean_fp),
                'std': float(std_fp),
            },
            'random': {
                'mean': float(mean_rand),
                'std': float(std_rand),
            },
            'z_score': float(z_score),
            'significant': bool(abs(z_score) > 2),
        }

    # Summary
    print_header("OCTUPOLE SEARCH SUMMARY")

    print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                    OCTUPOLE FIXED-POINT SEARCH RESULTS                       ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  HYPOTHESIS: T³/Z₂ topology creates enhanced correlation at 8 fixed points  ║
║                                                                              ║
║  ALIGNMENT TESTS:                                                            ║""")

    for align, res in results.items():
        sig = "**SIGNIFICANT**" if res['significant'] else "not significant"
        print(f"║    {align:15}: Z = {res['z_score']:+5.2f}σ  {sig:20}║")

    best_alignment = max(results.keys(), key=lambda x: abs(results[x]['z_score']))
    best_z = results[best_alignment]['z_score']

    print(f"""║                                                                              ║
║  BEST ALIGNMENT: {best_alignment:12} (Z = {best_z:+.2f}σ)                              ║
║                                                                              ║
║  INTERPRETATION:                                                             ║
║    • Z > 2: Tentative evidence for octupolar structure                       ║
║    • Z > 3: Strong evidence (would warrant publication)                      ║
║    • Z > 5: Discovery-level (topological fingerprint confirmed)              ║
║                                                                              ║
║  CURRENT STATUS: {'OCTUPOLE SIGNAL DETECTED' if any(r['significant'] for r in results.values()) else 'No significant octupolar excess':^52}║
║                                                                              ║
║  NOTE: With limited O3a data, this is a proof-of-concept.                    ║
║        Full O4 dataset needed for definitive test.                           ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

    # Save results
    output = {
        'analysis': 'octupole_fixed_point_search',
        'date': time.strftime('%Y-%m-%d %H:%M:%S'),
        'results': results,
        'best_alignment': best_alignment,
        'best_z_score': float(best_z),
        'config': CONFIG,
    }

    with open(os.path.join(OUTPUT_DIR, 'octupole_search_results.json'), 'w') as f:
        json.dump(output, f, indent=2)

    print_status("Saved: octupole_search_results.json")

    # Create sky map visualization
    create_octupole_sky_map(results, strain_data)

    return output


def create_octupole_sky_map(results, strain_data):
    """Create HEALPix sky map showing fixed point positions and correlations."""
    fig = plt.figure(figsize=(16, 10))

    # Create correlation sky map
    print_status("Generating full-sky correlation map...")

    # Compute correlation at all HEALPix pixels (downsampled for speed)
    nside_low = 16
    npix_low = hp.nside2npix(nside_low)
    sky_map = np.zeros(npix_low)

    theta_pix, phi_pix = hp.pix2ang(nside_low, np.arange(npix_low))

    for i in range(npix_low):
        corr = compute_directional_correlation(
            strain_data['H1'][:1000000], strain_data['L1'][:1000000],
            theta_pix[i], phi_pix[i], CONFIG
        )
        sky_map[i] = corr['correlation']

    # Plot sky map
    plt.subplot(2, 2, 1)
    hp.mollview(sky_map, title='Cross-Correlation Sky Map',
                unit='Correlation', hold=True, cmap='RdBu_r')

    # Mark fixed points for best alignment
    best_align = max(results.keys(), key=lambda x: abs(results[x]['z_score']))
    fp_positions = results[best_align]['fixed_points']['positions']

    for i, (l, b) in enumerate(fp_positions):
        theta = np.radians(90 - b)
        phi = np.radians(l)
        hp.projscatter(theta, phi, marker='*', s=200, c='yellow', edgecolors='black')

    # Plot 2: Fixed point correlations
    plt.subplot(2, 2, 2)
    for align in results:
        fp_corr = results[align]['fixed_points']['correlations']
        plt.plot(range(1, 9), np.abs(fp_corr), 'o-', label=align, markersize=8)

    plt.axhline(y=results[best_align]['random']['mean'], color='gray',
                linestyle='--', label='Random mean')
    plt.xlabel('Fixed Point Index')
    plt.ylabel('|Correlation|')
    plt.title('Correlation at 8 Fixed Points')
    plt.legend()
    plt.grid(True, alpha=0.3)

    # Plot 3: Z-score comparison
    plt.subplot(2, 2, 3)
    alignments = list(results.keys())
    z_scores = [results[a]['z_score'] for a in alignments]
    colors = ['green' if z > 2 else 'orange' if z > 1 else 'red' for z in z_scores]

    plt.bar(alignments, z_scores, color=colors, alpha=0.7)
    plt.axhline(y=2, color='green', linestyle='--', label='2σ threshold')
    plt.axhline(y=3, color='blue', linestyle='--', label='3σ threshold')
    plt.xlabel('Alignment Hypothesis')
    plt.ylabel('Z-score (FP vs Random)')
    plt.title('Statistical Significance by Alignment')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')

    # Plot 4: Fixed point sky positions
    plt.subplot(2, 2, 4)
    for align in ['galactic', 'cmb_dipole']:
        fp_pos = results[align]['fixed_points']['positions']
        l_vals = [p[0] for p in fp_pos]
        b_vals = [p[1] for p in fp_pos]
        plt.scatter(l_vals, b_vals, s=100, alpha=0.7, label=align)

    plt.xlabel('Galactic Longitude l [°]')
    plt.ylabel('Galactic Latitude b [°]')
    plt.title('Fixed Point Positions (Different Alignments)')
    plt.xlim(0, 360)
    plt.ylim(-90, 90)
    plt.legend()
    plt.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig(os.path.join(OUTPUT_DIR, 'octupole_sky_map.png'), dpi=150)
    print_status("Saved: octupole_sky_map.png")
    plt.close()


if __name__ == '__main__':
    run_octupole_search()
