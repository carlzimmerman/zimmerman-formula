# L51 — the second combination: the clock's operator freedom, priced

2026-09-09. Lane L51. Script: [`L51_second_combination.py`](L51_second_combination.py) →
[`L51_second_combination.out`](L51_second_combination.out). **36 checks, 25 PASS / 11 FAIL.** ⚠️*Corrected 2026-09-09: this line originally read "34 checks, 23 PASS / 11 FAIL", which undercounts its own output by two passes. Re-running the script reproduces the committed `.out` check-for-check (25 PASS, 11 FAIL, exit 0). The FAIL count was always right and no verdict moves; the error was conservative, understating the passes.*
Both a₀ footings (9.3619e-11 / 1.1279e-10 m s⁻²) on every dimensional number.

Method: nothing under `closure_2026/` or the lead agent's directories was imported, executed or copied.
The symbolic algebra — linearised curvature from a general symmetric perturbation, the transverse-operator
solve, the ADM identity for `R_μν n^μ n^ν` — was built from scratch in sympy here. The cluster and galaxy
data were read directly from the on-disk public archives (X-COP FITS, SPARC rotmod, Herbonnet 2020
Tables 2–3); L24's and L6's numbers are **re-derived as controls**, not imported.

---

## The verdict, first

**The freedom is real, it is not illusory in any of the three ways the brief named, it is already
half-spent — and it cannot be spent again, because the slip it produces cannot be switched on at clusters
without being switched on in galaxies.**

- It does **not** degenerate in the static limit (B1, B2).
- It does **not** have to cost a propagating mode (D1).
- It does **not** have to break the preferred-frame parameters or GW170817 (D2, D3).
- It **is** worth something: inside the lensing-versus-dynamics budget it would take the cluster shear
  shape from **8.8σ to 4.9σ** (canonical) / **9.0σ to 4.7σ** (alt) — a real dent in the one failure no
  mechanism has touched, and not a cure (C8).
- It **cannot be made scale-selective**. On the acceleration and on the baryon density, 100% of the
  cluster weak-lensing rows sit inside the SPARC range, and in the shared bins the required weight
  overshoots the deposited theory's own `Φ = Ψ` to 1e-4 by **3.2 × 10⁶** and a generous empirical
  galaxy-lensing tolerance of 20% by **1.6 × 10³** (C9–C11).

**One door is left open and is not argued shut.** The potential-depth trigger `Φ_loc = g_bar r` does
**not** overlap SPARC over 0.5–2 Mpc, so the overlap argument is vacuous for it. It is priced instead:
it needs a weight rising by 1.7 × 10⁵ across a factor **2.22** in the trigger, a logarithmic slope of
**16.0 / 6.5** (canonical, against the theory's own bound / against the 20% empirical bound). That is
steep, not excluded. Two objections, neither a proof: `g_bar r` is not a covariant local scalar, and the
covariant candidate this theory has — the clock's lapse — has its zero fixed cosmologically, so the slip
would depend on a cluster's environment rather than its own structure.

---

## 1. Controls (A1–A6, B3b, B7, C1, C2, C5, D1a, D1c, D2a)

| control | result |
|---|---|
| A1 linearised Ricci from first-order Christoffels of a general `h_μν` (10 functions of `t,x,y,z`) | identical to the closed form, all 16 components |
| A2 gauge invariance of `R^(1)_μν` about flat space for a general `ξ_μ` | exact |
| A3 static two-potential curvature from the **exact nonlinear** metric | `R^(1)_00 = ∇²Φ`, `R^(1) = 2∇²(2Ψ−Φ)`, `G^(1)_00 = 2∇²Ψ`, `G^(1)_12 = ∂₁∂₂(Ψ−Φ)` |
| A4 L39's locked ratio, in L39's own convention | `PsiL + 2 PhiL`, ratio **1 : 2** |
| A5 transverse symmetric operators | **1** with no preferred vector, **2** with one unit timelike `u` |
| C1 projection machinery vs analytic NFW | Σ to 1.2e-6, ΔΣ to 2.2e-6 |
| C2 L24's 9σ shear-shape failure, rebuilt from the FITS | **+0.516 ± 0.058 (8.8σ)** / **+0.521 ± 0.058 (9.0σ)** vs L24's +0.531/+0.536 |
| C5 measured cluster `g_lens/g_dyn` | **1.148 ± 0.146** vs L24's 1.154 ± 0.147 |
| D1a ADM identity `R_μν n^μ n^ν = θ² − K_μν K^μν − ∇·(θn) + ∇·a` | residual **0**, symbolically |
| D2a aether invariants for hypersurface-orthogonal `n` | `(∇_μn_ν)(∇^μn^ν) = K_μνK^μν − a²`, `(∇_μn_ν)(∇^νn^μ) = K_μνK^μν` |

`ds² = −(1+2Φ)dt² + (1−2Ψ)δ_ij dx^i dx^j` throughout: `Φ` dynamical, `Ψ` curvature, lensing potential
`(Φ+Ψ)/2`, slip `s = Φ − Ψ`, `γ_PPN = Ψ/Φ`.

## 2. Both combinations, exhibited

    S₁ = R^(1)                = 2 ∇²(2Ψ − Φ)     the ONLY combination a frame-free theory has
    S₂ = R^(1)_μν u^μ u^ν     = ∇²Φ              the one that needs the clock

The map `(Φ, Ψ) → (S₁, S₂)` is `[[−2, 4], [1, 0]]`, **determinant −4**. So `S₂ = ∇²Φ` **isolates the
Newtonian potential** and `(S₁ + 2S₂)/4 = ∇²Ψ` **isolates the curvature (lensing) potential** — neither
is reachable alone without `u`. The static transverse count is still 2 at `k·u = 0`, so nothing collapses
in the static limit.

## 3. What a term built from each one does to the slip

Take `ΔS = ∫[w₁S₁[h] + w₂S₂[h]]` — the linearisation of an arbitrary `F(S₁,S₂)`, local or nonlocal
(a nonlocal `B(□)` only renames the weight). Varying with the Euler–Lagrange operator on the ten
independent components of a general static `h_μν`:

| | `δ/δh₀₀` | `δ/δh₁₁` | `δ/δh₁₂` (traceless ij) |
|---|---|---|---|
| frame-free `w₁S₁` | `∇²w₁` | `−(∂²_y+∂²_z)w₁` | `2∂_x∂_y w₁` — **nonzero** |
| u-built `w₂S₂` | `−∇²w₂/2` | **0** | **0** |

So the **second combination by itself does not change the slip at all** — statically it sources only the
00 equation. What it changes is the *lensing*. Writing the modified static system with undetermined
coupling constants and eliminating:

    (00)  2∇²Ψ = 8πGρ − c ∇²w₁ + e ∇²w₂
    (ij)  Ψ − Φ = − c w₁

    =>    ∇²(Φ + Ψ) = 8πGρ + e ∇²w₂        and       slip = − c w₁

**This sharpens L39's lock.** L39 states it as a fixed 1 : 2 ratio between the 00 and ij sources. Its
physical content is stronger and needs no normalisation at all: **for any frame-free covariant addition
and any weight, `∇²(Φ+Ψ) = 8πGρ` exactly** — the lensing potential is welded to the baryons and no
frame-free term, local or nonlocal, can move it. That is the exact quantitative form of Soussa–Woodard's
"far too little lensing" and of the conformal-invariance argument, and it covers the nonlocal case in one
line because `□⁻¹` only renames the weight.

And then, symmetrically: **the lensing potential is moved ONLY by the u-built piece and the slip ONLY by
the frame-free piece.** The slip is not a differential response to a weight — it *is* the weight,
algebraically. That is what makes the empirical part below so sharp.

**The lever.** Writing the added lensing potential as `P` and the slip as `s`, the added dynamical
potential is `P + s/2`. Frame-free (`P = 0`) the lever `d(lensing)/d(dynamics)` is **pinned at zero**;
with the clock it is free. Moving lensing with the dynamics *exactly unchanged* requires **`s = −2P`**.

**And the programme has already spent this freedom once.** The deposited action's AeST coupling
`2(2−K_B) J^μ ∂_μφ`, with `J^μ = n^ν∇_ν n^μ`, has exactly the same static variation as `∫w S₂` — 00-only,
ratio **−1** — because `∇_μ a^μ = R_μν n^μn^ν` at linear order about a static background. That is *why*
the theory delivers Milgrom's equation in the 00 equation with `Φ = Ψ` and no slip: it is the `w₁ = 0`
corner of the structure above. What has never been used is the **frame-free partner** that would make the
slip nonzero. **The lensing sector of this programme rides entirely on the clock; the dynamical sector
never needed it.**

## 4. Pointed at the cluster shear shape (a)

`ρ_P = ρ_lensing(measured NFW) − ρ_framework`, with dynamics held exactly fixed by `s = −2P`. Projection
is linear so `ΔΣ = (1−f)ΔΣ_fw + f ΔΣ_WL` exactly.

| | canonical | alt |
|---|---|---|
| median required `M_P(<R500)/M_fw(<R500)` | **0.806** | **0.669** |
| median required `\|slip\|` at R500 | **1.57e-5** | **1.13e-5** |
| as a fraction of the framework's own lensing potential | **0.31** | **0.20** |

A profile exists (C3 PASS) and it is unique. But it is **not a small perturbation** (C4 FAIL): the
required slip is a third of the potential itself.

## 5. Priced against what must not move (b)

`M_HSE` and `M_WL` are not two masses; they are measurements of two accelerations, so their ratio is a
direct measurement of the cluster slip. Measured here: **1.148 ± 0.146**. The deposited theory predicts
**1.000** (no slip), which is 1.0σ away — one of its quiet successes. Buying the whole shape makes the
prediction **1.806 (4.5σ)** canonical / **1.669 (3.6σ)** alt. **C6 FAILS: the full shape fix breaks the
agreement it was supposed to preserve.**

Inside the 3σ budget on that ratio the added lensing phantom is capped at `f ≤ 0.73` / `0.88`, and the
residual shape error is **+0.073 ± 0.015 (4.9σ)** / **+0.036 ± 0.008 (4.7σ)**, from 8.8σ / 9.0σ. So the
freedom is worth roughly **halving the 9σ**, and no more. C8 FAILS, and the FAIL is the honest ceiling.

## 6. THE CRUX — scale selectivity (C9–C13)

Because the slip *is* the weight, a galaxy point at the same trigger value gets the **same dimensionless
slip** as a cluster point — and a galaxy's entire potential is four to five orders of magnitude shallower.

| trigger | overlap with SPARC over 0.5–2 Mpc | worst induced galaxy slip | vs theory's 1e-4 | vs 20% empirical |
|---|---|---|---|---|
| `g_bar` (the theory's own `J(Y)` argument) | **100%** of cluster rows inside | **325 ×** the galaxy's own potential | **3.2e6 ×** | **1.6e3 ×** |
| `ρ_b` | **100%** inside | **122 ×** | **1.2e6 ×** | **6.1e2 ×** |
| `Φ_loc = g_bar r` | **none** — clusters 1.87–4.67e11, SPARC ≤ 8.42e10 m²s⁻² | — | **not tested** | **not tested** |

**C9 (the crux) FAILS on the acceleration**, which is the trigger this theory actually has: its `J(Y)` is
a function of the MOND scalar's spatial gradient, i.e. of the acceleration.

**What is NOT closed.** The potential-depth trigger survives the overlap argument, and this lane says so.
Priced (C12b): the trigger rises by only **2.22×** from the deepest SPARC point to the shallowest cluster
weak-lensing point, while `W` must rise from ≤ 7.8e-11 (theory) or ≤ 1.6e-7 (data) to 2.7e-5 — a
logarithmic slope of **16.0 / 6.5** canonical, **15.8 / 6.2** alt, against ~1–3 for chameleon/symmetron
screening. Steep, not excluded.

**And the internal test that might have shut it is not usable.** The cluster-to-cluster scatter of the
required weight at fixed trigger is 0.91–1.25 dex against a "single-valued" requirement of ≲0.15 dex
(C13a FAIL) — but the propagated fractional error from Herbonnet's own 21–63% `M500` errors is **1.4**,
and at order unity the log-scatter is unbounded below. **C13b FAILS as a control: C13a is noise-limited
with five clusters and MUST NOT be quoted as a kill.** The crux stays C9–C11, which never uses the
cluster-to-cluster scatter.

## 7. The galaxy-pair scale (c)

**No.** B6 settles it structurally: a frame-free term already moves the dynamical potential by `s/2`, so
the clock's extra combination buys nothing in the dynamical sector — and binary galaxies fail in
*dynamics* (L21: `A = 1.74 ± 0.06`). The new freedom is confined to the lensing sector, and the
dynamical door is the frame-free kernel door that L2/L6 already closed. The acceleration ranges also
overlap (clusters 0.046–0.207 a₀ over 0.5–2 Mpc; pairs 1e-4 to 1e-1 a₀), so even an
acceleration-triggered weight could not separate them.

## 8. The prices, each one checkable

**Modes (D1).** `R_μν n^μn^ν = θ² − K_μνK^μν − ∇·(θn) + ∇·a`, verified symbolically. The only
second-time-derivative content sits in the total divergence, so a term **linear** in `S₂` integrates by
parts to something first order in the extrinsic curvature — second-order field equations, **no new mode**,
and if the weight is the MOND scalar the theory already carries, nothing is added at all. A term
**nonlinear** in `S₂` keeps `(n·∇θ)²` and is Ostrogradsky (D1c, the control). This is exactly why the
admissible realisation is the AeST form the theory already uses.

**GW170817 (D2).** The K-quadratic part of a weighted `R_μν n^μn^ν` shifts `c₁₃` by `−w`, and the
deposited theory sets `c₁₃ = 0` *identically* so that `c_T = c` structurally. That would demand
`|w| < 2e-15` in the intergalactic propagation background. **A safe realisation exists**: `∫a·∇w` (the
AeST coupling) has no K-quadratic part at all and leaves `c₁₃ = 0` exactly. So GW170817 is not a
structural obstruction — but it does say which realisation is admissible.

**PPN (D3).** `γ − 1 = −s/Φ`. At the Cassini tracking geometry `Φ = 1.04e-9`, so `|s| < 2.39e-14` —
against `1.57e-5` at clusters, a contrast of `6.6e8` (canonical) / `4.7e8` (alt). But `g/a₀` at Saturn is
`7.0e5` against `0.046–0.207` in the cluster lensing range, so any monotone weight clears Cassini.
**Cassini is not the binding constraint; galaxies are.** `α₁ = −4c₁₄` and `α₂ = −0.2023 c₁₄` are untouched
in form by the acceleration realisation, which is linear in `a` and cannot renormalise `c₁₄`.

---

## 9. The PASS/FAIL lines

```
[PASS] A1 [control] the linearised Ricci machinery built here reproduces the standard expression for a general h_mn
[PASS] A2 [control] R^(1)_mn is invariant under h -> h + d_m xi_n + d_n xi_m
[PASS] A3 [control] the static two-potential curvature: R^(1)_00 = lap Phi, R^(1) = 2 lap(2 Psi - Phi), G^(1)_00 = 2 lap Psi, G^(1)_12 = d_1 d_2 (Psi - Phi)
[PASS] A4 [control] L39's locked ratio is reproduced: the frame-free scalar carries PsiL + 2 PhiL, ratio 1 : 2
[PASS] A5 [control] with no preferred background vector there is exactly ONE transverse symmetric operator; adjoining one unit timelike vector makes it TWO
[PASS] A6 [control] both static solutions are transverse and linearly independent
[PASS] B1 [test] is the second combination genuinely INDEPENDENT of the first in the STATIC weak field?      (det -4)
[PASS] B2 [test] the second combination does NOT reduce to the first in the static limit
[PASS] B3a [test] a term built from the SECOND combination alone sources ONLY the 00 equation statically, so BY ITSELF it does not change the slip
[PASS] B3b [control] the FRAME-FREE term sources both the 00 equation and the traceless ij equation
[PASS] B4 [test] THE FRAME-FREE LOCK, sharpened: lap(Phi + Psi) = 8 pi G rho EXACTLY
[PASS] B5 [test] with one unit timelike vector the 00 source and the slip become INDEPENDENT
[PASS] B6 [test] THE LEVER: frame-free it is pinned at zero, with the clock it is a free function
[PASS] B7 [control] the deposited theory's AeST coupling J^mu d_mu phi IS the second combination      (ratio -1, 00-only)
[PASS] C1 [control] the projection machinery reproduces the analytic NFW Sigma and DeltaSigma to 0.5%
[PASS] C2 [control] the 9-sigma cluster shear-shape failure is reproduced independently      (+0.516 +/- 0.058 / +0.521 +/- 0.058)
[PASS] C3 [test] a slip profile exists that reproduces the measured DeltaSigma shape with the dynamics exactly unchanged
[FAIL] C4 [test] the required slip at cluster radii is a SMALL perturbation (< 10% of the potential)      (0.31 / 0.20)
[PASS] C5 [control] the measured cluster lensing/dynamical ratio is reproduced      (1.148 +/- 0.146)
[FAIL] C6 [test] buying the cluster shear shape PRESERVES the lensing-versus-dynamics agreement      (4.5 / 3.6 sigma)
[FAIL] C8 [test] inside the 3-sigma lensing/dynamics budget the freedom removes the shape failure      (8.8 -> 4.9, 9.0 -> 4.7 sigma)
[FAIL] C9 [CRUX] the required weight can act at cluster accelerations WITHOUT acting at galaxy accelerations      (3.2e+06 x)
[FAIL] C10 [test] the required weight preserves the deposited theory's no-slip result Phi = Psi to 1e-4 in galaxies      (g_bar 3.2e+06 x, rho_b 1.2e+06 x, Phi_loc NOT TESTED)
[FAIL] C11 [test] it survives even a generous EMPIRICAL galaxy-lensing tolerance of 20% fractional slip      (1.6e+03 x, 6.1e+02 x)
[FAIL] C12b [test] the surviving (potential-depth) trigger needs only a moderate weight, logarithmic slope under 4      (16.0 / 6.5, 15.8 / 6.2)
[FAIL] C13a [test] the required weight is single-valued across the five clusters at fixed trigger      (0.91-1.25 dex; SEE C13b)
[FAIL] C13b [control] the observed scatter is separable from the published weak-lensing mass errors      (fractional error 1.41 -- C13a is NOISE-LIMITED and must not be quoted)
[FAIL] C14 [test] the second combination reaches the galaxy-pair failure
[PASS] D1a [control] the ADM identity R_mn n^m n^n = theta^2 - K_mn K^mn - div(theta n) + div(a)      (residual 0)
[PASS] D1b [test] a term LINEAR in the second combination adds no propagating mode
[PASS] D1c [control] a term NONLINEAR in the second combination DOES add one
[PASS] D2a [control] the aether invariants reduce to K_mn K^mn, theta^2 and a^2, with c_13 = c_1 + c_3
[PASS] D2b [test] a c_13-safe realisation of the second combination exists      (the acceleration form)
[PASS] D3a [test] the Cassini gamma bound is compatible with the required cluster slip
[PASS] D3b [test] the preferred-frame parameters alpha_1, alpha_2 are preserved in form
[FAIL] E1 [VERDICT] the second combination is a USABLE new handle on the cluster shear shape
```

---

## 10. What this changes in the standing record

1. **L39's lensing lock should be quoted in its stronger form.** Not "a locked 1 : 2 ratio" but
   **`∇²(Φ+Ψ) = 8πGρ` exactly, for every frame-free weight and every coupling constant.** The
   normalisation-free version is what makes it a statement about the class rather than about a
   coefficient, and it is what makes the corollary sharp: the lensing sector rides entirely on the clock.
2. **L24's statement "a slip changes lensing and leaves dynamics alone" is not right as written**, and
   correcting it strengthens L24's conclusion rather than weakening it. A slip alone moves the *dynamical*
   potential by `s` and the lensing potential by `s/2`; the "lensing moved, dynamics untouched"
   configuration needs the frame-free and the u-built operators **together**, tuned to `s = −2P`. L24's
   door is still shut — just for a slightly different reason than the one recorded.
3. **The deposited theory's `Φ = Ψ` is not an accident and not a fit.** It is the `w₁ = 0` corner of a
   two-operator structure, and the theory sits there because it uses the AeST coupling and nothing else.
   Recording it as "met structurally rather than fitted" is correct, and this lane says exactly which
   structure.
4. **The theory's `g_lens/g_dyn = 1.000` is a real, quiet prediction that currently agrees at 1.0σ**
   (measured 1.148 ± 0.146). It is worth quoting, and it is what the cluster shear-shape repair would
   spend.
5. **Do not quote the cluster-to-cluster scatter of a required weight as a kill on five clusters.** C13b
   is the control that says so, on this repository's own data.
6. **One door is added to the open list, not removed**: a potential-depth-triggered slip, needing a
   logarithmic slope of 6–16 and carrying a covariance objection. Deciding it needs either a covariant
   local scalar that separates cluster outskirts from galaxy outskirts, or a galaxy-galaxy-lensing slip
   measurement at `Φ_loc ≳ 1e11 m² s⁻²` — i.e. around groups and brightest cluster galaxies, which is
   precisely the regime the programme's group/cluster contrast is already estimator-limited in.
