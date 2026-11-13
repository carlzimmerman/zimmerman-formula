# Complete ECLIPSE–SILO coordinate crossmatch

The requested **15072 ECLIPSE-screen objects × 1551 SILO DR16 detections** yield **three pairs within 2 arcsec**, with no additional pair between 2 and 10 arcsec. These supply candidate foreground/background redshift associations, but every matched ECLIPSE object currently has an unsuccessful released lens model and lies outside the prior final sample. They are follow-up targets, not immediately usable precise gravity tests.

| ECLIPSE ID | Separation | Foreground z | Background candidate z | SILO spectrum / total grade | Euclid imaging grade |
|---|---:|---:|---:|---|---|
| L002777 | 0.04774 arcsec | 0.32741600 ± 0.00007120 | 0.97136903 | A / A | A |
| L001244 | 0.25188 arcsec | 0.52200198 ± 0.00033281 | 1.42531312 | B+ / B+ | A |
| L013442 | 0.36962 arcsec | 0.57596397 ± 0.00024684 | 1.36356688 | C / C | B |

The exact values, complete SILO inspection comments, SDSS plate/MJD/fiber identifiers and source-context fields are retained in [result.json](run_01/result.json). No source-redshift errors are supplied by these fixed metadata fields; none are invented here. All three have `ZWARNING_NOQSO=0` for the foreground galaxy, which does not independently validate the background source identification.

L002777 is the strongest spectral-quality follow-up. Its released model has success fraction zero, n≈1.345, circularized Re≈0.648 arcsec and q≈0.299; those rejected-fit outputs must not be used for a theory bound. It has a conditional SED mass summary log10 M=11.3713293 with offsets -0.0692497/+0.0698157 and a catalogue photo-z of 0.41. **The redshift actually used for this object's SED fit is unverified**; the photo-z column alone does not establish it, because the pipeline can use available spectroscopy. Its raw-download key is `Tile102157516RA1412954672915DEC0634238492404`. L001244 and L013442 have no SED mass in the current screen. Even the A-grade SILO comment discusses line/sky ambiguity, so the source association should be audited before a full image fit.

The raw ECLIPSE object archive contains **26662 distinct objects**, a different population from the 15072-row screen. A separate complete match adds two objects, both Euclid imaging grade C: L015442 (0.04895 arcsec; foreground z=0.3434090, candidate source z=0.8120401, SILO multi-line A−) and L005949 (0.42496 arcsec; foreground z=0.5748940, candidate source z=1.0595281, SILO single-line B−). Their raw-archive status is reported separately; they were not silently counted in the requested screen.

## Source and column audit

The [official SDSS DR16 VAC page](https://www.sdss4.org/dr16/data_access/value-added-catalogs/?vac_id=eboss-strong-gravitational-lens-detection-catalog) points to SILO version 1.0.1, and [Talbot et al. (2021)](https://doi.org/10.1093/mnras/stab267) describes 1551 candidates, including 1263 single-line and 288 multi-line detections. The downloaded metadata reproduce these counts, all 838 spectrum grades A− or better, and all 919 combined grades A− or better. These grades express candidate assurance; this is not a catalogue of uniformly confirmed lenses.

The [official data model](https://data.sdss.org/datamodel/files/EBOSS_SPECTRO_LENSING/silo/RUN2D/RUN1D/SILO_VER/silo_eboss_detections.html) defines `DETECTION_Z` as the background-candidate redshift, `Z_NOQSO` as the foreground target's preferred non-QSO fit, `ZERR_NOQSO` as its uncertainty, and separate spectral and combined imaging/spectral grades. Its HTML incorrectly labels numeric RA as hours. The **actual FITS header specifies degrees**, and comparison of all 1551 numeric coordinates against `RA_HMS`/`DEC_DMS` confirms degrees, with maximum rounding difference 0.11846 arcsec. The crossmatch uses the numeric degree columns. The stored ten-character string `Single-lin` is the truncated single-line search label.

There are 1551 unique detection IDs but 1545 unique coordinate pairs; no duplicate-coordinate or quality-grade entries were discarded. All background-candidate redshifts exceed their foreground redshifts. Source candidates sharing target positions remain separate rows.

## Download and computation provenance

Only **5263206 bytes** were fetched from the 323112960-byte FITS file, using a verified HTTP 206 byte range `0-5263205`. This includes the complete primary/header material and **all 1551 fixed rows**, each 3386 bytes starting at offset 11520. The 314832276-byte variable spectral-array heap was deliberately not fetched. The expected Astropy truncated-file warning refers to the absent heap; the selected fixed fields are complete, and a second `struct` decoder independently reproduces every coordinate and both redshift columns. No spectral heap pointers are dereferenced.

The [bounded fetch utility](fetch.py) records URL, UTC, HTTP headers/status, Content-Range, byte count and SHA256 in neighboring `.provenance.json` files. Initial sandbox DNS failures and a Strasbourg metadata timeout are retained as failed attempts. The successful SAS transfer and CfA VizieR transfer have distinct artifacts; none are represented as successful by assumption. The SL2S table fetched here is handed to the separate `external_sl2s_match` audit and is not folded into these SILO counts.

The [contract](contract.json), [script](crossmatch_silo.py), [manifest](run_01/manifest.json), [all fixed SILO metadata](run_01/SILO_all_fixed_metadata.csv), and [nearest candidate for every screened ECLIPSE object](run_01/nearest_per_ECLIPSE.csv) make the result reproducible. The bounded run completed and its v2 manifest validates with input/output hashes unchanged. A unit-vector tree match was independently checked against **all 23376672 great-circle pairs** using direct haversine evaluation; every pair within 10 arcsec agrees, and the largest nearest-distance difference is 8.74e-11 arcsec. The nearest nonmatch in the primary screen is 152.38 arcsec away, so no borderline 2–10 arcsec candidates were lost.

The verified assertion is this finite catalogue/coordinate crossmatch. A positional match does not by itself validate a lensed-image correspondence, remeasure a spectrum, establish a stellar mass, or support a theory exclusion. Absence statements apply only to the explicitly named catalogues, populations and match radius.

## Supplementary MaNGA SILO check

The [official DR17 MaNGA VAC](https://www.sdss4.org/dr17/data_access/value-added-catalogs/?vac_id=manga-strong-gravitational-lens-candidates) recommends version 1.0.4. Its complete 8354880-byte summary FITS was fetched with provenance. The overview has 457 rows: 8 A-class, 17 B-class and 69 C-class lens candidates, plus 363 X-class backgrounds that are not classified as plausible strong lenses. All 457 rows were retained for matching, so no quality prefilter could conceal a close target.

There are **zero pairs within either 2 or 10 arcsec** for both the 15072-row screen and the separate 26662-object archive. The nearest target is 161.678 arcsec away. The overview coordinates refer to the MaNGA target IFU center; its foreground field is `MEAN_ZF_INNER` and background field is `MEAN_ZB`. Background-redshift scatter is not automatically an independent uncertainty estimate.

The [MaNGA contract](manga_contract.json), [script](crossmatch_manga.py), [result](manga_01/result.json), [fixed overview metadata](manga_01/all_overview_fixed_metadata.csv), and [validated bounded manifest](manga_01/manifest.json) preserve this supplementary finite result. Independent direct evaluation of all 6887904 primary coordinate pairs agrees with the tree match. Neither predicted Einstein-radius arrays nor individual spectra are used in this check.

## L002777 target-only rescue audit

The [target audit](l002777_inputs/README.md) now includes all eight raw image bands, both rejected released models, the actual retained and dropped position metadata, and the original SDSS/SILO spectrum. The foreground velocity dispersion is **203.763 ± 19.807 km/s**, an observed independent constraint. Its candidate [O II] doublet is only partly resolved; actual-resolution local fits give descriptive Δχ²=1.47–6.55 over noise, window and AND-mask controls, with weak Hβ and [O III]. This remains a plausible background candidate rather than a new secure redshift confirmation. The northern dropped point is preserved for competing source associations, and no rejected Einstein radius is used for gravity inference. The actual SED-fit redshift remains unverified. [Result and provenance](l002777_inputs/audit_02/manifest.json) and [spectrum figure](l002777_inputs/audit_02/spectrum_windows.png) are retained.
