# CD26-3 scale evidence

Only the following records are accepted:

- `run_005/manifest.json`: exit 0 in 0.715411 s, 60 s cap, 34 exact scale identities, rank/nullspace and dimensional checks, and two numerical coupling controls. Manifest validation passed. No old galaxy fit was executed.
- `lean_record.json` / `lean_attempt3.log`: 12 scale statements, exit 0, no warnings/errors, no admissions. Source `ScalesInverse20260926.lean`.
- `gate_lean_record.json` / `gate_lean_attempt2.log`: four requested sibling gate/clock statements, exit 0, no warnings/errors, no admissions. Source `../gates_clock/GateClockInverse20260926.lean`.

Both Lean files print every theorem's axioms: only `propext`, `Classical.choice`, `Quot.sound`. Their exact commands, elapsed times, source/log hashes, toolchain and nonvacuity checks are in the records. They certify their conditional algebraic statements, not an action, a full field theory, a vacuum equation of state, a fit, a measured coupling, or a microscopic origin.

The actual science command is

```text
/Applications/Xcode.app/Contents/Developer/usr/bin/python3 real_research/dark_energy_inverse_2026_09_26/scales/check.py --output real_research/dark_energy_inverse_2026_09_26/scales/run_005/results.json
```

It ran from the repository root with Python 3.9.6 and SymPy 1.14.0. Actual runtime versions are embedded in the result in addition to the contract. The bounded runner's full manifest records the 60 s cap, one-thread settings and hashed inputs. Twelve source snapshots and their original paths/hashes are frozen under `source_snapshots/` and `source_snapshot_inventory.json`, captured at observed HEAD `ecffd2af3623ff3e32318234fd51e1fac50b9126` in a dirty tree. The checkpoint began at `7daaa5426076a2d78a50f3316007c7093255ce9a`; no claim is made that sources remained unchanged throughout concurrent work.

Both Lean commands use `/opt/homebrew/bin/lake env lean -j 1 <absolute source path>` from `/Users/carlzimmerman/new_physics/zimmerman-formula/fable_independent_2026/lean_2026`. Lean is 4.34.0-rc2, commit `6a10ac8c22beadecabdbb0919c2b50214762f91d`; mathlib is `85e3a25e006c35636f0e53b0e9296caca2685bc0`.

Retained development attempts are not accepted evidence:

- Science `run_001`: SymPy could not simplify an expanded perfect square; the implementation now explicitly factors it under the positive domain.
- `run_002`: scientific checks passed; an external source note later changed, making the manifest stale.
- `run_003`: scientific checks passed but its contract had incorrectly retained Miniconda software versions while argv used Xcode Python. The final run corrects this provenance error.
- `run_004`: scientific checks ran, then new runtime metadata referred to `sp` instead of the imported SymPy alias `s`; fixed in `run_005`.
- Scale `lean_attempt1`: timed out at 60 s; no accepted proof claim.
- Scale `lean_attempt2`: redundant tactics after closed goals produced errors; fixed in the accepted attempt.
- Gate `gate_lean_attempt1`: all statements compiled, with two tactic-style warnings; final attempt removes those warnings.

Failed/development source revisions were not separately archived. Their logs and hash records are preserved, but reproducing those failures from the final source is not promised. No source snapshot has been guessed from an old hash. The final accepted records identify the exact current source files.

Independent review of `../reconstruction/check.py` and `../reconstruction/RESULT.md` found no remaining correction to energy/pressure units, curvature sign, the `G_cosm=g G_N` convention, pressure/density inverse identifiability or their stated limitations. That was a source-level mathematical audit, not a second execution or a field-equation derivation.
