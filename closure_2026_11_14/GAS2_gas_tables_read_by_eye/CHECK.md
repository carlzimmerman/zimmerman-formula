# GAS2 check: every GAS1 number from the seven papers, read by eye from the PDF pages

Date: 2026-11-14. Not blind, not graded; relabels nothing; computes no forest number.

## Verdict first

- **151 of 151 table entries CONFIRMED BY EYE** (value and its uncertainty), plus 3 quoted statement numbers confirmed.
  No table value in GAS1's SOURCES.md is wrong.
- **2 CORRECTED**, both in GAS1's text rather than its tables:
  1. Kulkarni et al. 2015, Figure 14 caption (page 14): the flux-fitted scale is divided by **sqrt 2**, not 2 sqrt 2.
     The text layer drops the radical and prints "λps / 2"; the rendered legend and caption show sqrt 2. The page wins.
  2. Becker et al. 2013 (page 10): the Table 2 points are **not** 4 to 6 per cent below the Eq. 5 fit at every z
     checked. In tau they scatter both ways, from -5.8 to +5.4 per cent; at four of the bins GAS1 itself listed (3.35,
     3.45, 3.75, 3.85) the gap is +0.5, -1.0, +0.5, +0.5 per cent (`gas2_place.out`).
- **1 NOT FOUND**: the confidence level of Hiss et al. 2018 Table 4. The caption (page 20) says only "percentile based"
  errors and does not name the percentiles; GAS1's "16-84 %" is not on that page. Nothing else was searched for it.
- **1 wording correction (no number):** Rorai et al. 2017 do not define lambda_P as an exact Gaussian. The Gaussian
  exp(-k^2 lambda_P^2 / 2) of Eq. S21 is given "for example"; the kernel used is a cubic spline (Eq. S23) and lambda_P
  is defined as R_P / 3.25, the width of the Gaussian it "very closely resembles" in its centre (page 23). GAS1's
  "exactly" should read "to the accuracy of that approximation".

Method: `pdftotext -layout` only to find the page; each number then read on the page rendered by the file-reading
tool. Where the small print of a table was hard to read at that size, the same page region was rendered again at 220 to
250 dpi with `pdftoppm` (scratch files, not committed) and read from that image. Every page below was seen.

## Rorai et al. 2017 (arXiv:1704.08366)

Table S2, page 43. Caption: medians and 16 % / 84 % percentiles of the lambda_P posterior, with systematics in the last
two columns; "All columns except the first are in comoving kpc units." (seen).

| z | GAS1 | page | status |
|---|---|---|---|
| 2.0 | 82.1; stat 65.2 to 101.1; syst 59.9 to 105.6 | 82.1; 65.2, 101.1; 59.9, 105.6 | CONFIRMED BY EYE |
| 2.4 | 72.5; 55.6 to 95.8; 54.0 to 96.9 | 72.5; 55.6, 95.8; 54.0, 96.9 | CONFIRMED BY EYE |
| 3.0 | 113.8; 92.4 to 137.7; 91.4 to 138.6 | 113.8; 92.4, 137.7; 91.4, 138.6 | CONFIRMED BY EYE |
| 3.6 | 90.2; 60.1 to 123.6; 60.0 to 123.7 | 90.2; 60.1, 123.6; 60.0, 123.7 | CONFIRMED BY EYE |

Also on page 43, the error columns (comoving kpc), noise / resolution / metals / Lyman-limit systems: z 2.0: 9.9, 0.6,
5.9, 8.6; z 2.4: 0.4, 0.3, 5.7, 4.5; z 3.0: 4.7, 0.9, 3.5, 3.1; z 3.6: 0.5, 0.1, 1.0, 1.7. There are four bins only.

Table S3, page 43 (simulation, flux-power fit of Eq. S33, z = 3; does not count): standard 79.1, late reionization
heating 66.5, increased photoheating 106.5. GAS1's three values CONFIRMED BY EYE (3 entries).

Page 38, Section 9.3: the "almost one-to-one" relation between lambda_P and lambda_P,sim with scatter "less than 5%"
(Table S4, Fig. S11): CONFIRMED BY EYE. Table S4 (page 44) lists the 13 calibration runs; lambda_P,sim runs from 54.8 to
106.5 kpc.

## Kulkarni et al. 2015 (arXiv:1504.00366) (simulation values; do not count)

| item | GAS1 | page | status |
|---|---|---|---|
| fiducial (T0 = 9.5e3 K), z 3 | 79.0 comoving kpc | p. 13 text "79.0 comoving kpc"; p. 1 abstract λF = 79 kpc (comoving); Fig. 12 marks 79.0 | CONFIRMED BY EYE |
| hot run (T0 = 8.6e4 K) | 191.5 comoving kpc | p. 13 "191.5 comoving kpc" | CONFIRMED BY EYE |
| fitting form | Delta_F^2 = A k^n exp(-k^2 lambda^2) | p. 12 Eq. 16: A k^n exp(-k^2 / k_ps^2), lambda_ps = 1/k_ps (p. 13) | CONFIRMED BY EYE |
| Eq. 9 | delta_b / delta_m = exp(-k^2 lambda_F^2) | p. 4 Eq. 9, lambda_F from Eq. 8 | CONFIRMED BY EYE |
| Fig. 14 factor | 2 sqrt 2 | p. 14: legend "λps/√2", caption divides by sqrt 2 | **CORRECTED 2 sqrt 2 -> sqrt 2** |

Note: Fig. 12 (page 13) marks a second value, 183.4 kpc, for the hot run; the text gives 191.5. GAS1 used the text
value; both are on the page.

## Walther et al. 2019 (arXiv:1808.04367)

Table 3 (flat prior on mean flux), page 31; Table 4 (titled "Strong Prior" on mean flux; GAS1 calls it Gaussian),
page 32. Column headers: lambda_P [kpc], T0 [1e4 K], gamma, mean flux. Both captions: errors "purely statistical";
systematics (box size, fixed cosmology, cosmic variance) expected at about 0.5 to 1 sigma_stat more. The level is set by
Fig. 7's caption (page 14): median and the region between the 16 % and 84 % quantiles. All read at 220 dpi.

| quantity | prior | z values (GAS1's) | status |
|---|---|---|---|
| lambda_P | flat | 2.0 93.0 +8.3/-17.4; 2.2 91.0 +6.3/-6.4; 2.4 87.2 +5.4/-5.1; 2.8 93.8 +4.2/-4.2; 3.0 80.6 +6.0/-5.6; 3.2 84.9 +4.7/-6.3; 4.2 77.0 +3.6/-6.0; 4.6 73.7 +4.9/-5.8 | 8 CONFIRMED BY EYE |
| lambda_P | strong | 2.0 75.5 +9.8/-6.4; 2.2 79.4 +5.1/-5.0; 2.4 81.1 +4.6/-4.7; 2.8 91.3 +4.5/-5.3; 3.0 81.7 +5.8/-5.9; 3.2 83.4 +5.6/-5.3; 4.2 77.5 +3.3/-5.4; 4.6 76.2 +4.2/-5.4 | 8 CONFIRMED BY EYE |
| gamma | flat | 2.0 to 4.6, 12 rows as in GAS1 | 12 CONFIRMED BY EYE |
| gamma | strong | 2.0 to 4.6, 12 rows as in GAS1 | 12 CONFIRMED BY EYE |
| T0 | flat | 2.0 to 4.6, 12 rows as in GAS1 | 12 CONFIRMED BY EYE |
| T0 | strong | 2.0 to 4.6, 12 rows as in GAS1 | 12 CONFIRMED BY EYE |
| mean flux | flat | 2.0 0.831 +0.033/-0.011; 2.2 0.796 +0.010/-0.009; 2.4 0.772 +0.013/-0.012; 2.8 0.688 +0.013/-0.010; 3.0 0.694 +0.009/-0.015; 3.2 0.623 +0.018/-0.019; 4.2 0.355 +0.025/-0.031; 4.6 0.278 +0.023/-0.028 | 8 CONFIRMED BY EYE (errors not in GAS1; added here) |
| mean flux | strong | 2.0 0.865 +0.015/-0.019; 2.2 0.825 +0.009/-0.008; 2.4 0.799 +0.008/-0.008; 2.8 0.719 +0.008/-0.008; 3.0 0.687 +0.008/-0.008; 3.2 0.631 +0.007/-0.008; 4.2 0.346 +0.025/-0.022; 4.6 0.254 +0.021/-0.020 | 8 CONFIRMED BY EYE (errors added) |

The tables also hold rows GAS1 did not list (z 1.8, 2.6 for lambda_P and mean flux, 3.4 to 3.8 for lambda_P, 4.0, 5.0,
5.4). There is no z 4.4 row. The full rows used for placement are typed into `gas2_place.py`.

Page 20: the warning that the lambda_P uncertainties "might still be somewhat underestimated" is CONFIRMED BY EYE.

## Gaikwad et al. 2021 (arXiv:2009.00016)

Table 2, page 14, "Measurements of T0, gamma with total uncertainty" (read at 220 dpi). The table caption names no
level; the same page calls its contours and agreement 1 sigma (Fig. 11 caption and text).

| z | T0 (K) | gamma | status |
|---|---|---|---|
| 2.0 | 9500 +- 1393 | 1.500 +- 0.096 | CONFIRMED BY EYE |
| 2.2 | 11000 +- 1028 | 1.425 +- 0.133 | CONFIRMED BY EYE |
| 2.4 | 12750 +- 1132 | 1.325 +- 0.122 | CONFIRMED BY EYE |
| 2.6 | 13500 +- 1390 | 1.275 +- 0.122 | CONFIRMED BY EYE |
| 2.8 | 14750 +- 1341 | 1.250 +- 0.109 | CONFIRMED BY EYE |
| 3.0 | 14750 +- 1322 | 1.225 +- 0.120 | CONFIRMED BY EYE |
| 3.2 | 12750 +- 1493 | 1.275 +- 0.129 | CONFIRMED BY EYE |
| 3.4 | 11250 +- 1125 | 1.350 +- 0.108 | CONFIRMED BY EYE |
| 3.6 | 10250 +- 1070 | 1.400 +- 0.101 | CONFIRMED BY EYE |
| 3.8 | 9250 +- 876 | 1.525 +- 0.140 | CONFIRMED BY EYE |

(20 entries.) Table 1, page 3, mean flux, no level stated (as GAS1 said): 2.0 0.8690 +- 0.0214, 2.2 0.8261 +- 0.0206,
2.4 0.7919 +- 0.0210, 2.8 0.7398 +- 0.0212, 3.0 0.7105 +- 0.0213, 3.2 0.6731 +- 0.0223: 6 CONFIRMED BY EYE. Rows GAS1
did not list: 2.6 0.7665 +- 0.0216, 3.4 0.5927 +- 0.0247, 3.6 0.5320 +- 0.0280, 3.8 0.4695 +- 0.0278. Page 3 also says
all distances are comoving unless stated.

## Hiss et al. 2018 (arXiv:1710.00700)

Table 4, page 20, "Measurements and values adopted" (read at 250 dpi). Caption: median and "percentile based" errors;
which percentiles is not stated on this page -> level NOT FOUND (page 20 caption only).

| z | T0 (K) | gamma | status |
|---|---|---|---|
| 2.0 | 13721 +1694/-2152 | 1.47 +0.12/-0.1 | CONFIRMED BY EYE |
| 2.2 | 10927 +1961/-3843 | 1.67 +0.27/-0.14 | CONFIRMED BY EYE |
| 2.4 | 13334 +1206/-1530 | 1.56 +0.12/-0.12 | CONFIRMED BY EYE |
| 2.6 | 16281 +1940/-1601 | 1.38 +0.08/-0.1 | CONFIRMED BY EYE |
| 2.8 | 20036 +1416/-1507 | 1.29 +0.07/-0.07 | CONFIRMED BY EYE |
| 3.0 | 18371 +1087/-1388 | 1.12 +0.12/-0.06 | CONFIRMED BY EYE |
| 3.2 | 16244 +1153/-1135 | 1.38 +0.13/-0.13 | CONFIRMED BY EYE |
| 3.4 | 13439 +1542/-2318 | 1.31 +0.14/-0.1 | CONFIRMED BY EYE |

(16 entries.)

## Boera et al. 2019 (arXiv:1809.06980)

Table 5, page 14: best fits and "marginalized 68%" intervals (read at 250 dpi).

| z | T0 (1e3 K) | gamma | tau_eff | status |
|---|---|---|---|---|
| 4.2 | 8.13 +1.34/-0.97 | 1.21 +0.23/-0.28 | 1.02 +0.04/-0.04 | CONFIRMED BY EYE |
| 4.6 | 7.31 +1.35/-0.88 | 1.29 +0.19/-0.26 | 1.41 +0.08/-0.09 | CONFIRMED BY EYE |
| 5.0 | 7.37 +1.67/-1.39 | 1.33 +0.18/-0.27 | (1.69 +0.10/-0.11, not in GAS1) | CONFIRMED BY EYE |

(8 entries: T0 x 3, gamma x 3, tau_eff x 2.)

## Becker et al. 2013 (arXiv:1208.2584)

| item | GAS1 | page | status |
|---|---|---|---|
| Eq. 5 form and [tau0, beta, C], z0 | tau0 ((1+z)/(1+z0))^beta + C; [0.751, 2.90, -0.132], z0 = 3.5 | p. 10, Eq. 5 and text; Table 3 caption repeats them | CONFIRMED BY EYE |
| parameter errors | about 0.022, 0.116, 0.022 (from the covariance) | p. 10 Table 3 diagonal 0.00049, 0.01336, 0.00049; square roots 0.0221, 0.1156, 0.0221 | CONFIRMED BY EYE (diagonal); the square roots are my arithmetic |
| error level | "The errors are 1σ" | p. 8, Fig. 4 caption: error bars are 1 sigma | CONFIRMED BY EYE |
| C set by scaling to Faucher-Giguere et al. 2008 over 2.2 to 2.5 | as stated | p. 10 | CONFIRMED BY EYE |
| fit vs points: mean fractional flux deviation of two per cent | as stated | p. 10 ("two per cent"; formal chi^2 64 for 28 bins) | CONFIRMED BY EYE |
| gap "4 to 6 % below the fit in tau at every z checked" | as stated | p. 10 tables, computed in `gas2_place.out` | **CORRECTED** (see verdict) |

Table 2, page 10, column F(z) (read at 220 dpi):

| z | GAS1 F | page | status |
|---|---|---|---|
| 2.15 | 0.8806 +- 0.0103 | 0.8806 +- 0.0103 | CONFIRMED BY EYE |
| 2.25 | 0.8590 +- 0.0098 | 0.8590 +- 0.0098 | CONFIRMED BY EYE |
| 2.95 | 0.6966 +- 0.0084 | 0.6966 +- 0.0084 | CONFIRMED BY EYE |
| 3.05 | 0.6670 +- 0.0082 | 0.6670 +- 0.0082 | CONFIRMED BY EYE |
| 3.35 | 0.5762 +- 0.0074 | 0.5762 +- 0.0074 | CONFIRMED BY EYE |
| 3.45 | 0.5548 +- 0.0071 | 0.5548 +- 0.0071 | CONFIRMED BY EYE |
| 3.75 | 0.4723 +- 0.0068 | 0.4723 +- 0.0068 | CONFIRMED BY EYE |
| 3.85 | 0.4470 +- 0.0072 | 0.4470 +- 0.0072 | CONFIRMED BY EYE |
| 4.35 | 0.3441 +- 0.0102 | 0.3441 +- 0.0102 | CONFIRMED BY EYE |
| 4.45 | 0.3216 +- 0.0094 | 0.3216 +- 0.0094 | CONFIRMED BY EYE |

The other 18 bins (2.35 to 4.85) were read from the same page and are typed into `gas2_place.py`.

## Tally

| status | count |
|---|---|
| CONFIRMED BY EYE, table entries (value with its uncertainty) | 151 (Rorai 7, Kulkarni 2, Walther 80, Gaikwad 26, Hiss 16, Boera 8, Becker 12) |
| CONFIRMED BY EYE, quoted statement numbers (Rorai "less than 5%", Becker "two per cent", Becker 1 sigma) | 3 |
| CORRECTED | 2 (Kulkarni factor; Becker gap) |
| NOT FOUND | 1 (Hiss percentile level) |
| wording correction, no number | 1 (Rorai kernel is a spline approximating the Gaussian) |

Becker's 12 entries are the Eq. 5 parameter set, the covariance diagonal and the 10 F(z) rows.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
