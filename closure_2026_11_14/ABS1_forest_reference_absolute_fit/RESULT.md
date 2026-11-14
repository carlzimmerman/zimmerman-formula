# ABS1 RESULT (2026-11-14): the forest gate's reference model against the DESI P1D in absolute terms

**As frozen (FROZEN_CRITERIA.md, adefae297a). There is no amendment.**

| footing | fit word | gate word |
|---|---|---|
| canonical | **DOES NOT FIT** | **GATE MOVES**: J4.5 FAILS -> HOLDS |
| alt | **DOES NOT FIT** | **GATE MOVES**: J4 NO VERDICT -> HOLDS; J4.5 FAILS -> NO VERDICT |

In plain words:
- The gate's own reference model does not reproduce the DESI data. Its chi-squared against the data is 13,859 on 714
  points. The gate's line is a change of 4. With one amplitude per redshift bin it is 8,900; with an amplitude and a
  tilt per bin it is 5,802 on 690 degrees of freedom. The line for "fits" was 827, and for "fits with nuisance" 801.
- The model's flux power is 25 to 40 % too LOW at z 2.2 and 15 to 25 % too low at z 2.4. Those two bins carry most of
  every forest D in the record. At z 3 and above the model sits within about 10 % of the data at k 0.01 s/km.
- When the gate's change is scaled by the reference's own power instead of the data, every D falls to 0.55 to 0.76 of
  its stored value. The labels far from the line keep their words. Two labels on alt and one on canonical, all within
  about 2.7 of the gate, change.
- So the record's forest words near the gate (f between about 4 and 4.5) depend on an unchecked step: whether the
  layout's fractional change in flux power should be applied to the data or to the model. The words far from the gate
  do not depend on it. This lane does not say which choice is right.

This is a TEST lane, NOT blind. It tests the gate's MODEL, not the framework. A misfit of the reference is a property of
a 20 Mpc/h real-space fluctuating Gunn-Peterson box with fixed gas parameters. It is not evidence for or against any
layout, the framework, or Lambda-CDM. Nothing is relabelled: FWN1R, FWN2 and every earlier lane keep their labels. The
moved labels are readings under a different scale, and the HOLDS among them is a hit that awaits an independent blind
re-grade, never more. Cold dark energy is a gravitating field component; no particle is added.

## 1. The reference against the data (both footings; the reference is the same layout on both)

Points used: the 714 with k at or above the box's fundamental mode (41 points below it are left out; none lies above
the Nyquist mode). Full data covariance; per-bin rows use that bin's block alone.

| z | N | chi2, no nuisance | chi2, amplitude (A) | chi2, amplitude + tilt (A, alpha) | model / data at k 0.01 / 0.02 / top |
|---|---|---|---|---|---|
| 2.2 | 45 | 2333 | 996 (1.51) | 933 (1.47, -0.07) | 0.71 / 0.73 / 0.75 |
| 2.4 | 48 | 1429 | 820 (1.22) | 813 (1.24, +0.02) | 0.83 / 0.83 / 0.83 |
| 2.6 | 51 | 724 | 612 (1.08) | 506 (1.14, +0.07) | 0.93 / 0.85 / 0.85 |
| 2.8 | 54 | 606 | 575 (1.04) | 547 (1.06, +0.04) | 0.92 / 0.94 / 0.96 |
| 3.0 | 57 | 760 | 683 (0.95) | 316 (1.02, +0.14) | 1.02 / 0.98 / 0.94 |
| 3.2 | 60 | 1015 | 612 (0.89) | 215 (0.97, +0.14) | 1.04 / 0.99 / 0.94 |
| 3.4 | 62 | 1878 | 983 (0.84) | 259 (0.95, +0.20) | 1.10 / 1.00 / 1.00 |
| 3.6 | 64 | 447 | 231 (0.90) | 120 (0.95, +0.12) | 1.05 / 0.95 / 0.89 |
| 3.8 | 66 | 553 | 308 (0.83) | 110 (0.95, +0.21) | 1.07 / 0.98 / 1.04 |
| 4.0 | 67 | 296 | 146 (0.87) | 81 (0.93, +0.15) | 1.10 / 0.97 / 0.87 |
| 4.2 | 69 | 131 | 108 (0.92) | 70 (0.97, +0.18) | 1.10 / 0.87 / 0.85 |
| 4.4 | 71 | 139 | 116 (0.89) | 105 (0.92, +0.14) | 1.36 / 0.77 / 0.98 |
| **total, joint** | **714** | **13,859** (dof 714) | **8,903 / 8,901** (dof 702) | **5,802 / 5,803** (dof 690) | |

Canonical figures shown per bin; alt agrees to better than 0.1 %. Totals are canonical / alt where they differ. The
total is the joint fit with the full covariance (cross-bin terms kept), so it is not the sum of the rows. No tilt
reached its bound of +/- 1; the unbounded tilt gives the same numbers.

Variants (reported, never the word), canonical (alt within 0.1 %):

| variant | N | no nuisance | A | A + tilt |
|---|---|---|---|---|
| all 755 points, model held flat below k_f | 755 | 16,255 | 10,513 | 7,646 |
| 714 points, seed scatter of the model added to the covariance | 714 | 5,282 | 2,741 | 1,939 |
| only k >= 3 k_f | 585 | 3,754 | 1,858 | 1,696 |
| (re-check) linear-in-k interpolation instead of log-log | 714 | 17,162 | | |
| (re-check) model from seeds 0, 1 only / 2, 3 only | 714 | 12,874 / 16,114 | | |

Every variant is far above its line. The box's absolute power is noisy from seed to seed at the level of the data's own
errors (adding that scatter cuts chi2 by a factor of 2.6); the gate's ratio of seed sums cancels most of that noise, an
absolute fit cannot.

Gas brackets at the anchors (z 2.2, 3.0, 4.4; seeds 0 and 1; 173 points; chi2 no nuisance / A / A + tilt):
primary 3060 / 1668 / 1369; lambda_P x 0.5 2969 / 1625 / 1322; x 2 3712 / 1874 / 1445; gamma 1.2 3635 / 1733 / 1422;
gamma 1.6 2819 / 1573 / 1359; tau_eff x 0.9 3978 / 1681 / 1364; x 1.1 3426 / 1666 / 1373; lambda_P 91.4 kpc
3163 / 1697 / 1384; 138.6 kpc 3574 / 1822 / 1430. No frozen bracket comes near the line (about 173 to 210). The best,
gamma 1.6, improves the no-nuisance number by 8 %.

## 2. The gate with the reference's own power

d' = (r - 1) x P_ref,model at all 755 points; below the fundamental the model is held at its first mode. SE' by the
graders' jackknife. Labels by the graders' rule with the stored known-answer and twin status.

| case | footing | stored D (SE) | D' (SE') | D' / D | stored label | label with the model's power |
|---|---|---|---|---|---|---|
| J3 | canonical | 0.572 (0.044) | 0.320 (0.019) | 0.56 | (reported) | (reported) |
| J3.5 | canonical | 1.498 (0.087) | 0.861 (0.039) | 0.57 | HOLDS | HOLDS |
| J4 | canonical | 3.178 (0.155) | 1.888 (0.071) | 0.59 | HOLDS | HOLDS |
| J4.5 | canonical | 5.617 (0.227) | 3.450 (0.095) | 0.61 | FAILS | **HOLDS** |
| J5 | canonical | 8.834 (0.333) | 5.593 (0.144) | 0.63 | FAILS | FAILS |
| J10 | canonical | 194.47 (5.20) | 135.11 (3.51) | 0.69 | FAILS | FAILS |
| Jinf | canonical | 214.99 (5.23) | 157.58 (3.54) | 0.73 | FAILS | FAILS |
| C | canonical | 323.05 (4.48) | 244.02 (1.74) | 0.76 | (control) | (control) |
| U4 | canonical | 4.417 (0.391) | 2.788 (0.265) | 0.63 | (reported) | (reported) |
| J3 | alt | 0.691 (0.047) | 0.381 (0.021) | 0.55 | (reported) | (reported) |
| J3.5 | alt | 1.781 (0.099) | 1.020 (0.050) | 0.57 | HOLDS | HOLDS |
| J4 | alt | 3.712 (0.161) | 2.207 (0.084) | 0.59 | NO VERDICT | **HOLDS** |
| J4.5 | alt | 6.623 (0.291) | 4.061 (0.163) | 0.61 | FAILS | **NO VERDICT** |
| J5 | alt | 10.897 (0.564) | 6.813 (0.337) | 0.63 | FAILS | FAILS |
| J10 | alt | 288.01 (6.75) | 198.87 (4.46) | 0.69 | FAILS | FAILS |
| Jinf | alt | 314.69 (7.25) | 229.36 (4.98) | 0.73 | FAILS | FAILS |
| C | alt | 395.83 (8.54) | 300.26 (6.27) | 0.76 | (control) | (control) |
| U4 | alt | 4.250 (0.359) | 2.621 (0.238) | 0.62 | (reported) | (reported) |

Stored labels as in FWN2 / FWN1R (base word; every one from f 3.5 to 4.5 also carries FRAGILE).

- **Ceiling on f** (where the quantity equals 4, log-linear between run points; reported): canonical D + 2 SE 4.12 ->
  4.59, D 4.19 -> 4.65, D - 2 SE 4.28 -> 4.70; alt 3.99 -> 4.42, 4.06 -> 4.49, 4.14 -> 4.57. The ceiling rises by
  about 0.45 in f on both footings.
- **The amplitude-refit model** as the scale (the reference times its fitted amplitude per bin) brings D back to 0.94
  to 0.98 of the stored value (J4.5 5.38 / 6.46). The move is the reference's amplitude deficit at z 2.2 to 2.6, where
  the per-bin D is concentrated, and nothing else.
- **Bracket estimates with D'** (reported): J4 canonical lambda_P x 0.5 11.75, x 2 0.127; gamma 1.2 0.117, 1.6 6.30;
  tau x 0.9 2.25, x 1.1 1.61. J4.5 canonical 19.85, 0.268, 0.499, 11.93, 4.09, 2.95. Every label stays FRAGILE in the
  same way: the gas brackets still move D by factors of 50 to 100.

### How hard the "moves" was checked

A second script (`abs1_verify.py`, a separate code path: direct `np.linalg.solve`, its own loops) reproduces every D'
and SE' to the printed digits, and gives:

| case, footing | model held (primary) | linear-in-k model | data at the 41 uncovered points | model seeds 0, 1 | model seeds 2, 3 |
|---|---|---|---|---|---|
| J4.5 canonical, D' +/- 2 SE' | 3.64 / 3.26 HOLDS | 3.75 / 3.35 HOLDS | 4.13 / 3.56 NO VERDICT | 3.57 / 3.21 HOLDS | 3.72 / 3.32 HOLDS |
| J4 alt | 2.37 / 2.04 HOLDS | 2.44 / 2.10 HOLDS | 2.70 / 2.22 HOLDS | 2.32 / 2.01 HOLDS | 2.43 / 2.08 HOLDS |
| J4.5 alt | 4.39 / 3.73 NO VERDICT | 4.48 / 3.82 NO VERDICT | 4.76 / 3.95 NO VERDICT | 4.34 / 3.70 NO VERDICT | 4.45 / 3.78 NO VERDICT |

- The stored label of all three changes under every variant: no variant gives J4.5 FAILS on either footing, and none
  gives J4 alt NO VERDICT. So "moves" does not depend on the interpolation, on the seeds, or on the treatment of the
  points below the box's fundamental mode.
- What the new label is does depend on those choices for canonical J4.5: HOLDS in four variants, NO VERDICT when the
  data stand in for the model below the fundamental. The FAILS-to-HOLDS crossing is therefore not firm; the departure
  from FAILS is.
- The 41 points below the fundamental, where the box holds no mode and the grader holds r flat, carry about 10 % of D'
  (J4.5 canonical 3.45 against 3.85).
- The six labels far from the gate (J3.5 HOLDS; J5, J10, Jinf FAILS) do not change in any variant. The unchanged words
  were checked as hard: J5's D' - 2 SE' stays at 5.25 or above (canonical) and 6.12 or above (alt), J3.5's D' + 2 SE'
  at 1.33 or below.

## 3. Known answers and twins (all before any new number was read)

The known answers were run first in a separate pass (output not kept) with no new number computed; all passed, then
the full run was made.

- KA1 loader: 755 points, md5 33d7fc21bfd3d745ed71a0bbe80ca433. PASS.
- KA2 stored D and SE reproduced from the parts with the data as scale, 10 cases per footing (J3.5, J4, J4.5, J5, U4
  from FWN2's parts; J3, J5, J10, Jinf, C from FWN1R's): relative difference 0 in every case (J4 3.178241 / 3.712255,
  J5 8.833894 / 10.896713). PASS.
- KA3 data as model: chi2 0, amplitudes 1 to 3e-15, tilts 0 to 3e-17. PASS.
- KA4 mean flux: |meanF - target| at most 2.1e-14 over 985 fields per footing; target equals exp(-s tau_eff(z)) exactly.
  PASS.
- KA5 the reference in FWN2's parts equals FWN1R's in all 48 files per footing (difference 0). PASS.
- TW1 model x 1.2: chi2 rises by 14,461.93, the hand formula 0.44 m'C^-1m - 0.4 m'C^-1P gives 14,461.93 (relative
  4e-15); data x 1.2 gives 8,727.18 = 0.04 P'C^-1P (P'C^-1P = 218,180). Bites.
- TW2 amplitude nuisance on 1.2 x model returns the unscaled chi2 (relative 0) with every amplitude divided by 1.2
  (3e-15); on 1.2 x data it returns 7e-25. Bites.
- TW3 a tilt of 0.1 put into the model is absorbed by the amplitude-and-tilt fit (relative 7e-16). Bites.
- TW4 gate scale 1.2 x data gives D' = 1.44 D to 7e-16 in every case. Bites.

## 4. Hand estimate against the result

| item | estimate (frozen) | result | landed? |
|---|---|---|---|
| fit word | DOES NOT FIT 80 % | DOES NOT FIT, both | yes |
| chi2 no nuisance | above 10^4, 70 % | 13,859 | yes |
| amplitude fit | falls by 3 to 10, stays above 800 | falls by 1.56, 8,903 | stays above, yes; the fall was smaller |
| amplitude + tilt | above 801, 70 % | 5,802 | yes |
| model / data near k_f | low by 20 to 50 % | low by 25 to 40 % at z 2.2 to 2.4; HIGH by 10 to 40 % at z 3.0 and above | half right |
| model / data at the top k | off 10 to 50 %, more likely high | low by up to 25 % in most bins | sign wrong |
| D' / D | central 1.2, range 0.6 to 2.3 | 0.55 to 0.76 | below the central guess, at the low edge |
| gate word | GATE MOVES 80 % | GATE MOVES, both | yes |
| a HOLDS / FAILS crossing | 30 % | canonical J4.5, primary only; NO VERDICT in one variant | yes, not firm |
| P'C^-1P | 10^5 to 10^6 | 2.18 x 10^5 | yes |

I expected the real-space box to have too much small-scale power. It has too little at z 2.2 at every k, and too little
at the highest k in most bins. The gate's scale error therefore runs the other way from my guess: the stored D are too
large, not too small.

## 5. What this does and does not say

- **It says** that the gate's premise, "the reference reproduces the data", is false for build B's box by a wide
  margin (chi2 13,859 on 714 points), and that the margin is not removed by one amplitude and one tilt per bin, nor by
  any frozen gas bracket.
- **It says** that labels within about 2.7 of the gate depend on whether the layout's fractional change is applied to
  the data or to the model: the f ceiling moves from about 4.1 to about 4.5 (canonical) and from about 4.0 to about 4.4
  (alt). Labels far from the gate (f 3.5 holds; f 5, f 10, no settled radius fail) do not.
- **It does not say** which scale is right. Applying the model's fractional change to the data assumes the fractional
  response is right even where the absolute level is wrong. Applying it to the model assumes the absolute change is
  right. A box that fits the data in absolute terms (redshift space, a larger box, calibrated gas) would be needed to
  choose; none was computed here.
- **It does not say** anything for or against the framework, any layout, or Lambda-CDM. It relabels nothing; the record
  keeps FWN1R's and FWN2's words.
- **Not covered:** redshift-space distortions, larger boxes, more seeds, T0 brackets, metal and DLA contamination of the
  data, and the build-A box of FRZ6 / FWN1 (not read here).

## 6. What looked wrong or worth flagging in the library and graders

- The gate multiplies the DATA by a model ratio. The model's own level is 25 to 40 % below the data at z 2.2, the bin
  that carries most of every D. Nothing in the record checked this; this lane is the check.
- 41 of the 755 points lie below the box's fundamental mode. `at_points` holds r flat there and they still enter the
  gate with full weight; in D' they carry about 10 %.
- The absolute P1D of a 20 Mpc/h box at N 384 varies between seed halves by 25 % in chi2 against the data; the gate's
  ratio estimator hides that, which is its purpose, but it also means the absolute level was never constrained.
- Nothing in the code looked like a bug: every stored D was reproduced exactly, and the stored spectra are what the
  code says (real-space flux contrast, km/s, angular s/km, box-mean normalised, mean flux on target).

## 7. Procedure

- Criteria committed alone (adefae297a) before any script existed. Scripts and outputs: affd4d69ad. No amendment.
- Light compute: one process, one thread, nice 19; each run took a few minutes at most; the known-answer pass peaked at 0.26 GB resident.
  Free disk 13 GB, swap used 4.9 GB at start.
- Files: `abs1.py` -> `abs1.json`, `abs1.out`, `abs1_MUTATE.json`, `abs1_MUTATE.out`; `abs1_verify.py` ->
  `abs1_verify.out` (second path, reported). No file of another lane was written.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
