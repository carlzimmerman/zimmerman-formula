# External evidence for ECLIPSE screening (2026-11-13)

## Spectroscopic redshifts in the release

Primary ECLIPSE-A paper: https://eceb.astro.uni-bonn.de/public/dr1/lines.pdf (downloaded to /tmp/eclipse_lines.pdf; text /tmp/eclipse_lines.txt).
Section 5, page 5: DESI DR1 spectra vetted by Storfer et al. (in preparation) yield 351 deflector-only redshifts (95 A,146 B,110 C), eight source-only (4 A,4 B), and 20 pairs (12 A,5 B,3 C). Spectroscopy is not synonymous with a secure lens configuration. Appendix B illustrates the three C pairs.

IMPORTANT: direct inspection of the release object CSV and README finds only `desi_deflector_specz`, NOT source spectroscopic redshifts or their quality flags. Therefore the paper's 17 A/B paired systems cannot be isolated from this field alone. Do not label all rows with DESI deflector redshifts as having measured source distances.

## Placeholder quantities and masses

Primary portal documentation: https://euclid-eclipse-lenses.org/about
The time-delay prediction files `witt_wynne.csv` / `.in` use placeholder redshifts. These are not measured lens/source distances. Models assume an isothermal mass profile with external shear. Einstein-radius files include posterior intervals, but image model results are not independent kinematic observations.

The same documentation states stellar masses are Prospector fits with redshift FIXED TO THE PHOTOMETRIC REDSHIFT. They are surviving mass in living stars and remnants, log10(Mstar/Msun), with a Salpeter IMF and median/68% interval. Chabrier or Kroupa would reduce them by about 0.2–0.25 dex. Photometric-z intervals are 70%, not 68%.

ECLIPSE-D primary paper: https://eceb.astro.uni-bonn.de/public/dr1/nersesian.pdf, page 2: flat Planck2016 cosmology H0=67.74 km/s/Mpc, Omega_m=0.3089, Omega_Lambda=0.6911. It does not derive source photometric redshifts/physical properties (page 2). Its stricter science sample of 9538 is distinct from the larger released table. Replacing lens photo-z by spec-z without revisiting mass/distance assumptions is inconsistent.

## Public external kinematic catalogue fetched

SLACS Auger et al. 2009: https://arxiv.org/abs/0911.2471 ; dataset https://cdsarc.cds.unistra.fr/viz-bin/cat/J/ApJ/705/1099
Exact retrieved URL: https://vizier.cfa.harvard.edu/viz-bin/asu-tsv?-source=J/ApJ/705/1099/lenses&-out.all&-out.max=unlimited
Saved bytes: `inputs/external_slacs_auger2009.tsv` (27419 bytes); SHA256 `437c41e2492ae4876f78f54fc6cc7f14d9ad859dfaa133e1ddd581a6af65140e`.
85 rows. Columns include `SDSS`, `RAJ2000`, `DEJ2000`, `zlens`, `zsrc`, `sigma` (observed lens-galaxy velocity dispersion, km/s), `e_sigma`; plus stellar masses and Einstein radii. An in-memory tangent-plane nearest-neighbour search found NO matches within 10 arcsec to the ECLIPSE object CSV. This is a bounded catalogue-overlap check, not a claim that ECLIPSE lacks all external kinematics.

Additional primary SLACS VIMOS reference: https://academic.oup.com/mnras/article/419/1/656/1005904 . Table 1 lists lens/source redshifts, SDSS and VIMOS dispersions, coordinates, photometry and radii.
Additional un-fetched lead: 2026 TDCOSMO XXI SL2S spectra dataset https://vizier.cfa.harvard.edu/viz-bin/VizieR-3?-source=J%2FA%2BA%2F705%2FA13 ; 47 spectra, coordinates and instrument metadata. Do not assume its table contains the dispersion measurements. Earlier SL2S imaging/mass catalogue J/ApJ/777/97 is not itself verified here as a source of measured dispersions.

## Individual FOR J0332 fit inspected

Public lens page: https://euclid-eclipse-lenses.org/lens.html?lens=Tile102034383RA0532498193624DECNEG0359643115588
Direct figure: https://euclid-eclipse-lenses.org/files/Tile102034383RA0532498193624DECNEG0359643115588/results/vis_pix_fit.png
Downloaded and visually inspected: the bright upper/right arc and faint lower-left counterimage are reproduced in the image model; the lens-light-subtracted panel clearly separates the extended arc. Normalized residuals contain isolated outliers, but no comparably bright unmodelled arc is visually apparent. This is qualitative visual QA, not a quantitative goodness-of-fit test or a test of the modified-gravity prediction.
Primary source PDFs/text and SHA256+URLs saved in inputs/external_primary_provenance.json.
