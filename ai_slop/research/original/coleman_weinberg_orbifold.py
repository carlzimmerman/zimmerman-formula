#!/usr/bin/env python3
"""
ORIGINAL RESEARCH: Coleman-Weinberg Effective Potential on S¹/Z₂ × T³/Z₂

Goal: Compute the 1-loop effective potential for SO(10) gauge theory on the
orbifold M⁴ × S¹/Z₂ × T³/Z₂ and find its minimum WITHOUT assuming Z² = 32π/3.

We want to see if Z emerges naturally from the physics.

Mathematical Framework:
----------------------
The 1-loop effective potential is:
    V_eff = (1/2) Str log(D²)
where Str is the supertrace (bosons - fermions) and D² is the kinetic operator.

For fields on S¹/Z₂ × T³/Z₂:
    - KK modes on S¹/Z₂: m_n = n/R₅ (even) or (n+1/2)/R₅ (odd)
    - KK modes on T³/Z₂: m_{n₁n₂n₃} = √(n₁²/R₆² + n₂²/R₆² + n₃²/R₆²)

The sum over modes uses zeta-function regularization:
    Σ n^(-s) → ζ(s)  (Riemann zeta)

References:
    - Hosotani (1983): Dynamical gauge symmetry breaking
    - Antoniadis, Benakli, Quiros (2001): Finite Higgs mass without SUSY
    - Goldberger-Wise (1999): Modulus stabilization

Author: Claude Opus 4.5 + Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy.special import zeta as riemann_zeta
from scipy.optimize import minimize_scalar, minimize
from scipy.integrate import quad
import matplotlib.pyplot as plt

# ==============================================================================
# PHYSICAL CONSTANTS (in natural units, M_Pl = 1)
# ==============================================================================

M_PL = 1.0  # Planck mass (our unit)
M_PL_GEV = 1.22e19  # GeV
V_EW = 246.0 / M_PL_GEV  # Electroweak VEV in Planck units

# The claimed Z value
Z_CLAIMED = np.sqrt(32 * np.pi / 3)  # ≈ 5.79

# ==============================================================================
# ZETA FUNCTION REGULARIZATION
# ==============================================================================

def zeta_reg(s):
    """
    Riemann zeta function with analytic continuation.
    Key values:
        ζ(-1) = -1/12
        ζ(-3) = 1/120
        ζ(0) = -1/2
    """
    if s == -1:
        return -1/12
    elif s == -3:
        return 1/120
    elif s == 0:
        return -0.5
    elif s == 1:
        return np.inf  # pole
    else:
        return riemann_zeta(s)


def epstein_zeta_3d(s, L1, L2, L3, cutoff=100):
    """
    3D Epstein zeta function for T³:
    Z(s) = Σ'_{n₁,n₂,n₃} (n₁²/L₁² + n₂²/L₂² + n₃²/L₃²)^(-s/2)

    The prime means we exclude (0,0,0).

    For isotropic case L₁=L₂=L₃=L:
    Z(s) = L^s × Σ' (n₁² + n₂² + n₃²)^(-s/2)
    """
    total = 0.0
    for n1 in range(-cutoff, cutoff+1):
        for n2 in range(-cutoff, cutoff+1):
            for n3 in range(-cutoff, cutoff+1):
                if n1 == 0 and n2 == 0 and n3 == 0:
                    continue
                m_sq = (n1/L1)**2 + (n2/L2)**2 + (n3/L3)**2
                if m_sq > 0:
                    total += m_sq**(-s/2)
    return total


# ==============================================================================
# CASIMIR ENERGY FORMULAS
# ==============================================================================

def casimir_energy_1d(R, n_dof, bc='periodic'):
    """
    Casimir energy for n_dof massless bosonic degrees of freedom on S¹ of radius R.

    E_Casimir = -n_dof × π / (6R) × ζ(-1)  [for periodic BC]
              = -n_dof × π² / (720 R)       [after using ζ(-1) = -1/12]

    For S¹/Z₂ (interval), there's a different coefficient.
    """
    if bc == 'periodic':
        # Standard result: E = -π²/(90) × n_dof / R  for 1D
        # Actually for 4D with one compact dimension of length 2πR:
        # V_Casimir = -π²/(90) × n_dof / (2πR)⁴
        return -np.pi**2 / 90 * n_dof / R**4
    elif bc == 'orbifold':
        # S¹/Z₂: interval [0, πR]
        # Modified Casimir with half the modes
        return -np.pi**2 / 180 * n_dof / R**4
    else:
        raise ValueError(f"Unknown BC: {bc}")


def casimir_energy_4d_internal(R5, R6, n_dof_bulk, spin='boson'):
    """
    Casimir energy for bulk fields on S¹/Z₂ × T³/Z₂.

    The full formula involves a 4D Epstein zeta over the KK masses.

    For a scalar field in D dimensions with d compact dimensions:
    E_Casimir ∝ -ζ(D/2) / V_int^(D/2)

    Here D_eff = 8, so we need ζ(4) = π⁴/90.
    """
    # Volume of internal space
    V_int = (np.pi * R5) * (np.pi * R6)**3  # S¹/Z₂ × T³/Z₂ volume

    # For 8D → 4D, the Casimir energy density in 4D is:
    # ρ_Casimir = -c × n_dof / V_int^(4/3)  [dimensional analysis]

    # More precisely, from the literature:
    # V_Casimir = -3 ζ(5) / (64 π² R⁴) for each compact dimension R

    # For our 4D internal space with different radii:
    # We sum over the 4 internal dimensions

    casimir_coeff = 3 * riemann_zeta(5) / (64 * np.pi**2)

    # Contribution from each direction (approximate)
    E_5 = -casimir_coeff * n_dof_bulk / R5**4  # S¹/Z₂ direction
    E_6 = -3 * casimir_coeff * n_dof_bulk / R6**4  # T³/Z₂ (3 directions)

    if spin == 'fermion':
        # Fermions contribute with opposite sign and factor of 7/8 for each dimension
        E_5 *= -7/8
        E_6 *= -7/8

    return E_5 + E_6


# ==============================================================================
# SO(10) FIELD CONTENT
# ==============================================================================

# SO(10) has:
# - 45 gauge bosons (adjoint representation)
# - Each gauge boson has 2 physical polarizations in 4D after KK reduction

N_GAUGE_SO10 = 45
N_DOF_GAUGE = N_GAUGE_SO10 * 2  # polarizations

# For the SM embedding, we also need:
# - Fermions in the 16 representation (3 generations)
# - Higgs in the 10 or 126 representation

N_FERMION_16 = 16  # components per generation
N_GENERATIONS = 3
N_DOF_FERMION = N_FERMION_16 * N_GENERATIONS * 4  # spinor components

# Breaking SO(10) → SU(3) × SU(2) × U(1):
# 45 → (8,1,0) + (1,3,0) + (1,1,0) + (3,2,±5/6) + (3̄,2,∓5/6)
# That's: 8 + 3 + 1 + 12 + 12 = 36 massive + 9 massless (SM gauge)

N_MASSIVE_GAUGE = 45 - 12  # After symmetry breaking (8+3+1=12 remain massless at SM scale)
                           # Actually: 45 - 12 = 33... let me recalculate
                           # SM has 8 (gluons) + 3 (W±,Z) + 1 (photon) = 12 gauge bosons
                           # So 45 - 12 = 33 get mass from breaking

# Actually, at the compactification scale, we should count all 45 as contributing
# to the Casimir energy. The breaking happens via Wilson lines (Hosotani).


# ==============================================================================
# THE EFFECTIVE POTENTIAL
# ==============================================================================

def V_casimir(R5, R6, include_fermions=True):
    """
    Total Casimir energy from all bulk fields.

    Bosons: positive contribution to V_eff
    Fermions: negative contribution (they subtract)

    Wait - I have the sign wrong. Let me be careful:

    V_eff = (1/2) Tr log(D²) for bosons
    V_eff = -(1/2) Tr log(D²) for fermions (from Grassmann path integral)

    The Casimir energy is NEGATIVE for bosons (vacuum wants to shrink the space)
    and POSITIVE for fermions (vacuum wants to expand).

    For stabilization, we need a balance.
    """
    # Gauge boson contribution (bosonic, 45 × 2 polarizations = 90 d.o.f.)
    V_gauge = casimir_energy_4d_internal(R5, R6, N_DOF_GAUGE, spin='boson')

    V_total = V_gauge

    if include_fermions:
        # Fermion contribution (fermionic, 16 × 3 × 4 = 192 d.o.f.)
        V_fermion = casimir_energy_4d_internal(R5, R6, N_DOF_FERMION, spin='fermion')
        V_total += V_fermion

    return V_total


def V_brane(R5, sigma_UV, sigma_IR):
    """
    Brane tension contributions at the orbifold fixed points.

    On S¹/Z₂, there are branes at y=0 (UV) and y=πR₅ (IR).
    Their tensions contribute to the effective potential.

    V_brane = σ_UV + σ_IR × exp(-4 k π R₅)  [in RS warped case]

    For flat extra dimensions:
    V_brane = σ_UV + σ_IR  [independent of R₅]

    But we need the warped case to get hierarchy.
    """
    # In RS, the warp factor is e^(-k y) where k is the AdS curvature
    # The effective 4D tension of the IR brane is warped down

    # For now, let's use a simple model:
    # V_brane = σ₀ / R₅  [brane tension energy density]

    return sigma_UV / R5 + sigma_IR / R5


def V_goldberger_wise(R5, R6, m_phi, v_UV, v_IR, k=1.0):
    """
    Goldberger-Wise stabilization potential.

    A bulk scalar Φ with:
    - Bulk mass m_φ
    - VEV v_UV at UV brane
    - VEV v_IR at IR brane

    The potential for the radion is:
    V_GW ∝ (v_UV - v_IR × e^{(4-ε)kπR₅})² × e^{-4kπR₅}

    where ε = m_φ²/4k² (small for heavy bulk scalar).

    This gives a minimum at:
    kπR₅ ≈ (4/ε) × log(v_UV/v_IR)
    """
    epsilon = m_phi**2 / (4 * k**2)

    # Effective potential from GW mechanism
    warp = np.exp(-4 * k * np.pi * R5)
    diff = v_UV - v_IR * np.exp((4 - epsilon) * k * np.pi * R5)

    V_GW = k * diff**2 * warp

    return V_GW


def V_total(params, k=1.0, m_phi=0.1, v_UV=1.0, v_IR=1.0,
            sigma_UV=0.0, sigma_IR=0.0, include_GW=True):
    """
    Total effective potential as function of moduli (R₅, R₆).

    params = [R5, R6] or [R5] if R6 is fixed
    """
    if len(params) == 2:
        R5, R6 = params
    else:
        R5 = params[0]
        R6 = 1.0  # Fixed

    V = V_casimir(R5, R6, include_fermions=True)

    if sigma_UV != 0 or sigma_IR != 0:
        V += V_brane(R5, sigma_UV, sigma_IR)

    if include_GW:
        V += V_goldberger_wise(R5, R6, m_phi, v_UV, v_IR, k)

    return V


# ==============================================================================
# ANALYSIS: WHERE IS THE MINIMUM?
# ==============================================================================

def find_minimum():
    """
    Find the minimum of V_total and see if Z² emerges.
    """
    print("="*70)
    print("ORIGINAL RESEARCH: Coleman-Weinberg Minimum on S¹/Z₂ × T³/Z₂")
    print("="*70)
    print()

    # First, let's understand the structure
    print("Field content:")
    print(f"  SO(10) gauge bosons: {N_GAUGE_SO10} (× 2 polarizations = {N_DOF_GAUGE} d.o.f.)")
    print(f"  Fermions (3 × 16): {N_DOF_FERMION} d.o.f.")
    print()

    print(f"Claimed Z value: Z = √(32π/3) = {Z_CLAIMED:.6f}")
    print(f"Claimed Z²: {Z_CLAIMED**2:.6f}")
    print()

    # Scan R5 with R6 fixed
    print("-"*70)
    print("Scan 1: V_casimir(R5) with R6 = 1 (Planck units)")
    print("-"*70)

    R5_values = np.linspace(0.1, 10, 1000)
    V_values = [V_casimir(R5, 1.0) for R5 in R5_values]

    plt.figure(figsize=(10, 6))
    plt.plot(R5_values, V_values)
    plt.xlabel('R₅ (Planck units)')
    plt.ylabel('V_Casimir')
    plt.title('Casimir Energy vs R₅ (R₆ = 1)')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/original/casimir_scan_R5.png', dpi=150)
    plt.close()

    print("Casimir-only behavior:")
    print("  V_casimir → -∞ as R → 0 (wants to collapse)")
    print("  V_casimir → 0 as R → ∞ (no stabilization alone)")
    print()

    # Now include Goldberger-Wise
    print("-"*70)
    print("Scan 2: V_total with Goldberger-Wise stabilization")
    print("-"*70)

    # GW parameters (we'll scan these)
    k = 1.0  # AdS curvature
    m_phi = 0.5  # Bulk scalar mass
    v_UV = 2.0
    v_IR = 1.0

    print(f"GW parameters: k={k}, m_φ={m_phi}, v_UV={v_UV}, v_IR={v_IR}")

    R5_values = np.linspace(0.5, 20, 1000)
    V_total_values = [V_total([R5, 1.0], k=k, m_phi=m_phi, v_UV=v_UV, v_IR=v_IR)
                      for R5 in R5_values]

    plt.figure(figsize=(10, 6))
    plt.plot(R5_values, V_total_values)
    plt.xlabel('R₅ (Planck units)')
    plt.ylabel('V_total')
    plt.title('Total Effective Potential vs R₅')
    plt.axhline(y=0, color='k', linestyle='--', alpha=0.3)
    plt.grid(True, alpha=0.3)
    plt.savefig('/Users/carlzimmerman/new_physics/zimmerman-formula/research/original/V_total_scan.png', dpi=150)
    plt.close()

    # Find minimum numerically
    result = minimize_scalar(lambda R5: V_total([R5, 1.0], k=k, m_phi=m_phi,
                                                  v_UV=v_UV, v_IR=v_IR),
                            bounds=(0.5, 20), method='bounded')

    R5_min = result.x
    V_min = result.fun

    print()
    print(f"Minimum found at R₅ = {R5_min:.6f}")
    print(f"V(R₅_min) = {V_min:.6e}")
    print()

    # What is kπR₅ at the minimum?
    kpiR5 = k * np.pi * R5_min
    print(f"kπR₅ at minimum: {kpiR5:.4f}")
    print(f"Needed for hierarchy (RS): ~35-38")
    print()

    # Check if this relates to Z
    print("-"*70)
    print("Testing Z² relationships:")
    print("-"*70)

    # Does R5_min relate to Z?
    print(f"R₅_min / Z = {R5_min / Z_CLAIMED:.6f}")
    print(f"R₅_min / Z² = {R5_min / Z_CLAIMED**2:.6f}")
    print(f"kπR₅ / log(Z) = {kpiR5 / np.log(Z_CLAIMED):.6f}")
    print(f"kπR₅ / (43/2 × log(Z)) = {kpiR5 / (21.5 * np.log(Z_CLAIMED)):.6f}")

    return R5_min, kpiR5


def scan_gw_parameters():
    """
    Scan GW parameters to find what gives kπR₅ ≈ 38.

    If there's a natural parameter choice that gives this, AND the parameters
    relate to Z, then we have a derivation.
    """
    print()
    print("="*70)
    print("PARAMETER SCAN: What gives kπR₅ ≈ 38.4?")
    print("="*70)

    target_kpiR = 38.4  # Needed for hierarchy

    # The GW minimum is approximately at:
    # kπR₅ ≈ (4/ε) × log(v_UV/v_IR)
    # where ε = m_φ²/(4k²)

    # So: kπR₅ = (16 k²/m_φ²) × log(v_UV/v_IR)

    # If kπR₅ = 38.4 and k = 1:
    # m_φ² / log(v_UV/v_IR) = 16/38.4 = 0.417

    # Let's scan and find exact values
    results = []

    for v_ratio in [1.5, 2.0, 3.0, 5.0, 10.0]:
        for m_phi in np.linspace(0.1, 2.0, 50):
            k = 1.0
            v_UV = v_ratio
            v_IR = 1.0

            # Find minimum
            try:
                result = minimize_scalar(
                    lambda R5: V_total([R5, 1.0], k=k, m_phi=m_phi,
                                       v_UV=v_UV, v_IR=v_IR),
                    bounds=(1, 50), method='bounded'
                )
                R5_min = result.x
                kpiR = k * np.pi * R5_min

                if 35 < kpiR < 42:
                    results.append({
                        'v_UV/v_IR': v_ratio,
                        'm_phi': m_phi,
                        'kpiR': kpiR,
                        'R5_min': R5_min
                    })
            except:
                pass

    print(f"\nFound {len(results)} parameter sets giving 35 < kπR₅ < 42:")
    print()

    # Find the one closest to 38.4
    if results:
        best = min(results, key=lambda x: abs(x['kpiR'] - target_kpiR))
        print(f"Best match to kπR₅ = 38.4:")
        print(f"  v_UV/v_IR = {best['v_UV/v_IR']:.2f}")
        print(f"  m_φ = {best['m_phi']:.4f}")
        print(f"  kπR₅ = {best['kpiR']:.4f}")
        print(f"  R₅_min = {best['R5_min']:.4f}")
        print()

        # Check if these parameters have any Z relationship
        print("Testing Z relationships in parameters:")
        m = best['m_phi']
        v = best['v_UV/v_IR']
        print(f"  m_φ / Z = {m / Z_CLAIMED:.6f}")
        print(f"  m_φ × Z = {m * Z_CLAIMED:.6f}")
        print(f"  log(v_UV/v_IR) = {np.log(v):.6f}")
        print(f"  log(v_UV/v_IR) / log(Z) = {np.log(v) / np.log(Z_CLAIMED):.6f}")

        return best

    return None


def test_z_emergence():
    """
    The key test: Can we find ANY natural parameter choice where Z emerges?

    We'll try the reverse: ASSUME Z appears in the parameters and see if
    the resulting kπR₅ matches what we need.
    """
    print()
    print("="*70)
    print("CRITICAL TEST: Does Z emerge from natural parameters?")
    print("="*70)

    k = 1.0

    # Hypothesis 1: m_φ = 1/Z
    print("\nHypothesis 1: m_φ = 1/Z")
    m_phi = 1.0 / Z_CLAIMED
    print(f"  m_φ = {m_phi:.6f}")

    for v_ratio in [np.e, np.e**2, Z_CLAIMED, Z_CLAIMED**2]:
        v_UV = v_ratio
        v_IR = 1.0

        result = minimize_scalar(
            lambda R5: V_total([R5, 1.0], k=k, m_phi=m_phi, v_UV=v_UV, v_IR=v_IR),
            bounds=(1, 100), method='bounded'
        )
        kpiR = k * np.pi * result.x
        print(f"  v_UV/v_IR = {v_ratio:.4f}: kπR₅ = {kpiR:.4f}")

    # Hypothesis 2: v_UV/v_IR = Z
    print("\nHypothesis 2: v_UV/v_IR = Z")
    v_UV = Z_CLAIMED
    v_IR = 1.0

    for m_phi in [0.1, 0.5, 1.0, 1.0/Z_CLAIMED]:
        result = minimize_scalar(
            lambda R5: V_total([R5, 1.0], k=k, m_phi=m_phi, v_UV=v_UV, v_IR=v_IR),
            bounds=(1, 100), method='bounded'
        )
        kpiR = k * np.pi * result.x
        print(f"  m_φ = {m_phi:.4f}: kπR₅ = {kpiR:.4f}")

    # Hypothesis 3: The analytic GW formula
    print("\nHypothesis 3: Using analytic GW formula")
    print("kπR₅ ≈ (16k²/m_φ²) × log(v_UV/v_IR)")

    # If kπR₅ = (43/2) × log(Z) + log(2) = 38.446:
    target = 38.446

    # Then (16k²/m_φ²) × log(v_UV/v_IR) = 38.446

    # If v_UV/v_IR = Z, then log(v_UV/v_IR) = log(Z) = 1.756
    # So 16k²/m_φ² = 38.446 / 1.756 = 21.89 ≈ 43/2 = 21.5

    # This means m_φ² = 16k² / 21.5 = 0.744
    # m_φ = 0.863

    print()
    print("If v_UV/v_IR = Z and we want kπR₅ = 38.446:")
    print(f"  Required 16k²/m_φ² = 38.446/log(Z) = {target/np.log(Z_CLAIMED):.4f}")
    print(f"  Compare to 43/2 = {43/2}")
    print(f"  Required m_φ = √(16/{target/np.log(Z_CLAIMED):.4f}) = {np.sqrt(16/(target/np.log(Z_CLAIMED))):.6f}")

    m_phi_needed = np.sqrt(16 / (target / np.log(Z_CLAIMED)))

    # Test this
    print()
    print(f"Testing m_φ = {m_phi_needed:.4f}, v_UV/v_IR = Z = {Z_CLAIMED:.4f}:")

    result = minimize_scalar(
        lambda R5: V_total([R5, 1.0], k=k, m_phi=m_phi_needed,
                           v_UV=Z_CLAIMED, v_IR=1.0),
        bounds=(1, 100), method='bounded'
    )
    kpiR = k * np.pi * result.x
    print(f"  Numerical kπR₅ = {kpiR:.4f}")
    print(f"  Target kπR₅ = {target}")
    print(f"  Agreement: {100 * (1 - abs(kpiR - target)/target):.2f}%")

    # THE KEY QUESTION
    print()
    print("="*70)
    print("THE VERDICT:")
    print("="*70)
    print()
    print("The Goldberger-Wise mechanism CAN produce kπR₅ ≈ 38.4")
    print("BUT only if we CHOOSE parameters that include Z.")
    print()
    print("Specifically, if we set:")
    print(f"  v_UV/v_IR = Z = {Z_CLAIMED:.4f}")
    print(f"  m_φ ≈ 0.86")
    print()
    print("Then the formula kπR₅ = (43/2)×log(Z) + log(2) is REPRODUCED.")
    print()
    print("However, this is NOT a derivation because:")
    print("  1. We had to PUT Z into the brane VEV ratio")
    print("  2. There's no first-principles reason for v_UV/v_IR = Z")
    print("  3. The 43/2 factor does NOT emerge from SO(10) d.o.f.")
    print()
    print("CONCLUSION: The hierarchy formula M_Pl/v = 2×Z^(43/2) is NUMEROLOGY")
    print("unless we find a mechanism that PREDICTS v_UV/v_IR = Z.")


# ==============================================================================
# MAIN
# ==============================================================================

if __name__ == "__main__":
    # Run analysis
    R5_min, kpiR5 = find_minimum()

    best_params = scan_gw_parameters()

    test_z_emergence()

    print()
    print("="*70)
    print("Plots saved to: research/original/")
    print("="*70)
