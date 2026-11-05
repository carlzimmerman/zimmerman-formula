# Full coupled inhomogeneous cap test: continuation remains unresolved

**The expansion cap is not established as a cure. This calculation also does
not establish that it moves a physical singularity into another field.** The
resolved evolution develops steep polarization/lapse profiles while the cap is
still unsaturated. Later solver endpoints fail spatial/continuum validation and
must not be interpreted as physical singularities. No run reached target t=3.
Kappa=1/2 remains FITTED; no action is adopted.

## 1. What was actually evolved

The full stated action from ../clock_repair/RESULT.md, restricted exactly to
plane symmetry, with independent clock tau=t, dynamical metric A,B, canonical
scalar phi and all their momenta, polarization P, cap auxiliary lambda and
spatially varying lapse N. The shift equation supplies the momentum constraint
before zero shift is chosen. External matter is zero. No fixed metric, fixed
scalar, Newtonian truncation or forced homogeneous lapse is used.

See [REDUCTION.md](REDUCTION.md) for the full Lagrangian, Hamiltonian, constraint
solve and variational equations. Initial data satisfy both local Hamiltonian
and momentum constraints. The constants and initial perturbation were frozen
in [CONTRACT.md](CONTRACT.md). These data describe inhomogeneous contraction,
not the older tilted geodesic clock on a regular fixed FRW spacetime.

The uncapped control uses separately constrained initial scalar momenta. It
therefore does NOT provide an equal-physical-initial-data collapse-time ranking.
Its late endpoints also fail refinement; they cannot establish a benefit or
harm from the cap.

## 2. The mathematical result

Write v=exp(A+2B), Dp=exp(-A)(P_x+2B_x P), F=1+gamma Dp and

 Bcal=-Theta^2/3+sigma^2-lambda Theta_star-U-R3/2
       +pi_phi^2/(2v^2)+exp(-2A)phi_x^2/2+V,
 sigma^2=(kx-ky)^2/3.

Completing the square in the FULL Hamiltonian constraint gives

 **W + F^2/(2gamma) = 1/(2gamma)-Bcal = R.**

Consequently exact polarization saturation z=K|P|/a ->1 cannot occur with
uniformly bounded R and a bounded away from zero:

 **1-z >= exp[-1-K R/a^2].**

If the wall is genuinely reached, some other gravitational/scalar/cap quantity
must lose its bound, or a must tend to zero. Observing z close to one does not
prove either event. The potential energy grows logarithmically, but
W_P=K P/(1-z) becomes steep much sooner.

The exact polarization equation is

 **(log N)_x=[exp(A) W_P-gamma(Dp)_x]/F.**

With bounded coefficients, F away from zero and the periodic compatibility
condition, N is a strictly positive exponential. A truncated Fourier lapse
crossing zero is not a continuum singularity. F=0 is a separate potential
constraint-branch degeneracy; it did not occur in the resolved interval.

Meanwhile the cap bounds Theta-Theta_star. On this positive-phi branch,
Theta_star>0, so Theta>-T and **v(s)>=v(0)exp(-T s)** along the normal flow
while a smooth clock foliation persists. This truly excludes finite-proper-time
volume focusing in that regime. It does not bound shear, spatial curvature,
scalar gradients, lapse gradients or auxiliary stress. Full derivations and
precise assumptions are in [REGULARITY.md](REGULARITY.md).

## 3. Reliable finite portion of the computation

The audit checks79 output times from0 through.78, at spacing.01, with1024-point
Fourier interpolation for continuum residuals/domain checks. This is numerical
evidence, not an interval-arithmetic enclosure between output times or nodes.

At t=.78 on the257-node bracketed run:

| Quantity | Value |
|---|---:|
| minimum volume / initial volume | .65866475 |
| maximum polarization fraction, dense interpolation | .97529480 |
| minimum lapse | .85763185 |
| minimum Q=1/N | .90143062 |
| minimum cap gap 1-abs(Theta-Theta_star)/T | .17739698 |
| maximum abs(lambda) | .14466756 |
| minimum1+gamma Dp | .99638177 |
| maximum shear sigma^2 | .00374196 |
| maximum abs(R3) | .03831631 |

The cap is still about17.7% short of its wall while polarization is only2.47%
short of its wall. These percentages concern different dimensionless variables;
they are not comparable distances in field space or a singularity-time estimate.

Over all79 samples through.78:

- 33/65-node maximum normalized field-profile difference:1.78185e-4.
- 65-node rtol1e-7 versus1e-9 difference:2.63947e-6.
- 33-node time-control difference:6.02285e-6.
- 129/257-node difference:3.03645e-5.
- All audited dense domains remain valid and evaluated arrays finite.
- 65-node maximum continuum polarization residual:1.88714e-4;
  dense Hamiltonian residual8.23419e-8; momentum residual1.86199e-8.
- 129 and257 maximum continuum polarization residuals:2.08364e-6 and2.16825e-6.

Profile errors use max_x|f_low-f_high|/(1+max_x|f_high|), separately for all
metric/scalar fields, canonical momenta, P,N,lambda; the largest is reported.
The reference is not an exact solution. Constraints use the normalization
implemented in analyze.py. The frozen thresholds are passed on this finite
sampled interval. No success claim is extended to the target time.

## 4. Why the late endpoints cannot answer the singularity question

| Run | Last accepted coordinate time | Stop reason |
|---|---:|---|
| capped17 | .80551423 | polarization iteration budget |
| capped33 | .80987640 | Fourier lapse positivity |
| capped65 | .81149256 | Fourier lapse positivity |
| capped129 | .82751323 | Fourier lapse positivity |
| capped257, original root | .84472111 | cap Newton iteration |
| capped257, bracketed root | .84656546 | cap-root residual failure in a trial stage |

These are numerical stopping points, NOT physical collapse times. The retry
budget is finite and a bad internal trial state need not imply failure at the
last accepted state. The bracketed run did not establish complete continuation.

The off-grid audit is decisive: the65-node profile reaches dense z=1.00666 at
t=.81 even though its nodal z remains below one. The129-node dense profile
reaches1.00594 at t=.82. Those interpolants are outside the action's domain.
Even before domain violation, continuum polarization residuals grow: at.80,
65 nodes gives.14146,129 gives.05114,257 gives.001128. At.81 the257 residual
is.01005. The33/65 field-profile discrepancy at.80 is.03528, above the frozen
.02 threshold. Small discrete Hamiltonian residuals do not repair these failures.

The65-node tighter time run stops near.81149410, but spatial endpoints drift
strongly with refinement. Time-step agreement therefore does not establish a
continuum singularity. The uncapped endpoints at17/33/65 are1.71835/1.57416/
1.26378, with excessive late momentum residuals; these are also unvalidated.

## 5. Checks, failures, and evidence

- 10/10 exact independent symbolic checks: Legendre transform, canonical
  velocities, lambda envelope, shear decomposition, cap parametrization and
  polarization variation.
- 8/8 numerical initial-data/derivative/homogeneous checks for each cap-on and
  cap-off implementation control.
- Bracketed solver:10/10 checks, including reproduction of the original Newton
  failure and comparison with independent Brent roots (max error1.87e-14).
- The first evolution had an uncaught dense-output stage failure; retained
  source planar_first_attempt.py.txt. The handler was fixed without altering
  physical equations or tolerances.
- The original cap Newton solver has a reproducible2-cycle despite a unique
  regular root. ROOT_FIX.md gives the witness and bracket. This was a numerical
  defect, not a counterexample to the action.
- NumPy emitted floating-point warnings at some matrix multiplications despite
  finite audited saved arrays. Explicit summation checks of D2 B agree within
  1.94e-12 on the audited interval. This does not diagnose every warning or
  replace an independent implementation; it remains a numerical-environment risk.

Authoritative audit: evidence/analysis_interval/results.json and manifest.json.
It hashes all trajectories used, including ones not originally declared as
runner result files. Earlier selected-time analyses and failures are retained.
The129-node extension was authorized in REFINEMENT.md before execution; its
original machine contract still lists the initial17/33/65 grid set. That
metadata mismatch is disclosed, not silently rewritten. The257/refinement
contract lists the extended grid set explicitly.

## 6. Consequence for the candidate action

We have identified an additional continuation obligation, not completed the
action: the polarization/lapse constraint must remain regular and resolved
while shear and scalar/curvature derivatives are controlled. The current cap
supplies no proof of those controls. The calculation reaches a trustworthy
inhomogeneous contraction regime and then loses resolution of the stiff
polarization sector. It neither demonstrates a cured collapse nor a relocated
physical singularity. A positivity- and domain-preserving spatial method with
continuum constraint convergence is needed before extending the verdict.
