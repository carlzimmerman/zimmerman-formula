# DP1: the NSS-off robustness rung, DR3 reproduction check. FROZEN CRITERIA (written and committed alone, before any code)

Date 2026-11-05. Pre-data (Gaia DR4 due 2026-12-02). DR3 numbers are code-path tests, never results (Amendment 7(e));
NON-SCORING; no verdict words about gravity. κ = ½ FITTED; footings never pooled; not theory closed.

## 0. What this lane implements and why

`OWNER_DECISION_2026-11-05b_DR4_D7_D8.md`, D7 N4.1: the NSS-off rung is run as `build(drop_nss=True, smax_kau=30)` (the
code path in `campaign_fresh_gravity/CFG816_dr4_r_statistic_scoring/build_variant_catalogue.py`), wired into the sweep
tooling as new code before release, and it must reproduce the D2 lane's DR3 NSS-off probe on the DR3 extract before it is
used on DR4. If the DR3 check fails, the rung is declared NOT IMPLEMENTED in the DR4 report.

New code only, in `dr4_push_2026_11_05/DP1_nss_off_rung/`. Imported read-only, never edited: `wide_binary_pipeline.py`
(sha256 7c884e0e...), `catalog_builder/build_catalog.py`, `dr4_ready_1/dry_run_driver.py`, `dr4_ready_1/seed_sweep.py`,
`build_variant_catalogue.py`, the D2 lane. Offline (socket guard), `python -B`, OMP_NUM_THREADS=1, nice 10, RSS ≤ 4 GB.

## 1. The reference (what is reproduced)

The D2 lane (`doors_push_2026_10_22/D2_wide_binary_fork/d2_sigma_sys_defs.py`, results `d2_sigma_sys_defs_results.json`)
built its NSS-off probe as the CFG816 variant catalogue (`build(drop_nss=True, smax_kau=50)`, sha256 80c12924...,
6,308 pairs) restricted to s < 30 kAU (6,302 pairs), and fitted it with its in-script estimator (frozen pipeline functions,
1e6-object DR4-noise master, boot 200, one rng seeded 20261216 consumed in the order canonical V0..V5 then alt V0..V5).

| footing | baseline γ̂ (V0, N 6,210) | probe γ̂ (V3, N 6,302) | **reference shift** | σ_fit (V0) |
|---|---|---|---|---|
| canonical | 1.0750 | 1.1500 | **+0.0750** | 0.0550 |
| alt | 1.0700 | 1.1275 | **+0.0575** | 0.05125 |

The rung differs from the probe by construction in one way only: with the 30 kAU cap applied inside the build, the stage-G
velocity-error Monte Carlo runs over a different pair array, so its stream maps to different pairs and ~2-3 % of marginal
pairs flip each way (build_variant_catalogue self-test V2/V4; Amendment 18). **Byte identity with the probe is therefore
impossible by construction and is not required.** The tolerance below is set from the measured flip noise.

## 2. Noise scale used for every tolerance (set now, from the record, not from this run)

σ_G = the stage-G-only build-to-build SD of γ̂ on DR3, Q-G50, 51 builds, registered fit path
(`dr4_ready_1/seed_sweep_g50_summary.out`): **canonical 0.0249, alt 0.0211**. Rung and probe are two (near-independent)
stage-G realisations, so their γ̂ difference has SD ≈ √2 σ_G. Single-realisation tolerance T_f = 2√2 σ_G:
**T_can = 0.0704, T_alt = 0.0597.** Ensemble (K = 8) tolerance E_f = 2√2 σ_G / √8 = σ_G: **E_can = 0.0249, E_alt = 0.0211.**

Power statement made now: T_f is about the size of the reference shift itself (0.0704 vs 0.0750 canonical; 0.0597 vs
0.0575 alt). A single-realisation γ̂ comparison therefore cannot by itself tell the rung from "no change" on the alt
footing. The discriminating checks are P1 (pair level) and P4 (ensemble). This is stated, not tuned away.

## 3. Known-answer checks (all must pass, else the lane reports CODE FAULT and no verdict)

- **K1** the wrapper with drop_nss=False, smax 30, cut13 extract-builder reproduces the registered DR3 catalogue byte for
  byte (sha256 prefix 6fff64d964ebaa72 = the driver's REF_SHA_DR3, and equals the on-disk `wide_binaries_dr3.csv`).
- **K2** the wrapper's rung bytes (drop_nss=True, smax 30, extract-builder) equal `build_variant_catalogue.build(True, 30)`
  bytes exactly (same code path).
- **K3** `build_variant_catalogue.build(True, 50)` reproduces the committed CFG816 variant catalogue (sha256 80c12924...),
  i.e. the D2 probe's source is reproducible here.
- **K4** the D2 estimator, re-implemented in this lane, run on D2's exact six inputs in D2's order, reproduces all 12 D2 fits
  (γ̂ and σ_fit, both footings) to |Δ| ≤ 1e-9.
- **K5** sha256 of `wide_binary_pipeline.py` (7c884e0e...), `build_catalog.py`, `dry_run_driver.py`,
  `build_variant_catalogue.py` identical before and after every run; nothing written outside the DP1 folder.
- **K6** the rung catalogue: every s in (2, 30) kAU; ≥ 20 pairs with an NSS-flagged component (stage A `non_single_star`).

## 4. Reproduction criteria (ALL of P1-P4 must pass, both footings where a footing applies → REPRODUCED)

- **P1 pair level, rung vs probe (s < 30 kAU of the CFG816 variant).** Jaccard of the NSS-flagged pair sets ≥ 0.90; of the
  other pairs, the fraction of the probe absent from the rung ≤ 0.05 and the fraction of the rung absent from the probe
  ≤ 0.05 (reseed baseline 2.2-2.4 %).
- **P2 D2 estimator, one realisation (the registered seeds).** D2's sequence re-run with the rung catalogue in the V3 slot
  (everything else as D2); shift = γ̂(V3) − γ̂(V0) in that run. Pass if |shift − reference shift| ≤ T_f.
- **P3 registered fit path, one realisation.** `wide_binary_pipeline.py --catalog <csv> --seed 20261216` (seed_sweep's
  `fit_via_pipeline_cli`) on the rung CSV and on the probe CSV (variant ∩ s < 30, written in this folder). Pass if
  |γ̂(rung) − γ̂(probe)| ≤ T_f. (Baseline fitted too, for the shift reported.)
- **P4 ensemble, K = 8 (stage-G seed offsets k = 1..8, offline, each build's own existing seed_k<k> cache, read only).**
  For each k: base_k = registered build, probe_k = build(True, 50, k) ∩ s < 30, rung_k = rung build k. Each fitted by the D2
  estimator with the K4 model medians and a fresh rng(20261216) for the bootstrap. Pass if
  |mean_k[γ̂(rung_k) − γ̂(probe_k)]| ≤ E_f.

Under a correct implementation the expected false-failure rate of P2+P3+P4 together is ~10-15 % (three ~2σ cuts, two
footings each, correlated); stated now. A failure is reported as the result; no re-run with other seeds or tolerances.

## 5. MUTATE (must bite)

**M1** the rung run with drop_nss=False (smax 30): i.e. the registered build, no NSS-off change. P1-P4 are re-run on it,
outputs suffixed `_MUTATE`. **Bite requirement: the M1 verdict must be NOT REPRODUCED, and P1 must fail.** Whether P2,
P3 and P4 bite individually, per footing, is reported as the power of each check (§2 predicts P2/P3 may not bite on alt).
If M1 reads REPRODUCED, the check has no power and the rung is declared NOT IMPLEMENTED.

## 6. Reported beside the verdict (no weight)

D7 N4.2 reading of the DR3 rung: |shift| < 1 σ_fit counts as passing the NSS-off condition. The ensemble mean NSS-off
shift (rung_k − base_k, probe_k − base_k) and its SD, as a DR3 look at how much of the single-realisation +0.075 is flip
noise. This changes no σ_sys definition (D8 option (a) stands) and no band or verdict.

## 7. Verdict words

REPRODUCED (K1-K6 pass, P1-P4 pass, M1 bites) → the rung is IMPLEMENTED for DR4 with the command in the README.
NOT REPRODUCED (any of P1-P4 fails, or M1 does not bite) → per D7 N4.1 the rung is NOT IMPLEMENTED in the DR4 report,
does not block a verdict, and σ_sys(b) is computed without it, stated. CODE FAULT (a K check fails) → fixed forward only if
the fault is in this lane's new code, recorded; never by editing a frozen file.
