# Evolving density and alternative branches of the unchanged action

2026-09-11. Starting commit `cb8a5d98e`. **Theory OPEN; the tested
alternative branches fail the required past-history gradient gate.**

Carl Zimmerman explicitly requested that dark-energy density evolution be
examined, and approved testing other branches of the same fixed action.
This prompted the density/pressure bookkeeping and a broader initial-root
search rather than another coefficient reconstruction. Claude's L185/L186
instability work supplies the relevant preceding diagnostic, not a universal
exclusion of all branches. No claim of priority or complete theory is made.

## Density evolution was not absent

The action-derived quantities, in the existing natural units, are

\[
\rho_c=2q^2P_X-P+V-6\gamma Hq^3,\qquad
p_c=P-V+s_0W+2\gamma q^2\dot q.
\]

The combined non-baryon/radiation sector is

\[
\rho_X=M^2\Lambda+\rho_c,\qquad p_X=-M^2\Lambda+p_c.
\]

Its constant explicit Lambda term must not be confused with its evolving
clock energy density or with the evolving coefficient potential `V(tau)`.
Nor is the entire combined sector automatically the observationally inferred
dark-energy component: the clock carries approximately dustlike stress on
the original sampled branch.

The original scalar equations give

\[
\dot\rho_c+3H(\rho_c+p_c)
=q(\dot j+3Hj)-s_0(P_\tau-V_\tau-3HW)=0,
\quad j=2qP_X-6\gamma Hq^2.
\]

Thus `d ln(rho_X)/d ln(a) = -3(1+w_X)` follows from the action. The numerical
check computes the left-hand density derivative independently using the
constitutive jets and solved background rates, rather than assigning it
from continuity.

| Original branch a | V(tau) | rho_clock | rho_X | w_X |
|---|---:|---:|---:|---:|
| 1.0000 | 0.00909 | 0.09743 | 0.79743 | -0.87761 |
| 0.5028 | 0.03762 | 0.77224 | 1.47224 | -0.47180 |
| 0.3012 | 0.06319 | 3.60646 | 4.30646 | -0.16894 |
| 0.1003 | 0.06733 | 96.50993 | 97.20993 | -0.00801 |

The explicit `M^2 Lambda=0.7` stays constant. The absolute Ward residual is
at most `3.2e-12` at these samples. These are dimensionless solution data;
`a=1` is a normalization epoch, not an observationally calibrated today.

For a separately conserved *identified* dark-energy component, more generally,

\[
\rho_{DE}(a)=\rho_{DE}(1)
\exp\!\left[-3\int_1^a(1+w_{DE}(\tilde a))\,d\ln\tilde a\right].
\]

If Carl's global relation `a0 proportional to sqrt(rho_DE)` is additionally
assumed, it implies `d ln(a0)/d ln(a) = -3(1+w_DE)/2`. That is conditional
on identifying that component and its coupling; it is not derived by this
clock action. We do not substitute `rho_X` for `rho_Lambda`, insert a local
`a0`, or change `Lambda` by hand.

Observational evolution is an open question, not something ruled out here.
DESI's combined-data results strengthened hints of evolving dark energy in
[March 2025](https://www.desi.lbl.gov/2025/03/19/more-than-a-hint-of-evolving-dark-energy-new-results-and-data-from-desi/).
Its newer [July 2026 full-shape Ly-alpha result](https://www.desi.lbl.gov/2026/07/30/new-desi-dr2-lyman-alpha-results-shed-light-on-dark-energy/)
shifted toward LambdaCDM. These are not a measured unique rho_DE(a) to insert
into this action, and no observational fit was performed in this checkpoint.

## Four initial roots found; two previously missed local candidates

At exactly the old initial matter densities and clock epoch, eliminate H
with the actual clock equation,

\[
 H(q)=\frac{P_\tau(q^2,0)-V_\tau(0)}{3W(0,0)},
\]

then solve the Friedmann residual. Both orientations of q are searched inside
the logarithm domain. Two grid resolutions, with logarithmic boundary
sampling, recover the same four sign-changing roots. This is not exhaustive
root counting: tangential roots, arbitrarily close boundary roots and other
initial epochs/data are not excluded.

| q | H | s0 | high-k clock c_s^2 |
|---|---:|---:|---:|
| -0.947701754 | 0.696756037 | 0.859028989 | +0.000857602 |
| -0.907831613 | 0.519112974 | 1.031826466 | -0.001552910 |
| +0.907832151 | 0.519111819 | 1.031781069 | -0.001553975 |
| +0.947701717 | 0.696753206 | 0.859017635 | +0.000857601 |

`Lambda=.7`, `gamma=1e-6`, `a=1`, `tau=0`, `rho_b=.001`, `rho_r=.01` and all
coefficient functions are unchanged. Values of c_s^2 come from the actual
six-state operator at k=3000 and 30000, not from imposing the gamma=0 formula.
The radiation pair supplies the independent c_s^2=1/3 control.

## Immediate next gate: do the extra branches survive in time?

Both higher-|q| roots were continued backward and forward, with no history
extrapolation. Runs at checkpoint steps 0.025 and 0.0125 agree on the outcome.

| Initial q | Direction | Endpoint a | clock c_s^2 | Outcome |
|---|---|---:|---:|---|
| q positive | backward | 0.860708 | -6.9734e-5 | gradient gate FAIL |
| q negative | backward | 0.860708 | -6.9749e-5 | gradient gate FAIL |
| q positive | forward | 1.221403 | +0.00205134 | bounded sign check passed |
| q negative | forward | 1.221403 | +0.00205138 | bounded sign check passed |

The backward stop is a resolved sign failure, not a domain or numerical
constraint failure: relative logarithm margin is about 0.00942, background
condition number about 1.10e4, and all scaled constraints remain below
`1.5e-13` across the refined four continuations. Radiation fraction at the
backward failure is only about 0.00962. The endpoint is a sampled failure
location, not an exact analytic transition time.

## Action-derived kinetic check, with remaining constraints explicit

The actual quadratic action also supplies velocity Hessian A, mixed block B
and algebraic lapse/shift block C. Stationary elimination gives

\[
 K_{\rm partial}=A-BC^{-1}B^T.
\]

In spatial gauge `e=ed=0`, velocities are `(zd,sigmad,radd,thetad)` and
algebraic variables are `(n,b)`. The high-positive-q initial spectrum is
approximately `(0,0.000846863,0.360830,195.204)`. All four initial roots and
60 refined continuation samples have no eigenvalue below the recorded
scale-aware negative tolerance. No samples were skipped.

This distinguishes the encountered gradient failure from a detected negative
principal kinetic direction. **Dust density and residual constraints remain
unreduced.** No first-/second-class count, exact nullity, or complete no-ghost
theorem follows from this partial Schur complement.

## Decision and reproducibility

The extra roots genuinely exist and pass an initial necessary gradient/kinetic
screen, but neither higher-|q| continuation supplies the required stable
past-to-future history. The original two roots already fail at the initial
epoch. Consequently **none of the four found initial roots passes the
tested history requirement**. This is not a universal no-go for the action,
all initial data, or Carl's framework, and it is not a completed MOND theory.

A different dark-energy law cannot simply be pasted over these equations.
For example, promoting Lambda to Lambda(tau) in the action would also add
`-M^2 dLambda/dtau` to the clock equation. A rescue needs an action-derived
change consistent with the Ward identity, or a genuinely surviving branch
under physically justified initial data—not a chosen expansion history.

Fresh verification: **35 Python tests passed; all five archived executions
and their manifest validations returned exit 0**. The backward gradient
FAIL remains a scientific failure despite successful execution. No new Lean
certificate is claimed. [Exact scripts, commands and files](DARK_ENERGY_BRANCH_COMMANDS.md).

The computation-audit workflow required the alternative-root and time-history
tests to remain separate, with failed continuations and unreduced constraints
reported. The original action and earlier evidence files were preserved.
