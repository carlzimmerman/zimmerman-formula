# SAT1 FROZEN CRITERIA: where the Milky Way's satellites sit relative to the external field

2026-11-12. TEST lane. Written before any script, before the satellite table is downloaded, and
before any number bearing on the answer is computed. Adopts nothing. Relabels no other lane.

## Question

Under the framework's field reading (G239's QUMOND external-field formula), would a satellite-based
analysis of the Milky Way, using the satellites where they actually are on the sky, report a higher
or lower enclosed mass than the angle average, and by how much? Does the bias close PLT1's
plateau-row gap for the satellite class?

## What is already known (disclosed)

- PLT1 (closure_2026_11_12/PLT1_outer_mass_vs_literature/): at the record's field e_N = 0.01273 /
  0.01054 (canonical / alt) the angle-averaged line is flat near 5.26 x 10^11 Msun beyond 150 kpc;
  the four class-S rows at r >= 150 kpc have pulls -2.56, -2.88, -1.04, -3.20 (canonical), median
  -2.72. The post hoc reading put the -2 crossing at a plateau of 6.64 x 10^11, i.e. roughly a
  factor 1.26 on the line. That number is from PLT1's post hoc file; the factor graded here is
  recomputed by the frozen procedure below.
- G239: at 80 kpc, canonical, e_N = 0.01273, the direction-dependent apparent mass is +58 per cent
  (theta = 0) and +1 per cent (theta = 90 deg) relative to the angle average; along theta = 0 the
  apparent mass diverges with radius because the external field's own acceleration is credited.
- MWG1: with MB15 hot gas added, the angle-averaged line at the record's field already passes the
  plateau rows (class-S plateau pull -0.22 canonical / -1.34 alt).
- h81 (hunt_2026/h81_h82_mw_external_fields.out): the field points toward (l, b) = (268.5, +33.0).
- Background knowledge, not checked here: the classical satellites lie near a polar plane (VPOS)
  whose normal is close to (l, b) ~ (169, -2); the field direction is then roughly 80 to 100 deg from
  that normal, i.e. near the plane. Many ultra-faint satellites are in the north (SDSS/DES footprints
  bias the sky coverage).
- Hand expectation, written now: the odd-in-mu part of g_r (the external field's own term e_N mu,
  times nu) dominates beyond 150 kpc, so the answer depends on whether satellites sit more on the
  side the field points to (which LOWERS the apparent mass) or the opposite side (RAISES it), not
  only on how close they are to the axis. I do not know the sign in advance. Weak guess: the
  satellites are concentrated in the north (b > 0) and the field points to b = +33, so more sit on
  the side the field points to, so LOWERS IT. Confidence low.

## Sign convention (frozen)

G239 writes g_N = g_b r_hat + g_ext z_hat with g_b > 0 the INWARD baryonic pull, and
g_r = nu(|g_N|/a0)(g_b + e_N mu) the inward radial acceleration, mu = cos(theta). The external field
adds to the inward pull (mu = +1) at a satellite on the side OPPOSITE to where the field points.
So for a satellite whose Galactocentric position makes angle psi with the direction the field points
toward ((l, b) = (268.5, +33.0)):

    mu = -cos(psi)

(The uniform external acceleration g_ext points toward (268.5, +33.0); at a satellite on that side,
the baryonic pull is toward the Galaxy, i.e. away from that direction, so the two oppose.) A known-
answer check (KA3) tests this at psi = 0 and psi = 180 deg.

## Inputs

- Satellites: the Local Volume Database (Pace et al.), file data/dwarf_mw.csv from
  https://raw.githubusercontent.com/apace7/local_volume_database/main/data/dwarf_mw.csv (about
  46 kB), downloaded into SAT1_satellite_directions/lvdb/ with URL, size, sha256 recorded. Read with
  `python3 -I`. PROVISIONAL (web data). Columns used: name, host, ra, dec, distance_modulus,
  confirmed_galaxy, confirmed_real, pmra.
- Primary sample: host is the Milky Way (the file's code for it), confirmed_galaxy == 1, a finite
  distance modulus, and Galactocentric distance 50 <= r <= 300 kpc. Variants (reported, labelled):
  V-ALL all rows with confirmed_real == 1 or confirmed_galaxy == 1 (any confirmation, includes
  candidates the file confirms as real objects) and host MW; V-PM primary sample restricted to rows
  with a measured proper motion (pmra finite), closer to what tracer-mass estimators use.
- Conversion: ICRS (ra, dec) to Galactic (l, b) with the standard IAU rotation matrix (J2000; north
  Galactic pole at ra 192.85948, dec 27.12825, l of the north celestial pole 122.93192 deg).
  Heliocentric distance d = 10^(mu_dm/5 + 1) pc. Galactocentric Cartesian: x = d cos b cos l - R0,
  y = d cos b sin l, z = d sin b + z_sun, R0 = 8.122 kpc, z_sun = 0.0208 kpc. The field direction is
  a unit vector in the same Galactic axes (a uniform field has the same direction everywhere).
- Field: e_N = 0.01273 a0 (canonical a0 = 9.36e-11) and 0.01054 a0 (alt a0 = 1.13e-10), direction
  (l, b) = (268.5, +33.0), from h81.
- Baryons: McMillan 2017 census, M_sph(r) as in G239/MWJ1 (copied, not imported), A = 1. Variant HOT:
  census plus MB15 hot gas M_hot(<r) = 4.3e10 Msun (r / 250 kpc)^1.5 (MWG1's form, no cap).
- Kernel nu(y) = 1/(1 - exp(-sqrt(y))).
- PLT1 rows: closure_2026_11_12/PLT1_outer_mass_vs_literature/plt1_results.json, class S, rows with
  r >= 150 kpc (four rows), 20 per cent floor, PLT1's pull function (copied).

## The formula, exactly as G239's code has it

    g_b = G M_b(<r) / r^2 / a0                         (a0 units)
    |g_N| = sqrt(g_b^2 + e_N^2 + 2 g_b e_N mu)
    g_r(r, mu) = nu(|g_N|) (g_b + e_N mu)               (inward, a0 units)
    M_app(r, mu) = r^2 g_r a0 / G = [nu(|g_N|)(g_b + e_N mu) / g_b] M_b(<r)       (M_dyn_dir)
    M_avg(r) = (1/2) INT_{-1}^{1} dmu M_app(r, mu)      (M_dyn, trapezoid on 4001 points)

Variant REL (reported, labelled, not the headline): the Galaxy as a whole is accelerated by the
field; subtract that uniform part, g_r,rel = g_r - nu(e_N) e_N mu. Its angle average equals M_avg
exactly. This is not in G239's code; it is a frozen sensitivity variant.

## Statistic

For each satellite i with Galactocentric r_i and mu_i: M_app,i = M_app(r_i, mu_i) and
M_avg,i = M_avg(r_i). Two radial bins: B1 100 <= r < 150 kpc, B2 150 <= r <= 300 kpc.

- Primary: R_mean = mean_i(M_app,i) / mean_i(M_avg,i) over the bin (a tracer-mass estimator averages
  over tracers, so the mean is the closer analogue).
- Reported: R_med = median_i(M_app,i) / median_i(M_avg,i), and the median of per-satellite ratios
  M_app,i / M_avg,i. Negative M_app (outward net acceleration) are kept and counted.
- Uncertainty: leave-one-out range of R_mean, and a bootstrap (2000 resamples, seed 12) 16-84 per cent
  interval. Reported.

## Required factor F (how the line must rise)

For each footing and baryon variant: the angle-averaged line at each of PLT1's four class-S rows at
r >= 150 kpc (r = 200, 200, 240, 273 kpc), multiplied by a common factor F; F is the value at which
the median of the four pulls (PLT1's pull function, 20 per cent floor) equals -2, found by bisection
on F in [0.2, 5]. If the median is already >= -2 at F = 1, F <= 1 is reported as is.

## Labels (per footing x baryon variant; graded on bin B2, primary statistic)

- NO POWER: fewer than five satellites in the bin.
- R_mean >= 1.02: ANISOTROPY RAISES IT ENOUGH if R_mean >= F, else ANISOTROPY RAISES IT, NOT ENOUGH.
- R_mean <= 0.98: ANISOTROPY LOWERS IT (suffix ", STILL ENOUGH" if R_mean >= F, else ", NOT ENOUGH").
- 0.98 < R_mean < 1.02: NO CHANGE (suffix ", ENOUGH" if R_mean >= F, else ", NOT ENOUGH").
- FRAGILE appended if the leave-one-out range of R_mean crosses a label boundary (1.02, 0.98 or F).
Bin B1 gets the direction part only (RAISES / LOWERS / NO CHANGE / NO POWER); it has no plateau rows.
Headline: census variant, primary sample, both footings. HOT and the sample variants and REL are
reported with their own labels, not as the headline.

## Known-answer checks (all must pass before any label is printed; the script stops otherwise)

- KA1 isotropic directions: mean of M_app over 200,000 isotropic random mu (seed 7) at r = 200 kpc,
  canonical, census, e_N = 0.01273 equals 5.264e11 to 0.5 per cent, and equals the quadrature M_avg
  to 0.5 per cent.
- KA2 G239 anisotropy at 80 kpc, canonical, e_N = 0.01273: M_app(mu=+1)/M_avg - 1 within 1 percentage
  point of +0.58, and M_app(mu=0)/M_avg - 1 within 1 percentage point of +0.01.
- KA3 geometry and sign: (l, b, d) = (0, 0, 8.122 kpc) gives r < 0.03 kpc; (180, 0, 10) gives
  r = 18.122 kpc to 0.03; the ICRS-to-Galactic conversion puts (ra, dec) = (192.85948, 27.12825) at
  b = 90 to 0.01 deg and (266.40500, -28.93617) (Sgr A*) within 0.1 deg of (l, b) = (359.94, -0.05);
  a point at 200 kpc along the field direction gets mu = -1 and M_app < M_avg; along the opposite
  direction mu = +1 and M_app > M_avg.
- KA4 SI hand check: M_avg at 200 kpc canonical recomputed independently in SI with scipy.integrate.quad
  over mu (no a0-unit shortcut) agrees with the script to 0.1 per cent.
- KA5 data: the table parses; LMC distance 45 to 55 kpc heliocentric; Leo I Galactocentric distance
  240 to 270 kpc; at least 20 rows in the primary sample between 50 and 300 kpc.
- KA6 factor: the scaled line at the found F gives the median pull -2 to 1e-3 (when F > 1 is needed).

## Mutations (separate output file sat1_mut.out)

- M1 (must bite): rotate the field direction by 90 deg, two ways: M1a about the Galactic z axis to
  (l, b) = (358.5, +33.0); M1b in the meridian plane over the pole to (88.5, +57.0). Bites if, on both
  footings (census, primary sample), at least one of M1a/M1b changes R_mean in B2 by >= 0.01.
- M2 (must bite): flip the sign convention (mu = +cos psi, equivalently rotate by 180 deg). Bites if
  R_mean in B2 moves by >= 0.01 on both footings.
- M3 (sanity, must bite): e_N = 0 makes R_mean = 1 exactly (to 1e-9) in both bins (no anisotropy
  without a field), i.e. the anisotropy is the field's.

## Limits stated in advance

Published satellite masses come from line-of-sight and proper-motion velocities through an
estimator (tracer-mass estimators, distribution functions), not from accelerations at the
satellites' positions. A satellite's speed reflects the potential along its orbit, not the local
radial acceleration at its present position. So this lane gives the direction of the bias and a
rough size for a position-weighted reading, not a recomputed mass. QUMOND kernel, uniform static
field, LMC's own field neglected.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
