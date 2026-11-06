# AL1: why the 2026-11-06 row-B disc fits ended at I0 = 0 (scorer-side check). FROZEN CRITERIA, before any script or number

Written before any AL1 code or run. Committed alone. MOCK cubes only; no ALMA data (the release cutouts were deleted as the runbook requires), no download.
Scores nothing. Changes no frozen file, no prediction, no scorecard row. κ = ½ FITTED; one disc excludes no model; not theory closed.

## What is on record (read before writing this)
- `finish_2026_11_04/FN2_dated_tests/release_2026_11_06/ac1/ac1_score_RELEASE.json`: both thin-disc fits (incl-mom0, incl-Tadaki) end with
  I0 = 0.0, all six trial chi2 = 2,626,595.68 (identical), chi2/N 0.936 in both, eV_c = nan. No committed MOCK or validation fit has I0 = 0.
- The 3D line centroid is z 2.52253 against the scorer's z 2.52455: about -172 km/s. The fit starts at vsys0 = -29 km/s (kinematic_pa).
  Every committed MOCK puts the line at v = 0 exactly (write_mock_cube, vsys 0), so an off-centre line was never tested.
- `cfg942_common.lm_fit`: projected LM, bounds clip I0 at 0; the finite-difference step for I0 is 1e-4 |I0| (+1e-30).

## Hypotheses
- **M (mechanism):** I0 = 0 is an absorbing state of lm_fit: the model is proportional to I0, so at I0 = 0 every other Jacobian column is
  exactly 0 and the I0 column is a 1e-34 step; no step can leave it, and chi2 there is sum (D/sigma)^2 whatever the other parameters are.
- **H1 (trigger):** a start whose systemic velocity is off by ~140 km/s (with sigma0 start 40) puts the model where the line is not; an LM step
  that drives I0 below 0 is clipped to 0 and accepted because the zero model is cheaper than the misplaced one.

## Checks (`al1_check.py`; one run; outputs `al1_check.out/.json`)
- **T0** sha256 of `ac1_score.py`, `ac1_fit_checks.py`, `cfg942_common.py`, `ac1_predict.py`, `ac1_score_power_results.json` identical at start and end.
- **T1 (M)** On a MOCK cube box at p with I0 = 0: every non-I0 Jacobian column (forward differences as lm_fit forms them) is exactly 0.
  And lm_fit started at I0 = 0 returns the start parameters unchanged (max |dp| = 0). PASS iff both hold.
- **T2 (signature)** At I0 = 0 the cost equals sum (D/sigma)^2 to relative 1e-9, independent of vf (three vf values give the same cost to 1e-9).
  PASS iff both hold. This is the identical-trial-chi2 signature of the release.
- **T3 (H1 on MOCK)** MOCK cube at release-like settings: pix 0.015", beam 0.105" x 0.087", dv 6 km/s, per-channel noise 0.132 mJy/beam,
  S dV 0.718 Jy km/s, gas R_e 1.56 kpc, V_c 430, Tadaki inclination, seed fixed. Run the frozen scorer's `measure()` (G1-3D decides, no injection)
  twice: line at the scorer's z (T3a, v = 0) and line shifted to -172 km/s (T3b). Record I0 and validity for both inclination branches.
  - H1 REPRODUCED iff T3b ends with I0 = 0 in at least one branch AND T3a ends with I0 > 0 in both.
  - H1 NOT REPRODUCED otherwise (reported as such; the trigger then stays open).
- **MUTATE (`AL1_MUTATE=1`)** T3b with the fit's vsys start set to the true -172 (a hook in AL1's own copy of the start, not in a frozen file).
  If H1 is the trigger, I0 > 0 in both branches; the run must then differ from the main T3b. If the main T3b did not collapse, MUTATE is
  NOT DIAGNOSTIC.

## What this lane cannot do
- It cannot say what the real cube gives under a repaired fit: that needs the cube again (a new 34.7 GB stream = owner's yes) and a repair
  filed as a scorer addendum by the owner before it runs. AL1 may describe repair options; it applies none.
- A MOCK reproduction shows a plausible trigger, not that it was the trigger on the real cube.
