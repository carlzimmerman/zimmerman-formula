# MDZ1 RESULT: the law's a0(z) against MUSE-DARK's measured a0(z)

**Canonical (a0 = 9.3603e-11): NO VERDICT** in all four cases (rho_DE constant; the record's evolving rho_DE, D-Pan,
D-DES5, D-Uni).
**Alt (a0 = 1.1312e-10): NO VERDICT** in all four cases.

As published, the rise excludes the law on both footings. MUSE-DARK's binned a0 rises with slope 0.43 +- 0.08 per
unit z, where the law predicts 0 (constant rho_DE) or a slight fall (the D cases). That is P_S 5.3-6.9 sigma reading
the bin bars as 1 sigma, and 10-13 sigma reading them as 95 %. The global a1 = 1.59e-10 sits 31-34 sigma from the
law. One combination of frozen red-team brackets brings the shape pull down to 0.1-1.5 on both footings: molecular
gas left out of a_bar at Tacconi 2020 main-sequence levels, plus the paper's own < 10 % inner-cut change, plus the
interpolating-function window. The brackets alone span both words, so the label is NO VERDICT. No single bracket gets
below 2: the lowest is 2.30, from molecular gas at log M* 9.5 in case L, and 3.49-3.90 in the D cases. Read one bracket
at a time, the label would be EXCLUDES, FRAGILE for case L and EXCLUDES for the D cases, on both footings.

**What the test separates.** The law with constant rho_DE predicts the same flat a0(z) as plain constant-a0 MOND. The
D cases differ from it by at most 9 % in level (more than the smallest bin sigma, 4.3 %, so the frozen print says "could
separate"). In shape, which is all that survives a free M/L, they differ by at most -0.13 per unit z against
sigma 0.08, about 1.6 sigma. So in practice the test does not separate the law from constant-a0 MOND. LCDM-native
expectations are not graded. The paper quotes hydro simulations (Mayer: a0 rises about 3 times from z 0 to 2) that
allow a rise, so a confirmed rise would count against both MOND-like laws and not against LCDM.

TEST lane. Criteria c6085ac92a (committed alone, before any script or number). Adopts nothing, relabels nothing. The
scorecard is not touched. Footings are never pooled.

## Table (as published, then the frozen bracket grid of 648 configurations)

P_S = shape pull (slope of ln a0 vs z, amplitude free). P_L = level pull (amplitude fixed by the footing, chi^2 with
4 dof as a Gaussian sigma). P_G = the paper's global a1 (Eq. 4) against the law's linear slope over 0.33-1.44.

| footing | case | law slope | P_S pub | P_S min / max | S word | P_L pub | P_L min | L word | P_G (a1) | intercept law vs 1.00e-10 | headline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| canonical | L (rho_DE const) | 0 | 5.29 | 0.08 / 25.9 | NO VERDICT | 39.1 | 2.46 | EXCLUDES, FRAGILE | 31.2 | 9.54e-11 (2.3 sigma) | NO VERDICT |
| canonical | D-Pan | -0.095 | 6.47 | 0.97 / 28.2 | NO VERDICT | 39.4 | 3.24 | EXCLUDES | 32.9 | 1.030e-10 (1.5) | NO VERDICT |
| canonical | D-DES5 | -0.113 | 6.69 | 1.20 / 28.7 | NO VERDICT | 38.5 | 3.63 | EXCLUDES | 33.3 | 1.066e-10 (3.2) | NO VERDICT |
| canonical | D-Uni | -0.129 | 6.88 | 1.38 / 29.0 | NO VERDICT | 37.6 | 4.17 | EXCLUDES | 33.6 | 1.103e-10 (5.0) | NO VERDICT |
| alt | L (rho_DE const) | 0 | 5.29 | 0.14 / 25.8 | NO VERDICT | 31.0 | 1.42 | NO VERDICT | 31.2 | 1.150e-10 (7.3) | NO VERDICT |
| alt | D-Pan | -0.095 | 6.47 | 1.05 / 28.1 | NO VERDICT | 31.3 | 1.74 | NO VERDICT | 33.3 | 1.241e-10 (11.8) | NO VERDICT |
| alt | D-DES5 | -0.113 | 6.69 | 1.27 / 28.6 | NO VERDICT | 30.5 | 2.10 | EXCLUDES, FRAGILE | 33.7 | 1.285e-10 (14.0) | NO VERDICT |
| alt | D-Uni | -0.129 | 6.88 | 1.46 / 28.9 | NO VERDICT | 29.6 | 2.30 | EXCLUDES, FRAGILE | 34.1 | 1.329e-10 (16.1) | NO VERDICT |

The law slope is d ln f / dz from the bins, the difference between that case's measured slope and the 0.426 of case L.
Measured bins (1e-10 m/s^2): 1.99 / 2.200 / 2.572 / 2.71 at z 0.502 / 0.824 / 1.046 / 1.274. The law in the paper's
convention is 0.954e-10 (canonical) and 1.150e-10 (alt) times f(z). So as published the bins sit 2.1-2.8 times above
the canonical law and 1.7-2.4 times above the alt law.

f at the bins: D-Pan 1.032 / 1.007 / 0.984 / 0.958; D-DES5 1.059 / 1.032 / 1.002 / 0.969; D-Uni 1.088 / 1.058 / 1.023 /
0.983. The record's evolving rho_DE peaks near z 0.5 and then falls. Every D case predicts a0 falling across the
sample, which makes the disagreement slightly worse than with constant rho_DE.

Reported, not graded, as published:
- FRZ2's Q cases: P_S 5.1-5.4.
- a0 proportional to H(z) (Om 0.315): P_S 2.11, but P_G 12.5 (canonical) and 8.7 (alt), and P_L 16 / 8. The H(z) shape is
  near the binned rise, while its level and the global a1 are not.
- The paper's other global fits against the law's a1: Eq. 9 (best profile per galaxy) P 25.6-27.9; Eq. 14 (MOND fits)
  P 23.5-26.5; the per-galaxy MOND a0 regression (a1 1.42 +0.94/-0.89, CI level unstated, taken as 1 sigma) P 1.6-1.7.

## Brackets (frozen; single edges, case L canonical, P_S / P_L)
- B1, molecular gas left out of a_bar (Tacconi 2020 main sequence, mu_mol = t_depl sSFR):
  - log M* 9.0: 3.40 / 3.97. log M* 9.5: 2.30 / 11.9. log M* 10.0: 2.59 / 19.7.
  - mu_mol per bin is 0.94-1.71 at log M* 9.0, 0.60-1.21 at 9.5 and 0.38-0.86 at 10.0. The z ~ 1 values agree with the
    paper's 30-50 % gas fraction (KA7).
- B2, uniform M/L or IMF offset of +0.2 or +0.45 dex: 7.44 and 11.23. A uniform offset steepens the rise, because in the
  paper's Fig. 6 the low-z bins respond more. It lowers the level (P_L 21.9 and 14.1) but never rescues the shape.
- B3, inner-cut ramp (-10 % at bin 4): 3.60. The +10 % ramp gives 6.82.
- B4, interpolating-function window and drift: 4.85-5.49 on the shape. C_IF = 1.006-1.048 (canonical), so the
  conversion from the simple mu to McGaugh's function moves the level by under 5 %.
- B5, error-bar read as 95 %: 10.36.
- Combined minimum (B1 log M* 9.5 or 10.0, B3 -10 %, window [-11, -9.5], drift +0.5): 0.08-1.46 across footings and
  cases. At those minima the largest mass offset is 0.345 dex, inside the paper's own +0.45 dex response range (no
  extrapolation). Elsewhere in the grid, offsets reach 0.656 dex (B2 +0.45 plus gas), and those use the extrapolated
  response.
- For the unsourced brackets (pressure-support correction with z, stellar M/L evolution such as outshining, HI
  evolution, selection drift in M*), the needed size is a0 lower at bin 4 than at bin 1 by 0.084-0.123 dex for P_S = 2
  and 0.143-0.184 dex to flatten fully. For scale, the paper's own App. E reports M* 0.28 dex higher when a0 is fixed
  at 1.2e-10.

## Row E: Escala's BTFR reading (secondary; not in the headline)
Zero-point offsets read from Escala's Fig. 2: Ubler 2017, -0.439 +- 0.071 at z 0.90 and -0.269 +- 0.071 at z 2.30;
Gomez-Espinoza 2026 (submitted), -0.539 +- 0.191 at z 5.0. The law predicts -log10 f: 0 for case L, and +0.07 to +0.29
at z 2.3-5 for the D cases (the CPL is extrapolated far past its data). The law's offset has the opposite sign to the
data. With all of each offset attributed to a0 (k = 1), P_E is 7.2-8.4. At k = 0, where the z ~ 2 discs sit at
g ~ 3-11 a0 (Milgrom 2017, as Escala quotes) and the zero point barely depends on a0, P_E is 0-1.2. Row E is NO VERDICT
in every case on both footings (it does not depend on the footing). Escala's own reading needs a0 to rise with an
Omega_m 0.05 expansion history, which is not the law.

## Known answers, mutation, null twin
- KA1: FRZ2's f(3) reproduced (0.7750 / 0.7370 / 0.7062 / 0.9664 / 1.0046 / 1.0535). PASS.
- KA1b: AZ2's a0(2.33) is 1.2356e-10 / 1.4954e-10. PASS.
- KA2: canonical a0 from H0 67.4 and Om_L 0.685 is 9.36238e-11 (+2.2e-4). PASS.
- KA3: Fig. 6 against Fig. 3 bins, independent pixel reads, max diff 0.006e-10. PASS.
- KA4: C_IF deep is 1.0003. PASS.
- KA5: the paper's ~30 sigma reproduced as 31.2. PASS.
- KA6: the paper's Fig. 6 statement reproduced (1.245e-10 and 1.128e-10). PASS.
- KA7: t_c(0) 13.90 Gyr; mu_mol(z 1, log M* 9.5) 1.03. PASS.
- MUT: bins following H(z), P_S 7.93. Bites.
- NULL: bins following the law's own f(z) in each graded case, P_S 0.000. Does not bite.

## Red-team notes on the data teams' assumptions
- a_bar and a_tot both come from the same DC14 disk-halo fit, not from independent photometry. M* is inferred from the
  dynamics and agrees with the SED masses (their Fig. 11, Paper I).
- The baryons are a stellar disk traced by ionised-gas light, a constant-Sigma HI term and a bulge in 4 galaxies. H2 is
  not modelled separately, although the authors name it as a ~0.2 dex systematic at z ~ 1. This is the bracket that
  moves the shape most, because the gas-to-star ratio rises with z.
- The asymmetric-drift correction (Dalcanton & Stilp) grows with sigma/v, and sigma/v grows with z. Its direction and
  size per bin are not published, so only the size it would need is reported.
- The bins are equal-population quantiles of points, not of galaxies. Mass completeness is at log M* 8.8, but the M*
  distribution inside each bin is not published.
- The fitted "a0" is McGaugh's function. The law's simple function gives the same a0 in the deep regime (KA4), and the
  conversion is under 5 % here.

## Limits
- No per-galaxy RAR. The paper's data link (dark-matter.osu-lyon.fr via dark.univ-lyon1.fr/data-releases) timed out
  from this machine, A&A returned 403, and no Zenodo, VizieR or GitHub deposit was found. So no refit at fixed a0(z)
  with the law's own function was possible; the lane grades published values.
- Two bin values and all four bin errors are pixel reads of Fig. 3. The text gives 1.99 and 2.71; Fig. 6 cross-checks
  the other two to 0.006e-10. The caption does not state the CI level of the bin bars.
- The global fit's errors are statistical; the a0(0)-a1 correlation is taken as zero, per App. F.
- The bracket response is the paper's uniform-offset response, used for a z-dependent offset.
- Tacconi's Eq. 1 was read through pdftotext with minus signs restored to the S14 form. KA7 checks the result
  loosely.
- The D cases extrapolate CPL fits past their data at z 5 (row E only).
- The first run, before commit 55c05a60f4, gave the same words. The fix touched only the JSON writer, the chi^2 tail
  past chi^2 ~ 1500 (P_L printed as inf) and the root used for the required-ramp report (printed nan).

## Run (from a copy at the same folder depth; deterministic)
`python3 -I -B mdz1.py <lane_dir> <lane_dir>/mdz1_inputs.csv <mode>` for mode in MUT, NULL, canonical, alt. This writes
`mdz1_<mode>.out` and `.json`. A re-run from a scratch copy reproduced all eight files byte for byte. The script refuses
a CSV whose sha256 is not the frozen one.

Commits (local only, not pushed): criteria c6085ac92a (alone); script + inputs CSV 12042a4086; script fix 55c05a60f4;
outputs + this file (next commit).

kappa = 1/2 FITTED; not theory closed. Adopts nothing.
