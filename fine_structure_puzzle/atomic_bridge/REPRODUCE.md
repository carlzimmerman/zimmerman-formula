# Reproducing FSP-002

Use repository root /Users/carlzimmerman/new_physics/zimmerman-formula. Authoritative runs are hydrogen/run003, qcd_mass/run_002, scalar_bridge/run_002 and coordinator/run_001. coordinator/control_001 intentionally fails its concavity sign assertion. [Validation](reviews/MANIFEST_VALIDATION.json) pins the exact manifests.

Python/library versions and bounds are in each contract/manifest. Rerun finite checks into fresh files without overwriting saved evidence:

```sh
python3 fine_structure_puzzle/atomic_bridge/hydrogen/compute.py --output /tmp/fsp_hydrogen_new.json
python3 fine_structure_puzzle/atomic_bridge/qcd_mass/discriminator_v2.py --output /tmp/fsp_qcd_new.json
python3 fine_structure_puzzle/atomic_bridge/scalar_bridge/check_scalar_bridge.py --output /tmp/fsp_scalar_new.json
python3 fine_structure_puzzle/atomic_bridge/coordinator/selection_check.py --output /tmp/fsp_atomic_selection_new.json
```

For bounded provenance-recorded runs use each route's contract and a new directory: [QCD commands](qcd_mass/REPRODUCE.md), [scalar commands](scalar_bridge/REPRODUCE.md), hydrogen/reproduce.py. Coordinator runner arguments are in its manifests. Never reuse saved run directories.

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py PATH_TO_MANIFEST --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

The validator checks provenance, not physical validity. Historical hydrogen runs used earlier script hashes; the initial QCD partial formula omitted the variable-electron threshold; scalar run_001 failed at a macOS resource limit before calculation. These are retained, not current positive evidence. Tiny hydrogen effects use derivative/high-precision rescaling, not unresolved binary64 energy subtraction.

[Atomic selection](coordinator/ATOMIC_SELECTION_CLAIM.md), [QCD sensitivity](qcd_mass/CONSTRAINED_SENSITIVITY.md) and reviews contain analytic work distinguished from executed checks. No script computes the missing QCD cosmological coefficient or microscopic scalar potential. [Launch-phase reproduction](../REPRODUCE.md) remains separate.
