# Separate WHISP observation recovered

Client date: 20 October 2026. Checkpoint `ngc5023-cube-2026-10-20`,
base `be8fc76cb0e207b88710f130abf2aa937f0895a5`.
This acquisition task writes only this `independent/` directory.

**A genuine separate-observation HI cube was acquired.** It is the older
WHISP observation of UGC8286, hosted by NED under the image-archive refcode
`2011MNRAS.416.2437H`. Its own header says `DATE-OBS=1996.363`; its CLEAN
history is dated February 1997. It therefore does not consist of a second
reduction of the later HALOGAS observations. Both campaigns used WSRT,
so telescope-specific systematics remain shared in a broader sense.

## Files and verified acquisition

The [NED image inventory](https://ned.ipac.caltech.edu/cgi-bin/imgdata?objname=NGC+5023)
explicitly links the cube, as well as 30- and 60-arcsec products from the
same WHISP observation. Those variants are not independent replications
of one another. The inventory also links HALOGAS cubes; they were not
downloaded by this task or counted as an additional observation.

- [Direct NED WHISP cube](https://ned.ipac.caltech.edu/img/2011MNRAS.416.2437H/UGC_08286cl:I:HI:h2011.fits.gz):
  `UGC_08286cl_WHISP.fits.gz`, 52,535,033 bytes,
  SHA-256 `868a87be2962d9f69d86d951768b7207b51872ea93629e5cc4cc313e3cd014e6`.
- Gzip-only decompression: `UGC_08286cl_WHISP.fits`, 66,594,240 bytes,
  SHA-256 `1455c27c290a5ce0951dc2461df8d2c8958615b6c5a646ae735829a941af147d`.
- Actual cards: `WHISP_HEADER.txt`; parsed conventions, channels and
  center: `GEOMETRY.json`.
- URL/response/hash records, including failed endpoints: `acquisition.json`.

The download was bounded at 100 MB and 180 seconds, completed in 2.86
seconds, and the server Content-Length agreed with the retrieved byte count.
Decompression was separately bounded below 100 MB. No new dependency was
installed. The first header-print attempt decoded binary pixels after END
and failed; acquisition had already completed and was recorded. The corrected
header reader stops at END and the cube itself was not altered.

## Conventions that must be used

The cube is **127 x 512 x 512**, with FITS `BITPIX=16`,
`BSCALE=0.001402622`, `BZERO=-2.117850` and `BLANK=-32768`.
Mask integer BLANK values before scaling. The header says continuum
subtracted, cleaned to 0.5 sigma and restored, with `CLIP=0`. CLEAN mask
history is not proof that all noise outside a source mask has been blanked.

Flux is in Westerbork Units: **1 W.U. = 5 mJy/beam**. This is explicitly
confirmed in Giese et al. (2016), [arXiv:1606.07387v1, section 2.1](https://arxiv.org/html/1606.07387v1),
and independently in the [2016 star-formation/gas-accretion paper, section 2.3](https://academic.oup.com/mnras/article/463/2/2092/2892710).
The cube's `NOISE=0.460062 W.U.` becomes **2.30031 mJy/beam**, agreeing
with the separately retrieved [WHISP observation notes](https://www.astro.rug.nl/~whisp/Database/OverviewCatalog/ListByName/U8286/u8286obsred.html)
which report 2.3 mJy/beam. The header noise is not a substitute for a new
blank-region covariance estimate. The quantization interval is only
0.00701311 mJy/beam.

Native beam cards are `BMMAJ=18.114047893054`, `BMMIN=12.3021393772`
**in arcsec**, and `BMPA=0` degrees. They are not standard degree-valued
`BMAJ/BMIN` cards. Pixels are 4.999212 arcsec apart.

The spatial frame is **FK4 B1950, NCP projection**, not J2000/TAN.
The [primary SIMBAD ASCII record](https://simbad.cds.unistra.fr/simbad/sim-id?Ident=NGC%205023&output.format=ASCII)
provides the same optical center in both frames:

- ICRS J2000: `13:12:11.8036148808`, `+44:02:17.328663600`.
- FK4 B1950: `13:09:57.8503976860`, `+44:18:11.510623991`.

Using the exact NCP projection, this is native FITS one-based
`(x,y)=(257.3384193995,256.7028818445)`, or numpy zero-based
`(256.3384193995,255.7028818445)`. The declination/RA origin cards describe
the pointing center, not a replacement optical centroid.

The spectral axis is **FREQ-OHEL**, optical heliocentric velocity encoded
through a legacy observed-frequency primary axis plus a secondary velocity.
`DRVAL3=407 km/s` at `CRPIX3=64.0012349952`. Do not use a naive
`c*(f_rest/f-1)` on the primary frequency: it loses the specified reference
frame zero. The [official GIPSY coordinate documentation](https://www.astro.rug.nl/~gipsy/pguide/coordinates.html)
gives the optical conversion; `GEOMETRY.json` records it and the no-rest-frequency
fallback. Standard HI rest frequency is declared as 1420405752 Hz, since
this cube contains no rest-frequency card. The two GIPSY choices differ by
at most 0.01467 km/s across the cube, compared with 4.134 km/s central channel
separation. Keep legacy-frame refinements as a control if claiming a very
small velocity difference. [Kapteyn's documented legacy-header treatment](https://kapteyn.readthedocs.io/en/latest/spectralbackground.html)
also explains why a separately encoded velocity and frequency cannot be
treated as if both already share the same reference frame. It states that
legacy VELO-HEL defaults to optical unless VELREF>256 selects radio; the
HALOGAS header must be checked rather than assumed.

## Search limits and interpretation

The historical Groningen WHISP pages now expose an overview GIF and notes,
not a direct FITS download. The old WOW path returned 404, its dedicated
hostname did not resolve, and the old AMIGA port-9000 endpoint timed out.
A current VO-registry query for WHISP returned catalog/table services but
no cube endpoint. These failures do not imply that the data do not exist:
the NED route above recovered the cube.

The 1993 NRAO quarterly report lists an NGC5023 20-cm-line program AO117;
that is an additional archival lead, not proof that a calibrated VLA cube
was recovered. GBT21A-377 targets a few widely separated minor-axis spectra;
its coarse pointings cannot directly replicate a resolved disk residual.
No VLA or GBT data were acquired or treated as confirmation here.

No residual was evaluated by this acquisition task. Replication still
requires matched angular/spectral response, paired masks, the same frozen
candidate, careful frame/centering conversion, and sensitivity accounting.
The WHISP cube is substantially shallower than HALOGAS, so failure to see a
weak HALOGAS feature cannot automatically count against it.

General 3D asymmetry analysis is already established, including the
[2023 study *Measuring galaxy asymmetries in 3D*](https://academic.oup.com/mnras/article/523/3/4340/7192458).
This acquisition supports fresh local execution, not novelty of the method.
