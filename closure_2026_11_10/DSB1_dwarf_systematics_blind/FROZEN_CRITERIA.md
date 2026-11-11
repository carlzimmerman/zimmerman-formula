# DSB1 frozen criteria: the hosted dwarf classes regraded against form B with a full systematics budget, frozen blind

Frozen 2026-11-10, committed alone, before any DSB1 script exists and before any DSB1 number is computed. TEST lane: it
relabels nothing, registers nothing, changes no frozen label of RB2, DG1, SE2, XF1, X1 or S1. Cold dark energy is a
gravitating field component, never a particle; no particle is added anywhere. Footings graded separately, never pooled:
canonical a0 = 9.3603e-11 m/s^2, alt a0 = 1.1312e-10 m/s^2.

Purpose: the record's deciding step "the dwarf classes regraded with a full systematics budget, frozen before the
numbers". RB2 graded form B on four hosted classes with measurement scatter only; DG1 put a budget on two classes after
RB2's numbers were known. DSB1 freezes the whole budget and the grading rule first.

## 0. What I had seen when freezing (blindness disclosure)

Opened, as allowed: RB2 FROZEN_CRITERIA.md lines 1-72 only; rb2.py lines 1-622 as code (loaders, classes, estimators,
form B, the cut, the edges, its known-answer code; I did not read lines 623-810 and did not run it); SE2
FROZEN_CRITERIA.md (all); the raw LVD tables (names, sigma, sigma errors, sigma upper-limit flags, M_V, log M*, r_h,
distance_host, HI columns, references printed as a list), the Freundlich+2022 Coma TSV (all 11 rows, including its
lgbar / lgobs columns, which are data-side accelerations, not form B), the Arroyo-Polonio table header and one row, the
Geha match table header, the McConnachie 2012 and Collins 2013 headers, the header of X1's x1_per_system.csv (no rows).
Accidentally seen: two rows of S1's s1_coma_per_galaxy.csv (DFX1 and J125848.94: E_v3_dmean 2.25 and 2.24 ln, which are
v3 residuals with the external field, not form B). No form B residual, class median or class interval was seen.
Seen through the project's notes before this lane started (one-line summaries, no tables): "DG1: RB2's high dwarf rows:
history does not close them (both footings; per-system signal absent, stellar-mass trend renamed); the two FAILS HIGH do
not survive SE2 budget + LVD sigma upper limits". So I know RB2 had two FAILS HIGH class rows and that DG1's budget
removed them; I do not know which classes, their sizes or their intervals. The hand estimates in section 7 are written
with that knowledge and say so.

## 1. Classes and rows

RB2's membership, copied (X1's klass, verbatim): LVD files lvd_dwarf_mw / m31 / local_field; a row enters if it has
vlos_sigma > 0, a half-light radius (rhalf_sph_physical, else rhalf_physical) and a stellar mass (mass_stellar, else
from M_V); LMC, SMC, M 32 excluded.

- **MW classical** (graded): Carina, Draco, Fornax, Leo I, Leo II, Sculptor, Sextans, Ursa Minor.
- **MW ultra-faint** (graded): MW host, not classical, not Crater II / Antlia II / Canes Venatici I / Sagittarius,
  M_V > -7.7.
- **bright M31** (graded): M31 host, not NGC 147 / 185 / 205, log M* >= 5.
- **Coma UDGs** (graded): Freundlich+2022 rows with R_e >= 1.5 kpc and 3e7 <= M* (= L x ML) <= 3e8 (S1 / CFG933's 9).
- Reported only, not graded: M31 others (log M* < 5), LG field (control: no host, B = isolated law), and the weak- and
  strong-tide readings of every class (section 2).

**Censored rows (dispersion upper limit only), rule fixed before looking at any value against B.** A row that RB2's
loader dropped because vlos_sigma is empty but vlos_sigma_ul is set (and that has r_h and M*) is classed by the same
klass rule and ENTERS its class statistic. Rule (main): in every Monte Carlo draw its dispersion is drawn uniform on
[0, sigma_UL] (the LVD limit read as the edge of a flat-in-sigma posterior); its residual is then computed like any
other row's, with its own distance and r_h draws, and it takes part in the bootstrap. Reported bounds (not graded): the
row fixed at sigma_UL (the highest the row can sit) and the row dropped (RB2's convention). Rows with neither a
dispersion nor a limit are not rows. Coma has no censored row.

## 2. The prediction: form B, RB2's definition, copied into dsb1.py (nothing imported)

Isolated law in a0 units g = nu(g_N) g_N, nu(y) = 1/2 + sqrt(1/4 + 1/y). Plummer stars of scale a = projected
half-light radius R_h (Coma: R_e), mass M_b; y = G M_b / (a^2 a0); g_N(r) = y r / (1 + r^2)^(3/2) (r in units of a).
Form B: g_B(r) = g_iso(r) for r <= r_J; g_B(r) = g_N(r) + [g_iso(r_J) - g_N(r_J)] r_J^2 / r^2 for r > r_J. Jacobi radius
r_J: the largest root of g_iso(r_J) / r_J = K, K = k G M_host(<d) / d^3 (in a0 / a units), by bisection in log r.
- Primary (graded): k = 3; MW / M31: M_host(<d) = V_c^2 d / G, V_c = 200 / 230 km/s, d = LVD distance_host (X1's
  Rh_X1 rule: field rows have no host); Coma: M_host(<d) = g_beta(d) d^2 / G, S1's beta model (kT 8.6 keV, r_c 276 kpc,
  beta 0.71, mu 0.6), d = dmean_kpc.
- Weak-tide edge (reported): k = 2 (MW, M31); k = 2 d^2 / (d^2 + r_c^2) for Coma.
- Strong-tide edge (reported): RB2's rule verbatim (MW with LVD proper motions: 16th-percentile pericentre in the flat
  200 km/s log potential from 500 draws over the LVD errors, astropy default Galactocentric frame, rJ = min(rJ at the
  pericentre, rJ primary); MW rows without proper motions and M31 rows: r_J / 3^(2/3), M31 also the projected distance
  from M31 if smaller; Coma: d_proj).
- Residual of a row: Delta = log10(g_obs / a0) - log10 g_B(r_1/2), g_obs = 3 sigma^2 / r_1/2, r_1/2 = (4/3) R_h (Wolf).
  This is dex in g, measured minus form B. RB2's dSph Delta and RB2's Coma E / ln 10 are the same quantity.
- No screening (L* = 0) in the graded prediction, as RB2's primary.

## 3. The budget

Nominal data side = X1's: sigma x b with b the Arroyo-Polonio 2026 "free binary fraction" factor sig_free / sig_f0 for
listed systems, the table median for unlisted M_V > -7.7 rows, 1 otherwise; M* at Upsilon_V = 2 (LVD); the Plummer
scale R_h. Every term below perturbs this nominal side. "Coherent" = one draw per class per Monte Carlo draw (does not
average down); "independent" = one draw per system per draw. Gaussian widths are 1 sigma. A looked-up value is marked
PROVISIONAL.

| # | term | what it does | prior | coh / ind | source |
|---|------|--------------|-------|-----------|--------|
| T1 | stellar M/L, class zero point | M* x 10^u | u ~ N(0, 0.30 dex) dSph; N(0, 0.20 dex) Coma | coherent | SE2 2.5 (record prior Upsilon_V 2, bracket 1-4 as +-1 sigma); Coma: S1 / CFG948 / SE2 2.6 |
| T2 | stellar M/L, system to system | M* x 10^u_i | u_i ~ N(0, 0.10 dex) | independent | stated rule: spread of old-population Upsilon_V over [Fe/H] -2.5 to -1 in SSP models; PROVISIONAL, no look-up made |
| T3 | luminosity error (incl. stochastic IMF sampling in faint systems) | M* x 10^(-0.4 dM_V) | dM_V split normal (LVD M_V_em / M_V_ep; 0.1 mag if missing) | independent | LVD; X1 did not carry it |
| T4 | gas | M_b = M* + 1.33 q M_HI | M_HI ~ U[0, 10^mass_HI_ul] (a measured mass_HI is used as is), q ~ U[0, 0.5]; rows with neither: 0 | independent | SE2 2.5 rule verbatim (QX23); Coma: NOT IN BUDGET (no HI on disk; gas would raise B and lower the residual) |
| T5 | distance, per system | D x 10^(dDM/5): R_h x f, M* x f^2 | dDM split normal (LVD distance_modulus errors; 0.1 if missing) | independent | X1's MC verbatim |
| T6 | distance zero point | as T5, common shift | dDM ~ N(0, 0.10 mag) dSph; Coma: D x 1.05^N(0,1) | coherent | dSph: RR Lyrae / TRGB zero-point scale, stated rule, PROVISIONAL; Coma: S1 / CFG948 / SE2 (one cluster distance, so coherent) |
| T7 | half-light radius | R_h x split normal | LVD rhalf errors (10 % if missing); Coma: R_e x 10^N(0, 0.04 dex) | independent | X1's MC; Coma: no per-galaxy error on disk, stated rule 10 %, PROVISIONAL |
| T8 | dispersion measurement error | sigma split normal | LVD vlos_sigma_em / _ep; Coma esig | independent | X1's MC / S1 |
| T9 | velocity-error floor | sigma^2 -> sigma^2 - w (floor at 0.01 sigma^2) | dSph: w ~ N(0, 1.3 (km/s)^2) | coherent (one spectrograph pipeline per class) | half the spread of published DEIMOS floors, (2.2^2 - 1.49^2)/2 = 1.31 (km/s)^2 (Simon & Geha 2007: 2.2 km/s; Kirby+2015: 1.49 km/s; 1.1 km/s dmost 2026): PROVISIONAL web look-up |
| T9c | Coma line-spread / resolution floor | as T9 | w ~ N(0, 90 (km/s)^2) | coherent | stated rule: instrumental sigma 30 km/s known to 5 % (2 x 30 x 1.5); PROVISIONAL, no look-up made |
| T10 | unresolved binaries | sigma x b | M_V > -7.7 rows: log b = log b_free + t (log b_f07 - log b_free) for t >= 0, log b_free (1 + t) for t < 0, t ~ U[-1, 1] (f0 ... free ... f0.7); other dSph rows with 4 <= sigma < 10 km/s: b = 1 / (1 + s), s ~ U[0, 0.30]; sigma >= 10 km/s and Coma: 0 | coherent (binary population common to a class) | Arroyo-Polonio+2026 table A1 (on disk); Minor+2010 (dispersions 4-10 km/s unlikely inflated by more than 30 %; arXiv version says 20 %), PROVISIONAL look-up, bracket read uniform by SE2's rule |
| T11 | membership / dataset choice | sigma x 10^m | m ~ N(0, m_c), m_c = sqrt(mu^2 + (rms / sqrt N)^2) of log10(sigma_LVD / sigma_alt) over the class's matched systems (Collins 2013 for M31; McConnachie 2012 for MW; zero sigma skipped; names lower-cased, spaces / brackets / dashes removed, "andromeda" -> "and"; fewer than 3 matches -> pooled over the three dSph graded classes); Coma: m ~ N(0, s_mem) dex in g, s_mem = |mean residual over all 11 - mean over the 9| | coherent | SE2 2.5 / 2.6 rules verbatim |
| T12 | mass-estimator coefficient (intrinsic) | g_obs x 10^e_i | e_i ~ N(0, log10 1.23 = 0.090 dex) | independent | Campbell+2017 (MNRAS 469, 2335): Wolf estimator ~23 % 1 sigma scatter, little bias, on APOSTLE satellites and field dwarfs; PROVISIONAL look-up |
| T13 | velocity anisotropy / estimator form | g_obs x 10^e | e ~ N(0, a_c), a_c = median over the class of |log10(sigma^2_vir / sigma^2_Wolf)| under B primary at central values (B's global virial dispersion of a Plummer tracer vs the Wolf local estimate: S1's E-V vs E-W) | coherent | SE2 2.5 / 2.6 rule, computed on B's prediction (no data) |
| T14 | departure from equilibrium | g_obs x 10^e_i | flagged rows only: e_i ~ N(0, 0.20 dex) | independent | flag = SE2's A1 or A2 fails (A1: R_h / r_J >= 0.375 with r_J = d (M_W / (3 M_host))^(1/3), M_W = 4 sigma^2 R_h / G; A2: (4/3) R_h / sigma > 0.1 x 2 pi d / V_c), at central values (censored rows at sigma_UL). Width: stated rule, Campbell's estimator scatter doubled (no amplitude on disk) |
| T15 | host mass | V_c x 10^v (Coma: g_beta x 10^v) | v ~ N(0, 0.04 dex) MW, M31; N(0, 0.08 dex) Coma | coherent per host | stated rule: 10 % in V_c, 20 % in the Coma hydrostatic mass; PROVISIONAL, no look-up made |
| T16 | Coma 3-D position | d ~ U[d_proj, 2 dmean - d_proj] | per galaxy | independent | stated rule replacing SE2's coherent s_pos (3-D positions are independent) |
| T17 | Coma aperture / tracer | sigma x 1.15^N(0,1) | | coherent | S1 / CFG948 / SE2 2.6 (s_A) |
| T18 | censored rows | section 1 | | independent | section 1 |

Terms considered and not in the budget, with sign: Coma gas (lowers residual if present); tidal heating of the stars
beyond T14 (raises sigma in flagged systems; T14 is symmetric); non-sphericity / projection (inside T12, Campbell's
scatter is measured on triaxial simulated dwarfs). The ellipticity choice (circularised R_h, X1's choice) is kept.

## 4. Statistic, interval, labels

Monte Carlo: N = 4,000 draws per class, footing and reading; seed per (class, footing, reading) fixed in the script.
Each draw: one draw of every coherent term; a bootstrap resample of the class's rows (with replacement, censored rows
included); one draw of every independent term per resampled slot; residual per slot; class statistic = the median over
the slots (dSph classes: XF1 / RB2's statistic) or the mean (Coma: SE2 / RB2's statistic). The class residual is the
median of the 4,000 statistics; the 95 % interval is their 2.5 / 97.5 percentiles.

- **B CONSISTENT** if the interval contains 0; **B FAILS HIGH** if it lies above 0 (data above B); **B FAILS LOW** if below.
- **Power rule.** Planted-offset mocks drawn with the same budget: a mock with class offset delta returns a statistic
  delta + (s_j - s_med), s_j one of the 4,000 statistics, and its interval is that statistic plus the main interval's
  offsets (q2.5 - s_med, q97.5 - s_med). P_detect(delta) = share of the 4,000 mocks whose interval excludes 0. The
  minimum detectable offset MDO = the larger over the two signs of the smallest |delta| (grid 0.01 dex up to 2 dex) with
  P_detect >= 0.8. **Frozen line: a class whose MDO > 0.30 dex (a factor 2 in g, the test must detect a planted 0.30
  dex offset with probability 0.8) reads NO POWER instead of B CONSISTENT.** A FAILS label stands whatever the power.
  The shift construction assumes the interval's shape does not change with delta; KA-c checks it with a full mock.
- Per class: the common label if the two footings agree, else SPLIT (canonical / alt).
- **Lane label** (graded classes, primary reading, both footings):
  - **HIGH ROWS STAND** if at least one graded class reads B FAILS HIGH on both footings (any FAILS LOW rows are named in
    the same line);
  - else **LOW ROWS** if at least one graded class reads B FAILS LOW on both footings;
  - else **HIGH ROWS DO NOT STAND** if no graded class FAILS on either footing and at least 2 graded classes read
    B CONSISTENT on both footings;
  - else **NO POWER** if no graded class FAILS on either footing (fewer than 2 classes with power);
  - else **SPLIT** (a FAILS on one footing only).
- Reported beside the label, not graded: the censored-row bounds, the weak and strong readings, the equilibrium-flagged
  rows dropped (SE2's NOT A TEST rule), the budget-off class numbers in RB2's convention (XF1 boot_median over X1-built
  per-system medians and sds; Coma mean E with CFG933's se), and the per-term width table: the 95 % width with each term
  removed in turn and with each term alone.

## 5. Known answers (a failure stops grading; the result says where it stopped)

- **KA-a** Budget off reproduces X1: the X1 build copied verbatim (seed 20261031, same call order, NMC 2,000) with the
  Newtonian prediction gives, per system and footing, the median and sd of Delta[Newton] in x1_per_system.csv to 1e-9
  (per-system columns only; no class summary read). Also the deterministic central-value residual of my own residual
  function (no MC) against X1's medians: median |d| <= 0.01 dex, max |d| <= 0.06 dex.
- **KA-b** The estimator on Fornax (LVD sigma 12.1 km/s, R_h 695 pc): M_1/2 = 3 sigma^2 r_1/2 / G against Campbell+2017's
  reproduction of the Wolf estimator, log M = 7.88 (R_h 714 pc; PROVISIONAL look-up): |d| <= 0.15 dex; and against LVD's
  own mass_dynamical_wolf for Fornax: |d| <= 0.05 dex.
- **KA-c** Planted offset recovered: a mock catalogue whose dispersions are set so that every row sits at B primary
  (nominal values) times 10^delta, delta = +0.40 dex, every class, both footings: budget off returns delta to 1e-6; the
  full budget MC returns a class residual within 0.10 dex of delta. Also form B's limits (r_J -> inf gives the isolated
  law exactly; r_J -> 0 gives Newton to 1e-12; deep-MOND Wolf ratio).

## 6. Mutations (separate outputs dsb1_MUTATE.json / .out), all must bite

- **M1** T1 (class M/L zero point) removed: the 95 % width narrows in every graded class, both footings.
- **M2** a0 doubled: every graded class residual moves down (B rises with a0), both footings.
- **M3** planted offset delta = +0.60 dex in the mock of every graded class: reads B FAILS HIGH in every class whose MDO
  is <= 0.60 dex.

## 7. Hand estimates, before any number (written knowing only that RB2 had two FAILS HIGH rows and DG1 removed them)

- The coherent M/L term alone gives the dSph classes a 95 % half width of about 0.3 dex in g where tides have cut B back
  towards Newton (g ~ M) and about 0.15 dex where B is the deep isolated law (g ~ sqrt M); binaries and the floor add
  0.05-0.15 dex for the ultra-faints; the class width should land at 0.3-0.6 dex half width.
- MW ultra-faint: residual + 0.3 to + 0.6 dex (strong cuts at small d, small sigma), MDO 0.3-0.5 dex: borderline,
  FAILS HIGH or NO POWER; censored rows pull it down by ~0.05-0.1 dex.
- MW classical: residual 0 to + 0.2 dex, B CONSISTENT, MDO ~ 0.3 dex (borderline power).
- Bright M31: residual -0.1 to + 0.2 dex, B CONSISTENT with power (25 rows).
- Coma UDGs: residual + 0.2 to + 0.4 dex, interval about +-0.3 dex: borderline, CONSISTENT or FAILS HIGH.
- Lane: HIGH ROWS DO NOT STAND or NO POWER most likely; HIGH ROWS STAND if the ultra-faint offset is above ~0.5 dex.

## 8. Run rules

One thread, nice -n 19, fixed seeds, outputs small (dsb1.json / dsb1.out, dsb1_MUTATE.*), no large arrays on disk;
paths built from the script's own location. Order: this file committed alone; then the script and the blind result
(RESULT_BLIND.md) committed before RB2's or DG1's results are opened; then RESULT.md with the comparison. A label does not
move after RESULT_BLIND.md; an error found later goes into a dated amendment committed alone, with both readings.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
