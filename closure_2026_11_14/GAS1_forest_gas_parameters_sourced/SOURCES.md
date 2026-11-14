# GAS1: sources for the forest gate's gas parameters

Date: 2026-11-14.

## How to read the status column

- **SEEN IN TEXT**: the number was read in the page text of the paper (arXiv HTML rendering at ar5iv, or the arXiv
  abstract page for abstract values only where marked). Method caveat: pages were read through a fetch tool that renders
  the page and returns text through a small model asked for verbatim transcription. Long tables came back transcribed
  (the tool itself flagged the Walther et al. tables as reformatted). Treat these as read-but-not-proofread; the lead
  should spot-check a few rows against the arXiv PDF.
- **PROVISIONAL**: from a search snippet, an abstract-level statement, or memory. Never upgraded.
- Journal references from memory or from search snippets are PROVISIONAL even where the number is SEEN.
- "1 sigma" below means the paper's 16th to 84th percentile or its quoted 68 % interval. Where the confidence level was
  not stated in the text read, that is said.

## 1. Pressure smoothing scale lambda_P (comoving kpc)

| paper | z | value | interval (level) | where | definition | status |
|---|---|---|---|---|---|---|
| Rorai et al. 2017, Science 356, 418 (ref PROVISIONAL), arXiv:1704.08366 | 2.0 | 82.1 | 59.9 to 105.6 with systematics; 65.2 to 101.1 statistical (16th to 84th pct) | Table S2 | Gaussian sigma on the smoothed dark-matter density, W(k) = exp(-k^2 lambda^2/2); comoving: "All columns except the first are in comoving kpc units." | SEEN IN TEXT |
| Rorai 2017 | 2.4 | 72.5 | 54.0 to 96.9 syst; 55.6 to 95.8 stat | Table S2 | as above | SEEN IN TEXT |
| Rorai 2017 | 3.0 | 113.8 | **91.4 to 138.6** syst; 92.4 to 137.7 stat | Table S2, columns lambda_P,16syst and lambda_P,84syst | as above | SEEN IN TEXT |
| Rorai 2017 | 3.6 | 90.2 | 60.0 to 123.7 syst; 60.1 to 123.6 stat | Table S2 | as above | SEEN IN TEXT |
| Walther et al. 2019, ApJ (ref PROVISIONAL), arXiv:1808.04367; flat prior on mean flux | 2.0, 2.2, 2.4 | 93.0, 91.0, 87.2 | +8.3/-17.4, +6.3/-6.4, +5.4/-5.1 (16-84 % per Fig. 7 caption; table level not stated) | Table 3 | flux-power fit as Kulkarni 2015; units given as "kpc" with no comoving/proper word in the text | SEEN IN TEXT |
| Walther 2019 flat | 2.8, 3.0, 3.2 | 93.8, 80.6, 84.9 | +4.2/-4.2, +6.0/-5.6, +4.7/-6.3 | Table 3 | as above | SEEN IN TEXT |
| Walther 2019 flat | 4.2, 4.6 | 77.0, 73.7 | +3.6/-6.0, +4.9/-5.8 | Table 3 (no z 4.4 row) | as above | SEEN IN TEXT |
| Walther 2019, Gaussian prior on mean flux | 2.0, 2.2, 2.4 | 75.5, 79.4, 81.1 | +9.8/-6.4, +5.1/-5.0, +4.6/-4.7 | Table 4 | as above | SEEN IN TEXT |
| Walther 2019 Gaussian | 2.8, 3.0, 3.2 | 91.3, 81.7, 83.4 | +4.5/-5.3, +5.8/-5.9, +5.6/-5.3 | Table 4 | as above | SEEN IN TEXT |
| Walther 2019 Gaussian | 4.2, 4.6 | 77.5, 76.2 | +3.3/-5.4, +4.2/-5.4 | Table 4 | as above | SEEN IN TEXT |
| Kulkarni et al. 2015, ApJ 812, 30 (ref from search snippet: PROVISIONAL), arXiv:1504.00366 | 3.0 | 79.0 | none (SIMULATION, fiducial model, T0 = 9.5e3 K) | abstract and body | lambda_ps = 1/k_ps from Delta_F^2(k) = A k^n exp(-k^2/k_ps^2) on the real-space flux: "we find λF=79 kpc (comoving) at z=3 for our fiducial thermal model." | SEEN IN TEXT; simulation, does not count |
| Kulkarni 2015 | 3.0 | 191.5 | none (SIMULATION, T0 = 8.6e4 K) | body | as above | SEEN IN TEXT; simulation |
| Rorai 2017 | 3.0 | 79.1 (standard), 66.5 (late heating), 106.5 (extra heating) | none (SIMULATION, NYX) | Table S3, column lambda_P,sim | flux-power fit, Eq. S33 | SEEN IN TEXT; simulation |

Notes:
- Walther et al. warn: "the uncertainties in λP might still be somewhat underestimated", and their emulator prior ties
  lambda_P to T0. Their lambda_P is a measurement but a prior-informed one.
- At z = 3.0 Rorai 2017 (91.4 to 138.6) and Walther 2019 (about 75 to 88) do not overlap at 1 sigma. Both are given.
- No lambda_P measurement was found within 0.3 of z = 4.4 other than Walther 2019 at 4.2 and 4.6.

## 2. Slope gamma of T = T0 Delta^(gamma-1)

| paper | z | gamma | 1 sigma | where | status |
|---|---|---|---|---|---|
| Gaikwad et al. 2021, MNRAS (DOI 10.1093/mnras/stab2017 from snippet), arXiv:2009.00016 | 2.0, 2.2, 2.4 | 1.500, 1.425, 1.325 | 0.096, 0.133, 0.122 ("total uncertainty"; text calls errors 1 sigma) | Table 2, "Measurements of T₀, γ with total uncertainty" | SEEN IN TEXT |
| Gaikwad 2021 | 2.6, 2.8, 3.0, 3.2 | 1.275, 1.250, 1.225, 1.275 | 0.122, 0.109, 0.120, 0.129 | Table 2 | SEEN IN TEXT |
| Gaikwad 2021 | 3.4, 3.6, 3.8 | 1.350, 1.400, 1.525 | 0.108, 0.101, 0.140 | Table 2 | SEEN IN TEXT |
| Hiss et al. 2018, ApJ (ref PROVISIONAL), arXiv:1710.00700 | 2.0, 2.2, 2.4 | 1.47, 1.67, 1.56 | +0.12/-0.10, +0.27/-0.14, +0.12/-0.12 (16-84 %) | Table 4, "Measurements and values adopted" | SEEN IN TEXT |
| Hiss 2018 | 2.6, 2.8, 3.0, 3.2, 3.4 | 1.38, 1.29, 1.12, 1.38, 1.31 | +0.08/-0.10, +0.07/-0.07, +0.12/-0.06, +0.13/-0.13, +0.14/-0.10 | Table 4 | SEEN IN TEXT |
| Walther 2019 flat | 2.0, 2.2, 2.4, 2.6 | 2.15, 2.13, 2.07, 1.93 | +0.09/-0.26, +0.09/-0.13, +0.13/-0.18, +0.15/-0.17 | Table 3 | SEEN IN TEXT |
| Walther 2019 flat | 2.8, 3.0, 3.2, 3.4 | 2.16, 1.47, 1.85, 1.82 | +0.09/-0.13, +0.26/-0.24, +0.21/-0.25, +0.24/-0.27 | Table 3 | SEEN IN TEXT |
| Walther 2019 flat | 3.6, 3.8, 4.2, 4.6 | 1.74, 1.74, 1.73, 1.54 | +0.28/-0.36, +0.29/-0.39, +0.33/-0.40, +0.37/-0.39 | Table 3 | SEEN IN TEXT |
| Walther 2019 Gaussian | 2.0, 2.2, 2.4, 2.6 | 1.88, 1.74, 1.63, 1.67 | +0.20/-0.27, +0.15/-0.21, +0.16/-0.19, +0.13/-0.15 | Table 4 | SEEN IN TEXT |
| Walther 2019 Gaussian | 2.8, 3.0, 3.2, 3.4 | 1.78, 1.60, 1.75, 1.74 | +0.11/-0.12, +0.14/-0.16, +0.11/-0.13, +0.10/-0.11 | Table 4 | SEEN IN TEXT |
| Walther 2019 Gaussian | 3.6, 3.8, 4.2, 4.6 | 1.69, 1.41, 1.85, 1.84 | +0.14/-0.25, +0.20/-0.23, +0.23/-0.33, +0.23/-0.33 | Table 4 | SEEN IN TEXT |
| Boera et al. 2019, ApJ 872, 101 (ref from snippet: PROVISIONAL), arXiv:1809.06980 | 4.2, 4.6, 5.0 | 1.21, 1.29, 1.33 | +0.23/-0.28, +0.19/-0.26, +0.18/-0.27 ("marginalized 68% confidence intervals") | Table 5 | SEEN IN TEXT |
| Bolton et al. 2014, arXiv:1308.4411 | 2.37 | gamma - 1 = 0.54 | 0.11 (level not stated) | abstract | PROVISIONAL (abstract-level) |
| Rorai et al. 2018, MNRAS (DOI 10.1093/mnras/stx2862), arXiv:1711.00930 | 2.55 to 2.95 | 1.45 (cut-off method); 1.37 (median b method) | 0.17; 0.17 | abstract | PROVISIONAL (abstract-level) |

Walther 2019 flat-prior gamma near 2.1 at z 2.0 to 2.8 disagrees with Gaikwad 2021 and Hiss 2018 (1.25 to 1.5).

## 3. Temperature at mean density T0 (K)

| paper | z | T0 | 1 sigma | where | status |
|---|---|---|---|---|---|
| Gaikwad 2021 | 2.0, 2.2, 2.4, 2.6 | 9500, 11000, 12750, 13500 | 1393, 1028, 1132, 1390 | Table 2 | SEEN IN TEXT |
| Gaikwad 2021 | 2.8, 3.0, 3.2, 3.4 | 14750, 14750, 12750, 11250 | 1341, 1322, 1493, 1125 | Table 2; abstract gives the peak as "T0=(14750±1322)K" | SEEN IN TEXT |
| Gaikwad 2021 | 3.6, 3.8 | 10250, 9250 | 1070, 876 | Table 2 | SEEN IN TEXT |
| Hiss 2018 | 2.0, 2.2, 2.4, 2.6 | 13721, 10927, 13334, 16281 | +1694/-2152, +1961/-3843, +1206/-1530, +1940/-1601 | Table 4 | SEEN IN TEXT |
| Hiss 2018 | 2.8, 3.0, 3.2, 3.4 | 20036, 18371, 16244, 13439 | +1416/-1507, +1087/-1388, +1153/-1135, +1542/-2318 | Table 4 | SEEN IN TEXT |
| Walther 2019 flat (units 1e4 K) | 2.0, 2.2, 2.4, 2.6, 2.8 | 0.734, 0.789, 0.831, 1.000, 1.000 | +0.093/-0.071, +0.085/-0.068, +0.11/-0.078, +0.15/-0.090, +0.11/-0.087 | Table 3 | SEEN IN TEXT |
| Walther 2019 flat | 3.0, 3.2, 3.4, 3.6, 3.8 | 1.429, 1.115, 1.330, 1.010, 1.029 | +0.31/-0.27, +0.23/-0.15, +0.30/-0.22, +0.36/-0.30, +0.29/-0.25 | Table 3 | SEEN IN TEXT |
| Walther 2019 flat | 4.2, 4.6 | 0.905, 0.910 | +0.12/-0.082, +0.12/-0.12 | Table 3 | SEEN IN TEXT |
| Walther 2019 Gaussian | 2.0, 2.2, 2.4, 2.6, 2.8 | 0.732, 1.014, 1.165, 1.234, 1.286 | +0.17/-0.091, +0.25/-0.15, +0.29/-0.19, +0.19/-0.14, +0.19/-0.15 | Table 4 | SEEN IN TEXT |
| Walther 2019 Gaussian | 3.0, 3.2, 3.4, 3.6, 3.8 | 1.289, 1.186, 1.404, 1.038, 1.205 | +0.18/-0.14, +0.13/-0.12, +0.17/-0.16, +0.31/-0.27, +0.23/-0.19 | Table 4 | SEEN IN TEXT |
| Walther 2019 Gaussian | 4.2, 4.6 | 0.890, 0.877 | +0.093/-0.073, +0.13/-0.11 | Table 4 | SEEN IN TEXT |
| Boera 2019 (units 1e3 K) | 4.2, 4.6, 5.0 | 8.13, 7.31, 7.37 | +1.34/-0.97, +1.35/-0.88, +1.67/-1.39 (68 %) | Table 5 | SEEN IN TEXT |
| Bolton 2014 | 2.37 | 1.00e4 | +0.32/-0.21 e4 (level not stated) | abstract | PROVISIONAL |
| Rorai 2018 | 2.55 to 2.95 | 15.6e3; 14.6e3 | 4.4e3; 3.7e3 | abstract | PROVISIONAL |

Hiss 2018 (about 18000 to 20000 K at z 2.8 to 3.0) is above Gaikwad 2021 (14750 K) and well above Walther 2019 flat
(10000 K at z 2.8). These disagree; READING.md gives both readings.

Not opened: Becker et al. 2011 (temperature at a characteristic density, not T0 directly).

## 4. Effective optical depth tau_eff

| paper | z | value | 1 sigma | where | status |
|---|---|---|---|---|---|
| Becker et al. 2013, MNRAS (ref PROVISIONAL), arXiv:1208.2584 | fit | tau_eff = tau0 ((1+z)/(1+z0))^beta + C with "[τ0, β, C] = [0.751, 2.90, −0.132], for z0 = 3.5" | covariance only (Table 3); the fetch tool's square roots, about 0.022, 0.116, 0.022, are not the paper's text | Eq. 5 | SEEN IN TEXT (fit values); errors PROVISIONAL |
| Becker 2013 | 2.15, 2.25 | F = 0.8806, 0.8590 (tau 0.127, 0.152) | 0.0103, 0.0098 in F; "The errors are 1σ" | Table 2, column F(z) | SEEN IN TEXT |
| Becker 2013 | 2.95, 3.05 | F = 0.6966, 0.6670 (tau 0.362, 0.405) | 0.0084, 0.0082 | Table 2 | SEEN IN TEXT |
| Becker 2013 | 3.35, 3.45, 3.75, 3.85 | F = 0.5762, 0.5548, 0.4723, 0.4470 | 0.0074, 0.0071, 0.0068, 0.0072 | Table 2 | SEEN IN TEXT |
| Becker 2013 | 4.35, 4.45 | F = 0.3441, 0.3216 (tau 1.067, 1.134) | 0.0102, 0.0094 | Table 2 | SEEN IN TEXT |
| Gaikwad 2021 | 2.0, 2.2, 2.4 | mean F = 0.8690, 0.8261, 0.7919 | 0.0214, 0.0206, 0.0210 (level not stated) | Table 1 | SEEN IN TEXT |
| Gaikwad 2021 | 2.8, 3.0, 3.2 | 0.7398, 0.7105, 0.6731 | 0.0212, 0.0213, 0.0223 | Table 1 | SEEN IN TEXT |
| Walther 2019 flat (fitted mean flux) | 2.0, 2.2, 2.4, 2.8, 3.0, 3.2, 4.2, 4.6 | 0.831, 0.796, 0.772, 0.688, 0.694, 0.623, 0.355, 0.278 | asymmetric, Table 3 | Table 3 | SEEN IN TEXT |
| Walther 2019 Gaussian (prior from earlier mean-flux data) | 2.0, 2.2, 2.4, 2.8, 3.0, 3.2, 4.2, 4.6 | 0.865, 0.825, 0.799, 0.719, 0.687, 0.631, 0.346, 0.254 | asymmetric, Table 4 | Table 4 | SEEN IN TEXT |
| Boera 2019 | 4.2, 4.6 | tau_eff = 1.02, 1.41 | 0.04, +0.08/-0.09 (68 %) | Table 5 | SEEN IN TEXT |
| Kamble et al. 2020, ApJ 892, 70 (ref from snippet), arXiv:1904.01110 | power law | tau0 = 5.54e-3 +- 0.64e-3, gamma = 3.182 +- 0.074 for tau = tau0 (1+z)^gamma | parameter errors only | abstract | PROVISIONAL |
| Turner et al. 2024 (DESI Y1, LyCAN; "accepted to ApJ"), arXiv:2405.06743 | power law, 2.1 <= z <= 4.2 | tau0 = 2.46e-3 +- 0.14e-3, gamma = 3.62 +- 0.04 | parameter errors only | abstract | PROVISIONAL |

Notes:
- The record's formula is Becker et al. 2013 Eq. 5 exactly, with the offset C = -0.132 included and z0 = 3.5.
- Becker et al. state C was set by scaling to Faucher-Giguere et al. 2008 over 2.2 to 2.5, that the fit shows "a mean
  fractional deviation in the flux of two per cent" from the binned points, and that it should not be extrapolated.
- Not resolved: the Becker 2013 Table 2 F(z) values read here sit 4 to 6 % below the Eq. 5 fit in tau at every z checked
  (2.15 to 4.45). This may be real (within their stated 2 % flux deviation at high z) or a reading error; it was not
  resolved.
- Faucher-Giguere et al. 2008 was not opened.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
