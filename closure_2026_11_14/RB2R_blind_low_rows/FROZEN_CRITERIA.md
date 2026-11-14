# RB2R frozen criteria: rows below form B's isolated law, and whether tides can reach them (blind re-grade)

Frozen 2026-11-14, before any script of this lane exists and before any number of the lane is computed. What I had seen
is in `WHAT_I_SAW_AT_START.md` (committed with this file).

## A. The question and the rules (the specification, restated)

**Form B.** A dwarf's cold component is the isolated law's phantom of its own baryons:
M_ph(<r) = [nu(g_N,b(r)/a0) - 1] M_b(<r), nu(y) = 1/2 + sqrt(1/4 + 1/y). No external field effect, no host wind. Tides
strip the cold component outside the Jacobi radius r_J:
- g_B(r) = g_iso(r) = nu(g_N/a0) g_N for r <= r_J;
- g_B(r) = g_N(r) + G M_ph(<r_J) / r^2 for r > r_J.
Baryons as measured today.

**Jacobi radius.** g_iso(r_J) / r_J = k G M_host(<d) / d^3 (m_B = r^2 g_iso / G).
- Primary: k = 3, M_host(<d) = V_c^2 d / G, V_c = 200 km/s (Milky Way), 230 km/s (M31), d = catalogue distance from host.
- Weak edge: k = 2, same host.
- Strong edge: k = 3 at the smallest distance the record allows.
  - MW rows with proper motions: 16th percentile of the orbital pericentre over 500 Monte Carlo draws, flat V_c = 200 km/s
    logarithmic potential, astropy default Galactocentric frame. MW rows without proper motions: r_J(primary) / 3^(2/3).
  - M31 rows: the smaller r_J of (k = 3 at the projected distance from M31) and r_J(primary) / 3^(2/3). M31 at ra, dec
    10.6847, 41.2690; its distance = median over the M31 file's rows of the value implied by each row's heliocentric
    distance, `distance_m31` and angular separation.
  - Field file rows: no tidal edge (tides cannot reach any of them).
- DF2 / DF4: M* 2.0e8 / 1.5e8 Msun, R_e 2.0 / 1.6 kpc, D 20 Mpc, sigma 8.5 +2.3/-3.1 and 6.3 +2.5/-1.6 km/s; DF2 at
  40.4451, -8.4028; DF4 at 39.8128, -8.1160; NGC 1052 at 40.2700, -8.2558. M_host(<d) = d^2 g_law(G 1e11 Msun / d^2) / G at
  the projected distance, k = 3; this is the primary and the strong edge; the weak edge uses k = 2. Reported: the host mass
  inside d that B would need to reach each one.

**Rows and estimator.** Files `real_research/data/dsph/lvd_dwarf_mw.csv`, `lvd_dwarf_m31.csv`,
`lvd_dwarf_local_field.csv` (host MW, M31, field by file). A row is used if `vlos_sigma` > 0 and a half-light radius exists
(`rhalf_sph_physical`, else `rhalf_physical`; pc). log10 M* = `mass_stellar` if present, else 0.4 (4.83 - M_V) + 0.301.
Errors: `vlos_sigma_em`/`_ep` (default 10 %), the radius column's `_em`/`_ep` (default 10 %), `distance_modulus_em`/`_ep`
(default 0.1 mag). Exclude LMC, SMC, M 32. d: `distance_host` (kpc) for MW and M31 rows, fall back to `distance_m31` for
M31 rows, then to `distance`. 2,000 Monte Carlo draws per system: split-normal sigma, radius and distance modulus;
fD = 10^(dDM/5) rescales the radius by fD and M* by fD^2. Wolf: r_1/2 = (4/3) R_h, Plummer a = R_h, g_obs = 3 sigma^2 /
r_1/2, M_b(<r_1/2) = M*/2. Delta = log10(g_obs / g_pred(r_1/2)); Delta_i = median, sd_i = standard deviation.
DF2 / DF4: r_1/2 = (4/3) R_e, Plummer a = r_1/2 / 1.30477; E = 2 ln(sigma_obs / sigma_pred), sigma_pred =
sqrt(r_1/2 g_pred / 3); uncertainty 2 e / sigma_obs, e = lower error if sigma_obs > sigma_pred, else the upper error.

**LOW.** Dwarfs: Delta_iso,i + 2 s_i < 0, s_i = sqrt(sd_i^2 + (0.15 k_i)^2), k_i = d log10 g_B / d log10 M_b at central
values (untruncated law for the LOW test). DF2 / DF4: E_iso + 2 u < 0.

**Reach.** For each LOW row, per footing: r_J / r_1/2 at primary, weak and strong edges and B's residual at each.
TIDES CAN REACH if at the strong edge residual + 2 (its uncertainty) >= 0; TIDES CANNOT REACH otherwise (counts against
B). Any reach that needs r_J < r_1/2 is disclosed (stars outside the tidal radius; not the equilibrium the estimator
assumes); the count stands as frozen. Every graded row whose primary r_J < r_1/2 is listed.

**Words.** Per footing: LOW ROWS COUNT AGAINST B if at least one LOW row reads TIDES CANNOT REACH; else NO LOW ROW COUNTS
AGAINST B. Across footings: the part counts against B only if at least one row reads TIDES CANNOT REACH on both footings.
Footings: canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2; graded separately, never pooled.

**Lead's restrictions.** Grade only rows with catalogue M_V <= -7.7 (if M_V is missing: log10 M* >= 5.4); report how
many rows this leaves out. Rows with `vlos_sigma_ul` non-empty are graded and marked; the word is reported with and
without them. Beside each LOW row (not graded): the V-band mass-to-light ratio it would need to stop being LOW.

## B. Facts from the catalogue census (read before freezing; see WHAT_I_SAW_AT_START.md)

- `mass_stellar` is log10(M*/Msun) at Upsilon_V = 2 (PROVENANCE.md). It is filled for every row with a dispersion, so the
  M_V fallback formula is not used for real rows.
- `rhalf_physical` is the major-axis half-light radius in pc and `rhalf_sph_physical` the circularised one (pc); reading
  from the column names and from the sph value being the smaller one for elongated systems. The spec's order (sph first)
  is used; sensitivity: the major-axis column for the LOW rows.
- Rows with `vlos_sigma_ul` filled have `vlos_sigma` empty; all are fainter than M_V = -7.7. So no upper-limit row enters
  the graded sample; the "with and without" words are then identical. Reported as such.
- MW file rows with host `lmc` are fainter than M_V = -7.7 except the SMC (excluded). No LMC-satellite issue arises.
- M31 file: Andromeda XVIII has empty host and `distance_host` nan; per the spec's fallback d = `distance_m31`, host M31.
  Andromeda XXII has host `m_033` (M33) and is fainter than the cut.
- Field file: Antlia B carries host `ngc_3109`; per the spec the field file has no tidal edge, so it gets none. Disclosed.

## C. My choices where the specification is silent

1. **Constants.** G = 6.67430e-11, GM_sun = 1.32712440018e20 m^3/s^2, pc = 3.0856775814913673e16 m.
2. **Seeds.** numpy `default_rng(seed)`, seed = 20261114 + crc32(row key) mod 2^31 for the 2,000-draw build, and the same
   plus 1 for the 500-draw orbit build (order independent). Twins use seed 777 + index.
3. **Split-normal draw.** z ~ N(0,1); x = c + z ep if z > 0, else c + z em. Draws of sigma or radius <= 0 are set to
   1e-3 of the central value (counted and reported).
4. **Baryon profile.** Plummer shape with a = R_h, normalised so that M_b(<r_1/2) = M*/2 exactly (the Wolf mass the spec
   fixes): M_b(<r) = (M*/2) P(r) / P(r_1/2), P(r) = r^3 / (r^2 + a^2)^1.5. This makes g_B continuous at r_J = r_1/2. (For a
   = R_h, P(r_1/2) = 0.512, so the total is 0.977 M*.) DF2 / DF4: a = r_1/2 / 1.30477, which already gives M*/2 inside
   r_1/2 to 1e-4; same normalisation applied.
5. **Monte Carlo at the edges.** Per draw, r_J is re-solved from the drawn M* and R_h, with k, host mass and d (or the
   strong-edge distance) held at their frozen values. Residual = median over draws; its uncertainty s = sqrt(sd^2 +
   (0.15 k_edge)^2), k_edge = d log10 g_B / d log10 M_b at central values with r_J re-solved.
6. **Numerical derivative for k_i.** Central difference in log10 M_b, step +/- 0.01 dex (M* scaled, R_h fixed).
7. **Root finder for r_J.** scipy `brentq` on ln r over [1e-4 pc, 1e9 pc] for f(r) = ln(g_iso(r)/r) - ln(k G M_host/d^3);
   xtol 1e-14 relative. f is checked monotonic on a 400-point grid once per system at central values.
8. **Orbits.** Initial conditions: ICRS (ra, dec, D = 10^(DM/5 + 1) pc from the drawn modulus, pmra as mu_alpha cos
   delta, pmdec, vlos_systemic) to astropy's default `Galactocentric()` frame of the installed version (solar position,
   height and velocity all astropy's defaults; recorded in the output). Proper motions and vlos drawn split-normal from
   their `_em`/`_ep` (vlos default 1 km/s if missing); distance from the same modulus draw. Integrator: vectorised
   kick-drift-kick leapfrog in Phi = V_c^2 ln r, dt = 0.25 Myr, forward and backward 10 Gyr each; pericentre = min r.
   Check: the analytic pericentre (root of 2[E - Phi(r)] r^2 = L^2 below the present r) for every draw; where the two
   differ by more than 1 % (e.g. the integration window holds no turning point) the analytic value is used and the draw
   is counted. The strong edge uses the 16th percentile.
   Sensitivity (not graded): pmra read as mu_alpha without the cos delta factor.
9. **M31 distance.** For each M31-file row with finite `distance`, `distance_m31` and angle theta to M31:
   D_M31 = D cos(theta) + sqrt(d^2 - D^2 sin^2 theta) (the "+" root; rows with negative discriminant dropped). Median over
   rows. The "-" root median is reported beside it. Projected distance R_p = D_M31 sin(theta).
10. **DF2 / DF4 projected distance.** R_p = 20 Mpc x angular separation (spherical law of cosines). g_law in the host
    mass is the isolated law, nu(g_N/a0) g_N, on each footing. Host mass B would need: brentq in ln M_host(<d) for
    E_B + 2 u = 0 at k = 3 (reported also as a multiple of the law's 1e11 Msun value).
11. **Mass-to-light needed.** For each LOW row, the factor f on M* (central values, R_h fixed) such that
    Delta_i(f) + 2 s_i(f) = 0, with Delta_i(f) = Delta_i - [log10 g_iso(f) - log10 g_iso(1)] and s_i(f) using sd_i and
    k_i(f); reported as Upsilon_V = 2 f. Also the f that puts Delta at 0.
12. **Row names.** LMC, SMC, M 32 excluded by name. Host by file.

## D. Known answers (a failure means NO VERDICT for what it feeds) and twins

- KA1: r_J = 1e12 pc returns g_iso at r_1/2 to 1e-12 relative; r_J = 1e-6 pc returns g_N to 1e-6 relative.
- KA2: a Newtonian point-mass satellite through my root finder gives r_J = d (m / (3 M))^(1/3) to 1e-8.
- KA3: deep limit (g_N/a0 = 1e-13) g_iso / sqrt(g_N a0) - 1 below 1e-6.
- KA4: integrator pericentre equals the analytic one to 1 % at the central values of every MW row with proper motions;
  energy conserved to 1e-4 over the window.
- Twins (through the whole pipeline, to the MUTATE files), on both footings:
  T1 a dwarf exactly on Newton for its stars (M* = 1e6 Msun, R_h = 500 pc, 5 % errors on sigma and R_h, 0.05 mag) must
  read LOW; T2 the same stars exactly on the isolated law must not; T3 the T1 dwarf at d = 20 kpc from the Milky Way, no
  proper motions, r_J well inside r_1/2, must read TIDES CAN REACH; T4 the same dwarf in the field file must read TIDES
  CANNOT REACH. A twin that does not bite is reported as such.

## E. Hand estimate (before any number)

From general literature knowledge, not from the repository:
- DF2 and DF4 read LOW on both footings: 0.9. Both read TIDES CANNOT REACH (their projected distances, about 80 and 165
  kpc at 20 Mpc, give r_J well beyond r_1/2 for a 1e11 Msun law host): 0.85.
- At least one bright field dwarf (e.g. IC 1613-like, rotation and gas ignored) reads LOW: 0.6; any such row reads
  CANNOT REACH by construction.
- Bright MW / M31 satellites: 0 to 3 LOW rows (Crater II-like or large, cold M31 satellites the likeliest), most of them
  reachable at the strong edge only with r_J < r_1/2: 0.6.
- Word per footing LOW ROWS COUNT AGAINST B on both footings: 0.85; NO LOW ROW COUNTS AGAINST B on both: 0.1; split
  across footings: 0.05.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
