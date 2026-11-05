# Induced-gravity matching from the shared condensate

This explicit changed construction links the condensate to the gravitational
coupling and gives a joint algebraic matching formula. It does not select the
coefficient. Its scalar-tensor vacuum can have positive energy and a positive
amplitude mass, but the clock/polarization constraints and full health remain
untested. This is an alternative to, not an already unified implementation of,
SEQUESTER_RESULT.md. The earlier offset cancellation cannot be imported into
this changed gravitational action without rederiving its global constraints.

## Specified action terms

Use c=hbar=1 and minimally coupled Jordan-frame matter. Define

    F=xi(sigma^2+zeta p^2),
    U=U0-t(sigma^2+p^2)/2+A h^3(sigma^2+p^2)^(3/2)/3+B h^3 p^3/3,
    L_scalar_tensor=F R/2-Z(grad sigma)^2/2-U.

A,B,t,h,xi,Z are positive, sigma>0 and p>=0. U0 is an independent constant.
The two frozen options are zeta=0 and zeta=1. In this modified model h couples
to the whole radial spectral mass; the amplitude kinetic term defines its
field normalization. This is a changed set of physical assumptions, not a
claim that a field redefinition fixes a formerly free coupling.

At a homogeneous p=0 vacuum, set F0=xi sigma0^2 and
x=A h^3 sigma0/t. The scalar and Einstein equations are

    U_sigma=F_sigma R/2, R=4U/F.

They imply

    U0=t sigma0^2(3-x)/12,
    U_vac=t sigma0^2(x-1)/4,
    H^2=t(x-1)/(12xi).

This solves stationarity but retains x as vacuum data. It does not justify
choosing U0 to obtain a desired normalization.

## Scalar-metric mixing and the actual amplitude mass

Under g_E=(F/F0)g, the amplitude kinetic coefficient is

    K_E=F0[Z/F+(3/2)(F_sigma/F)^2].

At the vacuum K_E=Z+6xi, not Z. The mass calculated from the Einstein-frame
potential F0^2 U/F^2 is

    m_sigma^2=t(2-x)/(Z+6xi).

Thus the positive-energy, positive-amplitude-mass domain is1<x<2. This
qualifies only the scalar-tensor homogeneous subsector. It is not a complete
ghost/gradient/nonlinear health result for a polarized gravity theory.

Matter couples to the amplitude in the Einstein frame, with squared
dimensionless scalar charge alpha^2=xi/(Z+6xi). Therefore one cannot simply
identify the tensor coupling with the measured Newton constant at all radii.
The local force dictionary below uses

    G=1/(8pi F0), K=4pi G=1/(2F0)

only in a regime where scalar exchange is suppressed. A necessary scale
window for that reading is m_sigma r>>1 and Hr<<1, requiring

    m_sigma^2/H^2=12xi(2-x)/[(Z+6xi)(x-1)] >>1.

The formula exhibits such a possible hierarchy near x=1; a physical sourced
solution in that window has not been constructed.

## Curvature and the infrared force term

At fixed background curvature the stationary amplitude obeys

    sqrt(sigma^2+p^2)=(t+xi R)/(A h^3).

Ignoring amplitude derivatives only in this stationary matching, substitution
into U-FR/2 gives

    U_eff,R=U0-(t+xi R)^3/(6A^2 h^6)
             +xi R(1-zeta)p^2/2+B h^3 p^3/3.

The induced quadratic coefficient is therefore delta_curv=xi R(1-zeta).
For zeta=0 and a positive-curvature vacuum it is positive: the strict
infrared response is linear, with a possible intermediate MOND regime.
For zeta=1 it vanishes at tree level, while C3=B h^3 remains nonzero.

The second option is a concrete tree-level cancellation, not a demonstrated
quantum protection mechanism. The B p^3 sector distinguishes the polarization
from the amplitude, so the radial form of F and the other potential terms
does not establish a symmetry of the whole action. Independent p^2 and
curvature operators remain to be controlled. The nonminimal vector-curvature
coupling may also affect the full constraint structure, not computed here.

The local leading response assumes a held homogeneous background, negligible
screening, small metric potentials and controlled amplitude derivatives.
Source-induced scalar and curvature perturbations require an additional
calculation; fixed-curvature elimination is not a full metric-source solve.

## Joint normalization and the remaining dimensionless parameters

On the zeta=1 tree-level critical slice in the above local regime,

    a_MOND=1/(K B h^3).

Let r_B=B/A and theta=t/F0. Eliminating the condensate value in favor of
the tensor gravitational coefficient gives

    kappa^2=a_MOND^2/(G U_vac)
           =128pi/[r_B^2 x^2 theta^3(x-1)].

Even granting the stronger equal-amplitude hypothesis B=A leaves x and
theta. Stability supplies the interval1<x<2, not one value in it. As an
additional analytic bound, x^2(x-1)<4 on that interval, so
kappa^2>32pi/(r_B^2 theta^3). This is a conditional bound, not a prediction:
theta and r_B have not been fixed by the model.

The small-vacuum hierarchy is also informative. Define the symbolic ratio
epsilon=U_vac/F0^2>0. Then

    epsilon=theta(x-1)/(4xi),
    kappa^2=32pi/[r_B^2 x^2 xi epsilon theta^2].

At fixed finite positive theta,xi,r_B, letting epsilon tend to zero drives
x to1 and kappa^2 proportional to1/epsilon. The construction does not
automatically track a_MOND proportional to sqrt(G U_vac) along that family.
With xi and r_B fixed, one way to keep kappa finite is
theta=c/sqrt(epsilon), where c>0 remains an unfixed dimensionless amplitude.
In that limit

    kappa^2 ->32pi/(r_B^2 xi c^2),
    m_sigma^2/F0 ~ c/[(Z+6xi)sqrt(epsilon)].

For fixed finite Z and xi, the canonical amplitude then becomes parametrically
heavier than the background Planck scale. That limit is not a controlled
low-energy gravity explanation without an additional UV argument. Varying
Z,xi or r_B with epsilon changes this conclusion and introduces further
matching hypotheses; those possibilities are not excluded. No observed
cosmological number was inserted in this hierarchy calculation.

## Evidence and disposition

induced.py passes18 exact checks. Omitting the curvature contribution to
the polarization response fails precisely the full-coefficient and
zeta=1 cancellation checks. The successful and negative-control evidence
have separate validated manifests. Scalar-metric mixing, local Newtonian
calibration, fixed-curvature versus full-source matching, and independent
dimensionless parameters were kept explicit. Self-review only.

The changed construction establishes a joint formula and a tree-level
cancellation option. It does not provide the missing microscopic identity
fixing r_B,x,theta, protect criticality, or fix U0. Further precision on this
algebra cannot change that. A positive continuation needs an actual symmetry
or interaction determining these dimensionless data and its quantum/physical
matching, rather than setting them to make the coefficient come out correctly.
The goal remains open and no action is adopted.
