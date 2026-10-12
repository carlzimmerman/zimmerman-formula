# Polarization selector: useful effective target, missing microscopic origin

[Blanchet and Le Tiec, Dipolar Dark Matter and Dark Energy, v2](https://arxiv.org/html/0901.3114v2),
sections II-III, gives a conserved-current dipolar-fluid action. Its MOND
limit assumes weak clustering and nearly static polarization. The authors
explicitly describe the potential coefficients as phenomenological. This
is an alternative effective matter model, not a derivation from our scalar
carrier. Search scope was this primary paper and the abstract of its 2008
predecessor; no current empirical-viability claim is made.

## Independent coefficient audit

Declare an aligned spherical constitutive model with negligible monopole
source density. Let Pi be polarization magnitude and C=4 pi G. Set

    W(Pi)=W0+(A/2)Pi^2+(B/3)Pi^3,
    g=W'(Pi)=A Pi+B Pi^2,
    gN=g-C Pi=(A-C)Pi+B Pi^2.

Deep square-root force scaling requires A=C and B=C^2/a0. Then

    p=C Pi/a0, gN/a0=p^2, g/a0=p+p^2,
    g=gN+sqrt(a0 gN).

These equations specify a constitutive target. They do not prove dynamic
formation, stability or a microscopic action for the protected carrier.

Perturb A=C(1+e), keeping B fixed. The dimensionless equations become

    y=gN/a0=e p+p^2, g/a0=(1+e)p+p^2.

For any e>0, at y much smaller than e^2 the force becomes linear in gN,
with enhancement (1+e)/e, rather than proportional to sqrt(gN). The critical
quadratic coefficient must therefore be explained or protected; merely
choosing it to produce the target is not a derivation. The finite audit
checks e=0,1e-4,0.01,0.1 and y=1e-10 through 0.01. All 25 checks pass.

W0 drops out of both constitutive equations. Adding any positive constant
to W changes the vacuum density without changing a0. In SI units the repo's
specific relation a0=(1/2)c sqrt(G rho_DE), with W0=rho_DE c^2, would require

    G W0/a0^2=4.

Neither the response equations nor current conservation enforce this
identity. Multiplying W0 by four at fixed A,B leaves a0 unchanged and
changes inferred kappa from 1/2 to 1/4. This explicit parameter variation
separates dimensional resemblance from the requested exact coefficient.

## Microscopic gates for the existing carrier

An ordinary localized bound pair of positive Newtonian masses has positions
R+x_i relative to its center of mass, satisfying sum_i m_i x_i=0. Expanding
its external gravitational energy gives

    sum_i m_i Phi(R+x_i)
      = M Phi(R) + (sum_i m_i x_i) dot grad Phi(R)
        + (1/2) sum_i m_i x_i^a x_i^b partial_a partial_b Phi(R) + ... .

Its internal gravitational dipole term vanishes identically. Its leading
internal response is tidal. Binding our daughter/source particles into an
ordinary molecule therefore does not create a polarization coupling linear
in a spatially uniform gravitational field. Additional internal dynamics
or nonminimal couplings would have to be specified; the effective dipolar
fluid is not automatically such a molecule.

There is also an analyticity gate. If an isotropic local medium has an
analytic energy in Cartesian polarization components near zero, and all
eliminated internal variables have a nonsingular positive Hessian, their
smooth analytic stationary solution leaves an energy analytic in Pi^2.
Its expansion contains Pi^2, Pi^4, ... . The required |Pi|^3 term is not
analytic there. This argument only applies under those local, analytic,
gapped assumptions. A critical state, gapless modes, a nonlocal response
or nonanalytic microscopic interaction could evade it, but would require
an explicit derivation and stability check.

The useful output is a precise target for further construction: an internal
response that evades the ordinary dipole cancellation, explains critical
quadratic response and a cubic norm term, and links its coefficient to the
vacuum offset. None has been derived from the current protected carrier.

Evidence: `polarization_selector.py`, its contract and
`polarization_selector_run/results.json`; the run manifest validates against
current files. The finite arithmetic checks do not establish the analytic
microscopic gates or a full dipolar field theory.
