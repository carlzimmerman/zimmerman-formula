# CQ7 AMENDMENTS

κ = ½ FITTED; not theory closed.

**A1 (made after a first, stopped run, before any graded label).** The isolated rotation-curve ODE was to be solved with `solve_bvp`. In the first run every screened rotation-curve solve came back with a nonzero status (node limit: the problem is stiff, r/L★ up to ~2000), so K4 failed and every gate galaxy was marked FAILS on the solver status alone. The shifts printed by those unconverged solves were all below 0.11 dex max, 0.025 dex median. The ODE, its boundary conditions (regular p ∝ r inside, the law at 30 R_last) and the grading lines are unchanged. Only the solver changes, to a second-order finite-difference Newton solve on ln r (40,000 nodes, banded Jacobian, converged when max|Δp| < 1e-12 max p). K4 is the check that it equals the algebraic law at small L★. The first run's log is not kept as a result: it was overwritten by the rerun.
