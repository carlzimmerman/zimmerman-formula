# Evolution evidence, CD26-4

Accepted records are listed below. Each manifest validates against its current executed source or frozen inputs. Exact algebra is not a PDE proof.

| Run | Exact checks | Seconds | Exit |
|---|---:|---:|---:|
| run_003 | 35 | 2.117295 | 0 |
| transition_run_001 | 11 | 1.059262 | 0 |
| cp_run_001 | 14 | 0.649879 | 0 |
| carrier_run_001 | 12 | 0.567328 | 0 |
| perspective_run_001 | 8 | 0.509731 | 0 |
| barrier_run_001 | 7 | 0.602016 | 0 |

All six jobs used an explicit Xcode Python 3.9.6 executable, SymPy 1.14.0, a 60-second cap and one-thread settings. Actual runtime versions are embedded in results. Quadrature/root controls use mpmath 1.3.0. The CP preregistered numerical bound allowed 162 cases; 54 distinct exact-rational combinations were executed. The positive-floor run executed six 40-digit bracketed scalar roots. No fitting, large PDE simulation or dependency installation was performed.

`EvolutionBridge20260926.lean` has 14 accepted declarations in `lean_attempt4.log`; `lean_record.json` records the exact command, toolchain, axiom list and hashes. The compile exited0 in32.603seconds, with two harmless lint warnings documented in the record. There are no errors, admissions or custom axioms. Axioms are only `propext`, `Classical.choice`, `Quot.sound`.

Earlier main-check and Lean versions are preserved under `development_sources/`. Main scientific run_001 and run_002 passed their then-current smaller source, but the active manifest is run_003; later additions use separate named runs to retain the failed physical claims and their repairs. Earlier Lean outputs compiled smaller theorem inventories and are superseded by attempt4. They should not be matched to the current source.

Read RESULT.md for the fixed-background regularity proof and CP_AND_CARRIER.md for the latest common-action variants and their remaining obligations. The weighted-gate failure, exponential-carrier negative momentum Schur, and no-floor perspective boundary failure are retained as bounded counterexample controls; they are not silently removed when the candidate changes.

The perspective+positive-floor variant has a new input V0, a changed source rho/t, and a positive-domain requirement. The finite-cell repair and conditional continuum arguments do not derive V0 or prove global-time evolution of the full gravity/clock/carrier system.
