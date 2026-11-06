# Front speed and retained halo heating

Date: 2026-11-06. Parent physical checkpoint: a51d146c4b.
Frozen contract: 83632bad61. This continues REPLENISHMENT_RESULT.md.

**Result:** a specified wall action determines acceleration, and a specified
particle bath can regulate speed. Neither the bath nor the wall parameters are
selected by dark-energy density. Radiation production competes with wall energy;
intercepting radiation is not the same as retaining its recoil energy. The
explicit ballistic calculation below makes hard-radiation heating inefficient.
No finite stable halo or universal coefficient 1/2 is derived.

## 1. Acceleration, speed and available radiative power

Let Sigma be wall energy per area, Delta V the positive vacuum energy-density
drop, R its radius and gamma=(1-Rdot^2/c^2)^(-1/2). The spherical thin-wall action is

    L = -4 pi Sigma R^2/gamma + (4 pi/3) Delta V R^3.

Its equation, allowing an outward-motion friction pressure P_drag, is

    Sigma gamma^3 Rddot/c^2 + 2 Sigma gamma/R = Delta V - P_drag.

The wall-plus-vacuum energy relative to the original vacuum obeys

    E = 4 pi Sigma R^2 gamma - (4 pi/3) Delta V R^3,
    Edot = -4 pi R^2 P_drag Rdot.

This is an energy balance, not an independent radiation prescription. Drag can
heat surrounding particles; the fraction emerging as radiation and its spectrum
still need a microscopic transport calculation. In the empty classical
thin-wall model P_drag=0 and no radiation degrees of freedom are included.
For initial radius R_b=3 Sigma/Delta V and initial rest, E=0 and

    R(t) = sqrt(R_b^2+c^2 t^2),
    gamma = R/R_b,
    Rdot = c sqrt(1-R_b^2/R^2).

All latent power then grows the wall's area/kinetic energy. Assigning the same
solution the full latent power as photons double-counts energy. Our negative
control deliberately does that and fails energy conservation. Field radiation,
collisions or additional couplings can change this solution; their losses must
also appear in the equation of motion.

A stationary classical wall is at R_crit=2 Sigma/Delta V. With constant Delta V,
the outward pressure derivative there is +2 Sigma/R_crit^2, so radius
perturbations are destabilizing. This classical critical radius differs from
the zero-energy initial radius above. For slow motion with P_drag=xi Rdot,
a nearly planar terminal speed is approximately Delta V/xi; with curvature it
is (Delta V-2 Sigma/R)/xi. Positive xi damps velocity perturbations but does not
supply a restoring radius, halo equilibrium, or a universal value of xi.

## 2. Where a drag coefficient could come from

Use natural units in this section. For the earlier scalar-dependent mass
m_chi^2(phi)=m_0^2+g_chi^2 phi^2, a locally planar static wall conserves energy and
parallel momentum. If normal incoming momentum is k, then

    q^2 = k^2 + m_out^2 - m_in^2.

For an ideal sharp Klein-Gordon mass step, real positive q gives flux fractions

    reflection = (k-q)^2/(k+q)^2,
    transmission = 4 k q/(k+q)^2.

Their sum is one; for q^2<0 the particle is totally reflected. The normal
momentum delivered per incident particle is

    2 k reflection + (k-q) transmission.

Integrate this against f(p) |p_normal|/E_p d^3p/(2 pi)^3 on each incident side,
with opposing signs. The bath distribution must be transformed to the wall
frame. Its velocity-dependent excess over equilibrium contributes friction;
include equilibrium medium pressure only once, either in the phase pressure
balance or in this integral. Finite wall thickness changes reflection. Thus
this is a calculable microscopic prescription once distributions and the wall
profile are supplied, not a computed universal drag for our halo.

An explicit limiting example illustrates the remaining inputs. A perfectly
reflecting planar wall moving at slow nonrelativistic speed w through identical
Maxwell gases on both sides, each of mass density rho and one-dimensional
velocity dispersion s, has opposing pressure

    P_drag(w) = 2 rho [(s^2+w^2) erf(w/(sqrt(2) s))
                 + sqrt(2/pi) s w exp(-w^2/(2s^2))],
    xi = P_drag'(0) = 4 rho sqrt(2/pi) s.

This follows by integrating the specular momentum flux
2 rho (w-v_z)|w-v_z| over the normalized Gaussian v_z distribution.
Here w_terminal approximately Delta V/[4 rho sqrt(2/pi) s] only if this speed
is small compared with s, curvature is negligible, and opacity is sufficient.
This equal-gas example is not the solved phase-transition plasma. Different
rho, s or mass-step opacity give different speeds at the same Delta V.

## 3. What the halo intercepts and deposits

For a finite spherical tail n(r)=A/r^2, outer radius R_h, and impact parameter
b outside any regular core, its particle column is

    N_col(b) = (2 A/b) arccos(b/R_h).

A particle cross section sigma_el gives optical depth tau=sigma_el N_col and
probability 1-exp(-tau) of at least one collision for straight incident rays.
That probability is not the fraction of energy deposited. For a monoenergetic
beam and cold targets define sigma_E=sigma_el times mean fractional photon
energy loss. The thin-limit heating fraction is sigma_E N_col.

Integrating columns over projected area gives N_total exactly for any spherical
number profile. For the ideal integrable cusp N_total=4 pi A R_h. Consequently

    mean thin deposited fraction = sigma_E M_pool/(pi m R_h^2).

The ideal cusp has infinite central optical depth for any nonzero cross section;
this expression is a first-order thin expansion, not a uniform thin-ray claim.
A finite core is needed for an everywhere-thin approximation. The area/count
identity itself remains exact with a core. Multiple scattering requires a
transport solution, including spectrum changes and escape.

For the distant, lab-isotropic external front geometry of the previous report,
incident power is approximately pi R_h^2 eta_front Delta V w. Thus

    L_deposited,thin = eta_front Delta V w sigma_E M_pool/m.

This assumes the front can actually supply the stated radiative fraction; the
empty wall above has eta_front=0. It is conditional linear scaling in POOL mass,
not a derived relation to baryonic mass. Also the external field is nearly
uniform rather than a central inverse-square flux. Do not substitute deposited
luminosity into the earlier v_h^4=2 G zeta L_a/c relation: that relation already
contains scattering through zeta and assumed central-source geometry.

## 4. A recoil can leave the halo instead of heating it

For the existing contact chi-a scattering, with a cold stationary target of mass
m and incoming massless-particle energy E, in natural units,

    sigma_el = lambda^2/[16 pi m(m+2E)],
    recoil_max = 2 E^2/(m+2E),
    mean recoil = E^2/(m+2E),
    sigma_E = sigma_el E/(m+2E).

The contact amplitude is independent of center-of-mass scattering angle, so the
recoil energy is uniform between zero and recoil_max. In a fixed shallow halo
potential, let E_b=m v_escape^2/2 be the nonrelativistic escape energy and
E_cap=min(E_b,recoil_max). A collision leaves the target bound with probability

    f_bound = E_cap/recoil_max.

The mean recoil energy retained in bound targets per incident collision is
E_cap^2/(2 recoil_max), giving

    sigma_E,retained = sigma_E [min(1,E_b/recoil_max)]^2.

For hard annihilation-scale photons E=m c^2, restoring units,

    f_bound = (3/4)(v_escape/c)^2,
    sigma_E,retained/sigma_E = (9/16)(v_escape/c)^4

when v_escape is much smaller than c. This is a strong suppression in the
ballistic, single-collision limit. The escaped particles also deplete halo mass;
this calculation only counts recoil energy in retained targets and is not a
complete binding-energy or mass budget. Fast rescattering before escape could
redistribute recoil, but requires an independently established optical depth
and collision rate. Warm targets and soft photons require the earlier
heating/cooling treatment rather than this stationary-target formula.

## 5. Consequences for stability and the coefficient

The minimal candidate now has explicit equations for wall acceleration, a
microscopic prescription for drag, and a conditional retained-heating efficiency.
It does not close the system: wall tension, phase pressure, incident particle
distributions, radiation branching/spectrum, halo opacity and thermalization
remain physical inputs. Delta V alone does not specify them. Changing these
inputs changes speed and deposited power without changing rho_DE.

The preceding source-power bound already optimistically allowed all intercepted
power to be useful: for isotropic free propagation, P_ext=Delta V, and the
stated central-redistribution comparison, supplied/required power was at most
1/4. Introducing wall losses and incomplete retention cannot improve that
particular optimistic comparison. This is not a bound on arbitrary trapped,
beamed, differently confined or externally replenished models.

Velocity damping is not whole-halo stability. The empty spherical wall has no
stable static radius, and the ballistic hard-photon branch removes particles.
A coupled finite halo with a specified soft spectrum, collisional transport and
an external supply could behave differently, but has not been solved here.
Neither the earlier kinematic maximum zeta=1/2 nor the factors in these wall and
recoil equations select the coefficient of c sqrt(G rho_DE). Claiming that
selection would still require inserting an unselected normalization.

## Evidence and review

front_capture.py checks 16 exact identities in natural units, including the
Euler-Lagrange equation, hyperbolic motion, energy partition, linear drag limit,
reflection/transmission flux, column integration and recoil retention. All pass.
The identical script with --mutate grants the free wall full radiative latent
power and fails exactly the energy-budget check (15/16 pass). Both executions,
input hashes and software records are preserved under evidence/front_capture
and evidence/front_capture_mutate. These checks do not solve a Boltzmann
transport problem, establish thermalization, fit rotation curves, or test global
halo eigenmodes. No new literature priority claim is made.

Self-review covered this report, script and status addition: units, radiation
versus wall power, flux versus amplitude transmission, ideal-cusp limitation,
incident versus retained energy, and the distinction between local velocity
regulation and whole-halo stability. Proofreading found no remaining routine
notation issue in this scope. Frozen executed inputs were not changed.
