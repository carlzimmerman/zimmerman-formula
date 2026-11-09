# KO1 RESULT (criteria b1b91fae33; amendments A1 ae28af31fa, A2 a52e709b22)

**KO1: LAW LEVEL HOLDS / LAW LEVEL HOLDS** (canonical / alt) by the frozen gate as this lane read it.
**Independent regrade KO1R: NOT SEPARATED / LAW LEVEL HOLDS.** The canonical label sits on a knife edge (section 2a).

Commit ids: local b1b91fae33 (criteria), ae28af31fa (A1), a52e709b22 (A2), a11a8a9523 (result); on origin a8c30d93c3,
b64341eb9f, 66df609b0c, 9813a4adfb.

TEST lane, quarantined. Adopts nothing and relabels nothing. kappa = 1/2 FITTED; not theory closed. Footings never pooled.
The first run failed a known answer (KA5) and was NO VERDICT; A1 explains why the check, not the pair finder, was wrong, and
the re-run passes 11 of 11. A1 and A2 are post hoc and say so. Everything after section 1 is reported, not gated.

## Bottom line

1. **Frozen gate.** Lenses with no galaxy 0.3 dex more massive inside their own measured range (40,667 of 181,477; 29 % of
   the outer weight) show an outer amplitude of **1.10 +- 0.15 / 1.00 +- 0.14** of the law. That is above the 0.891 line and
   4.1 sigma above the two-phase exterior at the census cap (0.46 / 0.42).
2. **Robust on every reading: the record's share is not enough.** A two-phase exterior carrying the record's share
   (5.56 M_b) is excluded at 5.3 to 5.6 sigma, in a form that does not depend on the stellar-mass calibration and at every
   veto radius tried.
3. **Not decided: the law against a heavy exterior.** The exclusion of the census-cap exterior in item 1 rests on the
   record's stellar masses. Measured against the stack's own inner level, the least edge-affected sample gives
   0.81 +- 0.13; the law's floor is 0.98 and the census-cap exterior is 0.78 / 0.66. Both fit.
4. **What a two-phase exterior needs.** A share of 41 to 56 M_b at the wall (2 sigma: at least 28) on the canonical footing,
   48 to 66 (at least 33) on alt. That is at least 5.0 / 5.9 times the record's share. SWT1's gate clears a share only up
   to 2.8 to 4.0 times, and a shell that heavy outweighs the wall force by at least 5.6 / 7.1 times (Lean,
   `shell_unsupported_iff`). The two-phase reading therefore fails on KiDS without using the CMB-lensing allowance.
5. **My pre-freeze estimate was wrong.** I expected hosts to carry 30 to 50 % of the outer signal. The 4.9 sigma difference
   between hosted and host-free lenses at the frozen radius is mostly the edge of the veto: it falls to +0.31 +- 0.21 when
   the veto radius is widened to 1.6 R_h.

## 1. The frozen statistic

Cut chosen by the frozen rule from weights only: Delta 0.3 dex, W 230 Mpc (outer-weight share 0.290; the other three settings
0.472, 0.641, 0.772).

| quantity (outer bins, g_bar < 9.7e-15 m/s^2) | canonical | alt |
|---|---|---|
| W10 stack (181,477) | 1.707 +- 0.086 | 1.553 +- 0.078 |
| hosted (140,810) | 2.009 +- 0.107 | 1.828 +- 0.098 |
| **host-free A_hf (40,667)** | **1.098 +- 0.154** | **0.999 +- 0.141** |
| per bin, host-free / law | 0.09, 0.95, 1.56, 1.24 (+- 0.44, 0.36, 0.33, 0.27) | 0.08, 0.87, 1.42, 1.13 |
| hosted minus host-free | +0.912 +- 0.186 | +0.830 +- 0.169 |
| two-phase exterior, record's share / census cap | 0.056 / 0.463 | 0.051 / 0.422 |
| mass-scatter slope b, factor at sigma_M 0.2 (0.1) | 5.26 per dex, 1.274 (1.062) | same |
| corrected A_hf^c | 1.399 +- 0.197 | 1.273 +- 0.179 |
| label, raw and corrected | LAW LEVEL HOLDS, LAW LEVEL HOLDS | LAW LEVEL HOLDS, LAW LEVEL HOLDS |
| cross-shear null | +0.12 +- 0.18 | +0.11 +- 0.16 |

## 2. Checks

- **Known answers, all PASS after A1.** KA1 6.4e-14. KA2: 605,531 candidates, 181,477 lenses, rows, f20 and f30 all equal.
  KA3 exact to 4e-16. KA4: z over 200 random halvings has standard deviation 1.018. KA5 (A1): the tree-based finder equals
  the brute-force expectation over 4,000 x 4,000 pairs; 104 lenses were reached by another lens's planted object, which is
  what failed the first version of the check.
- **MUTATE, all bite** (`ko1_MUTATE.out`). M1 permuted flags: +0.376 +- 0.194, inside 2 sigma (the true difference is
  4.9 sigma). M2 signal x 0.4: BELOW THE LAW, TWO-PHASE WINDOW. M3 signal = the law: LAW LEVEL HOLDS. M4 mutated isolation:
  208,250 lenses, KA2 fails.
- **Lean.** `KO1.lean`: 12 theorems, `exit 0`, axioms propext, Classical.choice, Quot.sound only (`compile.txt`).
  `KO1_MUTATE.lean`: five false versions, five errors, `exit 1`.

## 2a. Independent regrade (lane KO1R, `fable52_push/KO1R_kids_outer_regrade/`)

A second session re-derived the primary statistic from the frozen criteria alone, with its own code, before opening any
KO1 file.

| quantity (canonical / alt) | KO1 | KO1R as it read the criteria | KO1R's code with KO1's tie rule |
|---|---|---|---|
| host-free lenses | 40,667 | 40,149 | 40,667 |
| A_hf | 1.098 +- 0.154 / 0.999 +- 0.141 | 1.082 +- 0.158 / 0.985 +- 0.144 | identical to KO1 (2e-15) |
| corrected A_hf^c | 1.399 +- 0.197 / 1.273 +- 0.179 | 1.388 +- 0.203 / 1.263 +- 0.185 | identical |
| hosted minus host-free | +0.912 +- 0.186 / +0.830 +- 0.169 | +0.927 +- 0.187 / +0.843 +- 0.170 | identical |
| label | LAW LEVEL HOLDS / LAW LEVEL HOLDS | **NOT SEPARATED** / LAW LEVEL HOLDS | LAW LEVEL HOLDS / LAW LEVEL HOLDS |

- **One traced cause.** The catalogue's stellar masses carry 5 or 6 significant digits, so a neighbour exactly 0.3 dex
  heavier is common. KO1 compares floats as they are; KO1R counts a decimal tie as a host. 518 lenses have only tied hosts.
- **Why the canonical label flips.** Not through the amplitude (1.08 against 1.10). The corrected error is 0.197 here and
  0.203 there, and the frozen NO POWER line is 0.20. Raw LAW LEVEL HOLDS with corrected NO POWER reads NOT SEPARATED.
- The criteria did not anticipate mass quantization. Neither run has a bug. The honest statement is: **alt LAW LEVEL HOLDS
  on both readings; canonical LAW LEVEL HOLDS or NOT SEPARATED, depending on 518 tied lenses.** Every measured number agrees
  within 1.5 %.
- KO1R also chose the brute-force reading of KA5 on its own, before seeing A1.

## 3. Reported items of the frozen list (canonical; alt in `ko1.out`)

- **R1, isolation shells.** W10 not W20 1.98 +- 0.14; W20 not W30 2.21 +- 0.21; W30 0.94 +- 0.16. The drop is
  1.04 +- 0.22. A2 applies here too: W30's veto has a 3 Mpc comoving radius, inside the graded range of massive lenses, so
  its outer bins are biased low by the same edge.
- **R2, host-free subsets.** Late types -0.19 +- 0.39, early types 1.34 +- 0.18. Mass terciles -1.14 +- 0.72,
  0.57 +- 0.32, 1.37 +- 0.18. Redshift halves 1.10 +- 0.22 and 1.23 +- 0.22. Three lowest bins only 1.01 +- 0.19.
- **R3, by number of hosts.** 0: 1.10 +- 0.15. 1: 1.68 +- 0.17. 2: 1.61 +- 0.25. 3 or more: 2.38 +- 0.15.
- **R4.** Not informative as designed, also after A1. The isolated lenses have 3 % fewer more massive pool objects in range
  than shuffled positions, because the record's isolation removes pairs inside 10 Mpc and thins dense environments. The
  only positive excess is inside 0.25 Mpc at 10 to 115 Mpc (+0.012 per lens; table E6 in `ko1_extra.out`). Being host-free
  is mostly chance: 22.4 % of lenses against 23.2 % of shuffled positions.
- **R5, sources.** Near 1.01 +- 0.23, far 1.16 +- 0.22.
- **All four settings.** 1.10 +- 0.15, 1.31 +- 0.11, 1.51 +- 0.11, 1.57 +- 0.09: the amplitude falls as the cut tightens.
- **R6, B21's published tables, four lowest points.** KiDS-bright isolated 1.50 +- 0.08. GAMA isolated (spectroscopic)
  0.97 +- 0.28, a ratio of 0.65, 1.8 sigma lower. With B21's hot-gas estimate in g_bar the same points sit at
  **0.47 +- 0.04**. Isolated over all-galaxy, per mass bin: 0.65, 0.53, 0.60, 0.49.
- **R7.** The W10 stack over B21's isolated points, per outer bin: 1.29, 0.94, 1.23, 1.08 (within 1.6 sigma each).

## 4. A1 extras (`ko1_extra.py`; declared before they were computed)

| lens set (canonical) | outer | middle (to 5.3e-14) | inner (to 1.6e-12) |
|---|---|---|---|
| W10 all | 1.71 +- 0.09 | 1.87 +- 0.09 | 1.65 +- 0.06 |
| host-free all | 1.10 +- 0.15 | 1.82 +- 0.14 | 1.81 +- 0.11 |
| host-free late (10,282) | -0.19 +- 0.39 | 1.53 +- 0.40 | 1.58 +- 0.27 |
| host-free early (30,385) | 1.34 +- 0.18 | 1.90 +- 0.15 | 1.84 +- 0.11 |
| W30 late (30,693) | 0.53 +- 0.23 | 1.54 +- 0.26 | 0.92 +- 0.16 |
| W30 early (26,572) | 1.19 +- 0.21 | 1.92 +- 0.20 | 1.92 +- 0.14 |
| host-free and W30 (16,526) | 0.45 +- 0.26 | 1.64 +- 0.24 | 1.86 +- 0.13 |
| hosted late / early | 1.50 +- 0.16 / 2.45 +- 0.13 | 1.12 +- 0.19 / 2.48 +- 0.12 | 1.28 +- 0.11 / 1.81 +- 0.10 |

- **E1.** The stack sits 1.6 to 1.8 times above the law at inner radii too. So the frozen comparison with A = 1 flatters
  the outer bins. The host-free late types have a normal inner signal, so their missing outer signal is not a
  badly-placed-lens artefact.
- **E2.** Tightening the host threshold to Delta 0.0 leaves 3,526 lenses (0.01 +- 0.52); Delta -0.3 leaves 1,189 (no power).
- **E3.** Early minus late in the outer bins: host-free +1.53 +- 0.46 (3.3 sigma), W30 +0.66 +- 0.30, W10 +0.75 +- 0.18.
- **E4.** The host-free late-type deficit is in both redshift halves and both mass halves (-0.08 to -0.35, each +- 0.4 to
  0.6).
- **E5.** Over 200 permutations within type x mass tercile x redshift half, hosted minus host-free averages +0.002 with a
  spread of 0.183. The true +0.912 is 5.0 sigma above composition. M1's single draw of +0.376 was a 2 sigma draw.

## 5. A2 checks (`ko1_shape.py`)

**The shape ratio R_s = A(outer) / A(inner), post hoc.** It cancels the stellar-mass calibration, the mass-scatter selection
and any unseen baryons inside the inner window. The law's floor is exact: enclosed mass cannot fall outward, and Lean bounds
the law's response to a mass factor k between sqrt(k) and k.

| lens set (canonical; alt within 0.01) | R_s | law's floor | sigma below the floor (without the outermost bin) |
|---|---|---|---|
| W10 all | 1.04 +- 0.06 | 0.98 | -0.8 (-1.0) |
| hosted | 1.26 +- 0.09 | 0.98 | -3.2 |
| host-free all | 0.61 +- 0.09 | 0.98 | 3.9 (2.7) |
| host-free late | -0.12 +- 0.25 | 0.98 | 4.4 (3.2) |
| host-free early | 0.73 +- 0.11 | 0.98 | 2.4 (1.6) |
| W30 all | 0.61 +- 0.10 | 0.98 | 3.7 (2.6) |
| host-free and W30 | 0.24 +- 0.14 | 0.97 | 5.1 (3.4) |

**E7, the edge test.** The frozen text said a uniform absence of hosts inside R_h makes no shear there. That holds for point
masses only; extended hosts leave a tapered edge that lowers the outermost bin. Widening the veto radius moves that edge
out of the graded range.

| veto radius | lenses | outer | R_s | late / early outer | W10 minus host-free |
|---|---|---|---|---|---|
| 1.0 R_h (frozen) | 40,667 | 1.10 +- 0.15 | 0.61 +- 0.09 | -0.19 +- 0.39 / 1.34 +- 0.18 | +0.61 +- 0.13 |
| 1.3 R_h | 25,708 | 1.27 +- 0.19 | 0.71 +- 0.12 | 0.01 +- 0.49 / 1.47 +- 0.22 | +0.43 +- 0.17 |
| 1.6 R_h | 17,335 | 1.40 +- 0.22 | 0.81 +- 0.13 | 0.13 +- 0.68 / 1.51 +- 0.23 | +0.31 +- 0.21 |

- The deficit shrinks as the edge moves out: 3.9 sigma below the law's floor at the frozen radius, 2.3 at 1.3 R_h, 1.3 at
  1.6 R_h. **The post hoc shape deficit is not established.**
- The same goes for "hosts carry the outer points": 4.6 sigma at the frozen radius, 1.5 at 1.6 R_h.
- The frozen label gets firmer, not weaker: with the edge moved out the outer amplitude is 1.27 and 1.40.

**PH2, B21's tables (inner amplitudes not seen before A2).** KiDS-bright isolated: R_s 1.05 +- 0.06, flat. GAMA isolated:
0.57 +- 0.18, 2.3 sigma below the floor. That is the direction A2 predicted, but GAMA's veto radius is 3 Mpc, the same as the
outermost radius measured, so the edge effect applies to it as well. With B21's hot-gas estimate: 0.35 +- 0.03.

**PH3, the two-phase exterior in the same calibration-free form** (added after E7 was seen; post hoc). k is the
enclosed-mass factor the inner window asks for (about 3 canonical, 2.6 alt).

| veto radius | R_s | law's floor | census cap (X 53.64) | record's share (X 5.56) | share needed (2 sigma) |
|---|---|---|---|---|---|
| 1.0 R_h, canonical / alt | 0.61 +- 0.09 | 0.98 (3.9 / 4.0 sigma) | 0.80 / 0.67 (2.0 / 0.7) | 0.095 / 0.080 (-5.5 / -5.6) | 41 (28-54) / 48 (33-64) |
| 1.3 R_h | 0.71 +- 0.12 | 0.98 (2.3 / 2.3) | 0.79 / 0.67 (0.7 / -0.4) | 0.095 / 0.080 (-5.3 / -5.5) | 48 (32-64) / 57 (38-77) |
| 1.6 R_h | 0.81 +- 0.13 | 0.98 (1.3 / 1.3) | 0.78 / 0.66 (-0.2 / -1.1) | 0.094 / 0.079 (-5.4 / -5.5) | 56 (37-74) / 66 (44-88) |

## 6. What it means for the switch class

- SWT1's conflict stands: nothing here lets the law switch off inside KiDS's range at the record's share.
- KO1 adds a second conflict that does not use the CMB-lensing allowance. A variational switch shows only M_b from outside
  (SWT1 T1), so the outer bins must be made by the swept share. They need at least 28 / 33 M_b at 2 sigma and 41 to 66 at
  best fit. SWT1 T3 clears a share only up to 2.8 to 4.0 times 5.56 M_b, about 16 to 22 M_b. A shell of 28 / 33 M_b at the
  allowance radius (112 / 123 MOND radii) outweighs the wall force by 5.6 / 7.1; at the best-fit shares by 12 to 22 /
  15 to 27. A wall further in does worse.
- So the two-phase reading has two exits and both are graded: a light share is cleared but leaves KiDS's outer bins empty
  (5 sigma); a heavy share fills them but cannot be cleared.
- What is not excluded: the law as the lens's own field out to 3 Mpc (R_s floor 0.98 against 0.81 +- 0.13). That is the
  reading SWT1 showed needs a filling of 0.29, twelve times the lensing allowance.

## 7. Limits

- The lens sample is the record's W10 reconstruction (stricter than B21's); the estimator has no random subtraction and no
  boost correction. R7 and the cross-shear null are the only checks on that.
- Absolute amplitudes are calibration-limited (CFG261). Only the shape ratio and the split differences are free of it.
- The veto removes hosts at least 0.3 dex more massive. Neighbours of comparable mass stay, so every host-free amplitude is
  an upper bound on the lens's own field.
- Photo-z pair scatter grows above z 0.3 (CFG502), so the 230 Mpc window catches fewer true hosts there.
- The late-type result (no outer signal in host-free late types, at every veto radius, 2 to 3 sigma) was seen after the
  freeze, sits in a sub-split and shares the edge effect. It is a lead, not a result.
- B21's hot-gas variant moves the published outer points from 1.50 to 0.47 of the law. The gas mass at Mpc radii is the
  largest single uncertainty in reading these bins, and nothing on disk measures it.

**What would settle the open part.** Spectroscopic isolation with a veto radius well beyond the measured range, a frozen
shape gate, and a measured hot-gas mass. None of it is on disk.

## Files

FROZEN_CRITERIA.md, AMENDMENT_A1.md, AMENDMENT_A2.md, ko1.py -> ko1.json / .out, ko1_MUTATE.json / .out,
ko1_run1_KA5_fail.json / .out (the first run, kept), ko1_extra.py -> ko1_extra.json / .out, ko1_shape.py -> ko1_shape.json /
.out, KO1.lean, KO1_MUTATE.lean, compile.txt, compile_MUTATE.txt. One thread; 21 s, 30 s and 24 s; under 1 GB. The shear
catalogue was not read. The independent regrade is lane KO1R.

Not registered: the closure register belongs to the orchestrator. Adopts nothing. kappa = 1/2 FITTED; not theory closed.
