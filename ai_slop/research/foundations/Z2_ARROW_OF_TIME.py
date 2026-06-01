#!/usr/bin/env python3
"""
THE ARROW OF TIME FROM Z²
=========================

Why does time flow forward?
Why does entropy increase?
Why can we remember the past but not the future?

The cube geometry provides the answer.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np

print("=" * 80)
print("THE ARROW OF TIME FROM Z²")
print("=" * 80)

# Constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
CUBE = 8
BEKENSTEIN = 4
N_GEN = 3
GAUGE = 12
FACES = 6
TIME = BEKENSTEIN - N_GEN  # = 1

print(f"""
THE MYSTERY OF TIME:

All fundamental physics equations are TIME-REVERSIBLE:
• Newton's laws: F = ma (same backwards)
• Maxwell's equations: symmetric in t → -t
• Schrödinger equation: unitary evolution
• Einstein's equations: symmetric

YET WE OBSERVE:
• Time flows ONE direction
• Entropy INCREASES
• We remember the PAST, not future
• Cause precedes effect

THIS IS THE ARROW OF TIME.

Where does it come from?
The answer lies in the cube.
""")

# =============================================================================
# PART 1: THE THREE ARROWS
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE THREE ARROWS OF TIME")
print("=" * 80)

print(f"""
THERE ARE THREE "ARROWS":

1. THERMODYNAMIC ARROW:
   Entropy increases: dS ≥ 0
   The second law of thermodynamics

2. COSMOLOGICAL ARROW:
   The universe expands: da/dt > 0
   Space grows larger over time

3. PSYCHOLOGICAL ARROW:
   We remember the past, not the future
   Consciousness flows forward

ARE THESE CONNECTED?

Yes! All three derive from the same source:
THE CUBE'S GEOMETRY.

In particular:
TIME = BEKENSTEIN - N_gen = 4 - 3 = 1

This tells us time is ONE-DIMENSIONAL.
But why does it have a DIRECTION?
""")

# =============================================================================
# PART 2: THE ORIGIN AS SPECIAL POINT
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: THE ORIGIN AS SPECIAL POINT")
print("=" * 80)

print(f"""
THE CUBE HAS A SPECIAL VERTEX:

The 8 vertices are:
(0,0,0), (0,0,1), (0,1,0), (0,1,1)
(1,0,0), (1,0,1), (1,1,0), (1,1,1)

One vertex is SPECIAL: the ORIGIN (0,0,0)

WHY THE ORIGIN IS SPECIAL:

• It's the "zero" of the coordinate system
• It's in tetrahedron A (the "matter" side)
• It's the natural starting point

THE OPPOSITE VERTEX:

(1,1,1) is the "far corner"
• Maximum distance from origin
• In tetrahedron B (the "antimatter" side)
• The natural "endpoint"

THE ARROW:

The cube has a natural direction:
(0,0,0) → (1,1,1)

This is THE ARROW OF TIME.

Origin (t=0) → Far corner (t=∞)
Big Bang → Heat Death
Low entropy → High entropy
Past → Future
""")

# =============================================================================
# PART 3: ENTROPY AND THE CUBE
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: ENTROPY FROM THE CUBE")
print("=" * 80)

print(f"""
THE SECOND LAW:

dS/dt ≥ 0 (entropy increases)

WHY?

THE CUBE EXPLANATION:

At the origin (0,0,0):
• Only 1 vertex = 1 microstate
• S = log(1) = 0

At the far corner (1,1,1):
• All paths lead here eventually
• Many microstates correspond to this macro state
• S = maximum

THE RANDOM WALK:

Imagine a random walk on cube vertices:
• Start at (0,0,0)
• At each step, move along one edge
• The walk explores more and more vertices

COUNTING STATES:

After n steps:
• Number of accessible vertices grows
• Eventually reaches equilibrium (all 8)
• S_max = log(8) = log(CUBE) = 3 bits

THE ARROW:

The walk is BIASED:
• More vertices are "away" from origin than "toward"
• Random motion → net flow AWAY from origin
• This is the THERMODYNAMIC ARROW

ENTROPY INCREASES BECAUSE THERE ARE MORE STATES
IN THE "FUTURE DIRECTION" THAN "PAST DIRECTION".
""")

# =============================================================================
# PART 4: THE TWO TETRAHEDRA AND TIME
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: THE TWO TETRAHEDRA")
print("=" * 80)

print(f"""
THE TETRAHEDRA AS PAST AND FUTURE:

TETRAHEDRON A (origin side):
Vertices: (0,0,0), (0,1,1), (1,0,1), (1,1,0)
Contains the origin
Represents: THE PAST

TETRAHEDRON B (far corner side):
Vertices: (0,0,1), (0,1,0), (1,0,0), (1,1,1)
Contains the far corner
Represents: THE FUTURE

THE CAUSALITY STRUCTURE:

Light cones in spacetime:
• Past light cone = events that CAN affect here
• Future light cone = events that here CAN affect

THE CUBE VERSION:

• Tetrahedron A = past light cone
• Tetrahedron B = future light cone
• The EDGES connect them (causal links)

NUMBER OF CONNECTIONS:

Each A vertex connects to 3 B vertices.
3 = N_gen = N_space

The CAUSAL STRUCTURE IS ENCODED IN THE CUBE.

The 12 edges (GAUGE) are the 12 causal connections.
Each connects past to future.
""")

# =============================================================================
# PART 5: WHY WE CAN'T GO BACK
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: WHY TIME TRAVEL IS FORBIDDEN")
print("=" * 80)

print(f"""
CAN WE GO BACK IN TIME?

THE CUBE ANSWER: NO.

WHY:

The cube's symmetry is 48-fold:
• 24 rotations (proper symmetries)
• 24 reflection-rotations (improper)

But NOT ALL permutations of vertices are symmetries.
8! = 40,320 possible permutations
Only 48 are symmetries.

THE FORBIDDEN OPERATION:

Exchanging tetrahedra A ↔ B requires PARITY REVERSAL.
This is NOT a continuous transformation.

You cannot smoothly go from A to B.
You cannot smoothly go from past to future.

TIME TRAVEL REQUIRES DISCONTINUOUS TRANSFORMATION.
This is topologically forbidden.

THE TOPOLOGY:

Tetrahedron A and B are LINKED.
Like two linked rings, they cannot be separated.
But they CANNOT be exchanged without cutting.

TIME FLOWS FORWARD BECAUSE A→B IS ALLOWED,
BUT B→A REQUIRES BREAKING THE GEOMETRY.
""")

# =============================================================================
# PART 6: THE BIG BANG AS THE ORIGIN
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: THE BIG BANG")
print("=" * 80)

# Calculate entropy ratio
S_initial = 3  # bits (one cube)
S_final = 122 * np.log2(10)  # bits (holographic bound ~ 10^122)
ratio = S_final / S_initial

print(f"""
THE INITIAL CONDITION:

At t = 0 (Big Bang):
• The universe was ONE Planck cube
• Entropy: S = log(CUBE) = 3 bits
• This is the ORIGIN (0,0,0) state

WHY WAS IT SO SPECIAL?

The origin is UNIQUE:
• Only one "lowest" vertex
• Minimum entropy configuration
• Maximum order

THE COSMOLOGICAL ARROW:

The universe expands: (0,0,0) → (1,1,1) direction
Space grows, entropy grows, time flows.

ENTROPY GROWTH:

Initial: S_i = {S_initial} bits
Final: S_f ~ 10^122 bits ≈ {S_final:.0f} bits
Ratio: S_f/S_i ≈ {ratio:.2e}

This enormous growth is "natural":
The universe simply explored more of the cube.

THE ARROW OF TIME EXISTS BECAUSE
THE BIG BANG WAS AT THE ORIGIN.

If the universe started at (1,1,1), time would run backwards!
(But that's not "backwards" - it's just relabeling.)
""")

# =============================================================================
# PART 7: MEMORY AND RECORDS
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: MEMORY AND RECORDS")
print("=" * 80)

print(f"""
THE PSYCHOLOGICAL ARROW:

Why do we remember the past but not the future?

THE CUBE ANSWER:

Memory is a RECORD of causation.
Causation flows A → B (past → future).
Records are LEFT BEHIND as we move forward.

THE MECHANISM:

At vertex v_past in tetrahedron A:
• Events happen
• Information is encoded in v_past

We then move to vertex v_future in tetrahedron B:
• We carry EDGES connecting to v_past
• These edges are MEMORY

COUNT THE EDGES:

Each B vertex connects to 3 A vertices.
We have 3 = N_gen memory channels.
(3 spatial dimensions = 3 ways to store information)

WHY NOT FUTURE MEMORY?

B vertices don't connect AHEAD to more B vertices.
They only connect BACK to A.

Memory works like this:
• Standing at B
• Looking back at A (via edges)
• Cannot "look forward" to more B

THE PSYCHOLOGICAL ARROW FOLLOWS THE THERMODYNAMIC ARROW.
""")

# =============================================================================
# PART 8: CPT AND TIME REVERSAL
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: CPT SYMMETRY")
print("=" * 80)

print(f"""
CPT THEOREM:

All physical laws are invariant under:
C: Charge conjugation (particle ↔ antiparticle)
P: Parity (mirror reflection)
T: Time reversal

THE CUBE VERSION:

C: Swap tetrahedra A ↔ B (matter ↔ antimatter)
P: Reflect cube through center (x,y,z) → (1-x,1-y,1-z)
T: Reverse the arrow (0,0,0) ↔ (1,1,1)

INDIVIDUALLY:
• C alone: takes A→B (not a cube symmetry alone)
• P alone: takes (x,y,z)→(1-x,1-y,1-z) (IS a symmetry)
• T alone: reverses time direction

COMBINED CPT:
• Do C (swap A↔B)
• Do P (reflect)
• Do T (reverse time)

Result: Full symmetry restored!

THE CUBE IS CPT INVARIANT.

Each operation alone may not be symmetric.
But CPT combined IS a cube symmetry (the antipodal map).

THE ARROW OF TIME EXISTS, BUT CPT IS CONSERVED.
""")

# =============================================================================
# PART 9: THE QUANTUM MECHANICAL ARROW
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: QUANTUM MEASUREMENT")
print("=" * 80)

print(f"""
THE MEASUREMENT PROBLEM:

Before measurement: superposition |ψ⟩ = α|0⟩ + β|1⟩
After measurement: definite state |0⟩ or |1⟩

This is IRREVERSIBLE!
Information is "lost" to the environment.

THE CUBE PICTURE:

Before measurement:
• System at one vertex
• Superposition over connected vertices
• All edges "active"

After measurement:
• System collapsed to one edge direction
• Other edges "frozen"
• Information went to environment

THE DECOHERENCE:

The 12 edges (GAUGE) provide decoherence channels.
Each edge can transfer information to environment.

Decoherence time ~ 1/(GAUGE × rate)
                 = 1/(12 × rate)

THE MEASUREMENT ARROW:

Measurement moves information from system to environment.
This is THE SAME DIRECTION as thermodynamic arrow.

Measurement increases total entropy.
Measurement is IRREVERSIBLE.

THE QUANTUM ARROW = THE THERMODYNAMIC ARROW.
""")

# =============================================================================
# PART 10: THE BLOCK UNIVERSE
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: IS TIME REAL?")
print("=" * 80)

print(f"""
THE BLOCK UNIVERSE:

Einstein's relativity suggests:
• Past, present, future all "exist"
• Time is a 4th dimension
• "Flow" is an illusion

THE CUBE PERSPECTIVE:

The cube exists TIMELESSLY as a mathematical structure.
All 8 vertices exist simultaneously (in the math).

But the PHYSICAL INTERPRETATION requires an arrow:
• We start at (0,0,0)
• We experience vertices in sequence
• We end at (1,1,1)

THE RESOLUTION:

BOTH views are correct:

TIMELESS VIEW (God's eye):
• The cube is eternal
• All vertices exist
• No preferred direction

TIME-BOUND VIEW (inside view):
• We're at one vertex
• We experience flow
• Arrow points toward higher entropy

THE ARROW OF TIME IS PERSPECTIVAL.

It exists FOR US, embedded in the structure.
The structure itself is timeless.

TIME = BEKENSTEIN - N_gen = 4 - 3 = 1

This tells us there is ONE time dimension.
The arrow comes from the ORIGIN being special.
""")

# =============================================================================
# PART 11: ENTROPY FORMULA
# =============================================================================

print("\n" + "=" * 80)
print("PART 11: THE ENTROPY FORMULA")
print("=" * 80)

print(f"""
THE Z² ENTROPY FORMULA:

S(t) = S_max × (1 - exp(-t/τ))

where:
S_max = log(CUBE) = 3 bits (maximum entropy)
τ = characteristic time ~ 1/Z² (relaxation time)

AT DIFFERENT TIMES:

t = 0: S = 0 (Big Bang, origin)
t = τ: S = S_max × (1 - 1/e) ≈ 0.63 × S_max
t → ∞: S → S_max = 3 bits (heat death, far corner)

THE RATE OF ENTROPY INCREASE:

dS/dt = (S_max/τ) × exp(-t/τ)
      = Z² × S_max × exp(-t/τ)

Initially: dS/dt = Z² × S_max ≈ 33.5 × 3 ≈ 100 bits/unit time
Finally: dS/dt → 0 (equilibrium)

THE COSMOLOGICAL CONNECTION:

The universe's entropy:
S_universe ~ (R/ℓ_P)² (holographic bound)

Since R grows with time:
S grows as t^(2/3) in matter era
S grows exponentially in de Sitter era

THE ARROW OF TIME STRENGTH VARIES:
Early universe: Strong arrow (fast entropy growth)
Far future: Weak arrow (near equilibrium)
""")

# =============================================================================
# PART 12: SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PART 12: SUMMARY - THE ARROW OF TIME")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║                     THE ARROW OF TIME FROM Z²                                ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  THE THREE ARROWS:                                                          ║
║  • Thermodynamic: entropy increases (S → S_max)                             ║
║  • Cosmological: universe expands (origin → far corner)                     ║
║  • Psychological: we remember past (edges point backward)                   ║
║                                                                              ║
║  THE CUBE ORIGIN:                                                           ║
║  • The origin (0,0,0) is SPECIAL - minimum entropy                          ║
║  • The far corner (1,1,1) is maximum entropy                                ║
║  • Arrow: (0,0,0) → (1,1,1)                                                 ║
║                                                                              ║
║  THE TWO TETRAHEDRA:                                                        ║
║  • Tetrahedron A = past (contains origin)                                   ║
║  • Tetrahedron B = future (contains far corner)                             ║
║  • 12 edges (GAUGE) connect them causally                                   ║
║                                                                              ║
║  WHY NO TIME TRAVEL:                                                        ║
║  • A → B is continuous (allowed)                                            ║
║  • B → A requires topology change (forbidden)                               ║
║                                                                              ║
║  CPT SYMMETRY:                                                              ║
║  • T alone is NOT a symmetry (arrow exists)                                 ║
║  • CPT combined IS a symmetry (antipodal map)                               ║
║                                                                              ║
║  THE DEEP ANSWER:                                                           ║
║  Time has an arrow because THE BIG BANG WAS AT THE ORIGIN.                  ║
║  The origin has minimum entropy, so entropy can only grow.                  ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

THE ARROW OF TIME IS GEOMETRIC.

WE EXPERIENCE TIME'S FLOW BECAUSE WE'RE MOVING
FROM (0,0,0) TO (1,1,1) IN THE CUBE.

THE CUBE ITSELF IS TIMELESS.
TIME IS OUR PATH THROUGH IT.

=== END OF ARROW OF TIME ANALYSIS ===
""")

if __name__ == "__main__":
    pass
