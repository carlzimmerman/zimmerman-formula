# AZ33 — LW1 board integration, both vertical-force forms

Tier 1 lane 3. This is a recorded-result integration and guard test, not new
physical evidence. Freeze before modifying the board or calculating checks.
Kappa = 1/2 FITTED; not theory closed. Footings never pooled.

Use LW1's committed JSON and README for K, X, Dw, MW and DM, overriding FG1
only for these five lines. All eleven FG1 identifiers remain on the board.
Recompute key counts from the per-key Z arrays; verify the summary has the
same count (ten of fifteen at the frozen absolute-Z<=2 gate in both h cells).
Known answers: K=10/15, X FAIL both, MW A FAIL/R PASS both, DM A NO LABEL/R
FAIL both. Verify displayed numeric literals against the source and compare
both footing values separately. Do not rerun or relabel LW1's physical models.

MW and DiskMass explicitly show both A and R. Do not select one as primary.
Retain MUST_STAY_RED including MW's existing red backing; explain that its
red backing records form A's failure, with separately drawn A/R labels on the
tile showing each form's two-footing verdict. DiskMass similarly shows its
ungraded A and failing R separately. Counts in the overall legacy colour
tally are backing colours, not a model-selection statistic.

MW: A infeasible both; R one/six in-prior cells. Include post-result scale
length discrepancy +3.9 to +4.4 sigma without treating it as a frozen gate.
DM: R ratios 1.239/1.204; A 1.477 both, NO LABEL because the a0 mutation did
not move r sufficiently. Preserve the OD1 tracer caveat. A is the field
equation, R the round rule; their disagreement is not pooled.

K becomes measured-chain 10/15 both (same tile identity to preserve guards).
X changes grey to FAIL, +0.467/rms0.476 and +0.434/rms0.444, factors2.93/2.72.
Dw remains FAIL, E1 ultra-faint +1.30 (Z6.76)/+1.26 (Z6.59).
PAPER67 footer becomes deposited v1.2, DOI10.5281/zenodo.23968171, per the
current goal's correction. No deposited document is edited.

Save the existing image as status_board_2026-11-04v3s.png before rendering.
Keep all column-0 scope and carried guards unchanged in this lane. Lane 4
will separately handle relativity. Preserve prior selftests; add controls
that turn X back to grey, promote an LW1 fail, remove either A or R, reverse
a footing's form verdict, and remove the LW1 source/override. All must be
caught. --selftest exits0; --mutate exits1 and writes no image. A separate
JSON-backed mutant intentionally drops form R and must fail the new guard.
Known-answer clean board must pass. Regenerate the markdown table and image;
inspect the image, verify title/footer/forms fit. Numerical convergence is
not applicable to this deterministic presentation integration.

PASS means accurate integration and functioning guards, not a physical pass.
FAIL means an uncaught mutation or source/display mismatch; inaccessible
source gives NOT EVALUABLE. Record hashes, tests and exact rerun commands.
