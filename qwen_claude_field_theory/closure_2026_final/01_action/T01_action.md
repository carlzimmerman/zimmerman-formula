# T01 — Exact action-level definition of M[g] and the first variation

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.
Verifies: `01_action/T01_action.py` (all local ingredients PASS).

---

## 1. Conventions  (DERIVED, frozen)

- Signature **(-,+,+,+)**. `Box = nabla_mu nabla^mu = (-∂_t² + ∇²)` in flat space.
- Curvature fixed by `+ (c³/16πG) ∫ √(-g) R` giving standard Einstein equations.
- `δ√(-g) = -½ √(-g) g_{μν} δg^{μν}`; `δR_{μν}` the standard linearized Ricci.
- `U_μ = -∇_μ T`, unit timelike: `U^μ U_μ = -1`.

## 2. The active repaired candidate (FROZEN)

```
S_tot = S_m[g,ψ] + (c³/16πG) ∫ d⁴x √(-g) [ R - 2Λ - κ M[g] ],   κ ≡ a₀²/c⁴.
```

Functional chain:
```
g_{μν} -> T[g] -> U_μ[g] -> Φ[g] -> Z[g] -> M[g]
```

## 3. Complete constrained auxiliary representation

Introduce multipliers `ξ` (for the retarded curvature response) and `η` (for the
transport definition of M):

```
S_aux = S_m + (c³/16πG) ∫ √(-g) [
     R - 2Λ
   - κ M
   + ξ ( Box Φ - R_{μν} U^μ U^ν )
   + η  ∇_μ ( U^μ ( M + F_ε(Z) ) )
]
```

Fields and multipliers:

| symbol | role | order |
|--------|------|-------|
| `g_{μν}` | metric (dynamical) | 2nd |
| `T` | clock scalar, `U_μ=-∇_μ T`, `∇T·∇T=-1` | constraint (mimetic) |
| `Φ` | curvature response `Box Φ = R_{μν}U^μU^ν` (retarded) | 2nd |
| `ξ` | multiplier for `Box Φ = R_{uu}` | 2nd (conjugate to Φ) |
| `M` | transport scalar | 0th (algebraic) |
| `η` | multiplier for transport eq | 1st (transport) |
| `Z` | `Z = (4c⁴/a₀²) ∇_μΦ ∇^μΦ` (defined, not dynamical) | — |

`Z` and `U_μ` are **defined** quantities, not independent fields. The only
independent fields are `g, T, Φ, ξ, M, η`.

### Euler-Lagrange equations (DERIVED)

- `δ/δξ`:  `Box Φ - R_{μν}U^μU^ν = 0`  (retarded solution).
- `δ/δη`:  `∇_μ[U^μ(M+F_ε(Z))] = 0`  (transport definition of M).
- `δ/δΦ`:  `Box ξ = (4c⁴/a₀²) F_ε'(Z) [ 2∇_μΦ ∇^μ δ... ]` — i.e.
  `Box ξ = - (8c⁴/a₀²) F_ε'(Z) ∇^μΦ ∇_μ(·)`  (the adjoint, see T02).
- `δ/δM`:  `-κ - ∇_μ U^μ + η ∇_μ[ U^μ (δ/δM of F-term) ] = 0` — **algebraic** in M
  (no derivatives of M after integrating `∇_μ(U^μ M)` by parts).
- `δ/δT`:  the mimetic constraint `∇_μT ∇^μT = -1` (via its multiplier) — see §5.
- `δ/δg`:  the full metric equation (this file, §6; carried to T02/T04).

## 4. The retarded boundary condition — how it is imposed

`Box Φ = R_{μν}U^μU^ν` has the general solution
`Φ = Φ_h + Box_ret^{-1}(R_{uu})`. The **retarded prescription** is imposed by
requiring `Φ → 0` (or the chosen physical background) on the **past** boundary /
Cauchy surface, i.e. `Φ` is the unique solution with vanishing advanced data:

```
Φ(x) = ∫ d⁴x' G_ret(x,x') R_{μν}(x') U^μ(x') U^ν(x') ,   G_ret = 0 for x outside future of x'.
```

**IMPOSED:** the retarded (vanishing-past-data) boundary condition is an *input*,
not derivable from the bulk action. Without it the auxiliary `Φ` carries
advanced/free data.

## 5. The T-determination gap  (UNKNOWN — must be closed)

The frozen chain writes `T[g]`, but the only T-equation is the **constraint**
`∇_μT ∇^μT = -1`, which does not determine `T` from `g`. There is no `δS/δT`
evolution in the frozen action. Two cases:

- **(i) T dynamical (mimetic):** add a constraint multiplier `λ` for `∇T·∇T+1=0`;
  T is then a mimetic scalar carrying **1** propagating DOF.
- **(ii) T = T[g]:** a specified functional of the metric (e.g. a coordinate time
  or a matter clock); then T carries **0** DOF and `δT` is a known functional of `δg`.

**Status: UNKNOWN.** The variation `δM[g]` is not uniquely defined until the
`T[g]` map (case ii) or the T-EOM (case i) is fixed. This is carried to T03.

## 6. The first variation δS/δg^{μν} — complete chain rule

Varying the repaired action gives

```
G_{μν} - Λ g_{μν} - (a₀²/c⁴) E_{μν} = (8πG/c⁴) T^{(m)}_{μν} ,
E_{μν} ≡ δM[g]/δg^{μν} .
```

The full chain rule for `δM` (every indirect dependency) is

```
δM = (∂M/∂g)δg + (∂M/∂T)δT + (∂M/∂Φ)δΦ + (∂M/∂Z)δZ ,
δΦ = Box_ret^{-1} δ(R_{μν}U^μU^ν) ,      (retarded)
δZ = (8c⁴/a₀²)( ∇_μΦ ∇^μ δΦ + ∇_μΦ ∇^μΦ δ... )  [metric part of ∇Φ∇Φ],
δU_μ = -∇_μ δT .
```

### The decisive result (DERIVED)

The transport equation `∇_μ[√(-g) U^μ (M+F)] = 0`, varied, gives a **linear
first-order transport PDE for δM along the flow lines of U**:

```
U^μ ∇_μ (δM) + (∇_μ U^μ)(δM) = S[g, δg, δU, δZ] ,          (∗)
S = -∇_μ[ δU^μ (M+F) + U^μ F'(Z) δZ ] - ½ (M+F) U^μ g^{αβ} ∇_μ δg_{αβ} .
```

Its solution, with initial data on a Cauchy surface Σ (retarded/IMPOSED), is

```
δM(x) = [transport of δM|_Σ] + ∫_{Σ→x along U} exp(-∫∇·U dτ) S(τ) dτ .
```

Consequences:

1. **δM is nonlocal in δg** — it is a transport integral of a source built from
   `δg, δU, δZ` (and their first derivatives). `E_{μν}` is therefore a **nonlocal
   (integral) tensor**, not a finite-order local differential operator. This is
   the rigorous form of the "naive Hessian" warning.
2. **The integration constant is an unfixed ambiguity** in `δM` (homogeneous
   solution of (∗)), to be fixed by the in-in/CTP prescription (T02).
3. **Conservation constraint:** on-shell, Bianchi + matter EOM require
   `∇^μ E_{μν} = 0`. For a nonlocal `E` this is **not automatic** — it is the
   crux (carried to T02/T03).
4. **Ghost-freedom is NOT claimed.** The auxiliary Hessian is indefinite
   (verified in `T01_action.py`); whether the negative mode is physical is the
   T03 question.

## 7. Boundary terms — shown, not dropped

Integrating `∫ √(-g) η ∇_μ(U^μ M)` by parts produces the boundary term
`∮ η U^μ M dΣ_μ`. It vanishes on the chosen spacelike Cauchy boundary **provided**
`η` and `M` have the prescribed (retarded / isolated) fall-off there. Similarly
`∫ √(-g) ξ Box Φ → -∫ √(-g) (Box ξ) Φ + ∮ ξ ∂_n Φ`. These surface terms are the
location where the retarded boundary condition is *enforced*; they are not
simply discarded. (The in-in/CTP contour supplies the matching that makes them
single-valued — T02.)

## 8. Single-copy vs doubled (in-in)

A **single-copy** variational action with a *fixed* retarded inverse gives the
retarded response directly (the physical classical equation). However, the
variation of a *functional containing a fixed inverse* is **not** obtained by
varying a local single-copy action naively: the localizing multiplier `ξ`
introduces the advanced/ghost branch. The **in-in / Schwinger-Keldysh doubled**
construction is the rigorous route that (a) fixes the integration constant of
(∗) and (b) selects the retarded physical branch while cancelling the advanced
adjoint piece. This is worked out in T02.

## 9. Output verdict

**PASS** for the *definition* and the *local ingredients* (verified in
`T01_action.py`). The first variation is **well-defined only as a nonlocal
transport expression** carrying (a) an unfixed integration constant and (b) a
non-conservation risk for `E_{μν}`, and (c) the `T[g]` gap. None is resolved by
the frozen candidate; they are carried to T02 (causal/adjoint) and T03 (DOF).

**Most important unresolved equation (carried to T02):**
```
U^μ ∇_μ(δM) + (∇·U)(δM) = S[g,δg,δU,δZ]   with retarded IC,
and the on-shell conservation constraint   ∇^μ E_{μν} = 0 .
```
