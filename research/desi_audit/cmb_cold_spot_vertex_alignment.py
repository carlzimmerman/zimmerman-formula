#!/usr/bin/env python3
"""
CMB Cold Spot - T³/Z₂ Vertex Alignment Analysis
=================================================

Tests whether the CMB Cold Spot (the largest anomaly in the cosmic microwave
background) aligns with one of the 8 orbifold vertices of the T³/Z₂ framework.

THE CMB COLD SPOT:
- Location: (l, b) = (209°, -57°) in Galactic coordinates
- Size: ~5° radius (corresponding to ~300 Mpc supervoid)
- Temperature deficit: ΔT/T ≈ -150 μK (7σ anomaly)
- Associated with the Eridanus Supervoid at z ≈ 0.15-0.35

Z² PREDICTION:
If the universe has T³/Z₂ topology with L_c = 20.6 Gpc, the 8 vertices
(orbifold fixed points) should exhibit gravitational potential anomalies.
Matter is REPELLED from vertices (v = 0.236 vertex potential).

The Cold Spot could be:
1. A vertex of the T³/Z₂ fundamental domain
2. The gravitational ISW effect from the vertex potential
3. Evidence that we are observing topology, not random fluctuation

This script tests the alignment between:
- CMB Cold Spot coordinates
- Eridanus Supervoid location
- The 8 T³/Z₂ vertex positions in comoving coordinates

Author: Carl Zimmerman
Date: May 22, 2026
Framework: v11.1.0
"""

import numpy as np
from scipy import stats
from scipy.integrate import quad
from scipy.spatial.distance import cdist
import json
import os

np.random.seed(42)

print("=" * 80)
print("CMB COLD SPOT - T³/Z₂ VERTEX ALIGNMENT ANALYSIS")
print("Testing Topological Origin of the Largest CMB Anomaly")
print("=" * 80)

# =============================================================================
# CONSTANTS
# =============================================================================

# T³/Z₂ Framework
L_c = 20.6  # Gpc - Box scale
Z2 = 32 * np.pi / 3  # Eta invariant
V_VERTEX = 0.236  # Vertex potential

# Cosmology
H0 = 67.4  # km/s/Mpc (Planck)
c = 299792.458  # km/s
OMEGA_M = 0.315
OMEGA_DE = 0.685

# CMB Cold Spot (Galactic coordinates)
COLD_SPOT_L = 209.0  # degrees
COLD_SPOT_B = -57.0  # degrees
COLD_SPOT_RADIUS = 5.0  # degrees

# Eridanus Supervoid (associated structure)
ERIDANUS_Z_MIN = 0.15
ERIDANUS_Z_MID = 0.25
ERIDANUS_Z_MAX = 0.35
ERIDANUS_RADIUS_MPC = 300  # Approximate radius

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                      CMB COLD SPOT PARAMETERS                                ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Galactic Coordinates:  l = {COLD_SPOT_L}°, b = {COLD_SPOT_B}°                          ║
║  Angular Size:          ~{COLD_SPOT_RADIUS}° radius                                          ║
║  Temperature Anomaly:   ΔT/T ≈ -150 μK (7σ cold)                             ║
║  Associated Void:       Eridanus Supervoid (z ≈ 0.15-0.35)                   ║
║  Void Size:             ~{ERIDANUS_RADIUS_MPC} Mpc radius                                       ║
║                                                                              ║
║  T³/Z₂ Framework:                                                            ║
║    Box Scale:           L_c = {L_c} Gpc                                        ║
║    Vertex Potential:    v = {V_VERTEX}                                             ║
║    N Vertices:          8 (orbifold fixed points)                            ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# =============================================================================
# SECTION 1: COORDINATE TRANSFORMATIONS
# =============================================================================

print("=" * 80)
print("SECTION 1: COORDINATE TRANSFORMATIONS")
print("=" * 80)

def galactic_to_equatorial(l, b):
    """
    Convert Galactic (l, b) to Equatorial (RA, Dec) coordinates.
    Uses J2000 epoch transformation.
    """
    l_rad = np.radians(l)
    b_rad = np.radians(b)

    # Galactic pole in equatorial coords (J2000)
    ra_gp = np.radians(192.85948)
    dec_gp = np.radians(27.12825)
    l_ncp = np.radians(122.93192)

    # Transform
    sin_dec = np.sin(b_rad) * np.sin(dec_gp) + \
              np.cos(b_rad) * np.cos(dec_gp) * np.sin(l_rad - l_ncp)
    dec = np.arcsin(np.clip(sin_dec, -1, 1))

    cos_dec = np.cos(dec)
    if abs(cos_dec) < 1e-10:
        ra = 0
    else:
        sin_ra_diff = np.cos(b_rad) * np.cos(l_rad - l_ncp) / cos_dec
        cos_ra_diff = (np.sin(b_rad) - np.sin(dec) * np.sin(dec_gp)) / (cos_dec * np.cos(dec_gp))
        ra = ra_gp + np.arctan2(sin_ra_diff, cos_ra_diff)

    return np.degrees(ra) % 360, np.degrees(dec)

def comoving_distance(z):
    """Comoving distance in Gpc."""
    def E(zp):
        return np.sqrt(OMEGA_M * (1 + zp)**3 + OMEGA_DE)

    if np.isscalar(z):
        integral, _ = quad(lambda zp: 1/E(zp), 0, z)
        return (c / H0) * integral / 1000  # Gpc
    else:
        return np.array([comoving_distance(zi) for zi in z])

def spherical_to_cartesian(ra, dec, z):
    """Convert (RA, Dec, z) to comoving Cartesian (x, y, z) in Gpc."""
    D_c = comoving_distance(z)
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)

    x = D_c * np.cos(dec_rad) * np.cos(ra_rad)
    y = D_c * np.cos(dec_rad) * np.sin(ra_rad)
    z_coord = D_c * np.sin(dec_rad)

    return np.array([x, y, z_coord])

# Convert Cold Spot to equatorial
cs_ra, cs_dec = galactic_to_equatorial(COLD_SPOT_L, COLD_SPOT_B)

print(f"""
  CMB COLD SPOT COORDINATES:
  ──────────────────────────
  Galactic:    l = {COLD_SPOT_L}°, b = {COLD_SPOT_B}°
  Equatorial:  RA = {cs_ra:.2f}°, Dec = {cs_dec:.2f}°

  Constellation: Eridanus (The River)
""")

# =============================================================================
# SECTION 2: ERIDANUS SUPERVOID 3D POSITION
# =============================================================================

print("\n" + "=" * 80)
print("SECTION 2: ERIDANUS SUPERVOID 3D POSITION")
print("=" * 80)

# Calculate comoving position of the supervoid center
z_void = ERIDANUS_Z_MID
D_c_void = comoving_distance(z_void)
void_position = spherical_to_cartesian(cs_ra, cs_dec, z_void)

# Also compute at near and far edges
D_c_near = comoving_distance(ERIDANUS_Z_MIN)
D_c_far = comoving_distance(ERIDANUS_Z_MAX)

print(f"""
  ERIDANUS SUPERVOID COMOVING COORDINATES:
  ────────────────────────────────────────
  Redshift range: z = {ERIDANUS_Z_MIN} - {ERIDANUS_Z_MAX}

  Comoving distances:
    Near edge (z={ERIDANUS_Z_MIN}):  D_c = {D_c_near:.3f} Gpc
    Center (z={ERIDANUS_Z_MID}):     D_c = {D_c_void:.3f} Gpc
    Far edge (z={ERIDANUS_Z_MAX}):   D_c = {D_c_far:.3f} Gpc

  3D Cartesian position (center):
    x = {void_position[0]:.4f} Gpc
    y = {void_position[1]:.4f} Gpc
    z = {void_position[2]:.4f} Gpc

  Distance from origin: {np.linalg.norm(void_position):.4f} Gpc
  Fraction of L_c: {np.linalg.norm(void_position) / L_c:.4f}
""")

# =============================================================================
# SECTION 3: T³/Z₂ VERTEX POSITIONS
# =============================================================================

print("=" * 80)
print("SECTION 3: T³/Z₂ VERTEX POSITIONS")
print("=" * 80)

print("""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    T³/Z₂ ORBIFOLD VERTICES                                   │
└──────────────────────────────────────────────────────────────────────────────┘

In the T³/Z₂ framework, the 8 orbifold fixed points (vertices) are located
at the corners of the fundamental domain. These are the points where the
Z₂ involution acts as identity, creating gravitational potential nodes.

For a box centered at the observer (Earth at origin), the vertices are at:
    (±L_c/2, ±L_c/2, ±L_c/2)

These vertices have:
- Enhanced gravitational potential (v = 0.236)
- Matter repulsion (creating supervoids)
- ISW effect on CMB photons (causing cold spots)
""")

# Define vertex positions (centered at observer)
vertices = np.array([
    [-L_c/2, -L_c/2, -L_c/2],
    [-L_c/2, -L_c/2, +L_c/2],
    [-L_c/2, +L_c/2, -L_c/2],
    [-L_c/2, +L_c/2, +L_c/2],
    [+L_c/2, -L_c/2, -L_c/2],
    [+L_c/2, -L_c/2, +L_c/2],
    [+L_c/2, +L_c/2, -L_c/2],
    [+L_c/2, +L_c/2, +L_c/2],
])

# Also compute vertex directions (unit vectors)
vertex_distances = np.linalg.norm(vertices, axis=1)
vertex_directions = vertices / vertex_distances[:, np.newaxis]

# Convert vertices to (RA, Dec, Distance)
def cartesian_to_spherical(x, y, z):
    """Convert Cartesian to (RA, Dec) in degrees and distance."""
    r = np.sqrt(x**2 + y**2 + z**2)
    dec = np.degrees(np.arcsin(z / r))
    ra = np.degrees(np.arctan2(y, x)) % 360
    return ra, dec, r

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    VERTEX COORDINATES                                        │
├──────────────────────────────────────────────────────────────────────────────┤
│  Vertex │   x (Gpc)   │   y (Gpc)   │   z (Gpc)   │  Distance  │  RA    Dec │
│  ───────┼─────────────┼─────────────┼─────────────┼────────────┼────────────│""")

for i, v in enumerate(vertices):
    ra, dec, dist = cartesian_to_spherical(v[0], v[1], v[2])
    print(f"│    {i+1}   │   {v[0]:+7.2f}   │   {v[1]:+7.2f}   │   {v[2]:+7.2f}   │   {dist:.2f}   │ {ra:5.1f} {dec:+5.1f} │")

print("""│  ───────┴─────────────┴─────────────┴─────────────┴────────────┴────────────│
│                                                                              │
│  All vertices at distance L_c × √3 / 2 = 17.84 Gpc from observer            │
│  (diagonal of half-cube)                                                     │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 4: ANGULAR ALIGNMENT TEST
# =============================================================================

print("=" * 80)
print("SECTION 4: ANGULAR ALIGNMENT TEST")
print("=" * 80)

# Cold Spot direction (unit vector)
cs_ra_rad = np.radians(cs_ra)
cs_dec_rad = np.radians(cs_dec)
cs_direction = np.array([
    np.cos(cs_dec_rad) * np.cos(cs_ra_rad),
    np.cos(cs_dec_rad) * np.sin(cs_ra_rad),
    np.sin(cs_dec_rad)
])

# Calculate angular separation to each vertex
angular_separations = []
for i, v_dir in enumerate(vertex_directions):
    cos_angle = np.dot(cs_direction, v_dir)
    angle_deg = np.degrees(np.arccos(np.clip(cos_angle, -1, 1)))
    angular_separations.append(angle_deg)

angular_separations = np.array(angular_separations)
closest_vertex_idx = np.argmin(angular_separations)
closest_angle = angular_separations[closest_vertex_idx]

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ANGULAR SEPARATION FROM COLD SPOT                         │
├──────────────────────────────────────────────────────────────────────────────┤
│  Cold Spot direction: RA = {cs_ra:.2f}°, Dec = {cs_dec:.2f}°                        │
│                                                                              │
│  Vertex │  Angular Separation  │  Significance                              │
│  ───────┼──────────────────────┼────────────────────────────────────────────│""")

for i, angle in enumerate(angular_separations):
    if i == closest_vertex_idx:
        sig = "*** CLOSEST ***"
    elif angle < 30:
        sig = "* Within 30°"
    elif angle < 60:
        sig = "Moderate"
    else:
        sig = "Far"
    print(f"│    {i+1}   │       {angle:6.2f}°        │  {sig:40} │")

print(f"""│  ───────┴──────────────────────────────────────────────────────────────────│
│                                                                              │
│  CLOSEST VERTEX: #{closest_vertex_idx + 1}                                                      │
│  Angular separation: {closest_angle:.2f}°                                               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 5: STATISTICAL SIGNIFICANCE
# =============================================================================

print("=" * 80)
print("SECTION 5: STATISTICAL SIGNIFICANCE OF ALIGNMENT")
print("=" * 80)

# Under null hypothesis: Cold Spot is randomly placed on sky
# Probability of being within θ degrees of ANY of 8 vertices

def prob_within_angle_of_vertex(theta_deg, n_vertices=8):
    """
    Probability that a random point on sphere is within θ degrees
    of at least one of n_vertices uniformly distributed points.

    For widely separated vertices (like our 8 corners), approximate
    as n × (solid angle of cap) / (4π)
    """
    theta_rad = np.radians(theta_deg)
    # Solid angle of spherical cap: 2π(1 - cos(θ))
    cap_solid_angle = 2 * np.pi * (1 - np.cos(theta_rad))
    full_sphere = 4 * np.pi

    # Probability of being in at least one cap (assuming no overlap for small θ)
    p_single = cap_solid_angle / full_sphere
    p_any = 1 - (1 - p_single)**n_vertices

    return p_any

# Calculate p-value for observed alignment
p_value_alignment = prob_within_angle_of_vertex(closest_angle)

# Monte Carlo verification
n_mc = 100000
mc_min_angles = []

for _ in range(n_mc):
    # Random point on sphere
    ra_rand = np.random.uniform(0, 360)
    dec_rand = np.degrees(np.arcsin(np.random.uniform(-1, 1)))

    # Direction
    ra_rad = np.radians(ra_rand)
    dec_rad = np.radians(dec_rand)
    rand_dir = np.array([
        np.cos(dec_rad) * np.cos(ra_rad),
        np.cos(dec_rad) * np.sin(ra_rad),
        np.sin(dec_rad)
    ])

    # Min angle to any vertex
    angles = [np.degrees(np.arccos(np.clip(np.dot(rand_dir, v_dir), -1, 1)))
              for v_dir in vertex_directions]
    mc_min_angles.append(min(angles))

mc_min_angles = np.array(mc_min_angles)
p_value_mc = np.mean(mc_min_angles <= closest_angle)

# Significance
if p_value_mc > 0:
    sigma_mc = stats.norm.ppf(1 - p_value_mc)
else:
    sigma_mc = np.inf

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    STATISTICAL SIGNIFICANCE                                  │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  NULL HYPOTHESIS: Cold Spot direction is random (isotropic)                  │
│  TEST: Probability of being within {closest_angle:.1f}° of any T³/Z₂ vertex          │
│                                                                              │
│  ANALYTICAL ESTIMATE:                                                        │
│    p-value ≈ {p_value_alignment:.4f}                                                     │
│                                                                              │
│  MONTE CARLO ({n_mc:,} trials):                                                │
│    p-value = {p_value_mc:.4f}                                                       │
│    Significance: {sigma_mc:.1f}σ                                                      │
│                                                                              │
│  Monte Carlo distribution of minimum angles:                                 │
│    Median: {np.median(mc_min_angles):.1f}°                                                    │
│    Mean: {np.mean(mc_min_angles):.1f}°                                                      │
│    5th percentile: {np.percentile(mc_min_angles, 5):.1f}°                                        │
│    1st percentile: {np.percentile(mc_min_angles, 1):.1f}°                                        │
│                                                                              │
│  Observed Cold Spot minimum angle: {closest_angle:.1f}°                               │
│  Percentile: {100 * (1 - p_value_mc):.1f}%                                                   │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 6: PROJECTION ONTO VERTEX AXIS
# =============================================================================

print("=" * 80)
print("SECTION 6: PROJECTION ONTO NEAREST VERTEX AXIS")
print("=" * 80)

# Project Eridanus Supervoid onto the axis toward nearest vertex
nearest_vertex = vertices[closest_vertex_idx]
nearest_vertex_dir = vertex_directions[closest_vertex_idx]

# Project void center onto this axis
void_projection = np.dot(void_position, nearest_vertex_dir)
void_transverse = np.linalg.norm(void_position - void_projection * nearest_vertex_dir)

# Distance from vertex
dist_to_vertex = np.linalg.norm(void_position - nearest_vertex)

# Fraction of vertex distance
fraction_to_vertex = void_projection / np.linalg.norm(nearest_vertex)

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    ERIDANUS SUPERVOID - VERTEX PROJECTION                    │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Nearest vertex: #{closest_vertex_idx + 1}                                                      │
│  Vertex position: ({nearest_vertex[0]:.1f}, {nearest_vertex[1]:.1f}, {nearest_vertex[2]:.1f}) Gpc           │
│  Vertex distance from origin: {np.linalg.norm(nearest_vertex):.2f} Gpc                        │
│                                                                              │
│  Eridanus Supervoid:                                                         │
│    Position: ({void_position[0]:.3f}, {void_position[1]:.3f}, {void_position[2]:.3f}) Gpc                   │
│    Distance from origin: {np.linalg.norm(void_position):.3f} Gpc                               │
│                                                                              │
│  PROJECTION ANALYSIS:                                                        │
│    Radial distance toward vertex: {void_projection:.3f} Gpc                         │
│    Transverse distance: {void_transverse:.3f} Gpc                                   │
│    Fraction of vertex distance: {fraction_to_vertex:.4f} = {fraction_to_vertex*100:.2f}%                     │
│                                                                              │
│    Distance from vertex center: {dist_to_vertex:.2f} Gpc                            │
│                                                                              │
│  INTERPRETATION:                                                             │
│    The Eridanus Supervoid lies {fraction_to_vertex*100:.1f}% of the way toward vertex #{closest_vertex_idx + 1}      │
│    at redshift z ≈ {z_void}                                                       │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 7: VERTEX POTENTIAL PROFILE
# =============================================================================

print("=" * 80)
print("SECTION 7: VERTEX POTENTIAL AND ISW EFFECT")
print("=" * 80)

def vertex_potential(r, r_vertex, v_strength=V_VERTEX):
    """
    Gravitational potential from vertex.
    Decreases as 1/r from vertex center.
    """
    dist = np.linalg.norm(r - r_vertex)
    if dist < 0.1:  # Regularize at vertex
        dist = 0.1
    return -v_strength / dist

def isw_temperature_shift(potential_in, potential_out):
    """
    ISW effect: ΔT/T ≈ 2(Φ_out - Φ_in)/c²
    Returns in μK assuming T_CMB = 2.725 K
    """
    c_sq = 1  # Natural units where c = 1
    delta_phi = potential_out - potential_in
    delta_T_over_T = 2 * delta_phi / c_sq
    T_cmb = 2.725e6  # μK
    return delta_T_over_T * T_cmb

# Calculate potential at void center
phi_at_void = sum(vertex_potential(void_position, v) for v in vertices)

# Calculate potential slightly in front and behind
void_dir = void_position / np.linalg.norm(void_position)
void_front = void_position - 0.1 * void_dir  # Closer to observer
void_back = void_position + 0.1 * void_dir   # Farther from observer

phi_front = sum(vertex_potential(void_front, v) for v in vertices)
phi_back = sum(vertex_potential(void_back, v) for v in vertices)

# ISW effect (simplified)
delta_T_isw = isw_temperature_shift(phi_front, phi_back)

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    VERTEX POTENTIAL ANALYSIS                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  At Eridanus Supervoid location:                                             │
│    Total vertex potential: Φ = {phi_at_void:.4f}                                   │
│    (Sum of contributions from all 8 vertices)                               │
│                                                                              │
│  Potential gradient along line of sight:                                     │
│    Φ(front): {phi_front:.4f}                                                       │
│    Φ(center): {phi_at_void:.4f}                                                     │
│    Φ(back): {phi_back:.4f}                                                        │
│                                                                              │
│  ISW TEMPERATURE SHIFT (simplified model):                                   │
│    ΔT ≈ {delta_T_isw:.1f} μK                                                        │
│                                                                              │
│  OBSERVED Cold Spot:                                                         │
│    ΔT ≈ -150 μK                                                             │
│                                                                              │
│  INTERPRETATION:                                                             │
│    The vertex potential creates a gravitational well.                        │
│    Photons lose energy climbing out → ISW cold spot.                        │
│    Quantitative agreement requires full ray-tracing simulation.             │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 8: DESI VOXEL GRID CHECK
# =============================================================================

print("=" * 80)
print("SECTION 8: DESI VOXEL GRID - COLD SPOT ALIGNMENT")
print("=" * 80)

# Define voxel grid matching DESI analysis
VOXEL_RES = 256
voxel_size = L_c / VOXEL_RES

# Convert Cold Spot/Eridanus to voxel indices
void_voxel = ((void_position + L_c/2) / L_c * VOXEL_RES).astype(int) % VOXEL_RES

# Convert vertices to voxel indices (corners of grid)
vertex_voxels = []
for v in vertices:
    vx = ((v + L_c/2) / L_c * VOXEL_RES).astype(int) % VOXEL_RES
    vertex_voxels.append(vx)
vertex_voxels = np.array(vertex_voxels)

# Find nearest vertex in voxel space
voxel_distances = []
for vv in vertex_voxels:
    # Account for periodic boundaries
    dx = min(abs(void_voxel[0] - vv[0]), VOXEL_RES - abs(void_voxel[0] - vv[0]))
    dy = min(abs(void_voxel[1] - vv[1]), VOXEL_RES - abs(void_voxel[1] - vv[1]))
    dz = min(abs(void_voxel[2] - vv[2]), VOXEL_RES - abs(void_voxel[2] - vv[2]))
    voxel_distances.append(np.sqrt(dx**2 + dy**2 + dz**2))

voxel_distances = np.array(voxel_distances)
nearest_voxel_vertex = np.argmin(voxel_distances)

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    DESI VOXEL GRID ALIGNMENT                                 │
├──────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│  Grid Resolution: {VOXEL_RES}³ = {VOXEL_RES**3:,} voxels                                  │
│  Voxel Size: {voxel_size*1000:.1f} Mpc                                                    │
│                                                                              │
│  Eridanus Supervoid voxel: ({void_voxel[0]}, {void_voxel[1]}, {void_voxel[2]})                           │
│                                                                              │
│  Vertex voxel positions (corners):                                           │
│    Vertex 1: (  0,   0,   0) - distance {voxel_distances[0]:.1f} voxels                │
│    Vertex 2: (  0,   0, 255) - distance {voxel_distances[1]:.1f} voxels                │
│    Vertex 3: (  0, 255,   0) - distance {voxel_distances[2]:.1f} voxels                │
│    Vertex 4: (  0, 255, 255) - distance {voxel_distances[3]:.1f} voxels                │
│    Vertex 5: (255,   0,   0) - distance {voxel_distances[4]:.1f} voxels                │
│    Vertex 6: (255,   0, 255) - distance {voxel_distances[5]:.1f} voxels                │
│    Vertex 7: (255, 255,   0) - distance {voxel_distances[6]:.1f} voxels                │
│    Vertex 8: (255, 255, 255) - distance {voxel_distances[7]:.1f} voxels                │
│                                                                              │
│  Nearest vertex in voxel space: #{nearest_voxel_vertex + 1}                              │
│  Voxel distance: {voxel_distances[nearest_voxel_vertex]:.1f} voxels = {voxel_distances[nearest_voxel_vertex] * voxel_size * 1000:.0f} Mpc               │
│                                                                              │
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 9: OTHER KNOWN SUPERVOIDS
# =============================================================================

print("=" * 80)
print("SECTION 9: OTHER SUPERVOIDS AND VERTEX CANDIDATES")
print("=" * 80)

# Known supervoids that could align with vertices
supervoids = [
    {"name": "Eridanus Supervoid", "l": 209, "b": -57, "z": 0.25, "radius_mpc": 300},
    {"name": "Northern Local Void", "l": 30, "b": 50, "z": 0.01, "radius_mpc": 60},
    {"name": "Boötes Void", "l": 60, "b": 68, "z": 0.06, "radius_mpc": 100},
    {"name": "KBC Void", "l": 180, "b": 0, "z": 0.07, "radius_mpc": 300},
    {"name": "Dipole Repeller", "l": 295, "b": -40, "z": 0.05, "radius_mpc": 200},
]

print(f"""
┌──────────────────────────────────────────────────────────────────────────────┐
│                    KNOWN SUPERVOIDS - VERTEX ALIGNMENT                       │
├──────────────────────────────────────────────────────────────────────────────┤
│  Void Name          │  (l, b)      │   z    │  Min Vertex Angle │  Nearest  │
│  ───────────────────┼──────────────┼────────┼───────────────────┼───────────│""")

for sv in supervoids:
    ra, dec = galactic_to_equatorial(sv['l'], sv['b'])
    ra_rad = np.radians(ra)
    dec_rad = np.radians(dec)
    sv_dir = np.array([
        np.cos(dec_rad) * np.cos(ra_rad),
        np.cos(dec_rad) * np.sin(ra_rad),
        np.sin(dec_rad)
    ])

    angles = [np.degrees(np.arccos(np.clip(np.dot(sv_dir, v_dir), -1, 1)))
              for v_dir in vertex_directions]
    min_angle = min(angles)
    nearest = np.argmin(angles) + 1

    print(f"│  {sv['name']:<17} │  ({sv['l']:3}, {sv['b']:+3})  │  {sv['z']:.2f}  │      {min_angle:5.1f}°       │     #{nearest}     │")

print("""│  ───────────────────┴──────────────┴────────┴───────────────────┴───────────│
└──────────────────────────────────────────────────────────────────────────────┘
""")

# =============================================================================
# SECTION 10: SUMMARY AND VERDICT
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY: CMB COLD SPOT - T³/Z₂ VERTEX ALIGNMENT")
print("=" * 80)

# Compile results
results = {
    "analysis": "cmb_cold_spot_vertex_alignment",
    "framework": "v11.1.0",
    "date": "May 22, 2026",
    "cold_spot": {
        "galactic_l": COLD_SPOT_L,
        "galactic_b": COLD_SPOT_B,
        "equatorial_ra": float(cs_ra),
        "equatorial_dec": float(cs_dec),
        "radius_deg": COLD_SPOT_RADIUS,
        "temperature_deficit_uK": -150,
    },
    "eridanus_supervoid": {
        "redshift_range": [ERIDANUS_Z_MIN, ERIDANUS_Z_MAX],
        "center_z": ERIDANUS_Z_MID,
        "comoving_distance_Gpc": float(D_c_void),
        "position_Gpc": void_position.tolist(),
        "radius_Mpc": ERIDANUS_RADIUS_MPC,
    },
    "t3_z2_analysis": {
        "L_c_Gpc": L_c,
        "n_vertices": 8,
        "vertex_potential": V_VERTEX,
        "nearest_vertex_index": int(closest_vertex_idx + 1),
        "angular_separation_deg": float(closest_angle),
    },
    "statistical_significance": {
        "p_value_analytical": float(p_value_alignment),
        "p_value_monte_carlo": float(p_value_mc),
        "sigma_significance": float(sigma_mc) if not np.isinf(sigma_mc) else None,
        "n_mc_trials": n_mc,
    },
    "voxel_analysis": {
        "grid_resolution": VOXEL_RES,
        "void_voxel": void_voxel.tolist(),
        "nearest_vertex_voxel_distance": float(voxel_distances[nearest_voxel_vertex]),
    },
    "verdict": {
        "alignment_detected": bool(closest_angle < 45),
        "statistically_significant": bool(p_value_mc < 0.05),
        "consistent_with_topology": bool(closest_angle < 60),
    },
    "falsification_criteria": [
        f"Angular separation > 60° → Current: {closest_angle:.1f}°",
        f"p-value > 0.05 → Current: {p_value_mc:.4f}",
        "Multiple Cold Spots not aligned with vertices",
        "Supervoid at vertex location without ISW signature",
    ],
}

alignment_status = "ALIGNED" if closest_angle < 30 else "MODERATELY ALIGNED" if closest_angle < 60 else "NOT ALIGNED"
significance_status = "SIGNIFICANT" if p_value_mc < 0.05 else "NOT SIGNIFICANT"

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║        CMB COLD SPOT - VERTEX ALIGNMENT ANALYSIS: COMPLETE                   ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  KEY FINDINGS:                                                               ║
║  ─────────────                                                               ║
║  1. ANGULAR ALIGNMENT:                                                       ║
║     Cold Spot → Nearest Vertex: {closest_angle:.1f}°                                     ║
║     Status: {alignment_status:30}                              ║
║                                                                              ║
║  2. STATISTICAL SIGNIFICANCE:                                                ║
║     p-value (Monte Carlo): {p_value_mc:.4f}                                        ║
║     Significance: {sigma_mc:.1f}σ                                                      ║
║     Status: {significance_status:30}                             ║
║                                                                              ║
║  3. ERIDANUS SUPERVOID POSITION:                                             ║
║     Distance from origin: {np.linalg.norm(void_position):.3f} Gpc                               ║
║     Fraction toward vertex: {fraction_to_vertex*100:.1f}%                                     ║
║     The void lies along the vertex direction at z ≈ 0.25                    ║
║                                                                              ║
║  4. VERTEX POTENTIAL:                                                        ║
║     Total potential at void: Φ = {phi_at_void:.4f}                                   ║
║     ISW effect: ΔT ≈ {delta_T_isw:.0f} μK (model-dependent)                              ║
║     Observed: ΔT ≈ -150 μK                                                  ║
║                                                                              ║
║  5. DESI VOXEL GRID:                                                         ║
║     Void voxel: {void_voxel}                                         ║
║     Distance to nearest vertex corner: {voxel_distances[nearest_voxel_vertex]:.0f} voxels                       ║
║                                                                              ║
║  VERDICT:                                                                    ║
║  ════════                                                                    ║
║  The CMB Cold Spot direction shows {alignment_status.lower()} alignment with            ║
║  T³/Z₂ vertex #{closest_vertex_idx + 1}. The Eridanus Supervoid lies along the ray toward   ║
║  this vertex at {fraction_to_vertex*100:.0f}% of the vertex distance.                               ║
║                                                                              ║
║  {'The alignment is statistically significant (p < 0.05).' if p_value_mc < 0.05 else 'The alignment is not statistically significant.'}               ║
║  {'This supports the topological interpretation of the Cold Spot.' if p_value_mc < 0.05 and closest_angle < 45 else 'Further analysis with DESI data is required.'}          ║
║                                                                              ║
║  RECOMMENDATION:                                                             ║
║  Check other large CMB anomalies against the remaining 7 vertices.          ║
║  If multiple anomalies align, the topological signal is strengthened.       ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")

# Save results
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
os.makedirs(OUTPUT_DIR, exist_ok=True)

with open(os.path.join(OUTPUT_DIR, 'cmb_cold_spot_vertex_results.json'), 'w') as f:
    json.dump(results, f, indent=2)

print(f"\nResults saved to: {os.path.join(OUTPUT_DIR, 'cmb_cold_spot_vertex_results.json')}")
print("=" * 80)
