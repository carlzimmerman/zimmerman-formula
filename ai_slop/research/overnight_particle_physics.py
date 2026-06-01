#!/usr/bin/env python3
"""
OVERNIGHT SEARCH: Particle Physics Connections

Can the Zimmerman constant connect to particle physics?
- Fine structure constant α
- Mass ratios
- Coupling constants
- Weinberg angle
"""

import numpy as np
from itertools import combinations
import time

print("=" * 80)
print("PARTICLE PHYSICS CONNECTION SEARCH")
print(f"Started: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)

Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888
sqrt_3pi2 = np.sqrt(3 * np.pi / 2)  # 2.1708

# =============================================================================
# PARTICLE PHYSICS CONSTANTS
# =============================================================================

PARTICLE = {
    # Electromagnetic
    'α': 1/137.035999084,        # Fine structure constant
    '1/α': 137.035999084,

    # Weak
    'sin²θ_W': 0.23122,          # Weinberg angle
    'G_F': 1.1663787e-5,         # Fermi constant (GeV^-2)

    # Strong
    'α_s(M_Z)': 0.1179,          # Strong coupling at Z mass

    # Masses (in MeV)
    'm_e': 0.511,
    'm_μ': 105.66,
    'm_τ': 1776.86,
    'm_u': 2.16,
    'm_d': 4.67,
    'm_s': 93.4,
    'm_c': 1270,
    'm_b': 4180,
    'm_t': 172760,
    'm_W': 80379,
    'm_Z': 91187.6,
    'm_H': 125100,

    # Mass ratios
    'm_p/m_e': 1836.15267343,
    'm_n/m_p': 1.00137842,
    'm_μ/m_e': 206.7682830,
    'm_τ/m_μ': 16.8167,
    'm_t/m_b': 41.33,
    'm_W/m_Z': 0.8815,

    # Cabibbo angle
    'sin_θ_C': 0.22500,
    'cos_θ_C': 0.97437,

    # CKM matrix elements
    'V_ud': 0.97370,
    'V_us': 0.2245,
    'V_ub': 0.00382,
    'V_cb': 0.0410,
}

# Cosmological for comparison
COSMO = {
    'Ω_m': 0.3153,
    'Ω_Λ': 0.6847,
    'Ω_b': 0.0493,
    'h': 0.6736,
    'τ': 0.0544,
    'n_s': 0.9649,
    'T_CMB': 2.7255,
    'N_eff': 3.046,
}

TARGETS = {
    'Z': Z,
    '√(3π/2)': sqrt_3pi2,
    'π': np.pi,
    '2π': 2*np.pi,
    '4π': 4*np.pi,
    '1/Z': 1/Z,
    '√π': np.sqrt(np.pi),
    'e': np.e,
}

print(f"\nSearching {len(PARTICLE)} particle physics constants...")
print(f"Targets: {list(TARGETS.keys())}")

matches = []

# =============================================================================
# SEARCH
# =============================================================================

def check(name, val, threshold=0.01):
    if not np.isfinite(val) or val == 0:
        return
    for tname, tval in TARGETS.items():
        for v, label in [(val, name), (1/val, f"1/({name})")]:
            if v > 0 and np.isfinite(v):
                err = abs(v/tval - 1)
                if err < threshold:
                    matches.append((label, v, tname, err*100))

# Single constants
print("\n--- Single Constants ---")
for name, val in PARTICLE.items():
    check(name, val)
    if val > 0:
        check(f"√({name})", np.sqrt(val))
        check(f"ln({name})", np.log(val))

# Products of two
print("--- Products ---")
keys = list(PARTICLE.keys())
for k1, k2 in combinations(keys, 2):
    v1, v2 = PARTICLE[k1], PARTICLE[k2]
    check(f"{k1}×{k2}", v1*v2)

# Ratios
print("--- Ratios ---")
for k1 in keys:
    for k2 in keys:
        if k1 != k2 and PARTICLE[k2] != 0:
            check(f"{k1}/{k2}", PARTICLE[k1]/PARTICLE[k2])

# With π
print("--- π Combinations ---")
for name, val in PARTICLE.items():
    check(f"{name}×π", val * np.pi)
    check(f"{name}×2π", val * 2 * np.pi)

# Cross with cosmological
print("--- Cross Cosmo-Particle ---")
for pk, pv in PARTICLE.items():
    for ck, cv in COSMO.items():
        if cv != 0:
            check(f"{pk}/{ck}", pv/cv)
            check(f"{pk}×{ck}", pv*cv)

# =============================================================================
# RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("RESULTS")
print("=" * 80)

# Sort and dedupe
matches.sort(key=lambda x: x[3])
seen = set()
unique = []
for m in matches:
    key = (round(m[1], 6), m[2])
    if key not in seen:
        seen.add(key)
        unique.append(m)

print(f"\n{'Formula':<40} {'Value':>12} {'Target':>12} {'Error':>8}")
print("-" * 75)
for m in unique[:30]:
    print(f"{m[0]:<40} {m[1]:>12.6f} {m[2]:>12} {m[3]:>7.3f}%")

# Best matches
print("\n" + "=" * 80)
print("BEST MATCHES (error < 0.5%)")
print("=" * 80)

best = [m for m in unique if m[3] < 0.5]
if best:
    for m in best:
        print(f"\n  * {m[0]}")
        print(f"    = {m[1]:.6f} ≈ {m[2]} ({m[3]:.3f}%)")
else:
    print("\n  No matches < 0.5%")
    print("  Best matches:")
    for m in unique[:5]:
        print(f"    {m[0]} = {m[1]:.6f} ≈ {m[2]} ({m[3]:.3f}%)")

# =============================================================================
# SPECIAL CHECKS
# =============================================================================

print("\n" + "=" * 80)
print("SPECIAL CHECKS")
print("=" * 80)

# α and Z
print(f"\nFine structure constant:")
print(f"  α = {PARTICLE['α']:.8f}")
print(f"  1/α = {PARTICLE['1/α']:.4f}")
print(f"  1/α / Z = {PARTICLE['1/α']/Z:.4f}")
print(f"  Z × α × 100 = {Z * PARTICLE['α'] * 100:.4f}")

# Weinberg angle
print(f"\nWeinberg angle:")
print(f"  sin²θ_W = {PARTICLE['sin²θ_W']:.5f}")
print(f"  sin²θ_W × 4π = {PARTICLE['sin²θ_W'] * 4 * np.pi:.5f}")
print(f"  Target √(3π/2) = {sqrt_3pi2:.5f}")

# Proton/electron mass ratio
print(f"\nMass ratios:")
print(f"  m_p/m_e = {PARTICLE['m_p/m_e']:.4f}")
print(f"  m_p/m_e / 1/α = {PARTICLE['m_p/m_e']/PARTICLE['1/α']:.4f}")
print(f"  Target 4π / Z = {4*np.pi/Z:.4f}")

print(f"\n" + "=" * 80)
print(f"Completed: {time.strftime('%Y-%m-%d %H:%M:%S')}")
print("=" * 80)
