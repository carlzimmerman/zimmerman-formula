# RB2 frozen criteria: form B on the hosted rows (Coma UDGs, Milky Way and M31 dwarf spheroidals)

Frozen before any RB2 script exists and before any RB2 number is computed. TEST lane: it relabels nothing, adopts nothing,
is not registered, and changes no frozen label of SE2, XF1, X1, S1, U1, PD1 or PD2. kappa = 1/2 FITTED; not theory closed.
Cold dark energy is a gravitating field component, never a particle. Both footings graded separately, never pooled:
canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2 (L* floor 21.68 / 22.85 pc where screening is reported).

## 0. What form B says here (from the brief and the owner decision of 2026-11-09)

A dwarf's cold component is real mass that fell in with it. The cold mass inside r is the isolated law's phantom of the
dwarf's own baryons, M_ph(<r) = [nu(g_N,b(r)/a0) - 1] M_b(<r), nu(y) = 1/2 + sqrt(1/4 + 1/y). There is no external field
effect and no host wind. Tides strip the cold component outside the Jacobi radius r_J; inside r_J it stays. For a spherical
dwarf this gives, exactly (shell theorem):

- g_B(r) = g_iso(r) = nu(g_N/a0) g_N for r <= r_J;
- g_B(r) = g_N(r) + G M_ph(<r_J) / r^2 for r > r_J.

Baryons are taken as measured today (the stars inside and outside r_J are kept as observed).

**Jacobi radius.** r_J solves m_B(<r_J) / r_J^3 = k M_host(<d) / d^3, i.e. g_iso(r_J) / r_J = k G M_host(<d) / d^3, where
m_B is the dwarf's own isolated-law mass (baryons + phantom; unchanged inside r_J by the cut, so the equation is
self-consistent), d the dwarf's distance from the host centre, M_host the host's measured mass inside d.

- **Primary (SE2's A1 convention, verbatim):** k = 3; MW and M31: M_host(<d) = V_c^2 d / G with V_c = 200 / 230 km/s, d = X1's
  d_host_kpc; Coma: M_host(<d) = g_beta(d) d^2 / G with S1's measured hydrostatic beta model (kT 8.6 keV, r_c 276 kpc,
  beta 0.71, mu 0.6), d = S1's d_mean_kpc.
- **Weak-tide edge (reported):** the host's own tidal factor at today's d: k = 2 for the flat-V_c MW / M31 hosts
  (Omega^2 - Phi'' = 2 V_c^2 / d^2), k = 2 d^2 / (d^2 + r_c^2) for Coma's beta model.
- **Strong-tide edge (reported):** k = 3 at the smallest distance the record allows:
  - MW systems with LVD proper motions: the orbital pericentre in the flat V_c = 200 km/s logarithmic host potential from the
    LVD ra, dec, distance modulus, pmra, pmdec and vlos_systemic, transformed with astropy's default Galactocentric frame;
    500 Monte Carlo draws over the LVD errors; the strong edge uses the 16th percentile pericentre (generous to tides).
    Systems without proper motions: SE2's pericentre reading, r_J / 3^(2/3).
  - M31 systems: the projected distance from M31 (ra, dec of M31 10.6847, 41.2690; M31's distance taken as the median over
    the LVD M31 rows of the value implied by each row's heliocentric distance, distance_m31 and angle), or SE2's reading
    r_J / 3^(2/3), whichever gives the smaller r_J.
  - Coma UDGs: S1's projected distance d_proj_kpc (a lower bound on the 3D distance, so its cut is an upper bound).
- DF2 / DF4 (U1's record inputs: M* 2.0e8 / 1.5e8, R_e 2.0 / 1.6 kpc, D 20 Mpc, sigma 8.5 +2.3/-3.1 and 6.3 +2.5/-1.6 km/s,
  positions and NGC 1052's from U1): the record carries only NGC 1052's baryonic mass 1e11 Msun. B's host mass at d is then
  the isolated law's dynamical mass of that point mass, M_host(<d) = d^2 g_law(G 1e11 Msun / d^2) / G, at the projected
  distance, k = 3 (this is already the strong edge). Reported: the host mass inside d that B would need to reach each one.

**Primary law and screening.** The graded B prediction uses the brief's algebraic law (no screening, L* = 0). Reported
beside it, not graded: B with v3's screening at the L* floor, isolated, from D10's 1D BVP route (iso_1d, copied, not
imported) at each system's central values, applied as a per-system shift. If the two readings give different class labels,
RESULT.md says so in its label lines.

## 1. Rows, data paths and estimators (copied from the lanes named; nothing imported from another lane's folder)

- **dSphs:** X1's sample, loader (LVD files), classes and Monte Carlo build, copied verbatim with the same seed (20261031)
  and the same call order, Wolf (E-W) estimator: g_obs = 3 sigma^2 / r_1/2, r_1/2 = (4/3) R_h, Plummer a = R_h,
  Delta = log10(g_obs / g_pred(r_1/2)). Per system: Delta_i = median over the 2,000 MC draws, sd_i = their sd (X1's columns).
  Classes (X1's, verbatim): MW classical (8 named), MW ultra-faint (M_V > -7.7, 31), bright M31 (log M* >= 5, not M32 or the
  three dEs, 25), M31 others (5), LG field (13; no host; control), individual rows Crater II, Antlia II, Canes Venatici I,
  Sagittarius. The Arroyo binary factor for M_V > -7.7 as in X1.
- **Coma UDGs:** S1's 9 admitted galaxies (Freundlich+2022 TSV, CFG933's admission), S1's estimator (Plummer a = R_e, E-W,
  E = 2 ln(sigma_obs / sigma_pred), sE = 2 e / sigma), S1's constants.
- **DF2 / DF4:** U1's geometry (Plummer a = r_1/2 / 1.30477, r_1/2 = (4/3) R_e, E-W at r_1/2), U1's error rule.

## 2. Statistics and frozen lines (the lanes' own, verbatim)

- **MW classical, MW ultra-faint, bright M31** (graded) and **M31 others** (reported, N = 5): XF1's C2 statistic: bootstrap
  median over the class's systems of Delta_i + N(0, sd_i), 4,000 resamples, seed 11; 95 % interval from the 2.5 / 97.5
  percentiles. Line: the 95 % interval contains 0.
- **Coma UDGs** (graded): SE2's joint posterior (post_udg, copied with its seeds), each galaxy's E replaced by B's.
  - Graded widths: SE2's frozen main widths. Reported: the half widths that XF1 quoted.
  - Knob widths s_k re-derived for B by S1's / SE2's own recipe applied to B's prediction: s_M (M* x 10^+-0.2), s_A
    (sigma x 1.15^+-1), s_D (distance x 1.05^+-1, which also moves R_e and M*), s_aniso = |E-V - E-W|, s_mem = |all 11 - 9|,
    s_pos = |B at d_proj - B at d_mean|. Reported beside it: the record's s_k kept (XF1's convention).
  - Line: the 95 % interval contains 0.
- **LG field** (control, no host): B equals the isolated law there; reported, not graded.

**Class labels**, per class and footing, from the primary B reading:
- **B CONSISTENT:** the 95 % interval contains 0.
- **B FAILS HIGH:** the interval lies above 0 (measured above B).
- **B FAILS LOW:** the interval lies below 0.
- The same rule is applied at the weak and strong edges and to the screened reading. If any of them gives a different label,
  the class label carries "(bracket-sensitive: weak X / strong Y)" or "(screening-sensitive: Z)".

## 3. The rows that cut the other way (graded first in RESULT.md)

A row is **LOW** if it sits below B's untruncated isolated law by more than twice its own uncertainty:
- dSphs: Delta_iso,i + 2 s_i < 0, with s_i = sqrt(sd_i^2 + (0.15 k_i)^2), 0.15 dex being X1's Upsilon_V prior and
  k_i = d log10 g_B / d log10 M_b at the central values (X1's s_i convention applied to B);
- Coma UDGs: E_iso + 2 sE < 0 (S1's per-galaxy sE);
- DF2 / DF4: E_iso + 2 e < 0, e by U1's rule.

For each LOW row, on each footing: r_J / r_1/2 at the primary, weak and strong edges, B's residual at each, and
- **TIDES CAN REACH** if at the strong edge B's residual + 2 (its uncertainty) >= 0;
- **TIDES CANNOT REACH** otherwise. Such a row counts against B, and RESULT.md states it first.
- Disclosed with every reach that needs r_J < r_1/2: stars then sit outside the tidal radius, so the system is not in the
  equilibrium the Wolf estimator assumes (SE2's admissibility A1 would remove it). The count stands as frozen.

Every row (LOW or not) whose primary r_J falls inside r_1/2 is listed.

## 4. Lane label

- **B HOLDS ON THE HOSTED ROWS:** every graded class (Coma UDGs, MW classical, MW ultra-faint, bright M31) reads B CONSISTENT
  on both footings and no LOW row reads TIDES CANNOT REACH on either footing.
- **B FAILS ON THE HOSTED ROWS:** at least one graded class FAILS (HIGH or LOW) on both footings, or at least one LOW row reads
  TIDES CANNOT REACH on both footings.
- **SPLIT:** anything else, with the cells printed.

## 5. Known answers (a failure stops grading; numbers printed in rb2.out)

- **KA1** X1 reproduced from the copied loader and build: every per-system Delta[Newton] equals x1_per_system.csv to 1e-9;
  Delta[iso AQUAL L*0] and Delta[v3 L*floor] through X1's committed stage tables (read as data) and the copied pred_draws
  to 1e-9.
- **KA2** XF1's C2 numbers from X1's CSV columns, XF1's boot_median and XF1's eps (xf1.json): MW classical +0.356 / +0.321
  (static) and +1.208 / +1.203 (moving); bright M31 +0.633 / +0.600 and +1.555 / +1.555; equal to xf1.json to 1e-9.
- **KA3** SE2 / XF1 Coma: the copied post_udg with the record's E and s_k gives se2.json's main +1.120 / +1.075 and half
  +1.121 / +1.076; with XF1's per-galaxy shifts (xf1.json) the half widths give +1.412 / +1.409; each to 1e-9.
- **KA4** B's law against the record's solver: the analytic isolated law gives S1's "S2 AQUAL isolated L*0 E-W" Coma mean
  (+0.3249 / +0.2855 dex) to 0.005 dex, and X1's per-system Delta[iso AQUAL L*0] medians to 0.01 dex (max over systems).
- **KA5** estimator and cut: r_J -> infinity returns the isolated law exactly; r_J -> 0 returns Newton exactly; the Newtonian
  Plummer E-W ratio equals X1's FW_N; the E-V virial integral in the deep isolated limit equals (4/81 G M a0)^(1/2) to 1e-3;
  a Newtonian point-mass satellite gives r_J = d (m / (3 M))^(1/3) to 1e-8; iso_1d at L* -> 0 equals the algebraic law at
  r_1/2 to 1e-3.
- **KA6** U1's DF2 / DF4 Newtonian (B0) residuals reproduced from U1's results JSON to 1e-6.

## 6. MUTATE (separate outputs rb2_MUTATE.out / rb2_MUTATE.json)

- **M1, external field back on (must return the law-alone shortfall):** B's isolated field replaced by the record's static
  external-field field (X1's emb_floor tables for the dSphs, S1's E_v3_dmean for Coma), no tidal cut, the rest of the pipeline
  unchanged. Bites iff it returns the law-alone numbers: Coma +1.120 / +1.075 (main) and +1.121 / +1.076 (half), MW classical
  +0.356 / +0.321, bright M31 +0.633 / +0.600, each to 1e-6.
- **M2, baryonic masses scrambled across dwarfs:** M* permuted within each class (20 fixed permutations; Coma within its 9),
  everything else unchanged. Bites iff, on both footings, the median over permutations of the rms of per-system B residuals
  about their class median, pooled over the four dSph classes, exceeds the unscrambled value. Per-class values reported.

## 7. What was seen before this freeze (not blind)

- Read in full: SE2's criteria and RESULT, XF1's criteria and RESULT, X1's README, the owner decision of 2026-11-09, and the
  code paths of S1, X1, SE2, XF1 and U1 named above.
- **Seen numbers that equal B where no tidal cut acts:**
  - X1's "iso AQUAL L*0" class medians: MW classical +0.28 / +0.24, MW ultra-faints +0.63 / +0.59, bright M31 +0.25 / +0.21,
    M31 others +0.64 / +0.59, LG field +0.05 / +0.02 (X1's own bootstrap statistic, not XF1's).
  - S1's isolated Coma rows: +0.325 / +0.286 dex.
  - U1's isolated (nu_e kernel) DF2 / DF4 residuals: -1.709 / -2.170 ln (canonical), -1.797 / -2.258 (alt); U1's Newtonian
    DF2 / DF4 mean +0.028 +- 0.539 ln.
- Also seen: X1's per-system lines for Crater II, Antlia II, CVn I and Sagittarius under the law with external field, and
  the law-alone class numbers quoted in the brief.
- **Not computed before this freeze:** any tidal radius from the record's data, any truncated B number, any pericentre.
- **Hand estimate (frozen, to be marked HIT / MISS):** Crater II's r_J at today's distance is about 2.6 kpc (outside
  r_1/2 about 1.4 kpc); a pericentre of 20 to 40 kpc (from memory of the literature, not from disk) would put r_J inside
  r_1/2. Coma UDGs: tides only lower B, so B's best is the isolated +0.33 / +0.29 dex; B CONSISTENT on the main widths.
  MW classical B CONSISTENT; bright M31 borderline; MW ultra-faints B FAILS HIGH; DF2 / DF4 LOW, reach uncertain.
  The brief's own estimate (Coma +0.2 to +0.5 dex; classical near zero with Draco and Ursa Minor high; low rows at risk) is
  noted, not used.

## 8. Limits stated now

- Spherical, isotropic, equilibrium Plummer dwarfs; Wolf estimator; mass follows light for the baryons; no gas term beyond
  the stellar mass the lanes used; an instantaneous tidal cut (no heating, no orbit-averaged stripping, no re-virialisation).
- The host masses are the lanes' conventions (flat V_c 200 / 230 km/s; Coma's hydrostatic beta model; NGC 1052's baryons
  under the law), not new measurements. No LCDM-calibrated quantity enters a graded row.
- The pericentres use the record's LVD kinematics and a flat-V_c host only; they are reported edges, not graded.

Compute: one thread, under 2 GB, minutes. Outputs: rb2.py, rb2.out, rb2.json, rb2_MUTATE.out, rb2_MUTATE.json, RESULT.md.
Any change after this freeze goes in an AMENDMENT_A#.md committed alone and labelled post hoc.

kappa = 1/2 FITTED; not theory closed. Relabels nothing.
