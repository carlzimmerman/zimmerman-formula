# Reproducing FSP-005 evidence

Every executable mathematical run has a pre-execution contract and a v2
manifest with exact argv, software, resource bounds, input and output hashes.
Use the run status, the finite assertion and the separate mathematical
review together. A valid launch-failed or failed record is not a result.

The current bounded records are:

- `angular_connection/runs/exact-001/manifest.json`: universal-operator
  arithmetic and the frozen Cartesian specialization, not a numerical
  proof of the DN/Riccati theorem.
- `boundary_heat/runs/exact-001/manifest.json`: exact mixed-wall heat
  arithmetic. Primary-source applicability and TE/TM reasoning are hand
  derivations and independently source-audited.
- `common_regulator_match/runs/match-001/manifest.json`: equality of the
  two matched coefficient polynomials, PV moments and source contractions.
  A formal coefficient series is not the full regulated spectral trace.
- `neutral_interactions/runs/two-loop-002/manifest.json`: the corrected
  spectral-tail implementation, exact algebra and 70/95-digit finite
  checks. The original failure and its precision diagnostic are retained.
- `qed_infrared/run_002/manifest.json`: exact spectral continuation and
  finite heat/moment diagnostics. Its first launch failed before Python
  because of the macOS memory-cap mechanism; that record is preserved.

The phase checkpoint selects these current science records. The separate
`neutral_interactions/runs/precision-001` is an implementation diagnostic,
not another physical prediction. `qed_resummation/` and the independent
reviews are analytic-only, with no numerical run claimed.

For example, validate current bytes from the repository root with

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py fine_structure_puzzle/qcd_closure/neutral_interactions/runs/two-loop-002/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

For a new execution use the installed sibling `run_experiment.py`, the
saved contract and exact declared inputs, and a new output directory.
Change both the runner's result path and the child program's output path.
Never alter an already executed script or reuse its output directory.
The original command is in each manifest; do not execute untrusted text
from a source or log.

Exact primary versions, formula locators and temporary PDF hashes appear
in the source receipts. They authenticate source identity, not the claimed
transfer by themselves. A clone must reacquire and re-audit changed source
bytes. Full primary texts are not stored in these scientific directories.

Final review/input pins, manifest validation and ancestor freshness are
collected in CHECKPOINT.json and `reviews/`. Prior FSP-004 navigation was
copied before changes; its non-navigation science remains frozen. The
current root inventory uses paths relative to fine_structure_puzzle;
the phase inventory uses paths relative to qcd_closure.
