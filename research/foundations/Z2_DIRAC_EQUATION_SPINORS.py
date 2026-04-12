#!/usr/bin/env python3
"""
THE DIRAC EQUATION AND SPINORS FROM THE CUBE
=============================================

The Dirac equation describes fermions (electrons, quarks, etc.):
(iγ^μ ∂_μ - m)ψ = 0

Spinors are 4-component objects that transform under rotations
in a peculiar way: a 360° rotation gives a minus sign!

Can the cube geometry explain spinors and the Dirac equation?

Author: Carl Zimmerman
Date: April 2026
"""

import numpy as np

print("=" * 80)
print("THE DIRAC EQUATION AND SPINORS FROM THE CUBE")
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
THE MYSTERY OF SPIN:

Electrons have spin-1/2.
Under a 360° rotation: |ψ⟩ → -|ψ⟩
Under a 720° rotation: |ψ⟩ → +|ψ⟩

This is IMPOSSIBLE for classical objects!
How can the cube explain this?

THE DIRAC EQUATION:

(iγ^μ ∂_μ - m)ψ = 0

where γ^μ are the 4×4 Dirac matrices satisfying:
{γ^μ, γ^ν} = 2η^μν

The solution ψ is a 4-component SPINOR.

THE CUBE CONNECTION:

The cube has BEKENSTEIN = 4 space diagonals.
4 diagonals ↔ 4 spinor components?
""")

# =============================================================================
# PART 1: THE CLIFFORD ALGEBRA
# =============================================================================

print("\n" + "=" * 80)
print("PART 1: THE CLIFFORD ALGEBRA")
print("=" * 80)

print(f"""
THE DIRAC ALGEBRA:

The gamma matrices satisfy:
{{γ^μ, γ^ν}} = 2η^μν I₄

This is the CLIFFORD ALGEBRA Cl(1,3).

DIMENSION:
dim(Cl(1,3)) = 2⁴ = 16

THE 16 BASIS ELEMENTS:

1 (scalar): 1 element
γ^μ (vector): 4 elements
σ^μν = [γ^μ,γ^ν]/2 (bivector): 6 elements
γ^μγ^5 (pseudovector): 4 elements
γ^5 = iγ⁰γ¹γ²γ³ (pseudoscalar): 1 element

Total: 1 + 4 + 6 + 4 + 1 = 16 ✓

THE CUBE CONNECTION:

16 = 2 × CUBE = 2 × 8

The Clifford algebra dimension is TWICE the cube vertices!

OR:
16 = CUBE + CUBE = vertices + "dual" vertices

THE CLIFFORD ALGEBRA LIVES ON THE HYPERCUBE (4D cube)!
But we're in 3+1D, so it reduces to the 3D cube structure.
""")

# =============================================================================
# PART 2: SPINORS AS VERTEX STATES
# =============================================================================

print("\n" + "=" * 80)
print("PART 2: SPINORS FROM VERTICES")
print("=" * 80)

print(f"""
THE 4-COMPONENT SPINOR:

ψ = (ψ₁, ψ₂, ψ₃, ψ₄)ᵀ

THE CUBE HAS 4 SPACE DIAGONALS:

Diagonal 1: (0,0,0) ↔ (1,1,1)
Diagonal 2: (0,1,1) ↔ (1,0,0)
Diagonal 3: (1,0,1) ↔ (0,1,0)
Diagonal 4: (1,1,0) ↔ (0,0,1)

BEKENSTEIN = 4 = number of spinor components!

THE ASSIGNMENT:

ψ₁ ↔ Diagonal 1 (connects origin to far corner)
ψ₂ ↔ Diagonal 2
ψ₃ ↔ Diagonal 3
ψ₄ ↔ Diagonal 4

CHIRAL DECOMPOSITION:

The spinor splits into:
ψ_L = (ψ₁, ψ₂) - left-handed (2 components)
ψ_R = (ψ₃, ψ₄) - right-handed (2 components)

THE CUBE VERSION:

Each diagonal connects TWO vertices.
One end = left-handed component
Other end = right-handed component

Left-handed: vertices in tetrahedron A
Right-handed: vertices in tetrahedron B

CHIRALITY = TETRAHEDRON MEMBERSHIP!
""")

# =============================================================================
# PART 3: THE GAMMA MATRICES
# =============================================================================

print("\n" + "=" * 80)
print("PART 3: GAMMA MATRICES FROM THE CUBE")
print("=" * 80)

# Define Pauli matrices
sigma_x = np.array([[0, 1], [1, 0]])
sigma_y = np.array([[0, -1j], [1j, 0]])
sigma_z = np.array([[1, 0], [0, -1]])
I2 = np.eye(2)

# Dirac matrices in chiral representation
gamma_0 = np.block([[np.zeros((2,2)), I2], [I2, np.zeros((2,2))]])
gamma_1 = np.block([[np.zeros((2,2)), sigma_x], [-sigma_x, np.zeros((2,2))]])
gamma_2 = np.block([[np.zeros((2,2)), sigma_y], [-sigma_y, np.zeros((2,2))]])
gamma_3 = np.block([[np.zeros((2,2)), sigma_z], [-sigma_z, np.zeros((2,2))]])

print(f"""
THE STANDARD GAMMA MATRICES:

In the CHIRAL (Weyl) representation:

γ⁰ = [[0, I], [I, 0]]
γⁱ = [[0, σⁱ], [-σⁱ, 0]]

where σⁱ are the Pauli matrices.

THE CUBE INTERPRETATION:

The Pauli matrices correspond to ROTATIONS:
σ_x = rotation around x-axis
σ_y = rotation around y-axis
σ_z = rotation around z-axis

These are the 3 AXES of the cube!
N_space = 3 = number of Pauli matrices ✓

THE GAMMA STRUCTURE:

γ⁰ exchanges left ↔ right (A ↔ B tetrahedra)
γⁱ rotates within a tetrahedron via σⁱ

THE BLOCK STRUCTURE:

The 4×4 gamma matrices have 2×2 blocks.
2 = number of vertices per diagonal endpoint
4 = BEKENSTEIN = number of diagonals

γ^μ maps between the two ends of each diagonal!
""")

# =============================================================================
# PART 4: THE DIRAC EQUATION
# =============================================================================

print("\n" + "=" * 80)
print("PART 4: THE DIRAC EQUATION DERIVATION")
print("=" * 80)

print(f"""
THE DIRAC EQUATION:

(iγ^μ ∂_μ - m)ψ = 0

Or in components:
iγ⁰∂_t ψ + iγⁱ∂_i ψ = mψ

THE CUBE DERIVATION:

STEP 1: Energy-momentum relation
E² = p²c² + m²c⁴

STEP 2: "Square root" of this
E = ±√(p²c² + m²c⁴)

But we need a LINEAR equation!

STEP 3: Dirac's insight
Write E = α·p + βm where α, β are matrices.

Squaring: E² = (α·p)² + {{α·p, βm}} + β²m²

This requires:
αⁱαʲ + αʲαⁱ = 2δⁱʲ (anticommute for i≠j)
αⁱβ + βαⁱ = 0
β² = 1

STEP 4: The solution
α = γ⁰γⁱ, β = γ⁰

THE CUBE VERSION:

The anticommutation relations:
{{γ^μ, γ^ν}} = 2η^μν

These say: "Moving along two different diagonals and back
            equals twice the metric."

THE METRIC η^μν COMES FROM DIAGONAL STRUCTURE!

η = diag(+1,-1,-1,-1) has:
- 1 positive (time diagonal)
- 3 negative (space diagonals)

TIME = 1, N_space = 3 ✓
""")

# =============================================================================
# PART 5: SPIN-1/2 FROM THE CUBE
# =============================================================================

print("\n" + "=" * 80)
print("PART 5: WHY SPIN-1/2?")
print("=" * 80)

print(f"""
THE SPIN-1/2 MYSTERY:

Under rotation by angle θ around axis n:
|ψ⟩ → exp(-iθ n·S/ℏ)|ψ⟩

For spin-1/2: S = ℏσ/2

Under θ = 2π:
|ψ⟩ → exp(-iπ σ·n)|ψ⟩ = -|ψ⟩

A FULL ROTATION GIVES A MINUS SIGN!

THE CUBE EXPLANATION:

The cube has 48 symmetries.
But SPINORS transform under the DOUBLE COVER.

THE DOUBLE COVER:

The rotation group SO(3) has π₁(SO(3)) = Z₂.
This means: there are TWO types of paths.
- Trivial: rotation by 0 or multiple of 4π
- Non-trivial: rotation by 2π (odd multiples)

THE SPINOR GROUP:

Spin(3) = SU(2) is the double cover of SO(3).
Every rotation in SO(3) corresponds to TWO elements in SU(2).

THE CUBE VERSION:

The cube's 24 rotations lift to 48 elements in Spin(3).
48 = 2 × 24 = double cover!

WAIT: The cube has 48 symmetries total (including reflections).
The 24 ROTATIONS lift to 48 spinor transformations.

THE CUBE NATURALLY IMPLEMENTS THE DOUBLE COVER!

WHY SPIN-1/2 EXISTS:

The cube has 8 vertices = 2³.
The exponent 3 = number of spatial dimensions.
2³ = 8 requires the 3rd root of unity structure.

But 360°/3 = 120° doesn't close on vertices.
You need 720° to return to the same vertex state.

SPIN-1/2 BECAUSE THE CUBE IS 3-DIMENSIONAL!
""")

# =============================================================================
# PART 6: CHIRALITY AND THE TWO TETRAHEDRA
# =============================================================================

print("\n" + "=" * 80)
print("PART 6: CHIRALITY FROM TETRAHEDRA")
print("=" * 80)

print(f"""
THE γ⁵ MATRIX:

γ⁵ = iγ⁰γ¹γ²γ³

Properties:
(γ⁵)² = I
{{γ⁵, γ^μ}} = 0

THE CHIRAL PROJECTORS:

P_L = (1 - γ⁵)/2  (left-handed)
P_R = (1 + γ⁵)/2  (right-handed)

THE CUBE VERSION:

γ⁵ EXCHANGES THE TWO TETRAHEDRA!

γ⁵ : Tetrahedron A ↔ Tetrahedron B

Since:
- A = even parity vertices
- B = odd parity vertices

γ⁵ = PARITY OPERATOR on the cube!

THE CHIRALITY EIGENVALUES:

γ⁵ ψ_L = -ψ_L (left-handed in A)
γ⁵ ψ_R = +ψ_R (right-handed in B)

THE WEAK INTERACTION:

The weak force only couples to LEFT-handed particles.
This means: weak bosons only see Tetrahedron A!

W and Z bosons couple to A vertices, not B vertices.
This is PARITY VIOLATION - built into the cube!

CHIRALITY = TETRAHEDRON PARITY.
""")

# =============================================================================
# PART 7: DIRAC SPINOR BILINEARS
# =============================================================================

print("\n" + "=" * 80)
print("PART 7: SPINOR BILINEARS")
print("=" * 80)

print(f"""
THE 16 BILINEARS:

From ψ and ψ̄ = ψ†γ⁰, we can form:

Scalar: ψ̄ψ (1 component)
Vector: ψ̄γ^μψ (4 components)
Tensor: ψ̄σ^μν ψ (6 components)
Axial vector: ψ̄γ^μγ⁵ψ (4 components)
Pseudoscalar: ψ̄γ⁵ψ (1 component)

Total: 1 + 4 + 6 + 4 + 1 = 16

THE CUBE COUNTING:

16 = 2 × CUBE = 2 × 8

The bilinears correspond to:
- 8 vertices (one tetrahedron contributes)
- 8 "dual" vertices (other tetrahedron contributes)

OR:

16 = CUBE + CUBE (particle + antiparticle)

THE PHYSICAL INTERPRETATION:

Scalar ψ̄ψ: vertex overlap (mass term)
Vector ψ̄γ^μψ: current along diagonals
Tensor ψ̄σ^μν ψ: rotation in face planes
Axial ψ̄γ^μγ⁵ψ: chiral current
Pseudoscalar ψ̄γ⁵ψ: tetrahedron exchange

THE 6 TENSOR COMPONENTS = 6 FACES!
THE 4 VECTOR COMPONENTS = 4 DIAGONALS!
THE 4 AXIAL COMPONENTS = 4 DIAGONALS WITH CHIRALITY!
""")

# =============================================================================
# PART 8: THE DIRAC LAGRANGIAN
# =============================================================================

print("\n" + "=" * 80)
print("PART 8: THE DIRAC LAGRANGIAN")
print("=" * 80)

print(f"""
THE DIRAC LAGRANGIAN:

L = ψ̄(iγ^μ∂_μ - m)ψ
  = iψ̄γ^μ∂_μψ - mψ̄ψ

THE KINETIC TERM:

iψ̄γ^μ∂_μψ

This describes PROPAGATION along diagonals.
γ^μ connects the tetrahedra.
∂_μ gives the momentum.

THE MASS TERM:

-mψ̄ψ

This describes MIXING between tetrahedra.
mψ̄ψ = m(ψ̄_L ψ_R + ψ̄_R ψ_L)

Mass requires BOTH tetrahedra!
A particle with mass oscillates between A and B.

THE CUBE PICTURE:

KINETIC: Move along a diagonal (γ^μ∂_μ)
MASS: Jump between tetrahedra (ψ̄ψ)

MASSLESS PARTICLES (m=0):
Stay within one tetrahedron.
Left-handed and right-handed decouple.

MASSIVE PARTICLES (m≠0):
Oscillate between tetrahedra.
Left and right are coupled.

MASS = INTER-TETRAHEDRA COUPLING!
""")

# =============================================================================
# PART 9: THE DIRAC SEA
# =============================================================================

print("\n" + "=" * 80)
print("PART 9: THE DIRAC SEA AND ANTIMATTER")
print("=" * 80)

print(f"""
THE DIRAC SEA:

The Dirac equation has negative energy solutions.
Dirac proposed: all negative energy states are FILLED.

This "sea" is the vacuum.
A "hole" in the sea = antiparticle!

THE CUBE VERSION:

The two tetrahedra:
- Tetrahedron A: particles (positive energy)
- Tetrahedron B: antiparticles (negative energy = holes)

THE 8 VERTICES:

4 in A: electron, muon, tau, neutrino (one generation)
4 in B: positron, antimuon, antitau, antineutrino

Actually, for ONE fermion type:
4 states in A: spin up/down × particle/antiparticle
4 states in B: the "sea" states

THE DIRAC SEA IS TETRAHEDRON B!

PAIR CREATION:

Creating an e⁺e⁻ pair:
- Excite an electron from B to A
- Leave a "hole" in B = positron

This is: B vertex → A vertex
        (filled)   (excited)

PAIR ANNIHILATION:

e⁺ + e⁻ → γγ
A vertex falls back into B hole.
Energy released as photons.

THE VACUUM HAS ALL B STATES FILLED.
""")

# =============================================================================
# PART 10: LORENTZ COVARIANCE
# =============================================================================

print("\n" + "=" * 80)
print("PART 10: LORENTZ TRANSFORMATIONS")
print("=" * 80)

print(f"""
HOW SPINORS TRANSFORM:

Under Lorentz transformation Λ:
ψ → S(Λ)ψ

where S(Λ) is a 4×4 matrix in spinor space.

THE GENERATORS:

S^μν = (i/4)[γ^μ, γ^ν]

These are the 6 generators of the Lorentz group:
- 3 rotations (J_i)
- 3 boosts (K_i)

THE CUBE VERSION:

6 generators = FACES of the cube!

Each face defines a plane of rotation/boost:
Face xy: rotation around z (or boost in z)
Face xz: rotation around y (or boost in y)
Face yz: rotation around x (or boost in x)

THE LORENTZ GROUP:

SO(3,1) has 6 parameters.
Its double cover Spin(3,1) = SL(2,C).

dim(SL(2,C)) = 6 (real parameters)

6 = FACES ✓

THE SPINOR REPRESENTATION:

Spinors form a 4-dimensional representation.
This is the (1/2, 0) ⊕ (0, 1/2) representation.

4 = BEKENSTEIN = number of diagonals ✓

LORENTZ INVARIANCE IS BUILT INTO THE CUBE.
""")

# =============================================================================
# PART 11: THE DIRAC PROPAGATOR
# =============================================================================

print("\n" + "=" * 80)
print("PART 11: THE PROPAGATOR")
print("=" * 80)

print(f"""
THE FEYNMAN PROPAGATOR:

S_F(p) = i(γ^μ p_μ + m) / (p² - m² + iε)

This describes fermion propagation in Feynman diagrams.

THE NUMERATOR:

(γ^μ p_μ + m) = "slash p" + m

The slash notation: /p = γ^μ p_μ

THE CUBE PICTURE:

/p represents: "move along diagonal with momentum p"

THE POLES:

The propagator has poles at:
p² = m²

i.e., E² = p² + m² (on-shell condition)

THE CUBE VERSION:

The on-shell condition is:
"The diagonal length equals the mass shell"

For massless particles: diagonal through center
For massive particles: diagonal offset by m

THE iε PRESCRIPTION:

The +iε tells us how to go around the poles.
This encodes CAUSALITY.

Particles: go around one way (forward in time)
Antiparticles: go around other way (backward in time)

THE CUBE'S TIME DIRECTION (origin → far corner)
DETERMINES THE iε PRESCRIPTION.
""")

# =============================================================================
# PART 12: SUMMARY
# =============================================================================

print("\n" + "=" * 80)
print("PART 12: SUMMARY - SPINORS FROM THE CUBE")
print("=" * 80)

print(f"""
+==============================================================================+
|                                                                              |
|                THE DIRAC EQUATION FROM THE CUBE                              |
|                                                                              |
+==============================================================================+
|                                                                              |
|  SPINOR STRUCTURE:                                                          |
|  - 4 spinor components = BEKENSTEIN = 4 diagonals                           |
|  - Left-handed = Tetrahedron A                                              |
|  - Right-handed = Tetrahedron B                                             |
|                                                                              |
|  GAMMA MATRICES:                                                            |
|  - gamma^0: exchanges tetrahedra (A <-> B)                                     |
|  - gamma^i: rotates within tetrahedron (3 axes)                                |
|  - gamma^5: parity operator (A <-> B with sign)                                |
|                                                                              |
|  CLIFFORD ALGEBRA:                                                          |
|  - dim(Cl(1,3)) = 16 = 2 x CUBE                                             |
|  - Lives on the hypercube structure                                         |
|                                                                              |
|  SPIN-1/2:                                                                  |
|  - Arises from double cover of rotation group                               |
|  - 48 spinor transformations = 2 x 24 cube rotations                        |
|  - 720 degrees needed to return to original state                            |
|                                                                              |
|  CHIRALITY:                                                                 |
|  - Left-handed = even parity vertices (A)                                   |
|  - Right-handed = odd parity vertices (B)                                   |
|  - Weak force sees only A (parity violation!)                               |
|                                                                              |
|  MASS:                                                                      |
|  - Mass term couples A and B tetrahedra                                     |
|  - Massless: stay in one tetrahedron                                        |
|  - Massive: oscillate between tetrahedra                                    |
|                                                                              |
|  ANTIMATTER:                                                                |
|  - Dirac sea = filled B tetrahedron                                         |
|  - Antiparticle = hole in B                                                 |
|  - Pair creation = B -> A excitation                                         |
|                                                                              |
|  LORENTZ GROUP:                                                             |
|  - 6 generators = 6 faces of cube                                           |
|  - Spinor rep = 4 diagonals                                                 |
|                                                                              |
+==============================================================================+

THE DIRAC EQUATION IS GEOMETRY.

FERMIONS ARE EXCITATIONS OF THE CUBE'S DIAGONAL STRUCTURE.

SPIN-1/2 EXISTS BECAUSE THE CUBE IS 3-DIMENSIONAL.

=== END OF DIRAC EQUATION ANALYSIS ===
""")

if __name__ == "__main__":
    pass
