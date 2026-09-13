# Stationary current halo gate implementation plan

**Goal:** Test whether the fixed density-repair action supports a regular static spherical counterflow halo; do not change its coefficients.

**Architecture:** Differentiate the invariant master function before equal-density specialization. Use conserved radial current flux and canonical time momentum to derive two first-order equations on a prescribed static metric. Integrate finite shells only while monitoring the actual current Hessian; distinguish this test from a self-gravitating halo or time evolution.

**Tech stack:** Existing SymPy, SciPy, NumPy, pinned Lean/Mathlib.

**Spec:** `qwen_claude_field_theory/closure_2026/entrained_current_construction_2026/DENSITY_REPAIR.md`, next stress/redistribution gate.

## Work sequence

- [ ] Add `test_stationary_halo.py`: fail if implementation absent, then check dust limit of canonical momentum, the independently derived Bernoulli expression, stress conservation, and convergence of conserved flux/energy on integrated shells.
- [ ] Add `stationary_halo.py`: derive H=-pi_t/N and stress from F, obtain the radial ODE by solving the differentiated first integrals, integrate equal-density p=b=1/2 at explicit dimensionless initial states in N=r^epsilon, record conservation residuals and energy-domain exit. No empirical normalization is assigned.
- [ ] Add `StationaryHalo.lean`: certify conditional regular-center flux obstruction and the steep-profile implication of the leading small-speed equations; do not call the truncated relation exact.
- [ ] Add reproducible JSON/report with commands, versions, source hashes, exit statuses, assumptions and nonclaims. Run existing Python and Lean regressions.
- [ ] Commit only owned explicit paths and push the verified checkpoint.

## Boundaries

No refit of p, b, a0, density units or potential to obtain depletion. No changes to other agents' files. No full-gravity/observational conclusion from a prescribed external metric. Current conservation rules out a regular nonzero stationary radial flux without sources, but does not rule out time dependence, other geometries or additional interactions.
