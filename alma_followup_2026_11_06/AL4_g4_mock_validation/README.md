# AL4: MOCK validation of filed addendum G4. VERDICT: G4 NOT VALIDATED (C: no collapse class found, so V4 cannot bite)

- Criteria: `FROZEN_CRITERIA.md` (local 31e5110862, origin 8551af59dd), committed and pushed alone before any code.
- Addendum: G4, filed by the owner in chat on 2026-11-06, commit 8ff85f806e.
- MOCK cubes only, NOT ALMA DATA. This lane scores nothing and downloads nothing.
- κ = ½ FITTED; one disc excludes no model; not theory closed.

**Per G4's own rule, G4 does not touch the real cube.** G4's text says: "If no f collapses, V4 cannot bite. G4 is then NOT VALIDATED,
and the owner decides." Rows B1–B4 of the 2026-11-06 release stay "FIT NOT CONSTRAINED: not scored". G3 stays FAILED VALIDATION
(AL3).

## Result (`al4_validate.out` / `.json`; per-job records in `jobs/`; selftest outputs in `v1_selftest/`)

| Check | Result |
|---|---|
| T0: frozen files, G3/G4 texts, the G4 filing record and AL3 code unchanged | PASS, all 92 jobs |
| K0: AL3 writer with options off = frozen writer | PASS (sha256 57413f24…) |
| K1: (a)–(d) and V3 cubes equal AL3's sha256 | PASS, 36/36 |
| T1: G4 live, 6 fits per detected cube, all final I0 > 0 | PASS: 72 runs, 246 fits, none at I0 ≤ 0 |
| **C**: collapse calibration, frozen fitter | **FAIL (no f collapses)**, see below |
| **V1**: no regression | **PASS**: selftest 10/10; valid counts = G2's; Tadaki P-B RMS ≤ G2 (archive compact 0.082 vs 0.090) |
| **V2**: (a) offset −172 | PASS: 6/6 valid, V_c 420–438, median error 1.5 % |
| **V2**: (c) ρ 0.24 | PASS: 6/6 valid, V_c 417–437, median error 1.3 % |
| **V2**: (b) clump, (d) a+b+c | PASS (refused): 0 valid fits, 0 confident wrong speeds |
| **V2**: (e) | NOT DRAWN, because C chose no f |
| **V3**: no false fits | PASS: noise-only and line-outside cubes, 0/6 scored each |
| **V4**: (i) and (ii) | Cannot bite, because no class (e) exists |

### C: the collapse is still not reproduced in mock cubes
Frozen fitter on class (e) = (a) + (c) with gas R_e × f, flux fixed, six new seeds per rung:
- **f = 2:** detected 6/6. Primary I0 is 0.032–0.056, no collapse.
- **f = 3:** detected 6/6. I0 is 0.016–0.036, no collapse.
- **f = 4:** detected only 3/6. Of the detected seeds, I0 is 0.007–0.033, still no collapse.

Spreading the same flux over a larger disc lowers per-voxel S/N until the cube stops being detected. It never makes the frozen fitter
fall to I0 = 0. As in AL1 and AL3, no mock reproduces the real cube's collapse.

## What G4 fixed relative to G3, on these mocks
- **Removing the PA grid ends G3's V1 regression.** Archive compact is 3/6 valid, against G3's 2/6 and G2's 3/6. Sister-like
  realistic and compact are both 6/6.
- **The new ρ₁ estimator reads −0.003 to −0.006 on independent noise** and 0.232–0.234 on ρ 0.24 cubes. G3's estimator read −0.05
  to −0.08 and 0.13–0.16.
- **Clumpy discs are now refused**, not mis-scored.
- The log amplitude still keeps every fit off I0 = 0.

## Disclosed
- **Verdict line regenerated.** The first summary (kept as `al4_validate_first_summary.out` / `.json`) printed "G4 FAILS VALIDATION".
  It had counted the undrawn class (e) as a V2 failure.
  - The frozen criteria made class (e) conditional on C, and G4's text sends a C failure to NOT VALIDATED.
  - The summary code was corrected to mark (e) "NOT DRAWN" when C chose no f. Nothing else changed: every number, line and job is the
    same. The owner may read either line. Both mean G4 does not run on the real cube.
- **Resources:** peak 3.7 GB per job, 6 jobs in parallel at nice 10, 8.0 job-hours. Mock cubes were written to the session scratch
  and deleted.

## What this means
- G4's rules behave well on every mock class that can be built: no regression, recovery, refusal and no false fits.
- The validation G4 itself requires is a mock that makes the frozen fitter collapse, as it did on the real cube. That can't be
  produced at f ≤ 4, so G4 is not validated. The real cube's collapse remains unexplained by these mock families.
- Any further step is the owner's call:
  - a new addendum with a different collapse model, e.g. a start worse than empty;
  - or leaving B1–B4 unscored for good.
- Running anything on the real cube would also need a new spw25 stream (34,749,031,680 B) and a separate yes from the owner.
