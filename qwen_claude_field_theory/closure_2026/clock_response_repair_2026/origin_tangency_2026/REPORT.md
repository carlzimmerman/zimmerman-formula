# Action-derived center consistency: a local repair, not theory closure

Base: `362ddbb5d`, including `ecce4e6ce`. The complete relativistic MOND
objective remains **OPEN**. No coefficient, constitutive function, physical
action, local acceleration scale or particle content was changed. The latest
unrelated PAPER14 publication commit was not used as numerical evidence.

## Exact cause of the origin discrepancy

At a smooth spherical center write a=A(0)=R_r(0), q=Q(0),
u1=chi_rr(0), and h=K_r(0)=K_angular(0). The existing clock constraint is

\[
3Wh=P_\tau-V_\tau+6qW_Yu_1/a^2.
\]

Subscripts tau on coefficient functions denote explicit clock derivatives,
not total derivatives through X. Since chi_t=NQ, even parity gives

\[
\dot u_1=(NQ)_{rr}(0)=N_{rr}(0)q+N(0)Q_{rr}(0).
\]

Differentiating the clock constraint, with a_dot=Nah, yields

\[
3W\dot h+3hW_\tau=P_{\tau\tau}-V_{\tau\tau}
+2qP_{X\tau}\dot q+
\frac6{a^2}\bigl[\dot qW_Yu_1+qW_{Y\tau}u_1
+qW_Y\dot u_1-2N hqW_Yu_1\bigr].
\]

`center_chain.py` imports the actual varied action's center equations and
verifies that this identity is exactly their preserved-clock row, not an
independently asserted evolution law. It then finds that the discrepancy
is entirely transported from the numerical mixed-derivative mismatch:

\[
\Delta\dot h=\frac{2qW_Y}{a^2W}\,\Delta\dot u_1.
\]

On the saved t=.02 states:

| Grid | Original discrete h-dot defect | Continuum chain/action defect |
|---|---:|---:|
| 129 | 2.5646592e-6 | 4.44e-16 |
| 257 | 1.7822061e-6 | 0 |

The directly differenced center projection agrees with the predicted defect.
This identifies a discrete derivative inconsistency, **not** an inconsistency
between the continuum center equations. It does not certify other field equations.

## Minimal numerical correction and falsification tests

The existing odd interpolant is r times a cubic spline in r^2. Its derivative
at the origin is a linear functional L of positive-radius samples. Only the
first positive-radius *rate* is corrected:

\[
v_1^{new}=v_1+\frac{u_{1,t}^{action}-L(v)}{L(e_1)}.
\]

No metric residual or fitted physical coefficient enters the target.
The correction enforces the already derived mixed derivative. Other positive
samples are unchanged. A smooth manufactured gradient preserves fourth-order
interior accuracy, while the first-sample correction decreases at least by
a factor 16 under each tested grid doubling.

The new mixed-derivative regression failed before the repair (exit 1,
error 5.02636e-6 versus 1e-10 threshold), then passed. Reusing the old saved
states after the repair, the center chain/action difference is 4.44e-16 at
129 and zero at 257; independent centered differences are about 1e-11 for
step1e-4. Those saved states were not retroactively claimed to have evolved
under the new operator.

The complete final suite ran all **16 tests**, exit **0**, in 225.242 seconds,
including the unchanged 129->257 Hamiltonian/momentum refinement gate. See
`tests_001/stderr.txt`. Both new tests were also independently reviewed and
rerun, passing. The whole solver remains experimental.

## What Lean actually certifies

`CenterConsistency.lean` proves two universally quantified real-algebra
identities: the derivative-error transport formula (a,W nonzero), and the
linear-jet correction formula (weight nonzero). Both compile with only
`propext`, `Classical.choice`, and `Quot.sound`; no sorry or physics axiom.

The action-to-expression bridge is exact SymPy, **not** a Lean formalization
of the covariant variation. The Lean statements do not prove PDE existence,
stability, measured gravitational behavior, or all theory gates. The initial
broad tactic import failed because a cached optional mathlib module was absent;
narrowing to the actually needed existing tactics resolved this without any
dependency installation. The final Lean run returned 0.

## Global radial consistency: still OPEN

`tangent_linear.py` differentiates the radial constraint ODE itself using
complex-step algebra rather than subtracting two independent adaptive solves.
PCHIP density interpolation and center startup derivatives are separately
center-differenced with steps1e-4 and1e-5. It does not pretend these are exact
or interval-certified derivatives.

For the saved states and the repaired operator, the full r<2.8 h/k rate
discrepancies are about (1.65e-6,9.64e-6) at129 and (1.12e-6,3.58e-6) at257.
They persist when the differentiation step changes; direct projection
differences agree. Reducing the radial startup radius from dr/16 to dr/64
barely changes these h/k errors. Thus neither noisy subtraction nor startup
radius alone explains the remaining defect. The k error on these old states
is slightly larger after the center correction; that is retained, not hidden.

A distinct control uses the same analytic Gaussian free data on65,129,257,513
grids and solves the constraints separately. Its full-domain h/k discrepancies
decrease about 16-fold per refinement through 257, but that rate is lost at
513, with the maxima moving away from the origin. An adaptive-solve error floor
is a possible cause, not established by this control. This is evidence of
consistency on this smooth family over the resolved range, **not** a global
fourth-order theorem or validation of the time-evolved data.

The next numerical discriminator is compatibility/regularity of the evolved
radial fields and their spline versus finite-difference jets, using the new
tangent-linear diagnostic. Do not add another fitted force or alter coefficient
functions to address a discretization issue.

## Relation to the requested neutrino-inspired mechanism

No neutrino particle has been added. No scale-dependent clock retention or
galaxy/cluster mass fraction is claimed. The intended mechanism still requires
the clock stress and its perturbations to produce the observed separation
from the same action, while preserving its radiation/CMB behavior. These
local numerical and algebraic results do not supply that mechanism. The
previous exact no-additive-cH-in-Y result remains valid, but identifying Y
with the physical exponential-MOND force law is still unproved.

Concurrent commit `33d7cda6f` was inspected before this checkpoint. Its L180
script explicitly chooses `G_eff/G=nu(cH/a0)` and assumes the dark component
clusters as in LCDM; its new Lean theorem proves an algebraic H0/a0 identity.
Neither calculation derives that force prescription from the fixed action
used here. It remains a separate conditional study, not a bridge closing this
action's cosmology gate. Its numerical predictions were not independently
rerun in this task and are not adopted as certified results here.

## Files, commands and evidence

Modified: `../nonlinear_evolution_2026/{project.py,evolve.py}`.
Added: `../nonlinear_evolution_2026/test_center_tangent.py` and this directory's
plan, report, two Python diagnostics, Lean certificate, contracts and run records.
Unrelated user files and the older interrupted memory draft are untouched.

The commands actually executed include (repository root except Lean):

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/origin_tangency_2026/center_chain.py
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026 -p 'test_*.py' -v
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/origin_tangency_2026/tangent_linear.py
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/origin_tangency_2026/tangent_linear.py --manufactured
```

Lean is run from the existing clock_constitutive_construction_2026/
lean_formalization_2026 project with `lake env lean` and the absolute path to
`CenterConsistency.lean`. Exact argv, input hashes, versions, caps, logs,
timings and exit codes are in `before_001`, `after_001`, `tests_001`,
`lean_001`, and `tangent_002`. All final executions returned0. Diagnostic
exit0 means the measurement completed, not that a closure gate passed.
`before_001` pins the old numerical source; `tangent_001` pins the script
before adding its smooth-control CLI. Preserve them as historical evidence;
use the final records for current-source verification.
Current-source manifest validation returned 0 for `after_001`, `tests_001`,
`lean_001`, and `tangent_002`.

Mathbox's research/computation audit and independent code review kept the
center identity, bounded numerical repair, and full-theory claim separate.
Proofreading covers this report and the new Lean statements only.
