# PF07: repaired pre-break evolution and dynamic-layer exclusions

2026-11-06. Base e50f32a0a7, initial criteria 48c08b18e5. Native AC7 action
unchanged. No new physical coefficient, dissipation, entropy prescription,
surface action or postfold continuation has been adopted.

## What is decided

The solver's early growth was largely a numerical aliasing problem. A curvature-
subtracted, constrained, padded formulation now gives checked pre-break results.
This is a repair over a demonstrated interval, not a validated postfold solver.

The analytic obstruction is substantially stronger than PF06's stationary
result. Regular time dependence cancels from the corner mismatch. In explicitly
controlled thin-layer limits, polarization and scalar surface storage vanish,
and the native matter Hilbert stress has no surface measure. Thus those native
mechanisms cannot be assigned the missing interface stress or charge.

The full three-way classification remains incomplete. We have not proved
smooth-data breakdown of the full coupled action, nor ruled out every singular,
nonmeasure or noncompact continuation. No result here establishes a unique
native postfold prediction. If AC2q develops the same-sign finite-state corner
under the intersected hypotheses below, a completion outside that class is
required. Calling every such completion "new physics proved necessary" would
exceed the evidence; calling the current action scientifically closed would too.

## Numerical root cause and repair

The canonical momentum p_beta contains a large spatial-curvature contribution.
We evolve

    r_mom = p_beta - [2 Mpl^4 exp(4 beta)/p_lambda]
                      (2 beta_xx+3 beta_x^2).

This exactly cancels curvature from the algebraic Hamiltonian solve. Its RHS
uses the chain rule of the independently reviewed canonical equations. At each
stage the odd-grid momentum constraint is reconstructed, preserving mean
p_lambda. No artificial viscosity is added.

Changing variables alone does not cure the cutoff instability. On the initial
inhomogeneous fixture, the finite-difference mode Jacobian has largest real
parts 22.049 (n15) and 90.117 (n31) without padding; with triple padding these
are about 2e-5 and 3e-4. The homogeneous principal modes already had the expected
imaginary frequencies. Nonlinear collocation product rules were corrupting the
large derivative cancellations. Evaluate nonlinear terms and constraints on a
padded grid and project the RHS back. This approximates Galerkin evaluation;
finite padding is not an exact rule for exp/log/reciprocal nonlinearities.
Padding sensitivity was therefore checked explicitly.

Independent code review found no coordinate or chain-rule error. It correctly
requested padded-wrapper tests, raw rather than only reconstructed constraints,
physical-field comparisons, spectra beyond q and padding sensitivity. Those
checks were added; the original reviews are retained, not retroactively rewritten.

## Demonstrated numerical interval

Reported cross-grid field differences are evaluated after restriction to a
common represented Fourier grid; separate full evaluation-grid spectra check
the omitted high modes. They are finite-grid error diagnostics, not certified
continuum error bounds.

The fixed dimensionless fixture is Mpl^2=1, K=.5, gamma=.1, s^2=.01, V=.01,
a0=.3, k=128, initial P=.002 sin(kx)/k. The constant V and a0 correspond to
an admissible fixed xi; they are not new observational calibrations. In particular
gamma*s^2=.001 is not the canonical astrophysical footing near 2.4e-17.
No universal parameter-range or empirical claim follows from this fixture.

- Exact curvature cancellation passes. The transformed RHS reconstructs the
  original canonical RHS to maximum absolute error 2.1e-9 on a smooth test.
- Padded homogeneous evolution error at t=.1 is 1.53e-10 (<1e-8 criterion).
- The independently derived mode-4 linear reference agrees at t=.01; relative
  beta errors fall from 2.72e-4 to 2.76e-5 as amplitude goes from 1e-8 to 1e-9.
  This supports the linear limit, not temporal convergence by itself.
- At t=.5, n31 versus n63 gives max charge difference 2.59e-11; halving dt
  gives 3.26e-11; padding factor3 versus5 gives 1.64e-11. Lapse and momentum
  comparisons are in comparison001/result.json. Raw normalized momentum improves
  from 6.57e-11 to 9.26e-13 with spatial refinement. Reconstruction corrections
  and idempotence errors are near machine precision in the represented modes.
- At t=1, n127 versus n255 gives max charge difference 3.75e-11; at n127,
  evaluation-grid sizes255 versus381 differ by 3.46e-11. Lapse differences are
  below 5e-12; max p_beta differences are a few e-6 against variation about3.14.
  All monitored fields have small upper-third spectral fractions and the raw
  momentum criterion passes. See comparison_t1/result.json.

Later refinement detects its own accuracy limit. With the stricter raw momentum
criterion 1e-7, n127 stops at t=1.2425 with either evaluation size255 or381,
and n255 at t=1.33375. At the latter stop,
q is in [0.005037,0.006640], min X=.002657 and the cap ratio is8.67e-6;
max |q_x|=.8454, against initial~.256. These finite values and increasing
resolution-dependent intervals support pre-break steepening, not a proof of
finite-time blowup or its time. The last step failing the threshold is not
part of the accepted interval. Earlier q-only runs reaching t~1.5 are exploratory
and cannot override the later, stricter constraint checks.

See evolution_diagnostics.png/pdf. Crosses denote numerical accuracy stops.
No run crosses a demonstrated physical shock or claims an outgoing postfold
observable. Increasing resolution alone cannot establish uniqueness of a
singular continuation.

## Exact time-dependent corner result

At a regular timelike planar interface, retain the common tangential derivative
T=P_t+2P beta_t. With ell=P_x+2P beta_x, v=-phi_x/phi_t, and
J=-pi_P^x, partial Legendre elimination gives exactly

    f(v)=exp(2alpha+2beta) f0(v)-J v T.

The correction is affine in v. It shifts the scalar normal current equally on
both sides and cancels from v f'-f. The PF02 convexity obstruction therefore
survives regular time dependence. Assumptions include common C1 tangential
traces, positive gamma, nondegenerate metric/timelike clock, strictly positive
endpoint q, same-sign nonzero flow, gamma exp(-2alpha)phi_t^2<1/3, and no defect
in the normal-current/stress matching. Distinct admissible endpoint states
cannot satisfy all those corner conditions.

The independent derivation is ../coupled/time_layer_review/REVIEW.md; eight
exact symbolic checks accompany it. It supersedes the stationary-profile
restriction of the earlier proof by retaining, rather than dropping, T.

## What genuine time-dependent layers cannot carry

The following statements concern smooth on-shell approximation families and
specified measure limits; they do not define all possible weak solutions.

1. **Polarization storage.** Define Q=1+gamma max(D+2X,0) and
   K^a=exp(-2beta)pi_P^a. Exactly,

       partial_a K^a=-exp(2alpha) W_P,
       K^x=-exp(alpha) C Q<0,  |K^t|<=-K^x.

   In a locally finite current-measure limit, no dipole source forbids a
   normal surface current. The fixed sign and domination then forbid temporal
   surface current as well, including fast time variation. A regular bounded
   hold-law source yields ordinary normal-flux continuity. The moving-interface
   proof uses its timelikeness; null interfaces and nonmeasure limits differ.

2. **Scalar storage.** The exact contraction is

       J_phi.dphi = E B(1-2gamma D)      on branch,
                    E B(1+2gamma B)     off branch, B=2X.

   For bounded clock norm/metric it is dominated by C(1+Q), with no surface mass.
   The identity div(phi J)=J.dphi+phi divJ passes to the limit using uniform
   phi convergence and bounded current total variation. Its surface coefficient,
   after subtracting phi times the scalar balance, is
   (d phi_trace/dt) j_phi^t=0. A regular future timelike trace has positive
   derivative, so scalar surface storage vanishes too. This avoids multiplying
   weakly convergent gradients by weakly convergent currents.

3. **Matter Hilbert surface stress.** Introduce Q>=1, A=Q/sqrt(2X),
   Pi=exp(2beta)P, and the exact auxiliary/KKT action described in
   AUXILIARY_STRESS.md. Its derivative coupling is a metric-independent wedge
   term. The on-shell Hilbert stress is algebraic in bounded frame-clock
   variables, A,P, and an off-branch multiplier mu=max(-D-2X,0).
   Along fixed clock slices,

       dA/dx=exp(2alpha)W_P/phi_t,
       dPi/dx=(E sqrt(2X)/phi_t)D.

   A bounded value anchored on a crossing boundary, cap separation, regular
   metric and clock bounds control A and D_+. Strong matching of endpoint Pi
   then forces the integrated negative variation, hence the L1 mass of mu,
   to vanish. The remaining stress is bounded and integrates to zero across
   a shrinking layer. No matter surface stress remains.

The third result needs uniform bounds on frame components (e.g. phi_t both
above and below, and sqrt(2X) above and away from zero), not merely on the
Lorentz invariant X. It also needs strong endpoint matching along the same
clock slices; a continuous weak limit of P is insufficient. Finite current
measure compactness is an additional hypothesis for statement2. No claim
that these hypotheses follow automatically from finite signed action is made.

Full proofs and independent audits: ../coupled/time_layer_review/
POLARIZATION_MEASURE.md and AUXILIARY_STRESS.md. The role of gravity and the
precise canonical/Hilbert matching bridge must also be respected; no matter
stress does not by itself exclude a gravitational concentration defect.

## Combined restricted no-layer theorem

The independent final audit in ../coupled/time_layer_review/MATCHING_BRIDGE.md
connects these statements without assuming an arbitrary canonical/Hilbert
identification. Direct normal-metric homogeneity gives

    Hx_matter = -E T^x_x.

Uniformly bounded metric first derivatives exclude a quadratic gravitational
surface defect. The full Einstein delta equations with no matter surface stress
then force extrinsic-curvature continuity. Stress conservation, with bounded
connection and vanishing absolute layer stress, gives normal Hilbert flux
continuity. Together with the current lemmas this supplies every required
normal corner condition.

An essential additional hypothesis is that bulk stress and currents converge
to the native expressions of the regular outer states: no unidentified bulk
oscillatory defect. Absence of a surface measure alone does not identify a
nonlinear bulk limit. With this and the intersected compactness, frame, cap,
strong-trace and metric assumptions, no smooth native thin-layer family can
connect distinct same-sign, positive-charge endpoint states in the PF02 range.
The layer may visit the negative-divergence/off branch internally; that does
not evade the result. This is a restricted nonexistence result for a controlled
native completion, not just a count of unspecified surface variables.

## What remains genuinely open

- Establish full coupled finite-time breakdown from valid smooth data, or show
  that native evolution avoids it. The PN simple wave and numerical accuracy
  stops do not discharge this obligation. The repaired solver now provides a
  checked starting point for that question.
- Prove compactness into the controlled layer class, or construct and test a
  specific escape: loss of frame-clock bounds, cap approach/source measures,
  discontinuous P traces, singular gravity, or currents without finite measure
  compactness. Merely naming one does not give its existence, uniqueness,
  stability or outgoing predictions.
- If an alternative completion is proposed, specify its actual equations and
  stress/charge budget. A viscosity, entropy rule or freely fitted surface
  stress is an extension unless derived as a unique limit of the native action.

These are open dependencies, not an exhausted list or a proof that arbitrary
singular completions are impossible. The practical conclusion remains that
AC2q has no established unique postfold prediction as written; the ordinary
controlled native-layer rescue has now been sharply constrained.

## Verification and retained failures

Nine exact auxiliary/current/stress identities pass in auxiliary001; the
reversed topological sign fails precisely clock_slice_A_equation in the mutation
control. The layer estimates themselves are analytic, independently reviewed
proofs under stated hypotheses, not conclusions inferred from those counts.

All 54 computation manifests available at this checkpoint validate against
their recorded inputs (including the prior 30). A valid manifest may record a
failed run. validation001 failed during NumPy-boolean JSON serialization;
validation002 changes output conversion and passes all five intended checks.
The unpadded and unprojected failures, later accuracy stops, and independent
review records remain preserved. See VERIFICATION.json.
