# Algebraic source conservation checkpoint

`REPORT.md` contains the complete dimension-independent C1 proof and physical calibration. `source_and_inputs.json` records source versions/locators and actual input hashes. `contract.json` declares the finite surrogate and exclusions.

Authoritative records: `runs/main_a/manifest.json` (completed) and `runs/control_a/manifest.json` (intentional failed trace-projector mutation). Both validate. `NORMALIZATION_REVIEW.md` independently checks the root normalization screen without running its script.

From repository root, direct regeneration uses a fresh folder:

```bash
python3 sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/algebraic_source/checks.py --output-dir sol61_push/puzzle_32pi/vacuum_coupling_2026_10_06/algebraic_source/runs/reproduction_new
```

The exact standard-runner argv and input list are in the authoritative manifests. A new audit-grade run must use fresh output/result paths. Finite ranks corroborate the full proof; they do not classify all dimensions or restricted physical matter models on their own.
