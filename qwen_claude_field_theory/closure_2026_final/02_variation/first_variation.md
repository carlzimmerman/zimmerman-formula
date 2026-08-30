# Phase II — The First Variation δM[g]  (decisive)

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

This phase answers the single most important question of the closure:
**given a metric variation δg, what is δM, and is the resulting tensor
`E_{μν} = δM/δg^{μν}` a well-defined, conserved, non-ghost tensor?**

We work from the frozen chain (BASELINE.md):

```
g_{μν} -> T[g] -> U_μ[g] -> Φ[g] -> Z[g] -> M[g]
U_μ = -∇_μ T ,  ∇_μ T ∇^μ T = -1                    (unit timelike)
Box_ret Φ = R_{μν} U^μ U^ν                           (retarded)
Z = (4 c^4/a_0^2) ∇_μ Φ ∇^μ Φ
∇_μ [ U^μ (M + F_ε(Z)) ] = 0                         (transport def of M)
```

---

## 1. The transport definition of M, and why M is nonlocal

The transport equation
```
∇_μ [ U^μ (M + F(Z)) ] = 0        ⇔        ∂_μ [ √(-g) U^μ (M + F(Z)) ] = 0
```
says that the **density** `√(-g) U^μ (M+F)` is conserved along the flow of `U`.
Equivalently, along each integral curve (flow line) of the unit vector `U^μ`,
the quantity `M + F(Z)` is **constant** (in the special case `∇_μ U^μ = 0`; in
general it is transported with the flow's expansion).

**DERIVED:** M is determined by this first-order PDE only up to an integration
constant on each flow line — i.e. up to data specified on a Cauchy surface Σ.
Thus M is a **nonlocal functional** of the data: it is the solution of a
transport equation, not a local expression in `g` and its derivatives. This is
the structural origin of the nonlocality of the theory.

On the intended isolated stationary branch, `M ≈ -F(Z)` (a target, not an
axiom). We keep the general transport solution; the branch is a special
choice of integration constant.

---

## 2. The varied transport equation

Let `J^μ = U^μ (M + F(Z))`. On-shell, `∇_μ J^μ = 0`, i.e.
`∂_μ [√(-g) J^μ] = 0`.

Under `g → g + δg`, the fields vary: `U → U + δU`, `Φ → Φ + δΦ`,
`Z → Z + δZ`, `M → M + δM`. The **perturbed** conservation law is
```
0 = δ ∂_μ [ √(-g) J^μ ] = ∂_μ [ δ(√(-g) J^μ) ] .
```
Using `δ√(-g) = -½ √(-g) g_{μν} δg^{μν} = ½ √(-g) g^{μν} δg_{μν}`,
```
δ(√(-g) J^μ) = √(-g) [ δJ^μ + ½ J^μ g^{αβ} δg_{αβ} ] ,
```
with
```
δJ^μ = δU^μ (M + F) + U^μ ( δM + F'(Z) δZ ) .
```
Therefore the **varied transport equation** is
```
∇_μ [ δJ^μ + ½ J^μ g^{αβ} δg_{αβ} ] = 0 ,
```
or, using `∇_μ J^μ = 0` on-shell,
```
∇_μ δJ^μ + ½ J^μ g^{αβ} ∇_μ δg_{αβ} = 0 .              (∗)
```

---

## 3. The transport PDE for δM  (the decisive result)

Substituting `δJ^μ` into `(∗)`:
```
∇_μ [ U^μ δM ] + ∇_μ [ δU^μ (M+F) + U^μ F'(Z) δZ ]
      + ½ J^μ g^{αβ} ∇_μ δg_{αβ} = 0 .
```
The first term expands as
```
∇_μ [ U^μ δM ] = (∇_μ U^μ) δM + U^μ ∇_μ δM .
```
Hence δM obeys a **linear first-order transport PDE**
```
U^μ ∇_μ (δM) + (∇_μ U^μ) (δM) = S[g, δg, δU, δZ] ,     (∗∗)
```
where the source `S` is the negative of the other two terms in `(∗)`:
```
S = - ∇_μ [ δU^μ (M+F) + U^μ F'(Z) δZ ] - ½ J^μ g^{αβ} ∇_μ δg_{αβ} .
```

**DERIVED (decisive):** Equation `(∗∗)` is a **transport equation for δM along
the flow lines of `U`**. Its solution, with an integration constant (initial
data) on a Cauchy surface Σ, is
```
δM(x) = [ transport of the IC from Σ to x ]
       + ∫_{Σ→x along U}  exp( -∫ (∇_μ U^μ) dτ )  S(τ) dτ .
```
Consequences:

1. **δM is nonlocal in δg.** The source `S` contains `δg`, `δU`, `δZ` (and their
   first derivatives), and δM is obtained by **integrating S along the flow lines
   of U from a Cauchy surface**. Therefore δM — and hence
   `E_{μν} = δM/δg^{μν}` — is a **nonlocal tensor**: it is built from retarded
   Green's functions (via δΦ, δZ) **and** transport integrals (via δM).

2. **δM is not a local differential expression in δg.** No finite-order
   differential operator in δg gives δM. The "Hessian" of the action with
   respect to `g` is therefore **not a local tensor**; it is a nonlocal
   (integral) operator. This is the rigorous form of the "naive Hessian"
   warning noted in the baseline.

3. **The integration constant (IC) is a physical degree of freedom.** The
   transport equation determines δM only up to data on Σ. Different ICs give
   different δM (and different `E_{μν}`). The IC is **not** fixed by the
   action principle unless an additional boundary term is specified. This is a
   **gauge/IC ambiguity** in the variation that must be resolved for the
   field equation to be well-defined. (See the causality phase, where the
   in-in/CTP prescription fixes the IC.)

---

## 4. The field equation and the conservation constraint

Varying the action
```
S = (c^3/16πG) ∫ √(-g) [ R - 2Λ - (a_0^2/c^4) M[g] ] + S_m
```
with respect to `g^{μν}` gives (structure; full form in Phase VII)
```
G_{μν} - Λ g_{μν} - (a_0^2/c^4) E_{μν} = (8πG/c^4) T^{(m)}_{μν} ,
```
where `E_{μν} = δM/δg^{μν}` (the M-stress tensor, up to the overall
`a_0^2/c^4` factor absorbed into the definition).

**DERIVED (conservation constraint):** Taking the covariant divergence and using
the contracted Bianchi identity `∇^μ G_{μν} = 0`,
```
∇^μ [ (a_0^2/c^4) E_{μν} ] = (8πG/c^4) ∇^μ T^{(m)}_{μν} .
```
For **matter on-shell** (`∇^μ T^{(m)}_{μν} = 0` by the matter EOM), this requires
```
∇^μ E_{μν} = 0        (on the full on-shell solution).       (C)
```
**This is the key consistency condition.** The nonlocal tensor `E_{μν}`
constructed from the transport-defined δM **must be covariantly conserved**
on-shell. Whether it is is the crux of the closure: it is not automatic,
because `E_{μν}` is a nonlocal (integral) tensor and its divergence involves
interchanging divergences with transport integrals and retarded Green's
functions. This is the relativistic analogue of the requirement that the MOND
force be a gradient (irrotational), and it is the condition most likely to
**fail** (as it did in the prior Deffayet-Woodard generation).

---

## 5. The T-determination gap  (UNKNOWN)

The frozen chain writes `T[g]`, but the **only** equation for `T` in the frozen
candidate is the unit-normalization **constraint**
```
∇_μ T ∇^μ T = -1 ,
```
which does **not** determine `T` from `g`. There is no evolution equation for
`T`, and the frozen action has **no** `δS/δT` term.

Therefore the variation `δM[g]` is **not well-defined** until the role of `T`
is fixed:

- **(i) `T` is an independent dynamical field.** Then the action must include a
  kinetic term for `T` (e.g. a mimetic/constraint term), and the functional is
  really `M[g, T]`, with `δM = (∂M/∂g)δg + (∂M/∂T)δT`. The unit constraint
  `∇T·∇T = -1` is then a constraint in the Hamiltonian sense (à la mimetic
  gravity), with a Lagrange multiplier. This adds a **new DOF** (or a
  constraint) that is absent from the frozen candidate.

- **(ii) `T` is a specified functional of `g`** via an unspecified map `T[g]`.
  Then `δM[g]` is well-defined only once the map is given. The frozen candidate
  does not specify it.

**Status: UNKNOWN.** This is a **gap in the frozen candidate**: the variation
δM[g] depends on an unspecified object (the map `T[g]` or the EOM for `T`).
The closure cannot produce a unique field equation until this gap is filled.

---

## 6. Summary of Phase II results

| # | Result | Status |
|---|--------|--------|
| 1 | M is a nonlocal functional (solution of a transport PDE up to IC on a Cauchy surface). | DERIVED |
| 2 | The varied transport equation is `∇_μ[δJ^μ + ½ J^μ g^{αβ}δg_{αβ}] = 0`. | DERIVED |
| 3 | δM obeys a linear first-order **transport PDE** `U^μ∇_μ δM + (∇·U)δM = S[g,δg,δU,δZ]`. | DERIVED (decisive) |
| 4 | **δM is nonlocal in δg** (transport integral of a source built from δg). `E_{μν}=δM/δg^{μν}` is a nonlocal (integral) tensor, not a local differential operator. | DERIVED (decisive) |
| 5 | The IC of the transport equation is an **unfixed ambiguity** in δM (a physical DOF or gauge, to be fixed by the in-in prescription). | DERIVED / UNKNOWN (fix pending) |
| 6 | The field equation requires `∇^μ E_{μν} = 0` on-shell (conservation constraint). Not automatic for a nonlocal E; the crux of the closure. | DERIVED (constraint) / UNKNOWN (satisfaction) |
| 7 | The variation δM[g] is **not well-defined** until the role of `T` (the `T[g]` map or the T-EOM) is fixed. | UNKNOWN (gap) |

**Phase II verdict:** The first variation is well-defined **only as a
nonlocal transport expression**, and it carries (a) an unfixed integration
constant, (b) a non-conservation risk for `E_{μν}`, and (c) a gap in the
definition of `T`. None of these is resolved by the frozen candidate. The
variation is therefore **structurally nonlocal and underdetermined**, which
carries directly into Phases III–VII.
