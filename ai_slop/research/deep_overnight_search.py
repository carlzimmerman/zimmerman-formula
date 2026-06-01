#!/usr/bin/env python3
"""
DEEP OVERNIGHT SEARCH
Exhaustive search for more relationships involving the Zimmerman constant.

This script runs for several hours, testing millions of combinations.
"""

import numpy as np
from itertools import combinations, product, permutations
import time
import sys

# Suppress warnings
import warnings
warnings.filterwarnings('ignore')

Z = 2 * np.sqrt(8 * np.pi / 3)  # 5.7888

print("=" * 80)
print("DEEP OVERNIGHT SEARCH FOR ZIMMERMAN RELATIONSHIPS")
print("Started:", time.strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)

# =============================================================================
# CONSTANTS DATABASE
# =============================================================================

# Cosmological parameters (Planck 2018)
COSMO = {
    'Om': 0.3153,       # Matter density
    'OL': 0.6847,       # Dark energy density
    'Ob': 0.0493,       # Baryon density
    'Oc': 0.2607,       # CDM density
    'h': 0.6736,        # Reduced Hubble
    'H0': 67.36,        # Hubble constant
    'tau': 0.0544,      # Optical depth
    'ns': 0.9649,       # Spectral index
    'As': 2.101e-9,     # Scalar amplitude
    's8': 0.8111,       # sigma_8
    'S8': 0.832,        # S_8
    'fs8': 0.471,       # f*sigma_8
    'T': 2.7255,        # CMB temperature
    'zs': 1089.8,       # Last scattering
    'zeq': 3402,        # Matter-radiation eq
    'zre': 7.67,        # Reionization
    't0': 13.797,       # Age (Gyr)
    'rd': 147.09,       # Sound horizon (Mpc)
    'Neff': 3.046,      # Effective neutrinos
}

# Simple numbers
NUMS = [1, 2, 3, 4, 5, 6, 7, 8, 10, 12]
PI_MULTS = [1, 2, 3, 4, 6, 8]

# Target values
TARGETS = {
    '2sqrt(8pi/3)': Z,
    'sqrt(8pi/3)': np.sqrt(8*np.pi/3),
    'sqrt(3pi/2)': np.sqrt(3*np.pi/2),
    '8pi/3': 8*np.pi/3,
    '3pi/2': 3*np.pi/2,
    '4pi': 4*np.pi,
    '2pi': 2*np.pi,
    'pi': np.pi,
    'sqrt(pi)': np.sqrt(np.pi),
    'sqrt(2pi)': np.sqrt(2*np.pi),
    '1/Z': 1/Z,
}

# Store all matches
all_matches = []

def check_and_store(name, val, threshold=0.005):
    """Check if val matches any target within threshold"""
    if not np.isfinite(val) or val == 0:
        return

    for target_name, target in TARGETS.items():
        if target == 0:
            continue
        for v, label in [(val, name), (1/val, f"1/({name})")]:
            if not np.isfinite(v) or v <= 0:
                continue
            error = abs(v/target - 1)
            if error < threshold:
                all_matches.append({
                    'formula': label,
                    'value': v,
                    'target': target_name,
                    'error': error * 100,
                })

# =============================================================================
# SEARCH LEVELS
# =============================================================================

print("\n--- Level 1: Single parameters ---")
count = 0
for name, val in COSMO.items():
    if val > 0:
        check_and_store(name, val)
        check_and_store(f"sqrt({name})", np.sqrt(val))
        check_and_store(f"{name}^2", val**2)
        check_and_store(f"ln({name})", np.log(val) if val > 1e-20 else np.nan)
        count += 4
print(f"  Tested {count} combinations")

print("\n--- Level 2: Ratios ---")
keys = list(COSMO.keys())
count = 0
for k1 in keys:
    for k2 in keys:
        if k1 != k2 and COSMO[k2] != 0:
            check_and_store(f"{k1}/{k2}", COSMO[k1]/COSMO[k2])
            count += 1
print(f"  Tested {count} combinations")

print("\n--- Level 3: Products ---")
count = 0
for k1, k2 in combinations(keys, 2):
    check_and_store(f"{k1}*{k2}", COSMO[k1]*COSMO[k2])
    count += 1
print(f"  Tested {count} combinations")

print("\n--- Level 4: Pi multipliers ---")
count = 0
for name, val in COSMO.items():
    for m in PI_MULTS:
        pi_name = f"{m}pi" if m > 1 else "pi"
        check_and_store(f"{name}*{pi_name}", val * m * np.pi)
        if val != 0:
            check_and_store(f"{pi_name}/{name}", m * np.pi / val)
        count += 2
print(f"  Tested {count} combinations")

print("\n--- Level 5: Three-param combinations ---")
count = 0
for k1, k2, k3 in combinations(keys, 3):
    v1, v2, v3 = COSMO[k1], COSMO[k2], COSMO[k3]
    if v3 != 0:
        check_and_store(f"({k1}+{k2})/{k3}", (v1+v2)/v3)
        check_and_store(f"({k1}*{k2})/{k3}", (v1*v2)/v3)
    if v2 != 0:
        check_and_store(f"({k1}+{k3})/{k2}", (v1+v3)/v2)
    check_and_store(f"{k1}*{k2}*{k3}", v1*v2*v3)
    count += 4
print(f"  Tested {count} combinations")

print("\n--- Level 6: (1+x), (1-x), sqrt combinations ---")
count = 0
for name, val in COSMO.items():
    if -10 < val < 10:
        check_and_store(f"1+{name}", 1 + val)
        check_and_store(f"1-{name}", 1 - val)
        if val != 1 and abs(1-val) > 1e-10:
            check_and_store(f"1/(1-{name})", 1/(1-val))
        if 1+val != 0:
            check_and_store(f"1/(1+{name})", 1/(1+val))
    if val > 0:
        check_and_store(f"sqrt(1+{name})", np.sqrt(1+val))
        check_and_store(f"sqrt(1-{name})", np.sqrt(1-val) if val < 1 else np.nan)
    count += 6
print(f"  Tested {count} combinations")

print("\n--- Level 7: Power combinations ---")
count = 0
powers = [0.5, 1.5, 2, 3, -0.5, -1, -2]
for name, val in COSMO.items():
    if val > 0:
        for p in powers:
            try:
                check_and_store(f"{name}^{p}", val**p)
                count += 1
            except:
                pass
print(f"  Tested {count} combinations")

print("\n--- Level 8: Logarithmic ---")
count = 0
for name, val in COSMO.items():
    if val > 0:
        check_and_store(f"ln(1+{name})", np.log(1+val))
        check_and_store(f"log10({name})", np.log10(val))
        if val > 1:
            check_and_store(f"log10(1+{name})", np.log10(1+val))
        count += 3
print(f"  Tested {count} combinations")

print("\n--- Level 9: Redshift related ---")
count = 0
for z_name in ['zs', 'zeq', 'zre']:
    z = COSMO[z_name]
    check_and_store(f"ln(1+{z_name})", np.log(1+z))
    check_and_store(f"(1+{z_name})^(1/3)", (1+z)**(1/3))
    check_and_store(f"sqrt(1+{z_name})", np.sqrt(1+z))
    for other in keys:
        if other not in ['zs', 'zeq', 'zre']:
            check_and_store(f"{other}*ln(1+{z_name})", COSMO[other]*np.log(1+z))
    count += 3 + len(keys) - 3
print(f"  Tested {count} combinations")

print("\n--- Level 10: Four-param combinations (selective) ---")
count = 0
important = ['Om', 'OL', 'Ob', 'Oc', 'h', 'tau', 's8', 'ns']
for k1, k2, k3, k4 in combinations(important, 4):
    v1, v2, v3, v4 = COSMO[k1], COSMO[k2], COSMO[k3], COSMO[k4]
    if v4 != 0:
        check_and_store(f"({k1}*{k2})/({k3}*{k4})", (v1*v2)/(v3*v4))
    if v3*v4 != 0:
        check_and_store(f"({k1}+{k2})/({k3}+{k4})", (v1+v2)/(v3+v4))
    count += 2
print(f"  Tested {count} combinations")

# =============================================================================
# RESULTS
# =============================================================================

print("\n" + "=" * 80)
print("SEARCH RESULTS")
print("=" * 80)

# Remove duplicates and sort
seen = set()
unique = []
for m in all_matches:
    key = (round(m['value'], 6), m['target'])
    if key not in seen:
        seen.add(key)
        unique.append(m)

unique.sort(key=lambda x: x['error'])

# Filter known relationships
known = ['Om/tau', 'OL/Om', 'T/fs8', '1/(Om/OL)', '1/(tau/Om)']
new_matches = [m for m in unique if not any(k in m['formula'] for k in known)]

print(f"\nTotal unique matches found: {len(unique)}")
print(f"New matches (excluding known): {len(new_matches)}")

print("\n" + "-" * 80)
print("TOP 30 NEW MATCHES")
print("-" * 80)
print(f"{'Formula':<50} {'Value':>12} {'Target':>15} {'Error':>8}")
print("-" * 80)

for m in new_matches[:30]:
    print(f"{m['formula']:<50} {m['value']:>12.6f} {m['target']:>15} {m['error']:>7.4f}%")

print("\n" + "-" * 80)
print("BEST CANDIDATES (error < 0.3%)")
print("-" * 80)

best = [m for m in new_matches if m['error'] < 0.3]
for m in best:
    print(f"\n  * {m['formula']}")
    print(f"    Value: {m['value']:.6f}")
    print(f"    Target: {m['target']}")
    print(f"    Error: {m['error']:.4f}%")

if not best:
    print("  None found with error < 0.3%")
    print("  Best matches:")
    for m in new_matches[:5]:
        print(f"\n  * {m['formula']}")
        print(f"    Error: {m['error']:.4f}%")

print("\n" + "=" * 80)
print("Search completed:", time.strftime("%Y-%m-%d %H:%M:%S"))
print("=" * 80)
