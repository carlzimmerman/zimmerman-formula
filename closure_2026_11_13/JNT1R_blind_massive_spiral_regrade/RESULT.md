# JNT1R RESULT: blind re-grade of JNT1 row S, and the comparison

**Blind label (unchanged from RESULT_BLIND.md, 754a7e120f): canonical (9 galaxies) REFERENCE FAILS AT THE RECORD SHARE
[L2 shape; L3 scatter], FRAGILE; beside it THE LAW FITS, FRAGILE. Alt (2 galaxies) NO POWER (n < 5); beside it THE LAW
FAILS [L2 shape], FRAGILE. Best-fit multiple of the record's halo (canonical, U 0.50) A = 0.58, 95 % [0, 1.69],
68 % [0.03, 1.13].**

TEST lane: adopts nothing, relabels nothing, registers nothing. Reading 543118d9b8 (alone); scripts and outputs
e29b235cfb; RESULT_BLIND 754a7e120f; JNT1's RESULT.md and outputs were opened only after that commit. Footings never
pooled. Cold dark energy is a gravitating field component; no particle. Nothing here says the data favour the framework.

## Comparison with JNT1's row S (RESULT.md 317b948cf5, outputs b5731fd9a5)

| quantity (canonical, fixed U 0.50 unless said) | JNT1 | JNT1R (own code) |
|---|---|---|
| members, points | 9, 249 | 9, 249 |
| reference A = 1: offset (se) | -0.028 (0.041), holds | -0.028 (0.041), holds |
| reference A = 1: shape (se) | -0.087 (0.021), FAILS | -0.087 (0.021), FAILS |
| law + T: offset ; shape | -0.009 ; -0.037, holds | -0.009 ; -0.037, holds |
| A = 0: offset ; shape | +0.271 ; +0.196 | +0.271 ; +0.196 |
| pooled scatter, fixed U (JNT1's S3, +0.02 line) | ref 0.1265 vs law 0.1065: FAILS by 3e-5 | not graded at fixed U |
| pooled scatter, record's fit mode (my L3, PD1 +0.010 line) | ref 0.105 vs law 0.052 (reported) | ref 0.105 vs law 0.052: FAILS |
| half the halo | TW-H (X / 2): off -0.006, shape -0.030, REFERENCE FITS | A 0.50 (post hoc): off -0.006, shape -0.030, fit-mode rms 0.052: all lines hold |
| double the halo | TW-D: off -0.093, shape -0.142, FAILS | A = 2 outside the 95 % interval |
| U 0.35 ; U 0.65 ; U fit | +0.031 / -0.143 ; -0.120 / -0.044 ; -0.018 / -0.074 | identical |
| alt offset / shape (ref ; law + T) | +0.043 / -0.100 ; +0.097 / -0.056 | identical |
| row word as frozen | NO POWER (TW-H does not bite) -> NO VERDICT | REFERENCE FAILS AT THE RECORD SHARE, FRAGILE |

**Every shared number agrees to the printed digit.** The two lanes share the record's loader, weights, U convention
and halo recipe; my halo code is my own and reproduces SRJ3's zC 400569 to 1e-7 and SRJ2's membership from its own
v_vir. So this is an independent re-computation, not an independent dataset.

**The words differ only because the frozen power rules differ.** JNT1 required the halved-halo twin to make the row
fail; it did not (half the halo fits), so JNT1 had to say NO POWER. I froze power as "the 95 % interval on A excludes at
least one of 0, 1, 2"; it excludes 2, so the row has power, A = 1 is inside, and the reference fails on the shape and
scatter lines. Neither rule is wrong. JNT1's is stricter about mass resolution; mine asks whether the curves can weigh
the halo at all. My FRAGILE comes from members JNT1 did not have (distance and inclination moved, a delete-one
jackknife) and from my interval widening at U 0.35, D - eD, i - eInc and two jackknife samples (word -> NO POWER).
No member gives REFERENCE FITS at the record share. JNT1's S3 failure at fixed U is a knife-edge (3e-5); in the record's
fit mode the scatter failure is not marginal (0.105 against 0.052 + 0.010), in every bracket member and jackknife sample.

**JNT1's ungraded reading stands, with two qualifications.** The reference at the record share over-predicts the outer
curves: all 9 reference shapes are negative (-0.025 to -0.169). About half the halo fits: A 0.40 to 0.58 pass all three
lines; the joint best A is 0.58, the per-galaxy median 0.44, and in the record's fit mode A 0.43 [0.33, 0.53].
Qualifications: (1) the graded 95 % interval [0, 1.69] does not exclude A = 1, because the galaxies disagree. ESO563-G021
wants A >= 5 (grid edge) and UGC02487 about 2, while NGC5371 wants 0.13. So "half" is a population median, not a property
of each curve. The failure at A = 1 is in shape and scatter, not in the amount. (2) The law also has a negative shape
here (-0.037; -0.031 without T fails 3 se). Part of the outer over-prediction is common to every layout on these discs at
fixed U, and the reference roughly doubles it.

## Alt

Both lanes: two galaxies, NO POWER, same offsets and shapes. Both shapes are negative under the reference. They cannot
give a population offset, a robust scatter or a jackknife. My chi2-only band on A ([1.52, 2.35] at U 0.50, [0.60, 0.76]
in fit mode) moves with U by more than its width, so it means nothing on its own.

## Blindness

Nothing of JNT1's outputs or RESULT was seen before 754a7e120f. Before freezing, the lane brief gave JNT1's ungraded
reading in words ("the reference layout over-predicts the outer curves at the record share and about half the halo
fits"), without numbers. This is recorded in READING.md. So my agreement on the reading is not fully blind. The numbers,
the shape statistic and the power rule were computed and frozen without JNT1's.

**Commit ids and the lead's re-run (added 2026-11-13, after landing; no number or label changes).** Local / origin:
READING 543118d9b8 / 9195085721; scripts and outputs e29b235cfb / 5d40824041; RESULT_BLIND 754a7e120f / f99d9d4d2e; RESULT 471ff93785 /
a9d6811b66. Pushed. The lead session re-ran `jnt1r.py` (MAIN, MUT_C, MUT_E) and `jnt1r_light.py` from a copy at the same
folder depth, one thread: all eight output files are equal byte for byte. That is a reproduction, not a further
independent re-grade. As this file's READING records, the lead's brief stated JNT1's ungraded reading in words before
the freeze, so the agreement with that reading is not fully blind; the numbers were computed blind.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
