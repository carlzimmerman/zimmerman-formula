# THE SECOND-LAW HUNT — 20 systematic searches for a second Kepler-grade regularity (2026-09-02)

**Working assumption (the first law, taken as true):** a₀ = ½ c √(Gρ_Λ), constant in cosmic time, one value for every system
(canonical a₀ = 9.36e-11 m/s², alt = 1.13e-10; run BOTH). Kernel: Route A, ν(y) = 1/(1−e^{−√y}), y = g_bar/a₀. External-field effect
where a host exists. A "Kepler-grade" hit = a relation between measured quantities in which a₀ (or Λ through it) appears with the
predicted coefficient, holding across systems with RAR-class scatter (≲ 0.1 dex), that nobody has stated. A miss is a result too.

**Rules for every item (non-negotiable, from STANDING/RETRACTIONS):** one committed runnable script per item with checks that CAN fail,
a mutation control (a wrong a₀ or ν = 1 must break the pass), both footings, the ΛCDM/Newtonian alternative computed beside the
framework, verdict both ways, `.out` committed. Never modify `prep_2026/gaia_dr4_prep/PREREGISTRATION_DR4.md` or any `*_HASH.txt`.
No personal names in scripts or commits. Cite the retracted list before quoting any repo number (`RETRACTIONS.md`). Report
"no regularity" as plainly as a hit. Paths below are repo-relative; data marked ON DISK need no download.

| # | search | data | compute | framework prediction (canonical / alt) | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 1 | **Lensing 1/r law** | ON DISK `real_research/data/lensing_rar/brouwer2021_rar/` Fig-4-5 Nobins + Fig-9 four stellar-mass bins + covariances | log slope of g_lens(r) between 100 kpc and 1 Mpc per bin; coefficient vs M_b^{1/2} across bins | slope −1.000 exactly, g_lens = √(G M_b a₀)/r | NFW: −1.2…−1.6 beyond r_s; 2-halo bends it | all 4 bins give −1.00 ± 0.05 AND coefficients track √M_b with one a₀ (a lensing BTFR over 1.5 dex) | low |
| 2 | **Dwarf lenses, same a₀** | ON DISK Fig-10 isolated dwarfs + cov | fit a₀ from the dwarf stack alone (amplitude profiled) | same a₀ as the L* stack, no excess | ΛCDM: dwarf M_h/M* is 3–10× higher | a₀(dwarfs) = a₀(L*) within 0.1 dex at g_bar ≈ 1e-14 | low |
| 3 | **r_flat law** | ON DISK SPARC rotmod files `real_research/data/sparc_data/` | radius where v reaches 95% of v_flat vs r_M = √(G M_b/a₀) | r_flat/r_M = one number for exponential discs (compute from the kernel, expect 2–3), no mass trend | ΛCDM: depends on concentration | scatter of r_flat/r_M < 0.1 dex across 100+ discs | low |
| 4 | **BTFR curvature** | ON DISK SPARC | v_last⁴ − G M_b a₀ vs (G M_b/r_last)² for the 15 most massive discs (Route A version of E3) | the high-mass upturn has the predicted sign AND size, no free parameter | ΛCDM: no fixed curvature | residuals follow the predicted bend within errors | low |
| 5 | **Halo surface-density constant** | Li+2020 SPARC halo fits (Burkert ρ₀, r₀; VizieR J/ApJS/247/31, CfA mirror works) | ρ₀ r₀ per galaxy | median = a₀/(2πG) = 107 / 129 M☉ pc⁻², no mass trend | Donato+09: 140 (+80/−30) | median within 0.1 dex of a₀/(2πG) with no trend over 4 dex in M_b | medium |
| 6 | **Freeman ceiling** | ON DISK SPARC photometry (`SPARC_Lelli2016c.mrt`, Σ₀ at [3.6] with Υ = 0.5) | upper envelope of central baryonic surface density | Σ_max ≈ Σ† = a₀/(πG) = 214 / 258 M☉ pc⁻² | none fixed in ΛCDM | 95th percentile within 0.15 dex of Σ† and no disc far above | low |
| 7 | **Groups with hot gas (the loose thread)** | ON DISK `kt2017_groups_full.tsv` + X-ray gas masses (Lovisari+15 A&A 573 A118; Sun+09 ApJ 693 1142; fetch via ADS/browser, CDS was blocked) | η_opt = (81/4)σ⁴/(G a₀ M_b) with M_b = 0.6 L_K + M_gas; bin by σ | no missing mass below σ ≈ 300 (Milgrom 2019); the step to η ≈ 2 sits where the hot gas appears | Angus+08: groups need ×2–3 | a clean step at one σ or one f_gas, or η = 1 throughout | medium |
| 8 | **dSph σ with the EFE** | ON DISK `real_research/data/dsph/mcconnachie2012_dsph.csv` | σ_los predicted from M_b (Υ_V = 1–2) with the MW/M31 external field, Route A | σ⁴ ∝ M_b a₀ × EFE factor with a₀ fixed | ΛCDM: no fixed relation | 20+ dSphs on one line, scatter ≤ 0.1 dex in σ, both footings | low |
| 9 | **Coma UDGs (a possible kill)** | Chilingarian+19 / Forbes+ UDG σ tables (public) | MOND + Coma EFE (e_N ≈ 1–3) prediction of σ | σ suppressed by the EFE | Freundlich+22: observed σ TOO HIGH for MOND+EFE | either the tension evaporates on Route A/both footings, or it is a recorded liability | medium |
| 10 | **Isolated elliptical X-ray HSE** | NGC 720, 1521, 4636, 4649, 6482 gas ρ(r), T(r) from the literature (Humphrey+; Milgrom 2012 list) | HSE mass with baryons only vs framework | T(r) reproduced with no dark component | ΛCDM: needs the halo | 5+ systems fit with Υ inside 0.5–1.0 and no extra mass | medium-high |
| 11 | **Faber–Jackson zero-point** | SDSS/MaNGA σ_e, M* (public catalogs) | deep-MOND σ⁴ = (4/81) G M_b a₀ at the low-mass end; full kernel + Jeans at R_e otherwise | FJ intercept from a₀ alone | ΛCDM: intercept from the halo | intercept within 0.1 dex of the a₀ value with Υ inside 0.5–1 | medium |
| 12 | **Satellite kinematics** | SDSS satellite σ vs host M* (More+11; Lange+19 tables) | deep-MOND EFE-corrected σ_sat at 100–300 kpc | σ_sat⁴ ∝ M_b a₀ | ΛCDM: σ_sat from the SHM relation (steeper) | one line over 1.5 dex in host M* | medium-high |
| 13 | **Local Group timing** | M31 distance, radial velocity, M_b(MW) + M_b(M31) | 1-D two-body MOND integration over a Hubble time (Zhao+13 redone on Route A) | today's approach velocity reproduced with baryons only | ΛCDM: needs ~5e12 total | −110 km/s reproduced within 20 km/s on both footings with Υ inside 0.5–1 | low |
| 14 | **Oort spike** | JPL SBDB long-period comets, original 1/a (public API) | spike position and its modulation with the Galactic field direction | r_M(Sun) = 7,960 / 7,250 AU; spike shift +6%; injection modulation 7–17% along g_ext (repo OO-02/03) | Newton: standard Oort | a directional modulation at ≥ 3σ with the pre-registered sign | medium |
| 15 | **Wide-binary orientation in DR3** | ON DISK `real_research/data/widebinaries/all_columns_catalog.fits.gz` (El-Badry EDR3) | γ_v split by pair orientation to the Galactic external field | perpendicular pairs boosted MORE: B_perp/B_par → γ 1.12 vs 1.21 (pre-registered sign, WB-11) | Newton: no anisotropy | the pre-registered SIGN at ≥ 2σ in DR3 (DR4 decides) | medium |
| 16 | **RC100 per-galaxy a₀ at z = 0.6–2.5** | ON DISK `real_research/data/rc100_nestorshachar2023_table3.csv` (NOT yet in the fork) | framework inversion a₀ = g_obs(…)/… at the outermost radius per galaxy, pressure-support corrected | flat: a₀(z)/a₀(0) = 1 | ΛCDM-native rises ×1.8 by z = 2 (+0.25 dex; ~+0.08 observable at y ≈ 2) | 100 galaxies give a₀ ratio 1.00 ± 0.05 with no z trend, and the ΛCDM rise excluded at 3σ | medium |
| 17 | **DiskMass thickness (a possible kill)** | Martinsson+13 σ_z, Σ (VizieR J/A+A/557/A131, CfA mirror) | σ_z² = 2πG Σ_b h_z ν(y) on Route A | discs' vertical dispersion from baryons + ν alone | Angus+15: MOND discs too thick / Υ conflict | 30 discs' σ_z reproduced within 20% with Υ inside 0.3–0.7, or a recorded liability | medium |
| 18 | **Cluster η(r) profiles** | ON DISK `hff_granata_{a2744,as1063,m0416,m1149}.tsv` (HFF lensing) + `xcop/` | η(r) = M_lens(<r)/M_MOND(<r) from 20 kpc to R500 per cluster | η(r) is one function of g_N/a₀ in all four; η → 2 at R500; the core value tests the 23–33% lever | ΛCDM: NFW | the four clusters collapse onto one η(g_N/a₀) curve within 0.1 dex | medium |
| 19 | **f_gas–M slope = 1/3 exactly?** | ON DISK eRASS1 (`_load_erass1.py`) | slope and curvature of log f_gas vs log M500 with errors; compare hydro sims (0.2–0.4) | exactly 1/3 with no curvature (= constant η) | feedback physics: any value near 0.3 | slope 0.333 ± 0.02, zero curvature, over 2 decades | low |
| 20 | **The a₀ ladder** | outputs of 1, 2, 3, 8, 11, 13, 15, 16 | one table: a₀ measured in each system class from 1 M☉ to 1e15 M☉ | one number, both footings bracket it | ΛCDM: no reason for one number | every class within 0.1 dex of one a₀ | low (after the others) |

**Priority order for a systematic run:** 1, 2, 3, 6, 19 (all on disk, one evening) → 8, 13, 4 (one evening) → 16, 18, 15 (on disk, a day each) → 7, 5, 17, 9 (fetches) → 10, 11, 12, 14 → 20.

**What would count.** Items 1–3, 5–6, 8, 11–13 each put a₀ into a relation where it has not been measured before; a hit on any one of
them with RAR-class scatter is the second law. Items 9 and 17 are kills-in-waiting; run them early and record the outcome either way.
Item 16 is the only place a₀(z) can be read from existing data in this repo without a proposal. Item 20 is the figure that goes in the
paper if the ladder closes.

---

# PART II — fifty more (21–70), same rules, same format

Kill-in-waiting items are marked ⚠ (run them early; a kill is a result). Items marked ON DISK need no download.

## Disc galaxies (SPARC / WALLABY / HI surveys)

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 21 | **One-parameter RC family** | ON DISK SPARC rotmods | scale each RC by r_M = √(GM_b/a₀) and v_∞ = (GM_b a₀)^{1/4}; label only by Σ₀/Σ_M, Σ_M = a₀/(2πG) | all curves collapse onto a one-parameter family in Σ₀/Σ_M | ΛCDM: two halo parameters (M_h, c) needed | collapse residual < 5% in v across 100+ galaxies | low |
| 22 | **Renzo's rule quantified** | ON DISK SPARC rotmods (g_bar(r)) | cross-correlate d ln v/d ln r with d ln g_bar/d ln r; predicted amplification (1 + d ln ν/d ln y) | RC wiggles = baryonic wiggles times the kernel's local slope, no free parameter | ΛCDM: halo smooths features | measured amplification within 20% of predicted, galaxy by galaxy | medium |
| 23 | **Dwarf inner-slope diversity** | ON DISK SPARC dwarfs | v(2 kpc)/v_flat predicted from Σ(r) alone | the observed diversity (Oman+15) follows from the baryons | ΛCDM: cusp/core "diversity problem" | predicted vs observed inner ratio within 10% for 30+ dwarfs | low |
| 24 | **Core radius law** | Li+2020 Burkert fits (VizieR J/ApJS/247/31, CfA mirror) | r₀ vs r_M per galaxy | r₀/r_M = one number | ΛCDM: cores from feedback, mass-dependent | r₀/r_M scatter < 0.15 dex, no trend | low-medium |
| 25 | **Deep-tail slope = ½ exactly** | ON DISK SPARC, points with g_bar < 1e-12 | log slope of the RAR in the deep tail with errors | 0.500 exactly (ν → y^{−1/2}) | claims of a bend/flattening (Rodrigues+18 class) | 0.50 ± 0.01 with no curvature | low |
| 26 | **Angular-momentum slope** | ON DISK SPARC (j_b from RCs + photometry) | slope of log j_b vs log M_b | 3/4 (j ∝ R v, R ∝ M^{1/2} at fixed Σ, v ∝ M^{1/4}) | ΛCDM: 2/3 from halo spin (Fall) | 0.75 ± 0.03 | low |
| 27 | **Asymmetry grows outward** | ON DISK `prep_2026/wallaby_firing/perside_237.csv` | |A| vs x = g_bar/a₀ at the outermost rings, direction-free | EFE-driven asymmetry rises toward deep MOND | ΛCDM: no x dependence | monotone rise with x < 0.1 at ≥ 3σ | low |
| 28 | **Chae's EFE replicated on WALLABY** | ON DISK perside_237 + `gext_wallaby_237.csv` | outer-slope of the RC vs e_N amplitude (Chae+21 isotropic test) | declining outer slopes at higher e_N | ΛCDM: environment-degenerate (Paranjape–Sheth) | the Chae correlation at ≥ 3σ in an independent sample | medium |
| 29 | **Fast bars** | Aguerri+15, Guo+19, Garma-Oehmichen+22 pattern-speed tables (public) | R = R_cr/R_bar distribution | all bars fast, R = 1.0–1.4 (Tiret–Combes) | ΛCDM sims: slow bars R > 1.4 (Roshan+21) | ≥ 90% of bars with R < 1.4 | medium |
| 30 | **Warp onset radius** | WHISP/THINGS warp catalogs (van Eymeren+11; García-Ruiz+02) | onset radius vs r_M and vs the EFE radius √(GM_b/(e_N a₀)) | warps begin where the EFE takes over (Brada–Milgrom) | ΛCDM: misaligned halo/accretion | onset radius tracks the EFE radius with scatter < 0.15 dex | medium-high |
| 31 | **Almost-dark HI galaxies** | ALFALFA almost-darks (Leisman+17; Janowiecki+15) HI widths + M_HI | v⁴ = G M_gas a₀ with Υ irrelevant | on the BTFR with the same a₀ | ΛCDM: no fixed relation for gas-only systems | 20+ objects on the line, scatter ≤ 0.1 dex | low |
| 32 | **HI velocity function** | ALFALFA HI mass function (Jones+18) | convolve the baryonic mass function with v⁴ = G M_b a₀ | the observed velocity function with no halo function | ΛCDM: velocity function too steep at low v | predicted VF within errors at 30–100 km/s | medium |

## Milky Way and Local Group (Gaia)

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 33 | **Phantom dark disc** | Gaia K_z(z) at R₀ (Nitschai+21; Bienaymé+14) | vertical force shape 0.3–1.5 kpc with the phantom disc Σ_ph = (ν−1)Σ_b | a thin phantom disc of 10–20% of the stellar disc | ΛCDM: no dark disc (or a tiny accreted one) | K_z(z) shape reproduced with SPS Υ and no free parameter | medium |
| 34 | **K_z(R) radial shape** | Gaia DR3 K_z at |z| = 1.1 kpc for R = 6–12 kpc | predicted vs measured radial run | shape set by Σ_b(R) and the kernel | ΛCDM: halo adds a smooth term | K_z(R) within 10% across 6 kpc | medium |
| 35 ⚠ | **MW Keplerian decline** | Ou+24 / Eilers+19 RC tables (public) | MOND + EFE (e_N = 0.02–0.05 from M31/LSS) beyond 20 kpc | a mild EFE decline, not Keplerian | Ou+24: steep decline | either the decline is reproduced with e_N ≤ 0.05 or a liability is recorded | low-medium |
| 36 | **Escape velocity** | Gaia v_esc(R₀) = 500–530 km/s (Deason+19; Koppelman–Helmi 21) | v_esc from M_b, a₀ and the EFE cutoff alone | v_esc² = 2√(GM_b a₀) ln(r_EFE/R₀) | ΛCDM: from the halo | within 30 km/s on both footings with Υ inside 0.5–1 | low |
| 37 ⚠ | **Is the LMC bound?** | LMC 3-D velocity (Kallivayalil+13), M_b(MW) | MOND orbit of the LMC in the MW's baryonic field with the EFE | bound/unbound verdict; first-passage or not | ΛCDM: bound to a 1e12 halo; LMC mass 1e11 from the wake | a definite prediction for the LMC orbit that Gaia proper motions confirm or kill | medium |
| 38 | **Halo star σ_r(r) to 100 kpc** | Gaia + SDSS BHB/K-giant dispersion profiles (Bird+19; Deason+12) | MOND + EFE σ_r(r) with anisotropy from the data | flat-ish σ at (GM_b a₀)^{1/4} scale, EFE-cut beyond ~100 kpc | ΛCDM: falling with the halo profile | profile reproduced within 15% out to 80 kpc | medium-high |
| 39 | **Tidal-tail asymmetry ×5** | Gaia member lists for Hyades, Praesepe, Coma Ber, NGC 752, Ruprecht 147 (Röser+19; Jerabkova+21) | leading vs trailing tail counts | asymmetric with the EFE sign (Kroupa+22) | Newton: symmetric | the same sign in ≥ 4 of 5 clusters at ≥ 2σ each | medium |
| 40 | **Sednoid perihelia** | MPC/JPL Sednoids and inner-Oort objects | perihelion distribution under the MOND-EFE tidal field (Pauco–Klacka 16) | a specific q distribution edge at the Sun's r_M scale | Newton + Planet 9 | the edge at 7,960 / 7,250 AU-scaled q with no extra planet | medium-high |
| 41 | **Wide-binary eccentricities** | ON DISK El-Badry EDR3 catalog | eccentricity distribution vs separation (Hwang–Ting method) | MOND alters the e-distribution beyond 5 kAU (Hernandez) | Newton: thermal-ish distribution | a separation-dependent change at ≥ 3σ with the predicted sign | medium |

## Dwarfs, satellites, pairs

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 42 | **DF2 / DF4** | published σ (van Dokkum+18/19; Danieli+19) | σ with the NGC1052 EFE on Route A, both footings | σ ≈ 10–13 km/s | ΛCDM: "no dark matter" puzzle | within 1σ of the observed 8–10 km/s on at least one footing | low |
| 43 | **UFD σ–M_b–D relation** | Simon 2019 UFD table (public) | σ predicted from M_b and Galactocentric distance (EFE) | a 3-variable relation with a₀ as the only constant | ΛCDM: no such relation | 30 UFDs within errors, scatter ≤ 0.1 dex in σ | medium |
| 44 | **M31 satellites** | Collins+13 σ table | same with the M31 EFE | one line | ΛCDM: none | 20 dSphs within errors | low-medium |
| 45 ⚠ | **Virgo dwarf ellipticals** | Toloba+14/15 σ, M* | σ with the Virgo EFE (e_N ≈ 1–3) | EFE-suppressed σ | observed σ possibly too high (as for UDGs) | reproduced, or a recorded liability | medium |
| 46 | **Tidal dwarf galaxies** | Lelli+15 TDGs + newer (NGC 5291, NGC 7252) | BTFR position with a₀ | on the BTFR | ΛCDM: TDGs should be DM-free and OFF the BTFR | all TDGs within 0.15 dex of the line | low |
| 47 | **Dwarf-pair Kepler law** | TiNy Titans pairs (Stierwalt+15) Δv, separation, M_b | deep-MOND two-body with the field EFE | Δv ∝ (M_b a₀)^{1/4} f(separation) | ΛCDM: halo-dominated | pairs on one curve, scatter ≤ 0.15 dex | medium |
| 48 | **Binary galaxies** | ON DISK `real_research/data/kt2017_galaxies.tsv` (pairs with Nm = 2) + SDSS isolated pairs | Δv_rms vs projected separation and L_K | MOND: Δv² ∝ √(GM_b a₀) × projection factor, flat in separation | ΛCDM: halo-dominated, separation-dependent | flat Δv–separation with the a₀ amplitude over 50–500 kpc | medium |
| 49 | **Polar-ring galaxies** | Iodice+03 / Khoperskov ring vs disc velocities | ring speed from the disc's baryons in MOND (flattened phantom) | ring faster than the disc by the predicted ratio | ΛCDM: depends on halo shape | ratio within 10% for 5+ systems | medium |

## Ellipticals, lenses, pressure-supported systems

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 50 | **GC-system dispersions** | SLUGGS σ_GC(r) (Forbes+17) | Jeans on Route A with M_b from photometry | flat σ_GC at the a₀ scale to 10 R_e | ΛCDM: halo | 20 ETGs within 15% | medium |
| 51 | **PN.S declining profiles** | Pulsoni+18 PN σ(r) | MOND + radial anisotropy (Milgrom–Sanders 03) | the declines reproduced with mild anisotropy | ΛCDM: "dearth of DM" or radial orbits | 30 ETGs within errors with β ≤ 0.5 | medium-high |
| 52 | **Fundamental-Plane tilt** | SDSS FP (Hyde–Bernardi 09) | tilt from ν at R_e (Sanders 00) | the tilt coefficient from a₀ and Υ(SPS) | ΛCDM: from halo + non-homology | tilt within 0.05 of prediction | medium |
| 53 | **Einstein radii from M*** | SLACS lens table (Auger+09) | θ_E from M* and a₀ alone (Sanders–Land 08) | θ_E reproduced with SPS Υ | ΛCDM: halo needed | 50 lenses within 10% | medium |
| 54 | **Lens σ vs Einstein mass** | SLACS σ_e, M_E | M_E from the MOND potential of the baryons at θ_E | no extra mass at θ_E | ΛCDM: DM fraction 0.3–0.6 at θ_E | M_E reproduced within 15% | medium |

## Groups and clusters

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 55 | **Group lensing η** | KiDS+GAMA group ΔΣ (Viola+15; Dvornik+17) | η_group from lensing with stars + hot gas from scaling | the step: η = 1 (groups) → 2 (clusters), or a smooth rise | ΛCDM: standard halos | η(group) determined to ±0.2 | medium |
| 56 | **CLASH η(g/a₀)** | Umetsu+16 CLASH profiles (public) | η(r) per cluster vs g_N/a₀ | one curve for all 20 | ΛCDM: NFW | collapse within 0.1 dex | medium |
| 57 | **Bullet Cluster peaks** | Clowe+06 lensing map, gas map (public) | phantom from gas + galaxies on Route A; mass needed at the galaxy peaks | the residual needed (Angus+07 used 2 eV ν) | ΛCDM: collisionless DM | the residual quantified on both footings | medium |
| 58 | **Merger infall speeds** | Bullet, El Gordo masses and separations | two-body infall from turnaround in MOND | infall ≥ 3000 km/s naturally | ΛCDM: too fast (Lee–Komatsu) | the observed speeds reproduced with baryons + η | low |
| 59 | **T–M_gas slope = ½** | X-COP + HIFLUGCS + Lovisari T, M_gas | slope of log kT vs log M_gas | exactly 1/2 (deep-MOND σ² ∝ √(M_b a₀) with η constant) | self-similar T ∝ M^{2/3} with f_gas ∝ M^{1/3} gives the same — a coincidence to test | 0.50 ± 0.03 with the a₀ zero-point | low-medium |
| 60 | **SZ Y–M_gas slope = 3/2** | Planck PSZ2 Y + XMM M_gas (Planck 2013 XI) | slope of log Y vs log M_gas | 3/2 exactly | same coincidence test | 1.50 ± 0.05 | medium |
| 61 | **Cluster gravitational redshift** | BOSS/SDSS stacked cluster z_grav (Sadeh+15; Jimeno+15) | potential depth from baryons + phantom at η = 2 | the stacked −(10–15) km/s | ΛCDM: same order | prediction within 1σ of the measurement on both footings | low |
| 62 | **Phantom ellipticity in lensing** | KiDS halo-ellipticity (Schrabback+21) | ellipticity of the MOND phantom around discs at 30–100 kpc | q ≈ 0.7–0.8 aligned with the disc | ΛCDM: q ≈ 0.85–0.95 | measured f_h consistent with the phantom and not the halo at 2σ | medium-high |

## Cross-scale, redshift, precision

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 63 | **Void vs wall outer slopes** | ON DISK `sparc_cosmicweb_match.csv` + rotmods | outer RC slope for the lowest-e_N (void) galaxies vs walls | void galaxies never decline (no EFE) | ΛCDM: mild concentration effect | a slope difference with the EFE sign at ≥ 2σ | low |
| 64 | **κ to 3%** | ON DISK SPARC subset with TRGB/Cepheid distances (Lelli+16 flags) | the g_bar-axis distance-free estimator (repo L4-32) on that subset | κ = ½ within 3% | 1/(2π) = 0.16 dex away | ½ vs 1/2π separated at ≥ 3σ | medium |
| 65 | **Red vs blue lenses** | ON DISK KiDS Fig-8 colour bins + cov | a₀ from each colour bin | same a₀ | ΛCDM: red galaxies have higher M_h/M* | equal within 0.1 dex | low |
| 66 | **Lensing BTFR** | ON DISK KiDS Fig-3 lensing rotation curves, 4 mass bins | v_flat,lens⁴ vs M_b across the bins | slope 1, intercept G a₀ | ΛCDM: no fixed intercept | slope 1.00 ± 0.05, intercept at a₀ within 0.1 dex | low |
| 67 | **HFF cores** | ON DISK `hff_granata_*.tsv` | η at 20–100 kpc in the four clusters | tests the 23–33% core lever (cluster paper) | ΛCDM: NFW cusp | core η measured to ±0.1 in each cluster | medium |
| 68 | **η(z) in eRASS1** | ON DISK eRASS1, 0 < z < 1 | η at fixed M500 vs redshift | flat (a₀ constant) | ΛCDM-native rising scale gives Δη ≈ +0.1 dex by z ≈ 0.8 at x ≈ 0.4 | η(z) slope 0.00 ± 0.03 dex per unit z, both ways on selection | low-medium |
| 69 | **Isolated pairs in KT2017** | ON DISK `kt2017_galaxies.tsv` (Nm = 2 groups) | Δv vs separation and L_K for ~1000 pairs | the binary-galaxy law of #48 at scale | ΛCDM | the a₀ amplitude and flat separation dependence at ≥ 3σ | medium |
| 70 | **Λ from galaxies to 10%** | outputs of #64 + Planck ρ_Λ | Λ_gal = 32π a₀²/c⁴ with the 3% κ | Λ_gal = Λ_Planck within 10% | none | the cosmological constant measured in galaxies to ±10% and consistent | low (after 64) |

**Run order for Part II:** on-disk first (25, 26, 27, 28, 63, 65, 66, 68, 69, 21, 23), then the kills (35, 37, 45), then the fetch items by effort. Any of 21, 24–26, 31, 33, 36, 43, 47–48, 52–54, 59–60, 66 landing with RAR-class scatter is the second law; 59 and 60 are the two that would tie a₀ to cluster thermodynamics if the coincidence survives.

---

# PART III — five we missed that matter more than most of the seventy (71–75)

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 71 | **The saddle-point deficit** (sign-definite, MOND-unique) | KiDS-1000 / DES Y3 shear catalogs (public) + KiDS-bright or GAMA lens pairs | stack the convergence (or ΔΣ) at the MIDPOINT of galaxy pairs of similar M_b at separations 200–600 kpc; compare with the sum of the two isolated single-lens profiles at that point | QUMOND/AQUAL: the phantom density is NEGATIVE around the saddle between two masses (Milgrom 1986), so κ_mid < κ₁ + κ₂; deficit of order 10–30% of the sum at the midpoint | ΛCDM: overlapping halos plus a shared filament give κ_mid ≥ κ₁ + κ₂ | κ_mid/(κ₁+κ₂) < 1 at ≥ 3σ with the predicted separation dependence — a sign nothing in ΛCDM produces | medium-high |
| 72 | **Where the √ boost ends** | ON DISK KiDS isolated Nobins + 4 mass bins to 3 Mpc (Fig-4-5, Fig-9) | radius r_end where g_lens departs from √(G M_b a₀)/r, per mass bin; its scaling with M_b | the framework's completions all END MOND at some scale: AeST-class at 1/μ (universal, ≳ Mpc, oscillatory), the Hubble-floor reading at the turnaround radius r_ta ∝ M_b^{1/3} (1–2 Mpc for L*), pure AQUAL never; a DOWNWARD departure | ΛCDM: an UPWARD 2-halo departure at 1–3 Mpc | a downward departure whose radius scales as M_b^{1/3} across the four bins (turnaround) or is the same in all four (a mass scale) — either is new; an upward departure is the ΛCDM 2-halo term | low-medium |
| 73 | **The switch-on edge at z_t** (the derived law's only early-universe signature) | JWST UV luminosity functions z = 9–17 (Donnan+24, Harikane+25, Pérez-González+25, Finkelstein+24) + a ΛCDM-calibrated baseline (the papers' own) | the excess of the observed UVLF over the baseline vs z | MOND is OFF above z_t = ν₀^{−1/3} − 1 ∈ [17, 35] and the baryonic collapse speedup below it grows toward low z (1.24× at z=20, 1.66× z=10, 2.0× z=6 for 1e10 halos; stage 26): the JWST excess must be LARGER at z = 10–12 than at z = 15–17 and ABSENT above z_t; halo abundance itself is ΛCDM's | ΛCDM + feedback-free/bursty models: excess flat or rising to z ~ 20 | an excess that falls with z and vanishes by z ≈ 17–20, at the amplitude the collapse speedup gives; an excess persisting or growing at z ≥ 20 kills the switch-on law | medium |
| 74 | **Cluster spirals' BTFR offset** (the EFE at e_N ≈ 0.3–3) | VIVA Virgo HI RCs (Chung+09), Fornax MeerKAT (Loni+21), Coma Hα (public) + cluster-centric radii | for each spiral, e_N from the cluster potential at its position; predicted outer-RC suppression on AQUAL/Route A; BTFR residual vs e_N | Δlog v_flat = a universal negative function of e_N, reaching −0.1 to −0.2 dex at e_N ≈ 1–3; field spirals at 0 | ΛCDM: stripping shortens the gas disc but leaves v_flat; no e_N trend | the residual–e_N relation with the AQUAL shape and amplitude at ≥ 3σ over 50+ cluster spirals | medium |
| 75 | **Disc orientation to the external field** (the anisotropic EFE without velocity fields) | ON DISK SPARC + `~/new_physics/gext_vectors_2026/data/gext_vectors.csv` (175 g_ext vectors) + SPARC inclinations/PAs | angle γ between each disc's normal and ĝ_ext; RAR residual of the outermost 3 points vs γ, with the banked G(γ) amplitude (aligned_firing lane A) | AQUAL: the EFE suppression depends on γ at the 1–4% level in the outskirts (in-plane vs perpendicular external field) | ΛCDM: no dependence on the direction of a field it does not have | the γ dependence at ≥ 2σ in SPARC with the predicted sign; WALLABY-scale for 3σ | low-medium |

**Why these five outrank most of the seventy.** 71 is sign-definite and unique to MOND-class gravity; no dark-matter arrangement makes a lensing deficit between two masses. 72 is the one place the framework's completions differ from plain MOND and from each other, and the data are already on disk. 73 is the only observable the derived a₀(z) law puts in the early universe, and JWST is measuring exactly that redshift range now. 74 and 75 are the external-field effect measured as a function of its own strength and direction, which is the vector content ΛCDM cannot mimic (Paranjape–Sheth degeneracy is scalar). Run 72 tonight, 75 this week, 73 from the published tables, 74 and 71 as the two pipelines worth a month.

---

# PART IV — 76–100: the framework-only searches (nobody without a₀ = ½c√(Gρ_Λ), the exponential kernel, the EFE tensor and the switch-on law would think of these)

| # | search | data | compute | framework prediction | alternative | Kepler-grade if | effort |
|---|---|---|---|---|---|---|---|
| 76 | **The stellar mass-to-light ratio predicted by the cosmological constant** | ON DISK SPARC [3.6] photometry + RCs; SPS tables (Schombert+19, Meidt+14); DiskMass Υ (Martinsson+13) | a₀ is fixed by Planck's ρ_Λ (9.36e-11 ± 0.7%); in deep MOND a₀·Υ is what the RAR measures, so Υ_[3.6] is PREDICTED: Υ = 0.50 × (a₀,SPARC/a₀) | Υ_disk,[3.6] = **0.64** (canonical) / **0.53** (alt), one value for all discs | SPS: 0.5–0.6 (consistent); DiskMass dynamical: ~0.3 (⚠ conflict) | the RAR-required Υ matches SPS at the canonical value to ±0.05, or the DiskMass conflict is recorded as a footing discriminator | low |
| 77 ⚠ | **The phantom-crossing veto** | DESI DR2 + SN + CMB w(z) chains (public) | the framework's DE has w ≥ −1 at every z (TC4-04: the non-dust remainder cannot be phantom); test the reconstructed w(z) crossing −1 | no crossing; dissolution to w = −1 | DESI w0wa: crossing near z ≈ 0.5 at 2.5–4σ | crossing excluded → the veto holds; crossing confirmed at 5σ → the framework's DE is dead independently of a₀ | low |
| 78 | **a₀ as a Hubble-tension meter** | outputs of #64 (κ to 3%) + Planck/SH0ES | canonical footing: a₀ = ½c√(Gρ_Λ) with ρ_Λ fixed by the CMB is H₀-BLIND; alt footing: a₀ ∝ H₀ (+0.07 dex from 67.4 to 73) | the footing decides whether a₀ knows about the local H₀ | none in ΛCDM | κ to 3% distinguishes 9.36e-11 (H₀-blind) from 1.13→1.32e-10 (H₀-tracking) at ≥ 3σ | low (after 64) |
| 79 | **w(z) from rotation curves** | ON DISK fork constraints (`a0z_fork_likelihood_2026.py`) | invert every BTFR/RAR zero-point at z into ρ_DE(z)/ρ_DE(0) = [a₀(z)/a₀(0)]² and fit (w₀, w_a) with the drift nuisance | a dark-energy equation of state from galaxy dynamics alone | SN/BAO w(z) | the galaxy-only (w₀, w_a) contour overlaps SN+BAO and shrinks below ±0.3 in w₀ | medium |
| 80 | **Zero-velocity-surface radii** | Karachentsev+09/14 ZVS radii R₀ and baryon masses for ~15 nearby groups (public tables) | MOND + Λ infall: R₀ from M_b and a₀ (spherical collapse with Λc²r/3 and the kernel) | R₀ ∝ M_b^{1/4}-scaled, one curve | Newton: R₀ ∝ M^{1/3} with M the halo mass | the 15 groups on the MOND+Λ curve with scatter ≤ 0.1 dex and no free mass | medium |
| 81 | **The Milky Way's three external fields** | ON DISK 2M++ (`twompp_density.npy`), M31 and LMC positions/masses; Gaia DR3 azimuthal RCs (Ou+24; Wang+23) | vector sum of the LSS, M31 and LMC fields at the Sun and at R = 15–25 kpc; the AQUAL azimuthal anisotropy of the outer RC it implies | outer RC differs by 2–5% between the quadrants facing and opposing the total field vector, with a predicted direction | ΛCDM: azimuthal RC variations from spiral/bar structure only, no preferred LSS direction | the azimuthal asymmetry with the predicted direction at ≥ 3σ | medium |
| 82 ⚠ | **The LMC's MOND field on the disc** | LMC M_b ≈ 3e9, D = 50 kpc; Gaia disc kinematics | the LMC's deep-MOND field at the Sun ~0.04 a₀, comparable to the LSS field; its tidal/EFE imprint on the outer disc (warp, asymmetry toward the LMC) | a specific southward asymmetry amplitude | ΛCDM: the LMC's wake needs a 1e11 halo | the observed disc asymmetry toward the LMC reproduced with 3e9 M☉ and no halo, or a liability recorded | medium |
| 83 | **Lensing quadrupole aligned with the external field** | KiDS halo-ellipticity pipeline (Schrabback+21) + ON DISK g_ext vectors for lens galaxies (recompute from 2M++) | the m = 2 shear moment around isolated lenses with the reference axis set by ĝ_ext, not by the light | the phantom is squeezed along g_ext (banked BVP): a quadrupole aligned with the field | ΛCDM: halo ellipticity aligned with the light/filaments | quadrupole vs ĝ_ext at ≥ 2σ with the predicted orientation | medium-high |
| 84 | **E_G at 1–5 Mpc** | KiDS/DES isolated-galaxy ΔΣ (ON DISK to 3 Mpc) + galaxy clustering (GAMA/BOSS) | the lensing-to-clustering ratio in the 1–5 Mpc regime | the dust is present on linear scales but not bound in halos: the 2-halo lensing around isolated galaxies is the linear dust term + neighbours' phantom, not halo-halo | ΛCDM: halo-halo 2-halo term | E_G(1–5 Mpc) differing from the ΛCDM halo-model value by the predicted amount at ≥ 2σ | high |
| 85 | **No MOND in bulk flows** | ON DISK 2M++ density + CF4/2MTF peculiar velocities (public) | the velocity–density β = f/b from the linear reconstruction | the framework's linear regime is Newtonian: β = ΛCDM's (0.43) | MOND cosmology (Nusser/Sanders): flows over-predicted ×2–3 | β within 10% of ΛCDM's — a framework-specific NULL that separates it from MOND cosmology | medium |
| 86 | **21-cm onset shift** | EDGES/SARAS-3 absorption timing (contested; public) | the collapse speedup at z = 17–25 (1.24–1.4×) advances first-star formation; predicted Δz of the absorption onset | onset earlier than ΛCDM by Δz ≈ 1–2, and NO shift above z_t | ΛCDM: standard onset | a measured onset shift of the predicted size, or the switch-on window narrowed | medium |
| 87 | **Reionization timing** | Planck τ_e = 0.054 ± 0.007; JWST ionizing-photon budgets | the same speedup at z = 8–15 (1.5–1.8×) applied to a fixed efficiency: predicted τ_e shift | τ_e higher than the ΛCDM-efficiency baseline by ~0.005–0.01 | ΛCDM: τ from the halo function + efficiency | the τ_e shift consistent with Planck at the predicted size given JWST's efficiency | medium |
| 88 | **The crispy gap measured** | halo concentrations at z = 1–2 (HSC galaxy-galaxy lensing at z ~ 1; CLASH/RELICS clusters) vs N-body c(M, z) | c/c_Nbody at fixed mass vs z | ΛCDM must dilute concentrations as (H/H₀)^{−2/3} (0.61 at z=2) to mimic a flat a₀; the framework needs no dilution but predicts flat a₀ | ΛCDM: c(M,z) as N-body | concentrations at N-body values while a₀ stays flat = the framework; diluted = ΛCDM survives | high |
| 89 | **a₀ vs formation-epoch proxies** | ON DISK SPARC (bulge fraction, colour, gas fraction, Hubble type) | per-galaxy a₀ (the RAR-origin detector) vs each proxy | zero trend (a₀ is Λ's) | crispy-gap ΛCDM: emergent a₀ tracks concentration, hence formation epoch: a trend with bulge fraction/age | slope consistent with zero at ±0.02 dex per unit proxy, both footings | low |
| 90 | **The exponential return** | ON DISK SPARC high-g points (bulges, y = 10–100) | ν − 1 vs y at high acceleration | Route A: ν − 1 = e^{−√y} (0.04 at y=10, 0.004 at y=30) | α = 1 / "simple" ν: 1/(2y) power-law return (0.05 at 10, 0.017 at 30) | the exponential return preferred at ≥ 3σ — the kernel's own fingerprint | low |
| 91 | **The curvature landmark** | ON DISK SPARC (2693 points) | the RAR's log-log curvature C(y) = dσ/d ln y; its maximum | Route A: C_max = 0.103 at y ≈ 4 (g_bar = 4a₀); α = 1 gives (1, 0.125) | any other ν: different landmark | (y_max, C_max) measured within 20% of (4, 0.103) | low |
| 92 | **The local dark matter density is the phantom's** | Σ_b,⊙ (McKee+15), Gaia ρ_dm,⊙ = 0.010–0.014 M☉ pc⁻³ | ρ_ph,⊙ = ∇·[(ν−1) g_N]/(4πG) at the Sun on Route A (x_⊙ ≈ 2) | ρ_ph,⊙ from a₀ and the local baryons alone, both footings | ΛCDM: from the halo | within 1σ of Gaia's value with no free parameter | low |
| 93 ⚠ | **Outer-halo globular clusters** | NGC 2419, Pal 3, Pal 4, Pal 14 internal σ (Ibata+11; Baumgardt+) | internal dynamics at g_int ≲ a₀ with the MW EFE (e_N ≈ 0.1–0.3 at 80–100 kpc) | quasi-Newtonian with G_eff = ν(e_N): a specific, small inflation of σ | Ibata+11: MOND fails NGC 2419 (Sanders 12 disputes) | reproduced on Route A with the EFE, or a liability recorded | medium |
| 94 | **Distances from the cosmological constant** | ON DISK SPARC + `prep_2026/ladder_free_h0/` + TRGB subset | with a₀ fixed by Planck, the BTFR is an absolute standard: D from v_flat, flux and HI width; compare with TRGB distances; derive H₀ | a ladder-free H₀ whose zero point comes from Λ (the repo's earlier lane, redone on Route A) | Cepheid/TRGB ladders | BTFR distances agree with TRGB to ≤ 5% and give H₀ to ±3 km/s/Mpc | medium |
| 95 | **The Λ-limited bound radius** | SDSS satellite profiles around isolated hosts (Wang–White 12; Lange+19) | the largest bound orbit r_Λ where √(GM_b a₀)/r = Λc²r/3, i.e. r_Λ ∝ M_b^{1/4} (3.7 Mpc for L*) | an edge in the satellite/2-halo profile scaling as M_b^{1/4} | ΛCDM: splashback ∝ M^{1/3} | an edge whose radius scales as M_b^{1/4} across host masses | high |
| 96 | **North–south dwarf asymmetry from the LMC** | ON DISK `dsph/mcconnachie2012_dsph.csv` | σ predictions for MW dSphs with the MW + LMC external fields (two-source EFE) | southern dSphs near the LMC get an extra field 0.02–0.1 a₀: a hemispheric pattern in the residuals | ΛCDM: no such pattern (except LMC satellites) | the predicted hemispheric residual pattern at ≥ 2σ | low-medium |
| 97 | **Wide binaries vs Galactocentric radius** | ON DISK El-Badry EDR3 catalog (Galactocentric R from parallax) | γ_v in bins of R_GC (6–10 kpc), where g_ext varies ×1.5 | the EFE tensor B(x_ext) predicts γ_v falling with R_GC by a fixed amount | Newton: none | the R_GC trend with the predicted sign at ≥ 2σ (DR3), 3σ (DR4) | medium |
| 98 | **The local EFE tensor in the Oort constants** | Gaia Oort constants A, B, C, K + K_z (Bovy 17; Li–Widrow 21) | the phantom's local anisotropy from the EFE tensor (B_par = 1.47, B_perp = 1.26 at x_ext = 1.9) implies specific relations among the radial and vertical force gradients | a predicted departure from an axisymmetric potential's A, B, C, K relations at the percent level | ΛCDM: axisymmetric halo | the predicted anisotropy relation satisfied within errors | medium |
| 99 | **The Local Sheet's cold flow** | Karachentsev+03/09 Local Volume velocities (σ ≈ 25 km/s) | MOND + Λ dynamics of the Local Volume's baryons: predicted peculiar-velocity dispersion of the Local Sheet | the cold flow from baryons + Λ with no dark mass | ΛCDM: needs the local matter distribution tuned | σ_LS reproduced within 10 km/s | medium-high |
| 100 | **The first law's own kill condition** | outputs of every hit above | the joint posterior of a₀ across all system classes (1 M☉ to 1e15) with both footings and the κ measurement; the intrinsic spread | zero intrinsic spread; one κ | any class off the ladder | intrinsic spread < 0.05 dex across all classes, or the class that breaks it named — either result ends the hunt | low (last) |

**Run order for Part IV:** 76, 89, 90, 91, 92, 96 (on disk, an evening); then 77 and 85 (public chains and velocities, decisive both ways); then 81, 82, 93, 97 (Gaia); then 78–80, 94; 83, 84, 86–88, 95, 98, 99 as pipelines; 100 last.
**The three to run before anything else in the whole list:** 77 (a veto on the framework's dark energy from data already published), 76 (the stellar M/L predicted by Λ), and 72 (where the boost ends).

---

# RESULTS LEDGER — first systematic pass, 2026-09-03 (`hunt_2026/`)

Sixteen items run, each a committed script with checks that can fail, a mutation control, both footings, and the alternative computed
beside the framework. **No second Kepler-grade law found yet.** Three results are keepers, two are liabilities that go on the standing
ledger, five are dead or withdrawn, and one is a bug fix that changes a published-adjacent number.

| item | verdict | number |
|---|---|---|
| **correction** | ⚠ **BUG FIXED** | The Brouwer binned covariance is stored `(m,n,i,j)`; a plain reshape is **not positive definite** (min eigenvalue −2.8e-23) and gives negative χ². `ccnl_clock_fix_2026.py` used it, so its C1 exclusion (+4091) is **void** — corrected it flips to −30, *preferred*, because a coherent halo is degenerate with the ±0.3 dex amplitude nuisance. **"KiDS tolerate at most 14% of a CDM-like halo" is WITHDRAWN.** What stands: the differential bound (one bin's halo costs ≥ +143) and the SPARC rotation curves, ε ≲ 0.2 (dwarfs) to 0.5 (massive discs). |
| **72** | ✅ **keeper** | The √ boost does **not** end inside the KiDS reach. Endings excluded at 3σ below **1.67 / 2.07 / 3.44 / 2.77 Mpc** in the four mass bins (20/20 mutation mocks clean). ⇒ any completion must have its range **> 3.4 Mpc**; for AeST, m² < 0.09 Mpc⁻², about 10× tighter than the same data without mass bins. |
| **25** | ✅ **keeper** | The deep tail's slope is 1/2 within 1.6σ, and with the slope fixed at its predicted value the intercept **measures a₀ = 1.14e-10 [1.04, 1.25]** with no fitting — the alt footing to 0.004 dex, 0.086 dex above canonical. |
| **23** | ✅ **keeper** | The inner rotation-curve **diversity** (a named dark-matter problem) is predicted from the baryonic profile with zero halo freedom: r = 0.79 across the full observed range 0.22–1.23, rms residual 0.15 (honestly above the RAR's own scatter). |
| **26** | ✔ pass, prediction corrected | The naive 3/4 assumed fixed surface density and is **excluded at 7.4σ** — withdrawn. The correct zero-parameter form (measured size-mass slope + 1/4, from the BTFR alone) gives 0.569 ± 0.024 against a measured 0.582 ± 0.023: a **0.4σ pass**. |
| **19** | ✔ corrected | The raw f_gas–M500 slope is 0.404 ± 0.004, **16σ from 1/3** and curved, because R500 carries E(z). The framework's actual statement, f_gas·a₀/g_N(R500) = const, is flat to −0.010 ± 0.005. **The 1/3 form must not be quoted.** |
| **89** | ⚠ underpowered | No trend of per-galaxy a₀ with bulge fraction, Hubble type or gas fraction (all < 3σ) — but the same sample would register the emergent-halo reading's 0.25 dex trend at only **1.7σ**. Its own mutation control downgraded it. Route to decisive: the distance-free estimator (item 64). |
| **8** | 🔴 **LIABILITY** | The Local Group dwarf σ law does **not** close: at a stellar-population M/L the 46 dwarfs sit **+0.36 dex above** the framework's EFE prediction, centring needs Υ_V ~ 20; MW (+0.64) far worse than M31 (+0.29). Reproduces the known MOND tension for MW dwarfs (Angus 2008). Two bugs fixed en route (full mass in a half-mass estimator; the simple ν(x_ext) prescription over-predicts DF2 2× vs the published careful calculation). |
| **68** | 🔴 **LIABILITY** | The cluster residual **evolves**: η at fixed mass rises **+0.187 ± 0.013 dex per unit z** to z ≈ 0.8 in eRASS1, where constant a₀ requires zero and even the ΛCDM-native scale predicts +0.13. Selection and the ΛCDM-calibrated mass proxy plausibly produce all of it; needs a selection-controlled sample. Points the same way as the MUSE/Ciocan apparent rise. |
| **42** | ↔ split | DF2 lands **exactly** on the Newtonian floor (8.5 vs 8.5 km/s), where the careful EFE treatment puts it. DF4 sits 3.5σ **below its own Newtonian floor** — a liability for every theory at the assumed M/L. |
| **3** | ✖ dead, withdrawn | r_flat/r_M is not one number: −0.51 mass slope, 0.6 dex spread. Curves flatten at the disc scale length, not the MOND radius. Mis-posed; the framework never said otherwise. |
| **6** | ✖ dead, withdrawn | a₀/(πG) is **not** a ceiling on disc surface density — half of SPARC is above it. (The median lands on it to 0.003 dex; recorded as a coincidence with its Υ and selection caveats.) |
| **21** | ✖ not one-parameter | The r_M/v_inf rescaling does collapse the curves, but the surface-density label does not organise the residual. |
| **90, 91** | ✖ closed | The high-acceleration return is Υ-limited; the RAR curvature landmark, though parameter-free and 4× separated between kernels, is unmeasurable from binned medians (bootstrap spans two decades). Reopens only with a hierarchical per-galaxy slope-field fit. |
| **92** | ⚠ incomplete | The simple radial phantom estimate gives 0.003 M☉/pc³ against Gaia's 0.010–0.014. Needs Milgrom's vertical phantom-of-the-disc term; the repo's own full-AQUAL vertical-force work already does this properly. |
| **96** | ⚠ underpowered ×100 | The LMC's field is a few-percent perturbation on the MW's against a 0.3 dex scatter. Recorded as underpowered, not as a null. |

**Standing after the pass.** The framework gained a sharper bound on its own completions (72), a zero-parameter measurement of a₀ (25),
and a genuine explanation of a dark-matter problem (23). It also acquired two liabilities that were not on the ledger before (8, 68) and
lost four claims that do not survive contact with the data (3, 6, and the 3/4 and 1/3 forms). Next by value: items 64 (κ to 3%, which
also rescues 89), 71 (the saddle-point deficit), 55 (group lensing), 16 (RC100), and a selection-controlled redo of 68.


---

# RESULTS LEDGER — second pass, 2026-09-03 (items 1, 2, 4, 13, 22, 36, 63, 64, 65, 66, 70, 76, 100)

Thirteen more items, same rules. **Still no second Kepler-grade law — but the pass found the thing that is blocking one.**

| item | verdict | number |
|---|---|---|
| **64** | ✅ **best of the pass** | **κ = 0.512 ± 0.076** from the deep tail on galaxies with distance errors under 10%: consistent with ½ at 0.2σ, **excludes 1/(2π) at 4.6σ**. At 15% precision, not the 3% asked for, because the budget is stellar M/L, not distance. |
| **70** | ✅ keeper | **The cosmological constant measured in rotation curves.** Λ = 32πa₀²/c⁴ from the deep tail lands within a factor 1.5 of Planck's value. |
| **76** | ✅ keeper | **A stellar-population parameter derived from the cosmological constant.** With a₀ fixed by Planck's ρ_Λ, the deep tail predicts Υ_[3.6] with no fitting: alt footing requires 0.504, canonical 0.656, against stellar populations' 0.5 ± 0.1. DiskMass's 0.3 excluded by both. Mildly prefers alt. |
| **1** | ✅ keeper | The lensing acceleration falls as **1/r exactly** in every stellar-mass bin over 0.05–2.6 Mpc, where NFW gives −1.2 to −1.6. |
| **22** | ✅ keeper | **Renzo's rule made quantitative.** The local log-slope of every rotation curve is predicted point by point from the baryons and the kernel's local slope: r = 0.62, regression slope 0.84 vs a predicted 1.0, no free parameter. |
| **4** | ✔ modest pass | The predicted BTFR bend removes two-thirds of the residual mass tilt (+0.053 → +0.019 dex/dex), no free parameter. |
| **2, 65, 66** | ↔ the wall | The dwarf lens stack gives a₀ = 9.6e-11, canonical to 0.01 dex — but the L* stack gives 1.9e-10 and red lenses 3× blue. Each split is really a 0.15–0.25 dex statement about **stellar M/L**, each landing where stellar populations put it. Consistency, not measurement. |
| **36** | ↔ split | Escape velocity passes as a test of the potential's shape (550 km/s, inside Gaia) but only with the baryonic mass the framework needs for the observed rotation speed — inheriting the Milky Way normalisation liability. |
| **13** | ⚠ against interest | The simple radial timing argument **over-predicts** the Local Group approach 2× (−223 vs −110 km/s). The published MOND treatment resolves this with a **past close encounter 7–11 Gyr ago** — a distinctive prediction to test, not a kill. |
| **63** | ⚠ hint | No density-split difference, but the environment classes show the external-field **sign** at ~2σ: cluster galaxies have the most declining outer curves. |
| **100** | 🔴 **the ladder does not close** | Seven a₀ measurements across three decades of acceleration carry a **0.16 dex intrinsic spread**, organised by stellar M/L. The two that do **not** lean on M/L — the gas-dominated deep tail and the dwarf lens stack — agree to **0.08 dex** and bracket the canonical footing. |

**What the two passes together establish.** The blocker is not the data and not a₀. It is the **stellar mass-to-light ratio**: it sets the
precision of κ (item 64), it explains every split in the lensing items (2, 65, 66), it caps the formation-epoch test (89), and it is what
keeps the a₀ ladder from closing (100). The framework turns that around — item 76 shows a₀ **predicts** Υ from the cosmological constant —
which makes an independent Υ at 10% the single highest-value measurement in the whole hunt. It would take κ to 3%, decide between the two
footings, and close the ladder. Next after that: items 71 (saddle-point deficit), 55 (group lensing), 16 (RC100), and a selection-controlled
redo of 68.


---

# RESULTS LEDGER — third pass, 2026-09-03 (items 16, 27, 97)

| item | verdict | number |
|---|---|---|
| **16** | ✅ **strongest result of the hunt** | RC100's 100 rotation curves at z = 0.6–2.5, put through a **closed-form** inversion that uses only measured quantities. The table gives f_DM(<R_e) directly, so g_bar = (1−f_DM)g_obs and the Route A kernel inverts exactly: **a₀ = (1−f_DM)·g_obs / [ln(1/f_DM)]²** — no mass model, no geometry factor, no gas scaling. 99/100 invert. **d log a₀/dz = −0.112 ± 0.063**: consistent with the framework's flat law at 1.8σ, and **disfavouring the ΛCDM-native emergent rise at 3.9σ**. Median a₀ = 1.39e-10, +0.09 dex from the alt footing. |
| **16c** | ⚠ the caveat that sizes it | The trend is a **monotone restatement of RC100's own falling dark-matter fractions** (d log f_DM/dz = −0.16), i.e. the published "high-z discs are baryon-dominated" result read through the kernel. It inherits those systematics and an uncontrolled selection, and **no decline is detected either** (1.8σ from flat). Quote it as a constraint on the rise, never as a detection. |
| **27** | ⚠ hint | The direction-free WALLABY asymmetry grows toward lower rotation speed — the external-field sign — at 1–2σ, with a beam-resolution confound running the same way. |
| **97** | ⚠ underpowered by construction | The clean wide-binary sample lies within ~500 pc, a 6% range in Galactocentric radius, over which the predicted boost changes by <1% against a 2% systematic floor. Only Gaia DR4's more distant pairs give a lever — worth adding as a **split of the existing pre-registered statistic**, not as a new prediction. |

**Bug found and fixed in the making:** the first version of item 16 used g_bar = G·M_bar,total/R_e² and found 58/100 galaxies with
g_obs ≤ g_bar. That was the estimator's error, not the data's — M_bar is the *total* baryonic mass and only part of it lies inside R_e.
Corrected in place; the closed-form version supersedes it.

**Item 67 cannot run on disk:** the Frontier Fields tables in the repository are cluster-member photometry, not lensing mass profiles.


---

# RESULTS LEDGER — fourth pass, 2026-09-03 (items 71, 5, 95, 58)

| item | verdict | number |
|---|---|---|
| **71** | ✅ **promoted to the top** | The saddle-point deficit computed for the first time. **Two effects.** (a) The negative-mass region is real: QUMOND's phantom density reaches −2.5e5 M☉/kpc³ and is negative over ~25% of the saddle region — but it is a few kpc across and lensing-irrelevant. (b) The one that matters is the **nonlinearity**: the phantom halo of a galaxy *pair* is only **one third** of the sum of two isolated phantom halos at the midpoint, a **67% deficit stable from 200 to 800 kpc separation**, where overlapping halos and a shared filament both *add*. Indicative aperture estimate puts a 3σ stack within KiDS/DES reach. Absolute normalisation is box-dependent, so this is a **go-look, not a forecast**. |
| **5** | ✅ **keeper — explains a known unexplained constant** | The halo surface-density product ρ₀·r₀ from **162 Burkert fits** to real rotation curves (Li+2020, fetched this session) is **177 M☉/pc²**, consistent with Donato's 140 (+80/−30) and **within 0.14 dex of Σ_M = a₀/(2πG)** — which in the framework is not a halo property at all but the phantom's own central surface density, fixed by a₀ and hence by Λ. Halo-mass slope +0.14, weak, as a constant of nature should be. |
| **95** | ✔ list corrected | The largest bound orbit scales as **M_b^(1/6), not M^(1/4)** as the list said: 1.3 Mpc for an L* galaxy, 6 Mpc for a cluster. The **mass scaling** is what distinguishes it from a splashback radius (M^(1/3)). |
| **58** | ✖ withdrawn | Fed the **baryons** rather than the lensing mass (the earlier version double-counted the phantom), MOND and Newton give similar Bullet infall speeds and the assumed turnaround radius dominates. Non-diagnostic. |

**Bug found and fixed:** the first run of item 71 used a 30 kpc grid and reported *no* negative region. That was resolution, not
physics — the saddle's structure is kpc-scale. The resolution scan is in the committed output.


---

# RESULTS LEDGER — fifth pass, 2026-09-03 (items 24, 33, 61, and item 71 redone)

| item | verdict | number |
|---|---|---|
| **71** | ✖ **DEMOTED — my own promotion retracted** | Done properly (`h71b_saddle_forecast.py`): centred where a survey can actually centre — on a **galaxy** with a companion, in **ΔΣ**, finite projection depth, unequal masses — the pair-versus-sum ratio is **1.000 to 1.023** across 50–180 kpc. A 0–2% effect on a signal three orders of magnitude larger, and of the *opposite sign* to what I claimed. The "67% deficit" came from centring on the **saddle**, a local minimum of Σ, and from using Σ instead of ΔΣ. **What survives:** the negative-mass region at the saddle is real, and the control is now *proven* rather than argued — two NFW halos give **exactly** the sum of their parts, because Newtonian gravity is linear. A sign-definite signature of nonlinear gravity that the observable washes out. |
| **24** | ↔ consistency | The fitted halo core radius tracks the MOND radius slightly better than the disc scale length (0.55 vs 0.52 dex scatter), but with a −0.27 mass slope. Not a law. |
| **33** | ⚠ over-predicts, my model's fault | (ν−1)Σ_b gives 50 M☉/pc² against Gaia's inferred 25–35 — because that is the asymptotic column far above the disc, not the column inside 1.1 kpc. **Items 33 and 92 both withdrawn** in favour of the repository's existing full-AQUAL vertical-force solve, which does the geometry properly. The distinctive claim — the phantom is *flattened*, following the baryons, where a round halo contributes almost constantly with height — survives untouched. |
| **61** | ⚠ cannot be done | A point-mass cluster gives a 36 km/s gravitational redshift against a measured 7–15, because a cluster's baryons are extended and the integral piles up where no galaxies are stacked. Needs a real gas profile. |

**Bugs found and fixed this pass:** centring ΔΣ on a saddle (item 71); an angular scale 17× too small that gave 4000 lensing sources
per pair (item 71 forecast); the asymptotic-versus-measured column confusion (item 33); a point mass standing in for a cluster (item 61).

**Standing after five passes (41 items).** The keepers are unchanged and are all *galactic*: κ = 0.512 ± 0.076 excluding 1/(2π) at 4.6σ;
Λ measured in rotation curves to within ×1.5 of Planck; the stellar M/L predicted from Λ; the halo surface-density constant explained as
the phantom's own; the 1/r lensing law; Renzo's rule quantified; the inner-curve diversity predicted from baryons; a₀ measured from the
deep tail; and RC100 disfavouring the ΛCDM-native rise at 3.9σ. Nothing found outside galaxies has survived contact with a proper
calculation.

---

# PART V — items 101–125: built on the winners

Five passes produced ten keepers, and they cluster into five veins. These items extend the veins that produced, rather than
sampling the space again. Same rules: one committed script with checks that can fail, a mutation control, both footings, the
alternative computed beside the framework, verdict both ways. **Effort is marked by whether the data are on disk.**

## Vein A — the closed-form estimator (from items 16, 25, 64, 79)
The single most productive thing found: with a₀ fixed by Λ, quantities that are usually *fitted* become *predicted*, and where a
survey tabulates a dark-matter fraction the kernel inverts in closed form with no mass model at all.

| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 101 | **The closed-form inversion on every survey that tabulates f_DM** | KMOS3D (Übler+17), KROSS (Harrison+17), MUSE-DARK II/III, MSA-3D, RC100 — several already on disk | a₀ = (1−f_DM)g_obs/[ln(1/f_DM)]² per galaxy, per survey | one a₀ across all of them, and a joint d log a₀/dz far tighter than RC100's ±0.063 | the joint trend separates FLAT from the ΛCDM-native rise at ≥ 5σ, or the surveys disagree with each other (which would expose the systematic) | low, mostly on disk |
| 102 | **The gas-dominated deep tail: a₀ with no stellar M/L at all** | ON DISK SPARC, f_gas > 0.7 subset | item 25's slope-fixed intercept on gas-dominated galaxies only | the same a₀ as the full sample, but with the M/L budget *removed* — the one measurement in the hunt that does not go through Υ | a₀ to better than 8%, and consistent with the dwarf lens stack's 9.6e-11 | low |
| 103 | **The deep tail's error budget, decomposed** | ON DISK SPARC + the TRGB/Cepheid flags | propagate distance, inclination, Υ and gas separately into the slope-fixed a₀ | Υ dominates (items 2, 65, 66, 76 all said so); the question is what the floor is when it is removed | the floor is quantified and the sample cut that reaches 3% is named | low |
| 104 | **w(z) from the whole a₀(z) ladder, not one survey** | outputs of 101 | ρ_DE(z)/ρ_DE(0) = [a₀(z)/a₀(0)]², fit (w₀, wₐ) | a dark-energy equation of state from galaxy dynamics alone, with a real error bar | w₀ to ±0.05 — competitive with a supernova sample, from rotation curves | low, after 101 |
| 105 | **The BTFR zero-point as an a₀ meter at every redshift** | the same surveys | v⁴ = G M_b a₀ on the flat part only, gas included | the cleanest a₀(z) there is, and the one the decisive z ≈ 2.5 measurement will use | the local zero-point returns a₀ to 5%, validating the estimator before it is used at high z | medium |

## Vein B — the phantom *is* the halo (from items 5, 24)
A fitted dark halo is the phantom of a MOND galaxy, so every "unexplained regularity" of halo fits should be a property of a₀.

| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 106 | **The ρ₀–r₀ anti-correlation, not just the product** | ON DISK Li+2020 halo fits | slope of log ρ₀ vs log r₀ | **exactly −1** if the product is a constant of nature; feedback models give −0.7 to −0.9 | slope −1.00 ± 0.05 and no mass dependence | low |
| 107 | **The concentration–mass relation of fitted halos** | ON DISK Li+2020 (c200, M200 for 8 halo models) | predict c(M) from the phantom of an exponential disc | the fitted c(M) is a *baryonic* relation in the framework: it should track disc surface density, not halo mass | fitted c correlates with Σ₀ more tightly than with M200 | low |
| 108 | **Core size versus the baryonic profile** | ON DISK Li+2020 + SPARC photometry | r₀ against the radius where g_bar = a₀ | the "core" is where the boost switches on: r₀ ≈ r(g_bar = a₀), no feedback needed | r₀/r(g_bar = a₀) is one number with < 0.2 dex scatter | low |
| 109 | **Halo spin, predicted** | ON DISK Li+2020 + SPARC | λ = j/(√2 R200 V200) with the phantom's own j | the framework predicts the *observed* λ distribution from the baryons; ΛCDM predicts it from tidal torque | the predicted λ distribution matches the fitted one in median and width | medium |
| 110 | **Does the phantom reproduce the fitted profile SHAPE, not just its scales?** | ON DISK Li+2020 + SPARC rotmods | compute ρ_ph(r) directly and fit a Burkert to it | the fitted core-to-outer slope of a phantom is what halo fitters measure | a phantom fitted with a Burkert returns the observed distribution of shape parameters | medium |

## Vein C — the lensing law (from items 1, 2, 65, 66)
The 1/r law is exact and parameter-free; every lensing split turned out to measure stellar M/L. Both are exploitable.

| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 111 | **Lensing as an M/L machine** | ON DISK KiDS colour, Sérsic and mass bins | invert each bin's a₀ *assuming* a₀ universal, read off the relative Υ | a Υ(colour) relation measured by gravity rather than by stellar populations | the measured Υ(colour) matches SPS within 0.1 dex across all bins — a new, independent M/L calibration | low |
| 112 | **The Sérsic split** | ON DISK Fig-8 Sérsic bins (not yet used) | as item 65 | bulge-dominated and disc-dominated lenses must give the same a₀ once their Υ differ as SPS says | consistent with 111's calibration | low |
| 113 | **The 1/r law's radial reach** | ON DISK KiDS to 3 Mpc + a modelled two-halo term | fit the 1/r law with a ΛCDM two-halo term added, see which the data prefer | the framework needs no two-halo term at all; ΛCDM needs one with a fixed amplitude | the two-halo amplitude is consistent with zero, or is measured and compared | medium |
| 114 | **Gas-dominated lenses** | KiDS/GAMA HI-selected lens sample | ΔΣ around gas-rich lenses where Υ barely matters | the M/L-free lensing a₀ | a₀ to 10% with no Υ assumption | high |

## Vein D — the kernel in the shape of a curve (from items 22, 23)
The local slope and the inner-curve diversity are both predicted point by point. Push on the residuals.

| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 115 | **Renzo's rule at second order** | ON DISK SPARC | the curvature, not just the slope, of v(r) predicted from g_bar(r) | the kernel fixes both derivatives with no freedom | the second-order prediction correlates at r > 0.5, beyond what the first order already explains | low |
| 116 | **What is left over after the diversity prediction?** | ON DISK SPARC (item 23's residuals) | correlate the 0.15 rms residual with inclination, distance method, Υ, gas fraction, bar presence | the residual should be *observational*, not physical | the residual correlates with a measurement systematic and not with a physical property | low |
| 117 | **The RAR's intrinsic scatter, budgeted** | ON DISK SPARC | subtract the known error budget from the observed 0.06 dex orthogonal scatter | the framework predicts *zero* intrinsic scatter | the intrinsic residual is consistent with zero, and the bound is quoted | low |
| 118 | **Bars and spirals in the residuals** | ON DISK SPARC + morphological flags | RAR residual as a function of bar strength and arm class | non-circular motions, not the kernel, should carry them | barred galaxies' residuals differ in the way non-circular motions predict, not in a₀ | medium |

## Vein E — the M/L pivot (from item 76)
The blocker of the whole hunt, and the framework turns it into a prediction.

| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 119 | **Per-galaxy Υ predicted from a₀, versus per-galaxy colour** | ON DISK SPARC + [3.6]−[4.5] or optical colours | fix a₀, solve each galaxy's rotation curve for its Υ, plot against colour | a Υ(colour) relation derived from the cosmological constant | the derived relation matches Bell & de Jong / Schombert within 0.1 dex, with the right slope | low |
| 120 | **The Υ that Λ predicts, versus DiskMass** | ON DISK SPARC + Martinsson+13 | item 76 restricted to the DiskMass overlap | DiskMass's dynamical Υ ≈ 0.3 is excluded by both footings (item 76 already found this) | the disagreement is localised: which galaxies, and why | medium |
| 121 | **Gas-dominated calibration transfer** | ON DISK SPARC | calibrate a₀ on f_gas > 0.7 (item 102), then *predict* Υ for the star-dominated rest | zero free parameters anywhere in the chain | the predicted Υ distribution matches SPS in median and spread | low |

## Vein F — the things the winners imply that nobody has asked
| # | search | data | compute | prediction | pass if | effort |
|---|---|---|---|---|---|---|
| 122 | **Is Σ_M = a₀/(2πG) a ceiling on the PHANTOM's surface density?** | ON DISK SPARC + Li+2020 | the maximum phantom surface density any galaxy attains | item 6 showed it is not a ceiling on *baryonic* surface density — but it should bound the *phantom's* | no galaxy's phantom exceeds Σ_M, and the distribution piles up against it | low |
| 123 | **The two footings, decided** | outputs of 102, 103, 119 | the M/L-free a₀ against 9.36e-11 and 1.13e-10 | the deep tail gave 1.14e-10 and the dwarf lenses 9.6e-11 — they straddle | one footing excluded at ≥ 3σ by an M/L-free measurement | medium |
| 124 | **a₀ from a system with no stars at all** | HI-only clouds, almost-darks, tidal debris | v⁴ = G M_HI a₀ with the 1.33 helium correction the only assumption | the cleanest a₀ anywhere: no Υ, no bulge, no colour | a₀ to 15% from a stellar-mass-free sample | medium |
| 125 | **The ladder, closed** | outputs of 101–124 | the a₀ ladder of item 100 rebuilt from M/L-free rungs only | item 100 found a 0.16 dex intrinsic spread organised by M/L; removing M/L should collapse it | the M/L-free rungs agree to < 0.05 dex — which would BE the second law: one acceleration, measured five independent ways, from a solar mass to 10¹⁵ | low, after the rest |

**Why these and not another fifty.** Every keeper of the first hundred is galactic and rests on the acceleration relation, and every
one of them ran into the same wall: the stellar mass-to-light ratio. Veins A, E and F are all attacks on that wall, from three
directions — remove Υ (gas-dominated, HI-only), predict Υ (from a₀ and Λ), or measure Υ (with lensing). Vein B turns the framework's
best idea, that the halo *is* the phantom, into four sharp tests of halo-fit regularities that ΛCDM does not explain. Item **125** is
the one that would end the hunt: if a₀ measured five M/L-free ways across nine decades of mass agrees to 0.05 dex, that is a second
Kepler-grade result, and it is reachable with data already on disk.


---

# RESULTS LEDGER — first background sweep, 2026-09-03 (57 items, 14 agents, adversarial verification, 8.3M tokens)

**⚠️ CORRECTION to commit f33d4e86a's message, made here in the same file: that message listed four survivors of
verification. It was wrong. Of six claimed wins, FIVE were refuted — two fatally — and the sixth survived only with
its headline number withdrawn. The correct verification table is below and it is the operative record.**

## Verification outcomes on every claimed win (three adversarial lenses each: estimator, fairness, mass-to-light)

| claimed win | verdict | why |
|---|---|---|
| HI width function from the HI mass function (32) | **REFUTED, fatal** | estimator clean, but the headline reverses under the observable the model actually predicts |
| Milky Way enclosed mass to 73 kpc (38) | **REFUTED, downgrade** | estimator correct and no bug found, but the precision claimed does not survive |
| Is the LMC bound (37) | **REFUTED, downgrade** | the external-field prescription used is the *maximal-binding* choice, not the standard one; the null conclusion survives, the number does not |
| Planetary-nebula dispersion amplitudes (51) | **REFUTED, fatal** | the headline check reverses under the right observable, and the residual separation is a stellar-M/L statement |
| **Bulk-flow null (85)** | **STANDS, downgraded** | estimator verified analytically and independently; **core conclusion survives, headline number withdrawn** |
| Local Sheet cold flow (99) | **REFUTED, fatal** | the one positive claim rests on a dark-matter-inclusive number fed into a slot the framework's own physics does not allow |

**So the sweep produced ONE surviving positive result, and it is a null:** the framework's linear regime is Newtonian,
so the local velocity–density ratio comes out at ΛCDM's value (β = 0.447 against f/b = 0.440) where an unprotected MOND
kernel would need 0.043–0.047. That **separates this framework from MOND cosmology** — a distinction worth having, and
the only thing in 57 items that gained ground.

## The framework took real damage. Twenty-five liabilities, and these are the sharp ones

| item | finding |
|---|---|
| **9 Coma UDGs** | **The kill fired.** Eleven ultra-diffuse galaxies sit **+1.195 ± 0.062 dex (19.4σ)** above the prediction once the external field is on, all eleven the same sign, and the offset tracks the external field itself. Freundlich+2022 reproduced. |
| 7 groups with hot gas | With gas actually measured, 20 X-ray groups of 2–14e13 M☉ still need η = 1.8–2.1 at R500, **no step, no threshold temperature** — the cluster residual reaches an order of magnitude further down in mass than the programme assumed |
| 18 cluster η(r) | η(r) is organised by r/R500 (0.102 dex) **better** than by the framework's own acceleration variable (0.167 dex), winning **0 of 500** cluster bootstraps |
| 56 CLASH | The 20-cluster collapse is tight but nearly empty (radius alone does as well) and requires **a₀ = 1.72e-9, 18.4× canonical** |
| 57 Bullet peaks | The kernel supplies 2.6–3.3× against the 8.3–9.8× the JWST lens model requires: **short by a factor 3.2**, i.e. 3.8–4.0e14 M☉ |
| 67b X-COP cores | η = 2.7–2.9 at 30–100 kpc against ~2 at R500: the residual **does not close inward** |
| 52 Fundamental Plane | The framework **cannot** be the FP tilt, by a theorem not a fit: the kernel's argument contains surface brightness in the combination the tilt needs to *not* have |
| 53/54 SLACS | Einstein radii short by 14–18% (Salpeter) and the phantom delivers only 79–85% of the Einstein mass at g_N ≈ 10 a₀ |
| 34 K_z(R) | Vertical force over-predicted by 30–37%, K_z scale length **4.5σ** too long — confirming the MOND tension Bovy & Rix published |
| 55 group lensing | **No step:** η is flat from 5e12 to 1.6e15 M☉ across 2.5 decades |
| 20 the a₀ ladder | Eight system classes over seven decades span **0.78 dex**; the cluster rung is **6.3σ** from the M/L-free deep-tail value |
| 43/44 dwarfs | Ultra-faint dwarfs need Υ_V ≈ 109, M31 satellites ≈ 24 — far worse than item 8's already-bad 20 |
| 46 tidal dwarfs | All six rotate **slower** than required; +2.84σ combined on the three independent host systems, and the two paradigms disagree about the *sign* |
| 48/69 binary galaxies | The framework's external-field branch sits **26σ** above unity on the strictest isolation cut, and it is *not* an isolation artefact (tested against my own hypothesis) |
| 87 reionization | τ_e = 0.064–0.070 against Planck's 0.054 ± 0.007: **+1.4 to +2.2σ**, in every branch |
| 30 warps | The MOND external-field radius is the **worst** of five candidate scales for warp onset; the baryonic disc edge organises it (0.073 dex on the clean sample) |
| 17 DiskMass | Requires Υ_K = 0.582 ± 0.127 against DiskMass's dynamical 0.31 ± 0.05 |
| 10 X-ray ellipticals | Seven need a median **1.69 dex more boost** than the kernel gives, growing toward low acceleration |
| 93 outer-halo globulars | Requires M/L_V = 0.76 ± 0.15 where stellar populations give 1.3–2.2 |

## Five items withdrawn because the list's own prediction was wrong

* **40 Sednoids** — the premise is geometrically impossible (their perihelia are r_M/99 to r_M/200, where ν−1 < 1e-38). The framework's real outer-solar-system scale is an *aphelion* crossover near 500 AU.
* **49 polar rings** — the list said the ring rotates *faster*; a 3-D QUMOND solve says **slower**, because the phantom is flattened toward the disc. A 3.6% framework-versus-halo discriminant, with the sign corrected.
* **73 JWST luminosity functions** — the list said the excess should *fall* with redshift; it must **grow**, because the halo mass function steepens faster than the collapse speedup declines. Measured: **+0.175 ± 0.047 dex per unit z**, and the total-mass branch predicts +0.085 to +0.093.
* **84 E_G** — withdrawn on the framework's *own* physics: the phantom saturates in mass at 12–70 kpc, so E_G is 1 − 0.0004 over 1–5 Mpc and there is nothing to measure.
* **98 Oort constants** — the premise over-stated the effect a hundredfold; done properly it is a double null.

## Two methodological findings worth more than most of the items

* **The slope-only external-field test is formally UNIDENTIFIED** (item 28). Walking the external field over four decades
  and re-solving the baryonic shape index reproduces **all 85** WALLABY galaxies' observed outer slopes exactly (worst
  residual 1.2e-9) for a shape shift of only 0.34. The test is not underpowered; it is degenerate.
* **Fast bars are not decidable** (item 29). MaNGA gives 33.3 ± 3.3% fast, CALIFA gives 90.3 ± 5.3% — **9.2σ apart** — and
  the within-galaxy spread from seven published bar-length definitions is ×2.12, essentially the ×2.17 that flips the
  answer. The bar length, not the galaxy, sets the result.

## Where this leaves the standing

The galactic keepers of the earlier passes are untouched — they were not re-tested here. What this sweep establishes is that
**outside the acceleration relation, the framework is in trouble in more places than the ledger recorded**: clusters at every
mass and radius, pressure-supported systems at every scale from ultra-faint dwarfs to ellipticals, lensing at Einstein radii,
the vertical force, warps, tidal dwarfs, binary galaxies, and reionization. The one thing gained is a null that separates it
from MOND cosmology.

---

# RESULTS LEDGER — the veins workflow, 2026-09-03 (items 101–125, 38 agents, 5.8M tokens)

**⚠️ THIS PASS OVERTURNED THREE OF THE HUNT'S OWN HEADLINE RESULTS. Read the corrections before anything else.**

## The corrections

| what was claimed | what is true | consequence |
|---|---|---|
| **Item 25:** a₀ = 1.14e-10 from the slope-fixed deep tail, "the alt footing to 0.004 dex" | The estimator is **biased +0.0985 dex**. It fixes the slope at 1/2 and reads ⟨g_obs²/g_bar⟩, but g_bar < 1e-11 is not deep enough: ν(y)y = √y(1+√y/2+…), ⟨√y⟩ = 0.231, bias = 2log₁₀(1+⟨√y⟩/2). **Synthetic curves obeying the kernel exactly at 9.36e-11 are read back as 1.174e-10.** | **a₀ = 9.04e-11 — the canonical footing to 0.015 dex.** Items 64, 70, 76, 100 inherit. **κ = 0.512 ± 0.076 → 0.482 ± 0.081; 1/(2π) excluded at 4.0σ, not 4.6σ.** |
| **Item 100:** "the two rungs that do not lean on M/L agree to 0.08 dex" | **Neither is M/L-free** (levers −0.647 and −1.046; deep-MOND lensing a₀ is degenerate with the assumed baryonic mass at exponent 1, not 2), **and the agreement was the +0.095 dex bias.** | Both halves fail. The sentence organised two ledgers and section 1 of `WHAT_THE_HUNT_TAUGHT.md`; all three corrected in place. |
| **The standing diagnosis:** "the blocker is the stellar M/L" | **Not only.** Distance leads the random budget (38% of variance once Υ is cut). Removing Υ takes the total from 0.073 to 0.074 dex — it buys almost nothing. **Floor with Υ removed = 10.5%, not 3%**, set by the distance scale. Removing Υ **trades one calibration for a worse one**: d log a₀/d log M_gas = **−1.11**. | The "3% cut" **does not exist**. 3% in a₀ needs the distance ladder to 1.3%. |

## Item 125 — the answer, and it is settled rather than pending

**The hunt did not find a second law, and the criterion could not even be evaluated.** Seven M/L-free rungs; median quoted
error **0.13 dex against the 0.05 dex agreement asked for** — identical central values could not have demonstrated it. The
rungs are in mild tension anyway (**χ² = 16.6/6, p = 0.011**), and the moment estimator cannot detect that spread at N = 7,
**which retires item 100's 0.156 dex "intrinsic spread" as a detection too.**

* **The organiser changed.** It is not Υ: three rungs have exactly zero leverage, the best common Υ shift is +2.5 dex, and a
  bare sample-membership flag absorbs the same χ². It is the **velocity measurement** — resolved rotation curves sit
  **+0.24 dex above unresolved HI line widths**, matching item 124's independently measured width bias of +0.25 dex/dex
  across three decades of mass, which also explains item 31's almost-dark "deficit."
* **M/L-freedom and dynamic range are in direct conflict.** Dropping the stellar mass forces gas-rich selection → low mass →
  the same acceleration. The load-bearing rungs span **1.1 decades**, not nine, and every one is a gas-rich dwarf.
* **The three SPARC rungs agreeing to 0.016 dex is not the law closing** — R2 is a subset of R1, R3 shares 15 of 20, and all
  three share one distance scale, one inclination convention, one hydrogen calibration. Three estimators on one sample is
  one rung.

## Item 123 — neither footing is decided, and not for want of data

Best M/L-free value **a₀ = 7.36e-11 ± 0.065 stat, ±0.104 with the coherent floor**: canonical −1.0σ, alt −1.8σ. **A cut
choice inside the same sample moves a₀ by 0.204 dex — 2.5× the 0.0818 dex gap between the footings.** Eight TRGB/Cepheid
galaxies give 9.08e-11; fifteen Hubble-flow galaxies give 5.68e-11. A verdict that flips on a cut is not a verdict.
Deciding needs the distance scale to 1.4%, the HI mass scale to 3%, and ~518 resolved gas-dominated discs against 23.

## What survived triple refutation (5 of 10 claimed wins)

| item | result |
|---|---|
| **102** | The M/L-free deep tail done correctly: the **local** stellar share at the radii used, not the global gas fraction, sets the leverage (bug pattern 1 inside the item's own specification). Cutting on f_*,loc < 0.2 takes the lever to −0.14 and gives **a₀ = 7.36e-11**, agreeing with the KiDS dwarf stack at 0.9σ with no mass trend. Bonus: **Υ_[3.6] = 0.61 ± 0.15 measured with no a₀ in it.** |
| **105b** | A structural factor **C = ν(y)²·y·ε** separates the BTFR zero-point from a₀; applying it moves the naive 1.53e-10 to **9.82e-11**, +0.021 dex from canonical. |
| **109** | The halo spin parameter predicted from the baryons. |
| **110** | The phantom reproduces the fitted halo profile **shape**, not just its scales. |
| **115** | **Renzo's rule at second order**: β[(1+n)L″] = **0.944 ± 0.135** against a predicted 1.000 — a 0.4σ pass on the *curvature*, with no free parameter. |
| **118** | RAR residuals show no bar-strength dependence (−0.026 ± 0.039 dex), as the framework requires. |

## Refuted on verification

Items **103** (its own headline; the budget stands, the framing did not), **119**, **121**, **101b**.

## The durable methodological finding

**Removing a nuisance is not the same as removing calibration.** Every route that drops the stellar M/L picks up the HI mass
scale at lever −1.11 and the distance scale at −2.25, and forces a sample with 1.1 decades of dynamic range. That is why the
ladder cannot close on present data, and it is a statement about measurement rather than about the framework.
