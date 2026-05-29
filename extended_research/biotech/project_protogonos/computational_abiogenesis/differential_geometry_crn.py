#!/usr/bin/env python3
"""
================================================================================
DIFFERENTIAL GEOMETRY OF CHEMICAL REACTION NETWORKS
================================================================================

Based on recent advances in applying Riemannian geometry to reaction networks:
- Curvature-Induced Saturation (arXiv:2504.14700, April 2025)
- Topological Bounds on Dynamical Growth (arXiv:2603.02627, March 2026)

KEY INSIGHT:
  Concentration space can be treated as a RIEMANNIAN MANIFOLD where:
  - The metric encodes reaction kinetics
  - Geodesics represent thermodynamically favorable pathways
  - Curvature constrains which reaction sequences are accessible
  - Self-organization emerges from geometric structure

THIS FRAMEWORK ALLOWS:
  1. Predicting viable reaction sequences from curvature
  2. Identifying self-sustaining networks via positive curvature
  3. Explaining concentration robustness geometrically
  4. Understanding why some molecular configurations are favored

QUESTION: Does Z² appear in these geometric constraints?

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
import json
import os

# =============================================================================
# CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # ≈ 33.51
Z_CONSTANT = np.sqrt(Z_SQUARED)  # ≈ 5.79

# Protein geometrical factor (Liang & Dill, universal constant)
PROTEIN_FACTOR = 0.491  # V/(A⟨r⟩) for globular proteins

# =============================================================================
# RIEMANNIAN METRIC ON CONCENTRATION SPACE
# =============================================================================

@dataclass
class ConcentrationManifold:
    """
    A Riemannian manifold structure on the space of chemical concentrations.

    For n chemical species, the concentration space is R^n_+ (positive reals).
    We equip it with a metric that encodes thermodynamic structure.
    """
    n_species: int
    species_names: List[str] = field(default_factory=list)

    def __post_init__(self):
        if not self.species_names:
            self.species_names = [f"X_{i}" for i in range(self.n_species)]

    def fisher_information_metric(self, concentrations: np.ndarray) -> np.ndarray:
        """
        Fisher information metric on concentration space.

        For chemical systems, the natural metric is related to the
        Fisher-Rao metric from information geometry:
            g_ij = δ_ij / c_i

        This makes the manifold have constant negative curvature (hyperbolic)
        in each coordinate direction.
        """
        c = np.maximum(concentrations, 1e-10)  # Avoid division by zero
        return np.diag(1.0 / c)

    def chemical_metric(self, concentrations: np.ndarray,
                       stoichiometry: np.ndarray,
                       rate_constants: np.ndarray) -> np.ndarray:
        """
        A chemically-motivated metric that depends on reaction kinetics.

        The metric encodes how "hard" it is to change concentrations
        given the reaction network structure.

        This is analogous to the metric in thermodynamic geometry where
        distances correspond to entropy production.
        """
        n = len(concentrations)
        c = np.maximum(concentrations, 1e-10)

        # Base metric: Fisher information
        g = np.diag(1.0 / c)

        # Add coupling terms from reactions
        n_reactions = len(rate_constants)
        for r in range(n_reactions):
            nu = stoichiometry[:, r]  # Stoichiometric coefficients
            k = rate_constants[r]

            # Off-diagonal terms couple species involved in same reaction
            coupling = k * np.outer(nu, nu)
            g += 0.1 * coupling / np.sqrt(np.sum(c))

        # Ensure positive definite
        g = 0.5 * (g + g.T)
        min_eig = np.min(np.linalg.eigvalsh(g))
        if min_eig < 0:
            g += (-min_eig + 0.01) * np.eye(n)

        return g


def compute_christoffel_symbols(metric_at_point: np.ndarray,
                                metric_derivatives: np.ndarray) -> np.ndarray:
    """
    Compute Christoffel symbols Γ^k_ij from the metric.

    Γ^k_ij = (1/2) g^{kl} (∂_i g_{jl} + ∂_j g_{il} - ∂_l g_{ij})
    """
    n = metric_at_point.shape[0]
    g = metric_at_point
    dg = metric_derivatives  # Shape (n, n, n): dg[i, j, l] = ∂_l g_{ij}

    # Inverse metric
    g_inv = np.linalg.inv(g)

    # Christoffel symbols
    gamma = np.zeros((n, n, n))

    for k in range(n):
        for i in range(n):
            for j in range(n):
                sumval = 0.0
                for l in range(n):
                    sumval += g_inv[k, l] * (dg[j, l, i] + dg[i, l, j] - dg[i, j, l])
                gamma[k, i, j] = 0.5 * sumval

    return gamma


def compute_riemann_tensor(christoffel: np.ndarray,
                          christoffel_derivatives: np.ndarray) -> np.ndarray:
    """
    Compute Riemann curvature tensor R^l_{ijk}.

    R^l_{ijk} = ∂_j Γ^l_{ik} - ∂_k Γ^l_{ij} + Γ^l_{jm} Γ^m_{ik} - Γ^l_{km} Γ^m_{ij}
    """
    n = christoffel.shape[0]
    gamma = christoffel
    dgamma = christoffel_derivatives  # Shape (n, n, n, n): dgamma[l, i, k, j] = ∂_j Γ^l_{ik}

    R = np.zeros((n, n, n, n))

    for l in range(n):
        for i in range(n):
            for j in range(n):
                for k in range(n):
                    # Partial derivative terms
                    R[l, i, j, k] = dgamma[l, i, k, j] - dgamma[l, i, j, k]

                    # Connection terms
                    for m in range(n):
                        R[l, i, j, k] += gamma[l, j, m] * gamma[m, i, k]
                        R[l, i, j, k] -= gamma[l, k, m] * gamma[m, i, j]

    return R


def compute_ricci_curvature(riemann: np.ndarray) -> np.ndarray:
    """
    Compute Ricci curvature tensor R_{ij} = R^k_{ikj}.
    """
    n = riemann.shape[0]
    R = riemann

    ricci = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            for k in range(n):
                ricci[i, j] += R[k, i, k, j]

    return ricci


def compute_scalar_curvature(ricci: np.ndarray, metric: np.ndarray) -> float:
    """
    Compute scalar curvature R = g^{ij} R_{ij}.
    """
    g_inv = np.linalg.inv(metric)
    return float(np.trace(g_inv @ ricci))


# =============================================================================
# GEODESICS AND REACTION PATHWAYS
# =============================================================================

def geodesic_equation(c: np.ndarray, v: np.ndarray,
                     christoffel: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
    """
    Geodesic equation: d²c^k/dt² + Γ^k_ij (dc^i/dt)(dc^j/dt) = 0

    Returns (dc/dt, dv/dt) for integration.
    """
    n = len(c)
    gamma = christoffel

    # Acceleration
    a = np.zeros(n)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                a[k] -= gamma[k, i, j] * v[i] * v[j]

    return v, a


def integrate_geodesic(manifold: ConcentrationManifold,
                      c0: np.ndarray, v0: np.ndarray,
                      stoichiometry: np.ndarray,
                      rate_constants: np.ndarray,
                      dt: float = 0.01, n_steps: int = 100) -> np.ndarray:
    """
    Integrate a geodesic starting from c0 with initial velocity v0.

    Geodesics represent thermodynamically favorable reaction pathways.
    """
    trajectory = [c0.copy()]
    c = c0.copy()
    v = v0.copy()

    for _ in range(n_steps):
        # Compute metric and Christoffel symbols at current point
        g = manifold.chemical_metric(c, stoichiometry, rate_constants)

        # Numerical derivatives for Christoffel symbols
        epsilon = 0.001
        n = len(c)
        dg = np.zeros((n, n, n))

        for l in range(n):
            c_plus = c.copy()
            c_plus[l] += epsilon
            c_minus = c.copy()
            c_minus[l] -= epsilon

            g_plus = manifold.chemical_metric(c_plus, stoichiometry, rate_constants)
            g_minus = manifold.chemical_metric(c_minus, stoichiometry, rate_constants)

            dg[:, :, l] = (g_plus - g_minus) / (2 * epsilon)

        gamma = compute_christoffel_symbols(g, dg)

        # Integrate one step
        dc, dv = geodesic_equation(c, v, gamma)
        c = c + dt * dc
        v = v + dt * dv

        # Keep concentrations positive
        c = np.maximum(c, 1e-10)

        trajectory.append(c.copy())

    return np.array(trajectory)


# =============================================================================
# CURVATURE CONSTRAINTS ON AUTOCATALYSIS
# =============================================================================

def analyze_autocatalytic_curvature(n_species: int = 3,
                                   n_reactions: int = 5) -> Dict:
    """
    Analyze how curvature affects autocatalytic network stability.

    HYPOTHESIS: Positive Ricci curvature stabilizes autocatalytic cycles.
    """
    results = {
        'n_species': n_species,
        'n_reactions': n_reactions,
        'trials': []
    }

    for trial in range(10):
        # Random reaction network
        stoichiometry = np.random.randn(n_species, n_reactions)
        rate_constants = np.abs(np.random.randn(n_reactions)) + 0.1

        # Random concentrations
        c = np.abs(np.random.randn(n_species)) + 0.1

        # Create manifold
        manifold = ConcentrationManifold(n_species)

        # Compute metric
        g = manifold.chemical_metric(c, stoichiometry, rate_constants)

        # Compute curvature (simplified - using Fisher metric for now)
        # Full calculation would require numerical derivatives
        g_fisher = manifold.fisher_information_metric(c)

        # For Fisher metric, scalar curvature has known form
        # R = -n(n-1)/2 for product of hyperbolic spaces
        scalar_curvature_fisher = -n_species * (n_species - 1) / 2

        # Determinant of metric (related to volume element)
        det_g = np.linalg.det(g)

        results['trials'].append({
            'concentrations': c.tolist(),
            'det_metric': det_g,
            'scalar_curvature_fisher': scalar_curvature_fisher
        })

    return results


# =============================================================================
# Z² INVESTIGATION IN GEOMETRIC FRAMEWORK
# =============================================================================

def investigate_z2_in_geometry() -> Dict:
    """
    Systematically investigate whether Z² = 32π/3 appears in
    the geometric constraints of reaction networks.

    QUESTIONS:
    1. Does scalar curvature relate to Z²?
    2. Does the metric volume element involve Z²?
    3. Do geodesic lengths relate to Z²?
    4. Does the phase transition threshold involve Z²?
    """
    print("\n" + "=" * 70)
    print("Z² INVESTIGATION IN DIFFERENTIAL GEOMETRY FRAMEWORK")
    print("=" * 70)

    results = {
        'z_squared': Z_SQUARED,
        'z_constant': Z_CONSTANT,
        'findings': []
    }

    # 1. Check if curvature relates to Z²
    print("\n1. CURVATURE ANALYSIS")
    print("-" * 50)

    for n in range(2, 8):
        # Fisher metric curvature for n-dimensional space
        R_fisher = -n * (n - 1) / 2

        # Check ratio to Z²
        ratio_z2 = abs(R_fisher) / Z_SQUARED
        ratio_z = abs(R_fisher) / Z_CONSTANT

        print(f"   n={n}: R = {R_fisher:.2f}, |R|/Z² = {ratio_z2:.4f}, |R|/Z = {ratio_z:.4f}")

        if abs(ratio_z2 - round(ratio_z2)) < 0.1:
            results['findings'].append(f"n={n}: |R|/Z² ≈ {round(ratio_z2)} (close to integer)")

    # 2. Check sphere and geometric factors
    print("\n2. GEOMETRIC FACTORS")
    print("-" * 50)

    # Volume of n-sphere
    from scipy.special import gamma

    for n in range(2, 8):
        V_n = np.pi ** (n / 2) / gamma(n / 2 + 1)
        S_n_minus_1 = 2 * np.pi ** (n / 2) / gamma(n / 2)  # Surface of (n-1)-sphere

        ratio_v = Z_SQUARED / V_n
        ratio_s = Z_SQUARED / S_n_minus_1

        print(f"   n={n}: V_n = {V_n:.4f}, Z²/V_n = {ratio_v:.4f}")
        print(f"         S_{n-1} = {S_n_minus_1:.4f}, Z²/S_{n-1} = {ratio_s:.4f}")

        # Z² = 8 × V_3 exactly!
        if n == 3 and abs(ratio_v - 8) < 0.001:
            results['findings'].append(f"EXACT: Z² = 8 × V_3 (8 unit sphere volumes)")

    # 3. Check protein factor connection
    print("\n3. PROTEIN FACTOR CONNECTION")
    print("-" * 50)

    # Protein geometrical factor V/(A⟨r⟩) = 0.491
    # This is a UNIVERSAL constant across 10,000+ proteins

    z_over_12 = Z_CONSTANT / 12
    protein_ratio = z_over_12 / PROTEIN_FACTOR
    percent_diff = abs(z_over_12 - PROTEIN_FACTOR) / PROTEIN_FACTOR * 100

    print(f"   Protein factor: {PROTEIN_FACTOR}")
    print(f"   Z/12 = {z_over_12:.6f}")
    print(f"   Difference: {percent_diff:.2f}%")

    # What divisor gives exact match?
    exact_divisor = Z_CONSTANT / PROTEIN_FACTOR
    print(f"   Exact divisor for match: Z/{exact_divisor:.3f} = {PROTEIN_FACTOR}")

    # Is 12 special?
    print(f"\n   Is 12 geometrically special?")
    print(f"     12 = number of vertices in icosahedron")
    print(f"     12 = number of faces of dodecahedron")
    print(f"     12 = kissing number in 3D (spheres touching central sphere)")
    print(f"     12 = 2² × 3")

    # Check if icosahedral geometry relates
    golden_ratio = (1 + np.sqrt(5)) / 2
    icosa_edge = 2 / golden_ratio  # Edge length for unit circumradius

    print(f"\n   Icosahedral analysis:")
    print(f"     Golden ratio φ = {golden_ratio:.6f}")
    print(f"     Z/φ = {Z_CONSTANT/golden_ratio:.6f}")
    print(f"     Z/φ² = {Z_CONSTANT/golden_ratio**2:.6f}")

    # 4. Packing geometry connection
    print("\n4. PACKING GEOMETRY CONNECTION")
    print("-" * 50)

    ETA_FCC = np.pi / (3 * np.sqrt(2))  # 0.7405
    ratio_8pi_z2 = 8 * np.pi / Z_SQUARED

    print(f"   8π/Z² = {ratio_8pi_z2:.6f} (EXACTLY 3/4 = 0.75)")
    print(f"   FCC packing = {ETA_FCC:.6f}")
    print(f"   Difference: {abs(ratio_8pi_z2 - ETA_FCC)/ETA_FCC * 100:.2f}%")

    # Why 3/4?
    print(f"\n   Why 3/4?")
    print(f"     Z² = 32π/3 was DEFINED as Friedmann(8π/3) × Bekenstein(4)")
    print(f"     So 8π/Z² = 8π/(32π/3) = 8π × 3/(32π) = 24/32 = 3/4")
    print(f"     This is BY DEFINITION, not emergent")

    # 5. Does Z² appear in thermodynamic geometry?
    print("\n5. THERMODYNAMIC GEOMETRY")
    print("-" * 50)

    # In thermodynamic geometry, the Fisher-Rao metric has
    # a specific form related to entropy
    print("   The Ruppeiner metric in thermodynamic geometry:")
    print("   g_ij = -∂²S/∂X^i∂X^j")
    print("")
    print("   For an ideal gas with n particles:")
    print("   g = diag(1/T², 1/T²) in (E, V) coordinates")
    print("")
    print("   Scalar curvature R relates to interaction strength:")
    print("   R = 0 for ideal gas (no interactions)")
    print("   R ≠ 0 indicates interactions/correlations")
    print("")
    print(f"   Z² = 32π/3 does NOT appear naturally in Ruppeiner geometry")

    results['conclusion'] = """
    CONCLUSION:

    After systematic investigation, Z² = 32π/3 does NOT appear naturally
    in the differential geometry of reaction networks.

    WHAT WE FOUND:
    1. Z² = 8 × V_3 (8 unit sphere volumes) - by construction
    2. 8π/Z² = 3/4 exactly - by definition of Z²
    3. Z/12 ≈ 0.482, close to protein factor 0.491 (1.8% off)
    4. The curvature of concentration space does NOT involve Z²

    HONEST ASSESSMENT:
    The differential geometry framework (Ricci curvature, geodesics) IS
    relevant to understanding reaction network dynamics and could help
    explain self-organization. BUT this geometry does not require or
    involve the specific constant Z² = 32π/3.

    The near-match Z/12 ≈ protein factor is intriguing but:
    - 12 is the kissing number in 3D, relating to sphere packing
    - Protein packing is constrained by geometry
    - BUT the 1.8% discrepancy suggests coincidence, not deep connection

    If there IS a connection, it would require:
    1. Deriving why proteins should pack with factor Z/12 from first principles
    2. Finding the exact divisor (11.79, not 12)
    3. Connecting to the Z² cosmological origin (Friedmann + Bekenstein)
    """

    print(results['conclusion'])

    return results


# =============================================================================
# MAIN
# =============================================================================

def main():
    """Run differential geometry analysis of reaction networks."""

    print("=" * 70)
    print("DIFFERENTIAL GEOMETRY OF CHEMICAL REACTION NETWORKS")
    print("=" * 70)

    # 1. Basic curvature analysis
    print("\n" + "-" * 70)
    print("1. CURVATURE ANALYSIS OF RANDOM NETWORKS")
    print("-" * 70)

    curvature_results = analyze_autocatalytic_curvature(n_species=4, n_reactions=6)

    print(f"\nAnalyzed {len(curvature_results['trials'])} random networks")
    avg_det = np.mean([t['det_metric'] for t in curvature_results['trials']])
    print(f"Average metric determinant: {avg_det:.4f}")
    print(f"Fisher curvature: {curvature_results['trials'][0]['scalar_curvature_fisher']:.2f}")

    # 2. Geodesic analysis
    print("\n" + "-" * 70)
    print("2. GEODESIC REACTION PATHWAYS")
    print("-" * 70)

    n_species = 3
    manifold = ConcentrationManifold(n_species, ['A', 'B', 'C'])

    # Simple reaction network: A + B <-> C
    stoichiometry = np.array([
        [-1, 1],   # A
        [-1, 1],   # B
        [1, -1]    # C
    ])
    rate_constants = np.array([1.0, 0.5])

    c0 = np.array([1.0, 1.0, 0.1])
    v0 = np.array([0.1, 0.1, 0.2])

    trajectory = integrate_geodesic(manifold, c0, v0, stoichiometry, rate_constants,
                                   dt=0.01, n_steps=50)

    print(f"Starting concentrations: {c0}")
    print(f"Final concentrations: {trajectory[-1]}")
    print(f"Geodesic represents thermodynamically favorable pathway")

    # 3. Z² investigation
    z2_results = investigate_z2_in_geometry()

    # Save results
    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(output_dir, 'differential_geometry_results.json')

    output_data = {
        'curvature_analysis': curvature_results,
        'z2_investigation': {
            'z_squared': z2_results['z_squared'],
            'z_constant': z2_results['z_constant'],
            'findings': z2_results['findings'],
            'conclusion': 'Z² does not appear naturally in CRN geometry'
        }
    }

    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2, default=str)

    print(f"\n  Results saved to: {output_file}")


if __name__ == "__main__":
    main()
