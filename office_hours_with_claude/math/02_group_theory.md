# Group Theory

Group theory is the mathematics of symmetry. The Standard Model is built on symmetry groups, so understanding groups is essential for the Z² framework.

---

## 1. What is a Group?

### Real-World Intuition: The Rubik's Cube

Before the formal definition, think about a **Rubik's Cube**:

- Each move (rotate a face) is a **group element**
- Doing two moves in sequence is the **group operation**
- There's a "do nothing" move (the **identity**)
- Every move can be undone (the **inverse**)
- The order of moves matters! (This makes it **non-abelian**)

The Rubik's Cube group has 43 quintillion elements - but it's still a group because it follows the same rules as simple groups.

### Another Example: Clock Arithmetic

A 12-hour clock is a group:
- Elements: {12, 1, 2, 3, ..., 11} (the hours)
- Operation: addition mod 12
- Identity: 12 (adding 12 hours = same time)
- Inverse of 3: 9 (because 3 + 9 = 12)

**3 hours after 10 o'clock = 1 o'clock** (10 + 3 = 13 = 1 mod 12)

This is the group Z₁₂!

### Definition

A **group** (G, ·) is a set G with an operation · satisfying:

1. **Closure:** If a, b ∈ G, then a · b ∈ G
2. **Associativity:** (a · b) · c = a · (b · c)
3. **Identity:** There exists e ∈ G such that e · a = a · e = a for all a
4. **Inverse:** For each a ∈ G, there exists a⁻¹ such that a · a⁻¹ = a⁻¹ · a = e

### Simple Examples

**Integers under addition (ℤ, +):**
- Closure: sum of integers is an integer ✓
- Associativity: (a+b)+c = a+(b+c) ✓
- Identity: 0 (since a + 0 = a) ✓
- Inverse: -a (since a + (-a) = 0) ✓

**Positive reals under multiplication (ℝ⁺, ×):**
- Identity: 1
- Inverse of a: 1/a

**NOT a group:** Integers under multiplication (no inverse for 2, since 1/2 ∉ ℤ)

---

## 2. Abelian vs Non-Abelian

### Abelian Groups

A group is **abelian** (or commutative) if:
```
a · b = b · a   for all a, b
```

**Example:** (ℤ, +) is abelian since a + b = b + a.

### Non-Abelian Groups

A group is **non-abelian** if the operation doesn't always commute.

**Example:** Matrix multiplication. In general, AB ≠ BA.

**Why this matters for Z²:**
- U(1) (electromagnetism) is abelian
- SU(2) and SU(3) are **non-abelian** - this is why they're called "non-abelian gauge theories"

---

## 3. Important Finite Groups

### Cyclic Groups Zₙ

The group ℤₙ = {0, 1, 2, ..., n-1} under addition mod n.

**Example:** Z₄ = {0, 1, 2, 3}
- 2 + 3 = 5 mod 4 = 1
- Identity: 0
- Inverse of 1: 3 (since 1 + 3 = 4 mod 4 = 0)

### The Z₂ Group (Extremely Important!)

Z₂ = {0, 1} under addition mod 2, or equivalently {1, -1} under multiplication.

| · | 1 | -1 |
|---|---|---|
| 1 | 1 | -1 |
| -1 | -1 | 1 |

**Key insight:** Z₂ is the simplest non-trivial group. It represents a **reflection** or **parity flip**.

### Real-World Z₂ Examples

**1. Light switch:** ON/OFF. Flipping twice returns to original. {ON, OFF} with "flip" operation.

**2. Mirror reflection:** Looking in a mirror is a Z₂ operation. Two reflections = back to original.

**3. Your hands:** Left hand ↔ Right hand. You can't continuously rotate a left hand into a right hand - you need a FLIP. This is why chirality (handedness) is connected to Z₂!

**4. A coin:** Heads/Tails. Flipping the coin is the Z₂ operation.

**5. Even/Odd numbers:** Even + Even = Even, Odd + Odd = Even, Even + Odd = Odd. This IS Z₂!

```
Even ↔ 0 (identity)
Odd  ↔ 1

Odd + Odd = 1 + 1 = 0 (mod 2) = Even ✓
```

**Why Z₂ matters for physics:** The orbifold T³/Z₂ uses this flip symmetry. Points y and -y are identified. This creates the 8 fixed points AND gives us chiral fermions (like your left and right hands being different).

**Why this matters for Z²:** The orbifold T³/Z₂ uses Z₂ to identify points y ↔ -y. This Z₂ action is why we get 8 fixed points and chiral fermions!

### Permutation Groups Sₙ

The symmetric group Sₙ consists of all permutations of n objects.

- S₂ has 2! = 2 elements
- S₃ has 3! = 6 elements
- Sₙ has n! elements

S₃ is the smallest non-abelian group.

---

## 4. Continuous Groups (Lie Groups)

### Definition

A **Lie group** is a group that is also a smooth manifold (you can do calculus on it).

**Examples:**
- Rotations in 3D
- Lorentz transformations
- Gauge transformations

### Key Lie Groups for Physics

| Group | Description | Dimension | Appears in |
|-------|-------------|-----------|-----------|
| U(1) | Complex phases eⁱθ | 1 | Electromagnetism |
| SU(2) | 2×2 unitary, det=1 | 3 | Weak force |
| SU(3) | 3×3 unitary, det=1 | 8 | Strong force |
| SO(3) | 3D rotations | 3 | Angular momentum |
| SO(3,1) | Lorentz group | 6 | Special relativity |

---

## 5. The Unitary Groups U(n) and SU(n)

### U(n): Unitary Group

**Definition:** n×n complex matrices U satisfying U†U = I

**Properties:**
- |det(U)| = 1 (determinant has magnitude 1)
- Preserves inner products: ⟨Uv, Uw⟩ = ⟨v, w⟩
- Dimension: n² (as a real manifold)

### U(1): The Circle Group

U(1) = {eⁱθ : θ ∈ [0, 2π)}

This is just the unit circle in the complex plane!

**Multiplication:** eⁱθ₁ · eⁱθ₂ = eⁱ⁽θ₁⁺θ₂⁾

**Why this matters for Z²:** U(1) is the gauge group of electromagnetism. Electric charge is a U(1) quantum number.

### SU(n): Special Unitary Group

**Definition:** U(n) matrices with det(U) = 1

**Dimension:** n² - 1

### SU(2): The Weak Force Group

Dimension: 2² - 1 = 3

A general SU(2) element can be written:
```
U = exp(iθₐσₐ/2)
```
where σₐ are the **Pauli matrices**:

```
σ₁ = [0  1]    σ₂ = [0  -i]    σ₃ = [1   0]
     [1  0]         [i   0]         [0  -1]
```

**Key fact:** SU(2) is the double cover of SO(3) (3D rotations).

### SU(3): The Strong Force Group

Dimension: 3² - 1 = 8

Generators are the **Gell-Mann matrices** λₐ (8 of them).

**Why 8 gluons?** Because dim(SU(3)) = 8!

**Why this matters for Z²:** The 8 gluons ↔ 8 fixed points of T³/Z₂ is not a coincidence. This is Piece 7 of the framework.

---

## 6. Lie Algebras

### Definition

The **Lie algebra** 𝔤 of a Lie group G is the tangent space at the identity, equipped with a bracket operation [·,·].

**Intuition:** The Lie algebra captures the "infinitesimal" structure of the group.

### The Lie Bracket

For matrix groups, the bracket is the commutator:
```
[A, B] = AB - BA
```

**Properties:**
- Antisymmetry: [A, B] = -[B, A]
- Jacobi identity: [A, [B, C]] + [B, [C, A]] + [C, [A, B]] = 0

### Structure Constants

For basis generators Tₐ:
```
[Tₐ, Tᵦ] = ifₐᵦᶜTᶜ
```

The fₐᵦᶜ are called **structure constants**.

- For abelian groups: fₐᵦᶜ = 0 (all generators commute)
- For non-abelian groups: fₐᵦᶜ ≠ 0

**Why this matters for Z²:** The structure constants determine the self-interactions of gauge bosons. Gluons interact with each other (non-abelian). Photons don't (abelian).

---

## 7. Representations

### Definition

A **representation** of a group G on a vector space V is a homomorphism:
```
ρ: G → GL(V)
```

This assigns a matrix ρ(g) to each group element g, preserving the group structure:
```
ρ(g₁g₂) = ρ(g₁)ρ(g₂)
```

### Dimension of a Representation

The **dimension** of a representation is dim(V), the size of the matrices.

### Important Representations

**Trivial representation:** ρ(g) = 1 for all g (dimension 1)

**Fundamental representation:** The "smallest" non-trivial representation
- SU(2) fundamental: dimension 2 (the doublet)
- SU(3) fundamental: dimension 3 (the triplet)

**Adjoint representation:** Dimension equals dim(G)
- SU(2) adjoint: dimension 3
- SU(3) adjoint: dimension 8

**Why this matters for Z²:** Particles are classified by their representations:
- Quarks are in the fundamental (3) of SU(3)
- Gluons are in the adjoint (8) of SU(3)
- Left-handed fermions are doublets (2) of SU(2)

---

## 8. The Standard Model Gauge Group

### The Group

```
G_SM = SU(3)_C × SU(2)_L × U(1)_Y
```

- SU(3)_C: Color (strong force), 8 generators = 8 gluons
- SU(2)_L: Weak isospin, 3 generators = W⁺, W⁻, W⁰
- U(1)_Y: Hypercharge, 1 generator = B⁰

After electroweak symmetry breaking: W⁰ and B⁰ mix to give Z⁰ and photon γ.

### Rank of a Group

The **rank** is the dimension of the maximal abelian subgroup (Cartan subalgebra).

| Group | Rank |
|-------|------|
| U(1) | 1 |
| SU(2) | 1 |
| SU(3) | 2 |
| G_SM = SU(3)×SU(2)×U(1) | 2 + 1 + 1 = **4** |

**Why this matters for Z²:** The rank 4 appears directly in the formula α⁻¹ = **4**Z² + 3!

### Dimension of G_SM

```
dim(SU(3)) + dim(SU(2)) + dim(U(1)) = 8 + 3 + 1 = 12
```

This is why there are 12 gauge bosons: 8 gluons + W⁺ + W⁻ + Z⁰ + γ.

**Why this matters for Z²:** The 12 gauge bosons appear in the Higgs derivation: 16 - 12 = 4 Higgs components.

---

## 9. Z₂ Actions and Orbifolds (Preview)

### Group Actions

A group G **acts** on a space X if there's a map G × X → X satisfying:
- e · x = x (identity acts trivially)
- (gh) · x = g · (h · x) (composition)

### The Z₂ Action on T³

On the 3-torus T³ with coordinates (y₁, y₂, y₃), define:
```
Z₂: (y₁, y₂, y₃) ↦ (-y₁, -y₂, -y₃)
```

This is a **reflection through the origin**.

### Fixed Points

A **fixed point** is a point x where g · x = x.

For the Z₂ action on T³, the fixed points satisfy:
```
(y₁, y₂, y₃) = (-y₁, -y₂, -y₃)  mod 2π
```

This requires each yᵢ ∈ {0, π}, giving 2³ = **8 fixed points**.

**Why this matters for Z²:** These 8 fixed points are the vertices of a cube. They correspond to the 8 gluons. This is the geometric origin of SU(3)!

---

## Exercises

1. **Group axioms:** Show that the set {1, -1, i, -i} under multiplication forms a group. What is it isomorphic to?

2. **Lie algebra:** Verify that [σ₁, σ₂] = 2iσ₃ for the Pauli matrices.

3. **Dimension counting:** What is dim(SU(5))? (This is the GUT group.)

4. **Rank:** The group E₈ has dimension 248 and rank 8. How many generators does it have?

5. **Fixed points:** If Z₃ acts on T² by rotation by 120°, how many fixed points are there?

---

## Connection to Z² Framework

| Group Theory Concept | Z² Application |
|---------------------|----------------|
| Z₂ | The orbifold action creating 8 fixed points |
| SU(2) | Weak force, 3 generators |
| SU(3) | Strong force, 8 generators = 8 fixed points |
| U(1) | Electromagnetism |
| rank(G_SM) = 4 | Appears in α⁻¹ = 4Z² + 3 |
| dim(G_SM) = 12 | 12 gauge bosons |
| Representations | Classify particle content |

---

**Next:** `03_topology_basics.md` - Manifolds and the global structure of space.
