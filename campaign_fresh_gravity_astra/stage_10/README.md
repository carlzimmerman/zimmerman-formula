# Checkpoint: stability controlled by the scale profile

2026-09-30, 04:23 UTC heartbeat pass. Parent: [stage nine](../stage_09/README.md).
The physical theory remains open. This pass takes the stronger-analytic-bound
route in FGF-025; no numerical continuation, spectrum or observational test
was executed or inferred.

## A stronger exact criterion

On the inherited regular Q/R hydrostatic wall slab define
w=chi', R=rho q/lambda and M=U''-T_chi-q²/lambda. Differentiating the actual
background equations gives

    J w''=M w-C R,   C=4piG.

For a scale profile strictly increasing throughout the closed interval,
w>0, the troublesome coupling has the exact identity

    J eta'²+M eta²+C R(w xi²+2xi eta)
      =J w²[(eta/w)']²+(C R/w)(eta+w xi)²
        +[J(w'/w)eta²]'.

Together with the existing fluid-gradient and potential-gradient squares,
this writes the entire quadratic potential as four nonnegative squares.
The endpoint term vanishes for fixed xi,psi,eta. The energy is strictly
positive and coercive on each regular compact patch with w bounded away
from zero. Positive kinetic coefficients and the retained conserved boundary
flux give conditional linear longitudinal stability.

This **removes the explicit short-domain determinant condition** within that
sign domain. It is not a uniform spectral-gap bound, nor proof that an IVP
admits arbitrarily long increasing-scale solutions. No specific longer
example failing the old bound has been constructed. The criterion applies
to every existing solution satisfying the stated hypotheses; local existence
provides nonempty examples.

The complete static scale operator after eliminating the potential includes
the positive rank-one wall term. The new squares justify its positive inverse
in this sign domain. Static minimization is not elimination of dynamical
fields with positive inertia. Neither boundary condition has been dropped.

## A useful negative control on interpretation

The weighted expression divides by w and is invalid at a zero. The original
quadratic form is regular there. Choose interior initial data B,rho>0 and
chi=w=0. The inherited cosh potential gives w'=-T/J<0, so a two-sided smooth
local solution crosses w=0. On sufficiently short symmetric induced-wall
patches the earlier general Poincare criterion still guarantees positive
energy. Thus loss of the increasing-scale criterion does not imply instability.
This is a separate local family, not continuation of a previously fixed long
slab through its first turning point.

## Independent evidence and scope

Root proposed and recorded the weighted identity. The FGF-025 worker
reconstructed the algebra and extended static elimination, with attribution
preserved. A separate agent independently audited the root candidate,
coercivity and turning-point control without using the new worker proof.
These are distinct verification roles, not independent discoveries.

- [Root candidate and proof](monotone_scale/ROOT_CANDIDATE.md).
- [Turning-point control](monotone_scale/TURNING_POINT_CONTROL.md).
- [Independent proof audit](monotone_scale/INDEPENDENT_AUDIT.md).
- [FGF-025 reconciliation](../../deepseek_push/astra_spawn_ideas/fresh_gravity_followups/reviews/FGF-025_RECONCILIATION.md).
- [Coordinator receipt](COORDINATOR_VERIFICATION.json).

All scientific claims are conditional on the local Q/R diagnostic action,
positive coefficients, nonzero gravitational field, fixed impermeable walls
and induced field endpoints. Both a0 normalizations and constant-vacuum versus
frozen H reference families remain separate. Source flux is MOND throughout;
no registered M action is invented. Actual a varies, so the literal pointwise
constant-vacuum scale relation remains incompatible without further changes.
No filtered-MONO, photon/metric, global isolated, 3D/nonlinear or empirical
closure follows.

The remaining stability boundary is a selected full continued slab containing
a scale turning point, using the nonsingular original form. A local stable
crossing alone does not answer that full-domain question. Pressure information
FGF-024 remains separately ready; AS228 metric repair retains its primary owner.

FGF-026 records the full-domain first-turning-point question as an unlaunched
specification. Queue: 26 tasks, thirteen reviewed_scoped and thirteen ready.
Both actual agents completed; no FGF worker running. Findings were sent to the
authorized peer; no reply, physical acceptance or repaired metric is implied.
