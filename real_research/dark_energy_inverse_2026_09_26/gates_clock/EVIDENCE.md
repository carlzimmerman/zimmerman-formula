# Evidence for CD26-3 gate and clock inverses

`run1/manifest.json` is the immutable computation record. The run completed
at shared revision `ecffd2af3623ff3e32318234fd51e1fac50b9126`, dirty, in
1.016129 seconds. It contains the exact command, enforced limits, Python
3.9.6 / SymPy 1.14.0 / NumPy 1.26.2 versions, contract, four execution-input
hashes before and after, and result/log hashes. It exited zero with no
missing or invalid results and unchanged input hashes.

`run1/results.json` records 45 exact SymPy identities and 15 bounded checks
and negative controls. The numerical examples use four synthetic epochs,
sixteen stored DE1 edges at the same declared gate cell, and three vacuum
shifts in one fixed quartic clock model. The historical mocks are never
executed or imported. The stored DE1 comparison is deliberately bounded to
one percent, with actual maxima 0.006624471454710568 and
0.005001897965706714 in the two separately labeled footings.

The main run was validated using:

```sh
python3 /Users/carlzimmerman/.codex/plugins/cache/openai-curated-remote/mathbox/3.2.0/skills/computation-audit/scripts/validate_manifest.py --root /Users/carlzimmerman/new_physics/zimmerman-formula real_research/dark_energy_inverse_2026_09_26/gates_clock/run1/manifest.json
```

The validator reported `valid evidence record; mathematical interpretation
requires review`. A separate read-back confirmed exactly 60 passing
results, completed exit-zero status, and all four current input hashes
equal to both recorded hashes. This validates the record and bounded
computation; the conditional mathematical and physical interpretation is
spelled out in `RESULT.md`.

`source_provenance.json` distinguishes the assigned base, prewrite checkout,
run checkout, and subsequent source-review checkout. The repository changed
concurrently; no prior source or result was edited by this route. This
source record also pins the consulted derivations and scripts that were
read but not executed.

`de4_scope_record.json` is a later read-only extraction of DE4's stored
results. It is not part of the 60-check run. Its source hash and extraction
scope are explicit; the resulting lower-branch qualification is in
`RESULT.md`. DE4's failed universal test and its unconfirmed stronger
predeclared hypothesis are preserved separately.

No external literature novelty claim, new galaxy/cosmology fit, action-level
identification of the prescribed gate with the clock, or full coupled
constraint/evolution closure follows from this record.

## Formal algebra bridge

`GateClockInverse20260926.lean` has four accepted statements:

- The two-environment affine inverse under distinct log fractions.
- The stress sum and its invariance under an additive vacuum shift.
- The total-gap dispersion inverse for `u>0,q>0`.
- The squared rotation-rate dispersion inverse for `u>0,q>0`.

The final compiler run exited zero in 78.634278959 seconds, using Lean
4.34.0-rc2 (commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`) and Mathlib
`85e3a25e006c35636f0e53b0e9296caca2685bc0`. All four axiom reports contain
only `propext`, `Classical.choice`, and `Quot.sound`. There are no admissions,
custom axiom declarations, compiler warnings, or compiler errors in the
accepted source/log. These facts and their hashes were independently
read back and checked; see `lean_review_record.json`.

The compiler owner preserved full command/environment metadata in
`../scales/gate_lean_record.json` and the accepted log in
`../scales/gate_lean_attempt2.log`. The final source hash is
`76ab63c30a5d8336fe1fa7cc56b7b34de36867680edfb6785389ef4352897247`; the accepted
log hash is
`d78e1901ee2c74dc25a871740282d15329808cb8d9078e3fa881863f45bea2b1`.
The earlier successful compile had two tactic-style warnings; the final
compile removes them without changing the four statements. It is not a
formal derivation of the physical gate, stress tensor, dispersion, or
quartic vacuum-constant interpretation.
