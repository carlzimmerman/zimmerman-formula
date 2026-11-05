# A scoped nonselection theorem for the actual polarization kernel

The coefficient has not been derived. The following explicit family shows
that covariance, the existing internal symmetries, homogeneous/quadratic
cosmological data, global polarization convexity and saturation do not fix
the operational MOND scale. This does not exclude an additional microscopic
principle or a stronger, independently established full-health condition.

## Exact deformation

Let K=4pi G, a>0, u=p/a in[0,1). Replace the polarization potential only by

    W_e(p,a)=a^2/K [-u-log(1-u)+e u^3(1-u)^2/3], -1/2<=e<=1/2.

Here a denotes the saturation scale, which need not equal the measured
deep-MOND normalization after deformation. The added term is a scalar made
from the same p and a(X,phi), and preserves all stated diffeomorphism,
canonical scalar shift (for constant V) and scalar reflection symmetries.
It changes neither the P.A normalization nor the Einstein coefficient.

The added term and its first two field variations vanish at P=0 for every
smooth positive a(X,phi). Thus the homogeneous branch and its entire
quadratic action, including minimally coupled matter, are unchanged. The
|P|^3 dependence is C2 at zero; no third Frechet derivative is claimed there.

## Convexity and saturation are preserved uniformly

Write f_e=K W_e/a^2. Its second derivative is

    f_e''=1/(1-u)^2+e C(u),
    C(u)=2u-8u^2+(20/3)u^3.

The cubic Bernstein coefficients of C on[0,1] are
(0,2/3,-4/3,2/3). The Bernstein basis is nonnegative and sums to1,
so |C|<=4/3. Consequently f_e''>=1-2/3=1/3 and
W_pp>=1/(3K)>0 throughout the declared domain.

Also f_e'(0)=0 and (1-u)f_e'(u)->1 as u->1-. Thus the conjugate
acceleration A=K W_p=a f_e'(u) maps p in[0,a) monotonically onto[0,infinity),
and the limiting saturation is still p->a. No instability inference for the
entire gravitating action is being made from this constitutive convexity.

## The operational acceleration changes

In the leading weak-field, unscreened, static spherical response at fixed
local scalar state, the flux equation is gN=A-p and the physical force is
g=A. This excludes screening, cosmological-source dominance and finite
potential corrections from the density-dependent portal. At this order,

    gN=a u^2 [1/(1-u)+e(1-u)(1-5u/3)].

It is positive for0<u<1: the bracket is at least1-1/2. It is also strictly
increasing. To see this, C/u=2-8u+(20/3)u^2 lies between-2/5 and2,
while1/(1-u)^2-1>=2u. Therefore

    d(gN)/dp=f_e''-1 >= 2u-|e|*2u >= u>0.

Expansion at u=0 gives A=a[u+(1+e)u^2+O(u^3)] and
gN=a[(1+e)u^2+O(u^3)]. Hence the operational scale is

    a_MOND = lim[gN->0+] g^2/gN = a/(1+e).

For the density portal a^2=b rho, c=1,

    kappa_operational = a_MOND/sqrt(G rho)
                      = sqrt(b/G)/(1+e),
    partial_e kappa_operational = -sqrt(b/G)/(1+e)^2 != 0.

Neither the exact target value nor a measured coefficient was used in
constructing or evaluating this family. The unchanged e=0 kernel recovers
the original simple-mu relation. The family demonstrates a physical force
normalization change with the metric and matter calibration held fixed,
not just a change of notation for a.

## Why normalizing the clock does not remove the free coupling

Allow the canonical sector to be written Z X-V. Under the invertible field
redefinition phi_new=lambda phi, its coefficient becomes Z_new=Z/lambda^2.
The physical density Z X+V is unchanged, as is the normalized clock n for
lambda>0. The equation a^2=b rho therefore retains b. Setting Z=1 fixes a
field convention, not b/G. An arbitrary relabeling of clock leaves is also
not a symmetry of the canonical kinetic action, even though n alone is
unchanged by a monotone relabeling. One cannot use that absent symmetry to
set the portal normalization.

## Exact obstruction and missing input

These stipulated principles leave a continuous family of different
operational coefficients. They cannot imply one exact coefficient. Even
if an additional argument fixed b, it would have to fix the response
deformation as well, or otherwise fix the invariant combination
sqrt(b/G)/(1+e). Choosing e=0 because it is the preferred interpolation
function is a model choice, not a derivation of that invariant.

A successful continuation needs a named microscopic matching equation,
new symmetry identity, quantization condition, or genuine dynamical
selection which fixes this invariant and survives the full action/source
matching. We have not supplied one. We have not computed a quantum loop,
proved that e is radiatively generated, or excluded every possible new
symmetry. Nor have all deformed actions been tested for full nonlinear
health. Those are separate, still-open obligations.

### The vacuum term needs protection as well

The stated symmetries also allow a field-independent term
`-DeltaV integral sqrt(-g)`. This observation is about allowed classical
operators; it does not assert that a particular loop calculation generates
DeltaV. With the original portal held fixed, the homogeneous physical
density becomes rho_total=X+V+DeltaV while the saturation scale still uses
a^2=b(X+V). Its operational ratio would be

    kappa_total = sqrt(b/G)/(1+e)
                     * sqrt[(X+V)/(X+V+DeltaV)].

Thus a genuine prediction must jointly fix which vacuum energy gravitates
and the operational response coefficient. Simply declaring that every
vacuum correction must also be inserted into the portal is another matching
rule, not a consequence of the symmetries checked here. This is the known
vacuum-counterterm obstruction specialized to this actual candidate; no
claim of a newly discovered cosmological-constant problem is made.

Equivalently, write the small-p kernel as

    W=p^2/(2K)+C3*p^3/3+O(p^4), C3=(1+e)/(K a).

In the stated force regime a_MOND=1/(K C3), so the required invariant
matching condition is `K^2 C3^2 G rho_total = 4` in c=1 units. This is a
transparent restatement of the target, NOT a derivation. It specifies the
two physical quantities that an upstream mechanism must connect, while
the coefficient of the quadratic term is already fixed by the chosen
Newtonian/MOND matching. No arbitrary clock normalization supplies it.

## Proof audit and evidence

Primary verdict: proved as written for the explicitly listed principles
and leading response regime. Self-review only. Dependency checks: exact
action deformation, degree counting, Bernstein bound, saturation limits,
monotonic Newtonian flux, operational definition, fixed matter/metric
normalization and clock field redefinition. Whole-action admissibility
beyond those properties is not addressed.

normalization_v2.py checks all16 exact identities. The mutation incorrectly
holds the deep coefficient fixed as e varies and must fail. The original
script's expression-tree comparison failure is preserved and explained in
NORMALIZATION_ERRATUM.md. No domain or physical assumption was changed.
No novelty claim: the explicit test applies the prior allowed-deformation
strategy (CFG894 K721/K756/K783) to this candidate, with additional global
convexity and saturation checks.
