#!/usr/bin/env python3
"""
═══════════════════════════════════════════════════════════════════════════════════════════
                        QUANTUM STATISTICS
                      Bose-Einstein vs Fermi-Dirac
═══════════════════════════════════════════════════════════════════════════════════════════

Classical particles follow Maxwell-Boltzmann statistics.
Quantum particles obey different rules:

    BOSONS: Bose-Einstein statistics (photons, phonons, etc.)
    FERMIONS: Fermi-Dirac statistics (electrons, quarks, etc.)

This leads to radically different behavior:
    • Bosons condense into the same state (lasers, BEC)
    • Fermions spread out (atomic structure, white dwarfs)

WHY? This document shows statistics emerge from Z = 2√(8π/3).

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
k_B = 1.380649e-23  # J/K

print("═" * 95)
print("                    QUANTUM STATISTICS")
print("                  Bose-Einstein vs Fermi-Dirac")
print("═" * 95)

print(f"""
                           Z = {Z:.10f}

    Z² = 8 × (4π/3) = CUBE × SPHERE

    FERMIONS: From factor 2 (spin-1/2, antisymmetric)
    BOSONS: From integer spin (symmetric)

    The two statistics reflect two ways particles
    can occupy CUBE vertices in the SPHERE.
""")

# =============================================================================
# SECTION 1: THREE TYPES OF STATISTICS
# =============================================================================
print("═" * 95)
print("                    1. THREE TYPES OF STATISTICS")
print("═" * 95)

print(f"""
MAXWELL-BOLTZMANN (Classical):

    n(E) = g(E) × e^(-(E-μ)/(k_B T))

    Particles are distinguishable.
    Any number can occupy any state.
    High-T limit of quantum statistics.

BOSE-EINSTEIN (Bosons):

    n(E) = g(E) / (e^((E-μ)/(k_B T)) - 1)

    Particles are INDISTINGUISHABLE.
    Any number can occupy same state.
    μ ≤ 0 (chemical potential)

FERMI-DIRAC (Fermions):

    n(E) = g(E) / (e^((E-μ)/(k_B T)) + 1)

    Particles are INDISTINGUISHABLE.
    At most ONE per state (Pauli).
    μ can be any value.

THE KEY DIFFERENCE:

    Bose-Einstein: -1 in denominator
    Fermi-Dirac: +1 in denominator

    This ±1 comes from the ±1 phase under exchange!
    Bosons: +1 (symmetric)
    Fermions: -1 (antisymmetric)

THE PHYSICS:

    At low T, bosons pile into lowest state (BEC).
    At low T, fermions fill up to Fermi energy.

    Profoundly different behavior from ±1 sign!
""")

# =============================================================================
# SECTION 2: THE ±1 FROM Z
# =============================================================================
print("\n" + "═" * 95)
print("                    2. THE ±1 FROM Z GEOMETRY")
print("═" * 95)

print(f"""
Z = 2√(8π/3)

WHERE DOES ±1 COME FROM?

    Exchange of two particles:
        ψ(1,2) → ψ(2,1)

    In 3D space, this can be done smoothly.
    The phase acquired depends on SPIN.

SPIN AND EXCHANGE:

    Exchange = rotation by 360° around the other particle.

    Spin 0: 360° → phase +1 (back to original)
    Spin 1/2: 360° → phase -1 (flipped!)
    Spin 1: 360° → phase +1
    Spin 3/2: 360° → phase -1
    ...

    Integer spin → +1 → Bosons
    Half-integer spin → -1 → Fermions

FROM Z:

    The factor 2 in Z = 2√(8π/3) gives:
        Spin-1/2 particles (fermions)
        -1 phase under exchange

    Without the 2:
        Only integer spins
        Only bosons
        No exclusion, no atoms, no us!

THE COUNTING:

    Statistical weight for N particles in states:

    Classical: Each particle independent
        W = n₁ᴺ¹ × n₂ᴺ² × ...

    Quantum bosons: Indistinguishable, symmetric
        W = (n + N - 1)! / (N!(n-1)!)

    Quantum fermions: Indistinguishable, antisymmetric
        W = n! / (N!(n-N)!)  (at most 1 per state)

    These lead to the three distributions!
""")

# =============================================================================
# SECTION 3: BOSE-EINSTEIN CONDENSATION
# =============================================================================
print("\n" + "═" * 95)
print("                    3. BOSE-EINSTEIN CONDENSATION")
print("═" * 95)

print(f"""
BEC: AT LOW T, BOSONS CONDENSE:

    Below critical temperature T_c:
        Macroscopic number of particles in ground state!
        Quantum coherence on macroscopic scale.

EXAMPLES:

    Superfluid helium-4: T_c ≈ 2.17 K
    Dilute atomic gases: T_c ~ nK (Nobel Prize 2001)
    Photons in cavity: T_c ~ room temperature

THE DISTRIBUTION:

    n(E) = 1 / (e^((E-μ)/(k_B T)) - 1)

    As T → T_c: μ → 0 (chemical potential approaches 0)

    At E = 0: n(0) = 1 / (e^(-μ/k_B T) - 1)

    As μ → 0⁻: n(0) → ∞ !

    This divergence = macroscopic occupation of ground state.

SUPERFLUIDITY:

    BEC leads to superfluidity (zero viscosity).
    Superfluid flows without friction!
    Quantum vortices can form.

FROM Z:

    Why can bosons condense?
    Because +1 phase allows SAME state occupation.

    Z² = CUBE × SPHERE

    Bosons are SPHERE-like:
        Continuous
        Wavelike
        Can overlap completely

    At low T, all bosons join the SAME SPHERE mode.
    This is BEC!
""")

# =============================================================================
# SECTION 4: FERMI-DIRAC AND DEGENERACY
# =============================================================================
print("\n" + "═" * 95)
print("                    4. FERMI-DIRAC AND DEGENERACY PRESSURE")
print("═" * 95)

print(f"""
FERMION OCCUPATION:

    n(E) = 1 / (e^((E-μ)/(k_B T)) + 1)

    At T = 0:
        n(E) = 1 for E < μ (= E_F)
        n(E) = 0 for E > μ

    All states filled up to Fermi energy E_F.
    No more than ONE particle per state!

THE FERMI SURFACE:

    In momentum space, occupied states form a sphere.
    Radius = Fermi momentum p_F.
    Surface = Fermi surface.

DEGENERACY PRESSURE:

    Even at T = 0, fermions have kinetic energy.
    Average KE = (3/5) E_F per particle.

    This creates PRESSURE even at zero temperature!

    P = (2/3) (E/V) = (ℏ²/5m) (3π²)^(2/3) n^(5/3)

APPLICATIONS:

    White dwarfs: Electron degeneracy pressure
        Supports up to 1.4 M☉ (Chandrasekhar limit)

    Neutron stars: Neutron degeneracy pressure
        Supports up to ~3 M☉

    Metals: Electron gas with degeneracy pressure
        Explains why metals don't collapse!

FROM Z:

    Why do fermions have degeneracy pressure?
    Because -1 phase forbids same-state occupation.

    Z² = CUBE × SPHERE

    Fermions are CUBE-like:
        Discrete
        Localized at vertices
        Can't overlap (exclusion)

    They fill CUBE vertices one by one.
    When all vertices at energy E filled, must go higher.
    This creates pressure!
""")

# =============================================================================
# SECTION 5: PHOTON STATISTICS
# =============================================================================
print("\n" + "═" * 95)
print("                    5. PHOTON STATISTICS (BLACKBODY)")
print("═" * 95)

print(f"""
PHOTONS ARE BOSONS:

    Spin = 1 (integer)
    μ = 0 (photons created/destroyed freely)

PLANCK DISTRIBUTION:

    n(ω) = 1 / (e^(ℏω/(k_B T)) - 1)

    Energy density:
        u(ω) = (ℏω³/π²c³) × 1/(e^(ℏω/k_B T) - 1)

    This is the BLACKBODY spectrum!

THE ULTRAVIOLET CATASTROPHE:

    Classical physics predicted:
        u(ω) ∝ ω² (Rayleigh-Jeans)
        Total energy = ∫ u dω → ∞ !

    Quantum solution:
        At high ω, n(ω) → e^(-ℏω/k_B T) → 0
        No catastrophe!

PLANCK'S CONSTANT:

    Planck introduced ℏ to explain blackbody.
    Quanta of energy E = ℏω.

    From Z:
        ℏ = CUBE cell size in phase space
        Quantization = CUBE discreteness

THE STEFAN-BOLTZMANN LAW:

    Total power radiated: P = σT⁴

    σ = (π²k_B⁴)/(60ℏ³c²)

    This involves π², ℏ, c - all from Z!

FROM Z:

    Photon statistics come from:
        Spin 1 (integer, not from factor 2)
        μ = 0 (photons are SPHERE boundary)
        Bosonic (symmetric wavefunction)

    Blackbody is the thermal SPHERE at temperature T.
""")

# =============================================================================
# SECTION 6: LASERS AND STIMULATED EMISSION
# =============================================================================
print("\n" + "═" * 95)
print("                    6. LASERS: BOSONIC ENHANCEMENT")
print("═" * 95)

print(f"""
STIMULATED EMISSION:

    For bosons, probability of emission INTO a state
    is ENHANCED if photons already there!

    P(emission) ∝ (n + 1)

    Where n = number of photons in mode.

LASER PRINCIPLE:

    Population inversion: More atoms in excited state
    Stimulated emission: Photon triggers more photons
    Coherence: All photons in same mode

    Result: Intense, coherent, monochromatic light!

THE FACTOR (n + 1):

    Spontaneous: Proportional to 1 (into vacuum)
    Stimulated: Proportional to n (existing photons)
    Total: n + 1

    This enhancement is BOSONIC!
    Fermions would have (1 - n) instead.

BOSONIC AMPLIFICATION:

    More photons → More likely to add photons
    Positive feedback → Exponential growth
    Limited by gain saturation

FROM Z:

    Why do bosons have (n + 1)?
    Because +1 symmetry allows occupation.

    In state counting:
        Bosons: Ways to put N balls in bins = (n+N-1)!/(N!(n-1)!)
        The +1 is there!

    Fermions: (1 - n) factor (Pauli blocking)
    The -1 is there!

    These ±1 determine ALL of laser physics!
""")

# =============================================================================
# SECTION 7: SUPERCONDUCTIVITY
# =============================================================================
print("\n" + "═" * 95)
print("                    7. SUPERCONDUCTIVITY: FERMIONS BECOME BOSONS")
print("═" * 95)

print(f"""
THE PUZZLE:

    Electrons are fermions (spin 1/2).
    But superconductors have zero resistance!
    How can fermions flow without friction?

THE ANSWER: COOPER PAIRS

    Two electrons pair up:
        Spin 1/2 + Spin 1/2 = Spin 0 or 1 (integer!)
        A Cooper pair is a BOSON!

    Cooper pairs can condense (like BEC).
    The condensate flows without resistance.

BCS THEORY:

    Electrons attract via phonon exchange.
    This attraction pairs them.
    All pairs in same quantum state (condensate).

THE GAP:

    Energy Δ needed to break a pair.
    Below T_c, pairs are stable.
    Above T_c, pairs break, normal metal.

FROM Z:

    Z = 2√(8π/3)

    The factor 2 allows:
        Two fermions (factor 2) to pair
        The pair has integer spin
        Pair can Bose-condense

    Without the 2: No spin-1/2, no pairing, no superconductivity!

THE PHYSICS:

    Single electrons: Fermions, exclusion, resistance
    Paired electrons: Bosons, condensation, zero resistance

    Superconductivity converts fermions to bosons!
""")

# =============================================================================
# SECTION 8: ANYONS (2D STATISTICS)
# =============================================================================
print("\n" + "═" * 95)
print("                    8. ANYONS: BEYOND BOSE AND FERMI")
print("═" * 95)

print(f"""
IN 3D: ONLY TWO CHOICES

    Exchange phase: e^(iθ)
    Double exchange = identity: e^(2iθ) = 1
    So: e^(iθ) = ±1

    +1 = Bosons
    -1 = Fermions

IN 2D: MORE OPTIONS!

    Paths can't be smoothly deformed in 2D.
    Double exchange ≠ identity (topologically different)
    Phase can be ANY value: e^(iθ) for any θ

    These particles are called ANYONS.

EXAMPLES:

    Fractional quantum Hall effect:
        Quasiparticles with fractional charge
        Fractional statistics (anyons)
        θ = π/m for filling fraction 1/m

    Majorana fermions:
        θ = π/2 (half way between boson/fermion)
        Non-Abelian statistics!
        Used for topological quantum computing

FROM Z:

    Z structure assumes 3D space (SPHERE = 4π/3).
    In 3D, only ±1 phases (bosons/fermions).

    In 2D (restricted SPHERE):
        More phases possible
        Anyonic statistics emerge

THE MEANING:

    Bosons and fermions are 3D phenomena.
    In lower dimensions, richer structure.
    But 3D is special (from Z geometry).
""")

# =============================================================================
# SECTION 9: IDENTICAL PARTICLES AND GIBBS PARADOX
# =============================================================================
print("\n" + "═" * 95)
print("                    9. GIBBS PARADOX AND INDISTINGUISHABILITY")
print("═" * 95)

print(f"""
THE GIBBS PARADOX:

    Mix two boxes of gas.
    Classical entropy increases.
    But if gases are IDENTICAL, no change!

    Classically: Entropy of mixing = k_B ln(2)
    Quantumly: Entropy of mixing = 0 (for identical)

THE RESOLUTION:

    Quantum mechanics: Identical particles are TRULY identical.
    No hidden labels distinguish them.
    States must be symmetric (bosons) or antisymmetric (fermions).

THE FACTOR 1/N!:

    Classical partition function overcounts by N!
    Correct: Z_quantum = Z_classical / N!

    This 1/N! is the "correct Boltzmann counting."
    It prevents Gibbs paradox.

FROM Z:

    Why are identical particles truly identical?

    Z² = CUBE × SPHERE

    Particles are EXCITATIONS of the Z structure.
    Two electrons are two copies of the SAME mode.
    No way to distinguish them!

    The CUBE vertices don't have labels.
    Vertex 1 = Vertex 2 (if same state).
    Particles at same vertex are identical.

THE MEANING:

    Indistinguishability is not an approximation.
    It's FUNDAMENTAL to quantum mechanics.
    It's required by Z geometry.
""")

# =============================================================================
# SECTION 10: SYNTHESIS
# =============================================================================
print("\n" + "═" * 95)
print("                    10. STATISTICS FROM Z")
print("═" * 95)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                                                                                      ║
║                    QUANTUM STATISTICS = ±1 FROM Z                                   ║
║                                                                                      ║
╠══════════════════════════════════════════════════════════════════════════════════════╣
║                                                                                      ║
║  Z = 2√(8π/3)                                                                        ║
║                                                                                      ║
║  THE FACTOR 2:                                                                       ║
║      • Creates spin-1/2 fermions                                                     ║
║      • Exchange → -1 phase                                                           ║
║      • Fermi-Dirac statistics                                                        ║
║      • +1 in denominator                                                             ║
║                                                                                      ║
║  INTEGER SPIN:                                                                       ║
║      • Bosons (spin 0, 1, 2, ...)                                                   ║
║      • Exchange → +1 phase                                                           ║
║      • Bose-Einstein statistics                                                      ║
║      • -1 in denominator                                                             ║
║                                                                                      ║
║  THE CONSEQUENCES:                                                                   ║
║      Fermions:                    Bosons:                                            ║
║      • Pauli exclusion            • No exclusion                                     ║
║      • Fermi energy               • Bose condensation                                ║
║      • Degeneracy pressure        • Stimulated emission                              ║
║      • Atomic structure           • Lasers                                           ║
║      • White dwarfs               • Superfluids                                      ║
║                                                                                      ║
║  SUPERCONDUCTIVITY:                                                                  ║
║      • Two fermions pair → boson                                                     ║
║      • 2 × (1/2) = integer spin                                                      ║
║      • Cooper pairs condense                                                         ║
║      • Zero resistance                                                               ║
║                                                                                      ║
║  The ±1 that determines all of statistics                                           ║
║  comes from the factor 2 in Z = 2√(8π/3).                                           ║
║                                                                                      ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

    Why are there exactly two types of particles?

    Because exchange in 3D gives only ±1.
    3D comes from SPHERE (4π/3).
    ±1 comes from spin (factor 2 in Z).

    Fermions fill CUBE vertices (one each).
    Bosons share SPHERE modes (many together).

    All of statistical mechanics follows from Z.

""")

print("═" * 95)
print("                    QUANTUM STATISTICS ANALYSIS COMPLETE")
print("═" * 95)
