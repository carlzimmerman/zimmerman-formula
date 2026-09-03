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
