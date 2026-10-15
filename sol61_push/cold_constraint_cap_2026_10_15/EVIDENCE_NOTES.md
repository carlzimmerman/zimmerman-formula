# Frozen run interpretation and reproduction

The bounded runner records the actual command, repository state, software environment, frozen script/contract hashes, limits, logs and outputs in each run's manifest. None of those records has been edited after execution. Completed execution is not a positive scientific verdict: adverse eigenvalues in the oblique runs are intentional search output.

The oblique contracts evolved by copying the prior contract. Their generic `profiles`, `period` and `controls` descriptions retain the baseline/default values. Per-case overrides are the explicitly listed bounds and the frozen script calls, and are recorded in each result row. In particular, oblique v6 executes six staged cases only: the two exact control benchmarks were actually executed in v5, not repeated in v6. V6 increases the period to 48 in its N=91 cases despite a retained generic period=32 default field. It also overrides the relative shift cutoff in two cases. These inheritance inaccuracies are disclosed here rather than modifying frozen inputs. The explicit argv, executable input and per-case result metadata determine what was actually run.

The manifest validator checks provenance and checksums, not the interpretation of the proofs. Regenerate with the bounded runner and a **new** output directory, passing the matching frozen script, contract, results and checks paths. Python3 is the recorded Xcode Python 3.9.6; the different `python` interpreter is not the canonical environment.

For all manifests in this package, use the installed computation-audit validator with `--root` pointing to this repository. Every failed run remains valid execution evidence of that failure, not mathematical success.
