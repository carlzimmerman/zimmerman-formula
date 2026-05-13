# Linear Algebra

Linear algebra is the language of quantum mechanics and gauge theory. You cannot understand the Z² framework without it.

---

## 1. Vectors

### What is a Vector?

A vector is an ordered list of numbers:

```
v = (v₁, v₂, v₃)   or   v = [v₁]
                         [v₂]
                         [v₃]
```

**Notation:**
- Bold **v** or arrow v⃗ for vectors
- Components: vᵢ (the i-th entry)
- Dimension: n-dimensional vector has n components

### Vector Operations

**Addition:**
```
(a₁, a₂) + (b₁, b₂) = (a₁+b₁, a₂+b₂)
```

**Scalar multiplication:**
```
c(a₁, a₂) = (ca₁, ca₂)
```

**Dot product (inner product):**
```
a · b = a₁b₁ + a₂b₂ + ... + aₙbₙ
```

The dot product gives a **scalar** (number), not a vector.

**Geometric meaning:** a · b = |a||b|cos(θ), where θ is the angle between them.

### Orthogonality

Two vectors are **orthogonal** (perpendicular) if:
```
a · b = 0
```

**Why this matters for Z²:** The three axes of the cube are orthogonal. The three fermion generations correspond to three orthogonal 1-cycles.

---

## 2. Matrices

### What is a Matrix?

A matrix is a rectangular array of numbers:

```
A = [a₁₁  a₁₂  a₁₃]
    [a₂₁  a₂₂  a₂₃]
```

This is a 2×3 matrix (2 rows, 3 columns).

### Matrix Operations

**Matrix-vector multiplication:**
```
[a  b] [x]   [ax + by]
[c  d] [y] = [cx + dy]
```

The matrix **transforms** the vector.

**Matrix-matrix multiplication:**
```
(AB)ᵢⱼ = Σₖ AᵢₖBₖⱼ
```

Row i of A dots with column j of B.

**Key property:** Matrix multiplication is **not commutative** in general:
```
AB ≠ BA  (usually)
```

**Why this matters for Z²:** Non-commutative multiplication is the essence of non-abelian gauge groups like SU(2) and SU(3).

### Special Matrices

| Name | Definition | Example |
|------|------------|---------|
| Identity I | Iᵢⱼ = δᵢⱼ (1 on diagonal, 0 elsewhere) | [1 0; 0 1] |
| Diagonal | Only diagonal entries nonzero | [3 0; 0 5] |
| Symmetric | Aᵀ = A (Aᵢⱼ = Aⱼᵢ) | [1 2; 2 3] |
| Antisymmetric | Aᵀ = -A | [0 1; -1 0] |
| Orthogonal | AᵀA = I | Rotation matrices |
| Unitary | A†A = I (for complex matrices) | Quantum gates |

### Transpose and Hermitian Conjugate

**Transpose:** Flip rows and columns
```
Aᵀᵢⱼ = Aⱼᵢ
```

**Hermitian conjugate (dagger):** Transpose + complex conjugate
```
A†ᵢⱼ = (Aⱼᵢ)*
```

**Hermitian matrix:** A† = A (important in quantum mechanics!)

---

## 3. Determinants

### Definition (2×2)

```
det[a  b] = ad - bc
   [c  d]
```

### Definition (3×3)

```
det[a  b  c]
   [d  e  f] = a(ei-fh) - b(di-fg) + c(dh-eg)
   [g  h  i]
```

### What Determinants Tell You

- det(A) = 0 means A is **singular** (not invertible)
- |det(A)| = volume scale factor of the transformation
- det(A) < 0 means the transformation flips orientation

**Why this matters for Z²:** The Z₂ action flips orientation (det = -1). The orbifold quotient identifies points related by this flip.

---

## 4. Eigenvalues and Eigenvectors

### The Key Equation

An **eigenvector** v of matrix A satisfies:
```
Av = λv
```

The scalar λ is the **eigenvalue**.

**Meaning:** A stretches v by factor λ, without changing its direction.

### Finding Eigenvalues

Solve the **characteristic equation:**
```
det(A - λI) = 0
```

### Example

```
A = [3  1]
    [0  2]

det(A - λI) = det[3-λ   1 ] = (3-λ)(2-λ) = 0
                 [0   2-λ]

Eigenvalues: λ₁ = 3, λ₂ = 2
```

### Diagonalization

If A has n linearly independent eigenvectors, then:
```
A = PDP⁻¹
```

where D is diagonal (eigenvalues on diagonal) and P has eigenvectors as columns.

**Why this matters for Z²:** Quantum observables are Hermitian matrices. Their eigenvalues are the possible measurement outcomes. The Standard Model gauge groups are characterized by their eigenvalue structure.

---

## 5. Vector Spaces

### Definition

A **vector space** V over a field F (usually ℝ or ℂ) is a set with:
- Vector addition: v + w ∈ V
- Scalar multiplication: cv ∈ V for c ∈ F
- Satisfying certain axioms (associativity, commutativity, etc.)

### Basis and Dimension

A **basis** is a set of vectors that:
1. Spans the space (any vector can be written as a linear combination)
2. Is linearly independent (no redundancy)

The **dimension** is the number of basis vectors.

**Example:** ℝ³ has dimension 3. A basis is {(1,0,0), (0,1,0), (0,0,1)}.

### Subspaces

A **subspace** is a subset that is itself a vector space.

**Example:** A plane through the origin in ℝ³ is a 2-dimensional subspace.

**Why this matters for Z²:** The 16 bosonic modes and 3 fermionic modes span different subspaces. The net effective capacity (13) is a dimension count.

---

## 6. Inner Product Spaces

### Inner Product

An **inner product** ⟨u, v⟩ generalizes the dot product:
- ⟨u, v⟩ = ⟨v, u⟩* (conjugate symmetry)
- ⟨u, av + bw⟩ = a⟨u, v⟩ + b⟨u, w⟩ (linearity)
- ⟨v, v⟩ ≥ 0, with equality iff v = 0

### Hilbert Space

A **Hilbert space** is a complete inner product space.

**This is the setting for quantum mechanics!**

In quantum mechanics:
- States are vectors |ψ⟩ in Hilbert space
- Inner product ⟨φ|ψ⟩ gives probability amplitudes
- Observables are Hermitian operators

**Dirac notation:**
```
|ψ⟩ = "ket" = column vector
⟨ψ| = "bra" = row vector (Hermitian conjugate)
⟨φ|ψ⟩ = inner product
|ψ⟩⟨φ| = outer product (a matrix)
```

---

## 7. Tensors (Preview)

### What is a Tensor?

A tensor is a multi-indexed array that transforms in a specific way under coordinate changes.

- **Scalar (rank 0):** Just a number. T
- **Vector (rank 1):** One index. Tᵢ
- **Matrix (rank 2):** Two indices. Tᵢⱼ
- **Higher rank:** More indices. Tᵢⱼₖ...

### Tensor Notation

**Einstein summation convention:** Repeated indices are summed over.
```
AᵢⱼBⱼₖ means Σⱼ AᵢⱼBⱼₖ
```

This makes equations much cleaner!

### Index Position

In general relativity and differential geometry:
- Upper indices (Tⁱ) = contravariant
- Lower indices (Tᵢ) = covariant

The metric gᵢⱼ raises and lowers indices:
```
Tⁱ = gⁱʲTⱼ
```

**Why this matters for Z²:** The metric tensor gᵢⱼ defines geometry. The field strength tensor Fᵢⱼ describes electromagnetic fields. Tensors are everywhere in physics.

---

## 8. Trace and Rank

### Trace

The **trace** is the sum of diagonal elements:
```
Tr(A) = Σᵢ Aᵢᵢ = a₁₁ + a₂₂ + ... + aₙₙ
```

**Key properties:**
- Tr(A + B) = Tr(A) + Tr(B)
- Tr(AB) = Tr(BA) (cyclic property)
- Tr(A) = sum of eigenvalues

### Rank

The **rank** of a matrix is the dimension of its image (column space).

**Equivalently:** The number of linearly independent rows (or columns).

**Why this matters for Z²:** The rank of the Standard Model gauge group SU(3)×SU(2)×U(1) is 4 (= 2+1+1). This appears directly in α⁻¹ = 4Z² + 3.

---

## Exercises

1. **Matrix multiplication:** Compute AB where A = [1 2; 3 4] and B = [0 1; 1 0]. Then compute BA. Are they equal?

2. **Eigenvalues:** Find the eigenvalues of A = [2 1; 1 2].

3. **Determinant:** What is det(A) for the matrix in exercise 2? Is A invertible?

4. **Trace:** What is Tr(A)? Verify it equals the sum of eigenvalues.

5. **Orthogonality:** Show that (1, 1, 1) and (1, -1, 0) are orthogonal in ℝ³.

6. **Dimension:** The set of 2×2 symmetric matrices forms a vector space. What is its dimension?

---

## Connection to Z² Framework

| Linear Algebra Concept | Z² Application |
|----------------------|----------------|
| Dimension | Mode counting (16B + 3F = 19) |
| Eigenvalues | Quantum numbers, particle masses |
| Rank | rank(G_SM) = 4 appears in α⁻¹ formula |
| Trace | Anomaly calculations |
| Hermitian matrices | Observable operators |
| Unitary matrices | Gauge transformations |
| Non-commutativity | Non-abelian gauge groups (SU(2), SU(3)) |

---

**Next:** `02_group_theory.md` - The mathematics of symmetry.
