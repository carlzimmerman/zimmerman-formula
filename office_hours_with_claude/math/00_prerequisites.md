# Mathematical Prerequisites

Before diving into the advanced mathematics of the Z² framework, let's make sure the fundamentals are solid.

---

## 1. Numbers and Sets

### Types of Numbers

| Symbol | Name | Examples | What it means |
|--------|------|----------|---------------|
| ℕ | Natural numbers | 1, 2, 3, ... | Counting numbers |
| ℤ | Integers | ..., -2, -1, 0, 1, 2, ... | Whole numbers (positive and negative) |
| ℚ | Rationals | 1/2, 3/4, -7/3 | Fractions (ratios of integers) |
| ℝ | Real numbers | π, √2, -1.5 | All points on a number line |
| ℂ | Complex numbers | 3 + 2i, -i | Numbers with real and imaginary parts |

### Set Notation

```
{x : condition}  means "the set of all x such that condition holds"
```

**Examples:**
- `{x : x > 0}` = all positive numbers
- `{n ∈ ℤ : n² < 10}` = {-3, -2, -1, 0, 1, 2, 3}

### Key Set Operations

| Symbol | Meaning | Example |
|--------|---------|---------|
| ∈ | "is an element of" | 3 ∈ ℤ (3 is an integer) |
| ⊂ | "is a subset of" | ℕ ⊂ ℤ (naturals are inside integers) |
| ∪ | Union (or) | {1,2} ∪ {2,3} = {1,2,3} |
| ∩ | Intersection (and) | {1,2} ∩ {2,3} = {2} |
| × | Cartesian product | ℝ × ℝ = ℝ² (the plane) |

**Why this matters for Z²:** The orbifold T³/Z₂ is defined using quotient notation, and mode counting uses set cardinality.

---

## 2. Functions

### Basic Definition

A function f: A → B assigns to each element of A exactly one element of B.

```
f(x) = x²     means "f takes x and returns x squared"
```

### Important Properties

| Property | Definition | Example |
|----------|------------|---------|
| Injective (1-to-1) | f(a) = f(b) implies a = b | f(x) = 2x |
| Surjective (onto) | Every element in B is hit | f: ℝ → ℝ⁺, f(x) = x² is NOT onto |
| Bijective | Both injective and surjective | f(x) = x + 1 |

### Composition

```
(g ∘ f)(x) = g(f(x))     "first apply f, then apply g"
```

**Why this matters for Z²:** Gauge transformations are functions. Group actions are functions. Everything is functions.

---

## 3. Calculus Review

### Derivatives

The derivative measures the rate of change:

```
f'(x) = df/dx = lim[h→0] (f(x+h) - f(x))/h
```

**Key formulas:**

| Function | Derivative |
|----------|------------|
| xⁿ | n·xⁿ⁻¹ |
| eˣ | eˣ |
| ln(x) | 1/x |
| sin(x) | cos(x) |
| cos(x) | -sin(x) |

**Chain rule:**
```
d/dx[f(g(x))] = f'(g(x)) · g'(x)
```

### Integrals

The integral measures accumulated area:

```
∫ f(x) dx = F(x) + C    where F'(x) = f(x)
```

**Key formulas:**

| Function | Integral |
|----------|----------|
| xⁿ | xⁿ⁺¹/(n+1) |
| eˣ | eˣ |
| 1/x | ln|x| |
| sin(x) | -cos(x) |
| cos(x) | sin(x) |

### Multivariable Calculus

**Partial derivatives:** Differentiate with respect to one variable, treating others as constants.

```
f(x,y) = x²y + y³

∂f/∂x = 2xy       (y is treated as constant)
∂f/∂y = x² + 3y²  (x is treated as constant)
```

**Gradient:**
```
∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
```

**Why this matters for Z²:** The action principle uses integrals. Field equations use partial derivatives. Everything in physics is calculus.

---

## 4. Complex Numbers

### Definition

A complex number has a real part and an imaginary part:

```
z = a + bi    where i² = -1
```

### Visualization

Complex numbers are points in a 2D plane:
- x-axis = real part
- y-axis = imaginary part

### Key Operations

| Operation | Formula | Example |
|-----------|---------|---------|
| Addition | (a+bi) + (c+di) = (a+c) + (b+d)i | (2+3i) + (1-i) = 3+2i |
| Multiplication | (a+bi)(c+di) = (ac-bd) + (ad+bc)i | (2+i)(1+i) = 1+3i |
| Conjugate | z* = a - bi | (3+2i)* = 3-2i |
| Modulus | |z| = √(a² + b²) | |3+4i| = 5 |

### Euler's Formula (Extremely Important!)

```
e^(iθ) = cos(θ) + i·sin(θ)
```

This connects exponentials to rotations!

**Special cases:**
- e^(iπ) = -1 (Euler's identity)
- e^(2πi) = 1 (full rotation)

**Why this matters for Z²:** Quantum mechanics uses complex numbers everywhere. The phase e^(iθ) is fundamental to gauge theory.

---

## 5. Exponentials and Logarithms

### The Exponential Function

```
e ≈ 2.71828...
eˣ = 1 + x + x²/2! + x³/3! + ...
```

**Key property:** The derivative of eˣ is itself: d/dx(eˣ) = eˣ

### Logarithms

The logarithm is the inverse of exponentiation:

```
ln(eˣ) = x
e^(ln(x)) = x
```

**Key properties:**
- ln(ab) = ln(a) + ln(b)
- ln(aⁿ) = n·ln(a)
- ln(1) = 0
- ln(e) = 1

### Orders of Magnitude

When we say something is "order 10⁻¹²⁰", we mean:

```
x ~ 10⁻¹²⁰  means  ln(x) ≈ -120 × ln(10) ≈ -276
```

**Why this matters for Z²:** The hierarchy problem involves e^(-Z²) ≈ 10⁻¹⁵. The CC problem involves e^(-8Z²) ≈ 10⁻¹¹⁶. Exponential suppression is everywhere.

---

## 6. Summation and Product Notation

### Summation (Σ)

```
Σᵢ₌₁ⁿ aᵢ = a₁ + a₂ + ... + aₙ
```

**Examples:**
- Σᵢ₌₁⁵ i = 1+2+3+4+5 = 15
- Σᵢ₌₀^∞ xⁱ/i! = eˣ

### Product (Π)

```
Πᵢ₌₁ⁿ aᵢ = a₁ × a₂ × ... × aₙ
```

**Example:**
- Πᵢ₌₁⁵ i = 1×2×3×4×5 = 120 = 5!

**Why this matters for Z²:** Mode counting sums over states. Partition functions involve products.

---

## 7. Trigonometry

### The Unit Circle

For angle θ:
- cos(θ) = x-coordinate
- sin(θ) = y-coordinate
- tan(θ) = sin(θ)/cos(θ)

### Key Values

| θ | sin(θ) | cos(θ) |
|---|--------|--------|
| 0 | 0 | 1 |
| π/6 (30°) | 1/2 | √3/2 |
| π/4 (45°) | √2/2 | √2/2 |
| π/3 (60°) | √3/2 | 1/2 |
| π/2 (90°) | 1 | 0 |

### Key Identities

```
sin²(θ) + cos²(θ) = 1
sin(2θ) = 2sin(θ)cos(θ)
cos(2θ) = cos²(θ) - sin²(θ)
```

### Inverse Trig Functions

```
arcsin(x) = θ  means  sin(θ) = x
arccos(x) = θ  means  cos(θ) = x
arctan(x) = θ  means  tan(θ) = x
```

**Why this matters for Z²:** The magic angle θ = arctan(1/√2) ≈ 35.26° comes directly from cubic geometry.

---

## 8. Dimensional Analysis

### The Power of Units

Every physical quantity has dimensions. The fundamental dimensions are:
- [L] = Length
- [T] = Time
- [M] = Mass

### Key Principle

**Both sides of any equation must have the same dimensions.**

**Example:** Velocity = Distance / Time
```
[v] = [L]/[T] = m/s
```

### Natural Units (Used in Z² Framework)

In particle physics, we often set:
```
c = 1    (speed of light)
ℏ = 1    (Planck's constant)
```

Then energy, mass, and inverse length all have the same dimensions!

**Why this matters for Z²:** Understanding why Z² is dimensionless (it's a pure number ≈ 33.51) is crucial.

---

## Exercises

1. **Set theory:** Write the set of all integers whose square is less than 50.

2. **Complex numbers:** Compute (1 + i)⁴. (Hint: Use Euler's formula or expand step by step.)

3. **Calculus:** Find the derivative of f(x) = e^(x²).

4. **Exponentials:** If e^(-Z²) ≈ 10⁻¹⁵ and Z² ≈ 33.5, verify this is approximately correct using ln(10) ≈ 2.303.

5. **Trigonometry:** The magic angle satisfies tan(θ) = 1/√2. Find sin(θ) and cos(θ). (Hint: Draw a right triangle with opposite = 1, adjacent = √2.)

---

## Connection to Z² Framework

| Concept | Where it appears in Z² |
|---------|----------------------|
| Sets | Mode counting (16 bosonic, 3 fermionic) |
| Complex numbers | Quantum amplitudes, gauge phases |
| Exponentials | Hierarchy (e^(-Z²)), CC problem (e^(-8Z²)) |
| Trigonometry | Magic angle, Weinberg angle |
| Summation | Kaluza-Klein modes, partition functions |

---

**Next:** `01_linear_algebra.md` - Vectors, matrices, and the language of quantum mechanics.
