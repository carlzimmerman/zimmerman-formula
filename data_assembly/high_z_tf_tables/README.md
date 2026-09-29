# High-z Tully-Fisher per-galaxy tables (CDS copies), parsed and checked

Built 2026-09-28 by `build.py`. Raw files are byte-for-byte in `raw_small/` with URL, size and sha256 in
`manifest.json`; every parse is checked in `checks.txt`. No fit, no derived physics. These are per-galaxy tables
that the a0(z) ledger (`prep_2026/highz_tfr_fork/DATA_LEDGER.md`) currently carries only as summary offsets.

| output | rows | source | what it holds |
|---|---|---|---|
| `ubler2017.csv` | 135 | Ubler+2017, ApJ 842, 121 (KMOS3D), CDS J/ApJ/842/121 | z, log M*, log Mbar, max modelled circular velocity, sigma0 |
| `budhies_hi.csv` | 166 | Gogate+2020, MNRAS 496, 3531 (BUDHIES), CDS J/MNRAS/496/3531 | z_HI, D_L, W20, W50, HI flux, HI mass (A963: 127, A2192: 39) |
| `budhies_optical.csv` | 166 | same | optical redshift (where known), B and R magnitude, GALEX FUV/NUV |
| `budhies_joined.csv` | 166 | same | HI + optical joined by the ReadMe's serial number |
| `tiley2019.csv` | 754 | Tiley+2019, MNRAS 482, 2166, CDS J/MNRAS/482/2166 | KROSS (259), SAMI matched (186), SAMI original (309): v2.2, log M*, K-band mag |

## What the checks established
- Ubler: the redshift split is 65 (z<1.3), 24 (1.3-1.8) and 46 (z>=1.8), so the ledger's 65 at z~0.9 and 46 at
  z~2.3 are the two outer bins and 24 intermediate galaxies are not in the ledger's two bins. All ReadMe ranges
  hold and log Mbar >= log M* for every row.
- BUDHIES: HI and optical tables have different names for one detection, so the join is by serial number; HI and
  optical positions agree to 22.4 arcsec at most (median 3.8), which is a real counterpart match. **One galaxy,
  A963 #68, has z_HI = 0.19947 but a literature optical z of 0.12**; it is kept and flagged
  (`z_opt_hi_mismatch_flag`). The next-largest |z_opt - z_HI| is 0.0021. Eight galaxies have B and R magnitudes
  converted from SDSS (near bright stars or at the field edge; flagged `*` in the source, kept in `bmag_flag`).
- Tiley: exactly the three survey labels; the SAMI-matched rows were built with the identical pipeline as KROSS,
  which is what makes them a same-method local control.

## What these tables do NOT contain (read before using)
- **Ubler** gives no per-galaxy errors, no radii and no gas masses in this table. `Mbar` is the paper's modelled
  baryonic mass, and its gas method is in the paper, not verified here. The velocity is the maximum modelled
  circular velocity, a different convention from Tiley's v2.2 (v at 1.3 R_e) and from the ledger's rows.
- **BUDHIES** has NO stellar masses: a baryonic mass needs a stellar M/L from B and R (not applied here), and its
  velocities are HI line widths (W20, W50) NOT corrected for inclination in the table. The galaxies sit in two
  clusters (Abell 963 and Abell 2192), so environment can bias the gas content.
- **Tiley** is stellar-mass Tully-Fisher only (no gas); it is a same-pipeline z~0 versus z~1 control for the
  stellar relation, not a baryonic one.
- None of these is a test of a0. Calculations belong to the calculation thread.

Cross-references: KMOS3D cubes and the PHIBSS gas set are in `../kmos3d_phibss/`.
