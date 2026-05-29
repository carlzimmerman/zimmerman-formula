#!/usr/bin/env python3
"""
================================================================================
INVESTIGATING Z² AND PACKING GEOMETRY
================================================================================

We found: 8π/Z² = 3/4 EXACTLY

And FCC packing efficiency is π/(3√2) ≈ 0.7405

The difference is only 1.3%. Is this meaningful?

Let's investigate whether Z² encodes packing geometry.

Author: Carl Zimmerman + Claude
License: AGPL-3.0-or-later
================================================================================
"""

import numpy as np
from scipy.optimize import minimize_scalar

# =============================================================================
# Z² DEFINITION AND PACKING RELATIONS
# =============================================================================

Z_SQUARED = 32 * np.pi / 3
Z_CONSTANT = 2 * np.sqrt(8 * np.pi / 3)

# Exact packing efficiencies
ETA_FCC = np.pi / (3 * np.sqrt(2))  # 0.7405
ETA_BCC = np.pi * np.sqrt(3) / 8    # 0.6802
ETA_SC = np.pi / 6                   # 0.5236

print("="*70)
print("Z² AND PACKING GEOMETRY INVESTIGATION")
print("="*70)

print(f"""
Z² = 32π/3 = {Z_SQUARED:.6f}
Z = 2√(8π/3) = {Z_CONSTANT:.6f}

EXACT RELATIONS:
  8π/Z² = 8π/(32π/3) = 3/4 = 0.75 EXACTLY

PACKING EFFICIENCIES:
  FCC: π/(3√2) = {ETA_FCC:.6f}
  BCC: π√3/8 = {ETA_BCC:.6f}
  SC:  π/6 = {ETA_SC:.6f}

COMPARISON:
  8π/Z² = 0.75
  FCC   = {ETA_FCC:.6f}
  Difference: {(0.75 - ETA_FCC)/ETA_FCC * 100:.2f}%
""")

# =============================================================================
# IS Z² DEFINED TO ENCODE PACKING?
# =============================================================================

print("\n" + "-"*70)
print("HYPOTHESIS: Z² encodes optimal packing geometry")
print("-"*70)

# If 8π/Z² were exactly equal to FCC packing, what would Z² be?
# η_FCC = 8π/Z²_hypothetical
# Z²_hypothetical = 8π/η_FCC

Z2_from_FCC = 8 * np.pi / ETA_FCC
print(f"""
If 8π/Z² = η_FCC exactly, then:
  Z²_FCC = 8π/η_FCC = 8π × 3√2/π = 24√2 = {Z2_from_FCC:.6f}

But actual Z² = 32π/3 = {Z_SQUARED:.6f}

Ratio: Z²/Z²_FCC = {Z_SQUARED / Z2_from_FCC:.6f}
""")

# =============================================================================
# WHAT PACKING DOES Z² ACTUALLY ENCODE?
# =============================================================================

print("-"*70)
print("WHAT GEOMETRY DOES Z² = 32π/3 ACTUALLY REPRESENT?")
print("-"*70)

# Z² = 32π/3 has a specific geometric meaning
# Let's find it

# Volume of an n-sphere with radius R is V_n = π^(n/2) R^n / Γ(n/2 + 1)
# For n=3: V_3 = 4πR³/3
# For n=4: V_4 = π²R⁴/2

def sphere_volume(n, R=1):
    """Volume of n-dimensional sphere of radius R."""
    from scipy.special import gamma
    return np.pi**(n/2) * R**n / gamma(n/2 + 1)

print("\nSphere volumes (R=1):")
for n in range(2, 7):
    V = sphere_volume(n)
    ratio = Z_SQUARED / V
    print(f"  V_{n} = {V:.6f}, Z²/V_{n} = {ratio:.4f}")

# Check specific geometric objects
print("\n" + "-"*70)
print("CHECKING GEOMETRIC INTERPRETATIONS OF Z² = 32π/3")
print("-"*70)

geometries = {
    "4 × V_3 (4 unit spheres)": 4 * (4*np.pi/3),
    "8 × S_2 (8 unit 2-spheres)": 8 * (4*np.pi),
    "V_4 × 2 (2 unit 4-balls)": 2 * (np.pi**2/2),
    "32π/3 (definition)": 32*np.pi/3,
    "Volume of torus (R=2, r=1)": 2 * np.pi**2 * 2 * 1**2,  # 2π²Rr²
    "8 spheres × π/3 correction": 8 * (4*np.pi/3) * 1,
}

print(f"\nZ² = {Z_SQUARED:.6f}\n")
for name, value in geometries.items():
    diff = abs(value - Z_SQUARED) / Z_SQUARED * 100
    match = "✓ EXACT" if diff < 0.01 else ("~ close" if diff < 5 else "")
    print(f"  {name:40s}: {value:.6f} ({diff:.2f}% off) {match}")

# =============================================================================
# THE 32π/3 GEOMETRIC MEANING
# =============================================================================

print("\n" + "-"*70)
print("DERIVING THE GEOMETRIC MEANING OF Z² = 32π/3")
print("-"*70)

print("""
Z² = 32π/3 can be written as:

  Z² = 32π/3 = (8/3) × 4π = (8/3) × S²  (where S² = surface of unit sphere)

Or:
  Z² = 32π/3 = 8 × (4π/3) = 8 × V³     (where V³ = volume of unit sphere)

So Z² = 8 × (volume of unit sphere)!

This is the volume of 8 unit spheres, or equivalently,
the volume of a 2×2×2 cubic arrangement of unit spheres.

PACKING INTERPRETATION:
  In a cubic arrangement with 8 spheres:
    - Each sphere has volume 4π/3
    - Total sphere volume = 8 × 4π/3 = 32π/3 = Z²
    - The cubic box has side 2 (diameter of sphere)
    - Box volume = 8
    - Packing efficiency = Z²/8 = 4π/3 ≈ 4.19 ... wait, that's > 1

Let me reconsider...
""")

# Actually, Z² = 32π/3 ≈ 33.51, which is NOT a packing efficiency

# Let's think about it differently
# 8π/Z² = 3/4 means Z² = 8π/(3/4) = 32π/3

print("""
Reconsidering:
  8π/Z² = 3/4 means:
    - Z² = 8π × (4/3) = 32π/3

  Where does 8π come from?
    - 8π = 2 × 4π = 2 × (surface of unit sphere)
    - Or: 8π = 8 × π (8 times pi)

  And 3/4?
    - 3/4 is close to FCC packing (0.7405)
    - But 3/4 = 0.75 is not exactly FCC

  The exact relation 8π/Z² = 3/4 appears to be a DEFINITION,
  not an emergent property.
""")

# =============================================================================
# PROTEIN FACTOR CONNECTION
# =============================================================================

print("-"*70)
print("INVESTIGATING Z/12 ≈ PROTEIN FACTOR")
print("-"*70)

protein_factor = 0.491
z_over_12 = Z_CONSTANT / 12

print(f"""
Protein geometrical factor: V/(A⟨r⟩) = {protein_factor} ± 0.005
Z/12 = {Z_CONSTANT}/12 = {z_over_12:.6f}
Difference: {abs(z_over_12 - protein_factor)/protein_factor * 100:.2f}%

Is this meaningful?

12 appears in:
  - Icosahedron: 12 vertices
  - Dodecahedron: 12 faces
  - 12 = 2² × 3

Let's check if there's a deeper connection:
  Z = 2√(8π/3) = 2 × √(8π/3)
  Z/12 = √(8π/3)/6 = √(8π/27) = √(8π)/√27 = 2√(2π)/3√3
       = (2/3) × √(2π/3)

  This doesn't simplify to anything obviously related to 0.491.
""")

# What value of the divisor would make Z/n = protein_factor exactly?
n_for_protein = Z_CONSTANT / protein_factor
print(f"  If Z/n = 0.491, then n = Z/0.491 = {n_for_protein:.3f}")
print(f"  This is close to 12 but not exactly 12.")

# =============================================================================
# CONCLUSION
# =============================================================================

print("\n" + "="*70)
print("CONCLUSION")
print("="*70)

print(f"""
FINDINGS:

1. 8π/Z² = 3/4 EXACTLY (by definition of Z² = 32π/3)
   - This is 1.3% from FCC packing (0.7405)
   - But this appears to be a DEFINITION, not emergent physics

2. Z² = 8 × (volume of unit sphere)
   - Z² = 8 × (4π/3) = 32π/3
   - This gives Z² geometric meaning as "8 unit sphere volumes"
   - But the significance of "8 spheres" is unclear

3. Z/12 ≈ 0.482, close to protein factor 0.491 (1.8%)
   - This could be coincidence (12 is not obviously special)
   - Or it could indicate Z relates to icosahedral geometry

4. Z ≈ 11 × a₀ (Bohr radii)
   - 11 is not a special number in physics
   - The Bohr radius is the fundamental scale, not Z

HONEST ASSESSMENT:
  Z² = 32π/3 appears to be a CONSTRUCTED constant, designed to have
  certain properties (like 8π/Z² ≈ 3/4), rather than emerging from
  fundamental physics.

  The near-matches (Z/12 ≈ protein factor, 8π/Z² ≈ FCC) are
  APPROXIMATE, not exact, suggesting they are coincidences
  within the range of many possible mathematical relationships.

  To truly validate Z², we would need:
  1. An exact match (not 1-2% off)
  2. A physical DERIVATION of why Z² should equal 32π/3
  3. Multiple independent predictions that all work

  Currently, Z² lacks these criteria.
""")
