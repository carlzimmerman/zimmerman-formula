# Carrier-derived feedback: large recoil jumps and source-lifetime competition

Checkpoint CF-2026-10-13. Starting shared revision:
`db10b5368ceedbf32c88ae5372537e1406d222f7`.
Original cold-energy mechanism remains OPEN. This work examines the actual
mixed elastic channel identified in the repository's carrier reduction, instead
of introducing a new receiver, noise spectrum, or selector force.

## 1. Pinned physical inputs and admissibility

`INPUT_CARRIER_REDUCTION.txt` preserves the input reduction. Its proposed
positive-frequency NR model has masses m and M=2m+delta, delta>0,

    c3=g/[2m*sqrt(2M)],
    H_excess=int[T+delta*nb+c3*(b*psi^2+conjugate)+k*npsi^2].

The same conversion vertex conditionally generates off-resonant mixed elastic
scattering psi+b -> psi+b. We use the supplied leading NR contact coefficient,
not an independently fitted coupling:

    g_ab=4*c3^2/delta,
    mu=m*M/(m+M),
    sigma_ab=mu^2*g_ab^2/pi,
    Gamma_b=g^2*epsilon/(8*pi*M)=c3^2*m^2*epsilon/pi,
    epsilon=sqrt(1-4m^2/M^2).                                    (1)

The contact amplitude and cross section require dilute, weak Born scattering,
a narrow source quasiparticle and energy detunings well away from the internal
pole. In particular the daughter kinetic energy E must be much smaller than
delta for the threshold contact expansion. Real production daughters have
E approximately delta/2 and FAIL that condition. Do not apply these results to
the resonant production shell or count its real intermediate state twice.
The input reduction also records a relative NR matching discrepancy M/(2m)
from its covariant expression; the present rate ratios are leading-NR results,
not exact relativistic precision predictions.

The new test takes the cold-source limit: each incoming source is at rest,
and scattering is isotropic in the center-of-mass frame under the contact
approximation. These are additional state/kinematic assumptions. No bath
preparation, quantum kinetic admission, physical density or halo distribution
is derived here. Standard center-of-mass and exponential decay conventions are
consistent with [PDG Kinematics, sections 49.2 and 49.4.1](https://pdg.lbl.gov/2025/reviews/rpp2025-rev-kinematics.pdf).
The formulas below are explicitly derived in the stated NR limit.

## 2. The exact one-collision energy kernel in this approximation

Set r=M/m, a=4*r/(1+r)^2 and z=cos(theta). An incoming daughter of speed v
has COM velocity v/(1+r). After rotating the relative velocity by theta,

    E'/E = (1+r^2+2*r*z)/(1+r)^2 = 1-a*(1-z)/2.                  (2)

Because z is uniform on [-1,1], R=E'/E is uniform on [1-a,1]. Therefore

    <(Delta E)^j> = (-a*E)^j/(j+1),  j>=1,
    <Delta E>=-a*E/2,
    <(Delta E)^2>=a^2*E^2/3.                                    (3)

These are raw jump moments, not the central variance of an individual jump.
The latter is a^2*E^2/12. In a Poisson collision process the raw second moment
enters the Kramers-Moyal coefficient because random event counts also fluctuate.
Every collision has E'<=E; the source receives the energy loss and opposite
momentum. Direct velocity reconstruction checks both energy and all nonzero
momentum components.

Near M/m=2, a approaches 8/9. A single collision loses 4/9 of daughter kinetic
energy on average, and can lose as much as 8/9. The mass ratio 2 itself is used
only as the kinematic limit; at exact threshold epsilon=0 the decay-rate ratio
in section 4 is not defined.

These are large fractional jumps. For example,

    |<(Delta E)^3>|/[E*<(Delta E)^2>] = 3*a/4 -> 2/3.

There is no small-jump parameter in this isotropic near-threshold mass ratio.
A Fokker-Planck truncation is consequently not justified merely by computing its
first two coefficients. This does not exclude a different forward-peaked
interaction, a high-temperature bath with a different controlled limit, or a
coarse observable for which an approximation is independently validated.

The conditional energy-density jump equation for a fixed cold bath is

    partial_t F(E) = integral_E^{E/(1-a)} nu(E')*F(E')/(a*E') dE'
                    -nu(E)*F(E),
    nu(E)=nb*sigma_ab*sqrt(2E/m).                                 (4)

For M>m, 1-a>0. This equation preserves particle count when endpoint fluxes
are controlled; it transfers energy to the omitted source distribution. It is
not a closed two-species energy-conserving model unless the source recoil and
source evolution are included. It is a more faithful conditional starting
operator than an assumed small-step diffusion in orbital energy.

## 3. A concrete false prediction from the diffusion replacement

For a diagnostic only, freeze the collision rate nu. The exact process is a
compound multiplicative Poisson jump process. With exposure Lambda=nu*t,

    <(E/E0)^j>_jump = exp[Lambda*(<R^j>-1)].

The two-moment diffusion uses A_E=-nu*a*E/2 and D_E=nu*a^2*E^2/6. Its moments are

    <(E/E0)^j>_FP = exp[Lambda*(-j*a/2+j*(j-1)*a^2/6)].            (5)

The first two moments agree exactly, so checking them alone would falsely
validate the approximation. The third-moment log discrepancy is Lambda*a^3/4.
For a=8/9 and Lambda=1:

| moment | exact jump | two-moment diffusion |
|---:|---:|---:|
| 1 | 0.6411803884 | 0.6411803884 |
| 2 | 0.5349861591 | 0.5349861591 |
| 3 | 0.4873401855 | 0.5808807013 |
| 4 | 0.4607020255 | 0.8207548083 |

The exact cold-bath process NEVER raises E above E0. Its diffusion replacement
is geometric Brownian motion and at this exposure predicts

    P_FP(E>E0) = 0.13079828535, versus P_jump(E>E0)=0.              (6)

That heating tail is an approximation artifact. This is a mathematical
counterexample within the frozen-rate diagnostic, not an observed particle
fraction or a calculation using the actual energy-dependent rate. The exact
monotone-support statement remains true for the cold-source kernel (4).

## 4. Does the source survive long enough to provide the collisions?

Let C=c3^2 and define a dimensionless source-density proxy

    chi_b=4*C*nb/delta^2.

For a coherent background this equals the square of 2*c3*sqrt(nb)/delta,
a useful off-resonant mixing scale. Here it is only a dimensionless density
parameter; chi_b<<1 is a declared regime, NOT a proved necessity for every
incoherent or nonthermal source state. We do not combine a coherent pump and
an independent-particle gas as if their reductions were identical.

Using the same vertex in both rates (1) gives the cancellation

    nu0/Gamma_b = 4*chi_b*(mu/m)^2*(v/epsilon).                    (7)

For 0<v<=epsilon and small chi_b, nu0/Gamma_b<=4*chi_b. The actual grid below
uses the stronger off-resonant requirement E/delta<=0.01. To obtain a ratio
of at least one would instead require

    chi_b >= (m/mu)^2*epsilon/(4*v).                              (8)

Near threshold at E/delta=0.01 this is about 3.98, outside the chosen small
mixing/density regime. Increasing density to that level requires a new medium
and coherence analysis; (8) is not a universal physical prohibition.

For an unreplenished resting source bath in the independent dilute decay
approximation, nb(t)=nb(0)*exp(-Gamma_b*t). Before a tagged daughter undergoes
its FIRST elastic collision its energy is unchanged. Neglecting other forces
and interactions, its time-dependent collision hazard is therefore
nu0*exp(-Gamma_b*t). The first-event probability over the entire depletion is

    P_first=1-exp(-nu0/Gamma_b)<=nu0/Gamma_b.                      (9)

This treats the bulk density as its large-population deterministic limit and
ignores inverse replenishment, stimulated decay, and collisions with daughter
products. It does not approximate the number of later collisions after the
first recoil changes the energy.

The finite grid uses m=1, C=1e-9,
M=2*sqrt(1+u^2), u={0.001,0.02,0.1},
chi_b={0.001,0.01,0.1}, E/delta={0.0001,0.001,0.01}.
It gives nu0/Gamma_b from 2.51416e-5 to 0.0253192. Thus P_first is at most
about 2.50% in this specified grid. There is no astronomical density or time
unit behind these dimensionless examples.

## 5. Recoil is storage; decay returns it to daughters

There is a second distinction between cooling a tagged daughter and cooling
the whole sector. Suppose a source initially at rest receives kinetic energy L
in an elastic encounter. The tagged daughter loses L. If that source later
completes b->psi+psi, its products carry total kinetic energy L+delta by total
energy conservation and the rest-mass difference. Counting the tagged daughter
and both new daughters, the combined kinetic change is +delta, not -L.
This is independent of the intermediate redistribution, subject to closed
completed particle events and no exported energy. Mean energy per particle is
a different observable because particle number changes.

The existing transport identity K=E_total-m*Q-delta*N_b expresses the same
ledger globally. A maintained source bath requires actual replenishment and
energy accounting; inverse conversion, export, coherent storage or a live hot
source state cannot be replaced by a permanent cold sink. We have not derived
which of these states the carrier theory dynamically prepares.

## 6. What changed, verification, and the remaining route

This work moves from an arbitrary noise/filter model to an allowed process in
the supplied carrier action's conditional particle reduction. Its new result
is a joint recoil-and-lifetime constraint: in the tested cold-source contact
regime, collisions are large jumps and the bath is usually lost before even
one tagged-daughter elastic encounter. Treating it as a persistent Gaussian
cooling bath would fail two distinct admission checks.

`run/results.json` records 163 deterministic checks: recoil moments and
conservation, rate cancellation, integrated first-event probabilities and exact
jump/diffusion moment comparisons. `lean_run/results.json` records seven exact
algebra/inequality statements and three rejected damaged controls. Lean does
not derive scattering theory, quantum kinetic admission, the Poisson process,
source-state preparation or a halo. The external input reduction is pinned in
this directory and both manifests hash it or the relevant proof sources.
This is self-review; there is no claim of new empirical evidence.

The next physical route must retain finite recoil jumps and live conversion,
with a matched resonance treatment and a state capable of maintaining any
receiver population. A controlled hot/replenished/collective source could change
the present limits but needs its own derived closure. The cold-source results
must not be extrapolated to that untested regime or to the production pole.
No target-free halo selector, confinement mechanism or acceleration scale has
yet followed from these calculations.
