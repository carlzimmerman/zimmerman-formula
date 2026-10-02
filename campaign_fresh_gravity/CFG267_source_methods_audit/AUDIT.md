# CFG267: methods audit of the source papers behind the high-z a₀ lanes

> **κ = ½ FITTED. a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. This is a reading of the published papers, not a re-analysis. No lane is re-run and no number in any lane changes. Nothing was downloaded: every paper was read from a local arXiv TeX source already on disk (`~/new_physics/_external_data/arxiv_src/<id>/`), from the RC100 text layer already on disk (`~/new_physics/_external_data/papers/rc100.txt`), or as a page read of the arXiv PDF turned into text and not saved. Quotes are under 15 words, are copied from the primary text and were checked against it. Anything I could not find in the primary text is marked UNVERIFIED. No sentence here says the data favour a law.**

**Programme constants used for comparison:**
- canonical footing a₀ = 9.3603e-11 m/s²; alt footing a₀ = 1.1312e-10 m/s²;
- kernels ν_mono (the chain's monotone repair of the McGaugh+16 RAR function) and P2, ν(y) = √(1 + 1/y);
- the literature default is a₀ = 1.2e-10 m/s².

**Arithmetic helper:** `a0_kernel_shift_arithmetic.py` (output `.out`, `_results.json`). It reads no data. It computes the ratio of the predicted g_obs at fixed g_bar between the programme's law and a literature law at a₀ = 1.2e-10, both in general and at each lane's own regime. Every "shift" number below comes from it and is **arithmetic, not a re-analysis**.

---

## 1. Bottom line

1. **Only three of the 22 audited papers make a quantitative MOND/RAR statement with an a₀ value. All three use the McGaugh+16 RAR (exponential) interpolating function.**
   - Brouwer+21 (KiDS lensing) fixes g† = 1.20e-10.
   - MUSE-DARK III fits a₀ = 2.38e-10 at z ≈ 0.3–1.4.
   - Vărăşteanu+26 (MIGHTEE-HI) fits a₀ = 1.50e-10 at z ≤ 0.09.
   - Lelli+21 (ALESS 073.1) mentions a₀ ≃ 1e-10 only to say the galaxy is Newtonian. Genzel+20 names MOND once and does not test it. The other 17 make no MOND or RAR comparison at all.
   - Nobody uses the "simple" or "standard" function in a headline result. Nobody includes the external field effect in a headline result.
2. **So, for most of our high-z lanes, there is no published "MOND works/fails" statement to inherit.** What the lanes inherit is the papers' recipes:
   - ΛCDM-halo decompositions (NFW plus priors), from which our D_obs = 1/(1 − f_DM) is built;
   - pressure prescriptions;
   - scaling-relation gas;
   - assumed geometry.
3. **Three recipe differences between the papers and our lanes matter most (Section 5):**
   - (i) the gas;
   - (ii) the pressure term;
   - (iii) the assumed baryon geometry and radius.
   Each one moves an implied a₀ by more than the canonical-versus-1.2e-10 difference. At the lanes' typical y ≈ 2, that difference is only 0.03 dex in g_obs. It reaches 0.05 dex only in the deep regime.
4. **Four findings bear on committed lanes (Section 6).** None of them re-runs a lane.
   - **F2:** CFG229's ALESS 122.1 pressure variants (α = 1.68 and 3.36) count the pressure term twice. The source's V_circ(2 r_e) already contains it.
   - **F4:** CFG271's "M_rot" sensitivity rows are not a kinematic reading. Parlanti+23 built HZ9's M_rot as M★ + M_gas.
   - **F3:** CFG274's α_CO = 0.92 and its eight-disc list are from arXiv v1 of Amvrosiadis+. The published version appears to differ (UNVERIFIED in character).
   - **F1, F9:** the source labels "Lelli+21 for ALESS 122.1" and "MUSE-DARK II for CFG198/199/236/262" are wrong. The lanes themselves used the right files.

---

## 2. Master table (one row per paper; details and quotes in Section 7)

Column key:
- (1) selection;
- (2) kinematics, and the radius at which V is quoted;
- (3) pressure term;
- (4) baryons: M★ method and IMF; gas; helium; geometry;
- (5) MOND/RAR statement;
- (6) where our lane departed;
- (7) shift under our a₀. This is arithmetic: the ratio of predicted g_obs, programme law over the McGaugh+16 RAR at 1.2e-10, at the lane's regime, given as ν_mono canonical / alt.

| # | Paper (arXiv) | Lanes | (1) Selection | (2) Kinematics; V radius | (3) Pressure | (4) Baryons | (5) MOND / RAR | (6) Our departure | (7) Shift (arithmetic) |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Nestor Shachar+23, RC100 (2209.12199) | CFG216/217/233 | v_rot/σ₀ > 2.3, log M★ > 9.5, −0.6 < δMS < 1; resolution and coverage cuts "less strict than G20"; z 0.6–2.5 | DYSMAL least squares plus two DysmalPy MCMC methods, beam forward-modelled; Table 3 averages the three methods; V_c(R_e) from the mass model | V_rot² = V_circ² − 3.36σ₀²(r/R_e) (eq. 8, Burkert+10); V_c in Table 3 is V_circ | SED (Wuyts+11), Chabrier; gas from **Tacconi+20 scaling** (molecular, includes He per Tacconi+20; HI not mentioned) as a Gaussian prior on M_bar; disc q₀ 0.2–0.25 plus bulge plus NFW (plain and contracted, averaged) | **none** (0 hits for MOND or Milgrom) | D_obs = 1/(1 − f_DM) and g_obs = V_c²/R_e taken as published, so their NFW, priors and 3.36σ₀² are inherited; variant (d) uses a thin disc; CFG217's M★ reconstruction used Tacconi+18, not +20; the CSV had 16 rows wrong (corrected copy) | no MOND claim to shift; at median y_can 1.96: 0.942 / 0.985 |
| 2 | Genzel+17 (1703.04310) | background for RC41 and KMOS3D | 6 deep outer-RC discs, v_rot/σ₀ > 3, log M★ ≥ 10.5; z 0.85–2.38 | DYSMAL beam-convolved fit; v_c(R_1/2) | v_c² = v_rot² + 3.36σ₀²(R/R_1/2) (Table 1 note a) | BC03 SED, Chabrier; molecular gas from scaling relations (Genzel+15 / Tacconi+); HI neglected; He UNVERIFIED; bulge plus exponential disc plus NFW | **none** | not used directly | none |
| 3 | Genzel+20, RC41 (2006.03046) | RC41 lanes CFG210/215; via RC100 | v_rot/σ₀ > 2.3, 9.5 ≤ log M★ ≤ 11.5, z 0.65–2.45, R_e ≥ 2 kpc, line detected at R ≥ R_e | forward-modelled cube, major-axis cuts; v_c(R_e) | eq. A5/A6: 3.36σ₀²(R/R_e) | SED, Chabrier; gas prior from Tacconi+18 (or Scoville+17); He UNVERIFIED; bulge plus thick Sérsic disc plus NFW | MOND named once as one possible reason for DM cores; **no a₀, no function, no test** | not used directly | none |
| 4 | Price+21, RC41 (2109.02659) | CFG210/215; RC100 method B | the RC41 sample; 14 with 2D maps | DysmalPy MCMC, 4 free parameters, NFW without contraction; f_DM at R_e,disk | eq. A4/A5: 2σ₀²(R/r_d), i.e. 3.36 at R_e | SED, Chabrier; prior Gaus(M★,SED + M_gas, 0.2 dex) with gas measured (Tacconi+13/18) or Tacconi+20; He UNVERIFIED | **none** | RC41 lanes read its Table 3 MAP values | none |
| 5 | Übler+17, KMOS3D TFR (1703.04321) | CFG6/CFG90 BTFR | KMOS3D, S/N ≳ 5, v_rot,max/σ₀ > √4.4 ≈ 2.1, no neighbours; 135 galaxies at z ~ 0.9, 1.5, 2.3 | dysmal thick exponential disc; v_circ,max at about 2.2 R_d | v_circ² = v_rot² + 2σ₀²(r/R_d) (eq. 1), i.e. 4.4σ₀² at 2.2 R_d | BC03, Chabrier; gas from Tacconi+17 depletion scaling (molecular; HI neglected, so a lower limit); He UNVERIFIED | **none**; BTFR with the Lelli+16 slope 3.75, Δb −0.44 (z 0.9) and −0.27 (z 2.3) | CFG270 does not use it; CFG270's 4.4σ₀² at 2.2 r_d equals this paper's term | none |
| 6 | Förster Schreiber+18, SINS/zC-SINF AO (1802.07276) | CFG280, CFG196 | 35 AO targets, z 1.45–2.52; five disc criteria (criterion 2: V_rot/σ₀ > √3.36 ≈ 1.83) | no mass model; V_rot = C_PSF Δv_obs/2 (maximum observed velocity difference), so **no fixed radius** | Vc = (V_rot² + 3.36σ₀²)^½ (eq. 1); M_dyn = 2R_eVc²/G (eq. 2) | BC03, Chabrier, M★ ± 0.2 dex; **no gas** | **none** | CFG280 adopts r = R_e for V_c (a convention, knobs 1.5 and 2 R_e), stars-only Freeman disc, four PHIBSS CO rows with α_CO 4.36 incl. He | at median y_can 2.14: 0.944 / 0.986 |
| 7 | KMOS3D cubes (Wisnioski+19 release; the Genzel / Price / Übler line) | CFG270 | — | **our own** arctan forward model; V_22 at 2.2 r_d | **we add** 4.4σ₀² by hand (= Burkert at 2.2 r_d) | stars only (catalogue SED M★, Chabrier) | — | the lane uses no paper's derived quantities | at median y_can 2.20: 0.944 / 0.986 |
| 8 | Amvrosiadis+ (2312.08959 v1; MNRAS 536, 3757, 2025) | CFG274; **CFG229 for ALESS 122.1** | 30 ALESS CO sources, S/N > 8 gives 20, 12 discs (v1); z 1.2–4.7 | GalPaK3D in the uv plane, h_z = 0.15 R_1/2, inclination free; **V_circ at 2 r_e** | V_circ² = V_rot² + **1.68**σ²(r/r_e) (eq. 8), i.e. 3.36σ² at 2 r_e (half of Burkert at r_e) | MAGPHYS (IMF UNVERIFIED); CO with **α_CO = 0.92 ± 0.36 derived from the same dynamics** with assumed f_dm = 0.25 (circular); He UNVERIFIED; no baryon mass model | **none** | CFG274: our thin disc with the CO r_e for stars and gas, α_CO 0.92; **CFG229: published V_circ (pressure inside) with the α = 1.68/3.36 variants added again (F2)** | ALESS 122.1 (y 4.8): 0.973 / 0.997; Amvrosiadis discs (y 6–53): 0.98–1.01 |
| 9 | Lelli+21, Science (2102.05957) | **none** (concerns ALESS 073.1, z 4.76) | single target | 3DBarolo, 9 rings | none (V_rot fitted) | bulge plus disc plus [CII] gas (α_CO 0.8) plus NFW; mass-model M★ | a₀ ≃ 1e-10 (order of magnitude), no function, no EFE: "expected to behave as a classic Newtonian system" | not a lane source (F1) | — |
| 10 | Rizzo+20, SPT0418-47 (2009.01251) | CFG228 | single lensed disc, z 4.2 | lens plus kinematic model on visibilities; V_flat 259 km/s | V_A² term computed, "small contribution (≲1%)" | dynamical Sérsic M★ 1.2e10 (SED 9.5e9 a check); gas disc with α_[CII] fitted = **7.3** (prior centred on 30); NFW c = 3.06; He UNVERIFIED | **none**; "dominated by baryons" (f_DM(<R_e) 0.018) | stars as a point mass, gas disc R_d 0.9 kpc, **α_[CII] = 30 primary** (the authors' dynamics prefer 7.3), α = 0 | y ≈ 10: 1.002 / 1.015 |
| 11 | Rizzo+23, ALPAKA I (2303.16227) | CFG229 (5 discs), CFG272 (5 discs) | archive, ≲ 0.5″, S/N ≳ 3.5 in ≥ 5 channels; 19 of 28 discs | 3DBarolo, thin disc, **inclination fixed** (i_HST for 21, i_ALMA for 7); V_ext = mean of the two outer rings | **none** ("rotation and not the circular speed") | STARDUST, Chabrier, AGN templates where known; **no gas masses** (only L′) | **none**; DM deferred | CFG229: Dunne+22 multi-tracer gas × 1.36, R_e = R_ext/1.2 for three discs; CFG272: stars only, gas floor α_CO 0.8, pressure as knobs | y 8–157: 0.996–1.005 / 1.006–1.011 |
| 12 | Jones+21, ALPINE (2104.03099) | CFG228 (comparison), CFG271 (HZ9 rings) | 75 detections, 29 fitted, 6 rotators; resolved sources only | 3DBarolo, thin disc, rings inside a ~1″ beam | **none** ("assuming perfectly circular rotation") | none in the paper (Faisst+20 LePhare M★ in a figure) | **none** | CFG228: our own forward model, α = 6.71 (2R/R_d at 2R_e) primary, [CII] α 30 plus dust; CFG271: Jones rings plus our 2σ₀²R/r_D | ALPINE y 1.3–3.3: 0.93–0.96 / 0.98–0.99 |
| 13 | Parlanti+23 (2304.00036) | CFG271 (σ₀, M★, M_rot, r_D) | archive [CII]/[OIII], z 4.2–7.6, MS only, S/N ≥ 7 | KinMS; **HZ9 fitted with Method II (integrated spectrum), not rings** | none | **Method II input M_rot = M★ + M_gas (eq. 9), M_gas = 30 L_[CII] (eq. 10)**; M★ from UV luminosity (C15: 9.86 ± 0.23); DM neglected by assumption | **none** | CFG271's "Mrot" rows treat M_rot as dynamics (**F4**); stars-only headline borrows r_D = 2.7 kpc for the stars | HZ9 y 0.41–1.13: 0.91–0.93 / 0.98 |
| 14 | Roman-Oliveira+23 (2302.03049) | CFG277 | archive < 0.3″, z 4–5, no lensed or protocluster sources; AzTEC 1 dropped (merger) | 3DBarolo, thin disc, CANNUBI inclination fixed; V_ext = mean of the last two points | **none** ("should not be used to retrieve dynamical models") | literature CO: α_CO 0.8 (3 for J081740); M_H2, He not stated; **no M★** | **none** | we add 3.36σ_ext² and use M_H2 (no He) as a point mass, half enclosed | y 4.4–21: 0.97–1.02 / 0.995–1.02 |
| 15 | Lee+25, ALMA-CRISTAL kinematics (2507.11600) | CFG213/220/234 | 32 MS galaxies, Disk Score (16 discs); z 4.4–5.7 | DysmalPy (n = 1 thick disc, small bulge, NFW, no contraction); V_rot at R_e | V_rot² = V_circ² − 3.36σ₀²(R/R_e); **tabulated V_rot(R_e) is the pressure-reduced speed** | M★ from Li+24 / Mitsuhashi+24 (Chabrier via the overview); gas = **Band-7 dust**, Tacconi+20 eq. 3, T_d = 50 K, metallicity δ_gd ([CII] gives +0.23 dex); He not stated; M_bary prior **1 dex** wide | **none**; "CRISTAL disks tend to be baryonic-dominated" (median f_DM 18%) | D = 1/(1 − f_DM) from MAP values; α = 3.36 (vector curves give 3.37); independent route: SED M★ plus the same dust gas via f_molgas | g_bar/a₀ 1.0–1.6: 0.928–0.937 / 0.982–0.984 |
| 16 | Herrera-Camus+25, CRISTAL overview (2505.06340) | inherited by 15 | [CII] S/N ≥ 3, ±0.5 dex of MS, M★ ≥ 10^9.5 | — | — | CIGALE (MAGPHYS cross-check), Chabrier; **no gas recipe** | **none** | — | — |
| 17 | Danhaive+25 (2503.21863) | CFG273 | gold: S/N > 20, PA cuts, r_e > 0.12″; 41 (v1); z 3.8–5.8 | geko grism forward model; v at r_e; thin disc (q₀ 0.2 for inclination) | v_circ² = v_rot² + 2(r/r_s)σ₀² = 3.36σ₀² at r_e; **M_dyn = k_tot r_e v_circ²/G with k_tot = 1.8 (total mass)** | Prospector (IMF not stated); **no gas** | **none**; DM deferred | g_obs = G M_dyn/(1.8 r_e²): correct; stars only; σ₀ limits at face value | conditioned, range deep to y ~ 10: 0.89–1.00 |
| 18 | Puglisi+23, KURVS-CDFS (2305.04382) | CFG140/141/160/175/184/189 | 22 galaxies, z 1.23–1.71; rotation-supported v_rot/σ₀ ≥ 1.5 (10 for f_DM) | Freeman fit used to interpolate; V at R′3D (beam-corrected), R′6D and the last point | Burkert+10 for f_DM only (formula not printed: UNVERIFIED); **tabulated V not pressure-corrected** | MAGPHYS, Chabrier, ± 0.2 dex; gas = **40% molecular fraction** (Tacconi+20 typical); Freeman thin disc | **none**; f_DM(R_e) = 50 ± 20% | V at R_max, gas bracket μ 0.25–4, pressure P0/P1/P2/Kretschmer, SPARC anchor offset | y_can 0.06–0.67: 0.895–0.921 / 0.974–0.980 |
| 19 | MUSE-DARK I, Ciocan+26 (2506.19721) | CFG198/199/236/262 (data release) | MHUDF, S/N_eff > 10, R_e/R_PSF > 0.5, i > 30°, no mergers, v_max/σ ≥ 1; 127 galaxies, z 0.28–1.49 | GalPaK3D 3D disc–halo decomposition (6 halo families) | **v_AD² = 0.92σ²(r/r_d)** (Dalcanton & Stilp) | Magphys, Chabrier; disc includes H2; HI fitted as a nuisance; **no M★ prior for DC14**; errors are 95% CIs | **none** | route (i) uses the DC14 fitted mass, route (ii) SED M★ plus MS H2; drift reading 0.92 | deep to intermediate: 0.89–0.95 |
| 20 | MUSE-DARK II, Jeanneau+26 (2603.28856) | CFG190 only | lensed [OII], 0.5 < z < 1.5, S/N_eff > 10, i > 30° | GalPaK3D with lensing; V at 1.8 / 2 R_e | v_⊥² = v_c² − 0.92σ_r²(r/R_d) | Bagpipes (Chabrier-corrected); gas = Tacconi+20 Tab. 2b molecular plus NeutralUniverseMachine HI × 1.33 | **none**; bTFR zero point Δb = 0.00 ± 0.06 dex from Lelli+19 | CFG190 used the bTFR offset | — |
| 21 | MUSE-DARK III, Ciocan+26 (2604.22613) | CFG190, CFG198/199/236/262 (the law) | 79 regular galaxies of Paper I, log M★ > 8.8, z 0.33–1.44 | a_bar and a_tot from the **same** DC14 model per galaxy | inherited 0.92 coefficient | M★ **dynamical** (not SED); disc = stars plus H2; HI constant Σ | **a₀ fitted = 2.38 (+0.12/−0.10)e-10 (95% CI), McGaugh+16 RAR; EFE not included**; a₀(z) = a₀(0) + a₁z, a₀(0) 1.0 ± 0.04, a₁ 1.59 ± 0.10 | our route (ii) replaces the dynamical M★ with SED M★ plus H2; the rise does not survive | the fitted 2.38 is 2.5× canonical and 2.1× alt; the intercept 1.0 lies between the footings |
| 22 | Brouwer+21, KiDS-1000 lensing RAR (2106.11677) | CFG61, CFG255, CFG261 | KiDS-bright, 0.1 < z < 0.5, isolated (no neighbour with > 10% of M★ within 3 Mpc/h70), M★ < 1e11; 259,383 lenses | ΔΣ → g_obs via an SIS conversion (eq. 6–7) plus 0.1 dex added to errors; isolation reliable for g_bar ≳ 1e-13 | n/a | LePhare (BC03, Chabrier) normalised to GAMA; cold gas f_cold (Boselli+14, eq. 23); **point mass; no hot gas** ("a secure lower limit on gbar") | **g† = 1.20 ± 0.26e-10 FIXED, McGaugh+16 RAR; EFE (e = 0.003) shown only in Fig. 4**; "agrees well with the MG predictions"; early/late RARs differ at ≥ 6σ | our own per-lens reconstruction (181,477 lenses), colour proxy u−r > 2.0 (paper 2.5), the same f_cold, B's law with a truncation edge | deep regime: 0.888 / 0.972 (−0.052 / −0.012 dex) |
| 23 | Vărăşteanu+26, MIGHTEE-HI / LADUMA (2608.03576) | CFG258 | 124 + 6 HI galaxies, ≥ 3 beams, 30° < i < 80°, z ≤ 0.09; no environment cut | 3DBarolo, razor-thin HI, optical inclination fixed, two points per beam | **none** ("We do not correct for asymmetric drift") | Bagpipes, Chabrier, resolved Υ★(r); HI × 1.4 for He; H2 from Tacconi+18 (He included) | **a₀ fitted = 1.50 ± 0.05e-10 (1.31–1.86 by subsample and δ-family), McGaugh–Lelli–Schombert RAR; EFE not applied**; "no significant redshift evolution"; the SPARC-anchored a₁ = 5.23 ± 1.05 is explained by sample selection and modelling | mocks only: the abstract numbers, nothing downloaded | the fitted 1.50 is 1.60× canonical (+0.20 dex) and 1.33× alt (+0.12 dex) |
| — | Lelli+23 (2302.00030) (context: on disk, used only for CFG229's class rule) | — | 2 discs, z 1.47, 2.24 | 3DBarolo on CO | none needed (V/σ ≳ 17) | free gas and stellar normalisations | **a₀ = 1.2e-10 FIXED, McGaugh+16 RAR**; curves "compatible with" the z ≈ 0 a₀ in the Newtonian regime (g > 3–4 a₀) | — | high y: ~1.00 |

---

## 3. The a₀ and kernel census

| paper | a₀ used | fixed or fitted | interpolating function | EFE | regime probed | statement |
|---|---|---|---|---|---|---|
| Brouwer+21 | 1.20 ± 0.26e-10 | fixed (McGaugh+16) | McGaugh+16 RAR (eq. 11) | e = 0.003 in Fig. 4 only; e = 0 in the main comparison | deep (g_bar 1e-15 to 5e-12) | "agrees well with the MG predictions"; early/late-type split ≥ 6σ |
| MUSE-DARK III | 2.38 (+0.12/−0.10)e-10 (95% CI) | fitted | McGaugh+16 RAR (eq. 1); a MOND refit with Famaey & Durakovic functions gives 2.19 | not included ("in isolation") | intermediate | a₀ rises with z, a₀(0) = 1.0 ± 0.04, a₁ = 1.59 ± 0.10 per unit z |
| Vărăşteanu+26 | 1.50 ± 0.05e-10 (fiducial) | fitted | McGaugh–Lelli–Schombert RAR | not applied | full RAR at z ≤ 0.09 | "no significant redshift evolution"; anchored 5σ slope explained by sample selection and modelling |
| Lelli+23 (context) | 1.2e-10 | fixed | McGaugh+16 RAR | — | Newtonian (g > 3–4 a₀) | compatible with the z ≈ 0 values |
| Lelli+21 (not a lane source) | ≃ 1e-10 | order of magnitude | none | not considered | ~7 a₀ | Newtonian |
| Genzel+20 | — | — | — | — | — | MOND named once, not tested |
| the other 17 papers | — | — | — | — | — | no MOND or RAR comparison |

- **No paper adopts a value below 1.2e-10.** Lelli+21's "a₀ ≃ 1e-10" is an order of magnitude only. The two that fit a₀ get values above both programme footings: MIGHTEE 1.50 at z ≈ 0.05, and MUSE-DARK III 2.38 at z ≈ 0.9 with its dynamically fitted M★.
- **The kernel is homogeneous: the McGaugh+16 RAR form.** The programme's ν_mono is a monotone repair of the same function, so the kernel difference is small. Combined with the canonical a₀, it is −0.025 dex at y ≈ 2, about 0 at y ≈ 10, and up to +0.006 dex (1.5%) at y ≈ 20–50, where ν_mono's tail sits slightly above the RAR. P2 at the canonical a₀ differs more: −0.06 to −0.09 dex at y_can ≈ 0.06–2.
- **The EFE is absent from every headline statement.** Brouwer's isolation criterion and MUSE-DARK III's exclusion of interacting galaxies are the only gestures toward it.

---

## 4. Which baryon recipes dominate

- **Stellar masses:**
  - SED fits with a Chabrier IMF are almost universal: BC03/Wuyts in SINS/KMOS3D/RC100; MAGPHYS in KURVS, Amvrosiadis and MUSE-DARK I; STARDUST in ALPAKA; CIGALE/MAGPHYS in CRISTAL; LePhare in KiDS and ALPINE; Bagpipes in MIGHTEE and MUSE-DARK II.
  - The IMF is not stated by Amvrosiadis or Danhaive (Prospector).
  - Three sources use **dynamical** stellar masses inside a halo decomposition: MUSE-DARK III (DC14), Rizzo+20 and Lelli+21.
  - Parlanti+23 uses UV-luminosity masses.
- **Gas: the Tacconi scaling relations are the dominant recipe.** They give molecular gas only, with the 1.36 helium factor included by Tacconi+20's convention ("we correct H2 masses upward by 1.36 for the content for helium", Tacconi+20 footnote 1), and they neglect HI. They enter as a **prior or a fixed fraction**, never as a measurement:
  - Tacconi+20: RC100, Price+21, KURVS's 40% fraction, MUSE-DARK II;
  - Tacconi+18: Genzel+20, MIGHTEE's H2;
  - Tacconi+17: Übler+17 (and Genzel+17's "PHIBSS: Unified Scaling Relations", submitted 2017).
- **Measured gas is rare.** It is converted with a wide spread of factors:
  - α_CO = 0.8 (Roman-Oliveira, Lelli+21);
  - α_CO = 0.92 (Amvrosiadis v1), derived from the same dynamics;
  - dust continuum at T_d = 50 K (CRISTAL; T_d = 25 K would add about 0.5 dex);
  - α_[CII] = 30 (Parlanti), where Rizzo+20's own dynamics give 7.3.
- **No gas at all:** FS+18, ALPAKA I (L′ only), Jones+21, Danhaive+25. These are exactly the sources behind our stars-only lanes (CFG272, CFG273, CFG280, CFG271).
- **Helium is stated only by Tacconi+20 (H2), MIGHTEE (HI × 1.4; H2 via Tacconi), MUSE-DARK II (HI × 1.33) and Lelli+21 (atomic gas).** It is UNVERIFIED everywhere else.
- **Pressure.** Four prescriptions are in use:
  - Burkert+10, 3.36σ₀²(r/R_e): RC100, Genzel+17/20, Price+21, FS+18, CRISTAL, Danhaive; KURVS cites it without printing it.
  - 2σ₀²(r/R_d), i.e. 4.4σ₀² at 2.2 R_d: Übler+17.
  - 1.68σ²(r/r_e): Amvrosiadis.
  - 0.92σ²(r/r_d) (Dalcanton & Stilp): MUSE-DARK I/II/III. At the same radius this is 0.46× the Burkert term.
  - None or negligible: Rizzo+20 (≲ 1%), ALPAKA I, Jones+21, Parlanti+23, Roman-Oliveira+23, MIGHTEE, Lelli+21/23.
- **Geometry:** the sources fit bulge + thick disc + NFW (RC100, RC41, CRISTAL, Lelli+21) or Sérsic + gas disc + NFW (Rizzo+20). Our lanes mostly use **one thin exponential disc for stars and gas with a borrowed scale and no bulge**.

---

## 5. The three most consequential recipe differences between the papers and our lanes

1. **Gas (the baryon normalisation).**
   - The sources' gas is either absent, a Tacconi scaling prior, or a single-tracer conversion with factor-of-several spread. Our lanes either drop it, which gives stars-only lower limits, or substitute our own conversion: Dunne+22 multi-tracer × 1.36 (CFG229), α_[CII] = 30 plus dust (CFG228), α_CO 0.8 / 4.36 / 0.92 (CFG272, CFG274, CFG280).
   - The size of the effect is on record. CFG217: a 0.25 dex differential gas tilt reverses RC100's flat-versus-rival reading. CFG228: the gas outer band alone flips two floors. CFG270/273: the scaling gas turns most roots into floors.
   - This is larger than the a₀ footing difference at every lane's regime.
2. **The pressure term.**
   - The sources range from no correction to 3.36σ₀²(r/R_e). Our own-extraction lanes add terms the papers do not use:
     - α = 6.71 at 2 R_e for ALPINE (CFG228 primary). The pressure term alone moves the pooled ALPINE s* from no root to 4.33.
     - 4.4σ₀² on an arctan V_22 (CFG270). Without it there is no root.
     - 2σ₀²R/r_D on Jones's rings (CFG271).
     - 3.36σ² on Roman-Oliveira's and ALPAKA's uncorrected V (CFG277, and CFG272 as knobs).
   - Where the paper's V already contains the term, adding it again double-counts (F2, CFG229 for ALESS 122.1).
3. **Geometry and radius.**
   - FS+18's V_c has no radius: it is half the maximum observed velocity difference. CFG280's r = R_e is a convention (knobs −0.19 to −0.24 dex).
   - Amvrosiadis gives V_circ at 2 r_e from a kinematic model inside the beam.
   - ALPAKA R_ext is about one beam for three discs.
   - The stellar scale is borrowed: the CO r_e (CFG229, CFG274), the [CII] disc scale (CFG271, where a compact stellar disc moves the bound by 1.6 dex) or R_ext/1.2.
   - Bulges that the sources fit are dropped.
   - CFG229's geometry variants move s* by a factor of 2 (7.9 to 14.7) for ALESS 122.1.

For comparison, the a₀ footing difference itself is small (helper output): at y_can ≈ 2, which is RC100, SINS and KMOS3D, the canonical a₀ with ν_mono changes the predicted g_obs by −0.025 dex against the 1.2e-10 RAR (alt −0.006). In the deep regime (KiDS, the KURVS outskirts) it is −0.05 dex canonical and −0.012 alt. In the Newtonian regime (ALPAKA, Amvrosiadis, SPT0418) it is −0.002 to +0.006 dex.

---

## 6. Where a published statement does not transfer to the programme's law as written, and what this audit finds about our lanes

**Statements that do not transfer (arithmetic and reading only):**

- **Brouwer+21, "agrees well with the MG predictions" (g† = 1.2e-10 fixed, point-mass stars plus cold gas, no hot gas, no truncation).**
  - At the programme's canonical a₀ the deep-regime prediction is lower by a factor 0.888 (−0.052 dex). That is equivalent to lowering the lens baryon masses by about 0.10 dex. The alt footing gives −0.012 dex.
  - Brouwer's own χ²_red with −0.2 dex in M★ is 14, against 4.0–4.6 nominal and 1.5 at +0.2 dex. So the agreement they report does not carry over automatically to the canonical footing: the arithmetic direction is toward a worse fit. That is consistent with CFG61 and CFG261, which find early-type lenses well above the law (s* 2.5–4.1) and late types near it.
  - The early/late difference (≥ 6σ in the paper; CFG61's 3.7σ in the 1-halo bins) transfers unchanged, because it is a statement against any colour-blind law, ours included.
  - B's law also has a truncation edge that Brouwer's MOND line does not.
- **MUSE-DARK III, "a₀ rises with z" (a₀ = 2.38e-10, a₁ = 1.59).**
  - Both axes come from one DC14 model per galaxy, with a dynamically fitted M★ and no M★ prior for DC14 (Paper I). The statement is about that decomposition.
  - Our lanes CFG198/199/236/262 showed the rise travels with the fitted-mass route. It is absent with SED M★ plus H2, and the routes disagree by up to a factor 13 at z ≈ 1.2.
  - The level does not transfer either. Their a₀ at z ≈ 0.9 is 2.5× our canonical value. Their z → 0 intercept, 1.0e-10, happens to lie between our footings (1.07× canonical, 0.88× alt), but it is an extrapolation of a linear form they call phenomenological.
  - Arithmetic, mine: their "∼19σ" against 1.2e-10 ignores the ±0.26 on 1.2e-10. Including it gives about 4.4σ.
- **MIGHTEE (Vărăşteanu+26), "no significant redshift evolution".**
  - This transfers as a slope statement (a₁ = −1.60 ± 2.33 within the sample), and that is all CFG258 used.
  - Their level is 1.50e-10 (fiducial), which is +0.20 dex above canonical and +0.12 dex above alt. It swings from 1.31 to 1.80 by photometric class, comes without an asymmetric-drift correction, and uses scaling-relation H2.
  - The SPARC-anchored a₁ = 5.23 is attributed by the authors to sample selection and modelling (it changes sign under a constant Υ_Ks = 0.6). It does not transfer as a physical law (CFG258: about 1σ under a modest shared budget).
- **Lelli+21 / Lelli+23 (Newtonian at > 3 a₀).** These transfer trivially. At y ≳ 10, ν_mono at the canonical a₀ gives up to 1.5% more boost than the 1.2e-10 RAR, so our law is, if anything, marginally less Newtonian there.
- **"Baryon-dominated" or "DM-poor" conclusions** (Genzel+17/20, Price+21, RC100, CRISTAL, Rizzo+20, Lelli+21) are ΛCDM-halo statements (NFW with abundance-matching or flat priors). They are not MOND statements.
  - Where our lanes use the resulting f_DM as D_obs (RC100, CRISTAL), the D inherits the halo model, the M_bar prior (0.2 dex for Price/RC100, 1 dex for CRISTAL) and the 3.36σ₀² term.
  - CFG233 and CFG234 already say this. The audit confirms the recipe from the primary texts.

**Findings about our lanes (record only; no lane re-run, no number changed):**

- **F1. Source label.**
  - Lelli+21 (Science, arXiv:2102.05957) is about ALESS 073.1 at z = 4.76, not ALESS 122.1.
  - CFG229 correctly takes ALESS 122.1 from Amvrosiadis+ (2312.08959): `cfg229_inputs.py` reads `amvrosiadis_bestfit.csv`. Only the brief's attribution was wrong.
  - No lane in scope uses Lelli+21.
- **F2. CFG229, ALESS 122.1: the pressure variants double-count.**
  - Amvrosiadis's V_circ(2 r_e) = 533 km/s is "defined as the rotational velocity corrected for asymmetric drift" (eq. 8, 1.68σ²(r/r_e), i.e. 3.36σ² at 2 r_e).
  - `cfg229_inputs.py` sets `V_noP = V` with `alpha_pub = 0`, so the headline (s* = 8.82) uses the published V_circ once, which is correct.
  - But the sensitivity rows "pressure α = 1.68 / 3.36" (s* 13 / 17.9) add the term a second time, and the README's envelope "3.7 to 17.9" includes them.
  - The physically meaningful pressure variant runs the other way: rotation only. Arithmetic, if eq. 8 was applied at r = 2 r_e: V_rot ≈ √(533² − 3.36·157²) ≈ 449 km/s, which lowers g_obs by 0.15 dex.
  - CFG274 treats the same tables correctly: its "P+" knob is labelled double-counted.
- **F3. CFG274 inputs are arXiv v1.**
  - In v1, α_CO = 0.92 ± 0.36 is derived from the same V_circ with an assumed f_dm = 0.25 (circular; v1's conclusions say 1.0 ± 0.4). There are 12 discs in v1.
  - The published MNRAS abstract, read twice through a page-fetch tool and **not character-verified**, gives α_CO = 0.74 ± 0.37. The reader of the published HTML also saw ALESS 065.1 moved to Class II and an 11-row best-fit table (UNVERIFIED).
  - CFG274's 065.1 row and its gas normalisation should be re-checked against the published PDF before citing.
- **F4. CFG271, HZ9: the Parlanti+23 M_rot rows are not dynamics.**
  - HZ9 was fitted with Parlanti's Method II ("Best-fitting results from method II for the target HZ9", Fig. 3). Its mass is an input: M_rot = M★ + M_gas (eq. 9), with M_gas = 30 L_[CII] (eq. 10).
  - So the "Mrot" sensitivity rows compare baryons with baryons. Their "within a factor 1.27" agreement with the ring reading is not a second kinematic reading. The README calls it "a second kinematic reading from a different method".
  - The only ring kinematics is Jones+21 (Table C1 in the arXiv text; the repo's file is named `tableA3`).
  - Arithmetic, not run: Parlanti's numbers imply a [CII]-based gas mass M_gas ≈ 10^10.8 − 10^9.86 ≈ 5.6e10 M☉ (±0.4 dex on M_rot, ±0.2 dex on α_[CII]). CFG271 says "no gas is on disk for HZ9"; a class-S gas estimate is in fact implied by the source.
- **F5. Checks that pass (the lane handled the source correctly):**
  - CFG273 divides Danhaive's M_dyn by k_tot = 1.8 (total-mass coefficient) and the pressure term is included once.
  - CFG213/234 avoid CRISTAL's pressure-reduced V_rot(R_e) by working from f_DM, and recover k = 3.37.
  - CFG236's best-supported drift reading (0.92) equals MUSE-DARK I's coefficient.
  - CFG280's M5 reproduces FS+18's eq. 1, and M6 its eq. 2.
  - CFG216/233's pressure relation is RC100's eq. 8.
  - CFG261 uses Brouwer's own f_cold (Boselli+14, eq. 23).
- **F6. CFG217's unverified assumptions A1 and A2 are now verified** from RC100's text:
  - the prior centre is SED M★ plus **Tacconi+20** molecular gas (no HI mentioned; He included by Tacconi+20's convention);
  - V_c includes 3.36σ₀²(r/R_e).
  - CFG217's M★ reconstruction used Tacconi+18, not +20. It was rejected at 0.229 dex anyway.
- **F7. CRISTAL table semantics:**
  - column (a) is labelled log M_tot while the free parameter is M_bary;
  - the Table 3 footnote mislabels column (h);
  - the gas is single-band dust at T_d = 50 K with metallicity-dependent δ_gd, helium not stated.
  - CFG234 already noted that no provenance note compares the repo's CRISTAL CSVs to the paper.
- **F8. KURVS:** the tabulated "velocity at the last observed data point" is called inclination-corrected only. Whether it is a model read or a data point is ambiguous in the paper. The pressure formula behind f_DM is not printed.
- **F9. MUSE-DARK naming:**
  - arXiv:2506.19721 is MUSE-DARK **I** (Ciocan+26). The repo's data front labels it correctly.
  - CFG198/199/236/262 use Paper I's release and Paper III's law.
  - MUSE-DARK II (Jeanneau+26, arXiv:2603.28856) is a lensed-galaxy TFR paper, used only by CFG190.

---

## 7. Per-paper details (quotes verified against the primary text; the location follows each quote)

### 7.1 RC100: Nestor Shachar+23, arXiv:2209.12199 (text layer `papers/rc100.txt`)
- **Selection:**
  - The sample: "rotation-dominated (v_rot/σ₀ > 2.3) SFGs at log(M⋆/M⊙) > 9.5" (Sect. 2, l. 232–233), with −0.6 < δMS < 1. Night-sky and resolution cuts were applied, but "we were less strict than G20" (l. 237).
  - There is no fixed S/N or size cut. z 0.6–2.5 (33 + 67 galaxies).
- **Kinematics:**
  - Three methods: (A) DYSMAL least squares; (B) DysmalPy MCMC (Price+21); (C) MCMC with galaxy-plane beam projection.
  - Table 3 is "the average value of all three" (l. 426). The radial extent is 2.2 R_e on average.
- **Pressure:** eq. 8, V_rot² = V_circ² − 3.36σ₀²(r/R_e), "an exponential disk with a constant velocity dispersion" (App. A, l. 1003).
- **Baryons:**
  - Chabrier (l. 155). M★ from SED (Wuyts+11).
  - Gas: "The scaling relations of Tacconi et al. (2020) provide the cold gas mass estimate" (Sect. 3, l. 355).
  - Disc q₀ 0.2–0.25 (l. 358). f_DM is "an average of a regular NFW halo and a contracted NFW halo" (l. 382).
- **MOND:** none. A grep for MOND, Milgrom, modif and "acceleration" finds no MOND, RAR or a₀ text.
- **Helium:** via Tacconi+20 (arXiv:2003.06245), footnote 1: "we correct H2 masses upward by 1.36 for the content for helium".

### 7.2 Genzel+17, arXiv:1703.04310 (PDF page read)
- **Selection:** v_rot/σ₀ > 3 and log M★ ≥ 10.5 (Methods).
- **Kinematics:** DYSMAL.
- **Pressure:** Table 1 note a gives v_c² = v_rot² + 3.36σ₀²(R/R_1/2).
- **Baryons:** molecular gas from "general scaling relations"; HI neglected, so "scaling relations may be lower limits".
- **DM:** "Our analysis leaves little space for dark matter in the" inner discs (main text).
- **MOND:** none. The only "MOND" substring is inside "diamonds".

### 7.3 Genzel+20, arXiv:2006.03046 (PDF page read)
- **Selection:** v_rot/σ₀ > 2.3, 9.5 ≤ log M★ ≤ 11.5, 0.65 ≤ z ≤ 2.5, R_e ≥ 2 kpc (Sect. 2.1).
- **Pressure:** eq. A5/A6 (3.36).
- **Gas:** a prior from Tacconi+18 / Scoville+17. Median f_DM(R_e) = 0.12 for z ≥ 1.2 (abstract).
- **MOND:** one mention, Sect. 4.3: a core explanation that "favors a fundamental change of the law of gravity, MOND (Milgrom 1983)". There is no a₀, no function and no test. The authors prefer baryon–DM interaction.

### 7.4 Price+21, arXiv:2109.02659 (PDF page read)
- **Kinematics:** DysmalPy MCMC on RC41, with free parameters log M_bar, R_e,disk, σ₀ and f_DM(R_e).
- **M_bar prior:** "Gaus log10 (M∗,SED + Mgas ), 0.2 dex" (Table 2). The gas is measured (Tacconi+13/18) or from Tacconi+20.
- **Pressure:** eq. A4/A5 (3.36 at R_e for n = 1).
- **MOND:** none.

### 7.5 Übler+17, arXiv:1703.04321 (PDF page read)
- **Pressure:** eq. 1, v_circ² = v_rot² + 2σ₀²(r/R_d).
- **Selection:** the cut is v_rot,max/σ₀ > √4.4.
- **Gas:** "Gas masses are obtained from the scaling relations by Tacconi et al. (2017)" (data section). Molecular only, so the masses are lower limits.
- **BTFR:** slope 3.75 fixed (Lelli+16).
- **MOND:** none.

### 7.6 Förster Schreiber+18, arXiv:1802.07276 (PDF page read)
- **Selection:**
  - 35 AO targets. For zC-SINF: "No explicit Hα flux or S/N cut was applied" (sample section).
  - Five disc criteria (Sect. 7.1). Criterion 2 is V_rot/σ₀ > √3.36.
- **Kinematics:** V_rot sin i = C_PSF,v Δv_obs/2 from "the maximum observed velocity difference". No radius is attached.
- **Pressure:** eq. 1, Vc = (V_rot² + 3.36σ₀²)^½.
- **Dynamical mass:** eq. 2, M_dyn = 2 R_e Vc²/G. The irregulars' line-width alternative is 1.4× higher in Vc.
- **Gas:** none.
- **MOND:** none. No dark-matter statement.

### 7.7 Amvrosiadis+, arXiv:2312.08959 v1 (local TeX `main.tex`)
- **Selection:** S/N > 8, giving 20 sources (l. 291); 12 discs (l. 439).
- **Kinematics:** GalPaK3D in the uv plane, h_z = 0.15 R_1/2 (l. 368).
- **Pressure:** V_circ is "the rotational velocity corrected for asymmetric drift" (l. 557), with eq. 8 V_circ² = V_rot² + 1.68σ²(r/r_e) (l. 563).
- **Dynamical mass:** M_dyn = r V_circ²/G at 10 kpc (l. 567).
- **Gas and α_CO:**
  - α_CO = 0.92 ± 0.36 (l. 305), derived with "we assume a fixed dark matter fraction, f_dm = 0.25" (l. 639).
  - The conclusions say 1.0 ± 0.4 (l. 754).
  - The ALESS 122.1 gas mass is from Calistro Rivera+18 (Table 1 note). CFG229 replaced it with Dunne+22.
- **MOND:** none.
- **TFR:** offsets Δb = −0.53 ± 0.29 (stellar) and −0.26 ± 0.19 (baryonic).

### 7.8 Lelli+21, arXiv:2102.05957 (PDF page read): ALESS 073.1
- **Kinematics:** 3DBarolo, 9 rings. The mass model is bulge + disc + gas + NFW.
- **DM:** "DM within 3.5 kpc is not strictly necessary" (Suppl.).
- **MOND:** "a0 ≃ 10−10 m s−2", assumed not to vary with z. The galaxy "is expected to behave as a classic Newtonian system" (Suppl., Alternative Mass Models). There is no interpolating function and no EFE.

### 7.9 Rizzo+20, arXiv:2009.01251 (local TeX `ms_rizzo_ex.tex`)
- **Pressure:** Methods eq. 6, V_A² = −Rσ² ∂ln(σ²Σ_gas)/∂R, which gives "small contribution (≲1%)" (l. 159).
- **Gas:** the conversion factor is the only free gas parameter, and "We infer a value of" α_[CII] = 7.3 (+1.0/−1.2) (l. 163).
- **MOND:** none.

### 7.10 Rizzo+23, ALPAKA I, arXiv:2303.16227 (local TeX `alpaka_v2.tex`)
- **Basics:** Chabrier (l. 166). 19 of 28 are discs (l. 503).
- **Inclination:** fixed to the GALFIT values for 21 galaxies (l. 471).
- **Velocities:** the curves "show the rotation and not the circular speed" (l. 656). V_ext is from "averaging the two outermost values in their profiles" (l. 669).
- **Gas:** no gas masses.
- **MOND:** none.

### 7.11 Jones+21, ALPINE, arXiv:2104.03099 (PDF page read)
- **Kinematics:** 3DBarolo, thin disc. M_dyn = v²r/G "assuming perfectly circular rotation".
- **Pressure:** the dispersion "is not accounted for in these dynamical masses".
- **HZ9 rings:** R = 0.54 / 1.61 / 2.68 kpc, V = 155.85 / 156.77 / 176.63 km/s, σ = 71.1 / 75.12 / 4.82 km/s (Table C1). These equal the repo's corpus rows.
- **MOND:** none.

### 7.12 Parlanti+23, arXiv:2304.00036 (PDF page read)
- **HZ9 fit:** "Best-fitting results from method II for the target HZ9" (Fig. 3).
- **Method II masses:** eq. 9, M_rot = M★ + M_gas; eq. 10, M_gas = α_[CII] L_[CII] with α_[CII] = 30, about 0.2 dex uncertain.
- **DM:** "We therefore neglected the contribution of dark matter to the circular motion" (model section).
- **σ:** the Method II σ is divided by 1.6.
- **MOND:** none.

### 7.13 Roman-Oliveira+23, arXiv:2302.03049 (local TeX `main.tex`)
- **Gas:** α_CO of 0.8, and 3 for J081740 (l. 204).
- **Kinematics:** an infinitely thin disc with CANNUBI inclination (l. 482).
- **Pressure:** none. "these rotation curves should not be used to retrieve dynamical models" (l. 603).
- **Stellar masses:** none.
- **MOND:** none.

### 7.14 Lee+25, CRISTAL, arXiv:2507.11600 (local TeX `main_arxiv.tex`)
- **Sample:** 32 galaxies (l. 234).
- **Pressure:** Burkert correction, V_rot² = V_circ² − 3.36σ₀²(R/R_e) (l. 818, 822). The tabulated rotation velocity is "the intrinsic total (baryons and dark matter) velocity" of that equation (l. 807).
- **M_bary prior:** "with a standard deviation of 1 dex centred on the sum of the stellar mass" (l. 907).
- **Gas:** dust, "following Eq. (3) in Tacconi2020" (l. 1898), at T_d = 50 K.
- **DM:** "CRISTAL disks tend to be baryonic-dominated" (l. 1247), with median f_DM 18% (l. 1249).
- **MOND:** none.

### 7.15 Herrera-Camus+25, CRISTAL overview, arXiv:2505.06340 (PDF page read)
- **Masses:** "normalized to a Chabrier (2003) initial mass function (IMF)" (introduction). M★ from CIGALE.
- **Gas:** no gas recipe.
- **MOND:** none.

### 7.16 Danhaive+25, arXiv:2503.21863 v1 (local TeX `main.tex`)
- **Selection:** S/N > 10 (l. 214); the gold criteria are in Table 1.
- **Pressure:** v_circ² = v_rot² + 2(r/r_s)σ₀² (l. 380), which is 3.36 at r_e (l. 384).
- **Dynamical mass:** M_dyn = k_tot r_e v_circ²/G with k_tot = 1.8 (l. 389).
- **DM:** deferred (l. 556).
- **MOND:** none.
- **Version:** the published version has 37 gold galaxies (CFG273 addendum; UNVERIFIED which four rows were dropped).

### 7.17 Puglisi+23, KURVS-CDFS, arXiv:2305.04382 (local TeX)
- **Selection:** "We use a threshold of v_rot/σ₀ ≥ 1.5" (l. 416).
- **Pressure:** Burkert+10 (l. 631), formula not printed.
- **Baryons:** stellar mass plus "a 40% molecular gas fraction" (l. 635), in a Freeman thin disc (l. 638).
- **DM:** "average dark matter fractions of 50 ± 20% at the effective radius" (l. 84).
- **MOND:** none.
- **KURVS II:** no dark-matter KURVS paper was found on arXiv. The chemistry paper is arXiv:2512.09983 and has no MOND content.

### 7.18 MUSE-DARK I, Ciocan+26, arXiv:2506.19721 (PDF page read)
- **Title page:** "I. Dark matter halo properties of intermediate-z star-forming galaxies".
- **Pressure:** v_AD = 0.92σ²(r/r_d), after Dalcanton & Stilp (Sect. 2.2). The printed left side is a typo for v_AD².
- **Mass priors:** none on M★ for DC14.
- **MOND:** none.

### 7.19 MUSE-DARK II, Jeanneau+26, arXiv:2603.28856 (local TeX `aa59953-26.tex`)
- **Selection:** 0.5 < z < 1.5 (l. 328).
- **Pressure:** v_⊥² = v_c² − 0.92σ_r²(r/R_d) (l. 223).
- **Gas:** Tacconi+20 Tab. 2b plus NeutralUniverseMachine HI, with f_gas,at = 1.33 M_HI/M_bar (l. 433–435).
- **bTFR:** Δb = 0.00 ± 0.06 dex (abstract).
- **MOND:** none (one introductory citation to the RAR).

### 7.20 MUSE-DARK III, Ciocan+26, arXiv:2604.22613 (PDF page read)
- **Title:** "III: The evolution of the radial acceleration relation at intermediate redshifts".
- **a₀:** fitted, 2.38 (+0.12/−0.10)e-10, "significantly higher, by ∼ 19σ," than 1.2 ± 0.26e-10 (eq. 2).
- **a₀(z):** a₀(0) = 1.0 ± 0.04 and a₁ = 1.59 ± 0.10 (eq. 4).
- **EFE:** the MOND prescription is "in isolation, without accounting for the external field effect (EFE)" (footnote 4).

### 7.21 Brouwer+21, arXiv:2106.11677 (PDF page read)
- **Isolation:** r_sat(f_M★ > 0.1) > 3 Mpc/h70, giving 259,383 lenses (Sect. 3.3).
- **g_obs:** SIS conversion (eq. 6–7).
- **Baryons:** a point mass. Cold gas from Boselli+14 (eq. 23). M_gal "serves as a secure lower limit on gbar" (Sect. 4.3).
- **a₀ and function:** "g† = 1.20 ± 0.26 × 10−10 m s−2" with the M16 function (eq. 11).
- **EFE:** e = 0.003, illustrative.
- **Conclusion:** "agrees well with the MG predictions" (abstract). The early/late RARs differ "with a 5.7σ significance" (main text).
- **Caveat:** the authors say the verdict depends "heavily on the systematic bias in the stellar mass measurements".

### 7.22 Vărăşteanu+26, MIGHTEE-HI / LADUMA, arXiv:2608.03576 (local TeX `main.tex`)
- **Sample:** 124 MIGHTEE + 6 LADUMA galaxies (l. 225), 30° < i < 80° (l. 229).
- **Pressure:** "We do not correct for asymmetric drift" (l. 498–499).
- **Helium:** a factor of 1.4 for HI; H2 includes He through Tacconi (l. 488).
- **Function:** the McGaugh–Lelli RAR (l. 526).
- **a₀:** 1.50 ± 0.05e-10 (l. 540).
- **Evolution:** "We find no significant redshift evolution in the RAR acceleration scale" (l. 104). The anchored fit gives "a formal 5.0σ preference" (l. 739), attributed to "the different sample selection" of SPARC (l. 742).
- **Data:** there is no public per-galaxy table. It is available on request (l. 1001).

### 7.23 Lelli+23, arXiv:2302.00030 (local TeX; context only)
- **MOND fits:** "We perform MOND fits assuming (1) the empirical value a0 = 1.2 × 10^-10" (section "Mass models in Milgromian dynamics"). The function is the RAR form.
- **Regime:** the curves are in the Newtonian regime, V²/R > 3–4 a₀.

---

## 8. What is UNVERIFIED

- Helium handling in Genzel+17/20, Price+21, Übler+17, FS+18 (no gas), Amvrosiadis, Rizzo+20, Roman-Oliveira+23, CRISTAL, Danhaive, KURVS, MUSE-DARK I/III and Brouwer+21. None states it.
- The IMF in Amvrosiadis, Danhaive (Prospector), Lelli+21, Rizzo+20 and Parlanti+23.
- KURVS's printed pressure formula.
- Amvrosiadis's published-version α_CO (0.74 ± 0.37), its 11-disc list and ALESS 065.1's class. These were read only through a page-fetch tool's rendering.
- Danhaive's published 37-galaxy gold table.
- Table numbering of the published A&A Parlanti+23 and of Jones+21. arXiv-text labels are used here.
- That Genzel+20's code is DYSMAL. Price+21 says so; Genzel+20 does not name it.
- The quotes from PDF page reads were checked against the pdftotext rendering of the arXiv PDF. Greek letters and exponents may differ typographically from the typeset paper.

## Files

- `AUDIT.md` (this file).
- `a0_kernel_shift_arithmetic.py`, `a0_kernel_shift_arithmetic.out` and `a0_kernel_shift_arithmetic_results.json`: arithmetic only. They read no data and import the programme's committed kernels read-only; the deep-limit control passes.
- Nothing else was written, and nothing was committed or pushed.
