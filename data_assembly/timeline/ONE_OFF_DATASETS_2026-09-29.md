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
