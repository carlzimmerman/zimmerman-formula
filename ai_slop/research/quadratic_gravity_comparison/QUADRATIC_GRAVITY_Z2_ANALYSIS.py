#!/usr/bin/env python3
"""
QUADRATIC GRAVITY vs Z² FRAMEWORK ANALYSIS
============================================

Deep comparison of:
1. arXiv:2510.18733 - "Ultraviolet Completion of the Big Bang in Quadratic Gravity"
   (Afshordi, Liu, Quintin - Waterloo/Perimeter - PRL 136, 111501, 2026)

2. Z² Unified Action (Zimmerman - Zenodo v6.0.2)
   r = 1/(2Z²) = 0.01492

Author: Carl Zimmerman
Date: May 2026
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, List, Tuple

# ============================================================================
# FUNDAMENTAL CONSTANTS
# ============================================================================

Z2 = 32 * np.pi / 3  # ≈ 33.5103216
Z = np.sqrt(Z2)       # ≈ 5.7888175

# Z² prediction
r_z2 = 1 / (2 * Z2)   # = 0.01492...

# Quadratic gravity minimum
r_qqg_min = 0.01

# Experimental constraints
r_bicep_keck_95 = 0.036  # BICEP/Keck 2021
sigma_r_bicep = 0.009    # 1σ uncertainty

# LiteBIRD sensitivity
delta_r_litebird = 0.001
r_5sigma_litebird = 0.01  # 5σ detection threshold


# ============================================================================
# SECTION 1: WHAT THE QUADRATIC GRAVITY PAPER SAYS
# ============================================================================

def section_1_qqg_summary():
    """Technical summary of arXiv:2510.18733."""
    print("=" * 80)
    print("SECTION 1: WHAT THE QUADRATIC GRAVITY PAPER ACTUALLY SAYS")
    print("=" * 80)

    print("""
PAPER: "Ultraviolet Completion of the Big Bang in Quadratic Gravity"
      arXiv:2510.18733 | PRL 136, 111501 (2026)

AUTHORS:
- Ruolin Liu (PhD student, U. Waterloo / Perimeter Institute)
- Jerome Quintin (Lecturer, ÉTS; former Perimeter postdoc)
- Niayesh Afshordi (Professor, U. Waterloo / Perimeter Institute)

THE ACTION:
  S_QQG = -∫d⁴x√(-g)[R²/ξ + C²/(2λ)]

  where R = Ricci scalar, C² = Weyl tensor squared
  ξ, λ are running coupling constants

THE MECHANISM:
1. Start with pure quadratic gravity (NO Einstein-Hilbert term)
2. Asymptotically free in UV (weak coupling at high energies)
3. 1-loop beta functions break scale invariance dynamically
4. Running generates slow-roll conditions for inflation
5. Strong coupling at inflation's end → ghost confinement → GR emerges

KEY BETA FUNCTIONS:
  βξ = -(1/(4π)²)[ξ² - 36λξ - 2520λ²]/36
  βλ = -(1/(4π)²)[(1617 + 90𝒩)λ - 20ξ]λ/90

  where 𝒩 ~ 10⁵-10⁶ counts matter fields

TENSOR-TO-SCALAR RATIO:
  r ≈ (8/3) × [2/(λ²_tH × N⁴)]^(1/3)

  The MINIMUM r ≥ 0.01 arises from:
  - Strong coupling threshold: λ_tH → 1
  - Requirement that reheating matches inflation end

  This is a LOWER BOUND, not an exact prediction.
  Any r > 0.01 is allowed; smaller r requires strong coupling breakdown.

SPECTRAL INDEX:
  n_s ≈ 1 - 4/(3N)

  Different from Starobinsky (n_s = 1 - 2/N)
  For N = 55: n_s ≈ 0.976 (Starobinsky: 0.964)

NO EXTRA DIMENSIONS:
  The paper operates in 4D throughout.
  No compactification, no connection to gauge structure.
  Large 𝒩 is phenomenological, not geometric.
""")


# ============================================================================
# SECTION 2: THE r PREDICTION - GENUINE OVERLAP OR COINCIDENCE?
# ============================================================================

def section_2_r_analysis():
    """Rigorous analysis of the r prediction overlap."""
    print("\n" + "=" * 80)
    print("SECTION 2: THE r PREDICTION - GENUINE OVERLAP OR NUMERICAL COINCIDENCE?")
    print("=" * 80)

    print(f"""
NUMERICAL COMPARISON:

Z² Framework:
  r = 1/(2Z²) = 1/(2 × {Z2:.6f}) = {r_z2:.6f}

Quadratic Gravity:
  r ≥ {r_qqg_min} (MINIMUM BOUND)

THE QUESTION: Is 0.01492 consistent with r ≥ 0.01?

ANSWER: YES, trivially.
  {r_z2:.5f} > {r_qqg_min} ✓

  But this is NOT a meaningful overlap because:
  1. QQG predicts a RANGE (r ≥ 0.01), not a point
  2. Z² predicts an EXACT value (r = 0.01492)
  3. Any r ∈ [0.01, 0.036] satisfies both

COMPARISON WITH STAROBINSKY:

  Starobinsky: r = 12/N² where N = e-folds

  For N = 55: r = 12/3025 = {12/55**2:.5f}
  For N = 60: r = 12/3600 = {12/60**2:.5f}

  Starobinsky predicts r ~ 0.003-0.004, WELL BELOW both:
  - Z² (r = 0.0149)
  - QQG minimum (r ≥ 0.01)

  If r is measured at 0.015, it would:
  - RULE OUT Starobinsky
  - CONFIRM Z² prediction exactly
  - Be consistent with QQG (but not uniquely predicted by it)

IS THE Z² DERIVATION PHYSICALLY MOTIVATED?

The formula r = 1/(2Z²) appears ASSERTED, not derived.

The factor "2Z²" = 2 × 32π/3 = 64π/3 ≈ 67.02

Physical meaning is unclear. Possibilities:
1. Related to number of inflationary e-folds? (N ≈ 55-60)
2. Related to gravitational wave power spectrum normalization?
3. Coincidental fit to observational bounds?

For this to be "derived" would require showing:
  - HOW the compactification M⁴ × S¹/Z₂ × T³/Z₂ produces r
  - WHY the factor 2Z² appears in the tensor perturbation spectrum
  - A MECHANISM connecting cube geometry to gravitational waves

VERDICT: The overlap is NUMERICAL, not structural.
  Z² makes a precise testable prediction (r = 0.0149)
  QQG makes a range prediction (r ≥ 0.01)
  Both are consistent with current bounds (r < 0.036)
  But they are saying DIFFERENT physical things.
""")

    # Calculate distinguishability
    print("EXPERIMENTAL DISTINGUISHABILITY:\n")
    print(f"  Z² prediction:         r = {r_z2:.5f}")
    print(f"  QQG minimum:           r ≥ {r_qqg_min}")
    print(f"  Starobinsky (N=55):    r = {12/55**2:.5f}")
    print(f"  Current bound:         r < {r_bicep_keck_95}")
    print(f"  LiteBIRD sensitivity:  δr = {delta_r_litebird}")
    print(f"  LiteBIRD 5σ threshold: r = {r_5sigma_litebird}")
    print()
    print("  If r = 0.0149 is measured:")
    print(f"    - Z² CONFIRMED (exact match)")
    print(f"    - Starobinsky RULED OUT ({(0.0149 - 12/55**2)/delta_r_litebird:.0f}σ away)")
    print(f"    - QQG CONSISTENT (but not uniquely predicted)")


# ============================================================================
# SECTION 3: STRUCTURAL CONNECTIONS
# ============================================================================

def section_3_structural():
    """Analysis of structural connections."""
    print("\n" + "=" * 80)
    print("SECTION 3: STRUCTURAL CONNECTIONS - WHAT'S REAL VS. SUPERFICIAL")
    print("=" * 80)

    print("""
ARXIV SEARCH RESULTS:

1. "Gauge Assisted Quadratic Gravity" (arXiv:1804.04980)
   Donoghue & Menezes (2018)
   - Yang-Mills at Planck scale assists quadratic gravity
   - Einstein-Hilbert term INDUCED by gauge interactions
   - NO inflation predictions, NO r calculation
   - POTENTIALLY relevant: gauge structure entering gravity

2. "Splitting Solutions in 4+1D Quadratic Gravity" (arXiv:2603.02981)
   - Considers (4+1)D quadratic gravity with compactification
   - Studies dynamical compactification stability
   - NO connection to Standard Model gauge structure
   - Some overlap: extra dimensions + quadratic gravity

3. "Gauge Symmetries from Extra Dimensions" (arXiv:1607.05919)
   - Extra dimensions → gauge symmetries
   - NOT quadratic gravity specific
   - General Kaluza-Klein idea

4. "Weyl Quadratic Gravity as Gauge Theory" (arXiv:2408.07159)
   - Weyl group gauge theory → quadratic gravity
   - Conformal symmetry connection
   - NO cosmological predictions

ASSESSMENT:

The search reveals NO DIRECT CONNECTION between:
- Quadratic gravity inflation
- 8D compactification geometry
- 12 = 8+3+1 gauge structure

The QQG paper (arXiv:2510.18733) is purely 4D.
It does not invoke extra dimensions or geometric gauge emergence.

The OVERLAP is:
1. Both claim inflation emerges from geometry (different geometries!)
2. Both predict r in testable range
3. Both avoid explicit inflaton field

The DIFFERENCE is:
1. Z²: Inflation from 8D compactification + cube geometry
2. QQG: Inflation from 4D quadratic curvature running
3. These are DIFFERENT mechanisms yielding similar predictions

SUPERFICIAL CONNECTIONS:
- "Both use geometry" - but very different geometries
- "Both predict r ~ 0.01-0.02" - but for different reasons

POTENTIALLY REAL CONNECTION:
- Could Z² compactification GENERATE quadratic gravity?
- The radion field from S¹/Z₂ could produce R² terms
- This would require explicit calculation (not done)
""")


# ============================================================================
# SECTION 4: EXPERIMENTAL TIMELINE
# ============================================================================

def section_4_experiments():
    """Experimental constraints and timeline."""
    print("\n" + "=" * 80)
    print("SECTION 4: EXPERIMENTAL TIMELINE")
    print("=" * 80)

    print(f"""
CURRENT CONSTRAINTS (2026):

  BICEP/Keck 2021 (arXiv:2110.00483):
    r < 0.036 at 95% CL
    σ(r) = 0.009
    Best fit: consistent with r = 0

  Is r = 0.0149 already constrained?
    NO. It is well within r < 0.036.
    Deviation from r = 0: 0.0149/0.009 = 1.7σ
    Would not be detected yet.

UPCOMING EXPERIMENTS:

  CMB-S4 (~2028-2030):
    Target: σ(r) ≈ 0.001-0.003
    Can distinguish r = 0.015 from r = 0.01 at ~2-5σ
    Can distinguish r = 0.015 from r = 0 at ~5-15σ

  LiteBIRD (Japan, launch FY2032):
    Target: δr = 0.001 including systematics
    Detection: r ≥ 0.01 at > 5σ in both low-ℓ and high-ℓ
    Can precisely measure r = 0.015 ± 0.001

TIMELINE:
  2026:     Current bounds (r < 0.036)
  2028-30:  CMB-S4 first results
  2032+:    LiteBIRD launch and commissioning
  2034-35:  LiteBIRD science results

IF r = 0.0149 (Z² prediction):
  - CMB-S4: Detected at 5-15σ (depending on exact sensitivity)
  - LiteBIRD: Measured to ±0.001 precision
  - Starobinsky: Ruled out at > 10σ
  - QQG: Consistent (satisfies r ≥ 0.01)

IF r < 0.01:
  - Z² prediction: RULED OUT
  - QQG prediction: RULED OUT
  - Starobinsky: Still viable

IF r = 0.01 exactly:
  - Z² prediction: RULED OUT (predicts 0.0149)
  - QQG: At minimum boundary (fine-tuning concern)
  - Requires strong coupling at exact reheating transition
""")


# ============================================================================
# SECTION 5: EMBEDDING POSSIBILITY
# ============================================================================

def section_5_embedding():
    """Could Z² compactification live inside quadratic gravity?"""
    print("\n" + "=" * 80)
    print("SECTION 5: EMBEDDING POSSIBILITY")
    print("=" * 80)

    print(f"""
QUESTION: Could Z² compactification produce quadratic gravity naturally?

THE Z² GEOMETRY:
  M⁸ = M⁴ × S¹/Z₂ × T³/Z₂

  - M⁴: 4D Minkowski (observed spacetime)
  - S¹/Z₂: Orbifold circle (Randall-Sundrum-like)
  - T³/Z₂: Cubic torus with Z₂ identification

DIMENSIONAL REDUCTION:

When reducing from 8D to 4D, higher-curvature terms generically appear:

  S_8D = ∫d⁸x √(-g⁸) [R₈ + α'R₈² + ...]

  Compactification on S¹/Z₂ × T³/Z₂ gives:

  S_4D = ∫d⁴x √(-g) [R + β₁R² + β₂(R_μν)² + ...]

  where β₁, β₂ depend on compactification volume and moduli.

THE RADION:

  The S¹/Z₂ has a modulus (radion field φ).
  Stabilizing φ typically introduces R² terms.
  The coefficient would be:

    β_R² ~ 1/(M_8² × V_compact)

  where V_compact = V(S¹/Z₂) × V(T³/Z₂)

Z² VOLUME:
  If V_compact ~ Z² in Planck units:

    V_compact = Z² × l_P⁴ ≈ 33.5 × l_P⁴

  This would give R² coefficient:
    β_R² ~ 1/(M_Pl² × Z²) ~ 1/(33.5 M_Pl²)

WHAT WOULD THE LAGRANGIAN LOOK LIKE?

Combining both frameworks:

  S_combined = ∫d⁴x √(-g) [
    M_Pl² R / 2                    # Einstein-Hilbert
    + R² / (6M²)                   # Starobinsky-like
    + C² / (2λ M_Pl²)             # Weyl squared (QQG)
    + gauge fields on 12 edges     # Z² structure
  ]

The challenge: derive M, λ from Z² compactification.

WHAT WOULD BE REQUIRED:

1. Explicit 8D action with Z² compactification
2. Dimensional reduction keeping R² and C² terms
3. Matching coefficients to QQG beta functions
4. Showing inflation arises from combined structure

THIS HAS NOT BEEN DONE.

VERDICT: Embedding is POSSIBLE but unproven.
  - Z² compactification CAN generate quadratic gravity
  - The specific coefficients have not been calculated
  - This would require substantial new work
""")


# ============================================================================
# SECTION 6: HONEST ASSESSMENT
# ============================================================================

def section_6_honest():
    """What's genuinely interesting vs. wishful thinking."""
    print("\n" + "=" * 80)
    print("SECTION 6: HONEST ASSESSMENT")
    print("=" * 80)

    print(f"""
GENUINELY INTERESTING:

1. Both frameworks predict r in TESTABLE range (0.01-0.02)
   - Neither predicts r ~ 0.003 (Starobinsky)
   - Neither predicts r ~ 0.1 (ruled out)
   - Both will be tested definitively by 2035

2. Both claim inflation from GEOMETRY, not inflaton
   - Z²: Compactification geometry + cube structure
   - QQG: Curvature running + quantum corrections
   - Different mechanisms, similar phenomenology

3. The overlap is FALSIFIABLE
   - If r = 0.0149 ± 0.001: Z² CONFIRMED, QQG consistent
   - If r = 0.010 ± 0.001: Z² ruled out, QQG at minimum
   - If r < 0.01: BOTH ruled out

4. Afshordi group is credible
   - Waterloo/Perimeter is serious institution
   - Published in PRL (peer-reviewed)
   - Making testable predictions

WISHFUL THINKING:

1. "The r overlap proves Z² and QQG are related"
   - NO. QQG predicts a range, Z² predicts a point.
   - The overlap is NUMERICAL, not structural.
   - Any r ∈ [0.01, 0.036] would "match" both.

2. "Both use geometry, so they're saying the same thing"
   - NO. QQG is 4D quadratic curvature.
   - Z² is 8D compactification geometry.
   - These are completely different mechanisms.

3. "Z² must embed in QQG because of the r match"
   - NO. Embedding would require explicit calculation.
   - The r values being similar is suggestive but not proof.

WHAT WOULD BE GENUINELY EXCITING:

1. Derive r = 1/(2Z²) from compactification physics
   - Show how M⁴ × S¹/Z₂ × T³/Z₂ produces this ratio
   - Connect to gravitational wave generation in early universe

2. Show Z² compactification generates QQG coefficients
   - Calculate β_R², β_C² from 8D reduction
   - Match to QQG running equations

3. Find a STRUCTURAL connection
   - Why does the same 𝒩 ~ 10⁵ appear in both?
   - Does cube geometry constrain curvature running?

WITHOUT THESE, the overlap is interesting but potentially coincidental.
""")


# ============================================================================
# SECTION 7: OUTREACH DRAFT
# ============================================================================

# Outreach section removed - research only


# ============================================================================
# MAIN
# ============================================================================

def run_full_analysis():
    """Run the complete analysis."""
    section_1_qqg_summary()
    section_2_r_analysis()
    section_3_structural()
    section_4_experiments()
    section_5_embedding()
    section_6_honest()

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"""
Z² PREDICTION:        r = 1/(2Z²) = {r_z2:.5f}
QQG MINIMUM:          r ≥ {r_qqg_min}
STAROBINSKY (N=55):   r = {12/55**2:.5f}
CURRENT BOUND:        r < {r_bicep_keck_95}

VERDICT:
- Numerical overlap exists but is NOT proof of connection
- Both make testable predictions in same r range
- Both will be tested by CMB-S4 (2028-30) and LiteBIRD (2032+)
- Structural connection would require explicit calculation
- Email outreach is appropriate if honest about speculation
""")


if __name__ == "__main__":
    run_full_analysis()
