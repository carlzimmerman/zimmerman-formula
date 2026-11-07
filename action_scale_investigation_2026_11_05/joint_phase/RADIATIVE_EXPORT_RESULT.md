# Radiative heat export without consuming heavy particles

2026-11-06. Base d87673a122380b0d6fc0cb8ca71aa52502053b97;
frozen contract 1c3a621d89. Continues RADIAL_SUPPLY_RESULT.md.

**Result:** an explicit excited-state extension permits collisional cooling
that preserves the number of heavy particles in each cooling cycle. Its decay,
thermal excitation rate, recoil and line-opacity conditions can be derived.
With prescribed injection and escaping radiation, the local number/temperature
system is restoring. This removes the need for evaporation as the cooling
mechanism, conditionally. It does not remove existing annihilation, prove
retention of every particle, solve the finite halo boundary, or derive1/2.
The exactly isothermal flat-flow trial still fails a pointwise energy test.
The full steady spatial equations are given and conservation-checked below;
a boundary solution and its dynamical stability have not been established.

This is a NEW illustrative extension, not a consequence of rho_DE and not an
adopted action. It introduces a mass gap and two couplings. The current action
also admits higher-order number-preserving radiation, for example
chi chi -> chi chi a a. We have not computed its complete multi-diagram
phase-space rate, so do not claim an extra excited state is logically necessary.
The extension is a tractable alternative with an explicit radiative energy scale.

The general excitation-and-decay cooling idea is already present in dark-sector
research: [Das and Dasgupta, New dissipation mechanisms from multilevel dark
matter scattering](https://doi.org/10.1103/PhysRevD.97.023002) describes
upscattering followed by emission of lighter mediators. Its abstract was checked
for this context. Its particular model/rates are not imported here, and no
novelty claim is made for this mechanism.

Use c=hbar=kB=1 below; theta is temperature in energy units.

## 1. An explicit number-preserving cooling cycle

Add a real excited scalar eta with mass M=m+Delta, Delta>0, and interactions

    L_new = -h eta chi^3/3! -g eta chi a.

chi and eta are odd under the same Z2; a is even and effectively massless.
The original source, self-scattering and annihilation interactions remain.
Positive stabilizing terms and a consistent renormalized vacuum are needed;
the full potential, radiative mass stability and phenomenological bounds are
not established here. In particular, a small Delta is an input, not protected
or selected by the pool idea.

The cycle is

    chi+chi -> chi+eta,       eta -> chi+a.

The same h,g vertices also allow off-shell chi chi -> chi chi a. The displayed
rate isolates the narrow, on-shell excitation/decay contribution; nonresonant
emission is not computed and can matter when thermal excitation is strongly
suppressed. On-shell dominance is an additional regime condition.

The cycle begins and ends with two heavy particles. Kinetic energy excites the mass
gap, and escaping radiation carries energy away. Unlike evaporation, cooling
does not require losing a heavy particle. Unlike annihilation, it does not
convert the pair's rest mass into radiation.

At tree level the decay width and rest-frame emitted energy are

    Gamma_eta=g^2/(16 pi M) (1-m^2/M^2),
    epsilon=(M^2-m^2)/(2M).

The daughter chi receives recoil kinetic energy

    Q_recoil=(M-m)^2/(2M)=Delta^2/(2M),
    epsilon+Q_recoil=Delta.

For Delta much smaller than m, epsilon approximately Delta and
Gamma_eta approximately g^2 Delta/(8 pi m^2). If Delta is of order the cold
thermal energy, this recoil is much smaller than that energy. A necessary
retention check is Q_recoil much smaller than the local binding energy;
initial velocities, excitation scattering and the full velocity distribution
still matter. Preserving heavy-particle count in a reaction is not itself a
proof that all products remain gravitationally bound.

## 2. Excitation rate and cooling function

The h contact amplitude gives the distinct-final-particle cross section

    sigma_exc(s)=h^2/(16 pi s) p_final/p_initial.

For theta,Delta much smaller than m, with relative kinetic energy E,

    sigma_exc(E)=sigma_* sqrt(1-Delta/E) for E>=Delta,
    sigma_*=h^2/(64 pi m^2),

to leading nonrelativistic order, and zero below threshold. For Maxwell
relative energies, P(E)=2 sqrt(E) exp(-E/theta)/(sqrt(pi) theta^(3/2)) and
v_rel=2 sqrt(E/m). Hence

    k_exc(theta)=4 sigma_*/(sqrt(pi*m) theta^(3/2))
                  integral_Delta^infinity sqrt[E(E-Delta)] exp(-E/theta) dE
               =2 sigma_* Delta/sqrt(pi*m*theta)
                  exp(-x) K_1(x),        x=Delta/(2theta).

K_nu is the modified Bessel function. Substitution
E=Delta(1+cosh t)/2 reduces the integral to
Delta^2 exp(-x)[K_2(x)-K_0(x)]/8; the recurrence
K_2-K_0=2K_1/x gives the displayed result. This is an exact thermal average
of the leading nonrelativistic cross section, not a relativistic rate.

For prompt decay, negligible collisional de-excitation and escaping photons,

    C_rad=n^2 Lambda(theta),
    Lambda(theta)=epsilon k_exc(theta)/2.

The factor1/2 counts identical incoming pairs, with one photon emitted per
excitation. Boost corrections to the photon energy are of relative order
theta/m. If photons are trapped or eta is collisionally quenched, this cooling
law overestimates actual energy export and must be replaced by transport.

Its slope is positive:

    d ln k_exc/d ln theta
      =1/2+x[1+K_0(x)/K_1(x)] >0.

At high theta/Delta within the nonrelativistic regime, it approaches the usual
sqrt(theta) collision-rate scaling. At low theta it is suppressed by the
excitation threshold. This is a derived temperature-dependent cooling law,
not a chosen power law or a fitted luminosity.

## 3. The radiation must escape, and the new interaction has costs

The same g coupling permits inverse line absorption, chi+a -> eta. For a
stationary ground-state target, the resonant energy is

    E_res=(M^2-m^2)/(2m),
    E_res-epsilon=(M^2-m^2)Delta/(2mM).

The narrow-line cross-section area is

    S_line=integral sigma_abs(E)dE=pi g^2/(4m^2 E_res).

It follows from the invariant2->1 phase space, or equivalently the
Breit-Wigner peak4pi/p_CM^2 integrated over its energy width. These are scalar
single-state factors; no photon polarization multiplicity is assumed.
For a Maxwell target distribution with Doppler width
sigma_D=E_res sqrt(theta/m), a conservative peak optical-depth estimate is

    tau_line,max <= N_col S_line/(sqrt(2pi) sigma_D).

Use it only when Doppler broadening dominates the natural width and the target
is dilute. The bound is a sufficient thin-line test; recoil detuning may lower
absorption at emitted energies. Nonuniform temperatures, bulk velocities,
multiple scattering and frequency redistribution require explicit line transfer.
The old contact scattering opacity must also be small, not just this resonance.

For a uniform scale R with N_col=nR, prompt decay before a thermal crossing
requires Gamma_eta much greater than sqrt(theta/m)/R. Thin line escape gives
an upper bound on g^2, while prompt decay gives a lower bound:

    g_lower^2=16pi M^3 sqrt(theta/m)/[(M^2-m^2)R],
    g_upper^2=4m^2 E_res sqrt(2pi) sigma_D/(pi N_col).

A parametrically separated window requires g_lower^2 much less than
 g_upper^2. For Delta much smaller than m their ratio is

    g_upper^2/g_lower^2
      approximately sqrt(2pi) Delta^3/(2pi^2 n).

Thus prompt decay and low line opacity need not be contradictory at low enough
number density. This two-inequality comparison is not a demonstration that
all halo requirements hold simultaneously. One must additionally require
Gamma_eta to dominate collisional quenching, the natural width to be small
compared with the Doppler width, and the retained source/thermal assumptions
to be satisfied. None of n,Delta or g is fixed by rho_DE.

There is also new annihilation: eta exchange produces chi chi -> a a.
At threshold its two diagrams give amplitude magnitude
2g^2/(m^2+M^2), and the contribution considered alone is

    K_g=g^4/[16pi m^2(m^2+M^2)^2].

It can interfere with the original lambda contact amplitude. The following
local calculation assumes this amplitude is sufficiently small that the
original nearly constant K remains dominant, without arranging a cancellation.
Making g arbitrarily large to ensure prompt decay can therefore worsen both
opacity and annihilation. Extra processes from the extension, and radiative
corrections, must be checked before claiming a viable complete particle theory.

## 4. A local temperature regulator without evaporative cooling

For a prescribed source J of particles with mean retained kinetic energy e_in,
no local particle escape, constant K, and dilute escaping line radiation,

    n_dot=J-Kn^2,
    c_v n theta_dot=J(e_in-c_v theta)-n^2 Lambda(theta),    c_v=3/2.

These equations follow from differentiating kinetic energy c_v n theta;
annihilation removes mean-energy particles and is included in the number loss.
The cooling cycle itself contributes no heavy-particle-number sink. At steady
state,

    n*=sqrt(J/K),
    e_in=c_v theta*+Lambda(theta*)/K.

Because Lambda is increasing and vanishes toward zero temperature, the model
has a unique positive equilibrium temperature for positive e_in, if its solution
lies within the regime of the approximations. The Jacobian is lower triangular,
with eigenvalues

    -2K n*,       -n*[K+Lambda'(theta*)/c_v].

Both are negative. This is a local fixed-volume result, with source and photon
escape held fixed. Existing annihilation still requires replacement; radiative
cooling does not abolish that cost. Self-gravity, density-dependent opacity,
flow, delayed excited populations and outer-boundary perturbations are absent
from these two eigenvalues. They are not a stable-halo proof.

## 5. Test against the actual inward-flow energy requirement

Retain the previous long-decay example with n=A/r^2,
j=KA^2/(r0R), and u=U+jr/A+KA/r, where
U=-KA(1/r0+1/R). To leading subsonic isothermal order its required local energy
export Q_req satisfies

    r^4 Q_req=j r^2[e_in-(9/2)theta]-2A theta U r-KA^2 theta.

But the line cooling at fixed theta supplies

    r^4 C_rad=A^2 Lambda(theta),

a constant. The required expression has a strictly positive linear coefficient
2KA^2 theta(1/r0+1/R). Therefore this radiative channel cannot alone satisfy
that EXACT constant-temperature trial over an interval without conduction or
profile corrections. It can remove heat, but it does not automatically produce
the exact assumed flat profile. This restricted mismatch is not a no-go for
nonisothermal radiatively cooled halos.

## 6. The coupled spatial problem, now with a physical cooling term

Let M(r) include material and a specified baryonic density rho_b(r), and take a
stationary Newtonian potential Phi'=G M/r^2. Let kappa(theta,n)>0 be a specified
conductivity in its valid regime. Define q=J/n and
 e_rel=e_in-m u u_in+(m/2)u^2. A steady thin-radiation system can be written
without dividing by u, so it allows stagnation points:

    theta'=-F/kappa,
    n'/n={-m u[q-Kn-2u/r]-m GM/r^2+m q(u_in-u)-theta'}
            /(theta-mu^2),
    u'=q-Kn-2u/r-u n'/n,
    F'=J(e_rel-c_v theta)-n c_v u theta'
        -n theta(u'+2u/r)-n^2 Lambda(theta)-2F/r,
    M'=4pi r^2[m n+rho_b(r)].

A transonic point where theta=mu^2 needs a regularity treatment; simply
integrating through a zero denominator would not produce a valid solution.
Radiation gravity, viscosity and nonlocal transport are neglected only where
small. The outward radiation luminosity obeys

    L_rad'=4pi r^2 n^2 Lambda(theta)

when reabsorption and an incoming radiation source are absent. These equations
check against continuity, momentum and internal energy, and give the
conservative stationary total-energy identity

    (1/r^2) d/dr {r^2[n u(c_p theta+mu^2/2+mPhi)+F]}
      =J(e_in+mPhi)-Kn^2(c_v theta+mu^2/2+mPhi)-n^2 Lambda,
    c_p=c_v+1.

Adding L_rad/(4pi r^2) to the flux cancels the cooling term. Rest energy can
likewise be restored using continuity. For a time-dependent self-gravitating
stability calculation, the gravitational field and potential perturbations
must also be evolved; this stationary identity is not that calculation.

The five first-order material equations need source functions, microscopic
parameters and consistent inner/outer conditions. A specified pressure or
confinement mechanism is still required for a finite material boundary;
letting photons out does not establish an impermeable material surface.
No unique boundary data follow from the pool analogy or absolute vacuum
energy density. We have not filled in arbitrary values and called the result
a prediction. The equations have been checked, not solved as a boundary-value
problem or subjected to a global radial eigenmode calculation.

## 7. Coefficient and research status

This calculation supplies a concrete candidate heat-export law with its own
opacity and rate conditions. The mass gap Delta and couplings h,g are new
inputs. Source power, profile, outer pressure, core and transport remain inputs.
There is no relation that forces them to combine into
 a0=(c/2)sqrt(G rho_DE). The factor1/2 in identical-pair event counting is not
that MOND coefficient. Local regulation has not selected a galaxy mass-speed
family or verified its stability.

Next open route: solve the spatial boundary problem with a specified source,
confinement mechanism and admissible rates, and then linearize that solution
including gravity and radiation escape. The prior isothermal trial fails its
pointwise heat test; allowing temperature/density corrections is a meaningful
continuation, not a completed result. The original higher-order radiation route
is also open; its rate has not been shown negligible or evaluated here.

## Evidence and audit

radiative_export.py passes17 exact symbolic checks. A negative control that
counts each identical incoming pair twice fails exactly the cooling event-rate
check(16/17). radiative_flow_equations.py passes4 additional algebraic checks
of the steady continuity, momentum, internal and conservative total-energy
equations. The three manifests preserve hashes, commands and results under
 evidence/radiative_export, evidence/radiative_export_mutate and
 evidence/radiative_flow_equations. All21 positive checks pass. The Bessel
calculation verifies the integral reduction and recurrence, not numerical
collision transport. No spatial simulation or observational fit is claimed.

Self-audit verdict: **conditional on named inputs**. Tree factors, recoil,
thermal-rate derivative, local stability and spatial conservation identities
were checked. Prompt decay, escaping lines, negligible new annihilation,
weak gravity, valid conductivity and a physical finite boundary remain explicit
conditions, not jointly established facts. Author self-review covered these
limits and distinguished the new extension from the adopted model. Frozen
executed inputs were not edited. The broader stable-halo/1/2 goal is incomplete.
