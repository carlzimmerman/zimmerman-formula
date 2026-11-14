# DBL1 scope (frozen file of this lane; written 2026-11-14 before any look-up)

A look-up lane. Not blind, not graded. It relabels nothing and computes no forest number.

## Question

The forest gate of the record reads the DESI DR1 one-dimensional flux power spectrum (quadratic maximum likelihood
estimator) from the public archive `_external_data/desi_dr1_p1d_qmle/raw/data_points.tar` (never committed), member
`desi_y1_baseline_p1d_sb1subt_qmle_power_estimate_contcorr_v3.fits`, extension `P1D_BLIND`, whose header carries
`BLINDING = desi_y1`. Are the values in that public table the unblinded, published measurement?

## What was seen before writing this file

Only the brief: the extension name, the header keyword value, the loader's location
(`closure_2026_11_09/SS1_self_shielded_conversion/ss1_cosmo.py`, function `forest_setup`) and the archive's file
listing on disk. No header, column or value of the file has been read in this lane, and no web page has been opened.

## Items

1. From the file: every extension, header keyword and column of the three `.fits` members of the archive and of the
   copy under `_external_data/desi_dr1_p1d_qmle/ext/`; what `PLYA`, `PRAW`, `PFID`, `PINPUT`, `PSMOOTH`, `ThetaP`
   appear to be from their values; what the figure-data text files (`fig_*.txt`, in particular `fig_8a_qmle.txt`,
   `fig_8a_fft.txt`, `fig_8b_edr.txt`, `fig_9_eboss_dr1_dla.txt`) can and cannot tell about blinding. Script
   `dbl1_file.py`, output `dbl1_file.out`, write-up `FILE_FACTS.md`.
2. From the literature and release (web): the paper, its blinding section, when and how it was unblinded, the public
   data-release description, and the estimator code's documentation or source for the `BLINDING` keyword and the
   `P1D_BLIND` extension name. Write-up `SOURCES.md`, log `fetch_log.md`.
3. If a published number can be seen in fetched text: compare it with the table on disk.

## Verdict rule (frozen)

- **UNBLINDED: ESTABLISHED** if a primary source (paper text, release record or code, SEEN IN TEXT) says the released
  table is the unblinded measurement, or the keyword's meaning is documented and consistent with that, and no file fact
  contradicts it.
- **BLINDED: ESTABLISHED** if a primary source or a file fact shows the released values still carry a blinding.
- **NOT ESTABLISHED** otherwise, stating exactly what is missing. A plausible argument is not rounded up.
- A snippet or summariser paraphrase is PROVISIONAL and cannot carry either ESTABLISHED word alone.

## Hand estimate (before any look-up)

UNBLINDED: ESTABLISHED 0.55; NOT ESTABLISHED 0.40; BLINDED: ESTABLISHED 0.05. Reason: public releases accompany
unblinded papers, and figure files that agree with the table would support it, but the keyword's meaning may be
undocumented.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
