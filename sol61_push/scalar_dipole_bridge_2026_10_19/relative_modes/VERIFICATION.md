# Verification and provenance boundary

Initial observed HEAD: `f4424595259bd1ae40addb890e338f85c4f48eb1`.
The bounded runner observed concurrent HEAD
`970c67ce3dcd1c14e3488b9bce45e813ccfe0799`, with dirty state true.
The mathematical base remains CE087. These observations are not a claim of
ancestry inferred from arrival order. `source_pins.json` separately pins the
antecedent mathematical bytes. No Git mutation was made by this lane.

The command executed from the project root was:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/run_experiment.py \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula \
  --contract sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/contract.json \
  --input sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/check_relative_modes.py \
  --output sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/run \
  --result sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/run/results.json \
  --timeout 20 --max-output-bytes 100000 --max-cpu-seconds 10 --max-threads 1 \
  -- python3 sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/check_relative_modes.py
```

The program deliberately writes the fixed `run/results.json` path. Reproduce
in a fresh isolated project copy where that output directory does not yet
exist; do not overwrite this evidence record. A parameterized output-path
interface is not part of this minimal experiment.

Validation command:

```bash
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/4.0.0/skills/computation-audit/scripts/validate_manifest.py \
  sol61_push/scalar_dipole_bridge_2026_10_19/relative_modes/run/manifest.json \
  --root /Users/carlzimmerman/new_physics/zimmerman-formula
```

Observed: `valid evidence record (run status: completed); mathematical
interpretation requires review`. Python 3.9.6, standard library only;
runtime 0.041291 seconds; process exit 0. Caps were 20 s wall, 10 s
per-process CPU, 100000 combined log bytes, one requested library thread.
No memory or CPU-affinity cap was requested. No random sampling was used.

The exact rational checks verify the uniform-sphere overlap Poisson polynomial,
exterior matching, and four representative reduced-inertia/COM identities.
The Gaussian checks cover exactly the size ratios and infrared wavenumbers
in the contract. They verify the corresponding formulas in floating arithmetic,
with an independent curvature finite difference. They are not a GP-Poisson
evolution, equilibrium construction, population model or mode-stability proof.
The displayed general results are supported by their analytic derivations,
not by extrapolating the finite checks.

Final math proofreading covered the entire new `RELATIVE_MODES.md` and
equations (1)–(27). Routine edit: removed one accidental punctuation/string
artifact in the primary-source paragraph. Mathematical-token proofreading
changes: none. The subsequent background/second-order-source paragraph and
explicit restriction of the finite-band inference were substantive research
clarifications, not typographical changes. No preexisting manuscript was edited.

The lane's source note was frozen at SHA-256
`9a726b50fb9b2d6b077cf4ad06613ebf3e4fe25385846c587980f7015976eb2f`
for independent review. Its scalar-state/rigid-live-mode bridge remains
conditional. The sibling virial review in `VIRIAL_REVIEW.md` is a separate
independent review artifact and does not certify this lane's own derivation.
