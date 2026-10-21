# Later NGC5023 HI evidence: bounded follow-up

Checked 2026-10-20. This is an additive source note. All frozen SPARC inputs, earlier manifests and inversion outputs remain unchanged. No cube was downloaded, no curve was digitized, and no new fit was run.

**A later resolved 3D HI model exists, with public observations. A directly reusable numerical radial model was not recovered in this bounded check.** Therefore the packet's positive-mass witness remains a result conditional on its frozen SPARC curve; its persistence under the later HI analysis is untested. Comparing against that analysis is a material next data obligation before a robust observational interpretation.

## Authenticated primary model and quantitative results

**Kamphuis et al. (2013)**, *HALOGAS observations of NGC 5023 and UGC 2082: modelling of non-cylindrically symmetric gas distributions in edge-on galaxies*, **MNRAS 434, 2069–2093**, DOI [10.1093/mnras/stt1153](https://doi.org/10.1093/mnras/stt1153). Checked full text: [arXiv:1306.5312v1](https://arxiv.org/pdf/1306.5312v1), submitted 2013-06-22. Publisher [article locator](https://academic.oup.com/mnras/article/434/3/2069/1033177) authenticates the journal identity; direct full-page access was blocked, so detailed extraction is pinned to v1.

The 20-ring TiRiFiC model fits the full cube, including a line-of-sight warp and spiral overdensities. Figure 12 presents radial rotation speed, inclination, position angle and HI density. Table 4 reports:

| Published quantity | NGC5023 result |
|---|---|
| Central inclination | 88.5 ± 1.3 degrees |
| Central position angle | 28.0 ± 1 degree |
| Rotation speed at `D_HI`, as captioned | 87.6 ± 5 km/s |
| Main **HI** disk scale height | 0.29 ± 0.10 kpc |
| Systemic velocity | 404.8 ± 4 km/s |

Table 1 adopts 6.6 Mpc and gives maximum rotation speed 89 km/s. Table 3's high-resolution fitted lag is −14.9 ± 2.7 km/s/kpc for the base model versus −9.4 ± 3.8 for the spiral model. Section 3.6 estimates parameter errors by varying one parameter while fixing others until clear disagreement; these are not a supplied joint Gaussian covariance. The HI height is not a stellar-height measurement. A vertical lag cannot simply be added to equatorial circular speed. The single tabulated speed is not a full replacement curve.

## Exact public data availability

The primary release is **George Heald, The Westerbork HALOGAS Survey: Data Release 1, version 2**, published **2020-03-20**, DOI [10.5281/zenodo.3715549](https://doi.org/10.5281/zenodo.3715549), [record](https://zenodo.org/records/3715549), [metadata API](https://zenodo.org/api/records/3715549). The API file inventory was inspected directly. It lists eight NGC5023 FITS products: high- and low-resolution cubes, plus column-density, integrated-intensity and mean-velocity maps for each resolution. The generic release resolutions are approximately 15 and 30 arcsec. Version 2 corrects NGC4448; the release states that other galaxies' products are unchanged.

| Public NGC5023 cube | Exact bytes | Release-advertised MD5 |
|---|---:|---|
| [NGC5023-HR-cube.fits](https://zenodo.org/records/3715549/files/NGC5023-HR-cube.fits?download=1) | 289422720 | `ac29e70c0b5a36b3941c266b2c935fad` |
| [NGC5023-LR-cube.fits](https://zenodo.org/records/3715549/files/NGC5023-LR-cube.fits?download=1) | 289422720 | `171c4d421e7d9d14662633912fdbf122` |

Each associated map is 4222080 bytes. Exact filenames, URLs and all eight checksums are retained in `LATER_HI_SOURCE_PINS.json`; these are catalog-advertised checksums, **not** hashes independently verified against downloaded FITS bytes. The mean-velocity map is an observational moment map, not a circular-speed table.

No rotation-curve ASCII, TiRiFiC `.def` parameter file, model cube or ring covariance is included in that release inventory. The exact arXiv v1 source archive was also inspected in memory: it contains TeX/BibTeX material and 22 PostScript figures, with no separate radial numeric model. Targeted searches for this paper's supplemental data, NGC5023 TiRiFiC definitions and VROT files recovered no direct numeric radial product. Publisher access limitations mean this is **not** a claim that no such product exists anywhere.

## Consequence and remaining bounded obligation

The later paper supplies a concrete independent kinematic comparison that the frozen 17-point analysis has not consumed. Its gas geometry and stellar geometry must remain distinguished. The next comparison needs the preferred model's angular ring radii, equatorial rotation speeds, radial geometry, HI density and error definition, ideally from the original parameter files. If only figures are available, digitization would require a separate provenance/error record; it was not performed here.

It would be premature either to replace all 17 speeds with 87.6 km/s or to infer a numerical change in the recovered surplus from the lag. This note establishes the available evidence and missing machine-readable bridge, not a revised inversion result or a reanalysis of the HI cube.

## New source pins and scope

- `LATER_HI_SOURCE_PINS.json`: SHA-256 of the fetched versioned arXiv PDF, metadata API response, response headers, and the retained API metadata/file inventory. Full paper PDF/text and FITS data were not retained.
- `LATER_HI_AVAILABILITY_PINS.json`: exact source-archive SHA-256 and member inventory; publisher access failure recorded.
- Main dataset and geometry authentication are unchanged. No `.mathbox` ledger, original dataset, owner process or Git state was changed. No global literature or novelty claim is made.

**Status:** source identity and extracted summary parameters verified; public cube availability verified by primary inventory; existence of a directly usable full radial replacement table remains unverified; application to the finite-source witness remains conditional and uncomputed.
