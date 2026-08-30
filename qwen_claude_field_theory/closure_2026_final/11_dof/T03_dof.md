# T03 — Physical DOF / constraint analysis (the crux)

Status labels: `DERIVED` / `IMPOSED` / `FITTED` / `UNKNOWN`.
Verifies: `11_dof/T03_dof.py` (bi-scalar diagonalization + constraint reduction PASS).

This file answers the single most important remaining question of the closure:
**does the apparent negative mode (the bi-scalar ghost `b = Φ − ξ`) correspond to
an independently specifiable physical propagating DOF after the full causal
restrictions are imposed, or is it a spurious localization artifact?**

---

## 1. The three descriptions (separated, per the task)

| | A. naive local auxiliary | B. constrained local (retarded BC) | C. physical nonlocal functional |
|---|---|---|---|
| `(Φ,ξ)` | 2 independent fields (bi-scalar) | `Φ = Box_ret^{-1}J` a functional; `ξ` multiplier | `Φ = Box_ret^{-1}J` a functional of `g` |
| independent initial data for `(Φ,ξ)` | 2 (field+velocity each) | 0 (retarded BC removes homogeneous part) | 0 (fixed retarded functional of `g`) |
| DOF from `(Φ,ξ)` | 2 (1 healthy `a` + 1 ghost `b`) | 0 | 0 |
| ghosts | 1 (`b`) | 0 | 0 |

## 2. The bi-scalar diagonalization  (DERIVED, verified)

The localized kinetic term `∫ ξ Box Φ` (after integrating by parts) is, in
velocities `v_Φ = ∂_tΦ`, `v_ξ = ∂_tξ` (flat, signature −+++):
```
L_kin = v_ξ v_Φ .
```
Change variables to the bi-scalar combinations
```
a = Φ + ξ  (healthy),    b = Φ − ξ  (ghost),
v_Φ = (v_a + v_b)/2,     v_ξ = (v_a − v_b)/2 .
```
Then (verified in the script)
```
L_kin = (1/4)( v_a² − v_b² ) .
```
- `a`: coefficient `+1/4` → **healthy** kinetic sign (Hessian `+1/2 > 0`).
- `b`: coefficient `−1/4` → **ghost** kinetic sign (Hessian `−1/2 < 0`).

Full quadratic action (time + space):
```
∫ ξ Box Φ  =  (1/4) ∫ a Box a  −  (1/4) ∫ b Box b .
```
This is the **standard Woodard / Deffayet-Woodard bi-scalar**: localizing the
retarded inverse `Box^{-1}` *off-shell* introduces one healthy scalar `a` and
one ghost scalar `b`. **This is the naive-Hessian warning made precise**
(eigenvalues `{+1, −1}`, `det = −1`).

## 3. The constraint reduction  (DERIVED, decisive)

The off-shell localized system has `(Φ, ξ)` as two independent fields (2 DOF).
But the **physical theory is the nonlocal functional**, in which
```
Φ = Box_ret^{-1} J[g, T] ,   J = R_{μν} U^μ U^ν ,
```
with the **retarded boundary condition** (vanishing past data). This makes `Φ`
a **functional of the source** `J`, i.e. of the metric and clock. It is **not**
an independently specifiable field: its "initial data" are fixed by the retarded
prescription, not chosen freely.

A homogeneous bi-scalar mode `b_h` (a free solution of `Box b_h = 0`) is
exactly the kind of data the retarded boundary condition **removes**. Therefore:
- **off-shell (description A):** `b` is an independent propagating DOF → ghost.
- **on the retarded branch (descriptions B, C):** `b` is fixed to its sourced
  (particular) value `b = b_p[g]`; the homogeneous `b_h` is not allowed →
  `b` is **not** an independently specifiable physical DOF.

**DERIVED (decisive DOF result):** In the physical (retarded) nonlocal theory,
the ghost `b = Φ − ξ` is a **spurious localization artifact**. It is not a
physical propagating degree of freedom. The physical DOF count is:
```
2 (tensor, as in GR)  +  (0 or 1 clock T, see §5)  +  0 (nonlocal sector)
= 2 or 3 physical DOF,   GHOST-FREE (in the DOF sense).
```

## 4. The (M, η) transport sector  (DERIVED)

- `M`: algebraic EOM (no kinetic term) → Lagrange-multiplier-like, **0** DOF.
- `η`: first-order (transport) EOM → **0** propagating DOF at quadratic order.
Contribution: **0** propagating DOF. (Higher-order couplings make them weakly
dynamical but add no independent propagating DOF.)

## 5. The clock T  (UNKNOWN — the T01 gap)

- If `T = T[g]` (a specified functional, e.g. a coordinate/matter clock): **0** DOF.
- If `T` is a dynamical mimetic scalar (constraint `∇T·∇T = −1` with multiplier):
  **1** DOF.
The frozen candidate does not specify which. **Status: UNKNOWN.** This adds 0 or
1 to the total. It does **not** affect the ghost conclusion.

## 6. Dirac-Bergmann summary (Minkowski background)

| quantity | A. naive local | B. constrained | C. nonlocal |
|---|---|---|---|
| canonical fields | `g, T, Φ, ξ, M, η` | same, with retarded BC | `g, T` (+ functionals) |
| primary constraints | `p_ξ ≈ 0`, `p_M ≈ 0` (multipliers) | same | n/a (functionals) |
| secondary constraints | `Box Φ = J`, `∇·(U(M+F))=0`, `∇T·∇T=−1` | same | same (as definitions) |
| 1st-class | diffeo (4) | diffeo (4) | diffeo (4) |
| 2nd-class | bi-scalar pair `(Φ,ξ)` off-shell | removed by retarded BC | removed (functionals) |
| constraint matrix rank | 2 (bi-scalar) | 0 | 0 |
| physical phase-space dim | 4 (tensor) + 2 (bi-scalar) + … | 4 (tensor) + … | 4 (tensor) + … |
| **physical DOF** | 2 tensor + 2 bi-scalar (+T) | 2 tensor (+T) | 2 tensor (+T) |
| **ghosts** | 1 (`b`) | 0 | 0 |

**Multiplier fixing:** in description A the bi-scalar pair is 2nd-class (fixes
the momenta); in B/C the retarded BC plays the role of the constraint that fixes
the homogeneous data.

## 7. FLRW background (sketch)

On a homogeneous FLRW background, `U^μ = (1,0,0,0)` (comoving clock) and
`R_{μν}U^μU^ν = R_{00}` is spatially constant. Then `Box Φ = R_{00}` gives
`Φ(t)` a **spatially constant** function of time (a functional of the FLRW
scale factor). The bi-scalar `b` is again spatially constant and fixed by the
retarded prescription → **0** spatially-localized DOF. The tensor sector reduces
to the 2 graviton polarizations as in GR. The same conclusion as Minkowski holds:
**the nonlocal sector carries no independent propagating DOF on FLRW.**
(Feeds the linear-cosmology analysis; no new ghost appears.)

## 8. THE CAVEAT — a DOF count is NOT a stability proof  (UNKNOWN)

This is the critical honesty point and the remaining part of Gate 5:

- The DOF analysis shows `b` is **not an independently specifiable** DOF. That
  removes the *free* ghost (no arbitrarily-seeded negative-norm state).
- **However**, the *sourced* (particular) part `b_p[g]` is a causal response of
  the metric. A causal response can still be **unstable**: it could exhibit
  exponential growth (a "ghost-like" instability in the homogeneous sector) or
  a gradient instability (superluminal / tachyonic propagation) even with no
  independent initial data.
- **No such stability proof has been established.** The dispersion relation of
  the sourced `b_p` mode, the sign of its residue at the pole, and the
  absence of exponential growth are all **UNKNOWN**.

Therefore the DOF result is a **necessary but not sufficient** condition for
health. The theory is **ghost-free in the DOF sense** but its **stability is
not yet proven**.

## 9. Output verdict

**PASS** for the DOF/ghost *count* (verified in the script). The decisive
conclusion:

> **The ghost `b = Φ − ξ` is a spurious localization artifact, not a physical
> propagating DOF, in the physical (retarded) nonlocal theory.** The nonlocal
> sector contributes 0 independent initial data; the physical DOF are the 2
> tensor modes (plus 0 or 1 clock T).

**But** the stability of the sourced response (no exponential/gradient
instability) is **UNKNOWN** and remains the open part of Gate 5. This is the
exact obstruction if a full proof is demanded: one must compute the dispersion
relation and pole residues of the sourced `b_p` mode (or the effective
nonlocal `E_{μν}`) and show they are stable.

**Most important unresolved item (carried to final report / Gate 5):**
Stability of the sourced nonlocal response (no exponential/gradient
instability) — a DOF count does not establish this.
