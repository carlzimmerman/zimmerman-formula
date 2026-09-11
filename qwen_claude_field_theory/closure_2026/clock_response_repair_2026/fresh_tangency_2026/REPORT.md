# Fresh evolution and an action-derived constraint-energy balance

2026-09-11; base `67c9ceaa8`. **Full gravity theory OPEN.**

Carl Zimmerman's primordial-clock proposal and insistence on a single derived
theory motivate this work. No particle component, local a0, reconstructed
coefficient function, or physical action is introduced or adjusted here.
The existing action's P/W/V functions are still previously reconstructed
inputs; the following result does not derive those inputs from first principles.

## New exact result: an error-propagation identity from the same action

Let V_s=A R^2 be the spherical spatial volume density (angular factor omitted),
k=K_r, h=K_angular, and Theta=N(k+2h). Define the normalized *total* metric
Euler–Lagrange residuals C_H=E_N/(A R^2), C_M=E_shift/(A R^2), including
minimally coupled dust, and let C_tau be the existing clock constraint.
These C variables are errors in satisfying field equations, not new fields.

The hypotheses are the chi Euler–Lagrange equation, the constraint-added
spatial metric equations, and the dust continuity/geodesic equations. The
regular shift-zero spherical patch has N,A,R nonzero; r=0 requires regular
limits. C_tau is retained as a possible source, not silently set to zero.

`balance.py` reruns the actual action's two Noether identities, independently
checks the matter contribution with U_d=sqrt(1+w^2/A^2), and derives, for the
solver's eta=1 spatial constraint addition,

\[
\begin{aligned}
\dot C_H={}&-2\Theta C_H+\frac{N}{A^2}\partial_r C_M
 +\frac{2N_r+N(2R_r/R-A_r/A)}{A^2}C_M-C_\tau,\\
\dot C_M={}&N\partial_r C_H+2N_r C_H-\Theta C_M.
\end{aligned}
\]

Here A_r denotes the radial derivative of A, not the radial metric coefficient.
The computed principal characteristic polynomial is lambda^2-eta N^2/A^2.
At eta=1 its roots are +/-N/A. These are **constraint-error characteristics**,
not a calculation of the physical gravitational-wave sector or a DOF count.

Writing Z=C_M/A and E=C_H^2+Z^2, the weighted identity is

\[
\boxed{
\partial_t(V_s E)-\partial_r\left(\frac{2V_sN}{A}C_H Z\right)
=V_s\left[-3N(k+2h)C_H^2-N(3k+2h)Z^2
 +6\frac{N_r}{A}C_HZ-2C_\tau C_H\right].}
\]

For homogeneous expanding coefficients k=h=H>=0, N>=0, N_r=0 and C_tau=0,
the right-hand side per unit V_s is

\[
-NH(9C_H^2+5Z^2)\le-5NH E.
\]

At an outer radial boundary the incoming characteristic is C_H+Z. Imposing
C_H+Z=0 makes the displayed outward-boundary contribution
-2V_s N C_H^2/A<=0 for V_s,N>=0,A>0. The sign follows from the PDE convention
partial_t u=B partial_r u: the positive eigenvalue of B travels inward there.
An integrated energy argument additionally requires regularity and compatible
boundary conditions for the full problem; existence of such a full solution
has not been proved here.

This gives a continuum diagnostic and a candidate constraint-preserving
boundary target. It does not show that the discrete evolution obeys the same
identity, or that physical scalar perturbations are stable.

### Precisely what Lean verifies

`ConstraintEnergy.lean` proves four real-algebra statements:

1. E=0 iff both normalized constraint residuals vanish.
2. Factorization of the eta=1 characteristic polynomial.
3. The expanding-coefficient balance bound above.
4. The nonpositive outer flux under zero incoming characteristic data.

All four compile with only propext, Classical.choice and Quot.sound; no sorryAx.
`balance.py` reads the actual Lean energy/balance definitions and checks their
identity with the expressions derived from the action. The symbolic variational
bridge, dust differential calculus, function spaces and integration are **not**
formalized in Lean. The four algebra certificates are not a complete theory proof.

## Fresh-state test of the unresolved metric consistency

The older tangency audit reused states evolved before the center repair.
`fresh.py` instead evolves the current initial data anew and then differentiates
the radial constraint projection independently using `tangent_linear.py`.
Parameters remain amplitude=.02, width=.3, outer=3, gamma=1e-6, t=.02,
dt=.00025. The background interval is extended to .022 only for the centered
directional probes at t=.02. The probes use both steps 1e-4 and 1e-5.

The following maxima include the origin over 0<=r<2.8; the displayed values
use the 1e-5 directional step. k-dot and h-dot denote radial and angular
curvature rates. These are *projection-tangency discrepancies*, not the
Hamiltonian and momentum residuals themselves.

| Fresh grid | h-dot discrepancy | k-dot discrepancy |
| --- | ---: | ---: |
| 65 | 6.58908e-6 | 6.31603e-5 |
| 129 | 4.36368e-6 | 1.70690e-5 |
| 257 | 6.85818e-7 | 2.14401e-6 |
| 513 | 1.14622e-6 | 4.13031e-6 |
| 257, half dt | 6.86491e-7 | 2.17634e-6 |

The 129->257 comparison improves, but 257->513 deteriorates, especially in
the first positive-radius cells. Halving dt at 257 barely changes the dominant
defect. This verifies that the issue is not only historical-state contamination
or an ordinary time-step error. It does not identify the entire spatial cause.
The 513 Hamiltonian/momentum residuals also plateau around 2e-7. We retain
those failures; the original 129->257 unit-test pass is insufficient.

`jets.py` compares the projection's spline b_r,b_rr,Q_r,Q_rr,chi_rr and k_r
with finite differences, and compares the constraint ODE's A_r,h_r with
evolution's derivatives. It also measures

    derivative_r(interpolated chi_r time rate)
       - [Q N_rr + 2 N_r Q_r + N Q_rr].

The regular center uses the actual action's limiting jets. The comparisons
are node samples, not uniform off-grid bounds. They are diagnostics: none
of these differences is subtracted from a physical force or used to tune
P/W/V. The k-constraint sample agreement is an assembly check, not independent
physics evidence, since projection supplies that same algebraic quantity.

On the final shifted-lapse states, the mixed-derivative maximum grows from
2.06171e-6 at 257 points to 4.07577e-6 at 513, with the latter maximum at
r=.01171875. This tracks the fine-grid curvature-rate deterioration and is
a concrete candidate source, not yet a proof that it accounts for all of it.

## A small numerical repair, with its unsuccessful stronger test retained

A manufactured exact N=1 background exposed cancellation in the old banded
solve: the 257-point error was 3.37952e-13, failing the new 2e-14 regression.
The lapse equation is now solved for n=N-1:

    n'' = a n' + b n + (b+c),
    n''(0) = b_center n(0) + b_center+c_center,
    n(outer)=0.

This is an affine change of numerical unknown, with the same continuum
equation, derivative stencils, monitors and physical boundary N(outer)=1.
The regression passed after the change, as did both existing nonconstant
lapse tests and the full 17-test solver suite (222.072 s, exit 0).

However, freshly evolving with this change does **not** repair the finer-grid
tangency failure:

| Grid, shifted lapse solve | h-dot discrepancy | k-dot discrepancy |
| --- | ---: | ---: |
| 129 | 4.36327e-6 | 1.70678e-5 |
| 257 | 6.85572e-7 | 2.16822e-6 |
| 513 | 1.15688e-6 | 4.18074e-6 |

The exact-background improvement is retained, not advertised as full
convergence repair. Further coefficient reconstruction would not fix this.

## Next unavoidable calculation and full-goal status

The next numerical construction should enforce compatibility of the discrete
clock-constraint derivative with the same spatial representation used in the
action evolution and projection, rather than matching only the center jet.
The derived continuum balance provides an independent target: monitor its
discrete defect, including scalar and matter evolution residuals and boundary
flux. First isolate the responsible spatial-jet term on the saved 513-point
state; a smaller dt or another force coefficient is not supported by these tests.

Even numerical closure would leave the physical exponential-MOND reduction,
galaxy/cluster clock retention, physical perturbation stability, complete PPN,
cosmological spectra, nonlinear DOF analysis and derivation of kappa unresolved.
No result here changes a0, supplies a measured Kepler-grade law, or proves
this action is nature's gravity theory. The original objective remains active.

## Files, commands, verification, and provenance

Changed existing files: `../nonlinear_evolution_2026/evolve.py`, its
`test_lapse.py`, and the parent `README.md`. New files are this directory's
plan/report, `fresh.py`, `jets.py`, `balance.py`, `ConstraintEnergy.lean`,
contracts, generated JSON/NPZ results and execution records.

The main commands (repository root, except the stated Lean working directory):

```sh
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fresh_tangency_2026/fresh.py --result-file <fresh-run>/result.json
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fresh_tangency_2026/fresh.py --points 513 --dt .00025 --result-file <fine-run>/result.json
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fresh_tangency_2026/fresh.py --points 257 --dt .000125 --result-file <time-run>/result.json
python3 -B qwen_claude_field_theory/closure_2026/clock_response_repair_2026/fresh_tangency_2026/fresh.py --points 129 257 513 --result-file <offset-run>/result.json
python3 -B -m unittest discover -s qwen_claude_field_theory/closure_2026/clock_response_repair_2026/nonlinear_evolution_2026 -p 'test_*.py' -v
```

The four evolution executions exited 0: the measurements completed, **not**
that every refinement criterion passed. Exact command argument arrays,
paths replacing the labels above, hashes, versions, resource limits and logs
are in `run_001`, `fine_001`, `time_001` and `offset_001` manifests.
The final jet, action-balance and Lean command arrays are in `jets_002`,
`balance_002` and `lean_001`. All exited 0. Lean ran through the existing
clock_constitutive_construction_2026/lean_formalization_2026 project.

Before the fix, the single constant-background unit test exited 1; after it,
all three lapse tests exited 0. The first development dust-Ward calculation
also exited 1 because its differentiated volume term omitted U_d; correcting
that algebraic coding error made both independently checked matter Ward
identities pass. This was not a failure of the matter theory. The earlier
`jet65.json`, `balance_development.json` and `balance_001` are development
checkpoints, not final-source certificates.

`run_001`, `fine_001`, `time_001` and `jets_001` pin the pre-offset evolution
source and must remain historical records. Final-source evidence is
`offset_001`, `jets_002`, `balance_002`, and `lean_001`. No old manifest or
old evolved state has been overwritten to appear current.
All four final-source manifests were validated with `--root .`, exit 0.

Independent read-only review reconstructed the Noether/energy signs, dust
conventions, incoming characteristic and lapse offset. It identified the
need to state the on-shell chi equation explicitly and to broaden the jet
diagnostic beyond four free-field derivatives; both were incorporated.
Mathbox proof/computation review separates exact differential algebra,
conditional Lean leaves, finite-grid measurements and missing physical gates.
Self-proofreading covers this report, new Lean statements and README update;
no outside theorem or priority/novelty claim is invoked.
