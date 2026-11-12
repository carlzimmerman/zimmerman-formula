# EUC5 (DYNAMICAL BOOST): RESULT

2026-11-12. Criteria 7fa4e74869 (committed alone, before any script or lens dispersion).

## Verdict: NOT EVALUABLE / NOT EVALUABLE (canonical / alt)

The sample is too small. Of the 1,240 lenses of sample S north of Dec −15, only 20 have an SDSS DR17 spectrum within
1″; 16 pass the frozen quality cuts; **7 are in sample P, against the 30 the gate requires.** Euclid's northern field
lies mostly outside the SDSS / BOSS spectroscopic footprint, and most lens galaxies are fainter than its targets. The
machinery is sound (all instrument checks pass; the mutation twin exits 1). The numbers below are readings on 16
lenses, not a gate.

κ = ½ FITTED. Footings never pooled. No outcome favours the framework.

## 1. Instrument checks (all pass; run before any lens dispersion was read)

| Check | Result |
|---|---|
| J1 Plummer sphere, projected dispersion | max error 7.1e-4 |
| J2 power-law tracer in a flat rotation curve, β = 0.3 | max error 6.4e-5 |
| J3 SLACS, lensing-calibrated masses: predicted / measured dispersion | median 0.966, mean 0.978 (A85: 0.977), scatter 0.125 |
| J4 SLACS, `b_dyn` against `b_lens` at the true source redshift | +0.085 against +0.070; median difference +0.032 dex |
| MUTATE newton | `b_med` on P −0.126 → −0.082 and −0.134 → −0.082; exit 1 |

On SLACS the law's lensing and the law's dynamics ask for the same stellar mass to 0.03 dex.

## 2. The data

20 SDSS rows on 20 lenses. Removed: 1 redshift warning, 3 on the dispersion cuts, none on the photo-z match. 16 remain
(15 BOSS fibres, 1 SDSS), 7 of grade A. Medians: z_l = 0.49, dispersion 219 km/s with a 16 % error, log M★ = 11.63,
θ_E = 1.34″. These are massive, wide-ish lenses: 13 of the 16 have θ_E above 0.9″.

## 3. Readings (N = 16; not a gate)

Law S, β = 0, seeing 1.5″.

| Quantity | canonical | alt |
|---|---|---|
| `b_dyn` median, sample S (N = 16) | +0.051 [−0.156, +0.242] | +0.040 [−0.165, +0.235] |
| `b_dyn` median, sample P (N = 7) | −0.126 [−0.172, +0.253] | −0.134 [−0.181, +0.244] |
| source-free lensing bound `b∞`, same 16 lenses | +0.179 | +0.154 |
| median (`b_dyn − b∞`) | −0.056 | −0.041 |
| lenses whose dynamics fall below their lensing bound | 9 of 16 | 9 of 16 |

Anisotropy (β = ±0.2) and seeing (1.2″, 1.8″) move `b_med` on P by at most 0.008 dex. One lens
(EUCL-DR1-L010930, dispersion 411 ± 87 km/s) reads +0.71 and is kept.

**What the reading says, with its limits.** The stars in these 16 galaxies move as the law says for about a Salpeter
stellar mass (+0.04 to +0.05 dex), as in SLACS (+0.085). Their lensing asks for more than that even with the source at
infinity (+0.15 to +0.18), and more again at any real source redshift. In SLACS the two agree. If this held up it
would mean the extra mass is seen by the light, which crosses the whole line of sight, more than by the stars inside a
1″ fibre: an extended component around the galaxy rather than extra mass in its centre. That is the same picture
EUC4's wide lenses point to.

It does not hold up yet. Each `b_dyn` carries about 0.15–0.2 dex of noise from a 16 % dispersion error, so the median
difference of −0.04 to −0.06 dex is uncertain by about 0.06 dex, and the interval on `b_dyn` itself spans −0.16 to
+0.24. Sixteen lenses cannot separate "dynamics equals the lensing bound" from "dynamics is 0.2 dex below the true
lensing value".

## 4. What would make it evaluable

The 382 DESI spectra of 369 Euclid lens galaxies are already on disk (EUC2). They carry no pipeline dispersion; one
would have to be fitted from each spectrum with stellar templates. 39 of those lenses are in sample P, so N ≥ 30 is
within reach if most fits succeed. That needs a template-fitting package and template library that are not installed
here. Not done.

## 5. Files

`euc5_fetch.py` (NOIRLab Data Lab TAP, `sdss_dr17.specobj`; coordinate boxes, because the service does not translate
ADQL cone searches for this table), `euc5_sdss_matches.csv` (20 rows), `euc5.py`, `euc5.out`, `euc5_results.json`,
`euc5_per_lens.csv` (16 lenses), `euc5_MUTATE_newton.out` / `_results.json` (exit 1). EUC1's code is imported.
