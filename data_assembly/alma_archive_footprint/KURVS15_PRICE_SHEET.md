# Pricing the ALMA products for KURVS-15 (cdfs_31127; z_Hα = 1.613; CO(2-1) at 88.23 GHz, CO(5-4) at ~220.5 GHz)

Priced 2026-09-29 from the ALMA archive's own metadata (TAP `ivoa.obscore` and the public DataLink documents, copies in `datalink_metadata/`). **Nothing has been downloaded.**
Two programmes observed KURVS-15 as their target (target names `CDFS_31127` / `cdfs_31127` are its CANDELS ID); all data are listed public, QA2 passed.

| MOUS (member OUS) | programme | band, what covers KURVS-15 | resolution; on-source time | product package (`#this` tar) | auxiliary tar | raw ASDM tars (not needed) |
|---|---|---|---|---|---|---|
| uid://A001/X1465/X137f | 2019.1.01238.S (Molina, kpc-scale CO at z~1.5) | Band 3, spw 23 (86.9–88.8 GHz) holds CO(2-1); spw 25/27/29 give continuum and neighbouring windows | 0.11″; 6205 s | **43.60 GB** | 1.10 GB | 3 tars of 50–55 GB |
| uid://A001/X133d/X7a8 | 2018.1.00164.S (Ibar, KMOS+ALMA) | Band 3, spw 29 (87.1–88.9 GHz) holds CO(2-1) | 2.48″; 2722 s | **8.63 GB** | 1.61 GB | 6 tars of 11–14 GB |
| uid://A001/X133d/X7ac | 2018.1.00164.S (Ibar) | Band 6, 219–235 GHz: CO(5-4) window (~220.5 GHz) plus 1.2 mm dust continuum | 1.0″; 816 s | **3.89 GB** | 0.65 GB | 3 tars of 3.6–7.9 GB |
Each MOUS also has a 3.5 kB README listing its products.

## What each would give (facts about the data, not a result)
- Molina Band 3: the deepest and highest-resolution CO(2-1) here (0.53 mJy/beam per 10 km/s archive estimate); resolved gas at ~1 kpc scale, a CO velocity curve if detected.
- Ibar Band 3: same line at 2.5″ (whole galaxy in one beam), 1.1 mJy/beam per 10 km/s: an integrated flux, no resolved kinematics.
- Ibar Band 6: CO(5-4) and dust continuum, both independent estimates of the cold gas; 1″.
Whether the line is detected is unknown; an archive window is not a detection.

## Practical constraints
- **Disk:** this Mac has 101 GB free on a 95%-full volume (`~/new_physics/_external_data` is on the same volume, 17 GB now). The Molina package (43.6 GB) would need ~45 GB to hold the tar and about twice that while unpacking; it does not fit safely without freeing space or an external disk.
- **Network:** the archive's download speed from here is unmeasured; an earlier public server delivered about 265 kB/s (9 h for 8.6 GB at that rate). I would measure with the two READMEs first.
- **Format:** each package is a tar of the QA2 products; I have not seen its file list. The README lists it (3.5 kB). A tar can be streamed and unpacked selectively (only the cube for the CO window), but if the wanted member sits late in the archive most of the 43.6 GB still travels.
- **What I would run on it:** nothing physical; I would only extract the cube(s), record beam, channel width and header, and report the file hashes. Any flux, moment map or conversion is the calc thread's.

## Options (each needs my user's go; filename, source and size as above)
1. **READMEs only**: the three `member.uid___..README.txt` files, 3.5 kB each, from almascience.nrao.edu (one call each). Tells us what is in each package before we commit to it.
2. **Ibar Band 3 package** (`2018.1.00164.S_uid___A001_X133d_X7a8_001_of_001.tar`, 8.63 GB) and/or **Band 6** (`..._X7ac_001_of_001.tar`, 3.89 GB): 12.5 GB together, fits on this disk.
3. **Molina Band 3 package** (`2019.1.01238.S_uid___A001_X1465_X137f_001_of_001.tar`, 43.60 GB): needs disk space first.

## Update after the three READMEs and the file-level DataLink lists (2026-09-29; the READMEs are the only files fetched, 3.5 kB each, stored in `~/new_physics/_external_data/alma_kurvs15/`)
The READMEs are the generic ALMA text. They say the FITS products can be downloaded **file by file** ("download files individually from the 'product' category"), and the DataLink file lists (`kurvs15_product_file_list.csv`, 514 files with sizes and direct URLs) confirm it. So the full tars are not needed. Pipeline products are already imaged, primary-beam-corrected, continuum-subtracted cubes, so no CASA and no re-imaging are required.
| what | file (member.uid___...) | size |
|---|---|---|
| Ibar Band 3, CO(2-1) window (spw 29, 87.1–88.9 GHz) | `A001_X133d_X7a8.cdfs_31127_sci.spw29.cube.I.pbcor.fits` + `...spw29.cube.I.pb.fits.gz` | 273 MB + 91 MB |
| Ibar Band 6, CO(5-4) window (spw 29, 220.3–222.2 GHz; CO(5-4) at 220.5 GHz) | `A001_X133d_X7ac.cdfs_31127_sci.spw29.cube.I.pbcor.fits` + `...pb.fits.gz` | 69 MB + 23 MB |
| Molina Band 3, CO(2-1) window (spw 23, 86.9–88.8 GHz), coarse-channel version | `A001_X1465_X137f.CDFS_31127_sci.spw23.repBW.I.pbcor.fits` + `...repBW.I.pb.fits.gz` | 4.76 GB + 1.37 GB |
| Molina Band 3, full-resolution cube (optional) | `...spw23.cube.I.pbcor.fits` + `...pb.fits.gz` | 28.8 GB + 8.3 GB |
| continuum images of all three (`*cont.I.tt0.pbcor.fits`, `*cont.I.pb.tt0.fits`) | spw-combined | ~40 MB each for Molina, under 1 MB to a few MB for Ibar |
**Minimum set (three line cubes with their beam responses, no full-resolution Molina cube): about 6.6 GB.** With all continuum images about 6.8 GB. It fits on this disk (101 GB free). The optional full-resolution Molina cube is +37 GB and is not needed for an integrated flux.
Tools: Python with numpy and astropy (checked below); no CASA.
