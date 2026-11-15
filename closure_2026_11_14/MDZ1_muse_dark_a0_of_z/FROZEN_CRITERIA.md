# MDZ1 FROZEN CRITERIA: the law's a0(z) against MUSE-DARK's measured a0(z)

Committed alone, before any MDZ1 script or computed number. TEST lane: adopts nothing, relabels nothing, never edits
the scorecard or other lanes' files. Footings canonical a0 = 9.3603e-11 m/s^2 and alt a0 = 1.1312e-10 m/s^2, graded side
by side, never pooled. Cold dark energy is a gravitating field component; no particle is added. All units SI.

## Question
The law: a0(z) = (c/2) sqrt(G rho_DE(z)), so a0(z)/a0(0) = f(z) = sqrt(rho_DE(z)/rho_DE(0)). MUSE-DARK III
(Ciocan et al., arXiv:2604.22613v1) fit the RAR of 79 star-forming galaxies at 0.33 < z < 1.44 with McGaugh's function
a_tot = a_bar / (1 - exp(-sqrt(a_bar/a0))) and report a0 rising with z: global a0(z) = a0(0) + a1 z with
a0(0) = 1.00e-10, a1 = 1.59e-10 (95 % CI +-0.04 / +-0.10), and four quantile z bins rising from 1.99e-10 to 2.71e-10.
Escala (arXiv:2608.10073) reads BTFR zero-point offsets at z 0.9, 2.3 (Ubler 2017) and 5 (Gomez-Espinoza 2026,
submitted) as a0(z). Does the law's a0(z) agree with these?

## Inputs (data only; downloads in `_external_data/mdz1_muse_dark/`, untracked; sha256)
- html_2604.22613.html 8747fb8931ed80b4f1c00df66c4093c914c1653266471cfcf88cb14bcd21ab48
- abs_2604.22613.html 78a3bfabc68bdb21d3e22e2ae7ca61183ecd73652a744aa36f63f5844f9c1111
- src_2604.22613.tar (arXiv source) ac6e7528b0d6262a7cf2a016e142aa11b0c237a29e57333b0b41190d7c51c15f
  - sliding_widnow_newsample_fin.png (Fig. 3) a9bd442936c7ca9d2697f1b4983381eb30f930c5989aa6b6168399035017157b
  - Mstarbias_z.png (Fig. 6) 86098d4b6418ee6dbe0d2560e0e91001a6c159ccfb04d6161418a6ebb210e6dd
  - paper_v4.tex 340b600c054f68f4ca7d06d7d9b451d2ec1ca54eaabc4b6106b2b4cca8841e0b
- html_2608.10073.html 6ec513b5bf1f4efd586184447e8a0becadb5a781b365c56407f5284bfa221ac1
- src_2608.10073.tar b21471fc332e5dd22996193111dd86c3f59c4a3d6793f89728d286dca7e47210; Fig2N.png
  a867fa58d2b9422535ff62f792acca1483855fb437bcc1262cb79814c9269988
- tacconi2020_2003.06245.pdf (Tacconi, Genzel, Sternberg 2020 ARA&A) 2773b05b39d5182b114e5612a8e80eaca3741a5dee50aa41ed37d51925bcf88e
- abs_1703.04321.html (Ubler 2017 abstract) da31a3715c642e14e9a8a37617b6aa358e9cc61ba818b30885b9519631113416
- Transcription: `mdz1_inputs.csv` (every number used, with location and method; text vs pixel read)
  sha256 3e6f0bb072985e0eecd81105f12730d5ff25e4719dc256700aa20c668ca26a3a. The script refuses to run on another hash.

Per-galaxy data: the paper points to https://dark.univ-lyon1.fr/data-releases/, which links the MUSE UDF sample at
dark-matter.osu-lyon.fr. That host resolves but timed out (60 s, https and http) from this machine; A&A returns 403;
a web search found no Zenodo / VizieR / GitHub deposit. So no refit at fixed a0(z) with the law's interpolating
function is possible here; the lane grades the published a0(z) values. Middle-bin values and all bin errors are pixel
reads of Fig. 3 (y axis anchored on the two text values 1.99 and 2.71); Fig. 6's fiducial points are read
independently and serve as a transcription check (KA3).

Values transcribed (1e-10 m/s^2): bins z = 0.502 / 0.824 / 1.046 / 1.274, a0 = 1.99 / 2.200 / 2.572 / 2.71,
half error bars 0.086 / 0.105 / 0.112 / 0.136 (CI level not stated in the caption). Fig. 6 (+0.2 dex disk mass)
1.245 / 1.409 / 1.731 / 1.952; (+0.45 dex) 0.567 / 0.663 / 0.904 / 1.130. Escala Fig. 2: Delta ZP = -0.439 +- 0.071
(z 0.899), -0.269 +- 0.071 (z 2.298), -0.539 +- 0.191 (z 4.999).

## Law, cases and conversion
- f(z), (i) rho_DE constant: f = 1. (ii) the record's evolving convention (FRZ2's D cases, frz2_hm.py line 89):
  f = sqrt(F), F = (1+z)^(3(1+w0+wa)) exp(-3 wa z/(1+z)), (w0, wa) = Pan (-0.838, -0.62), DES5 (-0.752, -0.86),
  Uni (-0.667, -1.09). Graded cases: L (Lambda), D-Pan, D-DES5, D-Uni.
- Reported, not graded: FRZ2's Q cases (f = sqrt(w(z) F / w0)); a0 proportional to H(z) with Om 0.315 (not the law; the
  rival the paper names).
- Interpolating function. The record's law is the simple one, mu(x) = x/(1+x), g = (g_bar + sqrt(g_bar^2 + 4 a0 g_bar))/2
  (DD1 KA4, as used in FINAL2). MUSE-DARK's a0 is McGaugh's. Conversion C_IF = a0_McGaugh / a0_simple, obtained by a
  least-squares fit in log g of McGaugh's function to the simple law on a uniform grid of log10 g_bar over a window W.
  Base window W0 = [-11.5, -10.0] (the sample "predominantly probes the low-acceleration regime"; r < 2 kpc removed).
  Law in MUSE-DARK's convention: a0_R,law(z) = C_IF(W, a0_footing) x a0_footing x f(z).

## Rows and statistics (sigma in ln a0 per bin: s_i = err_i / a0_i, plus 0.005e-10 / a0_i transcription for bins 2-3)
- Row S (shape, amplitude free; primary): weighted linear fit of y_i = ln a0_i(corrected) - ln[C_IF,i f(z_i)] against z_i;
  P_S = |slope| / sigma_slope. The law predicts slope 0. Footings enter only through C_IF.
- Row L (level, amplitude fixed by the footing; primary): chi^2 of ln a0_i(corrected) against ln a0_R,law(z_i), 4 dof,
  converted to a two-sided Gaussian sigma P_L.
- Row G (the paper's global fit, as published; supporting): a1_law = C_IF(W0) a0_footing x (least-squares slope of f(z)
  on a uniform z grid over [0.33, 1.44]); P_G = |a1 - a1_law| / sigma_a1, sigma_a1 = 0.10e-10/1.96. The law's intercept
  against a0(0) = 1.00e-10 (sigma 0.04e-10/1.96) reported. Same for Eq. 9 (best profile per galaxy) and Eq. 14 (MOND
  fits) reported; the per-galaxy MOND regression a1 = 1.42 (+0.94 / -0.89) reported (CI level unstated, taken as 1 sigma).
- Row E (Escala BTFR; secondary): the law's offset Delta ZP_law = -log10 f(z) (deep-MOND BTFR M = V^4/(G a0)); the
  data's a0-attributable offset k x Delta ZP_obs; chi^2 3 dof -> sigma P_E. D cases at z 5 extrapolate the CPL fits far
  past the SN / BAO data (flagged).

## Red-team brackets (frozen; applied as corrections to the measured bin a0 or to the law's conversion)
- B1 molecular gas omitted from a_bar (the paper's baryons are stellar disk + constant-Sigma HI (+ bulge); App. C names
  H2 at 30-50 % at z ~ 1, ~0.2 dex). Edges: none (H2 fully inside the fitted gas) / fully omitted with Tacconi 2020's
  main-sequence mu_mol = t_depl sSFR, t_depl = 1.6 (1+z)^-1 Gyr, sSFR from Eq. 1 (S14 main sequence), at
  log M* = 9.0, 9.5, 10.0 (the sample spans 8.8-11). Mass offset per bin Delta_i = log10(10^B2 + mu_i).
- B2 uniform stellar M/L or IMF offset: 0, +0.2, +0.45 dex (the paper's own Fig. 6 values, read directly; the authors
  argue against them).
- Mass-offset response: Delta log10 a0 per bin interpolated linearly in Delta through (0, 0), (0.2, Fig. 6 blue),
  (0.45, Fig. 6 green), extrapolated with the last segment above 0.45 (largest Delta used is printed).
- B3 beam smearing / inner cut: the paper says removing r < 2 kpc changes a0 by < 10 %. Edges: a linear-in-z ramp from
  0 at bin 1 to -10 % at bin 4, none, and +10 %.
- B4 interpolating function: window W in {[-12.0, -10.5], [-11.5, -10.0], [-11.0, -9.5]} for the level, and a drift of
  the window of -0.5, 0, +0.5 dex from bin 1 to bin 4 (linear in z: higher-z bins at lower or higher g_bar).
- B5 error-bar reading: E1 = the half bars as 1 sigma (primary, conservative), E2 = as 95 % (sigma = half bar / 1.96).
- Not bracketed numerically (no sourced size): asymmetric-drift / pressure-support over- or under-correction with z,
  stellar M/L evolution beyond B2 (e.g. outshining), HI evolution, selection drift in M* inside bins. For these the
  script prints the differential correction (dex in a0 between bin 1 and bin 4) needed to bring P_S to 2 and to 0.
Grid: B1 (4) x B2 (3) x B3 (3) x B4 (3 x 3) x B5 (2) = 648 configurations per case per footing. As-published = B1 none,
B2 0, B3 none, W0, drift 0, E1.

## Words
Per row and per (footing, case): P0 = as-published pull; Pmin / Pmax over the grid.
- AGREES if P0 <= 2; FRAGILE added if Pmax > 3.
- EXCLUDES if P0 > 3 and Pmin > 3; EXCLUDES, FRAGILE if P0 > 3 and 2 < Pmin <= 3.
- NO VERDICT if P0 > 3 and Pmin <= 2 (brackets alone span both), or 2 < P0 <= 3.
Headline per footing and case:
- "a0(z) AGREES" if rows S and L both AGREE (FRAGILE carried).
- "MEASURED RISE EXCLUDES THE LAW [footing]" if row S EXCLUDES and row G as published has P_G > 3 (FRAGILE carried from S).
  Row L adds "(level also excluded)" or not; it cannot make the word alone, because the level is degenerate with M/L.
- "NO VERDICT" otherwise.
Per footing headline: the four cases (L, D-Pan, D-DES5, D-Uni) are listed; if they differ, each is stated.
Row E gets its own word by the same rule with brackets k in {1, 0.5, 0} (k = 0: the z ~ 2 data sit at g ~ 3-11 a0 by
Milgrom 2017 as Escala quotes, where the BTFR zero point barely depends on a0). It does not enter the headline.
NOT EVALUABLE only if the known answers cannot run.

## Separation (stated in the headline)
Plain constant-a0 MOND predicts f = 1, i.e. case L of the law; the D cases differ from it by a few per cent at z < 1.5.
The script prints max |f - 1| over the bins; if it is below the smallest bin sigma, the test does not separate the law
from constant-a0 MOND. LCDM-native: no a0 law; hydro simulations quoted by the paper (Mayer: a0 x ~3 from z 0 to 2)
allow a rise, so a measured rise is not evidence against LCDM-native expectations; the lane does not grade LCDM.

## Known answers (stop before any word if one fails)
- KA1: f(3) for FRZ2's D and Q cases reproduce frz2_summary.out (0.775, 0.737, 0.706, 0.966, 1.005, 1.054) to 0.0005.
- KA1b: AZ2's a0(2.33) = sqrt X x footing: 1.320 x 9.3603e-11 = 1.235e-10 and 1.322 x 1.1312e-10 = 1.495e-10 to 0.001e-10.
- KA2: canonical a0 = (c H0 / 2) sqrt(3 Om_L / (8 pi)) with H0 67.4 km/s/Mpc, Om_L 0.685 within 5e-4 relative of
  9.3603e-11 (KAP1 got 9.3624e-11).
- KA3: Fig. 6 fiducial points agree with the Fig. 3 bin values to 0.02e-10 each (independent pixel reads).
- KA4: C_IF in a deep window [-13.0, -12.0] equals 1 within 0.01 (both functions share the deep limit and the +1/2 term).
- KA5: the paper's "~30 sigma" for a1: 1.59 / (0.10/1.96) in [25, 35].
- KA6: Fig. 6 statement reproduced through the response: corrected bin 1 at +0.2 dex and bin 4 at +0.45 dex both inside
  [1.0, 1.4]e-10 (the paper: these offsets reconcile with 1.2e-10).
- KA7: Tacconi check: t_c(z 0) in [13.5, 14.2] Gyr and mu_mol(z 1, log M* 9.5) inside the paper's 30-50 % gas fraction
  range expressed as mu in [0.3, 1.2] (loose; a failure means the sign restoration is wrong).

## Mutation and null twin (as published, row S, case L, canonical)
- MUT (must bite): bins replaced by 2.0e-10 x E(z_i)/E(z_1), E = sqrt(0.315 (1+z)^3 + 0.685), same sigma: P_S > 3.
- NULL (must not bite): bins replaced by 2.0e-10 x f(z_i) (the law's own shape, each graded case), same sigma: P_S < 1.

## Hand estimate (before any number)
f stays within a few per cent of 1 over 0.5 < z < 1.3 in every graded case, so S is about the measured rise itself:
ln(2.71/1.99) = 0.31 over dz 0.77, slope ~0.4, sigma ~0.07 under E1, P_S ~5-6 (E1) and ~11 (E2). G: P_G ~30. L: the
bins sit ~2x above both footings, ~15 per-bin sigma, so P_L huge as published, but B2 at +0.45 brings the level to
~0.6-1.1e-10. B1 at log M* 9.0-9.5 should take ~0.1-0.15 dex more mass at bin 4 than at bin 1, and B3 another 0.04 dex,
so Pmin for S should land near 2. Expected: NO VERDICT on both footings, all four cases, or EXCLUDES, FRAGILE. Row E:
as published Delta ZP is far from the law's ~0 (P ~6), k = 0 removes all power: NO VERDICT. The test does not separate
the law from constant-a0 MOND.

## Limits
Published bin values (half of them pixel reads) and the paper's own uniform-offset response stand in for a refit; the
bin CI level is not stated; the global fit's errors are statistical only and its a0(0) and a1 correlation is taken as
zero ("no significant correlations", App. F); a_bar and a_tot both come from the DC14 model fits, not from independent
data; the Tacconi relation is a field main-sequence average read through pdftotext with minus signs restored; the CPL
sets are extrapolated past their data at z 5 (row E).

## Run
`python3 -I -B mdz1.py <lane_dir> <inputs_csv> <mode>` with mode in {canonical, alt, MUT, NULL}; outputs
`mdz1_<mode>.json` / `.out` in the lane dir. Commits: this file alone; then script + CSV; then outputs and RESULT.md.
No push.

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
