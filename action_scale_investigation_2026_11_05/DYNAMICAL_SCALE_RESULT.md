# Making the coefficient dynamical does not yet select it

This is an exact obstruction for the minimal canonical, monotone promotion
specified in DYNAMICAL_SCALE_CONTRACT.md. It is not a no-go for arbitrary
new scalar potentials, derivative operators, or microscopic completions.
It extends the auxiliary-field calculation in DERIVATION.md by keeping
time evolution and gravitational backreaction.

## Exact homogeneous solution and retained memory

Write the FRW scale factor as A, use c=1 and M^2=1/(8pi G), and add a
canonical field chi. Let the polarization scale be

    a = a_ref(phi,X) exp(chi/f), f>0.

Take the clock scalar potential to be V0>0 and include no chi potential.
On the exact P=0 branch the polarization terms and their first variations
vanish. The two canonical momenta and Friedmann equation are therefore

    Q_phi=A^3 phi_dot, Q_chi=A^3 chi_dot,
    C=Q_phi^2+Q_chi^2>0,
    3 M^2 H^2=V0+C/(2 A^6).

Q_phi is nonzero so the normalized phi clock is defined at every finite A.
This includes the chi energy in the metric equation; it is not a test-field
calculation on a prescribed de Sitter background.

Set x=A^3, d=sqrt(C/(2V0)), alpha=sqrt(3V0)/M. On the expanding branch

    x_dot=alpha sqrt(x^2+d^2),
    chi(x)=chi_i+Q_chi/(alpha d) [asinh(d/x_i)-asinh(d/x)].

Direct differentiation gives x chi_dot=Q_chi and the initial value chi_i.
The late-time limit is finite:

    chi_infinity = chi_i + sqrt(2/3) M Q_chi/sqrt(C)
                                  * asinh[sqrt(C/(2V0))/A_i^3].

In particular partial chi_infinity/partial chi_i=1. Holding both initial
velocities, A_i and V0 fixed while varying chi_i leaves the entire homogeneous
geometry, density and clock history unchanged, but multiplies the local
constitutive acceleration scale by exp(delta chi_i/f). Hubble damping
selects zero velocity, not one field value or one coefficient. There is a
continuum of asymptotic values; this is not attraction to a unique value.

This statement holds already at any finite A. We do not claim that the
formal endpoint X_phi=0 has a well-defined normalized clock. Nor do we
equate the frozen local constitutive scale with a complete measured galaxy
response after chi gradients and gravitational backreaction are included.
The symbolic check labelled operational-scale sensitivity uses only this
conditional local scale definition; no sourced force law was solved here.

## Polarization supplies a signed drive, not an equilibrium

For the original kernel at fixed p, set s=p/(a-p) and

    h(s)=s+s/(1+s)-2log(1+s),
    h(0)=0, h'(s)=s^2/(1+s)^2>0 for s>0.

Then

    W_a=-a h(s)/K,
    W_chi=-a^2 h(s)/(K f)<0 for 0<p<a.

The canonical equation is Box chi-W_chi=0. In a spatially homogeneous
description its source is -W_chi, of positive sign; nonzero polarization
cannot create a finite stationary point of this local kernel. This sign
statement does not assume that homogeneous nonzero spatial polarization
is an isotropic cosmological solution. It is a statement about the local
force in the field equation.

There is also a covariant static obstruction. On any regular static domain
with metric -N^2 dt^2+h_ij dx^i dx^j, N>0, and time-independent chi,

    partial_i(N sqrt(h) h^{ij} partial_j chi)
        =N sqrt(h) W_chi.

Integrating gives the exact weighted boundary-flux identity

    integral_boundary N n^i partial_i chi dSigma
        = integral_domain N W_chi dVolume.

If total flux through all boundaries is zero, the right side is strictly
negative whenever 0<p<a on a set of positive volume. No such regular static
solution exists in this class. This covers compact boundaryless domains
and zero-flux boundary conditions, not an exterior with nonzero scalar
charge, horizon boundaries, singular cores or time-dependent chi. In an
exterior, a negative outgoing flux can balance the drive and is allowed.
The identity does not rule out those charged solutions.

The same sign argument holds for any differentiable scale map with a_chi>0
throughout the domain. A turning point in that map, chi-dependent stiffness,
or new potential changes the equation and lies outside this result.

## What an added potential would have to do

Adding -U(chi) changes the equation to Box chi=U_chi+W_chi. A homogeneous
P=0 stationary field then obeys U_chi=0; a suitable positive curvature can
make a chosen minimum attractive. But its position is new physical input.
The family U_mu(chi)=U0+m_chi^2(chi-mu)^2/2 illustrates the freedom: for any
mu, the same vacuum energy U0 and local curvature m_chi^2 coexist with a
different scale exp(mu/f). This example illustrates nonselection; it is
not a proposed microscopic potential or a full-health proof.

Even selecting chi does not protect the relation to total vacuum energy:
an independent constant in U changes the gravitating density without
changing U_chi. A portal that explicitly includes that shifted density is
another matching assumption, and still leaves the selected dimensionless
response coefficient to explain. The missing input is a justified relation
between the selector potential, gravitating vacuum energy, and nonlinear
response coefficient, as identified in NORMALIZATION_RESULT.md.

## Evidence and audit

Thirteen exact symbolic identities pass in evidence/dynamical_scale. The
deliberate omission of chi_i fails exactly the initial-offset and scale-
sensitivity checks in evidence/dynamical_scale_mutate. No numerical fit,
physical source calculation, or coefficient input was used.

Self-review checks: fixed-p derivative; scalar Euler-Lagrange sign;
backreaction from both kinetic energies; expanding-branch integration;
initial and asymptotic values; positive lapse and all boundary components;
strict versus zero polarization; finite-time clock domain; local scale
versus solved force law. Verdict: proved for the stated promotion and
boundary class. No independent audit or universal impossibility claim.
