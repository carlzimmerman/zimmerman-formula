# NP2 Amendment A1, 2026-11-03, pre-result, committed alone before any control or real-data number

No control, real fit, gate or Stage 3 number has been read. Before this I ran two smoke checks, outside the lane (scratch, not committed):
- a finite-difference check of the kernel derivative formulas (gradient of the rule and the derivative-derivative covariance agree to 1e-9);
- a timing run of the constrained fit on BF1's planted form (noise-free), L3 canonical, at λ 4 and 32, to time it and see the active set behave. Its gate numbers were not computed.

What the timing run showed, and the fixes. Each is an implementation detail of FROZEN_CRITERIA C1, not a change to the constraint, the gates or the labels.

1. **Solve at ε + 0.001, check at ε − 1e-6.** The NNQP is solved with a 1e-9 relative jitter, so binding functionals land a few 1e-5 below their target and the frozen convergence test (no violation beyond 1e-6) could never pass. Each round now solves for S_v ≥ ε + 0.001 and tests S_v ≥ ε − 1e-6, as frozen.
2. **Working set shrinks to the binding functionals.** After each solve, functionals with μ = 0 leave the working set; the next round adds the new violators (up to 1500). Without this the working set grew to 6000+ functionals and its matrix toward the 1 GB RSS cap. The 40-round cap and the non-convergence label are unchanged.
3. **Overflow-safe evaluation.** The constraint box is padded by 3 frozen lengths; where an ML length is long (the planted data drove one to the bound, 50 sd) the box reaches far outside any physical leaf, and 10^log y or 10^log ell overflow. The law's slope is computed in its scale-free form with x = g_b/a0 clipped to [1e-30, 1e30] (it is ½ or 1 to machine precision there), and asinh D is computed from log10 D (asinh D = ln 2 + ln D when log10 D > 300). D = 0 when s ≤ −2, SY1's floor.
4. **Two processes.** `np2.py controls --only L3` and `--only L5` (and the same for `real`) may run side by side, one thread each, to keep wall time down. The shared controls (known answer, Υ loader, checker, zero-weight law card) run in the L3 process. Outputs are then `np2_<mode>_L3.*` and `np2_<mode>_L5.*`; `real` reads both control files.

Gates, tolerances, split, model class, constraint, smoothness grid, mode U, labels and controls are unchanged.

κ = ½ FITTED; not theory closed.
