# Verification performed

On26 October2026:

-22 archived manifests passed schema validation and verification of pinned input
  and result hashes. Full output: manifest_validation.json.
- audit.py completed successfully through the provenance runner. It asserts
  rejection of deep-pole order8 cases, checks corrected pole plausibility,
  independent eigenphase printouts modulo pi, and nuclear derivative refinement.
  Its results include all numerical comparisons and explicit false flags for
  physical DR rates and new photon coupling.
- Four corrected300-energy scans completed; all locate the candidate at0.199.
  The corrected outer-radius scan completed at20,40,80,160 with explicit intervals.
- Figure regenerated from archived JSON and visually inspected for labels/cropping.
- No new physical photon/chemistry integration was run. No conservation residual
  for an uncomputed physical reaction network is asserted. The old manufactured
  rate tests were not relabeled as physical evidence.

Manifest verification (run from repository root):

```sh
python3 /path/to/computation-audit/scripts/validate_manifest.py --root . \
  two_state_mechanism_2026_10_26/continuum/run_audit/manifest.json
```

For each other `run_*/manifest.json`, use the same validator command. Each
manifest contains the exact executed command, software declarations, limits,
pinned inputs and outputs. Re-run changed configurations into a NEW output
folder and contract; do not overwrite immutable runs.

Quick independent aggregate recheck without changing recorded evidence:

```sh
PYTHONDONTWRITEBYTECODE=1 OPENBLAS_NUM_THREADS=1 python3 \
  two_state_mechanism_2026_10_26/continuum/audit.py \
  --output /private/tmp/continuum-audit-recheck.json
```

For a new continuum point, first rebuild the external dependency, use a new
work/output directory, and explicitly set `--multipole20`. The driver's default8
is historical and rejected. See BUILD.md for the two-thread override and the
upstream test timeout. No complete upstream benchmark pass is claimed.

Limits: manifest validity proves provenance, not physics. The continuum target
basis, angular coverage, nuclear outgoing flux and reaction branching are still
incomplete. This is a bounded checkpoint in an unresolved research objective.
