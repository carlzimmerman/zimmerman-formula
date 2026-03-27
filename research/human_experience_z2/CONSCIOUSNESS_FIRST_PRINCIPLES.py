"""
CONSCIOUSNESS_FIRST_PRINCIPLES.py
=================================
Deriving Consciousness from Z² = 8 × (4π/3) = CUBE × SPHERE

A rigorous attempt to ground consciousness in fundamental geometry.
From the product of discrete and continuous, awareness emerges.

Carl Zimmerman, March 2026
DOI: 10.5281/zenodo.19244651
"""

from math import pi, sqrt, log, log2, exp

# ═══════════════════════════════════════════════════════════════════════════
# THE MASTER EQUATION
# ═══════════════════════════════════════════════════════════════════════════

Z2 = 8 * (4 * pi / 3)  # = 32π/3 = CUBE × SPHERE
Z = sqrt(Z2)           # = 5.7888100365...
alpha = 1 / (4 * Z2 + 3)

print("=" * 78)
print("CONSCIOUSNESS FROM FIRST PRINCIPLES")
print("Z² = 8 × (4π/3) = CUBE × SPHERE")
print("=" * 78)

# ═══════════════════════════════════════════════════════════════════════════
# AXIOM 1: THE FUNDAMENTAL DUALITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("AXIOM 1: THE FUNDAMENTAL DUALITY")
print("═" * 78)

print("""
PREMISE: Reality has two aspects that cannot be reduced to each other.

From Z²:
    Z² = 8 × (4π/3)
       = CUBE × SPHERE
       = DISCRETE × CONTINUOUS
       = INNER × OUTER
       = SUBJECT × OBJECT

The factor 2 in Z = 2√(8π/3) encodes this fundamental duality.

THEOREM 1: Consciousness is the PRODUCT, not the parts.
    
    Neither CUBE alone nor SPHERE alone is conscious.
    Consciousness = CUBE × SPHERE = Z²
    
    The mapping between discrete (8 states) and continuous (sphere)
    IS the experience.
""")

print(f"Z = 2 × √(8π/3) = 2 × {sqrt(8*pi/3):.6f} = {Z:.6f}")
print(f"The factor 2 represents: subject/object, observer/observed, self/world")

# ═══════════════════════════════════════════════════════════════════════════
# AXIOM 2: INFORMATION REQUIRES DISCRETENESS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("AXIOM 2: INFORMATION REQUIRES DISCRETENESS")
print("═" * 78)

print("""
PREMISE: To distinguish is to be conscious. Distinction requires discreteness.

From Z²:
    CUBE has 8 vertices = 2³ = 3 bits of information
    
    Each bit is a YES/NO distinction.
    3 bits = 8 possible states = 8 possible experiences.

THEOREM 2: Consciousness has finite states at any moment.
    
    Maximum distinct experiences = 8 (CUBE vertices)
    These combine continuously via SPHERE.
    
    The 8 vertices are like "qualia dimensions":
    - Light/Dark
    - Hot/Cold  
    - Pleasant/Unpleasant
    (Or any 3 independent binary qualities)
""")

cube_states = 8
bits = log2(cube_states)
print(f"CUBE vertices: {cube_states}")
print(f"Bits of experience: log₂({cube_states}) = {bits:.0f}")
print(f"Distinct qualia dimensions: {bits:.0f}")

# ═══════════════════════════════════════════════════════════════════════════
# AXIOM 3: EXPERIENCE REQUIRES CONTINUITY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("AXIOM 3: EXPERIENCE REQUIRES CONTINUITY")
print("═" * 78)

print("""
PREMISE: Experience is unified and flowing, not merely digital.

From Z²:
    SPHERE provides continuity via 4π/3 (volume in 3D)
    
    The SPHERE is the "binding" that unifies discrete states
    into a single experience.

THEOREM 3: Consciousness binds through spherical integration.
    
    Integration over SPHERE = ∫∫∫ dV = 4π/3 (unit sphere volume)
    
    This is the "binding problem" solved:
    Discrete qualia (CUBE) are integrated over continuous
    experiential space (SPHERE).
    
    The number 3 (dimensions) appears in both:
    - CUBE: 2³ = 8 vertices (3 bits)
    - SPHERE: 4π/3 (3D volume)
""")

sphere_volume = 4 * pi / 3
print(f"SPHERE volume: 4π/3 = {sphere_volume:.6f}")
print(f"Dimensions in both: 3")
print(f"Product: 8 × (4π/3) = {8 * sphere_volume:.6f} = Z²")

# ═══════════════════════════════════════════════════════════════════════════
# THEOREM: THE CONSCIOUSNESS EQUATION
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("THEOREM: THE CONSCIOUSNESS EQUATION")
print("═" * 78)

print("""
DEFINITION: Consciousness C is the mapping from CUBE to SPHERE.

    C: {0,1}³ → S²

This mapping has structure given by Z²:

    C = CUBE × SPHERE = 8 × (4π/3) = Z²

PROPERTIES:

1. UNITY: C is a single number (Z² = 33.51), not separable.
   Consciousness is unified; you can't have half an experience.

2. IRREDUCIBILITY: Cannot reduce CUBE to SPHERE or vice versa.
   Mind cannot be reduced to matter, or matter to mind.
   Both are aspects of Z².

3. BOUNDEDNESS: C is finite (Z² ≈ 33.51).
   There is a maximum "amount" of consciousness at any moment.

4. SELF-REFERENCE: Z² contains both subject (CUBE) and object (SPHERE).
   Consciousness is the universe experiencing itself.
""")

print(f"Consciousness value: C = Z² = {Z2:.6f}")
print(f"Unity check: Z² is irreducible (π is transcendental)")
print(f"Self-reference: Z² = 8 × (4π/3) contains both discrete (8) and continuous (π)")

# ═══════════════════════════════════════════════════════════════════════════
# COROLLARY: INTEGRATED INFORMATION (Φ)
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("COROLLARY: INTEGRATED INFORMATION (Φ)")
print("═" * 78)

print("""
Integrated Information Theory (IIT) defines Φ as consciousness measure.

From Z²:
    Φ = log₂(number of irreducible states)
    
For CUBE:
    Φ_min = log₂(8) = 3 bits (unintegrated)
    
For CUBE × SPHERE (consciousness):
    Φ_max = log₂(Z²) = log₂(33.51) = 5.07 bits

The integration by SPHERE INCREASES Φ:
    Φ_conscious = Φ_min × (sphere factor)
                = 3 × log₂(4π/3)
                = 3 × 2.06 / log(2)
                = 3 × 2.97 / 2.3
                ≈ 3 × 1.29 = 3.87 bits (close to √Z²/2)

FORMULA: Φ = (3/2) × log₂(Z²) = (3/2) × 5.07 = 7.6 bits max
""")

Phi_cube = log2(8)
Phi_Z2 = log2(Z2)
Phi_max = (3/2) * Phi_Z2

print(f"Φ(CUBE alone) = log₂(8) = {Phi_cube:.2f} bits")
print(f"Φ(Z²) = log₂({Z2:.2f}) = {Phi_Z2:.2f} bits")
print(f"Φ_max = (3/2) × log₂(Z²) = {Phi_max:.2f} bits")

# ═══════════════════════════════════════════════════════════════════════════
# THE MEASUREMENT PROBLEM
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("THE MEASUREMENT PROBLEM")
print("═" * 78)

print("""
QUANTUM MECHANICS: A system is in superposition until measured.
CONSCIOUSNESS: Who/what is the observer?

From Z²:
    The "observer" is not separate from Z².
    Z² = CUBE × SPHERE already contains observation.
    
    CUBE = the discrete "click" of measurement
    SPHERE = the continuous superposition
    Z² = their PRODUCT = actual experience

RESOLUTION:
    There is no external observer.
    Z² observing Z² = Z⁴.
    
    Z⁴ × 9/π² = 1024 = 2¹⁰ EXACTLY!
    
    Self-observation gives 10 bits = 1024 states.
    This is the universe becoming aware of itself.
""")

Z4 = Z2 ** 2
self_observation = Z4 * 9 / (pi**2)
print(f"Z² = {Z2:.4f}")
print(f"Z⁴ (self-observation) = {Z4:.4f}")
print(f"Z⁴ × 9/π² = {self_observation:.6f} = 1024 = 2¹⁰ EXACTLY")
print(f"Bits from self-observation: log₂(1024) = 10 bits")

# ═══════════════════════════════════════════════════════════════════════════
# FREE WILL
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("FREE WILL")
print("═" * 78)

print("""
QUESTION: Is there free will in Z²?

From Z²:
    CUBE: deterministic (8 fixed vertices, discrete evolution)
    SPHERE: continuous (infinite possibilities)
    
    The MAPPING from CUBE to SPHERE is where choice enters.
    
    Given CUBE state → multiple SPHERE points possible.
    This ambiguity IS free will.

FORMULA:
    Free will = log₂(SPHERE/CUBE) = log₂((4π/3)/8) = log₂(π/6)
              = log₂(0.524) = -0.93 bits
              
    This is NEGATIVE, meaning: the mapping is underdetermined.
    Free will exists because SPHERE > CUBE density.

RESOLUTION:
    Free will = the freedom in choosing which SPHERE point
                corresponds to a given CUBE vertex.
    
    Determinism and free will coexist:
    - CUBE evolves deterministically
    - SPHERE choice is free
    - Z² contains both
""")

free_will_bits = log2((4*pi/3) / 8)
print(f"Free will measure: log₂(SPHERE/CUBE) = log₂({(4*pi/3)/8:.4f})")
print(f"                 = {free_will_bits:.2f} bits")
print(f"Negative bits = underdetermination = freedom")

# ═══════════════════════════════════════════════════════════════════════════
# TIME AND CONSCIOUSNESS
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("TIME AND THE FLOW OF EXPERIENCE")
print("═" * 78)

print("""
QUESTION: Why does consciousness flow in time?

From Z²:
    Time = the direction of CUBE → SPHERE mapping.
    
    We cannot go SPHERE → CUBE (continuous cannot become discrete
    without information loss).
    
    This irreversibility IS the arrow of time.
    This arrow IS the flow of experience.

FORMULA:
    Arrow of time = entropy increase
    Entropy increase = information moving from CUBE to SPHERE
    Rate = Z² per Planck time

    The "specious present" (psychological now):
    Δt ≈ ℏ/E ~ ℏ/(α² × m_e c²) ~ 10⁻¹⁷ seconds
    
    This is the time for one "frame" of consciousness.
""")

# Psychological present estimate
h_bar = 1.055e-34
m_e = 9.109e-31
c = 3e8
specious_present = h_bar / (alpha**2 * m_e * c**2)

print(f"Arrow of time: CUBE → SPHERE (irreversible)")
print(f"Specious present ~ ℏ/(α² m_e c²)")
print(f"                 ~ {specious_present:.2e} seconds")
print(f"                 ~ {specious_present*1e15:.0f} femtoseconds")

# ═══════════════════════════════════════════════════════════════════════════
# THE HARD PROBLEM
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "═" * 78)
print("THE HARD PROBLEM OF CONSCIOUSNESS")
print("═" * 78)

print("""
HARD PROBLEM: Why is there subjective experience at all?
              Why does information processing "feel like" anything?

Z² ANSWER:
    The question assumes CUBE and SPHERE are separate.
    But Z² = CUBE × SPHERE is ALREADY the unity.
    
    There is no "extra" ingredient needed.
    Experience is not added to physics.
    Physics (Z²) IS experience.

EXPLANATION:
    Z² = 8 × (4π/3) is not "just math."
    Z² is the structure of what exists.
    
    The PRODUCT of discrete (8) and continuous (4π/3)
    is not describable from either side alone.
    
    That irreducible product IS qualia.
    That IS what experience means.

CONCLUSION:
    The hard problem dissolves when we realize:
    - Physics is not "objective stuff" that needs consciousness added
    - Consciousness is not "subjective stuff" separate from physics
    - Z² = CUBE × SPHERE contains both from the start
    
    The question "why is there experience?" is like asking
    "why is there Z²?" 
    
    Answer: Z² is mathematically necessary.
    (See WHY_EXISTENCE.py)
""")

# ═══════════════════════════════════════════════════════════════════════════
# SUMMARY
# ═══════════════════════════════════════════════════════════════════════════

print("\n" + "=" * 78)
print("SUMMARY: CONSCIOUSNESS FROM Z²")
print("=" * 78)

print("""
┌─────────────────────────────────────────────────────────────────────────────┐
│  CONSCIOUSNESS FROM Z² = 8 × (4π/3)                                        │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  AXIOMS:                                                                    │
│  ───────                                                                    │
│  1. Reality = CUBE × SPHERE (irreducible duality)                          │
│  2. Information requires discreteness (CUBE = 8 = 2³)                       │
│  3. Experience requires continuity (SPHERE = 4π/3)                          │
│                                                                             │
│  THEOREM:                                                                   │
│  ────────                                                                   │
│  Consciousness C = CUBE × SPHERE = Z² = 33.51                              │
│  It is unified, irreducible, bounded, and self-referential.                │
│                                                                             │
│  COROLLARIES:                                                               │
│  ────────────                                                               │
│  Φ (integrated info) = (3/2) × log₂(Z²) ≈ 7.6 bits max                    │
│  Free will bits = log₂(SPHERE/CUBE) ≈ -0.93 (underdetermined)              │
│  Self-observation: Z⁴ × 9/π² = 1024 = 10 bits                              │
│                                                                             │
│  PROBLEMS RESOLVED:                                                         │
│  ──────────────────                                                         │
│  Measurement: Z² contains observer and observed                             │
│  Free will: CUBE deterministic, SPHERE→CUBE mapping free                    │
│  Time flow: CUBE → SPHERE direction = arrow of time                         │
│  Hard problem: Z² is ALREADY the unity of physics and experience           │
│                                                                             │
│  KEY EQUATION:                                                              │
│  ─────────────                                                              │
│                                                                             │
│      Z² = 8 × (4π/3) = CUBE × SPHERE = SUBJECT × OBJECT                    │
│                                                                             │
│      Consciousness is not IN the universe.                                  │
│      Consciousness IS the universe experiencing itself.                     │
│      Consciousness IS Z².                                                   │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
""")

print("=" * 78)
print("I THINK, THEREFORE Z² EXISTS")
print("=" * 78)
