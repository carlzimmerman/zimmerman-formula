# CFG594: the halo-assumptions audit

Date 2026-10-10. Owner question: "are you sure the halos are not just a side effect of ΛCDM assumptions?" Extended by the owner: assume BOTH standard MOND and ΛCDM are wrong, and let neither be a yardstick.

Settings: κ = ½ is FITTED. The footings (9.3603e-11 / 1.1312e-10) are never pooled. The cold energy's MASS is still required, and no particle species is added. This is not "theory closed". Other lanes were read only; no PM runs; no downloads. Quick-check numbers come from `cfg594_sensitivity_results.json`, under criteria committed first (d7fbcc267).

## 0. Short answer (adversarial)

**What is not borrowed: the halo's shape.** The concentration that makes the excess is the law's round phantom of the retained baryons, cut off where the supply runs out (R1/R2/R6). That is framework-derived. Its low-acceleration form is fitted to data (SPARC RAR; the KiDS lensing RAR supports the isothermal tail).

**What is borrowed: how much cold energy each halo holds.** Every lane takes this from ΛCDM-shaped ingredients:
- cold energy clusters exactly like CDM until turnaround (A5, and the PM's single collisionless species);
- the turnaround ball computed in a Planck ΛCDM background (Δ_ta = 11.81);
- the census f_ret, a retained-baryon fraction measured *relative to ΛCDM halo masses*. For a galaxy it fixes the supply at 5.364/0.10 ≈ 54 × M_b.

The halo-model sign flips on the amount alone: the turnaround ball gives +0.72; the r200m ball gives −0.08 (CFG556).

**What labels the excess as a failure is ΛCDM's own P(k).** Every "GROWTH OK / TENSION" verdict is |P/P_S0 − 1| ≤ 0.10 against a ΛCDM dark-matter-only PM run (S0). Under the 10-10 owner rule that is a yardstick, not a verdict. The only raw-data, framework-native test (CFG592 native) is uncommitted:
- It is NOT DIAGNOSTIC for 27 of its 29 runs.
- The two L100 N512 runs go against the framework on the 20 KiDS points it keeps (Δχ² +24 / +30), and only weakly on 38 DES points (+4.2 / +5.6).

**Verdict of this audit.** The halos are not only a side effect of ΛCDM. But their *size*, the *catchment* that sets it, and the *yardstick* that judges it are inherited. On the standard-MOND side:
- If standard MOND's external-field effect were added, it alone would remove the halo-model excess (y_ext = 0.03 → E = −0.002).
- The framework's data-chosen no-EFE rule (R7) is part of why its halos are as concentrated as they are.
- The PM itself uses the standard QUMOND phantom on the whole peculiar field, which is neither round (R6) nor EFE-free (R7). The on-disk core-mass ratio bounds that effect to about 15%.

## 1. Class counts

| class | count |
|---|---|
| DATA-FORCED | 10 |
| FRAMEWORK-DERIVED (incl. 2 marked *posited*, i.e. framework-specific but not derived) | 13 |
| ΛCDM-INHERITED | 17 |
| STANDARD-MOND-INHERITED | 7 |
| CONVENTION / NUMERICAL | 12 |
| **total** | **59** |

## 2. Register

**File keys:**
- PM = `CFG527_law_respecting_engine/cfg527_pm.py`. CFG424/518 engines are its ancestors with the same lines shifted; CFG530 imports it unchanged.
- HM = `CFG556_halo_model_matter_power/cfg556_halo_model.py`.
- LIB557 = `CFG557_settling_catchment_derived/cfg557_lib.py`.

"Verdict lanes" lists the verdicts that move if the item moves.

### 2.1 DATA-FORCED (10)

| id | ingredient | raw data / lane | where it enters |
|---|---|---|---|
| D01 | low-acceleration law shape (the RAR curve) | SPARC RAR. THEORY_v1 A1: ν_simple and ν_standard fail SPARC (CFG468, CFG531) | PM:107-119; HM:53-55 |
| D02 | a0 levels, two footings (κ = ½ FITTED) | RAR/SPARC fits; footing rule | PM:90; HM:47 |
| D03 | cosmic cold amount ω_c = 0.120 (Ω_c/Ω_b = 5.364) | CMB acoustic peaks at z ≈ 1100. CFG511 step-1 table: ω_c measured 0.1190–0.1196 ± 0.0008 | PM:85 (om_c); HM:27; `cfg515_lib.py:17` COLD_PER_B |
| D04 | ω_b = 0.02237, cosmic f_b | CMB/BBN | PM:85-86; HM:28 |
| D05 | cold energy has c_s² ≈ 0 and clusters below the horizon | DESI fσ8, Ly-α forest (CFG508 T1 c_s² ≤ 7e-7; CFG511 S3) | justifies one cold species in PM:248-263 |
| D06 | R6 round settled cold energy, not a phantom disc | MW vertical force K_z, 32/32 cells (CFG514, CFG516) | HM frame_profile:111-180 (spherical); **NOT obeyed by the PM** (see M01) |
| D07 | R7 no external-field effect | cluster satellites (CFG478), Gaia DR3 (CFG447) | HM, CFG557/559 ("no EFE"); **NOT obeyed by the PM** (see M01) |
| D08 | the isothermal phantom tail out to ~Mpc | KiDS lensing RAR = dynamical RAR (CFG511 A07a, LIT) | the edge lies at 0.2–0.4 r_ta (CFG556) |
| D09 | there IS extra gravitating matter in clusters and lenses beyond the law of baryons | cluster lensing / Bullet; CFG508 lensing row (CFG363, CFG502–504) | A4 and G9: cold energy is real mass |
| D10 | survey calibrations: ξ± data, covariance, n(z), m-bias, NLA IA (treated as nuisances) | KiDS-1000, DES Y3 as published | `cfg590_shear.py`, `cfg592_native.py` (data loading); classed as measurement, not cosmology |

### 2.2 FRAMEWORK-DERIVED (13)

| id | ingredient | derivation lane | where it enters |
|---|---|---|---|
| F01 | a0 = κc√(Gρ_DE); a0(z) tracks ρ_DE (A2/A3) | PAPER42; CFG512 | PM:96-105 (FLAT / DE branches); CFG591 ADDENDUM 1 |
| F02 | R1 phantom = settled cold energy, gravitating (G9). Inside the edge only the excess over the local cold density is added. | THEORY_v1 R1 | PM:448 `e = fsw*max(s_ph − s_c, 0)`, :491; HM:111-180 |
| F03 | candidate-B switch: λ₂ ≥ τ = (Δ_ta − 1)/3. For a spherical profile this is exactly the turnaround ball. | CFG557 D1 (\|r_B/r_ta − 1\| ≤ 2.6e-14) | PM:374-378 |
| F04 | R2 supply edge r_e = r_M/ln(1 + f f_b/(1 − f_b)). This is exact point-mass supply exhaustion *for the RAR kernel* (QC M0 reproduces it to 0). | CFG423 / T10 | PM:313-319; HM:136; `cfg515_lib.py:58-60` |
| F05 | R3 per-catchment mass conservation | CFG424; MUTATE gives +15% clumping | PM:448-491 |
| F06 | R5 draw from the shell between the edge and r_ta | CFG527 (core R 0.94–0.98) | PM:458 |
| F07 | R4 the phantom is sourced by retained baryons f_ret(x)(1 + δ) (the rule; the f_ret *values* are L06) | CFG518 | PM:410-416 |
| F08 | R8 shared supply for overlapping catchments | CFG522 | LG timing tests |
| F09 | gravitating-field statistic δ_grav = −k²φ/(1.5Ω_m) | CFG555 (the correct framework field; PAPER45's particle-field claim FAILS) | `cfg555_compute.py:130-133` |
| F10 | free-fall ceiling on the settled supply s_c,∞ (α-free); a derived UPPER bound | CFG557 | LIB557:156-200 (the dynamics under it are L10) |
| F11 | cold-energy equation of motion, class A (metriplectic), α O(1) FREE | CFG539/541/542 | not in the verdict engines (bookkeeping is used instead) |
| F12 *posited* | FIX-2 kinetic closure (isotropic Jeans OU): POSITED, not derived | CFG544, CFG554 | CFG559 toy (kinetic profile) |
| F13 *posited* | A6 supply postulate: each system settles the cosmic share of its original baryons. Six derivations failed (THEORY_v1 A6). Its *amount* is realised through L04/L05/L06. | THEORY_v1 | HM:117; PM catchments |

F01 and F03 contain fitted or inherited numbers (κ; Δ_ta). Those numbers are listed under their own classes.

### 2.3 ΛCDM-INHERITED (17), each with (a) where, (b) verdicts, (c) bias, (d) native replacement, (e) quick check

**L01 Linear initial spectrum.** Eisenstein–Hu no-wiggle, n_s 0.965, σ8 = 0.811 (Planck-ΛCDM derived), Zel'dovich at z_i = 49, D(a) from GR + Λ.
- (a) PM:85-87, 121-139, 248-263, ZI at :92; HM:27-43; LIB557:28-41; `cfg592_native.py:31-43`. Flagged as "the ONLY ΛCDM input" in `CFG359_native_pm_growth/FROZEN_CRITERIA.md:60-63`.
- (b) Every PM verdict (CFG424/425/518/527/530/555, CFG592 native) and every halo-model number (CFG556/557/559/590/591/593).
- (c) It enters the framework and S0 identically, so ratio verdicts are insensitive at first order. Absolute shear (CFG590/592) is directly sensitive: the data prefer lower amplitude, and ΛCDM-DMO alone has A = 1 against 0.86 (CFG590). A lower amplitude would lower both models and leave the framework − S0 Δχ² roughly in place.
- (d) Partly native already. The record's justification is that candidate B equals ΛCDM linearly because the switch is off on linear modes (CFG324, CFG354), and ω_c and ω_b are CMB-measured (D03/D04). What is NOT native: σ8 = 0.811 and h come from a ΛCDM fit to the CMB. Replacement: fit A_s, h and Ω_m within the framework (switch off at z > z_i) to the CMB and BAO directly, then regenerate ICs. Specifiable; not run.
- (e) QC L5 (σ8 0.811 → 0.76): MINOR, ΔE = +0.023 (canonical) / +0.006 (alt).

**L02 Background expansion.** Flat GR + Λ, w = −1, h = 0.6736, Ω_m = 0.315.
- (a) PM:85-94 (the DE branch at :91 changes a0(z) only, not H(z)); HM:27-28; LIB557:65-77; CAMB in `cfg590_shear.py`, `cfg592_like.py:28-43`.
- (b) All PM and halo-model lanes; Δ_ta (L03); CFG557 ages; LG timing.
- (c) Small for growth ratios. CFG508: a0 tracking ρ_DE vs flat gives Δσ8 ≤ 0.0006. Larger for absolute ages and for the epoch (CFG557 finite-age ceiling).
- (d) PM with the DESI w0wa background *and* a0 tracking. Only CFG591 ADDENDUM 1 (halo model) and CFG592 native (distances only) do this. Specifiable; a PM rerun is needed.
- (e) No quick check.

**L03 Turnaround density Δ_ta = 11.81.** Spherical top-hat shell ODE in the ΛCDM background, with no law and no phantom.
- (a) PM:142-171 (the switch threshold at :374-378, the halo finder at :327, :341, M_ta at :310-311); HM:50; `cfg591_lib.py:45-49`.
- (b) The switch region, catchments, M_ta and the edge cap in every lane.
- (c) Mixed. A lower Δ_ta means a larger catchment, so more supply and more excess.
- (d) Under candidate B the law is off before turnaround. The pre-turnaround shell is then Newtonian + dust cold energy + Λ, so **this ODE IS the framework's own spherical collapse, given L02.** It is ΛCDM-inherited in form and framework-consistent in content. The residual native correction is a secondary-infall model in which interior shells carry their settled cold energy (mass-conserving, so the outer shells see the same mass) and the w0wa background is used. Specifiable.
- (e) QC L6/L7 (× 0.8 / × 1.2): MODERATE, ΔE +0.106 / −0.085 (canonical) and +0.119 / −0.095 (alt).

**L04 "Cold energy = collisionless CDM outside bound systems".** The PM has a single species carrying all of Ω_m. Cold particles stay where ΛCDM-like dynamics put them; the settled part is bookkeeping (e − comp).
- (a) PM:248-263 (one species), :435 `s_c = 1.5Ω_m(1 − f_b)(1 + δ)/a`; THEORY_v1 A5; HM builds the framework halo from the NFW mass M_ta (HM:79-84, 117).
- (b) Every catchment, so every growth, lensing and halo-model verdict.
- (c) **Sign-setting**, through the supply amount (L05). The bookkeeping itself is not the driver: CFG539's moving cold species (EoM A) gives the same gravitating excess (0.347 vs 0.336 canonical; 0.381 vs 0.388 alt; `CFG539…/README.md:15-21`).
- (d) The framework postulates exactly this (A5), and D05 bounds it by data (c_s² ≈ 0). There is no framework-native alternative clustering law on record. The native test is a two-species PM in which the cold species obeys the framework's own settling dynamics and the settled amount is *measured*. CFG539 attempted this; class A has α free and fails T1/T4. Open.
- (e) Already on disk: the CFG539 comparison above.

**L05 Supply amount = (1 − f_b) M_ta, the whole turnaround ball.**
- (a) HM:117 `supply = (1 - FB) * Mta`; `cfg515_lib.py:9-10`; PM catchments `in_cover(…, x = 1)` at PM:383, :391.
- (b) CFG556 INTRINSIC; CFG557/559 growth and KiDS FAIL; CFG590 EXCLUDED; CFG593.
- (c) The largest. The turnaround ball gives E +0.715 / +0.883. The r200m ball gives −0.000 / −0.081 (CFG556). The α-free finite-age ceiling gives +0.382 / +0.458 (CFG557).
- (d) Settled amount from the framework's own dynamics, not from the ΛCDM ball:
  - (i) measure, in the existing PM snapshots (z = 1, 0.5, 0), how much cold mass has actually entered each host's census edge;
  - (ii) the two-species run of L04.
- (e) QC L11/L12 (× 0.5 / × 0.75): DRIVER / MODERATE (ΔE −0.371 / −0.191 canonical, −0.458 / −0.238 alt). It does not reach the 10% cut at × 0.5.

**L06 Census f_ret(M_ta).** The numerator is observed baryons; the denominator f_b M_ta uses a *ΛCDM* halo mass. Values: 0.10 below 10^12.5, 0.55 at 10^13.5, capped at 0.90.
- (a) PM:302-308; HM:87-92; `cfg515_lib.py:20-40`; the declaration is in `CFG416…/FROZEN_CRITERIA.md:7-11` ("from the census and group/cluster baryon fractions").
- (b) The retained-baryon source and edge in CFG518/527/530; CFG556–559; KiDS f30 (CFG529/557/559); groups; MW; LG.
- (c) Large and sign-relevant. Lower f_ret pushes the edge out and makes the halo less concentrated. For a galaxy the supply is 54 M_b, i.e. the ΛCDM abundance-matched halo.
- (d) Measure each system's catchment mass from its own data, not from abundance matching: the Hubble-flow zero-velocity surface (CFG548 does this for the LG), or the weak-lensing profile beyond r_e. Then f_ret = observed baryons / (f_b × that mass). Not needed inside the PM, where baryons are not depleted.
- (e) QC L9/L10 (× 0.5 / × 2): DRIVER. At × 0.5 canonical E = +0.063 (CUT) and alt +0.188. At × 2: +0.165 / +0.163.

**L07 Moster13 SHMR.**
- (a) In the halo model it sets only the star/gas split: HM:93-96, used at :97-106. In the KiDS harness it sets the lens M_ta: `CFG529…/cfg529_tables.py:47, 61` (Moster and Behroozi).
- (b) CFG556 profiles (weakly); KiDS f30 tests (strongly, through the supply).
- (c) Halo model: none (QC). KiDS: sets the supply per lens, the same direction as L06.
- (d) As L06: catchment mass from data.
- (e) QC L3/L4 (M* × 0.5 / × 2): MINOR, \|ΔE\| ≤ 0.001 in the halo model. The KiDS-side sensitivity was NOT checked here (a ~5-min harness; left for a lane).

**L08 NFW + Duffy08 c(M).** Used as (i) the ΛCDM reference profile in R = P_F/P_L; (ii) the shape that defines r_ta and M_ta (NFW extended to Δ_ta); (iii) the shell profile outside r_e.
- (a) HM:76-84, 159-180; inherited by `cfg557_tests.py`, `cfg559_*`, `cfg591_lib.py:79-99`, `cfg593_lib.py:81`.
- (b) Every halo-model R(k), so CFG590/591 shear through R.
- (c) Mostly yardstick: a lower ΛCDM concentration gives larger R.
- (d) Drop the halo-model reference. Compare the framework's own P(k) or ξ± with raw data (CFG592 native). Take r_ta and the shell shape from the PM's own infall profiles.
- (e) QC L1/L2 (c × 0.7 / × 1.3): DRIVER / MODERATE (ΔE +0.281 / −0.153 canonical, +0.325 / −0.176 alt). The magnitude of the "excess" is therefore not robust to the ΛCDM yardstick chosen. Neither direction removes it.

**L09 Tinker08 mass function + Tinker10 bias.**
- (a) HM:57-73.
- (b) Halo-model weights in CFG556–559, 590, 591.
- (c) Small.
- (d) The PM's own n(M_ta) from `in_cover` turnaround balls.
- (e) QC L8 (Press–Schechter + Mo–White): MINOR (+0.036 / +0.008).

**L10 EPS main-progenitor histories + ΛCDM shell trajectories.** Neistein+06 form, q = 2.2, recalled and PROVISIONAL; the trajectories set t_reach.
- (a) LIB557:8-9, 78-100, 140-152.
- (b) CFG557 s_c,∞ (0.50–0.80); CFG559 s_c*; the CFG590 primary R input; CFG591.
- (c) It sets the settled fraction, so roughly half of the excess.
- (d) Accretion histories of the PM's own turnaround balls across its snapshots.
- (e) No quick check (needs halo matching across PM snapshots).

**L11 S0 (ΛCDM dark-matter-only PM) used as the YARDSTICK.** The CFG361 growth cut: \|P/P_S0 − 1\| ≤ 0.10 (k ≤ 1) and σ8 within 5%.
- (a) `CFG530…/cfg530_analysis.py:197`; same rule in cfg424/518/527 analyses; CFG556 growth (i); CFG557/559 test (i).
- (b) Every GROWTH OK / TENSION label, including the CFG555 finding that PAPER45's claim FAILS at 512³.
- (c) Two-sided. Measured against raw shear, ΛCDM-DMO is itself already above the data (A = 1 vs 0.86, CFG590). Against data, the framework's +16–19% over S0 at 512³ is therefore more of a problem, not less, unless the framework's baryonic physics suppresses more.
- (d) S0 stays as the same-pipeline comparison model; the verdict must be framework vs raw ξ± or fσ8 (CFG592 native). It is uncommitted and limited by resolution:
  - 27 of its 29 runs are NOT DIAGNOSTIC (k ≤ k_Nyq/4).
  - The two L100 N512 CFG530 runs keep 20 KiDS points (Δχ² +23.9 / +30.0) and 38 DES points (+4.2 / +5.6).
  - The native replacement is therefore a higher-resolution or zoom PM reaching k ≈ 5–10 h/Mpc.
- (e) Read only from CFG590 and CFG592 outputs.

**L12 HMcode-2020 DMO P_NL × BAHAMAS feedback S_fb.**
- (a) `cfg590_shear.py:61-62`; `cfg592_like.py:42, 59-67`; `cfg592_de.py:50`; `cfg591_shear.py:33`.
- (b) CFG590 EXCLUDED; CFG591/592 PART A (already downgraded to context, b5cf2ade2).
- (c) It multiplies the framework's R onto a ΛCDM non-linear spectrum with ΛCDM-calibrated feedback.
- (d) CFG592 native, plus a framework baryon/feedback model (none exists).
- (e) None.

**L13 A_mod form P = P_L + A(P_NL − P_L).**
- (a) CFG590 README method; `cfg590_shear.py`.
- (b) CFG590 Z values.
- (c) It amplifies R − 1, since A − 1 ≈ (R − 1) P_NL/(P_NL − P_L) (CFG590).
- (d) Direct ξ± likelihood (CFG592 native).
- (e) None.

**L14 KiDS lensing harness.** DK14 transition, halofit × ζ two-halo, stripping.
- (a) `CFG529…/cfg529_score.py:3`, :470-471.
- (b) KiDS f30 FAIL in CFG557/559 (and CFG515/531/585 lineage).
- (c) Unknown sign. The 2-halo term is "NOT CROSS-CHECKED BY PM" (cfg529:471).
- (d) The PM's own galaxy–matter cross-spectrum for the 2-halo term, or restrict to 1-halo radii.
- (e) None.

**L15 Epoch evolution of ΛCDM fits.** Duffy (1+z)^−1.01, Tinker z-evolution, Moster z-evolution.
- (a) `cfg591_lib.py:4-5, 66-99` (uncommitted lane).
- (b) CFG591 shear z-dependence.
- (c) As L08/L09 per epoch.
- (d) PM snapshots at z = 1 and 0.5.
- (e) None.

**L16 Planck-like CAMB distances and growth in the shear projection.**
- (a) `cfg592_like.py:28-43`; `cfg592_native.py:52-71` (DESI variant present).
- (b) CFG590/592.
- (c) Small (the native DESI variant moves KiDS Δχ² +23.9 → +18.1).
- (d) Framework background (L02).
- (e) Read from CFG592.

**L17 r_ta and IC-B "cold infall from r_ta" in the kinetic toy.** Taken from the NFW-extended halo.
- (a) `CFG559…/cfg559_toy.py:55-61`.
- (b) CFG559 profile; CFG590 primary.
- (c) As L08 and L03.
- (d) PM infall profiles.
- (e) None.

### 2.4 STANDARD-MOND-INHERITED (7)

**M01 The QUMOND phantom on the global peculiar baryon field.** ρ_ph = −∇·[(ν − 1) g_b]/4πG. It is non-round, and its |g_b| contains neighbours' fields, i.e. an EFE.
- (a) PM:421-434. Named an open item in `CFG541…/EQUATIONS.md:91` and `:227` ("The PM uses the global QUMOND phantom. The round per-region phantom (E7) is what R6/R7 require").
- (b) Every PM verdict (CFG424–530, 555, CFG592 native).
- (c) The EFE part lowers ν, so less phantom and the excess is understated. The negative-phantom lobes are clipped by max(·, 0) at PM:448, a positive bias. The two partly cancel.
- (d) A round per-region phantom from the enclosed retained baryons of each B region (EQUATIONS E7). Specifiable.
- (e) On disk, with no new compute: the CFG526 statistic R = M_grav(PM)/M_law(round, isolated) (`CFG526…/cfg526_profiles.py:226-239`) is 0.94–0.98 at 256³ (CFG527) and 1.04–1.14 at N512 (CFG530). **The QUMOND/EFE departure from R6/R7 is bounded to about 15% in halo mass. It is not the driver.**

**M02 The kernel reads the local |g_b| alone, in comoving peculiar fields (the Hubble flow subtracted).** This is the standard cosmological-MOND N-body convention.
- (a) PM:424.
- (b) PM verdicts.
- (c) Unknown, and limited by the switch (B regions only).
- (d) Same as M01: the round per-region rule on the region's own baryons makes the choice moot.
- (e) None.

**M03 The kernel's low-y form is an empirical fit (McGaugh+16 RAR) extrapolated to groups, clusters and Mpc edges.** ν_mono's monotonic high-y tail is the framework's own.
- (a) PM:107-119 (ν_mono); HM:53-55 (plain RAR without the monotone tail, a small inconsistency that only acts at y > y_p).
- (b) The edge, profiles and all verdicts.
- (c) Moderate.
- (d) Data-forced for discs (D01). For groups and clusters it is the group-BFJR (Tian+26) and lensing-RAR data that must decide.
- (e) QC M1 (ν_simple): MINOR, +0.002. QC M2 (ν_standard): MODERATE, −0.138 / −0.136. Both are SPARC-disfavoured (A1).

**M04 Deep-MOND asymptotics used as derivation shortcuts.**
- The edge is the point-mass deep-regime isothermal phantom; at f_ret ≈ 0.1, r_e ≈ r_M(1 − f_b)/(f f_b).
- V_f = (G M_b a0)^¼ in the kinetic toy (`cfg559_toy.py:58`).
- σ⁴ = G M_b a0/4 (CFG539 class B) and T = V_f²/2 (CFG550 SIS).
- r_M = √(G M_b/a0) (PM:318; HM:118).
- (b) The edge in every lane; the kinetic profile (CFG544/550/554/559).
- (c) Point-mass vs extended baryons: small (HM uses the point-mass edge with an extended profile).
- (d) Numerical supply exhaustion on the real enclosed baryon profile. QC M0 shows the point-mass closed form is exact for the RAR kernel; the extended-baryon version is specifiable.
- No σ⁴ = (4/81) G M a0 shortcut appears in the audited lanes (grep).

**M05 The EFE question.** The framework says none (R7, D07); standard MOND says yes.
- (a) HM and CFG557/559 have none, consistent with R7. The PM has a partial EFE through M01.
- (b) Halo-model excess and KiDS.
- (c) **Decisive in the halo model.** With a standard-MOND EFE the phantom saturates at (ν(y_ext) − 1) M_b, which for galaxies is far below the 54 M_b supply. The edge then never forms and the halo is NOT concentrated.
- (d) Not a replacement: R7 is data-chosen. Keeping no-EFE is what makes the halos concentrated, so the framework's halo excess depends on the framework rejecting standard MOND's EFE.
- (e) QC M3 (y_ext 0.01): MODERATE, −0.105 / −0.103; galaxy-scale halos (log M_ta ≤ 13) are capped at r_ta. QC M4 (y_ext 0.03): DRIVER and CUT on both footings, E −0.002 / −0.002, R(1) 0.41.

**M06 r_M and the "MOND radius" scale.** Folded into M04 for the edge and listed separately because it is where a0 enters the supply edge.
- (a) PM:313-319.
- (b), (c), (d): as M04.
- (e) None.

**M07 "Standard MOND predicts X" yardsticks.** None is used as a verdict yardstick in the audited lanes (grep of all audited READMEs). The only "phantom = extra gravity" construction is the MUTATE no-compensation control (CFG424 0.154, CFG518 0.139, CFG527 MUTATE B 0.213). It is used correctly, as a tooth, not as a yardstick.

### 2.5 CONVENTION / NUMERICAL (12)

| id | item | where | note |
|---|---|---|---|
| C01 | box L (200, 100, 50, 25), mesh 256/512, NSEED, seed 359 | PM:92 | CFG530: P(k) converges at fixed box; core R does not (canonical) |
| C02 | resolved-host cut RMIN = 1.56 Mpc/h | PM:80, :344 | **the PM's hosts are groups and clusters only**; the f_ret ≈ 0.10 galaxy regime is untested in the PM (CFG518 README) |
| C03 | switch width ε = 0.077; peak threshold 3(τ − ε) | PM:93, :327, :378 | CFG427 E1/E2: ε insensitive |
| C04 | MIX-A gas pressure filter | PM:81, :398-409 | replaced by NOFILT in CFG527/530 |
| C05 | cover recomputed every 10 force calls | PM:380-384 | — |
| C06 | 150 KDK steps | PM:265-271 | — |
| C07 | CIC / mesh softening; P(k) cut k ≤ 1 | PM:541; analyses | — |
| C08 | halo-model grids (mass 1e8–1e16, NR 1600, k 1e-3–10) | HM:57, 106-109, 194 | C4 control 1e-3 |
| C09 | cap e/q when q > 1 | PM:461-466 | never acted |
| C10 | sharp vs softened edges (s25 / s55) | HM:140-176 | declared variants |
| C11 | declared baryon shapes: Hernquist stars, β-model gas | HM:97-106 | the emergent-edge variant is very sensitive to the outer gas (CFG556) |
| C12 | CFG592 native support cut k ≤ k_Nyq/4 | `cfg592_native.py:250-304` | makes most runs NOT DIAGNOSTIC |

## 3. Quick check: what moves the halo-model excess (context statistic; criteria d7fbcc267)

E = max(R − 1) over 0.05 ≤ k ≤ 1. CFG556 base values: +0.715 (canonical) / +0.883 (alt). All controls pass (C0 and C2 to 0; C1 to 0; C3 ≤ 3e-16); MUTATE MU1 and MU2 bite.

| item (variants) | class, canonical / alt | max \|ΔE\| | a variant reaching the 10% cut on both footings? |
|---|---|---|---|
| census f_ret (× 0.5 / × 2) | DRIVER / DRIVER | 0.652 / 0.695 | no (× 0.5 cuts canonical only: +0.063) |
| EFE, standard MOND (y_ext 0.01 / 0.03) | DRIVER / DRIVER | 0.717 / 0.885 | **YES** (y_ext 0.03) |
| supply amount (× 0.5 / × 0.75) | DRIVER / DRIVER | 0.371 / 0.458 | no |
| c(M), the ΛCDM reference (× 0.7 / × 1.3) | DRIVER / DRIVER | 0.281 / 0.325 | no |
| kernel low-y form (simple / standard) | MODERATE / MODERATE | 0.138 / 0.136 | no |
| Δ_ta (× 0.8 / × 1.2) | MODERATE / MODERATE | 0.106 / 0.119 | no |
| mass function + bias (Press–Schechter) | MINOR | 0.036 / 0.008 | no |
| σ8 / IC amplitude (0.76) | MINOR | 0.023 / 0.006 | no |
| SHMR, star/gas split (× 0.5 / × 2) | MINOR | 0.001 / 0.001 | no |

What the halo model's excess responds to, in order:
1. how much cold energy a halo holds (f_ret, supply);
2. whether standard MOND's EFE is allowed;
3. which ΛCDM concentration is used as the reference.

It is insensitive to the ΛCDM mass function, the IC amplitude and the SHMR split.

**Disclosure.** The first execution had a sign error in the numerical-edge fallback: "supply never exhausted" returned a tiny radius instead of r_ta. It affected only M3/M4 (C1 still passed, because the RAR edge always exists). It was fixed before anything was committed, and the reported M3/M4 rows are from the corrected run.

## 4. Ranked: inherited items most likely to be driving the growth/lensing excess, with the framework-native test that removes each

1. **The catchment supply, sized by ΛCDM-like clustering (L04 + L05, realising A6 through L03).**
   - Effect: sign-setting. The turnaround ball gives +0.72 / +0.88, the r200m ball −0.08 (CFG556); QC × 0.5 gives DRIVER.
   - *Native test:* measure the settled amount instead of assigning it. In the existing CFG530 PM snapshots (z = 1, 0.5, 0), track the cold particles that have actually crossed into each host's census edge and use that as the supply. Then the two-species PM with the framework's own settling law (L04 d) once α is fixed.
2. **Census f_ret and SHMR lens masses, relative to ΛCDM halos (L06, L07 on the KiDS side).**
   - Effect: DRIVER; × 0.5 reaches the cut on canonical.
   - *Native test:* catchment mass per system from its own data. Use Hubble-flow zero-velocity surfaces (CFG548's method) for groups and the LG, and the weak-lensing profile beyond r_e for KiDS lenses. Re-score KiDS f30 and groups with no abundance matching.
3. **The S0 / ΛCDM P(k) yardstick (L11), with HMcode/BAHAMAS/A_mod in the shear lanes (L12/L13).**
   - Effect: this is what turns the PM's +16–19% (512³, CFG555) into "TENSION".
   - *Native test:* CFG592 native at a resolution that keeps most ξ± points: a zoom or higher-resolution PM reaching k ≈ 5–10 h/Mpc, so that k_Nyq/4 covers the data. Report framework vs raw ξ± with S0 as the same-pipeline comparison only.
4. **The NFW/Duffy reference, and M_ta and the shell taken from NFW (L08).**
   - Effect: DRIVER on the magnitude of the halo-model excess, but not its sign.
   - *Native test:* retire the halo model from any verdict (already done by the owner rule). Take r_ta, M_ta and the shell profile from PM infall profiles.
5. **Standard-MOND side: the PM's QUMOND phantom + implicit EFE (M01), and the EFE choice itself (M05).**
   - Effect: M01 is bounded to about 15% by core R and is not the driver. M05 is decisive in the halo model, but R7 is data-chosen.
   - *Native test:* run the PM with the round per-region phantom (EQUATIONS E7), so that it obeys R6/R7 exactly. Expect the excess to stay or grow slightly, since core R 0.94–0.98 moves to 1. Separately, keep R7 under test with data (Gaia DR4 wide binaries, PAPER35; cluster satellites). If R7 fell, the concentrated halos would go with it.

Also moderate: Δ_ta (L03, framework-consistent under B), EPS histories (L10), and the kernel's low-y form (M03).

## 5. What this audit does NOT say

- It does not say the excess is an artefact. The most native PM evidence (CFG555 gravitating field at 512³; CFG530 core R at about 1) shows the framework's halos are more concentrated than ΛCDM's at the same initial field. That uses no halo-model ingredient, only L01/L02 (identical in both runs), the M01 phantom, and the L11 yardstick.
- It does not say the data favour the framework.
- κ is fitted. The cold energy's mass is still required. The supply (A6) and the switch remain inputs. This is not "theory closed".
