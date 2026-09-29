# CFG166 — Referee re-derivation of CFG164 (a measured PHIBSS gas prior for the KURVS discs, and the decision-cell verdict marginalised over it). FROZEN CRITERIA, PHASE 1

Written 2026-09-29 by the referee agent, BEFORE any script exists and before any gas ratio (Mmol/M*) has been computed or looked at.

**What I have read (and only this):** `CFG164_FROZEN_CRITERIA.md`, `CFG164_README.md`, `CFG165_kurvs_referee/README.md` (and, for the map's definition and one function signature, `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` lines 1-425), `CFG162_README.md`, a few lines of `CFG160_FROZEN_CRITERIA.md` (the verdict map), and the data-assembly README of `kmos3d_phibss`. I have NOT opened any CFG164 script, `.out` or `.json`, nor CFG160/162/163 scripts.

**What I have looked at in the data tables, sample-definition fields only (same as the CFG164 author did):** the flags, z_CO and M* columns of `phibss13_joined.csv`, and z and log M* of the ten KURVS discs. From these I confirmed by counting: 73 rows, **51 clean, 17 matched, 38 clean at z < 1.7**, and that all 38 clean z < 1.7 rows have log M* >= 10.40 while 8 of the 10 KURVS discs (log M* 9.55-10.24) lie below it (only KURVS-3 at 10.64 and KURVS-11 at 10.68 are above). No Mmol value, no gas ratio, no SFR was printed. The count check is therefore not blind; the gas numbers are.

**The README numbers below are TARGETS I read, not blind predictions.** My own labelled hand estimates (section 3) were made AFTER reading the README, and are disclosed as such. Nothing in this file may change after a result is seen; any later deviation goes in the README as a disclosed departure. Wrong expectations are kept.

---

## 1. What is re-derived, and where independence STOPS

**Re-derived from the frozen CFG164 text alone (my own code):**
- the clean set, the matched set, the 38-row set, mu_mol = Mmol/M* per row;
- the primary prior (empirical draw of PHIBSS rows per disc), Variant M (OLS in log mu vs log M*, scatter draw), Variant Z (declared (1+z)^2.5), the coherent lognormal systematics, the alpha_CO factor 0.8/4.36 and the HI factor (1+h);
- P1 (window fractions of the sample-median mu-bar), P2 (class probabilities at the placed s), P3 (KURVS-15 dust check), R0 (power width), H1 (the label), C1-C3;
- the Monte Carlo marginalisation.

**SHARED, NOT INDEPENDENT (stated, not hidden):**
1. **Data tables.** `data_assembly/kmos3d_phibss/phibss13_joined.csv` and `data_assembly/arxiv_tables/kurvs2023_*.csv`, `kurvs_sigma_profiles`, and the SPARC anchor files. I do not re-check them against Tacconi et al. 2013 or Kretschmer/Lelli (no network). C3 checks only internal arithmetic (fgas_recomputed = Mmol/(Mmol+M*)).
2. **The decision-cell map (CFG160/CFG165).** I REUSE the CFG165 referee's code (`CFG165_referee_kurvs_p4.py`, imported read-only as a module: `load_kurvs`, `load_sparc_anchor`, `per_object`, `cell`, `classify`, `spec`, `alpha_K`), which itself imports `CFG4_common` (nu_mono, the a0 constants). This is a SHARED element: it carries CFG160's map, the Kretschmer alpha(x) as quoted, the spherical thin-disc baryon surrogate, the error model, the anchor pooling, and the inclination-column definition. I will use `inc_col = "inc_star_deg"` (the column that reproduced CFG160 to four decimals in CFG165's diagnostic), so that C1 can be tested at 4 decimals. The CFG165 referee reproduced the CFG160 cell at that footing; I do not re-test the physics of the map. What this lane can and cannot test: it re-derives the PRIOR and the marginalisation; it does not test nu_mono, alpha(x), the pressure-support model, or that a disc with mu_i lies where the map says.
3. **CFG164's setup choices, reused as given (frozen in its criteria, attacked in section 6 where the repo's tables allow):** the windows z in [1.0, 1.7], log M* in [9.5, 10.8]; the systematics sigma_ln = ln 1.5 (Mmol, multiplying) and ln 1.3 (M*, dividing); the exponent 2.5; the alpha_CO factor 0.8/4.36; h in {0, 0.5, 1}; N = 4000 per prior, seed 164; the placed s = 1.00, 1.42, 1.62, 1.69, 3.00 (from CFG162, as s x K21's alpha; I do not re-derive the placement); the CFG162 windows rival [0.6, 1.7], flat [2.1, 3.7]; CFG163's dust limits 1.90 and 3.79 (taken as quoted numbers, not re-derived); gas disc scale 2 R_d (CFG165's default, `gas_scale = 2.0`), delta = 0, canonical footing.
4. **What I cannot re-derive:** PHIBSS-2/Tacconi+2018 (not in repo); HI at z ~ 1.5; a real per-disc gas measurement.

**Pinned interpretations (chosen NOW, from the frozen text; not tuned):**
- mu_i passed to the pipeline is the TOTAL gas/M* for disc i (gas = mu_i x KURVS M*_i, disc scale 2 R_d). `mu = mu_mol x (1+h)`.
- mu-bar in a draw = median of the ten per-disc mu_i.
- Draw for the primary prior: for each of N draws, (i) one Mmol factor exp(N(0, ln 1.5)) and one M* factor exp(N(0, ln 1.3)) shared by all ten discs; (ii) each of the ten discs independently picks one of the 17 rows uniformly with replacement; mu_i = mu_mol,row x Mmol-factor / M*-factor. The systematics are applied in EVERY variant (M, Z, alpha_CO, HI). alpha_CO and HI are deterministic multiplicative factors on the same draws (common random numbers).
- Variant M: OLS of log10 mu_mol on (log M* - 10.5), all 38 clean z < 1.7 rows; residual scatter = sqrt(RSS/(N-2)) (ddof = 2; the ddof = 0 value is reported); per-disc epsilon ~ N(0, scatter) in dex, independent per disc; mu_i = 10^(a + b(lm_i - 10.5) + eps) x systematics.
- Variant Z: draw a row j per disc as in the primary, multiply by [(1+z_i)/(1+z_CO,j)]^2.5.
- s = 3.00 is applied as `alpha x 3.0` in the P4 form (the frozen text says "as s x K21's alpha"); the true P2 spec at the same draws is reported as a diagnostic.
- The scaled alpha is applied to KURVS and to the SPARC anchor (same spec object), the natural reading; the anchor's sensitivity to this is <= 0.005 dex (CFG165 attack c).
- Classes exactly as `classify` (lean flat needs flat within 2 sigma AND rival < -2 sigma; lean rival needs rival within AND flat > +2 sigma; "both" = both within; else "neither"). The map is not label-symmetric (CFG165 M3).
- Window fractions use closed intervals: rival [0.6, 1.7], between (1.7, 2.1), flat [2.1, 3.7], below < 0.6, above > 3.7.
- Percentiles are of the 4000 (or 40000) draws, linear interpolation (numpy default).

## 2. Headline pinned (README targets, read, not blind)

| item | README target |
|---|---|
| counts | 73 rows; clean 51; matched 17; z < 1.7: 38 |
| primary (17 rows, h = 0) | sample-median mu-bar 1.01, 16-84%: 0.60-1.69 |
| P1 primary | 68% in rival window [0.6,1.7]; 7% in flat window [2.1,3.7] |
| R0 | 16-84% width of mu-bar 0.45 dex vs break-even separation 0.53 dex (0.62 vs 2.11 at s = 1) |
| P2 s = 1.00 primary | lean flat 0.21 / lean rival 0.55 / both 0.24 |
| P2 s = 1.42-1.69 primary | lean rival 0.70-0.81 (min and max over the three s) |
| h = 0.5 | median 1.57 (0.91-2.57); s = 1: 0.47 / 0.24 / 0.25; rival at s 1.42-1.69: 0.58-0.68 |
| h = 1 | median 2.05 (1.19-3.47); s = 1: 0.59 / 0.11 / 0.19; rival 0.37-0.52 |
| Variant M | slope -0.22, scatter 0.28 dex, N = 38; median 1.30 (0.75-2.26); s = 1: 0.37 / 0.32 / 0.29; rival 0.67-0.70 |
| Variant Z | median 1.31 (0.75-2.19); s = 1: 0.33 / 0.31 / 0.34; rival 0.65-0.71 |
| alpha_CO ULIRG-like | median 0.18 (0.11-0.31); s = 1: 0.00 / 1.00 / 0.00; rival 0.01-0.06 |
| s = 3 | mostly "neither" |
| X (spread) | P(lean rival, s = 1) spans 0.11-1.00 across variants; median mu spans 0.18-2.05 (1.0-2.05 without alpha_CO) |
| P3 KURVS-15 | median mu 1.00; 16% of the prior above 1.90; 53% at h = 1 |
| H1 | max class 0.55 < 0.68 -> NON-DIAGNOSTIC |
| C1 | mu = 0.67 for all discs gives +0.1441 / -0.0060 (4 decimals) |
| MUTATE 1 (mu x 4) | P(lean rival, s = 1) = 0.01 (< 0.32 required) |
| MUTATE 2 (mu x 0.25) | P(lean flat, s = 1) = 0.00 (< 0.05 required) |

(Sums: primary 1.00; h = 0.5 0.96; h = 1 0.89 (the rest "neither"); M 0.98; Z 0.98.)

## 3. Hand ESTIMATES (made AFTER reading the README; labelled) and reproduction probabilities

Estimates are what I expect to get, from the README's own structure. They are not blind.

- **Primary prior.** Row median mu_mol 1.0-1.05; row scatter (sd of log10 mu) 0.28 +/- 0.06. The width of mu-bar is dominated by the coherent systematics: 0.176 dex (Mmol) and 0.114 dex (M*) give 0.21 dex; the per-disc scatter averaged over ten discs and the median give ~0.11 dex; total ~0.24 dex, so 16-84% width ~0.48 dex (README 0.45). My run: median 1.01 +/- 0.04, 16-84% 0.60 +/- 0.04 to 1.69 +/- 0.08.
- **Class probabilities at s = 1, primary:** 0.55 +/- 0.03 rival, 0.21 +/- 0.03 flat, 0.24 +/- 0.03 both. Lean rival for effective mu below ~1.1, "both" between ~1.1 and ~1.4, lean flat above (from CFG165: lean flat at mu >= 1.2-1.5, with mu = 1.5 flat/rival at +1.25 sigma/-2.01 sigma).
- **Variant Z:** median 1.31 +/- 0.05 (1.01 x [2.5/2.25]^2.5 ~ 1.30, a consistency check on the README).
- **alpha_CO:** median 0.185 (1.01 x 0.8/4.36). The HI rows: 1.01 x 1.5 = 1.52 and 1.01 x 2 = 2.02; the README's 1.57 and 2.05 are 3.6% and 1.5% higher than the exact scalings of the primary median, larger than the ~1.1% median MC noise at N = 4000. I infer CFG164's h variants did NOT use common random numbers (different stream per prior). This is a hand inference from the README, labelled as such. It sets the tolerances below.
- **Variant M:** the fitted slope reproduces to -0.22 +/- 0.02 and scatter 0.28 +/- 0.01; a(10.5) ~ 1.05. Median 1.30 +/- 0.06.
- **KURVS-15 P3:** fraction above 1.90 is 0.17 +/- 0.04; fraction above 3.79: 0.00-0.02 (primary), 0.05-0.10 (h = 1). Not in the README, my estimate.
- **Slope significance (attack a):** se of the slope ~0.17 +/- 0.05, so |b|/se ~1.3 (range 0.8-2.0); permutation p (two-sided, |b_perm| >= 0.22) 0.2-0.4. I expect the mass trend to be UNDETERMINED in this sample (P = 0.70 that |b|/se < 2).
- **Slope grid, P(lean rival, s = 1), a(10.5) pinned:** b = +0.22: 0.68; 0: 0.52; -0.22: 0.32 (README); -0.44: 0.10; -0.66: 0.02 (each +/- 0.10 except the README row).
- **Kernel per-disc prior (width 0.3 dex):** effective sample size 3-8 rows for the lowest-mass discs; P(lean rival, s = 1) 0.40 +/- 0.15.
- **In-repo z exponent (attack b):** gamma in mu ~ (1+z)^gamma with a mass term, 51 clean rows: 2.5 +/- 1.5 (se ~1.3); P(|gamma - 2.5| <= 2 se) = 0.7.
- **Window grid (attack c):** P(lean rival is the modal class at s = 1 in >= 80% of windows with N >= 8) = 0.65. The upper mass edge (10.8) sits between rows at 10.78 and 10.82: the most sensitive edge; the z lower edge sits on the row at z = 1.00. Expected largest single-step move of P(lean rival): 0.10.
- **Marginalisation definition (attack d):** hyperprior-bootstrap (resample the 17 rows before drawing) moves any class probability by <= 0.04 (P = 0.8); lognormal fit by <= 0.05 (P = 0.75); a fully coherent one-row-per-draw prior widens: lean rival 0.50 +/- 0.06, lean flat 0.27 +/- 0.05, "both" falls to ~0.18.
- **Probability that my numbers REPRODUCE the README to the pass lines (section 4):** counts 0.97; primary median/16/84 0.85; primary class probs (three numbers) 0.70 jointly; P1 fractions 0.85; R0 0.90; C1 0.9 (given inc_star_deg; 0.05 chance of a 0.003 column offset); HI rows 0.65; alpha_CO row 0.90; Variant Z 0.6; Variant M 0.45 (most ambiguous: ddof, eps definition, whether systematics apply); s = 1.42-1.69 range 0.6; P3 0.6; H1 label 0.95; MUTATE 1 and 2 targets 0.95 each. All README rows jointly 0.15.

## 4. Pass lines (exact, frozen)

**Counts:** 73 / 51 / 17 / 38: exact, else FAIL.

**Monte Carlo protocol (pinned):** every README row is compared to TWO runs of mine: (i) "parity": N = 4000, seed 164 (numpy `default_rng(164)`, one generator per prior, drawn in the order: two systematic factors, then the ten-disc row indices); (ii) "converged": N = 40,000, seed 166. Reason: the MC noise of a class probability at N = 4000 is up to 0.008 and of a median up to ~1.1%; the README values carry that noise and I cannot reproduce their stream (unknown). The pass tests use the converged run against the README.

| quantity | pass line (converged run vs README) |
|---|---|
| median mu-bar | within 4% relative (min 0.03) |
| 16th and 84th percentiles | within 7% relative |
| P1 window fractions (rival 0.68, flat 0.07) | within 0.03 abs |
| R0 width in dex | within 0.03 dex |
| P2 class probabilities, primary, s = 1.00 (each of three) | within 0.03 abs |
| P2 rival range over s = 1.42/1.62/1.69, primary (min and max) | within 0.04 abs |
| P2 class probabilities, h = 0.5, h = 1, Z, M, alpha_CO rows | within 0.04 abs (the setup-ambiguous rows; the h and alpha_CO rows are deterministic rescalings of my primary draws, so any excess is a definition difference) |
| Variant M slope and scatter | slope within 0.02, scatter within 0.02 dex |
| P3 fractions above 1.90 (0.16, h = 1: 0.53) | within 0.04 abs |
| C1 (mu = 0.67) | +0.1441 and -0.0060 within 0.0005 |
| H1 label | NON-DIAGNOSTIC (max class < 0.68) |
| MUTATE 1, 2 targets (0.01, 0.00) | within 0.03 abs |
| parity run | reported; not a pass criterion, except that every class probability must lie within 4 x sqrt(p(1-p)/4000) + 0.01 of the converged value (consistency of the MC, not of the science) |

A quantity outside its line is a DISAGREEMENT, classified in the README by cause (definition / MC / physics), never repaired.

## 5. MUTATE controls (exit 1 = the control bites; each runs with `MUTATE=k`, saved to its own files)

Each flips a load-bearing cell. Bite thresholds are pinned here; a control that does not bite is kept.

- **M0a (CFG164's pinned control, replicated):** every mu x 4. Bites if P(lean rival, s = 1) < 0.32 (README: 0.01).
- **M0b:** every mu x 0.25. Bites if P(lean flat, s = 1) < 0.05 (README: 0.00).
- **M1 (matching window selects other rows):** z in [2.0, 2.5], log M* in [9.5, 11.5] (the 13 clean z ~ 2.2 rows), everything else as the primary. Bites if the total-variation distance between the M1 and the primary class-probability vector at s = 1 is >= 0.15. (Hand estimate: bites with P = 0.6; I do not know the sign, because the z ~ 2.2 rows are also more massive.)
- **M2 (molecular-only swapped for total gas with h = 1):** bites if P(lean rival, s = 1) < 0.25 AND P(lean flat, s = 1) > 0.45 (README: 0.11 / 0.59).
- **M3 (mass-scaling slope sign flipped):** Variant M with b = +0.22 instead of -0.22 (a(10.5) and scatter unchanged). Bites if P(lean rival, s = 1) exceeds the primary's by >= 0.08 (the opposite direction of the true Variant M, which lowers it from 0.55 to 0.32).
- **M4 (mu permuted against mass):** among the 38 z < 1.7 rows, permute mu against log M* 200 times (seed 166); refit b each time; for each permutation run Variant M at N = 2000 (seed 166). Bites if the median over permutations of P(lean rival, s = 1) is >= (primary - 0.06), i.e. the Variant M shift (0.55 to 0.32) is not reproduced by scrambled data. Also reported: the permutation two-sided p-value for |b| >= |b_hat|.
- **M5 (map labels swapped):** classify with Delta'_flat and Delta'_H interchanged, at the primary prior, s = 1. Bites if P(lean rival) < 0.05 (the map is not label-symmetric, CFG165 M3).
- **M6 (negative control, must NOT bite):** replace the systematics with a factor of 1 (sigma_ln = 0). It is reported informatively (the label under sigma_ln = 0 is recorded, whatever it is); it tests that the systematics, not the machinery, set the width. Pass: mu-bar width falls to <= 0.20 dex; exit 0 either way, recorded.

Exit convention for the whole set: main exits 0 iff C1-C3 and the count checks pass; MUTATE=k exits 1 iff the control bites (M6 always 0).

## 6. ATTACKS (frozen procedures; each has a pass/fail meaning)

All attacks: primary prior unless said; s = 1.00 and s = 1.62; h = 0; N = 4000 at seed 166 (converged N = 40,000 at s = 1 for the headline of each attack); classes and pipeline as section 1. Attacks are labelled sensitivity grids; the headline stays the primary prior at s = 1.

### (a) The PHIBSS-to-KURVS matching rule: does the low-mass extrapolation drive the prior?
Facts (counted, sample fields only): every clean z < 1.7 row has log M* >= 10.40; only KURVS-3 and KURVS-11 exceed it.
- **a0. Vacuity check:** "rows with log M* >= 10.40" restricts the primary 17 to the same 17, so it is vacuous. It is reported as such, not as a test.
- **a1. Split of the 17:** rows above vs below the median log M* of the 17; mu medians and class probabilities of each half; Spearman rho(mu, log M*) for the 17 and the 38.
- **a2. Slope grid:** Variant M with b in {+0.22, 0, -0.11, -0.22 (fitted), -0.33, -0.44, -0.66}, a(10.5) and scatter fixed at the fit; P(class, s = 1 and 1.62) for each. Also b = b_hat +/- se.
- **a3. Slope significance:** OLS se of b, the t value, the bootstrap 16-84% of b (2000 row-resamples, seed 166), and the permutation p from M4.
- **a4. Parameter-uncertain Variant M+:** per draw, resample the 38 rows (bootstrap), refit (a, b, scatter), then draw as Variant M. This carries the slope's uncertainty into the extrapolation.
- **a5. Each disc at its own mass (kernel prior):** for disc i, draw row j among the 38 with weight exp(-(lm_i - lm_j)^2 / 2w^2), w in {0.2, 0.3, 0.5} dex; print each disc's effective sample size; use the primary systematics. The lowest-mass discs collapse onto the 10.40-10.48 rows; that is the point.
- **Pass/fail meaning:** the prior is **EXTRAPOLATION-DRIVEN** if across b in [b_hat - se, b_hat + se] (or across the kernel widths) P(lean rival, s = 1) spans >= 0.20, or if Variant M+ moves any class by >= 0.10 from the primary. It is **EXTRAPOLATION-ROBUST** if all those moves are < 0.10. The mass trend is **UNDETERMINED** if |b|/se < 2 (my expectation), in which case NEITHER the primary (implicitly b = 0) nor Variant M (b = -0.22) is established, and the honest prior is the wider Variant M+. A finding that Variant M's shift (0.55 to 0.32) is within the slope's uncertainty is a valid result and does not contradict CFG164's "the matching matters".
- The literature's mass dependence of gas fractions and the metallicity-dependent alpha_CO (higher alpha_CO at low mass, i.e. the same direction as b < 0) are recalled from memory, are NOT in the repo, and are used only as a sanity comment on the sign, not as data.

### (b) Direction of each selection bias (expected sign; test where the repo allows)
1. **Stellar mass (expected: prior under-states KURVS gas):** tested in (a).
2. **Redshift (expected: under-states):** in-repo test: fit log10 mu = c + b (log M* - 10.5) + gamma log10(1+z) to the 51 clean rows (z 1.0-2.43); report gamma +/- se and b. Meaning: Variant Z's declared 2.5 is CONSISTENT if |gamma - 2.5| <= 2 se_gamma; the fit is confounded (the z ~ 2.2 rows are more massive) and is labelled so. Also the ratio [(1+z_i)/(1+z_CO,j)]^2.5 median over the draws (expected ~1.30).
3. **CO detection (expected: over-states):** the six upper limits and the three inconsistent rows all have NaN z_CO or z > 2 (checked: 5 of the 6 upper limits have NaN z; BX528 z = 2.268), so none falls in the z window: the detection bias CANNOT be tested from the repo's matched rows. Report the inventory (name, z, log M*) and state that CFG164's "not corrected" is a bound-free omission. Bounding run: add the 4 flagged rows with log M* in [9.5, 10.8] and NaN z (MD66 10.59, BX389 10.61, PEP-J123712 10.62, PEP-J123759 10.58) at mu = 0 (limit) or at the tabulated upper-limit value / quoted-fgas value, to size the maximum effect of the omission on the median and the classes. Labelled a bound, not an estimate: their redshifts are unknown here.
4. **SFR selection (expected sign of the mu-sSFR correlation: positive):** in-repo test: sSFR = SFR/M* for the 17 matched rows (PHIBSS `sfr_msun_yr`) and for the ten KURVS discs (integrated table `sfr_msun_yr`, log M*). Report both sSFR medians (different SFR tracers: IR/UV vs H-alpha, so a level offset is confounded and only flagged), the partial slope of log mu on log sSFR in the 51 clean rows (with the mass and z terms), and a reweighted prior (each KURVS disc draws rows with a Gaussian kernel of width 0.3 dex in log sSFR). Meaning: sSFR-INSENSITIVE if the reweighted median mu is within a factor 1.25 of the primary's; otherwise the selection difference is a named driver and its sign is reported.
5. **alpha_CO:** the two brackets are frozen by CFG164. Additional declared toy, labelled as such: a mass-dependent alpha_CO multiplier 10^(0.3 (10.5 - log M*_i)) applied per KURVS disc (a metallicity-like trend, no repo data behind it); it is the same lever as a2. Pass/fail meaning: report only; the toy's amplitude is a guess.
- **Frozen reading:** the OVER-statement (CO detection) is not correctable here, so the sum of the stated directions is not determinable; I report which direction each test pointed and do not net them.

### (c) Were the window edges (z in [1.0, 1.7], log M* in [9.5, 10.8]) tuned?
Counted fact: gap between rows at z = 1.53 and 2.01 (any z_hi in [1.53, 2.0] is identical); all 38 rows at z < 1.7 have log M* >= 10.40 (any log M* lower edge <= 10.40 is identical); the z lower edge sits on the z = 1.00 row; the upper mass edge 10.8 sits between rows at 10.78 and 10.82.
- **Pre-declared grid:** z_lo in {0.95, 1.00, 1.05, 1.10, 1.20, 1.30}; z_hi in {1.6, 1.7, 2.5}; log M*_lo in {9.5, 10.45, 10.60}; log M*_hi in {10.70, 10.75, 10.80, 10.85, 10.90, 11.00, 11.30}. Full factorial (378 windows), each with N = 4000 (common seed 166); windows with fewer than 8 rows are listed and skipped. Report: N_rows, median mu_row, P(class, s = 1) per window; the table of P(lean rival) over (z_lo, log M*_hi) at the frozen log M*_lo and z_hi; and the largest single-step move of each class per edge.
- **Pass line:** the headline is **NOT TUNED** if (i) lean rival is the modal class at s = 1 in >= 80% of the windows with N >= 8, AND (ii) every window that shares >= 12 rows with the frozen 17 has |P(lean rival) - 0.55| <= 0.12. Otherwise the headline depends on the window and CFG164's 17-row prior is not stable to its own edges, an outcome I will report as such. If P(lean rival) >= 0.68 in >= 20% of windows the frozen H1 label (NON-DIAGNOSTIC) is edge-dependent.

### (d) How the marginalisation is defined and whether the answer depends on it
Compare at s = 1, h = 0, N = 40,000, seed 166:
1. **Frozen:** empirical rows, per-disc independent, coherent systematics.
2. **Hyperprior bootstrap:** resample the 17 rows (with replacement) once per draw, then draw the discs from that resample (carries the finite-N uncertainty of the prior itself).
3. **Lognormal fit:** log10 mu ~ N(mean, sd) of the 17 rows, discs independent.
4. **Coherent one-row-per-draw:** all ten discs share the same row (the sample-level mu is one PHIBSS-like galaxy; the extreme of population coherence).
5. **Per-disc scatter off:** each disc takes the row median exactly, only the coherent systematics remain (isolates what the systematics alone give).
6. **Systematics off:** the intrinsic per-disc scatter only.
7. **Decision statistic at mu-bar:** class of a constant mu = mu-bar draw (all discs the same, from item 1's mu-bar), to test whether the per-disc pipeline differs from the sample-median summary.
- **Pass/fail meaning:** the answer is **DEFINITION-ROBUST** if items 1-3 agree to <= 0.05 abs in every class and 4-7 keep the modal class. It is **DEFINITION-DEPENDENT** if items 1-3 differ by >= 0.05 or the modal class changes; the frozen H1 label is then partly a product of the sampling rule. Independent of the number, the width of the prior (0.45 dex) is set mostly by the two frozen systematics, not by the PHIBSS rows (item 5 vs 6); this is reported. Also reported: the class of the hard boundaries, e.g. lean rival vs "both" edge in mu (a scan of the class at constant mu = 0.5, 0.75, 1.0, 1.25, 1.5, 2, 3 at s = 1), so the reader can see which mu-bar values the probabilities integrate over.

### (e) Extras (reported, not pass/fail)
- inc_sfr_deg vs inc_star_deg: the primary uses inc_star_deg; the class probabilities with inc_sfr_deg are reported (expected shift <= 0.02).
- the true P2 spec vs alpha x 3.0 at s = 3.
- alpha_K scale applied to the anchor or not (expected <= 0.005 dex).
- ddof = 0 vs 2 scatter in Variant M.

## 7. Script plan (nothing written in phase 1)

Scratch dir `.../scratchpad/cfg166/`; the repo untouched; no network; no absolute home path printed (`ZF_REPO` env var or walk up from `__file__`; the scripts print `<repo>`). Seeds fixed (164 parity, 166 all else); numpy only.
- `CFG166_gas_prior_referee.py`: main and `MUTATE=0a,0b,1,2,3,4,5,6`; imports the CFG165 referee module read-only (SHARED); computes counts, C1-C3, R0, P1, P2 at the five s values for the six priors (parity N = 4000 seed 164; converged N = 40,000 seed 166), P3, H1, then the pass-line comparison table. Outputs `CFG166_main.out`, `CFG166_main_results.json`, `CFG166_MUTATE_<k>.out/_results.json`. Exit 0 iff C1-C3 and counts pass; MUTATE exits 1 iff it bites.
- `CFG166_attacks_abcd.py`: attacks (a), (b), (c), (d), (e) as in section 6. Outputs `CFG166_attacks.out/_results.json`. Exit 0.
- `CFG166_manifest.py` (or a shell one-liner): sha256 of the inputs, scripts, outputs.
- Runtime: main ~1-3 min (40,000-draw runs for six priors x five s values on a per-draw pipeline; the run switches to a vectorised pooling if slower); attacks ~5-10 min (378 windows at N = 4000 plus the permutations at N = 2000); target under ~15 min per run. If a run would exceed it, N drops to 10,000 for the converged run and this is disclosed; the pass lines then use the wider MC term.
- Order of work in phase 2: my scripts written from THIS file alone -> main, MUTATE 0a-6, attacks run and saved -> ONLY THEN the CFG164 script, `.out` and `.json` opened -> a post-comparison diagnostics script (clearly labelled post-comparison, outside the frozen main).

## 8. What would count as disagreement (a valid result)

- Any table row outside its pass line (section 4), classified by cause: **definition** (ddof, eps, systematics-in-variants, RNG stream, inc column, anchor scale), **MC** (within the noise bound), **physics**.
- A count other than 51 / 17 / 38 (already confirmed by the sample-field count).
- The frozen H1 label reversing (a class >= 0.68 at s = 1 in my converged run, or a different label because the modal class changes).
- Attack outcomes that contradict the README's wording: (a) EXTRAPOLATION-ROBUST where CFG164 says the matching matters; (a) the slope UNDETERMINED (|b|/se < 2), which would mean Variant M's "even split" is not a measurement of a mass trend; (c) windows NOT robust; (d) DEFINITION-DEPENDENT; (b) the in-repo gamma inconsistent with 2.5.
- A control that fails to bite (kept); an estimate in section 3 that is wrong (kept, scored in the README).
- Not a disagreement: the physics of the map itself, which I share and do not test.

## 9. Standing rules for the write-up

kappa = 1/2 is FITTED; the flat a0(z) is the framework's distinctive law, a0 proportional to H(z) the rival; nothing here says the data favour either model or the framework; a lean is not a detection; the result concerns the GAS PRIOR conditional on the selection, not an a0 verdict; failed controls and wrong expectations are kept, never repaired.
