# DSC1R reconcile: why DSC1 and DSC1R read the same discs differently

Written after DSC1R's blind work and its A1 amendment were committed (A1 run 75e3203c75, RESULT A1 section c1d4da0525).
Blindness ended here: DSC1's criteria, script, outputs and RESULT were then opened. This file grades nothing and
relabels neither lane. Script `dsc1r_reconcile.py`, outputs `dsc1r_reconcile.json / .out`.

## Headline

1. **Above the switch, the error and correlation treatment (d) carries the difference.** DSC1 counts every digitised
   point as independent. It uses s^2 over N - 1 and a 4 s^2 interval. DSC1R divides each disc's chi^2 by
   N / N_eff, with one beam per 0.6" per side, so c is 1.85 to 5.1 per disc. It uses s^2 over sum N_eff - 1 and a
   3.84 s^2 interval. From DSC1R's A1 build, swapping in (d) alone narrows the canonical interval from
   [-0.130, 1.580] to [0.195, 1.105]: A = 0 leaves it while A = 1 stays inside. Every other single swap leaves A = 0
   inside. The point cut (e) and the bulge convention (b1) then shift A_best by about +0.1 and the chi^2 values. With
   (b) + (d) + (e) together, DSC1's 0.670 [0.250, 1.175] is reproduced exactly.
2. **Below the switch, no ingredient changes which layout wins.** A free reference halo at A about 1.25 to 1.57 beats
   the law in every row of the table, in both builds. The difference between "LAW FAILS BELOW" and "LAW HOLDS BELOW"
   is the decision line, not the data:
   - DSC1 compares chi^2_L - chi^2_min against 4 s^2 on uncorrected chi^2. That is 94.6 against 21.3 canonical.
   - DSC1R compares the same quantity against 9 s^2 on correlation-corrected chi^2, and also requires p < 0.0027.
     That is 45.1 against 102.3.
   - The ingredient that moves the margin most is again (d): it alone takes the canonical margin from 45 to 78.
   - The zC-488879 gas mass (b2: alpha_CO 4.3 against 1.31) lowers the law's chi^2 by 77, but it lowers the halo's
     too. The margin moves only from 45 to 30.

The halo construction (c), the pressure term (a), the Lelli kpc/" (f2), the law kernel (f3) and the A grid's floor
(f1) change nothing material. The A1 halo equals the record's to 4e-5. The all-swapped run reproduces every number
DSC1 reports, on both footings: A, the interval, chi^2 at A = 0 / 1 / law, and the below group's chi^2 and best A.

## Swap table (from DSC1R's A1 build; one ingredient at a time, then combined)

Above: A_best [95 %], chi^2 at A = 0 / A = 1 / law. Below: chi^2 law (L), baryons alone (N), free halo (H, best A),
halo at A = 1 (H1). chi^2 values are on each row's own error and correlation convention, so compare them within a row.

| swap | above canonical | above alt | below canonical L / N / H (A) / H1 | below alt L / N / H (A) / H1 |
|---|---|---|---|---|
| A1 base (DSC1R) | 0.590 [-0.130, 1.580]; 90.8 / 76.5 / 68.8 | 0.120 [-0.585, 1.160]; 41.5 / 63.1 / 51.4 | 252.9 / 609.7 / 207.8 (1.40) / 226.1 | 253.4 / 659.0 / 218.7 (1.40) / 239.5 |
| (a) pressure term (DSC1's drift radius for zC-488879) | unchanged | unchanged | unchanged | unchanged |
| (b) baryons (both b1 and b2) | 0.730 [-0.040, 1.775]; 106.5 / 77.5 / 74.7 | 0.185 [-0.515, 1.190]; 39.2 / 56.6 / 46.0 | 155.7 / 476.5 / 120.3 (1.31) / 131.4 | 168.9 / 543.9 / 136.7 (1.35) / 152.3 |
| (b1) Genzel bulge = B/T x M* (CFG401) | as (b) | as (b) | 233.0 / 604.2 / 180.7 (1.45) / 203.9 | 241.2 / 671.5 / 196.2 (1.47) / 224.8 |
| (b2) zC-488879: alpha_CO 4.3, R_bul 0.35" | unchanged | unchanged | 175.6 / 482.1 / 145.9 (1.25) / 153.6 | 181.1 / 531.4 / 157.2 (1.27) / 167.0 |
| (c) halo (SRJ2's code path) | unchanged | unchanged | unchanged | unchanged |
| **(d) errors: c = 1, s^2 over N - 1, 4 s^2** | **0.610 [0.195, 1.105]**; 411.1 / 347.4 / 319.9 | **-0.025 [-0.440, 0.500]**; 179.2 / 284.2 / 237.0 | 534.7 / 1245.2 / 456.4 (1.33) / 483.8 | 585.9 / 1477.1 / 508.2 (1.35) / 547.1 |
| (e) cut at 0.6" (not 0.3") | 0.570 [-0.045, 1.385]; 57.3 / 45.2 / 37.5 | 0.190 [-0.400, 0.995]; 20.4 / 36.4 / 26.5 | 213.1 / 597.2 / 147.9 (1.57) / 181.4 | 202.6 / 634.2 / 157.3 (1.53) / 190.2 |
| (f1) A grid 0 to 6 | 0.590 [0.000, 1.580] | 0.120 [0.000, 1.160] | unchanged | unchanged |
| (f2) Lelli kpc/" 8.69 | unchanged | unchanged | 253.0 / 609.9 / 207.8 / 226.1 | 253.4 / 659.1 / 218.7 / 239.6 |
| (f3) the record's glaw kernel | unchanged | unchanged | unchanged | unchanged |
| (b) + (e) | 0.590 [-0.090, 1.520] | 0.170 [-0.490, 1.110] | 137.7 / 472.8 / 90.3 (1.43) / 109.9 | 134.4 / 515.1 / 100.2 (1.42) / 120.7 |
| (b) + (d) | 0.755 [0.305, 1.285] | 0.025 [-0.395, 0.535] | 334.8 / 993.9 / 261.3 (1.28) / 281.8 | 435.4 / 1311.0 / 338.6 (1.36) / 380.0 |
| (d) + (e) | 0.645 [0.265, 1.090] | 0.150 [-0.220, 0.595] | 428.7 / 1182.9 / 303.7 (1.54) / 365.9 | 431.2 / 1329.7 / 340.2 (1.48) / 400.9 |
| (b) + (d) + (e) | 0.670 [0.250, 1.175]; 241.2 / 169.5 / 156.2 | 0.120 [-0.295, 0.640]; 72.9 / 126.7 / 98.3 | 281.3 / 943.0 / 186.7 (1.42) / 224.3 | 303.2 / 1111.3 / 225.9 (1.39) / 267.1 |
| **all swapped** | **0.670 [0.250, 1.175]**; 241.2 / 169.5 / 156.2 | **0.120 [0.000, 0.640]**; 72.9 / 126.7 / 98.3 | **281.2 / 942.9 / 186.6 (1.415) / 224.1** | **303.1 / 1111.2 / 225.8 (1.390) / 266.9** |
| DSC1 RESULT | 0.670 [0.250, 1.175]; 241.2 / 169.5 / 156.2 | 0.120 [0.000, 0.640]; 72.9 / 126.7 / 98.3 | 281.2 / 942.9 / - (1.415) / 224.1 | 303.1 / 1111.2 / - (1.390) / 266.9 |
| reported: (g) c = 2 per point | 0.610 [0.040, 1.335] | -0.025 [-0.590, 0.750] | 267.4 / 622.6 / 228.2 (1.33) / 241.9 | 293.0 / 738.6 / 254.1 (1.35) / 273.5 |
| reported: (b) + (e) + (g) | 0.670 [0.095, 1.415] | 0.120 [-0.455, 0.905] | 140.7 / 471.5 / 93.3 (1.42) / 112.1 | 151.6 / 555.7 / 113.0 (1.39) / 133.5 |

"Unchanged" means equal to the A1 base row to the printed digit. The membership is the same in every row: canonical
above zC 406690, zC 400569, D3a 15504; alt above zC 400569, D3a 15504.

On alt, (d) moves A = 1 outside the interval ([-0.44, 0.50]). DSC1 read alt ABOVE as NO POWER only because its own rule
needs three discs.

## Which treatment is closer to the source papers

Checked on disk:
- Genzel+2017, the PDF outside the repo (`<repo-parent>/_external_data/arxiv_pdf/1703.04310.pdf`, read with pdftotext): Table 1,
  the Fig. 1 caption and the methods.
- Lelli+2023, the TeX source (`<repo-parent>/_external_data/arxiv_src/2302.00030/ColdGasDiskCosmicNoon.tex`).

- **(a) Pressure term.** Both lanes use Table 1's footnote formula, v_c^2 = v_rot^2 + 3.36 sigma0^2 (R / R_1/2).
  That is exact to the paper. For zC-488879, Lelli+23 states that no pressure correction is needed (V/sigma of 17 or
  more); both lanes apply a negligible 15 km/s term. It makes no difference.
- **(b1) Bulge mass.** Table 1 labels B/T "Mbulge/Mbaryon". The methods say it gives "the mass in the bulge relative
  to the total (disk+bulge) baryonic mass", the rest being in the disc.
  - DSC1R applies it to M_b. That is closer to the paper's definition, but DSC1R caps the bulge at M*, which binds
    for zC 406690 (B/T 0.6, M* 0.42, M_b 1.4).
  - DSC1, following CFG401's record construction, applies it to the stars only.
  - Neither is exact: B/T is a fit parameter tied to the fitted M_baryon (1.7 for zC 406690, not the prior 1.4).
- **(b) Mass priors.** Table 1 gives linear 1-sigma prior errors (M_b 0.9 ± 0.5, 2.3 ± 1.1, 0.75 ± 0.37, 1.4 ± 0.7,
  2.5 ± 1.2, 2.0 ± 1.0 x 1e11). DSC1's M_b brackets use exactly these. DSC1R's ±0.2 dex is an approximation: the
  paper's errors are -0.28 to -0.35 dex and +0.17 to +0.19 dex.
- **(b2) zC-488879 gas.**
  - Lelli+23 brackets M_gas between alpha_CO 0.4 and 4.3 and centres its prior at log Upsilon_gas = 0.5 ± 0.5.
  - Its dynamical fit returns alpha_CO = 2.9 (+0.7 / -0.9), "consistent with the Milky-Way" value.
  - DSC1's 4.3 is closer to the paper's own reading than DSC1R's 1.31, the log-midpoint of the bracket. The 2.9 is
    itself a fit to the same kinematics.
- **(c) Halo.** The two lanes now match (A1); the brief's 5.41 M_b was the lead's error.
- **(d) Errors and correlation.** Genzel+17's methods say the position-velocity cuts use slits of "about 1.1 and 0.5
  resolution elements". So the points are roughly Nyquist sampled, about two per beam along the line of nodes. The fit
  errors were already multiplied by 1.5. The Fig. 1 caption gives FWHM ~0.25" for the top four panels and 0.55-0.67"
  for the bottom two.
  - DSC1 (c = 1) treats Nyquist-sampled points as independent and so overstates the information about 2x.
  - DSC1R (one beam per 0.6" for every disc, c 1.85-5.1) overstates the correlation for the adaptive-optics discs.
  - The paper's statement points to c ≈ 2. The reported row (g) gives [0.040, 1.335] canonical from DSC1R's
    ingredients, and [0.095, 1.415] with DSC1's baryons and cut. A = 0 sits just outside on canonical in both, and
    inside on alt.
  - I could not map the caption's panel order to the six galaxies from the text dump, so per-disc beams were not set.
- **(e) Cut.** Genzel+17 fits beam-convolved models and applies no cut, so neither 0.3" nor 0.6" is the paper's. For
  the four adaptive-optics discs, the 0.6" cut removes resolved points.
- **Inclination brackets (DSC1R only).** Table 1 gives ±5° for COS4 01351, D3a 6397, GS4 43501 and D3a 15504, ±12°
  for zC 406690 and ±10° for zC 400569. DSC1R's uniform ±10° overstated the I- and I+ brackets for four discs. DSC1
  ran no inclination bracket.
- **Alternative curve for zC 400569.** Lelli+23 attributes the mild outer decline in Genzel's H-alpha curve to
  H-alpha-bright companions affecting the position angle, and finds the CO curves flat. Both lanes' brackets with
  that curve leave their readings unchanged.
- **Could not check:** each digitised point against the paper's own plotted errors (CFG400's digitisation was taken
  as given); the per-galaxy beam; any covariance between points.

## What can and cannot be said

The two lanes see the same thing in these curves. They disagree only in how much to believe it. For the three
canonical discs above the switch, the record's halo is preferred at about 0.6 to 0.7 of its size by both builds. Whether
"none at all" is excluded depends on how many of Genzel's digitised points count as independent:
- counting them all excludes zero;
- counting one per 0.6" beam does not;
- the paper's own Nyquist sampling sits on the edge.
The drift-support and baryon-mass assumptions move that best value from about zero (or below) to about 1.4.

Below the switch, every build prefers a modest halo (about 1.3 to 1.6 record halos) to the law. Whether that is called
a failure of the law depends on the line, 4 s^2 or 9 s^2, and on the correlation correction. No layout fits the curves
to their stated errors, and zC-488879's photometric baryons drive much of the misfit. So these seven discs cannot decide
the crossing-speed joint on either side. The above-switch reading rests on three discs and two degenerate nuisances,
and the below-switch reading rests on a threshold choice. Resolving it needs the paper-level inputs these lanes lacked:
- beam-forward modelling with the real per-disc PSF and covariance;
- measured gas profiles, with alpha_CO fixed independently;
- curves beyond about 3 R_1/2.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
