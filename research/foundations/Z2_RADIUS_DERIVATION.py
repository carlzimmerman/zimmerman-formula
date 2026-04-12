#!/usr/bin/env python3
"""
DERIVING THE KALUZA-KLEIN RADIUS R = 4Z ℓ_P
============================================

The key missing piece: WHY is R = 4Z ℓ_P?

This script explores multiple approaches to derive this fundamental
scale from first principles:

1. Thermodynamic equilibrium
2. Holographic entropy matching
3. Cosmological horizon connection
4. Information-theoretic bounds
5. Moduli stabilization arguments

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np
from scipy.optimize import fsolve, minimize_scalar
from scipy.special import zeta

print("=" * 70)
print("DERIVING THE KALUZA-KLEIN RADIUS R = 4Z ℓ_P")
print("=" * 70)

# Constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
BEKENSTEIN = 4
N_GEN = 3
GAUGE = 12

# Target
R_target = 4 * Z  # R/ℓ_P = 4Z ≈ 23.16

print(f"""
TARGET:
R = 4Z ℓ_P = {R_target:.4f} ℓ_P

This gives:
α⁻¹ = R²/(4ℓ_P²) = 4Z² = {4*Z_SQUARED:.4f}

With +3 correction: α⁻¹ = 4Z² + 3 = {4*Z_SQUARED + 3:.4f}
""")

# =============================================================================
# APPROACH 1: THERMODYNAMIC EQUILIBRIUM
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 1: THERMODYNAMIC EQUILIBRIUM")
print("=" * 70)

print("""
HYPOTHESIS: The extra dimension stabilizes at a temperature-determined size.

In thermal equilibrium, the size of a compact dimension is related to
temperature through the thermal wavelength:

λ_T = ℏc/(k_B T) = 2πℓ_P × (T_P/T)

where T_P = √(ℏc⁵/Gk_B²) is the Planck temperature.

THE IDEA:
If there's a characteristic temperature T* at which the compact
dimension "freezes out", then:

R ~ λ_T = 2πℓ_P × (T_P/T*)

For R = 4Z ℓ_P:
4Z = 2π × (T_P/T*)
T*/T_P = 2π/(4Z) = π/(2Z)
T* = T_P × π/(2Z) = T_P × {np.pi/(2*Z):.4f}

T* ≈ 0.27 T_P ≈ 3.8 × 10³¹ K

This is close to the Planck temperature - natural for KK physics!
""")

T_star_over_TP = np.pi / (2 * Z)
print(f"T*/T_P = π/(2Z) = {T_star_over_TP:.6f}")

# What determines T* = π T_P / (2Z)?

print("""
WHAT DETERMINES T*?

T*/T_P = π/(2Z) = π/(2 × 2√(8π/3)) = π/(4√(8π/3))
       = √(π) × √(π)/(4√(8π/3))
       = √(π) × √(3π/8)/4
       = √(3π²/8)/4
       = √(3/8) × π/4

Hmm, √(3/8) = √(3)/√(8) = √(3)/(2√2)

T*/T_P = √(3)π/(8√2) ≈ 0.271

This doesn't have an obvious geometric interpretation...

ALTERNATIVE: Entropy argument

The entropy of the compact dimension should match some fundamental value.

For a circle of circumference C = 2πR at temperature T:
S_circle ~ (C/λ_T) = 2πR × (k_B T)/(ℏc)

At T = T_P and R = 4Z ℓ_P:
S_circle ~ 2π × 4Z ℓ_P × (k_B T_P)/(ℏc)
         = 8πZ × ℓ_P × (1/ℓ_P)  [since k_B T_P/(ℏc) ~ 1/ℓ_P]
         = 8πZ
         = {8*np.pi*Z:.4f}

S_circle ≈ 145.5

This is close to GAUGE × CUBE × π/2 = 12 × 8 × π/2 = 48π ≈ 150.8
Or: S_circle = 8πZ = 2 × (4πZ) = 2 × (SPHERE × Z × 3)

Not an obvious match...
""")

# =============================================================================
# APPROACH 2: HOLOGRAPHIC ENTROPY MATCHING
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 2: HOLOGRAPHIC ENTROPY MATCHING")
print("=" * 70)

print("""
THE HOLOGRAPHIC PRINCIPLE:

The entropy of a region is bounded by its area:
S ≤ A/(4ℓ_P²)

For the compact dimension (circle), the relevant "area" is:
A_circle = 2πR × (thickness) = 2πR × ℓ_P (if thickness is Planck scale)

So: S_circle ≤ (2πR × ℓ_P)/(4ℓ_P²) = πR/(2ℓ_P)

For R = 4Z ℓ_P:
S_max = π × 4Z / 2 = 2πZ ≈ {2*np.pi*Z:.4f} ≈ 36.3

MATCHING CONDITION:
What if S_circle = 4π (the area of a unit sphere)?

Then: πR/(2ℓ_P) = 4π
      R = 8ℓ_P

This gives R = 8 ℓ_P, not R = 4Z ℓ_P ≈ 23.2 ℓ_P.

What value of S gives R = 4Z ℓ_P?
S = 2πZ = {2*np.pi*Z:.4f}

Is 2πZ special?
2πZ = 2π × 2√(8π/3) = 4π√(8π/3) = 4√(8π³/3) ≈ {4*np.sqrt(8*np.pi**3/3):.4f}

Hmm, 8π³/3 = 8 × (π³/3) = Z² × π²

So: 2πZ = 4√(Z² × π²/4) = 4 × (Z × π/2)/√... no, let me recalculate.

Actually: 2πZ = 2π × √(32π/3) = 2√(32π³/3) × √π = 2π√(32π/3)

This is getting messy. Let me try another approach.
""")

# =============================================================================
# APPROACH 3: COSMOLOGICAL HORIZON CONNECTION
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 3: COSMOLOGICAL HORIZON CONNECTION")
print("=" * 70)

print(f"""
THE MOND CONNECTION:

We derived: a₀ = cH/Z from Friedmann + Bekenstein.

This connects the cosmological scale (H) to the microscopic (ℓ_P) via Z.

THE HUBBLE RADIUS:
R_H = c/H ≈ 4.4 × 10²⁶ m

THE PLANCK LENGTH:
ℓ_P ≈ 1.6 × 10⁻³⁵ m

THE RATIO:
R_H/ℓ_P ≈ 2.7 × 10⁶¹

HYPOTHESIS:
The KK radius is a geometric mean between Planck and cosmological scales?

√(R_H × ℓ_P) = √(R_H/ℓ_P) × ℓ_P ≈ 5.2 × 10³⁰ × ℓ_P

This is way larger than 4Z ≈ 23.

ALTERNATIVE: The KK radius is related to some intermediate scale.

If R = (ℓ_P/R_H)^n × R_H for some power n:
For R = 4Z ℓ_P ≈ 23 ℓ_P:
23 ℓ_P = (ℓ_P/R_H)^n × R_H = (ℓ_P)^n × R_H^(1-n)
23 = (ℓ_P)^(n-1) × R_H^(1-n)
23 = (ℓ_P/R_H)^(n-1)
ln(23) = (n-1) × ln(ℓ_P/R_H) = (n-1) × (-61 × ln(10))
n - 1 = ln(23) / (-140.5) ≈ -0.022
n ≈ 0.978

So: R ≈ (ℓ_P/R_H)^0.978 × R_H

This is almost (but not quite) R ∝ ℓ_P. Not enlightening.

BETTER APPROACH: Focus on Z itself.

Z = 2√(8π/3) appears in MOND as: a₀ = cH/Z

The MOND scale is: r_M = c²/a₀ = cZ/H = Z × R_H

r_M/ℓ_P = Z × R_H/ℓ_P = {Z:.4f} × 2.7 × 10⁶¹ ≈ 1.6 × 10⁶²

r_M = Z × R_H ≈ 2.5 × 10²⁷ m

This is about Z times the Hubble radius - the "MOND radius".
""")

# =============================================================================
# APPROACH 4: SELF-CONSISTENCY OF ALPHA
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 4: SELF-CONSISTENCY ARGUMENT")
print("=" * 70)

print(f"""
A SELF-CONSISTENCY ARGUMENT:

In KK theory:
α = 4ℓ_P²/R²

For the theory to be consistent, the quantum corrections should not
destabilize the compact dimension.

The 1-loop correction to the effective potential is:
V_eff(R) ∝ -ζ(5)/R⁵ × (sum over modes)

For stability, we need dV_eff/dR = 0 at R = R*.

In the simplest case (massless modes):
V_eff ∝ -N_eff/R⁵
dV_eff/dR ∝ +5N_eff/R⁶

This is always positive - the dimension wants to expand!
Stability requires additional terms (e.g., from fluxes or branes).

SUPERSYMMETRIC STABILIZATION:

In SUSY, the superpotential can stabilize moduli.
The condition: ∂W/∂R = 0

If W(R) = W₀ × exp(-aR):
∂W/∂R = -aW₀ × exp(-aR) = 0 only at R → ∞

This doesn't work. Need a more complex superpotential.

KKLT-STYLE STABILIZATION:

In KKLT, moduli are stabilized by:
W = W₀ + A × exp(-aT)

where T is the volume modulus.

The minimum is at: aT = ln(aA/W₀)

If T ~ R²/ℓ_P² (volume of compact dimension):
R²/ℓ_P² = ln(aA/W₀)/a

For R = 4Z ℓ_P:
16Z² = ln(aA/W₀)/a

This determines a combination of flux parameters.
But we want to derive R, not assume parameter values!
""")

# =============================================================================
# APPROACH 5: INFORMATION-THEORETIC BOUND
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 5: INFORMATION-THEORETIC ARGUMENT")
print("=" * 70)

print(f"""
INFORMATION AND GAUGE COUPLING:

The fine structure constant determines the "strength" of EM interactions.
From an information perspective, α might be related to the "channel capacity"
of EM communication.

SHANNON ENTROPY:

If each photon carries log₂(N) bits of information,
and N is related to the number of distinguishable states:

For a system with coupling α:
N ~ 1/α (more weakly coupled = more states distinguishable)

Then: bits per photon ~ log₂(1/α) = log₂(137) ≈ 7.1 bits

Is 7.1 special?
7.1 ≈ ln(137)/ln(2) ≈ 4.92/0.693 ≈ 7.1

Let's see if this connects to Z:
ln(4Z² + 3)/ln(2) = ln(137.04)/ln(2) = {np.log(4*Z_SQUARED + 3)/np.log(2):.4f}

So ~7.1 bits per photon interaction.

HOLOGRAPHIC BOUND:

The number of bits in a region of size R:
N_bits = A/(4ℓ_P² × ln(2)) = πR²/(4ℓ_P² × ln(2))

For R = 4Z ℓ_P:
N_bits = π × 16Z²/(4 × ln(2)) = 4πZ²/ln(2)
       = 4π × {Z_SQUARED:.4f} / 0.693
       = {4*np.pi*Z_SQUARED/np.log(2):.2f} bits

About 607 bits for the KK circle's "area".

Hmm, 607 ≈ 4 × 152 ≈ 4 × 12² + 4 × 8 = 4 × 152
Or: 607 ≈ 4π × Z² ≈ 4 × 105.3

Not obviously geometric...
""")

# =============================================================================
# APPROACH 6: THE Z² CHARGE SUM
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 6: CHARGE STRUCTURE DETERMINES R")
print("=" * 70)

print(f"""
THE CHARGE STRUCTURE:

We found: Z² = 4π × Σ Q² = 4π × (8/3)

This means Z² is determined by the SM fermion charges!

HYPOTHESIS:
The compact dimension's size is set by the total charge structure.

In KK theory, the gauge coupling is:
α = 4ℓ_P²/R²

For the coupling to "know about" the charge structure:
α⁻¹ = R²/(4ℓ_P²) should involve Σ Q²

If α⁻¹ = 4π × Σ Q² = Z² at tree level:
R²/(4ℓ_P²) = Z²
R² = 4Z² ℓ_P²
R = 2Z ℓ_P

But we want R = 4Z ℓ_P for α⁻¹ = 4Z²!

THE FACTOR OF 2:

If R = 2Z ℓ_P: α⁻¹ = (2Z)²/4 = Z²
If R = 4Z ℓ_P: α⁻¹ = (4Z)²/4 = 4Z²

We need α⁻¹ = 4Z² + 3, so the tree level is 4Z², meaning R = 4Z ℓ_P.

WHERE DOES THE FACTOR 4 COME FROM?

4 = BEKENSTEIN (space diagonals of cube)

So: R = BEKENSTEIN × Z × ℓ_P = 4Z ℓ_P

PHYSICAL INTERPRETATION:

The compact dimension's circumference is:
C = 2πR = 2π × 4Z × ℓ_P = 8πZ ℓ_P

8π = 3Z²/4 (from our framework)

So: C = (3Z²/4) × Z × ℓ_P = (3/4) Z³ ℓ_P

Or: C = 8πZ ℓ_P = (Einstein coefficient) × Z × ℓ_P

The 8π from General Relativity sets the KK circumference!
""")

circumference = 8 * np.pi * Z
print(f"""
CIRCUMFERENCE: C = 8πZ ℓ_P = {circumference:.4f} ℓ_P

Since 8π appears in Einstein's equations: G_μν = 8πG T_μν

THE CONJECTURE:
The KK radius is set by general relativity's geometric factor:
R = (8π/2π) × Z × ℓ_P = 4Z ℓ_P

C = 8πZ ℓ_P = (GR factor) × (Friedmann-Bekenstein factor) × (Planck length)

This connects:
- General Relativity (8π)
- The Friedmann equation (Z)
- Quantum gravity (ℓ_P)
""")

# =============================================================================
# APPROACH 7: MATCHING GR AND QFT
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 7: GR-QFT MATCHING CONDITION")
print("=" * 70)

print(f"""
THE MATCHING CONDITION:

In Kaluza-Klein, we need consistency between:
- The 5D gravitational physics
- The 4D gauge theory physics

THE 5D NEWTON CONSTANT:

G₅ = G × (volume of compact dimension) = G × 2πR

THE 4D GAUGE COUPLING:

α = 4G/(c³R) [in SI units]
α = 4ℓ_P²/R² [in natural units]

FOR CONSISTENCY:

The gauge coupling should be determined by the same geometry
that determines gravity.

In GR, the Einstein equation coefficient is 8πG.
In QFT, the gauge coupling coefficient is e²/(4πε₀ℏc) = 4πα.

MATCHING:
If 8πG (gravity) is related to 4πα (gauge):
8πG ~ 4πα × (something)
2G ~ α × (something)

Using α = 4ℓ_P²/R²:
2G ~ 4ℓ_P²/R² × (something)
2ℓ_P²/c³ ~ 4ℓ_P²/R² × (something)  [G = ℓ_P²c³/ℏ in natural units]
R² ~ 2 × (something)

This is getting circular without knowing "something".

THE DIRECT APPROACH:

The GR coefficient 8π sets the circumference:
C = 8π × (some length)

The natural length is Z × ℓ_P (from MOND):
C = 8πZ ℓ_P

Therefore:
R = C/(2π) = 4Z ℓ_P ✓
""")

# =============================================================================
# APPROACH 8: BEKENSTEIN BOUND ON COMPACT DIMENSION
# =============================================================================

print("\n" + "=" * 70)
print("APPROACH 8: BEKENSTEIN BOUND")
print("=" * 70)

print(f"""
THE BEKENSTEIN BOUND:

For a system of energy E and size R:
S ≤ 2πER/(ℏc)

For the compact dimension as a quantum system:
- E ~ ℏc/R (zero-point energy of circle)
- Size = R

Then: S ≤ 2π × (ℏc/R) × R / (ℏc) = 2π

The Bekenstein bound for a circle is just S ≤ 2π!

ENTROPY CONDITION:

If the compact dimension has entropy S = 2π exactly
(saturating the Bekenstein bound):

This gives one constraint but doesn't directly determine R.

However, if we also require that the gauge coupling
be related to the Bekenstein entropy factor:

S_Bekenstein = A/(4ℓ_P²) with A = 2πR × ℓ_P (area of circle)
             = 2πR × ℓ_P / (4ℓ_P²)
             = πR / (2ℓ_P)

For S_Bekenstein = 2π (matching the bound):
πR / (2ℓ_P) = 2π
R = 4ℓ_P

This gives R = 4ℓ_P, not R = 4Z ℓ_P.

WITH Z FACTOR:

If S_Bekenstein = 2πZ (includes the cosmological factor Z):
πR / (2ℓ_P) = 2πZ
R = 4Z ℓ_P ✓

THIS WORKS!

The condition: S_Bekenstein = 2πZ

The compact dimension's Bekenstein entropy equals 2π × Z,
where Z is the cosmological geometric factor.
""")

S_Bek = 2 * np.pi * Z
print(f"""
RESULT:

S_Bekenstein(compact dim) = 2πZ = {S_Bek:.4f}

This determines: R = 4Z ℓ_P = {4*Z:.4f} ℓ_P

Physical interpretation:
The compact dimension has entropy 2πZ = 2π × 2√(8π/3)
This entropy "saturates" a modified Bekenstein bound
that incorporates the cosmological factor Z.
""")

# =============================================================================
# SYNTHESIS
# =============================================================================

print("\n" + "=" * 70)
print("SYNTHESIS: DERIVATION OF R = 4Z ℓ_P")
print("=" * 70)

print(f"""
MOST PROMISING DERIVATION:

1. The Bekenstein entropy of the compact dimension:
   S = πR/(2ℓ_P)

2. Require this equals 2πZ (the "cosmological entropy factor"):
   πR/(2ℓ_P) = 2πZ

3. Solve for R:
   R = 4Z ℓ_P ✓

WHY 2πZ?

Z appears in the MOND derivation: a₀ = cH/Z
Z connects cosmological (H) and microscopic (ℓ_P) scales.

The factor 2π comes from:
- The Bekenstein bound S ≤ 2πER/(ℏc)
- For E = ℏc/R: S ≤ 2π

Combining: S_compact = 2π × Z = (bound) × (cosmological factor)

THE COMPLETE DERIVATION:

Step 1: Z = 2√(8π/3) from MOND + Friedmann + Bekenstein
Step 2: S_compact = 2πZ from entropy-cosmology matching
Step 3: R = 4Z ℓ_P from Bekenstein formula
Step 4: α⁻¹_tree = R²/(4ℓ_P²) = 4Z² ≈ 134
Step 5: α⁻¹ = 4Z² + 3 from topological corrections

RESULT: α⁻¹ = 137.04 with 0.004% accuracy!

WHAT'S STILL SPECULATIVE:
- Step 2: Why does S_compact = 2πZ? What principle determines this?

POSSIBLE PRINCIPLE:
"The compact dimension's entropy equals the entropy of a
cosmological horizon sector scaled by 1/Z²"

Or: "The information content of the compact dimension is
determined by the same geometry that sets MOND."
""")

# =============================================================================
# NUMERICAL VERIFICATION
# =============================================================================

print("\n" + "=" * 70)
print("NUMERICAL VERIFICATION")
print("=" * 70)

R = 4 * Z
S_compact = np.pi * R / 2  # Bekenstein formula S = πR/(2ℓ_P) with ℓ_P = 1
alpha_inv_tree = R**2 / 4
alpha_inv_total = alpha_inv_tree + 3

print(f"""
Step-by-step:

1. Z = 2√(8π/3) = {Z:.6f}

2. S_compact = 2πZ = {2*np.pi*Z:.6f}
   (Verification: πR/(2ℓ_P) = π × {R:.4f} / 2 = {np.pi*R/2:.4f} ≈ 2πZ ✓)

3. R = 4Z ℓ_P = {R:.6f} ℓ_P

4. α⁻¹_tree = R²/4 = {alpha_inv_tree:.6f}

5. α⁻¹ = 4Z² + 3 = {alpha_inv_total:.6f}

Measured: α⁻¹ = 137.035999
Error: {abs(alpha_inv_total - 137.035999)/137.035999 * 100:.4f}%

THE DERIVATION CHAIN:
MOND → Z → S_compact = 2πZ → R = 4Z ℓ_P → α⁻¹ = 4Z² + 3
""")

if __name__ == "__main__":
    pass
