# Conversion cannot switch off the charge-aligned portal force

Status: local identities for arbitrary classical fields in the retained
leading NR theory. They do not assume a homogeneous condensate, a particular
source fraction or local thermal equilibrium. They do not close the
coarse-grained kinetic stress or replace relativistic/quantum dynamics.

## Canonical NR fields and charge density

Let psi_1 and psi_2 have leading masses m and 2m. Write n_i=|psi_i|^2,
rho=m(n_1+2n_2), and S=(n_1+2n_2)/(2m) in natural units. The relevant
Hamiltonian terms are

    H=integral [|grad psi_1|^2/(2m)+|grad psi_2|^2/(4m)
      +delta_gap n_2+gamma(psi_2* psi_1^2+c.c.)+U(S)+...] dV.

The ellipsis denotes the preexisting local quartic and gravitational terms.
gamma is the canonically normalized NR conversion coupling; no new value
is fitted here. The local cubic flow obeys

    i dot psi_1=2gamma psi_2 psi_1*,
    i dot psi_2=gamma psi_1^2,
    dot n_1+2 dot n_2=0.

Thus conversion changes composition but not S at that point. The local
portal flow is

    psi_1 -> exp(-i theta) psi_1,
    psi_2 -> exp(-2i theta) psi_2,
    theta=U'(S) t/(2m).

It leaves both S and psi_2* psi_1^2 invariant. Since S is also invariant
under the cubic flow, these two local Hamiltonian flows commute. The
statement applies at arbitrary field amplitudes in this NR model; it is
not restricted to the large-density limit of U.

This does not make the portal dynamically irrelevant. Spatially varying
theta creates currents through the gradient Hamiltonian. Its flow does
not generally commute with spatial transport. Only a spatially uniform
linear mass shift can be removed globally without this force.

## Portal force in the exact NR momentum equation

The portal chemical-potential terms are mu_1=U'/(2m), mu_2=U'/m.
Their contribution to the total momentum equation is therefore

    -n_1 grad mu_1-n_2 grad mu_2=-S grad U'
                             =-grad [S U'(S)-U(S)].

This is precisely the portal pressure functional used in the earlier
averaging analysis. It follows from the NR field equations for arbitrary
spatial fields and phases, rather than being imposed as a fluid EOS.
Other stresses remain in the same momentum equation: kinetic/quantum
stress, conversion stress, the original quartic, and gravity. This identity
isolates one contribution; it does not claim that it is the whole stress.

In particular, the source rest gap has no direct pressure in the NR
Hamiltonian, while the local cubic has a separate stress contribution.
Keeping those terms is necessary when deriving the full evolving response.
They have not been shown to cancel the portal force.

## Composition independence in the cold two-fluid limit

If kinetic and gradient stresses are temporarily omitted, both species
have the same acceleration per unit leading mass from U. Linearize around
a homogeneous mixture with source mass fraction f. For fractional density
perturbations delta_1, delta_2, the portal-only acceleration matrix is

    delta_i_double_dot=-k^2 c_U^2[(1-f)delta_1+f delta_2],
    c_U^2=S U''/(2m^2).

Its eigenvalues are k^2 c_U^2 and zero, independent of f. The nonzero mode
changes total density; the zero mode changes composition at fixed total
density. At an exactly absent species the fractional perturbation of that
species is only a formal limiting variable; the physical occupied-fluid
density mode has the same nonzero eigenvalue. Reactions can affect the
composition mode, and kinetic stress changes the spectrum, but merely
changing f cannot remove this restoring coefficient.

These identities do not prove that an inhomogeneous mixture has the same
coarse-grained sound speed as a coherent state. Spatial averaging gives
-grad <P_U>, and the response of the intensity distribution and other
stresses remains dynamical. Relativistic source/daughter normalization
corrections also lie outside the leading mass alignment used here.

## Evidence and implication

portal_mixture_identity.py checks local charge conservation, phase
covariance and invariance of the cubic interaction, the weighted momentum
force using exact rational arithmetic, the cold mixture matrix and the
pressure derivative. All 35 checks pass; the manifest validates provenance.
The general statements are the displayed algebraic identities, not inferences
from the finite samples. The derivation is self-reviewed.

The coherent-mode calculation applied to a special phase-locked branch.
This result shows that the underlying local portal force and its charge
alignment are much more general. The produced mixture cannot evade that
term solely by retaining sources or undergoing local conversion. A viable
route still needs an evolved transport/state response or a different
interaction, as well as a derivation of the repo's halo law.
