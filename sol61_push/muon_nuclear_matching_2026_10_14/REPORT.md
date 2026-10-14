# Muon-loop matching preserves the conditional Coulomb wall

2026-10-14. Parent checkpoint: 02bce160b4947d33a6d5630855655c5d0c80dbf5.

A specified one-muon-loop completion reduces the preceding uniform-nucleus
Coulomb response by 2.835%, rather than suppressing it by orders of magnitude.
The stronger assigned barrier becomes 4.97e-7 eV. This resolves the constant
photon-coefficient extrapolation for this particular loop and nuclear model.
It does not establish the full material scalar charge, empirically allowed
particles, or creation into confined modes.

## Specify the microscopic and renormalization assumptions

Take L_int=-y_mu R mubar mu, so m_mu(R)=m_mu+y_mu R. Hold the high-scale
matching parameters fixed under that variation. Do not impose an additional
independent RF^2 interaction that cancels the threshold contribution. In the
convention L_photon=-(1+gR)F^2/4, the soft one-loop coefficient is

    g(0)=-2 alpha y_mu/(3pi m_mu).

The desired positive g(0)=1e-20/eV therefore corresponds to

    y_mu=-6.82306850e-10, m_mu=105658375.5 eV.

Earlier source reports used magnitudes for widths; the signed choice here
selects the repulsive Coulomb-wall branch for positive carrier coupling mu.
This is a low-energy Yukawa model, not an electroweak completion. Independent
scalar-electron, scalar-quark and scalar-gluon matching contributions remain
separate obligations. Setting them to zero at one matching scale is not proof
that they remain absent under running.

A change of subtraction convention cannot physically remove the induced
coupling. If the vacuum polarization is subtracted at zero momentum with an
R-dependent mass, its matching term must also be differentiated. Holding the
low-energy alpha fixed for every R instead would change the model's physical
response. This calculation retains the threshold term normalized by g(0).

## Soft scalar insertion with spacelike photon momentum

The material background has scalar momentum of order eV, negligible relative
to m_mu. The photons inside nuclear Coulomb energy can have much larger
spacelike momentum Q. At zero scalar momentum, differentiate the muon vacuum
polarization with respect to its mass. The relevant mass dependence is

    integral_0^1 dx x(1-x) ln[m_mu(R)^2+Q^2 x(1-x)].

After normalization to Q=0, the coefficient ratio is

    f(r)=g(Q)/g(0)=6 integral_0^1 dx x(1-x)/[1+r^2 x(1-x)],
    r=Q/m_mu.

Equivalently, for r>0,

    f(r)=6/r^2 * [1-4 atanh(r/sqrt(4+r^2))/(r sqrt(4+r^2))].

Its continuous value at r=0 is one. It is positive, at most one, and has small-r
expansion 1-r^2/5+O(r^4). This is a two-spacelike-photon, soft-scalar matching
calculation; it is not the timelike on-shell two-photon decay form factor.

Kniehl and Spira, [Low-Energy Theorems in Higgs Physics,
hep-ph/9505225v1](https://arxiv.org/pdf/hep-ph/9505225), section 2.1, Eqs. (1)-(2),
checked 2026-10-14, justify generating a soft scalar insertion through a mass
variation and specify differentiation before renormalization with other bare
couplings held fixed. The spacelike parameter integral and its nuclear weighting
are given explicitly here; that paper is not evidence for this new scalar.

## Weight the coefficient with the actual modeled Coulomb momenta

For the preceding uniform nuclear distribution, put x=Q R_N and

    F_charge(x)=3 j_1(x)/x,
    b=m_mu R_N=3.80621938.

The Coulomb pair energy is proportional to integral dQ F_charge(QR_N)^2.
Consequently the correction is the weighted integral

    ratio = integral_0^infinity dx F_charge(x)^2 f(x/b)
            / integral_0^infinity dx F_charge(x)^2,
    denominator = 3pi/5.

This replaces evaluating the loop at one nominal momentum. The radius and
pair-energy model, including its Z(Z-1) approximation, are inherited without
claiming a more accurate nuclear distribution. The scalar varies on a scale
much larger than the nucleus, so neglecting its eV-scale momentum in this
muon-loop insertion is distinct from neglecting the nuclear photon momenta.

A useful analytic cross-check follows from positivity and Jensen's inequality.
The normalized Feynman weight 6u, u=x(1-x), has mean u=1/5. The normalized
nuclear momentum weight has mean (Q R_N)^2=5/2. The latter follows from
Parseval for a normalized uniform sphere: integral x^2 F_charge(x)^2 dx=3pi/2.
Thus

    1/[1+1/(2b^2)] <= ratio <= 1,
    lower bound = 0.966638434.

This bound is for the specified uniform charge distribution and loop. It is
not a universal lower bound on arbitrary material scalar response.

## Result and numerical controls

The calculated ratio is 0.9716517483, yielding

    matched Coulomb pair response energy = 784.40 MeV,
    stronger barrier (lambda_rep=1e-6) = 4.9704e-7 eV,
    weaker barrier (lambda_rep=1e-15) = 1.5718e-11 eV.

The stronger case remains above the chosen 1e-8 eV carrier energy limit and
above the preceding centimetre-sphere localization threshold. The weaker case
remains below both. The reduced Coulomb response does not resolve source decay
distance, reciprocal scattering, or loading into a finite cavity.

Nineteen bounded checks pass: parameter-integral versus closed-form matching,
60-decimal mass derivatives, nuclear normalization, radial cutoff refinement,
and high-momentum precision controls. Integrals stop at dimensionless radial
cutoffs 200 and 400. Since |sin x-x cos x|<=1+x and 0<f<=1, the omitted tail
is bounded by

    9[1/(3L^3)+1/(2L^4)+1/(5L^5)].

At L=400 this bounds the omitted contribution to the ratio by 2.50e-8. It is
a truncation bound only, not a rigorous bound on floating-point quadrature or
nuclear-model errors. The two radial evaluations differ by 1.27e-10.

Initial preflight Gauss quadratures did not meet high-Q refinement tolerances
because the Feynman-parameter integrand develops narrow endpoint structure.
The authoritative calculation uses the analytic expression above for r>0.1,
checked against 60-decimal values, and a 256-node integral at smaller r to
avoid subtractive cancellation. The reported run uses this corrected method.
No failed preflight is counted as passing evidence.

## Remaining physical gap and next work

This is one controlled contribution to nuclear matching, not the whole atom.
It still omits proton/neutron electromagnetic mass sensitivities, electron
binding and mass terms, nuclear correlations, other induced scalar operators,
and a global constraint analysis of the eV mediator. The optical g value and
the particle masses remain assumptions. A fitted nuclear radius does not
validate those assumptions.

The wall candidate now has an explicit soft-scalar/spacelike-photon completion
rather than an unchanged optical coefficient imposed at nuclear momentum.
The next distinct preparation calculation is the source overlap with finite
cavity pair modes and the competing escape/recombination channels, keeping this
wall contribution conditional until the full material response is established.

Reproduce:

    python3 sol61_push/muon_nuclear_matching_2026_10_14/check.py /tmp/muon_nuclear_results.json

The manifest pins the prior wall data and executable code. This is self-review,
not a Lean or empirical certificate. The full creation-and-capture goal remains
open.
