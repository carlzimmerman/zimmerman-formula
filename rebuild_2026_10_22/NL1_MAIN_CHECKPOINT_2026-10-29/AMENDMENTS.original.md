# NL1 amendments

## A1 (committed alone, after the measurement printed and before any grade): forked-pool pickling

**What happened.** The first run measured the nine ng 64 runs, all flagged ok: L_nat = 4.8646, 68 % [3.831, 5.805]. It
then crashed before grading. LEE1's harness runs children in a forked pool that pickles `_child` by module name, and the
read-only namespace `lee1_ro` was not importable. The log is kept as `run1_pickle_error.log`.

**Fix.** The namespace is registered as a module (`types.ModuleType("lee1_ro")` in `sys.modules`), as SG1 did. This is
a code fix only; no rule, input or measurement changes.

**Disclosed context, not a rule change.**
- The per-seed c_f spread is large (2.44–15.09).
- A parallel audit (CSM2, c259bbc116) shows the first-crossing estimator is binning-sensitive for some seeds.
- Separately, CSM1 shows the CL3 constant-coefficient switch is inconsistent with the S9 core. NL1's PRIMARY grade is at
  the frozen T = 12.3, so CSM1 does not change NL1's frozen rule.
