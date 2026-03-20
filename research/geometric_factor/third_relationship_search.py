#!/usr/bin/env python3
"""
Systematic Search for Third Relationship Involving 2√(8π/3)

We have two relationships:
1. a₀ = cH₀/(2√(8π/3))  - MOND acceleration
2. Ω_Λ/Ω_m = 4π/(2√(8π/3)) = √(3π/2)  - dark energy ratio

This script systematically searches for a THIRD relationship.
"""

import numpy as np
from itertools import combinations, permutations
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# TARGET VALUES (what we're looking for matches to)
# =============================================================================

TARGETS = {
    '2√(8π/3)': 2 * np.sqrt(8 * np.pi / 3),           # 5.7888
    '√(8π/3)': np.sqrt(8 * np.pi / 3),                 # 2.8944
    '8π/3': 8 * np.pi / 3,                              # 8.3776
    '√(3π/2)': np.sqrt(3 * np.pi / 2),                 # 2.1708
    '3π/2': 3 * np.pi / 2,                              # 4.7124
    '4π': 4 * np.pi,                                    # 12.566
    '1/(2√(8π/3))': 1 / (2 * np.sqrt(8 * np.pi / 3)), # 0.1727
    '2π': 2 * np.pi,                                    # 6.2832
    'π': np.pi,                                         # 3.1416
}

print("=" * 80)
print("TARGET VALUES TO MATCH")
print("=" * 80)
for name, val in TARGETS.items():
    print(f"  {name:20s} = {val:.6f}")
print()

# =============================================================================
# COSMOLOGICAL PARAMETERS (Planck 2018 + other sources)
# =============================================================================

COSMO_PARAMS = {
    # Density parameters
    'Ω_m': 0.3153,          # Total matter
    'Ω_Λ': 0.6847,          # Dark energy
    'Ω_b': 0.0493,          # Baryonic matter
    'Ω_c': 0.2607,          # Cold dark matter (Ω_m - Ω_b)
    'Ω_r': 9.15e-5,         # Radiation (photons + neutrinos)
    'Ω_γ': 5.38e-5,         # Photons only
    'Ω_ν': 3.77e-5,         # Neutrinos
    'Ω_k': 0.0007,          # Curvature (essentially 0)

    # Hubble parameter
    'H₀': 67.36,            # km/s/Mpc
    'h': 0.6736,            # H₀/100

    # CMB parameters
    'T_CMB': 2.7255,        # CMB temperature (K)
    'z_*': 1089.80,         # Redshift of last scattering
    'z_eq': 3402,           # Matter-radiation equality
    'z_re': 7.67,           # Reionization redshift

    # Primordial parameters
    'A_s': 2.101e-9,        # Scalar amplitude
    'n_s': 0.9649,          # Spectral index
    'r': 0.06,              # Tensor-to-scalar ratio (upper limit)
    'τ': 0.0544,            # Optical depth

    # Structure
    'σ_8': 0.8111,          # Amplitude of fluctuations
    'S_8': 0.832,           # σ_8 √(Ω_m/0.3)

    # Age
    't_0': 13.797,          # Age of universe (Gyr)

    # Baryon-to-photon ratio
    'η': 6.12e-10,          # Baryon-to-photon ratio

    # Neutrino mass
    'Σm_ν': 0.06,           # Sum of neutrino masses (eV, minimum)
}

# =============================================================================
# FUNDAMENTAL PHYSICS CONSTANTS
# =============================================================================

PHYSICS = {
    # Electromagnetic
    'α': 1/137.036,         # Fine structure constant
    '1/α': 137.036,         # Inverse fine structure constant

    # Mass ratios
    'm_p/m_e': 1836.15,     # Proton to electron mass
    'm_n/m_p': 1.00138,     # Neutron to proton mass

    # Gravitational
    'G': 6.67430e-11,       # Gravitational constant (SI)
    'c': 299792458,         # Speed of light (m/s)

    # Planck units (dimensionless combinations)
    'l_P/l_H': 1.6e-61,     # Planck length / Hubble length

    # Other
    'e': 2.71828,           # Euler's number
}

# =============================================================================
# DERIVED RATIOS
# =============================================================================

print("=" * 80)
print("COMPUTING ALL RATIOS AND COMBINATIONS")
print("=" * 80)

# Combine all parameters
ALL_PARAMS = {**COSMO_PARAMS, **PHYSICS}

# Store matches
matches = []

def check_match(name, value, threshold=0.02):
    """Check if value matches any target within threshold (2% default)"""
    if value is None or np.isnan(value) or np.isinf(value) or value == 0:
        return

    for target_name, target_val in TARGETS.items():
        if target_val == 0:
            continue

        # Check both value and 1/value
        for v, label in [(value, name), (1/value, f"1/({name})")]:
            if v <= 0 or np.isinf(v):
                continue

            ratio = v / target_val
            error = abs(ratio - 1)

            if error < threshold:
                matches.append({
                    'formula': label,
                    'value': v,
                    'target': target_name,
                    'target_val': target_val,
                    'error': error * 100,
                })

# =============================================================================
# SEARCH 1: Simple ratios of cosmological parameters
# =============================================================================

print("\n--- Simple Ratios ---")

cosmo_keys = list(COSMO_PARAMS.keys())
for i, k1 in enumerate(cosmo_keys):
    for k2 in cosmo_keys[i+1:]:
        v1, v2 = COSMO_PARAMS[k1], COSMO_PARAMS[k2]
        if v2 != 0:
            ratio = v1 / v2
            check_match(f"{k1}/{k2}", ratio)
            check_match(f"{k2}/{k1}", v2/v1)

# =============================================================================
# SEARCH 2: Combinations with π
# =============================================================================

print("\n--- Combinations with π ---")

for k, v in COSMO_PARAMS.items():
    check_match(f"{k} × π", v * np.pi)
    check_match(f"{k} / π", v / np.pi)
    check_match(f"{k} × 2π", v * 2 * np.pi)
    check_match(f"{k} × 4π", v * 4 * np.pi)
    check_match(f"√({k})", np.sqrt(abs(v)) if v > 0 else None)
    check_match(f"√({k} × π)", np.sqrt(abs(v * np.pi)) if v > 0 else None)

# =============================================================================
# SEARCH 3: Products of two parameters
# =============================================================================

print("\n--- Products of Two Parameters ---")

for i, k1 in enumerate(cosmo_keys):
    for k2 in cosmo_keys[i+1:]:
        v1, v2 = COSMO_PARAMS[k1], COSMO_PARAMS[k2]
        prod = v1 * v2
        check_match(f"{k1} × {k2}", prod)

# =============================================================================
# SEARCH 4: (1 - x) and (1 + x) combinations
# =============================================================================

print("\n--- (1 ± x) Combinations ---")

for k, v in COSMO_PARAMS.items():
    if 0 < v < 2:  # Only for values near 1
        check_match(f"1 - {k}", 1 - v)
        check_match(f"1 + {k}", 1 + v)
        check_match(f"1/(1 + {k})", 1 / (1 + v))
        check_match(f"1/(1 - {k})", 1 / (1 - v) if v != 1 else None)

# =============================================================================
# SEARCH 5: Power combinations
# =============================================================================

print("\n--- Power Combinations ---")

for k, v in COSMO_PARAMS.items():
    if v > 0:
        for power in [2, 3, 0.5, 1/3, -1, -0.5]:
            check_match(f"({k})^{power}", v ** power)

# =============================================================================
# SEARCH 6: Three-parameter combinations
# =============================================================================

print("\n--- Three-Parameter Combinations (selected) ---")

# Focus on density parameters
density_keys = ['Ω_m', 'Ω_Λ', 'Ω_b', 'Ω_c']
for k1, k2, k3 in combinations(density_keys, 3):
    v1, v2, v3 = COSMO_PARAMS[k1], COSMO_PARAMS[k2], COSMO_PARAMS[k3]

    # Various combinations
    check_match(f"({k1} + {k2})/{k3}", (v1 + v2) / v3 if v3 != 0 else None)
    check_match(f"{k1}/({k2} + {k3})", v1 / (v2 + v3) if (v2+v3) != 0 else None)
    check_match(f"({k1} × {k2})/{k3}", (v1 * v2) / v3 if v3 != 0 else None)

# =============================================================================
# SEARCH 7: Special combinations found in literature
# =============================================================================

print("\n--- Special Combinations ---")

# H₀ × t₀ (dimensionless age)
H0_per_sec = COSMO_PARAMS['H₀'] * 1000 / 3.086e22  # Convert to 1/s
t0_sec = COSMO_PARAMS['t_0'] * 1e9 * 3.156e7  # Convert to seconds
check_match("H₀ × t₀", H0_per_sec * t0_sec)

# Coincidence: Ω_c/Ω_b
check_match("Ω_c/Ω_b (CDM/baryon)", COSMO_PARAMS['Ω_c'] / COSMO_PARAMS['Ω_b'])

# σ₈ relationships
check_match("σ₈ × π", COSMO_PARAMS['σ_8'] * np.pi)
check_match("σ₈ × 2π", COSMO_PARAMS['σ_8'] * 2 * np.pi)
check_match("σ₈ × √(8π/3)", COSMO_PARAMS['σ_8'] * np.sqrt(8*np.pi/3))

# n_s relationships
check_match("1/(1 - n_s)", 1 / (1 - COSMO_PARAMS['n_s']))
check_match("n_s × π", COSMO_PARAMS['n_s'] * np.pi)

# A_s relationships
As_scaled = COSMO_PARAMS['A_s'] * 1e9  # Scale to ~2.1
check_match("A_s × 10^9", As_scaled)
check_match("ln(A_s × 10^10)", np.log(COSMO_PARAMS['A_s'] * 1e10))

# Redshift combinations
check_match("ln(1 + z_*)", np.log(1 + COSMO_PARAMS['z_*']))
check_match("ln(1 + z_eq)", np.log(1 + COSMO_PARAMS['z_eq']))
check_match("z_*/z_eq", COSMO_PARAMS['z_*'] / COSMO_PARAMS['z_eq'])

# τ combinations
check_match("τ × 2√(8π/3)", COSMO_PARAMS['τ'] * 2 * np.sqrt(8*np.pi/3))
check_match("1/τ", 1 / COSMO_PARAMS['τ'])

# =============================================================================
# SEARCH 8: Cross-combinations with fundamental physics
# =============================================================================

print("\n--- Cross Physics-Cosmology Combinations ---")

# Fine structure constant combinations
check_match("α × Ω_m × 1000", PHYSICS['α'] * COSMO_PARAMS['Ω_m'] * 1000)
check_match("α × 137 × π / Ω_m", PHYSICS['α'] * 137 * np.pi / COSMO_PARAMS['Ω_m'])

# =============================================================================
# SEARCH 9: Looking for 8π/3 directly
# =============================================================================

print("\n--- Direct 8π/3 Search ---")

# Is there any parameter X such that X × (something simple) = 8π/3?
target_8pi3 = 8 * np.pi / 3

for k, v in COSMO_PARAMS.items():
    if v > 0:
        multiplier = target_8pi3 / v
        # Check if multiplier is a simple number
        for simple in [1, 2, 3, 4, 6, 8, 10, 12, np.pi, 2*np.pi, 4*np.pi]:
            if abs(multiplier / simple - 1) < 0.02:
                print(f"  FOUND: {k} × {simple:.4f} ≈ 8π/3")

# =============================================================================
# SEARCH 10: Density parameter algebra
# =============================================================================

print("\n--- Density Algebra ---")

Om, OL, Ob, Oc = COSMO_PARAMS['Ω_m'], COSMO_PARAMS['Ω_Λ'], COSMO_PARAMS['Ω_b'], COSMO_PARAMS['Ω_c']

# Various density combinations
combinations_to_check = {
    'Ω_Λ/Ω_m': OL/Om,
    'Ω_m/Ω_b': Om/Ob,
    'Ω_Λ/Ω_b': OL/Ob,
    'Ω_c/Ω_b': Oc/Ob,
    '(Ω_Λ - Ω_m)/Ω_m': (OL - Om)/Om,
    '(Ω_Λ + Ω_m)/Ω_b': (OL + Om)/Ob,
    'Ω_Λ × Ω_m': OL * Om,
    'Ω_Λ - Ω_m': OL - Om,
    'Ω_Λ² / Ω_m': OL**2 / Om,
    'Ω_m² / Ω_b': Om**2 / Ob,
    'ln(Ω_Λ/Ω_m)': np.log(OL/Om),
    'Ω_c / (Ω_b × π)': Oc / (Ob * np.pi),
    '(Ω_c - Ω_b)/Ω_b': (Oc - Ob)/Ob,
}

for name, val in combinations_to_check.items():
    check_match(name, val)

# =============================================================================
# RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("TOP MATCHES (sorted by error)")
print("=" * 80)

# Sort by error
matches_sorted = sorted(matches, key=lambda x: x['error'])

# Remove duplicates (same value matching same target)
seen = set()
unique_matches = []
for m in matches_sorted:
    key = (round(m['value'], 6), m['target'])
    if key not in seen:
        seen.add(key)
        unique_matches.append(m)

# Print top matches
print(f"\n{'Formula':<40} {'Value':>12} {'Target':>15} {'Error':>8}")
print("-" * 80)

for m in unique_matches[:30]:
    print(f"{m['formula']:<40} {m['value']:>12.6f} {m['target']:>15} {m['error']:>7.3f}%")

# =============================================================================
# HIGHLIGHT BEST CANDIDATES
# =============================================================================

print("\n" + "=" * 80)
print("BEST CANDIDATES FOR THIRD RELATIONSHIP (error < 1%)")
print("=" * 80)

best = [m for m in unique_matches if m['error'] < 1.0]
for m in best:
    print(f"\n  ★ {m['formula']}")
    print(f"    Value: {m['value']:.6f}")
    print(f"    Target: {m['target']} = {m['target_val']:.6f}")
    print(f"    Error: {m['error']:.4f}%")

if not best:
    print("\n  No matches found with error < 1%")
    print("  Showing best matches with error < 2%:")
    for m in [m for m in unique_matches if m['error'] < 2.0][:5]:
        print(f"\n  {m['formula']}")
        print(f"    Value: {m['value']:.6f}")
        print(f"    Target: {m['target']} = {m['target_val']:.6f}")
        print(f"    Error: {m['error']:.4f}%")

# =============================================================================
# ALREADY KNOWN RELATIONSHIPS (for reference)
# =============================================================================

print("\n" + "=" * 80)
print("KNOWN RELATIONSHIPS (confirmed)")
print("=" * 80)

print(f"""
1. MOND Acceleration Scale:
   a₀ = cH₀/(2√(8π/3)) = cH₀/5.7888
   Target: 2√(8π/3) = {2*np.sqrt(8*np.pi/3):.6f}

2. Dark Energy Ratio:
   Ω_Λ/Ω_m = √(3π/2) = 4π/(2√(8π/3))
   Observed: {OL/Om:.6f}
   Target: √(3π/2) = {np.sqrt(3*np.pi/2):.6f}
   Error: {abs(OL/Om - np.sqrt(3*np.pi/2))/np.sqrt(3*np.pi/2)*100:.4f}%
""")
