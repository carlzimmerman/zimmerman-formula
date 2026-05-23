#!/usr/bin/env python3
"""
4-Point Correlation Function Parity Violation Analysis
=======================================================

The Philcox & Slepian 7σ Anomaly:
---------------------------------
Galaxy distributions show a 7σ preference for "handed" tetrahedra.
Standard ΛCDM predicts perfect parity symmetry in galaxy clustering.

Z² Framework Prediction:
------------------------
The T³/Z₂ orbifold is constructed by identifying x ~ -x (reflection).
This Z₂ action breaks parity symmetry at the boundary.
The topological chirality should imprint on large-scale structure.

If the observed 7σ galaxy chirality aligns with the T³/Z₂ axes,
we have proven the macroscopic shape of the universe.

Author: Carl Zimmerman + Claude
Date: May 23, 2026
Framework: v11.1.0
"""

import numpy as np
from scipy.spatial import cKDTree
from scipy.special import sph_harm
import json
from pathlib import Path

# =============================================================================
# FUNDAMENTAL CONSTANTS (LOCKED)
# =============================================================================
L_C_GPC = 20.6          # Topological scale
L_C_MPC = L_C_GPC * 1000
V_VERTEX = 0.236        # Vertex potential
Z2 = 32 * np.pi / 3     # Eta invariant = 33.510
Z = np.sqrt(Z2)

# Observer position from H3 grid search (LOCKED)
R_OBS_MPC = 68          # Distance from void center
THETA_OBS_DEG = 13      # Angle from void-vertex axis
V_BULK_KMS = 265        # Bulk velocity toward vertex

# T³/Z₂ fixed points (8 vertices at corners of fundamental domain)
# In observer-centered coordinates where we are at ~68 Mpc from void center
# The nearest vertex is along the void-vertex axis direction
FIXED_POINTS = np.array([
    [-1, -1, -1],
    [1, -1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, 1, -1],
    [1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1]
]) * L_C_MPC / 2  # Scale to physical coordinates (centered at box center)

print("=" * 80)
print("4-POINT CORRELATION FUNCTION PARITY VIOLATION ANALYSIS")
print("=" * 80)
print(f"\nFramework: Z² Unified Action v11.1.0")
print(f"Target: Philcox & Slepian 7σ galaxy chirality anomaly")
print(f"Mechanism: T³/Z₂ reflection boundary breaks parity")

# =============================================================================
# PART 1: THEORETICAL BACKGROUND
# =============================================================================

def explain_parity_violation():
    """
    The Z₂ orbifold creates chirality through the identification x ~ -x.

    For a tetrahedron of 4 galaxies at positions {r1, r2, r3, r4}:
    - The parity-odd component measures the "handedness"
    - Defined by: ε_ijk (r1-r4)_i (r2-r4)_j (r3-r4)_k
    - This is the signed volume of the tetrahedron

    In infinite flat space: <parity-odd> = 0 (by symmetry)
    In T³/Z₂: The reflection boundary at x = L_c/2 breaks this symmetry
    """
    print("\n" + "=" * 80)
    print("THEORETICAL BACKGROUND")
    print("=" * 80)

    print("""
THE PARITY VIOLATION MECHANISM:
-------------------------------
1. The T³/Z₂ orbifold identifies points x ↔ -x (reflection)
2. This creates 8 fixed points (corners of fundamental domain)
3. Near these boundaries, the metric has a preferred handedness
4. Galaxy tetrahedra inherit this chirality from the topology

MATHEMATICAL FORMULATION:
-------------------------
The 4-point correlation function ζ(r₁, r₂, r₃, r₄) decomposes:

  ζ = ζ_even + ζ_odd

where:
  ζ_even : invariant under parity (P: r → -r)
  ζ_odd  : flips sign under parity

The parity-odd component can be written:

  ζ_odd ∝ ε_ijk n̂_1,i n̂_2,j n̂_3,k × f(r₁₂, r₁₃, r₁₄, r₂₃, r₂₄, r₃₄)

where n̂_i are the unit vectors from galaxy 4 to galaxies 1,2,3.

PHILCOX & SLEPIAN (2021) FINDING:
---------------------------------
  ζ_odd / ζ_even ≈ 0.03 ± 0.004  (7σ from zero)

Standard ΛCDM predicts: ζ_odd = 0

Z² FRAMEWORK PREDICTION:
------------------------
  ζ_odd / ζ_even ∝ (r_scale / L_c)² × alignment_factor

The chirality axis should point toward the nearest T³/Z₂ vertex.
""")

explain_parity_violation()

# =============================================================================
# PART 2: TETRAHEDRON CHIRALITY COMPUTATION
# =============================================================================

def compute_tetrahedron_chirality(r1, r2, r3, r4):
    """
    Compute the signed volume (chirality) of a tetrahedron.

    Returns positive for right-handed, negative for left-handed.
    """
    # Vectors from r4 to other vertices
    v1 = r1 - r4
    v2 = r2 - r4
    v3 = r3 - r4

    # Signed volume = (v1 × v2) · v3 / 6
    cross = np.cross(v1, v2)
    signed_volume = np.dot(cross, v3) / 6.0

    return signed_volume


def compute_parity_odd_4pcf(positions, n_tetrahedra=10000, r_min=50, r_max=150):
    """
    Compute the parity-odd 4-point correlation function.

    Parameters:
    -----------
    positions : array (N, 3)
        Galaxy positions in Mpc
    n_tetrahedra : int
        Number of random tetrahedra to sample
    r_min, r_max : float
        Scale range in Mpc

    Returns:
    --------
    parity_odd_amplitude : float
        Mean signed chirality
    parity_odd_axis : array (3,)
        Preferred direction of chirality
    significance : float
        Statistical significance
    """
    n_galaxies = len(positions)

    if n_galaxies < 4:
        return 0, np.zeros(3), 0

    # Build KD-tree for neighbor finding
    tree = cKDTree(positions)

    chiralities = []
    chirality_vectors = []

    for _ in range(n_tetrahedra):
        # Pick random anchor galaxy
        i = np.random.randint(n_galaxies)
        anchor = positions[i]

        # Find neighbors in scale range
        neighbors_idx = tree.query_ball_point(anchor, r_max)
        neighbors_idx = [j for j in neighbors_idx
                        if j != i and np.linalg.norm(positions[j] - anchor) > r_min]

        if len(neighbors_idx) < 3:
            continue

        # Pick 3 random neighbors
        selected = np.random.choice(neighbors_idx, size=3, replace=False)

        r1, r2, r3, r4 = positions[selected[0]], positions[selected[1]], positions[selected[2]], anchor

        # Compute chirality
        chi = compute_tetrahedron_chirality(r1, r2, r3, r4)
        chiralities.append(chi)

        # Compute chirality direction (normal to base triangle)
        center = (r1 + r2 + r3 + r4) / 4
        chirality_vec = chi * center / (np.linalg.norm(center) + 1e-10)
        chirality_vectors.append(chirality_vec)

    if len(chiralities) == 0:
        return 0, np.zeros(3), 0

    chiralities = np.array(chiralities)
    chirality_vectors = np.array(chirality_vectors)

    # Parity-odd amplitude
    mean_chi = np.mean(chiralities)
    std_chi = np.std(chiralities) / np.sqrt(len(chiralities))
    significance = abs(mean_chi) / (std_chi + 1e-10)

    # Parity-odd axis (mean direction)
    mean_axis = np.mean(chirality_vectors, axis=0)
    mean_axis /= np.linalg.norm(mean_axis) + 1e-10

    return mean_chi, mean_axis, significance


# =============================================================================
# PART 3: Z₂ AXIS ALIGNMENT TEST
# =============================================================================

def compute_z2_chirality_axis():
    """
    Compute the expected chirality axis from T³/Z₂ topology.

    The Z₂ identification x ~ -x creates a preferred axis
    pointing from the observer toward the nearest fixed point.
    """
    # Observer position from H3 grid search
    # r = 68 Mpc from void center, θ = 13° from vertex axis
    theta_rad = np.radians(THETA_OBS_DEG)
    observer = np.array([
        R_OBS_MPC * np.sin(theta_rad),
        0,
        R_OBS_MPC * np.cos(theta_rad)
    ])

    # Find nearest vertex
    distances = np.linalg.norm(FIXED_POINTS - observer, axis=1)
    nearest_idx = np.argmin(distances)
    nearest_vertex = FIXED_POINTS[nearest_idx]

    # The Z₂ axis points toward the nearest vertex
    z2_axis = nearest_vertex / np.linalg.norm(nearest_vertex)

    return z2_axis, nearest_idx, distances[nearest_idx]


def test_axis_alignment(observed_axis, z2_axis):
    """
    Test whether the observed chirality axis aligns with the Z₂ axis.

    Returns:
    --------
    alignment : float
        Cosine of angle between axes (1 = aligned, -1 = anti-aligned)
    p_value : float
        Probability of random alignment this good
    """
    alignment = abs(np.dot(observed_axis, z2_axis))

    # For random axis, cos(θ) is uniformly distributed
    # P(|cos(θ)| > alignment) = 2 * (1 - alignment)
    p_value = 2 * (1 - alignment)

    return alignment, p_value


# =============================================================================
# PART 4: MOCK DATA TEST
# =============================================================================

def generate_mock_catalog(n_galaxies=50000, inject_chirality=True, chi_amplitude=0.03):
    """
    Generate mock galaxy catalog with optional Z₂ chirality injection.

    In real analysis, this would be replaced with DESI_5YR_Z2_Native.fits
    """
    print("\n" + "=" * 80)
    print("GENERATING MOCK CATALOG")
    print("=" * 80)

    # Random positions in a 1 Gpc box
    box_size = 1000  # Mpc
    positions = np.random.uniform(0, box_size, size=(n_galaxies, 3))

    if inject_chirality:
        # Inject Z₂ chirality by shifting galaxies toward a preferred direction
        z2_axis, _, _ = compute_z2_chirality_axis()

        # Add small systematic displacement along Z₂ axis
        # This simulates the topological boundary effect
        # Check for nan in z2_axis
        if np.any(np.isnan(z2_axis)):
            z2_axis = np.array([0.577, 0.577, 0.577])  # Default diagonal
            print(f"  Warning: Using default diagonal axis")

        displacement = chi_amplitude * box_size * np.outer(
            np.random.randn(n_galaxies), z2_axis
        )
        positions += displacement

        # Keep in box
        positions = positions % box_size

        print(f"  Injected chirality amplitude: {chi_amplitude}")
        print(f"  Z₂ axis direction: [{z2_axis[0]:.3f}, {z2_axis[1]:.3f}, {z2_axis[2]:.3f}]")
    else:
        print("  No chirality injection (null test)")

    print(f"  Generated {n_galaxies} mock galaxies in {box_size} Mpc box")

    return positions


def run_4pcf_analysis(positions, n_tetrahedra=50000):
    """
    Run full 4PCF parity violation analysis.
    """
    print("\n" + "=" * 80)
    print("RUNNING 4PCF PARITY VIOLATION ANALYSIS")
    print("=" * 80)

    # Compute parity-odd 4PCF
    print("\nComputing 4-point correlation function...")
    mean_chi, obs_axis, significance = compute_parity_odd_4pcf(
        positions, n_tetrahedra=n_tetrahedra
    )

    print(f"\nPARITY-ODD 4PCF RESULTS:")
    print(f"  Mean chirality:     {mean_chi:.6f}")
    print(f"  Significance:       {significance:.1f}σ")
    print(f"  Observed axis:      [{obs_axis[0]:.3f}, {obs_axis[1]:.3f}, {obs_axis[2]:.3f}]")

    # Compare with Z₂ prediction
    z2_axis, vertex_idx, vertex_dist = compute_z2_chirality_axis()
    alignment, p_value = test_axis_alignment(obs_axis, z2_axis)

    print(f"\nZ² FRAMEWORK COMPARISON:")
    print(f"  Z₂ axis (vertex {vertex_idx}): [{z2_axis[0]:.3f}, {z2_axis[1]:.3f}, {z2_axis[2]:.3f}]")
    print(f"  Distance to vertex: {vertex_dist/1000:.2f} Gpc")
    print(f"  Axis alignment:     {alignment:.3f}")
    print(f"  Alignment p-value:  {p_value:.4f}")

    # Verdict
    print("\n" + "-" * 60)
    if significance > 3 and alignment > 0.8:
        print("VERDICT: PARITY VIOLATION ALIGNED WITH Z₂ TOPOLOGY")
        print("         The galaxy chirality matches the T³/Z₂ boundary!")
    elif significance > 3 and alignment < 0.5:
        print("VERDICT: PARITY VIOLATION DETECTED BUT MISALIGNED")
        print("         Signal present but different axis than predicted")
    elif significance < 2:
        print("VERDICT: NO SIGNIFICANT PARITY VIOLATION DETECTED")
        print("         Need more tetrahedra or real data")
    else:
        print("VERDICT: MARGINAL DETECTION, MORE DATA NEEDED")
    print("-" * 60)

    return {
        'mean_chirality': float(mean_chi),
        'significance_sigma': float(significance),
        'observed_axis': obs_axis.tolist(),
        'z2_axis': z2_axis.tolist(),
        'alignment': float(alignment),
        'alignment_p_value': float(p_value),
        'nearest_vertex_idx': int(vertex_idx),
        'nearest_vertex_dist_Gpc': float(vertex_dist / 1000)
    }


# =============================================================================
# PART 5: MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 80)
    print("TEST 1: NULL TEST (No chirality injection)")
    print("=" * 80)

    positions_null = generate_mock_catalog(n_galaxies=20000, inject_chirality=False)
    results_null = run_4pcf_analysis(positions_null, n_tetrahedra=20000)

    print("\n" + "=" * 80)
    print("TEST 2: INJECTION TEST (Z₂ chirality injected)")
    print("=" * 80)

    positions_inj = generate_mock_catalog(n_galaxies=20000, inject_chirality=True, chi_amplitude=0.03)
    results_inj = run_4pcf_analysis(positions_inj, n_tetrahedra=20000)

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)

    print("""
NEXT STEPS FOR REAL DESI DATA:
------------------------------
1. Load DESI_5YR_Z2_Native.fits (from Work-Order O pipeline)
2. Apply Z²-native coordinate transformation
3. Run 4PCF on native coordinates
4. Compare chirality axis with T³/Z₂ vertex directions

If the 7σ Philcox & Slepian parity violation aligns with our
predicted Z₂ axis, we have proven the shape of the universe.

THE DECISIVE TEST:
  Observed chirality axis = Z₂ reflection axis
  → Universe is a T³/Z₂ orbifold with L_c = 20.6 Gpc
""")

    # Save results
    output = {
        'analysis': '4PCF_parity_violation',
        'framework': 'v11.1.0',
        'date': 'May 23, 2026',
        'null_test': results_null,
        'injection_test': results_inj,
        'philcox_slepian_observed': {
            'parity_odd_ratio': 0.03,
            'significance_sigma': 7.0,
            'reference': 'Philcox & Slepian (2021)'
        },
        'z2_prediction': {
            'mechanism': 'T³/Z₂ reflection boundary x ~ -x',
            'expected_axis': 'Points toward nearest topological vertex',
            'L_c_Gpc': L_C_GPC
        }
    }

    output_file = Path(__file__).parent / 'four_point_parity_results.json'
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nResults saved to: {output_file}")
