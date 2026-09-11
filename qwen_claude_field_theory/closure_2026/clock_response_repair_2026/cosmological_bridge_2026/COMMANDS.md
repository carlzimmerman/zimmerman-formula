# Commands and evidence — 2026-09-11

Repository working directory: /Users/carlzimmerman/new_physics/zimmerman-formula. All relative paths below use this root.
Manifests record exact input hashes, executable arguments, environment, output hashes and exit status. Zero means the stated checks completed, not that the whole theory is correct.

## Recorded experiments

### linear_001: exit 0

Unrestricted-shear scalar action and all Euler equations match independent stress, current, Ward and background-preservation formulas.

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/derive.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/linear_001/result.json
```

Evidence: [manifest](linear_001/manifest.json), [stdout](linear_001/stdout.txt), [stderr](linear_001/stderr.txt).

### background_001: exit 0

Short physical-time homogeneous evolution with fixed clock coefficients and separately conserved dust/radiation.

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_evolve.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_001/result.json
```

Evidence: [manifest](background_001/manifest.json), [stdout](background_001/stdout.txt), [stderr](background_001/stderr.txt).

### gr_001: exit 0

Run specified stock CLASS GR comparator and record derived spectra/peak summaries.

```bash
/opt/homebrew/Caskroom/miniconda/base/bin/python -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/gr_reference.py --result-file qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/gr_001/result.json
```

Evidence: [manifest](gr_001/manifest.json), [stdout](gr_001/stdout.txt), [stderr](gr_001/stderr.txt).

### lean_001: exit 0

Two conditional real-algebra implications of the derived finite-k shear and energy Ward equations.

```bash
/bin/bash -c 'cd qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 && /opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/MetricWard.lean'
```

Evidence: [manifest](lean_001/manifest.json), [stdout](lean_001/stdout.txt), [stderr](lean_001/stderr.txt).

These are exact child commands executed under the Mathbox experiment runner. The adjacent *_contract.json files declare each bounded assertion and domain. Use a fresh output directory when repeating an experiment; do not replace the archived _001 evidence.

## Fresh regression and formalization checks

### ten_unit_tests: exit 0

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026 -p 'test_*.py' -v
```

### existing_cubic_current: exit 0

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_current_audit/derive.py
```

### existing_cubic_finite_wavelength: exit 0

```bash
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cubic_finite_wavelength/derive.py
```

### lean_recheck: exit 0

Working directory: /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026.

```bash
/opt/homebrew/bin/lake env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/MetricWard.lean
```

The new suite contains 10 tests. The existing current audit reports 13 checks; the finite-wavelength audit reports seven named checks plus its computed matrices, rank and nullspace. Lean rechecks two conditional algebra theorems with no sorry and only the displayed standard dependencies.

Test-first failures observed during implementation: missing derive module (five initial tests), missing general clock rate/Ward mapping (two added tests), missing background system (one added test), and missing background evolution module (one numerical test). The true-k0 normalization check was added for an already available raw action expression; no red result is claimed for that check.

## Manifest validation

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/linear_001/manifest.json
```

Exit 0; input and output hashes verified against the current files. The validator explicitly leaves mathematical interpretation to review.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/background_001/manifest.json
```

Exit 0; input and output hashes verified against the current files. The validator explicitly leaves mathematical interpretation to review.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/gr_001/manifest.json
```

Exit 0; input and output hashes verified against the current files. The validator explicitly leaves mathematical interpretation to review.

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/lean_001/manifest.json
```

Exit 0; input and output hashes verified against the current files. The validator explicitly leaves mathematical interpretation to review.

## Independent review and limitations

Two independent read-only reviews checked (1) covariant stress, Euler/Ward equations and the reduction, and (2) the GR installation and new L183 implementation. The mathematical reviewer also checked the final report and first-order handoff; the only prose correction was to display the Fourier factor in the momentum-stress equation.

No new radial solver was run or modified. Its unresolved convergence failure remains a gate. The finite-k first-order reduction has not yet been integrated. Stock CLASS is a comparator, not a clock CMB prediction.

## Exact changed/created files

Modified: qwen_claude_field_theory/closure_2026/clock_response_repair_2026/README.md.

Created below qwen_claude_field_theory/closure_2026/clock_response_repair_2026/cosmological_bridge_2026/:

- CLAUDE_L183_REVIEW.md
- COMMANDS.md
- FIRST_ORDER_HANDOFF.md
- MetricWard.lean
- PLAN.md
- REPORT.md
- background_001/manifest.json
- background_001/result.json
- background_001/stderr.txt
- background_001/stdout.txt
- background_contract.json
- background_evolve.py
- derive.py
- gr_001/manifest.json
- gr_001/result.json
- gr_001/stderr.txt
- gr_001/stdout.txt
- gr_contract.json
- gr_reference.py
- lean_001/manifest.json
- lean_001/stderr.txt
- lean_001/stdout.txt
- lean_contract.json
- linear_001/manifest.json
- linear_001/result.json
- linear_001/stderr.txt
- linear_001/stdout.txt
- linear_contract.json
- test_background.py
- test_bridge.py
- validation.json

Only this package and the parent checkpoint link are in scope for staging.
Concurrent Claude commits and unrelated untracked files are preserved.
