#!/usr/bin/env python3
"""
THE PRINCIPLE OF LEAST ACTION FROM Z²
======================================

The principle of least action is the deepest principle in physics:

"Nature chooses the path that minimizes the action."

S = ∫ L dt

Why does nature do this? The cube geometry provides the answer.

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np

print("=" * 80)
print("THE PRINCIPLE OF LEAST ACTION FROM Z²")
print("=" * 80)

# Constants
Z_SQUARED = 32 * np.pi / 3
Z = np.sqrt(Z_SQUARED)
CUBE = 8
GAUGE = 12
FACES = 6
BEKENSTEIN = 4
N_GEN = 3
TIME = BEKENSTEIN - N_GEN

print("""
THE DEEPEST PRINCIPLE:

All of physics follows from ONE principle:

    δS = 0

The action S = ∫ L dt is stationary (usually minimal).

From this single principle:
• Newton's laws
• Maxwell's equations
• Einstein's equations
• Quantum mechanics (path integral)
• The Standard Model

WHY does nature minimize action?
The cube tells us.
""")

# =============================================================================
# PART 1: THE ACTION IN PHYSICS
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: WHAT IS ACTION?")
print("=" * 80)

print(f"""
THE ACTION FUNCTIONAL:

S[path] = ∫ L(q, q̇, t) dt

where L = T - V is the Lagrangian.

EXAMPLES:

Classical mechanics:
S = ∫ (½mv² - V(x)) dt

Electromagnetism:
S = ∫ (-¼F_μν F^μν) d⁴x

General relativity:
S = ∫ R/(16πG) √(-g) d⁴x

The Standard Model:
S = ∫ (gauge + fermion + Higgs + Yukawa) d⁴x

THE Z² COEFFICIENTS:

Notice the 16π in GR action:
16π = 2 × 8π = 2 × (3Z²/4) = 3Z²/2

And the ¼ in EM action:
¼ = 1/BEKENSTEIN

THE ACTION IS BUILT FROM Z² NUMBERS!
""")

# =============================================================================
# PART 2: PATH COUNTING ON THE CUBE
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: PATH COUNTING ON THE CUBE")
print("=" * 80)

print(f"""
PATHS ON THE CUBE:

Consider paths from origin (0,0,0) to far corner (1,1,1).

SHORTEST PATH:
• Minimum 3 edges (one in each direction)
• There are 3! = 6 such paths

ALL PATHS:
• Can revisit edges, take longer routes
• Infinitely many paths

THE CUBE'S PATH STRUCTURE:

From any vertex, there are 3 possible next steps.
Each step moves along one edge.

PATH LENGTH = number of edges traversed
MINIMUM PATH = 3 (for origin to far corner)

THE ACTION ANALOGY:

Path on cube ↔ Trajectory in spacetime
Edge count ↔ Action S
Minimum edges ↔ Minimum action

WHY MINIMUM?

The 6 shortest paths (length 3) are SPECIAL:
• They're geodesics on the cube
• They minimize "edge action"
• There are exactly FACES = 6 of them!

THE CUBE NATURALLY SELECTS SHORTEST PATHS.
""")

# =============================================================================
# PART 3: THE FEYNMAN PATH INTEGRAL
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: THE PATH INTEGRAL")
print("=" * 80)

print(f"""
FEYNMAN'S FORMULATION:

The quantum amplitude is:

K(b,a) = ∫ exp(iS[path]/ℏ) D[path]

Sum over ALL paths, weighted by exp(iS/ℏ).

THE CLASSICAL LIMIT:

When S >> ℏ:
• Nearby paths interfere destructively
• Only paths near δS = 0 survive
• Classical trajectory emerges

THE CUBE VERSION:

Sum over all cube paths:
K = Σ_paths exp(i × edge_count × θ)

where θ is a phase factor.

DESTRUCTIVE INTERFERENCE:

Long paths: Many edges → large phase → cancel out
Short paths: Few edges → small phase → add coherently

THE MINIMUM PATH SURVIVES!

K ≈ (number of shortest paths) × exp(i × 3 × θ)
  = FACES × exp(3iθ)
  = 6 × exp(3iθ)

THE PATH INTEGRAL SELECTS THE GEODESICS.
""")

# =============================================================================
# PART 4: THE PRINCIPLE FROM INFORMATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: LEAST ACTION FROM INFORMATION")
print("=" * 80)

print(f"""
THE INFORMATION INTERPRETATION:

Action S has units of [Energy × Time] = [ℏ].
S/ℏ is DIMENSIONLESS - it counts something!

WHAT DOES ACTION COUNT?

Proposal: S/ℏ counts INFORMATION TRANSFER.

THE CUBE VERSION:

Each edge crossing transfers 1 bit of information.
Minimum path = minimum information transfer.
Minimum action = minimum bits.

THE PRINCIPLE:

NATURE MINIMIZES INFORMATION TRANSFER.

Why? Because:
• Information costs energy (Landauer)
• Minimum energy → minimum information
• δS = 0 ↔ minimum bits

THE FORMULA:

S/ℏ = number of fundamental operations
    = number of Planck-scale edge crossings
    = information content of the path

For classical path: S/ℏ >> 1 (many operations)
For quantum path: S/ℏ ~ 1 (few operations)

THE QUANTUM OF ACTION IS ONE EDGE CROSSING.
""")

# =============================================================================
# PART 5: THE LAGRANGIAN FROM THE CUBE
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: THE LAGRANGIAN STRUCTURE")
print("=" * 80)

print(f"""
WHY L = T - V?

The Lagrangian is:
L = Kinetic energy - Potential energy

NOT L = T + V (total energy).
Why the minus sign?

THE CUBE ANSWER:

The two tetrahedra represent:
• Tetrahedron A: kinetic (motion, change)
• Tetrahedron B: potential (position, storage)

THE MINUS SIGN:

The tetrahedra are OPPOSITE parity.
A has even parity: +
B has odd parity: -

L = T_A - T_B = T - V

THE MINUS SIGN COMES FROM TETRAHEDRA PARITY!

THE EULER-LAGRANGE EQUATIONS:

d/dt(∂L/∂q̇) = ∂L/∂q

This says: rate of change of momentum = force.

THE CUBE VERSION:

Momentum lives on edges (GAUGE = 12 components in phase space).
Force lives on faces (FACES = 6 directions).
The equation connects them.

∂L/∂q̇ ~ edge structure
∂L/∂q ~ face structure
d/dt ~ time evolution (along diagonal)
""")

# =============================================================================
# PART 6: THE EINSTEIN-HILBERT ACTION
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: GRAVITY FROM THE CUBE")
print("=" * 80)

print(f"""
THE EINSTEIN-HILBERT ACTION:

S_EH = ∫ R/(16πG) √(-g) d⁴x

THE 16π FACTOR:

16π = 2 × 8π = 2 × CUBE × π

In Z² terms:
16π = 3Z²/2 × (4/3) = 2Z²

So the GR action is:

S_EH = ∫ R/(2Z²G) √(-g) d⁴x
     = (1/2Z²) × ∫ R/G √(-g) d⁴x

THE INTERPRETATION:

The factor 1/Z² appears because:
• Gravity couples to the VOLUME of the cube
• Volume = (sphere volume)/(cube count) = (4π/3)/8 = Z²/8

More precisely:
1/(16πG) = 1/(2 × CUBE × π × G)

CUBE appears explicitly in the gravitational action!

THE COSMOLOGICAL CONSTANT:

S_Λ = -∫ Λ/(8πG) √(-g) d⁴x

Here 8π = CUBE × π appears.

Λ/(8πG) = Λ/(CUBE × π × G)

THE CUBE IS IN THE GRAVITATIONAL ACTION.
""")

# =============================================================================
# PART 7: GAUGE THEORY ACTIONS
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: GAUGE THEORY FROM THE CUBE")
print("=" * 80)

print(f"""
THE YANG-MILLS ACTION:

S_YM = ∫ (-1/4g²) Tr(F_μν F^μν) d⁴x

THE FACTOR ¼:

¼ = 1/BEKENSTEIN

This is NOT arbitrary!

THE INTERPRETATION:

The gauge field strength F_μν lives on PLAQUETTES (faces).
But the action is about DIAGONALS (the physical degrees of freedom).

# faces / # diagonals = FACES / BEKENSTEIN = 6/4 = 3/2

The ¼ normalizes the action correctly.

THE COUPLING CONSTANT:

g² ~ 1/α

For electromagnetism: 1/g² = α⁻¹/4 = (4Z² + 3)/4 ≈ Z²

THE GAUGE ACTION:

S_gauge = (1/BEKENSTEIN) × (1/g²) × ∫ Tr(F²) d⁴x
        ≈ (1/4) × Z² × ∫ Tr(F²) d⁴x

Z² AND BEKENSTEIN APPEAR IN THE GAUGE ACTION.
""")

# =============================================================================
# PART 8: QUANTUM CORRECTIONS
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: QUANTUM CORRECTIONS")
print("=" * 80)

print(f"""
THE EFFECTIVE ACTION:

In quantum field theory, the classical action gets corrections:

Γ[φ] = S[φ] + ℏS₁[φ] + ℏ²S₂[φ] + ...

THE LOOP EXPANSION:

S₁ = one-loop correction (∝ ln(Λ/μ))
S₂ = two-loop correction
...

THE Z² STRUCTURE:

Each loop contributes a factor related to:
• GAUGE = 12 (gauge field loops)
• CUBE = 8 (vertex loops)
• FACES = 6 (plaquette loops)

THE BETA FUNCTIONS:

For SU(N) gauge theory:
β(g) = -b₀ g³/(16π²) + ...

where 16π² = (4π)² = (Z²)² × (3/8)² ≈ Z⁴/7

THE RUNNING INVOLVES Z⁴!

THE ANOMALOUS DIMENSIONS:

γ = c × g²/(16π²) = c × g²/Z⁴ × 7

The quantum corrections are suppressed by Z⁴.
This explains why perturbation theory works!
""")

# =============================================================================
# PART 9: THE PRINCIPLE OF STATIONARY ACTION
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: WHY STATIONARY, NOT MINIMUM?")
print("=" * 80)

print(f"""
STATIONARY VS MINIMUM:

The principle is δS = 0 (stationary), not S = min.
Sometimes S is a maximum or saddle point!

THE CUBE EXPLANATION:

The cube has 8 vertices.
Paths can go "up" (toward more 1's) or "down" (toward fewer 1's).

FROM ORIGIN TO FAR CORNER:
• Only "up" moves possible
• S is MINIMUM

FROM MIDDLE TO MIDDLE:
• Both "up" and "down" possible
• S is STATIONARY (saddle point)

THE TOPOLOGY:

The cube's Euler characteristic: χ = V - E + F = 8 - 12 + 6 = 2

This equals 2 = 1 + 1 (genus 0 surface).

For genus g surface: χ = 2 - 2g

The cube (χ = 2, g = 0) has:
• Minimum along one direction
• Maximum along perpendicular direction
• Saddle points exist!

THE PRINCIPLE IS STATIONARY BECAUSE THE CUBE HAS χ = 2.
""")

# =============================================================================
# PART 10: NOETHER'S THEOREM
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: SYMMETRY AND CONSERVATION")
print("=" * 80)

print(f"""
NOETHER'S THEOREM:

Every continuous symmetry → a conservation law.

THE CUBE'S SYMMETRIES:

48 symmetries total:
• 24 rotations (proper)
• 24 reflections (improper)

CONTINUOUS vs DISCRETE:

The cube has DISCRETE symmetries.
But at large scales, discrete → continuous.

THE CONSERVATION LAWS:

From rotations around axes (3 axes):
→ Angular momentum conservation (3 components)
→ N_gen = 3 ✓

From translations (3 directions):
→ Linear momentum conservation (3 components)
→ N_space = 3 ✓

From time translation (1 direction):
→ Energy conservation (1 component)
→ N_time = 1 ✓

THE CUBE HAS 3 + 3 + 1 = 7 CONSERVED QUANTITIES.

In phase space: 7 = ?
Actually, it's 10 for Poincaré group (4 translations + 6 rotations).

THE CUBE'S 12 EDGES CONNECT TO:
• 6 rotations (Lorentz)
• 4 translations (Poincaré)
• 2 extra (scale? conformal?)

GAUGE = 12 might encode the FULL spacetime symmetry!
""")

# =============================================================================
# PART 11: THE HAMILTONIAN FORMULATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 11: HAMILTONIAN FROM THE CUBE")
print("=" * 80)

print(f"""
THE LEGENDRE TRANSFORM:

H = Σ p_i q̇_i - L

THE CUBE PICTURE:

Lagrangian L lives on VERTICES (configuration space).
Hamiltonian H lives on EDGES (phase space).

The Legendre transform is:
VERTEX description → EDGE description

THE PHASE SPACE:

For N degrees of freedom:
• N positions q_i
• N momenta p_i
• 2N-dimensional phase space

For the cube (N = 3):
Phase space is 6-dimensional = FACES!

HAMILTON'S EQUATIONS:

dq/dt = ∂H/∂p
dp/dt = -∂H/∂q

These describe flow on the 6D phase space.

THE CUBE CONNECTION:

• 6 faces = 6D phase space
• 12 edges = 12 canonical variables (6 q's + 6 p's? No, 3+3=6)
• 8 vertices = 8 states (Hamiltonian eigenstates)

THE ENERGY SPECTRUM:

H|n⟩ = E_n|n⟩

For the cube: n = 0,1,...,7 (8 states)
E_n ~ n (linear spectrum for simple systems)

THE CUBE HAS 8 ENERGY EIGENSTATES.
""")

# =============================================================================
# PART 12: SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PART 12: SUMMARY - ACTION FROM Z²")
print("=" * 80)

print(f"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║               THE PRINCIPLE OF LEAST ACTION FROM Z²                          ║
║                                                                              ║
╠══════════════════════════════════════════════════════════════════════════════╣
║                                                                              ║
║  WHY DOES NATURE MINIMIZE ACTION?                                           ║
║                                                                              ║
║  1. PATH COUNTING:                                                          ║
║     • Shortest paths on cube = geodesics                                    ║
║     • 6 shortest paths (origin to far corner) = FACES                       ║
║     • Minimum edges = minimum action                                        ║
║                                                                              ║
║  2. PATH INTEGRAL:                                                          ║
║     • Long paths interfere destructively                                    ║
║     • Short paths add coherently                                            ║
║     • Classical limit selects minimum                                       ║
║                                                                              ║
║  3. INFORMATION:                                                            ║
║     • S/ℏ = number of edge crossings = bits                                 ║
║     • Minimum action = minimum information transfer                         ║
║     • Nature is efficient                                                   ║
║                                                                              ║
║  THE Z² STRUCTURE IN ACTIONS:                                               ║
║                                                                              ║
║  • GR: 16π = 2 × CUBE × π = 3Z²/2 × (4/3)                                  ║
║  • YM: 1/4 = 1/BEKENSTEIN                                                   ║
║  • Quantum: 16π² = Z⁴ × (something)                                         ║
║                                                                              ║
║  THE LAGRANGIAN:                                                            ║
║  • L = T - V (tetrahedra parities: + and -)                                 ║
║  • Kinetic = Tetrahedron A                                                  ║
║  • Potential = Tetrahedron B                                                ║
║                                                                              ║
║  THE HAMILTONIAN:                                                           ║
║  • Phase space = FACES = 6 dimensions                                       ║
║  • Energy eigenstates = CUBE = 8 states                                     ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝

THE PRINCIPLE OF LEAST ACTION IS GEOMETRY.

NATURE MINIMIZES ACTION BECAUSE THE CUBE SELECTS SHORTEST PATHS.

δS = 0 IS THE CUBE'S WAY OF SAYING "TAKE THE GEODESIC."

=== END OF LEAST ACTION ANALYSIS ===
""")

if __name__ == "__main__":
    pass
