# CFG314: DES / DESI / JWST scoping. Where is the crispiest next step?

> **Scoping only.** Nothing was downloaded. What was read: arXiv abstract and HTML pages, DESI directory index pages (names and sizes only), a GitHub landing page, the record's committed files, and the data already on disk. κ = ½ is FITTED. FLAT a₀(z) is the framework's distinctive law, a₀ ∝ H(z) is the rival, and ΛCDM has no a₀. The cold component is still required, and no particle is added. No sentence here says the data favour a law. "Crispy" was checked as hard as "not possible": every power number comes from `cfg314_power.py`, whose stated assumptions are bracketed.

Owner request: "what is the crispiest next step for DES or DESI or JWST that has real crispy data that maybe the scientists didnt chop or use the right way or used certain assumptions.. investigate rigorously!"

## Bottom line
1. **The crispiest step tests B's one specific failure, not a₀(z).** It replicates the KiDS early/late lensing split (B-specific, 4.4σ; CFG88/95/96) with **DESI DR1 spectroscopic lenses** and three independent shear surveys (DES Y3, KiDS-1000, HSC Y3).
   - **The KiDS analysis used ΛCDM in exactly the step a jackknife cannot see.** Its photo-z isolation was validated on MICE, a ΛCDM simulation with HOD and abundance matching, at about 80% purity (Brouwer+21).
   - **The published record is in conflict.** Mistele & McGaugh (JCAP 04 (2024) 020) report that early and late types lie on one RAR "when a sufficiently strict isolation criterion is adopted", using a GAMA spectroscopic subsample. The record's CFG96 finds the split persisting at 4.1σ under twice-stricter photo-z isolation.
   - **DESI resolves this.** It gives 8–20× the 13,957 GAMA spectroscopic lenses (116k–275k isolated lenses, P1) in the shear overlaps (1,447 deg²).
   - **Power:** B against the split is 3.6–5.6σ with all three surveys. Without HSC (which needs an account, so it is the owner's step) it is 2.3–3.6σ, and 1.5–2.3σ with CFG108's ×1.58 covariance. My own pre-written check P1b FAILED: without HSC, the worst cell does not reach 2σ.
2. **The cheapest step uses data the cosmologists measured and then cut.** DESI DR1's galaxy–galaxy lensing ΔΣ is measured from 0.08 to 80 h⁻¹ Mpc (Heydenreich+25, arXiv:2506.21677; public on GitHub, MIT). The cosmology fits threw away everything below 2.5–6 h⁻¹ Mpc (arXiv:2512.15962, 2512.15960). That cut removes the whole galaxy-scale (1-halo) regime.
   - The authors report "excess scatter, driven primarily by small-scale measurements of r ≤ 1 Mpc/h" between the shear surveys.
   - That scatter is an empirical measure of the systematic the KiDS split was said to be "fragile only to". It tells us whether the ×1.58 covariance inflation (CFG108) is real.
3. **a₀(z): no DES, DESI or JWST product beats the calibration wall today.**
   - Lensing BGS→LRG: the rival shift is +0.072 dex. The M★ drift must stay ≤ 0.048 dex across z, and the hot-gas difference can be 0.05–0.15 dex.
   - JWST z ≈ 4 discs: at the record's operating point FLAT and the rival differ by only 0.25 dex in the baryons they require. So 3σ needs a shared calibration of 0.084 dex, against scaling-relation gas of about 0.3 dex. Deep discs open the separation to 0.55–0.72 dex.
   - DESI PV Tully–Fisher: the rival's lever is 0.015 dex in a₀ across its whole range.
   - COSMOS-Web lensing: 0.45σ.
   - So the answer to "a₀ at z ≈ 2.5" stays where PAPER38 put it.
4. **Two findings along the way:**
   - **The KiDS-1000 shear catalogue on disk is TRUNCATED.** `_external_data/kids_lensing_zsplit/KiDS_DR4.1_ugriZYJHKs_SOM_gold_WL_cat.fits` is 7,154,622,464 B against the 17,711,426,880 B its header implies (21,262,011 rows × 833 B), i.e. 40.4%, and `curl_shear.log` is empty. The record's KiDS lanes used the staged June per-lens sums, not this file, so no committed number is affected. Any new lane that reads it must first finish the download (10.56 GB more, the owner's go).
   - **The record's "collapse timing 1.34–1.96×" row (THE_COMPLETION v9, `nbody_2026/stage26_*`) cannot be used for JWST.** Its own text calls it an upper bound that "runs down toward ~1 if the dust dominates", and under B the cold component does dominate. Its "speedup declines with z" uses a declining a₀(z), which is not the standing flat law (Branch A, CFG6).

## Ranked table

| rank | dataset | framework question | power (`cfg314_power.out`) | dominant systematic | ΛCDM / model assumptions found | on disk / download | verdict |
|---|---|---|---|---|---|---|---|
| 1 | DESI DR1 BGS spec-z isolated lenses × DES Y3 + KiDS-1000 + HSC Y3 shear | B's KiDS early/late split (B-specific 4.4σ), which is also the massive-elliptical excess (SLUGGS) in lensing form | B vs split: **3.6–5.6σ** (all three); 2.3–3.6σ without HSC; ×1.58 covariance 2.3–3.5σ / 1.5–2.3σ | class-dependent baryons (hot gas, ETG M/L: Mistele's Q = 1.4, i.e. 0.15 dex) are shared with KiDS and not cured by DESI; the isolation purity IS cured | KiDS isolation purity ~80%, validated on MICE (ΛCDM HOD + abundance matching); photo-z 3-D isolation (σ_z ≈ 0.026); LePhare M★ | KiDS bright + LePhare on disk; KiDS shear on disk but truncated (10.56 GB to finish); DESI BGS full catalogue 5.19 GB; CIGALE M★ 7.32 GB; DES Y3 shapes (size not verified); HSC Y3 needs an account | **CRISPY** (with HSC or the upper isolation bracket); MARGINAL on public shear alone |
| 2 | DESI DR1 ΔΣ data vectors 0.08–80 h⁻¹ Mpc, BGS 0.1–0.4 and LRG 0.4–1.1, four shear surveys (Heydenreich+25) | the size of the cross-survey small-scale systematic, i.e. whether CFG108's ×1.58 is real | not a law test; it calibrates rank 1's error budget | not isolated, no M★, so it cannot give a RAR by itself | the cosmology analyses cut below 2.5–6 h⁻¹ Mpc and model with AbacusSummit + HOD with assembly bias | GitHub repo (MIT; size not verified) | **MARGINAL (enabling; cheapest first step)** |
| 3 | JWST NIRCam grism z ≈ 4–6 discs (Danhaive+25 gold, arXiv:2503.21863; the 163-galaxy follow-up, arXiv:2510.14779) plus MEASURED gas | FLAT vs a₀ ∝ H(z) at the largest lever available (the rival is ×6.65 at z = 4.17) | baryons required: median disc +0.25 dex (needs ≤ 0.084 dex shared calibration); deep discs (y★ ≤ 0.3) +0.55–0.72 dex (needs ≤ 0.18–0.24); CFG273's 95% upper bounds exclude nothing (0 of 6) | gas (f_gas ≈ 0.77 from scaling relations), the pressure term 3.36σ₀², Prospector M★ (IMF unstated, outshining) | M_dyn from a thin-disc v/σ₀ model (not NFW, good); gas from scaling relations calibrated at z ≲ 4 | Danhaive v1 table on disk (CFG273); gas needs NOEMA (GOODS-N is beyond ALMA's +47°) | **MARGINAL**: NOT POSSIBLE with scaling gas; possible only for a measured-gas deep subset |
| 4 | DESI LRG (z 0.4–1.1) vs BGS (z ~0.25) isolated lenses × HSC/DES | lensing a₀(z), FLAT vs H(z) | rival +0.072 dex in the deep amplitude; stat ≈ 0.6σ (isolated LRGs, stated assumptions); needs M★ drift ≤ 0.048 dex | M★ drift (mimics a₀ drift by δ/2, CFG255); hot gas of LRGs 0.05–0.15 dex in amplitude | LRGs are group centrals (ownership and hot gas); SPS method-to-method 0.2 dex | as rank 1 plus the LRG catalogues | **NOT POSSIBLE (DR1)**; MARGINAL with DR2+ and a demonstrated M★ drift |
| 5 | DES Y6 cosmic shear / 3×2pt (S₈ = 0.789 ± 0.012; shear-only 0.783; arXiv:2601.14559, 2602.10065) | the framework's small-scale power boost R(k ~ 1) ≈ 1.05 (canonical) / 1.12 (alt) (CFG1 A18, CFG6 §6: a halo-model lever estimate) | no committed framework P(k); R sits inside the 10–30% baryon-feedback range | baryon feedback (degenerate in sign and size) | ΛCDM nonlinear P(k) emulators, feedback marginalisation or scale cuts, IA models | the DES Y6 release (not sized) | **NOT POSSIBLE** until the framework commits a P(k) |
| 6 | DESI DR1 PV Tully–Fisher, 10,262 galaxies, 0.03 < z < 0.10 (arXiv:2512.03227) | TF zero point vs z (a₀ drift) | rival 0.0063 dex in a₀ between halves (0.015 over the full range), i.e. 0.011–0.016 mag; stat 0.009 mag | luminosity evolution ±0.014 mag between halves; K-corrections; Malmquist; no gas (r-band TF, not BTFR); V at 0.4 R₂₆, not V_flat | a free intercept per redshift bin, set by "no average radial peculiar velocity", which absorbs any z-dependent zero point by construction; fiducial flat ΛCDM (Ω_M 0.3151) for magnitudes; zero point from SH0ES/Pantheon+ | Zenodo "upon acceptance" | **NOT POSSIBLE** |
| 7 | DESI DR2 BAO + w0wa chains (arXiv:2503.14738) | κ footing; a₀(z) under the √ρ_DE branch | the four fits move the predicted local a₀ by −0.038 to +0.002 dex against the ~0.16-dex spread in the measured local a₀ (CFG309); a₀(2.5) −0.085 to −0.141 dex (CPL, already the chart's band) | the local a₀ calibration, not BAO | fiducial-cosmology templates (shown robust by DESI); the framework's background is ΛCDM/w0wa, so nothing is hidden | chains on disk (328 MB) | **NOT POSSIBLE** (no lever on κ; a₀(z) already charted) |
| 8 | COSMOS-Web lensing (0.54 deg², 129 shapes arcmin⁻²) + COSMOS2025 M★ | a₀ at z ~ 1 from galaxy–galaxy lensing | σ_A ≈ 0.28 dex vs the rival's +0.126 dex: 0.45σ | statistics (one field), M★ calibration | photo-z and SED M★ | not sized; shear catalogue release status unverified | **NOT POSSIBLE** |
| 9 | JWST "too massive too early" abundances | collapse timing | no native halo mass function (Gap 2); the stage-26 speedup is an upper bound → ~1 with a dominant cold component, and its z-decline uses a non-standing a₀(z) | M★ (IMF, AGN/LRD contamination) | ΛCDM HMF in every published comparison | n/a | **NOT POSSIBLE** |
| 10 | DES-discovered MW satellites + DESI DR1 MWS radial velocities | the ultra-faint liability (3.5–3.9σ) | DESI floor 1–2 km/s = 0.5–1.0 of a 2 km/s UFD dispersion; Keck/DEIMOS (1.1 km/s) is already in the record's inputs | binaries; floor | n/a | 3.3 GB of MWS RVTAB on disk, but only for wide-binary pixels | **NOT POSSIBLE** |
| 11 | DESI DR1 Fundamental Plane (PV) | the SLUGGS ellipticals | central-fibre σ is in the Newtonian regime (g ≫ a₀) | aperture | FP distances | n/a | **NOT POSSIBLE** (rank 1 is the lensing route to the same physics) |

## 1. DESI spec-z isolated lenses × DES / KiDS / HSC: the early/late split (rank 1)
**Data products.**
- **DESI DR1** (public): BGS density 854 deg⁻², over 5.5 M reliable redshifts, 7,500 deg² (DR1 paper, AJ, doi:10.3847/1538-3881/ae4c43).
- **Catalogue files at `data.desi.lbl.gov/public/dr1/`** (sizes read from the directory index):
  - `survey/catalogs/dr1/LSS/iron/LSScats/v1.5/BGS_BRIGHT_full_HPmapcut.dat.fits` (5,186,908,800 B) holds the observed and unobserved targets an isolation census needs;
  - `BGS_BRIGHT_{NGC,SGC}_clustering.dat.fits` (340,464,960 + 122,624,640 B) is the smaller clustering subset.
- **M★:**
  - the CIGALE VAC `vac/dr1/cigale/iron/v1.2/IronPhysProp_v1.2.fits` (7,322,716,800 B);
  - the stellar-mass/emission-line VAC (52.3 GB, not needed);
  - the 6.7 M-galaxy BGS spectral-fit catalogue (arXiv:2607.19162);
  - FastSpecFit v3.0 (`vac/dr1/fastspecfit/iron/v3.0/catalogs/`, nine main-bright files totalling over 27 GB) carries the fibre velocity dispersion needed for a per-lens ETG M/L.
- **Overlaps with shear** (arXiv:2512.15960, Table 3): KiDS-1000 446.3, DES-Y3 587.5, HSC-Y3 413.3 deg².
- **On disk:** the KiDS bright sample (85 MB) and its LePhare file (246 MB), Brouwer's released ESDs (2.3 MB), and the KiDS SOM-gold shear catalogue, **truncated** at 40.4%.
- **Not on disk:** DES Y3 metacal shapes (public; the DES DM page did not render a size); HSC Y3 shear (registration required, so the owner creates the account, not Claude).

**What the published analysis assumed** (Brouwer+21, arXiv:2106.11677, A&A 650, A113):
- the early/late difference is "at least 6σ" at fixed M★;
- the 3-D isolation (no neighbour with > 0.1 M★ within 3 h₇₀⁻¹ Mpc) uses photo-z and was validated on GAMA/MICE to about 80%. MICE is a ΛCDM HOD/abundance-matching mock, so the purity, and its dependence on type, is a ΛCDM-calibrated input;
- the escape "only the early types have M_gas ≈ M★ circumgalactic haloes" is offered as a hypothesis.

Mistele & McGaugh (arXiv:2310.15248) take a 4 Mpc criterion and their own SPS masses (ETG/LTG mass ratio Q = 1.4 relative to KiDS), and find one RAR for both types. Satellites contaminate early types more, and they raise the ESD at large radii in a type-dependent way, so an isolation impurity can fake a split. The record's own audit names "satellites (the isolation flags were not read)" among the systematics a jackknife cannot see (CFG108).

**Power (P1).**
- **The reference:** the split needs 0.35–0.4 dex more baryons for the early types (CFG95). In the deep regime that is S = 0.1875 dex in g_obs. The KiDS jackknife at 4.4σ gives σ_S = 0.0426 dex. B predicts 0.035 dex after its own calibration.
- **Scaling:** by σ ∝ (N_lens × n_eff)^(−1/2) from KiDS's 181,477 isolated lenses × 6.2 arcmin⁻², over the DESI overlaps with a BGS density of 500–730 deg⁻² and an isolated fraction of 0.16–0.26 (both brackets are assumptions):
  - all three surveys: N 116k–275k, σ_S 0.028–0.042, B vs split **3.6–5.6σ** (2.3–3.5σ with ×1.58);
  - no HSC: 2.3–3.6σ (1.5–2.3σ);
  - DES alone: 1.7–2.7σ.
- **Caveats:** shape noise is taken as equal across surveys, and HSC's deeper n(z) gain is ignored (a conservative choice). It is a scaling from KiDS, not a forecast with a covariance.
- **Calibration wall:** not relevant (this is a differential test at fixed z).

**Framework-native re-analysis.** This is B's own chain (the CFG61/88 estimator; B's g_bar with the CFG95 dynamical calibration; 1-halo bins; colour + Sérsic classes as in Brouwer). The new pieces are:
- spectroscopic isolation from DESI z, with photo-z only for unobserved targets;
- per-lens α_dyn(σ) for early types from the DESI fibre σ, instead of the class median.

Controls:
- (C1) on the KiDS-N ∩ DESI overlap, reproduce the KiDS split with photo-z isolation, then switch to spec-z isolation. **This contrast is the decisive one;**
- (C2) cross-shear nulls;
- (C3) random lenses;
- (C4) MUTATE: inject the 0.19-dex split into a split-free mock;
- (C5) the three surveys separately.

## 2. The cut small scales of DESI DR1 lensing (rank 2)
- **Data:** Heydenreich+25 (arXiv:2506.21677) measure ΔΣ for BGS (0.1–0.2–0.3–0.4, with M_R cuts at −19.5, −20.5 and −21) and LRG (0.4–0.6–0.8–1.1) with HSC, KiDS, SDSS and DES, in 15 bins from 0.08 to 80 h⁻¹ Mpc. Repository `github.com/sheydenreich/DESI_Y1_measurements` (public, MIT; contents and size not verified).
- **What the analyses did:** the cosmology fits cut lensing below 2.5 h⁻¹ Mpc (2512.15962, AbacusSummit + HOD with assembly bias) or 6 h⁻¹ Mpc (2512.15960). The source paper finds a trend with source redshift that "vanishes once we apply shifts to the" HSC n(z), and excess scatter driven by r ≤ 1 h⁻¹ Mpc.
- **Use:** no law test, because the lenses are not isolated and carry no M★. Measure the survey-to-survey ratio of ΔΣ(r_p < 1 h⁻¹ Mpc) for the same lens bin. Its excess over the quoted errors is an empirical, E-mode, survey-dependent multiplicative systematic, which is the class of systematic the KiDS split is "fragile only to" (CFG107/108).
  - If the excess is below about 25% of the errors, the ×1.58 inflation that kills the split's significance is disfavoured.
  - If it is above, rank 1 must carry it.
- **Downloads:** the GitHub repository only (size to be read on the owner's go).

## 3. JWST z ≈ 4–6 grism discs with measured gas (rank 3)
- **Data:**
  - Danhaive+25 gold (arXiv:2503.21863; v1 table of 41 on disk via CFG273; the MNRAS version has 37, with the dropped rows unverified, CFG266);
  - the 163-galaxy follow-up (arXiv:2510.14779; "Gas masses are estimated via scaling relations", median f_gas 0.77).
- **Assumptions:**
  - M_dyn from v/σ₀ with an exponential-disc pressure term (v_c² = V² + 3.36σ₀²);
  - Prospector M★ with an unstated IMF;
  - scaling-relation gas extrapolated beyond z ≈ 4;
  - no NFW in M_dyn (unlike RC100/CRISTAL, CFG303).
- **Power (P4, with the committed ν_mono):** at z = 4.17 the rival's a₀ is ×6.65.
  - **The median disc:** with D★ = 4.35 at the operating point where FLAT needs M_b/M★ = 3.9 (CFG273 PALL), the rival needs 2.18. The separation is **0.25 dex**, so 3σ needs a shared baryon calibration ≤ 0.084 dex.
  - **Illustrative fixed-D rows:** the separation is 0.72 / 0.55 / 0.33 / 0.14 dex at y★ = 0.08 / 0.3 / 1 / 3. So deep discs need ≤ 0.18–0.24 dex.
  - **The record's own stars-only upper bounds:** 6 of 32 rooted discs have central s★ below the rival at their z (5 are σ₀-limit rows), but **0 of 32** have a 95% bound below it. The bounds span about 2 dex.
  - **The CFG240 floor:** with about 7 deep discs at 0.3 dex each, it gives σ(log a₀) ≥ 0.34 dex against 0.82 dex, at most 2.4σ.
  - **Verdict:** MARGINAL. NOT POSSIBLE with scaling gas.
- **Re-analysis:**
  - Select y★ ≤ 0.3 discs from the published (v2) table plus 2510.14779.
  - Measured CO/[CII] gas from NOEMA (GOODS-N) or ALMA (the three GOODS-S rows).
  - Run CFG273's estimator with the gas as a value.
  - Controls: the pressure term varied (CFG308 showed it dominates), the IMF ±0.1 dex, and the floor logic.
- **Downloads:** the MNRAS table (journal page, small); NOEMA archive cubes (sizes unknown; owner's go).

## 4. DESI LRG vs BGS lensing a₀(z) (rank 4)
- **Arithmetic (P2):** a₀ ∝ H(z) shifts the deep-regime lensing amplitude by ½ log[E(0.8)/E(0.25)] = **+0.072 dex** (FLAT: 0).
  - 3σ needs total σ ≤ 0.024 dex and an M★ drift between the epochs ≤ 0.048 dex.
  - The published SPS method-to-method systematic is 0.2 dex (Brouwer+21).
- **The statistics fall short too:** for isolated LRGs (600 deg⁻² × completeness 0.5 × 15% isolated; n_eff behind z ≈ 0.8 of 8 / 2 / 1.5 arcmin⁻² for HSC / DES / KiDS; a D_A penalty of 3.65), σ ≈ 0.13 dex, i.e. 0.6σ.
- **Physics:** LRGs are group centrals with hot gas M_gas ~ M★, a baryon term of 0.05–0.15 dex in amplitude that does not cancel against BGS (the prior lane b3be606a0 found a similar mass-dependent term).
- **Verdict:** NOT POSSIBLE in DR1. It would need DR2+ area and a demonstrated M★ drift.

## 5. DES Y3/Y6 cosmic shear (rank 5)
- **DES Y6:** S₈ = 0.789 ± 0.012 (3×2pt; 2.7σ from the CMB), and shear-only 0.783 (arXiv:2601.14559, 2602.10065).
- **DES Y3 small scales:** suppressed relative to Planck-ΛCDM on nonlinear scales (arXiv:2305.09827).
- **The framework's only number:** a halo-model lever estimate R(k ~ 1) of about 1.05 (canonical) / 1.12 (alt) (CFG1 A18 "SOFT"; CFG6 §6). That is an enhancement, the opposite sign from what the data prefer. It sits inside the baryon-feedback budget, so a ΛCDM-template analysis with feedback marginalised would absorb it as weaker feedback.
- **No committed action produces a nonlinear P(k) for B.** A test would need one, plus feedback pinned independently (kSZ/X-ray, e.g. arXiv:2509.10455).
- **Verdict:** NOT POSSIBLE now. If a P(k) is ever derived, the R > 1 sign is a possible liability, not a win.

## 6. DESI DR1 PV Tully–Fisher (rank 6)
- **Data:** 10,262 galaxies; slope −7.22 mag/dex; intrinsic scatter 0.466 mag; 4,050 calibrators in 14 bins (arXiv:2512.03227). Data on Zenodo upon acceptance. The DR1 VAC index lists no PV VAC.
- **The assumptions:**
  - **Each redshift bin has its own free intercept**, fixed by assuming "no average radial peculiar velocity", so any genuine redshift dependence of the zero point is removed by construction;
  - absolute magnitudes use flat ΛCDM (Ω_M = 0.3151);
  - the zero point comes from SH0ES/Pantheon+ (arXiv:2512.03232).
- **Power (P3):** between the volume-weighted halves (z 0.062 / 0.091) the rival moves a₀ by 0.0063 dex, i.e. 0.011–0.016 mag. The statistical σ is 0.009 mag, and the luminosity-evolution uncertainty (±0.5 mag per unit z) is 0.014 mag. There is no gas.
- **Verdict:** NOT POSSIBLE.

## 7. DESI BAO and the w0wa fits (rank 7)
- **P5, from the chains on disk (`desi_dr2_chains/*/chain.margestats`):** a₀ ∝ √ρ_DE,0 ∝ H₀√(1 − Ω_m), relative to the Planck footing, shifts by −0.038 (CMB), −0.006 (DESY5), +0.002 (Pantheon+) and −0.014 (Union3) dex.
- **The measured local a₀** spans 0.9–1.31e-10 (0.16 dex; CFG309), and κ = ½ stays fitted.
- **a₀(2.5) under the CPL branch:** −0.085 to −0.141 dex (CFG6: −0.10 to +0.14 across the branches). The chart's teal band already shows it.
- **The BAO fiducial-cosmology templates are not a hidden assumption here.** The framework's background is the same ΛCDM/w0wa.
- **Verdict:** NOT POSSIBLE.

## 8–11. The rest (NOT POSSIBLE)
- **COSMOS-Web (P6):**
  - Data: 0.54 deg² (arXiv:2601.17239; COSMOS2025, arXiv:2506.03243).
  - Assumptions: about 1,080 isolated lenses (8,000 deg⁻² × 25%) and 50 sources arcmin⁻² behind them.
  - Result: σ_A ≈ 0.28 dex against the rival's +0.126 dex at z = 1 (0.45σ).
- **"Too massive too early":** every published comparison uses a ΛCDM halo mass function. The framework has none (CFG303: collapse masses not derivable on native inputs). The stage-26 row is an upper bound whose decline uses a non-standing a₀(z).
- **Satellites:**
  - DESI's floor is 1 km/s (bright) / about 2 km/s (backup) (arXiv:2505.14787; `data_assembly/DESI_MWS_RV_2026-09-30.md`).
  - DESI DR1 dwarf work (Sestito & Kobayashi, arXiv:2512.13783) gives systemic velocities, not UFD dispersions.
  - The record's inputs already use Keck/DEIMOS (CFG257).
  - The MWS files on disk cover only the wide-binary pixels.
- **DESI Fundamental Plane:** central σ in the Newtonian regime cannot see the outer-halo deficit of massive ellipticals. Rank 1 is the route to that physics.

## Top 3 recommendations: lane designs
1. **CFG3xx: "Spec-z isolation decides the KiDS split."**
   - **Before any data:** freeze the criteria.
     - B survives if the spec-z-isolated split is < 2σ from B's 0.035 dex in at least two of three surveys.
     - B's specific failure is confirmed if the split is > 3σ above B under spec-z isolation in at least two surveys and C1 shows photo-z and spec-z isolation agree.
     - The KiDS split is an isolation artefact if C1 shows the spec-z split collapses on the same lenses and the same shear.
   - **Stage A (on disk plus DESI only):**
     - finish the KiDS shear download (10.56 GB) and fetch the BGS full catalogue (5.19 GB) and CIGALE (7.32 GB);
     - build the KiDS-N ∩ DESI lens set (about 446 deg²) and run C1 with B's committed estimator.
   - **Stage B:** add DES Y3 metacal (public), then HSC Y3 (the owner's account).
   - **Controls:** C1–C5 above; MUTATE injects the split; the per-lens α_dyn(σ) with and without.
   - **Power:** 2.3–3.6σ (KiDS + DES), 3.6–5.6σ (with HSC).
   - **Owner's yes needed for:** each download named above.
2. **CFG3xx: "The small scales DESI cut."**
   - Download the Heydenreich+25 GitHub data vectors (size to be read first).
   - For each lens bin and each survey pair, compute the ratio ΔΣ_A/ΔΣ_B at r_p < 1 h⁻¹ Mpc and its χ² against the quoted covariances. That gives the empirical excess-scatter factor f_x.
   - Freeze before reading: if f_x < 1.25, CFG108's ×1.58 inflation is disfavoured and the KiDS split's 4.4σ stands as quoted. If f_x ≥ 1.58, the split's significance is carried at the inflated error in every future citation.
   - Control: the same statistic at r_p > 1 h⁻¹ Mpc, where the paper reports 2σ consistency.
   - No framework model enters, so it cannot fake a signal.
3. **CFG3xx: "Deep JWST discs with measured gas."**
   - Freeze a y★ ≤ 0.3 selection on the published Danhaive tables (v2 gold plus arXiv:2510.14779).
   - Obtain measured gas: NOEMA CO for GOODS-N, ALMA for GOODS-S.
   - Run CFG273's estimator with the gas as values, on the pressure-term grid of CFG308.
   - Pre-flight: the separation is 0.55–0.72 dex in required baryons. The CFG240 floor caps about 7 discs near 2.4σ, so the lane is worth running only if at least 7 deep discs get measured gas with a shared calibration ≤ 0.2 dex.
   - Owner's yes needed for: the journal table and any NOEMA/ALMA archive data (sizes to be read first).

## Checks (`cfg314_power.py`)
- **Main run:** 15/16 pass. **P1b FAILS and is kept:** without HSC, the worst cell with ×1.58 covariance gives 1.49σ, against the 2σ I wrote before running. Exit code 1.
- **MUTATE run** (`MUTATE=1`, a₀ ∝ 1/H): P2a, P4a and P4b fail as required, the sentinel passes, and P1b fails as in the main run. 13/17.
- Every literature number in the script carries its source, and every guess is marked ASSUMPTION with a bracket. P1 scales from KiDS; it is not a covariance forecast.

## Disclosures
- **Read at abstract or summariser level (WebFetch):** 2512.03227 (its fitting method from the HTML), 2506.21677, 2512.15960/1/2, 2310.15248, 2106.11677, 2601.14559, 2602.10065, 2610.01541. These are PROVISIONAL per the record's WebFetch rule. Numbers that matter for a lane (the overlap areas, the scale cuts, the per-bin TF intercepts) must be re-read from the PDFs before any criteria are frozen.
- **Rana+26 (arXiv:2610.01541, 1 Oct 2026)** forecasts an 8.5% constraint on a stellar M/L "mismatch" from 10–100 h⁻¹ kpc lensing of DESI-like BGS, assuming NFW. It is context for rank 1's M/L systematic and was not used.
- **File sizes** come from the DESI directory index (bytes as listed). The DES Y3 and HSC sizes were not obtained.
- **Not done:** contacting anyone; creating any account; any header or byte-range read of a remote data file.
- **κ = ½ and Ω_c h² stay fitted.** Nothing here says the theory is closed.

## Files
- `cfg314_power.py`: the power arithmetic. Run from the repository root; `MUTATE=1` for the control.
- `cfg314_power.out`, `cfg314_power_results.json`: the main run.
- `cfg314_power_MUTATE.out`, `cfg314_power_MUTATE_results.json`: the control.
