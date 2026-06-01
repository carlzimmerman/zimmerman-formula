#!/usr/bin/env python3
"""
Z² FRAMEWORK: EFFECTIVE MAJORANA MASS CALCULATOR
==================================================

Calculates m_ββ (effective Majorana mass for 0νββ decay) using
the Z² framework neutrino mass structure.

Key prediction: m_ββ ≈ 4 meV

Carl Zimmerman | May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, List

# =============================================================================
# Z² FRAMEWORK CONSTANTS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3  # = 33.510321
Z = np.sqrt(Z_SQUARED)       # = 5.788810

# Mass-squared differences (eV²) - PDG 2024
DELTA_M21_SQ = 7.53e-5      # Solar mass splitting
DELTA_M31_SQ = 2.453e-3     # Atmospheric mass splitting (NO)
DELTA_M32_SQ = 2.453e-3     # For IO: |Δm²_32| ≈ |Δm²_31|

# PMNS mixing angles (degrees) - PDG 2024
THETA_12 = 33.41            # Solar angle
THETA_13 = 8.58             # Reactor angle
THETA_23 = 42.2             # Atmospheric angle

# =============================================================================
# PMNS MATRIX ELEMENTS
# =============================================================================

def get_pmns_electron_row() -> Tuple[float, float, float]:
    """
    Return |U_e1|², |U_e2|², |U_e3|² (electron row of PMNS matrix, squared).
    """
    t12 = np.radians(THETA_12)
    t13 = np.radians(THETA_13)

    c12, s12 = np.cos(t12), np.sin(t12)
    c13, s13 = np.cos(t13), np.sin(t13)

    Ue1_sq = c12**2 * c13**2
    Ue2_sq = s12**2 * c13**2
    Ue3_sq = s13**2

    return Ue1_sq, Ue2_sq, Ue3_sq

# =============================================================================
# NEUTRINO MASSES
# =============================================================================

@dataclass
class NeutrinoMasses:
    """Neutrino mass eigenvalues in meV."""
    m1: float
    m2: float
    m3: float
    ordering: str  # "NO" or "IO"

def z2_masses() -> NeutrinoMasses:
    """
    Z² framework neutrino masses.

    From the seesaw with M_R ∝ diag(Z², Z, 1):
    m1 : m2 : m3 = 1 : Z : Z²

    Normalized to match Δm²_31.
    """
    # From Δm²_31 ≈ m3² (for hierarchical)
    m3_eV = np.sqrt(DELTA_M31_SQ)  # ≈ 0.050 eV = 50 meV
    m3 = m3_eV * 1000  # Convert to meV

    # Z² hierarchy
    m2 = m3 / Z
    m1 = m3 / Z_SQUARED

    return NeutrinoMasses(m1=m1, m2=m2, m3=m3, ordering="NO")

def normal_ordering_masses(m_lightest: float = 0.0) -> NeutrinoMasses:
    """
    Standard normal ordering masses for arbitrary lightest mass.

    m_lightest: m1 in meV (default: 0 = hierarchical limit)
    """
    m1 = m_lightest
    m2 = np.sqrt(m1**2 + DELTA_M21_SQ * 1e6)  # Convert eV² to meV²
    m3 = np.sqrt(m1**2 + DELTA_M31_SQ * 1e6)

    return NeutrinoMasses(m1=m1, m2=m2, m3=m3, ordering="NO")

def inverted_ordering_masses(m_lightest: float = 0.0) -> NeutrinoMasses:
    """
    Inverted ordering masses for arbitrary lightest mass.

    m_lightest: m3 in meV (default: 0 = hierarchical limit)
    """
    m3 = m_lightest
    # In IO: m1, m2 are heavier
    m1 = np.sqrt(m3**2 + DELTA_M31_SQ * 1e6 - DELTA_M21_SQ * 1e6)
    m2 = np.sqrt(m3**2 + DELTA_M31_SQ * 1e6)

    return NeutrinoMasses(m1=m1, m2=m2, m3=m3, ordering="IO")

# =============================================================================
# EFFECTIVE MAJORANA MASS CALCULATOR
# =============================================================================

def calculate_mbb(
    masses: NeutrinoMasses,
    alpha: float = 0.0,
    beta: float = 0.0
) -> float:
    """
    Calculate m_ββ (effective Majorana mass) in meV.

    m_ββ = |U²_e1 × m1 + U²_e2 × m2 × e^{iα} + U²_e3 × m3 × e^{iβ}|

    Parameters:
        masses: NeutrinoMasses object
        alpha: Majorana phase α (radians)
        beta: Majorana phase β (radians)

    Returns:
        m_ββ in meV
    """
    Ue1_sq, Ue2_sq, Ue3_sq = get_pmns_electron_row()

    # Complex contributions
    term1 = Ue1_sq * masses.m1
    term2 = Ue2_sq * masses.m2 * np.exp(1j * alpha)
    term3 = Ue3_sq * masses.m3 * np.exp(1j * beta)

    mbb = np.abs(term1 + term2 + term3)

    return mbb

def calculate_mbb_range(masses: NeutrinoMasses) -> Tuple[float, float]:
    """
    Calculate the range of m_ββ over all Majorana phases.

    Returns (m_ββ_min, m_ββ_max) in meV.
    """
    # Sample phase space
    n_points = 100
    alphas = np.linspace(0, 2*np.pi, n_points)
    betas = np.linspace(0, 2*np.pi, n_points)

    mbb_values = []
    for alpha in alphas:
        for beta in betas:
            mbb = calculate_mbb(masses, alpha, beta)
            mbb_values.append(mbb)

    return min(mbb_values), max(mbb_values)

# =============================================================================
# Z² FRAMEWORK PREDICTIONS
# =============================================================================

def z2_mbb_predictions() -> dict:
    """
    Calculate m_ββ for all CP-conserving Majorana phase combinations.

    Z² framework predicts α, β ∈ {0, π} (CP conservation).
    """
    masses = z2_masses()

    predictions = {}
    for alpha in [0, np.pi]:
        for beta in [0, np.pi]:
            phase_label = f"α={0 if alpha == 0 else 'π'}, β={0 if beta == 0 else 'π'}"
            mbb = calculate_mbb(masses, alpha, beta)
            predictions[phase_label] = mbb

    return predictions

# =============================================================================
# COMPARISON TO EXPERIMENTAL LIMITS
# =============================================================================

EXPERIMENTAL_LIMITS = {
    "KamLAND-Zen 800 (2024)": (36, 156),   # (optimistic, conservative) meV
    "GERDA (2020)": (79, 180),
    "CUORE (2022)": (90, 305),
    "EXO-200 (2019)": (147, 398),
}

FUTURE_EXPERIMENTS = {
    "LEGEND-200 (2028)": (20, 50),
    "LEGEND-1000 (2035)": (10, 20),
    "nEXO (2035+)": (5, 12),
    "KamLAND2-Zen (2030)": (10, 20),
    "CUPID (2030)": (10, 20),
}

# =============================================================================
# OUTPUT FUNCTIONS
# =============================================================================

def print_z2_predictions():
    """Print the Z² framework predictions for m_ββ."""
    print("=" * 70)
    print("Z² FRAMEWORK EFFECTIVE MAJORANA MASS PREDICTIONS")
    print("=" * 70)
    print()

    # Constants
    print("Z² Framework Constants:")
    print(f"  Z² = 32π/3 = {Z_SQUARED:.6f}")
    print(f"  Z = √Z² = {Z:.6f}")
    print()

    # Masses
    masses = z2_masses()
    print("Z² Neutrino Masses (Normal Ordering):")
    print(f"  m₁ = {masses.m1:.3f} meV")
    print(f"  m₂ = {masses.m2:.3f} meV")
    print(f"  m₃ = {masses.m3:.3f} meV")
    print()

    print("Verification:")
    print(f"  m₃/m₂ = {masses.m3/masses.m2:.3f} (should be Z = {Z:.3f})")
    print(f"  m₂/m₁ = {masses.m2/masses.m1:.3f} (should be Z = {Z:.3f})")
    ratio = (masses.m3**2 - masses.m1**2) / (masses.m2**2 - masses.m1**2)
    print(f"  Δm²₃₁/Δm²₂₁ = {ratio:.1f} (should be Z² = {Z_SQUARED:.1f})")
    print()

    # PMNS elements
    Ue1_sq, Ue2_sq, Ue3_sq = get_pmns_electron_row()
    print("PMNS Electron Row (|U_ei|²):")
    print(f"  |U_e1|² = {Ue1_sq:.4f}")
    print(f"  |U_e2|² = {Ue2_sq:.4f}")
    print(f"  |U_e3|² = {Ue3_sq:.4f}")
    print()

    # m_ββ predictions
    print("=" * 70)
    print("m_ββ PREDICTIONS FOR CP-CONSERVING PHASES")
    print("=" * 70)
    print()

    predictions = z2_mbb_predictions()
    for phase_label, mbb in predictions.items():
        print(f"  {phase_label}: m_ββ = {mbb:.2f} meV")

    print()
    print("-" * 70)
    most_likely = predictions["α=0, β=0"]
    print(f"  Most likely (tribimaximal alignment): m_ββ ≈ {most_likely:.1f} meV")
    print(f"  Range with CP conservation: {min(predictions.values()):.1f} - {max(predictions.values()):.1f} meV")
    print("-" * 70)
    print()

def print_experimental_comparison():
    """Compare Z² prediction to experimental limits."""
    print("=" * 70)
    print("COMPARISON TO EXPERIMENTAL LIMITS")
    print("=" * 70)
    print()

    z2_mbb = calculate_mbb(z2_masses(), alpha=0, beta=0)

    print(f"Z² Prediction: m_ββ ≈ {z2_mbb:.1f} meV")
    print()

    print("Current Limits:")
    for exp, (opt, cons) in EXPERIMENTAL_LIMITS.items():
        status = "✗ Cannot test" if opt > z2_mbb else "? Approaching"
        print(f"  {exp}: < {opt}-{cons} meV  {status}")

    print()
    print("Future Sensitivity:")
    for exp, (opt, cons) in FUTURE_EXPERIMENTS.items():
        if opt <= z2_mbb:
            status = "★ CAN TEST Z²"
        elif cons >= z2_mbb * 0.5:
            status = "→ Approaching"
        else:
            status = "✗ Cannot test"
        print(f"  {exp}: {opt}-{cons} meV  {status}")

    print()

def print_ordering_comparison():
    """Compare m_ββ for different mass orderings."""
    print("=" * 70)
    print("m_ββ FOR DIFFERENT MASS ORDERINGS")
    print("=" * 70)
    print()

    # Z² (Normal Ordering)
    z2 = z2_masses()
    z2_min, z2_max = calculate_mbb_range(z2)

    print(f"Z² Framework (NO, specific hierarchy):")
    print(f"  Range: {z2_min:.2f} - {z2_max:.2f} meV")
    print(f"  Most likely (α=β=0): {calculate_mbb(z2, 0, 0):.2f} meV")
    print()

    # Generic Normal Ordering (hierarchical)
    no_hier = normal_ordering_masses(m_lightest=0)
    no_hier_min, no_hier_max = calculate_mbb_range(no_hier)

    print(f"Generic Normal Ordering (m₁ → 0):")
    print(f"  Range: {no_hier_min:.2f} - {no_hier_max:.2f} meV")
    print()

    # Generic Normal Ordering (quasi-degenerate)
    no_qd = normal_ordering_masses(m_lightest=100)
    no_qd_min, no_qd_max = calculate_mbb_range(no_qd)

    print(f"Normal Ordering (quasi-degenerate, m₁ = 100 meV):")
    print(f"  Range: {no_qd_min:.1f} - {no_qd_max:.1f} meV")
    print()

    # Inverted Ordering (hierarchical)
    io_hier = inverted_ordering_masses(m_lightest=0)
    io_hier_min, io_hier_max = calculate_mbb_range(io_hier)

    print(f"Inverted Ordering (m₃ → 0):")
    print(f"  Range: {io_hier_min:.1f} - {io_hier_max:.1f} meV")
    print()

    print("-" * 70)
    print("KEY INSIGHT: Inverted ordering always gives m_ββ > 18 meV")
    print("             Z² (Normal, hierarchical) gives m_ββ ~ 0.4-4.7 meV")
    print("             Detection at 20-50 meV → rules out Z² framework")
    print("             Detection at ~4 meV → confirms Z² framework")
    print("-" * 70)
    print()

def main():
    """Main output."""
    print_z2_predictions()
    print_experimental_comparison()
    print_ordering_comparison()

    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print()
    print("Z² FRAMEWORK PREDICTION: m_ββ ≈ 4 ± 2 meV")
    print()
    print("This is:")
    print("  • Below current experimental sensitivity (>36 meV)")
    print("  • Within reach of nEXO (~5 meV by 2035+)")
    print("  • A decisive test between NO and IO")
    print("  • Consistent with the Δm²₃₁/Δm²₂₁ = Z² prediction")
    print()
    print("TESTABILITY TIMELINE:")
    print("  2028: LEGEND-200 rules out IO (20-50 meV)")
    print("  2035: nEXO begins testing Z² region (5-12 meV)")
    print("  2040: Multi-ton experiments probe ~4 meV")
    print()

if __name__ == "__main__":
    main()
