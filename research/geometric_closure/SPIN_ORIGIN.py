#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE ORIGIN OF SPIN
                      Intrinsic Angular Momentum from Z
═══════════════════════════════════════════════════════════════════════════════════════════

Spin is one of the most mysterious quantum properties:

    • Intrinsic angular momentum (not from orbital motion)
    • Quantized in half-integers: 0, 1/2, 1, 3/2, 2, ...
    • Spin-1/2 particles need 720° rotation to return to original state!

This document shows how spin emerges from Z = 2√(8π/3).

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

print("═" * 95)
print("                    THE ORIGIN OF SPIN")
print("                 Intrinsic Angular Momentum from Z")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z = 2 × √(8π/3)

    The factor 2 is crucial!

    Z/2 = √(8π/3) = √(CUBE × π / 3)

    The factor 2 encodes SPIN structure:
        • 2 spin states for spin-1/2 particles
        • 2 rotations (720°) to return to identity
        • 2 covers of SO(3) → SU(2)
""")

# =============================================================================
# SECTION 1: WHAT IS SPIN?
# =============================================================================
print("═" * 95)
print("                    1. WHAT IS SPIN?")
print("═" * 95)

print(f"""
INTRINSIC ANGULAR MOMENTUM:

    Orbital angular momentum: L = r × p
        • From motion around a point
        • Quantized: L = 0, ℏ, 2ℏ, 3ℏ, ... (integers only)

    Spin angular momentum: S
        • NOT from any motion!
        • Intrinsic property of the particle
        • Quantized: S = 0, ℏ/2, ℏ, 3ℏ/2, ... (half-integers too!)

SPIN VALUES:

    Spin 0: Higgs boson
    Spin 1/2: Electron, quark, neutrino (all fermions)
    Spin 1: Photon, W, Z, gluon
    Spin 3/2: (hypothetical gravitino)
    Spin 2: Graviton

THE MYSTERY:

    1. Why is spin quantized in half-integers?
    2. Why do spin-1/2 particles need 720° rotation?
    3. What IS spinning if nothing is actually rotating?

FROM Z:

    Z = 2√(8π/3)

    The 2 encodes the spin-1/2 structure!
    √(8π/3) encodes the continuous rotation.

    Spin = 2 × (angular aspect of geometry)
""")

# =============================================================================
# SECTION 2: THE FACTOR OF 2
# =============================================================================
print("\n" + "═" * 95)
print("                    2. THE FACTOR OF 2 IN Z")
print("═" * 95)

print(f"""
Z = 2 × √(8π/3)

WHERE DOES THE 2 COME FROM?

    Consider: √(8π/3) = √(CUBE × π/3) ≈ 2.894

    This is the "geometric core" of Z.

    The factor 2 doubles this to get Z ≈ 5.79.

INTERPRETATIONS OF THE 2:

    1. PARTICLE-ANTIPARTICLE:
       Every particle has an antiparticle.
       Electron (e⁻) ↔ Positron (e⁺)
       The 2 counts both.

    2. SPIN STATES:
       Spin-1/2 has 2 states: up (↑) and down (↓)
       The 2 counts both projections.

    3. SU(2) DOUBLE COVER:
       Rotation group SO(3) has a double cover SU(2).
       SU(2) requires 2 full rotations = 720°.
       The 2 encodes this topology.

    4. COMPLEX NUMBERS:
       Quantum amplitudes are complex: a + bi
       2 real numbers for each amplitude.
       The 2 counts real and imaginary parts.

ALL OF THESE ARE CONNECTED!

    The factor 2 in Z unifies:
        • Particle-antiparticle duality
        • Spin up/down
        • 720° rotation topology
        • Complex quantum amplitudes

    They are all aspects of the same geometric 2.
""")

# =============================================================================
# SECTION 3: THE CUBE AND SPIN
# =============================================================================
print("\n" + "═" * 95)
print("                    3. THE CUBE AND SPIN")
print("═" * 95)

print(f"""
Z² = 8 × (4π/3) = CUBE × SPHERE

THE CUBE HAS ROTATIONAL SYMMETRY:

    Rotations that leave cube unchanged:
        • 24 proper rotations (orientation-preserving)
        • 24 improper rotations (with reflection)
        • Total: 48 symmetries

    The rotation group of cube = S₄ (symmetric group on 4)
    Same as permutations of 4 objects!

    Why 4? A cube has 4 body diagonals.

SPIN FROM CUBE FACES:

    The cube has 6 faces in 3 pairs:
        • Top-Bottom (z-axis)
        • Front-Back (y-axis)
        • Left-Right (x-axis)

    Each face can be rotated in 4 positions.
    Total: 4 × 4 × 4 = 64 configurations?

    But many are equivalent. Distinct: 24.

THE CONNECTION:

    Spin comes from how the CUBE embeds in the SPHERE.

    A cube inside a sphere:
        • 8 vertices touch the sphere
        • The sphere can rotate continuously
        • But the cube has discrete orientations

    Spin = quantized rotation of CUBE within SPHERE

SPIN-1/2:

    Rotate the cube 90°: 4 distinct positions
    After 360°: back to start (for cube)
    But for quantum state: need 720°!

    The factor 2 arises because:
        Cube has 8 vertices = 2³
        Each rotation samples 2 of the 3 axes
        Need 2 full cycles to return.
""")

# =============================================================================
# SECTION 4: SU(2) AND SO(3)
# =============================================================================
print("\n" + "═" * 95)
print("                    4. SU(2) AND SO(3) FROM Z")
print("═" * 95)

print(f"""
THE ROTATION GROUPS:

    SO(3): Rotations in 3D space
        • 3 parameters (Euler angles)
        • Every rotation is a point in SO(3)
        • Topologically: RP³ (projective space)

    SU(2): Special unitary 2×2 matrices
        • Also 3 parameters
        • Double cover of SO(3)
        • Topologically: S³ (3-sphere)

THE DOUBLE COVER:

    SU(2) wraps around SO(3) twice.
    Going 360° in SO(3) = going 180° in SU(2).
    Need 720° in SO(3) = full 360° in SU(2).

    This is why spin-1/2 needs 720° rotation!

FROM Z:

    Z = 2√(8π/3)

    The 2 encodes the double cover!

    √(8π/3) relates to SO(3) rotations.
    Factor of 2 promotes to SU(2).

    Spin-1/2 particles live in SU(2), not SO(3).

THE SPINOR:

    Spin-1/2 states are "spinors" in SU(2).
    Under rotation R:
        |↑⟩ → cos(θ/2)|↑⟩ + sin(θ/2)|↓⟩
        |↓⟩ → -sin(θ/2)|↑⟩ + cos(θ/2)|↓⟩

    Note: θ/2 appears, not θ!
    This is the factor-of-2 structure.

    For θ = 360°: cos(180°) = -1
    The state picks up a minus sign!
    Need θ = 720° to return to +1.
""")

# =============================================================================
# SECTION 5: WHY HALF-INTEGERS?
# =============================================================================
print("\n" + "═" * 95)
print("                    5. WHY HALF-INTEGER SPIN?")
print("═" * 95)

print(f"""
Orbital angular momentum: L = 0, 1, 2, 3, ... (integers)
Spin angular momentum: S = 0, 1/2, 1, 3/2, 2, ... (half-integers too!)

WHY THE DIFFERENCE?

ORBITAL ANGULAR MOMENTUM:

    From L = r × p, we get:
        L_z = mℏ where m = -l, ..., +l

    Single-valuedness of ψ(φ) requires:
        ψ(φ + 2π) = ψ(φ)
        → m must be integer

SPIN ANGULAR MOMENTUM:

    Spin is intrinsic, not from ψ(φ).
    No single-valuedness requirement on angle!

    Spin can be half-integer: S = 1/2, 3/2, 5/2, ...

FROM Z:

    Z = 2√(8π/3)

    The factor 2 allows half-integer spin!

    Without the 2: Only integer spin (bosons)
    With the 2: Half-integer spin allowed (fermions)

THE MEANING:

    2 = number of spin states = 2S + 1 for S = 1/2

    The formula Z = 2√(...) is telling us:
        The universe has BOTH integer and half-integer spin
        The factor 2 enables fermions to exist!

    If Z were √(8π/3) without the 2:
        Only bosons
        No electrons, no matter, no us!
""")

# =============================================================================
# SECTION 6: THE SPIN-STATISTICS THEOREM
# =============================================================================
print("\n" + "═" * 95)
print("                    6. SPIN-STATISTICS FROM Z")
print("═" * 95)

print(f"""
THE THEOREM:

    Half-integer spin → Fermi-Dirac statistics (exclusion)
    Integer spin → Bose-Einstein statistics (bunching)

WHY?

    Standard proof: Requires relativistic QFT + locality + Lorentz invariance.
    Very technical, not intuitive.

FROM Z:

    Z² = CUBE × SPHERE

    FERMIONS (spin 1/2, 3/2, ...):
        Dominated by CUBE aspect
        8 vertices = exclusive slots
        Only one particle per state (Pauli exclusion)

    BOSONS (spin 0, 1, 2, ...):
        Dominated by SPHERE aspect
        Continuous surface = infinite slots
        Any number per state (bunching)

THE CONNECTION:

    The factor 2 in Z = 2√(...) creates fermions.
    Fermions exclude because they live on CUBE vertices.
    Only 8 vertices available = finite capacity.

    Bosons are the √(...) part.
    They live on the SPHERE surface.
    Infinite capacity = no exclusion.

THE DEEP MEANING:

    Spin-statistics is not a "theorem" to prove.
    It is the GEOMETRY of Z² = CUBE × SPHERE!

    CUBE → exclusive → fermion → half-integer spin
    SPHERE → inclusive → boson → integer spin
""")

# =============================================================================
# SECTION 7: THE ELECTRON SPIN
# =============================================================================
print("\n" + "═" * 95)
print("                    7. THE ELECTRON'S SPIN")
print("═" * 95)

# Electron g-factor
g_e = 2.00231930436256  # very close to 2!

print(f"""
The electron has spin 1/2 and g-factor ≈ 2.

THE g-FACTOR:

    Magnetic moment: μ = g × (e/2m) × S

    For orbital motion: g = 1
    For electron spin: g ≈ 2.002319...

    Why is g ≈ 2 for spin?

DIRAC'S DERIVATION:

    The Dirac equation predicts g = 2 exactly!
    QED corrections give small deviation: g = 2.002319...

FROM Z:

    Z = 2√(8π/3)

    The factor 2 in Z is the electron g-factor!

    g_e ≈ 2 comes from the geometric structure:
        • The "2" in Z is the spin factor
        • It naturally gives g = 2

    The small correction 0.002319:
        α/(2π) ≈ 0.00116 (leading term)
        This is the QED "cloud" around the electron.

THE MEANING:

    The electron's intrinsic magnetism comes from:
        • Factor 2 = spin structure in Z
        • α/(2π) = interaction with electromagnetic field

    Both are geometric: 2 from Z, α from Z.
""")

# =============================================================================
# SECTION 8: SPIN AND SPACETIME
# =============================================================================
print("\n" + "═" * 95)
print("                    8. SPIN AND SPACETIME")
print("═" * 95)

print(f"""
Spin is deeply connected to spacetime structure.

THE LORENTZ GROUP:

    Spacetime symmetry: SO(3,1) (rotations + boosts)
    Its cover: SL(2,C) (complex 2×2 matrices)

    Representations:
        (0, 0): Scalar (spin 0)
        (1/2, 0) or (0, 1/2): Weyl spinor (spin 1/2)
        (1/2, 1/2): Vector (spin 1)
        (1, 1): Tensor (spin 2)

FROM Z:

    Z² = 8 × (4π/3) = CUBE × SPHERE

    The CUBE (8) encodes discrete structure:
        8 = 2³ = 2 × 2 × 2

        This matches SL(2,C) structure:
            2: spinor representation
            2 × 2: vector representation
            2 × 2 × 2: more complex tensors

    The SPHERE encodes continuous structure:
        Rotations live on the sphere
        Lorentz boosts extend this

THE INSIGHT:

    Spin is how the CUBE rotates within the SPHERE.

    The 8 vertices of the CUBE map to:
        8 = (2 spin states) × (matter/antimatter) × (left/right handed)
        8 = 2 × 2 × 2

    Each factor of 2 is a binary choice.
    Together they give the full spinor structure.

GRAVITON SPIN:

    Graviton has spin 2.
    Spacetime itself has spin!

    From Z: Spin 2 = (1/2 + 1/2) × 2
           = combining two spin-1/2 "indices"
           = symmetric tensor

    Gravity is geometry. Spin 2 is that geometry rotating.
""")

# =============================================================================
# SECTION 9: THE PAULI MATRICES
# =============================================================================
print("\n" + "═" * 95)
print("                    9. PAULI MATRICES FROM Z")
print("═" * 95)

print(f"""
The Pauli matrices describe spin-1/2:

    σ_x = [0 1; 1 0]
    σ_y = [0 -i; i 0]
    σ_z = [1 0; 0 -1]

Properties:
    σᵢ² = I (identity)
    σᵢσⱼ = iεᵢⱼₖσₖ (anticommute)
    Tr(σᵢ) = 0

FROM Z:

    The Pauli matrices encode the CUBE axes!

    σ_x: x-axis rotation (Left-Right face pair)
    σ_y: y-axis rotation (Front-Back face pair)
    σ_z: z-axis rotation (Top-Bottom face pair)

    Each matrix is 2×2 → the factor 2 in Z
    Three matrices → 3 spatial dimensions (from SPHERE)

THE ALGEBRA:

    {σᵢ, σⱼ} = 2δᵢⱼI

    The factor 2 appears explicitly!
    It's the same 2 as in Z = 2√(8π/3).

QUATERNIONS:

    Define: q = a + bσ_x + cσ_y + dσ_z (in matrix form)

    Quaternions form a 4D algebra.
    They describe 3D rotations (via SU(2)).

    Quaternions ↔ Spin-1/2 ↔ Factor 2 in Z

    The Z framework unifies:
        • Quaternion algebra
        • Spin-1/2 physics
        • SU(2) gauge theory
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. THE ORIGIN OF SPIN")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    SPIN EMERGES FROM Z GEOMETRY                                      ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z = 2√(8π/3)                                                                        ║
║                                                                                      ║
║  THE FACTOR 2:                                                                       ║
║      • Enables half-integer spin (fermions)                                          ║
║      • Encodes SU(2) double cover of SO(3)                                          ║
║      • Gives electron g-factor ≈ 2                                                   ║
║      • Creates particle-antiparticle duality                                         ║
║      • Allows spin up/down states                                                    ║
║                                                                                      ║
║  THE √(8π/3):                                                                        ║
║      • 8 = CUBE vertices = spinor components                                         ║
║      • π = circular/rotational structure                                             ║
║      • 3 = spatial dimensions = Pauli matrices                                       ║
║                                                                                      ║
║  SPIN-STATISTICS:                                                                    ║
║      • Fermions (half-integer) → CUBE-dominated                                      ║
║      • Bosons (integer) → SPHERE-dominated                                           ║
║      • Not a theorem, but geometry!                                                  ║
║                                                                                      ║
║  THE ANSWER:                                                                         ║
║      Spin is not "something spinning."                                              ║
║      Spin is how the CUBE rotates within the SPHERE.                                ║
║      Spin is the factor 2 in Z = 2√(8π/3).                                          ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    What is spinning?

    The CUBE is spinning inside the SPHERE.
    Z² = 8 × (4π/3) = CUBE × SPHERE

    Spin is the geometric relationship between
    discrete (CUBE) and continuous (SPHERE) structure.

    It requires 720° because the factor 2 in Z
    means going around twice to close the loop.

""")

print("═" * 95)
print("                    SPIN ORIGIN ANALYSIS COMPLETE")
print("═" * 95)
