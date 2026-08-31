# RESULTS.md — FC-KH v1.0 terminal falsification

Start commit `750805926eaaa1b0207e3b354d76b12deefcc1cf`. No git state altered. All artifacts are
untracked plain files in this directory.

## VERDICT: **GLOBAL STABILITY — KILL**  (failure class A: structural)

FC-KH v1.0 (`α=2β`, β>0, λ>0 branch) has an **unavoidable radial (parallel) gradient
instability of the khronon scalar throughout the MOND→Newtonian transition** `1 < a/a0 < y*`
(`y*≈31–45`). The K²(β,λ) khronometric backbone removes the ghost (kinetic A>0) and rescales
the instability's magnitude, but **cannot flip its sign**, which is locked to sign(f'').

## The decisive numbers (deep sub-horizon, physical band a0≪k≪M_*)
Reduced khronon dispersion `ω² = V(k)/A` after eliminating lapse φ and shift B:
```
A          = (1−β)(2+β+3λ)/(β+λ)                     > 0     (kinetic; no ghost)
c²_perp    = (4y0−W1)(β+λ)/[W1(1−β)(2+β+3λ)]         > 0 ∀y0 (transverse; safe)
c²_par     = (4−W2)(β+λ)/[W2(1−β)(2+β+3λ)],   W2=f''(y0)
             sign(c²_par) = sign(f'')  — β,λ-independent  ⇒  c²_par < 0 for 1<y0<y*
```
`f''(y) = 2α + 2(2−α)(1−y)e^{−y}`.

## Worst transition point (benchmark P1: α=2e-15, β=1e-15, λ=1e-3)
| quantity | value |
|---|---|
| kinetic eigenvalue A | +2.003e3 (>0) |
| c²_par at y0=2 (radial) | **−4.19e-3** (UNSTABLE), k-independent over 4 decades (k=1e2…1e6 a0) |
| c²_perp at y0=2 (tangential) | +3.19e-3 (>0) |
| divergent-worst c²_par | → −∞ at window edges y0→1⁺ and y0→y*⁻ (W2→0⁻; strong coupling) |
| tensor speed c_T² | 1/(1−β)=1+1e-15 |
| scalar high-a speed c_s² | (β+λ)/[β(2+β+3λ)] ≈ 5e11 (BB α→0 strong coupling, positive) |
| growth time (y0~2, k~1/kpc) | ~5e4 yr ; (k~1/100pc) ~5e3 yr — catastrophic |
| G_N/G_C = (2+β+3λ)/(2−α) | 1.0015 |

## Unavoidability (Phase 6, 42 grid points, PARAMETER_SCAN.csv/json)
`min_y c²_par < 0` on **every** (β,λ) in {1e-18…1e-12}×{1e-7…1e-1}, α=2β. Analytic reason:
`(4−W2)>0` (W2≤4) and `(β+λ)/[(1−β)(2+β+3λ)]>0` for all β,λ>0, so `sign(c²_par)=sign(f'')`
regardless of the parameters. The backbone sets the *magnitude* (∝(β+λ)/[(1−β)(2+β+3λ)]) but
never the *sign*.

## Two independent derivations agree (machine precision)
- Route I: Hermitian Schur-complement reduction, `(1−β)` convention (this run, `decisive_reduction.py`).
- Route II: EL-determinant `ω²=−D0/D1` from the pre-existing `wf_adm_scalar_reduction.py`
  (`adm_mond.pkl`), with `β_script=−β`. Reproduces ω²(kx,kz) to rel.diff ≤1.5e-16 at all
  sampled points (`phase5_numeric_dispersion.out`).

## Consistency checks the symbol passes (guards against a false kill)
- Pure-quadratic f=αa² ⇒ c²_par=c²_perp=**BB Eq.(14)** exactly, y0-independent, m²=0.
- High-a limit ⇒ BB c_s²; c_T²=1/(1−β). (decisive_reduction.out)
- Transverse mode c²_perp>0 ∀y0 (matches f'/a>0 prediction), i.e. only the radial direction is dangerous.
- Flat-space machinery matches BB Eq.(14) exactly (`../khronometric_mond/wf_flat_validation.py`).

## Background occupies the unstable window (Phase 3, phase3_background.out)
Static spherical (K_ij=0 ⇒ β,λ absent) modified-Poisson `μ_phys(a/a0)·a=g_N`, μ_phys=1−e^{−y}:
- Point mass: unstable shell 1<y0<38 spans **0.16 < r/r_M < 1.26** (r_M=√(GM/a0)).
- Plummer sphere: spans **0.1 < r/b < 8**.
Inversion converged (residual 1e-14). Every realistic source carries a finite unstable shell at
its MOND radius.

## Observational gates (Phase 10, phase10_constraints.out) — ALL PASS at P1
c_T−1=+4.4e-16 (GW170817 ✓), α1_PPN=0 identically (α=2β ✓), β+λ=1e-3 > 2.5e-7 (BB 1PN floor ✓),
G_N/G_C≈1.0015. So the failure is **not** observational — FC-KH was engineered to clear the
c_T/α1 pincer that killed the old α=½ model. It dies on internal transition stability instead.

## Relation to Flanagan (Phase 13)
Flanagan (BM, β=λ=0) showed f''≤0 must fail near a~a0 but that this "does not imply instability"
(footnote 7) and can be cured by higher spatial derivatives. **FC-KH does NOT escape:** turning on
the β,λ backbone makes the khronon genuinely propagating (finite A>0) and turns Flanagan's
"might be unstable" into a definite, local, mode-by-mode radial gradient instability whose sign is
pinned to f''<0 and is untouched by β,λ. Higher-derivative L4/L6 (scale M_*≳eV) regulate only
k≳M_*, leaving the whole a0≲k≲M_* band unstable — a positive k⁴ cannot cure a genuine B2<0.
