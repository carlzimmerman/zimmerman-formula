# PB2 FROZEN CRITERIA: the ceiling f_max(M) on primordial black holes, 1e0 - 1e9 Msun, standard vs framework

Written and committed alone, before any PB2 script, lookup-driven table or PB2 number. Adopts nothing.
kappa = 1/2 FITTED; not theory closed. No particle: PBHs are compact objects born in the radiation era; their mass is
a component that must be paid for. The cold sector stays RETIRED (11-01); nothing here reinstates it. Footings canonical
a0 = 9.3603e-11 and alt 1.1312e-10 m/s^2, graded separately, never pooled.

## 0. Record read before freezing
- CFG510 Part B: f = 1 bands for 1e17 g - 1e55 g, all RECALLED, UNVERIFIED; FM1 (dynamical bounds at full strength)
  and FM2 (microlensing tau 0.67-0.85 x NFW) were computed for the SETTLED-PHANTOM ontology, which assumed a cold
  component of 5.364 Omega_b. That component is retired; PB2 does NOT reuse FM1/FM2 numbers. In PB2 the only real mass
  is baryons + PBHs.
- DB1: only 1e2-1e7 Msun black holes pass DB1's order-of-magnitude gates as cluster dark baryons; millilensing and
  dynamical limits not computed. DB1/CFG510 need CBDM ~ 19-54 % of cosmic baryons in clusters alone (PROVISIONAL).
- PB3 frozen criteria (read, not edited): PBH spheroid M_PBH(<r) = F M_b,tot min(r / r_vir, 1),
  r_vir = [3 (1+F) M_b,tot / (4 pi 200 rho_c0)]^(1/3), h = 0.70 (PROVISIONAL convention). PB2 uses the SAME convention
  for galaxy-hosted PBH populations so PB2 and PB3 numbers can be combined in PB4.
- Not re-derived here: PB1 (seed growth under R1), PB3 (cluster/SPARC budget). A rotation-curve budget row is
  REPORTED ONLY (section 4, FW-RAR) and does not enter the envelopes: it is PB3's territory.

## 1. Definitions and grid
- f_b = Omega_PBH / Omega_b (primary). Also reported: f_DM-equivalent = Omega_PBH / Omega_c(LCDM) = f_b / 5.364
  (S = Omega_c / Omega_b = 5.364, record value) and f_m = Omega_PBH / Omega_m(LCDM) = f_b / 6.364, so others can convert.
- Monochromatic mass function. Grid log10(M/Msun) = 0.0 to 9.0 step 0.05; table rows at 1e0, 1e1, ..., 1e9.
- "STANDARD" f_b,max(M) = literature f_DM,max(M) x 5.364: the same physical Omega_PBH, re-expressed. No framework input.
- "FRAMEWORK" f_b,max(M) = the standard row after the computed modifications of section 3. Ratio FW/STD reported per row:
  > 1 LOOSENS, < 1 TIGHTENS, = 1 UNCHANGED (within 1e-12).
- Each literature value carries its arXiv id and a status: "page-read, provisional" (read from an arXiv abstract or page
  text this session) or "recalled, unverified". Summariser reads are provisional (record rule 10-02). A row's value is
  piecewise log-log linear between frozen anchor points; outside its anchors a row sets no bound.

## 2. Bound rows (each its own row; R = robust, C = contested, G = Gaussian-formation only)
| id | bound | class | primary sources to read |
|---|---|---|---|
| A1 | CMB accretion, spherical, naked (collisional ionisation) | R | Ali-Haimoud & Kamionkowski 2017, 1612.05644 |
| A2 | CMB accretion, disk (photoionisation / disk geometry), naked | C | Poulin+2017, 1707.04206; Serpico+2020, 2003.09806 (naked curve) |
| A3 | CMB accretion, disk, CDM-halo dressed | C | Serpico+2020, 2003.09806 (dressed curve) |
| X1 | X-ray / radio from accreting Galactic PBHs (Galactic centre, Chandra/VLA, Gaia velocities) | C | Gaggero+2017, 1612.00457; Manshanden+2019, 1812.07967 |
| D1 | wide binaries (halo) | R | Monroy-Rodriguez & Allen 2014, 1406.5169; Yoo+2004; Quinn+2009 |
| D2 | UFD / Eridanus II star-cluster heating | R | Brandt 2016, 1605.03665; Koushiappas & Loeb 2017 |
| D3 | Galactic disk heating | R | Lacey & Ostriker 1985; Carr & Sakellariadou 1999; Carr+2021 review 2002.12778 |
| D4 | dynamical friction to the Galactic centre | R | Carr & Sakellariadou 1999; Carr+2021 review 2002.12778 |
| L1 | Galactic microlensing toward the LMC (MACHO/EROS) | R | EROS-2 Tisserand+2007, astro-ph/0607207; MACHO Alcock+2001 |
| L2 | quasar microlensing (lens-galaxy compact fraction) | C | Mediavilla+2017, 1708.01187; Esteban-Gutierrez+2022 |
| L3 | millilensing of compact radio sources | R | Wilkinson+2001, astro-ph/0101328 |
| L4 | FRB / GRB lensing | C | CHIME FRB (Leung+2022 / Zhou+2022); GRB (Ji+2018 is a forecast: not scored if forecast only) |
| G1 | LVK merger rate of early (primordial) binaries | R | Ali-Haimoud+2017 1709.06576; Raidal+2019 1812.01930; Hutsi+2021 2012.02786 |
| G2 | PTA / SIGW (Gaussian peaks) | G | NANOGrav 15-yr interpretations, e.g. Franciolini+2023 2306.17149 |
| S1 | mu / y distortions from the Gaussian peaks (FIRAS) | G | Nakama+2018 1710.06945; Kohri+2014; non-Gaussian escape Nakama+2016 1609.02245 |
| P1 | Lyman-alpha Poisson power | R | Afshordi+2003 astro-ph/0302035; Murgia+2019 1903.10509 |
| P2 | Planck CMB isocurvature from Poisson noise (DERIVED here, section 3) | R | Planck 2018 X (1807.06211) beta_iso limit |
Retracted/forecast-only items are listed in the output and not scored. A row whose value cannot be located even as a
recalled number is reported "NOT LOCATED" and not scored (never invented).

## 3. Framework modifications (computed, not hand-waved)
Common inputs (frozen): Omega_b = 0.049, S = 5.364, h = 0.674 for densities (Planck-like; PB3's h = 0.70 only inside the
r_vir rule), MW observed v_c = 220 km/s at 8 kpc; standard MW DM halo NFW r_s = 20 kpc, rho(8 kpc) = 0.0105 Msun/pc^3
(0.4 GeV/cc, recalled). nu(y) = 1 / (1 - exp(-sqrt y)) (record nu_mono). External-field (EFE) approximation:
g = nu((g_N + e a0)/a0) g_N (algebraic 1-D form, disclosed approximation).

FM-H (galaxy-hosted PBH population; used by D1, D2, D3, D4, L1, L2, X1). No CDM halo exists; PBHs are collisionless and
do not dissipate. Galaxy PBH content = f_b x M_b,tot in PB3's spheroid, M_PBH(<r) = f_b M_b,tot min(r / r_vir, 1)
(rho = f_b M_b,tot / (4 pi r_vir r^2)), velocity dispersion v_c / sqrt2 (isothermal tracer, disclosed).
MW: M_b,tot = 6e10 Msun primary (CFG510 value); brackets M_b,tot 1.5e11, and r_vir x {0.5, 2} (PB3's brackets).
Eri II (D2): PBH content f_b x eta x M_*, distributed like the stars (Plummer, r_h = 280 pc, M_* = 6e4 Msun, recalled);
eta = M_b,orig / M_* = 3 primary, brackets {1, 10}. Standard comparison density: Eri II dynamical density inside r_h
from sigma = 6.9 km/s (recalled), M_dyn = 4 sigma^2 r_h / G, minus stars.
For a bound proportional to the local PBH density at radius r: FW/STD factor on f = (rho_DM,std(r) / rho_PBH,fw(r; f_b=1))
/ S. Radii: D1, D3 at 8 kpc; D4 at r_c = 2 kpc (plus the DF-time factor below); X1 at 1 kpc; L1 = line-of-sight
optical-depth integral to the LMC (l = 280.5, b = -32.9, 50 kpc); L2 = the same SIS ratio as the MW at 8 kpc
(lens-galaxy proxy, disclosed). A host can hold N = f_b M_b,tot / M PBHs; where N < 1 at the row's f the row's
host-based bound is set to NO BOUND for that mass (incredulity limit), for both STD (with the DM halo mass 1e12 MW,
M_dyn for Eri II) and FW.
- D1 extra (law binding of the binary): factor x nu_bind / nu_imp^2, nu_bind = nu(e_MW) with e_MW = g_MW(8 kpc)/a0,
  nu_imp = nu((G M / b^2 + g_MW)/a0) at b = a_bin = 0.1 pc (frozen).
- D4 extra (dynamical-friction medium): the medium is real mass only, linear QUMOND response: rho_med,fw = nu rho_real.
  MW baryons Hernquist M = 6e10, a = 3 kpc (disclosed toy), rho_dyn from the law's g. Factor x
  sqrt(rho_dyn / (nu rho_real)) at r_c (dragged mass ~ normalisation x r_DF, r_DF ~ rho_med^(1/2)).

FM-A (accretion, A1-A3). No CDM dressing exists: A3 (dressed) is replaced in FW by the naked row A2. Baryon dressing under
the law is computed at z_ref = 600 (brackets 300, 1000): v_eff = sqrt(c_s^2 + v_bc^2), c_s from T = T_CMB(z) (coupled),
v_bc = 30 km/s (1+z)/1000 (recalled); EFE e = 0.026 primary (EB1b's upper web value), brackets 0.006 and 0.1.
r_a = outermost root of r g_law(r) = v_eff^2; Phi_x(r_a) = integral_{r_a}^{100 r_a,N} (g_law - g_N) dr;
E = (r_a / r_B)^2 exp(Phi_x / v_eff^2) (density boost of an isothermal-like envelope at v_eff: disclosed recipe).
Luminosity boost E_L = E^p, p = 2 for A1 (L ~ Mdot^2), p = 1 for A2; capped so that the boosted mdot <= 1 (Bondi,
lambda = 1, Eddington Mdot at 10 % efficiency). FW f_max = STD_naked f_max / E_L.
Background: the standard H(z) is used throughout (assumption A_BG, disclosed). Sensitivity, not scored: a baryon-only
background (Omega_m = Omega_b + Omega_PBH) changes energy injection per Hubble time by H_std/H_bo at z_ref.

FM-L (lensing, L3, L4 and cosmological rows). Uniform cosmological optical depth ~ Omega_PBH x distance integrals at the
standard background: UNCHANGED in f_b units (factor exactly 1). Galactic/lens-galaxy rows use FM-H.

FM-G (G1). Early-binary decoupling a_dec = (Omega_r / Omega_PBH)(x / xbar)^3 depends on Omega_PBH only; the AHK rate
R ~ f^2 (f^2 + sigma_eq^2)^(-21/74) has a torque term from the other matter's small-scale fluctuations, sigma_eq = 0.005
(recalled). In FW the other matter is baryons, Silk-damped on binary scales: sigma_eq -> 0. FW f_max solves
R_fw(f) = R_std(f_std,max), f in Omega_PBH / Omega_m(LCDM) units for the formula. Late-time disruption factors: same.

FM-P (P1, P2). P2 derived in both: Poisson Delta^2 = k^3 / (2 pi^2 n_PBH), CDI-equivalent S = (Omega_PBH / Omega_c) delta,
limit Delta^2_S <= beta/(1-beta) A_s with beta = 0.04, A_s = 2.1e-9, k = 0.1 /Mpc (frozen). FW: the matter entropy
amplitude is Omega_PBH delta / Omega_m,cluster; read with Omega_c -> Omega_c (same CMB-fit background, A_BG) -> UNCHANGED;
noted as A_BG-conditional. P1: linear growth of the Poisson seed from z = 3400 to z = 3 in the standard H(z), clustering
matter = CDM + PBH (STD) vs baryons (released at z = 1100) + PBH (FW), Newtonian gravity; FW/STD factor on f from the
baryon-density amplitude ratio squared at the limiting f (iterated). The law's own growth is PB1's question: P1's FW
value is labelled NEWTONIAN-GROWTH CONDITIONAL.

FM-S (S1, G2). Photon-baryon physics (Silk damping, SIGW from horizon-entry peaks) has no CDM input: UNCHANGED in f_b
units. Gaussian-only: a non-Gaussian (heavy-tailed) formation escapes S1/G2 (Nakama+2016); stated, not scored.

## 4. Envelopes and labels
- ROBUST envelope = min over R rows (contested and Gaussian rows dropped). AGGRESSIVE envelope = min over R + C rows.
  GAUSSIAN envelope = AGGRESSIVE plus G rows (reported only; labels never use it). Each for STD and FW, both footings.
- FW-RAR (reported only, not in any envelope; PB3 territory): the PBH spheroid's mass inside 30 kpc added to the MW's
  6e10 baryons in deep MOND shifts the outer g by Delta log g = 0.5 log(1 + M_PBH(<30)/M_b); f_b where it reaches 0.05 dex.
- Labels per mass and threshold X, on the ROBUST envelope, framework primary brackets: WINDOW OPEN at f_b >= X if
  f_b,max >= X, else CLOSED at X. X in {1, 0.2, 1e-2, 1e-4}. Main threshold X = 0.2 (DB1's cluster amount). A label
  is FRAGILE if any frozen bracket (M_b,tot, r_vir, eta, z_ref, e) flips it. The open mass range at each X is reported.
- Each table row names the dominant (minimum) bound.

## 5. Checks (exit 1 if any fails)
- KA1: the STANDARD ROBUST envelope at 1e1, 1e3, 1e5 Msun within a factor 3 of review envelope values (Carr+2021
  2002.12778 and/or Green & Kavanagh 2021 2007.10722), page-read if possible. Recalled reference values, disclosed now
  (f_DM): 1e1 ~ 3e-3 (LVK); 1e3 ~ 1e-3 (accretion / dynamics); 1e5 ~ 1e-4 (accretion / Ly-alpha). If rows were taken from
  the same review, KA1 is marked NOT INDEPENDENT for that mass.
- KA2: P2 derived vs any literature CMB-Poisson value (if located): within 1 dex, else flagged.
- KA3: G1 FM-G with sigma_eq kept at 0.005 returns the STD row exactly.
- MUTATE M1: a planted R row f_DM = 1e-6 over 1e3-1e4 Msun must move both envelopes there and flip X = 1e-4 to CLOSED.
- MUTATE M2: all framework modifications off (factors 1, A3 kept, sigma_eq kept) must return FW == STD exactly (max |diff| 0).
- MUTATE M3: FM-H with the PBH spheroid normalised to the standard halo (rho_fw = rho_DM,std / S at f_b = 1) must return
  FW == STD for every FM-H row (to 1e-12).
- Footings never pooled; a0 enters only through nu (FM-A, D1, D4).

## 6. Disclosures fixed in advance
Every literature value is provisional or recalled. The MW/Eri II inputs, FM-A recipe, EFE form and A_BG are disclosed
choices. PB2 does not claim PBHs exist, are needed, or are favoured by data. Nothing here says the data favour the framework.
