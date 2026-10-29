# Native ng64: completed seed outputs, partial ensemble

This package publishes finished seed snapshots as they arrive so Claude can
inspect the completed data before the full NL1 ensemble is available.
`completed_results.json` records the observed seed set, metadata, completion
checks and hashes. `completed/` contains byte-identical copies of each finished
snapshot, `done.json` and final run log. No rolling checkpoint is included.

At the initial publication, seeds **3 and 7 of 9** have finished, with 895
and 991 integration steps respectively; both have 57,777 particles. The other
seven runs remain pending. This is a partial ensemble, with **no aggregate
concentration estimate or observational grade**. The original NL1 scorer
requires at least seven valid measurements before grading; it has not produced
a result at this checkpoint. Snapshot `meta.L` is the simulation box length,
not the inferred concentration level `L_nat`.

Publication checks verify seed/grid/mass identity, finite position/velocity
arrays, particle count/mass, agreement of final snapshot metadata with the
completion marker and final log, stable source hashes, and exact copied bytes.
These checks establish completed-file integrity, not simulation convergence
or a successful scientific model. No run was restarted or modified.

Reproduce the publication/integrity check from the repository root:

```sh
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 /opt/homebrew/Caskroom/miniconda/base/bin/python3 -I rebuild_2026_10_22/NATIVE_PARTIAL_2026-10-28/publish_completed.py
```

The script adds only complete seed sets and refuses to replace an existing
snapshot with different bytes. It refreshes the observation timestamp and
completion inventory. It does not invoke NL1 or compute any new fitted number.
Read the corrected-model result in `../CSM1_consistent_core_switch/README.md`:
the old fixed-T NL1 primary grade cannot establish a corrected linked-T pass,
and a native level near 4 would not itself restore the lost lensing pass.
