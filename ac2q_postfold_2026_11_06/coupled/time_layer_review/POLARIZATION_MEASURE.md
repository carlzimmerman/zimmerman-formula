# Independent audit: no polarization surface storage in the finite-measure class

**Primary verdict: proved as written under the explicit measure and source
hypotheses below.** The sign and domination argument works even with
arbitrarily fast temporal variation. With a bounded weighted hold-law
source it also gives ordinary normal polarization-flux matching. It does
not exclude scalar/metric storage, stress concentration, or more singular
and noncompact limits.

## Normalized claim and assumptions

Consider smooth thin-layer approximants in the oriented conformal planar
chart, with gamma>=0 and timelike scalar gradient. Write

    Q=1+gamma max(D+B,0)>=1,
    pi_P^x=-exp(alpha+2beta) C Q,
    pi_P^t=v pi_P^x, |v|<1, C=(1-v^2)^(-1/2).

The interface Sigma is timelike; initially take it to be x=0. Assume local
uniform total-variation bounds on the spacetime current measures and
weak-* convergence to locally integrable bulk currents plus possible finite
surface measures. Assume the limiting P equation has no dipole source.
For the additional flux-continuity conclusion, assume the source has no
surface measure either. Uniform regular/nondegenerate metric coefficients
and uniform separation from the hold-law cap are sufficient source bounds
in the precise weighted formulation below.

Bulk subtraction means the locally integrable bulk part of the limit.
It cannot include a separately inserted surface term or a singular
reference "bulk" profile. One-sided normal traces are required to express
the balance as a jump. Without traces the result is distributional, not a
pointwise jump formula.

Conclusion: the polarization current has no surface-supported normal or
temporal measure. With no surface source, its normal flux has no jump.

## Exact integrating factor eliminates source-product ambiguity

The full-switch reduced Lagrangian has

    L_,P=2 beta_t pi_P^t+2 beta_x pi_P^x-exp(2alpha+2beta) W_P.

This follows because D is affine in P through
P_t+2P beta_t and P_x+2P beta_x; the remaining explicit P dependence is W.
Therefore each smooth approximant obeys the exact equation

    partial_a K^a=-exp(2alpha) W_P,
    K^a=exp(-2beta) pi_P^a.

In particular

    K^x=-exp(alpha) C Q<=0,
    K^t=v K^x,
    |K^t|<=-K^x.

This is preferable to passing separately to products of weakly convergent
currents and beta derivatives. If metric coefficients converge locally
uniformly to finite nondegenerate limits, weighting and unweighting current
measures is justified. The smooth-family identity passes to the limit
directly. Bounded metric first derivatives are a sufficient regularity
assumption; the integrating-factor argument does not need to assign an
ambiguous value to a discontinuous beta derivative on a surface measure.

For the stated hold law,

    W_P=Khold P/(1-Khold |P|/a0).

Uniform cap separation and bounded regular field/parameter values make the
weighted source locally bounded. Its integral over a shrinking spacetime
strip then vanishes. For a more general source, explicitly require absence
of a singular source measure rather than merely calling it "explicit."

## Proof of surface-storage exclusion

Let mu_epsilon=-K_epsilon^x dt dx and nu_epsilon=K_epsilon^t dt dx.
These satisfy mu_epsilon>=0 and |nu_epsilon|<=mu_epsilon as measures.
Local weak-* compactness gives limits mu>=0 and nu with |nu|<=mu. For
example this follows by testing the inequalities
-mu_epsilon<=nu_epsilon<=mu_epsilon against every nonnegative continuous
compactly supported test function and passing to the limit.

Write the interface-supported parts as

    K^x=K_bulk^x+j^x(t)delta(x),
    K^t=K_bulk^t+j^t(t)delta(x).

The coefficients may be finite measures along the interface; the equations
below are then understood distributionally in t. The normal derivative
produces j^x delta'(x). The temporal derivative of a current supported on
the fixed interface produces only a tangential derivative of its
coefficient, not a normal dipole. No dipole source therefore forces j^x=0.

The domination inequality restricts to Sigma:

    |j^t|<=-j^x=0.

Hence j^t=0. The proof does not subtract two positive divergent masses:
the singular part of the nonnegative limiting mu is nonnegative, and
the locally integrable bulk part assigns zero mass to Sigma. Thus ordinary
bulk subtraction cannot conceal a compensating negative surface mass.

The remaining delta coefficient in the field equation is

    [K^x]+partial_t j^t=r_surface.

If r_surface=0, this gives [K^x]=0. With continuous beta, equivalently
[pi_P^x]=0. If a source surface measure is present, storage is still absent
under the same no-dipole assumptions, but the flux jump equals that source.

Arbitrarily fast temporal variation does not change this argument. It is
joint spacetime weak convergence, not convergence at each fixed time.
Once the current has no surface measure, temporal differentiation cannot
create one from a vanishing surface-current limit. A claim of rapid
variation alone is therefore insufficient to supply polarization storage.

## Moving interfaces and coordinate speed

In the conformal metric, v=-phi_x/phi_t is the coordinate velocity of the
timelike scalar normal; the conformal light speeds are exactly +/-1.
Thus the domination inequality is correct in this chart. In a general ADM
chart with shift, an unmodified |v|<1 formula is not the coordinate formula;
one must transform the current and the cone together.

For Sigma given by x=xi(t), the normal dipole coefficient is

    j^x-xidot j^t.

The no-dipole condition, domination, and timelikeness |xidot|<1 imply

    -j^x=|j^x|=|xidot j^t|<=|xidot|(-j^x),

so j^x=j^t=0 locally. On compact regular timelike portions a uniform speed
margin makes this argument immediate for measures. The remaining bulk
matching is [K^x-xidot K^t]=0, or the corresponding weighted original
current condition. In a local rest chart it reduces to [pi_P^x]=0.
Merely setting xidot=0 at one event while differentiating a distribution
over a moving interface would be insufficient; the formula above retains
the motion correctly.

A conformal local-rest boost also preserves the current cone: the new
normal component is proportional to K^x(1-u v)<0 for |u|<1, and the new
ratio of temporal to normal components is (v-u)/(1-u v), of magnitude
less than one. The conclusion is therefore not an artifact of selecting
the interface rest frame.

## Failure modes and exact limits of the statement

* At the hold-law cap W_P can diverge and produce a surface source or fail
  to have a finite-measure limit. A finite source measure can allow a flux
  jump even though the storage exclusion still holds. A dipole/nonmeasure
  source can invalidate the normal-dipole step itself.
* A scalar-null limit v->+/-1 does not by itself invalidate domination:
  the inequality survives as a non-strict inequality. But C can diverge,
  destroying the assumed local finite current-measure bounds. If those
  bounds and the other hypotheses do survive, the exclusion still holds
  for a timelike interface. Thus scalar-null approach is not an automatic
  counterexample to this conditional lemma.
* A null interface is different: |xidot|=1 permits equality in the moving
  cone argument and a nonzero null-tangent surface current is not excluded.
* Degenerating/unbounded metric coefficients or lack of uniform metric
  convergence can obstruct the weighting/unweighting limit. More singular
  derivatives, dipole currents, nonmeasure limits, or unresolved nonlinear
  bulk defects require a different analysis.
* Gamma<0 could destroy Q>=1 and the fixed-sign argument. The reviewed
  AC2q branch has positive gamma. Gamma=0 does not obstruct this particular
  measure lemma, unlike the earlier PF02 Legendre elimination.
* The lemma controls polarization current, not every nonlinear stress.
  For example a schematic amplitude epsilon^(-1/2) over width epsilon has
  vanishing linear current integral but finite quadratic stress integral.
  This is a scaling observation, not a constructed AC2q solution. Ruling
  out such stress concentration requires additional field equations and
  compactness estimates.

Consequently native polarization cannot provide an independently adjustable
surface storage charge in this finite-measure class. This does not imply
that all native layer stress is absent or that the remaining scalar/metric
mechanisms exist or are unique.

## Audit obligations and provenance

| Obligation | Verdict |
| --- | --- |
| Full-switch sign and temporal/normal domination | passed |
| Weighted P equation from the action | passed by direct differentiation |
| Weak limit and ordinary bulk subtraction | passed under local finite-measure bounds |
| No normal dipole implies zero polarization surface measure | passed for timelike interface |
| Flux continuity | conditional on no surface source and existence of traces |
| Arbitrarily fast temporal variations within this class | covered |
| All stress concentration or all weak continuations excluded | out of scope |

Independent delegated proof audit, 2026-11-06. No solver runs, external
theorems, or code changes. The decisive proof is the positive-measure
domination argument; no finite sampling is used as a substitute.

Input SHA-256 revisions at inspection:

    time_layer_review/REVIEW.md b571291f1874e227fd3aef34c386d99ea40fe63c678e0bbc0a61a1bed00c9f7b
    coupled/JUNCTION_RESULT.md 5f1e2582013d677f4fb69faa2af726ed9000ae8d5c6716cf6920ce35f9f895ec
    AC7_charge_switch/README.md 6627a35733c1700445d35e1dc1dc1125f6d1bc35e18d159ffe88b633f4d037e6
