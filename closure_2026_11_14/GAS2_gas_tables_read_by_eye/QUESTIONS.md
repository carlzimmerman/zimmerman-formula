# GAS2: the four open questions, answered from the pages

Date: 2026-11-14. Not blind, not graded; relabels nothing; computes no forest number. Page numbers are PDF pages (they
equal the printed page numbers in all four papers used here).

## Verdict first

1. **Kulkarni et al. 2015: the factor is sqrt 2, not 2 sqrt 2, and it maps the flux-fitted scale onto the record's
   convention with factor 1.** GAS1's Reading 2 (factor 1/2) came from the misread factor and is void.
2. **Walther et al. 2019: comoving.** lambda_P is Kulkarni's flux-power cut-off; the paper defines it in words, with no
   numbered equation of its own.
3. **Becker et al. 2013: there is a gap between the binned points and the fit, but it is scatter of both signs, not a
   steady 4 to 6 per cent offset.** The paper says why the two differ.
4. **Rorai et al. 2017: Table S2 has four bins, all as GAS1 gave them.** lambda_P is the width of a Gaussian-like
   smoothing of the dark-matter density, but the kernel is a cubic spline, so the Gaussian is an approximation, not the
   definition.

## 1. Kulkarni et al. 2015: what Figure 14 divides, and by what

- Page 12, Eq. 16: the power spectrum of the real-space flux F_real is fitted as Delta_F^2(k) = A k^n exp(-k^2 / k_ps^2).
  Page 13: lambda_ps = 1/k_ps. That is the paper's own definition of the pressure smoothing scale (Eq. 16). It is a
  cut-off in a power spectrum of the flux field, so the field itself is cut by exp(-k^2 lambda_ps^2 / 2).
- Page 4, Eq. 9: the linear filtering scale lambda_F is defined on density contrasts, delta_b / delta_m =
  exp(-k^2 lambda_F^2), so the baryon power is cut by exp(-2 k^2 lambda_F^2).
- Page 14, Figure 14: what is plotted is **lambda_ps / sqrt 2** (legend), beside the Jeans scale and lambda_F. The
  caption says the flux-power scale is divided by **sqrt 2** for consistency, because the other two scales are
  defined on density contrasts. The text layer prints this as "λps / 2" because it loses the radical; the rendered page
  shows sqrt 2.
- What it implies: the record smooths the density field by exp(-k^2 lambda^2 / 2), so its power is cut by
  exp(-k^2 lambda^2). In Eq. 9's convention that is lambda = sqrt 2 lambda_F. Kulkarni's sqrt 2 puts lambda_ps on the
  lambda_F footing; going back to the record's footing multiplies by sqrt 2 again. So a flux-fitted lambda_ps and the
  record's lambda have the same functional form, and the conversion factor is 1. The record's 79 comoving kpc is
  Kulkarni's lambda_ps itself (page 13, a simulation value) taken at factor 1.
- This agrees with Rorai et al. 2017, page 38, where the density-kernel lambda_P and the flux-fit lambda_P,sim (Eq.
  S33, page 37, the same form as Kulkarni's Eq. 16) lie almost one to one. GAS1's Reading 1 and Reading 2 therefore no
  longer differ; only Reading 1 is shown in PLACEMENTS.md.
- What this does not settle: whether the cut-off of a nonlinear flux field measures the same physical width as a cut on
  the density. That is what Rorai's calibration addresses (scatter under 5 per cent, 13 runs, z = 3 only), not a
  definition.

## 2. Walther et al. 2019: comoving or proper, and the definition

- Comoving. Page 14, Figure 7 (the flat-prior results of Table 3) labels the axis lambda_P [ckpc]. The table headers on
  pages 31 and 32 say only [kpc]; the text layer also shows "[com. kpc]" axis labels on other figures (pages 7, 9, 12),
  which I did not open. The values in Fig. 7 match Table 3 (for example about 90 at z 2.2, 80 at z 3.0).
- Definition: page 5, in words, no numbered equation: the cut-off in the power spectrum of the real-space flux F_real,
  fitted as described in Kulkarni et al. 2015. So it is Kulkarni's Eq. 16, and question 1's factor 1 applies.
- Also on the page: Tables 3 and 4 give purely statistical errors (median and 16 % to 84 %, Fig. 7 caption), with
  systematics expected at about 0.5 to 1 sigma_stat more; page 20 adds that the lambda_P errors may be somewhat
  underestimated.

## 3. Becker et al. 2013: the table against Eq. 5

- Read from page 10: Eq. 5, tau_eff = tau0 ((1+z)/(1+z0))^beta + C, with [0.751, 2.90, -0.132] and z0 = 3.5; Table 2,
  28 bins of F(z) from 2.15 to 4.85, all read.
- The gap (`gas2_place.out`): (tau_table - tau_fit) / tau_fit runs from -5.8 % (z 2.15, 4.65) to +5.4 % (z 2.45). The
  bins GAS1 checked happened to include several low ones (2.15, 2.25, 2.95, 3.05, 4.35, 4.45 at -3.6 to -5.8 %), but
  3.35, 3.45, 3.75, 3.85, which GAS1 also listed, sit at +0.5, -1.0, +0.5, +0.5 %. In flux the gaps are -2.7 % to
  +8.0 %, mostly under 2 %. So the gap is real but it is scatter about the fit, not an offset.
- The paper's explanation, page 10: tau0 and beta were fitted directly to the composite flux ratios corrected for
  optically thick absorbers, not to the binned F(z), and C was then set separately by scaling to Faucher-Giguere et al.
  2008 over 2.2 to 2.5. The fit to the discrete points has formal chi^2 64 for 28 bins; the authors say some residual
  structure may be real, the power-law form may be inadequate, or the discrete errors somewhat underestimated, and give
  the mean fractional flux deviation as two per cent. No correction is applied to one and not the other beyond that
  separate scaling.

## 4. Rorai et al. 2017: Table S2 and the definition

- Table S2, page 43, comoving kpc: z 2.0: median 82.1, 16-84 % 65.2 to 101.1, with systematics 59.9 to 105.6; z 2.4:
  72.5, 55.6 to 95.8, 54.0 to 96.9; z 3.0: 113.8, 92.4 to 137.7, 91.4 to 138.6; z 3.6: 90.2, 60.1 to 123.6, 60.0 to
  123.7. There are only these four bins. All match GAS1.
- Definition, page 23: the baryon density is the dark-matter density convolved with a window W_IGM (Eq. S21,
  delta_IGM(k) = W_IGM(k, lambda_P) delta_DM(k)). The page gives the Gaussian of width sigma = lambda_P, W = exp(-k^2
  lambda_P^2 / 2), as an example. The kernel actually used is a cubic spline with support R_P (Eqs. S22, S23); its centre
  closely resembles a Gaussian with sigma about R_P / 3.25, and lambda_P is defined as R_P / 3.25.
- So the record's kernel exp(-k^2 lambda^2 / 2) on the density matches Rorai's lambda_P at factor 1 to the accuracy of
  the spline-to-Gaussian match; GAS1's "exactly" is too strong. The spline has compact support, so its outer Fourier
  tail is not the Gaussian's; how much that matters for the forest is not checked here.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
