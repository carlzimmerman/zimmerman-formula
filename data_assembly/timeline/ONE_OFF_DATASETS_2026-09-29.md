# One-off and unconventional data places not yet used (data front, 2026-09-29)

Abstract pages and search summaries only; nothing downloaded. Everything is **UNVERIFIED beyond the abstract** unless marked. The selection rule of
`ACCUMULATION_ROUTES_2026-09-29.md` applies: an item is worth chasing for what it can tell us (gas, radius, σ(R), pressure support), never for its offset.

## 1. Calibrating the pressure-support correction (the thing CFG140/141 turn on)
| resource | what the abstract states | use |
|---|---|---|
| Ubler+2021, arXiv:2008.05486 (TNG50 at z = 2) | 7 galaxies in 5 projections each; rotation speeds and dispersions from observational-style modelling "broadly consistent" with observations; more asymmetric curves than observed (large radial and vertical motions); line-of-sight velocity profiles differ by up to 200 km/s; the search summary says pressure-support effects were not very important under the Burkert+10 ansatz (from a snippet, not the abstract) | a simulation test of whether the constant-σ Burkert correction recovers V_c at cosmic noon; simulation data availability not stated |
| Bershady+2024, arXiv:2405.02460 (MaNGA asymmetric drift) | ~500 nearby discs; power-law exponent b_r decreases with radius above 10.4 dex in stellar mass, roughly constant below; in-plane σ_0,r 10–40 km/s | a local, measured check of radially varying dispersion and drift; z ≈ 0 only |
| arXiv:1908.05274 (dynamical masses from gas kinematics in simulated high-z galaxies) | found in a search; abstract not read | possible second simulation calibration |
| de Araujo-Carvalho+2025, arXiv:2507.10544 | surface-brightness dimming and lost resolution make cosmic-noon curves look smoother and more symmetric than the truth | direction of the bias on outer-curve quality |
| Sharma+2021, arXiv:2005.00279 | 409 KROSS galaxies, 237 with high-quality co-added curves, z 0.57–1.04, out to 6.4 disc scale lengths; an asymmetric-drift correction that changes the velocity by 10–87% | the size range of the correction at z ≈ 1 (already have the per-galaxy FITS, `sharma2024_gs21b.csv`) |

## 2. Gas
- **Herschel-based dust/gas** (Berta+2016, arXiv:1511.05147): at the deepest GOODS-S depth, dust masses at S/N ≥ 3 for main-sequence galaxies down to M* ≈ 1e10 only up to z ≈ 1, and at z ≤ 2 only at the tip of the main sequence or above. So Herschel cannot give gas masses for the KURVS discs (z 1.2–1.6, log M* 9.6–10.7 for most).
- **Stacking public 1.1 mm maps at all 22 KURVS positions** (GOODS-ALMA / ASAGAO): the standard way to reach fluxes below single-source detection. It needs the maps, not the catalogue, and I did not find them hosted (see `GOODSALMA_HOSTING_2026-09-29.md`). Needs a go for any download; the stack would be a mean flux, not a per-galaxy gas mass.
- **The ALMA archive itself:** archival Band 3/4 CO(2-1)/(3-2) or Band 6/7 pointings that cover the KURVS positions may exist as PI programmes outside the big surveys. A read-only archive footprint query at the 22 positions would tell; not run (needs a go; I do not know that a query interface is reachable from this machine).

## 3. High-z discs with published rotation curves
| resource | note |
|---|---|
| KGES (Tiley+2021) | reduced cubes of 288 star-forming galaxies at z ~ 1.5 in ECDFS, UDS, COSMOS (search summary). KURVS-CDFS targets are 20 of 22 KGES galaxies (per the KURVS paper), so KGES cubes overlap KURVS on the sky and give an independent, shallower σ(R) and V(R) for the same galaxies. Hosting not confirmed; a download needs a go |
| ALPINE kinematics, Jones+2021, arXiv:2104.03099 | [CII] rotation at z 4.4–5.9; rotation-curve shapes vary from flat to declining |
| Molina+2019 (arXiv:1906.06245), Ubler+2018 (arXiv:1802.02135) | one or two galaxies with CO and Hα; inner radii (see earlier note) |
| KAOSS, arXiv:2301.05720 | dust-obscured star-forming galaxies at z 1.3–2.6, kinematics; not read |
| arXiv:2411.08958 | one AGN host at z ≈ 2.6, regular rotation, mass models; not read |

## 4. A compilation to treat with caution
Flynn, arXiv:2605.25339, "High-z Kinematic Corpus Z1": 31 [CII] galaxies at z 4.26–5.68, 3DBarolo per-ring V_rot and σ (2–3 rings per galaxy), distributed as JSON/CSV/"RAG-ready" JSONL on Zenodo (10.5281/zenodo.20369285 and a corrected version 10.5281/zenodo.21834678). It is a single-author compilation of other people's data with a corrected release, so its provenance is one step away from the primary papers. **Do not use it as data**; if anything in it looks useful, go to the primary paper (ALPINE, CRISTAL, Roman-Oliveira) and check against the table we already parsed.

## 5. What needs the owner's go
1. A read-only ALMA-archive footprint query at the 22 KURVS positions.
2. Any KGES cube or map download (filename, source, size to be stated first).
3. Nothing else here requires a download.

## 6. Second hunt (later 2026-09-29; abstract pages only; seven rows appended to `sample_ledger.csv`)
- **MIGHTEE-HI, z > 0.25 (Jarvis+2025, arXiv:2506.11935):** 11 individually detected HI galaxies at z = 0.26–0.38 (highest z = 0.3841), the first bTFR with HI beyond z = 0.25; consistent with the local bTFR, with tentative flattening at high mass. This is the only individually HI-detected sample beyond z = 0.25 I found; the abstract gives no numbers and no data-release statement, so the tables in the paper must be read (HTML route, like GOODS-ALMA). Proposed tier: B candidate.
- **MXDF [OII] discs (Bouche+2022, arXiv:2109.07545):** 9 z ≈ 1 galaxies, log M* 8.5–10.5, rotation curves to ~3 R_e from 3D forward modelling; the gas is a model component. Low-mass discs at 3 R_e are low-acceleration if the gas is known.
- **ACE (Shivaei+, arXiv:2609.21604):** 25 z = 2.0–2.5 galaxies at log M* 9–10.5, 17 CO(3-2) and 17 Band 7 continuum detections: measured gas for low-mass, low-metallicity galaxies, but no dynamics in the abstract.
- **GA-NIFS DLA0817g1 (Jones+, arXiv:2512.05213):** the z = 4.26 disc (the Neeleman+2020 object on my earlier not-fetched list): Hα and [CII] rotation nearly identical, gas mass re-derived from metallicity plus CO and [CII].
- **Rybak+ (arXiv:2411.06474):** CO(1-0) in 19 z = 2–4.5 dusty galaxies with half-light radius 3.8 kpc, 2–3× more extended than the dust-obscured star formation; up to 80% of the gas outside the star-forming region. It bears on where the gas sits relative to the outer velocities, not on dynamics.
- **LEGA-C (arXiv:2203.06194)** and **MAGPI (arXiv:2406.20017):** intermediate-z kinematics with no gas measurement.
- **Context, not data:** Lelli+ (arXiv:2608.07290) is a forward-looking paper on SKA HI rotation curves out to z ~ 1, with no results; Lang+2017 (arXiv:1703.05491, 101 galaxies) and Genzel+2017 found declining outer curves at z = 0.6–2.6; Nelson & Williams (arXiv:2401.13783) argue that steeply falling curves would imply no dark matter; the python package RotCurves (arXiv:2601.08348) models high-z rotation curves. None of these was read beyond the abstract.

## 7. Third hunt (later 2026-09-29; abstract pages only; six rows appended to `sample_ledger.csv`)
- **Girard+2021, arXiv:2101.04122:** for 9 DYNAMO discs and 12 z ~ 0.5–2.5 galaxies, the resolved molecular-gas velocity dispersion is lower than the ionised-gas dispersion by a factor 2.45 ± 0.38 after thermal correction, and the offset is constant within the disc; the authors read it as a thin molecular and a thick ionised disc, and molecular-gas pressures are ~0.22 dex lower. This bears directly on the pressure-support question: the Hα dispersion used in Burkert-type corrections (as in KURVS) is the ionised-layer value.
- **Wisnioski+2025, arXiv:2505.24129:** a literature compilation of 237 discs at z = 0.5–8 (63 with molecular gas fractions) that states ionised dispersions are ~2× the molecular ones at fixed gas mass and shows minimal evolution between z ≈ 1.5 and 8. A compilation, so go to the primary papers before using any number.
- **DYNAMO (White+2017, arXiv:1707.07005; Fisher+2014, arXiv:1405.7410):** z ≈ 0.1 clumpy turbulent discs with measured CO(1-0) gas fractions (~20%), Hα IFU kinematics (mean ionised σ ≈ 50 km/s) and a linear relation between f_gas and σ/v_c: a low-redshift test bed with measured gas for the pressure-support correction.
- **Übler+2019, arXiv:1906.02737:** 175 KMOS3D discs, σ₀ ≈ 45 km/s at z ≈ 2.3 falling to ≈ 30 km/s at z ≈ 0.9; the abstract has no radial profile.
- **PHIBSS2 z = 0.5–0.8 (Freundlich+2019, arXiv:1812.08180):** 61 galaxies with 60 CO(2-1) detections, measured molecular gas masses, HST disc sizes and B/T; kinematic content and the table were not read. Proposed tier: B candidate (gas only).
- **CO Tully–Fisher (Topal+2018, arXiv:1806.06272):** 25 isolated galaxies at z ≤ 0.3, baryonic-mass CO TFR log M_b = (4.9 ± 2.8)[log(W₅₀/sin i) − 2.5] + (10.2 ± 0.5), no significant evolution since z = 0.3; the paper carries four tables.

## 8. Fourth hunt (later 2026-09-29; abstract pages only; five ledger rows appended)
- **PKS 0529-549 (z ≈ 2.6):** Lin+ (arXiv:2411.08958) get a flat [CI](2-1) rotation curve to 3.3 kpc at 0.18″ (V/σ = 6 ± 3) and say the dynamical gas and stellar masses from the rotation-curve fit are inconsistent with the photometric estimates; Huang+ (arXiv:2411.04290) measure ~10¹¹ M☉ of molecular gas by three methods that differ by up to a factor 4. One object, but a measured-gas rotation curve with a stated baryon inconsistency.
- **KLASS (Girard+2020, arXiv:2006.14633):** 44 lensed galaxies at 0.6 < z < 2.3, log M* 8.1–11.0; median v_rot/σ₀ ≈ 2.5; a stellar-mass Tully–Fisher offset of +0.18 dex versus local, read by the authors as more gas-rich galaxies. **KLENS (arXiv:1801.05816, search summary only):** 24 lensed galaxies at 1.4 < z < 3.5, a quarter rotation-dominated. Both are ionised-gas, low-mass and lensed.
- **SINS/zC-SINF AO (Förster Schreiber+2018, arXiv:1802.07276):** 35 galaxies, cubes on disk (6.3 GB, verified). The paper's tables (kinematic classes, dispersions, sizes) are the quick way in; not parsed yet.
- **MAGPI (Sharma+2026, arXiv:2601.12315):** f_DM ≈ 0.85 below M* = 10^9.5 and ≈ 0.47 above 10^10.5, a tight inverse correlation with baryon surface density, no evolution within 0.1 < z < 0.85 (abstract).
- **Per-galaxy tables available from the arXiv HTML** (found by structure only; contents not read): Price+2021 (arXiv:2109.02659), a 41-galaxy sample table (z, M*, SFR, M_gas, …) and a second table with M_bar, R_e, σ₀, f_DM, M_vir for each galaxy, plus Lang+2017 (arXiv:1703.05491, stacking sample table). These are the candidates for a table parse, each needing the owner's go.
