# Photon scattering and spontaneous conversion diagnostics

Parent checkpoint: a4b3559aa7fc8c791f1d4b652dc82e4085792fcb.
This tests two losses implied by the same photon portal used for creation.
Neither loss is significant at the assigned benchmark in the approximations
below. This is not a complete apparatus loss budget or proof of particle
existence. It also shows that this benchmark does not supply a visible glow.

## Photon scattering from a carrier

Use L_int=-g R F^2/4-mu R |phi|^2, g=1e-20/eV, mu=.002 eV,
m=1 eV and M_R=2 eV+2e-9 eV. For gamma(k)+phi(p) -> gamma(k')+phi(p'),
the tree-level t-channel amplitude, up to an irrelevant overall phase, is

    M = mu g [(k.k')(epsilon.epsilon')
              -(k.epsilon')(k'.epsilon)]/(t-M_R^2).

Averaging over two incoming photon polarizations and summing two outgoing
ones gives

    mean |M|^2 = mu^2 g^2 t^2/[4(M_R^2-t)^2].

The implementation checks this using explicit transverse polarization vectors
at six scattering angles and verifies both photon Ward identities. No charged
carrier or extra electromagnetic vertex is introduced.

For a free carrier initially at rest, s=m^2+2m omega and
Q=(s-m^2)^2/s. With q=-t in [0,Q],

    sigma = mu^2 g^2/[64 pi (s-m^2)^2]
            integral_0^Q q^2/(M_R^2+q)^2 dq.

For b=Q/M_R^2 the integral is
M_R^2 [b+1-1/(1+b)-2 log(1+b)]. Natural-unit cross sections are multiplied
by (hbar c)^2. Independent lab-angle integration uses
omega'=omega/[1+(omega/m)(1-cos theta)] and the two-body recoil Jacobian.
The two integrations agree within their recorded tolerance.

At the prescribed pump photon energy, approximately 1 eV:

    sigma = 6.17330e-64 m^2,
    summed independent-beam peak photon flux = 1.24830e31 /(m^2 s),
    scattering rate per carrier = 7.70614e-33 /s.

This uses the PEAK intensity 1e12 W/m^2 of each wave rather than a spatial
orbital average. Within the independent-beam free-scattering model it is a
conservative illumination choice. It is not an upper bound on coherent or
stimulated processes in a standing-wave resonator.

The exact free-target recoil is K=q/(2m). Taking q>2m(U-E0) as an escape
criterion leaves the cross section unchanged to displayed precision. That is
an impulse ejection diagnostic, not a finite-shell transition calculation.
Momentum transfers dominating the integral are much greater than the inverse
trap size. Bound-state form factors, very small recoil transitions and
subsequent wall interactions are outside this calculation.

For a prescribed isotropic 300 K Planck distribution, integrating c times
photon number density times the ejecting cross section gives 2.33e-43 /s.
The dimensionless energy integral is truncated at omega/(kT)=100. This does
not include near-field thermal noise or fluctuating material potentials.

## Spontaneous conversion back to photons

For the scalar operator -g R F^2/4, the vacuum width is

    Gamma_R,gammagamma = g^2 M_R^3/(64 pi) = 3.97887e-42 eV.

This normalization is independently stated in Liu, McGinnis, Wagner and Wang,
“nu scalar in the early Universe and (g-2)mu,” Phys. Rev. D 105, L051702
(2022), published March 14, equations (3)-(4), page 2:
https://doi.org/10.1103/PhysRevD.105.L051702
Primary published PDF inspected October 14, 2026:
https://scoap3-prod-backend.s3.cern.ch/media/files/68484/10.1103/PhysRevD.105.L051702.pdf
Their scalar phi maps to this repo's R and g_gamma_gamma maps to g. Only
the operator normalization and vacuum width are used. Their MeV benchmark,
neutrino coupling and empirical admissibility conclusions are not transferred
to this eV model. This is a normalization check, not a novelty claim; the
source was read remotely and is not represented as locally hash-cached.

In a local, nearly on-shell nonrelativistic approximation, add
-i Gamma_R,gammagamma/2 to the free-mediator Hamiltonian. First-order
perturbation of the normalized dressed pair then gives

    pair conversion rate = P_virtual_R Gamma_R,gammagamma/hbar.

The preceding calculated P_virtual_R=7.64843e-5 gives 4.62345e-31 /s.
This approximation treats the imaginary photon self-energy as locally
constant over the small mediator energy and momentum spread; it is not a
full confined-photon continuum calculation. It includes the preceding
residue through P_virtual_R. The open vacuum R->carrier-pair width is not
inserted into this below-threshold state.

The corresponding spontaneous radiated power is 1.48152e-49 W per pair.
Typical photons have about 1 eV energy, wavelength 1.23984 micrometres:
infrared, not visible light. The spontaneous channel therefore provides
neither the proposed visible glow nor a useful single-pair readout.
A different radiative channel or externally driven readout would need its
own calculation; none is silently supplied by this small width.

## Scope and interpretation

Over the 0.1854 s preparation pulse, the independent-beam collision
probability diagnostic for two carriers is 2.86e-33 and the spontaneous
conversion diagnostic is 8.57e-32. The modeled shell tunneling rate is many
orders larger. These comparisons make these two particular channels low
priority in the benchmark loss budget, conditional on the assigned model.

Twenty tolerance checks pass and the bounded-run manifest validates its
input/output hashes. No Lean verification of scattering or apparatus physics
is claimed. Missing channels include stimulated sideband emission, coherent
standing-wave effects, wall excitations, material absorption and actual cavity
photon density of states. Coherent reverse conversion into the prescribed
pump is already part of the pair-drive Hamiltonian; it must not be counted
again as a vacuum-width loss. Other stimulated processes remain uncomputed.

The overarching creation goal remains open. The next high-impact obligations
are the coherent pump-induced potential and stimulated loss budget, followed
by a feasible electromagnetic mode and empirical constraints on this specific
parameter point. None of these small loss rates establishes propulsion or
identity with the cosmological cold component.
