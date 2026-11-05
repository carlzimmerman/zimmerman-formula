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
- Small-gate points0-6 and56 have both resolution rungs. All eight numerical
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
