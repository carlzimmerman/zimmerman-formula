# AL1: the 2026-11-06 row-B fits ended at I0 = 0. MECHANISM CONFIRMED; TRIGGER H1 NOT REPRODUCED; trigger open

Criteria `FROZEN_CRITERIA.md` (832fb4b7f5), committed alone before the code. MOCK cubes only, NOT ALMA DATA. No download.
Scores nothing; no frozen file, prediction or scorecard row changed (T0 PASS). κ = ½ FITTED; one disc excludes no model; not theory closed.

## Result (`al1_check.out/.json`; MUTATE `al1_check_MUTATE.out/.json`)
| check | result |
|---|---|
| T1 at I0 = 0 every non-I0 Jacobian column is exactly 0; lm_fit started there does not move (max \|dp\| 0) | PASS |
| T2 cost at I0 = 0 = sum (D/sigma)^2 exactly, the same for any vf | PASS |
| T3a MOCK, line at the scorer's z: I0 0.176 / 0.177, both fits valid | no collapse |
| T3b MOCK, line at -172 km/s (scorer's vsys start -40): I0 0.172 / 0.175, vsys fitted -180, both valid | no collapse |
| H1 (vsys-start offset is the trigger) | **NOT REPRODUCED** |
| MUTATE (vsys start = true -172): V_c P-B 448 / 439, P0 430 / 421 against true 430 | runs, but NOT DIAGNOSTIC (main T3b did not collapse) |
| T0 frozen files unchanged | PASS |

## What this means
- **Mechanism (M) holds.** Once a projected LM step clips I0 to its bound 0, the model is identically zero, so no other parameter has a
  gradient, and the fit cannot leave. The release's V_c values (P-B 169/146, P0 120/79 km/s) are wherever the other parameters stood
  when I0 hit 0, with nan errors. They are not measurements, so they say nothing about B1 (the 431 km/s grid floor) either way.
- **Identical trial chi2 alone is not the signature.** Healthy MOCK fits also land all three starts on one chi2. The signature is I0 = 0.
- **The trigger is still open.** A smooth disc with the release's offset, noise, beam and channel width fits cleanly from the frozen start.
  So the real cube differs from a smooth mock somehow: clumpy or lopsided gas, correlated channel noise, a residual continuum, or a header
  or axis convention that the 0-offset mocks never exercised. AL1 cannot tell which without the cube.

## Not done (needs the owner)
- Re-reading the real cube means streaming spw25 again (34,749,031,680 B). That is a new download.
- Any fitter repair, for example fitting log I0, re-starting from the moment-0 flux when I0 reaches 0, or refusing a step that zeroes the
  model, has to be filed as a scorer addendum (like ADDENDUM_G2) before it runs on the real cube. AL1 applies none.

Peak RSS 4.1 GB, 223 s per run, single-threaded. No 1024³ run was live.
