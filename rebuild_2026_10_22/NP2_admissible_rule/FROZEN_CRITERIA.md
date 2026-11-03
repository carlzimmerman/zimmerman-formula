# NP2_admissible_rule: FROZEN CRITERIA, committed alone before any script or number

**Not blind:** NP1 (its criteria, amendment A1, README, scripts and every number on its cards), BF1, SY1, CX1 and RQ3_acceptance_v2 are read. κ = ½ FITTED. No cold component, no particle; the cold sector stays retired and nothing here reinstates it. Not theory closed. Nothing here says the data favour the framework. A pass is a description of data, not a theory.

## Question
NP1's train-only Gaussian-process leaf rule passed gates 1-5 in both arms and both footings, and RQ3_acceptance_v2 rejected it. Two of its failures are defects of the rule class, not of the data:
1. **Not admissible.** g was not increasing in g_b on 30-34 of 50 dwarf rows and about 10 % of SPARC points, so RQ3's dwarf block (A11-A13) raised a math domain error and read NOT COMPUTABLE.
2. **Υ pinned.** BF1's train targets are built at Υ_disc 0.5, Υ_bulge 0.7, so the Υ that RQ3's FG1 path infers for the rule returns 0.50 and rows A5-A7 can't move.
3. Also: λ sat at the top of NP1's CV grid (4) in every cell.

NP2 asks: does an **admissible** smooth leaf rule, fitted on train only, with smoothness chosen by train CV on a grid that extends past NP1's edge, pass gates 1-5 and RQ3_acceptance_v2 (run unedited)? Arm U asks the same with Υ_disc profiled per train galaxy.

## Reused from NP1 unchanged
Imported read-only from `../NP1_nonparametric_rule/np1_core.py` (and through it SY1's `sy1_data` / `sy1_leaves` and BF1's loader): BF1's split (train: odd SPARC names, Q < 3, inclination ≥ 30; X-COP clusters 0, 2, 4, 6, x ≤ 0.75), the leaves, the arms L3 (log10 y, log10 ell, f) and L5 (+ s, asinh D), the target t = log10 B = log10(g_obs / law(g_b, a0_foot)), W3 wrapper g = law(g_b, a0_foot) · 10^m(leaves), standardisation by train mean and sd, the ARD squared-exponential kernel, class noises σ_X, σ_S, step A (type-II ML, 4 fixed starts, NP1's bounds), the 4-fold grouped CV folds and loss of step B, ties to the larger λ, gates 1-4 and their tolerances, gate 5 and Stage 3 via RQ3 `acceptance.py` run unedited from its own source with this lane as working directory, the CX1 centre rows, and the hull and reach rules including NP1 AMENDMENT_A1 (L5 hull on (log y, log ell, f, s)). Footings 9.3603e-11 (canonical) and 1.1312e-10 (alt), each fitted separately, never pooled. Nothing is fitted on any holdout.

## What changes (declared here, nothing else)

### C1. Admissibility constraint
Admissible means g increases when baryons are added, in both elementary ways, at fixed r (ell) and fixed s:
- **stars-only** direction: g_gas fixed, so f = g_gas/g_b falls: d f / d log10 y = −f ln 10;
- **gas-only** direction: g_stars fixed: d f / d log10 y = +(1 − f) ln 10.
In L5, asinh D moves with y along both directions (D ∝ y at fixed s, ell): d asinh D / d log10 y = ln 10 · D / √(1 + D²); s is held fixed. The fixed-gas-share direction (NP1's post check) is a positive combination of these two, so it is covered.

Along direction v, the slope is S_v = d log10 g / d log10 g_b = σ_law(y) + v · ∇m, where σ_law = g_b law′(g_b) / law(g_b) at the footing's a0 (between ½ and 1).

**Enforced constraint:** S_v ≥ ε = 0.05 on every point of a fixed constraint set C, for both directions. C is a scrambled Sobol set (scipy.stats.qmc, seed 20261103) of 2^15 points (final fits) or 2^13 points (CV fits) in the **constraint box**: in each continuous leaf, the train range padded by 3 frozen lengths (3 λ ℓ_d, in standardised units) each side; f in [0, 1]. In L5 the box is on (log y, log ell, f, s) and asinh D is computed from them by SY1's D formula.

**Fit with the constraint:** the constrained rule is the posterior mode of the same Gaussian process (same σ_f, ℓ, noises) projected onto the constraint set: minimise the posterior quadratic form subject to the linear derivative constraints. Solved through its dual, a non-negative QP in the multipliers μ ≥ 0 on the derivative functionals (scipy `nnls` on the Cholesky factor), with an active set: start empty, add the most violated functionals (up to 1500 per round), re-solve, until no functional in C violates S_v ≥ ε − 1e-6, at most 40 rounds. The frozen rule is m(x) = Σ α′_i k(x, x_i) + Σ μ_j v_j · ∇_z k(x, z_j). It keeps prior mean 0: far from train and constraint points it returns to the plain law. Not converged in 40 rounds → the cell reads UNDETERMINED (INADMISSIBLE).

### C2. Smoothness grid
Step B's λ grid becomes {¼, ½, 1, 2, 4, 8, 16, 32}. CV is run on the **constrained** fit (each fold's fit uses the constraint set C at that λ, 2^13 points). σ_f and noises stay at step A. If λ lands on 32, it is reported as the grid edge and the grid is not extended.

### C3. Arms and modes
Eight cells, each graded on its own: arm L3 / L5 × Υ mode F / U × footing canonical / alt.
- **Mode F:** BF1's targets at Υ_disc 0.5, Υ_bulge 0.7 (NP1's train exactly), constrained.
- **Mode U:** Υ_disc profiled per train galaxy.
  - **Range, from the record:** CRG1 SPEC set E (`CRG1_clean_room_regrade/v1/crg1_sparc.py`, `UPS` and `gB_mat`), the grid FG1/RQ3 use: Υ_disc 0.30 to 1.20, step 0.01, Υ_bulge = 1.4 Υ_disc. (BF1's 0.5 / 0.7 is the point 0.5 of this grid.) Nothing outside it.
  - **Rows:** BF1's SPARC loader rebuilt with Υ as a per-galaxy input, same filters (r > 0, V > 0, g_b > 0 at that Υ), same f = |V_gas|V_gas / V_b² clipped to [0, 1]. Control: at Υ 0.5 for every galaxy it must reproduce BF1's ST and SH arrays exactly.
  - **Profile criterion:** CRG1's FG1 criterion per galaxy, weighted mean squared log10 residual with W = (max(V, 1)/max(eV, 1))², over that galaxy's rows; argmin on the grid.
  - **Procedure, two passes, fixed:** U0 = Υ per train galaxy profiled under the plain law at the footing's a0 → targets and leaves at U0 → steps A and B (constrained) → rule R1 → U1 = Υ re-profiled under R1 (leaves recomputed at each grid Υ) → targets and leaves at U1 → steps A and B again (constrained) → frozen rule R2, the graded rule. Medians of U0 and U1 and the median |U1 − U0| are reported.
  - **Gates in mode U:** gate 1 unchanged. Gate 2: train rows at U1; rms ≤ 1.05 × the plain law's rms on train at U0 (the law's own profile), |median| ≤ 0.03. Gate 3 SPARC: even galaxies with Υ profiled per galaxy under the frozen rule (same grid and criterion), rms ≤ 1.05 × the law's rms with Υ profiled under the law on the same galaxies, |median| ≤ 0.03; the value at Υ 0.5 is also reported, not gated. Gate 3 X-COP, gate 4, gate 5 unchanged.

### C4. Admissibility checker (graded, independent of the fit)
The frozen rule is checked, not trusted:
- S_v > 0 (strict, no margin) in three directions (stars-only, gas-only, fixed gas share) at: a second Sobol set (seed 20261104, 2^16 points) in a **wide box** log10 y ∈ [−8, 14], log10 ell ∈ [−18, −2], f ∈ [0, 1], s ∈ [−4, 5]; every train row; every holdout row (SPARC even, X-COP other, LITTLE THINGS) and CX1 centre row, at its leaves.
- End to end through the RQ3 candidate: NP1's post test, g over g_b × 0.3-3 (25 steps) at fixed r and gas share, on CX1's G, L, Dw, Dw-UFD, IC 1613 rows and SPARC even, must be strictly increasing at every row.
- Any violation: the cell reads UNDETERMINED (INADMISSIBLE), with the count.

### C5. RQ3 rows decided before the run
- **A11** reads NOT COMPUTABLE for every candidate that is not the plain law: RQ3 computes it only from LW1's cached AQUAL solves of the law. That holds here by RQ3's construction; it is not a defect of the rule. A12 and A13 are computable when the rule is admissible.
- **C1** (planets) is decided by the prior mean, as NP1 AMENDMENT_A1 found: the law fails C1 (Z +16492) and every rule here returns to the law far from data. C1 is listed, never counted as a data failure or as a pass.
- **L5 point-rule rows** (SY1's s = −2 stand-in: A9, A10, A11, A12, A13, A20, A23a, A23b, A25, A26b, B2, C1): passes are listed and not counted as passes; their fails are listed as fails carrying the stand-in.
- Groups (B1), the Milky Way and Bullet stay NOT COMPUTABLE when their inputs are NaN, as frozen in NP1.

## Verdict labels, per cell (arm × mode × footing), never pooled
- **UNDETERMINED (controls):** any control below fails for that cell.
- **UNDETERMINED (INADMISSIBLE):** the constrained fit did not converge or the C4 checker finds any violation.
- **UNDETERMINED (UNDERFIT):** gate 1 or gate 2 fails.
- **ADMISSIBLE RULE PASSES ALL COMPUTABLE ROWS:** gates 3, 4, 5 pass and no computed Stage 3 row FAILS other than C1 (prior-decided, listed). NOT COMPUTABLE counts are stated. A description of data, not a theory.
- **ADMISSIBLE RULE FAILS ON <rows>:** gates 1, 2 pass, admissible, and at least one of gate 3, 4, 5 or a computed Stage 3 row other than C1 fails. Every failing row is listed with its value or Z and its hull status by NP1's method:
  - aggregate RQ3 rows: IN HULL if ≥ 90 % of the matching line's located points are in train's hull (NP1's ROWLINE map: A1-A7, A21 SPARC; A9 LT; A10 IC 1613; A11-A13 Dw and Dw-UFD; A30 L; B1 G; B4-B25 X-COP), OUT OF HULL if below, NOT LOCATED if the row has no map;
  - point lines (gate 3 SPARC, gate 3 X-COP, gate 4): IN HULL if the line still fails on its in-hull points alone.
  - In mode U the SPARC hull line uses the even galaxies at their rule-profiled Υ; in mode F, BF1's rows.

No oracle is run (NP1 ran one; NP2's question is admissibility and Υ, and the labels don't use it).

**Reported in every cell:** A5, A6, A7 (Z) under F and U side by side; A12, A13; λ and the CV losses; the number of active constraints and of rounds; λ at the grid edge if so.

## Controls, run and read before the real result (mode `controls`; `real` refuses without its output)
1. **Known answer:** H = 1 on the cached rows: X-COP mean log B over seven clusters +0.4675, LITTLE THINGS median −0.0252, each within 0.0005 (NP1's code path).
2. **Zero-weight rule:** α = 0, no constraint, through NP2's candidate loader and RQ3 unedited (`--no-keys --no-bullet`), both footings: every row present in RQ3's own `results/law.json` card is reproduced, label identical and |ΔZ| ≤ 1e-6 (or |Δvalue| ≤ 1e-6 for line-only rows).
3. **Checker:** (a) flags a planted non-monotone rule (a Gaussian bump of −1.5 dex in m, width 0.3 in standardised log y and 1 in the others, centred at the train mean); (b) passes the zero rule; (c) flags NP1's frozen `real_L3_canonical` rule (NP1's post check found 30-34 non-monotone dwarf rows).
4. **Planted leaf form,** mode F, every arm and footing: synthetic g_obs = law · (1 + f) log1p(1/y) (BF1's planted form, W3) on train and every point holdout line, noise-free (N0) and at SPARC's real errors (N1, NP1's draw). Constrained fit, steps A and B, frozen. Gates 3 and 4 must pass (gate 3 SPARC line 1.05 × the real law's rms on the same rows). Declared in advance: the planted form is itself not admissible at the high-y end of train (its fixed-f slope turns negative near y ≈ 4-5), so exact recovery there is impossible under the constraint; the fraction of planted train rows where its own slope is below ε is reported. The control asks only that gates 3 and 4 pass.
5. **Planted class boost:** the planted form × 10^(±0.25) by SPARC galaxy, NP1's split ((sorted index // 2) odd → +). Gate 3 SPARC must fail.
6. **MUTATE:** log B permuted across all train rows with NP1's seed (20261106), constrained fit, graded on the real holdouts: gates 1-3 must not all pass. In mode U it runs on the U0 targets with one fit (no re-profile), graded with mode U's gates.
7. **Constraint solver:** on the planted N0 fit of each cell, every functional in C satisfies S_v ≥ ε − 1e-6 and the C4 checker passes.
8. **Υ loader:** at Υ 0.5 for every galaxy the per-galaxy loader reproduces BF1's ST and SH exactly.

Controls 1-3 and 8 apply to every cell; 4, 5, 7 are run in mode F and carry to mode U of the same arm and footing (same machinery); 6 is run per cell.

## Run
Scripts committed and verifiable, run `PYTHONHASHSEED=0 nice -n 10 python3 -I`, OMP/MKL/OPENBLAS/VECLIB threads 1, under 1 GB RSS. Outputs named by mode: `np2_controls.*`, `np2_real.*`, RQ3 cards `results/np2_<mode>_<arm>_<F|U>.*`. Frozen rules in `rules/` (small npz). RQ3 caches and stage-3 logs gitignored. No downloads; missing input = NOT COMPUTABLE. Nothing is written in BF1, SY1, CX1, NP1, RQ3, LE1 or other lanes. Amendments go in AMENDMENT_A*.md, labelled pre- or post-result.

κ = ½ FITTED. Not theory closed.
