# Physical common-gravity response of the shared n=1 state

2026-10-19. Parent CE-SCALAR-DIPOLES-2026-10-19 / CE-FM-090.
This derives the static response of the actual shared-state fluid control,
rather than a rigid subsystem spring or an imposed distribution of dipoles.
The physical baryon closure and finite-GP corrections remain explicit in
`modes/SHARED_MODES.md` and the equilibrium lane; see their final file names
in the packet handoff. This calculation uses the exact common-density n=1
fluid channel. It is not the complete relativistic Phi/X/baryon theory.

## 1. Shared state, physical source and rest frame

For pressures p_d=K_d rho_d^2 and p_b=K_b rho_b^2, the common-profile
equilibrium has rho_d=a rho_0, rho_b=b rho_0, with

    a=K_b/(K_d+K_b), b=K_d/(K_d+K_b), a+b=1,
    K=K_d K_b/(K_d+K_b), K_d a=K_b b=K,
    rho_0=rho_c sin(pi r/R)/(pi r/R), R^2=pi K/(2G).

The common total-density channel has pressure K rho^2. Its mass-constrained
second energy variation is

    E2=K integral delta rho^2 - (G/2) integral integral
                                     delta rho(x)delta rho(y)/|x-y|.

Translations are its l=1 zero modes. Work in the object's accelerating COM
frame, with integral z delta rho=0. This removes free whole-object fall,
while retaining internally compressional l=1 perturbations. A common
finite-wavelength external gravitational potential is

    U_e=-E phi_k, phi_k=sin(kz)/k, D_k=integral rho phi_k.

Its source is -E D_k. The required internal self-response is
chi_D=partial D_k/partial E, at fixed masses and COM. It is not a response
to a species-dependent force. The test source overlaps the object because
laplacian U_e=-k^2 U_e; a plane-wave density perturbation may be realized
locally about an ordinary positive background, rather than as an isolated
globally positive sinusoidal source. The full external source dynamics is
separate from this susceptibility probe.

Since the exact mass dipole integral rho z is zero in this frame,

    D_k=-(k^2/6) integral rho z^3 + O(k^4),
    phi_k = r P1 - k^2 r^3(P1/10+P3/15)+O(k^4 r^5).         (1)

The l=1 cubic compression and l=3 octupole are both needed. Deleting the
entire l=1 sector would incorrectly delete a physical internal response.
Deleting only its translation eigenfunction without imposing COM would
also give the wrong source projection.

## 2. Exact cubic l=1 response with the COM constraint

Set G=R=1, K=2/pi for the following dimensionless calculation. Let the source
be U_e=-E r^3 P1 and the COM Lagrange multiplier lambda r P1. Write

    H=delta U_self-E r^3 P1-lambda r P1,
    delta rho=-H/(2K), (laplacian+pi^2)H=-10E r P1.

A regular solution is

    H=[A j1(pi r)-10E r/pi^2]P1.

The exterior self-potential has zero mass dipole, so both its value and
radial derivative vanish at r=1. These two conditions give

    A=2pi E/3, lambda/E=10/pi^2-5/3.                         (2)

The COM condition is independently verified by
integral_0^1 r^3 j1(pi r)dr=3/pi^3. Direct mass-moment integration gives

    chi_1 = partial integral rho r^3P1 / partial E
          = [20/(3pi^2)-40/63] R^7/G.                       (3)

The coefficient is positive. Although the applied cubic potential contains
a nonharmonic l=1 component, the *induced* exterior dipole remains zero.

An independent check expands the density in Newton-kernel eigenfunctions
j1(n pi r/R). For n>=2, subtracting the mass-dipole constraint changes each
source coefficient from f_n to f_n-f_1 z_n/z_1, where f_n is its cubic
overlap and z_n its ordinary dipole overlap. The exact susceptibility term
in G=R=1 units is

    t_n=(600/pi^6)(n^-4-n^-6).

Summing with zeta(4)=pi^4/90 and zeta(6)=pi^6/945 gives exactly (3).
This also supplies a rigorous positive remainder bound after N terms:

    0 < sum_{n>N} t_n < 600/(3pi^6 N^3).                    (4)

## 3. Exact cubic l=3 response

For U_e=-E r^3 P3 the source is harmonic, and

    H=A j3(pi r)P3, delta rho=-H/(2K).

Matching the self-potential to B r^-4 P3 gives
A=-7pi E/3. Integrating the conjugate mass moment gives

    chi_3 = partial integral rho r^3P3 / partial E
          = [(105-10pi^2)/(3pi^2)] R^7/G.                   (5)

There is no mixing of (3) and (5) at quadratic order, by angular
orthogonality. The l=3 coefficient includes the Legendre rather than an
unannounced STF normalization.

## 4. The shared-state gravitational normalization actually obtained

Equations (1), (3), (5) imply

    chi_D(k)=(R^3/G)[C(kR)^4+O((kR)^6)],
    C=2/(9pi^2)-4/189=0.001351797423165... .                 (6)

The static susceptibility is independent of the free mass amplitude in
this exact n=1 fluid limit. That is a genuine consequence of its density
Hessian, not a universal density-normalization prediction. The masses
still set mode frequencies, oscillator strengths, allowed forcing and
departure from the linear regime.

For one object per physical volume V_R=4pi R^3/3,

    4piG (chi_D/V_R)=3C(kR)^4+O((kR)^6).

For an independent separated population of filling f, replace the right
side by 3C f(kR)^4. It tends to zero; it does not yield the requested
constant 1/(4piG) acceleration susceptibility. This result is stronger
than dimensional 1/G scaling because it includes the complete shared
source and its constrained internal susceptibility.

The l=1 part alone is 3[20/(3pi^2)-40/63](kR)^4/100 at leading order.
It can be compared with the other lane's dynamical eigenmode sum; its
source-carrying total modes are distinct from compensated composition
modes with zero physical linear source. A static density-Hessian eigenbasis
is not itself the dynamical normal-mode frequency spectrum.

The relevant small-deformation parameter is approximately

    epsilon_def = E(kR)^2 / (G M_total/R^2).

It must be small along this near-equilibrium branch. Thus the nonlinear
departure scale depends on mass, size and k; neither (6) nor the equilibrium
selects a universal acceleration a0 or a fixed dipole ceiling. Large forcing
requires a moving-boundary/full GP and baryon calculation and may produce
deformation, stripping or branch changes. No claimed saturation is extrapolated
from a linear susceptibility.

## 5. Finite controls and historical correction

`run_002` completed with 45-second wall, 30-second CPU, 65536-byte logs and
one numerical-library thread. Its deterministic checks include boundary
matching, independent COM moments, cubic mass moments, six finite kR values
(0.02,0.05,0.1,0.2,0.5,1), odd partial waves 1,3,5,7, and a separate
64-term COM-constrained eigenbasis sum. Terms beyond l=7 are not asserted
zero at finite k; (6) uses the analytic small-k reduction, where they are
higher order. Quadrature is binary64, not interval certification.

The first run failed its final assertion because a 64-term positive series
was compared with its infinite sum at an unjustified relative tolerance
3e-7. Its actual relative truncation deficit was 1.91119e-5. Analytic
term formula (4) identified the cause, rather than changing a physical
conclusion. The successful run compares the two independent *finite* sums
and bounds the uncomputed positive tail by (4). The original script is
preserved as `check_response_v1.py`, matching the failed input hash; no old
manifest was refreshed. No extra resource escalation or broad rerun was used.

The previous packet's n=1 density Hessian and tidal matching are antecedents,
with actual bytes pinned by the run. The finite-k source, COM-constrained
cubic coefficient, eigenbasis tail and combined response above were derived
here. A peer review is recorded separately; neither a successful process nor
agreement of two finite computations proves microscopic medium occupation.
