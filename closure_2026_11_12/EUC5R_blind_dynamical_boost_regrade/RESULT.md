# EUC5R (BLIND RE-GRADE OF EUC5, DYNAMICAL BOOST): RESULT

2026-11-12. READING bef8d940d8 → code and runs f7db373fa1 → AMENDMENT F1S 871ab16058 (post hoc, alone) → F1S run
10312399b2 → RESULT_BLIND 9b2fac6561 → this file (EUC5 opened only after RESULT_BLIND was committed).
κ = ½ FITTED; not theory closed. No outcome here favours the framework. EUC5 is not relabelled.

## Verdict

**Blind words (canonical / alt).** Frozen route: not re-graded (no SDSS rows available to me; EUC5's own N = 7 < 30).
**A1 as frozen: NOT EVALUABLE / NOT EVALUABLE** (F1 fails: 0.959, 0.891, 0.835 at 150, 250, 350 km/s). Would-be word on
the A1 numbers, the post hoc F1S reading and READING R: NO VERDICT / NO VERDICT, stable over β ±0.2 and seeing
0.9-1.3″. Sample P 35 lenses, S 60. b_med (P, law S, β = 0): **+0.202 [+0.117, +0.267]** canonical,
**+0.197 [+0.112, +0.261]** alt.

**Comparison: AGREES WITH DIFFERENCES THAT DO NOT MOVE A LABEL.** EUC5 has NOT EVALUABLE as frozen and under A1
(F1 FAIL), with b_med +0.196 [+0.110, +0.270] / +0.191 [+0.105, +0.265] on 32 P lenses. Every label matches. The F1
failures have different causes (below), and that is the one difference that matters for anyone using these fits.

## Comparison

**Per-spectrum dispersions (72 spectra fitted by both).** Mine / EUC5: median **1.002**, interquartile 0.997-1.006,
10-90 % 0.994-1.017; 70 of 72 within 5 %. The two outliers (L015227: 1002 against 279 km/s; L008756: 310 against 212)
fail the quality cuts in both lanes. σ_fit agrees to 0.2 %; σ_tpl 69.55 against 69.54 km/s; σ_inst 30.1 against 29.9
km/s. My V is +84 km/s against EUC5's because EUC5 moved the templates to vacuum and I left E-MILES in air; σ is not
affected (ratio 1.002). Errors: mine 3.6 % smaller (median), because I propagate err_fit through the resolution
correction (err_fit·σ_fit/σ).

**Per-lens b_dyn (55 lenses graded by both).** Mine − EUC5 (law S, alt): median +0.0007 dex, sd 0.007, max 0.028.
Stellar masses after the spec-z rescaling agree to 6e-4 dex; b∞ to 5e-4 dex. The Jeans and lensing machinery agree.

**Sample (35 against 32 in P; 60 against 55 in S).** Five lenses are mine only: L016656 (P), the one EUC2 extension
lens, which EUC5's list (flagged only) does not include; L014365 (P), L016695 (P), L003376 (S), L025605 (S), whose
error ratio sits at 0.236-0.245 in my fit and 0.250-0.256 in EUC5's, the 3.6 % error difference above. No lens is
EUC5 only. These five move the P median by +0.006 dex and the S < 1.0″ class from +0.043 to −0.005 (alt).

**Checks.** J3 0.966 both; J4 +0.033 against +0.032; J1 2.4e-4 against 7.1e-4; J2 1.1e-4 against 6.4e-5. Both Newton
twins rise and exit 1 (mine on the DESI P sample, EUC5's on its SDSS sample).

**F1: both fail, for different reasons.**
- Mine: I read A1.5 literally (reference = median-S/N flagged primary, mock at z = 0.45 scaled to that spectrum's flux
  in the z = 0.45 window). The reference is at z = 0.745, so the mock had S/N 1.46 per pixel, 2.4× below the graded
  spectra (3.58). At matched S/N (F1S, post hoc, single-template mock) the same fitter recovers 0.972, 0.963, 1.004:
  inside 5 %.
- EUC5: mock scaled to the reference's own S/N (3.2; effectively my F1S noise), but built from a **mix of two
  templates** (0.6 × 12 Gyr Z = +0.26 + 0.4 × 3 Gyr Z = −0.35) with a 15 % continuum tilt, where A1.5 says "a 10 Gyr solar
  template". Result 0.984, 0.937, 0.913. That departure from A1.5's text is not stated in EUC5's RESULT. It makes the
  gate harder (template mismatch), so it cannot have produced a false pass; it may be why EUC5 fails where my F1S
  passes. Neither lane's gate is met as frozen, so A1 stays NOT EVALUABLE in both.
- Consequence: the mocks bound the fitter's bias at DESI S/N to between −4 % (mine, matched template) and −9 % (EUC5,
  mismatched template) at 250-350 km/s, i.e. 0.03-0.08 dex too low in b if real.

**Real-spectra scale.** Both fitted the same 30 SLACS SDSS spectra. As observed: mine 1.049 [1.014, 1.108], EUC5 1.068
[1.031, 1.122]. At DESI noise: mine 1.057 [0.989, 1.103] (5 draws per lens), EUC5's adopted DESI-fit scale 1.064
[1.016, 1.141]. Scaled readings on P: mine +0.151 / +0.146 (envelope [+0.027, +0.277] / [+0.021, +0.271]), EUC5
+0.138 / +0.133 [+0.051, +0.213] ± 0.066. Same direction and size; I declared the scale before measuring it, EUC5
calibrated post hoc. Both put the fitter about 5-7 % above the published SLACS dispersions, opposite in sign to the
mock bias.

**F2 and F3.** EUC5 found 4 DESI/SDSS pairs (1.11, 0.98, 1.08, 1.52): fewer than 5, so F2 does not gate. My blind words,
which were conditional on F2, therefore stand as written. F3: same three lenses, all secondaries lower in both.

**What explains the differences.** (1) The F1 construction (S/N of the mock and the template used); (2) the extension
lens and the error definition, which add five lenses; (3) air against vacuum templates (V only). None crosses a line:
every P interval in both lanes has its upper bound above 0.15 and its lower bound below 0.25.

**Shared reading, not a gate.** Both lanes find b_dyn rising with Einstein radius (mine, P alt: +0.11 below 1.0″,
+0.17 at 1.0-1.3″, +0.25 above 1.3″), and b_dyn above the source-free lensing bound in the median (P: +0.12 / +0.13).
Both are readings on noisy spectra whose dispersion scale is uncertain by about ±5-7 %.

## Blindness record

- Before READING, the session's start-up context showed recent commit subjects and a memory index, not opened by me.
  They said that EUC8 reads "fibre dispersion from EUC5's DESI fits on its post hoc scale", that a file
  `euc5_a2_scale.json` exists, that EUC5's J3 "lets the boost go negative", and that EUC3 ended NOT EVALUABLE. They gave
  no EUC5 number. READING did not record this; it is recorded here.
- Allowed file AMENDMENT_A1.md gave EUC5's SDSS medians (+0.05 / +0.04) and the count of 39 P lenses (disclosed in
  READING).
- No EUC5 file other than FROZEN_CRITERIA.md and AMENDMENT_A1.md was opened before 9b2fac6561. Nothing was imported from
  EUC1, EUC4, EUC5 or EUC7 code. A55 and A85 scripts were read for their SLACS conventions.

## Unverified

F2 on my side; whether a vacuum conversion changes σ beyond 0.2 % on spectra where the fits disagree; the arc-light
dilution; catalogue n up to 10 taken as given; the SLACS published dispersions as truth.

## Files

`READING.md`, `AMENDMENT_F1S.md`, `RESULT_BLIND.md`; `euc5r_model.py` (Jeans, lensing), `euc5r_checks.py` (.out, .json),
`euc5r_data.py`, `euc5r_fit.py` (stages f1, f1diag, f1s, desi, slacs; outputs `euc5r_f1*`, `euc5r_desi_fits.*`,
`euc5r_slacs*`), `euc5r.py` (`euc5r.out`, `euc5r_results.json`, `euc5r_per_lens.csv`, `*_MUTATE_newton.*`, exit 1).

## Commit ids and the lead's re-run (dated addition, 2026-11-12; no number or label changes)

Local / origin: READING bef8d940d8 / 7b1a1cabd0; code and runs f7db373fa1 / ab8af23bf1; AMENDMENT F1S 871ab16058 /
3b3961f6e7; F1S run 10312399b2 / dc6ba2bcd6; RESULT_BLIND 9b2fac6561 / 391a019c0a; RESULT 4d4f81a2d1 / d280e2fd4b.
Re-run by the lead from a copy of the five scripts, one thread, every stage in order: all seven JSON files, all four
CSV files and both main outputs equal byte for byte; the mutation twin exits 1; the six stage logs equal except the
elapsed-seconds stamps in the DESI fit log. A reproduction, not a further independent re-grade. Blindness checked in the
lane's tool log: the first read of any EUC5 file other than its criteria and A1 came 8 seconds after RESULT_BLIND's commit.
