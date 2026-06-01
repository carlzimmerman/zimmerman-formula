#!/usr/bin/env python3
"""
Rigorous Analysis: Does T³/Z₂ Give r = 1/(2Z²)?

Following the same careful approach we used for h_× = 0, let's examine
whether the tensor-to-scalar ratio prediction r = 1/(2Z²) is valid.

Carl Zimmerman | May 2026
"""

import numpy as np

print("="*70)
print("RIGOROUS ANALYSIS: TENSOR-TO-SCALAR RATIO r = 1/(2Z²)")
print("="*70)

# =============================================================================
# PART 1: THE CLAIMED DERIVATION
# =============================================================================

print("""
PART 1: THE CLAIMED DERIVATION
==============================

The existing documents claim:

  r = 1/(2Z²) = 1/(2 × 33.510321) = 0.0149

With two ingredients:
  1. Factor of 1/2 from "Z₂ mode counting"
  2. Factor of Z² from "Z² normalization"

Let's examine each claim carefully.
""")


# =============================================================================
# PART 2: WHAT IS THE TENSOR-TO-SCALAR RATIO?
# =============================================================================

print("""
PART 2: WHAT IS r IN STANDARD COSMOLOGY?
========================================

The tensor-to-scalar ratio is defined as:

  r = P_T(k*) / P_S(k*)

where:
  P_T = primordial tensor (gravitational wave) power spectrum
  P_S = primordial scalar (density perturbation) power spectrum
  k* = pivot scale (typically 0.05 Mpc⁻¹)

In slow-roll inflation:

  P_S = (1/8π²) × (H²/ε) × (1/M_Pl²)
  P_T = (2/π²) × (H/M_Pl)²

Therefore:
  r = P_T/P_S = 16ε

where ε is the first slow-roll parameter:
  ε = (M_Pl²/2) × (V'/V)²

KEY POINT: In standard inflation, r depends on the inflaton potential V(φ).
Different potentials give different r values.
""")


# =============================================================================
# PART 3: THE Z₂ MODE COUNTING ARGUMENT
# =============================================================================

print("""
PART 3: EXAMINING THE "Z₂ MODE COUNTING" ARGUMENT
=================================================

CLAIM: On T³/Z₂, half the modes are projected out, reducing P_T by 1/2.

Let's check this carefully.

THE Z₂ ACTION ON COSMIC TOPOLOGY:
---------------------------------
If the 4D spatial sections have T³/Z₂ topology:

  Z₂: x → -x  (spatial reflection)

Fourier modes on T³ are:
  exp(i k·x) with k = 2πn/L

Under Z₂:
  exp(i k·(-x)) = exp(-i k·x)

So:
  - cos(k·x) = [exp(ikx) + exp(-ikx)]/2  → EVEN → survives
  - sin(k·x) = [exp(ikx) - exp(-ikx)]/2i → ODD  → projected out

QUESTION: Does this affect SCALARS and TENSORS differently?

SCALAR PERTURBATIONS (Φ):
-------------------------
Φ(x) is a scalar field (density perturbation).

Under Z₂: x → -x
  Φ(-x) = Φ(x)  for Z₂-even modes (cos)
  Φ(-x) = -Φ(x) for Z₂-odd modes (sin) → projected out

TENSOR PERTURBATIONS (h_ij):
----------------------------
h_ij(x) is a rank-2 tensor (gravitational wave).

Under Z₂: x → -x
The Jacobian is ∂x'/∂x = -1 (diagonal -1 matrix).

For a rank-2 tensor:
  h'_ij(x') = (∂x^k/∂x'^i)(∂x^l/∂x'^j) h_kl(x)
            = (-δ^k_i)(-δ^l_j) h_kl(x)
            = (+1) × h_ij(x)

So h_ij transforms as a SCALAR under the Z₂ reflection!

(This is because (-1)² = +1 for a rank-2 tensor.)

CONCLUSION:
-----------
BOTH scalar (Φ) and tensor (h_ij) perturbations transform the SAME way
under the Z₂ reflection:
  - cos modes survive
  - sin modes are projected out

The RATIO r = P_T/P_S is UNCHANGED because both are reduced by the
same factor!

  r_T³/Z₂ = (P_T/2) / (P_S/2) = P_T/P_S = r_standard

THE Z₂ MODE COUNTING DOES NOT CHANGE r!
""")


# =============================================================================
# PART 4: WHAT ABOUT POLARIZATIONS?
# =============================================================================

print("""
PART 4: WHAT ABOUT THE TWO POLARIZATIONS?
=========================================

CLAIM: "The two polarization states (+, ×) are both affected by projection"

We already proved this is WRONG for the extra-dimensional Z₂!

But what about the cosmic topology Z₂ (spatial reflection)?

Under spatial reflection x → -x:

For GW propagating in z-direction:

  Polarization tensors:
    e^(+)_ij = diag(1, -1, 0)   (+ polarization)
    e^(×)_ij = [[0,1,0],[1,0,0],[0,0,0]]  (× polarization)

Under x → -x, y → -y, z → -z:

  Both e^(+) and e^(×) transform as rank-2 tensors.
  Both pick up factor (+1)² = +1.

BOTH POLARIZATIONS ARE EVEN UNDER SPATIAL REFLECTION!

This is the same conclusion as before:
  - The Z₂ does not distinguish between h_+ and h_×
  - Both polarizations survive
  - No factor of 1/2 from polarization counting
""")


# =============================================================================
# PART 5: WHERE DOES Z² COME FROM?
# =============================================================================

print("""
PART 5: WHERE DOES THE Z² IN THE DENOMINATOR COME FROM?
=======================================================

The claim r = 1/(2Z²) has Z² = 32π/3 in the denominator.

In standard slow-roll inflation:
  r = 16ε

For r = 1/(2Z²) = 0.0149, we would need:
  ε = r/16 = 0.0149/16 = 0.000931

QUESTION: Does Z² framework predict ε = 1/(32Z²)?

Let's check the slow-roll parameter:
  ε = (M_Pl²/2) × (V'/V)²

This depends on the inflaton potential V(φ).

PROBLEM: The Z² framework does NOT specify a unique inflaton potential!

The Z² constant appears in:
  - Fine structure: α = 1/(4πZ²) ← Different context
  - Dark energy: Ω_Λ/Ω_m = 13/6 ← Derived from Z²
  - MOND: a₀ = cH/Z ← Derived from Z²

But there is NO derivation showing why the INFLATON POTENTIAL
should have V'/V related to Z².

THE Z² IN THE DENOMINATOR IS NOT DERIVED FROM FIRST PRINCIPLES!
""")


# =============================================================================
# PART 6: COULD r = 1/(2Z²) BE RIGHT FOR OTHER REASONS?
# =============================================================================

print("""
PART 6: COULD r = 1/(2Z²) BE CORRECT FOR OTHER REASONS?
=======================================================

Let's explore if there's ANY valid derivation that could give r = 1/(2Z²).

OPTION A: Specific Inflaton Potential
-------------------------------------
If the Z² framework DICTATED a specific inflaton potential V(φ),
then ε could be determined, giving a specific r.

But the framework doesn't specify V(φ).

OPTION B: Quantum Corrections from Orbifold
-------------------------------------------
The T³/Z₂ orbifold might give quantum corrections to the inflationary
dynamics. These could modify r.

But this would need explicit calculation, which hasn't been done.

OPTION C: Numerology / Coincidence
----------------------------------
Perhaps r ≈ 0.015 just happens to be close to 1/(2Z²).

Current constraint: r < 0.034
Z² prediction: r = 0.015

If r is eventually measured to be, say, 0.02 or 0.01, the 1/(2Z²)
formula would be falsified.

OPTION D: Mode Normalization on Compact Space
---------------------------------------------
On a compact manifold, the normalization of modes is different.
This could affect the overall amplitude of perturbations.

But this would affect P_T and P_S equally, leaving r unchanged.

CONCLUSION: No valid derivation of r = 1/(2Z²) has been found.
""")


# =============================================================================
# PART 7: HONEST ASSESSMENT
# =============================================================================

print("""
PART 7: HONEST ASSESSMENT
=========================

CLAIM: r = 1/(2Z²) = 0.0149

ANALYSIS OF DERIVATION:
-----------------------

1. "Factor of 1/2 from Z₂ mode counting"

   STATUS: ❌ INVALID

   REASON: Both scalar and tensor perturbations transform the SAME way
   under the Z₂ spatial reflection. The ratio r = P_T/P_S is unchanged.

2. "Z² normalization gives 1/Z² factor"

   STATUS: ❌ NOT DERIVED

   REASON: There is no first-principles derivation connecting Z² = 32π/3
   to the inflaton potential or slow-roll parameters.

3. "Combined gives r = 1/(2Z²)"

   STATUS: ❌ NOT ESTABLISHED

   REASON: Neither factor has a valid derivation.

VERDICT:
--------
The prediction r = 1/(2Z²) = 0.0149 is NOT rigorously derived.

It appears to be:
  - An assumption, not a derivation
  - Possibly numerology (Z² appears elsewhere, so include it here)
  - Consistent with current data (r < 0.034), so not falsified YET
""")


# =============================================================================
# PART 8: WHAT CAN WE ACTUALLY SAY?
# =============================================================================

print("""
PART 8: WHAT CAN Z² ACTUALLY PREDICT ABOUT r?
=============================================

WHAT Z² TOPOLOGY DOES PREDICT:
------------------------------

1. Mode discretization: k = 2πn/L (from finite topology)
   - Affects low-ℓ CMB (which we observe!)
   - Does NOT change r

2. Both polarizations exist: h_+ ≠ 0 and h_× ≠ 0
   - We just proved this
   - Does NOT change r

3. Cosmic topology at L ~ 12-14 Gpc
   - Explains quadrupole suppression
   - Explains missing large-angle correlations
   - Does NOT directly predict r

WHAT Z² DOES NOT PREDICT (without additional assumptions):
----------------------------------------------------------

1. The specific inflaton potential V(φ)
2. The slow-roll parameter ε
3. The tensor-to-scalar ratio r

HONEST CONCLUSION:
------------------
Without specifying an inflaton potential, the Z² framework
CANNOT predict a specific value of r.

The claim r = 1/(2Z²) is an ADDITIONAL HYPOTHESIS, not a derivation.
""")


# =============================================================================
# PART 9: COMPARISON TABLE
# =============================================================================

print("""
PART 9: COMPARISON - h_× = 0 vs r = 1/(2Z²)
===========================================

| Aspect                | h_× = 0           | r = 1/(2Z²)       |
|-----------------------|-------------------|-------------------|
| Claim                 | Cross-pol = 0     | Tensor/scalar     |
| Stated reason         | Z₂ projects out   | Z₂ mode counting  |
| Actual Z₂ action      | y → -y (extra dim)| x → -x (space)    |
| Transformation        | h_μν is EVEN      | h_ij is EVEN      |
| Affects both pols?    | No (both survive) | N/A               |
| Affects both S/T?     | N/A               | Yes (equally)     |
| Changes ratio?        | N/A               | NO                |
| Derivation status     | ❌ WRONG          | ❌ NOT DERIVED    |
| Should be removed?    | YES               | PROBABLY YES      |

BOTH predictions suffer from similar problems:
  - Claimed Z₂ action doesn't do what the derivation says
  - The mathematical reasoning has gaps
  - The predictions are ASSUMED, not DERIVED
""")


# =============================================================================
# PART 10: RECOMMENDATION
# =============================================================================

print("""
══════════════════════════════════════════════════════════════════════
PART 10: RECOMMENDATION
══════════════════════════════════════════════════════════════════════

FINDING: r = 1/(2Z²) is NOT a valid first-principles prediction.

REASONS:
1. The Z₂ mode counting argument is invalid (affects S and T equally)
2. The Z² normalization is not derived from the framework
3. No inflaton potential is specified that would give ε = 1/(32Z²)

OPTIONS:

OPTION A: REMOVE THE PREDICTION
  - Most honest approach
  - r becomes "not predicted" by Z²
  - LiteBIRD result won't test Z² (for r)

OPTION B: REFRAME AS HYPOTHESIS
  - State r = 0.015 as a GUESS, not a derivation
  - Acknowledge it's consistent with data but not derived
  - Wait for LiteBIRD to see if it's correct

OPTION C: DERIVE A SPECIFIC INFLATON POTENTIAL
  - If Z² dictates a specific V(φ), then r could be derived
  - This requires new theoretical work
  - Would make r a genuine prediction

RECOMMENDATION:
---------------
Similar to h_× = 0, the r = 1/(2Z²) prediction should be MARKED AS
UNVERIFIED until a rigorous derivation is found.

It should NOT be listed as a "prediction" of the Z² framework without
acknowledging that it is not derived from first principles.

══════════════════════════════════════════════════════════════════════
""")


# =============================================================================
# SUMMARY
# =============================================================================

Z2 = 32 * np.pi / 3
r_claimed = 1 / (2 * Z2)

print(f"""
SUMMARY
=======

CLAIMED PREDICTION:
  r = 1/(2Z²) = 1/(2 × {Z2:.6f}) = {r_claimed:.6f}

CURRENT OBSERVATIONAL CONSTRAINT:
  r < 0.034 (95% CL, Planck + BICEP/Keck 2018)

DERIVATION STATUS - EXAMINING EXISTING DOCUMENTS:
=================================================

From perturbation_theory.md (line 180-188):
  "h_+ → h_+  (even)
   h_× → -h_× (odd)
   The Z₂ projection eliminates h_× at the fundamental level."

From HONEST_DERIVATION_AUDIT.md (line 266-271):
  "Tensor modes halved → r ∝ 1/Z²
   Factor 1/2 from orbifold projection"

PROBLEM: THE r = 1/(2Z²) DERIVATION RELIES ON h_× BEING PROJECTED OUT!

We just rigorously proved (kaluza_klein_reduction_rigorous.py) that:
  - The Z₂ acts on EXTRA dimensions: y → -y
  - h_μν has indices in {{0,1,2,3}} only
  - Both h_+ and h_× are Z₂-EVEN
  - NEITHER is projected out

Therefore:
  ❌ Factor of 1/2: INVALID (relies on h_× projection, which is wrong)
  ❌ Factor of 1/Z² from ε: NOT DERIVED (stated without proof)
  ❌ Overall: THE DERIVATION IS FLAWED

VERDICT:
  The r = 1/(2Z²) prediction relies on the SAME ERROR as h_× = 0.
  Both predictions claim the Z₂ projects out one GW polarization.
  This is WRONG - the Z₂ acts on extra dimensions, not 4D polarizations.

WHAT REMAINS VALID:
  - Z² framework does NOT predict a specific r (without additional input)
  - The inflaton potential is NOT specified → ε is NOT determined
  - r could be anything consistent with slow-roll constraints

IMPLICATIONS FOR Z² FRAMEWORK:
  - Two major "predictions" are now RETRACTED:
    * h_× = 0 (WRONG)
    * r = 1/(2Z²) (WRONG - same error)

  - The remaining STRONG predictions are:
    * Ω_Λ/Ω_m = 13/6 (excellent match, 0.1σ)
    * Quadrupole suppression (explains CMB anomaly)
    * a₀ = cH/Z (matches MOND)
    * α⁻¹ = 4Z² + 3 (from index theorem)

  - The framework is NOT falsified, but is less predictive than claimed
  - GW tests (polarization and tensor-to-scalar) are NO LONGER APPLICABLE
""")
