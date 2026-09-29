# Sky positions of the 22 KURVS-CDFS galaxies and their placement relative to public ALMA surveys

Built 2026-09-29 by `build.py`; approved by the owner ("yes, run the KURVS position query"). Data only: no gas mass, no g, no verdict.

## Correction
I told the calculation thread earlier that the sky positions were not in the KURVS paper. That was wrong: Table 1 of arXiv:2305.04382 lists RA and Dec (columns 3–4);
my earlier parse of that table had dropped them. `kurvs_positions.csv` takes them from the TeX table (`build.py` parses it, not by hand). Two independent checks pass: z and log M* equal
`kurvs2023_integrated.csv` for all 22, and the two KURVS galaxies that are also in the KMOS3D catalogue (GS4_10784, GS4_16960) agree with it to 0.08 and 0.04 arcsec.

## Negative control (kept so nobody repeats it)
The paper's "CANDELS ID" (`cdfs_NNNNN`) is not the ZFOURGE sequence number. I queried VizieR J/ApJ/830/51 (ZFOURGE CDFS, Straatman+2016) for the 20 IDs; 14 of them came back, at redshifts
that do not match the Hα redshifts (for example KURVS-2: z_Hα = 1.360, the ZFOURGE object with that number has z_phot = 0.88; 14 of 14 fail either the redshift or the position test) and 10.3–13.6 arcmin from the KURVS position of the same number (checked for all 14). The raw output is
`zfourge_idtest_NEGATIVE_CONTROL.csv` and is NOT a set of KURVS positions.

## Files
| file | content |
|---|---|
| `kurvs_positions.csv` | `kurvs_id`, `candels_id`, `ra_hms`, `dec_dms`, `ra_deg`, `dec_deg` (J2000), `z_halpha`, `logMstar`, the KMOS3D separation for the two shared galaxies, separation from the GOODS-ALMA centre, `GOODSALMA_status`, `ASPECS_status` |
| `build.py`, `checks.txt` | 4 PASS |
| `zfourge_idtest_NEGATIVE_CONTROL.csv` | the failed ID test above |

## Coverage (geometry only, from the papers' own text; source in brackets)
- **GOODS-ALMA** (1.1 mm, ALMA Band 6): field centre 03:32:30, −27:48:00; "about 10′ × 7′"; continuous area 72.42 arcmin²; average sensitivity 68.4 μJy/beam; catalogue of 88 sources
  [arXiv:2106.13246, HTML version]. The mosaic's position angle is NOT stated, so a galaxy counts as inside only if it is within the inscribed radius of a 10′ × 7′ rectangle (3.5′), outside only beyond the circumscribed radius (6.1′).
  Result: **10 inside for any orientation** (KURVS 9, 10, 11, 12, 14, 16, 18, 19, 20, 22), **11 depend on the orientation** (2, 3, 4, 5, 6, 7, 8, 13, 15, 17, 21) and **1 outside** (KURVS-1).
  Of the ten rotation-supported discs (3, 7, 8, 9, 11, 13, 15, 16, 17, 21): inside 9, 11, 16; orientation-dependent 3, 7, 8, 13, 15, 17, 21; none certainly outside.
- **ASAGAO** (1.2 mm): 26 arcmin² in GOODS-South, 25 sources at ≥ 5σ [arXiv:1808.04502 abstract]. Its centre and extent are not stated on the abstract page, so no placement was made.
- **ASPECS** (HUDF): "the ~1′ region covered within the UDF" [arXiv:1607.06768 abstract]. Using the HUDF centre 03:32:39.0, −27:47:29 (**UNVERIFIED**: I did not read a source for these coordinates), the nearest KURVS galaxy is 1.9′ away (KURVS-18) and none lies within 1′, so I mark all 22 outside.

## What was NOT done
- No ALMA source table was cross-matched. The GOODS-ALMA and ASAGAO catalogues are not on VizieR under the reference codes I tried (a table-name search found none), and the abstract/HTML pages I read do not say where they are hosted. Whether any KURVS galaxy is a catalogue detection is therefore unknown.
- A non-detection in a source catalogue is not a measured limit. Only the survey's average sensitivity (68.4 μJy/beam) is known to me, not the local map rms at each position.
- No gas mass or Scoville conversion is applied.
