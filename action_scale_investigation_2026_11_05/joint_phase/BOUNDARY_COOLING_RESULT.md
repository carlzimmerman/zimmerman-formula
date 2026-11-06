# Cooling the finite boundary and deriving phase-conversion kinetics

## Outcome

The existing scalar contact scattering can cool a cold material boundary when
it sees an even softer dilute radiation bath. A local restoring thermal mode
exists conditionally if the radiation energy density satisfies

    16 U_a > rho_pool c^2.

This removes the previous boundary sign obstruction only when that bath is
provided. It does not establish a finite stable halo or supply the bath.
An explicit tilted-quartic phase potential gives an exponentially barrier-
dependent vacuum-decay rate and a time-dependent conversion power. The absolute
vacuum density does not fix the barrier, prefactor or front speed. No1/2 is
derived, and the cooling and conversion models have not been merged into a
conservation-complete halo solution.

Base7428c64f1c; contract2288d8f348. This work continues on the isolated published
branch. No adopted action or other investigation is changed.

## 1. Soft radiation can remove particle kinetic energy

Retain the interaction -lambda chi^2 a^2/4. Let chi have mass m, nonrelativistic
isotropic velocities, and let radiation a be massless and dilute, so stimulated
scattering can be neglected. Work to leading order in kB T/(mc^2) and radiation
energy E/(mc^2). The soft elastic cross section is

    sigma_0=lambda^2/(16 pi m^2)

in natural units. Its angular distribution in the target rest frame is
isotropic to this order. This is the soft limit of the exact stationary-target
cross section in TRANSPORT_CAPTURE_RESULT.md.

For a moving target of speed beta c, incident-direction cosine mu, the
rest-frame energy is gamma E(1-beta mu). With elastic soft scattering, averaging
the outgoing rest-frame direction gives lab outgoing mean energy
 gamma^2 E(1-beta mu). Scattering events carry the relative-flux weight
(1-beta mu). Averaging incident directions relative to an isotropic target
velocity distribution gives fractional Doppler gain

    gamma^2 <(1-beta mu)^2>-1 = (4/3) gamma^2 beta^2.

Using <beta^2>=3kB T/(mc^2) in the nonrelativistic limit gives radiation gain
4kB T E/(mc^2). Stationary-target recoil contributes radiation loss E^2/(mc^2).
Therefore the leading mean radiation energy change per collision is

    <Delta E_a>=E(4kB T-E)/(mc^2).

This derivation uses the scalar contact's soft angular limit, rather than
assuming that an arbitrary particle interaction has the photon-electron
Compton coefficient. Cross-section energy corrections, relativistic targets,
induced scattering and nonthermal target distributions require a revised
collision integral.

If u_E is radiation energy density per energy, define

    U_a=integral u_E dE,
    kB T_C=[integral E u_E dE]/(4 U_a).

The heat gained by the material per volume per time is then

    H_a=4 n sigma_0 c U_a kB(T_C-T)/(mc^2).

It cools the particles when T>T_C. No blackbody detailed-balance claim is made:
for high occupation numbers, induced effects omitted here matter. A soft bath
with the required large U_a must be checked against that dilute approximation.
The derivation fixes a rate for a specified spectrum; it does not create that
spectrum or energy density.

## 2. The boundary condition and its restricted stability

FINITE_HALO_RESULT.md showed that a smooth, stationary impermeable boundary
with no local production requires H_net=-K n^2 kB T, where K is the annihilation
coefficient. Let

    A_T=4 n sigma_0 c U_a kB/(mc^2),
    B_T=K n^2 kB.

For the boundary's local thermal perturbation, with n, bath and the
quasistationary compression relation held fixed,

    n c_v T_dot=A_T T_C-(A_T-B_T)T.

A finite positive equilibrium and restoring temperature response for T_C>0
require A_T>B_T, and then

    T*=T_C/[1-B_T/A_T].

The same interaction gives sigma_0 c/K=4. Hence

    A_T/B_T=16 U_a/(n m c^2),
    U_a>rho_pool c^2/16.

This is a locally stable temperature mode under the stated fixed-density/bath
assumptions. It is not stability against coupled density, wall, gravity,
radiation or capture perturbations. Extra positive heating would increase the
required cooling burden. It also does not select n or the phase pressure.
At equality there is no finite positive equilibrium for T_C>0; the inequality
must be strict. Very near it, T* can violate the nonrelativistic approximation.

### Letting density respond at fixed boundary pressure

A fixed-density thermal test is not the same as a pressure-confined wall.
For a prescribed constant external material pressure Pext, let
n=Pext/(kB T), retain u(R)=0, and allow time-dependent density. Continuity gives

    div(u)|R=T_dot/T-K n.

Combining it with internal energy gives an enthalpy equation. Define
C_a=4 sigma_0 c U_a/(mc^2) and c_p=c_v+kB. Then

    c_p T_dot=-kB C_a(T-T_C)+K Pext,
    T*=T_C+K Pext/(kB C_a),
    n*=Pext/(kB T*).

The temperature perturbation decays with rate kB C_a/c_p, and density follows
through the imposed pressure relation. Thus this restricted local boundary
system can erase both temperature and density memory when the pressure and
bath are externally maintained. For T_C>0 its equilibrium automatically
satisfies C_a>K n*, equivalently the same radiation-density inequality above.
The case T_C=0 lies at equality and differs from the fixed-density thermal
test because density now changes. These equations follow analytically from
the two balance equations; they are not a new global eigenmode calculation.

This local closure is more constructive than the fixed-density test, but it
selects the answer through Pext, U_a and T_C. None is supplied by the pool
analogy or by absolute dark-energy density. Radial motions, wall displacement,
source supply and gravitational stability remain outside this closure.

The bath's gravity and stress cannot simply be omitted: even the minimum U_a
corresponds to radiation active gravitational density2U_a/c^2 greater than
rho_pool/8. Its enclosed gravitational effect depends on geometry, but the
previous matter-only approximation requires reassessment. An external bath's
pressure can act on both sides of a wall; only its stress difference confines
matter. No extra positive boundary pressure is inferred from U_a alone.

## 3. Supplying this bath is a strong additional requirement

For a particular one-pass, outward, optically thin source,
U_a(R)=L_soft/(4 pi R^2 c). If the preceding flat material tail estimates
rho_pool(R)=v_h^2/(4 pi G R^2), the cooling condition requires

    L_soft > v_h^2 c^3/(16 G).

This is an optimistic lower bound in that specified geometry, not a universal
bound on trapped or externally maintained isotropic radiation. Optically thick
trapping might change luminosity needs, but would invalidate the preceding
radiative-transfer assumptions and requires radiation pressure/diffusion to be
solved. The finite-boundary density estimate itself remains conditional until
a complete halo solution is constructed.

Suppose a finite vacuum reservoir of available mass-equivalent energy M_vac
supplies the one-pass luminosity, with100% conversion into the needed soft
radiation. Then

    t_deplete < 16 (M_vac/M_halo) R/c,
    M_halo approximately v_h^2 R/G.

This follows from energy conservation, without observational numbers. A small
vacuum reservoir relative to the material halo cannot supply this bath for a
long time in the one-pass model. Less-than-unit radiative conversion worsens
that budget. Dark-energy density alone specifies neither reservoir volume
nor the replenishment process.

The previous outer tail used radiative heating, while this wall requires
cooling. A global solution must produce a temperature/spectrum profile with
the appropriate heat-flow direction in each region. Assigning an independent
bath to each region is not a derivation. No such coupled transport solution
is claimed here.

## 4. Explicit vacuum potential and conversion rate

Use a canonical scalar phi, natural units, and a small tilted quartic:

    V(phi)=Vout+lambda_v(phi^2-v^2)^2/4+DeltaV q(phi/v),
    q(z)=(2+3z-z^3)/4.

Both endpoints are stationary; the phase energy difference is DeltaV. For
DeltaV much less than lambda_v v^4, approximate the wall by the degenerate
quartic. Its tension follows from the one-dimensional energy integral:

    Sigma=integral_-v^v sqrt[lambda_v/2](v^2-phi^2)dphi
         =(2sqrt(2)/3)sqrt(lambda_v) v^3.

For a flat-space, zero-temperature thin-wall bounce,

    B(R)=2 pi^2 Sigma R^3-(pi^2/2)DeltaV R^4,
    R_b=3 Sigma/DeltaV,
    B_b=27 pi^2 Sigma^4/(2DeltaV^3)
       =(32 pi^2/3)lambda_v^2 v^12/DeltaV^3.

The leading semiclassical nucleation rate per physical four-volume is
Gamma_4=A_pref exp(-B_b). The fluctuation prefactor A_pref has not been
calculated. The bounce requires a thin wall and radius small enough for the
neglect of gravitational curvature to be justified. Thermal or strong-gravity
nucleation would be different calculations.

This is an explicit answer to what controls the rate: the barrier shape, wall
tension, phase splitting and fluctuation dynamics. Holding Vout and DeltaV
fixed does not fix lambda_v or v. Changing the barrier changes B_b and hence
the rate exponentially. The dependence cannot be removed by calling DeltaV
the observed dark-energy density. Local baryonic coupling can modify the
potential, but its coefficient and the baryonic density profile remain inputs.

## 5. Nucleation is not a steady luminosity

As a tractable growth model, assume constant homogeneous nucleation rate,
constant wall speed w, nonexpanding flat space, and Poisson nucleation with
the usual extended-volume overlap prescription. The expected converted
fraction is

    f(t)=1-exp[-I(t)],
    I(t)=integral_0^t Gamma_4(4 pi/3)w^3(t-t')^3 dt'
        =(pi/3)Gamma_4 w^3 t^4.

The released latent power per initial volume is

    q_release(t)=DeltaV f_dot
       =(4 pi/3)DeltaV Gamma_4 w^3 t^3 exp[-I(t)].

It starts at zero, peaks at

    t_peak=[9/(4 pi Gamma_4 w^3)]^(1/4),

and falls as the reservoir converts. Its time integral is DeltaV, not an
unlimited supply. Finite geometry, expansion, inhomogeneous nucleation and
wall interactions change the history. Wall speed itself depends on pressure
and friction; it is not determined by vacuum levels alone. In a steady
low-speed drag approximation DeltaV=eta_wall w, the friction eta_wall is a
new medium-dependent quantity, not a derivation of w.

Only some fraction of released energy may become the required soft radiation;
other fractions can go into walls, bulk motion or hard particles. The displayed
particle theory has not calculated that fraction or spectrum. A hypothetical
luminosity eta_rad V_res q_release(t) therefore still contains uncomputed
microphysics, state and geometry. It is not automatically proportional to Mb,
constant over a halo lifetime, or tied to the MOND normalization.

## 6. Coefficient and halo status

The conditional flat-tail relation remains v_flat^4=2G zeta L_a/c, requiring
L_a/Mb=c^2 sqrt(G rho_DE)/(4zeta) to obtain the target. Neither the cooling
condition nor the conversion calculation establishes that luminosity relation.
The factors4,16 and the bounce coefficients are derived in their respective
calculations; they are not interchangeable with the desired1/2.

The boundary thermal sign can be repaired by a specified soft bath. A local
restoring mode has been derived. But capture, the radiation budget, finite
mass/pressure boundary, global radial dynamics and the full thermal spectrum
have not been solved together. The previous no-cooling boundary obstruction
is conditionally removed, not replaced by a proved finite stable halo.

## Evidence and continuation

boundary_cooling.py passes15 exact checks: flux-weighted Doppler gain,
boundary equilibrium/restoring slope, common-coupling threshold, luminosity
and reservoir bounds, quartic tension, bounce action, conversion fraction and
power integral. Reversing the cooling sign fails the equilibrium and restoring-
slope checks. Both manifests are retained and validated. These are self-reviewed
conditional derivations, not an independent proof audit or a simulation of a
finite galaxy.

Primary-source context: [Coleman and De Luccia, Gravitational effects on and of
vacuum decay](https://static.ias.edu/pitp/archive/2011files/PhysRevD.21.3305.pdf)
contains the thin-wall framework; [Analytic false-vacuum decay rate in the
thin-wall approximation](https://arxiv.org/abs/2304.02290) emphasizes the
renormalized rate including prefactors. The action and tension used here are
derived explicitly; no complete prefactor result is borrowed or claimed.

Next physical work must supply a consistent radiation source/spectrum and
conversion microphysics with an actual reservoir and wall dynamics, then solve
the coupled finite halo. Selecting a bath or barrier to reproduce a desired
luminosity would be calibration. The analogical premise does not specify those
inputs, and no universal rate or1/2 follows from the model as currently defined.
