# LAM6 FROZEN CRITERIA: does the law's residual at r_half track orbit shape (integrated h4)?

Frozen before any residual is joined to h4. kappa = 1/2 FITTED; footings never pooled; not theory closed.

## Why
KU2 found the board law's residual at r_half the same for slow and fast rotators (D +0.023 +- 0.023 ln).
JAM masses assume an anisotropy; orbit structure is the main known systematic in them. LAM4's integrated h4
(1000 gas-poor MaNGA galaxies, K2 rms 0.021) carries orbit and rotation shape. If the residual moves with h4
at fixed M*, sigma and spin class, either the JAM masses are biased by orbit shape or the law's residual has
an orbit dependence. A null makes KU2's UNIVERSAL robust to that systematic.

## Data and definitions (nothing new downloaded)
- Residual r: KU2's code and conventions exactly (`KU2_kappa_universality_model_choice/ku2.py`: chosen JAM
  model by lowest chi2_dof, r = ln g_obs - ln(nu(g_bar/a0) g_bar) at r_half, KU2's distances and masses),
  canonical a0 9.3603e-11 and alt a0 1.1312e-10 separately.
- Cells and class: KU2's (log M* 0.2 dex x log sigma_Re 0.1 dex; slow = lambda_Re < 0.08 + eps/4 and eps < 0.4).
- h4: LAM4's h4_int from `LAM4_whole_galaxy_absorption/lam4_fit.jsonl`.
- Sample: LAM4's 1000 galaxies that are in KU2's sample with a finite residual.

## Statistic
Within each (cell, class) group with >= 3 galaxies, subtract the group mean from r and from h4. OLS slope b of
demeaned r on demeaned h4; effect E = b x IQR(h4_int over the sample), in ln. 95 % interval from 2000 bootstrap
draws over galaxies (seed 20261104), groups re-demeaned in each draw.

## Checks
- C1: N >= 800 galaxies in groups. C2: KU2's D reproduced on KU2's full sample to 1e-6 (both footings).
- M1 (MUTATE, outputs named by mode): h4 shuffled within groups; E's 95 % interval must include 0, else NO VERDICT.

## Labels, per footing
- **TRACKS ORBIT SHAPE**: |E| >= 0.05 and the 95 % interval excludes 0.
- **NO ORBIT DEPENDENCE**: the 95 % interval lies inside +-0.05.
- otherwise **NO VERDICT**.
0.05 ln is about 2x KU2's sigma(D): the size of shift that could matter for KU2's reading.

## Rows (ungraded)
The same E with LAM2's fibre h4 on the same galaxies; E within slow and within fast separately.
