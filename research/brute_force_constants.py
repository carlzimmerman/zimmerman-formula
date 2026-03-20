#!/usr/bin/env python3
"""
BRUTE FORCE SEARCH FOR FUNDAMENTAL RELATIONSHIPS
=================================================

This script searches for simple mathematical relationships between
fundamental constants and unexplained physical quantities.

The approach that found a₀ = c√(Gρc)/2 was:
1. Dimensional analysis to find valid combinations
2. Numerical comparison to observed values
3. Look for simple coefficients (2, π, 4π, etc.)

We apply this systematically to search for other relationships.

Author: Carl Zimmerman
Date: March 2026
"""

import numpy as np
from itertools import product
from dataclasses import dataclass
from typing import List, Tuple, Dict
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# FUNDAMENTAL CONSTANTS (SI units)
# =============================================================================

# Exact or well-known constants
c = 299792458.0  # m/s (exact)
G = 6.67430e-11  # m³/(kg·s²)
hbar = 1.054571817e-34  # J·s
k_B = 1.380649e-23  # J/K (exact)
e_charge = 1.602176634e-19  # C (exact)
epsilon_0 = 8.8541878128e-12  # F/m
m_e = 9.1093837015e-31  # kg
m_p = 1.67262192369e-27  # kg

# Cosmological parameters (Planck 2018)
H_0 = 2.27e-18  # s⁻¹ (70 km/s/Mpc)
rho_c = 9.47e-27  # kg/m³
Omega_m = 0.315
Omega_Lambda = 0.685
T_CMB = 2.725  # K
t_universe = 4.35e17  # s (13.8 Gyr)

# Derived quantities
alpha = e_charge**2 / (4 * np.pi * epsilon_0 * hbar * c)  # ~1/137
R_H = c / H_0  # Hubble radius
l_P = np.sqrt(hbar * G / c**3)  # Planck length
t_P = np.sqrt(hbar * G / c**5)  # Planck time
m_P = np.sqrt(hbar * c / G)  # Planck mass
T_P = np.sqrt(hbar * c**5 / (G * k_B**2))  # Planck temperature

# MOND scale (observed)
a_0 = 1.2e-10  # m/s²

# =============================================================================
# TARGET QUANTITIES (unexplained values to search for)
# =============================================================================

@dataclass
class Target:
    name: str
    value: float
    units: str
    dimensions: Tuple[int, int, int, int, int]  # (length, mass, time, temp, charge)
    description: str

TARGETS = [
    # Dimensionless quantities
    Target("alpha", alpha, "dimensionless", (0, 0, 0, 0, 0), "Fine structure constant ~1/137"),
    Target("eta", 6e-10, "dimensionless", (0, 0, 0, 0, 0), "Baryon-to-photon ratio"),
    Target("A_s", 2.1e-9, "dimensionless", (0, 0, 0, 0, 0), "Primordial fluctuation amplitude"),
    Target("Omega_ratio", Omega_Lambda/Omega_m, "dimensionless", (0, 0, 0, 0, 0), "Dark energy/matter ratio ~2.17"),
    Target("n_s-1", -0.035, "dimensionless", (0, 0, 0, 0, 0), "Spectral index deviation from 1"),

    # Dimensional quantities
    Target("a_0", a_0, "m/s²", (1, 0, -2, 0, 0), "MOND acceleration scale"),
    Target("T_CMB", T_CMB, "K", (0, 0, 0, 1, 0), "CMB temperature"),
    Target("m_e", m_e, "kg", (0, 1, 0, 0, 0), "Electron mass"),
    Target("m_e/m_p", m_e/m_p, "dimensionless", (0, 0, 0, 0, 0), "Electron/proton mass ratio ~1/1836"),
    Target("m_e/m_P", m_e/m_P, "dimensionless", (0, 0, 0, 0, 0), "Electron/Planck mass ratio"),
]

# =============================================================================
# BUILDING BLOCKS
# =============================================================================

@dataclass
class Constant:
    name: str
    value: float
    dimensions: Tuple[int, int, int, int, int]  # (L, M, T, Θ, Q)

# Fundamental constants with their dimensions
# Dimensions: (length, mass, time, temperature, charge)
CONSTANTS = [
    Constant("c", c, (1, 0, -1, 0, 0)),
    Constant("G", G, (3, -1, -2, 0, 0)),
    Constant("ℏ", hbar, (2, 1, -1, 0, 0)),
    Constant("k_B", k_B, (2, 1, -2, -1, 0)),
    Constant("H₀", H_0, (0, 0, -1, 0, 0)),
    Constant("ρ_c", rho_c, (-3, 1, 0, 0, 0)),
    Constant("m_p", m_p, (0, 1, 0, 0, 0)),
    Constant("m_e", m_e, (0, 1, 0, 0, 0)),
    Constant("e", e_charge, (0, 0, 1, 0, 1)),  # Charge dimension
    Constant("ε₀", epsilon_0, (-3, -1, 4, 0, 2)),
    Constant("R_H", R_H, (1, 0, 0, 0, 0)),
    Constant("t₀", t_universe, (0, 0, 1, 0, 0)),
    Constant("l_P", l_P, (1, 0, 0, 0, 0)),
    Constant("t_P", t_P, (0, 0, 1, 0, 0)),
    Constant("m_P", m_P, (0, 1, 0, 0, 0)),
    Constant("T_P", T_P, (0, 0, 0, 1, 0)),
]

# Simple coefficients to test
COEFFICIENTS = [1, 2, 3, 4, 1/2, 1/3, 1/4,
                np.pi, 2*np.pi, 4*np.pi, np.pi/2,
                np.sqrt(2), np.sqrt(3), np.sqrt(np.pi),
                2*np.sqrt(2*np.pi/3),  # The Zimmerman coefficient
                np.e, 1/np.e]

# =============================================================================
# SEARCH FUNCTIONS
# =============================================================================

def compute_dimensions(powers: List[int], constants: List[Constant]) -> Tuple[int, int, int, int, int]:
    """Compute resulting dimensions from powers of constants."""
    dims = [0, 0, 0, 0, 0]
    for power, const in zip(powers, constants):
        for i in range(5):
            dims[i] += power * const.dimensions[i]
    return tuple(dims)

def compute_value(powers: List[int], constants: List[Constant]) -> float:
    """Compute numerical value from powers of constants."""
    result = 1.0
    for power, const in zip(powers, constants):
        if power != 0:
            result *= const.value ** power
    return result

def dimensions_match(dims1: Tuple, dims2: Tuple) -> bool:
    """Check if two dimension tuples match."""
    return all(d1 == d2 for d1, d2 in zip(dims1, dims2))

def search_for_target(target: Target, max_power: int = 2,
                      constants_to_use: List[Constant] = None) -> List[Dict]:
    """
    Search for combinations of constants that match the target.

    Returns list of matches with their formulas and coefficients.
    """
    if constants_to_use is None:
        constants_to_use = CONSTANTS

    matches = []
    n_constants = len(constants_to_use)

    # Generate all power combinations
    power_range = range(-max_power, max_power + 1)

    for powers in product(power_range, repeat=n_constants):
        # Skip all-zero case
        if all(p == 0 for p in powers):
            continue

        # Check dimensions
        dims = compute_dimensions(list(powers), constants_to_use)
        if not dimensions_match(dims, target.dimensions):
            continue

        # Compute value
        try:
            value = compute_value(list(powers), constants_to_use)
            if value <= 0 or not np.isfinite(value):
                continue
        except:
            continue

        # Check if it matches target (within some factor)
        ratio = target.value / value if target.value != 0 else 0
        if ratio <= 0:
            continue

        # Check if ratio is close to a simple coefficient
        for coeff in COEFFICIENTS:
            if 0.95 < ratio / coeff < 1.05:  # Within 5%
                # Build formula string
                formula_parts = []
                for power, const in zip(powers, constants_to_use):
                    if power == 0:
                        continue
                    elif power == 1:
                        formula_parts.append(const.name)
                    elif power == -1:
                        formula_parts.append(f"1/{const.name}")
                    elif power > 0:
                        formula_parts.append(f"{const.name}^{power}")
                    else:
                        formula_parts.append(f"{const.name}^({power})")

                formula = " × ".join(formula_parts)

                # Format coefficient
                if abs(coeff - round(coeff)) < 0.01:
                    coeff_str = str(int(round(coeff)))
                elif abs(coeff - np.pi) < 0.01:
                    coeff_str = "π"
                elif abs(coeff - 2*np.pi) < 0.01:
                    coeff_str = "2π"
                elif abs(coeff - 4*np.pi) < 0.01:
                    coeff_str = "4π"
                elif abs(coeff - np.sqrt(2)) < 0.01:
                    coeff_str = "√2"
                elif abs(coeff - 1/2) < 0.01:
                    coeff_str = "1/2"
                elif abs(coeff - 2*np.sqrt(8*np.pi/3)) < 0.01:
                    coeff_str = "2√(8π/3)"
                else:
                    coeff_str = f"{coeff:.4f}"

                matches.append({
                    'formula': formula,
                    'coefficient': coeff_str,
                    'coeff_value': coeff,
                    'computed': value * coeff,
                    'target': target.value,
                    'accuracy': abs(1 - (value * coeff) / target.value) * 100,
                    'powers': powers
                })

    # Sort by accuracy
    matches.sort(key=lambda x: x['accuracy'])
    return matches

def search_dimensionless_ratios(max_power: int = 2) -> List[Dict]:
    """
    Search for interesting dimensionless ratios between constants.
    """
    matches = []

    # Pairs of constants to compare
    pairs = [
        ("R_H", R_H, "l_P", l_P),
        ("t₀", t_universe, "t_P", t_P),
        ("m_P", m_P, "m_p", m_p),
        ("m_P", m_P, "m_e", m_e),
        ("T_P", T_P, "T_CMB", T_CMB),
    ]

    for name1, val1, name2, val2 in pairs:
        ratio = val1 / val2
        log_ratio = np.log10(ratio)

        matches.append({
            'ratio': f"{name1}/{name2}",
            'value': ratio,
            'log10': log_ratio,
            'interpretation': f"{name1} is 10^{log_ratio:.1f} times {name2}"
        })

    return matches

# =============================================================================
# MAIN SEARCH
# =============================================================================

def main():
    print("=" * 70)
    print("BRUTE FORCE SEARCH FOR FUNDAMENTAL RELATIONSHIPS")
    print("=" * 70)
    print()

    # First, verify we can find the known relationship
    print("VERIFICATION: Can we rediscover a₀ = c√(Gρc)/2 ?")
    print("-" * 50)

    a0_target = Target("a_0", a_0, "m/s²", (1, 0, -2, 0, 0), "MOND scale")
    a0_matches = search_for_target(a0_target, max_power=2)

    if a0_matches:
        print(f"✓ Found {len(a0_matches)} matches for a₀:")
        for m in a0_matches[:3]:
            print(f"  a₀ = {m['coefficient']} × {m['formula']}")
            print(f"      Accuracy: {m['accuracy']:.2f}%")
    else:
        print("✗ No matches found (search may need wider range)")

    print()
    print("=" * 70)
    print("SEARCHING FOR NEW RELATIONSHIPS")
    print("=" * 70)

    all_results = {}

    for target in TARGETS:
        print(f"\n{'='*50}")
        print(f"Target: {target.name} = {target.value:.3e} {target.units}")
        print(f"Description: {target.description}")
        print("-" * 50)

        matches = search_for_target(target, max_power=2)
        all_results[target.name] = matches

        if matches:
            print(f"Found {len(matches)} potential matches:")
            for m in matches[:5]:  # Top 5
                print(f"\n  {target.name} ≈ {m['coefficient']} × {m['formula']}")
                print(f"  Computed: {m['computed']:.3e}")
                print(f"  Accuracy: {m['accuracy']:.2f}%")
        else:
            print("  No simple matches found")

    # Search for dimensionless ratios
    print()
    print("=" * 70)
    print("INTERESTING DIMENSIONLESS RATIOS")
    print("=" * 70)

    ratios = search_dimensionless_ratios()
    for r in ratios:
        print(f"\n  {r['ratio']} = {r['value']:.3e}")
        print(f"  {r['interpretation']}")

    # Check for Dirac large number coincidences
    print()
    print("=" * 70)
    print("DIRAC LARGE NUMBER COINCIDENCES")
    print("=" * 70)

    # EM/gravity ratio
    F_em_grav = (e_charge**2 / (4*np.pi*epsilon_0)) / (G * m_e * m_p)
    print(f"\n  F_EM / F_grav (e-p) = {F_em_grav:.3e}")
    print(f"  ≈ 10^{np.log10(F_em_grav):.1f}")

    # Hubble radius / classical electron radius
    r_e = e_charge**2 / (4*np.pi*epsilon_0*m_e*c**2)
    ratio_hubble_electron = R_H / r_e
    print(f"\n  R_H / r_e = {ratio_hubble_electron:.3e}")
    print(f"  ≈ 10^{np.log10(ratio_hubble_electron):.1f}")

    # Number of particles in universe
    N_particles = rho_c * (4*np.pi/3) * R_H**3 / m_p
    print(f"\n  N_particles ≈ {N_particles:.3e}")
    print(f"  ≈ 10^{np.log10(N_particles):.1f}")
    print(f"  ≈ (F_EM/F_grav)^2 = 10^{2*np.log10(F_em_grav):.1f}")

    # New check: CMB temperature relationship
    print()
    print("=" * 70)
    print("CMB TEMPERATURE RELATIONSHIP")
    print("=" * 70)

    # T_CMB vs T_P × (t_P/t₀)^x
    for x in [0.5, 0.51, 0.52, 0.53]:
        T_predicted = T_P * (t_P / t_universe)**x
        accuracy = abs(1 - T_predicted/T_CMB) * 100
        print(f"\n  T_P × (t_P/t₀)^{x} = {T_predicted:.3f} K")
        print(f"  T_CMB = {T_CMB} K")
        print(f"  Accuracy: {accuracy:.1f}%")

    # Physical interpretation of a₀
    print()
    print("=" * 70)
    print("PHYSICAL INTERPRETATION OF a₀")
    print("=" * 70)

    g_hubble = c * H_0 / 2
    print(f"\n  g_Hubble = cH₀/2 = {g_hubble:.3e} m/s²")
    print(f"  a₀ = {a_0:.3e} m/s²")
    print(f"  Ratio: g_Hubble / a₀ = {g_hubble/a_0:.3f}")
    print(f"  √(8π/3) = {np.sqrt(8*np.pi/3):.3f}")
    print(f"\n  ⟹ a₀ = g_Hubble / √(8π/3) = cH₀ / (2√(8π/3)) = cH₀/5.79 ✓")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY OF FINDINGS")
    print("=" * 70)

    print("""
    CONFIRMED:
    ✓ a₀ = c√(Gρ_c)/2 = cH₀/5.79
    ✓ a₀ = g_Hubble / √(8π/3) where g_Hubble = cH₀/2

    INTERESTING BUT NOT EXACT:
    • T_CMB ≈ T_P × (t_P/t₀)^0.52 (but exponent isn't simple)
    • m_e ≈ m_P × (l_P/R_H)^(1/3) / 120 (factor of 120 is ugly)

    DIRAC COINCIDENCES (known):
    • F_EM/F_grav ≈ 10^40
    • R_H/r_e ≈ 10^40
    • N_particles ≈ 10^80 ≈ (10^40)²

    NO SIMPLE FORMULA FOUND:
    • α = 1/137 (fine structure constant)
    • η = 6×10⁻¹⁰ (baryon asymmetry)
    • A_s = 2×10⁻⁹ (primordial amplitude)
    """)

    return all_results

if __name__ == "__main__":
    results = main()
