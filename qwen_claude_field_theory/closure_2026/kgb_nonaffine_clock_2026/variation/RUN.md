# Frozen verification record

The final combined run completed successfully: **14 exact Python tests and
9 Lean theorems passed**, with no Lean warnings or `sorryAx` in the recorded
output. Every printed theorem depends only on `propext`, `Classical.choice`
and `Quot.sound`. `run_001/manifest.json` validates against current inputs.

The task began at `583fdf69a597ef9ed57b4f9ced48dd457c8ef2de`; the shared
repository advanced while work proceeded. The actual verification run records
commit `3363fda06c2835ad60e3cd153042227b804095b2` and a dirty worktree.
Selected input hashes, not the task-start commit alone, identify the evidence.
No file outside this variation directory was written by this lane.

The manifest pins the test, both Lean files, both reports, prior variation
record/test, the exact principal source, the target-metric/source-unit files,
and the Lean environment definitions. Input hashes before and after the run
agree. Important external-to-this-directory source SHA-256 values:

```
kgb_mass_compatibility_2026/conformal_inverse.py
d8629d79b04cac4b60c24187134d23580c93314b6a687d4d8df2cc1551a720f5

kgb_joint_action_2026/joint_static.py
920921c4b1e9057ae035a7c4171868448f4c6c3ab3e5f92989a9c4a1ad48b190

ticking_kgb_inverse_2026/kgb_inverse.py
e62a7b14332fe17ddf7e84cfe4229c909283ec81634fe097bdcafa491ad138b8
```

From the repository root, direct reproduction is:

```sh
python3 -B qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/variation/test_nonaffine_variation.py
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/variation/NonaffineAlgebra.lean
lake --dir qwen_claude_field_theory/closure_2026/clock_constitutive_construction_2026/lean_formalization_2026 env lean /Users/carlzimmerman/new_physics/zimmerman-formula/qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/variation/ConeWindow.lean
```

The combined bounded runner command is preserved verbatim in the manifest.
It ran at `2026-09-10T15:24:24.063162+00:00`, took 4.869752 seconds and returned
exit status 0. The wall timeout was 60 seconds, the output cap 1 MiB, with no
additional memory/CPU/core/thread cap. Software: Python child 3.9.6,
SymPy 1.14.0, runner Python 3.11.13, Lean 4.34.0-rc2, Mathlib revision
`85e3a25e006c35636f0e53b0e9296caca2685bc0`. No numerical sampling, randomness,
tolerances or numerical rank assignments enter this run.

Manifest validation command:

```sh
/opt/homebrew/bin/python3.11 -B /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula qwen_claude_field_theory/closure_2026/kgb_nonaffine_clock_2026/variation/run_001/manifest.json
```

It returned `valid evidence record; mathematical interpretation requires
review`. This is provenance validation, not a physical-theory certificate.
The reports keep the conditional physical mappings separate from exact
symbolic/Lean results. Final mathematical proofreading covered only the new
variation files; a uniquely forced trace-index typo was corrected before the
recorded run. No unresolved typographical issue was found. The full-theory,
source-normalization and common-mass existence gaps remain explicit.
