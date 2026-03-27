#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        THE PAULI EXCLUSION PRINCIPLE
                      Why Fermions Can't Share States
═══════════════════════════════════════════════════════════════════════════════════════════

The Pauli exclusion principle states:

    Two identical fermions cannot occupy the same quantum state.

This explains:
    • Atomic structure (electron shells)
    • The periodic table
    • Why matter takes up space
    • Neutron stars and white dwarfs

But WHY? This document shows exclusion emerges from Z = 2√(8π/3).

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
print("                    THE PAULI EXCLUSION PRINCIPLE")
print("                      Why Fermions Can't Share States")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    The factor 2 in Z = 2√(8π/3) gives:
        • Spin-1/2 particles (fermions)
        • Two-valued spinors
        • Antisymmetric wavefunctions

    The Pauli principle is a CONSEQUENCE of:
        The factor 2 creating spinors that are ANTISYMMETRIC
        under particle exchange.
""")

# =============================================================================
# SECTION 1: FERMIONS AND BOSONS
# =============================================================================
print("═" * 95)
print("                    1. FERMIONS VS BOSONS")
print("═" * 95)

print(f"""
TWO TYPES OF PARTICLES:

    FERMIONS (spin 1/2, 3/2, 5/2, ...):
        Electrons, protons, neutrons, quarks
        Obey PAULI EXCLUSION
        Antisymmetric wavefunction

    BOSONS (spin 0, 1, 2, ...):
        Photons, W/Z, gluons, Higgs, gravitons
        CAN share states
        Symmetric wavefunction

THE SPIN-STATISTICS THEOREM:

    Particles with half-integer spin → Fermions
    Particles with integer spin → Bosons

    This is NOT an assumption!
    It's a THEOREM from QFT + relativity.

THE PAULI PRINCIPLE:

    Two identical fermions CANNOT occupy the same state.

    Mathematically:
        ψ(1,2) = -ψ(2,1) (antisymmetric)
        If state 1 = state 2, then ψ = -ψ
        Therefore ψ = 0 (impossible!)

THE QUESTION:

    WHY are there exactly two types?
    WHY does spin determine statistics?
    WHY is ψ(1,2) = -ψ(2,1) for fermions?
""")

# =============================================================================
# SECTION 2: THE FACTOR 2 IN Z
# =============================================================================
print("\n" + "═" * 95)
print("                    2. THE FACTOR 2 AND SPIN-1/2")
print("═" * 95)

print(f"""
Z = 2√(8π/3)

THE FACTOR 2 APPEARS:

    • 2 components of spinor (↑, ↓)
    • 2 states of spin-1/2
    • 2 = dimension of SU(2) fundamental rep
    • 2 particles to exchange (1 ↔ 2)

SPIN-1/2 FROM Z:

    Spin = intrinsic angular momentum
    For spin-1/2: S = ℏ/2

    The "2" divides ℏ, giving half-integer spin.

    Spin-1/2 means:
        Rotate 360°: ψ → -ψ (not back to ψ!)
        Rotate 720°: ψ → ψ (finally!)

    This is the SU(2) DOUBLE COVER of SO(3).

EXCHANGE AND ROTATION:

    Exchanging two particles = rotating one around the other by 360°.

    For spin-1/2:
        360° rotation gives factor -1
        Therefore exchange gives factor -1
        ψ(2,1) = -ψ(1,2) (antisymmetric!)

THE CONNECTION:

    Z = 2 × √(8π/3)

    The factor 2 creates spinors.
    Spinors pick up -1 under 360° rotation.
    Exchange is equivalent to 360° rotation.
    Therefore fermions are antisymmetric!

    The Pauli principle comes from the "2" in Z!
""")

# =============================================================================
# SECTION 3: THE CUBE AND 8 STATES
# =============================================================================
print("\n" + "═" * 95)
print("                    3. THE CUBE AND FERMION STATES")
print("═" * 95)

print(f"""
Z² = 8 × (4π/3) = CUBE × SPHERE

THE CUBE HAS 8 VERTICES:

    8 = 2 × 2 × 2 = 2³

    Label with binary: (s₁, s₂, s₃) where sᵢ ∈ {{0,1}}

    These 8 states could represent:
        • 8 gluons (SU(3))
        • 8 fermion states in a generation
        • etc.

FOR A SINGLE FERMION:

    2 spin states: ↑ (s=0), ↓ (s=1)

    This is ONE factor of 2 from 8 = 2³.

FOR TWO FERMIONS:

    4 states: (↑↑), (↑↓), (↓↑), (↓↓)

    But symmetry constrains:
        Symmetric: ↑↑, ↓↓, (↑↓ + ↓↑)/√2 (triplet)
        Antisymmetric: (↑↓ - ↓↑)/√2 (singlet)

    The antisymmetric singlet = the DIAGONAL of the CUBE.

THE EXCLUSION:

    Two fermions in the SAME spatial state:
        Must have antisymmetric spin state
        Only the singlet works
        They MUST have opposite spins!

    Two fermions with the SAME spin:
        Must have antisymmetric spatial state
        ψ(x₁,x₂) = -ψ(x₂,x₁)
        This is zero if x₁ = x₂!

    You CANNOT put two same-spin fermions at the same place.
""")

# =============================================================================
# SECTION 4: WHY MATTER TAKES UP SPACE
# =============================================================================
print("\n" + "═" * 95)
print("                    4. WHY MATTER TAKES UP SPACE")
print("═" * 95)

print(f"""
THE PUZZLE:

    Atoms are mostly empty space (nucleus is tiny).
    Yet solid matter resists compression.
    Why can't we push atoms together?

THE ANSWER: PAULI EXCLUSION!

    As you compress matter:
        Electrons get closer
        Same-state electrons would overlap
        Pauli forbids this!

    Result: "Degeneracy pressure"
        A quantum pressure that resists compression
        Even at absolute zero temperature!

ELECTRON DEGENERACY:

    In a white dwarf star:
        Gravity tries to compress
        Pauli pressure resists
        Star stabilizes at ~Earth size, ~Sun mass

    Maximum mass: Chandrasekhar limit ~1.4 M☉
        Above this, electrons go relativistic
        Gravity wins → collapse!

NEUTRON DEGENERACY:

    In a neutron star:
        Even more compressed
        Neutron Pauli pressure holds it up
        ~10 km diameter, 1-2 M☉

    Above ~3 M☉: Black hole (nothing can resist)

FROM Z:

    Matter takes up space because:
        Fermions have factor 2 (from Z)
        Factor 2 → antisymmetric wavefunctions
        Antisymmetric → exclusion
        Exclusion → degeneracy pressure
        Pressure → matter has volume!

    Without the "2" in Z: No Pauli, no structure, no us.
""")

# =============================================================================
# SECTION 5: THE PERIODIC TABLE
# =============================================================================
print("\n" + "═" * 95)
print("                    5. THE PERIODIC TABLE FROM EXCLUSION")
print("═" * 95)

print(f"""
ATOMIC STRUCTURE:

    Electrons fill orbitals in order of energy.
    Each orbital holds LIMITED electrons (Pauli!).

    n=1: 2 electrons (1s²)
    n=2: 8 electrons (2s² 2p⁶)
    n=3: 18 electrons (3s² 3p⁶ 3d¹⁰)
    ...

THE COUNTING:

    Each orbital (n,l,m) holds 2 electrons (spin ↑ and ↓).
    The "2" is from spin-1/2 states.
    This "2" is the "2" in Z = 2√(8π/3)!

THE PERIODIC TABLE:

    Period 1: H (1), He (2) → 2 elements (2 = 2×1)
    Period 2: Li-Ne → 8 elements (8 = 2×4 = 2×(1+3))
    Period 3: Na-Ar → 8 elements
    Period 4: K-Kr → 18 elements (18 = 2×9 = 2×(1+3+5))
    ...

    The structure is:
        Number of elements = 2 × (sum of odd numbers)
        The factor 2 from spin!

CHEMICAL PROPERTIES:

    Noble gases: Closed shells (stable)
    Alkalis: One extra electron (reactive)
    Halogens: One missing electron (reactive)

    ALL of chemistry comes from Pauli exclusion!

FROM Z:

    Without Pauli (no factor 2 in Z):
        All electrons in 1s orbital
        No shell structure
        No periodic table
        No chemistry
        No life!
""")

# =============================================================================
# SECTION 6: THE SPIN-STATISTICS CONNECTION
# =============================================================================
print("\n" + "═" * 95)
print("                    6. SPIN-STATISTICS THEOREM")
print("═" * 95)

print(f"""
THE THEOREM:

    Half-integer spin → Fermi-Dirac statistics (antisymmetric)
    Integer spin → Bose-Einstein statistics (symmetric)

    This is a THEOREM, not an assumption!

THE PROOF (SKETCH):

    Requires:
        1. Lorentz invariance
        2. Locality (causality)
        3. Positive energy

    With these, wrong statistics → negative probabilities!

FROM Z:

    Z² = CUBE × SPHERE

    Lorentz invariance: From SPHERE (spacetime)
    Locality: From SPHERE geometry
    Positive energy: From CUBE discreteness

    All requirements come from Z!

THE FACTOR 2:

    Spin s comes from representation of rotation group.

    Integer spin: Regular representation (vectors, tensors)
        Exchange → +1 (symmetric)
        Bosons

    Half-integer spin: Spinor representation (SU(2))
        Exchange → -1 (antisymmetric)
        Fermions

    The spinor representation exists because:
        SO(3) has double cover SU(2)
        The "2" in SU(2) = the "2" in Z

WHY TWO TYPES:

    There are ONLY two possibilities for exchange:
        ψ(2,1) = +ψ(1,2) (bosons)
        ψ(2,1) = -ψ(1,2) (fermions)

    (In 2D there are more options → anyons!)

    In 3D, only ±1 because π₁(SO(3)) = Z₂.
    The "2" again!
""")

# =============================================================================
# SECTION 7: SUPERFLUIDITY AND BEC
# =============================================================================
print("\n" + "═" * 95)
print("                    7. BOSONS: NO EXCLUSION → BEC")
print("═" * 95)

print(f"""
BOSONS DON'T OBEY EXCLUSION:

    Bosons CAN all occupy the same state!
    No antisymmetry requirement.

BOSE-EINSTEIN CONDENSATION (BEC):

    At low temperature:
        Bosons condense into lowest energy state
        ALL particles in SAME quantum state
        Macroscopic quantum coherence!

    Examples:
        Superfluid helium-4 (below 2.17 K)
        BEC of alkali atoms (nK temperatures)
        Superconductivity (Cooper pairs)

THE CONTRAST:

    Fermions: Pauli pressure, fill levels, complex structure
    Bosons: Condense together, simple ground state

COOPER PAIRS:

    Electrons are fermions.
    But two electrons can pair up!
    The pair has integer spin → boson!
    Cooper pairs can condense → superconductivity.

FROM Z:

    Z² = CUBE × SPHERE

    Fermions: Factor 2 from Z → exclusion → structure
    Bosons: Integer spin → no exclusion → condensation

    Both behaviors encoded in Z:
        The "2" distinguishes them
        Fermions (half-integer) vs Bosons (integer)
""")

# =============================================================================
# SECTION 8: FERMI ENERGY AND FERMI SEA
# =============================================================================
print("\n" + "═" * 95)
print("                    8. THE FERMI SEA")
print("═" * 95)

print(f"""
FILLING STATES:

    Fermions fill available states from lowest energy up.
    Each state holds at most ONE fermion (per spin).

THE FERMI ENERGY:

    E_F = highest occupied energy at T = 0

    For free electrons in a metal:
        E_F ~ (ℏ²/2m)(3π²n)^(2/3)

    Typical values: E_F ~ few eV

THE FERMI SEA:

    All states below E_F are filled.
    States above E_F are empty.
    Like a "sea" of electrons up to level E_F.

EXCITATIONS:

    To excite the system:
        Must lift electron from below E_F to above
        Creates particle (above) + hole (below)
        Minimum energy ~ k_B T

    At low T, few excitations → stable structure.

FROM Z:

    The Fermi sea exists because:
        Electrons are fermions (factor 2 in Z)
        They can't all be in lowest state
        They stack up, filling levels

    Without Pauli: All electrons at E = 0
        No Fermi energy
        No metallic conduction
        No electronics!

THE CUBE PICTURE:

    8 CUBE vertices = 8 available states
    Fermions fill them one by one
    When full, must go to next level

    The 8 = 2³ structure creates the shell structure.
""")

# =============================================================================
# SECTION 9: IDENTICAL PARTICLES
# =============================================================================
print("\n" + "═" * 95)
print("                    9. WHAT DOES 'IDENTICAL' MEAN?")
print("═" * 95)

print(f"""
CLASSICAL PARTICLES:

    Even "identical" balls can be tracked.
    You can label them: ball 1, ball 2.
    They have trajectories, distinguishable in principle.

QUANTUM PARTICLES:

    Identical particles are TRULY identical.
    No hidden labels!
    Swapping them: |1,2⟩ → |2,1⟩ should give same physics.

THE SYMMETRY REQUIREMENT:

    Physical observables must be unchanged under swap.
    |⟨ψ|O|ψ⟩|² must be invariant.

    This means: |ψ(1,2)|² = |ψ(2,1)|²
    So: ψ(2,1) = ±ψ(1,2) (up to phase)

THE PHASE:

    Exchanging twice must return to original:
        ψ(1,2) → ψ(2,1) → ψ(1,2)

    So (phase)² = 1
    Phase = +1 (bosons) or -1 (fermions)

FROM Z:

    Z = 2√(8π/3)

    The "2" determines the allowed phases!

    In 3D space (from SPHERE):
        Paths can be deformed
        Double exchange = identity
        Only ±1 phases allowed

    The SPHERE geometry forces: Bosons OR Fermions.

ANYONS (2D):

    In 2D, more phases allowed!
    Fractional statistics possible.
    Anyons have exchange phase e^(iθ) for any θ.

    This is used in topological quantum computing.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. PAULI IS THE FACTOR 2")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    PAULI EXCLUSION = THE FACTOR 2 IN Z                              ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z = 2√(8π/3)                                                                        ║
║                                                                                      ║
║  THE FACTOR 2:                                                                       ║
║      • 2 spin states (↑, ↓)                                                         ║
║      • Spin-1/2 = ℏ/2 angular momentum                                              ║
║      • 360° rotation → phase -1                                                      ║
║      • Exchange → phase -1 (antisymmetric)                                           ║
║                                                                                      ║
║  ANTISYMMETRY → EXCLUSION:                                                           ║
║      • ψ(1,2) = -ψ(2,1)                                                              ║
║      • If state 1 = state 2: ψ = -ψ = 0                                             ║
║      • Two identical fermions can't share a state!                                   ║
║                                                                                      ║
║  CONSEQUENCES:                                                                       ║
║      • Atomic shell structure (periodic table)                                       ║
║      • Matter takes up space (degeneracy pressure)                                   ║
║      • White dwarfs and neutron stars                                                ║
║      • All of chemistry and biology                                                  ║
║                                                                                      ║
║  WITHOUT THE 2:                                                                      ║
║      • Only bosons, no fermions                                                      ║
║      • No atomic structure                                                           ║
║      • No stable matter                                                              ║
║      • No us!                                                                        ║
║                                                                                      ║
║  The Pauli exclusion principle is not an arbitrary rule.                             ║
║  It's the geometric consequence of the "2" in Z = 2√(8π/3).                         ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why can't two electrons share a state?

    Because Z = 2 × √(8π/3).

    The factor 2 creates spin-1/2.
    Spin-1/2 → spinor → -1 under 360° rotation.
    Exchange = 360° rotation → -1 phase.
    -1 phase = antisymmetric wavefunction.
    Antisymmetric + same state = zero = forbidden.

    The "2" in Z is why matter exists.

""")

print("═" * 95)
print("                    PAULI EXCLUSION ANALYSIS COMPLETE")
print("═" * 95)
