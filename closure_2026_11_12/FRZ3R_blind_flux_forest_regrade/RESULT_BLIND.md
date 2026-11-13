# FRZ3R RESULT_BLIND: the forest row at flux level, blind re-grade

Written and committed before opening any FRZ3 result file. TEST lane: adopts nothing, relabels nothing, registers nothing.
Footings never pooled. Cold dark energy is a gravitating field component; no particle is added. Nothing here says the data
favour the framework.

## Labels

**As frozen (READING.md 4abb5b4a36, graded field M): NO VERDICT / NO VERDICT (canonical / alt).**

- Canonical: known answer (b) fails at z 2.2, k 3, and (e) fails at z 4.4 (seed scatter 0.0059 against E / 3 = 0.0057).
- Alt: known answer (b) fails at z 2.2, k 3 and k 5.
- The graded field also has 6.7 / 7.4 % of its gas pixels negative (floored to full transmission). This is not a frozen
  known answer, but it makes field M unphysical (AMENDMENT_A1, 5f39677e97).
- Ungraded numbers, reported only:

| footing | flux-level Delta chi^2 (12 bins) | matter-level Delta chi^2, same fields, record projection | ratio |
|---|---|---|---|
| canonical | 789.94 | 10815.6 | 0.073 |
| alt | 904.18 | 9671.8 | 0.093 |

  Every frozen bracket stays above the gate. The lowest are clustered placement 112 / 136 and lambda_P = 100 proper kpc
  267 / 184.

**Reading T (AMENDMENT_A1; reported, NOT the frozen label): FOREST ROW FAILS AT FLUX LEVEL / FOREST ROW FAILS AT FLUX LEVEL.**

- Reading T is the turnaround-scope halo model realised on its own terms. It is positive by construction (floored fraction
  at most 1.5e-4). Every one of its known answers passes and both of its mutations bite.

| footing | flux-level Delta chi^2 | matter-level Delta chi^2, same fields | ratio |
|---|---|---|---|
| canonical | 363.26 | 5035.1 | 0.072 |
| alt | 424.50 | 4376.9 | 0.097 |

- Its three brackets are all above the gate: lambda_P x 0.5, x 2 and 100 proper kpc give 1224 / 90.4 / 35.7 (canonical)
  and 1398 / 98.9 / 36.6 (alt).
- Reading T carries about half of FRZ1's matter-level redistribution. Its matter ratio matches its own halo model, not
  FRZ1's. Post hoc indicator, not graded: FRZ1's 9916.2 / 9008.7 x T's ratio = 715 / 874.

**The two readings point the same way, but no frozen label is FAILS.** The frozen graded field could not carry FRZ1's
matter ratio at z 2.2 in a 20 Mpc/h box, and it is not a positive density field. The positive field is internally
consistent, but it carries only about half of FRZ1's change, and its flux Delta chi^2 is still 90 to 110 times the gate.
On these builds the row does not come near the gate at flux level: the smallest value in any bracket of either reading is
35.7. Because the frozen reading is NO VERDICT, this is a fail reading that still needs a build passing (b) with a positive
field before it can be a label.

## Why the frozen (b) failed, and why M is not positive (the main finding about the matter level)

- FRZ1's R_cold = 1 + (P_B - P_Rb)_turnaround / (P_std R_bar). The change is computed in the turnaround-scope halo model
  but divided by the standard (r200m) spectrum, which is about half as large at k 3. Two kinds of field result:
  - A positive field of spherical haloes that hold their turnaround mass (reading T) realises about half of FRZ1's R - 1.
  - A field whose power is P_std R_bar (reading M) needs a per-halo change about twice the profile difference, because
    the reference halo does not hold the turnaround outskirts that rule 5 rearranges. That change takes out mass the field
    does not have: 6 to 7 % of the gas pixels go negative.
- So FRZ1's matter-level ratio cannot be carried by a positive density field built from rule 5's profiles. The positive
  field carries about half of it.
- The z 2.2 failure in M has a second cause: a 20 Mpc/h box lacks the rare haloes above about 1e12.5 Msun/h. Those
  haloes carry much of P_std's one-halo power at z 2.2.
- Reading M at z 3.0 and 4.4 does reproduce FRZ1 (canonical k 1 / 3 / 5: 0.9912 / 0.8428 / 0.6479 against FRZ1 0.9920 /
  0.8446 / 0.6646 at z 3).

## Table per redshift (seed means; R_F = flux-power ratio at k_v in s/km; Delta chi^2 per bin on its own covariance block)

Reading M (frozen, ungraded):

| z | canonical R_F at 0.003 / 0.01 / 0.03 | canonical bin Delta chi^2 | alt R_F at 0.003 / 0.01 / 0.03 | alt bin Delta chi^2 | R_paint k 1 / 3 / 5 canonical (FRZ1) |
|---|---|---|---|---|---|
| 2.2 | 0.947 / 1.020 / 1.084 | 87.7 | 0.960 / 1.041 / 1.102 | 104.4 | 0.990 / 0.819 / 0.704 (0.991 / 0.873 / 0.767) |
| 2.4 | 0.963 / 1.028 / 1.076 | 124.2 | 0.969 / 1.048 / 1.094 | 173.2 | 0.991 / 0.801 / 0.600 (0.991 / 0.863 / 0.740) |
| 2.6 | 0.959 / 1.023 / 1.077 | 94.3 | 0.968 / 1.042 / 1.096 | 115.3 | 0.993 / 0.817 / 0.684 (0.991 / 0.850 / 0.707) |
| 2.8 | 0.972 / 1.027 / 1.057 | 68.6 | 0.985 / 1.040 / 1.073 | 67.2 | 0.992 / 0.852 / 0.710 (0.992 / 0.849 / 0.688) |
| 3.0 | 0.965 / 1.028 / 1.060 | 92.1 | 0.977 / 1.037 / 1.073 | 85.3 | 0.991 / 0.843 / 0.648 (0.992 / 0.845 / 0.665) |
| 3.2 | 0.977 / 1.036 / 1.044 | 67.1 | 0.985 / 1.043 / 1.056 | 69.8 | 0.992 / 0.844 / 0.630 (0.992 / 0.845 / 0.647) |
| 3.4 | 0.993 / 1.035 / 1.041 | 20.4 | 1.003 / 1.041 / 1.053 | 24.9 | 0.993 / 0.790 / 0.589 (0.993 / 0.849 / 0.637) |
| 3.6 | 0.980 / 1.015 / 1.029 | 14.2 | 0.989 / 1.023 / 1.041 | 12.7 | 0.995 / 0.881 / 0.664 (0.994 / 0.862 / 0.642) |
| 3.8 | 1.000 / 1.029 / 1.022 | 3.6 | 1.007 / 1.034 / 1.031 | 4.1 | 0.994 / 0.902 / 0.752 (0.994 / 0.870 / 0.644) |
| 4.0 | 0.997 / 1.010 / 1.023 | 2.0 | 1.005 / 1.016 / 1.031 | 3.4 | 0.994 / 0.869 / 0.638 (0.995 / 0.881 / 0.653) |
| 4.2 | 0.995 / 0.996 / 1.010 | 0.5 | 1.002 / 1.001 / 1.020 | 0.7 | 0.997 / 0.898 / 0.704 (0.995 / 0.892 / 0.667) |
| 4.4 | 1.002 / 1.020 / 1.016 | 0.4 | 1.008 / 1.024 / 1.026 | 0.6 | 0.998 / 0.886 / 0.687 (0.996 / 0.903 / 0.686) |

Reading T (reported):

| z | canonical R_F at 0.003 / 0.01 / 0.03 | canonical bin | alt R_F at 0.003 / 0.01 / 0.03 | alt bin | R_paint k 1 / 3 / 5 canonical (own halo model) |
|---|---|---|---|---|---|
| 2.2 | 1.026 / 1.073 / 1.053 | 78.5 | 1.041 / 1.083 / 1.042 | 98.6 | 0.993 / 0.910 / 0.806 (0.995 / 0.925 / 0.822) |
| 2.4 | 1.029 / 1.062 / 1.032 | 89.0 | 1.036 / 1.066 / 1.021 | 100.8 | 0.992 / 0.891 / 0.756 (0.994 / 0.923 / 0.812) |
| 2.6 | 1.024 / 1.046 / 1.014 | 48.4 | 1.032 / 1.051 / 1.004 | 61.8 | 0.994 / 0.913 / 0.801 (0.994 / 0.919 / 0.801) |
| 2.8 | 1.023 / 1.034 / 0.998 | 31.7 | 1.030 / 1.035 / 0.990 | 34.7 | 0.995 / 0.923 / 0.802 (0.994 / 0.920 / 0.799) |
| 3.0 | 1.021 / 1.024 / 0.989 | 22.7 | 1.026 / 1.024 / 0.981 | 26.3 | 0.994 / 0.913 / 0.785 (0.994 / 0.920 / 0.795) |
| 3.2 | 1.020 / 1.015 / 0.979 | 12.1 | 1.023 / 1.015 / 0.974 | 14.7 | 0.994 / 0.914 / 0.787 (0.994 / 0.920 / 0.794) |
| 3.4 | 1.021 / 1.012 / 0.974 | 12.2 | 1.024 / 1.013 / 0.971 | 15.3 | 0.994 / 0.899 / 0.756 (0.994 / 0.922 / 0.796) |
| 3.6 | 1.018 / 1.005 / 0.968 | 4.1 | 1.020 / 1.006 / 0.966 | 5.2 | 0.995 / 0.927 / 0.806 (0.995 / 0.928 / 0.805) |
| 3.8 | 1.020 / 1.004 / 0.966 | 2.9 | 1.022 / 1.004 / 0.965 | 3.6 | 0.996 / 0.949 / 0.849 (0.995 / 0.931 / 0.811) |
| 4.0 | 1.014 / 0.995 / 0.962 | 1.4 | 1.017 / 0.999 / 0.961 | 1.8 | 0.995 / 0.926 / 0.802 (0.995 / 0.934 / 0.818) |
| 4.2 | 1.016 / 0.996 / 0.961 | 0.7 | 1.017 / 0.997 / 0.962 | 0.8 | 0.996 / 0.935 / 0.823 (0.996 / 0.938 / 0.827) |
| 4.4 | 1.017 / 0.997 / 0.958 | 0.6 | 1.017 / 0.997 / 0.959 | 0.6 | 0.996 / 0.933 / 0.815 (0.996 / 0.943 / 0.836) |

Seeds: anchors (2.2, 3.0, 4.4) 4, other bins 2. The pull comes from z 2.2 to 3.4. Above z 3.6 every bin is near or below
the gate on its own block in both readings.

**Shape and sign.**
- Matter: the redistribution removes power at k 3 to 5 at every z.
- Flux in reading T: P1D rises by 2 to 4 % at the largest scales DESI uses (k_v 0.003 s/km). From z 2.8 up it falls by
  2 to 4 % at 0.03 s/km.
- Flux in reading M has the opposite tilt (below 1 at low k_v, up to +10 % at 0.03 s/km). I attribute this to its 6 to 7 %
  floored (fully transmitting) pixels; that attribution is not tested separately.
- In neither reading is the flux response a scaled copy of the matter response. Saturation and the mean-flux retuning
  change the sign of the response at large scales.

## Known answers

| check | reading M (frozen) canonical / alt | reading T canonical / alt |
|---|---|---|
| (a) zero difference through the same path: R_F = 1 exactly; gate 0 at R = 1; md5 | PASS / PASS | PASS / PASS |
| (b) matter ratio vs FRZ1 at k 1, 3, 5, anchors (tol 0.01 + 0.25 \|R - 1\|) | FAIL / FAIL: z 2.2 k 3 0.819 vs 0.873 (tol 0.042) and 0.812 vs 0.879; alt also k 5 0.713 vs 0.795 (tol 0.061); z 3.0 and z 4.4 pass at every k (largest miss 0.021) | not applicable; against FRZ1 it fails by design (about half the effect) |
| (b_T) matter ratio vs own turnaround-scope halo model | — | PASS / PASS (largest miss 0.029, z 2.2 k 5 alt, tol 0.049) |
| (c) thin limit vs 1D matter ratio on the same skewers | PASS / PASS (max dev 7e-5) | PASS / PASS (7e-5) |
| (d) mean flux matched | PASS / PASS (2.5e-14) | PASS / PASS (2e-14) |
| (e) seed scatter S_mean <= E / 3 at anchors | canonical FAIL at z 4.4 (0.0059 vs 0.0057); alt PASS | PASS / PASS (S_mean 0.0011 to 0.0020 against E 0.018 to 0.078) |
| floored gas pixels, primary fields (not a frozen check) | 6.7 % / 7.4 % (max) | 1.2e-4 / 1.5e-4 |

Per-seed anchor-bin Delta chi^2, reading M: 229 / 163 / 165 / 258 (canonical) and 221 / 188 / 173 / 274 (alt), against the
seed-mean field's 179 / 190. The seed scatter is about 25 % of the value, against a gate that is 45 times smaller.

## Mutations (anchor bins, three-bin joint covariance; separate `*_MUTATE*` outputs)

| mutation | reading M canonical / alt | reading T canonical / alt |
|---|---|---|
| M1 saturation removed (F = 1 - A tau) | 11224 / 12609 vs 179 / 190 (x 63 / x 67): bites | 10515 / 11295 vs 102 / 125 (x 103 / x 90): bites |
| M2 difference doubled | 798 / 870 (x 4.4 / x 4.6): bites | 408 / 503 (x 4.0 / x 4.0): bites |

- M1 takes the flux Delta chi^2 to the level of the matter-level projection: **saturation is the step that does the
  softening**.
- M2 scales as the square of the amplitude: the response is close to linear in the redistribution's amplitude.

## Brackets (12-bin estimates = primary x anchor ratio; gate 4)

| bracket | M canonical | M alt | T canonical | T alt |
|---|---|---|---|---|
| primary | 789.9 | 904.2 | 363.3 | 424.5 |
| lambda_P x 0.5 (0.027 Mpc/h) | 1749.5 | 2067.8 | 1224.1 | 1398.2 |
| lambda_P x 2 (0.106 Mpc/h) | 274.8 | 247.3 | 90.4 | 98.9 |
| lambda_P = 100 proper kpc (record stage16; 0.215 to 0.366 Mpc/h) | 266.9 | 184.3 | 35.7 | 36.6 |
| gamma 1.2 / 1.6 | 749.1 / 954.7 | 708.6 / 1126.0 | not run | not run |
| mean flux tau_eff x 0.9 / x 1.1 | 766.3 / 813.5 | 891.3 / 915.8 | not run | not run |
| peculiar velocities (linear; seeds 0, 1) | 723.4 | 812.5 | not run | not run |
| resolution N 256 (seeds 0, 1) | 482.9 | 635.7 | not run | not run |
| clustered halo placement (seeds 0, 1) | 111.8 | 136.1 | not run | not run |

- No bracket crosses the gate in either reading.
- Pressure smoothing is the strongest lever. Going from 79 comoving kpc to 100 proper kpc (about x 4 to x 7 in comoving
  terms) cuts the flux Delta chi^2 by 3 (M) to 10 (T).
- Clustering the haloes onto the smooth field's overdensities cuts it by 7 (M). In that bracket, field M's matter ratio is
  no longer FRZ1's.
- Gamma, the mean flux and the velocities move it by less than 30 %.

## The softening

- Flux / matter-level (same fields, record projection) is 0.073 / 0.093 (M) and 0.072 / 0.097 (T). This is a factor 10
  to 14, the same in both readings.
- Its order: pressure smoothing at lambda_P = 79 comoving kpc does little. The gas-level 1D Delta chi^2 of field M is
  19896 / 16527, larger than the matter projection. Saturation does nearly all of it (M1). The mean-flux retuning turns
  the large-scale response positive in T.
- If the record's own pressure-smoothing value is used, the softening grows to about 100 (T at 100 proper kpc: 36 against
  matter 5035).

## Physics left out

- Hydrodynamics: gas follows the total matter above lambda_P.
- Shock heating and hot halo gas.
- Self-shielding and damped systems in haloes.
- UV-background and temperature fluctuations, metals and continuum.
- Form B's change of halo velocities and potentials. Velocities are the same in both fields, and appear only in the
  bracket.
- Haloes below 1e8 Msun/h.
- In the primary, halo positions are uncorrelated with the smooth IGM (bracketed).
- The box is 20 Mpc/h: DESI points below the fundamental take the first mode's ratio, and rare massive haloes are
  missing at z 2.2.
- Reading M's difference is a k-space construction.

## Blindness

- Before writing READING.md, the session context showed me the subjects of FRZ3's two result commits: their labels, flux
  4.71 / 2.58, matter 4720 / 4120, "saturation is the step that softens", brackets crossing, "about half". This is stated
  in READING.md section 0.
- I opened no FRZ3 file other than the three criteria commits.
- I saw FRZ3's folder name list and two sibling folder names (`_rerun_FRZ3_grade`, `_rerun_FRZ3_parts`) in a directory
  listing; I did not open them.
- Before AMENDMENT_A1 I opened only the matter-level ratios and floor counts of the first anchor parts, and no flux array.

## Hand estimate against outcome

- Estimated: flux Delta chi^2 20 to 300, softening 0.003 to 0.03, FAILS on both footings.
- Found, ungraded: 790 / 904 (M) and 363 / 424 (T), with softening 0.07 to 0.10. The flux kept about three times more of
  the matter-level signal than I estimated.
- The reason: the redistribution's two-halo and outskirt parts reach gas at overdensities the forest still sees, and the
  mean-flux retuning turns them into a large-scale tilt.

## Commits

READING 4abb5b4a36 (alone); AMENDMENT_A1 5f39677e97 (alone); code, parts and grading outputs, then this file (ids in
RESULT.md).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
