# JNT1R RESULT (BLIND): JNT1 row S re-graded on the SPARC spirals above v_stiff

**Canonical (9 galaxies): REFERENCE FAILS AT THE RECORD SHARE [L2 shape; L3 scatter], FRAGILE. Beside it: THE LAW FITS,
FRAGILE. Alt (2 galaxies): NO POWER (n < 5). Beside it: THE LAW FAILS [L2 shape], FRAGILE. As frozen in READING.md
(543118d9b8). Neither word is a pass of the theory.**

Best-fit multiple of the record's reference halo, canonical, at the record's U (disc 0.50, bulge 0.70): **A = 0.58**,
95 % interval [0, 1.69] (frozen union of the rescaled-chi2 band [0.53, 0.64] and A +- 2 jackknife SE, SE 0.55; the
lower end -0.53 is cut at the physical 0), 68 % [0.03, 1.13]. The interval excludes A = 2 only, so the row has power by
the frozen rule. A = 1 is inside it, so the failure is not the amount of halo. The reference fails on the SHAPE: at the
record share it puts too much mass in the outer half of each curve (shape -0.087 dex, 3 se 0.064), and its pooled
scatter in the record's fit mode is twice the law's (0.105 against 0.052 dex).

TEST lane: adopts nothing, relabels nothing, registers nothing. Footings never pooled. Cold dark energy is a gravitating
field component; no particle. kappa = 1/2 and the share 5.41 are FITTED. Nothing here says the data favour the
framework. JNT1's RESULT.md, scripts and outputs were not opened before this file was committed.

## Main table (fixed U 0.50 / 0.70; per-point residual r = log10 V_obs^2 / V_mod^2, weights from the quoted errors)

| galaxy | Vflat | log M_b | R_last kpc | ref A=1: d | ref A=1: shape | law+T: d | law+T: shape | A=0: d | A=0: shape | best A_i |
|---|---|---|---|---|---|---|---|---|---|---|
| ESO563-G021 | 315 | 11.33 | 42.4 | +0.168 | -0.057 | +0.217 | -0.078 | +0.445 | +0.144 | 5.00 (grid edge) |
| NGC0801 | 220 | 11.37 | 59.8 | -0.139 | -0.169 | -0.077 | -0.127 | +0.271 | +0.157 | 0.21 |
| NGC2955 | - | 11.36 | 35.4 | -0.027 | -0.044 | -0.022 | -0.020 | +0.074 | +0.210 | 0.36 |
| NGC5371 | 210 | 11.37 | 46.2 | -0.128 | -0.146 | -0.096 | -0.143 | +0.167 | +0.054 | 0.13 |
| NGC6195 | 252 | 11.41 | 36.4 | -0.076 | -0.061 | -0.061 | -0.037 | +0.087 | +0.196 | 0.18 |
| UGC02487 | 332 | 11.50 | 80.4 | +0.106 | -0.112 | +0.184 | -0.058 | +0.632 | +0.144 | 2.02 |
| UGC02885 | 290 | 11.56 | 74.1 | -0.020 | -0.087 | +0.070 | -0.036 | +0.437 | +0.248 | 0.70 |
| UGC09133 | 227 | 11.35 | 108.3 | -0.094 | -0.121 | -0.009 | -0.036 | +0.448 | +0.350 | 0.44 |
| UGC11455 | 269 | 11.40 | 41.9 | -0.028 | -0.025 | +0.004 | -0.016 | +0.239 | +0.203 | 0.68 |

d = W-weighted mean residual (positive = model too low); shape = outer half (R >= R_last / 2) minus inner half. The
formal per-galaxy errors are 0.001 to 0.007 dex in d (the misfits are far above the quoted velocity errors; the class
lines use the robust scatter, see se below). NGC2955 has Vflat 0 in the Lelli table (no flat part measured).

| line (canonical, n 9) | reference A = 1 | law + T | law, no T | A = 0 (no cold component) |
|---|---|---|---|---|
| L1 offset: median d (se) | -0.028 (0.041), holds | -0.009 (0.042), holds | -0.016 (0.045), holds | +0.271 (0.108), FAILS |
| L2 shape: median (se) | **-0.087 (0.021), FAILS** | -0.037 (0.013), holds | -0.031 (0.010), FAILS | +0.196 (0.032), FAILS |
| L3 fit mode: pooled rms / mean | **0.105 / -0.049, FAILS** (line: <= law + 0.010) | 0.052 / -0.004, holds (<= 0.066) | - | - |

Alt (UGC02487, UGC02885): reference A = 1 offset +0.043, shape -0.100; law + T +0.097, shape -0.056 (fails 3 se on the
formal error of two galaxies), fit-mode rms 0.032 (reference) / 0.022 (law). Best A 1.89, chi2 band [1.52, 2.35]; no
jackknife with two galaxies. Two galaxies can show that each curve's outer half sits below the reference (both shapes
negative) and that UGC02487 wants a heavier halo than UGC02885; they cannot give a population offset, a robust scatter or
a jackknife, and the A band rests on chi2 alone. NO POWER by the n < 5 rule.

## Power, mutations, known answers

- **Power (frozen):** canonical 95 % interval [0, 1.69] excludes A = 2 -> has power. Its width is set by the jackknife
  (SE 0.55): deleting UGC09133 moves A to 1.17, deleting UGC02487 to 0.44. The chi2 band alone ([0.53, 0.64]) would
  exclude A = 1; it is not used alone because the residuals are ~ 8 x the quoted errors (chi2 / dof 64).
- **TW-N (A = 0), must bite:** offset +0.271 > 0.10 -> L1 FAILS. Bites (canonical and alt).
- **MUT-C (concentration halved), must bite:** A_best 0.58 -> 2.73 and the word -> NO POWER. Bites. (`jnt1r_MUTATE_C.*`)
- **MUT-E (fractional error profiles shuffled cyclically between members), reported:** A_best 0.62, jackknife SE 0.15,
  95 % [0.32, 0.92] (now excludes A = 1); reference L2 holds (-0.055, se 0.039), L3 fails -> REFERENCE FAILS [A = 1
  outside; L3]. So which line fails depends on the per-point weights; that the reference fails does not. (`jnt1r_MUTATE_E.*`)
- **KA1** 175 galaxies; QX8's fixed-U 0.50 readings recomputed: canonical law 0.1124 / +0.0504, exact 0.1181 / +0.0594,
  alt law 0.1029 / +0.0239. PASS. **KA2** my own halo at z on SRJ3's zC 400569: d = -0.0061041 (srj3.json -0.0061041). PASS.
  **KA3** my own v_vir puts exactly SRJ2's 9 / 2 above v_stiff (nearest the boundary: ESO563-G021 at 267.3 against
  265.8 km/s canonical; NGC6195 283.0 against 288.1 alt). PASS. **KA4** SI second route, NGC5371: r_200m 667.28 vs 667.23
  kpc, C_R(46.2 kpc) 6.062e11 vs 6.063e11 Msun. PASS.

## Brackets (canonical) and jackknife

| member | A_best, 95 % | ref L1 / L2 | word | law word |
|---|---|---|---|---|
| frozen (U 0.50) | 0.58 [0, 1.69] | -0.028 / -0.087 | FAILS [L2; L3] | FITS |
| U 0.35 | 0.76 [0, 2.57] | +0.031 / -0.143 | NO POWER | FAILS [L1; L2] |
| U 0.65 | 0.45 [0, 1.14] | -0.120 / -0.044 | FAILS [L1; L3] | FITS |
| U fit (record's mode) | 0.43 [0.33, 0.53] | -0.018 / -0.074 | FAILS [A = 1 outside; L2; L3] | FAILS [L2] |
| reference + T | 0.58 [0, 1.69] | -0.018 / -0.105 | FAILS [L2; L3] | FITS |
| D + eD | 0.32 [0, 0.87] | -0.098 / -0.090 | FAILS [A = 1 outside; L2; L3] | FITS |
| D - eD | 1.23 [0, 3.87] | +0.022 / -0.083 | NO POWER | FITS |
| i + eInc | 0.38 [0, 0.97] | -0.090 / -0.087 | FAILS [A = 1 outside; L2; L3] | FITS |
| i - eInc | 0.97 [0, 3.28] | -0.018 / -0.087 | NO POWER | FITS |

Jackknife (delete one): 7 of 9 give REFERENCE FAILS (L3 fails in all 9; L2 in 8 of 9); deleting NGC5371 or UGC09133 gives
NO POWER (the interval widens to include 2). A_best 0.44 to 1.17. The law: FITS in 7, FAILS [L2] in 2 (without NGC2955 or
UGC11455). Every member that does not say FAILS says NO POWER; no member says REFERENCE FITS. The reference's L3 failure
(scatter ~ 2 x the law's) holds in every bracket member and every jackknife sample.

## Reported, post hoc (not graded): a lighter halo (`jnt1r_light.*`)

Canonical: at A 0.40, 0.50 and 0.58 all three lines hold (A 0.50: offset -0.006, shape -0.030, fit-mode rms 0.052 against
the law's 0.052); at A 0.25 L3 fails (shape +0.028, rms 0.072); from A 0.75 up L2 and L3 fail. So about half of the
record's halo reproduces these curves as well as the law; the record's full share does not. This scan was not frozen;
the A interval above is the graded statement, and it does not exclude A = 1.

## Hand estimate against the outcome

Frozen: off -0.03 to -0.08 (got -0.028, at the edge), shape -0.05 to -0.15 (-0.087, inside), best A 0.3 to 0.7 (0.58,
inside); P(FAILS) 0.55, P(FITS) 0.25, P(NO POWER) 0.20; P(law fits) 0.6. The estimate was formed knowing JNT1's ungraded
reading in words (READING.md's blindness record), so its agreement is not independent evidence.

## What is left out

Distances and inclinations per galaxy are moved together, not one at a time; no Monte Carlo over them. No bracket on X
(the share median), on v_stiff or on the Duffy normalisation beyond MUT-C. Halo shape is NFW to r_ta with no adiabatic
response to the disc. Membership is fixed at the U 0.50 baryon mass (ESO563-G021 sits 1.5 km/s above the canonical
boundary). The A interval's jackknife over nine galaxies is coarse. Under the D bracket the baryon mass, hence the halo,
is rescaled with D^2 (READING's D-bracket rule; the U brackets keep M_b fixed).

## Blindness

Nothing of JNT1's outputs was seen. Before freezing I knew JNT1's ungraded reading in words from the lane brief ("the
reference layout over-predicts the outer curves at the record share and about half the halo fits"); no JNT1 number.

## Files and runs

`jnt1r.py` (MAIN, MUT_C, MUT_E; about 12 s each, one thread), `jnt1r_light.py`; outputs `jnt1r.json / .out`,
`jnt1r_MUTATE_C.*`, `jnt1r_MUTATE_E.*`, `jnt1r_light.*`. A second MAIN run reproduced `jnt1r.json` byte for byte.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
