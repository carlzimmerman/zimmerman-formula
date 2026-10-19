# FSP-009 reproducibility and interpretation

Use `/Users/carlzimmerman/new_physics/zimmerman-formula` as repository root. Keep completed run directories and declared inputs immutable. A later correction requires a companion restriction or a new execution record.

- [Proton reproduction](nonborn_proton/REPRODUCE.md) records the source-notebook/static coefficient and distinct full-HB finite-band commands. These are different approximations with declared source inputs; neither is a complete physical mass prediction.
- [Vacuum reproduction](vacuum_global/REPRODUCE.md) records exact normalized-partition jet checks, action contacts and source-action reflection controls. Fixtures validate the estimator algebra, not QCD expectation values.
- [Common-response reproduction](common_response/REPRODUCE.md) records exact source coefficient differences and independent effective-action/tensor angular checks, with the chiral/soft limit order retained.
- [Connected-response control](coordinator/vacuum_let/REPRODUCE.md) records the positive finite-ensemble counterexample to a raw-to-connected inference and exact constant-density sphere identity. It is not a QCD counterexample.
- [Photon-filter reproduction](photon_mass/REPRODUCE.md) records exact propagator projectors and the full-HB/independent Dirac numerical controls. Its imported HB code and frozen inputs are part of the dependency closure. The coordinate-moment and six-mass companions postdate that author run; the separate reviewer records identify what was actually checked.

All new executed mathbox-v2 records may be checked with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Use the installed bounded runner for new executions with the local contract's exact execution_artifacts, fresh output/result paths and its stated wall/CPU/thread/log caps. No RLIMIT_AS is requested on macOS. Do not execute a command copied from an untrusted evidence record. Independent reviewer code/results are separate evidence from author reproduction.

Validation proves recorded execution/input freshness, not the physics application or an interval-certified quadrature tolerance. Source receipts distinguish version authentication, inspected equations and the missing source-to-target implication. Shared Git HEAD may advance through unrelated work; exact content hashes identify the ancestry and audited revision.

The common-response clean review and both photon-review runs use explicitly recorded bounded subprocess executions outside the bundled runner. Their v2 validation is retained; unavailable Git observations and unmeasured dirty flags are labeled rather than reconstructed. Review provenance distinguishes definitions/source-first algebra, subsequent code, prior numerical-answer exposure and the post-target coordinate addition. Mechanical validation files are not mathematical computation records.
