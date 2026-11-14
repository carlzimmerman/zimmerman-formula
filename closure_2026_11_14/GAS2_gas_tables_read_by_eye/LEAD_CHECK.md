# GAS2 LEAD CHECK (2026-11-14): commit ids, what the lead checked, and what GAS2 changes in GAS1

Written by the lead session after the lane's files were committed. A verification lane: not blind, not graded, relabels
nothing, computes no forest number. The agent's files in this folder are not edited.

## Commit ids

| what | local | origin |
|---|---|---|
| SCOPE.md (alone, before any PDF page was opened) | a8fd76da89 | 1d96cd2c5c |
| gas2_place.py and gas2_place.out | 0bb3d53b13 | 40d4787839 |
| CHECK.md, QUESTIONS.md, PLACEMENTS.md | 74a17e1d5e | 44116f8694 |

## What the lead checked

- **Tool calls**, listed by script: 87 calls, 59 of them page or file reads, no web call, no copy of a PDF into the
  repository. The committed files hold no PDF, no image and no home path.
- **The placement script** re-run from a copy in a new folder at the same depth: its printed output is byte-identical
  to the committed `gas2_place.out`.
- **Two pages read by the lead, by eye, from the same PDFs:**
  - Kulkarni et al. 2015, page 14, Figure 14: the legend reads lambda_ps / sqrt 2 and the caption says the pressure
    smoothing scale "has been divided by" sqrt 2 for consistency with the density-defined scales. So the factor is
    sqrt 2, as GAS2 says, and not the 2 sqrt 2 that GAS1 took from the fetched text.
  - Rorai et al. 2017, page 43, Table S2: z 2.0, 2.4, 3.0, 3.6 read 82.1, 72.5, 113.8, 90.2 comoving kpc; the bounds
    with systematics are 59.9 to 105.6, 54.0 to 96.9, 91.4 to 138.6 and 60.0 to 123.7. Table S3 on the same page gives
    79.1 for the standard simulation at z 3. All as GAS2 and GAS1 have them.
- The seven PDFs were downloaded by the lead on the owner's go from arxiv.org (30.1 MB in total) into the
  `_external_data/gas1_papers_2026_11_14/` folder beside the repository root, with a note of sizes and md5 sums. They
  are not in the repository.

## What GAS2 changes in GAS1 (GAS1's files are left as they are)

- **The numbers are no longer provisional in the house sense**: 151 table entries were read from the rendered pages
  and agree with GAS1; two statements are corrected and one confidence level (Hiss et al. 2018, Table 4) is not on the
  page GAS1 cited.
- **GAS1's second reading of the smoothing-scale convention is void.** It rested on the misread factor above. With
  sqrt 2 the flux-fitted scale of Kulkarni et al. and Walther et al. maps onto the record's density smoothing at factor
  1. One reading is left, and under it half the smoothing scale (39.5 comoving kpc) is inside twice the error at z 2.2
  only and outside the measurements at z 3.0 and 4.4. GAS1's lead check said this question was open; it is closed.
- **GAS1's "exactly" is too strong.** Rorai et al. 2017 use a cubic-spline kernel and quote the Gaussian only as its
  near equivalent, so the record's Gaussian matches their definition approximately, at factor 1.
- **Becker et al. 2013:** the binned points scatter about the fit by a few per cent in both directions; they do not sit
  4 to 6 per cent below it. The paper says the fit was made to corrected flux ratios with the offset set separately.
- No placement cell changes level. The reading of the FRAGILE flags is as GAS1's lead check gave it, with the caveat
  removed: the flags through gamma 1.2 and 1.6 stay live; the flags that rest only on half the smoothing scale rest on
  a value the measurements mostly exclude.

## What is still not checked

- Walther et al. 2019's table errors are statistical only; its captions say systematics would add about half to one
  statistical error. The placements use the statistical errors.
- Twice the 1 sigma half-width stands in for each paper's 2 sigma bound, since none gives its own.
- The papers GAS1 marked as abstract-level only (Bolton 2014, Rorai 2018, Kamble 2020, Turner 2024) were not opened;
  they decide no cell.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
