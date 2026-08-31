# FINAL_REPORT.md — FC-KH v1.0 terminal falsification (Phase 15)

Start commit `750805926eaaa1b0207e3b354d76b12deefcc1cf`. No git state touched; all files untracked.

# ███ GLOBAL STABILITY: KILL ███
**Failure class A (structural). Branch-wide, benchmark-independent, adversarially cross-checked.**

FC-KH v1.0 — `S=(M_Pl²/2)∫√-g[R−((β+3λ)/3)θ²−βσ²+f_FC(a)]`, `f_FC=−2Λ+αa²+2(2−α)a0²[1−(1+y)e^{−y}]`,
branch `α=2β` (β>0, λ>0, β≪1) — does **not** admit a stable hyperbolic MOND→Newtonian transition.
The khronometric K²(β,λ) backbone repairs the khronon *kinetic* ghost but leaves an **incurable
radial (parallel) gradient instability** in the band `a0 < a < y*·a0` (`y*≈31–45`, i.e. exactly the
`f''<0` window the mission flagged).

## The c²_IR sign behavior through a~a0 (the decisive result)
Reduced khronon dispersion after eliminating lapse and shift, physical sub-horizon band a0≪k≪M_*:
```
kinetic     A          = (1−β)(2+β+3λ)/(β+λ)                    > 0   (no ghost — backbone works)
tangential  c²_⊥(y)    = (4y0−W1)(β+λ)/[W1(1−β)(2+β+3λ)]        > 0   for ALL y0   (safe)
radial      c²_∥(y)    = (4−W2)(β+λ)/[W2(1−β)(2+β+3λ)],   W2=f''(y0)
            sign c²_∥  = sign f''(y0)
```
`f''(y)=2α+2(2−α)(1−y)e^{−y}`: **> 0** for y<1 (deep-MOND side) and y>y* (Newtonian side), but
**< 0 for 1<y<y***. Therefore:
- y0 < 1 (deep-MOND): c²_∥ > 0 — stable.
- y0 = 1 (a=a0): W2→0⁺ ⇒ c²_∥ → +∞ — strong coupling at the MOND scale.
- **1 < y0 < y* (the transition): c²_∥ < 0 — RADIAL GRADIENT INSTABILITY.**
- y0 > y* (Newtonian): c²_∥ > 0 — stable.

The instability sign is set by `f''` alone; the `(β+λ)/[(1−β)(2+β+3λ)]` prefactor is positive for
every β,λ>0, so it rescales the growth rate but **cannot flip the sign** — no branch point escapes.

## Required terminal numbers
| item | value |
|---|---|
| surviving region | y0<1 and y0>y* (deep-MOND & Newtonian ends) |
| failed region | 1 < a/a0 < y* (y*≈31–45), radial-wavevector khronon modes |
| worst transition point | benchmark y0≈2 (mid-transition); edges y0→1⁺, y0→y*⁻ diverge (W2→0⁻) |
| its a/a0, r, k | a/a0≈2; point-mass r≈0.5 r_M (r_M=√(GM/a0)); k-independent for a0≪k≪M_* |
| kinetic eigenvalue A | +2.003e3 (P1) — positive, no ghost |
| radial gradient c²_∥ (y0=2) | **−4.188e-3** (k-independent over 15 decades) |
| tangential gradient c²_⊥ (y0=2) | +3.190e-3 |
| tensor speed c_T² | 1/(1−β) = 1+1e-15 |
| scalar speed c_s² (high-a) | (β+λ)/[β(2+β+3λ)] ≈ 5.0e11 (BB α→0 strong coupling; positive) |
| G_N/G_C | (2+β+3λ)/(2−α) = 1.0015 |
| growth time (y0~2) | ~5e4 yr at k~1/kpc, ~5e3 yr at k~1/100pc — catastrophic |

## Why β,λ tuning cannot evade (the no-go core)
`c²_∥·A = (4−W2)/W2` is manifestly β,λ-free; the whole β,λ dependence is the positive scalar `A`.
So `sign c²_∥ = sign(4−W2)/sign(W2) = sign(W2) = sign(f'')`, and `f''<0` somewhere in (1,y*) is FORCED
by the boundary conditions (μ→0 deep-MOND, μ→1 Newtonian, + residual αa² high-a): f'' must dip
negative between the two positive ends. This is Flanagan's boundary-condition argument, here turned
from "might be unstable" (his β=λ=0 integral-balance caveat) into a definite LOCAL mode-by-mode
gradient instability, because the β,λ≠0 backbone makes the khronon genuinely propagate (finite A>0).
Higher-spatial-derivative L4/L6 (Hořava, M_*≳eV) only stabilize k≳M_*, leaving the entire a0≲k≲M_*
band unstable — a positive k⁴ cannot cure a k-independent B2<0.

## Convergence / robustness evidence
- **Two independent reductions** (Hermitian Schur-complement; EL-determinant −D0/D1) agree to
  rel.diff ≤1.5e-16 at all sampled points.
- **Exact closed form** — c²_∥(y0=2) flat & negative over **15 decades in k**; identical under
  y0-grid 1×/2×/4×/8×; unstable fraction of the window = 1.000 at every resolution.
- **Consistency limits**: pure-quadratic f=αa² ⇒ BB Eq.(14) exactly, m²=0; high-a ⇒ BB c_s²;
  c_T²=1/(1−β); deep-MOND stable; transverse always stable. Flat machinery matches BB Eq.(14) exactly.
- **Background occupies the window** (point mass 0.16<r/r_M<1.26; Plummer 0.1<r/b<8; inversion 1e-14).
- **Full 42-point (β,λ) scan**: min_y c²_∥<0 on every point.
- Concurrent independent write-up (`FC_KH_PAPER_vNEXT.md`, not produced by this run) reaches the same
  KILL with the same mechanism — external corroboration.

## What FC-KH passes (so the kill is INTERNAL, not observational)
GW170817 (c_T−1≈4e-16), solar-system α1 (=0 identically on α=2β), BB 1PN floor (β+λ≥2.5e-7 via λ),
G_N/G_C≈1. FC-KH was engineered to clear the c_T/α1 pincer that excluded the old α=½ model; it dies
instead on internal transition stability. The static background stays elliptic (ϖ'=1+(y−1)e^{−y}>0,
ELLIPTICITY_RESULT.md) — but that is the *background* operator; the *khronon perturbation* radial
stiffness is f''<0. Both statements are correct and compatible; the perturbation one is decisive.

## Scope / honesty
- Frozen-local principal-symbol reduction (leading order; background-gradient corrections
  O(1/kL_bg)≪1 do not affect the sign of the k² coefficient). A global inhomogeneous mode-solve on a
  full a(r) profile was not performed — unnecessary, since c²_∥ is a local function of y0 and every
  profile traverses the window, but it is the one computation that could be added for extra rigour.
- The super-horizon (k<a0) branch of the exact dispersion has a pole and opposite sign; it is outside
  frozen-background validity and physically irrelevant (a0≈1/Hubble). The physical (sub-horizon)
  band is unstable.
- KILL is scoped to FC-KH v1.0 as written (single khronon f_FC + K² backbone, μ=1−e^{−y}). It does
  NOT bear on other completion doors (bimetric, two-field, etc.).

## Artifact index
Derivations: `phase2_symbolic.py`, `decisive_reduction.py` (+`.out`,`decisive_symbols.pkl`),
`phase3_background.py`, `phase5_numeric_dispersion.py`, `phase6_scan.py`, `phase78_robustness.py`,
`phase10_constraints.py` (all with `.out`). Data: `PARAMETER_SCAN.csv/json`.
Docs: `CONVENTION_MAP.md`, `STABILITY_OPERATOR.md`, `RESULTS.md`, `PASS_KILL.md`, `CONVERGENCE.md`,
this `FINAL_REPORT.md`.
