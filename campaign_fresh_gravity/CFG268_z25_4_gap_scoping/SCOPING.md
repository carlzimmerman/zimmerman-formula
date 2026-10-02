# CFG268: what public data exist at z ≈ 2.5–4 for an implied a₀, and is any of it conditioned? (scoping, 2026-10-01)

> **κ = ½ is FITTED. a₀(z) FLAT is the framework's distinctive law; a₀ ∝ H(z) is the rival. No a₀ is computed in this lane, no law is fitted, no kernel is inverted, and no sentence here says the data favour a law.** Both footings are carried (canonical 9.36e-11, alternative 1.131e-10 m s⁻²).
>
> **Page reads only; nothing was downloaded into the repository.** The only quantities computed are conditioning ESTIMATES: y = g/a₀ at the radius where each paper quotes a velocity (`cfg268_y_estimates.py`), and the sizes of public ALMA products, from archive metadata (`cfg268_alma_price.py`, TAP plus DataLink, no file fetched). arXiv source sizes come from HTTP HEAD requests.
>
> **How each source was read:**
> - **text**: full text, from a PDF the fetch tool cached outside the repository, or arXiv HTML streamed and searched;
> - **abstract**: the arXiv abstract page (title, authors and date checked for every arXiv ID cited);
> - **page**: a web page through a summariser, so the wording is the summariser's;
> - **snippet**: a search snippet only, marked **UNVERIFIED**.
>
> Not committed.

## Bottom line
1. **No sample and no single object at 2.5 ≲ z ≲ 4 is CONDITIONED+GAS.** I checked 33 entries: 12 sample classes, 6 out-of-band or already-done items, 12 single objects and 3 references just below the band.
   - Every galaxy here with a **measured** gas tracer is a massive dusty or AGN-host disc. Its outermost quoted radius sits at **y ≳ 2** (y_obs ≈ 3.4–8 for the best cases) and its inner radii at y ≈ 6–25.
   - The only galaxies that reach **y ≲ 0.3** are low-mass Lyman-break galaxies (LBGs) in the KMOS Deep Survey (KDS) and in AMAZE/LSD. They have **no measured gas**. Their seeing-limited, mostly pressure-supported kinematics also make g_obs model-dependent: in KDS the pressure term exceeds V_C² in 29 of 32 rows.
2. **Verdict counts (honest):**
   - CONDITIONED+GAS: **0**.
   - CONDITIONED-NO-GAS (upper bounds only): **2**, both marginal — KDS and AMAZE/LSD.
   - ILL-CONDITIONED: every single object, GA-NIFS, the lensed IFU LBGs, the ALMA CO sets and the quiescent σ* set.
   - NO-DATA (for this purpose): MOSDEF (no per-galaxy table), KLEVER (kinematics unpublished), JWST MSA/grism in this slice, MUSE/KCWI, VUDS/VANDELS, stacks.
3. **Shortlist (at most 3 lanes; details and downloads in the Shortlist section below):**
   - **S1. ADF22.1.** The [CII] rotation curve: 8–9 nearly independent rings out to about 14 kpc, measured CO(1–0), a JWST stellar profile. It reaches y_bar ≈ 2–5 at the last ring. It is the same galaxy as ALPAKA 23, so it would **replace** CFG272's no-root row, not add a second point.
   - **S2. KDS + AMAZE/LSD.** The two tabulated z ≈ 3–3.8 LBG sets. They give stars-only upper bounds and floors, and they include **5 galaxies measured by both surveys**, which give an empirical velocity-systematics control.
   - **S3. The Big Wheel.** y_bar ≈ 2–4 at 10 kpc with measured CO(4–3). It is worth running only after the 0.24″ data (ALMA 2025.1.00107.S) become public on **2026-12-17**.
   - **S1 and S3 are single objects: CFG240 says neither can be conditioned.** They would be labelled envelopes next to ALESS 122.1, not constraints.
4. **Downloads that would be needed (none done; each needs the owner's go):**
   - arXiv e-print sources:
     - 2604.07440: 3.84 MB;
     - 2410.22155: 6.84 MB;
     - 1704.06263: 6.68 MB;
     - 1007.4180: 0.83 MB;
     - 2605.04144: 3.84 MB.
   - Optionally, ALMA 2021.1.01406.S: 2.43 GB plus 0.26 GB.
   - After 2026-12-17, ALMA 2025.1.00107.S: 30.27 GB.
   - The full list is in the Shortlist section.
5. **Side findings:**
   - **(a) The repeat measurements disagree badly.**
     - CDFS-16767 / KDS lbg_113: AMAZE V_max 623 km/s (unconstrained, i fixed at 15°) against KDS V_C 41 km/s.
     - KDS b012141_012208 is "rotation-dominated" in KDS and "not rotating" in AMAZE.
     - Only CDFS-14411 / lbg_109 agrees (69 against 53 km/s).
   - **(b) Archival ALMA data at 0.08–0.14″ exist with no kinematics paper found:**
     - SPT2147-50: Band 8 0.08″, 8.66 GB;
     - SPT0103-45: Band 8 0.11″, 19.81 GB;
     - the Cosmic Eye: Band 3 0.14″, 60.51 GB.
     - All but the Cosmic Eye are massive dusty galaxies, so ILL-CONDITIONED by mass.
   - **(c) PKS 0529-549 is already being run as CFG275** in another session (commits 4108d99e9, c81be9e8c, bddebde63), so it is not repeated here. This scoping agrees it is ILL-CONDITIONED (y_obs ≈ 8, gas alone y ≈ 8).
   - **(d) No paper in this band compares its data to MOND or the RAR.** Full texts were searched for "MOND", "Milgrom" and "radial acceleration relation" (0 hits in 14 papers: Turner+17, Gnerucci+11, Price+20, Rodríguez del Pino+24, Lamperti+24, Swinbank+15, Gururajan+22, Rizzo+21, Quadri+26, Pensabene+25, Rizzo+26, Lin+25, Westoby+26, Umehata+25); for the other papers only the abstracts were checked.

## The yardstick (CFG240, `../CFG240_calibration_wall/README.md`; PAPER38 10.5281/zenodo.23085582)
- With the baryon calibration f free:
  - σ(log a₀) ≥ 3σ/√N (T4);
  - for P2, N = 20, σ = 0.1 dex: y_min = 0.01 needs y_max ≳ 8, and y_min = 0.1 never reaches 0.1 dex;
  - a 0.15 dex prior on f lowers the requirement to y_max ≳ 5.5.
- About 0.1 dex of baryon calibration is needed (PAPER38).
- y here is the **nominal** y = g/a₀ at the paper's numbers. CFG240's y is f g/a₀ at the true f.
- A single object is conditioned only if its own curve spans y ≲ 0.1–0.3 to y well above 1. **None does.**

## Ranked table: samples (y values are ESTIMATES from `cfg268_y_estimates.out`, canonical footing)
| # | sample (source; how read) | z; N | field, Dec; ALMA? | tracer; resolution | curve or V, σ; radius | M* (method) | gas | public products (size) | y estimate; deep points? | verdict | MOND/RAR in paper? |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **KMOS Deep Survey (KDS)**, Turner+17, arXiv:1704.06263, MNRAS 471, 1280 (text) | 3.067–3.794 in Tables 2–3. 77 targeted, 62 detected, 47 resolved (38 field + 9 cluster). **32 isolated field galaxies tabulated, 13 rotation-dominated** | GOODS-S (Dec ≈ −27.7 to −27.9); SSA22 (Dec ≈ +0.1 to +0.3; the protocluster pointing is excluded). **Both ALMA-reachable** | [O III]5007, KMOS K/HK. Seeing 0.50–0.62″ (Table 1), ≈ 3.7–4.5 kpc (my conversion) | Beam-smearing-corrected model **V_C at 2 R_1/2** and σ_int (Table 3). Per-galaxy 1D extractions only in figures. R_1/2 0.46–3.30 kpc (GALFIT, HST) | SED (McLure+11 code), Chabrier; 0.2 dex quoted | **none** | Tables 2–3 printed (transcribed into the script). Raw KMOS data in the ESO archive (092.A-0399, 093.A-0122, 094.A-0214, 095.A-0680, 096.A-0315); reduced cubes not found; size not priced. Zenodo 834215 is a 2.2 MB poster | y_bar\* (stars only) 0.02–21, median 1.1; **4 of 32 below 0.3** (1 of the 13 rotators). y_obs (rotation only) 0.10–2.4. With +3.35σ² it is 0.26–10. Pressure term > V_C² in 29/32 | **CONDITIONED-NO-GAS (marginal)**: the y span exists across galaxies, but the median V_C error is ≈ 39% (half the quoted ± range over V_C, all 32 rows; ≈ 0.28 dex in g), so the T4 floor at N = 32 is ≈ 0.15 dex. Bounds only | no (0 hits, text) |
| 2 | **AMAZE/LSD**, Gnerucci+11, arXiv:1007.4180, A&A 528, A88 (text) | 2.616–3.797. 33 analysed (4 lensed, incl. the Cosmic Eye, observed but not analysed). **11 rotating** (Table 2) | SSA22, CDFS, Q0302, DSF2237, Q1422 (+23.0), 3C324 (+21.5), CDFa (+12.5). **All ALMA-reachable** | [O III] (Hα for one), SINFONI. AMAZE seeing-limited: PSF 0.5–0.7″ (Table 3). LSD with AO (0.3″ for Q0302-C131) | Exponential-disc model fitted to the velocity maps: M_dyn, V_max, r_e (scale radius, held fixed) in Table 3. 3 of 11 have parameters unconstrained, 2 are limits | Broad-band SED (Table 4); errors up to +1.07 dex | **Inverted Schmidt–Kennicutt only** (slope 1.4). Troncoso+14 gas fractions named in the ESO release: **UNVERIFIED** | Tables 1–4 printed. ESO Phase 3 release: 25 extracted 1D spectra + catalogue, **no cubes** (release description read). LSD AO cubes: raw only (**UNVERIFIED**) | y_bar\* 0.16–23 (median 1.7); y_obs 0.47–169 (median 3.2); 3 rows below 0.5 | **CONDITIONED-NO-GAS (marginal)**: N = 11; T4 floor ≈ 0.27 dex if 0.3 dex per point is assumed. Bounds only | no (text) |
| 3 | **MOSDEF**, Price+20, arXiv:1902.09554, ApJ 894, 91 (text); Kriek+15, arXiv:1412.1835 (abstract) | 1.4–3.8; 681 kinematic, 105 with resolved rotation. **At 2.9 ≤ z ≤ 3.8: 14 resolved/aligned rotators** (Table 2: 7 + 7), median log R_E 0.32 (2.1 kpc), V/σ ≈ 0.8 | CANDELS fields: AEGIS (+52.9, **no ALMA**), COSMOS, GOODS-N (+62.2, **no ALMA**), GOODS-S, UDS (field list from a page) | Hα/[O III], MOSFIRE slits, seeing-limited | V(R_E) and σ_V,0 per galaxy, but **only medians are tabulated** (Tables 2–4) | FAST, Chabrier | Inverted KS (N = 1.4) | No per-galaxy kinematic table in the paper. The MOSDEF site now redirects (checked 2026-10-01): **availability UNVERIFIED**. Raw data at the Keck Observatory Archive | not computable per galaxy (median z ≈ 3.2 bin: log M* 9.3–9.9, R_E 2.1 kpc) | **NO-DATA** (ill-conditioned by design: one radius, V/σ < 1) | no (text) |
| 4 | **KLEVER**, Curti+20, arXiv:1910.13451; Hayden-Pawson+22, arXiv:2110.00033 (page) | 192 galaxies at 1.2–2.5; **27 lensed at z 2–3.45** | AS1063 (−44.5), MACS0416 (−24.1), MACS1149 (+22.4) | KMOS, seeing-limited | **No kinematics paper found** ("resolved capabilities … future work") | — | — | ESO raw data only | — | **NO-DATA** | — |
| 5 | **GA-NIFS at z 3–4**: GS_4891 (Rodríguez del Pino+24, arXiv:2309.14431, text); GS5001 (Lamperti+24, arXiv:2406.10348, text); mini-BAL QSO (Perna+24, arXiv:2411.13698, abstract) | 3.47–3.70; 3 systems | GOODS-S (ALMA-reachable) | NIRSpec IFS, ≈ 0.1″ | GS_4891: one fitted v_rot ≈ 90 km/s at 2.2 kpc, M_dyn ≈ 1.7e10. GS5001: X-ray AGN, outflow, kinematic axis ≈ 40° from photometric. QSO: ±1000 km/s outflow | GS_4891: 5.5e9 inside the kinematic region (prism SED) | GS5001: CO(4–3) reservoir to 40 kpc; others none | MAST (not priced) | GS_4891: y_obs 1.3, y_bar ≤ 1.7 | **ILL-CONDITIONED** (one radius, or AGN/outflow dominated) | no (text) |
| 6 | **JWST NIRSpec MSA / NIRCam grism at 2.5–3.7**: JADES DR3 σ stacks (Sanyal & Rahaman 2026, arXiv:2609.14071, abstract); AURORA (Shapley+24, arXiv:2407.00157, page); NIRCam grism Hα (CONGRESS) reaches only z ≳ 3.7 | 1.5–3.5 (587 stacked); AURORA 1.4–4.4, 97 galaxies | GOODS-S/N, COSMOS | R ≈ 1000 MSA (integrated) | Stacked σ in 4 z bins turned into "rotation curves using GR"; no baryon model. AURORA: no kinematics paper found | — | — | MAST | — | **NO-DATA** (stacks without baryons; Danhaive gold already done; Danhaive+26, arXiv:2510.14779, is z ≈ 4–6) | no |
| 7 | **Lensed IFU LBGs**: Law+09 (arXiv:0901.2930, abstract); Jones+10 (arXiv:0910.4488, abstract); Livermore+15 (arXiv:1503.07873, abstract); Nesvadba+06 arc&core (astro-ph/0606527, abstract) | Law: 12 at 2.0–2.5 + 1 at 3.3 (at most 5 of 13 rotate). Jones: 6 at 1.7–3.1 (4 coherent). Livermore: 17 at 1–4 (59% discs) | various | OSIRIS/SINFONI/NIFS with AO, ~100–200 pc in the source plane | Inner few kpc; Jones: V sin i/σ 0.5–1.3, M_dyn 10^9.7–10.3 | mostly not in the abstracts | none | ESO/Keck raw | arc&core y_obs ≈ 3 inside 1 kpc | **ILL-CONDITIONED** (few in band, inner kpc, no gas) | no |
| 8 | **ALMA/NOEMA CO and [CII] sets at z 3–4**: Westoby+26 (arXiv:2606.11444, text); ADF22-WEB CO census (Umehata+26, arXiv:2609.06679, abstract); ASPECS (repo record: "three sources with a clear velocity gradient", **UNVERIFIED** here); Birkin+21 (snippet: 61 SMGs, CO for 50, **UNVERIFIED**) | Westoby: ALESS3.1, 3.1-comp, 9.1 (median z 3.5). Census: 18 DSFGs at z 3.09 | ECDFS (−27.8); SSA22 (+0.3) | Westoby: CO(5–4)/(4–3) at 0.25″ ≈ 2 kpc. Census: CO(1–0) for 12, CO(3–2) for 18 | Westoby: **≤ 3 independent rings**, "baryon dominated on ≲ 10 kpc", α_CO ≲ 1.2 from the dynamics. Census: no rotation curves | Westoby: SED with JWST | CO measured | ALMA (not priced) | Westoby: y ≫ 1 (baryon-dominated) | **ILL-CONDITIONED** (Westoby); **NO-DATA** for dynamics (census, ASPECS, Birkin). **No [CII] kinematic survey at z 3–4 found** (Band 8; targeted objects only) | no (Westoby text) |
| 9 | **MUSE / KCWI** | — | — | Lyα (resonant) at z > 2.9; MUSE [O II] only below z ≈ 1.5 (MUSE-DARK, done). Foran+23 (arXiv:2311.15721, abstract) relates nebular IFU kinematics to Lyα at z 2–3; instrument and N not in the abstract (**UNVERIFIED**) | — | — | — | — | — | **NO-DATA** | — |
| 10 | **VUDS / VANDELS**: VANDELS DR (Garilli+21, arXiv:2101.07645, abstract); VUDS not checked (**UNVERIFIED**) | 1–6.5, 2087 spectra | CDFS, UDS | rest-UV, 2.5 Å dispersion | redshift survey; no gas-dynamical σ catalogue | — | — | ESO | — | **NO-DATA** | — |
| 11 | **Stacks**: Tiley+19, arXiv:1811.05982 (abstract) | 0.6–2.2 | — | KMOS/MUSE | stacked shapes | — | — | — | — | **NO-DATA in band** | — |
| 12 | **Quiescent σ\***: MAGAZ3NE, Forrest+22, arXiv:2208.04329 (abstract) | ≳ 3 | — | MOSFIRE/NIRES absorption lines | σ\* ≈ 400 km/s for 8 ultramassive galaxies, compact | SED | — | — | y ≫ 1 | **ILL-CONDITIONED** | — |
| — | Out of band or already done (checked, not ranked) | Rizzo+21 lensed SPT [CII] discs: z 4.23–4.77 (arXiv:2102.05671, text, Table 1); de Graaff+24: JADES z 5.5–7.4 (arXiv:2308.09742; it is **not** GA-NIFS); Saldana-Lopez+25: z 4–7.6 (arXiv:2501.17145); Danhaive+26: z ≈ 4–6; GN20: z 4.055 (single-object table); DLA0817g1: z 4.26 (arXiv:2512.05213) | | | | | | | | | |

## Single objects (the orchestrator's section): one-offs at z 2.5–4, ranked by (a)–(c) together
Columns:
- (a) independent radii and the outer radius in disc units;
- (b) the y range across those radii (ESTIMATE; `cfg268_y_estimates.out`, canonical footing);
- (c) gas MEASURED or scaled;
- (d) stellar mass and its method;
- (e) published products and sizes (ALMA sizes are from `cfg268_alma_price.out`, product tar only).

**For comparison:** CFG229 tried seven class-M galaxies.
- Six have no root.
- ALESS 122.1 has s\* = 8.82 at y = 4.8, with a wide envelope (statistical 68% ×4.2 to ×14.4 in the record; the orchestrator quotes 3.7–17.9).
- A one-off is "worth more" here only if it adds independent radii, a measured gas tracer, or y nearer 1.

| rank | object (sources; how read) | z; Dec | (a) radii; outer radius | (b) y (estimate) | (c) gas | (d) M\* | (e) products (size) | verdict | beyond CFG229 / the record |
|---|---|---|---|---|---|---|---|---|---|
| 1 | **ADF22.1 = ADF22.A1 = ALPAKA 23**: Umehata+25, PASJ 77, 432, arXiv:2410.22155 (text); Rizzo+26, arXiv:2604.07440 (text) | 3.09; +0.30 | [CII] beam 0.23″ × 0.27″ (Rizzo+26; Umehata+25 lists 0.23″ × 0.17″). **8–9 rings, 0.23″ wide (≈ 1.8 kpc), "nearly independent"**. Outermost ≈ 14 kpc, flat to ≥ 16 kpc in tapered imaging. V_rot = 530 ± 10 km/s at 2 r_e. r_e = 6.2–7.0 kpc, so R_out ≈ 2.0–2.3 r_e ≈ 3.4–3.8 R_d | outer y_obs 6.9; y_bar 2.2 (stars), 2.7 / 3.9 / 5.3 with gas at α_CO 0.8 / 2.5 / 4.6. Inner (4 kpc) y_bar ≈ 6–11. **No point below y ≈ 2** | **MEASURED**: CO(1–0) with the JVLA, L′ = (8.1 ± 1.4)e10, so M_gas = (α_CO/2.5) × 2.0e11. Resolved CO(3–2) and [CII]. Rizzo+26 fit α_CO = 1.8 dynamically: circular, not an independent route | SED 10^11.4 (Umehata+25), JWST F444W profile, B/T 0.2 from resolved SED. **X-ray AGN; protocluster core** | No V(R) table (Fig. 6 of Umehata+25, Fig. 8 of Rizzo+26). ALMA 2021.1.01406.S: 2.43 GB (0.16″) + 0.26 GB (0.35″). 2021.1.00041.S: 4.55 GB. 2018.1.01306.S CO(3–2) 0.07″: 134.25 GB. Deeper 0.07″ Band 8 (2025.1.01331.S) is proprietary until 2027-07-17. JWST GO 3547 via DJA | **ILL-CONDITIONED** (single, y ≥ 2), but the best one-off in the band | CFG272 used ALPAKA's CO(3–2) curve and M\* = 5.3e11 at y = 15.3: D = 0.856, no root. Here the radius is ≈ 2–3× larger and M\* is half, so D_stars ≈ 3.2 (estimate). **The no-root row could become an ALESS-122.1-like envelope**, with α_CO the dominant knob |
| 2 | **Big Wheel**: Wang+25, Nature Astronomy 9, 710, arXiv:2409.17956 (abstract); Quadri+26, arXiv:2605.04144 (text) | 3.245; −49.6 | Public CO(4–3) beam 1.17″ × 1.05″ ≈ 9 kpc, i.e. **1–2 beams** across R_obs ≈ 10 kpc. The 0.35″ Cycle-12 data used by Quadri+26 are proprietary. r_half-mass 6.3 kpc, so R_out ≈ 1.6 r_e ≈ 2.7 R_d | y_obs 3.4 (i = 38° +8/−10: +72% / −27%). y_bar 2.3 with the dynamical M\* + gas; 4.3 with the SED M\* + gas | CO(4–3) **measured**; α_CO/r₄₁ is a free parameter with a prior (posterior log M_gas 10.76) | SED 10^11.37 ± 0.20 (CIGALE) against the dynamical posterior 10^11.00: they disagree by 0.37 dex. X-ray AGN | arXiv source 3.84 MB. ALMA 2021.1.00793.S low-res: 26.29 GB (Band 3), 6.49 GB (Band 6). **2025.1.00107.S 0.24″: 30.27 GB, proprietary until 2026-12-17** | **ILL-CONDITIONED** (single, inclination) | Reaches y ≈ 2–3 at 10 kpc, close to ALESS 122.1, with measured CO. Its two stellar-mass routes already show the calibration wall |
| 3 | **PKS 0529-549**: Lin+25, arXiv:2411.08958 (text); Huang+24, arXiv:2411.04290 (abstract). **Being run as CFG275** | 2.57; −54.9 | [CI](2–1), 0.18″ (1.5 kpc). 5 rings at half-beam spacing, so ≈ 2–3 independent. Outer radius 3.3 kpc ≈ 1.3 × the gas R_e (2.57) ≈ 1.1 × the stellar R_e (3.0) | y_obs 8.2 (V 280; ×1.23 at 310). Gas alone gives y_bar 8.3; with stars, 11–27 | **MEASURED three ways** ([CI], CO(4–3), dust); they differ by up to ×4 (~1e11) | SED 3e11 (elliptical template) against CIGALE (preliminary) 0.4–1.2e11 and a dynamical stars-only upper limit of 1.1e11. Radio-loud AGN, gas tails | ALMA 2018.1.01669.S: 44.52 GB (Band 6, 0.10″) and 56.62 GB (Band 4). No V(R) table (CFG275 digitised the vector figure) | **ILL-CONDITIONED** (not repeated here) | Three gas tracers, but y ≥ 8 |
| 4 | **SDP.81** (H-ATLAS J090311.6+003906): Dye+15, arXiv:1503.08720; Swinbank+15, arXiv:1505.05148 (text); Rybak+15b, arXiv:1506.01425 (abstract) | 3.042; +0.65 | Lensed; source plane ≈ 50–100 pc. V_rot 320 ± 20 (i = 40 ± 5) within 1.5 kpc; R_CO ≈ 6 kpc (Rybak). A few radii in the source plane, lens-model dependent | y_obs 24 at 1.5 kpc; ≈ 3.3 at 6 kpc (from M_dyn ≈ 8e10) | **MEASURED** (CO(1–0) and dust): 2.7–3.9e10 | 6.6e10 (Negrello+14), but **offset by 1.5 kpc from the gas disc: an interacting pair** (Dye+15). Swinbank+15 adopt ≲ 3e10 inside the disc | ALMA long-baseline science verification: 253.73 GB (16 tars). Also Band 8 0.22″, Band 3 0.07–0.25″, Band 10 | **ILL-CONDITIONED** (Newtonian inner disc; interacting; stars offset) | — |
| 5 | **Cosmic Eye** (LBG J213512.73−010143): Coppin+07, arXiv:0705.1721 (abstract); Stark+08, arXiv:0810.1471 (abstract); Riechers+10, arXiv:1010.4299 (abstract) | 3.074; −1.0 | Lensed (×28). OSIRIS, ~100 pc. Rotation to ±2 kpc with v sin i ≈ 55 and σ ≈ 54 (**UNVERIFIED**: secondary page, not in the abstracts). Two UV components ≈ 2 kpc apart | y_obs ≥ 3.0 at 2 kpc (i = 90° lower bound); y_bar ≤ 3.1 (all baryons inside 2 kpc, an upper bound) | **MEASURED**: CO(3–2), M_gas = (2.4 ± 0.4)e9 (α_CO used **UNVERIFIED**); CO(1–0) from the EVLA | ≈ (6 ± 2)e9 (mid-IR) | ALMA **2019.1.01642.S Band 3 at 0.14″: 60.51 GB, public since 2022-10-27, no kinematics paper found**. The AMAZE SINFONI cube was observed but not analysed by Gnerucci+11 | **ILL-CONDITIONED** (compact; inclination unknown) | The only low-mass (M\* ≈ 6e9) z ≈ 3 disc with measured CO and lensing-boosted resolution. Overlooked archive data. Its ≈ 2 kpc extent keeps y ≳ 1–3 |
| 6 | **GA-NIFS GS_4891** (arXiv:2309.14431, text) | 3.70; −27.8 | **One radius**: v_rot ≈ 90 km/s at 2.2 kpc | y_obs 1.3 (alt 1.05); y_bar ≤ 1.7 | **none** | 5.5e9 inside the kinematic region | MAST (not priced) | **ILL-CONDITIONED** (one radius, no gas) | The only z 2.5–4 rotator found with **y_obs ≈ 1**. In GOODS-S, so ALMA gas follow-up is possible |
| 7 | **GN20** (z 4.055, **just outside the band**): Hodge+12, arXiv:1209.2418 (abstract); Übler+24, arXiv:2403.03192 (TeX on disk) | 4.055; **+62.4, no ALMA** | CO(2–1) with the VLA at 1.3 kpc; gas disc 14 ± 4 kpc across. Hα: v_c(3.6 kpc) = 496, maximum 574 at 6.8 kpc. **Inclination 30–45° in the literature** (V 442–646) | y_obs 17 at 6.8 kpc; y_bar ≈ 9 | CO multi-J, [CI] and dust **measured**, but Hodge+12's α_CO = 1.1 ± 0.6 is dynamically derived (circular) | 1.1–2.3e11; MIRI R_e 3.6 kpc | VLA / NOEMA / JWST (not priced) | **ILL-CONDITIONED** | — |
| 8 | **MQN01-QC**: Pensabene+25, arXiv:2507.16921 (text) | 3.25; −49.6 | CO(4–3) at 0.3″; **rings oversampled 1.6× (not independent)**; disc to ≈ 4 kpc | y_obs 22 (M_dyn 2.5e11 within 4.1 kpc) | CO(4–3) **measured** (α_CO 1.7, r₄₁ 0.87): 6e10 | 9.1e10 inside 2.3 kpc (JWST, calibrated colour relation) | 2021.1.00793.S 0.24″: 109.53 GB | **ILL-CONDITIONED** | — |
| 9 | **SPT2147-50** (z 3.760) and **SPT0103-45** (z 3.089): Gururajan+22, arXiv:2109.03450 (text) | −50.6; −45.6 | **No rotation curve**: one M_dyn each, from red and blue source positions (2.5–3.4e10; 1.2–1.55e11) | not computable from the paper; Newtonian by its own statement (gas ≈ M_dyn) | [CI](2–1), CO(7–6) and dust **measured** | not in the paper | 2018.1.01060.S: 3.46 + 1.07 GB; 2017.1.01018.S: 3.72 GB. **Archival higher-resolution Band 8 with no kinematics paper found**: SPT2147-50 2019.1.00471.S 0.08″ (8.66 GB); SPT0103-45 2023.1.01354.S 0.11″ (19.81 GB, public 2025-08-06). Line content **UNVERIFIED** | **ILL-CONDITIONED** | — |
| 10 | **ALESS 3.1 / 9.1**: Westoby+26 (text) | ≈ 3.4–3.7; −27.8 | **≤ 3 rings**; baryon-dominated | y ≫ 1 | CO **measured** (α_CO ≲ 1.2 from the dynamics) | SED with JWST | ALMA | **ILL-CONDITIONED** | Both are in Amvrosiadis' parent table but were not among its 12 modelled discs |
| 11 | **arc&core** (lensed by 1E0657-56): Nesvadba+06 (abstract) | 3.2; −55.9 | Inner kpc only | y_obs ≈ 3 | none | — | — | **ILL-CONDITIONED** | — |
| 12 | **W2305-0039**: Tadaki 2026, arXiv:2603.01352 (abstract) | 3.111 | 230 pc; CO(11–10) disc plus a point mass (black hole) | AGN-dominated | — | — | — | **ILL-CONDITIONED** | — |
| ref | **Cosmic Eyelash** (z 2.326, below band): Swinbank+11, arXiv:1110.2780 (abstract) | −1.0 | V 320 ± 25, v/σ 3.5, M_dyn 6.0e10 inside 2.5 kpc | y_obs 14 | CO(6–5)/(1–0) | — | — | ILL-CONDITIONED | reference only |
| ref | **J0901+1814** (z 2.259, below band): Sharon+19, arXiv:1905.09845 (page); Liu+23, arXiv:2211.08488 (abstract) | +18.2 | ≈ 600 pc ALMA CO(3–2) + Hα forward model; v_circ ≈ 260, r₁/₂ ≳ 4 kpc; "baryon-dominated" | y_obs ≈ 5.5 | CO(1–0)/(3–2) | — | — | ILL-CONDITIONED | reference only (whether J0901 is in RC100: **UNVERIFIED**) |

**Reading.**
- The band splits cleanly in two:
  - massive, gas-measured discs reach y_bar ≈ 2–5 at best (ADF22.1, the Big Wheel);
  - low-mass LBGs reach y ≲ 0.3 but have no gas and are pressure-dominated.
- Nothing links the two populations in one calibration. That is exactly the design CFG240 says cannot separate f from a₀.

## KDS × AMAZE/LSD repeat measurements (an empirical velocity-systematics control; `cfg268_y_estimates.out`)
| AMAZE/LSD | KDS | separation | Δz | velocities |
|---|---|---|---|---|
| CDFS-14411 (rotating) | lbg_109 (DD) | 0.47″ | 0.001 | V_max 69 against V_C 53 (σ_int 91) |
| CDFS-16767 (rotating, V unconstrained, i fixed at 15°) | lbg_113 (DD) | 0.76″ | 0.002 | **V_max 623 against V_C 41** |
| CDFS-4414 / 4417 (not rotating) | b012141_012208 (**RD**) | 1.31″ / 0.56″ | 0.000 / 0.002 | KDS V_C 93 |
| CDFS-6664 (not classified) | lbg_124 (DD) | 0.33″ | 0.003 | KDS V_C 32 |
| CDFS-16272 (not classified) | lbg_112 (DD) | 0.45″ | 0.002 | KDS V_C 63 |
| CDFS-11991 | lbg_111 | 1.29″ | **0.052** | different objects (Δz excludes the match) |

Two instruments observed the same z ≈ 3.5 LBGs at similar seeing. They disagree on the classification in 2 of 3 classified pairs, and on V by a factor of 15 in one. Any lane on these sets must carry an instrument-to-instrument velocity term, not the quoted errors alone.

## Shortlist: at most 3 lanes, each with the download it needs (the owner's go required; nothing fetched)
### S1. ADF22.1 [CII] curve plus CO(1–0) plus JWST: a one-off envelope
- **What it replaces.** It supersedes CFG272's ALPAKA 23 row, the same galaxy; it is not a new point.
- **Why it is worth a lane.**
  - It is the only z 2.5–4 disc with a lowest-J measured gas line.
  - It has a multi-ring curve to ≈ 3.5 R_d and a JWST stellar profile.
  - Its outer y_bar ≈ 2–5 is as close to the transition as ALESS 122.1.
- **What it cannot do.** Separate FLAT from a₀ ∝ H(z): it is one object with y_min ≈ 2 (CFG240).
- **What the envelope is expected to depend on.**
  - α_CO across 0.8–4.6 moves y_bar by a factor of 2.
  - The AGN-host SED mass.
  - The pressure correction: σ ≈ 60 km/s is small against V = 530 km/s.
- **Downloads:**
  - D1: arXiv e-print 2604.07440, 3.84 MB (HEAD content-length 3,838,036 bytes). Its figures are used to digitise the circular-velocity curve; whether Fig. 8 is a vector figure is **UNVERIFIED**.
  - D2: arXiv e-print 2410.22155, 6.84 MB. Its Fig. 6 gives the curve at 0.2″ and 0.9″, plus CO(1–0) and the SED.
  - D3, optional, only if the figures are raster or an independent re-derivation is wanted: ALMA 2021.1.01406.S MOUS uid://A001/X1590/X712 product tar, **2.43 GB** (0.16″ [CII]), plus X714, 0.26 GB.

### S2. KDS + AMAZE/LSD: the z ≈ 3–3.8 LBG tables (stars-only upper bounds and floors; repeat-measurement control)
- **Why it is worth a lane.**
  - It is the only multi-galaxy set in the band with per-galaxy V, R and M\* printed: 32 + 11 rows, 5 overlapping.
  - It is never treated as an a₀ data set in the record.
  - Its fields are ALMA-reachable, so a later gas follow-up is possible.
- **Expected outcome (honest).**
  - Mostly floor rows and vacuous bounds: in 25 of 32 KDS rows the stars alone exceed the rotation-only g_obs.
  - The pressure term exceeds V² in 29 of 32 rows, so the result hinges on an unmodelled pressure correction at V/σ < 1.
  - The useful product is an empirical instrument-to-instrument velocity error at z ≈ 3.5, and a measured size of that pressure systematic.
- **Downloads:**
  - D4: arXiv e-print 1704.06263, **6.68 MB**;
  - D5: arXiv e-print 1007.4180, **0.83 MB**.
  - Both only to verify the transcription in `cfg268_y_estimates.py` against the TeX tables. No archive data needed.

### S3. The Big Wheel: run after 2026-12-17 (when 2025.1.00107.S becomes public)
- **Why it is worth a lane.** y_bar ≈ 2–4 at 10 kpc with a measured CO line, at z = 3.25.
- **Why wait.** The public data have a ≈ 9 kpc beam (1–2 independent radii).
- **Caveats.**
  - The inclination alone moves g_obs by +72% / −27%.
  - The SED and dynamical stellar masses disagree by 0.37 dex.
- **Downloads:**
  - D6 now: arXiv e-print 2605.04144, **3.84 MB**;
  - D7 after 2026-12-17: ALMA 2025.1.00107.S MOUS uid://A001/X3833/X5839 product tar, **30.27 GB** (0.24″ CO(4–3)).

### Not recommended for a lane (and why)
- **SDP.81:** interacting, stars offset from the gas, y ≥ 3.
- **Cosmic Eye:** compact and of unknown inclination; its 60.51 GB archival CO is the one "overlooked" dataset, but y stays ≳ 1–3.
- **GN20:** outside the band, no ALMA, and its α_CO is dynamically derived.
- **MQN01-QC, the SPT DSFGs, ALESS 3.1/9.1, arc&core, W2305-0039:** Newtonian, AGN-dominated, or not resolved into rings.
- **PKS 0529-549:** already CFG275.
- **MOSDEF:** no per-galaxy table.
- **KLEVER:** no kinematics published.

## What would change a verdict
- **A CONDITIONED+GAS case at z 2.5–4 needs one of two things:**
  - **(i)** a sample of low-mass, extended discs (M\* ≲ 10^9.5) with resolved curves to ≳ 3 R_d AND a gas tracer measured per galaxy. No such sample exists. The nearest are KDS/AMAZE (no gas, seeing-limited) and GS_4891 (one radius).
  - **(ii)** an external calibration prior of ≲ 0.15 dex on the baryons at z ≈ 3. Not available (PAPER38; `data_assembly/GAS_ANCHOR_SCOPING_2026-09-30.md`).
- **Not a substitute:** the SSA22 CO(1–0) census (12 detections at z = 3.09) is a gas-calibration resource, not kinematics.

## Not verified or still open
- The Cosmic Eye's v sin i ≈ 55 and σ ≈ 54 (secondary source), and the α_CO behind its 2.4e9 gas mass.
- Troncoso+14 gas fractions (AMAZE).
- Birkin+21 and ASPECS kinematic details.
- VUDS resolution.
- The MOSDEF field list (page) and data availability.
- The line content of the archival Band 8 / Band 3 programmes (2019.1.00471.S, 2023.1.01354.S, 2019.1.01642.S).
- Whether Rizzo+26 Fig. 8 and Quadri+26's curve are vector figures.
- Reduced KDS cubes at ESO.
- Whether J0901 is in RC100.
- Lemoine-Busserolle+10 (not checked).
- A KLEVER kinematics paper after 2022: none found by search.
- GS_4891 ALMA coverage.
- The AMAZE RA precision (0.1 s) makes the 1.29″ CDFS-11991 match ambiguous; Δz rejects it.
- **What the y estimates assume:**
  - a thin exponential disc (Freeman), with R_d = R₁/₂/1.678 or the paper's scale radius;
  - the gas scale set equal to the stellar scale where none is published (ADF22.1);
  - a Hernquist sphere for PKS 0529-549's n ≈ 5.6 stars;
  - spherical enclosed mass where only M_dyn(< R) is given.

## Files and exact re-run commands
- `SCOPING.md` (this file).
- `cfg268_y_estimates.py`: conditioning estimates plus the KDS × AMAZE cross-match.
  - Outputs: `cfg268_y_estimates.out`, which passes C1–C5 (exit 0); and `cfg268_y_estimates_MUTATE1.out`, where MUTATE=1 swaps the disc for a point mass and C1 fails (exit 1, as required).
- `cfg268_alma_price.py`: read-only ALMA TAP and DataLink pricing.
  - Outputs: `cfg268_alma_price.out` and `.csv`, which pass C1–C2 (exit 0); and `cfg268_alma_price_MUTATE1.out` / `.csv`, where MUTATE=1 shifts every position by +1° in Dec and C1 fails (exit 1).
```
cd campaign_fresh_gravity/CFG268_z25_4_gap_scoping
python3 cfg268_y_estimates.py > cfg268_y_estimates.out; MUTATE=1 python3 cfg268_y_estimates.py > cfg268_y_estimates_MUTATE1.out
python3 cfg268_alma_price.py > cfg268_alma_price.out;  MUTATE=1 python3 cfg268_alma_price.py > cfg268_alma_price_MUTATE1.out   # network: ALMA archive metadata only
```
