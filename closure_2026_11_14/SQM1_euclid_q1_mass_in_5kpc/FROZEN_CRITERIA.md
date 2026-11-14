# SQM1 (EUCLID Q1 TOTAL MASS INSIDE 5/h kpc FROM STARS UNDER THE LAW): FROZEN CRITERIA

TEST lane, 2026-11-14. Committed alone, before any SQM1 script exists and before any graded number is computed.
Adopts nothing, relabels nothing, edits no scorecard or other lane's file.

kappa = 1/2 FITTED. Footings canonical a0 = 9.3603e-11, alt a0 = 1.1312e-10 m/s^2, graded side by side, never pooled.
The test is one-sided against the framework's own no-dark-matter claim: a PASS is not a pass of the lensing gate.

## 0. Question

Sonnenfeld, Nersesian, Rojas et al. (Euclid Collaboration), arXiv:2611.00224 v1 (30 Oct 2026), "Euclid Quick Data
Release (Q1). Mass-to-light ratio of elliptical galaxies: constraints from strong lensing". 95 "golden" lenses with a
forward-modelled selection function. Result (their Table 4, Eq. 25):

    mean log10(M5 h / Msun) = mu_M0 + beta_z (z - 0.5) + beta_L [log10(L_r h^2 / Lsun,r) - 10.7]
                                    + beta_R [log10(R_e h / kpc) - 0.5]
    mu_M0 = 11.300 +- 0.021, beta_L = 0.71 +- 0.07, beta_z = -0.33 +- 0.05, beta_R = -0.15 +- 0.07, sigma_M = 0.099.

M5 = total projected mass inside a cylinder of radius 5/h kpc (physical). Does the law, from the stars alone (no halo,
no particle dark matter), predict the amplitude at the pivot, the luminosity slope beta_L and the redshift trend beta_z?

**Which number is graded (RAW DATA vs FRAMEWORK-NATIVE).** M5 is a total lensing mass: the paper fits an SIS total
profile (not a halo decomposition) and shows (Sect. 7) that mu_M0 is unchanged for gamma = 1.9 and gamma(z); the median
Einstein radius sits at about 5/h kpc, so M5 is close to a direct Einstein mass. That is graded. The paper's Fig. 10
NFW / contracted-halo curves and its stellar-to-halo relation are LCDM-model quantities: not used, not graded.

## 1. Inputs (frozen, read as data; downloads untracked under `_external_data/sqm1_sonnenfeld_q1/`)

| File | sha256 | Use |
|---|---|---|
| `2611.00224v1.html` (arxiv.org/html/2611.00224v1) | f0e6f872a44345b32939591cb1a28e692531e5bbc6ef35ac57803d67acd09b53 | every paper number |
| `astro-ph_0302543.pdf` (Bell, McIntosh, Katz, Weinberg 2003, ApJS 149, 289) | 7696b09581a0a156a5e9fdba35d52599ea700e7d003bdb29297a60e58cd8ddbc | stellar M/L vs colour, primary |
| `0904.4252.pdf` (Zibetti, Charlot, Rix 2009, MNRAS 400, 1181) | ad200f04a53bf34d46fb5d6aa4040e7245ebb9cd4d12ee59788c07fa55ae1429 | stellar M/L vs colour, bracket |
| `real_research/data/slacs_auger2009_lenses.tsv` (tracked) | d78d7627d6bbcc0789bde334ca607f760b40b5b7f8a1d04720eae8206f2d7b6d | known answer K2 only |

Every number used is transcribed, with its location, into `sqm1_paper_numbers.csv` (committed with the script). The
script reads that CSV; nothing is typed into the script that is not in it, except the footings and constants of §3.

Numbers read before freezing (all from the files above):
- Paper Table 4: as in §0. Table 3 (non-lens population, z = 0.5 pivots): mu_C0 = log10(L_r/L_g) = 0.316 +- 0.001,
  zeta_C = -0.078 +- 0.003 per unit z, sigma_C = 0.0101; mu_R0 = 0.40, zeta_R = -0.36, rho_L1 = 0.34, rho_L2 = 0.93,
  log L_t = 10.48, b_L = 0.20, sigma_R = 0.187. Sect. 5.1: L_r,sun = 6.00e11 W/Hz (Willmer 2018). Sect. 1: Omega_m = 0.3,
  h explicit. Sect. 3.1 / Table 1: lens light fitted with a de Vaucouleurs (n = 4) profile; L and R_e from that fit.
- Sect. 6: M5/L5 inside 5/h kpc at the pivot with average size = 6.7 +- 0.3 Msun h / Lsun,r. SLACS comparison: the
  paper's model gives 11.38 +- 0.03 at log L = 10.67 at SLACS redshift (SLACS itself 11.33 +- 0.01). Passive
  evolution (Galaxev single burst at z = 2.5, solar Z, H0 = 70): luminosity drops 0.36 dex from z = 1 to 0 at fixed
  stellar mass (no-growth case). Lenses vs population at fixed L: +0.08 dex at log L = 10.6, +0.05 dex at the bright end.
  Range of the measurement 0 < z < 1.
- The paper reports no stellar mass and no stellar M/L as a measurement. Its Fig. 10 SPS curves (Galaxev, tau = 1 Gyr,
  7 Gyr since burst, Chabrier and Salpeter) are given only as curves; no number is readable from the text.
- Bell et al. 2003 Table A7: log10(M/L_r) = -0.306 + 1.097 (g - r), SDSS AB, "diet" Salpeter IMF (70 % of Salpeter
  mass at the same colour and light); subtract 0.15 dex for Kroupa / Kennicutt; scatter about 0.1 dex.
- Zibetti et al. 2009 Table B1: log10(M/L_r) = -0.840 + 1.654 (g - r), Chabrier IMF; Sect. 2.4: Bell's M/L scaled down
  by 0.093 dex to Chabrier (after Gallazzi et al. 2008).

## 2. Stellar M/L prior (frozen; never fitted to the lensing)

Colour. The paper's luminosities are spectral (W/Hz, solar unit 6.00e11 W/Hz), so the rest-frame colour
`(g - r)_AB = 2.5 x log10(L_r/L_g)`. Reason, fixed here: in solar-luminosity units the same 0.316 would mean
g - r = 1.23 AB, far redder than any elliptical; the per-Hz reading gives 0.79, a normal red-sequence colour.
Population mean colour at redshift z: `(g - r)(z) = 2.5 [0.316 - 0.078 (z - 0.5)]` (paper Eq. 21, Table 3). The
paper's colour model has no luminosity dependence, so the M/L prior is independent of L at fixed z.

- **Primary relation (P-Bell):** Chabrier `log10 Y_r = -0.306 + 1.097 (g - r) - 0.093`.
- **Bracket (B-Zib):** Chabrier `log10 Y_r = -0.840 + 1.654 (g - r)`.
- **IMF bracket (continuous):** `log10 Y = log10 Y_Chab + delta`, delta from 0 (Chabrier) to 0.248 (Salpeter =
  diet Salpeter + log10(1/0.7) = Chabrier + 0.093 + 0.155). Graded on a grid of delta, 0 to 0.248 in steps of 0.004.
- Redshift dependence of Y at fixed L: through the colour above (primary, same relation as the amplitude). Bracket
  (B-pass): the paper's own passive-evolution number, `d log10 Y / dz = -0.36` (0.36 dex from z = 1 to 0, linear).

## 3. Prediction recipe (frozen)

Physical units, SI throughout (constants as EUC1: G = 6.67430e-11, Msun = 1.98847e30 kg, kpc = 3.0856775814913673e19 m).

- Pivot galaxy: z = 0.5; `L = 10^10.7 / h^2 Lsun,r`; `R_e = 10^0.5 / h kpc` (the Table 4 pivot); aperture
  `R5 = 5 / h kpc`. **Primary h = 0.70** (the paper's own choice for its age-redshift conversion, Sect. 6).
- Baryons: a spherical de Vaucouleurs (Sersic n = 4) body of mass `M* = Y L`, deprojected with Prugniel-Simien
  (EUC1's `M3D_frac`). Stars only: no gas, no halo, no neighbours, no external field (each omission raises the supply
  or is negligible inside 7 kpc; §8).
- Law S (primary, the verdict law as in EUC1): `g = (g_N/2)(1 + sqrt(1 + 4 a0(z)/g_N))`. Law B
  (`g^2 = g_N^2 + a0 g_N`) reported beside it, never the word.
- a0(z): the record's tracking convention (CFG681, AZ2, FRZ2), `a0(z) = a0 sqrt(X(z))`, `X = rho_DE(z)/rho_DE(0)`.
  **Primary X = 1** (AZ2's A2 headline: FLAT HOLDS at z 2.33). Bracket (B-cpl): FRZ2's D-DES5, X = F(z) =
  (1+z)^(3(1+w0+wa)) exp(-3 wa z/(1+z)), (w0, wa) = (-0.752, -0.86).
- Projection: `M5 = M_2D(<R5) = (R5^2/G) int_R5^rmax g dr / sqrt(r^2 - R5^2)`, rmax = 1e6 kpc (EUC1's `M2D_from_gfun`,
  Gauss-Legendre 400 nodes in r = R cosh u). Code copied from `closure_2026_11_12/EUC1_eclipse_saturation_ceiling/euc1.py`
  (commit 5926a21305), cited in the script.
- Amplitude: `A_pred = log10(M5 h / Msun)` at the pivot.
- Luminosity slope: least-squares slope of `log10(M5 h)` against `log10(L h^2)` over 10.40 to 11.00 in steps of 0.05
  at fixed R_e h, z = 0.5, fixed Y (the paper's beta_L is at fixed R_e).
- Redshift trend: least-squares slope of `log10(M5 h)` against z over 0.20 to 0.80 in steps of 0.05 at fixed L h^2
  and R_e h, with Y(z) and a0(z) as above.
- Newton (stars only, a0 = 0) is computed beside every number.

## 4. Sigma budget and words (frozen)

sigma per quantity = sqrt(sigma_obs^2 + sigma_pred^2): amplitude sigma_obs 0.021; beta_L 0.07; beta_z 0.05.
sigma_pred = the propagated error of the paper's colour numbers (mu_C0 +- 0.001, zeta_C +- 0.003) through the M/L
relation; IMF, relation choice, h and a0(z) are brackets, not sigma.

Per quantity, at each delta: **PASS** if |pred - obs| <= 2 sigma; **HIGH** if pred - obs > 2 sigma; **LOW** if
pred - obs < -2 sigma.

Row word per footing (law S, primary everything else):
- **PASSES** if all three PASS at every delta in [0, 0.248].
- **STILL FAILS [q, ...]** if some quantity q fails at every delta in the bracket (no IMF in the bracket rescues it),
  or if no single delta passes all three at once (then the label lists "[no single IMF passes all three]").
- **NO VERDICT** if some delta passes all three and some other delta fails one (the IMF / M/L bracket alone spans
  pass and fail).
- Reported with it: the delta interval on which each quantity passes, and the delta interval passing all three.

**FRAGILE** is appended if any bracket of §6 changes the row word on that footing.

## 5. Known answers (frozen; any failure stops the lane before any word: NOT EVALUABLE)

- **K1** EUC1's K1: point mass returned by the projection to 1e-6; SIS deflection constant to 1e-4.
- **K2** EUC1's K2 with the copied code: SLACS median R_E,pred/R_E,obs = 0.885 +- 0.005 (a0 = 1.132e-10, Salpeter,
  n = 4, Auger cosmology), the number EUC1 recorded as 0.8852.
- **K3** Newton limit: at a0 -> 1e-30 the projected M5 equals `Y L x M2D_frac(R5; R_e, 4)` to 1e-5.
- **K4** Paper side, my reading of Eq. 25: M5/L5 at the pivot (z 0.5, log L 10.7, average size from Eq. 23) =
  `10^(mu_M0 + beta_R (mu_R - 0.5)) / (10^10.7 x M2D_frac(5; 10^mu_R, 4))` must be 6.7 +- 0.35 Msun h / Lsun.
- **K5** Paper side: the model value at log L 10.67, SLACS mean redshift 0.2 (zeta_R, zeta_C as Table 3), average
  size, must be 11.38 +- 0.03.
- **K6** SI units: Lsun,r = 6.00e11 W/Hz must give M_sun,r(AB) = 4.65 +- 0.02 (Willmer 2018's r-band value).
- **MUTATE** (`SQM1_MUTATE=newton`, a0 -> 1e-30 on both footings): beta_L,pred must equal 1.000 +- 0.005 and the
  amplitude must fall by at least 0.03 dex on both footings; the script exits 1. Outputs under a separate name.
- **NULL twin** (`SQM1_MUTATE=null`): the whole primary recomputed in astronomical units (kpc, Msun, km/s,
  G = 4.300917e-6 kpc (km/s)^2/Msun) with 800 quadrature nodes; every graded number must agree with the SI run to
  1e-4 dex (1e-4 in the slopes) and every word must be the same; exit 0. Outputs under a separate name.

## 6. Brackets (written before the run; red-team of the paper's and my assumptions)

- **B-Zib** Zibetti M/L-colour relation in place of Bell (amplitude and z trend).
- **B-pass** Y(z) from the paper's passive evolution, -0.36 dex per unit z.
- **B-h** h = 0.6774 (EUC1's catalogue cosmology), h = 0.73, and the footing's own h at Omega_m 0.30 from AZ2 §3
  (0.667 canonical, 0.806 alt). The paper keeps h explicit; the law has a scale, so the prediction of M5 h moves with h.
- **B-cpl** a0(z) tracking DESI-like CPL (FRZ2 D-DES5).
- **B-size** Average size at the pivot (log R_e h from Eq. 23, 0.541) instead of 0.5, with the paper's beta_R applied
  to the observed amplitude.
- **B-along** Slope along the size-luminosity relation instead of at fixed R_e: observed beta_L + beta_R d mu_R/d log L
  (d mu_R/d log L from Eq. 23 at the pivot), error sqrt(0.07^2 + (0.07 d mu_R/d log L)^2) (no covariance printed in
  the paper; the paper says beta_L and beta_R are strongly degenerate, so this error is an upper bound); predicted
  slope with R_e following Eq. 23. Tests the beta_L / beta_R degeneracy.
- **B-sel** Selection: observed amplitude raised by the paper's lens-minus-population offset at the pivot (+0.05 to
  +0.08 dex; +0.065 used), i.e. as if the selection correction were wrong entirely.
- **B-n6** Stars as a Sersic n = 6 body with the same L and R_e (de Vaucouleurs may under-count wings of massive
  ellipticals; EUC1's median Sersic index was 5.34).
- **B-rmax** rmax = 300 kpc (truncated phantom field).

Not brackets, stated: the profile family (paper Sect. 7: mu_M0 unchanged for gamma = 1.9 and gamma(z); mass-sheet
transformations near lambda = 1 also); photo-z bias (paper: 0.014 mean, under 0.1 % in Sigma_cr); source-population
template (paper: SB6 changes the parameters very little).

## 7. Hand estimate (made before freezing; arithmetic on the numbers above, no code)

h = 0.7: R_e = 4.5 kpc, R5 = 7.1 kpc (1.58 R_e, de Vaucouleurs light fraction about 0.6), L = 1.0e11 Lsun.
g - r = 0.79; Chabrier Y about 2.9 (Bell and Zibetti agree to 0.01 dex at this colour), M* about 3.0e11 Msun.
Newton Chabrier: log M5 h about 11.11, about 0.19 dex LOW; Newton Salpeter about 11.36. The law's cold pull at
7 kpc (g_N about 5 a0) adds roughly 0.05 to 0.1 dex: Chabrier about 11.2 (LOW), Salpeter about 11.4 to 11.45
(HIGH); so the amplitude likely passes only inside the IMF bracket (delta near 0.1). Slope: Newton exactly 1 at fixed
R_e and Y (4 sigma HIGH); the law lowers it, guessed to about 0.9 (still near 2.7 sigma HIGH). z trend: Bell colour
route d log Y/dz about -0.21, so beta_z about -0.2 (HIGH by about 2.5 sigma); the Zibetti and passive routes give
about -0.3 (PASS). Expected: STILL FAILS [beta_L] on both footings, possibly FRAGILE through the z trend. This is a
guess; the run decides.

## 8. Limits (stated now)

- No gas: hot gas inside 7 kpc of a massive elliptical is a small fraction of the stars; leaving it out lowers the
  supply (favours a LOW amplitude, not a HIGH slope). No external field (raises the supply by omission).
- Y independent of L (the paper's colour model). A Y rising with L (colour-magnitude relation, IMF trends) would only
  steepen the predicted slope.
- A population-mean prediction from the pivot galaxy: the mean of log M5 over the scatter is not modelled; the law is
  close to linear in Y over the scatter (sigma_C gives about 0.03 dex in Y).
- One paper, one transcription; the paper's posterior covariances are not printed.
- No measurement of a0 or kappa; no statement about halos.

## 9. Order of work

Criteria (this file) alone; then script + transcription CSV; then results (RESULT.md and outputs). Local commits only,
no push. Commit subjects carry no outcome word.
