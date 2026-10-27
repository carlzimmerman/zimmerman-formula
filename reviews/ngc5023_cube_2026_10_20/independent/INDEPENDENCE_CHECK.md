# WHISP versus HALOGAS: independence leaf

Checked on the client date 20 October 2026. This is an append-only
qualification of the acquisition note; the downloaded cubes, geometry
record and earlier pins are unchanged.

**Distinct observing campaigns are verified. Complete zero overlap of
visibility inputs is not certified by the available records.** The
comparison can be described as an older-WHISP versus later-HALOGAS
observational check, with a stated provenance limit. Do not multiply
their significance as if full statistical and systematic independence
had been proved.

## Evidence actually checked

1. **Actual older cube.** WHISP's native FITS header has
   `DATE-OBS=1996.363`, reduction DATE `20/12/96` and CLEAN history
   on 19 February 1997. Its 127-channel, 2.48-MHz setup and GIPSY
   reduction are documented in the saved header and Groningen notes.
2. **Primary HALOGAS survey description.** Heald et al. (2011),
   *The Westerbork Hydrogen Accretion in LOcal GAlaxieS (HALOGAS)
   Survey I. Survey Description and Pilot Observations*,
   [arXiv:1012.0816v1](https://arxiv.org/abs/1012.0816v1), section 3,
   describes ten full 12-hour WSRT tracks per galaxy, two polarizations,
   1024 channels across 10 MHz, individually bracketed by flux
   calibrators, followed by the stated Miriad calibration, continuum
   subtraction, self-calibration, imaging and deconvolution sequence.
   NGC5023 is listed in the survey sample, although it is not one of
   the four pilot galaxies analyzed in that paper. The paper does not
   state that WHISP visibility data are included for NGC5023.
3. **An explicit exception exists elsewhere in the same primary source.**
   Section 4.4 specifically states that NGC4565's new observations are
   combined with archival observations. That confirms archival stacking
   is possible within HALOGAS and is not ruled out merely by the survey
   name. It also supports treating the absence of such a statement for
   NGC5023 as evidence about the described reduction, not a formal proof
   that no old visibility entered it.
4. **NGC5023's own primary analysis.** Kamphuis et al. (2013),
   [arXiv:1306.5312v1](https://arxiv.org/abs/1306.5312v1), section 2.1,
   identifies the observations as obtained for HALOGAS and refers to
   Heald et al. for the standard reduction and calibration. It then
   describes the 69-channel NGC5023 cube and Hanning smoothing. Searches
   of the entire saved TeX for WHISP, archival combination and older
   observations reveal no statement of WHISP stacking for NGC5023.
5. **Actual released HALOGAS cube history.** The HR cube has
   `DATE-OBS=2010-05-15T01:28:55.3`, imports
   `raw01/11002162_S0_T0.UVF` in November 2010, performs the recorded
   Miriad reduction, and images `vis=../red*/lin.uv` in March 2011.
   The final FITS export points into the `wsrt/10a/n5023` project
   directory. This is direct evidence of a separate 2010 observing
   campaign contributing to the product, not just a new filename for
   the 1996 cube. The HR/LR products of this campaign remain processing
   variants of shared observations.

## Exact limitation and permissible inference

The released FITS history retains one raw dataset path and a wildcard
for the collection of reduced visibility sets. It does **not** enumerate
all input observation IDs and dates or provide the original visibility
measurement sets. Consequently this check cannot prove the stronger
statement that every HALOGAS visibility is disjoint from every 1996
WHISP visibility. No primary source inspected reports such reuse for
NGC5023; the described workflow and actual history support separate
campaigns. The unresolved step is the complete input visibility manifest,
not whether an older observation exists.

Both campaigns use WSRT, view the same source and may share classes of
instrumental/flux-scale assumptions. Center, velocity convention,
deconvolution, masking, finite uv coverage and beam errors must still be
controlled. Distinct observing dates do not establish independence from
all calibration systematics.

For the present analysis, report whether the frozen observable recurs
in the old WHISP cube, after matching response and sensitivity. Call it
an **older-campaign cross-check with unverified zero-visibility-overlap**.
A stronger independent-replication claim needs the complete HALOGAS
visibility input list or a genuinely separate telescope observation.
No authors were contacted and no raw-observation reduction was performed.

## Source pins

`INDEPENDENCE_SOURCE_PINS.json` records the exact versioned Heald source
archive and extracted files, the unchanged Kamphuis source, the native
WHISP header, and the released HALOGAS header/cube identity. This check
adds no scientific numerical run and changes no previous source or result.
