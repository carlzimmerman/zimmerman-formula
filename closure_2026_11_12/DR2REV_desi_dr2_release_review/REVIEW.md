# DR2REV: the DESI DR2 November release, read in full

2026-11-12. A review, not a graded lane. It reads the papers and the released files, checks the
record's use of them, and names the one test the release now allows. No frozen verdict is changed
here. All arithmetic in this file is post hoc, uses diagonal errors and is not a grade.

## Verdict

The November release is a calibrated **amplitude** of the Milky Way's enclosed mass between 20 and
80 kpc. It is not a 13-point measurement of the profile's shape, and its virial mass is an
extrapolation whose small error bar comes from one method sitting on an informative prior.

For the framework's zero-parameter line (DW1's, A = 1, no external field):

| | canonical | alt |
|---|---|---|
| worst point against the joint profile | -3.5 sigma at 45 kpc | -2.1 sigma at 45 kpc |
| points at 20 to 65 kpc | all between -2.3 and -3.5 sigma | all between -0.95 and -2.1 sigma |
| 80 kpc (the radius DW1a graded) | -1.4 sigma | -0.3 sigma |

The 13 points are strongly correlated and no covariance is published, so these cannot be combined
into one significance. Read plainly: the canonical line is 12 to 18 per cent low from 20 to 65 kpc
and DW1a graded the single most favourable radius. This is the same fact DW1 recorded as
A* = 1.33 +/- 0.04 (canonical) and 1.15 +/- 0.03 (alt). With the Local Group external field the
80 kpc numbers are -2.77 / -2.50 sigma (G239's, not re-run here).

What the release adds that the record has not used: the per-method curves for the real Milky Way
are public now (section 4). They include the only method that measures the shape. Their values
were deliberately not read in this review, so a test against them can still be frozen blind.

## 1. What was released, and what was not

Released 3 to 4 November 2026 (arXiv versions v1, all read in full):

| arXiv | paper | role |
|---|---|---|
| 2611.05518 | DESI DR2 Results III: The Mass of the Milky Way | key paper, joint estimate |
| 2611.05519 | Riley et al., mock catalogues | the calibration set |
| 2611.05520 | Zhou et al., emPDF | method 1 |
| 2611.05521 | Medina et al., GME | method 2 |

Also public: the figure data of Results III, Zenodo 10.5281/zenodo.23712180 (concept
10.5281/zenodo.23712179), one file `desi-dr2-mw-mass-figdata.zip`, 2,652,537 bytes, md5
`5b0cc3aa9947286eb9348e947d01182d`, sha256
`1b132abc3f163887160efb29a88d294ce5fb0751d2e389951da9c4c237e35ee1`. The record's API reports access
open, no embargo. Its description warns the contents may change during journal review.

Not released:

- **The DR2 spectra and catalogues.** Results III uses "private data from Data Release 2". Riley et
  al. give the public release as "early 2027". The DESI releases page still lists DR1 as latest.
- **The NIMBLE paper** (Valluri et al.), cited as "in preparation". NIMBLE is methods 3 and 4 and
  carries the largest weight in the joint profile.
- **The DR2 RR Lyrae catalogue paper** ("a separate paper").
- **Galaxy full-shape DR2.** Results IV calls it "upcoming".

Not checked here: whether the emPDF (zenodo 22644507), GME (zenodo 23710246) and mock (zenodo
23599247) records are open.

## 2. How the joint profile is built

10,036 stars (5,198 BHB, 4,838 RRL), 6D, about 10 to 95 kpc. Four methods, two tracers, so eight
estimates. At each radius separately the eight are bias-corrected and combined by maximum
likelihood, with the biases, the method-to-method covariance and a per-method error floor all taken
from 24 mock surveys.

| method | what it assumes about the mass | stars used | weight |
|---|---|---|---|
| emPDF | the total mass is one spherical NFW, two parameters, no separate baryons | 1,863 BHB, 2,282 RRL, r > 20 kpc; median radius 27 kpc | under 40 per cent each |
| GME | potential is one power law, fitted only at 50 to 80 kpc | 279 BHB, 213 RRL (Medina et al.; Results III Table 2 prints 352 BHB, which in Medina et al. is the count before the RVS_WARN cut) | enters only at 50 to 80 kpc |
| NIMBLE-A | none: spherical Jeans, B-splines, fits its own tracer density | 4,628 BHB, 4,798 RRL | one NIMBLE branch alone carries |
| NIMBLE-B | none: spherical Jeans, B-splines, external tracer density | 4,573 BHB, 4,371 RRL | 40 to 70 per cent at every radius |

Consequences for anything that reads the shape of Table 4:

1. **The points are not independent.** Each comes from smooth fits to the same stars. No
   radius-to-radius covariance is published, in the paper or in the figure data.
2. **The rest of the weight, up to 30 to 60 per cent depending on radius, has an imposed shape.**
   emPDF returns an NFW curve by construction. GME returns a power law.
3. **GME's slope is its prior.** The prior on the potential slope is gamma = 0.440 +/- 0.046
   (adapted from Shen et al.). The posterior draws in the figure data give 0.461 with standard
   deviation 0.054 (RRL) and 0.450 with 0.046 (BHB). The data did not narrow it. For BHB the
   normalisation is also the prior (62.1 +/- 6.5 against 64.6 +/- 6.9). The framework's line needs
   gamma = 0.07 at 50 to 80 kpc, which is 8.0 prior widths from the prior mean, so GME could not
   have returned the framework's slope whatever the stars did.
4. **GME's correction changes the slope.** Its raw masses are high in every one of the 24 mocks, by
   about 20 per cent at 50 kpc and 13 per cent at 80 kpc. Removing that adds about 0.14 to 0.25 to
   d ln M / d ln r.

So DW1's sentence that the 13 points are "13 independent chances to fail" is wrong, and the
chi2/dof of 0.26 for a free-amplitude fit shows compatibility, not a passed shape test. G238's
corrected reading already says the slope is not a calibrated test; this is the reason.

## 3. What the calibration can and cannot carry

Every bias, weight and error in the joint estimate comes from six Auriga haloes seen from four
positions. From the paper, the mock paper and the figure data:

- **Six haloes, all LambdaCDM, M200c 1 to 2 x 10^12.** True M(<80 kpc) runs from 5.67 to
  8.11 x 10^11 (figure data, `figA1/truths.csv`). The Milky Way's 6.36 is inside that range.
- **The true outer slope is the same in all six.** d ln M / d ln r between 50 and 80 kpc is 0.64 to
  0.72 in every halo; between 20 and 50 kpc it is 0.76 to 0.93. The framework's line has 0.93 at 50
  to 80 kpc. No mock tests how the methods behave on a profile that keeps rising that fast, so the
  corrections are untested there. The joint Milky Way value over the same range is 0.73 (RRL only
  0.61, BHB only 0.82), with an error near 0.2 if the end points were independent.
- **No LMC.** Neither the methods nor the mocks model it. The paper quotes a bias of up to 20 per
  cent in this radial range from the LMC (Erkal et al. 2020, whose title says equilibrium masses are
  biased high).
- **The mock tracers sit much further out than the real ones.** About 20 per cent of mock stars lie
  beyond 50 kpc and 0.5 per cent beyond 80 kpc; the real samples have about 5 and 0.1 per cent.
- **The real data have stars the mocks lack.** Velocity outliers above 500 km/s exist in the DESI
  samples and not in the mocks; the paper says its bias values "may still underestimate the true
  bias" for that reason.
- **24 mocks estimate a 36-element covariance.** It is shrunk half-way to diagonal. Views of the
  same halo are treated as independent and are not.
- **The methods disagree by more than the joint error.** At 80 kpc: GME 5.3 +/- 0.5 (RRL) and
  6.4 +/- 0.6 (BHB); emPDF 6.7 (+2.0, -1.7) (BHB) and 7.8 (+2.6, -2.0) (RRL); joint 6.36
  (+0.53, -0.48), all in 10^11. The 8 per cent joint error rests on the mock covariance.

The paper says this itself: the joint estimate "should not be read as a substitute for the
individual measurements" and its calibration "is only as reliable as the mocks".

## 4. The new instrument: per-method curves

`fig10/desi-dr2-menc.csv` in the figure data holds, for the real Milky Way, the bias-corrected
median and 16th and 84th percentiles of M(<r) for each method and tracer: emPDF, NIMBLE-A and
NIMBLE-B at 25 radii from 20 to 80 kpc, GME at 13 radii from 50 to 80 kpc, and the per-tracer joint.
`fig09/` holds the method-to-method residual correlations at 30 and 80 kpc.

NIMBLE-A and NIMBLE-B are the only curves whose shape is measured. The paper's text about them:

- NIMBLE-B agrees between tracers "across nearly all radii".
- NIMBLE-A's RRL curve "rises much more quickly and flattens at a much higher mass" than its BHB
  curve beyond 30 kpc.
- A Milky Way that flattens beyond 80 kpc "only seems possible from the NIMBLE-A RRL modeling", and
  the authors attribute that curve to the tracer-density reconstruction.

That last point is the framework's own outer prediction (a plateau beyond about 90 to 100 kpc), so
the NIMBLE curves are where this release bears on it. This review printed the file's structure only
(`figdata_inventory.out`), not its values.

## 5. The virial mass

M200c = 1.19 (+0.14, -0.12) x 10^12 is an NFW extrapolation; the paper says it "requires
significant extrapolation" and reports no enclosed mass beyond 80 kpc.

- GME carries about 75 per cent of the weight, because its extrapolated M200c was accurate on the
  mocks. Its own potential parameters sit on the prior of section 2.
- Without GME the paper gets 1.52 (+0.35, -0.30) x 10^12: the centre moves up 28 per cent and the
  error doubles.
- GME's two tracers give 0.95 (+0.09, -0.08) and 1.19 +/- 0.09, about 2 sigma apart; their mock
  residuals at 80 kpc correlate at 0.88.

DW1e (the framework's plateau against M200c, FAIL) stands as frozen. What this adds: the number it
was graded against is not a measurement at 200 kpc, and its 11 per cent error is not a DESI
constraint there. The measurements that reach those radii are the literature points in
`fig13/` (4 halo-star rows and 4 satellite or globular-cluster rows beyond 100 kpc; values not read
here). The paper notes "a hint of a ceiling" near 8 x 10^11 in the distant halo-star results that
the satellite results do not show.

## 6. Other statements that touch the framework

- **Rotation curve.** The joint profile gives a circular speed of 204 km/s at 20 kpc falling to
  185 km/s at 80 kpc. The paper reads the Keplerian decline claimed from Gaia DR3 as an artefact. A
  Keplerian decline would have been a failure for any flat-curve law, so this is favourable, and
  equally so for NFW.
- **Measured without a mass model:** tracer density slope beyond 50 kpc 4.57 +/- 0.08 (RRL) and
  4.71 +/- 0.08 (BHB), moved six to seven prior widths from the prior, so data-driven. The
  anisotropy 0.33 to 0.34 +/- 0.05 equals its prior (0.30 +/- 0.05) and is not a measurement.
- **Table 4 as transcribed in `dw1.py`** matches the paper in all three columns and both error
  bars. An independent SI recomputation reproduces the lane's 80 kpc values (5.691 / 6.219; with the
  scalar-additive field 4.308 / 4.508).

## 7. Results IV (July 2026), for completeness

Lyman-alpha Alcock-Paczynski at z = 2.33: D_M/r_d = 39.32 +/- 0.33, D_H/r_d = 8.600 +/- 0.066,
correlation 0.225. The paper reports "excellent agreement" with the LambdaCDM prediction and about
2 sigma tension with the evolving-dark-energy prediction from DESI plus CMB. The preference for
evolving dark energy is 1.9 sigma for DESI alone and 2.7 sigma with the CMB (a shift of about 0.3
sigma toward a constant), and 3.0 to 3.5 sigma with supernovae.

For a0(z) = kappa c sqrt(G rho_DE(z)): dark energy is 5.8 per cent of H^2 at z = 2.33, so this point
alone resolves rho_DE(2.33)/rho_DE(0) to about +/- 0.26 at best, which is +/- 13 per cent in a0. An
illustrative evolving model (w0 = -0.75, wa = -0.86, values from memory) puts a0 at 0.82 of today's
at that redshift. The point leans toward constant a0 and cannot settle it. CFG681 to CFG689 still
use the older BAO-only pair (38.988 +/- 0.531, 8.632 +/- 0.101, correlation -0.431); if that row is
re-run the new pair replaces it and is not added to it.

## 8. What would decide something

1. **Now:** grade the framework's line against the NIMBLE curves in `fig10/`, per tracer, with the
   criteria frozen before the values are read. Amplitude at every radius, and the 50 to 80 kpc
   slope, on both footings, with and without the external field.
2. **When Valluri et al. appears:** the measured radial dispersion and tracer density profiles
   allow the Jeans mass to be recomputed without any LambdaCDM-calibrated correction.
3. **When DR2 is public (early 2027):** the stars themselves.
4. **Beyond 100 kpc:** the plateau against the literature points, not against M200c.

## Files

- `review_arith.py`, `review_arith.out`: the arithmetic quoted above (Table 4 against the A = 1
  line, slopes, the NFW comparator, the Lyman-alpha sensitivity).
- `figdata_inventory.py`, `figdata_inventory.out`: the calibration-side content of the figure data
  (mock truths, mock biases, correlations, GME posterior summaries) and the structure of the
  real-galaxy files. Takes the zip's path as its argument; the zip is not stored in the repository.

Sources: arXiv 2611.05518, 2611.05519, 2611.05520, 2611.05521, 2607.27410 (HTML, fetched
2026-11-12); Zenodo record 23712180. The three supporting papers were read by parallel readers and
their key statements checked against the text.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
