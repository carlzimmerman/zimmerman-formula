#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        WHY QUANTUM MECHANICS?
                      Why Is Nature Probabilistic?
═══════════════════════════════════════════════════════════════════════════════════════════

Classical physics is deterministic: know the initial conditions, predict the future.
Quantum mechanics is probabilistic: outcomes are fundamentally random.

WHY? This isn't just "how nature works" - there must be a REASON.

This document shows quantum mechanics emerges from Z = 2√(8π/3).

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

print("═" * 95)
print("                    WHY QUANTUM MECHANICS?")
print("                  Why Is Nature Probabilistic?")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    Quantum mechanics arises because:
        CUBE is discrete (countable states)
        SPHERE is continuous (uncountable positions)

    To relate them requires PROBABILITY:
        Which CUBE vertex corresponds to which SPHERE point?
        The answer is probabilistic, not deterministic.
""")

# =============================================================================
# SECTION 1: CLASSICAL VS QUANTUM
# =============================================================================
print("═" * 95)
print("                    1. CLASSICAL VS QUANTUM")
print("═" * 95)

print(f"""
CLASSICAL MECHANICS:

    State: Position x and momentum p
    Evolution: Deterministic (Hamilton's equations)
    Measurement: Reveals pre-existing values
    Reality: Particles have definite properties

QUANTUM MECHANICS:

    State: Wavefunction ψ (complex amplitude)
    Evolution: Deterministic (Schrödinger equation)
    Measurement: Probabilistic collapse to eigenstate
    Reality: Properties emerge upon measurement

THE MYSTERY:

    Why is nature quantum at all?
    Why probability instead of certainty?
    Why complex amplitudes?
    Why the measurement problem?

ATTEMPTS TO EXPLAIN:

    Copenhagen: "Shut up and calculate"
    Many-worlds: All outcomes happen
    Pilot wave: Hidden deterministic variables
    QBism: Probability is subjective

    But NONE explains WHY nature chose this structure!
""")

# =============================================================================
# SECTION 2: QM FROM CUBE × SPHERE
# =============================================================================
print("\n" + "═" * 95)
print("                    2. QUANTUM MECHANICS FROM Z")
print("═" * 95)

print(f"""
Z² = CUBE × SPHERE = 8 × (4π/3)

THE KEY INSIGHT:

    CUBE: Discrete, finite (8 vertices)
    SPHERE: Continuous, infinite (uncountable points)

    These are FUNDAMENTALLY DIFFERENT structures!
    Relating them requires a bridge: PROBABILITY.

THE ARGUMENT:

    In classical physics:
        State = point in phase space (continuous)
        Evolution = continuous trajectory
        No CUBE/SPHERE mismatch

    In quantum physics:
        State = superposition over CUBE vertices
        Evolution = rotation in Hilbert space
        Measurement = projection onto SPHERE

    The CUBE-SPHERE mismatch IS quantum mechanics!

WHY PROBABILITY:

    CUBE has 8 vertices (discrete).
    SPHERE has infinite points (continuous).

    When CUBE state projects onto SPHERE:
        Which of the infinite SPHERE points?
        Can't be deterministic (8 → ∞ is not a function)
        Must be probabilistic!

    P(x) = |⟨x|ψ⟩|² is the probability distribution.
    This is FORCED by the mismatch.
""")

# =============================================================================
# SECTION 3: SUPERPOSITION
# =============================================================================
print("\n" + "═" * 95)
print("                    3. SUPERPOSITION FROM CUBE VERTICES")
print("═" * 95)

print(f"""
SUPERPOSITION:

    A quantum state can be a sum of basis states:
        |ψ⟩ = α|0⟩ + β|1⟩

    The particle is "both" until measured.

FROM Z:

    The CUBE has 8 vertices.
    A quantum state assigns amplitude to each vertex.

    |ψ⟩ = Σᵢ cᵢ |vertex_i⟩

    This is superposition over CUBE vertices!

WHY SUPERPOSITION EXISTS:

    The CUBE vertices are the "basis."
    Any state is a combination of vertices.
    This combination = superposition.

    Without CUBE structure:
        Only one "vertex"
        No superposition
        Classical physics

    With CUBE:
        Multiple vertices
        Superposition over them
        Quantum physics!

THE FACTOR 2:

    Z = 2√(8π/3)

    The "2" gives complex amplitudes (2D).
    Each vertex has 2 components (real, imaginary).
    This enables interference!

    Without the 2:
        Real amplitudes only
        No interference
        Different physics
""")

# =============================================================================
# SECTION 4: THE BORN RULE
# =============================================================================
print("\n" + "═" * 95)
print("                    4. THE BORN RULE: P = |ψ|²")
print("═" * 95)

print(f"""
THE BORN RULE:

    Probability to find state |φ⟩ in |ψ⟩:
        P = |⟨φ|ψ⟩|²

    Why SQUARED? Why not |ψ| or |ψ|³?

FROM Z:

    Z² = CUBE × SPHERE

    The SQUARE is built in!

    Amplitude: √(CUBE × SPHERE) ~ Z
    Probability: Z² = amplitude squared

THE ARGUMENT:

    Complex amplitude ψ lives in 2D (complex plane).
    Probability P must be real and positive.

    |ψ|² = ψ*ψ is the unique:
        • Real
        • Positive
        • Quadratic
        norm that works.

THE GEOMETRIC MEANING:

    Amplitude ψ = direction in CUBE × SPHERE
    Probability |ψ|² = "size" of projection

    CUBE contributes 8 (vertices)
    SPHERE contributes 4π/3 (volume)
    Product gives phase space volume

    |ψ|² is the measure on this space.

WHY THIS WORKS:

    The Born rule P = |ψ|² is UNIQUE because:
        1. Probabilities must sum to 1 (normalization)
        2. Composite systems must multiply (tensor products)
        3. Time evolution must preserve probability

    Only |ψ|² satisfies all three!
    This is Gleason's theorem.
""")

# =============================================================================
# SECTION 5: MEASUREMENT
# =============================================================================
print("\n" + "═" * 95)
print("                    5. THE MEASUREMENT PROBLEM")
print("═" * 95)

print(f"""
THE PROBLEM:

    Before measurement: ψ evolves smoothly (Schrödinger)
    During measurement: ψ "collapses" to eigenstate
    After measurement: Definite outcome observed

    Where does collapse come from?
    Why is it instantaneous?
    What triggers it?

FROM Z:

    Z² = CUBE × SPHERE

    Measurement = CUBE projecting onto SPHERE.

THE PICTURE:

    System state: Lives in CUBE (8 vertices)
    Apparatus: Lives in SPHERE (many positions)

    Interaction:
        CUBE state couples to SPHERE apparatus
        Correlation is established
        CUBE "decoheres" in SPHERE

THE RESOLUTION:

    "Collapse" is not a physical process.
    It's the TRANSITION from CUBE to SPHERE description.

    Before: CUBE superposition
    After: SPHERE position

    These are two views of the same Z² structure.
    "Collapse" is changing viewpoint, not physics.

DECOHERENCE:

    When system interacts with environment:
        Off-diagonal CUBE elements suppress
        Effectively classical behavior emerges

    Decoherence is CUBE → SPHERE transition.
    It's built into Z² structure.
""")

# =============================================================================
# SECTION 6: WAVE FUNCTION ONTOLOGY
# =============================================================================
print("\n" + "═" * 95)
print("                    6. WHAT IS THE WAVEFUNCTION?")
print("═" * 95)

print(f"""
THE QUESTION:

    Is ψ real (ontic)?
    Or just knowledge (epistemic)?

VIEWS:

    Ontic: ψ is a real physical field
           (Many-worlds, pilot wave)

    Epistemic: ψ represents our knowledge
               (QBism, Copenhagen)

FROM Z:

    ψ encodes the CUBE structure.
    The CUBE is real (it's the quantum geometry).
    So ψ IS real in this sense.

    But ψ is not a classical field.
    It's not "made of stuff."
    It's the geometric structure itself.

THE RESOLUTION:

    Z² = CUBE × SPHERE

    ψ = the CUBE aspect of Z²
    Spacetime = the SPHERE aspect of Z²

    Both are equally real.
    Neither is "more fundamental."

WAVEFUNCTION OF THE UNIVERSE:

    Ψ_universe encodes ALL of CUBE structure.
    It never collapses (no external observer).
    Branches = different CUBE → SPHERE projections.

    Many-worlds ≈ all CUBE projections coexist.
    But they're on the SAME SPHERE (spacetime).
""")

# =============================================================================
# SECTION 7: WHY COMPLEX NUMBERS
# =============================================================================
print("\n" + "═" * 95)
print("                    7. WHY COMPLEX AMPLITUDES?")
print("═" * 95)

print(f"""
QM USES COMPLEX NUMBERS:

    ψ = a + bi (complex amplitude)
    i = √(-1) (imaginary unit)

    WHY? Real numbers work for classical physics!

FROM Z:

    Z = 2 × √(8π/3)

    The factor 2 = dimension of complex plane!

    Complex number: 2 real components
    Z has factor: 2

    Same 2!

THE NECESSITY:

    Experiments confirm: QM must be complex.
    Real quantum mechanics makes wrong predictions.
    (Renou et al. 2021 - experimental proof!)

WHY 2 COMPONENTS:

    1. INTERFERENCE:
       Waves need phase to interfere.
       Phase requires 2D (amplitude, angle).
       2D = complex plane.

    2. UNITARITY:
       Time evolution preserves probability.
       Unitary operators need complex numbers.
       Real orthogonal matrices are not enough.

    3. SPIN:
       Spin-1/2 requires spinors.
       Spinors are inherently complex.
       The factor 2 creates spin.

THE MEANING:

    Complex numbers aren't a mathematical trick.
    They're the GEOMETRY of the factor 2 in Z.
    QM is complex because Z = 2 × (something).
""")

# =============================================================================
# SECTION 8: THE UNCERTAINTY PRINCIPLE (REVISITED)
# =============================================================================
print("\n" + "═" * 95)
print("                    8. UNCERTAINTY IS BUILT IN")
print("═" * 95)

print(f"""
ΔxΔp ≥ ℏ/2

THE ORIGIN:

    Position x = CUBE projection onto SPHERE
    Momentum p = SPHERE flow along CUBE

    These are DIFFERENT operations!
    They don't commute: [x, p] = iℏ

WHY NONZERO MINIMUM:

    Z² = CUBE × SPHERE

    To have BOTH x and p defined:
        Need overlap of CUBE and SPHERE projections
        Minimum overlap = ℏ/2

    If you could have Δx = 0 AND Δp = 0:
        Pure CUBE AND pure SPHERE simultaneously
        But Z² = CUBE × SPHERE is a PRODUCT
        Can't have both factors be zero!

THE GEOMETRIC PICTURE:

    Phase space has cells of size ℏ.
    Each cell = one CUBE vertex worth of space.
    Can't resolve below one vertex.

    ℏ = CUBE cell size in SPHERE.

UNCERTAINTY IS GEOMETRIC:

    Not a limitation of measurement.
    Not a disturbance effect.
    Not due to wave nature.

    It's the CUBE × SPHERE structure itself.
    You can't be localized in both simultaneously.
""")

# =============================================================================
# SECTION 9: WHY NOT CLASSICAL?
# =============================================================================
print("\n" + "═" * 95)
print("                    9. WHY ISN'T NATURE CLASSICAL?")
print("═" * 95)

print(f"""
CLASSICAL PHYSICS SEEMS SIMPLER:

    Deterministic (no probability)
    Real values (no complex numbers)
    Definite properties (no superposition)

    Why didn't nature choose this?

THE ANSWER:

    Classical physics can't support STRUCTURE.

    Without quantum:
        • Atoms would collapse (electron falls to nucleus)
        • No discrete energy levels (no chemistry)
        • No stable matter (no Pauli exclusion)
        • No universe as we know it!

FROM Z:

    Z² = CUBE × SPHERE

    If only SPHERE (classical):
        Continuous, no discrete structure
        Everything falls to lowest energy
        No atoms, no life

    If only CUBE (pure quantum):
        Discrete but no spacetime
        No positions, no dynamics
        Also no universe

    NEED BOTH: Z² = CUBE × SPHERE

THE BALANCE:

    Quantum (CUBE) provides:
        • Discreteness
        • Stability
        • Structure

    Classical (SPHERE) provides:
        • Spacetime
        • Dynamics
        • Observation

    Together: A universe that can exist AND be observed.

WHY QUANTUM:

    Nature isn't "choosing" to be quantum.
    Nature IS the structure Z² = CUBE × SPHERE.
    Quantum behavior is the CUBE part.
    It's not optional - it's geometry.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. QUANTUM MECHANICS IS Z GEOMETRY")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    QUANTUM MECHANICS = CUBE × SPHERE                                ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  WHY PROBABILITY:                                                                    ║
║      • CUBE (discrete) mapping to SPHERE (continuous)                                ║
║      • 8 vertices → infinite points                                                  ║
║      • This mapping is inherently probabilistic                                      ║
║                                                                                      ║
║  WHY SUPERPOSITION:                                                                  ║
║      • State = combination of CUBE vertices                                          ║
║      • 8 vertices allow superposition                                                ║
║      • Classical = 1 vertex, Quantum = multiple                                      ║
║                                                                                      ║
║  WHY COMPLEX NUMBERS:                                                                ║
║      • Factor 2 in Z = dimension of complex plane                                    ║
║      • Needed for interference and unitarity                                         ║
║      • QM is complex because Z = 2 × √(8π/3)                                        ║
║                                                                                      ║
║  WHY BORN RULE P = |ψ|²:                                                            ║
║      • Z² = amplitude squared                                                        ║
║      • Unique rule satisfying normalization/composition                              ║
║      • Geometric measure on CUBE × SPHERE                                           ║
║                                                                                      ║
║  WHY MEASUREMENT "COLLAPSE":                                                         ║
║      • CUBE state projecting onto SPHERE                                             ║
║      • Transition between two views of Z²                                            ║
║      • Not a physical process - viewpoint change                                     ║
║                                                                                      ║
║  Quantum mechanics is not mysterious.                                                ║
║  Quantum mechanics IS the geometry Z² = CUBE × SPHERE.                              ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why is nature quantum mechanical?

    Because reality has the structure Z² = CUBE × SPHERE.

    The CUBE is discrete, the SPHERE is continuous.
    Relating them requires probability.
    The factor 2 requires complex numbers.
    The product structure creates superposition.

    Quantum mechanics IS the geometry of Z.

""")

print("═" * 95)
print("                    WHY QUANTUM MECHANICS ANALYSIS COMPLETE")
print("═" * 95)
