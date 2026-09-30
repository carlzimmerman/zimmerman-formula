# ALMA cubes: what was priced, fetched and skipped (data front, 2026-09-30; my user: "yes fetch big cubes")

All from the public ALMA Science Archive (TAP + DataLink, official endpoints). Blocked by bot protection and NOT circumvented: Zenodo (403) and the ALPINE team site cesam.lam.fr (JavaScript cookie gate); my user downloaded the Zenodo corpus in a browser instead (see below).

## Fetched (raw files in `~/new_physics/_external_data/`, not committed; scripts, file lists and sha256 manifests committed in `data_assembly/alma_alpine/`)
| what | size | files | notes |
|---|---|---|---|
| **ALPINE rotators** (`alpine_alma/`; project 2017.1.00428.L): PI-provided [CII] cube image, cube PSF, cube flux (pb), moment-0, continuum for CG32, DC396844, DC494057, DC552206, DC881725, VC5110377875 | **2.1 GB** | 54, 0 failures, sizes match | each cube 256 x 256 x 537 channels (29 MHz, [CII] at ~364 GHz), beam ~1.06 x 0.80 arcsec (about 6 kpc): Jones+21 could fit only 2-3 rings; HZ9 was not found under its ALPINE name and J0817 is another programme |
| **SPT0418-47 (z = 4.225, lensed [CII] disc of Rizzo+2020)** (`spt0418_alma/`; project 2016.1.01499.S, MOUS uid://A001/X87a/X837): pipeline-cleaned cubes (pbcor, pb, masks) and continuum for the four spectral windows | **9.48 GB** | 26, 0 failures | [CII] cubes spw25 and spw27 (363.7 and 361.9 GHz, 1400 x 1400 x 238), beam 0.14 x 0.11 arcsec; spw29 and spw31 (351.8, 349.9 GHz) are dust-continuum windows |
| **High-z Kinematic Corpus Z1** (`alpine_corpus_z1/`, zip from my user's browser download) | 238 kB | 3 | 31 ALPINE galaxies, 8 tier-1 with per-ring curves; `highz_literature_tables/alpine_corpus_z1/` holds the flattened CSVs: **all 18 ring rows equal the Jones+21 Table A3 I parsed independently** (the two apparent mismatches are a truncated name, VC.7875 = VC5110377875). The zip also contains `omega_results_z1.csv` and a figure: the corpus author's own derived 'omega' quantity, not data, not used |

## Priced and NOT fetched (why)
| what | size | why skipped |
|---|---|---|
| all other ALPINE cubes (project 2017.1.00428.L, 61 member OUS, 129 targets) | cube FITS 327 files, **38.5 GB** (all products incl. raw 1,006 GB; 4 OUS returned no file list) | beams of ~1 arcsec give 2-3 rings at best; the six rotators above carry the useful information; can be fetched on request |
| ASPECS LP 3 mm mosaic (2016.1.00324.L, UDF_mosaic_3mm) | ~9.5 + 9.0 GB for two member OUS (13 OUS, cube FITS 22.6 GB in total, 1,922 GB with raw) | only three sources show a velocity gradient; compact array, marginally resolved |
| SDP.81 (2011.0.00016.SV, z = 3.042) | one MOUS, **580.7 GB raw, no pipeline cube FITS** | needs CASA reduction of 580 GB; not practical |
| other SPT sources (SPT0346-52, SPT0311-58, SPT2147-50: dozens of projects) | not totalled | need per-source selection |
| JADES DR3/DR4 NIRSpec (MAST, `archive.stsci.edu/hlsps/jades/`) | catalogue 60 MB (DR4 GOODS-S); spectra are nested per tile and per target, total not priced | slit spectra of ~1000 galaxies; group curves need reprocessing |
| GA-NIFS (MAST) | not priced | needs the JWST pipeline |

## Disk
Free space after these downloads: 134 GB of 1.8 TB. The folder `_external_data/` now holds about 33 GB (KMOS3D 6.7, SINS AO 10, SPT0418-47 8.9, DESI 3.3, ALPINE rotators 2.1, others small).
