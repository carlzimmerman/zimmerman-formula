# A fixed-flux vacuum portal that preserves the charged production model

Status: an explicit classical, tree-level extension with a nonpropagating
four-form. It gives a vacuum-flux-dependent carrier mass and retains the
positive charged potential. It does not derive a halo selector, flux value,
cosmic abundance, or the required acceleration law.

## Research question and declared extension

The curvature audit showed that inferring vacuum energy from local geometry
mixes in matter pressure. An alternative is to include an explicit vacuum
sector. This is additional physics, not a property already derived from
the repo. The research probe is whether that sector can couple to the
carrier without breaking charge or destabilizing its potential.

In four spacetime dimensions, introduce a three-form gauge potential A_3,
F_4=dA_3, with no membranes or other charged sources. Use signature -+++
and natural units. Add to canonical scalar and Einstein terms

    L_4 = - Z(S) F_abcd F^abcd/(2*4!),
    S = |phi|^2+4|chi|^2,
    Z(S) = 1/(1+alpha S/mu^2),   alpha>=0, mu>0.

The scalar potential before eliminating F is

    V_0=m_0^2 S+|sqrt(Delta) chi+(g/sqrt(Delta)) phi^2|^2
        +lambda_rep |phi|^4,

with m_0^2>=0, Delta>0 and lambda_rep>=0. The charges of phi and chi are
1 and 2. S and every displayed interaction are U(1)-invariant. Z is smooth
and strictly positive at finite field values. No curvature invariant or
matter-pressure estimator appears in this coupling.

Four-form flux potentials with scalar-dependent kinetic coefficients are
established constructions; for related primary-source context see
[Herráez et al., arXiv:1802.05771](https://arxiv.org/pdf/1802.05771),
particularly the inverse four-form metric in equation (7.1). That work is
not evidence for this specific carrier coupling or a halo mechanism. The
single-field reduction and normalization used here are derived below.

## Fixed-flux reduction and the sign

Write F_abcd=f epsilon_abcd, so F^2=-4! f^2. The gauge equation gives

    d(Z *F)=0,   or Z f=q,

up to the orientation convention absorbed into constant q. In a connected
region without membrane sources, q is constant. There is no local
propagating four-form mode. The local energy density is

    H_4=Z f^2/2=q^2/(2Z).

Simply substituting f=q/Z into the unreduced Lagrangian gives the wrong
sign for an effective scalar potential. The fixed-flux variational problem
requires the corresponding boundary/Legendre term. In a local electric
coordinate the momentum is q=Z f, so the Routhian is

    L_4-q f=-q^2/(2Z).

Thus the correct reduced potential contribution is positive:

    V_4=q^2/(2Z)=epsilon_v [1+alpha S/mu^2],
    epsilon_v=q^2/2.

The same sign follows from the original scalar equation: its four-form
force contains (Z_S/2)f^2, equal to -partial_S[q^2/(2Z)] at fixed q.
This fixes the reduction without treating a substituted on-shell action
as an unconstrained variation.

## Exact matching and retained cold-energy bound

After subtracting the constant background epsilon_v,

    V_eff-epsilon_v=m_eff^2 S
       +|sqrt(Delta) chi+(g/sqrt(Delta)) phi^2|^2
       +lambda_rep |phi|^4,
    m_eff^2=m_0^2+alpha epsilon_v/mu^2.

The source mass obeys M_eff^2=4m_eff^2+Delta. The positive square, quartic
coefficient and mass-squared gap Delta are unchanged. On a fixed flat
background with absent surface fluxes, the earlier completed-square proof
therefore gives

    E_material >= m_eff |Q|.

Here E_material includes the field-dependent four-form energy and subtracts
only the homogeneous epsilon_v background. It is not the scalar-only bare
energy. This statement is classical; it does not establish a renormalized
quantum bound or a global positive-energy theorem for self-gravitating
spacetimes. The full gravity calculation must include the vacuum stress.

A circular source has the same formula

    eta=1-2m_eff/M_eff,
    u_eff^2=Delta/(4m_eff^2).

These are flux dependent unless parameters are matched at a specified q.
Near-threshold conversion and a repulsive threshold contact term can
therefore coexist with this portal at the classical level. The coefficient
4 in S is a declared alignment of the two mass shifts; no extra symmetry
protecting it against quantum corrections has been established.

For illustration, take epsilon_v corresponding to rho_v=6e-27 kg/m^3,
namely 2.586078319e-11 eV^4. With alpha=1, m_eff=1e-12 eV and half of
m_eff^2 supplied by the portal, choose

    m_0^2=m_eff^2/2,
    mu=7.191770740 MeV.

Then the reduced scalar potential is exactly the previously tested one
plus epsilon_v. This numerical example is a parameter match, not a
measurement or a prediction of the portal scale. If additional bare or
quantum vacuum contributions are present, the flux energy need not equal
the total observed dark-energy density; identifying the two is an explicit
assumption of this illustration.

## What this does and does not solve

It provides a mathematically explicit vacuum-sector coupling without the
Ricci-pressure contamination. The four-form responds algebraically to
scalar amplitudes, while its fixed flux determines the baseline vacuum
energy and part of the masses. The reduced scalar theory remains canonical
with a bounded potential. At this level there is no extra propagating mode
or higher-curvature metric equation introduced by this portal.

But in a fixed-q sector, all local scalar equations are exactly those of
the old theory with m replaced by m_eff. Matching m_eff, Delta, g and
lambda_rep reproduces the same local dynamics. There is no new spatial
force, target density or baryonic normalization that can select a halo.
Ordinary gravity from epsilon_v remains the outward vacuum contribution
already audited. Changing q across hypothetical sectors relates masses to
vacuum energy; it is not an evolution law selecting the observed sector.

The portal also does not create the initial source energy or charge. With
alpha>=0 and the displayed positive potential, its fixed-flux ground state
still has zero scalar fields. Production still needs the charged source or
preparation mechanism. No membranes, flux relaxation, tunneling calculation,
radiative stability or ultraviolet completion has been supplied. A mass
scale proportional to sqrt(epsilon_v) is not itself an acceleration law;
additional constants and dynamics would be needed to turn it into the
repo's a0 with its specified coefficient.

## Evidence and decision

four_form_portal.py uses exact rational checks for the fixed-flux
Hamiltonian, Routhian sign, scalar mass identity and unchanged gap, then
checks the illustrative unit conversion and parameter match. All 40 checks
pass; the run manifest validates provenance. The general identities are
algebraic derivations, not conclusions inferred from the sampled values.
The proof and interpretation are self-reviewed.

The preceding turn made progress by identifying limitations of curvature
reconstruction. This turn supplies an explicit alternative action that
survives the classical energy/charge checks. The local equivalence result
also sets a clear limit: this affine portal cannot be advertised as the
missing halo selector. Any further vacuum-mediated stress or baryonic
response must be present in an action and tested, not inserted as a desired
density profile. The full cold-energy objective remains incomplete.
