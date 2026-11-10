# CO2 RESULT: form B's clustering amplitude, pinned with large-angle polarisation, against lensing

**AMPLITUDE EXCLUDED BY RAW KiDS AT 3 SIGMA / the same (canonical / alt), by the frozen rule, for form B as stated
(gravity-only S0, nothing ejecting gas beyond R200c; inherited halo list in R). The label is not robust: p is 0.0026 /
0.0021 against a line of 0.0027, and a check made after grading moves it to TENSION.** The rest holds: the pinned fit is
adequate, the CMB lensing amplitude now sits 0.30 sigma from the prediction, and the growth rate passes.

TEST lane, quarantined. Adopts nothing, relabels nothing, registers nothing. Kappa = 1/2 FITTED; not theory closed. Footings
graded separately, never pooled. Cold dark energy; no particle. Criteria 2bd776c60d; amendment A1 b6dd6d0641 (a tolerance,
before any graded number). Nothing was downloaded: the low-L table was already on disk.

## What came out

1. **The pin works.** Adding the Planck 2018 low-L EE table moves tau from 0.070 / 0.073 to **0.0532 +- 0.0066** on both
   footings and sigma8 from 0.8405 / 0.8429 to **0.8271**. The high-L fit pays +1.17 / +1.07; the low-L table gains 6.37 /
   8.26. The cold amount does not move (5.411 / 5.412 times the baryons).
2. **CMB lensing is now on the prediction.** PR4 bandpowers read 0.9928 +- 0.0239 of the predicted amplitude (-0.30
   sigma; it was -1.66 / -1.89 unpinned). chi^2 at A = 1 is 8.64 for 9 bandpowers.
3. **The growth rate passes** (chi^2 1.95 / 2.14 over four DESI DR1 bins).
4. **Weak lensing is where it fails.** For form B's spectrum, raw KiDS-1000 is best at sigma8 **0.736 +- 0.016** (0.735 to
   0.745 across every variant below). The pinned fit gives 0.827, and 0.815 with one 0.06 eV neutrino. That is 5.1 to 5.8
   KiDS widths (4.3 to 5.0 with the neutrino), Delta chi^2 +30 to +39 for one parameter. This gap is the robust statement.
5. **The absolute-fit label is at its line and does not survive a check.** As frozen: chi^2 157.89 / 159.35 on 104
   points, p 0.0026 / 0.0021. Found after grading: the reference run is one box of 100 Mpc/h whose large-scale power is a
   high draw. With that taken out four ways, p is 0.003 to 0.013 (TENSION). See "Post hoc" below.

## The table (co2.json, co2.out)

| row | canonical | alt | line |
|---|---|---|---|
| tau (width along the A_s exp(-2 tau) direction) | 0.0532 +- 0.0066 (was 0.0697) | 0.0532 +- 0.0066 (was 0.0729) | reported |
| ln 1e10 A_s | 3.0432 (was 3.0752) | 3.0432 (was 3.0811) | reported |
| chi^2: PA / low-L EE (change from unpinned) | 3741.33 (+1.17) / 395.95 (-6.37) | 3741.38 (+1.07) / 395.95 (-8.26) | reported |
| **P1** pinned fit adequate, Delta_cal' | -63.79 **PASS** | -63.75 **PASS** | <= 9 |
| sigma8; S8 | 0.8271; 0.8481 | 0.8271; 0.8481 | reported |
| **P2** PR4 lensing amplitude, data / prediction | 0.9928 +- 0.0239 (-0.30 sigma) **PASS** | 0.9929 +- 0.0239 (-0.30 sigma) **PASS** | within 2 sigma |
| P2 shape chi^2; chi^2 at A = 1 | 8.55; 8.64 | 8.55; 8.64 | <= 18.48 |
| **P3** DESI DR1 f sigma8, chi^2 ShapeFit / + BAO | 1.95 / 2.14, largest pull 1.13 **PASS** | 1.95 / 2.14, 1.13 **PASS** | every pull <= 2 |
| **P4** raw KiDS-1000, S0 x R_tot, the run's own response | chi^2 157.89, p 0.0026 **EXCLUDED AT 3 SIGMA** | chi^2 159.35, p 0.0021 **EXCLUDED AT 3 SIGMA** | p >= 0.05 / >= 0.0027 |
| constant factor (bracket) | 153.74, p 0.0044 | 155.04, p 0.0037 | bracket |
| S0 alone / S0 x R_bar, own response | 156.88 / 156.18 | 156.85 / 156.16 | reported |
| KiDS's own best sigma8 for this spectrum | 0.7358 +- 0.0162 (chi^2 120.37, p 0.147) | 0.7341 +- 0.0161 (120.00, p 0.152) | reported |
| pinned minus best, in KiDS widths; Delta chi^2 | +5.62; +37.52 | +5.78; +39.36 | reported |
| bracket: one 0.06 eV neutrino (sigma8 0.8152) | 148.05, p 0.0090 | 149.20, p 0.0077 | bracket |
| bracket: prefactor-0 layout | 150.43, p 0.0057 | 151.17, p 0.0055 | bracket |
| bracket: unpinned sigma8, own response | 170.95, p 0.0004 | 175.47, p 0.0002 | bracket |
| DES Y3 at the pinned amplitude (52 points) | 74.69, p 0.050 | 74.67, p 0.051 | reported |

- Both footings land on the same parameters because the footing rule gives both the same h (0.6741 / 0.6740).
- P1's two parts: the high-L fit is 64.04 / 63.99 below the calibration point, the low-L table 0.24 above it.
- The two Nelder-Mead starts end at 4137.32 / 4137.37 (tau 0.0532) and 4137.42 / 4137.53 (tau 0.0550; that start used all
  250 evaluations). The lower is taken. The tau width is along one direction with the other parameters held, so it
  understates the profile width.
- KiDS's best sigma8 here, as S8 at this Omega_m, is 0.754 +- 0.017. The survey's own published values (0.76 to 0.77, quoted from
  memory) are close to that, which is a check on the machinery and not a new measurement.
- With a 0.06 eV neutrino at the pinned parameters (not a refit) sigma8 is 0.8152 and PR4 lensing reads +0.40 sigma.

## Post hoc: the reference run's realisation noise (co2_posthoc.py; reported, changes no label)

Found after P4 was graded. CFG596's S0 run is a single box of 100 Mpc/h. Its starting spectrum over its own linear spectrum
is 0.80, 1.03, **1.48**, 1.01, 1.06 in its first five bins (k = 0.08 to 0.32 h/Mpc), and the pattern is still there at
z = 0. A difference of two models on the same run (CO1's d_cold) cancels this. An absolute fit does not, and P4 is an
absolute fit. I did not think of it before the freeze.

| P4 with the realisation taken out | p at the pinned amplitude (can / alt) | would read | KiDS best sigma8 | pinned away by | with the neutrino |
|---|---|---|---|---|---|
| as graded | 0.0026 / 0.0021 | EXCLUDED AT 3 SIGMA | 0.7358 / 0.7341 | 5.62 / 5.78 widths | 4.89 / 5.04 |
| R1: divided by the run's own starting ratio (full to k 0.3, none above 1) | 0.0060 / 0.0049 | TENSION | 0.7391 / 0.7373 | 5.36 / 5.52 | 4.63 / 4.79 |
| R1b: the same, full to k 0.2, none above 0.5 | 0.0058 / 0.0047 | TENSION | 0.7390 / 0.7371 | 5.37 / 5.54 | 4.65 / 4.80 |
| R2: CFG411's 200 Mpc/h S0 run below k 0.5 | 0.0127 / 0.0102 | TENSION | 0.7454 / 0.7435 | 5.08 / 5.25 | 4.34 / 4.51 |
| R2b: CFG424's 200 Mpc/h S0 run (seed 360) below k 0.5 | 0.0042 / 0.0034 | TENSION | 0.7367 / 0.7349 | 5.55 / 5.71 | 4.82 / 4.97 |

- The 3 sigma line is crossed only by the uncorrected run. Every correction reads TENSION, with p from 0.003 to 0.013.
- The amplitude gap hardly moves: 5.1 to 5.8 widths, Delta chi^2 +29.6 to +39.4.
- The widths are KiDS's alone. Adding the pin's own width (sigma8 +- 0.0055 from tau, the other parameters held) makes
  the gap about 4.8 to 5.5 combined widths, 4.1 to 4.8 with the neutrino.
- **CO1's absolute KiDS p values carry the same noise** (its S0 row, p 0.014, reads 0.021 to 0.049 with the corrections).
  CO1's label rests on d_cold, a difference, and is not affected.

## What this does and does not say

- **Solved by the pin:** the CMB lensing amplitude. With tau held by raw large-angle polarisation, form B's primary fit
  predicts the PR4 lensing power to 0.3 sigma.
- **Not solved:** the weak-lensing amplitude. Form B as stated (a gravity-only spectrum, massless neutrinos) over-predicts
  raw KiDS shear, and no layout bracket of CO1 relieves it (the prefactor-0 layout gains chi^2 7.5 / 8.2 and stays at p 0.006 / 0.005).
- **It is not peculiar to form B.** Any cold-component fit to the CMB carries this tension; the usual ways out are gas
  expelled from haloes and neutrino mass, and form B states neither. The neutrino bracket alone moves p to 0.008 to 0.009
  as graded.
- **The absolute-fit label should be read as "3 sigma as frozen, TENSION once the reference run's realisation is
  corrected".** I would not quote the exclusion without the second half.

## Known answers and MUTATE

- KA1: the transcribed low-L EE reader at the package's published test point: 396.040 against 396.04.
- KA2: F1A's calibration cosmology replays 3805.368; F1A's best fits replay with the low-L term off to 8e-9 / 5e-6.
- KA3 (tolerance 0.25 by A1; as frozen 0.1): interpolated minus exact chi2_E at the pinned fits +0.044 / +0.050. It
  passes the frozen 0.1 too; the amendment was written on the +0.11 seen at the test point.
- KA4: the shear path reproduces CO1 (162.04 / 165.18 with the constant factor at CO1's sigma8; 144.95 / 146.01 at f = 1).
- KA5: the response is 0.96, 0.98, 0.99 in the one bin below k 0.12 at the three nodes (within 0.15 of 1).
- **M1 bites:** tau forced to 0.10 raises chi2_E by 30.8. **M2 bites:** sigma8 0.90 gives p 7e-11 / 3e-11.
  **M3 bites:** the response gives 157.89 / 159.35 against the constant factor's 153.74 / 155.04.
- Reported check (`co2_check_replay.py`): both pinned fits replayed in a fresh process to 1e-7 in PA and exactly in chi2_E.

## The response

alpha(k) = d ln P / d ln D^2 from the S0 run's own snapshots: 1.01 at k 0.1, 1.07 at 0.2, 1.36 at 0.3, 1.58 at 0.5, 1.45 at
1, 1.55 at 2 to 3 (node z 0); nodes 0 and 0.5 differ by at most 0.48. The pinned move is a factor 1.040 in the linear
spectrum, so a change of 0.48 in alpha is 1.9 % in the moved spectrum at worst. The constant factor (alpha = 1) understates
the move, as the criteria said: it gives p 0.0044 / 0.0037.

## Hand estimate against the outcome

Written before any code: tau 0.055 to 0.060 (found 0.0532); sigma8 about 0.828 (0.8271); PR4 lensing within 1 sigma
(-0.30); raw KiDS p about 0.004 with the constant factor (0.0044 / 0.0037) and lower with the response, the label near the
line between TENSION and EXCLUDED AT 3 SIGMA (0.0026 / 0.0021, just below it). P4's lines were chosen with CO1's p values
in view; that was disclosed and it shows.

## Limits

- One reference run, gravity-only, 104 of 225 published KiDS points; the realisation noise above.
- The response treats a change of amplitude as a change of epoch at fixed linear shape.
- F1A's massless-neutrino setting is kept in the fit; the neutrino row is a bracket at fixed parameters.
- The low-L table is Planck 2018 (SimAll), the high-L spectra PR4. The low-L TT table on disk was not used.
- The halo list in R is inherited (CO1's criteria). The layout is put in by hand (the decision's open item 1).
- The cold amount is fitted from the acoustic peaks; nothing here is independent evidence for the framework.

## Files

- `FROZEN_CRITERIA.md` (2bd776c60d), `AMENDMENT_A1.md` (b6dd6d0641).
- `co2_fit.py <footing>` -> `parts/fit_<footing>.json` (958 s / 908 s; 485 / 456 evaluations).
- `co2_rows.py` -> `co2_rows.json`, `co2_rows.out`: KA1 to KA3, P1 to P3 (19 s).
- `co2_shear.py` -> `co2_shear.json`, `co2_shear.out`: P4, brackets, scan (151 s).
- `co2_grade.py` -> `co2.json`, `co2.out`.
- `co2_check_replay.py` -> `co2_check_replay.out`. `co2_posthoc.py` -> `co2_posthoc.json`, `co2_posthoc.out` (493 s).
- Read-only: F1A's likelihood and stored fits, QX3 iter2's PR4 loader, CFG592's library part, CFG596's S0 run, CFG411's
  and CFG424's S0 runs (post hoc), CO1's outputs, the Planck 2018 low-L EE table (outside the repository).
