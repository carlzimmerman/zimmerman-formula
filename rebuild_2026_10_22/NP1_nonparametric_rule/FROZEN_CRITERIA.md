# NP1_nonparametric_rule: FROZEN CRITERIA, committed alone before any script or number

**Not blind:** BF1 (L3 NO HIT, near-miss family), SY1's criteria and amendments, and CX1 (no X-COP neighbour in leaf space, the lensing-against-SPARC tension on one radius) are read. κ = ½ FITTED. No cold component, no particle; the cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## Question
BF1 and SY1 search closed forms for a class-blind rule on the a0 law. Forms are the bottleneck, so remove them. Does any smooth function of the leaves, fitted flexibly on BF1/SY1's train set only and then frozen, pass the holdout gates? A closed form is a special case of a smooth function, so a fail that survives the checks below bounds BF1 and SY1 in these leaves, at the smoothness train chooses.

## Arms
Leaves are SY1's `sy1_data._cols` / `sy1_leaves` exactly (s by system, D = y (2 + s)/(16 π ell)), at a0 canonical on both footings.
- **L3:** inputs (log10 y, log10 ell, f). BF1's leaves.
- **L5:** inputs (log10 y, log10 ell, f, s, asinh D). SY1's leaves. D is a function of the other four; it enters as a fifth coordinate only to let the metric see it.

## Model class
- Target per train row: t = log10 B = log10(g_obs / law(g_b, a0_foot)). That is SY1's W3 wrapper, g = law(g_b, a0_foot) · 10^m(x). W1 and W2 rules that depend on the leaves are W3 rules with a different m, since y is a leaf.
- m = posterior mean of a Gaussian process. Prior mean 0, the plain law, so far from all data the rule returns to the law. Kernel: ARD squared exponential, amplitude σ_f. Noise by class: σ_X² on X-COP rows, σ_S² on SPARC rows. Inputs standardised by the train mean and sd.
- **Smoothness is chosen on train only, in two steps, then frozen:**
  - A. Type-II maximum likelihood on train for σ_f, the ARD lengths ℓ_d, σ_X, σ_S. L-BFGS from 4 fixed starts, best kept.
  - B. One length multiplier λ in {¼, ½, 1, 2, 4} on all ℓ_d, chosen by 4-fold grouped cross-validation on train. Folds are by system: SPARC train galaxies by their train index mod 4; the 4 X-COP train clusters one per fold. Loss = ½ (mean squared held-out residual on X-COP + the same on SPARC), so the classes weigh equally, as in SY1. σ_f and the noises stay at step A. Ties go to the larger λ.
- **Footings:** each footing gets its own fit on train, steps A and B, because its target differs. This departs from SY1 A2.4 (no refit at alt): NP1 asks whether any function exists, per footing. Never pooled.
- Nothing is refit on any holdout.

## Data
BF1's split, unchanged. Train: odd SPARC names, Q < 3, inclination ≥ 30, Υ disc 0.5, bulge 0.7; X-COP clusters at positions 0, 2, 4, 6, x ≤ 0.75. Holdouts never enter steps A or B.

## Gates: BF1's and SY1's, numerically unchanged
- **Gate 1, train X-COP:** |mean log10(g_obs/g)| ≤ 0.05, rms ≤ 0.10.
- **Gate 2, train SPARC:** rms ≤ 1.05 × the law's rms on the same rows at the same footing, |median| ≤ 0.03.
- Gates 1 and 2 are the train-fit quality check, the test for underfitting.
- **Gate 3:** even SPARC names, gate 2's statistic. Other X-COP clusters, gate 1's statistic.
- **Gate 4:** LITTLE THINGS (SY1's `lt_rows`), |median E| ≤ 0.10.
- **Gate 5:** RQ3 `rows_sparc`, FG1's path: A1 rms ≤ 0.110, A2 median Υ in 0.50-0.80, |A3 tilt| ≤ 0.15.
- **Stage 3:** `RQ3_acceptance_v2/acceptance.py`, run unedited from its own source with this lane as its working directory, as SY1 does. Every row, keys and Bullet attempted. As in SY1 A2.9, Stage 3 passes when no computed row FAILS. NOT COMPUTABLE counts are stated. Rows the rule can't see are NOT COMPUTABLE and never a pass: groups and the Milky Way pass gas as NaN, and Bullet passes r as NaN. For L5, SY1's point-rule rows (s = −2 stand-in) are listed and not counted as a pass. Candidates declare `TRAINED_ON = ("xcop_train", "sparc_train")`.
- Tolerances come from BF1's FROZEN_CRITERIA and RQ3's `tolerances.json` (symlinked here, unedited).

## Hull and reach, reported for every holdout line
- **Hull:** the convex hull of the arm's standardised train inputs. Membership is tested by linear programming.
- **Reach:** the distance to the nearest train point in units of the frozen lengths λ ℓ_d. A point is within reach at ≤ 1.
- **Per line:** fraction in hull and fraction within reach.
  - Point-row lines are SPARC even, X-COP other and LITTLE THINGS, plus CX1's centre rows for groups (G), lensing (L), dwarfs (Dw), ultra-faint dwarfs (Dw-UFD) and IC 1613. For these, the line's statistic is recomputed on the in-hull points alone and reported beside the all-points value.
  - RQ3 aggregate rows take the in-hull fraction of their matching CX1 or BF1 rows: A1-A7 and A21 from SPARC, A9 from LITTLE THINGS, A10 from IC 1613, A11-A13 from Dw and Dw-UFD, A30 from L, B1 from G, B4-B25 from X-COP. Other rows read NOT LOCATED.
  - CX1's lines are graded at point level for reporting only, as median residual and its z on CX1's MC sd. That isn't a gate.

## Oracle: the check that a fail is a fail
Same arm, footing and frozen hyperparameters. Train is extended by every holdout point row with a measured g_obs:
- SPARC even and X-COP other, with their class noise
- LITTLE THINGS, noise 0.075 (RQ3's IC_sE)
- CX1's centre rows for G, L, Dw, Dw-UFD and IC 1613, each with noise equal to CX1's MC sd of log B for that row

The oracle is graded on gates 3-5 and Stage 3 exactly like the frozen rule. It is a diagnostic: it sees the holdouts. It's also run at λ/4, reported only.

## Verdict labels, per arm and per footing
- **UNDETERMINED (controls):** any control below fails for that arm and footing.
- **SMOOTH RULE EXISTS:** the frozen train-only rule passes gates 3, 4, 5 and Stage 3. Report its partial dependences as a target for BF1 and SY1. It is a description of data, not a theory.
- **NO SMOOTH RULE IN LEAF SPACE:** the frozen rule passes gates 1 and 2, so it isn't underfit, and fails at least one line. For at least one failing line:
  - (i) the line still fails on its in-hull points alone (point-row lines), or ≥ 90 % of its located points are in hull (aggregate RQ3 rows);
  - (ii) the oracle also fails that line.

  Read as: no function at the train-chosen smoothness reproduces train and that line together. This is not a no-go for arbitrarily wiggly functions. CX1 found no data-level collision apart from L|S.
- **UNDETERMINED:** anything else. That covers gates 1 or 2 failing (underfit), failures only out of hull, or an oracle that passes the failing lines (train doesn't determine the rule). The failing lines are named.

## Controls, run and read before the real result
- **Known answer:** H = 1 on the cached rows reproduces the plain law. X-COP mean log B over all seven clusters is +0.4675 (BF1, CX1) and the LITTLE THINGS median is −0.0252 (CX1), each within 0.0005.
- **Planted leaf form:** synthetic g_obs = law(g_b, a0) · (1 + f) log1p(1/y), BF1's planted form in W3, on train and on every point holdout line (SPARC even, X-COP other, LITTLE THINGS). It runs noise-free and with SPARC's real errors (SY1's `sparc_err`, one fixed draw). Fit by steps A and B, then frozen. Gates 3 and 4 must pass, with gate 3's SPARC line taken as 1.05 × the real law's rms on the same rows.
- **Planted class boost:** the same planted form, times 10^(±0.25) by SPARC galaxy, + for (sorted-name index // 2) odd and − otherwise. Both halves then appear in train and holdout, at the same leaves, so a leaf function can't carry it. Gate 3 must fail.
- **MUTATE:** log B permuted across all train rows, both classes, with a fixed seed, then fit by steps A and B. Gates 1-3 graded on the real holdouts must fail.
- If a control fails for an arm and footing, that cell reads UNDETERMINED (controls).

## Run
Scripts are committed and verifiable, run with `PYTHONHASHSEED=0 python3 -I`, OMP/MKL/OPENBLAS threads 1, `nice -n 10`, under 1 GB RSS. Outputs are named by mode: `controls`, `real`, `oracle`. `real` refuses until the controls output exists. No downloads; missing data is NOT GRADED. Nothing is written in BF1, SY1, CX1, RQ3 or other lanes; RQ3's caches land here, gitignored.

κ = ½ FITTED. Not theory closed.
