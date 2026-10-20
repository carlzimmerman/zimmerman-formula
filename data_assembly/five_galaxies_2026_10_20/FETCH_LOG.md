# Five pulled SPARC galaxies: independent kinematics and colour profiles. Fetch log (approved by the owner in chat 2026-10-20)

- **Purpose:** follow-up to AG4g and AG4h. The five clean (Q = 1) positive-pull galaxies NGC0024, NGC5985, UGC00128, UGC00731
  and UGC08286 (= NGC 5023) need a non-stellar-population Υ through their rotation-curve shape. These data test non-circular
  motions and radial M/L gradients for them.
- **Where:** stored outside the repo in `_external_data/five_galaxies_2026_10_20/`, alongside the repo, as for cosmicflows4
  and little_things_oh2015.
- **Integrity:** `FETCH_MANIFEST.jsonl` (url, path, bytes, sha256, UTC time) and `SHA256SUMS.txt` are there. 30 files,
  73,441,472 bytes.
- **Checks:** every URL was HEAD-checked first (HTTP 200, Content-Length equal to the listed size). After download every size
  matched, `shasum -c` gave 30/30 OK, and `file` showed FITS, gzip, bzip2 or ASCII, with no HTML pages. One SDSS connection
  timed out and curl's retry recovered it.
- Nothing downloaded is executed. Readers open these files with `python3 -I`.
- Sources were found by a research subagent. The load-bearing items were re-verified independently in this session: sizes by
  HEAD, and galaxy presence by per-galaxy VizieR queries (GHASP UGC 9969 = NGC 5985; de Blok & Bosma UGC731 and NGC5023).

## Kinematics, independent of SPARC's sources (SPARC used Di08/Ch06, Bl04/Br92, VB99/VH93, Sw09/Sw02)
| subdir | source | files | covers |
|---|---|---|---|
| `kinematics/ghasp_epinat2008` | GHASP Hα Fabry–Perot, Epinat, Amram & Marcelin 2008, MNRAS 390, 466 (VizieR J/MNRAS/390/466) | tablef.dat (185,152), ReadMe | NGC 5985 (UGC 9969): rotation curve per side |
| `kinematics/catinella2005` | Catinella, Haynes & Giovanelli 2005, AJ 130, 1037 (J/AJ/130/1037) | table1.dat (41,106), ReadMe | NGC 5985: Polyex fit parameters only |
| `kinematics/deblok_bosma2002` | de Blok & Bosma 2002, A&A 385, 816 (J/A+A/385/816) | rawcurve.dat.gz (20,478), procurve.dat.gz (7,068), galaxies.dat.gz (441), ReadMe | UGC 731 (28 raw points; weak receding side), NGC 5023 (149 raw, 33 processed; processed switches to Swaters' HI beyond 180″, so it is only partly independent) |

**No independent kinematics was found for NGC 24 or UGC 128.**

## Profiles and images for M/L gradients
| subdir | source | files | covers |
|---|---|---|---|
| `profiles/munozmateos2009_sings` | Muñoz-Mateos et al. 2009, ApJ 703, 1569 (J/ApJ/703/1569) | table2.dat (214,060: FUV–Ks), table4.dat (353,155: IRAC/MIPS), ReadMe | NGC 24 |
| `profiles/s4g_p3` | S4G Pipeline 3 (Muñoz-Mateos et al. 2015), IRSA | NGC0024/NGC5985/NGC5023 `.{1,2}fx2a_noclean_fin.dat` (3.6/4.5 μm) | NGC 24, NGC 5985, NGC 5023 |
| `profiles/bouquin2018_galex_s4g` | Bouquin et al. 2018, ApJS 234, 18 (J/ApJS/234/18) | table3.dat.gz (1,953,043), ReadMe | FUV/NUV/3.6 μm for NGC 24, NGC 5985, NGC 5023 |
| `profiles/sga2020` | Siena Galaxy Atlas 2020 (Moustakas et al. 2023) | NGC5985 and NGC5023 ellipse.fits (420,480 / 63,360) | g/r/z ellipse profiles |
| `images/ugc00128_irac_seip` | Spitzer Enhanced Imaging Products, IRSA | IRAC.1 and IRAC.2 mosaics (18,043,200 each) | UGC 128 |
| `images/ugc00128_sdss_dr17` | SDSS DR17 frame run 4822, camcol 1, field 547 | u, g, r, i, z frames (.bz2, 16,446,005 total) | UGC 128. The galaxy is about 4′ from the frame centre, so neighbouring fields may be needed (not fetched). |
| `images/ugc00731_irac_pbcd` | Spitzer post-BCD, AOR 40287488, IRSA | I1 and I2 maic.fits (8,377,920 each) | UGC 731 (no public optical image was found) |

## Not fetched, by the owner's choice or because unverified
- The HALOGAS NGC 5023 HI cubes (Zenodo 10.5281/zenodo.3715549, 289,422,720 B each): skipped by the owner.
- Kuzio de Naray et al. 2008 DensePak (UGC 128 not confirmed inside the file).
- The GHASP velocity-field FITS (the site's bot check).
- GALEX and WISE images for UGC 128.
- Legacy Surveys and NED BVRI images for NGC 24.
