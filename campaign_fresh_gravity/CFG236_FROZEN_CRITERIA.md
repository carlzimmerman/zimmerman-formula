# CFG236 -- Referee re-derivation of CFG198 + CFG199 (MUSE-DARK per galaxy: a0(z) at R_e, route (i) fitted masses vs route (ii) SED M* + H2). FROZEN CRITERIA (phase 1)

Written before any CFG236 script exists and before any number of mine has been computed. The CFG198 / CFG199 README numbers below are TARGETS I read, not blind predictions; my hand estimates (section 5) were made AFTER reading both READMEs and both frozen-criteria files, and are scored in the final README. kappa = 1/2 is FITTED, not derived. a0(z) FLAT is the framework's distinctive law; a0 proportional to H(z) is the rival. Nothing here says the data favour any law or that the theory is closed; a lean is not a detection; a failed control or a wrong expectation is kept, never repaired.

## 0. What I read, what I did not, and what I saw

READ (phase 1): `CFG198_musedark_pergalaxy_a0z/FROZEN_CRITERIA.md` (d5a73127b) and `README.md` (e9a92352d, with its appended correction after CFG199); `CFG199_musedark_level_pressure/FROZEN_CRITERIA.md` (997e5047a) and `README.md` (8edd82c3e); `data_assembly/musedark_catalogues/`: `README.md`, `NUMERIC_SET_2026-09-29.md`, `PER_GALAXY_LISTING_2026-09-29.md`, `PILOT_ID0003_2026-09-29.md`, `checks.txt`, `checks_numeric.txt`, `duplicated_rows.json`; the CSV header of `musedark_numeric.csv` and its line count (40 columns, 126 data rows; no row read); the directory listing (names only) of the data chat's external folder; `CFG233_rc100_referee/README.md` and `CFG234_cristal_referee/README.md` (for form and lessons); `closure_map/WHAT_WOULD_DECIDE_2026-09-29.md`.

NOT opened: any `*.py`, `.out`, `.json`, firstrun/secondrun or MUTATE file of CFG198 or CFG199; CFG190; CFG4_common; CFG90; the papers. Opened in phase 2 only after my own main and MUTATE runs are saved: CFG198's and CFG199's scripts and outputs (comparison is then post-run and labelled). One exception I declare now (section 2): CFG4_common's FP1 table is needed for nu_mono and is opened only for the labelled "import" row, never for the primary.

Numbers I saw in the documentation (so they cannot count as blind): ID0003 (muse_id 3): z = 0.6217, v from -145 to +154 km/s, sigma 49 -> 38 km/s, v22 = 149.4, fDM(R_e) = 0.76, DC14 log M_disk 10.11 against photometric 10.08, gas density 10.56 (95% 0.88 to 14.83), log_Mdyn 10.41; the data chat's summaries (Delta* median -0.14, 16-84% -0.67..+0.42, n = 124; HI upper 95% limit >= 14 for 117 of 126; true_Vrot reach median 6.8 R_e; v_table/v22 median 0.69, 0.87 after dividing by sin i, r = 0.57 with sin i; "v_AD^2/v_c^2 about 0.52 at 2.2 R_d" as inferred); the two duplicate rows of id 26 in the DC14 halo file (V_vir 141.03 / log_X -2.473 and V_vir 103.41 / log_X -2.009). No CSV data row was read.

## 1. Headline under test (pinned; README numbers are TARGETS)

"MUSE-DARK III's published a0 rise travels with its DC14-fitted masses. With SED M* + H2 the slope is about -0.2 +- 0.5; the fitted-minus-SED mass drift is -0.72 dex/z."

Pinned components (slopes in dex per unit z; Theil-Sen; 95% bootstrap CI over galaxies, 10,000 resamples):

| id | quantity | target | lane |
|---|---|---|---|
| T1 | Delta* = log M_fit - log M*_SED against z (n = 109) | -0.723 [-0.966, -0.498]; median -0.112 | CFG198 |
| T2 | Delta* - log(1+mu_mol) against z | -0.868 [-1.107, -0.616]; median -0.512 | CFG198 |
| T3 | route (i) b_i, CFG198 geometry, n = 108 | +0.789 [+0.514, +1.071] | CFG198 |
| T4 | route (ii) b_ii, CFG198 geometry, n = 85 (D <= 1.05: 9 low-z, 15 high-z) | -0.041 [-0.467, +0.360] | CFG198 |
| T5 | route (iii) b_iii, n = 99 | +0.075 [-0.233, +0.349] | CFG198 |
| T6 | paired Delta b = b_ii - b_i, n = 84 | -0.939 [-1.261, -0.633]; b_iii - b_i (n = 98) -0.693 [-0.931, -0.480] | CFG198 |
| T7 | reference slopes over the analysed z | flat 0; E(z) +0.258; III's law +0.298 | CFG198 |
| T8 | robustness rows of b_ii: Sigma_HI = 0 -0.182 (excludes E(z) and III's law); Sigma_HI = 15 +0.106; mu x0.5 -0.011; mu x2 -0.202 (excludes III's law); nu_RAR -0.040 | CFG198 |
| T9 | CFG198 level (z about 0.52, lowest third, routes i / ii / iii): -9.65 / -9.69 / -9.38 | WITHDRAWN by CFG199; I reproduce it as arithmetic only |
| T10 | CFG199 (model's own v at R_e), reading (a) / (b): b_i +0.65 [+0.25,+1.08] / +0.63 [+0.25,+1.00]; b_ii -0.20 [-0.74,+0.36] / -0.22 [-0.77,+0.30]; Delta b -1.03 [-1.32,-0.75] / -1.03 [-1.34,-0.74] | CFG199 |
| T11 | CFG199 level, lowest-z third, route (i): (a) -10.38 [-10.71, -10.12] (below both footings); (b) -10.14 [-10.45, -9.94] (consistent with both) | CFG199 |
| T12 | CFG199: in (b) route (ii)'s CI upper end +0.297 sits below III's +0.300 (excludes III's law "only just"); rho(v_perp / v_c,CFG198, sin i) = +0.40 (a), -0.01 (b); share s median 0.84 (a), 0.75 (b) | CFG199 |
| T13 | III's published law as quoted in CFG198's criteria (from CFG190; NOT verified by me, I have not read III): a0(z) = a0(0) + a1 z with a0(0) = 1.0 +- 0.04 and a1 = 1.59 +- 0.10 (x 1e-10 m s^-2) | quoted |

What CFG199 withdrew and why: CFG198's "against interest" level statement (a0 at z about 0.5 is 0.25-0.65 dex above both footings in every route). CFG198's g_obs was D x (thin-exponential-disc g_bar); the model's own v at R_e gives a g that is 3-7 times smaller (median log10 ratio -0.75 in reading (a), -0.49 in (b)). The level was a property of CFG198's geometry scale. CFG199 states the slope findings stand (route (i) rises, route (ii) not significantly rising, Delta b < 0). It also records the route-(i) "closure" (R0) that CFG198 missed by overshooting now passes.

## 2. What is re-derived, and where independence STOPS

Re-derived fresh with my own code: the loader and the sample chain; the thin exponential disc and HI geometry; mu_mol; the kernels nu_RAR and P2 and the inversion; the a0 per galaxy on each route; Theil-Sen; the bootstrap (my seeds); the reference slopes; every attack and the MUTATE controls; the four-reading test of the velocity column; the partial-regression and mass-bias grids.

Independence STOPS at:
1. **The numeric set** `musedark_numeric.csv` (the data chat's parse of the MUSE-DARK DC14 run files; every definition "as read, unverified against the papers' PDFs"). I use the same 126 rows. Any parsing error in it is shared. I check what I can internally (duplicated ids, id 26 against the two duplicate rows, rad_kpc vs Re_kpc, column finiteness), not against the papers.
2. **Model outputs, not measurements.** MEASURED columns: z, pixscale_arcsec, kpc_per_arcsec, logMstar_phot (SED). MODEL-VALUE columns (posterior medians of one GalPaK3D DC14 fit per galaxy): DC14_logMdisk (+err), DC14_log_X, DC14_logMvir, logMdyn, fDM_at_Re, v22, Re_kpc (the fitted radius), incl_deg, sersic_n, sigma_fit_kms, gas_density (+lo95, +hi95), Vvir, the rotation-curve and dispersion tables. So g_obs (from fDM and v) and every "g_bar,i" are model outputs of one analysis; the test cannot tell a z-dependent a0 from a z-dependent model prior, pressure term, inclination, or decomposition (the CFG233 / CFG234 lesson). Only the SED M* and z are measured, and the SED M* is a model-dependent SED fit.
3. **nu_mono** (the user's 09-26 kernel, CFG4_common's FP1 table). My primary kernel is nu_RAR (McGaugh-type, y = g_N/a0, nu = 1/(1 - exp(-sqrt y))); the README says its nu_RAR row reproduces the nu_mono primary to 0.001 in b_i, b_ii and Delta b, which I treat as a further target (kernel independence). nu_mono is added as a separately labelled "import" row from CFG4_common, with agreement of nu_mono(y) against the imported object not claimed. The P2 kernel nu = sqrt(1 + a0/g_N) is a one-liner (mine).
4. **mu_mol** is taken as the formula written in CFG198's criteria ("as coded in CFG90"): log10 mu = 0.06 - 3.3 (log10(1+z) - 0.65)^2 - 0.41 (log10 M*_SED - 10.7), log10 throughout (the natural-log reading is reported as a sensitivity row, not a pass line). A check that this reproduces the README's separation between T1 and T2 (the difference of the two slopes is the slope of log10(1+mu), target 0.145) is a pass line. I have not seen CFG90.
5. **The 25-row true_Vrot.dat files and run/model text files** live OUTSIDE the repo (a sibling `_external_data/muse_dark/numeric/` of the repo, 882 files, sha256 in the repo's `numeric_manifest_sha256.txt`). The CSV does not contain v(R_e) or sigma(R_e). Everything in CFG199 and my attack (b) that needs v at R_e needs them. **Scope question for the orchestrator (phase 2): may I read them?** They are no-network, already-downloaded, hash-checked data, but not "in the repo". Rows marked [DAT] below are run only with a yes; without it they are reported NOT RUN, and the CSV-only rows always run.
6. The III paper (arXiv:2604.22613) and MUSE-DARK I (2506.19721) are read only through the data chat's and CFG198's summaries (unverified). The asymmetric-drift prescription (Dalcanton and Stilp 2010; alpha = 0.92; v_AD^2 = alpha sigma^2 r/r_d) is quoted, not checked.

## 3. My definitions (frozen; geometry and constants as stated in CFG198's criteria, re-implemented by me)

**Sample S:** rows with finite z, logMstar_phot, DC14_logMdisk, fDM_at_Re, Re_kpc, gas_density_Msun_pc2; has_bulge = 0; 0 < fDM_at_Re < 1. Report the count at each step. Target chain 126 -> 124 -> 14 bulge set aside -> 110 -> 109 (the frozen criteria say 15 bulge galaxies in 126, the README sets aside 14 of the 124; I report both counts).

**Two constructions (kept separate, never pooled):**
- **R198** (CFG198's): geometry g_disc(M,R) = v^2/R with v^2 = (2GM/R_d) y^2 [I0(y)K0(y) - I1(y)K1(y)], y = R/(2 R_d), R_d = R_e/1.678, evaluated at R_e; g_HI = pi G Sigma_HI with Sigma_HI = gas_density (posterior median); route (i) g_bar,i = g_disc(10^DC14_logMdisk) + g_HI, D_i = 1/(1 - fDM), g_obs = D_i g_bar,i (held fixed in all routes); route (ii) M_ii = M*_SED (1 + mu_mol), g_bar,ii = g_disc(M_ii) + g_HI, D_ii = g_obs/g_bar,ii; route (iii) M_iii = M*_SED. G = 4.30091e-6 kpc (km/s)^2 / Msun; 1 (km/s)^2/kpc = 3.2408e-14 m s^-2.
- **R199** (CFG199's) [DAT]: v_f(R_e) = mean over the two sides of |v_kms| at |rad_Re| = 1 (linear interpolation; one side if only one reaches); reading (a) v_perp = v_f; (b) v_perp = v_f / sin i; g_perp = v_perp^2/R_e; route (i) g_bar,i = (1 - fDM) g_perp, D_i = 1/(1 - fDM); route r in {ii, iii}: g_bar,r = g_bar,i x rho_r with rho_r = [g_disc(M_r) + g_HI]/[g_disc(M_fit) + g_HI] (the R198 thin-disc baryon ratio), D_r = g_perp/g_bar,r.
- **a0 per galaxy:** a0 = g_bar / y*, with nu(y*) = D, defined only for D > 1.05 (counted per z-half and route otherwise); a0 is an upper bound when D <= 1.05.
- **z-thirds:** equal-count terciles of the route-(i) galaxies' z.
- **Slope:** Theil-Sen of log10 a0 on z (pairs with dz = 0 excluded). CI: 10,000 bootstrap resamples over galaxies, seed 236 (second seed 237), percentile 2.5 / 97.5; the SD is the ddof-0 bootstrap SD. Paired Delta b on galaxies defined in both routes, bootstrap resampling the pairs.
- **Reference slopes:** OLS slope of log10 L(z) on z over the analysed galaxies' own z, for L = 1 (flat), L = E(z) = sqrt(0.315 (1+z)^3 + 0.685) (the rival a0 proportional to H(z)), L = 1 + 1.59 z (III's law as quoted in CFG198). Footings: a0 = 9.3603e-11 (canonical) and 1.1312e-10 (alt); log10 = -10.0287 and -9.9465.
- **Classification of a slope against a law:** INSIDE if the law's slope lies in the 95% CI, OUTSIDE if not; also the signed distance in bootstrap SD. Words: "excludes" only for OUTSIDE; |distance| between 1 and 3 SD is a LEAN, >= 3 SD would be called a detection of a difference from that slope, and only as a statement about this analysis's route, never about a law.

## 4. Structural algebra fixed before any number (the predictions the runs can contradict)

Let g_obs be held fixed and D = g_obs/g_bar. Then ln a0 = ln g_bar - ln y*(D), and with eta = -d ln nu / d ln y at y*:

- **S(D) = d ln a0 / d ln g_bar |_{g_obs} = 1 - 1/eta.** Deep regime (eta -> 1/2): S = -1. P2 kernel: 1/eta = 2D^2/(D^2-1), so S = -(D^2+1)/(D^2-1), magnitude 1 at D >> 1 and diverging as D -> 1. So a mass error enters a0 with gain |S| >= 1, larger where baryons nearly account for the total (the ill-conditioned rows, which are exactly route (ii)'s rows).
- **A gas error enters only through the gas share of g_bar:** delta ln g_bar = f_HI delta ln g_HI with f_HI = g_HI/g_bar; a stellar (plus H2) mass error through f_d = 1 - f_HI. With M_ii = M*(1+mu) and mu proportional to M*^(-0.41): d log M_ii / d log M* = 1 - 0.41 mu/(1+mu).
- **Route contrast is arithmetic.** b_ii - b_i is the z-trend of rho = M_ii/M_fit (attenuated by f_d) times the gain S. From the targets, (S f_d) x 0.868 = 0.94 to 1.03 implies the effective gain S_bar f_d about 1.1-1.2. So reproducing T6 tests only that the same arithmetic is coded; the physics content is entirely WHICH MASS (section 9).
- **In R199, routes (i), (ii), (iii) all scale exactly as g_perp at fixed D_i and rho_r** (a0,r = rho_r g_bar,i / y*(D_i/rho_r), g_bar,i proportional to g_perp). Hence any change in how v(R_e) is read (reading (a) vs (b), drift term on or off) moves b_i, b_ii and b_iii by the SAME amount (the z-trend of the multiplicative change of g_perp) and leaves Delta b unchanged (to numerical precision); the level moves by the full factor. The SED-M* / fitted-mass question is therefore independent of attack (b) in the slope difference, but not in the level. This is a prediction I can fail.
- **Route (i) in R199 does not use M_fit at all** (only fDM, v, R_e); M_fit enters only through rho. "III's rise travels with the fitted masses" therefore means: the rise is in fDM(R_e) and g_perp (model outputs from the fit that also produced M_fit), and swapping in a different baryon mass at the same total removes it.
- In the deep regime ln a0 = 2 ln g_obs - ln g_bar; a slope b_i = 2 s_obs - s_bar, where s are the z-trends of log g_obs and log g_bar (reported as a decomposition).

## 5. Hand estimates (made after reading the READMEs; labelled; probabilities that MY result lands inside the pass line of section 6)

| est | statement | my estimate | P(reproduces) |
|---|---|---|---|
| H1 | sample chain 126/124/14/110/109 exact; n = 108 / 85 / 99 / 84 / 98 | I expect exact on the first, not more than one off on each of the others | 0.85 / 0.55 (all four exact) |
| H2 | T1 -0.723 within 0.03 (on S, n = 109; on the 124-row set it would differ) | Delta* slope about -0.72 | 0.75 |
| H3 | T2 -0.868 within 0.03 (slope of log10(1+mu) = +0.145) | | 0.65 |
| H4 | b_i (R198) +0.79 within 0.05 | | 0.70 |
| H5 | b_ii (R198) -0.04 within 0.05 | | 0.60 |
| H6 | Delta b -0.94 within 0.05 | | 0.55 |
| H7 | b_i (R199) +0.65 / +0.63 within 0.05 [DAT] | | 0.70 |
| H8 | b_ii (R199) -0.20 / -0.22 within 0.05 [DAT] | | 0.55 |
| H9 | R199 levels within 0.05 of -10.38 / -10.14 [DAT] | | 0.65 |
| H10 | CI edges within 0.05 of the README edges (each, info) | mine will be 0.01-0.04 off | 0.60 per edge |
| H11 | flat inside route (ii)'s CI in every row of my main and gas grid | | 0.90 |
| H12 | E(z) and III's law inside route (ii)'s primary CI | | 0.85 |
| H13 | route (i)'s CI excludes flat (lower edge > 0) | | 0.95 |
| H14 | III-law closure on route (i): R199 route (i) CI contains +0.298 | | 0.85 |
| H15 | tau* (the z-dependent SED-mass bias needed to bring b_ii up to b_i) | about +0.85 dex/z (range 0.6-1.2): SED masses too heavy at high z by roughly 0.9 dex per unit z | P(tau* > 0.4) = 0.92; P(tau* <= 0.25) = 0.03 |
| H16 | drift term ON (alpha = 0.92 with the file's sigma) | b_i and b_ii rise together by +0.04 to +0.15; Delta b moves < 0.03 | 0.80 |
| H17 | best-fitting reading of the file's v at 2.2 R_d against v22 | (c) projected + drift 0.45; (b) projected alone 0.25; (a) v_perp alone 0.20; (d) v already v_c 0.10 | -- |
| H18 | Delta* slope stays <= -0.4 after controlling log M*_SED (and in M* terciles) | | 0.65; shrinks to |.| < 0.25: 0.12 |
| H19 | slope beta of log M_fit on log M*_SED is below 0.8 | about 0.3-0.7 (regression dilution of a prior-free fit) | 0.65 |
| H20 | rows with prior-dominated gas (hi95 >= 14 and lo95 < 1) in S: between 98 and 106 | | 0.65 |
| H21 | half-range of b_ii over the declared gas grid (attack d) below 0.11 (contained in the bootstrap +-0.4-0.5) | | 0.45; 0.11-0.45 0.45; > 0.45 0.10 |
| H22 | censoring bracket keeps b_ii within [-0.6, +0.5] | | 0.80 |
| H23 | error-propagation MC through the tabulated errors shifts b_ii by < 0.10 and raises the SD by >= 1.2x | | 0.70 / 0.55 |
| H24 | linear-law anchor: B/A of a linear Theil-Sen on route (i) within 2 SD of 1.59 (III's quoted ratio) | | 0.50 |
| H25 | the route-(i) level at the lowest-z third sits > 0.3 dex below III's quoted law at that third's median z | | 0.75 |
| H26 | id 26: one row in the CSV; its V_vir and log_X match one of the two duplicate rows (which one unknown) | | 0.90 |
| H27 | leave-one-out max change: |d b_i| < 0.05 and |d b_ii| < 0.10 | | 0.75 |
| H28 | enclosed-mass overshoot fraction of SED + H2 baryons against M_dyn(<R_e) is larger in the high-z half than in the low-z half | | 0.75 |
| H29 | in reading (b) my route-(ii) CI upper edge is below +0.300 (the README's "only just") | this edge is a coin flip | 0.45 |

## 6. Pass lines (frozen; slopes within 0.05, drift within 0.03 dex/z, N exact)

PASS = my value within the stated tolerance of the target. Nothing is tuned after the run.

- **N (exact):** chain counts 126, 124, 14 (bulge among the 124; 15 among the 126), 110, 109; n(i) 108, n(ii) 85, n(iii) 99, paired 84, 98; D <= 1.05 counts per z-half 9 and 15 (route ii). Any difference is reported with the row that caused it.
- **Drift (0.03 dex/z):** T1 slope -0.723 and T2 -0.868; the medians -0.112 and -0.512 within 0.01 dex.
- **Slopes (0.05):** T3, T4, T5, T6 (R198) primary (nu_RAR); T7 reference slopes within 0.005; T8 rows; the nu_RAR row equals the primary to 0.005 (kernel independence); T10 (R199, both readings) if [DAT] allowed.
- **CI edges:** reported against the README edges, PASS within 0.05 (info, not load-bearing).
- **Classes (exact):** R1 sets (which of flat / E(z) / III's law lie outside b_ii's CI) in the primary row and in each robustness row of T8: primary none; Sigma_HI = 0: E(z) and III's law; Sigma_HI = 15: none; mu x0.5: none; mu x2: III's law; nu_RAR: none; route (iii): none.
- **Levels (0.05):** T9 (reported as arithmetic of a withdrawn statement), T11 [DAT], with L1 class: (a) below both footings (upper edge < -10.029), (b) consistent with both.
- **Structural predictions (section 4):** drift on/off and reading (a)/(b) move b_i, b_ii, b_iii by the same amount within 0.02 and Delta b by < 0.03; a hole in this is a failure of CFG199's route construction to be scale-free and is kept.

## 7. MUTATE controls (each flips a load-bearing cell; MUTATE exits 1 when the control bites, 0 when it does not; main exits 0)

| M | mutation | load-bearing cell flipped | predicted bite (frozen) |
|---|---|---|---|
| M1 | inject a known slope: g_perp (R199) or g_obs (R198) x 10^(0.30 (z - z_med)) at fixed fDM | b_i, b_ii, b_iii | each rises by 0.300 +- 0.03 (g_obs fixed by the model's D, so a0 scales linearly); Delta b unchanged within 0.02 |
| M2 | swap the routes: rho -> 1/rho (route "ii" gets the fitted mass and route (i) the SED + H2 mass) | sign of Delta b | Delta b changes sign (predicted to about +0.6 to +0.95; not exactly -T6 because of the nonlinear gain) |
| M3 | shift the SED M* by a known z-dependent bias: log M*_true = log M*_SED - tau (z - z_med), tau = +0.72 | b_ii, Delta b | Delta b returns within 0.35 of 0 (at least 65% of the gap closed); b_ii rises to within 0.40 of b_i |
| M4 | drop / add the drift term (drift ON with alpha = 0.92, sigma from the file at R_e) [DAT; if not allowed: multiply g_perp by the mean-z-dependent factor (1 + 0.1 (z - z_med)) as a stand-in and label it] | b_i and b_ii together | both move by the same amount (|diff| < 0.02); Delta b moves < 0.03; level moves; bites if b_i moves >= 0.03 |
| M5 | null: shuffle the regression axis only (a0 and mu at the true z), and separately shuffle z in both axis and mu | all slopes | every |b| < 2 bootstrap SD, T1 slope consistent with 0 after the axis shuffle; CFG233's lesson applies (mu_mol depends on z, so the both-shuffle may not go to zero: kept if it does not) |
| M6 | mirror z -> -z (z_med reflected) | antisymmetry | every Theil-Sen slope changes sign to 1e-10; bites |
| M7 | change the D <= 1.05 floor to 1.5 | n, b_ii | n(ii) drops by >= 10; reported |

The MUTATE exit code convention: bite = exit 1. Frozen expectations that turn out wrong are kept in the final README.

## 8. Attacks, with frozen procedures and what pass or fail means

Seeds: bootstrap 236 (10,000) for every pass-line CI; 237 as the stability check (the class and sign of every main row must agree; a flip is reported); grid attacks 2,000 resamples with seed 2360 + attack index (a=0, b=1, c=2, d=3, e=4, f=5); Monte Carlo draws below with seed 2365.

**(a) Reproduction.** Sections 3 and 6, R198 for certain, R199 [DAT]. Also the slope decomposition b = 2 s_obs - s_bar (s = Theil-Sen slopes of log g_obs and log g_bar on z) per route. PASS = the pass lines; any miss is classified (definition / numerical / README typo / framing) as in CFG233.

**(b) The velocity column and the drift term.** What the numeric set contains: the CSV has v22, sigma_fit_kms, incl_deg, sig_at_centre, sig_at_maxR_pos/neg, v_at_maxR_pos/neg, maxR_over_Re_pos/neg, logMdyn, Re_kpc; the 25-row profiles are in the .dat files. Procedures:
- B1 [DAT]: per galaxy, v_f at R = 2.2 R_d = 1.311 R_e (two-side average), compared with v22 (derived; the model's v_c, reading v22 as v_c at 2.2 R_d, A3 unverified), under four readings: (a) v_perp, predicted ratio sqrt(1 - s_AD); (b) projected, predicted ratio sin i; (c) projected + drift, predicted sin i x sqrt(1 - s_AD); (d) already v_c, predicted 1. s_AD = 0.92 sigma_f(2.2 R_d)^2 (2.2) / v22^2 (alpha = 0.92, r/r_d = 2.2, sigma from the file); a second drift (D2: thick disc, sigma = 0.15 v_c (h_z/r with h_z = 0.15 R_e), s_AD = 0.92 x 0.15^2 x (R/r_d)) is run as the alternative. Score: median and MAD of log10(observed/predicted) per reading, and the slope of the residual against log sin i (should be 0 for the correct reading). Frozen decision: the reading with the smallest median |residual| whose residual slope against log sin i is consistent with 0 (95%, 2,000 bootstrap) is "best supported"; a tie within 0.03 dex is "not separated".
- B2 [DAT]: Spearman rho of v_f/v_c against sin i for three comparators of v_c: CFG198's reconstruction sqrt(g_obs,198 R_e) (as CFG199 did; its scale is withdrawn), v22, and v_dyn = sqrt(G M_dyn / R_e) from logMdyn (reading log_Mdyn as the total mass within R_e, consistent with ID0003: (1 - fDM) M_dyn about half the disc mass; UNVERIFIED). CFG199's L3 uses the first comparator, which inherits CFG198's broken scale; I report whether the verdict (b) survives the other two.
- B3 [DAT]: slopes b_i, b_ii, b_iii and Delta b in the 2 x 2 (reading a, b) x (drift off, drift D1) and D2, R199. Predicted (section 4): b's move together, Delta b fixed within 0.03. PASS means the prediction holds; failure means the route factors are not scale-free somewhere.
- B4 (CSV only, always run): the same ratio test at the outermost row using v_at_maxR, sigma_at_maxR, R = maxR_over_Re x R_e with v_c taken equal to v22 (flat curve; stated approximation, weak) for the four readings.
- B5: the level under each reading and with the drift on (how far the R199 level statement moves); class L1 per reading. A level is reported against the footings, never graded.
- PASS / FAIL meaning: if reading (a) is best supported then CFG199's "(b) is better supported" is wrong-footed; if (c) is best, both CFG199 readings are lower bounds on g and the drift-on rows replace them; in every case the slope difference Delta b should not move.

**(c) Which mass is right.** List first (frozen): independent M*-type estimates in the repo for these galaxies, from the documentation: (1) `logMstar_phot` (SED; measured side, but model-dependent), with its error in `musedark_joined.csv` (an extra file I will use only for this row and label); (2) DC14 fit `DC14_logMdisk` (+err) and `DC14_log_X`, log_Mvir (fit outputs, no SED prior; quoted to include molecular gas); (3) the baryons-only fit's log_Mdisk and log_Mgas in `musedark_joined.csv` (no halo: an upper bound on the baryons the dynamics can tolerate); (4) `logMdyn` (derived dynamical mass); (5) the SFR in `musedark_joined.csv`. First action of phase 2: a filename/column grep of the repo for any other mass catalogue of these ids (UDF / MUSE-DARK / muse_id); if none, the list above is the whole list and I say so. I do not invent any independent estimate; literature relations quoted below are "from memory, unverified".
- C1 algebra: measure S(D) and f_d per galaxy (quantiles by route), and the gain from a mass error.
- C2 bias grid (frozen, 9 cells): tau in {-0.4, -0.2, 0, +0.2, +0.4, +0.6, +0.8, +1.0, +1.2} dex/z with log M*_true = log M*_SED - tau (z - z_med), applied to the SED mass in routes (ii), (iii), plus a constant offset in {-0.3, 0, +0.3}; also an H2-only bias (mu x 10^(t_H (z - z_med)), t_H in {-0.6, -0.3, 0, +0.3, +0.6}). Report b_ii(tau), Delta b(tau); tau*_i = the bias at which b_ii equals b_i (route (i)'s own slope), tau*_III = the bias at which b_ii equals +0.298 (by linear interpolation of the grid; if the grid does not bracket it, "not reached"). Also the combined M* and gas bias needed.
- C3 confound (Malmquist / regression dilution): slopes of log M_fit, log M*_SED, Delta* on z separately; beta = slope of log M_fit on log M*_SED (OLS and the errors-in-variables check with the quoted 0.32 dex median error); the partial slope of Delta* on z with log M*_SED - 9.24 as covariate (OLS, 2,000 bootstrap) and Theil-Sen of Delta* on z within M*_SED terciles; the same partial slopes for log a0,i and log a0,ii.
- C4 enclosed-mass overshoot (W3): (1 - fDM) M_dyn = the model's enclosed baryon mass at R_e; compare with 0.5 M_r + pi R_e^2 Sigma_HI (disc half mass inside R_e for an exponential disc; A1) for r in {fit, SED + H2, SED}; fraction exceeding M_dyn (an impossibility) per z-half with binomial intervals; also the R198 statistic D_r <= 1.05. This is the only test here that can reject a mass from the data side: heavier-than-total is impossible, lighter is not.
- C5 baryons-only bound (W4): fraction of S with M*_SED(1 + mu) above the baryons-only fit's disc + gas mass.
- C6 sSFR (W5; weak, from memory, unverified): slope of log(SFR/M*_SED) on z within a fixed M* window against a main-sequence evolution of about +0.67 +- 0.3 dex per unit z (sSFR proportional to (1+z)^2.8 over z 0.3-1.4; memory, not a repo number); it gives tau ~ expected - observed. Caveat frozen in advance: SFR and M* probably come from the same SED fit, and flux-limited selection biases both; this row cannot carry the decision alone.
- PASS / FAIL meaning: sections 9. The attack cannot show which mass is right from repo data unless C4 flags SED + H2 as overweight or C2 needs an implausible bias; it says so.

**(d) Prior-dominated gas.** Definition: prior-dominated if gas_density_hi95 >= 14 and gas_density_lo95 < 1 (prior box 0-15 M_sun pc^-2, assumed the same for all galaxies, UNVERIFIED for 125 of 126). Report the count in S and which rows (ids). Grid (frozen): G0 fitted median (primary); G1 Sigma = 0; G2 Sigma = 15; G3 Sigma = 7.5 for all; G4 per-row Sigma ~ U(0, 15), 1,000 draws (distribution of b_ii: mean, SD, 2.5/97.5); G5 per-row draw from the posterior via a piecewise-linear quantile through (2.5%, lo95), (50%, median), (97.5%, hi95), 1,000 draws; G6 z-tilt Sigma x 10^(t (z - z_med)), t = +-0.3; G7 constrained rows only (non-prior-dominated) slopes; G8 the coefficient of g_HI (pi G Sigma) x0.5 and x2; G9 H2 scale x0.5, x2 and tilt t_H = +-0.3. For each: b_i, b_ii, Delta b, R1 classes. Does +-0.4-0.5 already contain the gas? Frozen rule: with R_g = half-range of b_ii over G0-G3, G6, G8 (and the G4/G5 2.5-97.5 range), "contained" if R_g <= 0.25 x the half-width of the route-(ii) 95% CI; "partly" if 0.25-1.0 x; "dominates" if > 1.0 x; and the total interval reported as bootstrap CI widened by R_g linearly. Note (frozen): in R199 route (i) does not use Sigma_HI at all; gas only enters route (ii) and (iii) through rho.

**(e) III's law reproduced on III's route (sanity anchor).** III's law as quoted by CFG198: a0(z) = a0(0) + a1 z, a1/a0(0) = 1.59. Procedures: E1 the level-free anchor: a linear Theil-Sen of a0 (not log) on z for route (i) (R199 and R198), ratio B/A of slope to intercept at z = 0, bootstrap SD (2,000), compared with 1.59; E2 the log-slope against +0.298 (T7), with the CI; E3 the level at the lowest third against III's law evaluated at that third's median z (III level 1.0 + 1.59 z, in units of 1e-10), reported in dex; E4 III-like cuts (M*_SED > 10^8.8, 0.33 < z < 1.44; the "regular" flag is not in the files; 89 of 127 ids pass the two cuts per the data chat) rerun of the main rows; E5 the sample differs from III's 79-galaxy multi-radius RAR fit (which 79 is not known), so a failure to match III's level is not a failure of III; it is reported as "not reproduced at R_e on this construction". PASS (anchor holds) = B/A within 2 SD of 1.59 and E2 CI contains +0.298 and E3 within 0.15 dex; PARTIAL = slope consistent and level not; FAIL = otherwise. The anchor failing would not affect the route contrast (which is by algebra) but would say that route (i) is not "III's route" in a quantitative sense.

**Extras (f).**
- F1 duplicates: check for any duplicated muse_id in the CSV; locate id 26 and compare V_vir, log_X with the two rows of `duplicated_rows.json`; rerun the main rows with id 26 removed; report the id 36 / 69 absences as the source's. PASS = no CSV duplicates and id 26's parameters match exactly one of the two rows (said which).
- F2 selection: which rows enter each route (table of exclusions by cause and by z-half: bulge, fDM outside (0,1), D <= 1.05, missing gas); leave-one-out of b_i, b_ii, Delta b (max and top five influencers); drop the 10 most influential in each direction.
- F3 censoring: the D <= 1.05 rows are upper limits on a0; bracket: (lo) set to the a0 bound at D = 1.05, (hi) set to that bound minus 1 dex; slope bracket [min, max] for route (ii); plus the Spearman with them at the bottom rank (as CFG198). The selection removes low-a0 rows more often at high z, which biases b_ii upward.
- F4 error model: (i) bootstrap over galaxies (frozen above); (ii) Monte Carlo through the tabulated errors, 2,000 draws seed 2365: log M*_SED with the joined file's error (if absent, 0.15 dex declared), log M_fit with DC14_logMdisk_err, log mu_mol with 0.15 dex (declared), fDM and v not propagated (no errors in the CSV: an UNDECLARED BOUND of the original analysis, stated); the shift of b_ii (nonlinear inversion bias) and the SD added in quadrature; (iii) the joint "bootstrap + MC + gas range" total.
- F5 kernel: primary nu_RAR; P2; nu_mono (import, labelled); the slopes and Delta b for each (prediction: within 0.03 of each other).
- F6 placement against the laws: for every route and every robustness row, table of slope, CI, SD, signed distance to flat (0), E(z) (+0.258), III (+0.298), INSIDE / OUTSIDE. Statement written in advance: a route (ii) slope with flat, E(z) and III all inside is "non-diagnostic between them"; route (i) excluding flat is a statement about the fit route, not about a law.
- F7 multi-covariate: OLS of log a0 on z with covariates (log M*_SED - 9.24, log R_e, and log g_bar) to see whether z carries the slope alone; report the partial z slope and its bootstrap CI.
- F8 z-halves and subsets: slopes within M*_SED terciles and z-halves (n too small for slope? report the level medians only if n < 25).

## 9. "Which mass is right" decision table (fixed in advance; nothing here is graded as support for any a0 law)

Inputs: (C2) tau*_i, the bias that restores route (i)'s slope; B_pl, the plausibility ceiling for a z-dependent bias in SED M*, declared now as 0.25 dex per unit z (from memory, unverified: published SED mass systematics are of order 0.1-0.3 dex between codes and star-formation-history assumptions, mostly not z-dependent beyond about 0.1 dex per unit z; I take 0.25 as generous); (C3) partial drift slope after the M* control, d_M; (C4) overshoot fractions of SED + H2 baryons: f_low, f_high with binomial 95% intervals; (C6) the sSFR-implied tau (weak).

| outcome | conditions (all required) | what it implies (and does not) |
|---|---|---|
| O1 | tau*_i > 0.4 (more than 1.5 x B_pl), AND d_M <= -0.4 with upper CI < -0.1, AND C4 shows f_high - f_low not significant (< 2 SD) and both <= 10% | The SED mass cannot plausibly carry a bias large enough to restore the rise. The fitted-minus-SED drift is then a property of the fit (or of real baryons the SED does not see), not of an SED bias; route (ii) is not contradicted by any test here. The fitted mass is not shown wrong either: "fit artefact or missing baryons" stay open. Nothing follows for a0. |
| O2 | tau*_i <= B_pl (0.25) | A plausible SED-mass bias restores the rise. Route (i)'s rise is then compatible with a SED-mass systematic. The repo gives no handle to decide. |
| O3 | d_M within +-0.25 of 0 (with CI containing 0) | The drift is a mass-scale / selection confound (M*-z correlation with a prior-dilute fit), not a z-drift at fixed mass; the route contrast must be redone at fixed M*, and "III's rise travels with the fitted masses" is not supported as worded. |
| O4 | C4 flags SED + H2 as overweight: f_high >= 25% with f_high - f_low >= 2 SD | SED + H2 baryons exceed the model's total in a z-dependent share of galaxies: the SED (or H2 scaling) is too heavy at high z, in the direction that restores part of the rise; but only the flagged galaxies are excluded by this upper bound; it cannot exonerate the fitted mass. |
| O5 (default) | anything else, including C2 between 0.25 and 0.4 | Which mass is right is NOT determined by anything in the repo. The route contrast stays arithmetic, the slopes stay "gas- or H2-dependent" per the gas grid, and a rise cannot be called established or excluded. |

A table rule: if O1 and O4 both hold, report both and call the verdict O1 with the O4 tension marked. If C6 (sSFR) disagrees with the O1/O2 call by more than B_pl, I note it as a weak counter-indication; it is never a decider on its own.

## 10. Script plan (names CFG236_*; scratch dir only; <15 min per run)

`CFG236_common.py` (loader, constants, geometry, kernels, inversion, Theil-Sen, bootstrap, reference slopes; repo found from `ZF_REPO`, else by walking up from `__file__`, else `~/new_physics/zimmerman-formula`; prints `<repo>` and `<scratch>`, no absolute home path anywhere; reads the .dat directory only if `CFG236_DAT=1`, hash-checked against the repo's manifest); `CFG236_main.py` (attack a, pass lines, exits 0); `CFG236_MUTATE.py` (`MUTATE=1..7`, exits 1 when the control bites); `CFG236_attack_b.py` (readings and drift, B1-B5); `CFG236_attack_c.py` (C1-C6); `CFG236_attack_d.py` (gas); `CFG236_attack_e.py` (III anchor); `CFG236_attack_f.py` (duplicates, selection, censoring, MC error model, kernel, placement, covariates); `CFG236_compare.py` (post-run only, labelled, after CFG198 / CFG199 scripts and outputs are opened); `CFG236_run_all.sh`. Outputs `CFG236_<name>.out` and `_results.json`; main run kept unedited; the second seed (237) written as `*_seed237`. Nothing printed contains an absolute home path.

## 11. What would count as disagreement

- **DISAGREES** (a pass line fails): a slope differing from its target by more than 0.05 (0.03 for the drift, 0.005 for reference slopes), any N off, a class (R1 set) differing; with the cause classified (definition / numerical / README typo / framing).
- **Structural disagreement:** drift on/off or reading (a)/(b) changing Delta b by >= 0.03 (contradicting section 4), or tau*_i inside the plausibility ceiling B_pl (contradicting H15), or the duplicated-row issue changing any class.
- **Framing disagreement** (kept even when numbers reproduce): (i) "travels with the fitted masses" is worded as if the fitted mass were an input of route (i) in R199, which it is not; (ii) a slope of -0.2 +- 0.5 leaves flat, E(z) and III's law all inside: it is non-diagnostic, not a no-rise finding; (iii) CFG199 labels reading (b) better supported using a comparator (CFG198's reconstructed v_c) whose scale it has itself withdrawn; (iv) bootstrap over galaxies omits the measurement and model errors, the gas systematic, the D <= 1.05 censoring, and the fDM and v errors (not in the CSV).
- **Result-level disagreement:** if route (ii)'s slope under a pre-declared grid cell excludes flat or excludes E(z) in a row the README does not show, or if route (i)'s CI contains 0 in my construction.

## 12. Standing statements and open points for the orchestrator

- kappa = 1/2 FITTED; a0(z) FLAT is the distinctive law, a0 proportional to H(z) the rival; nothing will be written as the data favouring any law; a lean is not a detection; a failed control or a wrong expectation is kept.
- Not an a0 verdict: both routes read one analysis's model outputs (section 2.2).
- Open points: (1) permission to read the outside-the-repo `true_Vrot.dat` and run files for the [DAT] rows (attack b, CFG199's construction, drift term); (2) permission to read `musedark_joined.csv` (SFR, baryons-only masses, photometric errors) for C3-C6 and the MC error row; (3) permission to open CFG4_common's FP1 table for the labelled nu_mono import row; without (2) and (3) the related rows are reported NOT RUN.
