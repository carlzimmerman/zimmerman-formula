# WA1_wall_common_cause: frozen criteria, committed alone, before any script or number of this lane

**Question.** Is there one set of shared shifts, each inside an externally measured prior, that clears many walls at once for a candidate? Or do the walls hold under honest marginalisation? Either answer is a result. Adopts nothing. kappa = 1/2 FITTED; not theory closed; footings canonical 9.3603e-11, alt 1.1312e-10 m/s^2 reported, never pooled; no LCDM input, no Planck 5.364; the cold sector stays retired and nothing here reinstates it; nothing here says the data favour the framework.

**Not blind, heavily.** Before writing this I read RQ3's rows and scorecards (law, UX3), FG1, DW2, DA1, KS1, GS4, FR1, OD1, CRG1, MX1, J1, X19, BF2, BK2, M3A1, LF1, UL1, GS1. I know the law's Z on every RQ3 row and the kills on BF2's forms (A30, Saturn, Bullet). I ran RQ3's law rows once to time them and saw nothing new. I chose priors knowing which way each wall wants to move. So the priors are written below with their sources and a doubled-prior sensitivity.

**Expectation on record.** WALLS HOLD for every candidate. The Bullet sign, Saturn and equivalence are structural: no nuisance touches them, they are expected to stay as they are, and so CLEARS is expected to be unreachable for any candidate failing one. I expect Upsilon to be pulled upward, helping A5, A6; I expect M3, A30 and the dwarfs not to move enough.

## 1. Candidates, each per footing
| id | row | source |
|---|---|---|
| LAW | a0 law | RQ3 `candidates/law.py` |
| UX3 | UX3 gas term, k fit, unswitched | RQ3 `candidates/ux3_term.py`. X-COP is its training set, so X-COP lines sit out of its chi^2, as in RQ3; reported separately |
| P3, P7 | BF2's forms | BF2 `candidates/`. Picked from about 1.7e11 tries; BF2 is not above its control |
| MX1 | MAX rule, primary cell P | MX1 `cand_P.py` |
| BK2 | closest no-fit row (a): I5(g_b, a0) [(8 pi/3) g_gas / sqrt(a0 g_b) + (g_star/g_b)^4] | BK2 README; candidate written here, must reproduce BK2's G8 M3 at gas +0.005, f* 0.034 to 0.02. Picked from about 2.7e10 |
| CAL | retired route-E row, CRG1 C1, `cold_halo.py` | **Calibrator only, never a candidate, no label.** Reinstates nothing. On the lines it computes |

## 2. Nuisances, priors frozen. theta_j in prior sigma about the prior centre
Prior correlation: rho(ups, fstar) = +0.5, since both carry the IMF. All others zero, stated, not measured. Web numbers are PROVISIONAL (search summaries, not the papers).

| id | meaning | centre, sigma | source |
|---|---|---|---|
| ups | log10 true/assumed stellar mass-to-light, all stellar masses | 0, 0.10 dex | Meidt+14 ApJ 788 144: about 0.1 dex at 3.6 um, PROVISIONAL |
| hse | log10 M_true/M_HSE | +0.06, 0.06 dex | Mean and spread of weak-lensing ratios: Smith+16 0.95 +- 0.05, Mahdavi+13 0.88 +- 0.05, Hoekstra+15 0.76 +- 0.08 (conversion PROVISIONAL, web). Lensing masses, no background model in the ratio beyond geometry. LF1's -0.12 on X-COP uses the keys' shear, so it isn't used for the prior; it lies 3 sigma off, and the doubled-prior row covers it |
| gas_abs | absolute X-ray gas mass scale, X-COP, Lovisari groups and keys | 0, 0.02 dex | No clean independent absolute measurement on disk. Size taken from GS4's instrument class errors (XMM +0.005 +- 0.020). **Weak, said so** |
| gas_rel | eRASS1 against pointed gas, keys only | +0.005, 0.017 dex | GS4 |
| carry | gas density slope beyond R500, keys only (X-COP lines stop at x 0.7) | 2.777, 0.20 | GS1, bootstrap 16-84 % half range of [2.676, 3.071] |
| tilt | eRASS1 to pointed gas slope with mass, about lg M500 14.3: group gas against cluster gas, keys only | -0.10, 0.10 per dex | GS4. Lovisari groups are pointed gas, so B2 doesn't take it |
| dist | ln of the distance scale, about each dataset's own fiducial | 0, 0.03 | SH0ES 73.04 +- 1.04, CCHP about 70, PROVISIONAL. Ladder values; no CMB input |
| lens | shear calibration, data x (1 + m), keys and A30 | 0, 0.03 | m at most 0.02 (M3A1 provisional ceiling) with n(z) 0.02 in quadrature, PROVISIONAL; KiDS papers located, numbers not read |
| fstar | cluster stellar share in keys | 0.04775, 0.01375 | RQ3's cells 0.034 and 0.0615 as +-1 sigma (X71, CFG408). X-COP's stars are measured and take ups |

## 3. Lines, per candidate and footing, all through RQ3's functions and data
Residual z_i(theta) = (data - model)/sigma_i, each with its own stat error, and **any systematic now carried by a nuisance is removed from sigma_i, no double counting.**
| Lines | n | sigma used | Responds to | Can't respond, because |
|---|---|---|---|---|
| A3 tilt | 1 | RQ3 | dist | free Upsilon per galaxy absorbs ups |
| A4 | 1 | RQ3 | ups, dist | |
| A5, A6 Upsilon level per bin | 5 + 5 | RQ3's h; correlation between the two estimators from the shared boot and 0.04 terms | ups (-u/h, analytic), dist | |
| A9 LITTLE THINGS | 1 | RQ3 | ups, dist | |
| A10 IC 1613 | 1 | RQ3 | ups | Cepheid distance, not flow |
| A13 dwarfs by class, algebraic field | 5 | RQ3 (sd + stack term) | ups | Local Group distances. A12 sensitivity below; A11 reported for the law only, it needs LW1's solver |
| A15, A17 Milky Way, form R | 2 | RQ3 | none | star counts, cell search over its own priors already inside the row |
| A18 DiskMass, first declared form | 1 | RQ3, c inside | none | Upsilon solved per galaxy; c is its own unsettled term and is shared with nothing |
| A20 | 1 | RQ3, 0.24 kept | none | its 0.24 already holds Upsilon; form of the older chain differs, so not tightened |
| A23a TDG, Z = (chi2 - 6)/sqrt 12 | 1 | as A30's form | ups | |
| A23b DF2, DF4 | 2 | RQ3 | ups | |
| A24 UDG | 1 | RQ3, CFG31's floor kept | ups | floor may overlap ups, generous, disclosed |
| A26a, A26b | 2 | RQ3, A26b's IMF floor kept | ups | same disclosure |
| A30 lensing, Z = (chi2 - 56)/sqrt 112 | 1 | RQ3 | ups, lens | dist: its background and covariance are fixed in the source |
| B1 groups | 1 | stat only, the 0.10 dex stellar term removed | ups, dist | |
| B2 Lovisari, R500, R2500 | 2, rho 0.5 stated | er and stellar bracket; 20 % HSE removed | hse, gas_abs, ups, dist | |
| X-COP, x 0.1, 0.2, 0.3, 0.5, 0.7, log10(M_HSE/M_model), replaces B23 and B25, which are the same data | 5 | cluster scatter; covariance = 0.5 sample + 0.5 its diagonal, over N clusters; 0.12 dex HSE removed | hse, gas_abs, ups, dist | |
| Keys, 15 | 15 | RQ3's s; R_boot at h 0.672 with its 1e-3 eigenvalue cut; G-OUT-M3 only also takes M3A1's leak and seed in quadrature | gas_abs, gas_rel, carry, tilt, fstar, dist (via h 0.672 to 0.686), lens (m A/s) | ups: through fstar only |

Blocks are independent apart from the nuisances: no cross-block statistical covariance is on disk (RQ3).

**Not in chi^2, gates only.** LINE ONLY rows at the best-fit shift: A1, A2 (window 0.50-0.80 taken against U / 10^u), A16, A21, A25, B24. Structural rows: **S1 Bullet sign**, read from each lane's record; **S2 planets, C1**, RQ3's row, its Z is too large to enter a Gaussian chi^2; **S3 equivalence**, read from the record: FAIL blocks; NOT COMPUTABLE, with a tag, doesn't block and isn't a pass. B28's mass Z stays out: sigma PROVISIONAL. B19, B20 are combinations of keys, so out. A7 is a combination of A5 bins, so out of chi^2 and kept as a gate. Rows NOT COMPUTABLE for a candidate drop from its chi^2, are listed, and that is an advantage to it, stated.

**Response.** Each nuisance run through the real rows at -2, -1, +1, +2 sigma where the row is computed by g; a separable quadratic per line, z_i(theta) = z_i(0) + sum_j (a_ij theta_j + b_ij theta_j^2). Keys: 80-second real runs; gas from the cached 0.005 dex step, tilt and carry at +-1 sigma, fstar and h from cells, linear (quadratic where three nodes exist). Closure: rows are rerun at the fitted theta and the rms gap to the quadratic reported. If it is above 0.5 on a candidate's soft lines, I report that candidate's fit as NOT CONVERGED beside the number.

**Untouched.** A line is untouched if max_j |dz_i at +-1 sigma| < 0.10.

## 4. Statistics, stated before running
- chi2_0: theta = 0, sigma as above.
- chi2_prof: min over theta of |C^(-1/2) z(theta)|^2 + theta^T P^(-1) theta. **Penalty: the Gaussian prior term, nothing extra in the statistic, and any |pull| > 2 in the unconstrained minimum vetoes CLEARS outright. The fit inside a +-2 sigma box is printed too, with its chi^2 and its own line failures.**
- chi2_marg: -2 ln of the prior-averaged likelihood, Laplace about the minimum (exact in the linear case: chi2_prof + ln det(I + R^T C^-1 R P)).
- Pull: theta_j-hat in marginal prior sigma, the shift in physical units beside it.
- Pull table per line: harness Z, z(0), z(theta-hat).
- **Mocks.** 4000 per cell: draw theta from the prior, noise from C, data = candidate at theta + noise. Empirical p of each statistic, = (1 + count of mock >= observed)/(4001). chi2_0 on theta = 0 mocks too. Asymptotic chi^2 p printed beside it where the empirical p hits its floor. Rate of each label in the mocks is printed: how often a true candidate would read CLEARS, so the line's strictness is visible.
- **Scrambled-label control.** 2000 per cell: permute the whitened residuals among lines, keep responses and priors. Statistic D = chi2_0 - chi2_prof. p_scr = fraction >= real D. A high D that a scramble matches is no common cause.
- **Look-elsewhere.** 12 cells (CAL not counted), 9 single-nuisance releases, so 108 looks at release; p printed with Bonferroni over 12 cells. BF2's and BK2's search trials can't be corrected here and are stated.
- **Release.** One nuisance free inside its prior, the others at their centres: D_j. Also with its prior removed: the shift required, in sigma. **The nuisance whose release helps most candidates** = most cells where it has the largest D_j and D_j >= 4.

## 5. Labels, frozen. Joint p line 0.05, empirical, on chi2_prof
- **CLEARS**: p >= 0.05, every |pull| <= 2, every line-only gate passes at theta-hat, every untouched line |Z| <= 2, S1 and S2 PASS, S3 not FAIL.
- **SOFT CLEARS, WALLS STAND**: first three hold, but an untouched line, S1, S2 or S3 fails.
- **PULLED**: p >= 0.05, some |pull| > 2.
- **WALLS HOLD**: p < 0.05.
UX3 reads under the same rule on its non-training lines, tagged [X-COP TRAINED]. Any label better than WALLS HOLD needs its keys rerun for real at theta-hat, and stands on that rerun.

**Lane verdict.**
- COMMON CAUSE POINTS AT THE DATA: at least one cell CLEARS or SOFT CLEARS and p_scr < 0.05 in that cell.
- PARTIAL: no such cell, but p_scr < 0.05 in at least half the candidate cells: shared shifts really do move lines together, not enough to clear.
- WALLS HOLD UNDER MARGINALISATION: otherwise.
No result reads as support for a candidate; CLEARS means the shifts aren't excluded, nothing more.

Sensitivities, reported, no label: all priors x 2; A12 for A13; dropping RQ3's disputed rows.

## 6. Checks, reported however they fall
- K0 reproduction: at theta = 0 with RQ3's sigma, every line equals the RQ3 or lane scorecard on file, |dZ| <= 1e-6 (rows), 1e-4 (keys). My copies of B1, B2, X-COP must meet this.
- K1 known answer: inject shifts into the law's real rows, data = law at theta*, noiseless, fit with priors off. theta* all +-1 and each nuisance alone at +1.5. Recover to 0.25 sigma on every nuisance with information >= 1.
- K2 noise: 400 noisy injections with priors on; mean pull within 0.15 of expectation from shrinkage.
- K3 mock calibration: fraction of mock p below 0.05 from one further set of 2000 mocks in 0.05 +- 0.02.
- K4 BK2 candidate reproduces BK2's record.
- MUTATE twin, `WA1_MUTATE=1`: signs of all responses flipped. K1 must fail. Separate outputs.
- Byte-identical rerun of the final stage on its stored responses.
- One thread, nice 19, under 1 GB, small outputs. Other lanes read only. No downloads.
