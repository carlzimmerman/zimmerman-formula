#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE UNCERTAINTY PRINCIPLE
                      Why ΔxΔp ≥ ℏ/2 ?
═══════════════════════════════════════════════════════════════════════════════════════════

Heisenberg's uncertainty principle is fundamental to quantum mechanics:

    ΔxΔp ≥ ℏ/2
    ΔEΔt ≥ ℏ/2

You cannot simultaneously know position and momentum with arbitrary precision.
This is NOT a measurement limitation - it's a fundamental feature of reality.

WHY? This document shows uncertainty emerges from Z = 2√(8π/3).

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
hbar = 1.054571817e-34  # J·s

print("═" * 95)
print("                    THE UNCERTAINTY PRINCIPLE")
print("                      Why ΔxΔp ≥ ℏ/2 ?")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    The uncertainty principle arises from:
        CUBE = discrete (position-like, localized)
        SPHERE = continuous (momentum-like, wavelike)

    You cannot be fully in CUBE AND fully in SPHERE.
    The product ΔxΔp measures the CUBE-SPHERE overlap.
    Minimum overlap = ℏ/2 (set by Z structure).
""")

# =============================================================================
# SECTION 1: THE UNCERTAINTY RELATIONS
# =============================================================================
print("═" * 95)
print("                    1. THE UNCERTAINTY RELATIONS")
print("═" * 95)

print(f"""
HEISENBERG (1927):

    Position-Momentum:  ΔxΔp ≥ ℏ/2
    Energy-Time:        ΔEΔt ≥ ℏ/2

    These are FUNDAMENTAL, not just experimental limits.

THE MEANING:

    If you know position precisely (Δx small):
        Momentum is uncertain (Δp large)

    If you know momentum precisely (Δp small):
        Position is uncertain (Δx large)

    The product has a MINIMUM: ℏ/2

MATHEMATICAL ORIGIN:

    For any observables A, B:
        ΔAΔB ≥ ½|⟨[A,B]⟩|

    For position and momentum:
        [x, p] = iℏ
        ΔxΔp ≥ ℏ/2 ✓

THE QUESTION:

    WHY is [x, p] = iℏ?
    WHY does this commutator have value ℏ?
    WHY is there a minimum uncertainty at all?
""")

# =============================================================================
# SECTION 2: CUBE AND SPHERE PERSPECTIVES
# =============================================================================
print("\n" + "═" * 95)
print("                    2. CUBE VS SPHERE PERSPECTIVES")
print("═" * 95)

print(f"""
Z² = CUBE × SPHERE = 8 × (4π/3)

TWO COMPLEMENTARY VIEWS:

    CUBE perspective (position space):
        Particle is LOCALIZED
        Sits at a CUBE vertex
        Position is well-defined
        Momentum is spread out (Fourier transform)

    SPHERE perspective (momentum space):
        Particle is a WAVE
        Spread over SPHERE
        Momentum is well-defined
        Position is spread out (inverse Fourier)

THE COMPLEMENTARITY:

    You can't have BOTH perspectives simultaneously!

    Localized in position → Spread in momentum
    Localized in momentum → Spread in position

FROM Z:

    Z² = CUBE × SPHERE

    A particle IS both CUBE and SPHERE.
    But observation projects onto ONE.

    Δx = uncertainty in CUBE projection
    Δp = uncertainty in SPHERE projection

    The PRODUCT ΔxΔp measures:
        "How much CUBE-SPHERE mixing?"

MINIMUM MIXING:

    ΔxΔp ≥ ℏ/2 says:
        There's a MINIMUM overlap
        You can't be pure CUBE (Δx = 0, Δp = ∞)
        You can't be pure SPHERE (Δp = 0, Δx = ∞)
        Always some mixture!

    This minimum is ℏ/2 = the Z "coupling" scale.
""")

# =============================================================================
# SECTION 3: THE FACTOR 2 IN Z
# =============================================================================
print("\n" + "═" * 95)
print("                    3. THE FACTOR 2 AND ℏ/2")
print("═" * 95)

print(f"""
THE MINIMUM UNCERTAINTY:

    ΔxΔp ≥ ℏ/2

    Why "/2"? Where does the 2 come from?

FROM Z:

    Z = 2√(8π/3)

    The factor 2 appears!

THE CONNECTION:

    The "2" in Z relates to:
        • Complex numbers (2D complex plane)
        • Spin-1/2 (2 states)
        • Particle/antiparticle (2 types)

    And also:
        • Uncertainty minimum (ℏ/2)!

THE ARGUMENT:

    The minimum uncertainty state is a GAUSSIAN:
        ψ(x) = exp(-x²/2σ²)

    This is the "coherent state" - minimum uncertainty.

    The Gaussian has special property:
        Its Fourier transform is also Gaussian!
        ψ̃(p) = exp(-p²σ²/2ℏ²)

    The widths are related:
        Δx = σ/√2
        Δp = ℏ/(σ√2)
        ΔxΔp = ℏ/2 ✓

THE FACTOR 2:

    The √2 in the widths comes from:
        Gaussian variance formula
        The "2" in the exponent exp(-x²/2σ²)

    This "2" is the SAME "2" as in Z = 2√(8π/3)!

    The minimum uncertainty state is the state
    that perfectly balances CUBE and SPHERE.
""")

# =============================================================================
# SECTION 4: COMMUTATORS AND GEOMETRY
# =============================================================================
print("\n" + "═" * 95)
print("                    4. [x, p] = iℏ FROM Z")
print("═" * 95)

print(f"""
THE CANONICAL COMMUTATOR:

    [x, p] = xp - px = iℏ

    Position and momentum don't commute!
    The order of measurement matters.

WHY iℏ?

    i = imaginary unit (from complex structure)
    ℏ = Planck constant (quantum of action)

FROM Z:

    Z = 2√(8π/3)

    The "2" gives complex structure (i appears).
    ℏ comes from the CUBE structure (quantum).

THE GEOMETRIC MEANING:

    x = CUBE coordinate (position in SPHERE)
    p = SPHERE momentum (flow along CUBE→SPHERE)

    They don't commute because:
        Moving in x changes your p perspective
        Moving in p changes your x perspective

    It's like ROTATION:
        Rotate around x, then y ≠ Rotate around y, then x

    The commutator [x, p] measures the "twist."

THE VALUE iℏ:

    ℏ = minimum quantum of action
      = size of one CUBE cell in phase space

    i = the complex phase
      = rotation in the 2D plane (from "2" in Z)

    [x, p] = iℏ means:
        One CUBE step in x combined with SPHERE flow in p
        produces a phase rotation of magnitude ℏ.
""")

# =============================================================================
# SECTION 5: PHASE SPACE AND ℏ
# =============================================================================
print("\n" + "═" * 95)
print("                    5. PHASE SPACE QUANTIZATION")
print("═" * 95)

print(f"""
CLASSICAL PHASE SPACE:

    Each state is a point (x, p).
    States are continuous.
    Can know both x and p precisely.

QUANTUM PHASE SPACE:

    States occupy CELLS of area ℏ.
    Can't resolve smaller than ℏ.
    Uncertainty: ΔxΔp ≥ ℏ/2

THE PICTURE:

    Classical:     Quantum:

    p ↑            p ↑  ▓▓▓▓▓▓▓▓
      │              │  ▓▓▓▓▓▓▓▓
      │    ·         │  ▓▓ h ▓▓▓  ← Cell of area h
      │              │  ▓▓▓▓▓▓▓▓
      └────→ x       └────────→ x

    (Point)        (Cell)

FROM Z:

    ℏ = size of CUBE cell in phase space.

    One CUBE vertex occupies area ℏ in (x, p) space.
    You can't be at a "point" - you're always in a cell.

THE COUNTING:

    How many states in region of area A?
        N = A / ℏ (approximately)
        N = A / (2πℏ) (with proper normalization)

    The "2π" comes from:
        π in Z² = 8 × (4π/3)
        Full circle has circumference 2π

DENSITY OF STATES:

    ρ = 1/ℏ per unit area in phase space.

    This is why statistical mechanics works!
    Entropy S = k ln(Ω) counts cells of size ℏ.
""")

# =============================================================================
# SECTION 6: ENERGY-TIME UNCERTAINTY
# =============================================================================
print("\n" + "═" * 95)
print("                    6. ENERGY-TIME UNCERTAINTY")
print("═" * 95)

print(f"""
THE SECOND UNCERTAINTY RELATION:

    ΔEΔt ≥ ℏ/2

    Short-lived states have uncertain energy.
    Precise energy requires long measurement.

THE SUBTLETY:

    Time is NOT an operator in QM!
    [E, t] ≠ iℏ (t is just a parameter)

    So where does ΔEΔt ≥ ℏ/2 come from?

THE DERIVATION:

    For any observable A changing in time:
        ΔE Δt_A ≥ ℏ/2

    Where Δt_A = time for A to change by ΔA.

FROM Z:

    Z² = CUBE × SPHERE

    Energy: Related to CUBE structure (discrete levels)
    Time: Related to CUBE → SPHERE flow

    E and t are "conjugate" through the flow!

THE PICTURE:

    CUBE: Energy eigenstates (standing waves)
    SPHERE: Time evolution (flowing)

    Measuring energy = projecting onto CUBE
    Measuring time = projecting onto flow

    You can't fully project onto BOTH:
        Precise E → standing wave → "no time evolution"
        Precise t → flowing → energy spread

VIRTUAL PARTICLES:

    ΔEΔt ≥ ℏ/2 allows "borrowing" energy!

    For short time Δt, can have ΔE ~ ℏ/Δt.
    This creates virtual particles.
    They exist for Δt ~ ℏ/ΔE then disappear.

    Virtual particles ARE the CUBE-SPHERE fluctuations!
""")

# =============================================================================
# SECTION 7: WAVE PACKETS
# =============================================================================
print("\n" + "═" * 95)
print("                    7. WAVE PACKETS AND UNCERTAINTY")
print("═" * 95)

print(f"""
WAVE PACKETS:

    A localized particle is a superposition of waves:
        ψ(x) = ∫ φ(p) e^(ipx/ℏ) dp

    The spread Δp determines localization Δx.

FOURIER RELATIONSHIP:

    Narrow in x → Wide in p (and vice versa)

    This is MATHEMATICAL, not just physical!

    For any function:
        Width in x × Width in k ≥ 1/2

    With k = p/ℏ:
        Δx × Δp/ℏ ≥ 1/2
        ΔxΔp ≥ ℏ/2 ✓

FROM Z:

    Z² = CUBE × SPHERE

    Position representation: ψ(x) (CUBE view)
    Momentum representation: φ(p) (SPHERE view)

    Fourier transform connects them:
        ψ(x) ↔ φ(p)

    This is the CUBE-SPHERE duality in action!

THE MINIMUM PACKET:

    Gaussian wave packet minimizes uncertainty.
    ψ(x) = exp(-x²/4σ²) × exp(ip₀x/ℏ)

    This is the "coherent state."
    It's the most CLASSICAL quantum state.
    Closest to a point in phase space.

    Even this has ΔxΔp = ℏ/2.
    You CANNOT go below this!
""")

# =============================================================================
# SECTION 8: MEASUREMENT AND DISTURBANCE
# =============================================================================
print("\n" + "═" * 95)
print("                    8. IS UNCERTAINTY FROM MEASUREMENT?")
print("═" * 95)

print(f"""
COMMON MISCONCEPTION:

    "Uncertainty is because measurement disturbs the system."

    This is WRONG (or at least incomplete).

THE HEISENBERG MICROSCOPE:

    To see position precisely, use short wavelength light.
    Short wavelength = high momentum photons.
    These kick the particle, disturbing momentum.

    This gives ΔxΔp ~ ℏ (roughly).

BUT THIS ISN'T THE WHOLE STORY:

    Even WITHOUT measurement:
        States with definite x don't have definite p.
        States with definite p don't have definite x.

    Uncertainty is in the STATE, not just measurement.

FROM Z:

    Z² = CUBE × SPHERE

    A quantum state IS BOTH CUBE and SPHERE.
    It doesn't "have" a definite position AND momentum.
    These are complementary projections.

THE CORRECT VIEW:

    Before measurement:
        State is superposition (CUBE × SPHERE)
        Neither x nor p is definite

    After measurement of x:
        State collapses to position eigenstate (CUBE)
        Momentum becomes undefined (SPHERE spread)

    Measurement doesn't "disturb" a pre-existing value.
    The value didn't EXIST before measurement!
""")

# =============================================================================
# SECTION 9: APPLICATIONS
# =============================================================================
print("\n" + "═" * 95)
print("                    9. PHYSICAL CONSEQUENCES")
print("═" * 95)

print(f"""
1. ZERO-POINT ENERGY:

    Even at T = 0, harmonic oscillator has energy E₀ = ℏω/2.

    Why? Uncertainty!
        If E = 0, both x and p would be 0.
        This violates ΔxΔp ≥ ℏ/2.
        So minimum energy is nonzero.

    This is the "zero-point motion" = CUBE-SPHERE fluctuation.

2. ATOMIC STABILITY:

    Why doesn't the electron fall into the nucleus?

    If it did, Δx → 0 (very localized).
    Then Δp → ∞ (huge momentum uncertainty).
    Kinetic energy E ~ p²/2m becomes HUGE.

    The electron finds a BALANCE:
        Not too localized (too much KE)
        Not too spread (not enough PE gain)

    This gives Bohr radius a₀ ~ ℏ²/(me²) ≈ 0.5 Å.

3. TUNNELING:

    Particle can "tunnel" through a barrier!

    How? Uncertainty allows ΔE for short Δt.
    Particle "borrows" energy to cross.
    As long as Δt < ℏ/ΔE, it's allowed.

    Tunneling rate depends on barrier height/width.

4. VIRTUAL PARTICLES:

    Empty space is filled with virtual particle pairs!
    They pop in and out for time Δt ~ ℏ/2mc².

    This creates:
        • Casimir effect (vacuum force)
        • Lamb shift (energy level correction)
        • Hawking radiation (black hole evaporation)
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. UNCERTAINTY IS CUBE × SPHERE")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    UNCERTAINTY = CUBE × SPHERE COMPLEMENTARITY                      ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z² = 8 × (4π/3) = CUBE × SPHERE                                                    ║
║                                                                                      ║
║  CUBE (position-like):                                                               ║
║      • Discrete, localized                                                           ║
║      • 8 vertices = 8 basis states                                                   ║
║      • Measuring position = projecting onto CUBE                                     ║
║                                                                                      ║
║  SPHERE (momentum-like):                                                             ║
║      • Continuous, wave-like                                                         ║
║      • Infinite directions = continuous spectrum                                     ║
║      • Measuring momentum = projecting onto SPHERE                                   ║
║                                                                                      ║
║  UNCERTAINTY:                                                                        ║
║      • Can't fully project onto BOTH simultaneously                                  ║
║      • ΔxΔp ≥ ℏ/2 = minimum CUBE-SPHERE overlap                                     ║
║      • The "2" in ℏ/2 is the "2" in Z = 2√(8π/3)                                   ║
║                                                                                      ║
║  COMMUTATOR [x,p] = iℏ:                                                             ║
║      • i from complex structure (factor 2 in Z)                                      ║
║      • ℏ from CUBE cell size in phase space                                         ║
║      • Non-commutativity = CUBE-SPHERE twist                                         ║
║                                                                                      ║
║  CONSEQUENCES:                                                                       ║
║      • Zero-point energy (can't have E = 0)                                          ║
║      • Atomic stability (electron can't collapse)                                    ║
║      • Tunneling (borrow energy for short time)                                      ║
║      • Virtual particles (vacuum fluctuations)                                       ║
║                                                                                      ║
║  Uncertainty is not a limitation of knowledge.                                       ║
║  Uncertainty IS the CUBE × SPHERE structure of reality.                             ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why can't we know both x and p precisely?

    Because Z² = CUBE × SPHERE.

    Position is CUBE projection.
    Momentum is SPHERE projection.
    A state IS both, but we can only OBSERVE one at a time.

    The minimum uncertainty ℏ/2 is the irreducible
    CUBE-SPHERE mixing built into Z.

""")

print("═" * 95)
print("                    UNCERTAINTY PRINCIPLE ANALYSIS COMPLETE")
print("═" * 95)
