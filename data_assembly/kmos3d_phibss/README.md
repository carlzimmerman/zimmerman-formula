# KMOS3D + PHIBSS: high-z kinematics and baryon budget, assembled from public raw sources

Built 2026-09-28 by `build.py` (no fit, no tuned number). Every claim below is checked in `checks.txt`.
The purpose is to have, in one place with provenance, the public pieces needed to test whether the
galaxy acceleration scale a0 is flat with redshift (the framework's law) or tracks H(z) (the rival).

## What is here

| file | rows | what it is |
|---|---|---|
| `raw_small/` | 5 files | the small raw inputs, byte-for-byte, hashes in `manifest.json` |
| `kmos3d_catalog.csv` | 785 | KMOS3D main catalogue (Wisnioski+2019) with the Halpha aperture fluxes merged on (FIELD, ID) |
| `phibss13_joined.csv` | 73 | PHIBSS (Tacconi+2013) tables 1 and 2 joined on name: Vrot, Mmol, M*, radii, SFR, positions, z_CO |
| `kmos3d_phibss_match.csv` | 0 | the KMOS3D x PHIBSS sky+redshift cross-match (header only; the overlap is empty, see below) |
| `checks.txt` | | every assertion and control, PASS/FAIL |
| `manifest.json` | | URL, byte size and sha256 of each raw input (and of the cube tarballs once fetched) |
| `fetch_cubes.sh` | | resumable download of the three KMOS3D cube tarballs (3.15 GB, NOT in the repo) |

Sources: KMOS3D https://www.mpe.mpg.de/ir/KMOS3D/data (cite Wisnioski et al. 2019, ApJ 886, 124);
PHIBSS https://cdsarc.cds.unistra.fr/ftp/J/ApJ/768/74/ (Tacconi et al. 2013, ApJ 768, 74).

## What the assembly found (read this before using it)

1. **KMOS3D and the 2013 PHIBSS sample do not overlap.** 0 of the 56 PHIBSS galaxies with a position lie
   within 1.5 arcsec (and |dz|<0.01) of a KMOS3D galaxy; the nearest is 1237 arcsec away (zC406690).
   KMOS3D covers COSMOS, GOODS-S and UDS only. A positive control (0.3 arcsec jitter on KMOS3D's own
   positions) recovers 780/785 rows, and six shifted-position negative controls give 0 chance matches, so
   the empty result is the matcher working, not a bug. **Any KMOS3D + direct-CO combination therefore
   needs the later PHIBSS / PHIBSS2 tables (Tacconi+2018, Freundlich+2019), which I did not obtain in
   machine-readable form** (not at CDS under J/ApJ/853/179 or J/A+A/622/A105; the journal data page
   HTML exposed no table link; the arXiv e-print endpoint returned only the PDF).
2. **The KMOS3D catalogue carries no kinematics.** Columns are redshift, M*, SFR, R_half, axis ratio Q,
   PSF, exposure, colours, and Halpha flux and dispersion. No Vrot, inclination or gas mass. g_obs(R)
   requires fitting the 739 cubes ourselves.
3. **PHIBSS table 2 is itself a CO-based baryon-and-kinematics set**: 73 galaxies (z~1.2, z~2.2, plus
   BzK, PEP and lensed objects) with Vrot (65 have one, quoted 20-30% uncertain), Mmol (systematic 50%,
   Galactic conversion factor, CO(1-0)/(3-2) ratio 2), M* (systematic 30%) and radii. `mbar_msun` is
   plain M* + Mmol, with `mbar_is_upper_limit` set where the gas mass is a CO upper limit.
4. **Six PHIBSS gas masses are 3-sigma upper limits** (ReadMe note 4; the minus sign). They are stored as
   magnitudes with `co_upper_limit = 1`. Never treat them as measurements.
5. **Three rows in the source table are internally inconsistent**: PEPJ123709, PEPJ123712 and PEPJ123759
   quote an `fgas` that the same row's Mmol and M* do not reproduce (differences 0.036, 0.119, 0.055; the
   rounding floor is 0.02). Both values are kept (`fgas_quoted`, `fgas_recomputed`) and the rows are
   flagged `fgas_inconsistent_in_source`. Not corrected.

## What is not here

- Cubes: `fetch_cubes.sh` fetches them. At the time of writing the download was partial (see the session
  report); rerun the script to resume, then `python3 build.py --cubes DEST` to record hashes.
- HIGHz / BUDHIES (z~0.2 HI), MSA-3D and GA-NIFS tables, RC100 and Genzel+2020 rotation-curve tables:
  none obtained; per-galaxy machine-readable availability is unverified for all of them.

## Suggested use (proposals for the calculation thread, none of it run)

- A first z~1-2 check straight from `phibss13_joined.csv`: baryonic Tully-Fisher points (Vrot, Mbar) at
  z~1.2 and 2.2 against the local relation on the ledger's footing (`prep_2026/highz_tfr_fork/`). Vrot
  here is the CO or Halpha velocity as tabulated; inclination, pressure support and beam smearing are
  whatever Tacconi+2013 applied, and the ledger's convention (v at 2.2 R_d, sigma0 term) is NOT the same.
- A cube-fit pilot on KMOS3D COSMOS with one public tool (DysmalPy, 3DBarolo, GalPaK3D or RotCurves),
  **paired with the same code on a matched local sample**; a method-localised rise is what sank the
  MUSE-DARK III reading, so a fit without a local control means nothing.
- Only galaxies with g_bar < a0 somewhere in the measured range constrain a0; most high-z discs are
  baryon-dominated where measured, so select on that first.

I cannot verify that nobody has assembled these exact pieces; the merge is a bookkeeping convenience, not
a new measurement, and it carries every systematic listed above.
