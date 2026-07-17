# VERIFY — adversarial verification of the Jeanneau+26 low-acceleration bTFR refit

**2026-07-16.** Verifier script: `verify_refit.py` (exit 0; independent code paths, own
integrator, own RNG seed 777 — shares no in-memory state with `apply_frozen_cut.py` /
`deep_refit.py`). Both original scripts re-run first: exit 0, every recorded number reproduced
bit-for-bit (`Δb=+0.140`, stat ±0.070, band ±0.272, N=61, ALT −0.243, CPL −0.000, halo −0.363,
gap 0.120, gas stress +0.089/+0.320, Re-stress N=47/71, full-95 gate −0.037).

## Verdicts by attack lane

### 1. Freeze integrity — UPHELD, with one immaterial drift (F1)
- `FROZEN_CUTS.md` mtime **19:34**; the catalog csv **22:24**; every analysis file later.
  Consistent with freeze-before-data (mtimes can't prove intent, but content can't have been
  tuned to per-galaxy numbers that did not yet exist on disk, and the cut-scan in §6 shows
  there was no tuning incentive anyway — every nearby cut gives the same verdict).
- Selection, estimator, error terms, gate: implementation matches the frozen text verbatim
  (cut re-implemented independently → same 61 galaxies; the two frozen algebraic forms of the
  cut agree galaxy-by-galaxy).
- **F1 (drift, immaterial):** frozen §4 says the magnification fallback error goes *into the
  bootstrap resamples*; the originals carried it as the Re±0.14 selection stress + weighted-mean
  check instead. Injecting the authors' global ±0.2 dex per-galaxy M_bar error into the
  bootstrap moves stat 0.070→0.082 and the honest band 0.272→**0.276**. No verdict motion;
  logged as the one freeze-vs-implementation deviation beyond those already in `DATA.md` §8.

### 2. Independent zero-point — CONFIRMED
Own loader, own bootstrap: median **+0.1397**, 68% CI +0.102…+0.242 (stat 0.070), identical
to recorded. Cross-estimators: Hodges-Lehmann +0.199, 10%-trimmed mean +0.193, mean +0.217 —
the positive offset is estimator-robust (if anything the median is the most conservative).

### 3. Dilution arithmetic per footing — CONFIRMED (own-a0 audit clean)
- Finite-difference dln M/dln a0 at fixed g_obs equals −x/(2+x) to 3e-9 on all 61 galaxies,
  both footings, each with **its own a0** (median 0.763 canonical / 0.818 ALT — recorded
  0.76/0.82).
- Exact per-galaxy predictions re-derived independently: ALT **−0.2431**, CPL −0.0001,
  ΛCDM halo −0.3631, |halo−ALT| gap 0.120 — all match. The cross-footing (bugged) variant
  the parent VERIFY caught would read −0.2248; the scripts assert against it and use the
  own-a0 number. The exact (not linearized −dil·log₁₀E = −0.216) value is what's reported.
- Degeneracy statement verified: gap 0.120 ≪ band 0.272 → footing-internal, as recorded.

### 4. Lensed-faint-sample selection bias — NEW FINDING (F2), headline unchanged, lean softened
Observed in the catalog: corr(log μ, logM*) = −0.34, **corr(log μ, Δb) = +0.38** — magnified
galaxies are intrinsically fainter and sit high on the relation, exactly the Malmquist-type
pattern. Injection test (mock population on a TRUE zero-offset relation, empirical logV, gas
fractions and μ resampled from the catalog, detection floor on magnified stellar mass at the
observed deep-subsample floor/p5): selected-median bias **+0.02…+0.11 dex positive**
(σ_int 0.25–0.45, completeness 0.71–0.87).
- Direction: the bias inflates +0.140, so correcting it moves the true zero-point *toward*
  ALT — the **1.41σ ALT-side lean is likely overstated; a bias-aware reading is ≈1.0–1.3σ**.
- It cannot rescue ALT (max plausible bias ≪ the 0.383 dex gap to ALT) and cannot be used to
  manufacture an ALT kill (it works against the kill). Headline STILL-UNDERPOWERED unaffected.
- Caveat honestly carried: the floor proxy is stellar-mass-based; the real selection is
  [OII]-flux/S/N + the √μ·Re/R_PSF resolution cut, so the numbers are order-of-magnitude, and
  the same monotone positive trend of the median with cut depth (+0.32 at 0.3a0 → +0.12 at
  0.7a0) is co-produced by the NUM gas-fraction tilt — the two artifacts are not separable
  with this catalog.

### 5. Gas-model band honesty — UPHELD, not narrowed (F3)
- The frozen ±0.20 coherent term equals the parent ledger's Jeanneau row (M_bar ±0.2; honest
  band 0.00±0.27) — **no narrowing** anywhere in the chain.
- Deep-61 vs full-95 exposure quantified: gas fraction 0.83 vs 0.70 (HI-only 0.33 vs 0.22).
  Incoherent 0.8-dex per-galaxy HI scatter → only 0.058 dex scatter on the deep median
  (inside the stat+0.20 budget), but a +0.11 dex Jensen (log-sum convexity) asymmetry on the
  deep median (vs +0.015 full-95) and a worst-case *coherent* NUM bias of ±0.8 dex would move
  the deep median −0.08/+0.52. So ±0.20 assumes the NUM *relation* is unbiased to ~0.2 dex —
  the paper's own assumption, carried as-is. A larger term only strengthens UNDERPOWERED and
  further weakens the lean; it cannot flip anything toward a constraint. The stated
  asymmetric HI×0.5/×2 stress (+0.089/+0.320) reproduces exactly.

### 6. Manufactured outcomes — NONE FOUND, both hunted
- **Manufactured ALT-kill:** the strict frozen-text reading actually *permits* the stronger
  label "ALT-side constraint, 1.41σ" (both rule conditions verified True); the originals chose
  the weaker STILL-UNDERPOWERED headline and flagged the stat-only 5.5σ as DO-NOT-CLAIM. The
  one unfrozen choice (collision resolution) went AGAINST the kill. Clean.
- **Manufactured save:** band terms all pre-frozen and parent-banked; no post-hoc inflation
  (band 0.272 ≤ the parent's 0.27–0.35 family). The cut-scan (0.3–0.7·a0, N=47–68) gives
  STILL-UNDERPOWERED at every threshold with σ_ALT 1.27–2.05 — no cut choice manufactures
  either outcome. Clean.
- Bookkeeping gates re-verified: M_bar = M*+M_HI+M_mol (<0.02 dex, all 95), full-95 gate
  −0.037 within the frozen ±0.05, Reff confirmed source-plane by the paper's own √μ·Re/R_PSF
  criterion (so g_obs is magnification-corrected in the selection).

## Bottom line
**HEADLINE UPHELD: STILL-UNDERPOWERED (band 0.272–0.276 > separation 0.243), footing-internal,
nothing about MI-vs-ΛCDM.** One correction to the subsidiary number: the "1.41σ ALT-side lean"
should be quoted with the new magnification-incompleteness caveat as **≈1.0–1.4σ** (injection
test bounds the positive selection bias at +0.02…+0.11 dex; it inflates the lean, never the
band). Not a canonical win (0.5σ compatible only, and the positive offset is plausibly
selection+gas-model artifact in roughly equal parts). The upgrade path stands: direct gas
masses at z≈1 shrinking the coherent term to ≲0.10 dex make this same frozen pipeline a
1.6–2.5σ ALT test.

Files: `verify_refit.py` (exit 0), originals re-run clean. END.
