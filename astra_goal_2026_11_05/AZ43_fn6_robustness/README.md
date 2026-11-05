# IN PROGRESS — FN6 robustness grid has no final label yet

Criteria096759f915 freeze143(p,L_MW) points and729 local MW cells on
each footing. Reference amendment71c67eda3c selects an archived alt
survivor for its known-answer comparison; it changes no grid or gate.
Kappa=1/2 FITTED; not theory closed. This is the Gaussian form-R model,
not a native v3s-action result.

## Verified so far

- The original p=.35,L_MW=1.5 small-gate point reproduces8/8 checks
  across both footings. Its canonical MW anchor reproduces4/4; the
  alternative footing's own archived anchor reproduces4/4.
- The nu=1 small-gate twin passes its two Newtonian Solar controls and
  fails all eight original-anchor comparisons. The canonical MW twin
  passes its Newtonian-field identity and fails the original MW anchor
  (4/5 checks). Outputs are separate.
- Small-gate points0-41 and56 have both resolution rungs. All forty-three numerical
  pair checks pass. At the old anchor56, dwarf counts remain18/24 on
  both footings, the largest matched dispersion change is below0.085%,
  and the largest SPARC statistic change is below0.00005dex.
- At point56 on canonical, all729 MW cells have both rungs and V1(a,b)
  at both endpoint widths. Coarse15 passing cells become10 at refine2;
  all10 pass on both rungs. Five coarse-pass flips remain numerically
  unresolved rather than being retained as survivors. Maximum absolute
  changes over all729 cells are0.04714Msun/pc² in K0 and0.02192km/s in
  vc. The independent V1 checks pass on both rungs.
- Alternative-footing point56 now has both full729-cell rungs, with77
  cells passing at both resolutions. The full parameter grid remains open.
- An uninterrupted recomputation of the first16 canonical cells agrees
  exactly with the resumed full-point checkpoint. Completed-point resume
  exits0 without recomputing. Input hashes are checked before reuse.

These are partial results, not a final window count over143 points.
The recorded five MW flips illustrate why the full convergence pairs
are retained even when force differences look small.

## Runtime and checkpoint design

`engines.py` loads the original definitions/data read-only; it does not
execute their production loops or write in old folders. `small_worker.py`
runs one parameter point/rung and records dwarf evaluations as well as
the original gate summaries. Fine runs also recompute every recorded
coarse dwarf witness, even if their own search stopped earlier.
The radial kernel is constructed in row chunks; it agrees exactly on
the deterministic validation fixtures with the original matrix.

`mw_worker.py` saves each cell atomically and exits75 after a bounded
batch. It reuses the original solver, full even angular rank and V1
separable-reference calculation. Its completed checkpoint includes
cell coordinates, masses, widths, scalar observables and line flags.

The parent batch scripts run one child at a time and watch RSS with a
1GB threshold. Observed small-anchor fine peak is815MB; canonical MW
fine peak is636MB including V1. Each child has one numerical thread.
The shared heavy queue was not used. No1024³ process was identified in
the filtered process inventory; the existing W1 queue shim was live.

No new data have been downloaded. The failed first alt-anchor lookup,
its script and sanitized traceback are preserved in
alt_anchor_lookup_failure/. This was missing archived reference data,
not a failed observational comparison; A1 records the correction.

## Continue

From the repository root, a bounded small-gate batch is:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ43_fn6_robustness/batch_small.py --indices all --max-tasks 2 --resume

It skips verified complete checkpoints and exits75 while work remains.
Use `--mutate` for the independent nu=1 tree. A MW batch is:

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python3 astra_goal_2026_11_05/AZ43_fn6_robustness/batch_mw.py --index 56 --footing alt --rung 2 --max-batches 6 --resume

Use the appropriate point index, footing and rung. Parameter indices
come from `engines.points()`, with the old anchor at56. Complete the
small-gate pairs first to identify points still eligible for all-five
survival; a decisive small-gate failure does not require a MW solve.
The final report must distinguish such exclusions from unresolved gates.

`check_pairs.py` currently aggregates completed small and MW pairs into
main/small_pair_checks.json (or mutate/ with `--mutate`). It deliberately
does not issue a final robustness label. Remaining work includes the
rest of the parameter grid, eligible MW pairs on both footings, the
mutation grid, final gate aggregation and a final README verdict.

## First small-gate numerical failures retained

At the93-pair checkpoint,91 pairs meet all small-gate numerical lines.
Point91 (p=.425,L_MW=1.0) and point92 (p=.425,L_MW=1.25) miss the frozen
T2 dispersion-change line1% on both footings. The worst witness is
Andromeda IX at mass297187.1284574018Msun, widths.00556318454 and
.00695398068kpc. Relative changes are1.911659%/1.913153% (canonical/alt)
for point91 and1.166178%/1.167077% for point92. Dwarf pass lists themselves
do not flip, but that does not waive the numerical line. These T2 rows
remain UNDECIDED; any separate decisive physical gate remains separately
gradable under the frozen rules.

verify_dwarf_failures.py freshly recomputes all8 witness values at the
same2000/4000 radial sizes. All8 agree with their saved values, reproducing
the failed ratios exactly. It uses the unchanged bounded-kernel definition,
checks source identities, and writes separate diagnostic outputs. Runtime
is under1second, peak RSS257MB. No tolerance, grid point or resolution was
changed to obtain a pass. Remaining original-grid and mutation work continues.

The next checkpoint contains 103 paired points (indices 0 through 102).
Of these, 101 meet the small-gate numerical lines. The only failed points
remain 91 and 92, on T2 on both footings; newly completed points 93 through
102 meet those lines. This is still an incomplete robustness grid, with
eligible MW work and the independent mutation grid outstanding.

At 113 pairs (indices0–112),103 meet all small-gate numerical lines.
In addition to91/92, points104–111 fail T2 on both footings. These are
p=.45 at L_MW=1,1.25,1.45,1.475,1.5,1.525,1.55,1.75. Maximum relative
dispersion changes range from1.0881% to3.7326%, exceeding the frozen1%.
No other small-gate numerical line fails at this checkpoint. Failed T2
rows remain UNDECIDED; separate decisive physical gates are kept separate.

At123 pairs (indices0–122),107 meet the small-gate numerical lines and16
have T2 failures on both footings. Newly failed points117–122 have p=.475
and L_MW=1,1.25,1.45,1.475,1.5,1.525. Their worst dispersion changes range
from2.8930% to7.1744%, versus the unchanged1% line. Points113–116 meet the
numerical lines. The remainder of the frozen grid is still running; no
resolution, tolerance or point has been changed to recover a pass.

At133 pairs (indices0–132),110 meet the small-gate numerical lines and23
have T2 failures on both footings. The additional failures are123–126
(p=.475, L_MW=1.55,1.75,2,2.25) and130–132 (p=.5, L_MW=1,1.25,1.45).
The largest relative change is13.3046%, versus1%. Points127–129 meet the
numerical lines. The final ten main-grid pairs are running separately.

verify_all_dwarf_failures.py now selects the worst cached dispersion witness
for every failed T2 footing in the saved pair-audit snapshot, verifies input
and engine identities, and recomputes both unchanged resolutions. For this
133-pair snapshot, all92 values reproduce within2.23e-16 relative;184/184
checks pass. The complete scientific replay output repeats byte-identically.
This validates the numerical failures, not a final physical grid verdict.
The original first-failure replay is retained separately. No saved point,
threshold or resolution was changed.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python verify_all_dwarf_failures.py

Run from this directory in the recorded numerical environment. Update the
pair audit first when intentionally verifying a later completed-grid snapshot.

## Complete main small-gate grid (not a final robustness verdict)

All143 prescribed main-grid points now have both numerical rungs.110 meet
the small-gate numerical lines;33 fail T2 on both footings, with no other
small-gate numerical failure. Failed indices are91–92,104–111,117–126 and
130–142. The largest dispersion change remains13.3046% versus the frozen1%.
The last ten completed points all belong to the failed p=.5 row.

The current full-snapshot worst-witness replay recomputes132 values from
all66 failing point/footing combinations.264/264 checks pass; maximum
stored-versus-recomputed relative difference is4.45e-16, and the scientific
report repeats byte-identically. This confirms numerical nonconvergence;
it does not turn those T2 failures into physical exclusions. A separate
stable decisive physical gate may still exclude a point under the criteria.

The independent nu=1 mutation grid has started. Eligible local MW pairs,
mutation completion, final per-gate aggregation and robustness labels remain
outstanding. Main small-grid completion alone is not completion of AZ43.

The first20 mutation tasks have now finished (indices0–9, both rungs),
and the bounded batch exited75 normally. All10 pairs meet the numerical
comparison lines; every point fails the dwarf and SPARC physical gates
on both footings, so the nu=1 control bites without a convergence failure.
All20 output identities and known-answer check arrays were verified.
The other133 mutation pairs and eligible MW pairs remain outstanding.

A2 (5d675a522d) fixes controller-only signal handling before continuation:
the handler now only sets a flag, and the polling loop forwards SIGTERM once.
The bounded process fixture failed the old handler-structure check, then
passes9/9 twice with the correction, including a live parent interruption,
child termination, exit75, exact resumed outputs and idempotent completion.
This validates process control, not a new scientific result. Numerical
worker identities and all completed grid outputs are unchanged.

    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python check_batch_signal.py --tag NEW_TAG
