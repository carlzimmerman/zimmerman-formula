# FA1 Phase 1: selector ideas, written before reading the record

Written 2026-11-04 from the requirement sheet alone. No repo file was read
before this file was committed. Nothing here is adopted. kappa = 1/2 FITTED.

Fixed numbers used in the checks below:
- rho_DE ~ 0.69 rho_crit ~ 5.9e-27 kg m^-3, so a0 = kappa c sqrt(G rho_DE)
  ~ 0.5 * 3.0e8 * 6.3e-19 ~ 9.4e-11 m s^-2 (canonical footing 9.3603e-11).
- Mean cosmic dust-like density today ~ 0.26 rho_crit ~ 3.6e10 Msun Mpc^-3.
- Cluster need: dust ~ 1e14 Msun inside 300 kpc, mean density ~ 9e14 Msun
  Mpc^-3 ~ 6e3 rho_crit.
- MW-like disc: baryons ~ 6e10 Msun; the law's dynamical mass at 1 Mpc with
  v ~ 200 km/s is ~ 9e12 Msun.
- Lyman-alpha needs linear dust power to 0.4 Mpc/h comoving, a mass scale
  ~ 2e10 Msun/h. Any halo-mass cut above ~1e11 Msun that acts at z >~ 2 is
  dead on arrival.

The puzzle in one line: the dust-like part must weigh in FRW at z ~ 1100 and in
cluster interiors, but not in isolated galaxies out to the lensing scale
(~1 Mpc). Every selector below is something the banned list does not name.

---

## I1. Tidal isotropy (local-to-mean density ratio of the source)
Status: grounded geometry, speculative coupling.

(a) Selector: the dust part weighs where the tidal tensor of the baryonic source
is close to isotropic (local density close to the mean interior density), as in
FRW and in extended cluster gas, and not where it is strongly traceless, as
around a concentrated galaxy.

(b) Action sketch: metric g, the law's scalar (khronon/aether sector as in v3s),
plus a dust-like scalar chi with an AeST-type term
L_chi = -(1/2) M^2 F(S) (u^mu d_mu chi - Q0)^2, where the switch
S = (E_ij E^ij)^(1/2) / |E^k_k| uses the electric part of the Weyl tensor (E_ij)
over the Ricci trace term, built from the metric. In the Newtonian limit
E^TF_ij / tr E reduces to the traceless over trace part of d_i d_j Phi_N, which
for a sphere is 1 - rho(r)/rho_bar(<r) = 1 - (dlnM/dlnr)/3.

(c) FRW: Weyl = 0, S = 0, dust on. Cluster gas with rho ~ r^-2: dlnM/dlnr ~ 1,
S ~ 2/3. Galaxy outskirts (baryons converged, dlnM_b/dlnr ~ 0.1): S ~ 0.97,
dust off. Vacuum around any mass: S = 1, dust off (Solar System safe).

(d) Kill check: gas-rich dwarfs whose gas mass still rises at the last point
(dlnM_b/dlnr ~ 1) would have S like a cluster's and would get dust; the law
works best exactly there. Second kill: inside a cluster at 300 kpc the enclosed
gas mass rises roughly as r (S ~ 0.6-0.7), only modestly below a concentrated
spiral's outer S ~ 0.9; the response F(S) would need a steep step. Q2: S = 1
near the Sun, so the dust part is off; Q2 then rests on the MOND part (v3s L*)
exactly as before.

(e) Builds on: AeST dust term (Skordis & Zlosnik 2021); tidal-tensor
cosmic-web classification (Hahn et al. 2007, Forero-Romero et al. 2009); Weyl
invariants as screening switches (no direct precedent known to me).

## I2. Mean-flow vorticity of the matter frame
Status: speculative.

(a) Selector: the dust part is suppressed where the matter 4-velocity has
ordered vorticity (rotation-supported discs) and weighs where the mean flow is
irrotational (FRW, pressure-supported cluster gas and galaxy ensembles).

(b) Action: unit timelike aether A^mu aligned dynamically with the matter frame;
L = ... - (1/2) M^2 exp(-omega^2/omega_*^2) (A.dchi - Q0)^2, with
omega^2 = omega_{mu nu} omega^{mu nu} of A, omega_* ~ sqrt(G rho_DE)/kappa ~ a0/c.

(c) FRW and cluster interiors have no mean rotation; discs rotate with
omega ~ V/R ~ 200 km/s / 10 kpc ~ 6e-16 s^-1, versus a0/c ~ 3e-19 s^-1.
Large separation.

(d) Kill: isolated ellipticals and dwarf spheroidals have little mean rotation
yet are said to follow the law (ETG lensing and X-ray, dSph dispersions). If the
record has ETG lensing near the law, I2 dies. Also an aether locked to matter
flow inherits Lorentz-violation bounds; GW speed set by the aether c_T
coefficients.

(e) Jacobson-Mattingly Einstein-aether; vorticity in TeVeS-like vector sectors.

## I3. Fixed physical Jeans length of the dust field (higher-gradient dust)
Status: grounded (ghost-condensate dispersion), likely mass-selector in
disguise.

(a) Selector: the dust field cannot cluster below a fixed physical length L, so
it is a smooth background inside galaxies but collapses with clusters.

(b) Action: ghost-condensate-like P(X) - (alpha/M^2)(box phi)^2, giving
omega^2 = alpha k^4 / M^2 for fluctuations about the condensate.

(c) FRW: modes with k << 1/L cluster as dust. Galaxies: smaller than L.

(d) Kill: the Jeans length of a k^4 dispersion scales as (G rho)^-1/4, so the
Jeans mass falls with time; any cut that removes ~1e12 Msun galaxy dust halos
at z ~ 0 also removes 2e10 Msun/h Lyman-alpha power at z ~ 3. Fixed L ~ 100 kpc
does not stop dust accreting onto a galaxy on scales > L: a cored MW dust halo
with M(<100 kpc) ~ 6e11 Msun puts ~1.6e10 Msun inside 30 kpc (27 % of baryons)
and doubles the lensing signal at 0.1-1 Mpc. Q2: no effect.

(e) Arkani-Hamed, Cheng, Luty, Mukohyama 2004; fuzzy-DM Jeans scale (Hu,
Barkana, Gruzinov 2000), but as a field with no particle reading.

## I4. Staticity of the potential (time-derivative selector)
Status: speculative.

(a) Selector: the dust part weighs where the metric is non-stationary in the
matter frame (FRW expansion, assembling clusters) and is inert in stationary
systems.

(b) Action: AeST-type (A.dphi - Q0)^2 with the dust energy sourced by
u^mu d_mu Phi; in a stationary spacetime the minimum A.dphi = Q0 is reached and
the dust energy density vanishes.

(c) FRW: H != 0. Clusters still accreting (dynamical time ~ 1 Gyr ~ 0.1 t_H).

(d) Kill: X-COP clusters are selected as relaxed; their missing mass inside
300 kpc is the same 1.5-2x. Relaxed versus merging clusters show no clear
split in missing mass. Probably dead.

(e) Skordis-Zlosnik AeST; Bekenstein-Sanders time-dependent scalar.

## I5. Bulk motion relative to the preferred frame (disformal dust)
Status: speculative.

(a) Selector: dust coupling via a disformal metric
g~ = g + B(X) d phi d phi, whose correction is set by the matter velocity
relative to the khronon frame.

(b) Action: matter couples to g; the dust sector to g~; relative boost gamma
of matter to khronon frame sets the effective dust weight.

(c) FRW: comoving matter at rest in the khronon frame by construction.

(d) Kill: the Local Group moves at ~600 km/s relative to the CMB frame,
clusters at ~300-1000 km/s; no clean separation between galaxies and clusters.
Probably dead on order of magnitude.

(e) Bekenstein disformal metric; Zumalacarregui-Garcia-Bellido disformal
couplings.

## I6. Galileon determinant (dimensionality of the source)
Status: speculative.

(a) Selector: the dust part is switched by the cubic invariant det(d_i d_j pi)
of a Galileon-type field, which vanishes for planar or filamentary
configurations and is maximal for isotropic ones.

(b) Action: quintic Galileon epsilon epsilon d d pi d d pi d d pi, with the
dust-energy term multiplied by a function of that invariant.

(c) Discs are planar near the plane; clusters roughly spherical; FRW isotropic.

(d) Kill: beyond a few disc scale heights the field of a disc is nearly
spherical, so det is not small where rotation curves are measured
(R ~ 3-10 R_d). Isolated ellipticals would get dust. GW speed: quintic
Galileon is excluded by c_T = c (GW170817) unless tuned away.

(e) Nicolis, Rattazzi, Trincherini 2009; Vainshtein screening.

## I7. Defect network of the a0 field
Status: speculative.

(a) Selector: the dust part is the energy of topological defects of the a0
scalar, which collect at network nodes (clusters) and are absent in voids and
sheets where most isolated galaxies sit.

(b) Action: O(N) scalar with vacuum manifold giving defects.

(c) Nodes host clusters.

(d) Kill: strings scale with w = -1/3, walls with w = -2/3; neither is dust at
z ~ 1100. Only monopole-like point defects behave as w = 0, and those are
particle-like. Dead on item 5 or item 6.

(e) Kibble mechanism; Vilenkin-Shellard.

## I8. Weyl-to-Ricci ratio in the full metric (fill-factor selector)
Status: speculative; close to I1 but keyed to the total local source, not the
tidal shape of the baryons alone.

(a) Selector: dust weighs where the local Ricci (matter) term is comparable to
the Weyl (tidal) term.

(b) Action: dust term times F(C_{abcd}C^{abcd} / R_{ab}R^{ab}).

(c) FRW: C = 0. Cluster: volume-filling hot gas gives Ricci at 300 kpc.

(d) Kill: in a cluster the Ricci term at 300 kpc is gas, so this reads as a gas
density selector (banned). Self-referential once the dust itself sources Ricci.
Listed for completeness.

(e) Higher-curvature switches; Lovelock invariants.

## I9. Nonlocal curvature history (Deser-Woodard type)
Status: speculative.

(a) Selector: the dust part is a nonlocal functional of box^-1 R along the past
light cone, large where the past cone saw sustained collapse of large volume.

(b) Action: R f(box^-1 R) (Deser-Woodard), or Maggiore's R box^-2 R.

(c) FRW: box^-1 R grows from matter domination.

(d) Kill: this is a memory selector; cluster and galaxy past light cones are
nearly identical on the scales that matter. Overlaps the banned "memory" class.

(e) Deser & Woodard 2007, 2019 (nonlocal MOND); Maggiore 2014.

## I10. Coherence length of the a0 condensate set by rho_DE (domain selector)
Status: speculative.

(a) Selector: the a0 condensate has a coherence length l_c ~ c / sqrt(G rho_DE)
/ (2 pi) or similar; systems larger than a fixed fraction of l_c cannot keep
the condensate phase-locked and the dephased part behaves as dust.

(b) Action: complex scalar Psi with |Psi|^2 tied to rho_DE, phase gradient
supplying the law; the dephased fluctuation spectrum acts as dust.

(c) l_c ~ c / sqrt(G rho_DE) ~ 1.6e27 m ~ 50 Gpc; any fraction that falls
between galaxies (~100 kpc) and clusters (~1 Mpc) needs a number ~1e-5 put in
by hand.

(d) Kill: the needed ratio is not supplied; it is a size selector and inherits
I3's Lyman-alpha problem.

(e) Superfluid dark matter (Berezhiani-Khoury) with the condensate keyed to
rho_DE instead of a particle.

---

## Ranking for Phase 3 (before reading the record)
1. I1 tidal isotropy: cheapest to compute from existing SPARC mass models and
   X-COP gas profiles; has a sharp kill (gas-rich dwarfs).
2. I2 vorticity: killed or kept by isolated ETG/dSph evidence; needs data the
   record may hold.
3. I3, I10: size/Jeans selectors; expected to fail Lyman-alpha against galaxy
   halos.
4. I4-I9: order-of-magnitude problems above.

Nothing here adopts anything. kappa = 1/2 FITTED; not theory closed.
