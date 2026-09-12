# Commands and provenance

Working directory: `/Users/carlzimmerman/new_physics/zimmerman-formula`.
Only files under this audit directory were created by this work package.
No Claude source or prior action file was edited. No commit was made.

Commands actually executed, each with exit 0:

```bash
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_principal_audit_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/l192_principal_audit_2026/run_audit.py
```

Four tests passed in .443 seconds. A peer ran the same four tests successfully.
`run_audit.py` prints and executes the complete bounded-runner argv, then
executes `validate_manifest.py --root` against the resulting v2 record.
Experiment exit 0; manifest-validation exit 0. Runtime was 3.693498 seconds,
wall-clock cap 120 seconds, combined log cap 1 MiB, cooperative numerical
thread cap one. No hard memory or CPU-affinity bound is claimed.

`run_001/manifest.json` records actual base
`05d0eb98ae78f5d37d5cfcc67f3cec591e897477`, dirty state, argv, input hashes
before/after, software versions, output hashes, actual exit, and limits.
`run_001/result.json` retains the exact Hessian/Schur identities and all ten
source epochs, including both q conventions for all five unstable epochs.
`stdout.txt` and `stderr.txt` retain the actual process output.

The source `cs2` function is extracted from the inspected L192 AST and
executed in isolation with NumPy; importing its whole script would execute
its top-level write to Claude's result file. That import is deliberately
avoided. Both the original source and original result are hashed inputs.

A read-only `git diff --stat 5fdec3d9a --` on the L192 script and result
returned no differences, confirming the audited source remained the
requested version despite later shared-checkout commits.

Selected SHA-256 hashes:

| File | SHA-256 |
|---|---|
| principal_audit.py | fba62ae32a96efde804c438c7565471d1c2ecf0755531daaf6af1cf26e91392b |
| test_principal_audit.py | 12cefe942fc8bbf502f11a9a5c839db004edada0e01623e87d26b3bb0a1ea128 |
| run_001/result.json | 0131bb4a6ee139df7598e48432b020860d9be7351ac33ff7f64f6cde8fe21a63 |

The result is a restricted-symbol counterexample and a correction to the
claimed reduction, not a full Einstein/cubic stability theorem, a nonlinear
attractor, or a completed MOND theory.
