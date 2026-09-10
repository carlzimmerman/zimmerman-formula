# Checked derivative helper run

The frozen `run_001` completed at 2026-09-10 16:33 UTC on HEAD `f109d3d8ce1cdab6b5f63bea75bca83a8d4798f9`, with a dirty shared worktree. Exit status was 0; total recorded runtime was 2.53305 seconds. Only this new `derivatives/` directory was edited by this lane; no commits were made.

All four focused tests passed in 1.329 seconds. The five fixed-state comparisons use independent 60-digit differentiation, and the prior matched-pair next determinant is rechecked against independently refined 60- and 80-digit values. The original raw-curvature perturbation check showed the following relative infinity-norm errors as the step decreased through factors `(3,1,0.3,0.1)`:

| State `(epsilon,y)` | Base X-step | Four relative errors |
|---|---:|---|
| `(1e-6,0.1)` | `6.0724e-11` | `1.86e-7, 2.09e-8, 2.48e-9, 7.99e-10` |
| `(2e-6,0.153793693...)` | `5.7117e-11` | `6.66e-8, 7.40e-9, 6.27e-9, 8.45e-9` |
| `(1e-3,0.8)` | `3.7904e-6` | `4.21e-5, 4.68e-6, 4.21e-7, 4.68e-8` |

All three states have at least two adjacent estimates below the specified `1e-5` tolerance. The first two reach a floating roundoff plateau; these numbers are convergence evidence, not interval enclosures.

The separate 1000-call benchmark measured 0.725472042 seconds for one-time symbolic compilation and 0.040795042 seconds for all warm evaluations: approximately **40.8 microseconds per scalar `single` call**. This is machine/run-specific timing, not a performance guarantee. No expression explosion or numerical scan occurred.

Manifest: `run_001/manifest.json`, SHA-256 `60460c68f5f35d45f3e0d6b451f512a7bd52b89e1413befd6607b32947e41a1e`. Validation against the live input files returned `valid evidence record; mathematical interpretation requires review`. The manifest pins all declared implementation/reference files before and after the run, retains full stdout/stderr, and records actual arguments, 60-second timeout, and 1,048,576-byte log cap. The exact two entry-point commands are in `README.md`; both were run in this recorded execution.

Versions: Python child 3.9.6, runner Python 3.11.13, SymPy 1.14.0, NumPy 1.26.2, SciPy 1.11.4, mpmath 1.3.0. No randomness or dependency installation was used.

Self-review covered the new README's equations, notation, assumptions, and numerical scope; no mathematical-token correction was needed. Existing formal preservation statements are not being relabeled as certification of this compiler. The helper is ready for a separately audited joint solve; no joint root, health result, invariant continuation, or full-theory conclusion is asserted here.
