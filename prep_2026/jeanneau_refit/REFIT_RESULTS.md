# REFIT RESULTS — Jeanneau+26 low-acceleration bTFR zero-point vs the a0(z) footing fork (Lane R)

**2026-07-16.** Script: `deep_refit.py` (exit 0; re-asserts the banked fork anchors, the
paper's mass bookkeeping, and the full-95 pipeline gate before printing any subsample number;
includes a guard assertion against the parent VERIFY's cross-footing dilution bug).
Figure: `deep_refit.png`. Per-galaxy degeneracy table: `deep_refit_degeneracy.csv`.
Selection/estimator/error model: `FROZEN_CUTS.md` (frozen 19:34, BEFORE any per-galaxy number
was read; applied with zero deviations — fallbacks as pre-authorized, logged in `DATA.md` §8).
Data: `jeanneau26_catalog_cds.csv` = verbatim CDS/VizieR **J/A+A/709/A120/catalog** (Jeanneau+
2026, A&A 709 A120, arXiv:2603.28856, CC-BY-4.0), 95 rows = exactly their fiducial bTFR sample.
Parent: `prep_2026/highz_tfr_fork/` (this refit is that workflow's named wash-breaker #1).

**Convention:** Δb = bTFR zero-point offset along the MASS axis at fixed velocity vs the
Lelli+19 local reference (their line: log M_bar = 3.14 log v_c(2Re) + 3.54), dex.

## 1. The subsample and its zero-point (frozen estimator)

Frozen cut `g_bar < 0.5·a0_canon` (g_obs = v_c(2Re)²/(2Re), inverted through the framework's
OWN ν at a0_canon = 9.36e-11; cut defined once on the canonical footing so both footings test
the same galaxies) selects **N = 61 of 95** — far more than the forecast "third": the lensed
dwarf sample sits much deeper in the a0 regime than the parent's typicals
(g_bar/a0 median **0.16**, quartiles 0.06/0.16/0.25, range 0.00–0.49; z median 1.06;
logM* median 8.9; median v_c = 81 km/s; magnification median 2.4).

| quantity | value |
|---|---|
| **Δb (median, fixed slope 3.14)** | **+0.140 dex** |
| bootstrap 68% (10⁴ draws) | +0.102 … +0.242 (stat ±0.070) |
| MAD | 0.309 dex |
| **honest band** = √(0.070² ⊕ 0.20²_gas ⊕ 0.16²_locref ⊕ 0.06²_conv) | **±0.272 dex** |
| gas stress: HI ×0.5 / ×2 (coherent, the binding systematic) | +0.089 / +0.320 |
| selection stress: Re ±0.14 dex (magnification fallback) | +0.322 (N=47) / +0.102 (N=71) |
| full-95 gate | −0.037 dex → reproduces their 0.00±0.06, PASS |

The gas term dominates by construction: the deep subsample is **83% scaling-relation gas by
median** (Tacconi+20 molecular + NeutralUniverseMachine HI with 0.8 dex scatter in log τ_HI),
and that error is coherent — it does not shrink with N. The ±0.272 is the honest number.

## 2. Fork predictions for THIS subsample (exact per-galaxy, framework ν, each footing's OWN a0)

Dilution (dlnM/dlna0 = x/(2+x) exact through ν): median **0.76** with the canonical a0,
**0.82** with ALT's own a0 = 1.13e-10 — the parent forecast (>0.6) is exceeded; ~80% of the
deep-MOND a0-lever survives here, vs 7–55% in every published full sample.

| footing | Δb prediction (median; range) |
|---|---|
| canonical pure-Λ (a0 = cH_Λ/Z, ρ_DE, w=−1) | **0.000** (identically — a0 exactly constant) |
| canonical DESI-CPL (w0=−0.752, wa=−0.86) | **−0.000** (−0.020 … +0.022) |
| ALT ρ_tot/cH0 (a0 ∝ E(z), rising) | **−0.243** (−0.341 … −0.106) |

Cross-footing-bug guard (parent VERIFY §5): diluting ALT with the CANONICAL a0 would give
−0.225 (understated); the script asserts own-a0 > cross-footing and uses only the exact own-a0
number. The framework's Newtonian size term cancels as forecast: −0.035 dex residual in the
subsample (vs −0.059 full-95) — deep-MOND M = v⁴/(G a0(z)) is R-independent, so compactness
evolution drops out. The fork separation (0.243) exceeds the stat error (0.070) — the parent
forecast was right about that — but not the coherent gas floor.

## 3. ΛCDM degeneracy: computed, NOT broken

The standard halo-scaling drift (Jeanneau's own Eq. 9 first term, Dutton+11/MMW) is a
mass-assembly effect: it does **not** pass through ν and is **not** a0-diluted. Per-galaxy over
the subsample: median **−0.363 dex** at z_med = 1.06.

- ALT-vs-ΛCDM gap, undiluted (parent regime): median 0.095 dex (parent banked max 0.118).
- ALT-vs-ΛCDM gap **with** the deep-cut dilution: median **0.120 dex** (range 0.073–0.183).

The deep cut *widens* the gap slightly (dilution shrinks ALT to −0.243 while the halo term
stays −0.363) but 0.12 dex is far inside the ±0.272 band → **degeneracy NOT broken**. The size
term cancels in the deep regime; the halo term does not — and both ALT and the no-gas-
compensation ΛCDM edge predict a FALLING zero-point that is not seen, and both escape the same
way (rising gas fractions — exactly the model-mediated quantity the measurement is built on).
**The test stays footing-internal (canonical vs ALT), exactly as the parent banked. It says
nothing about MI-vs-ΛCDM.**

## 4. Verdict (mechanical, frozen rules; collision disclosed)

Δb = +0.140, B = 0.272, |Δ_ALT| = 0.243 → σ from canonical(0) = **0.51**; σ from ALT(−0.243)
= **1.41**. Two frozen rules fire simultaneously because Δb landed POSITIVE — away from BOTH
footings, a case the freeze did not anticipate:

1. **B > |Δ_ALT| → STILL-UNDERPOWERED** (0.272 > 0.243): a measurement placed exactly AT the
   ALT point would still sit only 0.89σ from canonical — the band cannot cleanly separate the
   fork in either direction.
2. |Δb| < B while |Δb − Δ_ALT| = 0.383 > B → nominal "ALT-side constraint at 1.41σ".

**HEADLINE: STILL-UNDERPOWERED, with a 1.41σ ALT-side lean (a lean, NOT a constraint).**
The structural rule wins: the honest band exceeds the fork separation, and the +0.14 central
value is gas-model-suspect (HI ×0.5/×2 alone moves it +0.09/+0.32 in a subsample that is 83%
scaling-relation gas). The stat-only contrast (**5.5σ from ALT / 2.0σ from canonical**) is
printed for transparency and is **DO-NOT-CLAIM** — it treats NUM-HI/Tacconi gas as noiseless.
Symmetrically, this is **NOT a canonical win**: 0.51σ is "compatible", not "confirmed", and
the offset sits on the positive side of even the canonical prediction.

What survives, straight: the first published-data number directly ON the ALT branch in the
near-deep regime shows **no trace of the falling zero-point ALT needs where it is least
diluted** — ALT is dented at ~1.4σ with everything carried honestly (the parent had only a
0.65σ full-sample lean). ALT is not killed; the wash persists because the deep cut trades
acceleration leverage for gas-model exposure one-for-one at current gas-measurement quality.

## 5. What would upgrade the lean to a constraint

The binding systematic is the coherent gas-scaling term (±0.20). Direct gas masses for even a
subset of these 61 (ALMA CO or dust-continuum for the brighter dwarfs, or a stacked HI/CO
constraint at z≈1) shrinking the coherent term to ≲0.10 would put B ≈ 0.15 < 0.243 and make
this exact frozen pipeline a ≥1.6σ–2.5σ ALT test with no other change. DESI DR3 w→−1 keeps
canonical exactly flat (the CPL variant is already indistinguishable from flat here, −0.000).

END.
