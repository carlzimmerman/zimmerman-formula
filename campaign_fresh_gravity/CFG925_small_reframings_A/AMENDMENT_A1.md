# CFG925 AMENDMENT A1 (2026-10-20, POST HOC): K6 residual bar made conditioning-aware

**When.** Written after the first K-only run (`CFG925_KONLY=1`, exit 2) and before any MUTATE or main run. No reframing number
and no class had been computed or printed at that point.

**What failed.** One check failed, K6. All the others passed: K1–K5 and K7.

K6's frozen bar is "fixed-point residuals ≤ 1e-10" (relative, |h(y)/y_b − 1|). On the test grid y_b ∈ [1e-6, 1e3], R2-A's
largest relative residual was 1.51e-10, at y_b = 1.2e-6. R2-B's residuals are 7e-16.

**Why it is not a solver defect.**
- R2-A solves h(y) = y (2 − ν(y)) = y_b just above the floor y_f = (ln 2)² = 0.4805, where h → 0.
- y is returned to the nearest double, so the evaluation error of h is about ε·y_f.
- Divided by y_b, this gives a relative residual of about y_f ε / y_b = 1.07e-10 at y_b = 1e-6. That matches the observed 1.5e-10.
- A stand-alone check gives the largest relative residual by grid floor:
  - y_b ≥ 1e-6: 1.5e-10;
  - y_b ≥ 1e-5: 2.0e-11;
  - y_b ≥ 1e-4: 1.2e-12.
- The data reach y_b ≈ 7e-5 at the lowest dwarf g_bar.

**Change.** K6's residual bar becomes |h(y) − y_b| ≤ 1e-10·y_b + 16 ε y, with ε the double-precision epsilon. The same form
applies to R2-B, with h(y) = y/ν(y).
- The test grid is unchanged: [1e-6, 1e3], both kernels.
- The relative residual is still printed.
- The data's minimum y_b is printed for information.

Nothing else changes: thresholds, grading, inputs, readings and MUTATE are as frozen in 661668f32.

**Effect.** This is a numerical-tolerance amendment only. It cannot move any reframing value. The R2 solutions are the same
doubles either way; only the pass/fail rule of the check changes.
