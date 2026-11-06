# Radiation spectrum, thermalization and retained energy

2026-11-06. Base c710dc164d395c1bc5ce1289d53728706a1b668e;
frozen contract 949c73998f. Continues FRONT_CAPTURE_RESULT.md.

**Outcome:** the existing scalar interaction admits a conditional dilute thermal
radiation spectrum, but its normalization and temperature are not selected by
vacuum density. The same interaction ties radiation opacity to annihilation.
In a uniform cold halo, being opaque and surviving many dynamical times without
replenishment are incompatible. Inverse reactions in dilute chemical equilibrium
do not rescue a cold, material-dominated halo. Independent material scattering
can redistribute recoils, but does not dispose of the injected energy or fix the
source. No globally stable halo, derived rotation curve, or MOND 1/2 results.

Unless restored explicitly, c=kB=hbar=1 and theta=kB T is an energy. These are
self-reviewed conditional analytic results, not a complete transport simulation.
Only this investigation is changed.

## 1. The specified source is hard; scattering can change its spectrum

The current interaction is -lambda chi^2 a^2/4, with massive chi and massless a.
For cold chi chi -> a a, the two outgoing particles each have energy m in the
pair rest frame at threshold. There is no soft emission branch at this order.
For nonrelativistic Maxwell chi at temperature theta, the leading Doppler width
is sigma_E^2=m theta/2: each component of the pair center-of-mass velocity has
variance theta/(2m). Thus the line is narrow relative to m, not centered on theta.
Its number-weighted mean energy is m+3 theta/2 to leading thermal order for a
velocity-independent annihilation coefficient, by conservation of the pair's
mean energy. The width is the leading Gaussian Doppler approximation; the exact
line including higher-order kinematics is not calculated here.

The earlier wall action contains no radiation coupling or emission spectrum.
This annihilation source is the specified particle channel, not a calculation
of radiation from the wall. Adding a new soft decay channel would add masses,
couplings and branching fractions requiring a new calculation.

For E,theta much smaller than m, dilute isotropic radiation scattering on a
Maxwell chi bath has energy drift and second moment per unit time

    D1(E) = nu E(4 theta-E)/m,
    D2(E) = 2 nu theta E^2/m,       nu = n_chi sigma_0 c.

D1 was derived in BOUNDARY_COOLING_RESULT.md. To derive D2, write the first-order
Doppler change as E beta dot (n_out-n_in). Isotropic velocities have covariance
<beta_i beta_j>=(theta/m) delta_ij, and the leading soft scalar angular law is
isotropic, giving <|n_out-n_in|^2>=2. Recoil variance is higher order in E/m in
the thermal E~theta regime. Consequently the normalized number spectrum obeys

    partial_t p = -partial_E(D1 p) + (1/2) partial_E^2(D2 p).

With zero energy-space current, its normalized stationary solution is

    p_eq(E) = E^2 exp(-E/theta)/(2 theta^3).

This Wien spectrum has <E>=3 theta, <E^2>=12 theta^2 and radiation Compton
temperature <E^2>/(4<E>)=theta. Hence the net mean heat exchange vanishes at
common temperature. This demonstrates kinetic equilibrium, not a continuing
heat source or a proof of convergence for a spatial halo. The diffusion equation
is not valid for the initial E~m collisions. Stimulated effects are excluded;
a high-occupation spectrum requires the full quantum collision term.

Elastic scattering conserves radiation particle number, so it cannot set the
amplitude from theta alone. A blackbody normalization must not be imposed.
Primary-source context: Sadowski and Narayan's
[photon-conserving Comptonization](https://arxiv.org/abs/1508.04980) likewise
tracks number separately from temperature rather than assuming a blackbody.
Only its abstract was checked for this contextual distinction. The scalar
coefficients and dilute spectrum above are derived here, not borrowed from its
photon-electron transport model. No novelty claim is made.

## 2. Softening competes with annihilation of the scattering material

For the current interaction, in the cold dilute limit,

    sigma_el(E) = sigma_0/(1+2E/m),
    sigma_0 = lambda^2/(16 pi m^2),
    K = <sigma_ann v> = lambda^2/(64 pi m^2),
    sigma_0 c/K = 4.

Thus the radiation collision rate is at most four times the target's
annihilation-depletion rate n_chi K. At E=m the ratio is only 4/3. Increasing
lambda cannot separate these clocks. This comparison presumes negligible
inverse pair production and the same cold population in both rates.

The exact stationary-target mean recoil per collision is E^2/(m+2E).
As a diagnostic, treating energy as a continuous mean variable gives

    dE/dN = -E^2/(m+2E),
    N(Ei -> Ef) = m/Ef-m/Ei + 2 ln(Ei/Ef).

At fixed target density, the corresponding mean-closure elapsed time is

    t_soft/t_ann = [m/Ef-m/Ei+4 ln(Ei/Ef)+4(Ei-Ef)/m]/4,
    t_ann = 1/(n_chi K).

These integrals are exact for this continuous closure, not exact expected
first-passage times of the stochastic scattering process. For Ef much smaller
than m the large m/Ef term shows why a few collisions are insufficient. Finite
material temperature eventually stops recoil-only cooling near E~theta.
Maintaining a cold fixed density over this interval is itself a new requirement.

The density cannot be held fixed without a supply. In a uniform, static,
unreplenished cell with negligible inverse reactions,

    n(t)=n0/(1+n0 K t),
    N_soft,exposure(t)=integral n(t) sigma_0 c dt
                     =4 ln(1+t/t_ann,0),
    n(t)/n0=exp[-N_soft,exposure/4].

The exposure is the mean collision-count clock for a retained soft test particle,
not its individual collision count. Hard particles have a smaller collision
rate. A many-collision processing stage cannot keep the original target
inventory in this homogeneous cold annihilation model.

### A stronger lifetime versus opacity condition

For a uniform region of size R, define soft optical depth tau=n sigma_0 R,
light-crossing time R/c, and dynamical time R/v_h. Algebra gives

    t_ann = 4 R/(tau c),
    t_ann/t_dyn = 4(v_h/c)/tau.

Therefore t_ann much greater than t_dyn requires tau much less than 4 v_h/c.
For a nonrelativistic halo this is optically thin. Conversely, tau much greater
than one gives a short material lifetime relative to its dynamical time. This
is a necessary-condition obstruction for this uniform, unreplenished cold
population, not a theorem for arbitrary multiphase or replenished halos.

The usual thick, uniform random-walk estimate t_diff~tau R/c also gives

    t_diff/t_ann ~ tau^2/4.

Its coefficient has geometric uncertainty; it is not an exact diffusion
solution. A static opaque medium cannot be assumed over its photon escape time
when this ratio is large. Supplying J=K n^2 can maintain density, but consumes
rest-mass-equivalent power m c^2 K n^2 per volume and injects hard annihilation
radiation. No such replenishment rate was derived from rho_DE.

## 3. Can inverse reactions or rapid material collisions rescue it?

Cold soft radiation cannot efficiently recreate pairs of mass m. If both
chi chi <-> a a directions instead reach chemical equilibrium, then
mu_chi=mu_a. In dilute kinetic and chemical equilibrium with one degree of
freedom per species and fugacity z=exp(mu/theta),

    n_a = z theta^3/pi^2,
    n_chi = z (m theta/(2 pi))^(3/2) exp(-m/theta),
    n_chi/n_a = sqrt(pi/8)(m/theta)^(3/2) exp(-m/theta).

These follow directly from the massless and nonrelativistic Maxwell-Boltzmann
phase-space integrals. The material rest-energy to radiation-energy ratio is

    m n_chi/(3 theta n_a)
       = sqrt(pi/8)(m/theta)^(5/2) exp(-m/theta)/3 -> 0

in the cold limit. So dilute chemical equilibrium makes this sector
radiation-dominated, not a cold material-dominated pool. A driven nonthermal
hard spectrum, degeneracy, another conserved charge or a different reaction
network is outside this result and needs explicit transport/source equations.

Independent chi self-scattering remains a real conditional way to share a hard
recoil before escape. With the earlier quartic self-coupling lambda_self,

    sigma_self = lambda_self^2/(128 pi m^2),
    Gamma_self/Gamma_ann
      = [lambda_self^2/(2 lambda^2)] (v_rel/c)

for nonrelativistic relative speeds. Fast thermal material collisions compared
with annihilation require a large coupling ratio. The fast initial recoil is
not nonrelativistic, so its actual stopping length needs the energy-dependent
cross section, not this cold formula. A necessary geometric criterion is
n sigma_self(E_recoil) R much greater than one; efficient redistribution then
also requires sufficient collisions and a thermal reservoir. No value of
lambda_self/lambda is selected here. This route is open but conditional, not
ruled out by the radiation-opacity test.

Even perfect redistribution does not eliminate energy. To expose this issue,
consider a closed fixed-volume cell with Nc material particles initially at
theta_i and Na radiation particles of mean energy E0. Neglect annihilation and
escape for this isolated diagnostic. If they reach dilute common-temperature
kinetic equilibrium while retaining both numbers, energy conservation requires

    theta_f = [(3/2) Nc theta_i + Na E0]/[(3/2) Nc+3 Na].

For theta_i<theta_bound and E0>3 theta_bound, staying below a prescribed cold
energy scale theta_bound requires

    Na/Nc <= (3/2)(theta_bound-theta_i)/(E0-3 theta_bound).

For hard E0~m this allows only a small radiation energy load in a cold cell.
This is a fixed-volume energy-budget result, not an escape criterion or a
virial halo evolution equation. Expansion, radiation escape or energy export
must be included when the budget is exceeded. Merely retaining every recoil
can heat or expand the halo rather than stabilize it.

## 4. Trapping changes pressure and does not establish global stability

The prior boundary cooling model required U_a>rho_chi c^2/16. If that bath is
isotropic, its pressure is U_a/3, and

    P_rad/P_gas > m c^2/(48 kB T).

It cannot generically be discarded in a cold halo. Forces depend on pressure
gradients and the stress difference across the boundary; an equally strong
external bath can cancel the boundary radiation pressure. The ratio is a
warning about the approximation, not proof of outward disruption for every
geometry. Radiation transport, its stress and the material boundary must be
solved together. An LTE spectrum at the material temperature alone provides
zero net scattering heat, not the cooling needed at the annihilating boundary;
a steady cooling flux requires departures from that local equilibrium.

A separate limiting stability check shows why local thermalization is
insufficient. For a fixed-mass, self-gravitating ideal-gas sphere with negligible
external pressure, radiation stress and rotation, virial equilibrium implies

    E_total=-C theta,    R theta=constant,    C>0.

If it changes slowly along this sequence with prescribed heating H and outgoing
luminosity L(theta), then theta_dot=(L-H)/C. The effective heat capacity is
negative. A hypothetical thermal emitting surface with L proportional R^2 theta^4
therefore has L proportional theta^2; at H=L(theta0) with fixed H,

    delta theta_dot = [2 L(theta0)/(C theta0)] delta theta.

That thermal mode is growing. The blackbody-like surface is an additional
emission assumption, not a result of number-conserving scattering. Alternatively,
a homologous thick diffusive LTE sphere with fixed opacity kappa has
L proportional R theta^4/(kappa rho) proportional R^4 theta^4/(kappa M), which
is independent of theta along the same virial sequence. This scaling test is
neutral, not restoring; variable opacity, source response and profile changes
matter. Neither diagnostic is a global stability result for the proposed halo,
and the matter-dominated virial assumptions cannot simultaneously be invoked
where radiation pressure dominates. They refute the inference that sharing
heat by itself proves whole-halo stability.

## 5. Rotation curves and the coefficient remain unselected

The earlier conditional flat-tail formula v_h^4=2 G zeta L_a/c assumed a central,
optically thin source with a specified spectrum. Thick diffusion, an external
bath or energy-dependent spectral evolution changes that derivation; its flat
rotation curve cannot simply be carried over to this calculation.

Even within that earlier limit, obtaining a0=(c/2)sqrt(G rho_DE) requires

    L_a/M_b = c^2 sqrt(G rho_DE)/(4 zeta).

A kinetic equilibrium spectrum fixes shape given temperature and particle
number. It does not fix these inputs, source power per baryonic mass, wall
conversion efficiency, or the self-scattering coupling. The derived factors
3,4 and1/2 in individual kinetic identities are not that MOND normalization.

## Evidence, audit and continuation

spectrum_thermalization.py passes18 exact checks. Its mutation reverses the
virial heat-capacity sign and fails precisely energy conservation and the
thermal eigenvalue (16/18). spectrum_equilibrium_limits.py passes6 additional
checks of phase-space densities, the cold chemical limit, opacity lifetime
and source-line variance. Three hash-recorded manifests and raw results are
under evidence/spectrum_thermalization, evidence/spectrum_thermalization_mutate
and evidence/spectrum_equilibrium_limits. All24 positive checks pass; they
verify the stated identities, not a spatial transport calculation.

Self-audit claim: the three stated limits do not provide a stable cold halo or
select its normalization. Verdict: **conditional on the named closures**.
Dependencies: contact rates -> opacity/lifetime comparison (passed algebra);
soft drift/variance -> zero-current spectrum (passed in dilute soft domain);
energy conservation -> cell temperature (passed for fixed numbers/volume);
virial closure -> local thermal response (passed for the stated source/loss
laws). A complete source spectrum, material stopping calculation, spatial
radiation transfer and global halo perturbations are not addressed. Hard-event
diffusion, arbitrary inhomogeneous opacity, quantum degeneracy and driven
chemical equilibrium are outside the proven scope. Review is by the author,
not independent; frozen script inputs were not edited after execution.

Route dispositions:
- Multiple radiation scattering in the SAME uniform cold unreplenished
  annihilating population fails the lifetime/opacity discriminator. This
  construction is closed; arbitrary replenished or different-particle media
  are not excluded.
- Dilute kinetic equilibrium is derived conditionally. Its absolute temperature
  and number normalization remain input-dependent. Adding dilute chemical
  equilibrium fails to preserve cold material dominance.
- Independent material self-scattering remains open. The next discriminating
  calculation requires its stopping cross section and an energy-export channel,
  together with an independently supplied particle/radiation source. The current
  action leaves the required coupling ratio and front emission unspecified;
  choosing them to fit a0 would be calibration.

A new calculation can proceed with a specified emission or cooling interaction,
but no such interaction is forced by the pool analogy or rho_DE. This report
lands the spectrum and competing-rate analysis; it does not mark the broader
research objective complete.
