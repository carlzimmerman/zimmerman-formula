# CFG166 — Referee re-derivation of CFG164 (a measured PHIBSS gas prior for the KURVS discs, and the decision-cell verdict marginalised over it)

- **Criteria:** `CFG166_FROZEN_CRITERIA.md` (committed eb98ed086, sha256 ad6826d6...) before any script existed. The README numbers in it are TARGETS I read; my hand estimates were made after reading the CFG164 README and are disclosed as such.
- **Order of work:** my scripts written from the frozen text alone -> main (parity N = 4000 seed 164; converged N = 40,000 seed 166), MUTATE 0a-6 and attacks (a)-(e) all run and saved -> ONLY THEN the CFG164 script and results JSON opened -> `CFG166_post_comparison.py` written after that (post-comparison, not part of the frozen main).
- **Repo untouched. No network. No absolute home path in any output** (`<repo>` is printed).

## Bottom line

**REPRODUCES, on every pass line (57 of 57 rows, all four counts exact, C1-C3 pass, H1 label NON-DIAGNOSTIC).** My converged run of the primary prior gives the sample-median mu 1.03 (16-84%: 0.60-1.72); at s = 1 lean flat / lean rival / both = 0.21 / 0.54 / 0.245 (CFG164: 0.21 / 0.55 / 0.24). Across all six priors, five s values and four classes, the largest class-probability difference to CFG164's committed JSON is 0.018, which is the size of the Monte Carlo noise of their N = 4000. Both MUTATE controls of CFG164 are replicated.

**Answers to the two questions asked:**
1. **Does the extrapolation to lower mass drive the prior? Partly: it drives the SHIFT, not the primary, and the slope behind it is weak.** All 38 clean z < 1.7 PHIBSS rows lie at log M* >= 10.40, and 8 of 10 KURVS discs lie below. Taking the fitted slope (b = -0.22 +/- 0.20, t = -1.1, permutation p = 0.28) and extrapolating moves P(lean rival, s = 1) from 0.54 to 0.32 (0.34 if the slope's uncertainty is carried, "M+"), so by the frozen rule the prior is **EXTRAPOLATION-DRIVEN** (the span across b = b_hat +/- se is 0.202 against a 0.20 line: borderline). But a prior taken from the rows nearest each disc's own mass (kernel, ESS 4-37 rows) gives 0.52-0.55, no shift. So the mass trend is UNDETERMINED in this sample: CFG164's "matching matters" is a conditional statement about an unmeasured slope, and the honest prior is the wider Variant M+ (width 0.52 dex), not either the primary or Variant M alone.
2. **Were the window edges tuned? Not in a way that picks a class, but the frozen line FAILS.** Lean rival is the modal class in 97% of the 317 windows with >= 8 rows; P(lean rival) >= 0.68 in 1.3%; any single-edge step moves a class by <= 0.094. The frozen pass line (ii) (windows sharing >= 12 rows with the 17 must stay within +/-0.12 of 0.55) is missed by 5 of 105 windows, worst 0.199, and ALL five are windows with z_hi = 2.5 that add three z ~ 2.2 rows while dropping high-mass ones; among the 70 windows with z_hi <= 1.7 the largest deviation is 0.106 (post-hoc breakdown, labelled). The frozen verdict is therefore "NOT STABLE to its own edges", kept as such.

Nothing here says the data favour either law or the framework; kappa = 1/2 and Omega_c h^2 stay fitted; a lean is not a detection. The result concerns the gas prior conditional on the PHIBSS selection.

## 1. Table vs CFG164, row by row (converged run N = 40,000, seed 166 vs CFG164's committed JSON; parity run N = 4000, seed 164 in the last column)

Pass lines as frozen (converged run vs the README target). "Theirs" = CFG164's committed `_results.json`, read after my runs; the README target is the same to rounding.

| row | CFG164 | mine (converged) | parity (N = 4000, seed 164) | pass line | verdict |
|---|---|---|---|---|---|
| counts: all / clean / matched / z < 1.7 | 73 / 51 / 17 / 38 | 73 / 51 / 17 / 38 | | exact | **REPRODUCES** |
| C1 (mu = 0.67 for all discs) | +0.1441 / -0.0060 | +0.1441 / -0.0060 | | 0.0005 | **REPRODUCES** (inc_star_deg) |
| C3 fgas identity | exact | 0.0 | | 1e-6 | **REPRODUCES** |
| primary: median (16-84%) mu-bar | 1.01 (0.60-1.69) | 1.025 (0.604-1.719) | 1.040 (0.615-1.711) | 4% / 7% | **REPRODUCES** |
| P1 primary: rival / flat window | 0.68 / 0.07 | 0.677 / 0.076 | 0.690 / 0.075 | 0.03 | **REPRODUCES** |
| R0 width (dex) vs 0.53 | 0.45 | 0.454 | 0.444 | 0.03 | **REPRODUCES** |
| primary s = 1: lean flat / rival / both | 0.21 / 0.55 / 0.24 | 0.210 / 0.540 / 0.245 | 0.207 / 0.541 / 0.247 | 0.03 | **REPRODUCES** |
| primary rival at s = 1.42 / 1.62 / 1.69 | 0.70-0.81 | 0.804 / 0.743 / 0.703 | 0.809 / 0.750 / 0.712 | 0.04 (min, max) | **REPRODUCES** |
| h = 0.5: median (16-84%) | 1.57 (0.91-2.57) | 1.538 (0.906-2.579) | 1.560 | 4% / 7% | **REPRODUCES** |
| h = 0.5, s = 1 | 0.47 / 0.24 / 0.25 | 0.453 / 0.249 / 0.259 | 0.458 / 0.237 / 0.265 | 0.04 | **REPRODUCES**; rival 0.588-0.684 vs 0.58-0.68 |
| h = 1: median (16-84%) | 2.05 (1.19-3.47) | 2.050 (1.208-3.438) | 2.080 | 4% / 7% | **REPRODUCES** |
| h = 1, s = 1 | 0.59 / 0.11 / 0.19 | 0.589 / 0.108 / 0.192 | 0.589 / 0.109 / 0.187 | 0.04 | **REPRODUCES**; rival 0.376-0.518 vs 0.37-0.52 |
| Variant M: slope, scatter (ddof 2) | -0.22, 0.28 | -0.219, 0.277 | | 0.02 | **REPRODUCES** (a(10.5) = 1.058) |
| Variant M: median (16-84%) | 1.30 (0.75-2.26) | 1.314 (0.766-2.243) | 1.325 | 4% / 7% | **REPRODUCES** |
| Variant M, s = 1 | 0.37 / 0.32 / 0.29 | 0.376 / 0.319 / 0.281 | 0.386 / 0.312 / 0.276 | 0.04 | **REPRODUCES**; rival 0.659-0.703 vs 0.67-0.70 |
| Variant Z: median (16-84%) | 1.31 (0.75-2.19) | 1.301 (0.763-2.208) | 1.312 | 4% / 7% | **REPRODUCES** |
| Variant Z, s = 1 | 0.33 / 0.31 / 0.34 | 0.328 / 0.306 / 0.351 | 0.336 / 0.295 / 0.352 | 0.04 | **REPRODUCES**; rival 0.648-0.708 vs 0.65-0.71 |
| alpha_CO ULIRG-like: median (16-84%) | 0.18 (0.11-0.31) | 0.188 (0.111-0.315) | 0.191 | 4% (floor 0.03) / 7% | **REPRODUCES** |
| alpha_CO ULIRG, s = 1 | 0.00 / 1.00 / 0.00 | 0.000 / 1.000 / 0.000 | same | 0.04 | **REPRODUCES**; rival 0.006-0.059 vs 0.01-0.06 |
| P3 KURVS-15: median mu; fraction > 1.90 (h = 0 / 1) | 1.00; 0.16 / 0.53 | 0.99; 0.166 / 0.524 | | 4%; 0.04 | **REPRODUCES**; fraction > 3.79: 0.024 (h = 0), 0.167 (h = 1) vs their JSON 0.021, 0.164 |
| H1 | NON-DIAGNOSTIC (0.55 < 0.68) | NON-DIAGNOSTIC (0.540) | NON-DIAGNOSTIC (0.541) | label | **REPRODUCES** |
| X (spread) | P(lean rival, s = 1) 0.11-1.00; median mu 0.18-2.05 | 0.108-1.000; 0.188-2.05 | | | **REPRODUCES** |
| s = 3 | mostly "neither" | primary 0.899 neither (alpha x 3.0); 0.851 with the true P2 spec | | | **REPRODUCES** |
| MUTATE 1 (mu x 4) | 0.01 | 0.004 (M0a) | | 0.03 | **REPRODUCES** |
| MUTATE 2 (mu x 0.25) | 0.00 | 0.000 (M0b) | | 0.03 | **REPRODUCES** |
| MC consistency, parity vs converged | | 0 inconsistent entries of 120 | | 4 sqrt(p(1-p)/4000) + 0.01 | pass |

The full 57-row pass table is in `CFG166_main.out`; also `CFG166_post_comparison.out` for their JSON row by row (windows per disc, all five s values).

**Every difference, classified.** All differences are smaller than or equal to the Monte Carlo noise of CFG164's N = 4000; no physics or definition difference remains.
- **Monte Carlo (the only source):** largest class probability difference 0.018 (h = 0.5, lean flat 0.472 theirs vs 0.453 mine converged; my parity run gives 0.458). CFG164's generator is a single `default_rng(164)` consumed sequentially across the six priors and drawn per draw in the order (two normals, ten integers); mine is a fresh generator per prior with vectorised blocks, so the streams differ. This is why CFG164's h rows are not exact rescalings of its primary (their h = 0.5 median 1.566 against 1.5 x 1.012 = 1.518): stream differences, not a definition difference. I had inferred this from the README before opening the script (hand estimate, section 5).
- **Definition:** none that matters. My inference from the frozen text (ddof = 2 for the Variant M scatter; epsilon per disc independent and in dex; systematics in every variant; alpha x s applied to the anchor too; s = 3 as alpha x 3.0; inc_star_deg) all match their script. (The ddof = 0 scatter and the true P2 spec at s = 3 are reported as extras and move nothing: 0.005 and 0.05 in one class at s = 3, "neither" 0.90 vs 0.85.)
- **Physics:** none. The shared map code (below) is the same object; the agreement is a check that the frozen text plus the data determine the numbers, not of the physics.
- **README typos in CFG164:** none found; every number in its README table is within rounding of its own JSON, and mine.

## 2. Where independence stops

- **Shared, not independent:** (i) the data tables (`phibss13_joined.csv`, the KURVS `kurvs2023_*` tables, the SPARC anchor files), not re-checked against Tacconi et al. 2013; (ii) the decision-cell map, CFG165's referee module imported read-only (`load_kurvs`, `load_sparc_anchor`, `cell`, `classify`, `spec`, `alpha_K`, and through it CFG4_common: nu_mono, a0). CFG165 in turn reproduced CFG160's cell. So the map, the Kretschmer alpha(x), the thin-disc baryon surrogate and the error model are shared; (iii) CFG164's setup choices (windows, systematics, the exponent 2.5, alpha_CO factor, h, N and seed, the placed s values, the CFG162 windows, CFG163's dust limits), reused as given and attacked in section 4 where the repo's tables allow.
- **Re-derived:** the clean/matched sets, mu per row, the four priors (primary, M, Z, brackets), the coherent systematics, P1, P2, P3, R0, H1, the marginalisation.
- **What this lane cannot say:** anything about nu_mono, alpha(x), pressure support, HI at z ~ 1.5 or the KURVS gas itself.

## 3. Controls (kept as they came)

Counts, C1, C3, C2b (all 38 rows have log M* >= 10.40; 8 of 10 KURVS discs below): 4/4 pass. MUTATE (exit 1 = the control bites; N = 10,000, seed 166, s = 1; primary at the same N is lean rival 0.538):

| MUTATE | what it does | result | frozen bite line | verdict |
|---|---|---|---|---|
| M0a | every mu x 4 | P(lean rival) 0.004 | < 0.32 | bites (exit 1) |
| M0b | every mu x 0.25 | P(lean flat) 0.000 | < 0.05 | bites (exit 1) |
| M1 | window z [2.0, 2.5], log M* [9.5, 11.5] (13 rows) | 0.206 / 0.469 / 0.320 (flat / rival / both); TV vs primary 0.078; row median mu 0.877 | TV >= 0.15 | **does NOT bite (exit 0)**. My estimate (P = 0.6 to bite) was wrong; the z ~ 2.2 PHIBSS rows are not gas-richer than the z ~ 1.2 rows in this table (see (b2)) |
| M2 | h = 1 | rival 0.104, flat 0.588 | rival < 0.25 and flat > 0.45 | bites (exit 1) |
| M3 | Variant M slope sign flipped (+0.22) | rival 0.531, flat 0.140, both 0.330 (true Variant M: 0.315 rival) | rival > primary + 0.08 | **does NOT bite (exit 0)**. My estimate (rival 0.68) was wrong: lowering mu does not raise "lean rival" past the plateau at ~0.54; the mass goes to "both" (0.33). The map is a plateau in mu below ~1.1, not a monotone ramp (see (d) scan) |
| M4 | mu permuted against mass (200 permutations) | median rival 0.550 (16-84%: 0.331-0.745); permutation p (|b| >= 0.219) = 0.285; median |b_perm| 0.141 | median >= primary - 0.06 | bites (exit 1): scrambled data do not reproduce Variant M's shift, but the spread 0.33-0.75 shows how little the slope constrains it |
| M5 | map labels swapped | rival 0.000 | < 0.05 | bites (exit 1); the map is not label-symmetric (as CFG165 M3) |
| M6 | systematics off (negative control) | width 0.175 dex (<= 0.20); flat 0.014 / rival 0.620 / both 0.366; NON-DIAGNOSTIC | informational, exit 0 | as expected: the two frozen systematics set the width |

## 4. Attacks (a)-(e), frozen procedures, results, and what they mean

### (a) Matching rule and low-mass extrapolation: EXTRAPOLATION-DRIVEN by the frozen rule (borderline); mass trend UNDETERMINED
- a0: "rows with log M* >= 10.40" is vacuous for the 17 (17 of 17).
- a1: the 17 split at log M* 10.61: low half (7 rows) row-median mu 1.18, high half (10 rows) 0.91; P(lean rival, s = 1) 0.53 vs 0.54. Spearman rho(mu, log M*) = -0.34 (17), -0.21 (38).
- a2: slope grid, P(lean rival, s = 1) [s = 1.62]: b = +0.22: 0.531 [0.733]; 0: 0.431 [0.732]; -0.11: 0.373; fit -0.219: 0.320 [0.705]; -0.33: 0.262; -0.44: 0.205; -0.66: 0.108 [0.510]. b_hat +/- se (-0.415, -0.023): 0.217 and 0.418; **span 0.202** against the frozen 0.20 line (mu-bar median 1.09-1.59). At s = 1.62 the lean rival stays 0.63-0.73 for b down to -0.44.
- a3: b_hat -0.219, se 0.196, t = -1.12, bootstrap 16-84% -0.40 to -0.05, permutation p 0.28. The slope is not established.
- a4: Variant M+ (rows resampled per draw): 0.363 / 0.338 / 0.259 (flat / rival / both), width 0.52 dex. M+ differs from M by <= 0.031 and from the primary by 0.202 in lean rival (flat +0.153).
- a5: kernel prior at each disc's own mass (w = 0.2, 0.3, 0.5 dex; ESS 3.8-37 rows, lowest-mass discs 3.8-7): P(lean rival, s = 1) 0.519, 0.529, 0.545; span 0.026. The kernel collapses onto the 10.40-10.5 rows, which behave like the primary.
- **Meaning:** by the frozen rule (span1 0.202 >= 0.20, M+ change 0.202 >= 0.10) the prior IS extrapolation-driven, but the driver is a linear slope at 1.1 sigma; the data alone (a1, a5) show at most a mild low-mass excess. CFG164's sentence "extrapolating the gas-mass relation to KURVS's lower masses splits it" is arithmetically right and conditional on that slope.

### (b) Selection biases (directions as stated; tested where the repo allows)
- **b2 redshift (expected: prior under-states gas):** the in-repo fit of log mu on log M* and log(1+z) over the 51 clean rows gives gamma = **+0.23 +/- 0.52** (z-only: +0.09 +/- 0.52); the declared 2.5 is **INCONSISTENT** with it (|gamma - 2.5| = 2.27 vs 2 se = 1.03). Variant Z's factor is 1.25 (median). **My estimate (gamma 2.5 +/- 1.5) was wrong.** The PHIBSS rows themselves show no redshift trend between z ~ 1.2 and z ~ 2.2 (mass confounded), consistent with M1 not biting. Variant Z's shift (median 1.01 to 1.30) thus rests on a declared exponent, not on these data.
- **b3 CO detection (expected: over-states):** none of the 6 upper limits and 3 inconsistent rows has a z_CO in the window (5 of 6 limits and all 3 PEP rows have NaN z; BX528 is at 2.27), so the bias CANNOT be tested from the matched rows. Bound (redshift unknown, 5 flagged rows with log M* in the window): adding them at their low bound lowers the median to 0.97 and gives rival 0.62; at the high bound 1.14 and rival 0.43 (from 0.54). It is a bound, not an estimate.
- **b4 SFR selection (expected: mu increases with sSFR):** beta = **+0.51 +/- 0.10** (51 rows, with mass and z terms): confirmed. KURVS sSFR median 2.35 per Gyr vs 1.81 for the matched rows (different tracers, level offset only flagged). sSFR-reweighted prior: median mu x1.02, P(lean rival) 0.536: **sSFR-INSENSITIVE**.
- **b5 alpha_CO(M*) toy** (10^(0.3(10.5 - log M*_i)), x0.88-x1.93, a guess with no repo data): median 1.36, lean flat 0.40 / rival 0.36 at s = 1; the same lever as a2; at s = 1.62 rival 0.74.
- Net direction: not determinable from the repo (detection over-states, mass and possibly alpha_CO under-state); I do not net them.

### (c) Window edges: frozen verdict NOT STABLE to its own edges (line (ii) fails); not tuned toward a class
- 378 windows; 61 skipped (< 8 rows); 317 evaluated (164 distinct row sets). (i) lean rival modal in 307/317 = **0.968** (pass >= 0.80). (ii) windows sharing >= 12 rows with the 17: 105; max |P(lean rival) - 0.55| = **0.199** (pass <= 0.12) at z [0.95, 2.5], log M* [9.5, 10.7]: FAIL. P(lean rival) >= 0.68 in 4/317 = 0.013 (H1 stable).
- Post-hoc breakdown (labelled): the 5 violating windows all have z_hi = 2.5 (they add three z ~ 2.2 rows and drop rows above 10.7 or 10.75); among the 70 windows with z_hi <= 1.7 the largest deviation is 0.106.
- Single-edge steps from the frozen window, largest change of a class: z_lo <= 0.048, z_hi 0.069, log M*_lo 0.018, log M*_hi 0.094 (P(lean rival) 0.44 at 10.70, 0.50 at 10.75, 0.54 at 10.80, 0.56 at 10.85). The upper mass edge, which sits between rows at 10.78 and 10.82, is the most sensitive; it moves the lean by 0.10 but never to another modal class.
- **Meaning:** no evidence the edges were chosen to produce a lean; the numbers depend on which rows are in by up to 0.10-0.20, more than the +/-0.008 Monte Carlo noise.

### (d) Marginalisation definition: DEFINITION-ROBUST
- s = 1, N = 40,000: frozen 0.210 / 0.540 / 0.245; hyperprior bootstrap 0.212 / 0.550 / 0.232 (max diff 0.013); lognormal fit 0.205 / 0.535 / 0.255 (0.010); coherent one-row-per-draw 0.252 / 0.588 / 0.127, width 0.59 dex; per-disc scatter off 0.273 / 0.539 / 0.179; systematics off 0.013 / 0.624 / 0.363; constant mu = mu-bar 0.243 / 0.590 / 0.158. Modal class lean rival in all.
- Width: 0.454 dex with both systematics, 0.420 with the systematics alone, 0.175 with the intrinsic scatter alone: **the two frozen systematics, not the PHIBSS rows, set the prior's width.**
- The map at constant mu, s = 1: lean rival for mu <= 1.0 (z_flat +2.38 at 1.0), "both" at 1.25, lean flat for mu >= 1.5. The primary's mu-bar median (1.03) sits ~10% below the lean-rival/both boundary, so 5% shifts of the median move P(lean rival) by ~0.05 (b = 0 in Variant M form has median 1.07 and gives 0.43). My post-hoc hypothesis, NOT tested: the pipeline's effective gas is mean-like (linear in mass), so per-disc scatter moves the boundary in median terms.

### (e) Extras
inc_sfr_deg: 0.192 / 0.547 / 0.256 vs inc_star 0.209 / 0.537 / 0.248 (shift <= 0.017). s = 3: true P2 spec 0.146 rival / 0.850 neither vs alpha x 3.0 0.098 / 0.899. Anchor scaled vs unscaled at s = 1.62: rival 0.756 vs 0.737, median |dz_flat| 0.06. Variant M with ddof 0 scatter (0.270): 0.371 / 0.325 / 0.284 vs ddof 2: 0.370 / 0.320 / 0.290.

## 5. Hand-estimate scorecard (frozen criteria section 3; wrong expectations kept)

| estimate | result |
|---|---|
| primary mu-bar median 1.01 +/- 0.04; 16-84% 0.60 +/- 0.04 to 1.69 +/- 0.08 | 1.025; 0.604 / 1.719 (in) |
| 17-row median 1.0-1.05; row scatter 0.28 +/- 0.06 | **1.10 (wrong)**; 0.22 (in) |
| width 0.48 dex vs README 0.45 | 0.454 (in) |
| classes at s = 1: 0.55 / 0.21 / 0.24 +/- 0.03 | 0.540 / 0.210 / 0.245 (in) |
| Variant Z median 1.31 +/- 0.05; alpha 0.185; HI 1.52 and 2.02 | 1.301; 0.188; 1.538 and 2.05 (in) |
| Variant M slope -0.22 +/- 0.02, scatter 0.28, a(10.5) 1.05; median 1.30 +/- 0.06 | -0.219, 0.277, 1.058; 1.314 (in) |
| README h medians not exact rescalings: different RNG streams | confirmed by their script (single generator, sequential) |
| KURVS-15 > 1.90: 0.17 +/- 0.04; > 3.79 (h = 0) 0.00-0.02 | 0.166 (in); 0.024 (just above) |
| slope se 0.17 +/- 0.05; |t| 0.8-2.0; permutation p 0.2-0.4; P(|t| < 2) = 0.70 | 0.196; 1.12; 0.28 (all in; undetermined confirmed) |
| slope grid P(lean rival, s = 1): +0.22: 0.68; 0: 0.52; -0.44: 0.10; -0.66: 0.02 (+/- 0.10) | **0.53 (wrong), 0.43 (edge), 0.205 (wrong), 0.108 (wrong)**: the response is flatter than I assumed; the map plateau |
| kernel P(lean rival) 0.40 +/- 0.15; ESS 3-8 for the lowest-mass discs | 0.529 (in); 3.8-7 (in) |
| in-repo gamma 2.5 +/- 1.5 (se 1.3) | **0.23 +/- 0.52 (wrong)** |
| window grid: lean rival modal >= 80% in 65% probability | passes (0.97), but the frozen line (ii) failed, which I had not weighted (estimated 0.65 for both lines) |
| largest single-step move 0.10 | 0.094 (in) |
| hyperprior <= 0.04, lognormal <= 0.05 | 0.013, 0.010 (in) |
| coherent variant: rival 0.50 +/- 0.06, flat 0.27 +/- 0.05, both ~0.18 | **rival 0.588 (wrong)**, flat 0.252 (in), both 0.127 (wrong) |
| MUTATE M1 bites with P = 0.6; M3 bites; M2, M4, M5, M0a/b bite; M6 width <= 0.20 | M1 and M3 did NOT bite (wrong); rest as expected |
| reproduction probabilities: primary class probs 0.70; Variant M 0.45; Z 0.6; all rows jointly 0.15 | all 57 reproduce (my probabilities were too low; the setup was pinned tightly enough) |

## 6. What would count as disagreement, and what I found

- **Any table row outside its pass line:** none.
- **Attack outcomes that contradict the CFG164 README's wording:** (i) its "the mass matching matters" holds only conditionally on a 1.1 sigma slope (a3), and a data-local prior does not shift (a5); (ii) Variant Z's exponent 2.5 is inconsistent with the PHIBSS rows' own z trend (gamma = 0.2 +/- 0.5), which the README does not test; (iii) the window edges: the frozen stability line fails for windows that add z ~ 2.2 rows.
- **Not a disagreement:** the physics of the map, shared and untested here.
- Failed controls and wrong estimates are in sections 3 and 5.

## 7. Files and re-run

Files (scratch dir; nothing in the repo): `CFG166_FROZEN_CRITERIA.md`, `README.md`, `CFG166_gas_prior_referee.py` (main and MUTATE), `CFG166_attacks_abcd.py`, `CFG166_post_comparison.py` (post-comparison), `run_all.sh`, `CFG166_main.out`/`_results.json`, `CFG166_MUTATE_{0a,0b,1,2,3,4,5,6}.out`/`_results.json`, `CFG166_attacks.out`/`_results.json`, `CFG166_post_comparison.out`, `CFG166_manifest.txt` (sha256 of inputs, scripts and outputs).

```
export ZF_REPO=<repo>
python3 CFG166_gas_prior_referee.py > CFG166_main.out                                    # rc 0, ~100 s
for k in 0a 0b 1 2 3 4 5 6; do MUTATE=$k python3 CFG166_gas_prior_referee.py > CFG166_MUTATE_$k.out; done   # rc 1 = bites (1 and 3: rc 0, do not bite; 6: rc 0 by design)
python3 CFG166_attacks_abcd.py > CFG166_attacks.out                                       # rc 0, ~90 s
python3 CFG166_post_comparison.py > CFG166_post_comparison.out                            # rc 0
```
(`./run_all.sh` does all of this; the whole set takes about 6 minutes.) The frozen criteria are `../CFG166_FROZEN_CRITERIA.md` (eb98ed086, sha256 ad6826d6...).

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

`./run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 0a, 0b, 2, 4, 5 exit 1 (bite); MUTATE 1 and 3 exit 0 (did not bite, kept); MUTATE 6 exit 0 by design; attacks 0; post-comparison 0. Every `.out` and `_results.json` is identical to the referee's. The frozen criteria are `../CFG166_FROZEN_CRITERIA.md` (eb98ed086). Independence stops at the data tables, the CFG165 map code (imported read-only) and CFG164's setup choices.
