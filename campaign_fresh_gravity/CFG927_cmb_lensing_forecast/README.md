# CFG927: sealed CMB-lensing forecast. Theory-v2 vs its control: ACT-DR6-like BLIND at all L ≤ 3000, SO-baseline-like DISCRIMINATING only out to L ≈ 2000 (rule-dependent), S4-like DISCRIMINATING from L ≈ 700 and ROBUST from L ≤ 1000. The KiDS-excluded CFG596 P1 is DISCRIMINATING for every model, already at L ≤ 400 for SO/S4-like.

- **Criteria:** `FROZEN_CRITERIA.md`, commit **8791d53c3**. It was committed alone, before any CFG927 script or number existed. There are no amendments.
- **Seal:** commit **d3bb2e4c6** holds the table, outputs, scripts and `FORECAST_HASH.txt` (sha256 of 25 files; check with
  `shasum -a 256 -c FORECAST_HASH.txt`). The sha256 of `cfg927_forecast_table.json` is da593d87f0439a08…. This README came after the seal and is not hashed.
- **Settings:**
  - κ = ½ is FITTED.
  - The footings (9.3603e-11 / 1.1312e-10) are never pooled; each pair is forecast on its own footing.
  - "Cold energy" throughout; its mass is required; no particle species.
  - Not "theory closed".
  - **A forecast is not a measurement.** DISCRIMINATING means that a survey of that kind could tell the two arms apart. It does not mean either arm is right, and nothing here says the data favour the framework.
  - Models are framework-native only: no ΛCDM fit, no CAMB/CLASS nonlinear spectrum, no halofit, HMcode or BAHAMAS.
- **Compute:** NC2x (1024³) was live throughout.
  - Every process ran alone, single-threaded under `nice -n 10`. Measured peak memory was 0.22 GB (noise script) and ≤ 0.57 GB (forecast script).
  - NC2x's outputs were not read. Nothing was downloaded, and no running process was touched.

## Result

All numbers are quoted from `cfg927_forecast_table.json` and `cfg927_<PAIR>.json`.
- Δχ² = f_sky Σ_L (2L+1)/2 · (X_F − X_S0)² / (X_S0 + N^X)², summed over integer L.
- Class codes: D = DISCRIMINATING (≥ 9), M = MARGINAL (4–9), B = BLIND (< 4).
- r = ROBUST: every member (ZHOLD, ZREL, KCUT, KLOW, BG) gives the same class.
- d = RULE-DEPENDENT.

| pair (footing / inputs) | model (L_min) | L ≤ 400 | L ≤ 763 | L ≤ 1000 | L ≤ 2000 | L ≤ 3000 | L_9 |
|---|---|---|---|---|---|---|---|
| **T1x** (canonical / inherited) | ACT-DR6-like (40) | 0.07 Br | 0.45 Br | 0.79 Br | 1.86 Br | 1.97 Br | none ≤ 3000 |
| | SO-baseline-like (30) | 0.29 Br | 2.53 Bd | 4.58 Md | 11.03 Dd | 12.77 Dd | 1590 |
| | S4-like (30) | 0.68 Br | 12.41 Dd | 31.70 Dr | 143.1 Dr | 200.7 Dr | 703 |
| **T2x** (alt / inherited) | ACT-DR6-like | 0.06 Br | 0.42 Br | 0.73 Br | 1.73 Br | 1.83 Br | none ≤ 3000 |
| | SO-baseline-like | 0.26 Br | 2.34 Br | 4.25 Md | 10.23 Dd | 11.84 Dd | 1712 |
| | S4-like | 0.63 Br | 11.50 Dd | 29.42 Dr | 132.8 Dr | 186.1 Dr | 717 |
| **NC1x** (canonical / native) | ACT-DR6-like | 0.08 Br | 0.53 Br | 0.91 Br | 2.11 Br | 2.22 Br | none ≤ 3000 |
| | SO-baseline-like | 0.33 Br | 2.93 Bd | 5.25 Md | 12.40 Dd | 14.30 Dd | 1431 |
| | S4-like | 0.77 Br | 14.03 Dd | 35.44 Dr | 156.8 Dr | 219.1 Dr | 682 |
| **P1** (canonical / inherited; KiDS-EXCLUDED) | ACT-DR6-like | 4.07 Md | 21.37 Dr | 32.31 Dr | 57.5 Dr | 59.4 Dr | 518 |
| | SO-baseline-like | 17.32 Dr | 117.3 Dr | 183.4 Dr | 334.3 Dr | 363.7 Dr | 339 |
| | S4-like | 40.68 Dr | 546.7 Dr | 1165 Dr | 3713 Dr | 4669 Dr | 295 |

**Context rows** (no class weight):
- **CV-limited ceiling (f_sky 0.4, L_min 30):** theory-v2 gives 0.82–1.00 at L ≤ 400 and 22.6–27.1 at L ≤ 763.
  - So even a noiseless survey cannot tell theory-v2 from its control at L ≤ 400.
- **Noise scan** (f_sky 0.4, beam 1.4′, L 30–3000). The Δ_T for which Δχ² = 9:
  - T1x: **8.0** μK-arcmin;
  - T2x: **7.5** μK-arcmin;
  - NC1x: **8.8** μK-arcmin;
  - P1: **> 20** μK-arcmin (Δχ² 76.9 at 20 μK-arcmin).
- **PR4 8–400 Asimov** (PR4 covariance, ΔB = (W + M)ΔX):
  - theory-v2: 0.017–0.021;
  - P1: 1.034. CFG917's realised P1 Δχ² of +1.88 lies within the expected spread of 2√1.03 ≈ 2.0.
- **For a future real-data scorer:**
  - If S0 is true, the realised χ²(F) − χ²(S0) has expectation +Δχ², with standard deviation 2√Δχ² (stored per cell as `sd_realised`).
  - If F is true, the expectation is −Δχ², with the same spread.

**Per-pair reading** (frozen rule: the shortest listed range that is DISCRIMINATING):
- **Theory-v2, all three finished runs** (canonical native, canonical inherited, alt inherited):
  - ACT-DR6-like: not within L ≤ 3000.
  - SO-baseline-like: L 30–2000 (rule-dependent).
  - S4-like: L 30–763 (rule-dependent), and ROBUST from L 30–1000.
- **P1:**
  - ACT-DR6-like: L 40–763, ROBUST. This is ACT's published baseline range.
  - SO-baseline-like and S4-like: L 30–400, ROBUST.

## Why high L helps

At L ≤ 400, a third of each S0 C_L comes from k < 0.08 h/Mpc, where the two arms are identical by construction (k < k_lo share at L = 400: 0.33). From L ≈ 763 that share is 0.000. The suppression measured in the box then reaches the lensing spectrum directly. For theory-v2, X_F/X_S0 is:

| L | 400 | 763 | 1000 | 2000 | 3000 |
|---|---|---|---|---|---|
| X_F/X_S0, T1x | 0.991 | 0.978 | 0.968 | 0.934 | 0.912 |

T2x and NC1x agree with T1x to 0.004. For P1 (a boost) X_F/X_S0 is 1.065, 1.135, 1.172, 1.286 and 1.332 at the same L. That is why CMB lensing at L ≤ 400 (CFG917) was weak, and why it stops being weak above L ≈ 700.

## Box support cut (declared, honoured)

- L_sup ≥ 3000 for every pair: no cell is NOT COMPUTABLE.
- The largest k > 7.98 h/Mpc share at L 8–3000 is 0.0013 of X_S0 and 0.0014 of X_F − X_S0, against a threshold of 0.10.
- KCUT, which uses measured spectra only to 4.02 h/Mpc, moves every graded cell by ≤ 0.2%.
- Nothing above L = 3000 was forecast.

## The main caveat: most of the high-L difference rests on the z > 1 continuation

The runs have no snapshot above z = 1. The share of X_F − X_S0 that comes from z > 1, under CFG917's primary rule (each arm keeps its z = 1 shape and grows linearly), is:

| pair | L = 400 | L = 763 | L = 1000 | L = 2000 | L = 3000 |
|---|---|---|---|---|---|
| theory-v2 | 0.45–0.48 | 0.58–0.60 | 0.62–0.63 | 0.72–0.73 | 0.77–0.78 |
| P1 | 0.53 | 0.63 | 0.66 | 0.80 | 0.87 |

- ZREL lets the F/S0 ratio relax to 1 at z_i. It roughly halves every high-L Δχ²:
  - S4-like, L ≤ 763: 7.2–8.8, which is MARGINAL. That is why those cells are RULE-DEPENDENT.
  - S4-like, L ≤ 1000: 17.4–21.0, still DISCRIMINATING.
  - SO-baseline-like, L ≤ 2000: 5.5–6.7, MARGINAL.
- ZHOLD changes cells by ≤ 12%. KLOW raises every cell.
- **What the sealed forecast does and does not depend on:**
  - The S4-like statement from L ≤ 1000 upward survives every declared continuation.
  - The SO-baseline-like statement does not survive ZREL.

## Noise-model anchors (K7, reported) and a post-hoc context check

- **Anchors.** The Gaussian quadratic-estimator Fisher errors are more optimistic than published analyses:
  - Planck-like over 8–400: σ(A) 0.0190, against 0.028 on disk (ratio 0.68);
  - ACT-DR6-like over 40–763: σ(A) 0.0127, against 0.023 (ratio 0.55).
- Both ratios lie inside the frozen [0.5, 2] band, so both models count as anchored, but the ACT-like ratio is near the edge.
- There is no on-disk anchor for SO or S4. In this code, σ(A) over 30–3000 is 0.0058 (SO-baseline-like) and 0.0026 (S4-like).
- **Post-hoc context check (arithmetic on the sealed numbers; dated 2026-10-20; not a class and not part of the seal).** The question: what if every model is as optimistic as these anchors? The test multiplies each Δχ² by ratio², which is 0.30 (ACT anchor) or 0.46 (Planck anchor). For theory-v2:
  - ACT-like 40–763 becomes 0.13–0.16.
  - SO-like 30–2000 becomes 3.1–3.8 (ACT anchor) or 4.7–5.7 (Planck anchor), so it would no longer discriminate.
  - S4-like 30–763 becomes 3.5–6.4.
  - S4-like 30–1000 becomes 8.9–16.2.
  - S4-like 30–2000 becomes 40–72. Even with ZREL and the ACT anchor together it is 21–25.
  - For P1, ACT-like 40–763 becomes 6.5 (MARGINAL) and SO/S4-like stay ≥ 100.
- **Conclusion:** the most secure sealed statement is "an S4-class survey using lensing modes to L ≈ 2000 separates theory-v2 from its control". The SO-class and L ≤ 1000 statements are less secure.

## K tests and MUTATE

| test | result |
|---|---|
| K1 F ≡ S0 → 0 in every cell, member, PR4 Asimov and PR4 Δχ² | PASS ×4 (max 2.8e-27) |
| K2 CFG917 PR4 8–400 Δχ² reproduced (primary + AGG/ZHOLD/ZREL/KCUT/KLOW/BG), ≤ 1e-6 | PASS ×4, all differences exactly 0. T1x −0.0881, T2x −0.0848, NC1x −0.2760, P1 +1.8808 (AGG +10.0537, KLOW +10.3969) |
| K3 extended projector = `LB.limber_X` on L 2–2500 | PASS ×4 (0.0) |
| K4 noise grid convergence (halved Δℓ, doubled angles), N_L^MV ≤ 1% | PASS (max 2.3e-3, SO-like) |
| K5 analytic flat-spectrum TT identity N_L = 8π²/(L⁴·Area), ≤ 0.5% | PASS (6.3e-4, 7.6e-4, 9.2e-4 at L 100/1000/2000) |
| K6 doubled z grid: every primary cell ≤ max(0.01, 1%), L_sup unchanged | PASS ×4 |
| K7 noise anchors (reported) | 0.68 / 0.55, anchored (see above) |

**MUTATE** (run first for every pair; separate `_MUTATE` outputs) **bites ×4.**
- M1 (F ≡ S0): exactly 0.
- M2, ±5% amplitude: the pipeline matches the analytic sum to ≤ 2e-15.
  - S4-like 30–3000: 396.7 (T1x, T2x, P1) and 408.7 (NC1x), for both signs. This is DISCRIMINATING.
  - SO-like: 76.5. ACT-like: 18.1 (T1x).
- M3 context, box-only ±5% (k 0.08–7.98, z ≤ 1 only), T1x:
  - S4-like: 1.69 at L ≤ 400, 6.37 at L ≤ 1000, 11.7 at L ≤ 3000.
  - ACT-like: ≤ 0.45.
  - The measured box itself carries little of the lensing weight; most of the signal comes through the z > 1 extension of the box-scale change.

## Disclosures

1. The first `cfg927_noise.py` run crashed after printing K4, K5 and K7. The crash was in the context line computing σ(A) over 30–3000 for SO/S4: CFG917's FFP10 loader stops at L 2500.
   - The fix reads the same file and column to L 3000, asserting identity with `LB.load_ffp10` up to 2500.
   - The rerun reproduced K4, K5 and K7 unchanged. No rule changed, and no forecast number existed yet.
   - One print line in `cfg927_forecast.py` was tidied before its first run.
2. **Shared, non-cancelling inputs:**
   - FFP10 (ΛCDM) lensed CMB spectra in the noise model, giving the same N_L for both arms;
   - illustrative survey parameters. Only ACT's L 40–763 and SO's f_sky 0.40 are on-disk quotes; all other parameters are ILLUSTRATIVE round values;
   - the inherited runs' EH σ8 = 0.811 spectrum and radiation-free background;
   - the native runs' CFG654 §6 inputs;
   - Limber; a Gaussian covariance (no N1, non-Gaussian, foreground or super-sample terms);
   - a flat-sky quadratic estimator (no iterative delensing, which is conservative for S4-like). The MV combination ignores estimator cross-covariances (slightly optimistic).
3. The fiducial is the control S0. Both arms are single 100 Mpc/h realisations, as in CFG917; the realisation-variance correction (k ≤ 1) is CFG917's and multiplies both arms.

## What this establishes, and what it does not

- **It establishes (sealed, before any such data were looked at):**
  - At L ≤ 400 no survey of any noise level separates theory-v2 from its control (CV ceiling 0.82–1.00). CFG917's low power is therefore a property of the multipole range, not of Planck's noise.
  - Above L ≈ 700, a survey near 8 μK-arcmin over 40% of the sky, using modes to L 3000, reaches Δχ² = 9 under the primary continuation.
  - An S4-like survey separates the arms robustly from L ≤ 1000 (and, after the post-hoc anchor penalty, from L ≤ 2000).
  - The KiDS-excluded CFG596 P1 would be separated even by an ACT-DR6-like survey on its published 40–763 range.
- **It does not establish:**
  - Anything about real data.
  - Anything about the alt footing with native inputs (NC2x, not forecast).
  - Anything above L 3000.
  - That the z > 1 continuation is right. It carries 45–78% of the theory-v2 difference, and ZREL halves the forecast.
  - A realistic survey covariance: the anchors suggest the Gaussian forecasts are optimistic by ×2–3 in Δχ².

## NC2x (later, as a dated addendum; not part of this seal)

Run these only after chain7 has finished NC2x and CFG917 has scored it.
- First add an `NC2x` entry to `PAIRS` in an addendum copy of the script, using CFG917's NC2x glob and `cfg917_NC2x.json` as the K2 target.
- Then run `CFG927_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 <script> --pair NC2x`.
- Then run the same command without `CFG927_MUTATE`.

## Files

| file | role |
|---|---|
| `FROZEN_CRITERIA.md` (8791d53c3) | criteria |
| `cfg927_noise.py` → `cfg927_noise.out/json` | Hu–Okamoto MV N_L for the declared models and the noise scan; K4, K5, K7 |
| `cfg927_forecast.py --pair <PAIR>` → `cfg927_<PAIR>[_MUTATE].out/json` | support cut, forecast cells, members, scan, PR4 Asimov; K1–K3, K6; MUTATE M1–M3 |
| `cfg927_table.py` → `cfg927_forecast_table.json/md`, `FORECAST_HASH.txt` | the sealed table and its hash file |
| `../CFG917_cmb_lensing_gate/cfg917_lib.py` (sha256 ec1e971bdb31c7b4…) | CFG917's machinery, imported unchanged |

Reproduce, one process at a time:
```
OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_noise.py
CFG927_MUTATE=1 OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_forecast.py --pair T1x   (and T2x, NC1x, P1)
OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_forecast.py --pair T1x                   (and T2x, NC1x, P1)
OMP_NUM_THREADS=1 nice -n 10 python3 cfg927_table.py
```

κ = ½ FITTED; footings never pooled; cold energy mass required; not theory closed.
