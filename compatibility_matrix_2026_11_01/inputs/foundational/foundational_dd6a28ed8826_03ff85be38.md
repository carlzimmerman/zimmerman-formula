# PN28: a pressure mechanism with a finite-halo continuation

The physical normalization target remains open. The strongest constructive
result is a new, explicitly specified dispersion-coupled scalar model. It
transfers random-motion energy to a reciprocal field, and its reduced total
pressure interpolates from a polytropic outer region to a logarithmic dense
core. The reduced model has finite spherical halos and recovers the earlier
core-column coefficient in a controlled mathematical limit. Six computed
halos also survive when scalar gradients and their anisotropic stress are
included. This is a
conditional candidate branch; it does not establish the owner's cold-field
parent, universal acceleration coefficient, or successful observational fit.

Checkpoint PN28 starts at `66c45c5082f651dd54e171f98c11acd9cb3d9086`.
The shared repository advanced while this work ran. Actual source hashes,
rather than commit titles or arrival order, identify the inputs in INPUTS.json
and the route provenance files. All work is confined to this new directory.

## The constructive equation

Couple a dimensionless scalar s to the relative stream kinetic metric
Z(s)=exp(2s), and choose the positive convex potential

    U(s)=V+B[exp(3s)-3s-1],                 B>0.                (1)

V is a candidate vacuum baseline; B is independent. The form of this potential
and the specified one-level isotropic canonical waterbag are explicit model
assumptions. Neither is derived from the earlier cold-field action.

Minimizing the local energy K exp(-2s)+U(s), with canonical random energy
K=k rho^(5/3), gives the exact parametric equation of state

    rho/rho_* = y^(2/5)(y-1)^(3/5),
    P_ex = B ln y,                  y=exp(3s)>=1,
    rho_*=[3B/(2k)]^(3/5).                                  (2)

Here P_ex=P_total+V includes both the conjugate kinetic stress and scalar
potential stress. It differs from the bare kinetic pressure used in MC27.
At low density it tends to (2/3)k rho^(5/3); at high density it tends to
B ln(rho/rho_*). The logarithmic slope is positive everywhere in the matter:

    dP_total/dln rho = 5B(y-1)/(5y-2).                        (3)

The pressure is obtained by differentiating the complete energy, not by
declaring a logarithm to be the bare stream pressure. The choice of potential
still supplies the required shape. A positive exp(6s) deformation preserves
the vacuum and energy positivity but changes the dense EOS to a rho^(5/4)
power law. Therefore the logarithm is not yet protected by a physical principle.

The [action and exchange derivation](dispersion_coupling/REPORT.md) establishes
a positive non-gravitational Hamiltonian, homogeneous random-energy exchange,
and reciprocal energy export in a reduced outgoing-wave model. A separate
fluid-plus-scalar approximation has positive squared longitudinal frequencies
around the tested homogeneous no-gravity background, supported by its exact
positive Schur complement. It does not establish general kinetic or halo
stability. The [frozen EOS](dispersion_coupling/EOS.md) keeps these distinctions
explicit.

## The finite-halo result and its physical limit

An exact enthalpy variable psi puts (2) into the particularly simple form

    rho/rho_*=psi^(3/2)/(1-psi^(5/2)),
    h=(5B/(2rho_*))psi,                 0<=psi<1.              (4)

In the stated Newtonian local-scalar approximation, regular spherical halos
satisfy

    psi''+(2/r)psi'=-psi^(3/2)/(1-psi^(5/2)).                  (5)

The [proof](halo/DERIVATION.md) shows finite radius and mass for every
0<psi_c<1. It also proves the high-central-density limit

    Sigma_core=rho_c r_(1/4) -> xi_q sqrt(B/(4piG)),
    xi_q=5.84477267596... .                                   (6)

Seven finite profiles were computed, with independent mass integration and
three tolerance refinements. At rho_c/rho_*=3999.70 the dimensionless column
coefficient is 5.84351, about 0.0216% below the independently integrated
logotropic reference. These numerical cases supplement the analytic limit;
they are not its proof or a comparison with observations.

There is a material restriction: scalar gradients do not stay negligible as
the core density goes to infinity at fixed parent parameters. Their local
length-scale ratio grows approximately linearly with rho_c. Thus (6) is a
mathematical limit of the reduced model. Physical use requires a finite
parameter window, cold-particle energies B/rho_* much smaller than c^2, and
negligible cosmological force locally. The independent review reconstructs
the core limit and the omitted central gradient residual.

The [finite-gradient continuation](finite_gradient/DERIVATION.md) goes beyond
that approximation. Variation of the full static excess energy gives

    n=exp(3s) psi_+^(3/2),
    Delta psi=-n,
    epsilon Delta s=exp(3s)(1-psi_+^(5/2))-1,                 (6a)

where n=rho/rho_*, epsilon=C_s/(3B ell^2), and
ell^2=5B/(8piG rho_*^2). An energy-cutoff waterbag supplies a stationary
kinetic interior. Its vacuum continuation is explicitly static; the parent
does not yet define general dynamical variations through zero density.
Conditional on a regular decaying solution, a maximum-principle bound on s
and the Poisson equation prove that its matter radius is finite. The scalar
tail extends beyond that edge.

Six numerical solutions cover psi_c={0.8,0.95,0.99} and
epsilon={0.0001,0.01}. Independent mass and scalar integrals, the complete
radial stress balance, and the virial identity pass their prescribed checks.
Maximum mass error is 7.90e-9 relative; the force residual is 7.44e-8 after
the stated global scaling. Two joint domain/tolerance refinements at
psi_c=0.99 change the reported observables by at most 6.82e-9 fractionally.
These are floating-point diagnostics, not certified error bounds. The
endpoint spline-curvature diagnostic remains unverified and is explicitly
excluded from the accuracy claims.

A useful finite observation is that at fixed psi_c=0.99, increasing epsilon
by a factor of 100 lowers n_c from 35.9183 to 11.9251, while the dimensionless
quarter-density column changes from 5.74673 to 5.81785, only 1.24%. This is
evidence for a relatively insensitive column in those two cases; it is not
a universal law or a comparison at fixed mass. The
[independent review](relativistic_mixing/REVIEW_FINITE_GRADIENT.md) checks the
equations, boundary treatment, conservation identities and exact tested range.

## What this says about an acceleration formula

With canonical scalar phi=F s and coupling g=1/F, the chosen potential has
curvature m_phi^2=U_phiphi(0)=9g^2 B. Thus the constructive branch gives

    B=m_phi^2/(9g^2).                                        (7)

m_phi^2 here names the canonical potential curvature in the action's field
units; it must not be read as an SI particle mass squared without conversion.
Combining (6) with the framework's separately adopted core-column
identification Sigma_core=a0/(2piG) gives the conditional bridge

    a0^2 = pi xi_q^2 G m_phi^2/(9g^2).                       (8)

This exposes a concrete physical candidate: the acceleration scale can depend
on the field's stiffness and its coupling to velocity dispersion. To recover
the proposed a0=(1/2)c sqrt(G rho_Lambda), the remaining selection requirement
is m_phi^2/(g^2 V)=9/(4pi xi_q^2), with V=rho_Lambda c^2. No argument here fixes
that ratio. The action allows B to change at fixed V, and the waterbag's phase
level still supplies rho_*.

Equation (8) therefore is not a newly predicted constant, nor a derivation of
the full observed acceleration relation. It is a conditional link between a
specific conserving model and the adopted phenomenological target.

## Other routes sharpened the target

| Route | Substantive result | Scope and remaining implication |
|---|---|---|
| [Transport](transport/DERIVATION.md) | Ordinary positive Fourier conduction cannot preserve the MC27 log closure during homogeneous compression or expansion; exact cooling profile and integrated power derived. | Instantaneous isotropic fixed-EOS test. Nonlocal transport and changed stress remain open. |
| [Reservoir](reservoir/DERIVATION.md) | Reciprocal constant-w energy equation solved; local vacuum closure has c_sound^2=5c^2(A-p)/(2rho c^2+5p), negative in the dense core p>A. | Fixed-parameter, zero-flux, local total perfect-fluid closure; not all interacting-vacuum models. |
| [Relativistic mixing](relativistic_mixing/RESULT.md) | Exact normalization A_mix=K/ln[Z(t_min)/Z(t_max)]; the NR near-match falls to 0.518–0.531 of the target in the three explicit broad-span controls. | The controls retain unproved energy and phase-span maps. A_mix is not automatically a spatial log coefficient. |
| Relativistic spatial extension | A static all-hot mixture gives P proportional to n^(4/3), despite its momentum power tail. | Prescribed static spacetime, finite global phase span. Massive self-gravitating mixtures remain open. |
| [Recent diffusion correspondence](reservoir/SOURCES.md) | A September 2026 source rewrites an assumed cosmological log fluid as a diffusion law. | Exact background dictionary; it supplies neither this kinetic closure nor an independent A/V. |

The recent diffusion source is [Cruz and Lepe, arXiv:2609.21006v1](https://arxiv.org/html/2609.21006v1).
Its assumptions and density/rate conventions were checked explicitly. The
general obligation to retain vacuum momentum transfer is known from
[Wands, De-Santiago and Wang, arXiv:1203.6776v2](https://arxiv.org/pdf/1203.6776v2).
No claim of worldwide novelty is made for the calculations here.

## Evidence and remaining physical work

The finite run records and independent reconstruction reports are collected
in VERIFICATION.json. They distinguish completed finite computations from
analytic proofs, conditional source transfers, and unresolved physical claims.
Two initial serialization failures are preserved; their successful replacements
change Boolean serialization rather than mathematical acceptance criteria.
An intermediate reservoir run was superseded after the written domain
qualifications were corrected during review.

The next decisive physical work is an origin for the chosen potential and
phase-space state, plus a mechanism selecting its stiffness relative to the
gravitating vacuum. Conserving kinetic formation and the model's empirical
tests are additional requirements. The earlier theory's observational passes
cannot be imported into this changed stress model.

The normalization objective is not closed. The useful advance is an explicit
energy-exchanging candidate with a derived reduced pressure law, finite-halo
theorems, and clearly exposed parameters and restrictions. The continuation
contract is in HANDOFF.md.
