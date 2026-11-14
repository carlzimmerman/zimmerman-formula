# GAS2 scope (frozen file; committed alone before any PDF page is opened)

Date: 2026-11-14. Lane type: proof-reading of a look-up lane. Not blind, not a graded test. It relabels nothing and
computes no forest number.

## What I had seen before freezing

The two briefs, and GAS1's five committed files (SCOPE.md, SOURCES.md, CONVENTION.md, READING.md, LEAD_CHECK.md). I have
listed the PDF folder but have not run `pdftotext` on any PDF and have not opened any PDF page.

## Source of the pages

Seven PDFs in the `_external_data/gas1_papers_2026_11_14/` folder beside the repository root (owner-approved download;
never copied into or committed to the repository). Method: `pdftotext -layout` only to find the page; the number is read
from the rendered page. A number is READ BY EYE only if seen on the rendered page; where the text layer and the page
disagree, the page wins and that is said.

## GAS1 SOURCES.md rows to be checked (every SEEN IN TEXT row from the seven papers)

1. Rorai et al. 2017 (arXiv:1704.08366): Table S2, lambda_P median, 16th and 84th percentiles with and without
   systematics, at every redshift bin (GAS1 lists z 2.0, 2.4, 3.0, 3.6); the comoving-units statement; Table S3
   simulation values at z 3.0 (79.1, 66.5, 106.5); the "one-to-one" calibration statement (Section 9.3); the definition
   of lambda_P (equation).
2. Walther et al. 2019 (arXiv:1808.04367): Table 3 (flat mean-flux prior) and Table 4 (Gaussian mean-flux prior), every
   row GAS1 lists: lambda_P, gamma, T0 and mean flux with their errors, at z 2.0 to 4.6; the confidence level of the
   errors; the "somewhat underestimated" warning.
3. Kulkarni et al. 2015 (arXiv:1504.00366): 79 comoving kpc at z 3 (fiducial, T0 9.5e3 K) and 191.5 (T0 8.6e4 K); the
   flux-power fitting form; Eq. 9 (lambda_F); the figure caption GAS1 calls Figure 14.
4. Gaikwad et al. 2021 (arXiv:2009.00016): Table 2 (T0, gamma, total uncertainty, z 2.0 to 3.8) and Table 1 (mean flux,
   z 2.0 to 3.2), with the stated confidence level.
5. Hiss et al. 2018 (arXiv:1710.00700): Table 4 (T0 and gamma, z 2.0 to 3.4) with the stated level.
6. Boera et al. 2019 (arXiv:1809.06980): Table 5 (T0, gamma, tau_eff at z 4.2, 4.6, 5.0) with the stated level.
7. Becker et al. 2013 (arXiv:1208.2584): Eq. 5 parameters [tau0, beta, C] and z0; Table 2 F(z) and errors at every
   redshift GAS1 lists (2.15, 2.25, 2.95, 3.05, 3.35, 3.45, 3.75, 3.85, 4.35, 4.45); Table 3 covariance if present; the
   statements about C and the 2 per cent deviation.

PROVISIONAL rows from other papers (Bolton 2014, Rorai 2018, Kamble 2020, Turner 2024) are out of scope and stay
PROVISIONAL.

## Statuses (one per checked number)

CONFIRMED BY EYE (the page shows GAS1's value), CORRECTED (old -> new, with page), NOT FOUND (say where I looked).

## The four open questions

1. Kulkarni et al. 2015: in the caption GAS1 calls Figure 14, what exactly is divided, by what factor, and what that
   implies for comparing their 79 comoving kpc with a density field smoothed by exp(-k^2 lambda^2 / 2); the paper's own
   definition of lambda_P with its equation number.
2. Walther et al. 2019: are lambda_P values comoving or proper kpc, and how is lambda_P defined (equation)?
3. Becker et al. 2013: read Table 2 and Eq. 5 from the page; is the 4 to 6 per cent gap in tau real, and does the paper
   explain it?
4. Rorai et al. 2017: Table S2 at every redshift bin (median, 16th, 84th, with and without systematics) and the
   definition of lambda_P (equation), to confirm it is the Gaussian exp(-k^2 lambda^2 / 2) on the density.

## Placement rule

GAS1's placement rule (its SCOPE.md, "The rule (restated, frozen)") is reused unchanged: same anchors z 2.2, 3.0, 4.4,
same 0.3 redshift window, same bracket values, same 2 sigma construction (twice the 1 sigma half-widths where a paper
gives no 2 sigma bound), simulation values do not count, disagreements given both ways. GAS1's Reading 1 / Reading 2
split is kept unless the page answer to question 1 settles it, in which case that is said and both are still shown.

## Files

SCOPE.md (this), CHECK.md, QUESTIONS.md, PLACEMENTS.md, and a small placement script with its output if one is used.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
