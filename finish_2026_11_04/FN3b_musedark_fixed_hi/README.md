# FN3b_musedark_fixed_hi: NOT DECIDABLE. Fixing the HI term from local HI structure isn't enough: at the cubes' S/N the law-imposed refit still carries a -0.10 to -0.16 dex bias and recovers a planted rise at 0.47 of 0.60. No cutout is requested

kappa = 1/2 FITTED. Not theory closed. Nothing here says the data favour the framework. Criteria `FROZEN_CRITERIA.md` (b94053ccce), committed alone first, after FN3 (`../FN3_musedark_law_refit/`, NOT DECIDABLE with HI free) at the owner's "you must find a way". Not blind: FN3's K2' and dry run were read first.

## What was tried
FN3 let each galaxy's HI surface density float over 0-15 Msun/pc^2, and that freedom swallowed the signal. FN3b fixed it at 6.0 Msun/pc^2, from the local HI mass-size relation, which makes inner HI surface density nearly independent of HI mass. It also used the z ~ 1 21-cm stacks, which find HI mass about equal to stellar mass (Chowdhury et al. 2020; provisional). The error went into the budget: 0.25 dex common mode, 0.15 dex per galaxy.

## Budget (`fn3b_budget.out`, before any data)
sigma_cm 0.215 / 0.238 / 0.262 dex canonical (0.215 / 0.239 / 0.271 alt); L_HI -0.24 / -0.36 / -0.48; slope sigma_s,sys 0.113 per unit z.

## K2'' (`fn3b_k2pp.out`), fresh seeds, S/N 30, planted Sigma_HI 6.0 x 10^N(0, 0.15), fitted at 6.0
| line | result | frozen line | reading |
|---|---|---|---|
| (a) median bias, thirds 0 / 1 / 2 | +0.022 / -0.160 / -0.095 | 0.07 | thirds 1 and 2 **FAIL** |
| (b) flat truth, slope | -0.202 per unit z | 0 +- 0.10 | **FAIL** |
| (c) planted rise 0.60, recovered | +0.465 | 0.60 +- 0.10 | **FAIL** |
| (d) MUTATE a0 x 2 | -0.460 | -0.30 +- 0.07 | **FAIL** |
| (e) power | the rise grades TENSION (slope 2.1 sigma), not BAND CONSISTENT | not BAND CONSISTENT | PASS |

Per-galaxy scatter (flat) runs from -0.634 to +0.139 dex (16-84 %).

**Line (d) was mis-specified.** It copied FN3's -0.30, but with HI fixed this lane's own lever L_band (-1.0 to -1.5) predicts -0.30 to -0.46. That is a design error, disclosed; (a)-(c) fail regardless.

## What it means
Pinning HI helps. The rise now comes back at 0.47 instead of FN3's 0.32, and the grader gains power, reading TENSION instead of BAND CONSISTENT. But a negative bias remains. These are small, pressure-supported galaxies, and at matched-filter S/N 30 the stellar mass also trades against the dispersion (pressure support) and the inclination box, not just the HI.

**No further redesign is made here.** A third fix chosen after two failures would be iterating until something passes.

**The a0(z) door's verdict: the existing MUSE-DARK cubes cannot decide it under the law.** It waits on deeper kinematics for galaxies like these, measured gas, or the z ~ 2.5 deep-MOND point (CFG689 P6).

## Files
`FROZEN_CRITERIA.md`, `fn3b_budget.py/.out`, `budget_fn3b.json`, `fn3b_k2pp.py/.out/.json/.jsonl`, `fn3b_k2pp.progress`, `fn3b_k2pp.time`, `fn3b_stage1.py` (built, plumbing-tested, not run), `fn3b_stage1_selftest.out`.
