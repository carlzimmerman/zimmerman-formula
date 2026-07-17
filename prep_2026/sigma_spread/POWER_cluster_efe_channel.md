# LANE P — Power analysis: MI relational σ-spread vs the MG exact zero (2026-07-16)

**Script:** `power_analysis.py` (+ `.out`, exit 0). Estimator + cuts FROZEN in the file header
before any real-data read; the estimator is never fired on real σ-vs-infall data here (specs only).
Companions: `rederive_mi_spread.py` (prediction re-derived from the framework's own premises),
`estimator_power.py` (analytic), `census_verify.py` (catalog census), `RECON.md`.

## What was Monte-Carlo'd

The frozen estimator (pooled cluster-centered OLS slope of the FJ residual d_i = ln σ_i −
⟨ln σ|M*,R_e⟩ on the standardized PPS infall proxy p_i, outer R500–R200 shell, DS-substructure cut,
one-sided 3σ, MG-truth + shuffle null) on synthetic clusters built from the **real touched catalog
specs**: Gannon+2024 carrier error distribution (median 24%, resampled row-by-row), HeCS-omnibus
cluster structure (227 clusters, median 180 members, σ_cl 686 km/s), HeCS e_cz = 36 km/s (proxy
measurement noise 5% of σ_cl → negligible; D is projection-limited), GalWCat19 measured outer-shell
fraction 0.40, Sohn+2017 A2029 for the dE backdoor. Signal injected from the framework's own
R(y) shape (ν(y)=√(1+1/y), μ_fw its exact inverse, fiducial Milgrom-2022 kernel), **both footings**:
canonical a0=9.36e-11 at f = 6% and 13% (tasked band), alternate a0=1.13e-10 at f = 7.6% and 14.4%
(banked alt band ends). MG runs: f ≡ 0 (the symbolic theorem, any a0/interpolation).

**Calibration (all asserted):** MG-truth null is exactly standard normal (20k trials: mean −0.008,
sd 1.002, P(z≥3)=0.0012); √N scaling holds (1.98 vs 2.00); the 90%-power normal approximation
verified empirically (0.91 at predicted N_90).

## Honest-floor findings (both ways, load-bearing)

1. **The astrophysical scatter floor was measured, not assumed:** residual of ln σ on (ln M*, ln R_e)
   in the actual in-hand carrier catalog (Gannon+2024, 24 objects), measurement variance subtracted,
   gives **s_FJ = 0.48 ln (0.21 dex) — ×3.2 the banked 0.15 floor**. Caveats both ways: 24
   heterogeneous objects (assumed distances, mixed instruments/apertures/environments), and if MI is
   true part of that scatter *is* signal — so using it as pure noise is conservative. Scenario grid
   carries {0.48 measured, 0.15 banked, 0.08 tight-control}.
2. **The banked analytic two-bin was ×1.43 optimistic** even at matched assumptions: it placed the
   bins at the y-window endpoints; real settled/plunger class means sit inside the window (usable
   contrast ~85% of f). MC fiducial N = 1,291 vs analytic 903. This stacks on the earlier ×2–5
   FJ-floor correction to the original banked N~100–180.
3. **y-distribution fork (new, pre-registered):** the settled-vs-plunger dichotomy (banked-compatible)
   vs a uniform-y continuum (conservative) is a ×~2–3 fork in N. Both reported; truth in between.

## The N-to-3σ grid (carriers; median-z crossing | 90% power; two-class y)

| Scenario | can f=6% | can f=13% | alt f=7.6% | alt f=14.4% |
|---|---|---|---|---|
| A 2026 in-hand (24% errs, s_FJ=0.48, D=0.4) | 26,545 \| 54,069 | 6,675 \| 13,597 | 16,629 \| 33,871 | 4,998 \| 10,181 |
| B ELT ≤10%, s_FJ=0.15, D=0.4 | 3,369 \| 6,863 | 776 \| 1,580 | 2,146 \| 4,372 | 642 \| 1,307 |
| C ELT ≤10%, s_FJ=0.15, D=0.6 (DESI-tagged) | 1,454 \| 2,961 | 343 \| 698 | 963 \| 1,961 | 281 \| 572 |
| D ELT ≤10%, s_FJ=0.08, D=0.6 (best realistic) | 756 \| 1,539 | 178 \| 363 | 495 \| 1,008 | 149 \| 304 |
| E ELT ≤10%, s_FJ stays 0.48, D=0.6 | 11,637 \| 23,703 | 2,342 \| 4,771 | 7,088 \| 14,437 | 1,971 \| 4,014 |

Continuum-y fork: multiply by ~×1.8–3 (full grid in `.out`). Alt footing needs ×0.7–0.8 the N of
canonical — **the discriminator is not footing-hostage**.

**N_clusters curve** (scenario C, canonical; 9.6 usable carriers per LEWIS-class 30-target campaign =
30 × 0.40 measured shell fraction × 0.8 cut retention): 3σ at **35 clusters (f=13%) / 157 clusters
(f=6%)**; the 227 public HeCS-omnibus phase-tagged clusters give z ≈ 3.6–7.6 across the band. The
cluster reservoir is NOT the wall — carrier σ precision is.

## Guardrails verified as hard as the power claims

- **In-hand firewall (both footings):** 23 carriers, real errors → median z = 0.09–0.20 (best corner
  0.36), P(z≥3) ≤ 0.006 ≈ the null rate. Any firing on in-hand data is exploratory; cannot support or kill.
- **dE/bright-member backdoor (A2029 real specs):** 665 usable σ≥60 km/s members at 10% median error,
  predicted f~0.7% → N_3σ = 216,747 → shortfall ×326. Dead; no bypass through survey-measurable members.
- **Substructure stress test (protects MG from a false kill):** MG truth + 15% coherent infalling
  groups, no DS cut, N=900 → median FAKE z = 2.36, P(fake 3σ) = 0.28; with the frozen DS cut → z = 0.03,
  P = 0.0008. A detection without the substructure cut proves nothing.

## VERDICT (frozen rule E9): **STILL UNDERPOWERED — with the exact gap**

- **POWERED NOW: no.** No public dataset qualifies. Gap at today's precision tier: 23 carriers in hand
  vs ~6,700–26,500 needed (canonical band, measured floor) → **×290–1,150**.
- **POWERED IF (specific, all named):** ELT-HARMONI-class σ errors ≤10% (first exists ~2032; every
  2026 spectrograph sits above the 8–20 km/s carriers) **+** FJ control at the 0.15 floor (needs
  homogeneous distances/apertures; the in-hand 0.48 floor alone inflates N ×7.5) **+** DESI/HeCS
  caustic phase tagging at D=0.6 (already public and free) → **343–1,454 carriers = 36–152
  LEWIS-class cluster campaigns** (best realistic corner 178; 90% power ~×2; continuum-y fork ~×2–3).
- **STILL UNDERPOWERED (2026): yes** — gap **×8–63 at a precision tier that does not exist before
  ~2032, ×290–1,150 today**. DESI DR2 is not public (verified 401) and would not touch the binding
  wall anyway (it feeds the already-solved phase-tagging side).
- **What to do now for free:** pre-register this estimator + cuts and build the ELT target list by
  cross-matching the DESI DR1 647k-dwarf VAC LSB tail against HeCS-omnibus/gfinder clusters.

Unchanged theorems: MG relational spread = exactly 0 (symbolic, any a0, any interpolation, both
footings); sign (plungers hotter) and outward-rising radial profile are kernel-independent; the
6–13% amplitude is kernel-hostage (cone 5–18%) as banked.
