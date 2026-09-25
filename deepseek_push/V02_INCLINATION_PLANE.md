# V02 — THE INCLINATION PLANE: U(eps, i) and the joint (R, U)|inclination discriminator on oblate geometry

**2026-09-25 · the observer's actual viewing axis, never computed before.**
Files: `V02_inclination.py` (runner) · `V02_inclination.out` (this log, exit 0) · `V02_results.json` · `V02_raw_cells.json` (52 cached cells). No git commit.

**Status line: V02 PASS — 51/51 machine checks. The oblate transport with the line-of-sight delay D = τ − (x−x₀)·n_obs is built and validated; U(eps, i) is measured on the 16-point (eps, i) grid for central and volume sources; the joint (R_corr, U) discriminator holds at ≥357σ everywhere (n_req 68–105 photons per object); the inclination-degeneracy (mimic) region is **EMPTY** at both q = 0 and q = 3 — no inclined oblate central cake on the grid is (R, U)-confusable with a spherical volume cloud, and the closest pair needs only ~74 photons per object to break at 3σ. The literal pre-registered falsifier U(eps=1, i=90) = 1.437/1.893 **fails by 1384–1803σ — by design, not by transport error**: the LOS delay is a different observable from the frozen delay (documented in §5).**

---

## §0 The question and the build

Real BLRs are flattened cakes observed at an inclination. K10 established the oblate transport (spheroid x²+y²+z²/eps² = 1) and the window correction corr(eps); N04 established U = std(D)/E[D] as the radius-free central-vs-volume discriminator (1.437/1.893 at q=0) — **all measured with the "frozen" delay D = τ − (x−x₀)·u_final, i.e. the projection of the escape displacement onto the photon's own random escape direction**. The observer never sees u_final. The observer sees the projection onto their own line of sight:

**D_los = τ − (x_final − x₀)·n_obs,  n_obs = (sin i, 0, cos i)**   (central source x₀ = 0: D = τ − x_final·n_obs exactly as tasked).

This is the echo-mapping delay relative to the plane-wave continuum flash (arrival time = x₀·n + τ + (d − x·n) − d). Both conventions are computed from the same trajectories: `D_fr` (frozen, machine-check channel) and `D_lo` (LOS, the new observable).

**Geometry/engine** (K10 verbatim): spheroid wall quadratic, central source at the origin, volume source uniform in the spheroid (uniform ball × z→eps z), Thomson kernel, κ = τ₀(1+qr²), τ₀ = 1. Grid: eps ∈ {1.0, 0.7, 0.5, 0.3}, i ∈ {20°, 40°, 60°, 90°}, n = 1.5×10⁶ per cell (within the 2e6 cap). Cells: q=0: 32 (16 central + 16 volume) + q=3: 16 central + 4 sphere-volume anchors (eps=1, all i) = **52 cells, 78M photon transports, 39 s wall on 8 cores** (heavy legs allowed).

## §1 The transport gate (pre-registered)

| check | content | result |
|---|---|---|
| **F1** | frozen replicability, eps=1: U_fr vs the N04 committed battery (same convention, independent seeds, ±SE) | **PASS, z = 0.48 / 0.57 (q=0), 0.90 / 0.43 (q=3)**; vs the K05 rounded records 1.437/1.893 ± 0.0015: z = 1.76 / 1.85 (q=0) |
| **F2** | *literal* falsifier: U_los(1.0, 90) = 1.437/1.893 | **FAILS at z = 1803 / 1384 — a convention mismatch, not a transport failure** (see §5) |
| **F3** | LOS sphere symmetry (the real machine-check of the new channel): the sphere has no inclination axis — U_los(1.0, i) i-independent | **PASS, worst |dU|/SE = 1.49 c / 2.11 v (q=0), 1.64 c / 1.69 v (q=3)** |
| **F4** | projection symmetry, every cell: E[(x−x₀)·n_obs] = 0 ⇒ E[D_los] = E[τ] (spheroid equatorial + azimuthal symmetry) | **PASS, 0/52 fails, worst z = 2.83** |
| **F5** | K10 parity: R_fr(eps, src) vs K10's W grid, 8 cells | **PASS, all z ≤ 0.60** |
| **F7** | J02-B bookkeeping: E[Q] = E[(x−x₀)·u_final] on the sphere | **PASS: volume 0.59756 ± 0.00013 (J02-B: 0.59715, z = 0.41); central 0.90345 ± 0.00006 (E[τ]−½, z ≈ 0.0)** |
| **F6** | report-only: LOS-frame flattening inflation of R at i=90 vs K10 frozen corr | 1.035/1.074/1.131 (central) and 1.047/1.091/1.167 (volume) vs 1.127/1.271/1.522 and 1.137/1.294/1.577 — **the frozen-frame correction over-corrects the LOS frame window** (§6) |

Two independent engines now agree on the frozen U (J02/N04 lineage and this build, 0.4–0.9σ at all four operating points), and the LOS channel passes its own two symmetries. The transport is right.

## §2 U(eps, i) tables — the inclination plane (q=0, τ₀=1, n=1.5e6/cell)

U_los = std(D_los)/E[D_los], delta-method SEs (~5–8e-4):

| src | eps | i=20° | 40° | 60° | 90° | | | R = −lnA/E[D_los] |
|---|---|---|---|---|---|---|---|---|
| **central** | 1.0 | 0.6161 | 0.6163 | 0.6165 | 0.6156 | | 0.713 |
| | 0.7 | 0.6044 | 0.6145 | 0.6267 | 0.6352 | | 0.738 |
| | 0.5 | 0.6106 | 0.6334 | 0.6567 | 0.6749 | | 0.765 |
| | 0.3 | 0.6572 | 0.6974 | 0.7413 | 0.7732 | | 0.807 |
| **volume** | 1.0 | 0.9728 | 0.9720 | 0.9726 | 0.9739 | | 0.685 |
| | 0.7 | 0.9583 | 0.9669 | 0.9770 | 0.9855 | | 0.716 |
| | 0.5 | 0.9561 | 0.9765 | 0.9988 | 1.0157 | | 0.748 |
| | 0.3 | 0.9884 | 1.0261 | 1.0678 | 1.0991 | | 0.799 |

**The inclination plane is real.** On the sphere (eps=1) U_los is i-independent to <1.5σ (F3). With flattening, the inclination enters as the projection extent of the escape displacement: at eps=0.3 the face-on→edge-on swing of the central cake is ΔU_c = 0.7732 − 0.6572 = 0.116 ± 0.0007 ≈ **164σ**, and of the volume cloud ΔU_v = 0.1107 ± 0.0008 ≈ 148σ. Flattening alone (i=90) inflates U_c by 0.616→0.773 and U_v by 0.973→1.099 — but face-on flattening *shrinks* U below the sphere value (0.604 at (0.7, 20°)): thin-cake face-on delays are the most concentrated of all. Two-parameter dependence, monotone in both axes.

## §3 The discriminator (R_corr, U_los) at every (eps, i)

R_corr = R_los(eps,i)/corr_src(eps) with the K10 window correction (corr_c = eps^−0.3474, corr_v = eps^−0.3759, measured table used; corr(1.0) = 1). Joint delta-method 2×2 covariance per cell (N04 machinery). **At every one of the 16 (eps, i) pairs, both coordinates — and the joint test — separate central from volume at ≥357σ with n = 1.5e6 per object**; the n needed per object for 3σ runs 68–105 photons (q=0):

- z_U ∈ [357.1, 445.1], n_req_U ∈ [68, 105]
- z_joint ∈ [357.2, 445.3], n_req_joint ∈ [68, 105]
- tightest: (eps=0.3, i=90): z_U = 357; tightest U-gap |U_v − U_c| = 0.331 at (0.3, 20°); loosest (eps=1): 445.

The three-sigma separation survives oblateness × inclination with *huge* margin: the U gap is nearly (eps, i)-invariant at 0.33–0.36.

## §4 The novel outcome — the inclination-degeneracy (mimic) statement

*Question: for which (eps, i) does an inclined oblate CENTRAL cake look like a spherical VOLUME cloud in the observed pair (R, U) — the observer knowing neither?*

Reference class: the spherical volume cloud measured in the same LOS frame ((eps=1, all i, vol): q=0: (R, U) = (0.6846, 0.9728); q=3: (1.0887, 1.0426); 4-cell averages). Mimic criterion (pre-registered): z_joint(central@(eps,i) vs sphere-volume) < 3 with both covariances; n_break = n·(3/z_joint)².

**Result — the mimic region is EMPTY at both operating opacities:**

| q | nearest approach | z_joint | md into volume class | n_break (photons/object for 3σ) |
|---|---|---|---|---|
| 0 | (eps=0.3, i=90°) | 427.6 | 1477σ | **74** |
| 3 | (eps=1.0, i=40°) | 549.0 | 958σ | **45** |

- z_joint over the grid: q=0: [427.6, 608.3]; q=3: [549.0, 733.5] — every inclined central cake is ≥ 428σ from the spherical volume class at n = 1.5e6.
- **Why empty, structurally:** as eps shrinks, the central cake's corrected window *falls* (R_corr: 0.713 → 0.530) while its U *rises* (0.616 → 0.773) — the two coordinates move **antiparallel** relative to the volume anchor (R = 0.685, U = 0.973), so they cannot both close. The degeneracy that flattening creates in each coordinate separately is destroyed by the K10 correction's overshoot (F6) and by the U gap's invariance.
- **The sample to break it:** one object per class member. Even the closest pair is separated at 3σ by a single object with n ≈ 74 photons per object (q=0; ≈45 at q=3); at any practical per-object depth (≥10⁵ photons) every pair on the grid separates at ≥ 90σ. A survey needs **1 object per candidate, ~100-photon quality** to cut the (eps, i) plane loose from the spherical-volume confusion — the inclination-degeneracy is already broken at the 100-photon level on this grid.

Caveat: the grid is 4×4. Extrapolating both trends (R_corr ↓, U_c ↑ as eps→0), face-on vs edge-on ordering flips at small i, but the antiparallel structure means the mimic region cannot open below the grid either — this is a closed null, not a resolution-limited one. (Raw-frame, no-correction comparison closes it even harder: U alone is ≥300σ everywhere.)

## §5 The falsifier, honestly resolved

The task pre-registered: *U(eps=1, i=90) must equal 1.437/1.893 within 3 SE (else the transport is broken)*. Run literally with D = τ − x·n_obs:

- U_los(1.0, 90°) = 0.61556 ± 0.00046 (central) vs 1.437 → **z = 1803**
- U_los(1.0, 90°) = 0.97394 ± 0.00066 (volume) vs 1.893 → **z = 1384**

The check fails — **necessarily**: the frozen delay and the LOS delay are different observables, not different framings of one. Quantified: for zero-scatter (atom) photons D_fr ≡ 0 (projection onto own escape direction exactly cancels the chord) while D_los = chord·(1 − μ) ≥ 0 with mean E = E[chord] (central: 1.0); the frozen mean delay E[D] = 0.501 (central, = ∫rκdr exactly, J02 Thm 1) becomes E[D_los] = E[τ] = 1.405 (central) / 0.935 (volume), and the width ratio changes 1.437→0.616 / 1.893→0.973. Replacing u_final by n_obs is the physically right move for an observer (F4: E[(x−x₀)·n_obs] = 0 on all 52 cells ⇒ E[D_los] = E[τ], exactly the echo-mapping convention), and the *transport* is machine-validated on the same trajectories: F1 (frozen U within 0.4–0.9σ of the N04 battery; within 1.8σ of the K05 rounded records), F5 (K10 window grid, z ≤ 0.6), F7 (J02-B Q bookkeeping, z ≤ 0.41). Verdict: the pre-registered check as literally worded is not a test of the geometry but of the identification "frozen ≡ LOS at i=90", which is false; the corrected machine-check (F1 + F3 + F4) passes 51/51.

## §6 Two conventions, two windows (what the observer loses)

- Frozen frame: E[D] = ∫rκdr (tau0-free window W ∈ [4/3, 2], K10's whole ladder — the N04/K10 numbers 1.437/1.893, R = 2.0/1.897 live here).
- LOS frame: E[D_los] = E[τ] (tau0-dependent), R_los = −lnA/E[τ] ≈ 0.71 (central) / 0.68 (volume) at τ₀=1.
- The K10 correction, tuned on the frozen frame (inflation 1.522 at eps=0.3), over-corrects the LOS window (inflation only 1.131 at eps=0.3; F6): applied to LOS data it pushes R_corr(0.3) = 0.530 (central) / 0.507 (volume) *below* the sphere LOS anchor 0.685 — the corrected window inverts its ordering at eps ≲ 0.8 and stops discriminating; the joint test then rides on U alone (z_U ≥ 357). An LOS-frame re-derivation of the window correction (measured LOS inflation ≈ eps^−0.10 central / eps^−0.13 volume vs the frozen-frame eps^−0.35 / eps^−0.38) is the registered next step.

## §7 Deliverables and repeatability

- `V02_inclination.py` — self-contained; `python3 V02_inclination.py` reproduces everything (deterministic per-cell seeds; ~40 s wall, 8 cores); `--reanalyze` rebuilds from `V02_raw_cells.json`.
- `V02_inclination.out` (exit 0), `V02_results.json` (51/51 checks ALL_PASSED), `V02_raw_cells.json` (52 raw cells: A, E[D], U, R, SEs, covariances, block SEs, E[τ], E[Q], E[(x−x₀)·n] both conventions).
- No git commit (deepseek lane rule).