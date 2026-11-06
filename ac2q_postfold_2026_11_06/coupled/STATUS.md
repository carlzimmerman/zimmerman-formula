# Coupled-field checkpoint: what is and is not decided

2026-11-06. Parent action unchanged. No new physical coefficient, surface action,
viscosity, smoothing rule, or empirical calibration has been adopted.

## Verdict

The regular native-field rescue is excluded in the planar interface class
specified below. AC2q has not been shown to remain predictive after a fold.
A universal claim that the full action must be extended is still unproved:
native singular or rapidly time-dependent layers, and full nonlinear avoidance
of breaking, remain unresolved. Numerical solver termination is not evidence
of a physical singularity.

This is a narrower, defensible result than either "gravity fixes it" or
"the complete theory is now disproved". If the physical continuation is an
ordinary finite same-direction shock in our class, it requires a change of
completion: the regular fields of the action cannot meet all its jump laws.
Whether a completion adds physics or can be derived from a unique native
singular limit remains the decisive open question.

## Results from the native action

1. **Metric response cannot hide the regular interface impulse.** Exact
   reduction of the four-dimensional action gives pi_beta =
   2 Mpl^2 exp(2 beta)(alpha'+beta') + 2 P pi_P and
   pi_alpha = 2 Mpl^2 exp(2 beta) beta'. Continuity of P and the normal
   conjugate fluxes forces both metric derivatives to be continuous.
   The spatial Hamiltonian then reduces to the previous matter obstruction.
   Assumptions: stationary timelike planar interface with stationary metric and polarization
   profiles (phi=s t+psi), gamma>0, continuous fields,
   uniformly nondegenerate metric, bounded one-sided derivatives and potential
   sources, no unresolved defect,
   same-sign nonzero through-flow, and gamma*s_local^2 < 1/3.
   The result does not cover arbitrary distributional spacetimes.
2. **The negative-divergence branch does not supply a quasi-stationary sheet
   under uniform regularity bounds.** The on-branch square alone is not a
   two-sided coercive bound. Instead, polarization-flux continuity fixes the
   off-branch Lorentz factor; the scalar normal current then has a nonzero
   coefficient multiplying P'. Bounded currents exclude the proposed sheet provided the limiting endpoint
   charge stays strictly positive, giving a uniform flux gap A>=1+delta>1.
   Rapid temporal variation, clock degeneration, unbounded metric gradients,
   and oscillatory limits are explicitly outside this argument.
3. **There is no automatically sourced plane tensor reservoir.** A transverse
   anisotropy obeys a homogeneous wave equation. Zero tensor initial data stay
   zero while its coefficients remain regular. This is a symmetry-restricted
   statement, not a claim that gravity never carries energy.
4. **The fully constrained homogeneous scalar sector has a wave-like high-k
   principal part, rather than a k^4 smoothing term.** The independent review
   derives, for the constant-V Mpl^2=1 fixture,

       b_dot = H n,
       n_dot = (A_dot/A + H_dot/H - 6H)n - (A s^2 Q^2/H)b,
       A = (K+gamma Q^2)/(2X(K+gamma Q^2)+(1-2gamma X)^2 Q^2).

   Here b is the metric perturbation and n is relative lapse, after the
   polarization and gravitational constraints have been eliminated. At large
   Q, A approaches a positive constant and omega^2 ~ A s^2 Q^2. Thus this
   coupled benchmark supplies neither a high-k linear instability nor a new
   dispersive regularizer. Linear behavior does not prove nonlinear shock
   formation, global smoothness, or absence of nonlinear oscillations.

## What the computations establish

- Exact coupled geometry and junction identities: main002 passes 10/10;
  layer identities: layers001 passes 9/9. Deliberately removed divergence
  coupling and altered Einstein coefficient produce the expected failures.
- Initial data satisfy the full planar constraints: initial002 passes 25/25.
  The exact hold-law cap, timelike scalar and positive branch are respected.
  These are dimensionless fixtures, not phenomenological parameters.
- The centered canonical solver reproduces homogeneous evolution to 9.4e-17;
  its elliptic Jacobian agrees with finite differences to 1.6e-9 relative.
- An independent reviewer verified the continuum canonical equations and
  compared a tiny Fourier perturbation with a separately derived two-variable
  linear system. Agreement is close at t=.01, but errors hit a numerical floor
  and do not demonstrate temporal convergence.
- Nonlinear longer runs are **not validated**. Even and odd grids, timestep
  changes and momentum reconstruction do not yield a converged endpoint.
  Earlier stopping at finer resolution cannot be called physical breakdown.
  Reconstruction enforces momentum but does not repair the unresolved dynamics.
- A joint lapse/polarization solve tested whether stale-stage polarization
  caused false X<=0 rejection. Its analytic Jacobian passes, but the first
  variant fails the homogeneous benchmark. A tightened variant passes that
  benchmark and stops on a Newton residual floor at t=.0014; a relaxed variant
  fails the homogeneous benchmark again. These are numerical failures, not
  new physical evidence. All variants and failed results are retained.

Independent junction review identified three needed qualifications: stationary
field profiles, positive gamma, and a uniform limiting endpoint gap. They are
now explicit in JUNCTION_RESULT.md and the PF02 derivation. The review itself
preserves the pre-correction hashes in REVIEW_JUNCTION.md.

All 30 manifests available at this checkpoint (including the seven earlier
PF01–03 manifests) validate against their recorded inputs. See VERIFICATION.json.
This verifies provenance, not the physical correctness of failed simulations.
The independent review_linear benchmark has its own frozen contract, executable,
command and result; it is separate from those 30 manifests. Two explicitly
unregistered timestep diagnostics are documented in JOINT_SOLVE_CONTRACT.md and
are not used as load-bearing evidence.

## What would decide extension versus native completion

A native survival result needs a well-posed constrained formulation and a
controlled nonlinear evolution (or theorem) that either avoids breaking or
produces a uniquely selected layer, including its stress and outgoing fields.
A sequence of regularizations is insufficient unless the limiting observables
and defect stress are independent of the auxiliary regulator, or that regulator
is itself specified physical input.

An unavoidable-extension result needs both (i) actual full-action smooth-data
breakdown, not just a PN simple wave, and (ii) exclusion or nonuniqueness of
admissible native continuations. We have strengthened the second obligation
for regular stationary-profile corners and bounded quasi-stationary layers; neither
obligation is completely discharged.

The next useful numerical work is to evolve variables adapted to the constraint
surface (the reviewed b,n system is the linear benchmark) with controlled
nonlinear constraints and product rules. Repeating the current canonical
solver at more grid sizes is not a closure strategy. The next analytic work is
an explicitly time-dependent layer balance with estimates for its surface
stress and dependence on incoming data. No arbitrary compensating stress may
be inserted and then called a prediction of AC2q.

## External theorem boundary

Bärlin, arXiv:2204.12101v3, Theorem 1.1 proves existence of derivative blowup
for a class of genuinely nonlinear, strictly hyperbolic first-order systems
with local smooth sources. It cannot be imported here without establishing
that the constrained AC2q equations meet its hypotheses. Eliminating spatial
polarization and Einstein constraints is potentially nonlocal; that reduction
has not been supplied. Source: https://arxiv.org/html/2204.12101v3 . This is a
conditional route, not a cited proof of full AC2q blowup.
