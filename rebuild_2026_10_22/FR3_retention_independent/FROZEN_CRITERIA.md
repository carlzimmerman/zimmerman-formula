# FR3_retention_independent: FROZEN CRITERIA (committed alone; no f_gas from these tables read before this commit)

**Side question. It reinstates nothing.** The owner retired route E's cold sector (`../OWNER_DECISION_2026-11-01_RETIRE_COLD_SECTOR.md`); only the owner can change that. Galaxies aren't touched. The owner authorised the four small table fetches. kappa = 1/2 FITTED, unused. Cold dark energy, never a particle. No a0 in the cold sector. Not theory closed. Nothing here will say the data favour the framework.

**Not blind.** I've read FR1's README and lines, FR2's published-line table (Chiu, Bucko, Akino, Zhang, Siegel), and GS4. Before this commit the tables were downloaded and I read: VizieR column metadata; Okabe's text and the first few rows of Table E.1 (masses, no gas joined); Umetsu's table header, not joined. Computed before freezing, from X-COP only: g and tau below. No Y or f_gas from Okabe, Umetsu, HIFLUGCS or Chiu computed; no y value read. **HIFLUGCS on VizieR has no gas column** (seen in metadata), so its gas comes from elsewhere, below.

## Question
FR1's H and W lines differ by 0.2 dex at the mass of G-OUT-M3. One-method lensing masses with the keys' own gas: which, and does the resulting line change FR1's grade?
- H: lg Y500 = -0.121 + 0.219 (lg M500 - 14.5). W: -0.321 + 0.263 (lg M500 - 14.5). Y500 = 6.2715 Mgas500 / M500, gas only, h 0.70. Explicit coefficients, as FR1's `fr1_line.json`.

## A. Primary: Okabe+25 Table E.1 x eRASS1 MGAS500
Mass: M500_WL per cluster, h70, Om 0.3, no X-ray prior. Gas: eRASS1 `MGAS500` (the keys' gas, so this tests mass only, not gas). Join: name string against eRASS1 `NAME`. Sample: z <= 0.5 (WL bias grows above); the 3 misassociated clusters out; all clusters with a table value in, **poor-fit (flagged) clusters included**, since dropping them selects on WL signal. Unmeasured association clusters (3): excluded; sensitivity with M = 0. Sensitivity without poor-fit.

**Binning: never on WL mass.** Primary bin: eRASS1 lg MGAS500 12.75 to 13.58, the union of what H and W each imply for lg M500 14-14.5, cut before seeing any Y. Cross-check: the same number of clusters taken by rank in eRASS1 `CR500`, centred on the same median rank. eRASS1 `M500` is never used as the mass, only to set the aperture start (next).

**Estimator, Eddington treatment:** linear ratio of means, Y = 6.2715 Sum w Mg / Sum w M. Noise in M is about Gaussian in M, so mean M is unbiased where the mean of lg M isn't. Weights w = 1 / (median table error in that z bin)^2, z bins [0, 0.2), [0.2, 0.35), [0.35, 0.5]; depend on z, never on one cluster's measured M. x = lg of the weighted mean M. Median of lg Y per cluster reported, not used. Bootstrap 2000 clusters, seed 20261101.

**WL bias:** Okabe's mock calibration, eq. 17 and Table B.1, M500 column: ln(M_WL/1e14) = 0.079 + (0.965 - 0.258 F) ln(M_true/1e14) + 0.665 F, F = ln((1+z)/1.21). Inverted at the ensemble mean M and z. **Primary uses the corrected M**; raw reported. It's their mock with no LSS, adopted not derived; half the shift goes in the budget.

**Aperture:** MGAS500 is inside the catalogue's R500, M_WL inside its own. Ensemble correction, so WL noise doesn't enter radii per cluster: delta = (1/3) lg(<M> / <M500_cat>); Mg(R_WL) = Mg_cat 10^(g delta). **g = 1.05** = dln Mgas / dln R over 0.7-1.3 R500, X-COP median, measured (`rms 0.22`). X-COP is massive; g at this mass isn't measured. Bracket g 0.75, 1.35 in budget. Per-cluster aperture reported.

**Compared at the measured x:** D_H = lgY - H(x), D_W = lgY - W(x).
**Error budget, in quadrature, each printed:** bootstrap; aperture bracket; half the eq. 17 shift; selection term from the injected-line mock (below), |bias| as a systematic, not applied; shear + photo-z 0.015 dex (their residual uncertainty, order of magnitude, my judgement); GS4's gas ±0.017 not added (same gas as the keys, reported only). Gas in the keys doesn't move.

**Labels:** **H FAVOURED**: |D_H| <= 2 sigma_tot and |D_W| >= 3 sigma_tot. **W FAVOURED**: the mirror. Otherwise **UNDECIDED**, with tag [BETWEEN] if both |D| >= 2 sigma_tot. Reported, no label change: Akino at same x, HG cross-check (Y at the bin's mean gas against FR1's lg Y on gas line, conditional on gas).

## Other tables
- **Umetsu+20 x Eckert+16: tests W's anchor.** Paper says masses 1e14 Msun, h 0.7, Om 0.28 (unit read from the paper, by look-up), not corrected for bias. Gas: `Mgas500` in `_external_data/gs4/xxl100/xxl100gc.tsv`, inside r500MT. Same estimator, aperture (g) from the E16 M500MT, class 1 and 2, z <= 0.5, bin on E16 gas at lg Mg 12.75-13.58, no Eq. 17 (theirs: raw, ±5 % stated). Compare with FR1's XXL alone at x and H, W. Also M500MT row, and lg ratio <M500_U>/<E16 mass from r500MT> on the same clusters. Report: **W ANCHOR HOLDS** if within 2 sigma of FR1's XXL line and >= 3 sigma from H; **W ANCHOR FAILS** if >= 3 sigma above that line and within 2 sigma of H; else UNSETTLED.
- **HIFLUGCS: is H's slope a step between samples?** Mass: M500NFWFreeze, Chandra hydrostatic, one method (other extrapolations reported). Gas: no column there, so eRASS1 MGAS500 by position (6 arcmin, |dz| <= 0.02), western sky only, at per-cluster aperture (masses precise; g as above). Second reading with GS4's pointed gas rows. X-COP clusters removed by position. OLS lg Y on lg M, bootstrap. **NO STEP NEEDED** if |b - 0.219| <= 2 SE and SE <= 0.08; **STEP** if b + 2 SE < 0.219 with SE <= 0.08; otherwise NOT MEASURED. Y at 14.34 reported against H.
- **eFEDS, Chiu+22 x Bahar+22: report only.** Chiu varies cosmology on priors, Bahar freezes it, M comes from count rate, so Y vs M is partly built in. Same estimator, no label.

## Part B. Carry from R500 to R200 from y
ACT DR6.02 NILC strips at the sibling path, read only by memmap, no copy. ComptonY primary, CIB-deprojected reported. Sample: eRASS1 lg MGAS500 13.1-13.6, 0.05 <= z <= 0.30 (beam 1.6' must be well under R500), non-zero map to 5 R500. Catalogue R500 sets the scale only. Compensation: background annulus x = R/R500 in 4-5 per cluster. Annuli x edges 0, 0.5, 1, 1.523, 2, 3 (R200 = 1.523 R500 from M200/M500 = 1.41, FR1's M3). Stack: mean annulus y, unweighted, bootstrap clusters. Onion peel with constant pressure in shells, out to x = 3, gives Ysph(<1), Ysph(<1.523).

**T(r), stated:** Mg200/Mg500 = 1 + (Y200/Y500 - 1)/tau, tau = mass-weighted T in the shell over T inside R500. **tau = 0.77 ± 0.14** derived from X-COP's measured Mgas and M_NFW by hydrostatic balance (9-10 clusters, massive, HSE). So it assumes self-similar T(r) at this mass and hydrostatic balance, neither measured here. Isothermal tau = 1 reported as a bound. **Two-halo:** the 4-5 pedestal removes only a flat part. Rising correlated signal inside remains (RF4: unseparable), so **the result is biased high by an unmeasured amount**; compared with a stated no-pedestal row. Beam: injected Arnaud-shape mock on the same positions, recovered Y ratio applied as a correction, printed.
Stars ignored in carry: carry = lg(Mg200/Mg500) - lg 1.41.
**Labels:** **CARRY NEAR X-COP +0.031** / **CARRY NEAR FR1 +0.062**: within 1 sigma_tot of one and >= 2 sigma_tot from the other. Otherwise **UNDECIDED**. sigma_tot: bootstrap, tau ± 0.14, half the difference between map versions.

## Grade through FR1's path
FR1's `fr1_def.py` (read only), ZN3's worker, ZN4's shapes, gas +0.005, both f*, both h, own cache dir. Mode M only, so the carry row is well defined.

Line R, measured: lg Y = a + b (lg Mg - 13.5), fit on all eligible z <= 0.5 clusters by weighted least squares in linear M (w as above), with M-hat self-consistent per cluster in aperture (delta_i from M-hat, not the noisy M) and eq. 17. Mapped exactly to lg M500 form: b_M = b/(1-b), a_M = (a + 0.203 b)/(1-b), with 14.297 = 13.5 + lg 6.2715. Y is conditioned on gas, so WL noise sits in y.
- **R row, label row:** if SE(b) <= 0.10: the fit. Otherwise: anchored at the primary bin (a from the bin's point at its mean gas) with HG's b +0.1968 (FR1's, gas conditional). The other is reported as a row either way.
- R +-sigma_tot in anchor. R with Part B's carry (FR1's `carry` path); reported, not the label, unless sigma_tot(B) <= 0.031.

**Labels, FR1's rule with FR1's lines:** NO INDEPENDENT MEASUREMENT if sigma_tot at M3's mass > 0.04 or fewer than 15 eligible clusters with M-hat lg M500 < 14.3; else RETENTION CLOSES CLUSTERS / PARTLY / NOT RETENTION as FR1 frozen. Tags as FR1 for error dependence: [ERROR-DEPENDENT] if ±sigma_tot change label read on reach alone. Pass lines: 15 keys |Z| <= 2 on +0.005, both f*, both h; X-COP |mean| <= 0.05, rms <= 0.10. Z_tot and joint chi^2 by FR1's path.

Read-across to G13 and EM1, **report only**: line R as Y200 against EM1's line, as in FR1's table, inside 13.5-14.4.

## Checks (failed check: no verdict)
K1 FR1's H row reproduced through my driver with its line: per key pred, X-COP, |d| <= 1e-6, both f*. K2 parse: 78 rows in Okabe, 72 with mass, 76 of 78 ids match eRASS1 (FR2's count; mismatch stops); |dz| and position sane; catalogue M500 consistent with R500, Om 0.3 h 0.7, within 2 %; units of MGAS500 (1e11), M500 (1e13) by median fgas not read beyond a range check; Umetsu 136; HIFLUGCS 64; Chiu row count. K3 injected-line recovery: mock masses from H, then from W, with Gaussian table noise and scatter 0.10 dex in gas at fixed M on real gas, z, weights, 500 realisations: mean recovered D within 0.02 of input's; the bias printed goes in the budget. Separates H and W at the mock noise. K4 map geometry vs WCS as GH3, and injected y recovered within 10 %.

**MUTATE, separate output:** (a) bin on WL mass in place of gas: must shift primary lg Y by more than 0.02 in the expected low-at-low-mass direction, showing the Eddington treatment bites; (b) grader slope flip on R: X-COP must fail or M3 must move, as FR1.

## No knobs
No scans. g, tau, weights, bins, thresholds fixed here. Anything added later is labelled post-result.

## Expectation on record
Between H and W, near Akino: 55 % (FR2's). UNDECIDED 60 %, H FAVOURED 20 %, W FAVOURED 20 %. Grader label: NO INDEPENDENT MEASUREMENT 65 %, since the budget likely exceeds 0.04. Part B: UNDECIDED 75 %, two-halo dominant. HIFLUGCS: NOT MEASURED 50 %. Umetsu: W ANCHOR FAILS 45 %, UNSETTLED 45 %.

Downloads live in `data/`, gitignored, logged in `FETCH_LOG.md` with URL, date, size, hash. Parsed with own scripts under `python3 -I`. Nothing downloaded is executed.
