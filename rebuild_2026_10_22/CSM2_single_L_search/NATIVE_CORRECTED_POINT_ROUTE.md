# Priority next test: actual corrected model at the frozen native point

The legacy NL1 main/rerun tests fixedT12.3 and an extrapolated historical CL3
switch. They do not answer how CSM1's actual same-column correction grades at
the measured native level. Before further uniform-mesh batches, freeze runnable
criteria/inputs/resources for exactly L=4.8646, the originally frozen rounded
NL1 main point. No new point is chosen to improve fit; the estimator remains
known to be binning-sensitive, so this is a numerical native-point test, not
robust physical derivation of L. Keep all legacy verdicts separate.

First check for an already running or completed corrected native-point test;
reuse and audit matching work instead of launching a duplicate.
Use the unchanged audited calibration/calibrate_replay.py through its existing
launch_exact.py --skip-baseline --levels 4.8646 interface and the pinned
run_003_audited reference. Choose a new owned output directory; do not overwrite
old runs, edit launchers or touch active NL1 work. Inspect actual dependency
closure and source hashes first. The frozen criteria must verify baseline
reference and cached-template controls against saved audited evidence, preserving
all source/input versions; no rerun of an unchanged baseline as new science.

The scorer already runs full corrected own/basin SPARC/groups/clusters and
switched/pure-halo lensing on separate canonical/alt footings. Preserve original
FP0/P4/EM1 units, actual pipeline-specific EPS tables/backgrounds, S9 shape,
same unfloored mass-dependent column for switch and core, equality-law handling,
kappa=.5, basin assignments and existing cuts. There is no independent T input.
Do not substitute the legacy NL1 CL3 T11.5915 or tune a new switch parameter.
Use the original full covariance and pinned two-halo template, and check actual
core/flag logs at this point. No data download or historical-input changes.

Bound the new point to one numerical thread, wall900/CPU600 and observed RSS<1GB,
using existing runner manifests and complete input hashes before/after. Inspect
all normal source controls, actual flags/decision counts,175SPARC per source
cell,63groups,15cluster keys at2h cells, own/basin core-amplitude identity and
finite source scores. Independently regrade completed raw summaries and score
arithmetic; reject a deliberate decision/grade perturbation. Retain all failures
and exact pipeline-column differences. If calibration fails a necessary cut,
that excludes this numerical point only. If it passes, it is merely a candidate:
remaining unchanged heldout/dwarf/MW requirements still need their own checks.
No full-model pass, robust derivedL, global continuous obstruction or original
floating continuum theorem follows from this one point.

Publish only the completed verified point with explicit relation to CSM1 and
legacy NL1. Keep the fixed mesh continuation in GROUP_MESH_008_ROUTE.md as the
following continuous-feasibility route; do not discard its pending/inconclusive
inventory or promote the existing L[2.62,2.76] union to global coverage.
