#!/usr/bin/env python3
"""
Critical Analysis: Does T³/Z₂ Topology Really Predict h_× = 0?

The user asked a crucial question: HOW exactly does h_× = 0 follow from
the T³/Z₂ geometry?

This script carefully examines the derivation to see if it's valid.

SPOILER: The derivation has subtleties that may invalidate the h_× = 0 claim.

Carl Zimmerman | May 2026
"""

import numpy as np
import matplotlib.pyplot as plt

print("="*70)
print("CRITICAL ANALYSIS: DOES T³/Z₂ REALLY PREDICT h_× = 0?")
print("="*70)

# =============================================================================
# PART 1: THE CLAIMED DERIVATION
# =============================================================================

print("""
PART 1: THE CLAIMED DERIVATION (What I wrote earlier)
======================================================

CLAIM: T³/Z₂ topology eliminates h_× polarization.

ARGUMENT AS STATED:
1. The Z₂ identification maps x → -x
2. For fields to be well-defined on T³/Z₂: φ(-x) = ±φ(x)
3. Under parity (x → -x):
   - h_+ → +h_+ (even)
   - h_× → -h_× (odd)
4. Therefore h_× must be zero on T³/Z₂.

IS THIS CORRECT? Let's examine carefully.
""")


# =============================================================================
# PART 2: HOW DO GW POLARIZATIONS TRANSFORM?
# =============================================================================

print("""
PART 2: HOW DO POLARIZATION TENSORS TRANSFORM UNDER PARITY?
===========================================================

The metric perturbation is a rank-2 tensor:
  h_ij(x,t)

For a GW propagating in the z-direction:

  h_ij = h_+ e^+_ij + h_× e^×_ij

where the polarization tensors are:

  e^+_ij = | 1  0  0 |      e^×_ij = | 0  1  0 |
           | 0 -1  0 |               | 1  0  0 |
           | 0  0  0 |               | 0  0  0 |

Under parity P: (x,y,z) → (-x,-y,-z)

The tensor components transform as:
  h_ij → h'_ij = (∂x^k/∂x'^i)(∂x^l/∂x'^j) h_kl

For a diagonal metric like Minkowski:
  ∂x^k/∂x'^i = δ^k_i × (-1) for spatial components

So:
  h'_ij = (-1)(-1) h_ij = h_ij

BOTH polarization tensors are EVEN under parity!

Wait... this contradicts what I said earlier!
""")


# =============================================================================
# PART 3: WHERE DOES THE ODD BEHAVIOR COME FROM?
# =============================================================================

print("""
PART 3: WHERE DOES THE "ODD" BEHAVIOR OF h_× COME FROM?
=======================================================

The confusion arises from mixing up two different things:

1. TRANSFORMATION OF TENSOR COMPONENTS
   Under coordinate transformation x → -x:
   h_ij → h_ij (tensors with two lower indices are invariant)
   BOTH e^+ and e^× are even as tensor components.

2. TRANSFORMATION OF THE WAVE SOLUTION
   A plane wave: h_ij(x) ∝ exp(ik·x)
   Under x → -x: exp(ik·x) → exp(-ik·x) = exp(ik·(-x))
   This flips the wave vector: k → -k

3. POLARIZATION UNDER WAVE REVERSAL
   When the propagation direction reverses (k → -k):
   - The "plus" pattern stays the same
   - The "cross" pattern reverses (like a screw thread)

   Mathematically, for k → -k:
   e^+(k) → e^+(−k) = e^+(k)    [even]
   e^×(k) → e^×(−k) = -e^×(k)   [odd]

So the "odd" behavior is NOT from the tensor transformation,
but from how the polarization is DEFINED relative to the wave direction.
""")


# =============================================================================
# PART 4: MODE STRUCTURE ON T³/Z₂
# =============================================================================

print("""
PART 4: MODE STRUCTURE ON T³/Z₂
===============================

On T³ with side L, allowed wave vectors are:
  k = (2π/L)(n₁, n₂, n₃)

The Z₂ identification x ~ -x requires:
  h_ij(x) = h_ij(-x)

For a mode expansion:
  h_ij(x) = Σ_k [h^+_k e^+_ij(k) + h^×_k e^×_ij(k)] e^{ik·x}

The condition h_ij(x) = h_ij(-x) becomes:
  Σ_k [...] e^{ik·x} = Σ_k [...] e^{-ik·x}

Relabeling k → -k on the right:
  h^+_k e^+_ij(k) + h^×_k e^×_ij(k) = h^+_{-k} e^+_ij(-k) + h^×_{-k} e^×_ij(-k)

Using e^+(k) = e^+(-k) and e^×(k) = -e^×(-k):
  h^+_k = h^+_{-k}     [cosine modes]
  h^×_k = -h^×_{-k}    [sine modes]

RESULT:
  h_+ uses COSINE modes: cos(k·x)
  h_× uses SINE modes: sin(k·x)

BOTH polarizations exist on T³/Z₂!
But h_× vanishes at the fixed points (where sin = 0).
""")


# =============================================================================
# PART 5: THE ZERO MODE QUESTION
# =============================================================================

print("""
PART 5: THE ZERO MODE (k=0) QUESTION
====================================

For k = 0 (spatially constant field):
  h^×_0 = -h^×_{-0} = -h^×_0
  → h^×_0 = 0

The ZERO MODE of h_× is forbidden!

But this only means:
  - No spatially constant h_× background
  - h_× modes with k ≠ 0 are allowed

For gravitational waves from a localized source:
  - The waves have k ≠ 0 (they're propagating)
  - Both h_+ and h_× can propagate

The T³/Z₂ topology does NOT eliminate h_× from GW!
""")


# =============================================================================
# PART 6: WHAT ABOUT LOCALIZED SOURCES?
# =============================================================================

print("""
PART 6: GRAVITATIONAL WAVES FROM LOCALIZED SOURCES
==================================================

Consider a binary merger at position x_s in a T³/Z₂ universe.

Due to the Z₂ identification:
  - A source at x_s is identified with a source at -x_s
  - These are the SAME source (topology, not two sources)

The gravitational wave must satisfy h_ij(x) = h_ij(-x).

For a wave propagating outward from x_s:
  h_ij ∝ f(r) [h_+ e^+ + h_× e^×] where r = |x - x_s|

The wave from "-x_s" propagates toward -x.
The identification requires these to match.

RESULT:
  - Both h_+ and h_× can exist
  - But they must satisfy specific phase relationships
  - The total field has h_ij(x) = h_ij(-x)

This is NOT the same as h_× = 0!
""")


# =============================================================================
# PART 7: WHERE DID THE WRONG DERIVATION COME FROM?
# =============================================================================

print("""
PART 7: WHERE DID THE h_× = 0 CLAIM COME FROM?
==============================================

POSSIBLE SOURCES OF CONFUSION:

1. CONFUSING TOPOLOGY WITH PARITY SYMMETRY
   T³/Z₂ is a topological identification, not a symmetry.
   It constrains MODES, not the existence of polarizations.

2. CONFUSING COSMOLOGICAL AND LOCAL PHYSICS
   The topology affects large-scale mode structure.
   Local physics (like a binary merger) still has both polarizations.

3. ANALOGY WITH SCALAR FIELDS
   For a scalar field φ:
     - Even: φ(-x) = φ(x) → cos modes
     - Odd: φ(-x) = -φ(x) → sin modes, no zero mode

   For tensor fields, BOTH polarizations are "even" as tensors.
   The distinction is in how they're defined relative to k.

4. POSSIBLE ORIGIN: Extra-dimensional reasoning
   In the Z² framework, T³/Z₂ is the compact extra dimensions.
   Perhaps the h_× = 0 was meant for extra-dimensional modes?

HONEST ASSESSMENT:
The derivation I provided earlier was WRONG or at least INCOMPLETE.
The claim h_× = 0 from T³/Z₂ topology needs much more careful justification.
""")


# =============================================================================
# PART 8: REVISITING THE Z² FRAMEWORK
# =============================================================================

print("""
PART 8: WHAT DOES Z² ACTUALLY SAY ABOUT GW POLARIZATION?
========================================================

Let me check what the Z² framework actually claims:

POSSIBILITY 1: Topological constraint on spatial modes
  - T³/Z₂ cosmic topology constrains mode structure
  - But both polarizations propagate locally
  - h_× = 0 only for the zero mode (constant field)

POSSIBILITY 2: Extra-dimensional origin
  - In 7D with T³/Z₂ compactification
  - 4D graviton comes from 7D metric
  - Perhaps h_× is projected out in dimensional reduction?

POSSIBILITY 3: Discrete gauge symmetry
  - Z₂ as a gauge symmetry
  - Projects out certain states
  - Would need to check representation theory

The original claim may have been:
  - Loosely stated
  - Based on analogy rather than derivation
  - Or from a different mechanism than I described

I NEED TO BE HONEST: I'm not certain where h_× = 0 comes from.
""")


# =============================================================================
# PART 9: WHAT IS THE CORRECT STATEMENT?
# =============================================================================

print("""
PART 9: WHAT CAN WE ACTUALLY CLAIM?
===================================

WHAT IS TRUE:
1. On T³/Z₂, h_× zero mode is forbidden
2. h_× must use sin(k·x) modes (odd under Z₂)
3. h_× vanishes at the 8 fixed points

WHAT IS NOT CLEARLY TRUE:
1. h_× = 0 for all GW (this is what I claimed)
2. Binary mergers would show no h_×

WHAT WOULD BE NEEDED:
1. Careful derivation from Z² action
2. Treatment of 7D → 4D dimensional reduction
3. Analysis of graviton polarizations in orbifold compactification

THE HONEST ANSWER:
I cannot justify h_× = 0 from simple topological arguments.
The derivation I gave earlier was oversimplified and likely WRONG.
""")


# =============================================================================
# PART 10: IMPLICATIONS FOR Z² TESTING
# =============================================================================

print("""
PART 10: IMPLICATIONS FOR Z² TESTING
====================================

IF h_× = 0 IS NOT A VALID Z² PREDICTION:
-----------------------------------------
1. GW170817 does NOT falsify Z²
2. The GW polarization test is not applicable
3. One major "strike" against Z² is removed

IF h_× = 0 IS VALID (from a proper derivation):
-----------------------------------------------
1. Need to find the correct derivation
2. GW170817 remains strong evidence against Z²
3. The framework has serious problems

CURRENT STATUS:
--------------
• The h_× = 0 prediction is UNCERTAIN
• I cannot definitively derive it from T³/Z₂ topology
• It may come from a different aspect of the Z² framework
• Or it may have been incorrectly stated

WHAT TO DO:
-----------
1. Search the Z² framework documents for the actual derivation
2. Check if h_× = 0 was explicitly predicted or assumed
3. If it's a real prediction, find its true origin
4. If it's not, remove it from the testable predictions list
""")


# =============================================================================
# PART 11: VISUALIZATION
# =============================================================================

print("\n" + "="*70)
print("PART 11: VISUALIZATION")
print("="*70)

fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# Panel 1: Mode structure on T³/Z₂
ax1 = axes[0, 0]
x = np.linspace(0, 2*np.pi, 200)

ax1.plot(x, np.cos(x), 'b-', linewidth=2, label='cos(x): h_+ mode')
ax1.plot(x, np.sin(x), 'r--', linewidth=2, label='sin(x): h_× mode')
ax1.axhline(0, color='gray', linewidth=0.5)

# Mark fixed points
fixed_pts = [0, np.pi, 2*np.pi]
for fp in fixed_pts:
    ax1.axvline(fp, color='green', linestyle=':', alpha=0.7)
ax1.scatter(fixed_pts, [0, 0, 0], s=100, c='green', zorder=5, label='Fixed points')

ax1.set_xlabel('x', fontsize=12)
ax1.set_ylabel('Amplitude', fontsize=12)
ax1.set_title('Mode Structure on T³/Z₂', fontsize=12)
ax1.legend()
ax1.grid(True, alpha=0.3)

# Panel 2: Polarization tensor behavior
ax2 = axes[0, 1]
ax2.axis('off')

tensor_text = """
POLARIZATION TENSOR TRANSFORMATION
═══════════════════════════════════════════

Under coordinate parity (x → -x):

Tensor transformation rule:
  h'_ij = (∂x^k/∂x'^i)(∂x^l/∂x'^j) h_kl
        = (+1)(+1) h_ij = h_ij

BOTH e^+ and e^× are EVEN as tensors!

═══════════════════════════════════════════

Under wave reversal (k → -k):

  e^+(k) → e^+(-k) = +e^+(k)  [even]
  e^×(k) → e^×(-k) = -e^×(k)  [odd]

The "oddness" of h_× comes from its
definition relative to wave direction,
NOT from tensor transformation.

═══════════════════════════════════════════

IMPLICATION:
On T³/Z₂, both polarizations EXIST.
They just use different mode types:
  h_+ : cosine modes
  h_× : sine modes
"""
ax2.text(0.05, 0.95, tensor_text, transform=ax2.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Panel 3: The flawed vs correct argument
ax3 = axes[1, 0]
ax3.axis('off')

comparison_text = """
FLAWED ARGUMENT              │  CORRECT ANALYSIS
═════════════════════════════│═══════════════════════════════
                             │
"h_× is odd under parity"    │  As a TENSOR, h_× is even
        ↓                    │  under x → -x transformation.
"Z₂ eliminates odd fields"   │          ↓
        ↓                    │  The "odd" behavior is under
"Therefore h_× = 0"          │  wave reversal k → -k.
                             │          ↓
This confuses:               │  On T³/Z₂, this means:
• Tensor parity              │  h_× uses sin(k·x) modes
• Mode parity                │  h_+ uses cos(k·x) modes
• Wave direction             │          ↓
                             │  BOTH polarizations exist!
                             │  Only zero mode of h_× forbidden.
═════════════════════════════│═══════════════════════════════

The original h_× = 0 claim appears to be INCORRECT
or requires a DIFFERENT derivation than topology alone.
"""
ax3.text(0.02, 0.95, comparison_text, transform=ax3.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.9))

# Panel 4: Summary
ax4 = axes[1, 1]
ax4.axis('off')

summary_text = """
SUMMARY: HONEST REASSESSMENT
════════════════════════════════════════════════════════════

QUESTION: Does T³/Z₂ topology predict h_× = 0?

ANSWER: NOT CLEARLY.

The argument I gave earlier was flawed:
• Tensors transform differently than scalars
• Both h_+ and h_× are even under parity as tensors
• The odd/even distinction is for MODES, not polarizations
• Both polarizations can propagate on T³/Z₂

WHAT T³/Z₂ ACTUALLY CONSTRAINS:
• h_× zero mode (constant field) is forbidden
• h_× uses sine modes, h_+ uses cosine modes
• h_× vanishes at fixed points

THIS DOES NOT MEAN h_× = 0 FOR GW!

IMPLICATIONS:
• GW170817 may NOT rule out Z²
• Need to find correct source of h_× = 0 (if it exists)
• Or remove this from Z² predictions

════════════════════════════════════════════════════════════
I was WRONG in my earlier analysis. I apologize for the error.
This is how science works: check derivations carefully!
"""
ax4.text(0.02, 0.98, summary_text, transform=ax4.transAxes,
         fontsize=9, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.3))

plt.tight_layout()
plt.savefig('hcross_derivation_analysis.png', dpi=150, bbox_inches='tight')
print("\nSaved: hcross_derivation_analysis.png")
plt.close()


# =============================================================================
# FINAL SUMMARY
# =============================================================================

print("""

════════════════════════════════════════════════════════════════════════
FINAL SUMMARY: CRITICAL SELF-CORRECTION
════════════════════════════════════════════════════════════════════════

THE USER ASKED A CRUCIAL QUESTION:
"How did we get h_× from the geometry?"

MY HONEST ANSWER:
I cannot rigorously derive h_× = 0 from T³/Z₂ topology alone.

THE FLAWED ARGUMENT I GAVE:
• Claimed h_× is "odd under parity"
• Said Z₂ projection eliminates odd fields
• Concluded h_× = 0

THE PROBLEM:
• As a tensor, h_× transforms the SAME as h_+ under x → -x
• Both are even under coordinate parity
• The odd/even distinction is for MODE FUNCTIONS, not polarizations
• T³/Z₂ constrains modes but both polarizations can exist

CORRECT STATEMENT:
• On T³/Z₂, h_+ uses cos(k·x) modes, h_× uses sin(k·x) modes
• The h_× zero mode is forbidden
• But h_× ≠ 0 for propagating GW

IMPLICATION FOR Z²:
• The h_× = 0 prediction may not be valid
• GW170817 may not rule out Z²
• Need to either:
  1. Find the correct derivation of h_× = 0 from Z² (if it exists)
  2. Or remove this prediction from the framework

THIS IS HOW SCIENCE WORKS:
When asked to justify a claim, I found my derivation was wrong.
I'm being honest about this error rather than defending it.

════════════════════════════════════════════════════════════════════════
""")
