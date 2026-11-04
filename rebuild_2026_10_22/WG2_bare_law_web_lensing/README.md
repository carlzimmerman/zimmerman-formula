# WG2_bare_law_web_lensing: the law alone FAILS CMB lensing under every web rule tried. Law off is far too low, QUMOND on the web is 11-14× too high (NOT EVALUABLE as frozen; labels under post-result Amendment A2)

**Commits.**
- Criteria: 8f484be581, committed alone before any script or number.
- Amendment A1 and engine: dca7a564b3, before any production run.
- Grader: 45708baf92, before any run finished.
- Amendment A2 (POST-RESULT) and result: this commit.

**Origin.** Owner 2026-11-04, on WG1's NOT EVALUABLE: "you sure we cnt figure it out?" and "swing harder".

**Standing.** κ = ½ FITTED. The cold sector stays retired. No particle and no cold component is added. Not theory closed. Nothing here says the data favour the framework.

## What was missing, and what this lane supplied
WG1 left board row D9 NOT EVALUABLE for the law alone, for lack of two inputs. This lane supplies the natural choice for each.
- **(b) A baryon field without a cold term.** CLASS with ω_cdm ≈ 0, ω_b 0.02237. The field at z_on 50 comes from the baryon-photon era with no dark component. A_s is bracketed at 1e-9 and 4e-9.
- **(a) A rule for the law on the web.**
  - **R0, law off:** Newton, sourced by baryons.
  - **R1, law on:** QUMOND on the peculiar field, Milgrom's simple form. This is the rule published MOND cosmology uses.
  - a0 is flat (TIE) or ∝ H(z) (RIVAL).
- **Engine:** CFG359's PM, adapted. Box 1600 h⁻¹ Mpc, 128³, from z 50 to 0.
- **Projection and grading:** the total potential is projected to C_L^φφ with WG1's Limber engine and graded against Planck PR4 lensing 8-400.
- **Backgrounds:**
  - B2 (primary): the measured-style expansion, carrying PAPER67's unexplained smooth matter term.
  - B1: baryons alone in the expansion.

## Result
r is the model's lensing amplitude over the measured one (PR4, PACKAGE rule; PLAIN agrees within 3 %).

| web rule | B2 (A_s 1e-9 / 4e-9) | B1 (A_s 1e-9 / 4e-9) | label (under A2) |
|---|---|---|---|
| R0, law off | 0.00022 / 0.00089 | 0.077 / 0.31 | **FAILS LOW** |
| R1, law on, a0 flat (TIE) | 11.4 / 14.1 | 560 / 657 | **FAILS HIGH** |
| R1, law on, a0 ∝ H(z) (RIVAL) | 345 / 391 | 6,220 / 6,850 | **FAILS HIGH** |

**D9 for the law alone, under A2: FAILS under every web rule tried.**
- The measured amplitude lies between the law off and the law on.
- With the measured expansion (B2), the law on overshoots by 11-14× in power, about 3.5× in potential. The law off falls more than three orders short.
- No rule on record lands in between. Such a rule would have to be derived, not tuned.

**As frozen: NOT EVALUABLE.** K4's mean-of-ratios statistic failed (1.979) on two bins at the baryon-acoustic nodes of the no-cold-term field. The median ratio (1.004) and the ratio of summed power (0.970) show the initial conditions are right. Amendment A2 records that and the grader's step-count fix.

## Checks
- **K1 growth (128³, A1):** 0.985, PASS.
- **K2 QUMOND plane wave:** 2.5e-7, PASS.
- **K3 Limber:** 7.9e-7, PASS.
- **K4 ICs:** FAIL as frozen; K4b PASS (A2, post-result).
- **K5 resolution** (12.5 → 8.3 h⁻¹ Mpc): r 12.71 → 12.77, ratio 1.005, PASS.
- **K6 time step** (200 → 400 steps): 12.71 → 12.71, PASS.
- **K7 turn-on** (reported): z_on 200 gives 13.24, against 12.71 at z_on 50.
- **Alt footing** (reported): 17.7, against 12.71 canonical.
- **MUTATE** (Poisson factor halved): K1 0.149 FAIL, and every label reads NOT EVALUABLE. The check bites.

## Diagnostics
- **Growth on 12.5 h⁻¹ Mpc cells (δ_rms at z 0):**
  - B2: 0.17-0.20 with the law on, against 0.002-0.004 with it off.
  - B1: 6-7 with the law on and a0 flat; 34 with a0 ∝ H(z).
- **Median field on the mesh:** 0.002-0.004 a0 at z 0-2 (B2, law on, a0 flat), with median boost ν ≈ 16-23. That is inside WG1's measured 0.003-0.22 a0.
- **A_s:** with the law on, r barely depends on A_s (×4 in A_s gives ×1.24 in r). Deep-regime growth saturates.
- **In-box share of each bin's C_L:** 0.73-1.00 for law-on B2, lowest in bins 1 and 9. The rest comes from the frozen extrapolations. The zero-beyond variant moves r by under 1 %.

## What this means for the record
- **Board D9.** It can now read FAILS for the law alone, both sides (WG2, under A2).
- **PAPER67's gaps section.** The CMB-lensing door now has a verdict, not just a missing input. The law alone can't give the measured lensing:
  - off on the web, baryons supply far too little;
  - on the web as QUMOND, from baryons alone, it gives 11-14 times too much.
- **Requirement for any action** (top-5 item 1). The rule on the web must sit between off and unscreened QUMOND, roughly an order of magnitude weaker in lensing power than QUMOND. It must come out of the action, not be fitted.
- **a0 ∝ H(z).** It overshoots about 30 times more than a0 flat. Both fail, so this is not evidence for the ρ_DE tie.

## What this lane can't say
- It is not a primary-CMB test, and the baryons-only acoustic peaks are not graded.
- Resolution was checked only from 12.5 to 8.3 h⁻¹ Mpc. The law's response at galaxy scales, where fields exceed a0, is smoothed on the mesh.
- It assumes lensing sees the dynamical potential.
- A_s is bracketed, not fitted.
- A rule between off and on is not excluded; none is on record.
- The labels rest on a post-result amendment to one initial-conditions check (A2).
- Nothing here reinstates the cold sector.

## Files
- `FROZEN_CRITERIA.md`, `AMENDMENT_A1.md`, `AMENDMENT_A2.md`
- Scripts: `wg2_pm.py` (engine and K1/K2), `wg2_run_all.py` (the 17-run matrix), `wg2_grade.py` (K3, K4, K4b, projection, labels).
- Run outputs: `runs/*.json` (17 runs and the checks; logs are not committed).
- Graded results: `wg2.out` and `wg2_results.json`, and the `_MUTATE` versions.

**Run.**
- `python3 wg2_pm.py checks`
- `python3 wg2_run_all.py`: about 45 min, at most 5 single-thread runs under 1 GB at a time.
- `python3 wg2_grade.py`, then `python3 wg2_grade.py --mutate` (after `WG2_MUTATE=1 python3 wg2_pm.py checks`).

## Correction 2026-11-04 (after WG3, d4d81be402)
"No rule on record lands in between" (Result section) was written when only R0 and R1 had been tried. WG3 then ran the record's one web rule, CFG354's bound-only switch T1. From a baryons-only start it never turns on and fails low with law-off. Read the line as: **no rule tried lands there: off, QUMOND on, or the record's bound-only switch (T1)**. No number here changes.

