#!/usr/bin/env python3
"""
MOND INTERPOLATING FUNCTION FROM Z² GEOMETRY
=============================================

This script attempts to derive the MOND interpolating function μ(x)
from Z² first principles, addressing the gap identified by Milgrom.

What's already derived:
    a₀ = cH₀/Z (the MOND acceleration scale)

What's NOT derived:
    μ(x) = interpolating function between Newtonian and MOND regimes

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("=" * 80)
print("MOND INTERPOLATING FUNCTION FROM Z² GEOMETRY")
print("=" * 80)

# Physical constants
c = 3e8  # m/s
H0 = 2.3e-18  # 1/s (H₀ ≈ 70 km/s/Mpc)
G = 6.67e-11  # m³/(kg·s²)

# Z² constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)

# MOND acceleration scale
a0_observed = 1.2e-10  # m/s² (Milgrom's value)
a0_Z2 = c * H0 / Z     # Z² prediction

print(f"\nZ² = {Z_SQUARED:.4f}")
print(f"Z = {Z:.4f}")
print(f"\na₀ (observed): {a0_observed:.2e} m/s²")
print(f"a₀ (Z²):       {a0_Z2:.2e} m/s²")
print(f"Ratio: {a0_Z2/a0_observed:.2f}")

# =============================================================================
# PART 1: THE PROBLEM
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: WHAT IS THE INTERPOLATING FUNCTION?")
print("=" * 80)

print("""
MOND DYNAMICS:

Standard MOND says:
    a = a_N × μ(a/a₀)

where:
- a_N = GM/r² (Newtonian acceleration)
- a₀ ≈ 1.2×10⁻¹⁰ m/s² (MOND scale)
- μ(x) = interpolating function

BEHAVIOR:
- μ(x >> 1) → 1    (Newtonian regime, high acceleration)
- μ(x << 1) → x    (MOND regime, low acceleration → a ~ √(a_N × a₀))

COMMON FORMS:

1. Simple:
   μ(x) = x / (1 + x)

2. Standard:
   μ(x) = x / √(1 + x²)

3. RAR (Radial Acceleration Relation):
   μ(x) = 1 / (1 + e^{-√x})

All satisfy the asymptotic limits, but differ in transition region.

THE CHALLENGE:
Can we derive which μ(x) is correct from Z² geometry?
""")

# =============================================================================
# PART 2: Z² SCALE DERIVATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: WHERE DOES a₀ = cH/Z COME FROM?")
print("=" * 80)

print("""
THE UNRUH-HAWKING MATCHING:

An accelerating observer sees the Unruh temperature:
    T_U = ℏa / (2πk_B c)

The cosmological horizon has Hawking temperature:
    T_H = ℏH / (2πk_B)

Setting T_U = T_H:
    a = cH

But MOND scale is a₀ ≈ cH/6, not cH.

Z² EXPLAINS THE FACTOR:

If a₀ = cH₀/Z where Z = √(32π/3) ≈ 5.79:
    a₀ = cH₀/Z ≈ cH₀/6

This matches observation!

THE QUESTION REMAINS:
WHY does Z enter? What is the physical mechanism?
""")

# Verify the Z factor
print(f"\nVerification:")
print(f"cH₀ = {c * H0:.2e} m/s²")
print(f"cH₀/Z = {c * H0 / Z:.2e} m/s²")
print(f"a₀ observed = {a0_observed:.2e} m/s²")
print(f"Agreement: {100*(1 - abs(c*H0/Z - a0_observed)/a0_observed):.1f}%")

# =============================================================================
# PART 3: DERIVING μ(x) FROM GEOMETRY
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: GEOMETRIC DERIVATION ATTEMPT")
print("=" * 80)

print("""
APPROACH 1: ENTROPY PARTITION

At low accelerations, the system "sees" the cosmological horizon.
At high accelerations, local physics dominates.

Define: f = fraction of entropy in "local" vs "horizon" modes

For high a: f → 1 (local dominates)
For low a: f → 0 (horizon dominates)

The interpolation is:
    μ(x) = f(x) where x = a/a₀

WHAT DETERMINES f(x)?

Conjecture: f(x) is the fraction of the lattice that is
"causally local" vs "horizon-influenced".
""")

# =============================================================================
# PART 4: SPECIFIC DERIVATION ATTEMPTS
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: SPECIFIC DERIVATION ATTEMPTS")
print("=" * 80)

def mu_simple(x):
    """Simple interpolating function: μ(x) = x/(1+x)"""
    return x / (1 + x)

def mu_standard(x):
    """Standard interpolating function: μ(x) = x/√(1+x²)"""
    return x / np.sqrt(1 + x**2)

def mu_rar(x):
    """RAR interpolating function: μ(x) = 1/(1+e^{-√x})"""
    return 1 / (1 + np.exp(-np.sqrt(np.maximum(x, 1e-10))))

# Test values
x_values = np.logspace(-3, 3, 100)

print("""
ATTEMPT 1: BOLTZMANN PARTITION

If local and horizon modes have energies E_local = kT_U and E_horizon = kT_H:
    T_U/T_H = a/cH = (a/a₀) × (a₀/cH) = x × (1/Z)

The Boltzmann factor gives:
    f = e^{-E_H/E_L} / (1 + e^{-E_H/E_L})
      = 1 / (1 + e^{T_H/T_U})
      = 1 / (1 + e^{Z/x})

For large x: f → 1 (local dominates)
For small x: f → e^{-Z/x} → 0 (horizon dominates)
""")

def mu_boltzmann(x, Z=Z):
    """Boltzmann-derived interpolating function"""
    return 1 / (1 + np.exp(Z / np.maximum(x, 1e-10)))

print("""
ATTEMPT 2: LINEAR PARTITION

Simpler: f = x / (x + Z)

For large x: f → 1
For small x: f → x/Z

This gives μ(x) = x / (x + Z)
""")

def mu_linear_Z(x, Z=Z):
    """Z-modified simple interpolating function"""
    return x / (x + Z)

print("""
ATTEMPT 3: GEOMETRIC PARTITION (Z² STRUCTURE)

The cube has 8 vertices, 12 edges, 6 faces.
The fraction of "structure" at scale r is:

f(r) = (r/L)^d where L is horizon scale, d is dimension

At acceleration a, the relevant scale is c²/a.
At horizon, scale is c/H.

f = (c²/a) / (c/H) = cH/a = (1/Z) × (a₀/a) = 1/(Z×x)... wrong direction!

Let's try inverse: f = a/(cH) = Z × x... but this exceeds 1.

Correct normalization:
f = Z×x / (1 + Z×x) = Zx / (1 + Zx)
""")

def mu_geometric_Z(x, Z=Z):
    """Geometric Z-derived interpolating function"""
    return (Z * x) / (1 + Z * x)

# =============================================================================
# PART 5: COMPARING INTERPOLATING FUNCTIONS
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: COMPARING ALL INTERPOLATING FUNCTIONS")
print("=" * 80)

print("\nInterpolating functions at key points:")
print("-" * 60)
print(f"{'Function':<20} {'x=0.1':<12} {'x=1':<12} {'x=10':<12}")
print("-" * 60)

funcs = [
    ("μ_simple", mu_simple),
    ("μ_standard", mu_standard),
    ("μ_RAR", mu_rar),
    ("μ_Boltzmann", mu_boltzmann),
    ("μ_linear_Z", mu_linear_Z),
    ("μ_geometric_Z", mu_geometric_Z),
]

for name, func in funcs:
    try:
        v01 = func(0.1)
        v1 = func(1.0)
        v10 = func(10.0)
        print(f"{name:<20} {v01:<12.4f} {v1:<12.4f} {v10:<12.4f}")
    except:
        print(f"{name:<20} ERROR")

# =============================================================================
# PART 6: WHICH IS CORRECT?
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: OBSERVATIONAL CONSTRAINTS")
print("=" * 80)

print("""
OBSERVATIONAL DATA:

The Radial Acceleration Relation (RAR) from McGaugh et al. (2016):
- Compiled rotation curves from 153 galaxies
- Found tight correlation between observed and Newtonian acceleration
- Best fit: μ_RAR(x) = 1/(1 + e^{-√x})

McGaugh relation:
    g_obs = g_bar / (1 - e^{-√(g_bar/g†)})

where g† ≈ 1.2×10⁻¹⁰ m/s² = a₀

This is equivalent to:
    μ(x) = 1 - e^{-√x}... wait, that's different!

Actually the RAR form is:
    g_obs = g_bar × μ(g_bar/a₀)

where μ(x) = 1/(1 + e^{-√x}) for their fit.

Z² COMPARISON:

Our Boltzmann form μ(x) = 1/(1 + e^{Z/x}) is DIFFERENT from RAR.
- RAR has e^{-√x} (grows with x)
- Boltzmann has e^{Z/x} (shrinks with x)

This suggests the Boltzmann approach is NOT correct as written.
""")

# =============================================================================
# PART 7: CORRECT Z² APPROACH
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: REVISED Z² APPROACH")
print("=" * 80)

print("""
INSIGHT: The RAR form has √x, not 1/x.

Could Z appear in a √x-like way?

ATTEMPT:
    μ(x) = 1 / (1 + e^{-x/Z})

For x >> Z: μ → 1 (Newtonian)
For x << Z: μ → 1/(1+1) = 0.5... wrong!

BETTER ATTEMPT:
    μ(x) = 1 / (1 + e^{-√(x×Z)})

For x >> 1: μ → 1
For x << 1: μ → 1/(1 + e^{-√(x×Z)}) ≈ e^{√(x×Z)}/2... still not linear in x!

THE PROBLEM:
None of our Z² forms naturally give μ(x) → x for small x,
which is required for MOND to produce a ~ √(a_N × a₀).

FUNDAMENTAL ISSUE:
The interpolating function shape is NOT determined by
the scale a₀ alone. It requires additional physics.
""")

def mu_z_sqrt(x, Z=Z):
    """μ(x) = 1/(1 + e^{-√(xZ)})"""
    return 1 / (1 + np.exp(-np.sqrt(x * Z)))

# =============================================================================
# PART 8: THE HONEST ASSESSMENT
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: HONEST ASSESSMENT")
print("=" * 80)

print(f"""
WHAT Z² FRAMEWORK DERIVES:
✓ The MOND acceleration scale a₀ = cH₀/Z
✓ This matches observation to ~{100*(1 - abs(c*H0/Z - a0_observed)/a0_observed):.0f}%
✓ The connection to Unruh-Hawking physics is meaningful

WHAT Z² FRAMEWORK DOES NOT DERIVE:
✗ The specific form of μ(x)
✗ Why μ(x) ≈ x/(1+x) or similar
✗ The √x dependence in RAR

THE GAP:
The interpolating function requires understanding HOW
the lattice geometry transitions from local to horizon-dominated.
This is not just about the SCALE but about the DYNAMICS.

POSSIBLE PATHS FORWARD:
1. Derive μ(x) from lattice random walk statistics
2. Use thermodynamic/entropy arguments more carefully
3. Connect to Verlinde's emergent gravity framework
4. Study numerical simulations of MOND on lattice

STATUS: PARTIAL GAP CLOSURE
- Scale a₀ is derived
- Functional form μ(x) is NOT derived
- This remains a genuine open problem
""")

# =============================================================================
# PART 9: WHAT WOULD CLOSE THE GAP
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: WHAT WOULD CLOSE THE GAP")
print("=" * 80)

print("""
TO FULLY DERIVE μ(x) FROM Z², WE WOULD NEED:

1. LATTICE DYNAMICS:
   - Define random walk on Z² lattice
   - Compute return probability as function of acceleration
   - Show this gives μ(x) form

2. ENTROPY APPROACH:
   - Partition function for lattice states
   - Local vs. horizon entropy balance
   - Show Boltzmann weights give μ(x)

3. FIELD THEORY:
   - Effective action on lattice
   - Running of gravitational constant with scale
   - Show RG flow gives MOND behavior

4. NUMERICAL:
   - Simulate N-body on Z² lattice
   - Measure effective μ(x) from dynamics
   - Compare to RAR data

MOST PROMISING: Random walk approach

If diffusion on lattice changes character at a₀,
the return probability might give μ(x).

This connects to spectral dimension (d_s)!
""")

# =============================================================================
# SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)

print(f"""
┌─────────────────────────────────────────────────────────────────┐
│         MOND INTERPOLATING FUNCTION STATUS                      │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHAT'S DERIVED:                                                │
│  ✓ a₀ = cH₀/Z = {c*H0/Z:.2e} m/s²                            │
│  ✓ Matches observed a₀ = 1.2×10⁻¹⁰ m/s²                        │
│  ✓ Physical mechanism: Unruh-Hawking temperature matching       │
│  ✓ Factor Z = {Z:.4f} from Z² = 32π/3                           │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  WHAT'S NOT DERIVED:                                            │
│  ✗ Functional form μ(x) of interpolation                        │
│  ✗ Why μ(x) ≈ x/(1+x) specifically                              │
│  ✗ √x dependence in RAR                                         │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ATTEMPTS MADE:                                                 │
│  - Boltzmann partition: Wrong asymptotic behavior               │
│  - Linear Z partition: μ(x) = x/(x+Z), plausible                │
│  - Geometric partition: μ(x) = Zx/(1+Zx), wrong limit           │
│  - √(xZ) form: Doesn't give μ → x for small x                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  MOST PROMISING PATH:                                           │
│  → Random walk on lattice + spectral dimension connection       │
│                                                                 │
│  STATUS: PARTIAL CLOSURE                                        │
│  - Scale derived, form not derived                              │
│  - This remains a genuine open problem                          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
""")

print("\nEnd of MOND interpolating function analysis.")
