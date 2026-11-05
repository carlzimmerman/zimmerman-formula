# AZ43 amendments

## A1 — reference lookup correction, after anchor attempt, before MW grid

The first alt anchor attempt found that the canonical surviving cell is
not among alt's saved passing rows at p=.35,L_MW=1.5. FN6 retains only
passing rows and the best row in that summary, so no saved numerical
reference for that particular canonical cell exists there. No robustness
grid has run and no numerical tolerance changes.

The canonical known-answer comparison keeps its exact original survivor.
For alt, compare the first saved original passing row at the same p,L_MW,
with its own cell coordinates. The common729-cell robustness grid remains
unchanged and retains the canonical survivor on both footings. Record
both the reference cell and the original lookup failure. This corrects
which archived observable exists; it does not choose a new observational
gate, expand a prior, or claim the canonical cell passes on alt.

## A2 — flag-only batch signal forwarding, after first ten mutation pairs

The batch controller currently calls child.poll/send_signal inside its
signal handler. This violates the flag-only handler requirement. Before
continuing the remaining mutation tasks, move child notification into the
normal polling loop and send it once per interrupted child. Preserve all
numerical engines, point/rung ordering, memory limit, output identities,
budgets and grading lines. Existing completed scientific outputs remain
valid because this is controller-only process handling.

Verify handler structure and an actual parent SIGTERM/child-forward/resume
cycle using a bounded stand-in child with independent deterministic output.
The fixture tests process control, not the physics. Require parent exit75,
child termination, preservation of completed work, exact resumed fixture
output and idempotent resume. Commit this amendment alone before editing
the controller; no scientific tolerance is changed.
