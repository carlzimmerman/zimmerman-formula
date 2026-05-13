# Intersection Theory

Intersection theory counts how geometric objects cross each other. In string theory, this determines the number of particle generations and gauge couplings. This is the mathematical foundation of Piece 14.

---

## 1. The Basic Idea: Counting Crossings

### Real-World Example: Road Intersections

Two roads in a city can:
- **Cross once** (a standard intersection)
- **Not cross** (parallel roads, or one is a bridge)
- **Cross multiple times** (winding mountain roads)

The **intersection number** counts these crossings with signs:

```
    Road A
      │
      │ (+1)
──────┼────── Road B
      │
      │
```

If they cross "the wrong way" (opposite orientations), it counts as -1.

### Why Signs Matter

A figure-8 curve crosses itself:
```
    ╱╲
   ╱  ╲
  │ +1 │
   ╲  ╱
    ╲╱
    ╱╲
   ╱  ╲
  │ -1 │
   ╲  ╱
    ╲╱
```

Total intersection number = +1 + (-1) = 0!

The signs cancel because the crossings have opposite orientations.

---

## 2. Intersection Numbers in Topology

### Curves on Surfaces

On a torus (donut), consider two curves:
- α: goes around the "hole"
- β: goes around the "tube"

```
      α
    ╭───╮
   ╱     ╲
  │   β   │
  │ ──────│─→
  │       │
   ╲     ╱
    ╰───╯
```

These curves intersect **exactly once**.

**Intersection number:** I(α, β) = 1

### The Intersection Pairing

For a surface, we get a pairing:
```
I: H₁(M) × H₁(M) → ℤ
```

This takes two homology classes and returns an integer.

### Properties

1. **Antisymmetric:** I(α, β) = -I(β, α)
2. **Bilinear:** I(α + α', β) = I(α, β) + I(α', β)
3. **Topological:** Only depends on homology class, not specific curve

---

## 3. Higher Dimensions: Cycles and Cocycles

### General Setup

In an n-dimensional manifold M:
- A **k-cycle** is a k-dimensional submanifold (possibly with coefficients)
- Two cycles of complementary dimension can intersect

### Dimension Counting

For cycles A (dimension k) and B (dimension l) to generically intersect in points:
```
k + l = n (dimension of M)
```

**Example:** In a 6-dimensional space:
- 3-cycle meets 3-cycle → points
- 2-cycle meets 4-cycle → points

### The Intersection Number

```
I(A, B) = # of intersection points (counted with signs)
```

This is a topological invariant - it doesn't change under continuous deformation!

---

## 4. D-Branes and Intersections

### What are D-Branes?

In string theory, **D-branes** are surfaces where open strings can end.

```
String theory picture:

    D-brane A                 D-brane B
    ─────────                 ─────────
        │                         │
        │    ~~~~~~~~             │
        │   (open string)         │
        │    ~~~~~~~~             │
        └─────────────────────────┘
              intersection
```

### Chiral Fermions at Intersections

When two D-branes intersect, **chiral fermions** appear at the intersection!

**This is the string theory origin of quarks and leptons.**

### The Intersection Number = Generations

```
I_ab = |Π_a · Π_b| = number of chiral fermions
```

where:
- Π_a = homology cycle wrapped by brane A
- Π_b = homology cycle wrapped by brane B

**For T³/Z₂:**
```
I_ab = b₁(T³) = 3 = number of generations!
```

---

## 5. The T³/Z₂ Intersection Calculation

### The Setup

Consider D6-branes wrapping 3-cycles in T³/Z₂:
- Brane stack A: supports SU(2)_L (weak force)
- Brane stack B: supports U(1)_Y (hypercharge)

### The 3-Cycles

T³ has three independent 3-cycles (dual to the three 1-cycles).

The branes wrap combinations of these cycles.

### Computing the Intersection

```
I_ab = |Π_a · Π_b| = |det(wrapping matrix)|
```

For the Standard Model embedding:
```
I_ab = b₁(T³) = 3
```

This is **topologically fixed** - it can't be anything else!

---

## 6. Why 3 Generations is Topological

### The Deep Reason

The number of generations equals b₁(T³) because:

1. D-branes wrap cycles in homology
2. Fermions appear at intersections
3. The intersection number = first Betti number
4. b₁(T³) = 3 (three independent loops)

### Visualization

```
        T³ = S¹ × S¹ × S¹

        Three independent circles:

        ○ → γ₁ (first generation)
        ○ → γ₂ (second generation)
        ○ → γ₃ (third generation)

        Each cycle hosts one generation of fermions!
```

### No Tuning Required

Unlike most models where the number of generations is put in by hand, here it's **derived from topology**:

```
N_gen = b₁(T³) = dim(H₁(T³)) = 3
```

---

## 7. The Weak Mixing Angle from Intersections

### The Key Formula (Piece 14)

```
sin²θ_W = I_ab / N_EW = 3 / 13
```

where:
- I_ab = 3 (intersection number = generations)
- N_EW = 16 - 3 = 13 (electroweak capacity)

### Where Does 16 Come From?

The twisted sector of T³/Z₂:
- 8 fixed points
- 2 complex moduli per fixed point
- Total: 8 × 2 = 16 bosonic modes

### The Capacity

```
N_EW = N_bosonic - N_fermionic = 16 - 3 = 13
```

This is the "room" available for electroweak gauge fields after accounting for fermionic matter.

### The Ratio

```
sin²θ_W = (fermionic intersection) / (electroweak capacity)
        = I_ab / N_EW
        = 3 / 13
        = 0.2308
```

**Experimental value:** 0.2312 (0.17% error!)

---

## 8. Intersection Products and Cup Products

### The Algebraic Structure

Intersection pairing is related to the **cup product** in cohomology:
```
∪: Hᵖ(M) × Hᵍ(M) → Hᵖ⁺ᵍ(M)
```

### Poincaré Duality

For a closed n-manifold:
```
Hₖ(M) ≅ Hⁿ⁻ᵏ(M)
```

This relates:
- Cycles (homology)
- Forms (cohomology)
- Intersections

### Why This Matters

The intersection pairing is computable from cohomology, which is computable from the topology of the space.

**No differential equations needed!**

---

## 9. Real-World Analogy: Social Networks

### Counting Connections

Think of intersection numbers like social connections:

- **People** = cycles
- **Mutual friends** = intersections
- **Intersection number** = # of mutual friends

Just as the topology of a social network determines possible connections, the topology of internal space determines particle physics.

### The Standard Model Network

```
   SU(2)_L brane ←── 3 fermion generations ──→ U(1)_Y brane
        │                                           │
        │              I_ab = 3                     │
        └───────────────────────────────────────────┘
```

The three "mutual friends" are the three generations!

---

## 10. Summary: Intersection Theory and Physics

### The Dictionary

| Math | Physics |
|------|---------|
| D-brane | Gauge group carrier |
| 3-cycle | Internal manifold the brane wraps |
| Intersection | Location of chiral fermions |
| I_ab | Number of fermion generations |
| b₁(T³) | = 3 = N_gen |

### The Power of Topology

The Standard Model's "arbitrary" features become **derived**:

| Feature | Standard Model | Z² Framework |
|---------|---------------|--------------|
| Generations | Put in by hand (3) | = b₁(T³) = 3 |
| sin²θ_W | Measured (0.231) | = 3/13 = 0.2308 |
| Chirality | Assumed | Z₂ projection (Ψ_R = 0) |

---

## Exercises

1. **Torus:** On T², the cycles α (around hole) and β (around tube) satisfy I(α, β) = 1. Verify I(2α, β) = 2.

2. **Self-intersection:** Show that I(α, α) = 0 for any cycle on an orientable surface.

3. **T³:** How many independent 3-cycles does T³ have? (Hint: Poincaré duality with 0-cycles)

4. **Generations:** If we compactified on T⁴ instead of T³, how many generations would we get?

5. **Capacity:** If there were 20 twisted bosonic modes instead of 16, what would sin²θ_W be?

---

## Connection to Z² Framework

| Intersection Concept | Z² Application |
|---------------------|----------------|
| I_ab = 3 | Three generations (Piece 14) |
| b₁(T³) = 3 | Same number from topology |
| D-brane gauge couplings | sin²θ_W = I_ab/N_EW |
| Homology | H₁(T³) = ℤ³ |
| 16 twisted modes | From 8 fixed points |
| 13 = 16 - 3 | Electroweak capacity |

---

**You've completed the math foundations!**

Now proceed to `physics/` to see how these tools are applied.
