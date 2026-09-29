# CFG168 — Referee re-derivation of CFG162 (KURVS a0(z) against the outer pressure-support strength s: the crossing, the break-evens, where the published prescriptions sit)

- **Criteria:** `CFG168_FROZEN_CRITERIA.md` (committed 7ab29fb78, sha256 cbbed519...), written before any script existed. Hand estimates in it were made after reading the CFG162 README and are disclosed as such; the CFG162 README numbers were targets I read, not blind predictions.
- **Order of work:** my own scripts written from the frozen text alone; main run, MUTATE M1-M7, attacks (a)-(c) with the scale scan (d1), and the mock test (d2, seeds 168 and 169) all run and saved; ONLY THEN CFG162's script, `.out` and `.json` opened; `cfg168_diag_postcomparison.py` written after that (labelled post-comparison, not part of the frozen main).
- **Repo untouched. No network. No absolute home path in any output** (`<repo>`, `<scratch>`).

## Answers to the three questions asked

1. **README break-evens (step-0.25 grid) versus root-finding: they are the same, and the README's wording is misleading.** CFG162's code (opened after my runs) brackets the sign change on a mu grid of step 0.25 in [0.25, 4] and then calls `brentq` inside the bracket, so its break-evens ARE continuous roots, as its frozen criteria said. My continuous roots (2.109 / 0.621 at s = 1) match its printed 2.109 / 0.621; even a naive linear interpolation on that grid gives 2.111 / 0.625, so the grid cannot matter above 0.004. The 2.14 / 0.65 of my CFG165 came from a different inclination column (`inc_sfr_deg`): with it I get 2.138 / 0.648 (D1, post-comparison). The README sentence "root-found on a mu grid of step 0.25" describes the bracketing and reads as an approximation; it is not one. One real consequence of the bracket: it stops at mu = 4, so P2's flat break-even is printed as "> 4" while the true root is 6.85 (via s_eq) / 6.89 (P2 itself).
2. **"Every published prescription sits above s_mid at that gas level": holds, with two qualifications.** At mu = 0.67 the five prescriptions sit at 1.00 / 1.42 / 1.62 / 1.69 / 3.00 against s_mid = 0.669 (margins +0.33 to +2.33); the bootstrap probability that s_mid lies below each placement is 0.968 (K21) and 1.000 (the other four). It survives every placement variant (a): match on the rival (moves <= 0.011), mean-pressure-fraction axis, median alpha ratio, sigma_0, anchor correction off. Qualifications: (i) K21's own +-40 % band is 0.6-1.4 and its lower edge is BELOW s_mid = 0.669 (above s_h2 = 0.599), and 33 % of the ten-disc bootstrap resamples have s_mid < 0.6, so K21 as a band straddles the crossing; (ii) with R_e = 2 R_eff (CFG160's own variant) K21 at s = 1 falls to the flat side (s_mid = 1.058), the other four stay above by the ordering argument. The README's words "at that gas level" carry the rest: at mu = 1.5 K21 is below and at mu = 4 all but P2 are below (both reproduced).
3. **Omission of P2 from "flat at mu ~ 2.1-3.7": the omission is real and it matters.** The README's ranges "s = 1.0-1.7" leave out P2 (self-gravitating disc, s_eq = 3.00), which its own table lists as a placed prescription. With P2 included the flat break-even range is 2.1-6.9 (not 3.7) and the rival's is 0.6-3.8 (not 1.7). The README does print P2's row (rival 3.83, flat "> 4"), so nothing is hidden; but the summary sentence and the reading "flat break-even 2.1-3.7" understate the range the frozen list itself defines.

## Bottom line

**Every headline row of CFG162 REPRODUCES within the frozen pass lines, in all seven groups, and no difference needed a physics explanation.** With my declared conventions (`inc_star_deg`, R_e = R_eff, anchor pooled) I get s_mid = 0.669, s_f2 = 0.726, s_h2 = 0.599 (README 0.67 / 0.73 / 0.60; CFG162's own printout 0.6693 / 0.7257 / 0.5993, equal to four decimals), bootstrap 0.513-0.844, gas-bracket s_mid 0.444 / 1.108 / 2.387, break-evens 2.109 / 0.621, all five placements and their own cells.

**What did not survive the attacks** (the referee's value, not an arithmetic error):
1. **(a) FAILS by my frozen rule, for one reason.** The geometric-mean-ratio placement flips P3 to 0.000 because KURVS-3's P3 correction is exactly zero (its sigma^2 rises outward, so the measured-gradient term is capped at 0) and the geometric mean of a set containing 0 is 0. That is a metric artefact of my own frozen variant, not a physical flip: dropping the zero disc (post hoc, labelled) gives 1.632 (base 1.617). Every other variant keeps every non-K21 prescription above s_mid.
2. **(b) FAILS as frozen: the crossing is stable to inclination, sigma_anchor, anchor selection and mass/inclination error (all <= 0.026), but not to the gas-disc scale (1 R_d: +0.14; 3 R_d: -0.11), not to the anchor offset choice (median 0.064 instead of pooled 0.092: -0.105), and not to which discs are in the sample (jackknife range 0.203, max shift 0.125; my frozen line 0.085 was too tight for ten discs, kept).** The R_e-invariant pressure fraction at the crossing is stable: q_mid = 0.548-0.559 across R_e = 1.0 / 1.5 / 2 R_eff.
3. **(d) The crossing does not identify the law.** A flat-law world at (s, mu) = (1, 2.14) and a rival-law world at (1, 0.65) give the same s_mid distribution (median 0.574 vs 0.565), by construction. Under flat truth at unknown gas the crossing lands at 1.00 (N1) or 0.61 (N2) (medians) rather than above the true s.
4. **A velocity scale of 10-15 % moves s_mid from 0.67 to 0.91 or 1.03 (d1).** The crossing is a data-level quantity as sensitive to the V scale as to the pressure model.

Nothing here says the data favour either law or the framework; kappa = 1/2 and Omega_c h^2 stay fitted; a lean is not a detection.

## 1. Table vs CFG162, row by row (frozen pass lines; canonical footing, delta = 0 unless stated)

"CFG162" = the README (and, opened after my runs, the printed `.out`). Verdict per group: REPRODUCES = every row inside its line.

| group | row | CFG162 | mine | line | in |
|---|---|---|---|---|---|
| crossings | s_mid | 0.67 (out: 0.6693) | 0.6693 | 0.02 | yes |
| | s_f2 | 0.73 (0.7257) | 0.7257 | 0.02 | yes |
| | s_h2 | 0.60 (0.5993) | 0.5993 | 0.02 | yes |
| | bootstrap 16 / 84 % | 0.51 / 0.85 (0.509 / 0.853) | 0.513 / 0.844 (seed 169: 0.518 / 0.849) | 0.03 | yes |
| | alt footing s_mid | 0.66 | 0.662 | 0.02 | yes |
| **crossings: REPRODUCES 6/6** | | | | | |
| gas-bracket crossings | s_mid mu = 0.25 / 1.5 / 4 | 0.44 / 1.11 / 2.39 | 0.444 / 1.108 / 2.387 | 0.03 / 0.03 / 0.05 | yes x3 |
| **REPRODUCES 3/3** | (mu = 0.67: 0.669; s_f2, s_h2 also equal to 3 decimals at all four mu) | | | | |
| break-evens | s = 1 flat / rival | 2.11 / 0.62 | 2.109 / 0.621 | 0.03 | yes |
| | D&S flat / rival | 3.10 / 1.26 | 3.100 / 1.260 | 0.08 | yes |
| | P3 | 3.56 / 1.56 | 3.560 / 1.563 | 0.08 | yes |
| | Price | 3.73 / 1.67 | 3.726 / 1.674 | 0.08 | yes |
| | P2 rival / flat | 3.83 / "> 4" | 3.830 / 6.85 | 0.08 / >4 | yes |
| **break-evens: REPRODUCES 10/10** | (direct, prescription applied itself: 3.11/1.25, 3.58/1.56, 3.74/1.67, 6.89/3.83) | | | | |
| placements (s_eq) | D&S / P3 / Price / P2 | 1.42 / 1.62 / 1.69 / 3.00 | 1.422 / 1.617 / 1.688 / 3.001 | 0.03 / 0.03 / 0.03 / 0.10 | yes |
| | own cell z_flat / z_H and class, six rows | as README table | all within 0.1 sigma, classes identical | 0.3 sigma | yes |
| **placements: REPRODUCES 10/10** | | | | | |
| counts | s = 1: rival / flat | 14 / 6 | 14 / 6 | 1 cell | yes |
| | s = 0.5: rival / flat | 4 / 10 | 4 / 10 | 1 cell | yes |
| | s >= 2.5: no lean-flat cell | yes | yes (all 17 grid rows equal CFG162's printed rows) | exact | yes |
| **counts: REPRODUCES 3/3** | | | | | |
| power R0 | s = 0 / 1 / 2 / 4 | 2.5 / 3.4 / 3.1 / 2.6 (out: 2.47 / 3.39 / 3.07 / 2.55) | 2.53 / 3.41 / 3.09 / 2.59 (mean sigma) | 0.3 | yes |
| **power: REPRODUCES 4/4** | | | | | |
| ordering claims | O1 (mu = 0.67 all above), O2 (mu = 1.5 K21 below, others above), O3 (mu = 4 all but P2 below), min margin >= 0.03 | as README | all True; min margin 0.11 (K21 at mu = 1.5) | exact | yes |
| **ordering: REPRODUCES 4/4** | | | | | |
| controls | C1 rows (0.6 / 1.0 / 1.4), C3 (P2 cell +0.390 / +0.237) | README | 0.0003 / 0.0000 / 0.0003; 0.0002 | 0.005 | yes |

Every other README statement checked: "s_h2 < s < s_f2: both within 2 sigma" (yes), "flat disfavoured above s_f2" (yes), the full-grid counts at all 17 s values (identical to CFG162's printout, which I read only afterwards), the gas-axis break-evens, the placed-prescription list (none unplaced).

## 2. Every difference, classified

| difference | class | detail |
|---|---|---|
| bootstrap 0.513 / 0.844 (mine, seed 168) vs 0.509 / 0.853 (CFG162, seed 162) | Monte Carlo | my seed 169 gives 0.518 / 0.849; the seed-to-seed spread is 0.005; resamples without an s_h2 root: 2 of 2000 (mine, seed 168), 0 (seed 169), 0 (CFG162); I exclude them |
| R0 denominators | definition | CFG162 divides by "the larger error" (2.47 / 3.39 / 3.07 / 2.55); the frozen text did not say; I scored the mean sigma (0.04-0.06 different), all inside 0.3 |
| break-evens 2.11 / 0.62 (CFG162) vs 2.14 / 0.65 (my CFG165) | definition | inclination column: `inc_sfr_deg` (CFG165) 2.138 / 0.648 vs `inc_star_deg` 2.109 / 0.621 (D1) |
| README: "break-even root-found on a mu grid of step 0.25" | README wording | the code brackets on the grid and calls brentq; the answers are continuous roots; naive grid interpolation would differ by <= 0.004 |
| README: P2 flat break-even "> 4" | README wording / bracket limit | the bracket stops at 4; the root is 6.85-6.89 |
| README: MUTATE "velocities x 2" | README typo | the code multiplies by 10^0.3 (1.995) as frozen |
| MUTATE printout "placed published prescriptions ... lie above s_mid = nan" | script cosmetic | printed with s_mid = nan under MUTATE; no physics; the H1 failure is the informative one |
| CFG162 main exit 1 | as disclosed | from its own C2 (a wrong 3/(8y) next-order term in the frozen check; correct expansion y + 1/2 - 1/(8y)); mine derived in the frozen file before any run: alpha(50) = 50.4975485, diff 4.9e-5, PASS; not independent in that the README's post hoc statement had been read |
| README rounds s = 0.6 rival -0.0917 to -0.092 | rounding | |

No difference was classified as physics; the frozen rule found none.

## 3. Controls and MUTATE (all runs saved; exit 1 = bites)

My controls (main run exits 0): C1 alpha := 2R/R_d equals the shared module's P2 (1.1e-16); C2 Price alpha(50) vs y + 1/2 - 1/(8y) (diff 4.9e-5 < 2e-4) and -d ln K0/d ln y (3.6e-11); C3 CFG160 rows and CFG141's P2 cell (<= 0.0003); C4 Delta'_flat(s) strictly increasing on [0, 6] (so s_eq is unique); C5 ten IDs are the f_DM rows and x in 1.04-3.54; C6 grid-crossing vs brentq on the full sample (3e-12); C-d0 the vectorised mock analysis equals the shared module on the real data (2e-16).

| MUTATE | what | result | frozen expectation | verdict |
|---|---|---|---|---|
| M1 | v_last x 10^0.3 | Delta'_flat +0.470 / +0.552 / +0.730 at s = 0 / 1 / 4; no s_mid; exit 1 | no crossing | bites (CFG162's own MUTATE prints the same +0.470 at s = 0 and +0.552 at s = 1) |
| M2 | label swap in s_f2, s_h2 | s_mid 0.669 unchanged (label-symmetric); s_f2 1.634, s_h2 0.059; exit 1 | s_mid unchanged; s_f2 about 1.65; s_h2 about 0.03 | bites on the 2-sigma crossings, as predicted (s_h2 0.03 off; kept) |
| M3 | anchor offset removed | s_mid 0.329; exit 1 | 0.25 +-0.1 | bites; my estimate was 0.08 low (inside my own band) |
| M4 | mu = 1.5 | s_mid 1.108; exit 1 | 1.11 | bites |
| M5 | sigma_out permuted (seed 168) | s_mid 0.776 (+0.107); **bites, exit 1** | expected NOT to bite (p = 0.7) | **wrong expectation, kept.** Post hoc: 200 permutations give s_mid 16/50/84 = 0.657 / 0.698 / 0.741 and 69 % within 0.05, so the frozen seed sits in the upper tail; the per-galaxy pairing of sigma with V moves s_mid by about +0.03 on average (CFG165's M6 did not bite for the lean class) |
| M6 | (i) Price alpha := y; (ii) D&S sign flipped | (i) s_eq 1.541 vs 1.688; (ii) Delta'_flat NaN, "unplaced"; exit 1 | 1.55; no root | bites; (ii) is unplaced because V_c^2 goes negative for some disc (NaN), not because no root exists |
| M7 | grid interpolation (step 0.25) instead of brentq | 0.675 vs 0.669 (0.006) | within 0.02, exit 0 | does not bite, as expected |

## 4. The attacks

### (a) Placement variants — FAIL (frozen rule), one metric artefact; the order claims are robust
Base s_eq: K21 1.000, D&S 1.422, P3 1.617, Price 1.688, P2 3.001; s_mid 0.669.
- **A1 match on Delta'_H:** moves <= 0.011. **A2 mean pressure-fraction axis:** f = 0.82 (K21), 1.22, 1.46, 1.45, 2.66; placements 1.49 / 1.79 / 1.77 / 3.25 (moves 0.07-0.25; P2 moves 0.247, not > 0.3 as I estimated, wrong, kept). **A3 median alpha ratio:** 1.36 / 1.85 / 1.63 / 2.96. **A3 geometric mean:** P3 = 0.000 (zero-ratio disc, artefact; FAIL by the frozen rule). **A6 anchor correction off:** moves <= 0.03 (P2 0.09), s_mid 0.655. **A7 sigma_0 (grad2 = 0):** s_mid 0.777, moves <= 0.07 (P2 0.17). All keep every non-K21 prescription above s_mid.
- **A4 placement equivalence across the gas:** the direct Delta'_flat of each prescription equals the K21-at-s_eq one to <= 0.0012 at mu = 0.25, 0.67, 1.5, 4 (line 0.02, PASS). s_eq changes by <= 0.013 with mu. The direct sides against s_mid(mu) are the README's: mu = 1.5 K21 below, D&S/P3/Price/P2 above; mu = 4 D&S/P3/Price below, P2 above. Two edge class differences (Price at mu = 0.67 and P2 at mu = 4 sit at the 2-sigma edge) are z differences of < 0.1 sigma.
- **A5 R_e = 1.5 / 2 R_eff (both KURVS and anchor):** s_mid 0.857 / 1.058; s_eq of the four others move up by 0.4-1.9 (labels only); they stay above s_mid; K21 at s = 1 falls below at 2 R_eff (the known CFG160 row).
- **Axis normalisation, plainly:** because placement is by equality of Delta'_flat, the order against s_mid does not depend on the normalisation of s. The normalisation fixes only the numeric labels and K21's +-40 % band. The R_e-free measure, the mean pressure fraction, is 0.55 at the crossing and 0.82 / 1.22 / 1.46 / 1.45 / 2.66 for the five prescriptions.

### (b) Stability of the crossing — FAIL as frozen (s_mid at the decision cell, base 0.669)
inc_sfr -0.018; inclination error 3 / 8 deg -0.010 / +0.021; mass error 0.10 / 0.20 dex -0.008 / +0.011 (s_f2 -0.031 / +0.045); sigma_anchor 7 / 15 km/s -0.007 / +0.018; anchor correction off -0.014; anchor inc >= 45 -0.002; anchor logM >= 10 -0.012 (all within 0.05). **Over the line:** gas-disc scale 1 R_d +0.138, 3 R_d -0.109; anchor offset = median -0.105; jackknife 0.591-0.794 (range 0.203, max shift 0.125, line 0.085); R_e = 1.5 / 2 / 2 (KURVS only): +0.188 / +0.389 / +0.398 in s (q_mid 0.552 / 0.555 / 0.559, spread 2 %, PASS). Bootstrap with the anchor also resampled: 0.501 / 0.674 / 0.859 (fixed anchor 0.513 / 0.672 / 0.844). The frozen phrase "anchor uncorrected" was read as the anchor's own pressure correction switched off; the anchor offset removed altogether is M3.
Reading: the crossing is definition-stable in the ways CFG165 tested (inclination column, sigma_anchor, anchor sub-selection) but its position depends at the 0.1 level on the gas-disc scale, the anchor offset statistic and which discs are in.

### (c) The (s, mu) map — scope, no CFG162 claim contradicted
- **c1: the both-within-1-sigma region is empty.** Area fraction 0.0000; minimum over the map of max(|z_flat|, |z_H|) = 1.293 (at s = 2.40, mu = 4); the minimum separation (Delta'_flat - Delta'_H)/mean sigma is 2.24 (> 2 excludes R1 by the bound) and the maximum 3.45. None of the 24-cell grids has a cell with both within 1 sigma at any of the 17 s values.
- **c2: both within 2 sigma:** 5.6 % of the box (s in [0, 4] uniform, mu in [0.25, 4] uniform in ln mu; grid 0.05 x 60); s-extent 0.40-0.45 at mu = 0.25, 0.60-0.70 at 0.67, 1.05-1.20 at 1.5, 2.10-2.80 at 4 (it widens with gas).
- **c3: break-even curves** are nearly linear in s: mu_f = 0.35 (s = 0.25), 0.93, 1.52, 2.11 (s = 1), 3.28 (1.5), 4.46 (2), 6.85 (3), 9.28 (4); mu_h = none (s <= 0.5), 0.25 (s = 0.75), 0.62 (1), 1.38 (1.5), 2.17 (2), 3.83 (3), 5.59 (4); none at s = 0 (flat over-predicts for every mu >= 0.05).
- **c4:** the direct break-evens agree with the placed ones to <= 0.043 in mu (line 0.3, PASS); the README's range "flat 2.1-3.7, rival 0.6-1.7" is correct for K21 / D&S / P3 / Price and omits P2 (flat 6.89, rival 3.83).

### (d) What a null would have looked like
- **d1 scale scan of KURVS v_last:** x0.85 s_mid 1.030 (K21 non-diagnostic); x0.9 0.907; x1.0 0.669; x1.1 0.441; x1.26 0.019 (s_h2 gone); x1.5 and x1.995: no crossing (K21 non-diagnostic, both far high). So the crossing vanishes for a 26-50 % increase in V and moves out of the K21 band for a -15 % change.
- **d2 mocks** (real baryons, sigma_out, errors, anchor; N = 2000 per family; seeds 168 and 169). **A departure, disclosed:** my first run (v0, kept in `CFG168_null_v0_nooffset.*`) built the mock without the simplified pipeline's z = 0 offset (the anchor's +0.092 dex, which real data carry), so the analysis subtracted an offset the mock did not contain; a flat-truth ideal world then gave s_mid = 1.57, inconsistent with the observed offset. I added the offset (g x 10^0.092) to the mocks and reran (`CFG168_null.*`, primary). Both sets are reported here; the frozen test result is the same in both.

| family (seed 168) | s_mid 16/50/84 | P(s_mid >= 0.67) | P(s_mid > 1) | P(K21 lean rival) |
|---|---|---|---|---|
| ideal flat (mu = 0.67, s = 1) | 1.07 / 1.24 / 1.42 | 1.000 | 0.916 | 0.050 |
| ideal rival | 0.39 / 0.56 / 0.73 | 0.257 | 0.005 | 0.962 |
| N1 flat (mu median 1.0) | 0.73 / 1.00 / 1.29 | 0.886 | 0.492 | 0.331 |
| N1 rival | 0.26 / 0.45 / 0.72 | 0.132 | 0.018 | 0.695 |
| N2 flat (mu median 2.0) | 0.35 / 0.61 / 0.89 | 0.352 | 0.075 | 0.707 |
| N2 rival | 0.13 / 0.33 / 0.55 | 0.009 | 0.001 | 0.275 |
| flat at (1, 2.14) | 0.40 / 0.57 / 0.77 | 0.299 | 0.016 | 0.931 |
| rival at (1, 0.65) | 0.40 / 0.57 / 0.75 | 0.275 | 0.008 | 0.954 |

(v0 without the offset: ideal flat s_mid 1.40 / 1.57 / 1.76; N1 flat P(>= 0.67) 0.997, N1 rival 0.680; N2 flat 0.828; flat (1, 2.14) 0.85 / 1.03 / 1.22.)
- **Frozen test (d2), as frozen: NOT informative** (P(s_mid >= 0.67 | flat, N1) = 0.886 (v0 0.997), needing < 0.05; P(>= 0.67 | rival, N1) = 0.132 (v0 0.680), needing > 0.3). **The frozen test's direction was wrong:** I wrote it as if the observed s_mid = 0.67 should be lower under flat truth. The mocks show the reverse for a fixed true s: under flat truth s_mid tends to lie ABOVE the true s (ideal 1.24 for s = 1), under the rival BELOW it (0.56); the map's reading "flat preferred below s_mid" is a statement about the true s versus s_mid. A wrong expectation kept, not repaired. The informative reading of the same mocks: at s_true = 1, P(s_mid > 1 | flat) is 0.92 with the assumed gas, 0.49 (N1), 0.075 (N2) and 0.016 (flat at mu = 2.14); P(s_mid < 1 | rival) is 0.995 or higher in every family. **A flat world with more gas than the assumed 0.67 looks like a rival world on this map.**
- Seeds 168 vs 169: max difference of any tabulated fraction 0.035 (line 0.02, MISSED); with N = 2000 the sampling error of two fractions is about 0.016, so this is Monte Carlo noise (max over 56 fractions); kept.
- Post hoc, not frozen: a density ratio of the observed s_mid = 0.669 (rival / flat), by KDE: ideal 139, N1 0.90, N2 0.08 (with the gas anywhere near 1-2 M* the observed crossing carries no information; only with the gas fixed at 0.67 does it, and there it is 139).
- Floored fraction (V^2 < 0.25 % of V_c^2): 3-18 % in the offset mocks (17.7 % in the ideal flat), as in CFG165.

## 5. Hand-estimate scorecard (frozen criteria section 4; wrong expectations kept)

| estimate | result |
|---|---|
| s_mid 0.67 +-0.02; s_f2 0.73; s_h2 0.60; boot 0.51-0.85; alt 0.66; gas-bracket 0.44 / 1.11 / 2.39 | all in (0.669, 0.726, 0.599; 0.513-0.844; 0.662; 0.444 / 1.108 / 2.387) |
| break-evens flat 2.10 +-0.04, rival 0.63 +-0.03 | 2.109, 0.621 (in; the inclination-column shift I predicted is confirmed by D1) |
| placements and own cells | in; counts exact; R0 in; ordering all True; joint P = 0.15 realised |
| M2: s_f2 about 1.65, s_h2 about 0.03 | 1.634 (in), 0.059 (0.03 off) |
| M3: s_mid 0.25 +-0.1 | 0.329 (in, low by 0.08) |
| M5: does NOT bite (p = 0.7) | **wrong: bites at the frozen seed** (0.776); 200 permutations centre on 0.698 |
| M6(i): 1.55 | 1.541 (in) |
| (a) K21 falls below s_mid at R_e = 2 R_eff (p = 0.75) | yes (1.058) |
| (a) P2 moves > 0.3 under the mean-pressure-fraction axis (p = 0.65) | **wrong: 0.247** |
| (a) non-P2 move < 0.15 under Delta'_H matching | yes (<= 0.011; much smaller than I said) |
| (b) inc / sigma_anchor / anchor rules <= 0.05 (p = 0.85) | yes for inc, sigma, sub-selection; **the median-anchor rule (-0.105) I had lumped in and missed** |
| (b) gas scale 3 R_d moves > 0.05 (p = 0.6); jackknife > 0.10 (p = 0.65) | yes (-0.109); yes (0.125) |
| (b) q_mid across R_e within 15 % (p = 0.5) | **within 2 %: far tighter than I expected** |
| (c) R1 empty (0.97); min max|z| about 1.4; R2 about 8 % | empty; 1.29 (low end of my 1.25-1.7 band); 5.6 % (inside my 4-15 %) |
| (d) P(s_mid >= 0.67 | flat, N1) about 0.3-0.5 | **wrong: 0.886** (I conflated the observed s_mid with the truth); the on-curve worlds give the same s_mid (0.574 vs 0.565) as I said |

## 6. Where independence stops

Reused, not re-derived: `CFG165_referee_kurvs_p4.py` (my earlier referee module, imported read-only): data loaders (`load_kurvs`, `load_sparc_anchor`), the sigma_out routine and sigma profiles, `per_object`, `pool`, `classify`, `alpha_K` (K21 alpha(x) as quoted in CFG160/162; I did not read Kretschmer et al.), `spec`, `corr`, `gbar`, `slope`, and through it `CFG4_common.nu_mono`, A0, G. The Price, Dalcanton & Stilp, P2 and P3 formulae come from the CFG162 frozen text, not from the papers. New in this lane: the continuous-s curves and brentq crossings, the bootstrap, the gas-axis and break-even roots, the placement roots, the direct-vs-placed check, the four attacks, the vectorised mock. The agreement to 1e-4 after the inclination column is fixed shows that the frozen text, the data and the shared pipeline determine the numbers; it does not test the kernel, the K21 alpha, the prescription formulae, the spherical surrogate or the baryon model.

## 7. What would count as disagreement, and what I found

- Pass-line misses in the crossings, gas-bracket crossings, break-evens, placements: **none**. Class differences of a prescription's own cell: none. An ordering claim of the wrong sign at mu = 0.67, 1.5, 4: none.
- Valid disagreements with the README's wording: (1) the break-even description "root-found on a grid" (bracketing only); (2) the "2.1-3.7" summary omits P2 (2.1-6.9); (3) "every prescription above s_mid" is true at the central s_eq but K21's own band edge 0.6 is below it and under R_e = 2 R_eff K21 sits below; (4) "velocities x 2" is x 10^0.3. None changes a number.
- Not a disagreement, stated in advance: "a map, not a verdict" is confirmed by (d): the crossing cannot separate a flat world with more gas from a rival world with less.

## 8. Files and re-run

Scratch dir (nothing in the repo): `CFG168_FROZEN_CRITERIA.md`, `README.md`, `cfg168_common.py`, `cfg168_main.py`, `cfg168_attacks.py`, `cfg168_null.py`, `cfg168_diag_postcomparison.py`, `cfg168_null_v0_nooffset_as_run.py.txt` (the null script as first run, before the offset option), `run_all.sh`, `CFG168_main.out/_results.json`, `CFG168_MUTATE_{1..7}.out/_results.json`, `CFG168_attacks.out/_results.json`, `CFG168_null.out/_results.json`, `CFG168_null_v0_nooffset.out/_results.json`, `CFG168_diag_postcomparison.out`, `CFG168_boot_smid_seed168.npy`, `CFG168_manifest.txt` (sha256), `*.err` (warnings only; paths replaced by `<repo>`, `<scratch>`).

```
export ZF_REPO=<repo>
cd <scratch>            # the directory holding these scripts
bash run_all.sh          # main 0; MUTATE 1-6 exit 1 (bite), MUTATE 7 exit 0 (informational); attacks 0; null 0; null v0 0; diag 0. About 30 s in total.
```

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 1-6 exit 1 (bite); MUTATE 7 exit 0 (informational, does not bite); attacks, null, null-v0 and the post-comparison diagnostic exit 0. Every `.out`, `.err` and `_results.json` is identical to the referee's. The frozen criteria are `../CFG168_FROZEN_CRITERIA.md` (7ab29fb78). Independence stops at the imported CFG165 pipeline. `cfg168_null_v0_nooffset_as_run.py.txt` is the first mock run without the pipeline z = 0 offset, kept as run.

## Provenance note (append-only; reported by the calc chat in 27bcce5a4, with the data chat's digitisation in 5e8617c81; no verdict changes)

The KURVS outer velocity that every a0(z) lane read, `v_at_last_point_kms` (the paper's Table B1 column 3), is the authors' fitted exponential-disc MODEL evaluated at R_max, not a measured data point: the data chat's digitisation shows model(R_max)/sin i_SFR equals it to about 1% for all ten discs. This lane imports the same column through the CFG165 loader, so it reproduced its target as that lane ran it; the note changes what the column means, not what was reproduced. The calc chat re-runs the test with the measured markers as CFG189 (criteria frozen first). Recorded here as reported and not re-verified by this lane's author.
