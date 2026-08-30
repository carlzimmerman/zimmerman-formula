# Phase V — Constraint Analysis / Physical Degrees of Freedom

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

We count the physical degrees of freedom (DOF) of the frozen candidate,
field by field, using the localized auxiliary representation (Phase IV) and
the constraint structure.

---

## 1. Field inventory

| Field | Role | EOM order | Propagating DOF |
|-------|------|-----------|-----------------|
| `g_{μν}` | metric | 2nd (Einstein) | 2 (tensor) after gauge |
| `T` (clock) | `U_μ = -∇_μ T`, `∇T·∇T = -1` | constraint (mimetic) | 1 (if dynamical) / 0 (if `T[g]`) |
| `Φ` | curvature response `Box Φ = R_{uu}` | 2nd | (see bi-scalar) |
| `ξ` | multiplier for `Box Φ = R_{uu}` | 2nd (conjugate to Φ) | (see bi-scalar) |
| `M` | transport scalar | 0th (algebraic) | 0 |
| `η` | multiplier for transport eq | 1st (transport) | 0 (at 2nd order) |

---

## 2. The metric sector

**DERIVED:** The metric `g_{μν}` has 10 components. Diffeomorphism invariance
(4 gauge parameters) and the 4 constraint equations (the `0μ` components of the
field equation, the Hamiltonian and momentum constraints) remove 8, leaving
**2 propagating tensor DOF** (the two graviton polarizations), exactly as in GR.
The nonlocal term `M[g]` modifies the field equation but does not change the
count of tensor DOF at leading order (it adds a nonlocal stress tensor, not new
tensor fields).

---

## 3. The (Φ, ξ) bi-scalar sector  (1 healthy + 1 ghost)

**DERIVED:** The term `∫ ξ Box Φ` is a second-order bi-scalar. Diagonalizing
with `a = Φ + ξ` (healthy) and `b = Φ - ξ` (ghost) gives
```
S_2^(Φξ) = (1/4) ∫ a Box a  −  (1/4) ∫ b Box b .
```
This is **two** scalar DOF: `a` (healthy, correct kinetic sign) and `b`
(ghost, wrong kinetic sign). So the (Φ, ξ) sector contributes **2 scalar DOF**,
one of which is a **ghost**.

---

## 4. The (M, η) transport sector  (0 propagating DOF)

**DERIVED:** The M-EOM is algebraic (0th order): `-κ - ∇_μ U^μ + ... = 0`, so
M is a Lagrange multiplier with **no kinetic term** and **no propagating DOF**.
The η-EOM is first-order (transport): `∂_t η = -κ` (on the stationary branch),
so η is a transported (non-propagating) variable with **no propagating DOF** at
quadratic order. Higher-order couplings make M and η weakly dynamical, but they
carry no independent propagating DOF at leading order.

**Contribution: 0 propagating DOF.**

---

## 5. The clock T  (1 DOF if dynamical, 0 if `T[g]`)

**UNKNOWN (gap from Phase II):** The frozen chain writes `T[g]`, but the only
T-equation is the mimetic constraint `∇_μ T ∇^μ T = -1`, which does not
determine T from g. Two cases:

- **If T is dynamical** (the action includes a T kinetic/constraint term): T is
  a mimetic scalar with **1 propagating DOF** (the constraint removes 1 of the
  2 scalar DOF, leaving 1).
- **If T is a specified functional `T[g]`**: T contributes **0 propagating DOF**
  (it is determined by the metric).

The frozen candidate does not specify which case holds. **Status: UNKNOWN.**

---

## 6. Total DOF count

| Case | Tensor | T | (Φ,ξ) bi-scalar | (M,η) | Total | Ghosts |
|------|--------|---|-----------------|-------|-------|--------|
| T dynamical | 2 | 1 | 2 (1 healthy + 1 ghost) | 0 | **5** | **1** |
| T = T[g] | 2 | 0 | 2 (1 healthy + 1 ghost) | 0 | **4** | **1** |

**DERIVED:** In either case, the candidate has **at least one physical ghost
scalar** (`b = Φ - ξ`) and **one healthy extra scalar** (`a = Φ + ξ`), in
addition to the 2 tensor DOF. The ghost is the central problem (Phase VI).

---

## 7. Summary

| # | Result | Status |
|---|--------|--------|
| 1 | Metric sector: 2 tensor DOF (as in GR). | DERIVED |
| 2 | (Φ, ξ) bi-scalar: 2 scalar DOF = 1 healthy (`a=Φ+ξ`) + 1 ghost (`b=Φ-ξ`). | DERIVED |
| 3 | (M, η) transport sector: 0 propagating DOF (M algebraic, η first-order). | DERIVED |
| 4 | Clock T: 1 DOF if dynamical, 0 if `T[g]`. | UNKNOWN (gap) |
| 5 | Total: 4 or 5 DOF, of which **1 is a physical ghost** (`b = Φ - ξ`). | DERIVED |

**Phase V verdict:** The candidate has **one ghost scalar** (`b = Φ - ξ`) in
addition to the 2 tensor DOF and one healthy extra scalar. Whether this ghost
is **physical** (couples to and back-reacts on the metric) or **decoupled**
(a Veneziano-type artifact removed by boundary conditions) is the question for
Phase VI.
