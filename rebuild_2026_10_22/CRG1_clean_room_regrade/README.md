# CRG1_clean_room_regrade: REPRODUCED, with limits on what that means

Criteria: `FROZEN_CRITERIA.md` (7a84d7c1d1), committed alone first. Spec 5ff6b230b5. Build sealed as `v1/` in 19efed282c, `crg1_results.json` sha256 da3c9104..., before any comparison. Compare: `crg1_compare.py`, `crg1_compare.json`. κ = ½ FITTED. T LOCATED, not derived. Cold dark energy, never a particle. Not theory closed. Nothing here says the data favour the framework.

## Verdict, as frozen
**REPRODUCED.** 295 compared items: 289 MATCH, 6 CLOSE, 0 DISAGREE, and no pass/fail flip in Tier A or B. Largest differences: rms, Υ, tilt, median E 0.0003; Z 0.005, which is the rounding of FG1's printed tables where those were the source; Δχ² 1.77. Each candidate's verdict by FG1's rule is unchanged on the recomputed lines, and [GAS-CONDITIONAL]'s input holds: C1's K is 15 of 15 at +0.111 at both f*. Route E's overall sentence doesn't change, so it isn't restated.

**The six CLOSE items** are all one KiDS Δχ² involving H2H, offset by 1.65 to 1.77 on every candidate and footing where it's compared. No class and no pass/fail changes. Not diagnosed: the criteria require a diagnosis only for DISAGREE.

## What this does and doesn't show
- **Shown:** FG1's numbers on these lines follow from the written definitions and the listed inputs. A coding fault in the existing graders that changes a graded cell by more than these sizes would have shown up, for the 295 items compared.
- **Not shown:** that the definitions are right. The spec was traced from the same chain, so a wrong definition carries through. This agreement is mainly a test of code.
- **Inputs taken as given:** zoom stacks and snapshots (reduced copies), raw data, EM1's map, the x48 c_f nodes, Planck-type values in the two-halo conversion (spec section 10). Errors there aren't caught.
- **Not recomputed, never agreement:** MW, DM, IC for all candidates; C2's G and Ln. K4 only confirms their sources: 12 literals and 5 files present. FG1's C1 K, X and C3's come from ZN4's row, and those were recomputed.
- **C4's K compared at h 0.672 only,** by item; its failing set covers either h.

## Separation, disclosed
- The harness loaded the project's memory index and git summary into the implementer's context, including commit subjects stating FG1's verdicts and values such as M3 +4.41 and Υ 0.75/0.76. The list is in `v1/DISCLOSURES.md`. It made no read outside its build folder. So verdict agreement isn't blind evidence.
- The criteria it was given printed the x62 flag's two numbers. One equals C4's rms.
- The spec agent read `fg1_read.py` and older outputs. A machine check of `SPEC.md` against FG1's table found only thresholds, constants and inputs.
- **Cells not voided, my decision.** The criteria void cells touched by a forbidden read, and the implementer made none. Those few lines can't produce agreement at this precision across 295 items, so a rerun would add little. The owner can overrule.

## Readings that matter for the ledger
From 17 listed ambiguities and 18 found in the build (`SPEC.md` section 11, `v1/NEW_AMBIGUITIES.md`). FG1's values match the primary readings.
- **C3's Dw pass depends on a reading (A13).** Primary, flag by host: passes. Alternate, flag by mass: fails at canonical, as C4's classes do. This is the only spec reading that flips a graded line at canonical. It should be stated beside C3's pass.
- **C4's failing keys depend on the tail (NA1).** Its K fails either way; the set differs.
- **A6(b)** moves C1's X out of the pass range at gas +0.111. That reading isn't graded.
- **NA18:** on canonical alone, as FG1 does, C3 and C4 have fewer failed lines. Alt adds S and Dw for both. FG1 reports this.
- NA5, NA8, NA10, NA15 have no second reading computed.

## Reported, not graded
- **x62 flag:** harness mode, not a grader fault; no graded cell touched (`X62_FLAG_NOTE.md`). From reading code and logs, no rerun. Agrees with FG1's own diagnosis.
- **Checks:** K1 injection, K2 data (309 files, sample sizes), K3 byte-identical, MUTATE all pass. The shear mock as first written has zero scatter and tests little; a twin with real scatter was added (NA6). Resume after SIGTERM untested. One sign fix in the EFE solver before any K cell ran.
- **Run:** 368 s total, 315 MB peak, one thread, nice 15.

FG1's files aren't edited.
