# Phase IV — Local Auxiliary Representation + Naive Hessian

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.

Phase II established that `E_{μν} = δM/δg^{μν}` is a **nonlocal (integral)
tensor**. To study its DOF and ghost content, we write a **local auxiliary
representation** of the nonlocal functional and analyze the **quadratic
(Hessian) action** of the auxiliary fields. This makes the "naive Hessian
warning" of the baseline precise.

---

## 1. The localized action

Introduce auxiliary fields to replace the retarded inverse and the transport
definition of M:

```
S_aux = ∫ d^4x √(-g) [ -κ M
                       + ξ ( Box Φ - R_{μν} U^μ U^ν )
                       + η  ∇_μ ( U^μ ( M + F_ε(Z) ) ) ]
κ = a_0^2/c^4 ,   Z = (4 c^4/a_0^2) ∇_μ Φ ∇^μ Φ ,   U^μ U_μ = -1 .
```

- `ξ` is the multiplier for `Box Φ = R_{uu}` (the retarded curvature response).
- `η` is the multiplier for the transport equation
  `∇_μ[√(-g) U^μ (M+F)] = 0`.
- `M` appears algebraically (see §2).

**DERIVED:** Varying `S_aux` with respect to `ξ` and `η` reproduces the frozen
chain (`Box Φ = R_{uu}`, transport equation). Varying with respect to `Φ` and
`M` gives the remaining EOMs. The localized action is **equivalent** to the
nonlocal action on-shell, **provided** the auxiliary fields satisfy their EOMs
and the correct (retarded) boundary conditions are imposed.

> **IMPOSED:** The retarded boundary conditions on `Φ` (and the in-in/CTP
> prescription of Phase III) are an **input**. Without them, the auxiliary
> action admits advanced/ghost solutions.

---

## 2. Field roles and the algebraic M

**DERIVED:** Collect the terms linear in `M` in `S_aux`:
```
S_M = ∫ √(-g) [ -κ M + η ∇_μ ( U^μ M ) ]
    = ∫ √(-g) M [ -κ - ∇_μ U^μ ]   (after integrating ∇_μ(U^μ M) by parts) .
```
The M-EOM is therefore **algebraic** (no derivatives of M):
```
-κ - ∇_μ U^μ + (η-couplings from F(Z) variation) = 0 .
```
On the isolated stationary branch (`∇_μ U^μ = 0`, `F` variation subleading),
`M ≈ -κ^{-1}` is algebraic. **M is a Lagrange multiplier (non-dynamical) at
leading order.** It carries **no kinetic term** and hence **no propagating DOF**
at leading order. (Higher-order couplings make it weakly dynamical; see Phase VI.)

---

## 3. The quadratic (Hessian) action around flat space

Set `g = η_Mink + ...` (we set δg = 0 for the auxiliary Hessian),
`U^μ = (1,0,0,0)`, `R_{uu} = 0`. Expand to second order in the auxiliary
fluctuations. The quadratic action is
```
S_2 = ∫ d^4x [ -κ δM + δξ Box δΦ + δη ∂_t(δM) + (cubic terms dropped) ] .
```

### 3.1 The (Φ, ξ) bi-scalar sector  (the ghost)

The term `∫ δξ Box δΦ` is the **Woodard bi-scalar**. Diagonalize with
```
a = δΦ + δξ   (healthy),      b = δΦ - δξ   (ghost).
```
By integration by parts (signature −+++, `Box = −∂_t² + ∇²`):
```
∫ δξ Box δΦ  =  (1/4) ∫ a Box a  −  (1/4) ∫ b Box b ,
```
and
```
∫ a Box a = ∫ [ (∂_t a)² − (∇a)² ]   (healthy kinetic),
∫ b Box b = ∫ [ (∂_t b)² − (∇b)² ] .
```
Therefore
```
S_2^(Φξ) = (1/4) ∫ [ (∂_t a)² − (∇a)² ]  −  (1/4) ∫ [ (∂_t b)² − (∇b)² ] .
```
**DERIVED (decisive):** `a = δΦ + δξ` has the **correct** kinetic sign
(healthy scalar), but `b = δΦ − δξ` has the **wrong** kinetic sign — it is a
**ghost scalar**. This is the **standard Woodard / Deffayet-Woodard
localization ghost**: localizing the retarded inverse `Box^{-1}` necessarily
introduces a ghost degree of freedom.

This is the **naive Hessian warning** made precise: the Hessian of the
localized action with respect to `(Φ, ξ)` has one negative-eigenvalue
direction (`b`), i.e. the auxiliary Hessian is **indefinite**.

### 3.2 The (η, M) constraint sector

The term `∫ [ -κ δM + δη ∂_t δM ]` is **first order** (no kinetic term). The
EOMs are
```
δS/δM  = -κ + ∂_t η = 0    =>  ∂_t η = -κ   (1st-order transport),
δS/δη  = ∂_t(δM)   = 0    =>  δM = const(t)  (algebraic at 2nd order).
```
**DERIVED:** At quadratic order, `(η, M)` is a **constraint pair** with **no
kinetic term** and **no ghost**. The ghost is entirely in the `(Φ, ξ)`
bi-scalar.

---

## 4. The naive Hessian and why it is misleading

**DERIVED:** The "naive Hessian" — the matrix of second functional derivatives
of the **localized** action with respect to the auxiliary fields `(M, Φ, ξ, η)`
— is **indefinite** (one ghost direction `b = Φ − ξ`). However, this Hessian is
**not** the Hessian of the **original nonlocal** action with respect to the
metric `g`. The relationship is:

1. The original action `S[g]` depends on `g` only through the **nonlocal**
   functional `M[g]`. Its "Hessian" `δ²M/δg δg` is a **nonlocal (integral)
   operator**, not a local matrix.

2. The auxiliary Hessian is a **local** approximation that is valid only after
   the auxiliary fields are integrated out (or constrained to their EOMs). The
   ghost `b` is a **gauge/auxiliary** artifact of the localization **unless**
   it couples to the physical (metric) sector.

3. The decisive question — deferred to Phase VI — is whether the ghost `b`
   **decouples** from the physical metric perturbations (in which case it is a
   harmless auxiliary artifact) or **couples** to them (in which case it is a
   **physical ghost** that makes the theory unstable / acausal).

**Phase IV verdict:** The localized auxiliary Hessian is **indefinite** (one
ghost direction `b = Φ − ξ`). This **confirms the baseline's naive Hessian
warning** at the level of the auxiliary representation. Whether this ghost is
**physical** (couples to the metric) is the question for Phase VI.
