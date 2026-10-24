# X7_cluster_core_significance: is the cluster-core excess real once the shear systematics are calibrated?

Criteria: `FROZEN_CRITERIA.md` (committed alone, 40ae8ff09f; amendments A1–A5 below). Inputs and classes:
`ASSUMPTION_LEDGER.md`. κ = ½ FITTED. Footings 9.3603e-11 / 1.1312e-10 m s⁻², never pooled. No dark-matter particle. Not
"theory closed". Nothing here says the data favour the framework.

## Verdict (frozen classes; JSON keys in `x7_analysis_results.json`)

- **V1 core excess: MARGINAL** (`V1`, `Z_MID_CAL`). With calibrated systematics Z_MID is 2.93 / 2.78 (canonical, h 0.672 /
  0.686) and 2.52 / 2.41 (alt). Statistical errors alone give 4.5–5.5 (REAL); X2's conservative treatment gives 2.2–2.7.
  The class is the same with the clipped boost, at C0, and with the per-tile leakage bracket (`V1_qualifiers`).
- **V2 mass trend of A_MID: UNDECIDED** (`V2`). The lightest tercile is **consistent with A = 1** (Z_CAL 0.01–0.24), but a
  step at X2's boundary improves χ² by only 4.2–4.6 (line 9), and a slope by 2.0–2.2.
- **V3 mass trend of A_OUTER: PRESENT, linear in log M** (`V3`). Δχ² = 15.5–19.3 over a constant. The slope is +0.83 to +1.00
  per dex in MGAS500. The lightest tercile lies **below** the law (A_OUTER 0.45–0.53, Z_CAL −2.2 to −2.7).

What decides V1 is the cross shear. The PSF leakage model explains almost none of it. It sits 2.2–2.5σ above pure shape
noise. So the calibrated systematic keeps about 90 % of X2's amplitude, and Z rises only from 2.2–2.7 to 2.4–2.9.

## Step 0: same data, same code

- **Extraction (E1–E3 PASS).** My own KiDS cache equals F1's byte for byte in all 7 shared columns. It adds PSF_e1, PSF_e2 and
  the tile name for all 21,262,011 rows; no PSF value is non-finite. THELI_INT is not a unique tile key (514 values for 988
  tiles), so it is not used.
- **Replay (M1–M6 PASS).** The measurement reproduces X2's committed npz exactly (max |Δ| = 0) for 326 clusters, including
  D, E, den, den_r, Dx, DRR and the source moments. The template path fed with (e1, e2) returns D and Dx exactly. A rotation
  by 0 returns D; a rotation by π/4 gives D_t = −D_x (2e-13).
- **K0 PASS.** X2's own functions on X2's npz reproduce 236 numbers of X2's JSON and F1's PRIMARY rows with max |Δ| = 0:
  C0, C\*, the terciles, both conventions, and A, s_jk, s_tot, A_x, A_RR. **K1:** my replay equals X2's npz.

| cell | C0 A_MID | C\* A_MID ± s_jk | C\* Z, X2 (e) | X2 JSON |
|---|---|---|---|---|
| canonical h 0.672 | 1.676 | 1.640 ± 0.118 | +2.70 | 1.640, +2.70 |
| canonical h 0.686 | 1.720 | 1.684 ± 0.113 | +2.58 | 1.684, +2.58 |
| alt h 0.672 | 1.540 | 1.505 ± 0.108 | +2.32 | 1.505, +2.32 |
| alt h 0.686 | 1.580 | 1.545 ± 0.104 | +2.24 | 1.545, +2.24 |

## Step 1: the calibrated systematics (all 326 clusters, C\* model, boost convention)

**(a) PSF leakage** (`x7_psf_regression.out`; `LKP`, `global`). The fit uses 21.16 M sources.
- Per patch × tomographic bin, α ranges from −0.037 to +0.069 with errors of 0.010–0.023. The c terms are ≤ 1.1e-3.
- The global fit gives α₁ = +0.0083 ± 0.0042, α₂ = +0.0087 ± 0.0045, c₂ = +6.1e-4.
- The per-tile fit (LK-T) is noise-dominated: σ_α ≈ 0.26 per tile, and the tile-to-tile χ²/dof is 1.10 / 1.13.

Projected around the clusters (cluster − random, in A units; `all.<C*|boost|cell>.<band>.leak_t|leak_x|leakT_t|s_leak`):

| band | LK-P tangential | LK-P cross | LK-T tangential (bracket) | raw PSF pattern, α = 1 (t / x) |
|---|---|---|---|---|
| MID | −0.0001 to +0.0000 ± 0.0004 | +0.0028 to +0.0032 | +0.024 to +0.027 | −0.013 to −0.016 / +0.054 to +0.061 |
| OUTER | +0.0024 to +0.0027 ± 0.0005 | +0.0024 to +0.0027 | +0.058 to +0.066 | +0.076 to +0.083 / +0.041 to +0.048 |

The PSF pattern around clusters is small, and α is a few per cent, so the leakage is ≤ 0.003 in A units. The per-tile
bracket is larger (+0.02–0.07), but its coefficients are noise, and it changes no class.

**(b) Random points** (`rand_t`, `rand_x`, `A_RR`).
- F1's raw random-point stack is consistent with zero tangentially (|Z| ≤ 0.6).
- In the cross channel it is −0.064 to −0.078 in MID (Z −1.7 to −1.9).
- R−R is consistent with shape noise in every cell (excess s_RR = 0).

**(c) 200 rotated-source realisations** (`s_n_*`, `p_x`, `cross_profile`).
- The rotated noise matches an analytic shape-noise estimate: MID 0.087–0.095 against 0.088–0.098 (`analytic_shape_noise`).
- Against it, the MID cross-shear offset is

| cell | A_× MID | shape noise σ_n,× | p (200 rotations) | calibrated excess s_× | X2 used |
|---|---|---|---|---|---|
| canonical h 0.672 | +0.205 | 0.091 | 0.015 | 0.180 | 0.205 |
| canonical h 0.686 | +0.236 | 0.096 | 0.010 | 0.212 | 0.236 |
| alt h 0.672 | +0.188 | 0.084 | 0.015 | 0.165 | 0.188 |
| alt h 0.686 | +0.216 | 0.088 | 0.010 | 0.195 | 0.216 |

- In OUTER the cross offset is +0.07–0.08 against a noise of 0.059–0.066 (p 0.24–0.29; excess 0.033–0.043).
- The cross-shear profile (bins 0–7) gives χ² = 19.3 / 19.4 for 8 degrees of freedom against the rotation covariance (p 0.013).
- The jackknife σ of the cross stack (MID 0.113–0.128) is 1.3–1.35 × pure shape noise.

## Step 2: Z_MID and Z_OUT under the three treatments (C\* model; `all.<C*|boost|cell>.<band>.Z_STAT|Z_CAL|Z_CONS`)

STAT = max(bootstrap, jackknife); the bootstrap σ is 4–11 % above the jackknife in MID and within ±6 % in OUTER. CAL = A − A_leak, σ² = σ_STAT² + σ_leak² +
s_×² + s_RR². CONS = X2's (e).

| cell | A_MID | Z_MID STAT | Z_MID CAL (σ) | Z_MID CONS | A_OUT | Z_OUT STAT / CAL / CONS |
|---|---|---|---|---|---|---|
| canonical h 0.672 | 1.640 | +5.21 | **+2.93** (0.218) | +2.70 | 0.932 | −0.78 / −0.72 / −0.57 |
| canonical h 0.686 | 1.684 | +5.47 | **+2.78** (0.246) | +2.58 | 0.931 | −0.80 / −0.77 / −0.60 |
| alt h 0.672 | 1.505 | +4.47 | **+2.52** (0.200) | +2.32 | 0.853 | −1.83 / −1.67 / −1.35 |
| alt h 0.686 | 1.545 | +4.74 | **+2.41** (0.226) | +2.24 | 0.852 | −1.87 / −1.76 / −1.40 |

- **Clipped boost.** Z_MID,CAL is 3.26 / 3.07 / 2.88 / 2.73, so canonical clears 3 and alt does not.
- **C0.** Z_MID,CAL is 3.03 / 2.86 / 2.63 / 2.51.

## Step 3: mass trend (catalogue MGAS500; `trend.terciles|<cell>|<band>|CAL`)

**Noise rule.** The largest quintile σ_STAT,MID is 0.591, above the 0.40 line, so **terciles are graded**. The edges are
7.37e12 and 1.73e13 M☉ (medians 3.3e12 / 1.17e13 / 2.92e13).

| tercile | A_MID CAL (can h0.672 / can h0.686 / alt h0.672 / alt h0.686) | A_OUTER CAL |
|---|---|---|
| T1 | 1.10 / 1.11 / 1.00 / 1.02 (σ ≈ 0.28–0.31) | 0.49 / 0.52 / 0.45 / 0.48 |
| T2 | 1.85 / 1.92 / 1.70 / 1.76 | 0.76 / 0.78 / 0.70 / 0.71 |
| T3 | 1.84 / 1.88 / 1.69 / 1.73 | 1.37 / 1.33 / 1.26 / 1.22 |

| band | Δχ² linear (S1) | Δχ² step (S2) | preferred | lightest bin Z_CAL |
|---|---|---|---|---|
| MID | 2.06 / 1.95 / 2.15 / 2.04 | 4.16 / 4.48 / 4.24 / 4.56 | step (lo 1.00–1.10, hi 1.69–1.89) | +0.22 / +0.24 / +0.01 / +0.04 |
| OUTER | 19.15 / 15.45 / 19.34 / 15.61 | 7.69 / 6.91 / 7.77 / 6.99 | linear (b +1.00 / +0.90 / +0.92 / +0.83 per dex) | −2.27 / −2.18 / −2.69 / −2.62 |

Reported, never graded:
- **CONS.** OUTER Δχ²_S1 is 12.8–13.0 (still ≥ 9). MID Δχ²_S2 is 3.0–3.1.
- **STAT.** OUTER 15.5–19.6; MID 4.9–5.6.
- **Clipped boost.** OUTER Δχ²_S1 is 15.6–19.6; MID Δχ²_S2 is 4.2–4.5.
- **Quintiles.** MID is not monotone: 1.32–1.48 / 1.13–1.24 / 1.67–1.88 / 1.26–1.43 / 2.02–2.26, with σ up to 0.59 in the
  lightest bin. OUTER is 0.59–0.72 / 0.39–0.47 / 0.65–0.72 / 1.16–1.31 / 1.23–1.37 (Δχ²_S1 14.0–16.7).
- **eRASS1 M500 terciles (ΛCDM-processed).** MID rises monotonically, 1.16–1.27 / 1.43–1.63 / 1.84–2.06. OUTER runs
  0.46–0.54 / 0.67–0.74 / 1.27–1.43.

## Against the record (suggested fixes; no other file edited)

1. **X2 (README "(e) Systematics") and MAP §4.** "This is conservative: the cross-shear stack is mostly shape noise" does not
   hold.
   - The shape-noise expectation of the MID cross offset is 0.084–0.096; the offset is 0.19–0.24 (p 0.010–0.015).
   - PSF leakage explains ≤ 0.003 of it.
   - Calibrating keeps ≈ 90 % of the systematic. Suggest: "core-excess Z = 4.5–5.5 statistical, 2.4–2.9 with calibrated
     systematics (MARGINAL), 2.2–2.7 with X2's propagation".
2. **MAP §1.A.3, F1 and CFG687 M1.** The cross shear was quoted at 1.5–2.0σ on jackknife errors. Against pure shape noise it is
   2.2–2.5σ, and the full cross profile fails at p 0.013. Its source is unidentified: it is not PSF leakage, not R−R, and
   partly the random-point cross stack (−0.07). Note too that the jackknife σ of the cross stack exceeds pure shape noise
   by 1.3×.
3. **X2 / MAP §4, "the lightest tercile has no core excess".** The numbers reproduce (MID 1.00–1.11, consistent with 1). But
   the mass dependence of the core excess is not established: the step gives Δχ² 4.2–4.6 < 9 (UNDECIDED), and the quintiles
   are not monotone. Do not cite it as a trend.
4. **CFG687 T2 / X2 V4.** The OUTER mass trend is confirmed. It survives calibrated systematics (Δχ² 15–19) and X2's
   conservative errors (12.8–13.0). Light clusters sit below the law in OUTER at 2.2–2.7σ.
5. F1's jackknife-only Z (4.9–6.2 at C0) is 4–11 % high against max(bootstrap, jackknife) (4.7–5.6).

## Amendments (full text in `FROZEN_CRITERIA.md`)

- **A1 (PRE-RESULT).** Extraction only. E2 was recoded to the frozen statement (THELI_INT is not unique). E3 failed twice on
  memory (astropy's full-column read; the int64 reorder index); both are fixed, and the third run passed.
- **A2 (POST-RESULT for G3 only).** The regression failed G3 three times (1.44 / 1.53 / 1.54 GB), caused by macOS keeping freed
  multi-MB temporaries resident. The fix was 100k-row chunks. The coefficient tables were identical in all four runs.
- **A3 (PRE-RESULT).** The measurement reads columns with `os.pread` and re-executes with `MallocMediumZone=0`. The rotated
  random-point stacks were added before any full run, and one full run was stopped at 25 clusters to add them.
- **A4 (POST-RESULT, K2 only).** K2(b) compared the bootstrap with the population σ, while the one synthetic draw sits 8.6 %
  low. It now uses the sample's σ, with the same 10 % line. RUN1 is kept (`x7_analysis_RUN1_K2.*`); every other line of RUN1
  is identical to the final run.
- **A5 (POST-RESULT, reporting only).** An analytic shape-noise line was added, plus a `--mutate` for the extractor.
- **Implementation (not an amendment).** Bootstrap draws use `default_rng([20261024, selection index])`, so every selection
  has fixed, paired draws.

## Checks

| script | checks | MUTATE |
|---|---|---|
| `x7_extract.py` | E1–E3 PASS (0.90 GB) | E1 FAIL as required (e2 flipped) |
| `x7_psf_regression.py` | G1–G3 PASS (0.54 GB) | G2 FAIL as required (weights dropped) |
| `x7_measure.py` | M1–M6 PASS (547 s, 0.51 GB) | M1 FAIL as required (20 clusters, e2 flipped) |
| `x7_analysis.py` | K0–K5 PASS (33 s, 0.38 GB) | K0 and K3 FAIL as required (cross shear as data; unweighted shape design) |

## What this does not show

- **The cross shear has no identified source.** The CAL rule treats its excess as an isotropic additive systematic with
  equal tangential variance. That is an assumption.
  - A B-mode systematic need not have a tangential counterpart. Without one, Z is the STAT value (4.5–5.5).
  - A systematic correlated with cluster positions could also be larger in the tangential channel.
  - The excess is estimated from a single band offset. If the true systematic were zero, a p ≈ 0.01 fluctuation would give
    the same s_×. So V1 MARGINAL means the data cannot tell these apart, not that a systematic was measured.
- **E-mode systematics tied to cluster positions are not tested.** Blending, the source deficit (the boost < 1), member
  dilution and magnification are seen neither by the cross shear nor by the PSF model.
- **Several calibrations are not re-derived.** The multiplicative bias (m = −0.01), the n(z) calibration (F1's bound only) and
  PSF size leakage are inherited or untested. No star catalogue or ρ-statistics are on disk.
- **The mass proxy is not neutral.** It carries eRASS1's selection; low-mass Mgas500 is the least certain. M500 is
  ΛCDM-processed and is reported only.
- **The model is X2's C\*,** with no new physics: no cluster component, asphericity or measured external field.
- **The step location and pivot are fixed by the record** (X2's tercile edge), not fitted. Another location was not tried
  (stop rule).

## Files and runs (`OMP_NUM_THREADS=1 nice -n 15`)

| file | what |
|---|---|
| `x7_extract.py` → `.out`, `_results.json`, `_MUTATE.*` | own KiDS cache with PSF and tile columns (session scratch, ~1.8 GB, ~9 s) |
| `x7_psf_regression.py` → `.out`, `_results.json`, `_MUTATE.*` | LK-P / LK-T / global leakage fits (~13 s) |
| `x7_measure.py` → `.out`, `_results.json`, `x7_measure_percluster.npz`, `_MUTATE.*` | replay + leakage templates + 200 rotations (~9 min); per-group templates and rotations go to scratch `x7_measure_extras.npz` |
| `x7_analysis.py` → `.out`, `_results.json`, `_MUTATE.*`, `_RUN1_K2.*` | reproduction, three treatments, mass trend, verdicts (~35 s) |

Run order: `x7_extract.py <cache> [<F1 cache>]`, `x7_psf_regression.py <cache>`, `x7_measure.py <cache> <scratch>`,
`x7_analysis.py <scratch>`. Read-only inputs:
- the KiDS FITS (outside the repo)
- the eRASS1 FITS
- X2's source, npz and JSON
- F1's source and JSON
- F2's `f2_aqual.py`
- the Chae+21 CSV
- CFG4_common

Nothing was downloaded.
