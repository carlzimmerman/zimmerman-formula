# QX30 assumption ledger: what the hot-system data products assume, and what it does to the plain-law offset

Kappa = 1/2 FITTED; not theory closed. Criteria f861a41f04. Delta = log10(M_obs / M_law); + = model short; a negative shift
helps the law. Shifts are canonical / alt from qx30.out unless marked. Web-read source details are PROVISIONAL (page-tool
summaries of the arXiv / ar5iv HTML, not tables). Classes: ADM = admissible (graded), BOUND = documented, no native value
(enters only the all-favourable row), INADM = LCDM / simulation calibrated or no ground truth, NE = not evaluable on disk.

## X-COP (Ettori+2019, A&A 621, A39; Ghizzardi+2021 stars; Eckert+2019 non-thermal)

| # | Assumption | Source (section) | Direction on Delta | Size (dex) | Class | Prior record audit |
|---|---|---|---|---|---|---|
| X1 | Fiducial flat LCDM H0 70, Omega_m 0.3 in D_A (r ~ D, M_gas ~ D^2.5, M_* ~ D^2, M_HSE ~ D) | Ettori+2019 Sect. 1 (PROVISIONAL) | native D_A larger by 1.038, lowers Delta | **-0.0205 / -0.0205** (h 0.674); h 0.671: -0.023; h 0.70: +0.0002; h 0.73: +0.023 | ADM (C1, graded) | CFG407 model side only (+0.006); new |
| X2 | Same, with SZ-pressure T (M_HSE ~ D^0.5) | Ettori+2019 Sect. 2-3: XMM T to about 0.9 R500, Planck P outside | lowers Delta | -0.029 / -0.029 | BOUND (beta 1/2) | new |
| X3 | Omega_m alone (0.3 -> 0.3085) at z 0.056-0.090 | as X1 | none | +0.0002 | ADM (inside X1) | new |
| X4 | Mass model: the graded M_FORW assumes no mass model (forward method); paper's reference is NFW (backward) | Ettori+2019 Sect. 3, 3.1, 3.2 (PROVISIONAL) | NFW column -0.006; Einasto +0.018, ISO +0.008, Burkert +0.006 | 0.006-0.018 | BOUND (NFW = LCDM prior, NOT used in the grade) | new |
| X5 | Non-thermal pressure: not in the published masses; Eckert+2019 estimate ~6 % at R500 from a universal Omega_b/Omega_m | Ettori+2019 Sect. 3.3, 6; Eckert+2019 (PROVISIONAL) | correcting raises M_obs, raises Delta | +0.027 at R500 (smaller inside) | INADM (LCDM f_b); wrong sign | QX2 (<= 0.03, wrong sign); CFG922 |
| X6 | Simulation hydrostatic bias (1-b) ~ 0.8 | not applied by X-COP | raises Delta | about +0.1 if applied | INADM; wrong sign | CFG922 (wrong sign) |
| X7 | Clumping: azimuthal median, substructure masked | Ettori+2019 Sect. 2 (PROVISIONAL) | mean instead of median raises M_gas, lowers Delta | -0.022 / -0.022 at sqrt(C) 1.1 (PROVISIONAL upper end) | BOUND | CFG922 (cannot) |
| X8 | Stars: Chabrier IMF, BC03 SED | Ghizzardi+2021 Sect. 4 (PROVISIONAL) | Salpeter x1.8 lowers Delta | -0.026 / -0.025 | BOUND | QX26 (sigma-IMF: -0.019) |
| X9 | Stars: projected -> spherical x0.75 from a gNFW galaxy profile | Ghizzardi+2021 Sect. 4.1 | dropping it (upper bound) lowers Delta | -0.011 / -0.011 | BOUND | new |
| X10 | Stars: ICL not included (BCG is) | Ghizzardi+2021 Sect. 4.1 | adding ICL lowers Delta | -0.022 / -0.021 at ICL = 40 % of stellar light (PROVISIONAL upper end) | BOUND | MB1 (30 % ICL, different model); CFG922 NE |
| X11 | Stars: galaxies > 1e9 Msun, statistical background subtraction (COSMOS) | Ghizzardi+2021 Sect. 4, 4.1 | < 2 % of stars missing | < 0.001 | not LCDM; negligible | new |
| X12 | XMM T calibration (Chandra T higher for hot clusters, about 10-15 %, PROVISIONAL) | instrument, not in the paper's text read | Chandra scale raises M_HSE, raises Delta | about +0.04 to +0.06 if Chandra is right | INADM (no ground truth); wrong sign | new |
| X13 | Spectroscopic-like T weighting, sphericity, deprojection, sky background | Ettori+2019 Sect. 2-3 | spectroscopic T biased low (would raise Delta); triaxiality averages | <= 5 % (paper's systematic budget) | not LCDM; NE separately | new |
| X14 | Cold / warm gas, WHIM inside 0.7 R500 | none measured | lowers Delta | < 1 % of baryons | negligible | CFG922 (HI, BCG H2 cannot) |
| X15 | Fresh non-parametric HSE from n_e(r), T(r) | not on disk (only derived masses) | - | - | NE (needs the X-COP n_e, T, P profiles, < 1 MB, public) | new |

## Lovisari+2015 groups (A&A 573, A118)

| # | Assumption | Source | Direction | Size | Class | Prior audit |
|---|---|---|---|---|---|---|
| G1 | Fiducial H0 70, Omega_m 0.27 | L15 Sect. 1 (PROVISIONAL) | lowers Delta | **-0.019 / -0.019** (C1) | ADM (graded) | new |
| G2 | Masses: HSE (Eq. 7), double-beta n_e, parametric T (3 groups isothermal); not scaling-relation, not NFW | L15 Sect. 3.4-3.6, 5 | - | - | not LCDM | new |
| G3 | T profiles cover only part of R500; T extrapolated to R500 | L15 Sect. 5, 6.1.1 | either sign | not computable on disk | NE | new |
| G4 | No hydrostatic-bias correction (paper cites up to 20 % for mergers, Kettula+2013 low bias) | L15 Sect. 6.2 | applying raises Delta | +0.05 to +0.1 | INADM; wrong sign | new |
| G5 | Stars not measured; record uses f* = 0.5 (bracket 0-1) | QX5 / QX20 | f* 1 lowers Delta | -0.068 / -0.068 (f* 0.5 -> 1, record bracket) | BOUND (record's own) | QX5, QX20 |
| G6 | IMF | QX26 | lowers Delta | -0.037 | BOUND | QX26 |
| G7 | Clumping gas x1.1 | (as X7) | lowers Delta | inside the bound row | BOUND | new |

## Humphrey+2006 X-ray ellipticals (ApJ 646, 899)

| # | Assumption | Source | Direction | Size | Class | Prior audit |
|---|---|---|---|---|---|---|
| E1 | Distances: SBF (Tonry+2001, Cepheid zero point), no cosmology; NGC 6482 LEDA kinematic (Hubble flow) | H06 Table 1 note (PROVISIONAL) | NGC 6482 only | **-0.0023 / -0.0023** (C1) | ADM (graded) | new |
| E2 | Mass model NFW + stars (Hernquist) fitted to HSE; alternatives N04, Sersic, AC-NFW, parametric check | H06 Sect. VI.3, VI.4, VII | not on disk | - | NE (non-NFW fits not transcribed) | new |
| E3 | Baryon-fraction prior in the fit, 0.03 < f_b < 0.16 or Kay+2003 | H06 Sect. VI.3 (PROVISIONAL) | affects M*/L_fit and the halo beyond the data, little at 2-8 Re | unknown | INADM-flavoured (cosmic f_b); NE | new |
| E4 | Data constrain the mass to about 50-100 kpc (~10 Re) | H06 Sect. VI.3, VIII.2 | 2-8 Re is inside | - | ok | QX18 |
| E5 | Hot gas excluded from baryons (< 1 % of gravitating mass within 100 kpc) | H06 Sect. VI.1 | including lowers Delta | needs 0.3-6 M* to null (QX18), far above | NE on disk (bound) | QX18 |
| E6 | IMF Kroupa (graded) vs Salpeter (SPS) | H06 table; QX18 | lowers Delta | -0.139 / -0.136 (Salpeter alone: +0.071 / +0.053) | BOUND | QX18, QX26 |

## Coma UDGs (S1 inputs)

| # | Assumption | Source | Direction | Size | Class | Prior audit |
|---|---|---|---|---|---|---|
| U1 | Coma distance 100 Mpc class, h70 (R_e, d, host beta model all ~ D) | S1 inputs | lowers Delta | -0.016 to -0.033 (p 2..3, scaling bracket, not re-solved) | ADM (scaling only) | new |
| U2 | UDG M*/L, IMF | S1 / QX26 | - | QX26 / GB1 handle it | BOUND | QX26, GB1 |

## Bullet

Not in the QX20 ladder and not graded here (DB1 carries its sigma as PROVISIONAL).

## Reading

The one admissible, framework-native correction (D_A) moves every hot class by about -0.02 dex. The record's prior items
(non-thermal, HSE bias, T calibration) all have the sign that makes the miss larger. Every favourable BOUND together moves
X-COP by -0.139 / -0.137 dex, to +0.329 / +0.298, still about 6x the line.
