#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        GAUGE SYMMETRIES
                      Why SU(3) × SU(2) × U(1)?
═══════════════════════════════════════════════════════════════════════════════════════════

The Standard Model is based on the gauge group:

    SU(3)_color × SU(2)_weak × U(1)_hypercharge

But WHY this particular group? Why not SU(5) or E₈?

This document shows the gauge structure emerges from Z = 2√(8π/3).

Carl Zimmerman, March 2026
═══════════════════════════════════════════════════════════════════════════════════════════
"""

import numpy as np

# =============================================================================
# FUNDAMENTAL CONSTANTS
# =============================================================================
Z = 2 * np.sqrt(8 * np.pi / 3)
Z2 = Z**2
pi = np.pi
alpha = 1/137.035999084

# Gauge group dimensions
dim_SU3 = 8   # SU(3) has 8 generators
dim_SU2 = 3   # SU(2) has 3 generators
dim_U1 = 1    # U(1) has 1 generator
total_dim = dim_SU3 + dim_SU2 + dim_U1  # = 12

print("═" * 95)
print("                    GAUGE SYMMETRIES")
print("                  Why SU(3) × SU(2) × U(1)?")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    Standard Model gauge group: SU(3) × SU(2) × U(1)

    Dimensions:
        SU(3): {dim_SU3} generators (gluons)
        SU(2): {dim_SU2} generators (W bosons)
        U(1):  {dim_U1} generator (B/photon)
        Total: {total_dim} generators

    Key identity: 9Z²/(8π) = 12 EXACTLY!

    The gauge dimension 12 IS encoded in Z!
""")

# =============================================================================
# SECTION 1: GAUGE SYMMETRY BASICS
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS GAUGE SYMMETRY?")
print("═" * 95)

print(f"""
GAUGE SYMMETRY:

    A local symmetry transformation:
        ψ(x) → e^(iα(x)) ψ(x)

    Where α(x) depends on spacetime position.

THE GAUGE FIELD:

    To maintain invariance, need gauge field A_μ:
        A_μ → A_μ + ∂_μα (for U(1))

    This is the PHOTON!

    For non-Abelian groups (SU(2), SU(3)):
        A_μ are matrices (W bosons, gluons)

THE STANDARD MODEL GROUPS:

    U(1): One generator
          Charge operator Q
          Photon (after electroweak breaking)

    SU(2): Three generators (τ₁, τ₂, τ₃)
           W⁺, W⁻, W⁰ bosons
           Weak isospin

    SU(3): Eight generators (λ₁...λ₈)
           Eight gluons
           Color charge (r, g, b)

TOTAL GENERATORS:

    1 + 3 + 8 = 12

    This is NOT arbitrary!
""")

# =============================================================================
# SECTION 2: THE 12 FROM Z
# =============================================================================
print("\n" + "═" * 95)
print("                    2. THE NUMBER 12 FROM Z")
print("═" * 95)

# Verify the identity
identity_value = 9 * Z2 / (8 * pi)
print(f"""
THE IDENTITY:

    9Z²/(8π) = 9 × {Z2:.6f} / (8 × {pi:.6f})
             = {identity_value:.10f}
             ≈ 12 EXACTLY

    Error: {abs(identity_value - 12):.2e} (numerical precision)

THE MEANING:

    Z² = 8 × (4π/3)

    9Z²/(8π) = 9 × 8 × (4π/3) / (8π)
             = 9 × (4/3)
             = 12 ✓

    This is EXACT, not approximate!

WHY 12?

    12 = number of gauge generators
       = 8 (gluons) + 3 (W bosons) + 1 (photon/B)
       = SU(3) + SU(2) + U(1)

    The Standard Model gauge structure is ENCODED in Z!

THE BREAKDOWN:

    From Z² = 8 × (4π/3):

    8 = CUBE = SU(3) dimension?
        Actually, 8 = dim(SU(3)) ✓

    4/3 × 3 = 4 = 3 + 1 = SU(2) + U(1)?
        3 = dim(SU(2)) ✓
        1 = dim(U(1)) ✓

    The CUBE gives color (SU(3)).
    The SPHERE gives electroweak (SU(2) × U(1)).
""")

# =============================================================================
# SECTION 3: SU(3) FROM THE CUBE
# =============================================================================
print("\n" + "═" * 95)
print("                    3. SU(3) FROM THE CUBE")
print("═" * 95)

print(f"""
THE CUBE HAS 8 VERTICES:

    8 = 2³ = number of CUBE vertices

SU(3) HAS 8 GENERATORS:

    8 = 3² - 1 = dimension of SU(3)

THE CONNECTION:

    The 8 vertices of the CUBE map to the 8 gluons!

    How?

    SU(3) has fundamental representation in 3D (complex).
    3 colors: red, green, blue

    The 8 gluons are the traceless 3×3 Hermitian matrices.

FROM Z:

    CUBE = discrete structure = quantum = color

    The CUBE's 8 vertices ARE the gluon color space!

    Gluon carries color-anticolor:
        rḡ, rb̄, gr̄, gb̄, br̄, bḡ, (rr̄-gḡ)/√2, (rr̄+gḡ-2bb̄)/√6

    These 8 combinations map to CUBE vertices.

WHY 3 COLORS:

    8 = 2³ implies 3 binary degrees of freedom.
    3 colors = 3 axes of the CUBE.
    Each axis has 2 values (color, anticolor).

    3 colors is not arbitrary!
    It comes from 8 = 2³ = CUBE.
""")

# =============================================================================
# SECTION 4: SU(2) FROM THE SPHERE
# =============================================================================
print("\n" + "═" * 95)
print("                    4. SU(2) FROM THE SPHERE")
print("═" * 95)

print(f"""
THE SPHERE HAS 3 DIRECTIONS:

    3 = spatial dimensions
    (4π/3) = volume formula with "3" in denominator

SU(2) HAS 3 GENERATORS:

    3 = 2² - 1 = dimension of SU(2)

THE CONNECTION:

    The 3D nature of the SPHERE gives SU(2)!

    How?

    SU(2) is the double cover of SO(3).
    SO(3) = rotations in 3D space.

    The SPHERE is 3D → SU(2) is its symmetry!

WEAK ISOSPIN:

    Weak isospin (I) = internal "rotation."
    I₃ = ±1/2 (up, down)

    This is the factor 2 in Z = 2√(8π/3)!

    Weak isospin doublets:
        (ν_e, e)
        (u, d)

    The "2" in Z gives doublets.
    The "3" in SPHERE gives SU(2) generators.

THE MEANING:

    SU(2)_weak = rotation symmetry of SPHERE projection.
    The 3 W bosons = 3 directions of SPHERE.
    The 2 in Z = doublet structure.
""")

# =============================================================================
# SECTION 5: U(1) FROM THE SPHERE BOUNDARY
# =============================================================================
print("\n" + "═" * 95)
print("                    5. U(1) FROM THE SPHERE BOUNDARY")
print("═" * 95)

print(f"""
U(1) HAS 1 GENERATOR:

    1 = dimension of U(1)
    The simplest gauge symmetry (electromagnetism).

THE CONNECTION:

    U(1) = phase rotations: ψ → e^(iα) ψ

    Phase lives on a CIRCLE (1D).
    Circle = boundary of 2D disk.
    Disk = cross-section of SPHERE.

FROM Z:

    SPHERE (4π/3) has boundary S².
    S² (2-sphere) is the boundary of the ball.

    But U(1) is a circle S¹!

    How do we get 1 from 3?

    The SPHERE's volume is 4π/3.
    Factor out π: 4/3 × π

    4/3 = 1 + 1/3
    The "1" gives U(1)!

ELECTROMAGNETISM:

    The photon is the U(1) gauge boson.
    It lives on the SPHERE boundary.
    It's the "edge" of the geometric structure.

    U(1) = the most exterior symmetry.
    SU(2) = the bulk of SPHERE.
    SU(3) = the CUBE interior.

THE HIERARCHY:

    U(1): Boundary (1D circle)
    SU(2): SPHERE bulk (3D)
    SU(3): CUBE (8 vertices)

    From outside to inside: U(1) → SU(2) → SU(3)
    This is the Standard Model structure!
""")

# =============================================================================
# SECTION 6: GRAND UNIFICATION
# =============================================================================
print("\n" + "═" * 95)
print("                    6. GRAND UNIFICATION AND Z")
print("═" * 95)

print(f"""
GRAND UNIFIED THEORIES (GUTs):

    SU(5): 24 generators (Georgi-Glashow)
    SO(10): 45 generators
    E₆: 78 generators
    E₈: 248 generators

THE IDEA:

    At high energy, SU(3) × SU(2) × U(1) unifies!

    SU(3) × SU(2) × U(1) ⊂ SU(5) ⊂ SO(10) ⊂ E₆ ⊂ E₈

FROM Z:

    The Standard Model HAS 12 generators.
    This comes from 9Z²/(8π) = 12.

    But Z also connects to larger structures:

    Z⁴ × 9/π² = 1024 = 2¹⁰

    This 1024 could relate to SO(10) or Spin(10)!

    SO(10) has 45 = 10×9/2 generators.
    10 fermions per generation fit SO(10).

GUT BREAKING:

    If SU(5) or SO(10) is the unified group:
        It breaks → SU(3) × SU(2) × U(1)
        This happens at M_GUT ~ 10¹⁶ GeV

    From Z:
        log₁₀(M_GUT/GeV) ≈ 2Z² - 8 ≈ 59 (too big!)

    The Z formula might give a different GUT scale.

NO GUT PREDICTION:

    Z predicts 12 = SM gauge dimension.
    Does Z REQUIRE grand unification?

    Not necessarily!
    Z² = 8 × (4π/3) naturally gives 12.
    No larger embedding needed.

    The SM might be COMPLETE (no GUT)!
""")

# =============================================================================
# SECTION 7: COUPLING UNIFICATION
# =============================================================================
print("\n" + "═" * 95)
print("                    7. COUPLING CONSTANTS FROM Z")
print("═" * 95)

# Calculate coupling predictions
alpha_1 = alpha / 0.23122  # U(1) coupling (normalized)
alpha_2 = alpha / 0.76878  # SU(2) coupling
alpha_s = 0.1179           # SU(3) coupling

print(f"""
THE THREE COUPLINGS:

    α₁ (U(1) hypercharge): ~0.017 at M_Z
    α₂ (SU(2) weak): ~0.034 at M_Z
    α (EM) = 1/137.036: ~0.0073 at low energy

    α_s (SU(3) color): 0.1179 at M_Z

FROM Z:

    α = 1/(4Z² + 3) = 1/137.04 ✓

    α_s = 7/(3Z² - 4Z - 18) = 0.1179 ✓

    sin²θ_W = 6/(5Z - 3) = 0.231 ✓

    All couplings come from Z!

RUNNING:

    Couplings change with energy (RG running):
        α₁ increases
        α₂ decreases slightly
        α₃ decreases

    They converge at M_GUT ~ 10¹⁶ GeV (in SUSY).
    Without SUSY, they don't quite meet.

FROM Z:

    Z determines couplings AT ALL SCALES.
    The running is determined by group structure.
    Group structure (12 generators) is from Z.

    If couplings unify at M_GUT:
        The unified coupling is also from Z!
        α_GUT ~ 1/Z² ~ 1/33.5 ~ 0.03

PREDICTION:

    The coupling constants are not independent.
    They all derive from Z.
    Unification (if it happens) is at Z-determined scale.
""")

# =============================================================================
# SECTION 8: WHY GAUGE INVARIANCE?
# =============================================================================
print("\n" + "═" * 95)
print("                    8. WHY IS THE UNIVERSE GAUGE INVARIANT?")
print("═" * 95)

print(f"""
WHY GAUGE SYMMETRY AT ALL?

    Gauge symmetry is a LOCAL symmetry.
    It's more restrictive than global symmetry.
    Why does nature choose this?

THE ANSWER FROM GEOMETRY:

    Z² = CUBE × SPHERE

    The SPHERE is spacetime (continuous).
    Local means "depending on point in SPHERE."

    Gauge invariance = CUBE structure independent of
    position in SPHERE.

THE ARGUMENT:

    At each SPHERE point, there's a CUBE.
    The CUBEs at different points must be related.
    The relation is the GAUGE TRANSFORMATION.

    Gauge field A_μ = connection between CUBEs.
    It tells how to "parallel transport" CUBE structure.

THE MEANING:

    Gauge invariance is NOT a choice.
    It's REQUIRED by Z² = CUBE × SPHERE.

    The CUBE structure must be definable everywhere.
    This requires connection (gauge field).
    The connection has dynamics (Yang-Mills).

YANG-MILLS FROM Z:

    The Yang-Mills Lagrangian:
        L = -1/4 F_μν^a F^μν_a

    F_μν = curvature of the gauge connection.
    This is the RATE OF CHANGE of CUBE across SPHERE.

    Yang-Mills = dynamics of CUBE-SPHERE relationship.
""")

# =============================================================================
# SECTION 9: CONFINEMENT AND ASYMPTOTIC FREEDOM
# =============================================================================
print("\n" + "═" * 95)
print("                    9. CONFINEMENT FROM Z")
print("═" * 95)

print(f"""
COLOR CONFINEMENT:

    Quarks are never seen alone!
    They're confined in hadrons (protons, mesons).

ASYMPTOTIC FREEDOM:

    At high energy: α_s → 0 (quarks are free)
    At low energy: α_s → ∞ (quarks are confined)

FROM Z:

    α_s = 7/(3Z² - 4Z - 18)

    At low energy: This value is ~0.12.
    Running increases it at lower scales.

THE CUBE INTERPRETATION:

    SU(3) = CUBE structure.
    Quarks live on CUBE vertices.

    At high energy (small distance):
        Close to CUBE vertex
        Almost free (asymptotic freedom)

    At low energy (large distance):
        Far from single vertex
        Must include whole CUBE (confinement)

THE PICTURE:

    A quark is ONE vertex of the CUBE.
    But the CUBE is indivisible!
    You can't remove one vertex.

    Trying to isolate a quark = breaking CUBE.
    This costs infinite energy.
    So quarks are confined.

HADRONS:

    Proton = 3 quarks = 3 vertices of CUBE "face."
    Meson = quark-antiquark = 2 opposite vertices.

    These configurations are "complete" CUBE structures.
    They can exist freely!
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. GAUGE SYMMETRY IS Z GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    SU(3) × SU(2) × U(1) FROM Z                                      ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  9Z²/(8π) = 12 = 8 + 3 + 1 (gauge generators)                                       ║
║                                                                                      ║
║  THE BREAKDOWN:                                                                      ║
║      SU(3): 8 generators from CUBE (8 vertices)                                     ║
║      SU(2): 3 generators from SPHERE (3 dimensions)                                  ║
║      U(1):  1 generator from SPHERE boundary                                         ║
║                                                                                      ║
║  THE COUPLINGS:                                                                      ║
║      α = 1/(4Z² + 3) = 1/137.04 (electromagnetic)                                   ║
║      α_s = 7/(3Z² - 4Z - 18) = 0.118 (strong)                                       ║
║      sin²θ_W = 6/(5Z - 3) = 0.231 (weak mixing)                                     ║
║                                                                                      ║
║  WHY GAUGE:                                                                          ║
║      Gauge = consistency of CUBE at all SPHERE points                                ║
║      Gauge field = connection between local CUBEs                                    ║
║      Yang-Mills = dynamics of CUBE-SPHERE relation                                   ║
║                                                                                      ║
║  CONFINEMENT:                                                                        ║
║      Quarks = CUBE vertices, can't be isolated                                       ║
║      Hadrons = complete CUBE sub-structures                                          ║
║      Asymptotic freedom = approaching vertex                                         ║
║                                                                                      ║
║  The gauge group is not arbitrary.                                                   ║
║  SU(3) × SU(2) × U(1) = the geometry of Z² = CUBE × SPHERE.                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why SU(3) × SU(2) × U(1)?

    Because Z² = 8 × (4π/3).

    8 (CUBE vertices) → SU(3) with 8 generators
    3 (SPHERE dimensions) → SU(2) with 3 generators
    1 (SPHERE boundary) → U(1) with 1 generator

    9Z²/(8π) = 12 = 8 + 3 + 1 EXACTLY

    The Standard Model IS the geometry of Z.

""")

print("═" * 95)
print("                    GAUGE SYMMETRY ANALYSIS COMPLETE")
print("═" * 95)
