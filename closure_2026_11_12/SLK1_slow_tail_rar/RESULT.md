# SLK1 (SLOW-TAIL KERNEL ON THE RADIAL ACCELERATION RELATION): RESULT

2026-11-12. Criteria 08f20ab497 (committed alone, before any script or number). A test lane; it adopts nothing.

## Verdict: RAR MARGINAL / RAR MARGINAL (canonical / alt)

On the 2,693 published SPARC points the Codex slow-tail kernel `μ★ = 1 − 1/√(1 + 2x)` has the same scatter as law S
(0.136 against 0.136 dex canonical; 0.140 against 0.133 alt) but a larger tilt across acceleration: its binned-median
residual ranges over 0.097 / 0.070 dex against law S's 0.053 / 0.036. The excess, 0.044 / 0.033 dex, falls between the
frozen COMPARABLE (0.03) and WORSE (0.06) lines. The tilt comes from the highest-acceleration bin, where the slow tail
over-predicts by 0.07–0.08 dex. Both instrument checks pass; the mutation twin exits 1.

The slow tail is not excluded by the relation at the published mass-to-light ratios, and it is not as good as law S.

κ = ½ FITTED. Footings never pooled. No outcome favours the framework.

## 1. Fixed footings, masses as published

Residual = log g_obs − log g_pred. Trend = range of the median residual over six bins of log g_bar.

| Footing | Kernel | rms | median | trend | reduced χ² | highest-acceleration bin |
|---|---|---|---|---|---|---|
| canonical | K slow tail | 0.1358 | −0.016 | 0.097 | 1.62 | −0.071 |
| canonical | S | 0.1361 | +0.026 | 0.053 | 1.68 | −0.011 |
| canonical | B | 0.1542 | +0.072 | 0.084 | 2.22 | +0.013 |
| canonical | R (published fit function) | 0.1371 | +0.032 | 0.041 | 1.71 | +0.007 |
| alt | K slow tail | 0.1399 | −0.042 | 0.070 | 1.75 | −0.081 |
| alt | S | 0.1328 | −0.002 | 0.036 | 1.61 | −0.022 |
| alt | B | 0.1419 | +0.043 | 0.059 | 1.86 | +0.008 |
| alt | R | 0.1329 | +0.005 | 0.039 | 1.62 | −0.003 |

K against S: rms −0.0003 / +0.0070; trend +0.044 / +0.033; |median| −0.011 / +0.040. Words: MARGINAL / MARGINAL.

## 2. Checks

| Check | Result |
|---|---|
| R1 published fitting function at a₀ = 1.20e-10 | rms 0.1329 dex (published 0.13) |
| R2 kernel inversions | 1.3e-13 ; 4.4e-16 |
| MUTATE newton | rms of K 0.136 → 0.514 and 0.140 → 0.514; exit 1 |

## 3. Reported (no word)

**One global shift of log g_bar (a common mass and distance scale):** the slow tail asks for −0.025 dex (canonical) and
−0.065 dex (alt), after which its rms is 0.1346 / 0.1331 and its trend 0.088 / 0.048. Law S asks for +0.035 / 0.000 and
reaches 0.1338 / 0.1328 with trend 0.063 / 0.036. On the alt footing, with baryonic masses 14 % lower, the slow tail
fits as well as law S does unshifted.

**a₀ free:**

| Kernel | best a₀ (m/s²) | rms | trend |
|---|---|---|---|
| K slow tail | 8.96e-11 | 0.1357 | 0.103 |
| S | 1.128e-10 | 0.1328 | 0.037 |
| B | 1.486e-10 | 0.1348 | 0.073 |
| R | 1.167e-10 | 0.1328 | 0.041 |

The slow tail's preferred a₀ is 4 % below the canonical footing (9.36e-11); law S's is the alt footing (1.132e-10) to
0.4 %. Each kernel picks one of the framework's two footings. That is an observation about two numbers, not a result:
the rms is nearly flat in a₀ (0.1357 at the optimum against 0.1358 at the canonical footing).

## 4. What this says, with EUC7

1. **The slow tail survives the rotation-curve relation, with a cost.** Same scatter as law S; 0.03–0.04 dex more tilt;
   0.07 dex too much acceleration in the innermost, bulge-dominated points at the published bulge mass-to-light ratio.
2. **The two gates pull the stellar masses in opposite directions for the slow tail.** In spiral bulges it wants stars
   about 0.1 dex lighter than the published (Kroupa-like) ratio. In SLACS ellipticals it wants Salpeter (EUC7), which is
   0.2–0.25 dex heavier than Kroupa. Law S wants the published ratio in bulges and 1.2 × Salpeter in SLACS. Both are
   statements about how the IMF differs between bulges and massive ellipticals; a heavier IMF in massive ellipticals
   is the measured direction, so neither kernel is contradicted, and neither is singled out.
3. **Limits.** The algebraic relation is exact for spheres only, and it is least accurate where the tilt arises (inner
   discs and bulges). The same approximation is applied to every kernel. No per-galaxy fit was made.
4. **Standing obligations of the kernel are unchanged:** the unscreened Solar correction of 5.27e-7 m/s² at 1 AU, and
   a screened static solution on which every gate here would have to be rerun.

## 5. Files

`slk1.py`, `slk1.out`, `slk1_results.json`, `slk1_MUTATE_newton.out` / `_results.json` (exit 1). Data:
`sol61_push/cold_production_2026_10_11/empirical_2026_10_12/RAR.mrt` (sha256 24aa7059dab7fa44…), as published.
