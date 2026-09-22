# I14 verification and handoff

Delegated base: `e3af62a453ca6625db8428f6d32957b27a7f1331`.
Observed HEAD at final verification: `c5f8887cd91425608d5fc74be8de1f420aa1796a`.
No commits were made by this work. The four cited physical source files and
tracked I14 were byte-identical in the delegated base and observed HEAD.
Only this task's I14 working copy was changed among those files. Existing
unrelated dirty/untracked files were left untouched.

## Results

- I14: 34 theorem declarations, including 17 new ones. The original 17
  proofs remain; unsupported scope comments were corrected.
- `lake env lean I14_phantom_vacuum_wall.lean`: exit 0, no errors.
- 29 printed certificates have exactly `propext`, `Classical.choice`,
  and `Quot.sound`; no `sorryAx`. Source scan found no sorry/admit tokens
  or axiom declarations. All new theorem declarations print their axioms.
- Lean 4.34.0-rc2, arm64-apple-darwin24.6.0, compiler commit
  `6a10ac8c22beadecabdbb0919c2b50214762f91d`.
- `git diff --check -- fable_independent_2026/lean_2026/I14_phantom_vacuum_wall.lean`:
  exit 0.
- Computation runner completed; manifest validator returned
  “valid evidence record; mathematical interpretation requires review.”
- Independent direct-form matrix checks: 30 cases; maximum eigenvalue error
  6.217248937900877e-15, recurrence error 1.2656542480726785e-13,
  orthogonality error 3.572120568957502e-13. These are floating finite
  checks and supplement the universal written proof.
- Exact symbolic checks passed for the G155 Hessian coefficient, dressed
  potential, asymptotic limits, nonconstant radial flux, and the different
  L5/G155 derivatives at zero.

## Regeneration commands

From `fable_independent_2026/lean_2026`:

```sh
lake env lean I14_phantom_vacuum_wall.lean
```

From the repository root (an existing results file is overwritten by this
standalone command, so use a fresh output path when preserving provenance):

```sh
python3 real_research/reviews/spectral_spine_closure_2026_09_22/i14/verify.py /tmp/i14_recheck.json
```

The bounded run's exact argv, software versions, limits, input/output hashes,
Git revision and dirty state are in `computation_run/manifest.json`.
The proof report, source report, code, logs, and source files are pinned in
`sha256.json`. Validator command used:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.0.1/skills/computation-audit/scripts/validate_manifest.py real_research/reviews/spectral_spine_closure_2026_09_22/i14/computation_run/manifest.json --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

## Remaining obligations

The exact finite spectrum has a complete written proof, and its sine-mode
energy identities and nonzero norm are Lean-certified. The general basis
completeness/minimum theorem is not a Lean declaration in this patch.
The sharp all-box floor and confined trichotomy are fully Lean-certified.
The physical map is not closed: the cited action/profile sources do not
produce I14's operator or identify its negative potential parameter with
the a0 scale ratio. SOURCE_BRIDGE.md derives concrete mismatches.
