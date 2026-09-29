# Per-galaxy tables taken from the public TeX/FITS source of four arXiv papers

Built 2026-09-29 by `build.py`. The source tarballs (arxiv.org/e-print/<id>, 76 MB in total) are kept outside the
repo in `~/new_physics/_external_data/arxiv_src/`; the exact table fragments and the two FITS files are
byte-for-byte in `raw_small/` with sha256 in `manifest.json`. Every parse is checked in `checks.txt` (all PASS).
This is how the tables the PDFs and supplements did not give became available: the papers' own LaTeX and
`extra_material/` files. No author was contacted. No fit, no derived physics.

Commented-out LaTeX (lines starting with `%`) is ignored: these files keep superseded drafts of their tables.

| output | rows | paper | holds |
|---|---|---|---|
| `msa3d_galaxies.csv` | 30 (23 golden, 7 good) | MSA-3D, arXiv:2606.27853 (JWST/NIRSpec, z 0.58-1.68) | z, RA, Dec, log M*, SFR, R_e (arcsec) |
| `msa3d_kinematics.csv` | 30 | same | inclination, PA, disk R_e (kpc), sigma0, **Vrot at R_e**, V/sigma, **f_DM(R_e)**, B/T, rotation-curve shape, each with errors and a fixed-parameter flag |
| `manceraPina2026_sample.csv` | 43 | Mancera Pina+2026, arXiv:2511.08685 (KROSS + KMOS3D, z 0.79-1.03) | z, log M*, j*, flat circular velocity V_circ,f (p16/p50/p84), V/sigma |
| `amvrosiadis_parent.csv` | 30 | Amvrosiadis+2025, arXiv:2312.08959 (ALMA CO, z 1.2-4.7) | z, CO transition, beam, log M*, **log M_gas from CO**, SFR, L_IR, class |
| `amvrosiadis_bestfit.csv` | 12 | same | r_e (arcsec), inclination, V_max, sigma, **V_circ at r = 2 r_e**, M_dyn(r < 10 kpc), with errors |
| `sharma2024_gs21b.csv` | 225 | Sharma+2024, arXiv:2406.08934 (KROSS, z 0.76-1.04) | inclination, R_e, **velocities at R_e, R_opt and R_out (about 5 R_D)**, M*, M_H2, M_HI, gas radius, quality flags |

## Cross-checks that passed
- MSA-3D: 23 golden and 7 good galaxies as the paper states; the median f_DM(R_e) of the golden sample recomputed
  from the table is 0.63, the paper's stated median; the two tables share the same 30 IDs in the same order.
- Mancera Pina: 43 galaxies as the paper states; velocity percentiles ordered for every row.
- Amvrosiadis: 12 fitted discs, all present in the 30-source parent table.
- Sharma: 225 rows, every velocity and mass finite and positive.

## What each table cannot do (read before using)
- **MSA-3D:** ONE velocity per galaxy, at R_e of the disk; no gas mass in either table (the paper's gas comes from a
  depletion-time scaling inside the dynamical model). f_DM is a model output.
- **Amvrosiadis:** the only set here with a MEASURED gas mass (molecular, from CO luminosity with a conversion
  factor) and a velocity at a STATED radius (2 r_e). It is 12 massive dusty star-forming galaxies
  (log M* about 10.5-12.3, V_circ about 250-530 km/s). Their r_e are 0.19-0.62 arcsec, and a rough estimate
  (velocity squared over 2 r_e, about 8 kpc per arcsec) puts the total acceleration at 2 r_e near ten times a0,
  so they probe the high-acceleration regime. That estimate is my back-of-envelope arithmetic, not a calculation
  in the repo. Molecular gas only (no HI).
- **Sharma:** velocities out to R_out, about 5 disk scale lengths (the outermost of any sample here). BUT the gas
  masses are NOT measured: M_H2 comes from the Tacconi+2018 scaling and M_HI from a stacked M*-M_HI relation at z~1
  (Chowdhury+2022). The median M_HI is 4.1 times the stellar mass and the median M_H2 is 0.27 times it, so the
  baryon budget at large radius is set by an assumed gas mass. The FITS has no radius column; the radii are as
  the paper defines them. 19 rows have `Rout_Flag = F`, 15 have `Mstar_flag = F`.
- **Mancera Pina:** stellar-mass sample with a flat circular velocity; no gas.
- The CRC file (`sharma2024_2406.08934_CRCs_FitsParam_Burkert.fits`, 16 rows) holds Burkert-halo fits to 16
  stacked bins (`bin_0`...`bin_15`), not to individual galaxies; it is in `raw_small/` but not parsed.
- None of these is a test of a0 by itself. Calculations belong to the calculation thread.
