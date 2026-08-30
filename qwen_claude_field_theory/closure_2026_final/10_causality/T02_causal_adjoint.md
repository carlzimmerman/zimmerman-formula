# T02 — Correct causal / adjoint variation of the retarded nonlocal functional

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.
Verifies: `10_causality/T02_causal_adjoint.py` (all identities PASS).

This file answers the central technical question of the closure:
**what is the correct causal variation `δM[g]/δg^{μν}` of the retarded
nonlocal functional, and is the physical response retarded or advanced?**

---

## 1. The two distinct responses (the key distinction)

The functional contains the **retarded inverse** `Box_ret^{-1}`:
```
Φ = Box_ret^{-1} J ,     J = R_{μν} U^μ U^ν .
```
Two mathematically distinct objects act on a metric perturbation `δg`:

- **Retarded physical response** `R_ret[δg]`: the change in the *physical* field
  `Φ` (the retarded solution) under `δg`. This is the object that enters the
  physical field equation. It is causal: `R_ret[δg](x)` depends on `δg` only in
  the **past** of `x`.

- **Advanced adjoint response** `R_adv[δg]`: appears when one *varies the
  functional* by integration by parts. The variational derivative of a
  functional containing `Box_ret^{-1}` naturally produces the **adjoint**
  operator, which for a self-adjoint `Box` is again `Box^{-1}` but acting with
  the **advanced** (or "in-out") boundary condition. This is the object that
  must be identified and controlled.

**DERIVED (decisive):** The physical classical equation requires the
**retarded** response. A naive single-copy local action, when varied, produces
the **adjoint (advanced-in-the-homogeneous-part)** response. The two agree on
the *particular* (forced) solution but differ in the *homogeneous* (free) part.
The difference is exactly the boundary/initial-data term.

## 2. The adjoint (Green second) identity

The conversion between the retarded and adjoint forms is the Green second
identity (verified pointwise in the script):
```
∫ √(-g) [ ψ Box χ - χ Box ψ ] = ∫ √(-g) ∇_μ( ψ ∇^μ χ - χ ∇^μ ψ ) .
```
Take `ψ = Φ` (the physical retarded solution) and `χ = δΦ` (its variation,
`Box δΦ = δJ`, retarded). Then
```
∫ √(-g) Φ Box δΦ = ∫ √(-g) δΦ Box Φ  +  boundary .
```
On-shell `Box Φ = J`, so the **adjoint form** of the `Φ`-dependent part of `δM`
is
```
(δM)_Φ  ~  ∫ √(-g)  F'(Z) (∇Φ·∇δΦ)  ~  ∫ √(-g)  F'(Z) [ δΦ · (Box Φ) + boundary ]
        =  ∫ √(-g)  F'(Z) δΦ · J  +  boundary ,
```
i.e. the adjoint form is **local in `δΦ`** (times the nonlocal coefficient
`F'(Z)`), with the nonlocality carried entirely by the **retarded** `δΦ =
Box_ret^{-1} δJ`. The boundary term is a total divergence fixed by the retarded
boundary condition (vanishes on the past boundary for retarded data).

**DERIVED:** Therefore the causal metric variation is
```
δM[g] =  (transport part, T01 eq. (∗))
       + ∫ √(-g)  [ adjoint kernel ](x) · δJ(x')  ,   δJ = δ(R_{μν}U^μU^ν),
```
where the adjoint kernel is a **retarded** Green's-function integral (the
physical response). The advanced part is absent from the physical equation
because the retarded boundary condition sets the homogeneous solution to zero.

## 3. The adjoint field equation

Define the **adjoint field** `Φ*` by
```
Box Φ* = F'(Z) · (coefficient from δZ/δΦ) ,     with ADVANCED boundary condition
        (Φ* → 0 on the FUTURE boundary / turning point).
```
Then the `Φ`-part of the metric variation is the **in-out pairing**
```
(δM)_Φ = ∫ √(-g)  Φ*(x)  δJ(x)  +  transport .
```
The advanced adjoint `Φ*` is a **bookkeeping device**: it re-expresses the
retarded response as a local-in-`δJ` integral. It does **not** add a physical
degree of freedom; it is the variational dual of the retarded `Φ`.

## 4. Single-copy vs doubled (in-in / CTP)

**DERIVED:** A **single-copy** local action `S_aux[g,Φ,ξ]` (T01 §3) varied
naively produces the **in-out** equation, which contains both the retarded
physical response and an advanced adjoint piece (the homogeneous/free part).
This is because the localizing multiplier `ξ` introduces an independent
(Φ, ξ) pair whose quadratic action is the bi-scalar (see T03).

To obtain the **purely retarded physical** equation, one of two equivalent
routes:

1. **Direct retarded functional:** define `M[g]` *as* the retarded functional
   (the nonlocal definition of T01). Then `δM/δg` is the retarded response by
   construction; no doubling is needed for the *physical* equation. The cost is
   that the "Hessian" is a nonlocal integral operator, not a local matrix.

2. **In-in / Schwinger-Keldysh doubled construction:** double the fields on the
   closed time contour, impose (a) causal IC at `t_0` (both branches coincide on
   the physical retarded data) and (b) turning-point matching `Φ_Δ(t_max)=0`,
   `M_Δ(t_max)=0`. Varying w.r.t. the **difference** field and taking `Φ_Δ→0`
   yields the retarded physical equation with the advanced piece cancelled by
   the turning-point condition.

**DERIVED (decisive):** The in-in turning-point condition `M_Δ(t_max)=0`
**uniquely fixes the homogeneous (integration-constant) part** of the transport
PDE for δM (T01 eq. (∗)). After this prescription, `δM` — and hence
`E_{μν}=δM/δg^{μν}` — is a **unique, causal (retarded) functional** of `δg`.
The integration-constant ambiguity flagged in T01 is **resolved**.

> **IMPOSED:** the specific retarded IC (vanishing difference at the turning
> point) is an *input*, not derivable from the bulk action. It is the standard
> in-in choice, physically motivated (selects the causal response).

## 5. Allowed initial data

**DERIVED:** The allowed (physical) initial data on a Cauchy surface Σ are:
- the metric and its conjugate momentum (the standard GR IVP data);
- the clock `T` and its mimetic constraint (T01 §5 gap — must be fixed);
- the retarded auxiliary fields are **NOT** independent data: `Φ` is fixed by
  `Box_ret^{-1} J` (retarded), and `M` is fixed by the transport equation with
  the in-in IC. The advanced/free homogeneous components are **not** allowed.

**The decisive question for T03:** are the auxiliary fields `(Φ, ξ)`
independently specifiable physical initial data, or fixed retarded functionals
of the metric? If the latter, the bi-scalar ghost of the *local* action is a
**spurious localization artifact**, not a physical DOF.

## 6. Explicit formula / algorithm for δM/δg

```
ALGORITHM  δM[g]/δg^{μν}(x):
  1. Compute δJ(x') = δ(R_{αβ}U^αU^β)/δg^{μν}(x')      [local, 2nd order in δg].
  2. Compute δΦ(x)  = ∫ G_ret(x,x') δJ(x') d⁴x'        [retarded, causal].
  3. Compute δZ(x)  = (8c⁴/a₀²)(∇Φ·∇δΦ) + (metric part of ∇Φ∇Φ).
  4. Solve the adjoint transport PDE (T01 (∗)) for δM with the in-in IC:
         U^μ∇_μ(δM) + (∇·U)(δM) = S[g,δg,δU,δZ],   δM fixed by turning-point cond.
  5. E_{μν}(x) = δM/δg^{μν}(x).
```
Every step is retarded/causal. `E_{μν}` is a **causal nonlocal tensor**.

## 7. Conservation constraint (carried to T03)

The on-shell conservation `∇^μ E_{μν}=0` (required by Bianchi + matter EOM) is
**not automatic** for the nonlocal `E`. It holds on the isolated stationary
branch (diffeomorphism-invariant IC) but is **UNKNOWN for general
time-dependent configurations** (the in-in IC may break diffeomorphism
invariance). This is carried to T03 along with the ghost question.

## 8. Output verdict

**PASS** for the causal-adjoint structure (identities verified in the script).
The causal variation is well-defined as a **retarded** functional once the
in-in/CTP prescription fixes the integration constant. The advanced adjoint
piece is a bookkeeping device (the dual `Φ*`), not a physical DOF. The two
remaining open questions — (a) whether the auxiliary bi-scalar ghost is
physical, and (b) whether `∇^μE_{μν}=0` holds generally — are carried to T03.

**Most important unresolved item (carried to T03):**
Are the auxiliary fields `(Φ, ξ)` independently specifiable physical initial
data, or fixed retarded functionals of the metric? (the ghost question)
