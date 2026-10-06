# Vacuum-constraint selection checkpoint

Read `REPORT.md` for the action derivation and restricted result; `ANALYTIC_UV_REVIEW.md` is the independently reconstructed peer-route audit. Source and original-input provenance is in `source_and_inputs.json`; the computation contract is `contract.json`.

Authoritative evidence: `runs/main_b/manifest.json` and `runs/control_b/manifest.json`. Main succeeds; the intentional dropped-response-derivative control fails. Both records validate. `runs/main_a` retains a caught and repaired factor-two implementation error, with its historical script hash; it is not a current-code run.

From repository root, direct regeneration must use a **new** output folder inside this lane:

```bash
python3 sol61_push/puzzle_32pi/selection_2026_10_06/vacuum_constraint/checks.py --output-dir sol61_push/puzzle_32pi/selection_2026_10_06/vacuum_constraint/runs/reproduction_new
```

Use the exact standard-runner command/input list recorded in the authoritative manifests if new audit-grade evidence is needed; choose fresh output/result paths. Validate an existing authoritative record with:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py sol61_push/puzzle_32pi/selection_2026_10_06/vacuum_constraint/runs/main_b/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

No local binary copy of the primary sequestering paper is claimed. The publisher version and exact equation locators are recorded; external scientific interpretation was checked against that source separately from code validation.
