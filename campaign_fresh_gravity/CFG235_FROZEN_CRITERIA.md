# CFG235 frozen criteria: a pre-registered per-galaxy "break" search at z > 3.5, scored symmetrically

Status: PHASE 1 document, written before any per-galaxy dynamical value or baryonic mass was opened by the author. To be committed before any CFG235 script exists. In phase 2 no rule in this file is changed after a value is seen; a wrong expectation is kept and reported.

Standing rules carried: kappa = 1/2 is FITTED, not derived. a0(z) FLAT is the framework's distinctive law; a0 proportional to H(z) is the rival and is REPORTED ONLY here (it never bears a label). Nothing in this lane says the data favour any theory, and nothing says any theory is closed. A failed control or a wrong expectation is kept as written. No network, no new data. Literature facts quoted from memory are marked "from memory, unverified". No personal name and no absolute home path appears in any CFG235 file; scripts print `<repo>`.

What the owner asked for: a z ~ 5 galaxy where a LambdaCDM dark-matter fit breaks. The campaign told the owner this would be done WITHOUT cherry-picking. This file is the mechanism: the criteria are frozen first, the same sample is scored for both theories, and EVERY galaxy that breaks EITHER theory is reported.

---------------------------------------------------------------------------------------------------

## 0. Disclosures: what the author saw before freezing (honest list; none was used to choose a threshold)

The author read the required documentation. In doing so the following per-object or aggregate values were seen. None was computed with. The test is NOT blind (see section 10).

1. From the CFG197 README (aggregates and a few per-object lines): pooled z > 3.5 median M_dyn(<r_e)/M* = 5.1 (Halpha 5.4, [CII] 4.4); gas-free floors 1.33 (flat) and 2.55 (rival); "below a floor even at 1 sigma": CRISTAL-23b and four Danhaive galaxies (1082948, 1009935, 1015956, 1085659) with ratio 0.02 to 0.43. For the four Roman-Oliveira sources, V_ext and sigma_ext (BRI1335-0417 125, 57; J081740 249, 33; SGP38326-1 548, 46; SGP38326-2 409, 40 km/s), the gas-only floor speeds and margins (BRI1335-0417: the observed V_ext is below even the Newtonian gas-only speed at f_g = 0.5, margin about -1.5 sigma; the rival's margin -2.6 sigma).
2. From the CFG213 README: D_obs for CRISTAL-09 (1.09) and -15 (1.21); per-disc route factors M_ind/M_fit (02 1.11, 03 1.15, 07a 1.11, 20 1.22, 12 1.21, 08 0.61, 11 0.45, 19 0.34, 23b 6.09); one-sided delta bounds for 08, 12, 23b.
3. From the CFG234 README: CRISTAL-23b SED log M* = 10.46 against fitted 9.8; dust f_molgas for 08 (0.63), 12 (0.67), 23b (0.25); SED + gas baryons exceed the whole dynamical mass (D_ind < 1) for 02, 03, 23b.
4. From the cristal_vector README: model g_bar/a0 at the outermost observed marker for 02 (0.63), 07a (0.95), 08 (0.51), 12 (0.60), 20 (0.72), 23b (0.75), 23c (0.22), others 1.7 to 4.7; total 0.72 (02), 1.0 (12), 1.3 (20), 1.4 (08); CRISTAL-09 R_e 2.6 vs 1.2 kpc and -15 sigma_0 67 vs 100 km/s between figure and table; observed V_rot 20 to 100 km/s against model V_circ 130 to 320 km/s.
5. From the Danhaive TeX (method lines only): 1082948 has log M* = 10.6 and log M_dyn = 8.9 (errors +0.4/-0.6 on M_dyn); the text says 5 systems lie on or above the one-to-one line and the figure caption says six.
6. From the data_assembly notes: literature values for GN20, J081740, REBELS-25 and others; ranges for Amvrosiadis (log M* 10.5 to 12.3, V_circ 250 to 530 km/s), Roman-Oliveira (V_max 198 to 562 km/s; M_H2 7.6e10 to 1.9e11), CRISTAL R_out/R_e (23c 9.2, 09 3.1, 02 3.0, median 2.5).
7. Redshifts (not dynamical): the 41 Danhaive z range 3.8 to 5.82; CRISTAL z for the 14 modelled; Amvrosiadis z of the 12 fitted; ALPAKA ID 28 z; the z-matches in section 2.4.
8. The structure of the tables was read as column headers and finite-number counts only (all 41 Danhaive rows have a finite log M*, r_e, log M_dyn and sigma_0; all 14 CRISTAL modelled rows have finite log M_tot, R_e, V_rot, sigma_0 and f_DM; 12 of the 14 have a finite log M* in the sample table under the mapping in section 2.2, the two without being 10a-E and 23c; 11 have a finite dust f_molgas under that mapping). No value was printed.

---------------------------------------------------------------------------------------------------

## 1. The three criteria in one paragraph

All three read ONE quantity per galaxy: the enclosed dynamical-to-baryonic ratio R_obs = V_c^2(r) / V_bar^2(r) at a stated radius r, with the baryons counted as a ONE-SIDED FLOOR (stars from the SED, plus measured gas only at the low end of its bracket, never a fitted or dynamically derived baryon mass). L1 asks whether R_obs is below 1 (no room for dark matter: LambdaCDM, and Newton, break). F1 asks whether R_obs is below nu(x), x = g_bar/a0, the flat framework's floor (both kernels, both footings). L2 asks whether the halo that would be required to supply the DM inside r is too rare to exist in the survey volume. By construction (section 11) L1 implies F1, because nu > 1. So a galaxy that breaks L1 breaks both laws and is labelled a "mass-estimate outlier"; "framework only" needs 1 <= R_obs < nu and a separation of nu from 1 that exceeds 3 sigma, which at high acceleration is unreachable with realistic sigma (stated up front, section 11); "LambdaCDM only" can come only from L2.

---------------------------------------------------------------------------------------------------

## 2. The sample (fixed before any value is read)

### 2.1 Inclusion rule (all must hold)

A galaxy is IN if:
1. its published spectroscopic redshift in the parsed table is > 3.5 (strict);
2. a dynamical estimate at a stated radius exists in a MACHINE-READABLE per-galaxy table under `data_assembly/` (parsed CSV, or the digitised CSV for the one source marked so), giving M_dyn, or a velocity and a radius from which V_c^2(r) is computed by section 3;
3. at least one baryon-floor input exists in such a table: an SED stellar mass (tier S), or, only where no SED mass exists, a measured gas mass (tier G, section 3.3).

Numbers that occur only in TeX prose, in an abstract-level summary, or in a figure that is not digitised are OUT (their extraction is an unfrozen transcription step). Rows are not dropped for having a limit flag or a large error (section 3.5 says how limits are scored), and not for any value.

### 2.2 N per source (verified by header and row count only)

| code | source table (under data_assembly/arxiv_tables/) | rows IN | tier | notes |
|---|---|---|---|---|
| D | `danhaive2025_gold.csv` (Danhaive+2025 gold, Halpha, GOODS-S and GOODS-N) | 41 | S | no gas measurement |
| C | `cristal2025_dynamics.csv` + `_sample.csv` + `_kinematics.csv` (ALMA-CRISTAL, 14 DysmalPy-modelled): 02, 03, 06b, 07a, 08, 09, 10a-E, 11, 12, 15, 19, 20, 23b, 23c | 14 | S (and S+G reported for the 6 dust detections 02, 03, 07a, 11, 19, 20) | ID mapping (frozen): a dynamics id X is joined to the sample and kinematics row X, else X+'a' (so 09 -> 09a); this mapping is an assumption and is printed. By a finite-number count, 10a-E and 23c have NO finite SED M* in the sample table (the data note also lists 09 as lacking M*; under the 09 -> 09a mapping the count finds one, a discrepancy to be printed by the first script, not resolved by hand): rows with no finite M* enter with NO stellar floor; L1/F1 are UNDEFINED for them (not dropped, counted in m). CRISTAL-09 and -15 disagree between table and vector figure (R_e, sigma_0); the TABLE values (the machine-readable source) are the frozen input and the figure values are a reported variant |
| R | `romanoliveira2023_*.csv` ([CII], literature CO gas): BRI1335-0417, J081740, SGP38326-1, SGP38326-2 | 4 | G only | AzTEC 1 has no kinematics: OUT. SGP38326-1 and -2 are the two components of one system; both kept |
| A | `amvrosiadis_bestfit.csv` + `_parent.csv`: ALESS 065.1 (z 4.445), ALESS 071.1 (z 3.709) | 2 | S | the source's own alpha_CO is justified by its kinematics, so its gas is NOT used (circular); 071.1 carries the paper's "SED possibly AGN-contaminated" flag: a break on it is annotated, not discarded |
| P | `alpaka1_*.csv` + `alpaka1_digitised/`: ALPAKA ID 28 (W0410-0913, z 3.63) | 1 | S | no conversion applied to its line luminosity: gas NOT used; optical R_e not tabulated (section 3.4) |
| | **Total unique rows** | **62** | | |

### 2.3 Sources OUT, with the rule that excludes them (listed so no one can say they were silently dropped)

GN20 and REBELS-25 (numbers only in TeX prose or abstract-level; REBELS-25 also has gas = M_dyn - M*, circular), SPT0418-47 (M* from the rotation-curve decomposition and a fitted alpha_[CII]: fails the independent-baryon rule), J081740's GA-NIFS data (no M* on disk), ALPINE rotators, Az9, ALESS 073.1, the Amvrosiadis sources below 3.5, Big Wheel (z 3.245), GS-9209 (quiescent), GS5001 (z 3.47), AzTEC 1. Any of them may be added later only as a labelled post-freeze addition; it would be scored by the same sections and is not part of the frozen family or its m.

### 2.4 Duplicates across sources

Identity test, applied BEFORE any statistic and printed by the first script: two rows are the same galaxy if (i) the same catalogue name, or (ii) the same field AND positions within 1.5 arcsec when both have coordinates on disk, or (iii) when one lacks coordinates (Danhaive has none on disk): same field AND |delta z| <= 0.02 is a POSSIBLE duplicate, unresolvable on disk.
Facts on disk (z only): the Danhaive fields are GOODS-S and GOODS-N (the paper's text on disk). The CRISTAL modelled rows in COSMOS (names DEIMOS_COSMOS_* and vuds_cosmos_*) cannot match; CRISTAL-08 (vuds_efdcs, ECDFS, z 4.43) and CRISTAL-12 (CANDELS_GOODSS_21, z 5.572) are in GOODS-S/ECDFS. The z-only comparison already run lists one candidate pair: CRISTAL-08 with Danhaive 1077545 (z 4.42; |dz| = 0.01, the Danhaive z has two decimals). CRISTAL-12 has no candidate. 
Treatment (frozen): a possible duplicate keeps BOTH rows in the tables, both are scored, both are reported if either fires, and the pair counts as ONE unique galaxy in the Sample table's "unique" count; BUT the trials factor m is fixed at 62 regardless (conservative). No other duplicates: CRISTAL-23b and -23c are distinct kinematic components of one blended host system and SGP38326-1/-2 are two components of one system; all are kept as separate rows and FLAGGED "same-system pair" in the label table.

### 2.5 The trials count

m = 62 for every criterion family (L1, L2, F1), independent of how many rows a criterion is defined for (definedness depends on the inputs, but m does not shrink). Known cases (section 10) are inside m.

---------------------------------------------------------------------------------------------------

## 3. Inputs and estimators per source (all from the table; the same estimator for L1, L2 and F1)

### 3.1 Enclosed dynamical mass at radius r

V_c^2(r) = V_rot^2(r) + k(r) sigma_0^2, with k = 2 r / r_s the authors' own asymmetric-drift term: k = 3.36 at r = r_e for an exponential disc (r_e = 1.678 r_s), so k(r) = 3.36 (r / r_e). M_dyn,enc(<r) = V_c^2 r / G (sphere convention, no extra coefficient); G = 4.30091e-6 kpc (km/s)^2 / Msun.
- **D (Danhaive):** the table carries the paper's M_dyn = k_tot r_e V_c^2 / G with k_tot = 1.8 (the paper's Eq. for M_dyn, on disk). V_c^2(r_e) = G M_dyn / (1.8 r_e); r = r_e (Halpha size). (The paper's k_tot extrapolates V_c^2 r_e/G to a total mass; dividing it out returns the circular-velocity mass at r_e, which is what the baryons inside r_e must be compared with.)
- **C (CRISTAL):** V_rot(R_e) and sigma_0 from the dynamics table; V_c^2 = V_rot^2 + 3.36 sigma_0^2; r = R_e,disk (a DysmalPy fit output with a [CII]-size prior, NOT a stellar-light radius). The fitted M_tot (a fitted baryon mass, 1 dex Gaussian prior, constrained by the same kinematics) is NOT a baryon input; f_DM and D = 1/(1 - f_DM) are MODEL OUTPUTS and are never used as data (reported column only).
- **R, A, P:** V_ext (or V_circ(2 r_e) for A) at the stated radius r of the table (R: r_ext = (N_rings - 1) x RADSEP x (kpc/arcsec) from the ring set-up in the paper, variant (N - 1.5) RADSEP; A: r = 2 r_e with r_e in kpc from its arcsec value and the z-scale; P: R_ext from the digitised curve). Pressure term k as above with r/r_e >= 1 taken as k = 3.36 when r_e is unavailable (R, P): the LARGER V_c^2 is the conservative choice for a break claim.

### 3.2 Baryon floor M_bar,floor(<r)

- **Tier S floor:** stars only, V_bar^2(r) = f_enc(r) G M* / r with f_enc the projected exponential-disc enclosed fraction f_enc = 1 - (1 + s) e^(-s), s = 1.678 r / r_e (0.5 at r_e, about 0.85 at 2 r_e). Gas = 0 (the one-sided floor, gas >= 0).
- Secondary reported cell S+G (never label-bearing): the measured gas, at x1/3 of the source value (the low end of the CFG234 bracket x1/3 to x3), added with the same f_enc; defined only for the 6 CRISTAL dust detections; the 4 CRISTAL dust-limit discs (08, 12, 15, 23b) and the two CRISTAL discs without usable gas never use gas as a value (an upper limit is not a floor).
- **Tier G floor (Roman-Oliveira only):** gas only, from the literature CO mass in the table at x1/3 (alpha_CO bracket low end), spread as a disc of radius r_ext (f_enc = 1 at r_ext, the most favourable to the theory and therefore conservative). Labels from tier G carry the suffix (G): their floor is a different object from the tier-S floor (they have no M*) and they are NOT pooled with tier S in any sample-level statement.
- M* is the SED value in the table, as tabulated (Prospector for D; Li+/Mitsuhashi+ SED for C: from memory, unverified; MAGPHYS for A; SED for P); no rescaling.

### 3.3 Geometry cells (declared, not fitted)

G-S: sphere with mass following light (V_bar^2 = f_enc G M / r), PRIMARY. G-D: thin exponential disc (Freeman), V_bar^2 computed numerically from Bessel functions at r, stars with r_e = 1.678 r_d (by hand it raises V_bar^2 by about a factor 1.5 over G-S at r_e; the script computes it). G-C: compact stars: half-light radius of the stars 0.6 of the tabulated r_e (sphere). A break claim must hold in G-S (the weakest cell); G-D and G-C strengthen it and are reported.

### 3.4 Missing radius

ALPAKA ID 28 has no tabulated optical r_e: f_enc = 0.5 (the G-S value at r_e) is used at R_ext (conservative if R_ext >= r_e; the row is annotated).

### 3.5 Censoring rule

- M_dyn (or V_c) flagged as an UPPER limit: used at face value with the tabulated or default error (this UNDER-states a break, so it is conservative). A LOWER limit on M_dyn cannot support a break: scored z = 0, "not testable for a break".
- M* flagged as an UPPER limit: no lower bound on the floor, so the break test is "not testable" (z = 0). A LOWER limit on M*: used at face value (conservative for a break).
- sigma_0 upper limits (Danhaive, many rows): the table's M_dyn already contains them; a V-lim variant (sigma_0 set to zero in V_c, reported only) shows the sensitivity; it never bears a label.
- The limit-flag semantics (which symbol means which side) are read from the table's flag columns in phase 2 and printed in the Sample table BEFORE any statistic; the rule above is applied to that reading; nothing is re-read after statistics.

---------------------------------------------------------------------------------------------------

## 4. Common statistics and the sigma convention (identical for L1, L2, F1)

### 4.1 Constants and kernels

a0 canonical = 9.3603e-11 m/s^2 (2888.3 (km/s)^2/kpc); alt footing = 1.1312e-10 m/s^2 (about 3490 (km/s)^2/kpc). a0 is FLAT (no z dependence). P2: nu(y) = sqrt(1 + 1/y). nu_mono: the chain's monotone kernel as committed (CFG5_common / CFG44 Bcommon; phase-2 re-implements it from its docstring and checks agreement with the committed object to 1e-9 (the CFG234 lesson: against the older CFG4 copy the difference is 3.3e-9, recorded and not repaired)). The prediction is g_obs = g_N nu(g_N/a0); the floor on R_obs is nu(x_*), x_* = g_*/a0, g_* = V_bar,*^2 / r. Lemma (CFG197, prior work cited, re-checked in phase 2 by `CFG235_00_*`): adding gas can only raise the predicted ratio for both kernels, so the stars-only nu(x_*) is a FLOOR for any gas amount. Differences from CFG197 (stated so nobody reads this as a re-run): (a) per galaxy, not a bin median; (b) a 3 sigma statistic with a min-over-cells robustness rule and trials correction, not a bootstrap-of-medians; (c) a sphere, a thin exponential disc and compact stars, with f_enc at r rather than a fixed half; (d) L1 and L2 are added and scored by the same machinery; (e) tier G for Roman-Oliveira is scored as a floor, not as an "over-prediction margin".

### 4.2 The statistic

For each galaxy, cell c and criterion X in {L1, F1}: Delta_c = log10 floor_c - log10 R_obs (positive = below the floor). Inputs are drawn from Gaussians in log (200,000 draws, seed 235): log M_dyn, log M* (mean = tabulated), with the error taken on the side that would cure the break: the UPPER error of M_dyn (a larger true M_dyn removes the break) and the LOWER error of M* (a smaller true M* removes it); where the table gives a symmetric error, that one. z_c = mean(Delta_c) / sd(Delta_c). The L1 case is also computed analytically as a check. One-sided p = 1 - Phi(z); "3 sigma" is z > 3 (p < 1.35e-3).

### 4.3 The systematic terms (in quadrature, the same for every criterion)

sigma_M*,sys = 0.25 dex (declared range 0.2 to 0.3: the SED mass systematic from the star-formation history, IMF and dust; CFG234 found the M* zero point alone moves the rival median by 0.29 dex over +/-0.2 dex); sigma_dyn,sys = 0.15 dex (non-equilibrium, inclination, unresolved rotation, virial coefficient; the paper's own q_0 sensitivity is 0.02 dex, the rest is declared). The tabulated statistical errors are added on top. The CRISTAL and Danhaive r_e, inclination and sigma_0 errors propagate through V_c^2 and r where the table gives them (r_e enters both M_dyn,enc and f_enc).

### 4.4 The robustness cells and z_rob

z_rob = MIN over cells of z_c, cells = geometry {G-S, G-D, G-C} x sigma setting {narrow (M* 0.20, dyn 0.10), primary (0.25, 0.15), wide (0.30, 0.25)}; for F1 also x kernel {P2, nu_mono} x footing {canonical, alt} (36 cells); for L1, 9 cells. For L2, cells in section 6. A PER-GALAXY FLAG ("T0") is z_rob > 3. The primary-cell z (G-S, primary sigma, canonical, P2) is always printed beside z_rob, together with the cell that attains the minimum. z_rob is deliberately the conservative reading: a galaxy that fires only in some cells is reported as "fragile", never as a break.

### 4.5 Route systematic floors (assumed and declared, not measured here)

Class A independent route (CRISTAL dust detections): gas bracket x1/3 to x3 and M* zero point +/-0.2 dex (the CFG234 bracket); on that route the rival is DISFAVOURED-under in 6 of 15 bracket cells and the flat law is over in 3, so a route systematic of order 0.07 (rival) to 0.27 (flat) dex in a median shift is the scale that a single-galaxy 3 sigma must exceed; the route factors of the 9-disc set run 0.34 to 6.09. The dust-limit discs carry no gas value. The enclosed-mass estimators (section 3) are model outputs of one analysis chain per source (DysmalPy for C, geko for D): the test reads one analysis each, not raw kinematics.

---------------------------------------------------------------------------------------------------

## 5. LambdaCDM criterion L1: "no room for dark matter"

Break if the required DM fraction is negative: M_dyn,enc(<r) < M_bar,floor(<r), i.e. R_obs < 1, with z_rob(L1) > 3. The baryon floor is stars only (gas >= 0), so a flag is a statement about the stars alone: the gas, whatever it is, can only make the break stronger. Reported beside it: the S+G cell (CRISTAL dust detections), and the tier-G value for Roman-Oliveira. f_DM as tabulated by the source is not used.

## 6. LambdaCDM criterion L2: "too massive too early"

### 6.1 Definition (same for every galaxy)

If M_dyn,enc - M_bar,floor <= 0, L2 is "not needed" (z_L2 = 0; L1 covers the case). Otherwise M_DM,need = M_dyn,enc(<r) - M_bar,enc(<r) (stars-only floor, so the smallest DM need: conservative). Solve for the NFW halo M200c (at z) whose DM inside r equals M_DM,need:
M_DM(<r) = M200 [ln(1 + c x) - c x/(1 + c x)] / [ln(1 + c) - c/(1 + c)], x = r / R200, R200 from 200 rho_crit(z), c = c200(M200, z).
Expected number of halos above M200 in the survey volume: N_exp = V_surv x integral over M > M200 of dn/dlnM (Sheth-Tormen). p2 = P(N >= 1) = 1 - exp(-N_exp) for the needed M200, averaged over the input draws (posterior-predictive), and z_L2 = Phi^-1(1 - p2). "T0" is z_rob(L2) > 3 (p2 < 1.35e-3). The literal owner wording ("needed mass exceeds the mass where fewer than one halo is expected") is reported as N_exp < 1 at the central values (the "L2-literal" column, NOT label-bearing).

### 6.2 Declared analytic forms (all "from memory, unverified" in their coefficients; the repo holds an on-disk implementation of each that phase 2 uses as a cross-check, not as the source)

- Cosmology: flat LambdaCDM, Planck 2018 values as in the repo's hunt_lib (Omega_m about 0.31, sigma_8 = 0.811, n_s = 0.965, delta_c = 1.686).
- Halo mass function: Eisenstein and Hu 1998 no-wiggle transfer function, sigma(M) normalised to sigma_8, growth factor from the integral, Sheth-Tormen (A = 0.3222, a = 0.707, p = 0.3). Implemented on disk in `hunt_2026/h73_h86_h87_cosmic_dawn.py` (dndlnM, n_above); phase 2 re-implements independently and requires agreement of n(>M) at z = 4.5 and 5.5 for M = 1e11, 1e12, 1e13 to 1%.
- Concentration-mass: PRIMARY Dutton and Maccio 2014 (Planck), log10 c200 = a + b log10(M200 / 1e12 h^-1 Msun), a = 0.520 + (0.905 - 0.520) exp(-0.617 z^1.21), b = -0.101 + 0.026 z, scatter 0.11 dex in log10 c (from memory, unverified; implemented on disk in `hunt_2026/h106_h107_h108_li2020_halos.py`); SECONDARY Duffy et al. 2008 (full sample, c200 = 5.71 (M / 2e12 h^-1)^-0.084 (1 + z)^-0.47, from memory, unverified). Calibration range taken as z <= 5 (from memory, unverified).
- **Out-of-range rule (frozen):** L2 is DEFINED for a galaxy only if z <= 5.0 and the solved M200 lies between 1e10 and 1e15 Msun. Otherwise L2 is reported as UNDEFINED (outside the c-M calibration), NOT approximated. A separate REPORTED-ONLY column gives the z-clamped (z_c = min(z, 5)) value for the z > 5 rows; it never enters a label. This makes L2 UNDEFINED for every galaxy above z = 5 (several D rows, CRISTAL-02, 03, 07a, 09, 10a-E, 12, 19, 20), which is a power loss declared in advance.
- Survey volume: V_ref = 2 deg^2 x Delta z = 1 centred on the galaxy's redshift (the COSMOS-scale reference; generous: the Danhaive parent footprint is about 175 arcmin^2 = 0.049 deg^2 by the paper's text on disk). A larger V makes a break harder, so it is the conservative primary; the same formula and the same V_ref for every galaxy.
- Not modelled (declared): adiabatic contraction, feedback cores, non-NFW shapes, baryon mass outside r, assembly bias, selection function; they are covered only by the bracket below.

### 6.3 L2 cells (z_rob takes the MIN)

c-M relation {DM14 primary, D08} x scatter {median c, c at +1 sigma (lower M200 needed)} x volume {V_ref, 10 V_ref} x needed-M200 shift {0, -0.3 dex (halo contraction and mass-definition bracket)} x sigma setting {narrow, primary, wide}. The flag must hold in the weakest of these (the most permissive to LambdaCDM: high c, big volume, -0.3 dex in M200).

## 7. Framework criterion F1

The observed R_obs falls below the floor nu(x_*) at > 3 sigma (z_rob(F1) > 3) in EVERY cell of section 4.4 for F1, which includes both kernels (P2, nu_mono) and both footings (9.36e-11, 1.13e-10): a break must survive every kernel and footing the framework allows. The rival a0 x E(z) floors are computed and reported, not label-bearing. The floor uses gas >= 0 (stars only), so a gas amount cannot rescue the law only if the lemma holds (phase-2 check L0 verifies it numerically for both kernels over y = 1e-6 to 1e6). External-field and cluster/environment corrections are NOT applied (none is committed for these discs); a flagged galaxy is therefore a statement about the isolated-galaxy flat law.

---------------------------------------------------------------------------------------------------

## 8. Symmetric trials treatment (look-elsewhere; about 60 galaxies)

Applied identically to L1, L2 and F1 (and to any row, real or planted). The per-galaxy 3 sigma flag T0 is NOT a detection at N about 60: the chance count under a correct Gaussian null is 62 x 1.35e-3 = 0.084 flags per criterion, and the sigma values are declared systematics, not measured ones.

- **T1, Bonferroni:** z_rob >= z_B = Phi^-1(1 - 0.05/62) = 3.16 (one-sided, family-wise 5% per criterion).
- **T2, permutation (Westfall-Young step-down max-T):** statistic T = max_i z_rob,i; null by 100,000 permutations (seed 235) of the residual vector r_i = log R_obs,i - log floor_i among the galaxies WITH THE sigma_i AND the floors held; the adjusted p of the k-th ranked galaxy is computed with the step-down rule; T2 requires adjusted p < 0.05. Known limitation, declared now: with several extreme residuals the permutation null is contaminated by those same residuals (masking) and has low power; a galaxy that reaches T1 and not T2 is labelled "Bonferroni only", not failed.
- **Parametric null (REPORTED ONLY, not label-bearing):** 100,000 simulated samples of the 62 galaxies with the truth exactly on the floor, noise from each galaxy's own sigma_tot plus an intrinsic route scatter 0.27 dex (the CFG234 route MAD; it is an aggregate, not a per-galaxy, value), giving a p for the observed maximum.
- A per-galaxy flag must be shown with all three numbers. "Confirmed" (used in the final labels) = T2 (which includes T1). The headline label for a galaxy is its T2 label; its T0 and T1 labels are listed beside it so that every galaxy that breaks either theory at any tier appears.
- Sample-level: the observed number of T0 flags per criterion against Poisson(0.084), reported.

---------------------------------------------------------------------------------------------------

## 9. Labels and outcomes

Per galaxy, at each tier (T0, T1, T2) and separately for each criterion, a flag is fired or not. Label:

| L1 or L2 fired | F1 fired | label |
|---|---|---|
| yes | no | breaks LambdaCDM only |
| no | yes | breaks the framework only |
| yes | yes | both ("mass-estimate outlier": R_obs < 1 breaks Newton as well, so neither theory is singled out; the row is reported as a data or estimator problem candidate) |
| no | no | neither |

Every galaxy with any flag at any tier is listed in a table with its tier, cell of minimum z, source, same-system-pair flag, dispersion-dominated flag (V_rot/sigma_0 < 1, where the enclosed-mass estimate is a virial, not a circular, estimate), and its "known case" status.

Sample-level outcomes (pre-declared; "both" rows are excluded from BOTH tallies, because the same number breaks both theories, and Newton):
- **The framework survives (this test):** no galaxy at T2 labelled "framework only". 
- **LambdaCDM survives (this test):** no galaxy at T2 labelled "LambdaCDM only".
- **Both survive:** both hold. The wording carried with it is frozen: "survives only at gross-outlier sensitivity": with sigma_tot about 0.4 to 0.6 dex and z_B = 3.16, a flag needs R_obs lower than the floor by a factor of about 20 to 100; the pooled tests of CFG197 are the sensitive ones and this lane does not add sensitivity.
- **One theory broken (in scope):** at least one galaxy at T2 with its label naming that theory, and the same galaxy not explained by a recorded estimator problem (same-system pair, dispersion-dominated with V/sigma_0 < 1, M* flagged, tier G). A galaxy that fires only with such a flag is reported as "flagged, systematic-prone".
- **Inconclusive:** T0 or T1 flags exist but no T2 (the permutation masking case), or fewer than 20 rows have the criterion defined (L2 with z <= 5 is the likely case), or the separability index (section 11) makes the two theories indistinguishable.
- A per-galaxy 3 sigma flag at N about 62 with route systematics is NOT a detection without the trials correction. Not one number in this lane is a result about a0(z) or about the two theories' evidential weight.

---------------------------------------------------------------------------------------------------

## 10. Known cases: the test is NOT blind

Known BEFORE freezing (from the papers' own text and the campaign READMEs): Danhaive 1082948, 1009935, 1015956, 1085659 (catalogue M_dyn below M*); CRISTAL-02, -03 and -23b (SED + gas baryons exceed M_dyn, D_ind < 1); Roman-Oliveira BRI1335-0417 (V_ext below the Newtonian gas-only speed); CRISTAL-09 and -15 (table and figure disagree). The procedure: they enter the sample like every other row, none is given a special rule, and m = 62 already counts them. They are listed in the label table with the tag "known before freezing", so a reader can see how many of the flags are rediscoveries. A flag on a known case is NOT treated as new evidence. No criterion, cell or threshold was tuned to a known case; the four Danhaive systems were known only from their M_dyn < M* statement, not from the SED or kinematic values.

## 11. Structural facts stated before any value (the test's limits)

1. nu(x) > 1 always, so the L1 floor (1) lies below the F1 floor (nu). For the same inputs z(F1) >= z(L1) in every cell, so every L1 flag is an F1 flag: "breaks LambdaCDM only" cannot arise from L1.
2. "Framework only" needs R_obs in [1, nu): the window is log10 nu(x_*) wide. A flag needs that window to exceed 3 sigma_tot,rob, with sigma_tot,rob at least about 0.4 dex (M* and dynamical systematics alone, the 'wide' cell 0.39 dex). So only galaxies with nu(x_*) > about 15 (x_* < about 0.005: very low baryonic acceleration) can be framework-only. At z > 3.5 the stars alone sit at high acceleration (the floors are about 1.3 to 3 by the CFG197 pooled numbers, which is an aggregate already seen). So "framework only" is expected to be UNREACHABLE for nearly every row. The first phase-2 script prints a "separability index" S_i = log10 nu(x_*)/sigma_tot,primary per galaxy BEFORE any statistic; rows with S_i < 3 cannot be labelled framework-only and the script says so.
3. L2 is UNDEFINED for z > 5 by the out-of-range rule. The framework has no halo-mass analogue of L2: its exposure is F1 alone, LambdaCDM's is L1 and L2. The trials factor is applied per criterion, so the framework is not penalised for LambdaCDM's second test and vice versa.
4. The only label that can be attained by a pure "mass-estimate outlier" is "both". It is not evidence against either theory; it is a statement that M_dyn < M_bar(stars) for the row.

## 12. Planted-galaxy controls (run BEFORE the real scoring; the main script refuses to print any real statistic if a control fails or its result file is missing)

Synthetic rows (id SYN_*, excluded from m in the real run; included with their own m = 62 + number planted in the controls) are injected into the sample through the SAME code path (inputs M*, r_e, V_rot, sigma_0, z, errors), never by overriding a statistic. A planted row is built from a target (R_obs, x_*) by solving for V_rot at fixed r_e, M*, sigma_0 = 50 km/s; statistical errors 0.05 dex in M_dyn and 0.05 in M*.

| id | design | must be |
|---|---|---|
| P1 | R_obs = 0.03 (log -1.5), x_* = 5, z = 4.5 | L1 T0 and T2 fired, F1 fired in all 36 cells: label "both" |
| P2 | R_obs = 1.0, x_* = 1e-4 (nu about 100), z = 4.5, S_i > 3 | F1 fired in all cells, L1 not fired: label "framework only" |
| P3 | very large V_c at r_e = 2 kpc chosen so that M200,need = 1e14 at z = 4.5 (c from DM14): R_obs >> 1, x_* = 5 | L2 fired in all L2 cells, L1 and F1 not: label "LambdaCDM only" |
| P4 | R_obs = 3 nu(x_*), x_* = 2 | no flag anywhere: "neither" |
| P5 | R_obs at the floor minus 1.5 sigma_tot,primary, x_* = 2 | no flag at z_rob (fragile to the wide cell): must not fire |
| P6 | R_obs set so that z_rob(F1) = 3.05 | T0 fired, T1 NOT fired (z_B = 3.16): "flagged, not confirmed" |
| P7 | R_obs = 0.3 at the stars-only floor but with a measured gas mass large enough that the S+G cell breaks L1 | L1 NOT fired (tier S primary), the S+G cell reported as fired |
| P8 | a same z row duplicating CRISTAL-08's z and field | duplicate list prints it as a possible duplicate; m stays 62 |
| P9 | a planted row with log M* flagged as upper limit and R_obs = 0.1 | "not testable", z = 0 |

Also: C0 = the printed Sample table has exactly N (41, 14, 4, 2, 1; total 62) and exits 2 otherwise; C1 = analytic L1 z against the MC z to 0.02 for 5 random planted rows; C2 = P2-kernel closed form vs the floor function to 1e-12 and nu_mono to the committed object to 1e-9; C3 = lemma L0 (floor monotone in gas, both kernels); C4 = HMF and c-M cross-checks (section 6.2); C5 = the permutation machinery on a synthetic null (no outlier, 62 draws): false-positive rate of T2 <= 7% over 1,000 synthetic samples, and on a sample with one planted 5 sigma residual T2 fires.

Exit-code convention: a MAIN run exits 0 iff every control passes; exit 1 if any control fails (a real failure, reported, never repaired); exit 2 on a sample or frozen-hash mismatch. A MUTATE run (env `MUTATE=k`) exits 1 iff the control BITES (at least one control fails, as required); a MUTATE run that exits 0 is itself a control failure and is recorded as such.

## 13. MUTATE controls (each flips one load-bearing cell; each must bite)

| k | mutation | the control that must fail |
|---|---|---|
| M1 | swap the floors: L1 uses nu, F1 uses 1 | P1, P2, P3 labels change |
| M2 | drop the M* and dynamical systematics (sigma_M*,sys = sigma_dyn,sys = 0) | P5 fires |
| M3 | drop the trials correction (T0 final) | P6 fires as confirmed |
| M4 | add the measured gas (x3) to the PRIMARY floor (drop the one-sided floor) | P7 fires L1 |
| M5 | take R_obs from the model output D = 1/(1 - f_DM) instead of V_c (the CFG213 pitfall) for a planted row whose f_DM and V_c disagree | the planted label changes |
| M6 | drop the min-over-cells rule (primary cell only) | P5 fires |
| M7 | use the actual footprint (0.049 deg^2) for V_surv in place of V_ref | P3-adjacent L2 marginal row fires (a second planted L2 row at N_exp = 0.05 at V_ref) |
| M8 | set m = 31 | P6 fires as confirmed |

## 14. Script plan (all in campaign_fresh_gravity/CFG235_break_search/; each < 15 minutes)

- `CFG235_common.py`: constants, kernels, geometry, estimators, sigma convention, HMF, c-M, MC; no output.
- `CFG235_00_sample.py` -> `.out`: ONLY the Sample table (id, source, tier, z, r, flags), counts per source, the duplicate list, the limit-flag reading, and the separability index S_i. No test statistic, no label. Exit 2 if N differs from section 2.2.
- `CFG235_01_controls.py` -> `.out`, `_results.json`: C0-C5, P1-P9 (runs on synthetic rows only; no real value enters).
- `CFG235_02_main.py` -> `.out`, `_results.json`: refuses to run unless `_01_controls_results.json` exists with all pass; computes L1, L2, F1 for the 62 rows in every cell, T0/T1/T2, labels, the reported-only columns (S+G, rival, L2-literal, L2-clamped, V-lim, fit-route), sample-level tallies, and the parametric null.
- `CFG235_03_report.py` -> `.out`: the label table with every galaxy that breaks either theory at any tier, the known-case table, and the scoring of section 16 (hand estimates against outcomes).
- `CFG235_MUTATE.py` (env `MUTATE=1..8`, or a loop) -> `CFG235_MUTATE_k.out`, `_results.json`.
- Outputs carry a repo placeholder `<repo>`; repo root from `ZF_REPO` or by walking up from `__file__`; no absolute path printed.

## 15. Phase-2 order (the ordering is itself pre-registered)

1. The orchestrator commits this file. 2. `CFG235_00_sample.py` is run and its output committed or saved BEFORE any other script runs; it prints the sample table before any test statistic. 3. `CFG235_01_controls.py` and the MUTATE runs are run and saved (a failed control stops the lane; it is reported). 4. `CFG235_02_main.py`. 5. `CFG235_03_report.py`. The per-galaxy dynamical values and baryonic masses are opened only in step 2 onward, and only after the commit of step 1. A wrong expectation in section 16 is kept.

## 16. Hand estimates, made before any value was opened (labelled; NOT results)

These are the author's priors, informed by the aggregate statements in section 0 (so not independent of them).

| # | statement | P |
|---|---|---|
| H1 | at least one galaxy has an L1 T0 flag (z_rob > 3) | 0.50 |
| H2 | at least one L1 flag reaches T1 (Bonferroni) | 0.25 |
| H3 | at least one L1 flag reaches T2 | 0.10 |
| H4 | every F1 T0 flag set contains every L1 T0 flag set (the structural fact) | 0.97 |
| H5 | any galaxy labelled "framework only" at T0 | 0.04 |
| H6 | any galaxy labelled "LambdaCDM only" at T0 (L2) | 0.04 |
| H7 | L2 is UNDEFINED for at least 20 of the 62 rows | 0.97 |
| H8 | the outcome wording is "both survive, only at gross-outlier sensitivity" or "inconclusive" | 0.85 |
| H9 | the known Danhaive cases carry the flags, if any; 1082948 is among them | 0.60 |
| H10 | Roman-Oliveira BRI1335-0417 is flagged at T0 by tier G | 0.15 |
| H11 | the planted P6 and P5 controls pass on the first run (no pipeline fix needed) | 0.65 |

## 17. What this lane cannot do

It cannot confirm or refute the flat law or LambdaCDM on power: sigma_tot is set by declared systematics, and the flag requires a gross outlier. It does not test a0(z) (the flat law only), does not model halos beyond an NFW with a c-M relation, and does not replace CFG197's pooled tests or CFG213/234's route analysis. The answer to "is there a z ~ 5 galaxy where a LambdaCDM dark-matter fit breaks" is whatever section 9 prints for the rows with z between 4.5 and 5.5 after the trials correction, together with every other galaxy that breaks either theory; if none reaches T2 the answer is "not at this sensitivity", and that is reported as found.
