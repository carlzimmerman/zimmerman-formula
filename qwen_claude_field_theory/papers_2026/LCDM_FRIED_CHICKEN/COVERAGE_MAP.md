# COVERAGE MAP: which rival routes this folder has graded, and which it has not

Research experiment, quarantined in this folder. Rival language only, adopts nothing, never feeds any other folder. It maps how a LCDM-type group could reverse-engineer the law g_obs = (g_b + sqrt(g_b^2 + 4 g_b a0))/2 and the tie a0 = kappa c sqrt(G rho_DE(z)), so that a swoop can be recognised. kappa = 1/2 FITTED; not theory closed. Nothing here says the data favour either side.

Built 11-04 from README.md, FROZEN_RECIPE.md (A1 to A16), FROZEN_A17.md to FROZEN_A29.md. No number computed for this map. Literature notes are PROVISIONAL web look-ups (search-result summaries, no PDF or data downloaded) or marked FROM MEMORY.

## Status of the amendments

| amendment | route | one-line result |
|---|---|---|
| A1 to A4 (R1 to R11b) | SHMR + Diemer19 c, contraction, coreNFW-type core, thermal halo, per-galaxy halos, 12-14 feedback knobs | global recipes stall: R11 0.0415, R11b 0.0275 dex; per-galaxy R9 0.0152 (1026 params); halo scatter gate weak pass |
| A5 | KiDS-1000 lensing, two-halo term | all fail p >= 0.01; recipes do not lose to the law |
| A6 | R12, halo defined from the law | exact by construction; rho_DE needs a non-LCDM term |
| A7 | mixing theorem, energy, scattering carrier | 139/171 allowed; energy 0.52 of SN budget; sigma/m 0.63 to 40 cm^2/g |
| A8, A9, A12 | effective particle / condensate / one-scale action | window 9.2-13.7 eV; one EoS fails 0.52 dex; tie a posit |
| A10, A11 | R13 21 knobs + AGN cutoff, satellites, hydrostatic bias, X-COP | NOT COMPLETE; R14 passes only as ~1066-parameter patchwork |
| A13 | Hubble, Lambda coincidence, NFW central g, BTFR at f_b, Lambda pull | no native tie; Lambda coincidence passes the number, fails G5 |
| A14 | SHMR Tully-Fisher, Lambda halo edge, coupled quintessence, halo x Lambda | no tie |
| A15 | per-galaxy halo scale; one-recipe SIDM | NO TIE; one global factor ties law on data at 0.1941 to observed; SIDM 0.12 |
| A16 | knob blocks on R11b | 15 knobs 0.0263, NOT EXACT |
| A17 | fuzzy DM soliton | 0.149 to 0.092; fits switch the soliton off |
| A18 | DC14, coreNFW, FIRE-2 Lazar | 0.116 to 0.177; 0.073 to 0.084 with 3 knobs |
| A19 | velocity-dependent / per-galaxy SIDM, WDM, WDM+SIDM | 0.122, 0.080, per-galaxy 0.0487 (holdout 0.110), WDM 0.116-0.120 |
| A20 | interacting vacuum Q1, Q2; systematic mock | kappa_eff 0.47-0.54 at Q2 xi ~ -0.55 but drifts in z; mock a0 0.23-0.42 dex high |
| A21 | published hydro RAR results | none passes E1 (best 0.029); z dependence rises where measured |
| A22 | superfluid DM (BK/BFK) | 0.037 to 0.081; Lambda^4 = rho_DE only by hand |
| A23 | dipolar DM | free W reaches the law (a MOND reformulation); Lambda link imposed |
| A24 | Verlinde emergent gravity | fails E1 every reading; de Sitter reading is the Lambda coincidence with 1/6 |
| A25 | 28 LCDM ingredients stacked | NOT EXACT at any knob count, floor 0.022; tie fails |
| A26 | R11b in other cosmologies, epochs | slope +0.19 to +1.45, a(2.33)/a(0) 3.0 to 4.6 |
| A27 | dimensional lattice of LCDM constants | hits at chance rate; all fail G5 |
| A28 | per-galaxy fits with nuisances, reverse RAR | cored halos fit better (BIC) but sit +0.06 to +0.11 dex off the tied a0 |
| A29 (recipe31) | halo machinery in evolving DE (CPL DESI-like, thawing, freezing, quintom-A, EDE) + R11b CPL grid, new gate GT | RUNNING, frozen, no result yet |
| A30 to A32 (recipe32 to recipe34) | in progress in other sessions | RUNNING, no frozen file seen at build time; topics not read |

Gates used below: E1 rms to law <= 0.02 dex, E2 p95 per-galaxy <= 0.04, E3 worst bin <= 0.02, holdout unseen <= 0.025; tie gates G1 kappa_eff within 0.05 dex of 0.5, G2 slope 0.50 +- 0.05, G3 E5 band, G4 one constant over log M200 11 to 12.5 <= 0.1 dex, G5 operative at galaxy radii; GT tracking |log10[a(z)/a(0)] - 0.5 log10[rho_DE(z)/rho_DE(0)]| <= 0.05 dex at z 1, 1.5, 2.33.

"Test cost" for uncovered rows: EASY = analytic or one lib.grade call on SPARC; MEDIUM = a new recipe on lib.py/colossus, minutes; HARD = needs data or simulation output not in this folder.

## (1) Baryonic physics knobs

| family | status | result / why it matters, test cost |
|---|---|---|
| SN feedback cores (energy, bursty outflows) | COVERED A3, A4, A16, A18, A25 | global floor 0.022 to 0.04 dex; no tie |
| Feedback microphysical scale (Grudic+2020, a ~ pi G Sigma_crit ~ 0.1 G m_p/sigma_T) | PARTIAL A21 (graded as a round number "~1e-10" only) | a native constant with no cosmology: passes G3 and G4 trivially, fails G2 and GT only in evolving DE. Not graded as a mechanism or a shape. EASY |
| AGN feedback | PARTIAL A10 (core cutoff above M_cut), A18 (DC14 clipped above X -1.3) | AGN-driven expansion in massive discs not a block; massive discs dominate E3 high-g bins. MEDIUM |
| Cosmic-ray feedback | NOT COVERED | CR pressure changes gas and SFR more than the halo; enters as SHMR/core shift already spanned by A25 knobs. Low swoop value. MEDIUM (stand-in only) |
| Gas inflow/outflow, f_gas dependence | COVERED A3 (a4 exponent), A25 (gas-rich split) | in the floor |
| Baryon-tracing dark mass (scaled-HI / dark molecular gas, Pfenniger-type cold gas) | NOT COVERED in this folder | dark mass proportional to the HI surface density follows the baryons (the Renzo rule); a one-knob swoop on the law's shape. EASY on SPARC (g = g_bar + k g_gas) |
| Angular momentum / disc size set by halo spin (Mo-Mao-White, Dalcanton-Spergel-Summers) | PARTIAL A16 N2, R7 (c and M200 as powers of Sigma_b) | the compactness exponent was fitted, never checked against the spin-model prediction. MEDIUM |
| Disc-halo coupling: bars, dynamical friction | PARTIAL (absorbed in core knobs) | no separate block; low expected gain |
| Contraction / expansion (Blumenthal, Gnedin) | COVERED A1, A3, A25 | in the floor |
| Stellar IMF / M/L, per galaxy | COVERED A20 mock, A28 nuisance priors | |
| M/L as a systematic trend (variable IMF, colour or mass dependent Upsilon) | NOT COVERED | every recipe fixes Y 0.5/0.7; a global Upsilon(M*) or Upsilon(Sigma) trend reshapes g_b along the relation and could absorb E3 residuals. EASY |
| Gas mass systematics (He factor, H2) | NOT COVERED | a global gas multiplier moves low-g_b bins where E3 fails for LCDM rows. EASY |
| Reionisation / low-mass SHMR suppression | COVERED A25 (SL slope break) | |

## (2) Halo / structure knobs

| family | status | result / why, cost |
|---|---|---|
| c(M) norm and slope, per-galaxy c | COVERED A1 to A3, A28 | |
| c(M) model choice (Ludlow, Prada, Duffy) | COVERED in effect by norm/slope knobs | |
| SHMR norm, shape, slope break | COVERED A3, A25, A26 (z terms) | |
| SHMR scatter and Eddington bias | COVERED A4 T2, A20, A25 SS | |
| Assembly bias: scatter correlated across c, M*, size | NOT COVERED (A4 T2 drew independent scatter, stated as its limit) | the rival's best answer to the relation's small scatter is anti-correlated c and SHMR residuals. A20(b) left mock intrinsic scatter 0.091 against SPARC 0.081 on good points. EASY-MEDIUM |
| Halo shape / triaxiality / baryon-induced oblateness | NOT COVERED (all halos spherical) | in-plane gravity of a flattened halo differs from spherical at the 5-15 % level, mass-dependent. EASY (oblate homeoid in-plane force) |
| Environment (density-dependent c, external tides) | NOT COVERED for SPARC | the law's own record has environment questions; SPARC here has no environment column. HARD |
| Tidal stripping / truncation | PARTIAL A11 (lens-side truncation k R200) | mostly beyond the last measured point. EASY |
| Satellites vs centrals | PARTIAL A10/A11 (lensing), A21 (ZOMG split) | SPARC is mostly field |
| Splashback / halo edge | PARTIAL A14 T7 (zero-gravity radius goes as M^(1/3)) | same scaling class; low |
| Two-halo term | COVERED A5, A10, A11 | |
| Mass definition (200c, vir, 200m) | PARTIAL (stated approximations A18) | absorbed by SHMR norm |
| Substructure / clumpiness | NOT COVERED | negligible for rotation curves; low |
| Constant halo surface density (rho0 r0 ~ 141 Msun/pc^2, Donato+2009) | COVERED as a recipe R3 (rho0 r_c = Sigma*), A1 | its tie to Lambda is the logotropic row in (4) |
| Semi-analytic models (Di Cintio & Lelli 2016, Desmond 2017) | COVERED in effect: A18 DC14, A20(b) mock | |

## (3) Dark matter particle variants

| family | status | result / why, cost |
|---|---|---|
| CDM | COVERED (base everywhere) | |
| WDM | COVERED A19 d1 | 0.116 to 0.120 |
| SIDM constant, velocity-dependent, per-galaxy | COVERED A15, A19, A25 | 0.12, 0.080 (5 knobs), 0.0487 (343 params) |
| SIDM gravothermal core collapse (high-density branch, large sigma/m) | NOT COVERED (A19 keeps the low-density branch) | rivals use both branches for diversity; the law has no diversity, so collapse moves away from it. MEDIUM (A19 solver) |
| Dissipative / atomic / mirror DM (Foot, Foot & Vagnozzi) | NOT COVERED | claims a quasi-isothermal halo with r0 ~ 1.4 R_d, rho0 r0 roughly constant and Tully-Fisher L ~ v^3, with halo heating by supernovae (provisional). Dark mass follows baryons, a direct route to g_DM(g_b). MEDIUM |
| Fuzzy / wave DM | COVERED A17 | 0.149 to 0.092 |
| BEC with repulsive self-interaction (Thomas-Fermi, fixed core radius) | PARTIAL A8, A9, A22 (condensate window, polytrope) | fixed-radius n = 1 core is not separately graded; one length, no acceleration. EASY |
| Mixed DM (CDM+WDM, CDM+FDM) | PARTIAL A19 d2 (WDM+SIDM) | low |
| Decaying DM (to dark radiation or with a kick) | PARTIAL A20 Q1 (DM into vacuum) | DM to DR with mass loss expands halos by M_i/M_f and gives a clock tied to t, not rho_DE. EASY |
| Primordial black holes as DM | NOT COVERED | CDM-like on galaxy scales, no acceleration scale; dismissable analytically. EASY |
| DM-baryon scattering (heavy, millicharged) | PARTIAL A7 M3 (necessary sigma/m only) | see FKP in (5) |
| DM-radiation / ETHOS, SIMP | PARTIAL by analogy (A19 WDM + SIDM) | low |
| DM-only long-range force (Yukawa) | PARTIAL A14 T8 (analytic: rescales G) | no SPARC curve; low |

## (4) Dark energy variants

| family | status | result / why, cost |
|---|---|---|
| Lambda | COVERED A13, A23, A24, A27 | coincidence passes number, fails G5 |
| w0-wa CPL (DESI-like) | RUNNING A29 B1, B1p, B1u and the R11b CPL grid | GT first graded here |
| Quintessence, thawing / freezing | RUNNING A29 B2, B3 (CPL stand-ins only) | real potentials (exponential, PNGB, inverse power) not run; CPL stand-in is adequate for background |
| Phantom, quintom | RUNNING A29 B4, B1, grid | |
| Early dark energy | RUNNING A29 B5 | |
| k-essence with small sound speed: clustering DE inside halos (Creminelli+2010 type, FROM MEMORY) | NOT COVERED | the only GR route in which rho_DE sits inside a halo; DE mass fraction ~ (1+w) Omega_DE/Omega_m. A13 named exactly this gap ("rho_DE has to reach the halo by a term LCDM does not contain"). MEDIUM |
| DE-DM momentum exchange ("dark scattering", Simpson 2010, FROM MEMORY) | NOT COVERED (A20 is energy exchange only) | a drag on DM proportional to (1+w) rho_DE: rho_DE enters halo dynamics natively, slope 1 not 0.5. EASY analytic |
| Running vacuum (Lambda + nu H^2) | COVERED in effect A20 Q1 (Q proportional to H rho_c in the matter era) | |
| Interacting vacuum / coupled quintessence | COVERED A20, A14 T8 | |
| Unified dark fluids: Chaplygin, generalised Chaplygin | NOT COVERED | halo behaviour poor in the literature (from memory); low |
| Logotropic dark fluid (Chavanis) | NOT COVERED | claims, with no free parameter, a universal halo surface density Sigma0 = 0.01955 c sqrt(Lambda)/G ~ 133 Msun/pc^2 and (2026 abstract) a universal acceleration and Tully-Fisher, "an alternative to MOND" (provisional). G Sigma0 is c sqrt(G rho_DE) times a number: this is the most direct published claim of the tie. EASY-MEDIUM |
| Chameleon, f(R) (Hu-Sawicki) | NOT COVERED | screening keyed to potential, 4/3 G boost when unscreened: no acceleration scale. EASY analytic |
| Symmetron | NOT COVERED | density threshold, Yukawa range ~ Mpc, G boost; scale only by choice. EASY analytic |
| K-mouflage | PARTIAL A12 (one-scale action L = -rho_DE[1 + c H(s)], s = grad phi/sqrt(rho_DE), a posit) | published k-mouflage screens on acceleration with the scale set by the DE energy density (provisional): a native sqrt(rho_DE)/M_Pl acceleration with slope 0.5. Standard K(X) not graded on SPARC. MEDIUM |
| Galileons / Vainshtein | NOT COVERED | Vainshtein radius gives g ~ (GM)^(1/3) H^(4/3): mass-dependent like A14 T7, fails G4. EASY analytic |
| Horndeski / beyond-Horndeski / DHOST | NOT COVERED | Vainshtein breaking inside sources gives O(1) potential corrections, no acceleration scale. EASY analytic |

## (5) Near-MOND hybrids

| family | status | result / why, cost |
|---|---|---|
| Superfluid DM (Berezhiani-Khoury) | COVERED A22 | 0.037 to 0.081; tie by hand |
| Dipolar DM (Blanchet) | COVERED A23 | free W reaches the law; Lambda link imposed |
| Emergent gravity (Verlinde, Hossenfelder) | COVERED A24 | fails E1; de Sitter reading is the coincidence |
| DM-baryon interactions that make the RAR (Famaey, Khoury & Penco 2018, arXiv 1712.01316; BIDM follow-up) | PARTIAL A7 M3 | a particle-DM route claiming the RAR emerges, with sigma times energy exchange inversely proportional to DM density (provisional). Whether its scale ties to rho_DE is untested. MEDIUM |
| Modified inertia from the de Sitter Unruh effect (Milgrom 1999, FROM MEMORY) and horizon variants (quantised inertia) | NOT COVERED as a mechanism (A13 T2, A27 graded the number only, with G5 as Lambda's pull) | the one route with a claimed mechanism tying a0 to Lambda; G5 does not apply in the same way to an inertia law. Its interpolation is fixed, so a shape test settles E1. EASY |
| Aether-scalar-tensor (Skordis-Zlosnik AeST), TeVeS, Einstein-aether | NOT COVERED | relativistic MOND fitting CMB; a0 is a free Lagrangian constant, so slope 0 natively. EASY analytic (the interpolation is the free function, like A23) |
| Bimetric MOND (BIMOND), MOG (Moffat STVG), conformal gravity (Mannheim), non-local gravity (Mashhoon) | NOT COVERED | MOG and conformal gravity have published universal parameters; conformal gravity's gamma0 c^2 is a cH0-type term. EASY each on SPARC |

## (6) Observational / systematic readings

| family | status | result / why, cost |
|---|---|---|
| Distance errors | COVERED A20(b), A28 | |
| Inclination errors | COVERED A20(b), A28 | |
| Per-galaxy M/L | COVERED A20(b), A28 | |
| Error-dominated scatter | COVERED A20(b) B1 | weak pass, error-driven |
| Fitting method / a0 circularity | PARTIAL A20(b) B2, A28 | |
| Sample selection (SPARC quality, HI-rich, edge cuts) | PARTIAL A28 (Q<3, Inc>=30 subset) | a selection-only reading of the law's tightness is ungraded. MEDIUM (mock with cuts) |
| Non-circular motions, bars, warps | NOT COVERED | biases inner V low in dwarfs and barred discs; moves high and low g_b ends differently. MEDIUM (mock bias model, no 2D data) |
| Beam smearing | NOT COVERED | needs beam sizes per galaxy, not in this folder. HARD |
| Pressure support / asymmetric drift | NOT COVERED | in gas-rich dwarfs sigma ~ 8-10 km/s adds V^2 terms at low g_b, exactly where LCDM rows miss E3. EASY (mock and real-data correction) |
| Disc thickness in V_bar | NOT COVERED | 5-10 % on inner g_b; low. EASY |

## (7) Simulation-based claims

| family | status | result / why, cost |
|---|---|---|
| Hydro sims, RAR emerges (EAGLE, MUGS2, NIHAO, MBII, ZOMG, Magneticum, FIRE-2) | COVERED A21 | none passes E1; tie not on record |
| Analytic halo-scale argument (Navarro+2017) | COVERED A15, A21 | |
| "RAR follows from BTFR plus any halo" (Wheeler, Hopkins & Dore 2019, FROM MEMORY) | PARTIAL A13 T4, A14 T6 | moves the question to the BTFR normalisation, which carries a0; a SPARC check is cheap. EASY |
| Varied-Lambda sims (Barnes, Salcido) | COVERED in effect A26 (analytic), A21 (no RAR reported) | |
| SIDM / FDM sims | COVERED by analytic stand-ins A17, A19 | |
| Emulators / ML on sims | NOT COVERED, out of scope | HARD |

## (8) Numerology / coincidence routes

| family | status | result / why, cost |
|---|---|---|
| Lambda coincidence c^2 sqrt(Lambda/3)/2 pi | COVERED A13, A15 U2, A23, A24, A27 | |
| Hubble cH/2 pi | COVERED A13 T1 | |
| Dimensional lattice of LCDM constants | COVERED A27 | chance rate |
| Microphysical lattice (G, m_p, m_e, sigma_T, alpha, hbar) | NOT COVERED (A27 excluded particle constants) | Grudic's 0.1 G m_p/sigma_T ~ 1.7e-10 is a native non-cosmological look-alike. EASY (reuse recipe29) |
| Anthropic / timing (a0 ~ cH0 because we live now) | NOT COVERED | not testable here |

## Count

Family rows in sections (1) to (8): 85. COVERED (incl. "covered in effect"): 33. PARTIAL: 19. RUNNING: 4 (A29 rows; A30 to A32 not counted, topics unread). NOT COVERED: 29.

Covered or partial: 52 of 85; not covered: 29; running: 4.

## Ranked uncovered families, with lane briefs

Every lane: SPARC from lib.load(), Y 0.5/0.7, lib.grade (E1, E2, E3, holdout GS[::2] to GS[1::2]), rms to observed against 0.1951; tie gates G1 to G5 plus GT in A29's backgrounds (reuse recipe31's rho_DE(z) tables once A29 lands; do not touch recipe31 to recipe34). Freeze criteria before any number, own FROZEN_A file, single thread, minutes.

**1. Logotropic dark fluid (unified DM+DE, Chavanis).** Route: the published claim that halo surface density is Sigma0 = 0.01955 c sqrt(Lambda)/G with no free parameter. Equations: logotropic P = A ln(rho/rho_P), A set by rho_DE; halo = logotropic Lane-Emden solution, central rho0 and r_h with rho0 r_h = Sigma0; take the profile as published (or the r^-1 envelope the 2026 abstract cites), plus SPARC baryons. Gates: E1 to E3 with 0 knobs and with one knob (r_h per galaxy against a global rule); G1 from G Sigma0 x the paper's prefactor against 0.5 c sqrt(G rho_DE); G2 slope (A, hence Sigma0, scale as sqrt(rho_DE): expected 0.5 natively, which would be a first); G3 and GT, since A is constant if the fluid behaves as Lambda today but rho_DE(z) of the fluid follows its own EoS; G4 across hosts; G5 halo gravity. This is the most direct published claim of the tie; the paper's own derivation of the 0.01955 must be read (look-up only).

**2. K-mouflage dark energy with acceleration screening.** Route: a published DE class whose screening radius R_K is set by an acceleration built from the DE scale M^4 ~ rho_DE. Equations: L = M^4 K(X), X = -(d phi)^2/(2 M^4), coupling beta phi rho/M_Pl; static solution K'(X) grad phi = beta M_Pl g_N (cf. A12); standard K = -1 + X + K0 X^n. Grade (i) a_K = beta M^2/M_Pl type scale against G1 and G2 (expected slope 0.5 natively if M^4 = rho_DE0); (ii) the unscreened force law on SPARC (expected a constant (1 + 2 beta^2) G boost, not the law's sqrt tail, so E3 should fail unless n = 3/2-like MOND kinetic terms are chosen, which is A12's posit); (iii) GT: M^4 is a Lagrangian constant, so a stays flat while rho_DE(z) moves in A29 backgrounds; (iv) Cassini from A9/A12 limits.

**3. Modified inertia from the de Sitter Unruh effect.** Route: inertia set by the difference of Unruh temperatures in de Sitter space. Equations (FROM MEMORY, to check): g_N = sqrt(g^2 + a_L^2) - a_L, a_L = c^2 sqrt(Lambda/3), with the MOND-limit a0 a fixed multiple of a_L. Gates: E1 to E3 with 0 knobs (shape fixed, so a single run decides), then one prefactor knob; G1 (expected 0.461-type number), G2 0.5 by construction, G3 flat; GT: if a_L uses H_inf(z) of the background, compute tracking in A29's CPL rows; G5 here asks whether an inertia law acts at 10 kpc (it does by posit; state it as a posit, as A24 did). Shape mismatch would settle it whatever the tie does.

**4. Dissipative / atomic / mirror DM.** Route: a halo that cools and is reheated by supernovae, so it follows the baryons. Equations: quasi-isothermal rho = rho0/(1 + r^2/r0^2), r0 = k R_d (published k ~ 1.4), rho0 r0 = Sigma_h constant, or energy balance Gamma_heat (SN rate from SFR proxy L) = Gamma_cool; 1 to 3 global knobs (k, Sigma_h, mass-scaling exponent). Gates: E1 to E3, holdout; G1 from G Sigma_h; G2 (Sigma_h set by dark-sector atomic physics, slope 0 natively expected); G3, GT (a constant of dark atomic physics stays flat); G4; G5 halo gravity. A pass on shape would be the strongest LCDM-adjacent shape swoop on record.

**5. Clustering dark energy (c_s ~ 0 k-essence) and DE-DM momentum exchange.** Route: the two GR routes that put rho_DE into halo dynamics. Equations: clustering DE mass in a collapsed halo M_DE/M_m ~ (1+w)(Omega_DE/Omega_m) evaluated at collapse (FROM MEMORY, Creminelli+2010 type), added to the R11b halo; dark scattering drag a_drag = (1+w) rho_DE (sigma_D/m) v on DM, integrated over 10 Gyr as a halo expansion. Backgrounds: A29's CPL rows (w != -1 needed, both vanish at w = -1). Gates: E1 to E3 on R11b with the extra term and its knob; G1, G2 (expected slope ~1 for drag, ~1 times (1+w) for clustering), G3, GT in each A29 background, G4, G5. Expected: tiny at DESI-like 1+w, but it is the only native carrier, so the size needs a number.

**6. Famaey-Khoury-Penco DM-baryon interaction.** Route: collisional DM-baryon exchange tuned so the RAR emerges in equilibrium. Equations: from arXiv 1712.01316 (read the text; provisional): heating/cooling balance with sigma times energy exchange proportional to 1/n_DM, giving rho_DM set by local g_b; implement as halo density from the balance condition at each radius plus NFW outside. Gates: E1 to E3, holdout; G1 from the cross-section parameters; G2 (slope 0 unless the cross-section scale is tied to Lambda by hand), G3, GT, G4, G5; and A7 M3's required sigma/m as a consistency check.

**7. Correlated halo scatter (assembly bias) plus a systematic M/L trend.** Route: the rival's scatter answer: the law's tightness from anti-correlated c and SHMR residuals, and its shape from Upsilon(M*). Equations: A20(b) mock with log c and log M200 residuals drawn with correlation rho in {-0.3, -0.6, -0.9}; Upsilon_disk = 0.5 (M*/1e10)^p, p in [-0.2, 0.2]; observer fit as A20(b). Gates: B1 on good points (errV/V <= 0.05) within 0.02 dex of SPARC's 0.081; B2 fitted a0 within 0.05 dex of A0; E1 to E3 of the noiseless mock; tie gates G1, G3, GT on the mock's fitted a(z) (halo routes expected to follow H(z), as A26). Answers whether tightness alone can be bought.

**8. Microphysical acceleration (Grudic feedback scale) and a particle-constant lattice.** Route: a native non-cosmological constant, 0.1 G m_p/sigma_T ~ 1.7e-10, passes G3 and G4 trivially. Equations: a_F = eta G m_p/sigma_T with eta from Grudic+2020; then recipe29's lattice with G, hbar, c, m_p, m_e, sigma_T, alpha added and the same look-elsewhere slide. Gates: G1, G2 (0 natively), G3, G4, GT (fails wherever rho_DE(z) moves, flat a), G5 (Eddington-limited feedback at disc radii: by posit). Shows whether the observable-only gates (A15 U2) can separate a feedback constant from the tie, and whether particle constants hit the target more than chance.

Not ranked but cheap if wanted: asymmetric-drift correction on SPARC dwarfs (EASY), scaled-HI dark mass (EASY), oblate halos (EASY), screened-gravity analytic sheet (chameleon, symmetron, f(R), Galileon, Horndeski: one paragraph each).

Sources (provisional look-ups, 11-04): arXiv 1504.08355, ar5iv 1810.11349, arXiv 2603.21302 (logotropes); arXiv 1712.01316 (Famaey, Khoury, Penco); arXiv 1403.5420, ar5iv 1504.01493, arXiv 2201.10817 (k-mouflage); arXiv 1307.1755, 1409.7174, 1502.07817 (dissipative DM).

Rival language; adopts nothing. kappa = 1/2 FITTED; not theory closed.
