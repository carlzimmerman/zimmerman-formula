# CFG323: the SLUGGS law-only offset re-scored with measured tracers

**Frozen criteria:** `FROZEN_CRITERIA.md`, commit b2e7ec16d, sha256 `27184df9b3211b98d3f0c3137dd83879ee9fef29e02cc292580b759d2e21d0cd`. It was written after the owner-approved downloads ("yeah download the elliptical tables boss", orchestrator chat, 2026-10-03) and before any table value was read.

**Fixed inputs:** kernel ν_mono, κ = ½, both footings (9.36e-11 | 1.13e-10). No knob scans. CFG55, CFG57, CFG111, CFG313 and the audit are never edited.

## Bottom line

**The measured tracers barely move the offset. The frozen error budget, not the data, takes it below 3σ.**

### Primary result (the 16 galaxies)

| | mean (dex) | Z_stat | Z_sys | class |
|---|---|---|---|---|
| canonical | +0.0920 | 4.41 | **2.07** | WEAKENED |
| alt | +0.0826 | 4.01 | **1.85** | NOT SIGNIFICANT |
| audit baseline, canonical (γ = 3, β = 0, no gas) | +0.0977 | 4.02 | — | — |

The primary uses measured GC density profiles for 4 of the 16 galaxies, γ = 3 for the rest, isotropic orbits, and the measured gas.

### Frozen verdict (rule (e), the weaker footing): **NOT SIGNIFICANT** [measured-tracer coverage 4/16]

The verdict is fragile, and depends on two things:
- **NGC 1023's Sérsic index.** Kartha+14 gives n = 3.15 ± 2.85. The n − 1σ = 0.30 profile moves NGC 1023 by 0.46 dex, which is σ_meas = 0.029 on the 16. Without that one term, Z_sys is 2.73 canonical and 2.44 alt: **WEAKENED on both footings**. These are reported rows, not decision rows.
- **The shared ±0.5 γ systematic on the 12 unmeasured galaxies.** It contributes 0.026, comparable to the statistical error of 0.021.
- The statistical-only significance stays at **4.0–4.4σ**.

### Pre-stated centrals split

| | mean (dex) | Z_stat | Z_sys | class |
|---|---|---|---|---|
| without the 4 centrals (N = 12), canonical | +0.062 | 2.96 | 1.21 | NOT SIGNIFICANT |
| without the 4 centrals (N = 12), alt | +0.053 | 2.56 | 1.03 | NOT SIGNIFICANT |
| the 4 centrals (4486, 4365, 4374, 5846), canonical | +0.182 | 10.8 | 4.8 | FAIL CONFIRMED |
| the 4 centrals, alt | +0.171 | 9.7 | 4.4 | FAIL CONFIRMED |

**Honest wording:** the outer-GC deficit is still positive at +0.08 to +0.09 dex with measured tracers and gas. It is carried by the four group/cluster centrals. With the frozen tracer-systematic budget it is not significant on the weaker footing and 2.1σ on the canonical one. It is not removed.

## What the measured tracers did (canonical, per galaxy; audit baseline → primary)

**NGC 1023** (Kartha+14, R_e = 1.00′, n = 3.15): +0.104 → **+0.153**.
- The deprojected slope steepens to γ = 3.0 / 3.4 / 4.1 at the outer bins, which makes the deficit *worse*.

**NGC 2768** (Kartha+14, R_e = 1.66′, n = 3.09): −0.004 → +0.019.
- γ = 2.6 / 3.0 / 3.4.

**NGC 3607** (Kartha+16, MA method, R_e = 1.99′, n = 1.97): +0.028 → +0.032, including Fukazawa gas.
- With the SB method instead: +0.021.

**M87 / NGC 4486**: +0.275 → **+0.131**.
- Tracer: Agnello+14's three-population Sérsic sum. The blue population has R_e = 2300″ = 186 kpc, so the deprojected γ is about 1.9–2.3 at the GC bins. This shallow tracer raises the predicted dispersion, so the offset goes from +0.275 to +0.218 with no gas.
- Gas: Lakhchaura D1 to 28 kpc, then Churazov+08's measured β-model to 48.6 kpc, which takes the offset to +0.131.
- Beyond 48.6 kpc the gas is EXTRAPOLATED (the β-model continued).
- With the Zhu+14/Peng+08 single total Sérsic (PROVISIONAL, text) instead of Agnello's sum: +0.210.

**Anisotropy:** no downloaded paper tabulates β for a galaxy in the 16, so the primary is isotropic everywhere.
- Text values, reported as PROVISIONAL, change M87 by only −0.007 to −0.010 dex:
  - Agnello+14: intermediate population β ≈ 0.3.
  - Zhu+14: β(r) from −0.2 to +0.2 to 0.
- The ±0.5 bracket gives σ_β = 0.003.

**Gas alone** (γ = 3 everywhere) moves the mean by 0.006 dex (+0.0977 → +0.0913). Almost all of that is M87 (+0.275 → +0.199). The other six covered galaxies each move by ≤ 0.018 dex.

## Pre-stated secondaries
- **S1** (local power law at each bin radius): Z_sys 1.62 canonical / 1.40 alt. It is flagged **PRIMARY/S1 DISAGREE** on the canonical footing; the primary decides.
- **S2** (profiles truncated at the published GC-system extents): Z_sys 2.16 / 1.95.

## Controls (8/8 across both runs: main 7/7, MUTATE 8/8)

| ID | Result |
|---|---|
| C1 | Audit baseline reproduced exactly: +0.0977 / +0.0885 (4.02σ / 3.67σ). |
| C2 | The general-profile Jeans code with ρ ∝ r⁻³ reproduces the audit per galaxy to 1.6e-14 dex. |
| C3 | Abel deprojection of a Plummer profile: slope error 5.7e-6. |
| C4 | Numerical deprojected slope at 3 R_e,GC vs Prugniel–Simien: max difference 0.016 over 8 profiles. No published power-law index exists for these profiles: Kartha's α is only a symbol in the azimuthal fit. |
| C5 | Script transcription row counts and spot values. |
| C6 | Gas-zero path identical to C2. |
| P1 | Row gap (post-freeze, provenance). |
| M1 | MUTATE (cyclic shuffle of the measured profiles in units of R_e,gal) moves the measured-subset mean by +0.0133 dex. This passes the ≥ 0.01 threshold narrowly. The verdict class is unchanged (NOT SIGNIFICANT), with ALL Z_sys at 1.94 / 1.75. |

## Row gap (3,575 vs 4,492): resolved

- The VizieR galaxy table's `N` column is "Number of galaxy data in tables 2–5" (J/AJ/153/114 ReadMe). The 4,492 counts four tables: 865 contaminants + 21 neighbour galaxies + 33 UCDs + 3,573 GCs (Table 5, from the erratum AJ 154, 80).
- The on-disk velocity file has **3,573** data rows. The audit's "3,575" also counted the TSV's column-name and units lines; the dashes line accounts for the remaining non-blank line.
- Per galaxy, it matches Forbes+17 Table 6 N_GC for 26 of 27 galaxies. NGC 4365 has 244 rows against 245.
- **No GC velocities are missing.**

## Disclosed departures and choices made after the freeze

1. **Lakhchaura gas.** The frozen text names "CFG57's D1 conventions", but its parenthesis described only the outer power law. D1 also *drops the upturned outermost shell*, and that is what is implemented.
   - Keeping the shell (CFG57's mechanical rule) gives unbounded gas and nonsense offsets: NGC 4374 −2.17, M87 −2.90, NGC 5846 −2.31 dex. This is printed as a reported row, as in CFG57.
2. **NGC 3607 SB vs MA method.** The frozen text did not choose. MA is primary because it is the paper's total-system curve in its Fig. 8. SB is reported: ALL changes by 0.0007 dex.
3. **M87 priority.** Agnello+14's population sum is used over Zhu+14's single total Sérsic, as the frozen M87-specific priority says. Zhu is reported.
4. **Zhu+14's b_n = 2.21 is read as log10.** Its ln-equivalent, 5.089, matches the Ciotti–Bertin value 5.091 for n = 2.71.
5. **The fragility rows and P1 were added after the first run.** They are reported only.

## Files and run commands

| File | Content |
|---|---|
| `cfg323_measured_tracers.py` | The lane script (~50 s). It execs the audit's source read-only up to its headline block. |
| `cfg323_measured_tracers.out`, `_results.json` | Main run, 7/7 checks. |
| `cfg323_measured_tracers_MUTATE.out`, `_MUTATE_results.json` | MUTATE run, 8/8 checks. |
| `cfg323_transcribed_values.tsv` (`_MUTATE` copy) | Every value parsed by script from the downloaded LaTeX. Zhu+14 values and all β text values are PROVISIONAL. |
| `cfg323_fetch.py` | The capped, logged fetch helper: VizieR/CDS + arXiv only, 50 MB total cap, 10 MB per-file cap. |
| `FETCH_LOG_CFG323.md`, `FETCH_MANIFEST_CFG323.jsonl` | The fetch log. |

```
python3 campaign_fresh_gravity/CFG323_sluggs_measured_tracers/cfg323_measured_tracers.py
CFG323_MUTATE=1 python3 campaign_fresh_gravity/CFG323_sluggs_measured_tracers/cfg323_measured_tracers.py
```

Run the main run first: MUTATE reads its verdict class.

## Fetch manifest

- Files are stored under `../_external_data/sluggs_tracers/`, outside the repo; paths are relative to the repo root.
- Total: **24,662,000 bytes** (cap 50 MB).
- The arXiv size checks (`curl -I`, headers only, no body) are not logged.
- The arXiv API queries were rate-limited (429/503). Their error bodies are logged, and paper IDs were found by web search instead.

| label | url | file | bytes | sha256 | status |
|---|---|---|---|---|---|
| ReadMe J/MNRAS/428/389 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/428/389/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_428_389_ReadMe | 8,307 | 643df794ea515903cf170b2dc910b6c161745cf15fa28b30af058aca123b826f | http 200 |
| ReadMe J/AJ/153/114 | https://cdsarc.cds.unistra.fr/ftp/J/AJ/153/114/ReadMe | ../_external_data/sluggs_tracers/readme/J_AJ_153_114_ReadMe | 8,258 | 161533382c9f1e01559b422646d46187ca74f6780831c4aaec9dc63589fe2459 | http 200 |
| ReadMe J/AJ/154/80 | https://cdsarc.cds.unistra.fr/ftp/J/AJ/154/80/ReadMe | ../_external_data/sluggs_tracers/readme/J_AJ_154_80_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| ReadMe J/MNRAS/437/273 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/437/273/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_437_273_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| ReadMe J/MNRAS/458/105 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/458/105/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_458_105_ReadMe | 5,974 | 5a3798e636ce8d91d8cf1f2ffcfc572d42c32ea2ff37d9c72658fd29235077d7 | http 200 |
| ReadMe J/ApJ/792/59 | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/792/59/ReadMe | ../_external_data/sluggs_tracers/readme/J_ApJ_792_59_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| ReadMe J/MNRAS/450/1962 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/450/1962/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_450_1962_ReadMe | 5,211 | e41ef74cdff174522e7ed16dd5e48139d7f79e7212c6aac0536be4e50fbd9c1b | http 200 |
| ReadMe J/ApJ/857/32 | https://cdsarc.cds.unistra.fr/ftp/J/ApJ/857/32/ReadMe | ../_external_data/sluggs_tracers/readme/J_ApJ_857_32_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| ReadMe J/MNRAS/442/3299 | https://cdsarc.cds.unistra.fr/ftp/J/MNRAS/442/3299/ReadMe | ../_external_data/sluggs_tracers/readme/J_MNRAS_442_3299_ReadMe | 283 | f5a8d05b5522789f86414a523fb831d1a9c6969437c4053644d4d092a6ea84ae | http 404 |
| arXiv API search 1 | http://export.arxiv.org/api/query?search_query=au:Pota+AND+ti:SLUGGS+AND+ti:2500&max_results=8 | ../_external_data/sluggs_tracers/arxiv_api/q1.xml | 14 | 467622e2f17f01d302d6c790b13078569f17d71cd83910558535019a594e07c1 | http 429 |
| arXiv API search 2 | http://export.arxiv.org/api/query?search_query=au:Kartha+AND+ti:SLUGGS&max_results=8 | ../_external_data/sluggs_tracers/arxiv_api/q2.xml | 126 | c00c6211c3a751584bab0a350d56272b60172019c648cf74a73ae4f9f319602e | http 503 |
| arXiv API search 3 | http://export.arxiv.org/api/query?search_query=au:Zhu_L+AND+ti:M87+AND+ti:globular&max_results=8 | ../_external_data/sluggs_tracers/arxiv_api/q3.xml | 14 | 467622e2f17f01d302d6c790b13078569f17d71cd83910558535019a594e07c1 | http 429 |
| Kartha+14 arXiv source | https://arxiv.org/e-print/1310.1979 | ../_external_data/sluggs_tracers/arxiv_src/1310.1979.tar.gz | 2,392,452 | 338b6c2c49aec75a329717503b25c25c611a2f76a0e66416fe0eda6692bb54d7 | http 200 |
| Kartha+16 arXiv source | https://arxiv.org/e-print/1602.01838 | ../_external_data/sluggs_tracers/arxiv_src/1602.01838.tar.gz | 1,195,136 | f9ac8de6101b241aef2a63a7ffb5aaf483e20648915ff1e444a6bb783a692f98 | http 200 |
| Zhu+14 arXiv source | https://arxiv.org/e-print/1407.2263 | ../_external_data/sluggs_tracers/arxiv_src/1407.2263.tar.gz | 3,166,898 | bed11ae3abfa903d45861b361f748dd27de2dc172d6b4e5965a0acc8edd9ad7e | http 200 |
| Agnello+14 arXiv source | https://arxiv.org/e-print/1401.4461 | ../_external_data/sluggs_tracers/arxiv_src/1401.4461.tar.gz | 5,756,997 | 6c5514ad7df038a19e09f2cb4efc1ce19d925b88a82074c79078cdcbbef0f3fa | http 200 |
| Pota+15_N1407 arXiv source | https://arxiv.org/e-print/1504.03325 | ../_external_data/sluggs_tracers/arxiv_src/1504.03325.tar.gz | 2,133,751 | a0540da3d59a3699ff65e4756edac50509a6bec1d7ef30f2453a720830840f5d | http 200 |
| Forbes+17 arXiv source | https://arxiv.org/e-print/1701.04835 | ../_external_data/sluggs_tracers/arxiv_src/1701.04835.tar.gz | 603,617 | b205da3fa1a09264744ea0a2b960d4afe129b4a875218f1244b1859f0ff63dad | http 200 |
| Churazov+08 arXiv source | https://arxiv.org/e-print/0711.4686 | ../_external_data/sluggs_tracers/arxiv_src/0711.4686.tar.gz | 1,706,749 | 559ebdaee1201efe86d8fe4441c2e252d333cb4263eab0dd355f90fc5f6cc6e8 | http 200 |
| Urban+11 arXiv source | https://arxiv.org/e-print/1102.2430 | ../_external_data/sluggs_tracers/arxiv_src/1102.2430.tar.gz | 511,781 | b128f249be70b31f1222743fd4ada7576b00424655dabc76b009d2c578320d34 | http 200 |
| Pota+13 arXiv source (expected >10MB) | https://arxiv.org/e-print/1209.4351 | - | 0 | - | FAILED rc=56 http=200 curl: (56) Maximum file si |
| Pota+13 arXiv HTML (source >10MB skipped) | https://arxiv.org/html/1209.4351 | ../_external_data/sluggs_tracers/arxiv_html/1209.4351.html | 741,559 | 27a09b83f0861c1f29021a9b7cbc45889855cf7d531df5f31ee1dac28dc8571c | http 200 |
| Babyk+18 arXiv source | https://arxiv.org/e-print/1802.02589 | ../_external_data/sluggs_tracers/arxiv_src/1802.02589.tar.gz | 6,423,741 | b4a329d1333ef4353b716d38d0d4dfd55fe8ed26c466778fc3d101fe90722643 | http 200 |

### Not available, or not machine-readable

- **Pota+13 source tarball (11.8 MB):** over the 10 MB per-file cap, so it was skipped. The arXiv HTML was fetched instead. Pota+13 tabulates **no** GC density fits: its Sérsic or power-law fits appear only in Fig. 6.
- **VizieR has no density-profile, anisotropy or gas tables for these papers.**
  - J/MNRAS/428/389 (Pota+13) and J/MNRAS/458/105 (Kartha+16) are velocity/photometry catalogues.
  - J/MNRAS/450/1962 is Pota+15's **M60** catalogue, not NGC 1407.
  - J/AJ/154/80, J/MNRAS/437/273, J/ApJ/792/59, J/ApJ/857/32 and J/MNRAS/442/3299 return 404.
- **Anisotropy appears only in figures or text:**
  - Agnello+14 (M87): posteriors in its Figs. 8–9.
  - Zhu+14: β(r) figure.
  - Pota+15 (NGC 1407): β is not scorable, because NGC 1407 has no ATLAS3D JAM. Its source was downloaded and is unused.
  - No SLUGGS β table for NGC 4365, 4374 or 5846 is in the approved papers. Napolitano+14 (NGC 5846, arXiv 1401.1501) is outside the approval.
- **Gas:**
  - Babyk+18 (arXiv 1802.02589; ApJ 862, 39) tabulates only the sample and global entropy fits. It has no per-galaxy gas masses.
  - Urban+11 gives n_e ∝ r^-1.21 with no tabulated normalisation (figure only).
  - Churazov+08's analytic n_e(r) is the only numerical M87 profile beyond 30 kpc.
- **Hargis & Rhode** and **Alabi+16** (per-galaxy GC slopes used in tracer-mass estimators) were not fetched, because they are outside the named approval. Alabi+16 would cover most of the 12 unmeasured galaxies, so it is the obvious next fetch if the owner approves.
