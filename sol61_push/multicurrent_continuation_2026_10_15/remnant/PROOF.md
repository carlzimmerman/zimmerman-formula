# Unequal charge ratios force separation in the prescribed halo comparison

Claim MC-REMNANT-001. Conditional analytic result for the specified Newtonian test-particle model, with symbolic and finite quadrature checks. This extends the finite-supply carrier work calculation retained in [the predecessor snapshot](../inputs/CARRIER_EXPORT_RESULT.txt); it does not derive a physical conversion rate or a live multi-species halo.

## Model and domain

Use G=M_b=a0=1. A fixed positive point baryon attracts a pressureless positive chi population. Its assigned charge-to-mass ratio is zeta=sqrt(4 pi G); its gauge response is D=E/(1+E/D0), D0=a0/zeta. Field energy, stiffness, pressure, metric corrections and backreaction from the test remnant are omitted. All radii considered are strictly positive.

Let s>0 be the finite chi rest-mass supply in baryon-mass units. Inside its support, the selected cold equilibrium is

\[
 u_0(r)={\sqrt{1+4r^2}-1\over2r^2},\qquad
 g(r)={1\over r^2}+u_0(r),\qquad
 {u_0^2\over1-u_0}={1\over r^2}.
\]

Here u0 is the chi contribution to gravitational acceleration. Its enclosed mass is r²u0, and the electric force per chi mass is zeta E=u0/(1-u0)=g. The finite-support edge obeys

\[
 R_e^2=s+s^2,\qquad u_0(R_e)={1\over1+s}.
\]

For the exterior force-law comparison, keep the same scalar electric constitutive relation in a prescribed rest chart. Enclosed chi mass and charge remain s, while the baryon remains 1. Gauss law then gives zeta E=s/(r²-s); no infinite MOND tail is inserted. Since Re>sqrt(s), this assigned exterior field never reaches its constitutive pole.

**Exterior assumption:** the original RTM material frame is built from a nonzero timelike carrier current. That frame is undefined in the vacuum outside this finite halo. Neither RTM nor this calculation derives the assigned scalar continuation as a healthy vacuum action or a matched interface. The exterior escape statements below belong to this additionally specified force-law comparison; the interior impossibility of unequal pressureless species both resting together does not depend on that exterior.

A dilute same-sign remnant has beta=(q_S/m_S)/(q_chi/m_chi)>0 and is coupled minimally to that electric field. At zero background magnetic field the material-frame magnetic term has vanishing first variation. For the radial test motion used here, boosts parallel to the electric field do not produce a magnetic field, so the radial force is the ordinary assigned gravitational plus electric force in this comparison.

## Static coexistence obstruction

Two pressureless species at rest in a common nonzero electric and gravitational field require

\[
 g=\zeta_1 E=\zeta_2 E.
\]

Thus they cannot both be at rest with unequal charge-to-mass ratios. This is a two-dust equilibrium statement; it does not exclude pressure-supported, flowing, segregated or separately interacting populations.

For the test remnant on the pure-chi equilibrium specifically,

\[
 a_S(r)=(\beta-1)g(r),\qquad 0<r\le R_e.
\]

It starts accelerating outward when beta>1. Equal gauge charges with the supplied portal masses give beta=939.06542194. This assigned mass ordering is not evidence that such particles exist.

## Sufficient condition for radial escape

For r>=Re the exact prescribed-field acceleration is

\[
 a_S(r)=-{1+s\over r^2}+{\beta s\over r^2-s}
 ={[(\beta-1)s-1]r^2+s(1+s)\over r^2(r^2-s)}.
\]

Consequently aS in the assigned exterior comparison is strictly positive at every finite exterior radius if

\[
 (\beta-1)s\ge1.
\]

Equality also gives positive acceleration at every finite radius; the leading inverse-square coefficient then vanishes. This is a sufficient condition, not a necessary classification of all escape cases. For beta>1 and s>=1/(beta-1), a remnant released at rest at any r0 in (0,Re] moves outward, encounters no turning barrier and reaches unbounded radius within this prescribed continuation. Its finite asymptotic kinetic energy per unit remnant mass is the integrated outward work. At the assigned beta, the sufficient supply threshold is approximately 0.001066 baryon masses. Physical escape in RTM remains contingent on an actual vacuum/interface completion and reciprocal dynamics.

The original chi provides a different control: beta=1 gives zero interior force and exterior acceleration

\[
 a_\chi(r)={R_e^2-r^2\over r^2(r^2-s)}<0\quad(r>R_e).
\]

It is bound and is not ejected at rest by the same argument. The remnant effect is not a universal expulsion of the original medium.

## Exact escape work

Set

\[
 I(r)=\operatorname{asinh}(2r)
       -{1+\sqrt{1+4r^2}\over2r},\qquad I'(r)=g(r).
\]

For a remnant initially at rest at r0<=Re, the total outward work is

\[
 W_S(r_0)=(\beta-1)[I(R_e)-I(r_0)]
          +\beta\sqrt{s}\operatorname{atanh}{\sqrt{s}\over R_e}
          -{1+s\over R_e}.
\]

Whenever the trajectory reaches infinity, this equals one-half the squared asymptotic speed in the dimensionless Newtonian comparison. In particular, that conclusion holds under the sufficient escape conditions above. Otherwise W is a formal work integral and need not be the kinetic energy of an accessible final state; beta=1 gives the negative binding-energy control. An arbitrary initial kinetic energy must be added separately. There is no assumption that an actual portal creates a remnant at rest.

Restoring units, W is multiplied by V_f²=sqrt(G M_b a0) for specific energy, lengths by r_M=sqrt(G M_b/a0), and the predicted Newtonian speed is V_f sqrt(2W). A weak-field interpretation requires gravitational potentials and all particle speeds small compared with c. For a purely illustrative V_f=200 km/s, the nine checked cases give speeds 0.0318–0.0826 c. These are comparison outputs, not observational predictions or a relativistic-accuracy certificate.

The energy per remnant is m_S V_f² W. Since beta=m_chi/m_S for equal charges, reducing the remnant mass does not make its leading electric work per original conversion vanish: m_S beta=m_chi. A live conversion must supply that work through the changing gauge field, source, reaction products and gravity. The fixed-background test cannot assign the reciprocal source of this energy.

## What charge separation does and does not repair

One equal-charge remnant carries the original particle's full Gauss charge despite its small rest mass. If a fraction f of a chi mass stock M is replaced by such remnants, their rest mass is f M/beta but their charge-weighted source, in chi-mass units, is f M. Before they leave, their field source cannot be replaced by their rest mass. After they leave an aperture, the aperture's field source changes, and the original chi static profile is no longer an unchanged solution. Globally the exported charge still exists.

Thus the interior force establishes a tendency to separate rather than a justification for deleting remnants. The exterior comparison supplies a quantitative escape benchmark after a vacuum rule is chosen; it does not supply that physical rule. A new evolving solution must include the interface, charge flux, the original carrier's response, any baryons produced, pressure and field energy. No retained neutral cold population, hot/condensed source selection, abundance or halo formation law follows from this result.

## Reproduction and review scope

[check_remnant.py](check_remnant.py) checks twelve exact algebraic identities, the assigned mass-ratio interval and nine work-integral cases using 60-digit arithmetic. The independent numerical evaluation integrates the exterior in inverse radius, including its infinite interval. Supplies are s=1,5,20 and launch radii are 0.1,0.3,0.8 times Re. Maximum absolute quadrature difference is below 4.8e-58 in the recorded run. The all-radius sign claim follows from the displayed analytic numerator, not these samples.

The [run manifest](run_v1/manifest.json) records exact inputs, command, software, bounds and resource limits. It validates as a complete computation record. The theory-level conclusion is conditional on the stated fixed-background weak-field model; no physical carrier or full-theory closure is established.
