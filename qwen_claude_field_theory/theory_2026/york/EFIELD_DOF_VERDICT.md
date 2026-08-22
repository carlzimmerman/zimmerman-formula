# EFIELD_DOF_VERDICT — does the auxiliary elliptic e-screen preserve York/CMC 2+0?

**Date:** 2026-08-22
**Question:** Adding an auxiliary elliptic external-field screening field `e` (with
`eps = e^2/a0^2` feeding `A(eps)` in the MOND kernel `U(y,eps)`) — does it preserve the
York/CMC 2+0 DOF, or does its coupling to `Phi` break it? Derived, not assumed. "No e-dot"
alone is explicitly **not** sufficient.

**Machine-verified scripts (all green, committed):**
- `york_efield_dof_2026.py` — Derivation-A (placeholder-coefficient Pfaffian, full Dirac + H_perp closure + DOF count)
- `york_efield_dof_crosscheck_2026.py` — Derivation-B (independent reduced-Phi cross-check, 16/16)
- `york_efield_dof_referee_2026.py` — hostile referee: the **real-coefficient** worst-case Pfaffian (k ∥ ∇Φ)

---

## VERDICT (scalar e): **2+0 PRESERVED — STRUCTURALLY VIABLE**

For a **scalar** screening field `e` carrying the elliptic gradient term `(1/2) D_i e D^i e`,
the York/CMC count is **2 local DOF + 0** (the two GR tensor polarizations; `Phi` and `e`
each carry **zero** propagating DOF), plus the one **global** York-time ↔ volume CMC pair
(not a local DOF). The Φ↔e coupling does **not** break it.

**The adversary agrees.** The hostile referee sharpened the Pfaffian to real principal
symbols in the worst-case direction (k ∥ ∇Φ) and attacked six ways; the scalar claim
survived every attack and the adversary's own verdict is `2+0_PRESERVED`. This is a
*confirmed* PASS under the hostile reading, not an unchallenged one — a breached claim
would not be a PASS, and nothing here was breached.

---

## (2) The Pfaffian and where it degenerates

Constraint set (per space point): gravity `H_perp, H_i` (first-class candidates) and the
auxiliary quartet `chi = (P_Phi, C_Phi, P_e, C_e)`, where
- `C_Phi = -δH/δΦ` = the eps-modified AQUAL elliptic equation,
- `C_e = -δH/δe = -D^2 e + W_e + 2 e U_eps(y,eps)` (the `2 e U_eps` term is the MOND→e back-coupling).

Structural zeros (both machine-verified):
- `{P_Phi, P_e} = 0` (momenta Poisson-commute)
- `{C_Phi, C_e} = 0` (both constraints are momentum-independent → zero symplectic overlap)

so the 4×4 Dirac matrix is the "checkerboard" whose Pfaffian is

```
Pf = {P_Phi,C_Phi}{P_e,C_e} - {P_Phi,C_e}{P_e,C_Phi} = a·d - b·c
```

Real principal symbols (worst case k ∥ ∇Φ, referee script):

| bracket | symbol | order in \|k\| |
|---|---|---|
| `a = {P_Phi,C_Phi}` | `(U_y + 2 y U_yy)·\|k\|^2`, `= (1-A) + A·√y(y+2)/(1+y)^{3/2}` | **2** (elliptic, AQUAL) |
| `d = {P_e,C_e}` | `\|k\|^2` (or `\|k\|^2 + M^2` with stabiliser `W=½M²e²`) | **2** (elliptic, from `-D^2 e`) |
| `b = {P_Phi,C_e}` | `i·(4e/a0²)·U_yeps·(k·∇Φ)` | **1** |
| `c = {P_e,C_Phi}` | adjoint of `b`, same coefficient (Hessian symmetry) | **1** |

with `U_yeps = A'(eps)·(mu_gal - 1)` the single shared coupling coefficient. Hence

```
Pf(k∥∇Φ) = (U_y + 2 y U_yy)·|k|^4  -  (16 e² y U_yeps² / a0²)·|k|^2
```

**The order-4 (principal) coefficient `U_y + 2 y U_yy` is strictly positive for any screened
point (`A<1`) or any `y>0`, and is INDEPENDENT of the coupling (`e, A'`)** — the coupling
enters **only** the subleading `k^2` term. So the diagonal `a·d ~ k^4` cannot be caught by
the cross `b·c ~ k^2`: `Pf ≠ 0` at principal-symbol order ⇒ the Dirac operator is elliptic of
order 4 ⇒ **all four (P_Phi, C_Phi, P_e, C_e) are second-class** ⇒ Φ and e each carry 0 DOF.
`Pf² = det(D)` verified.

**Why the cross can never catch the diagonal:** raising `b·c` to order 4 would need `C_e` to
depend on *second* derivatives of Φ (or `C_Phi` on second derivatives of e). The coupling is
only through the **algebraic** functions `U_eps(y)`, `U_yeps(y)` of the fields — exactly one
gradient per cross bracket. Order-4 diagonal is structurally protected.

**Where it degenerates (all benign / measure-zero):**
1. **Inherited deep-MOND point** `A=1` (no screening) **and** `y=0` (zero acceleration): the
   Phi principal symbol → 0. This is the *same* measure-zero degenerate-elliptic point as the
   Phi-only theory; at that very point the cross `b ∝ k·∇Φ ∝ √y` also → 0, so nothing new
   propagates. **Any screening `A<1` strictly lifts it** (coeff → `1-A > 0`). Frees no field DOF.
2. **Isolated finite-|k| zero** where the (real) `k^2` cross term equals the `k^4` diagonal.
   Irrelevant to constraint classification: second-class ⇔ the *leading* symbol is invertible
   as |k|→∞, which holds since the `k^4` coefficient > 0. A first-class combination would need
   a leading-order zero-mode direction; there is none.

**KNIFE-EDGE — the real content of "no e-dot alone is not enough":** `d = {P_e,C_e}` is order 2
**only** because of the `(1/2) D_i e D^i e` gradient term. A **purely algebraic** e (no gradient)
drops `d` to order 0, the diagonal `a·d` falls to order 2 and **ties** the order-2 cross `b·c` —
the Pfaffian could then vanish and free an extra propagating mode. The elliptic gradient term is
load-bearing. Adding a stabiliser `W=½M²e²` changes `d` only at order 0 (`|k|²+M²`), improving
invertibility with the same DOF count.

---

## (3) H_perp Dirac–DeWitt algebra: **CLOSES**

`{H_perp[N], H_perp[M]} = H_i[ h^{ij}(N ∂_j M − M ∂_j N) ]` with **unchanged structure functions**.
The e-density `V_e = (1/8πG)√h[ ½ h^{ij}∂_i e ∂_j e + W(e,q) ]` is (i) momentum-independent
(no π, no P_Φ, no P_e) ⇒ `{V_e,V_e}=0`, `{V_MOND,V_e}=0`; and (ii) **ultralocal in `h_ij`** —
algebraic in the metric *entries* (through `h^{ij}` and `√h`), carrying no derivative `∂_k h`.
Machine-verified: `δV_e/δh_ij` equals the ordinary ultralocal scalar e-stress over 30 random
positive-definite metrics (max error < 1e-9). An ultralocal metric variation multiplies the
*symmetric* kernel `N·M` ⇒ the antisymmetric bracket cancels ⇒ the e-sector rebuilds **no**
`H_i` term. The only non-ultralocal metric variation is `R³` (pure GR), which alone rebuilds
`H_i`. Tensor sector unchanged, **c_T = 1** intact. Same argument as the established Phi-only
closure (`dof_deformed_cmc_2026.py` step B), now extended to include `S_e`.

---

## (4) Honest scalar-vs-vector caveat

The result holds for a **SCALAR** `e` only, and a scalar screens **isotropically**: with
`eps = e²`, `A(eps)` multiplies the *whole* MOND term rotationally-invariantly. It suppresses the
MOND **monopole** — and with it the Cassini quadrupole `Q2` — **by switching MOND off**, not by
encoding the *direction* of `g_ext`. That is amputation, not an external-field mechanism, and it
likely **over-screens galaxies**. This is a phenomenology concern separate from (and not fatal to)
the DOF count, but it means the scalar is not physically the EFE object.

The physically-required anisotropic EFE quadrupole wants a **VECTOR** `E_i` (→ `g_Gal` at
infinity). Its DOF count is **NOT settled here** and does **NOT** inherit the scalar result
(referee-verified symbol algebra):
- A **non-gauge** full-gradient kinetic term `½(D_iE_j)(D^iE^j)` has symbol `|k|²·I₃`
  (`det = |k|⁶ ≠ 0`) ⇒ all 3 components elliptic/second-class ⇒ **0 DOF** — the scalar logic
  *would* carry over.
- A **Maxwell-type** `F_ij F^ij` has symbol `|k|²·I − k kᵀ`, **degenerate** in the longitudinal
  direction (`det = 0`, longitudinal eigenvalue 0) ⇒ transverse polarizations escape the elliptic
  constraint and **propagate (+2 DOF)**, demanding a fresh `c_T`/ghost check.

Which kinetic term the physical vector gets is undetermined here. **Vector version: INCOMPLETE —
flagged, not solved.** Do not assume the scalar 2+0 transfers.

Minor: global invertibility as an *integral* operator additionally needs the AQUAL/elliptic
boundary conditions (`Φ→0`, `e→g_Gal`) and convexity, assumed inherited from the Phi-only closure,
not re-proven for the coupled system here (principal-symbol ellipticity is proven).

---

## (5) Bottom line

**16 phase-space (12 h,π + 2 Φ,P_Φ + 2 e,P_e) − 4 second-class − 2×4 first-class = 4, /2 = 2.**

The scalar e-screen is **STRUCTURALLY VIABLE**: it adds zero propagating DOF, keeps `H_perp`
first-class, and preserves `c_T = 1`. The remaining question is **phenomenological, not
structural** — the fork the framework must clear is *Cassini-safe (small `Q2`)* ⇔ *Newtonian-ish
wide binaries*, to be decided by Gaia **DR4**. That fork is a data question about whether isotropic
scalar screening is the right physics, **not** a death of the construction at the level of degrees
of freedom.

Two live structural liabilities remain, both explicitly labelled INCOMPLETE, neither a scalar-count
breach: (a) the **vector** `E_i` version that the *anisotropic* EFE quadrupole actually needs —
own count required; (b) the phenomenological risk that scalar screening over-amputates galactic MOND.
