# KL1 PART B FROZEN CRITERIA: KiDS-Legacy's raw data through the same machinery and gate

Committed alone, before the KiDS-Legacy tarball is downloaded or opened. **No download has been made; Part B runs only after the
owner's go, relayed by the closure chat.** Part A's criteria are `FROZEN_CRITERIA.md` (99a42c78ef); everything not named here is
as there. TEST lane; relabels nothing, adopts nothing. **kappa = 1/2 FITTED; not theory closed.** Footings never pooled. Cold dark
energy, never a particle. CO2's label is not changed.

## 1. The data (after the go only)

- Source: `https://kids.strw.leidenuniv.nl/sci_data/KiDS_Legacy_cosmic_shear_data_release.tar.gz` (web look-up, PROVISIONAL:
  about 125 MB with data vectors, covariances, n(z) and chains). Downloaded into a new, empty folder
  `_external_data/kl1_kids_legacy_<date>/` (outside the repository, untracked). URL, date, size and sha256 recorded in
  `FETCH_LOG_PARTB.md` in this lane before anything is read.
- Untrusted data: extracted only inside that folder (no member path outside it, no links followed); never executed; KL1 scripts
  stay in this lane and read it with `python3 -I`, passing paths as arguments. Nothing from the tarball is committed.
- Read: the cosmic-shear xi+- data vector of the fiducial catalogue, its published covariance, the source n(z) per tomographic
  bin, the delta-z prior (means and covariance) and the published xi+- scale cuts, each from the release's own files. If the
  release carries no xi+- data vector (only COSEBIs or band powers), Part B reads NOT EVALUABLE BY THIS MACHINERY and an
  amendment, committed alone before any number, must say how to swing harder (for example the COSEBI filters applied to the same
  model xi+-).
- Not read into any verdict: the release's chains, best-fit parameters or theory vectors (survey posteriors). They may be quoted
  as context.

## 2. Machinery

- CFG592's projection, Hankel transforms and fit, generalised only in the loader: N tomographic bins (Legacy has six), the
  release's own angular bins and cuts, its delta-z prior entered as KiDS-1000's is (shifts in the decorrelated basis with unit
  prior widths; the Cholesky factor of the release's delta-z covariance), one alignment amplitude, no shear-bias parameter if the
  release puts the shear-bias uncertainty in its covariance (as KiDS-1000's "with_m_bias" file did), otherwise the release's
  shear-bias priors as parameters.
- The same model as Part A (S0 x R_tot moved by the run's response), the same support cut (>= 0.9 inside the run's k range).
- Rows: B0 (as CO2: CO2's target sigma8, published covariance, CO1's layout), B1 (A1's target), B2 (A2's covariance at the model,
  with the area fitted the same way from the release's per-bin shape noise and densities), B3 (A3's gas), BALL = B1 + B2 + B3,
  and BALL with A5c1 (alignment off) and A5a (long modes) as reported brackets. Each: chi^2, p, label by CO2's lines, the
  release's best sigma8 for form B's spectrum with its width, the gap in widths, delta-z pulls.

## 3. Known answers (before any graded number)

- KB1: the loader returns the release's own counts (data points per statistic, bins, a positive-definite covariance) and n(z) that
  integrate to 1 per bin.
- KB2: Part A's KA0 reproduced unchanged through the generalised loader on KiDS-1000 (157.89 / 159.35).
- KB3: Part A's KA2 rule on the Legacy covariance passes (i) and (ii); else B2 and BALL read NO VERDICT.
- KB4 (reported, context): the Legacy best sigma8 for form B's spectrum against KiDS-1000's (Part A row A0), and the published
  Legacy S8 0.815 +0.016 -0.021 (Wright et al. 2025) beside it; no tolerance, it is not a gate.

## 4. MUTATE

- MB1: sigma8 0.90 under BALL must give p < 0.0027 on Legacy.
- MB2: the delta-z prior means of the release replaced by KiDS-1000's (bins matched by mean redshift) must move the Legacy best
  sigma8 by at least 0.5 width (the redshift calibration has teeth in this machinery).

## 5. Label

- Per data set by CO2's lines at BALL. **Overall (Part B), per footing:** the worse of KiDS-Legacy and DES Y3 at their ALL rows,
  named AMPLITUDE CONSISTENT WITH RAW LENSING / TENSION / EXCLUDED / NO VERDICT as Part A's section 6; it is the lane's label for
  the newest release of each survey, with the neutrino floor. Part A's label for KiDS-1000 stays beside it.
- What counts against form B: BALL at TENSION or EXCLUDED on Legacy; the gap above 2 widths on Legacy; MB1 not biting.

## 6. Hand estimate (before any download)

Legacy's own S8 (0.815) sits about 0.06 above KiDS-1000's for comparable models. For form B's spectrum I expect the Legacy best
sigma8 near 0.78 to 0.80 (width about 0.015 to 0.02), so B1's gap about 1 to 2.5 widths and BALL's about 0.5 to 2; label at
BALL most likely CONSISTENT, TENSION possible.
