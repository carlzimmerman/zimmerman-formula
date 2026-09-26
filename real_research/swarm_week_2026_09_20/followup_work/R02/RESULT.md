# R02 — Replace the fitted power with a shell-mass theorem (result)

- Owner: Hermes (this lane); independent reviewer: none yet (self-review recorded)
- Execution state / claim state: completed / proved_conditional
- Baseline: followup work order `3e857b5a6f8f05b48e29d0cbe42136998e9f9445`;
  inputs `L304_phantom_active_mass.py`, `L311_phantom_law.py` unmodified at HEAD
  `29b5c74ff`.  `python3 cutoff_sensitivity.py` exit 0.
- Model/action ID: L304 surrogate (same as R01).

## Exact claim and scope

For rho = C/r^3 on r >= r0: M(r) = M(r0) + 4πC ln(r/r0).  The apparent power
exponent of a pure logarithm over L304's window with zero interior mass is
~0.578 and moves with the cutoff.  The actual profile's active mass increment
follows the log law on the converged tail; the finite-window remainder is
bounded.

## First discriminator and result

**4/4 PASS.**  R2.1 the shell integral, certified numerically at 2e-12.  R2.2
the fitted exponent is a cutoff artifact: 0.578 (1 Mpc) → 1.175 (2 Mpc) →
1.345 (5 Mpc) → 1.820 (10 Mpc) with the outer sample fixed — no power law is
being measured.  R2.3 with M0 tracked, the mass increment across the converged
outer half of the window is 4πC ln(r/r_hi) to 0.1%.  R2.4 the remainder
integral is 2.7e-4 of the log term, so the log shape is exact to <1% over the
whole fitted window.

## Evidence

- `cutoff_sensitivity.py` → exit 0, 4/4 PASS + results JSON with slopes and M0.
- R2.1's quadrature used 4e6 nodes (residual 2e-12, grid-level).

## Independent check

The cutoff-sweep itself is the control: a genuinely power-law shell (e.g.
rho ~ r^-2) would keep its fitted exponent under the same sweep; the log shell
does not (0.578 → 1.820).

## Novelty and physical interpretation

L304's V4 "M_act ~ r^0.58" and L311's V2 r^{1/8} outer-rise prediction are
artifacts of (i) starting the cumulative integral at the first grid point
(M0 = 0) and (ii) fitting a power over a finite window.  The corrected law is
M_act = M0 + 4πC ln(r/r0): the rise is slower than any power (d ln v/d ln r ->
0), which weakens the outer-rise signal L311 V2 promised but keeps the
suppression conclusion.  L311's curve table (V1) is quantitatively affected
beyond ~30 kpc and should be re-derived on the log law.

## Decision and next action

proved_conditional (numeric certification + R01's Lean algebra).  Hand the log
law to R03 (done — curvature invariant C_beta = 0 for the log continuation vs
beta/2 for sqrt) and to R05/E3 for lensing; flag L311 V1/V2 as needing a
re-run on the corrected law.  Next cheap test: the R19 negative control that
L311's own gate cannot reject a log profile.