# Cold scalar production on a stationary target

2026-10-14. Base checkpoint: 2463c24380832d4ba4458aa83203b702ac479ace.
This tests replacing one dilute photon beam by a charged target. The process
gamma+N -> R+N exists in the stipulated scalar-photon theory, but its
stationary-target Born amplitude suppresses precisely the near-rest output
needed here. The calculated cold-pair contribution is negligible for the
explicit benchmark. This is not a universal exclusion of target production.

## Assumptions and source normalization

Retain the hypothetical scalar mediator and vacuum daughter parameters:
m_phi=1 MeV, M_R=2m_phi+2e-9 eV, Gamma_gamma=Gamma_phi=3.41884037e-13 eV.
Use the local interaction -g R F_munu F^munu/4 with

    g=sqrt(64pi Gamma_gamma/M_R^3)=2.93129375e-15 eV^-1.

Treat the target as a free stationary spin-zero particle with mass
M_T=2e11 eV and charge Z=82. Set its elastic form factor to one. This is
a heavy charged point-target diagnostic, not a calculation of a particular
lead sample, lattice or atomic state. The column density 3e25 targets/m^2,
incident flux 1e8 photons/s, Gaussian energy RMS 5000 eV and peak tuning below
are assigned inputs. Attenuation, multiple scattering and detector efficiency
are omitted. This is a single-interaction thin-target calculation.

The scalar photon tensor is supported by Blinov, Gori and Hamer,
[Phys. Rev. D 110, 075006 (2024), Appendix A, Eq. (A1)](https://scoap3-prod-backend.s3.cern.ch/media/files/89008/10.1103/PhysRevD.110.075006.pdf),
checked 2026-10-14. Their tensor has the same gauge-invariant structure up to
an overall crossing/sign convention. They explicitly distinguish on-shell
and off-shell photon form factors. Here we approximate that form factor by
the local coefficient inferred from the on-shell width. Momenta are small
relative to the muon mass, but a full off-shell loop calculation is not included.
The paper's historical muon-anomaly motivation is not imported as current
evidence for the mediator. Its beam-dump yields are not transferred to this
near-rest kinematic regime.

## Exact stationary-target current reduction

Use metric (+---), k=(omega,0,0,omega), initial target P=(M_T,0),
outgoing scalar p=(E_R,p_vec), q=k-p=P'-P and t=q^2. The target current is
J=P+P'=2P+q, with J.q=0. The Born amplitude is, up to an overall sign,

    Mcal=(g Z e/t)[(k.q)(epsilon.J)-(k.J)(epsilon.q)].

For transverse photon polarization and stationary target,
epsilon.J=epsilon.q and k.J=2M_T omega+k.q. Therefore

    Mcal=-(2g Z e M_T omega/t)(epsilon.q),
    average |Mcal|^2=2 g^2 Z^2 e^2 M_T^2 omega^2 p_perp^2/t^2.

The polarization average is over the two incident transverse states. At zero
transverse scalar momentum the amplitude vanishes. This is not inferred from
a high-energy forward-scattering approximation; it follows from the full
stationary spin-zero current. The script independently contracts explicit
four-vectors and checks the photon Ward identity and target-current
conservation at six kinematic points, including a scalar at rest.

## Recoil and the wrong notion of threshold

The incident energy at the total two-body threshold is

    omega_thr=M_R+M_R^2/(2M_T).

At that threshold the scalar is at rest in the center-of-mass frame, with
laboratory momentum

    p_R,thr=M_R omega_thr/(M_T+M_R)=19.9999 eV.

The earlier laboratory cut K_phi<=1e-8 eV for BOTH daughters permits scalar
momentum only up to 0.268328 eV. Thus producing at the reaction threshold is
not the desired laboratory-cold preparation.

To produce a scalar at rest in the lab instead requires

    omega_0=M_R(2M_T-M_R)/[2(M_T-M_R)],
    omega_0-omega_thr=M_R^3/[2M_T(M_T-M_R)].

Numerically omega_thr-M_R=10 eV and omega_0-M_R=10.000100001 eV; the two
incident energies differ by about 1e-4 eV. At exactly p_R=0 the transverse
amplitude above is zero, so one must integrate a finite accepted momentum
neighborhood rather than count that point as an enhanced source.

## Spectral integration without an ultrarelativistic approximation

For p=|p_vec| and u=p_z/p, define E_R=sqrt(M_R^2+p^2). Energy conservation
fixes the photon energy uniquely in the accepted region:

    omega(p,u)=[2M_T E_R-M_R^2]/[2(M_T-E_R+p u)].

The final target has E_T=sqrt(M_T^2+omega^2+p^2-2omega p u). Starting from
the invariant two-body phase space,

    d sigma/d^3p = average |Mcal|^2
                   *delta(omega+M_T-E_R-E_T)/(64pi^2 M_T omega E_R E_T).

Integrating the incident spectral flux S(omega) removes the delta function
with Jacobian 1-(omega-pu)/E_T. The resulting rate is

    rate = N_column (hbar c)^2 Br_phi integral d^3p S(omega(p,u))
           *alpha g^2 Z^2 M_T omega p_perp^2
           /[8pi E_R (M_T-E_R+p u) t^2] *A(p).

A(p) is the previously derived isotropic daughter acceptance, not a target
angular distribution. Its input Kstar=1e-9 eV and Kcut=1e-8 eV are pinned
by the previous package. Br_phi=1/2 includes the competing photon decay.
Decay outside a finite collection region is not modeled, so the result is
an inclusive cold-decay contribution before collection losses.

For an approximately constant S across this extremely small cold region and
a heavy stationary target, the expression reduces to

    rate_static=N_column (hbar c)^2 S(omega_0) Br_phi
                 *alpha g^2 Z^2/(3 M_R^4) integral_0^pmax dp p^4 A(p).

Here the p^4 integral is 1.35970938e-4 eV^5. One power of p^2 comes from the
transverse amplitude, in addition to the radial momentum measure. The exact
recoil integral differs from this approximation by about -5.0e-6 relative,
consistent with the local factor 1-M_R/(2M_T). This comparison tests the
recoil implementation; it does not bound neglected material or loop physics.

With the Gaussian spectral peak tuned to omega_0,

    S(omega_0)=7978.84561 photons/(s eV),
    cold pair rate=5.56569e-42 /s.

There is no useful source at this benchmark. The dense target replaces the
second-beam luminosity problem, but does not remove the small coupling and
near-rest transverse-momentum suppression. The figure is conditional, not a
measured yield or a bound on every gamma-target arrangement.

## Scope of the obstruction

The stationary-target assumption matters. A moving target contributes spatial
components to J; epsilon.J=epsilon.q no longer holds. Thermal motion, atomic
binding, lattice recoil and coherent material response can therefore change
the near-rest node and require a different response calculation. Setting an
elastic point form factor to one does not prove that this rate upper-bounds
all such channels. Additional scalar couplings or production diagrams are
also not included. The remaining source problem cannot be closed simply by
extrapolating this stationary Born contribution to every material.

The next physically distinct candidate must specify either the target's
energy/momentum response or a production channel using the direct lepton
coupling. It must still propagate the laboratory cold acceptance and account
for recoil. A high total yield of boosted mediators is insufficient, and no
verified cooling or trapping stage has yet been supplied.

## Evidence and formal status

The authoritative run is run_covariant/manifest.json. It records 35 passing
checks: stationary-current algebra; threshold comparisons; energy roots,
Jacobian derivatives, full polarization contractions, Ward identities and
target-current conservation at six points; and two integral controls.
The earlier run and its matching initial_check.py are retained as an initial
calculation before the stronger four-vector verification. Its historical
check.py hash corresponds to that snapshot, not the revised current script.

CurrentReduction.lean proves the conditional target-current reduction and
photon Ward algebra. It does not prove the complete scattering calculation,
local-loop approximation, stationary-target model or particle existence.
Compilation logs and source hash are recorded. Numerical energy-root controls
use 65-decimal mpmath arithmetic; final integrals use double precision.

Reproduce:

    python3 sol61_push/cold_primakoff_target_2026_10_14/check.py /tmp/cold_primakoff_results.json

The overall goal remains open. This checkpoint calculates and rejects one
fixed-coupling source benchmark, without claiming that all routes are excluded.
