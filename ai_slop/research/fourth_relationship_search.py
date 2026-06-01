#!/usr/bin/env python3
"""
Search for FOURTH Relationship Involving 2√(8π/3)

We have THREE confirmed relationships:
1. a₀ = cH₀/(2√(8π/3))     - MOND acceleration
2. Ω_Λ/Ω_m = 4π/(2√(8π/3)) - dark energy ratio
3. τ = Ω_m/(2√(8π/3))      - optical depth

Now searching for a FOURTH.
"""

import numpy as np
from itertools import combinations, product
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# TARGET VALUES
# =============================================================================

Z = 2 * np.sqrt(8 * np.pi / 3)  # Zimmerman constant = 5.7888

TARGETS = {
    '2√(8π/3)': Z,
    '√(8π/3)': np.sqrt(8 * np.pi / 3),
    '8π/3': 8 * np.pi / 3,
    '√(3π/2)': np.sqrt(3 * np.pi / 2),
    '3π/2': 3 * np.pi / 2,
    '4π': 4 * np.pi,
    '1/(2√(8π/3))': 1 / Z,
    '2π': 2 * np.pi,
    'π': np.pi,
    '√(2π)': np.sqrt(2 * np.pi),
    '4π/3': 4 * np.pi / 3,
    '√π': np.sqrt(np.pi),
}

print("=" * 80)
print("SEARCHING FOR FOURTH RELATIONSHIP")
print("=" * 80)
print(f"\nZimmerman constant: 2√(8π/3) = {Z:.6f}")
print(f"Already found: a₀, Ω_Λ/Ω_m, τ")
print()

# =============================================================================
# EXPANDED PARAMETER SET
# =============================================================================

# Planck 2018 + other cosmological data
PARAMS = {
    # Density parameters
    'Ω_m': 0.3153,
    'Ω_Λ': 0.6847,
    'Ω_b': 0.0493,
    'Ω_c': 0.2607,
    'Ω_r': 9.15e-5,
    'Ω_γ': 5.38e-5,
    'Ω_ν': 3.77e-5,

    # Hubble
    'H₀': 67.36,
    'h': 0.6736,
    '100h': 67.36,

    # CMB
    'T_CMB': 2.7255,
    'z_*': 1089.80,
    'z_eq': 3402,
    'z_re': 7.67,
    'θ_*': 1.04110e-2,  # Angular size of sound horizon
    'r_*': 144.43,       # Comoving sound horizon at z_* (Mpc)

    # Primordial
    'A_s': 2.101e-9,
    'ln(10^10 A_s)': 3.044,
    'n_s': 0.9649,
    '1-n_s': 0.0351,
    'r_tensor': 0.06,
    'τ': 0.0544,

    # Structure
    'σ_8': 0.8111,
    'S_8': 0.832,

    # Age and distances
    't_0': 13.797,        # Age in Gyr
    'r_H': 4222,          # Hubble radius in Mpc (c/H₀)

    # Baryon physics
    'η_b': 6.12e-10,      # Baryon-to-photon ratio
    'Y_p': 0.2454,        # Primordial helium fraction
    'Ω_b*h²': 0.02237,
    'Ω_c*h²': 0.1200,
    'Ω_m*h²': 0.1424,

    # Neutrinos
    'N_eff': 3.046,
    'Σm_ν': 0.06,         # Sum of neutrino masses (eV)

    # Dark energy
    'w_0': -1.0,
    'w_a': 0.0,

    # Growth
    'f_σ8': 0.471,        # Growth rate × σ_8

    # BAO scale
    'r_drag': 147.09,     # Sound horizon at drag epoch (Mpc)
}

# Add some derived quantities
PARAMS['Ω_Λ/Ω_m'] = PARAMS['Ω_Λ'] / PARAMS['Ω_m']
PARAMS['Ω_c/Ω_b'] = PARAMS['Ω_c'] / PARAMS['Ω_b']
PARAMS['Ω_m/τ'] = PARAMS['Ω_m'] / PARAMS['τ']
PARAMS['Ω_Λ/τ'] = PARAMS['Ω_Λ'] / PARAMS['τ']

# Store matches
matches = []

def check_match(name, value, threshold=0.015):
    """Check if value matches any target within threshold (1.5% default)"""
    if value is None or not np.isfinite(value) or value == 0:
        return

    for target_name, target_val in TARGETS.items():
        if target_val == 0:
            continue

        # Check both value and 1/value
        for v, label in [(value, name), (1/value, f"1/({name})")]:
            if not np.isfinite(v) or v <= 0:
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
# SEARCH STRATEGIES
# =============================================================================

print("Running comprehensive search...\n")

# Strategy 1: All single parameters
print("Strategy 1: Single parameters...")
for name, val in PARAMS.items():
    check_match(name, val)
    if val > 0:
        check_match(f"√({name})", np.sqrt(val))
        check_match(f"({name})²", val**2)
        check_match(f"ln({name})", np.log(val) if val > 0 else None)

# Strategy 2: All pairwise ratios
print("Strategy 2: Pairwise ratios...")
keys = list(PARAMS.keys())
for i, k1 in enumerate(keys):
    for k2 in keys[i+1:]:
        v1, v2 = PARAMS[k1], PARAMS[k2]
        if v2 != 0:
            check_match(f"{k1}/{k2}", v1/v2)
        if v1 != 0:
            check_match(f"{k2}/{k1}", v2/v1)

# Strategy 3: Products
print("Strategy 3: Products...")
for i, k1 in enumerate(keys):
    for k2 in keys[i+1:]:
        v1, v2 = PARAMS[k1], PARAMS[k2]
        check_match(f"{k1} × {k2}", v1 * v2)

# Strategy 4: Combinations with π
print("Strategy 4: π combinations...")
for name, val in PARAMS.items():
    for mult in [np.pi, 2*np.pi, 4*np.pi, np.pi/2, np.pi/3, np.pi/4]:
        mult_name = {np.pi: 'π', 2*np.pi: '2π', 4*np.pi: '4π',
                     np.pi/2: 'π/2', np.pi/3: 'π/3', np.pi/4: 'π/4'}[mult]
        check_match(f"{name} × {mult_name}", val * mult)
        if val != 0:
            check_match(f"{mult_name} / {name}", mult / val)

# Strategy 5: (1 ± x) combinations
print("Strategy 5: (1 ± x) combinations...")
for name, val in PARAMS.items():
    if -2 < val < 2:
        check_match(f"1 + {name}", 1 + val)
        check_match(f"1 - {name}", 1 - val)
        if val != 1 and (1 - val) != 0:
            check_match(f"1/(1 - {name})", 1/(1-val))
        if (1 + val) != 0:
            check_match(f"1/(1 + {name})", 1/(1+val))

# Strategy 6: Three-parameter combinations (selected important ones)
print("Strategy 6: Three-parameter combinations...")
important = ['Ω_m', 'Ω_Λ', 'Ω_b', 'Ω_c', 'h', 'τ', 'σ_8', 'n_s']
for k1, k2, k3 in combinations(important, 3):
    v1, v2, v3 = PARAMS[k1], PARAMS[k2], PARAMS[k3]
    if v3 != 0:
        check_match(f"({k1}+{k2})/{k3}", (v1+v2)/v3)
        check_match(f"({k1}×{k2})/{k3}", (v1*v2)/v3)
    if v2 + v3 != 0:
        check_match(f"{k1}/({k2}+{k3})", v1/(v2+v3))

# Strategy 7: Logarithmic combinations
print("Strategy 7: Logarithmic combinations...")
for name, val in PARAMS.items():
    if val > 0:
        check_match(f"ln({name})", np.log(val))
        check_match(f"log₁₀({name})", np.log10(val))
        check_match(f"exp({name})", np.exp(val) if val < 100 else None)

# Strategy 8: Redshift-related
print("Strategy 8: Redshift combinations...")
check_match("ln(1+z_*)", np.log(1 + PARAMS['z_*']))
check_match("ln(1+z_eq)", np.log(1 + PARAMS['z_eq']))
check_match("ln(1+z_re)", np.log(1 + PARAMS['z_re']))
check_match("z_*/z_eq", PARAMS['z_*'] / PARAMS['z_eq'])
check_match("z_eq/z_*", PARAMS['z_eq'] / PARAMS['z_*'])
check_match("(1+z_eq)/(1+z_*)", (1+PARAMS['z_eq']) / (1+PARAMS['z_*']))

# Strategy 9: Physical constants in dimensionless combinations
print("Strategy 9: Special physics combinations...")
# H₀ × t₀ (dimensionless)
H0_per_Gyr = PARAMS['H₀'] * 1.0227  # Convert km/s/Mpc to 1/Gyr
check_match("H₀ × t₀", H0_per_Gyr * PARAMS['t_0'])

# CMB temperature related
check_match("T_CMB × ln(1+z_*)", PARAMS['T_CMB'] * np.log(1 + PARAMS['z_*']))
check_match("T_CMB × h", PARAMS['T_CMB'] * PARAMS['h'])

# Strategy 10: Powers of h
print("Strategy 10: Powers of h...")
for power in [0.5, 1, 1.5, 2, 2.5, 3]:
    check_match(f"h^{power}", PARAMS['h']**power)
    check_match(f"1/h^{power}", 1/PARAMS['h']**power)

# Strategy 11: Ω combinations with powers
print("Strategy 11: Ω power combinations...")
for name in ['Ω_m', 'Ω_Λ', 'Ω_b', 'Ω_c']:
    val = PARAMS[name]
    for p in [0.5, 2, 3, -1, -0.5]:
        check_match(f"({name})^{p}", val**p)

# Strategy 12: σ_8 and n_s combinations
print("Strategy 12: Structure parameters...")
check_match("σ_8 × n_s", PARAMS['σ_8'] * PARAMS['n_s'])
check_match("σ_8 / n_s", PARAMS['σ_8'] / PARAMS['n_s'])
check_match("σ_8 / (1-n_s)", PARAMS['σ_8'] / PARAMS['1-n_s'])
check_match("σ_8 × (1-n_s)", PARAMS['σ_8'] * PARAMS['1-n_s'])
check_match("S_8 / σ_8", PARAMS['S_8'] / PARAMS['σ_8'])

# Strategy 13: Baryon-related
print("Strategy 13: Baryon combinations...")
check_match("Ω_b × h² × 100", PARAMS['Ω_b*h²'] * 100)
check_match("Ω_c × h² × 10", PARAMS['Ω_c*h²'] * 10)
check_match("Ω_m × h² × 10", PARAMS['Ω_m*h²'] * 10)
check_match("Y_p × 4π", PARAMS['Y_p'] * 4 * np.pi)
check_match("1/Y_p", 1/PARAMS['Y_p'])

# Strategy 14: Sound horizon related
print("Strategy 14: BAO/sound horizon...")
check_match("r_drag / r_*", PARAMS['r_drag'] / PARAMS['r_*'])
check_match("r_* / 100", PARAMS['r_*'] / 100)
check_match("r_drag / 100", PARAMS['r_drag'] / 100)
check_match("θ_* × 100", PARAMS['θ_*'] * 100)

# Strategy 15: N_eff combinations
print("Strategy 15: Neutrino combinations...")
check_match("N_eff", PARAMS['N_eff'])
check_match("N_eff - 3", PARAMS['N_eff'] - 3)
check_match("N_eff / π", PARAMS['N_eff'] / np.pi)

# =============================================================================
# FILTER AND SORT RESULTS
# =============================================================================

# Remove duplicates
seen = set()
unique = []
for m in matches:
    key = (round(m['value'], 5), m['target'])
    if key not in seen:
        seen.add(key)
        unique.append(m)

# Sort by error
unique.sort(key=lambda x: x['error'])

# Remove already-known relationships
known_formulas = [
    'Ω_Λ/Ω_m', '1/(Ω_m/Ω_Λ)',  # Relationship 2
    'Ω_m/τ', '1/(τ/Ω_m)',       # Relationship 3
    'Ω_Λ/τ',                     # Derived from 2+3
]

new_matches = [m for m in unique if not any(k in m['formula'] for k in known_formulas)]

# =============================================================================
# RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("TOP NEW CANDIDATES FOR FOURTH RELATIONSHIP (excluding known)")
print("=" * 80)

print(f"\n{'Formula':<45} {'Value':>12} {'Target':>15} {'Error':>8}")
print("-" * 85)

for m in new_matches[:40]:
    print(f"{m['formula']:<45} {m['value']:>12.6f} {m['target']:>15} {m['error']:>7.4f}%")

# =============================================================================
# HIGHLIGHT BEST NEW CANDIDATES
# =============================================================================

print("\n" + "=" * 80)
print("BEST NEW CANDIDATES (error < 0.5%)")
print("=" * 80)

best = [m for m in new_matches if m['error'] < 0.5]

if best:
    for m in best:
        print(f"\n  ★ {m['formula']}")
        print(f"    Value: {m['value']:.6f}")
        print(f"    Target: {m['target']} = {m['target_val']:.6f}")
        print(f"    Error: {m['error']:.4f}%")
else:
    print("\n  No candidates with error < 0.5%")
    print("  Showing best with error < 1%:")
    for m in [m for m in new_matches if m['error'] < 1.0][:10]:
        print(f"\n  {m['formula']}")
        print(f"    Value: {m['value']:.6f}")
        print(f"    Target: {m['target']} = {m['target_val']:.6f}")
        print(f"    Error: {m['error']:.4f}%")

# =============================================================================
# SPECIFIC INTERESTING CHECKS
# =============================================================================

print("\n" + "=" * 80)
print("SPECIFIC INTERESTING COMBINATIONS")
print("=" * 80)

# Check if n_s has any relationship
print(f"\nn_s = {PARAMS['n_s']}")
print(f"1 - n_s = {PARAMS['1-n_s']}")
print(f"1/(1-n_s) = {1/PARAMS['1-n_s']:.4f}")
print(f"π × (1-n_s) = {np.pi * PARAMS['1-n_s']:.6f}")
print(f"Target 1/(2√(8π/3)) = {1/Z:.6f}")

# Check σ_8
print(f"\nσ_8 = {PARAMS['σ_8']}")
print(f"σ_8 × 2√(8π/3) = {PARAMS['σ_8'] * Z:.4f}")
print(f"σ_8 × π = {PARAMS['σ_8'] * np.pi:.6f}")
print(f"Target √(8π/3) = {np.sqrt(8*np.pi/3):.6f}")

# Check H₀ × t₀
H0t0 = H0_per_Gyr * PARAMS['t_0']
print(f"\nH₀ × t₀ = {H0t0:.6f}")
print(f"Target 2π/3 = {2*np.pi/3:.6f}")
print(f"Error: {abs(H0t0 - 2*np.pi/3)/(2*np.pi/3)*100:.2f}%")

# Check ln(1 + z_*)
lnz = np.log(1 + PARAMS['z_*'])
print(f"\nln(1 + z_*) = ln(1 + {PARAMS['z_*']}) = {lnz:.6f}")
print(f"Target 2√(8π/3) + 1 = {Z + 1:.6f}")
print(f"Error: {abs(lnz - (Z+1))/(Z+1)*100:.2f}%")

# Check Ω_b relationships
print(f"\nΩ_b = {PARAMS['Ω_b']}")
print(f"Ω_b × 2√(8π/3) = {PARAMS['Ω_b'] * Z:.6f}")
print(f"1/(Ω_b × 2√(8π/3)) = {1/(PARAMS['Ω_b'] * Z):.6f}")
print(f"Target √(3π/2) = {np.sqrt(3*np.pi/2):.6f}")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print("""
CONFIRMED RELATIONSHIPS (already found):
1. a₀ = cH₀/(2√(8π/3))           [0.8% error]
2. Ω_Λ/Ω_m = √(3π/2)             [0.04% error]
3. τ = Ω_m/(2√(8π/3))            [0.12% error]

STRONGEST NEW CANDIDATES:
""")

for i, m in enumerate(new_matches[:5], 1):
    print(f"{i}. {m['formula']} = {m['target']} ({m['error']:.3f}% error)")
