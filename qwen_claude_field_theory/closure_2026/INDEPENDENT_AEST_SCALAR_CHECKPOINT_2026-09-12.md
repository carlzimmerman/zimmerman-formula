# Independent AeST finite-k scalar checkpoint — 2026-09-12

## Bottom line

The explicit AeST host action used by the finite-k “winner” is not a certified
two-tensor theory.  A direct quadratic expansion of the same covariant action,
followed by a canonical/Dirac reduction, leaves a finite-k gauge-invariant
scalar

```text
X = delta phi + Q0 v
```

with

```text
D       = 2 K2 Q0^2 + K_B k^2
K_X     = 2 K2 K_B k^2 / D
Omega_X = 2 k^2 (2-K_B) (K2 Q0^2+k^2) / D
omega^2 = (2-K_B)(K2 Q0^2+k^2)/(K2 K_B).
```

For `K2>0`, `K_B>0`, `0<K_B<2`, every finite `k>0` therefore has a positive
kinetic scalar mode.  The finite-k phase space has two first-class constraints
`p_Phi=0` and `Q0 p_chi-p_v=0`, with an exactly zero computed Poisson matrix,
and one surviving physical scalar configuration DOF.  At `k=0`, the additional
primary `p_v=0` makes the homogeneous scalar count degenerate and zero.  The
zero-mode degeneracy does not remove the finite-k scalar.

This directly contradicts treating the negative `K_eff` band in the prior
board as a nonpropagating constraint.  Under a strict two-tensor gravitational
sector it closes the AeST host gate as **DEAD**.  If the model explicitly
reclassifies `X` as a separate clock scalar (which the target requirements
permit in principle), the result is instead an **OPEN** gate with a healthy
quadratic mode that must be included in the remaining PPN, cosmology, and
strong-coupling checks.  It is not a universal no-go theorem for arbitrary MOND
actions.

## Reproducible evidence

From `closure_2026/fried_chicken_final/fc_aest_finitek/`:

```bash
python3 verify_aest_source_lagrangian.py          # exit 0; source residual 0
python3 aest_metric_scalar_dirac_audit.py        # exit 0; status HOST_SCALAR_GATE_DEAD...
python3 -m unittest discover -s . -p 'test_*.py' # 3 tests, exit 0
python3 run_aest_metric_scalar_lean.py           # exit 0; warnings only
```

The Python source-match check compares the compact polynomial used by the
Dirac audit with the generated `L2flat` from `fc_fk_routeB_covariant.py`; the
residual is exactly zero.  The Lean certificate proves the rational kinetic,
gradient, dispersion, and positivity formulae.  It does not formalize the
full nonlinear covariant variation.

The old `C_effective_kinetic_and_decider.py` still exits 1 because its symbolic
limit call is sign-underdetermined in `H`; its earlier ghost-band ansatz is not
the Schur complement of the exact decoupling matrices.  The independent audit
does not use that ansatz.

## What remains

This closes only the AeST host scalar gate.  The full ten-gate relativistic
MOND target remains **OPEN globally**: no common explicit action in the repo
has yet derived exact exponential MOND, `Phi=Psi`, `gamma_PPN=1`, all preferred
frame parameters zero, ordinary matter conservation, stable FLRW and exactly
two gravitational tensor DOF simultaneously.  The next unavoidable calculation
for any attempted rescue is the full metric-coupled ADM quadratic action on
FLRW, with lapse/shift retained and the scalar Schur complement derived rather
than inserted.
