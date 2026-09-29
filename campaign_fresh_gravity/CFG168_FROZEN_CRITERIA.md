# CFG168 — Referee re-derivation of CFG162 (KURVS a0(z) against the outer pressure-support strength s: the crossing, the break-evens, where the published prescriptions sit). FROZEN CRITERIA

Written 2026-09-29, phase 1, BEFORE any script of this lane exists or any number is computed. Referee lane in the CFG84-86 / CFG165 way.
Nothing below may change after a result is seen; any later deviation is a disclosed departure in the README.

## 0. Rules of this lane

- Repo is untouched. All files live in the scratch dir. No network, no new data. No absolute home path is printed by any script (`ZF_REPO` env var or walk up from `__file__`; scripts print `<repo>`).
- Read in phase 1 (and only these): `CFG162_FROZEN_CRITERIA.md` (9f098e8a8), `CFG162_README.md`, `CFG160_README.md`, `CFG140_README.md`, `CFG141_README.md`, `CFG165_kurvs_referee/README.md`; file names of data by `ls`.
- NOT opened in phase 1: `CFG162_pressure_axis.py`, its `.out`, `_results.json`, `_MUTATE*`. They are opened in phase 2 only AFTER my own main run and all MUTATE runs are saved. The figure `CFG162_pressure_gas_axes.png` is not needed and is not opened before the runs.
- **The README numbers below are TARGETS I read, not blind predictions.** They are pinned here so that agreement or disagreement is scored against a frozen line. The hand ESTIMATES in section 4 were made AFTER reading the README, the CFG160/141/140 READMEs and my own CFG165 README; that is disclosed and they carry no blindness.
- Standing: kappa = 1/2 FITTED (Z = kappa); flat a0(z) is the framework's distinctive law, a0 proportional to H(z) the rival; nothing here says the data favour either law or the framework; a lean is not a detection; failed controls and wrong expectations are kept, never repaired.

## 1. What is re-derived, and where independence STOPS

**Imported read-only, shared, NOT independent** (from `CFG165_kurvs_referee/`, my own earlier referee module `CFG165_referee_kurvs_p4.py`, imported as a module with `MUTATE` popped from the environment before import; I use my own env var `CFG168_MUTATE`):
- data loaders: `load_kurvs` (10 f_DM discs, `inc_col` argument), `load_sigma_profiles`/`sigma_out` (sigma_out routine), `load_sparc_anchor` (75-galaxy SPARC same-pipeline anchor);
- the pipeline pieces `gbar`, `gpred`, `slope`, `per_object`, `pool`, `anchor_pool`, `cell`, `classify`, `alpha_K` (K21 alpha(x) as quoted in CFG160/162: -0.146 x^2 + 1.204 x + 1.475, x clipped to [0,4]), constants `MUS`, `DELS`, `FOOTS`, `KURVS_IDS`, `DEC`;
- through it, `CFG4_common.nu_mono` (kernel) and the constants A0, G, MSUN, KPC.
So agreement shows that the frozen text plus the data plus this shared pipeline determine the numbers. It does NOT test: the kernel, the K21 alpha coefficients (I do not read Kretschmer et al.; no fetch), the physical formulae of Price+2022 / Dalcanton & Stilp 2010 (taken from the CFG162 frozen text, not from the papers), the spherical surrogate, the baryon model, the gas bracket.

**Re-derived by my own new code, independent of CFG162's script (which I have not opened):**
1. The continuous-s decision-cell curves Delta'_flat(s), Delta'_H(s) with sigma, via the spec key `scale=s` of the shared K21 correction.
2. The three crossings (s_mid, s_f2, s_h2) by my own brentq; the bootstrap (my own resampler, own seed 168, cross-check seed 169); the gas-bracket and footing recomputations.
3. The full-grid verdict counts (24 cells x s grid) by `classify`.
4. The gas axis at s = 1 (60 log-spaced points) and its break-evens; the break-evens at each placed s; and the direct break-evens with each prescription applied itself (not via its s_eq).
5. The prescriptions: Price (alpha = y K1(y)/K0(y), y = R/R_d, scipy `k0`,`k1`), Dalcanton & Stilp (alpha = 0.92 R/R_d), P3 (C = max(sigma^2 R/R_d - R d(sigma^2)/dR, 0), from the shared `grad2`), P2 (alpha = 2R/R_d), the placement roots s_eq, with the prescription also applied to the anchor.
6. The four attacks and the null/mock test of section 6.

**Declared conventions (each fixed here; each is a place where I may differ from CFG162; all are attack variants in section 6):**
- Primary inclination column: `inc_star_deg` (CFG140/160's; known from my CFG165 to give the 0.003 dex difference; using it is a declared choice made AFTER the CFG165 finding, not blind). `inc_sfr_deg` is attack (b).
- R_e (Kretschmer's) = R_eff of the paper for KURVS; for the SPARC anchor 1.68 R_disk (the CFG165 convention). R_e = 2 R_eff on both is an attack variant.
- R_d = R_eff/1.68 for KURVS (CFG140); SPARC R_disk for the anchor.
- Anchor for the prescriptions: sigma = 10 km/s constant, no gradient (P3's gradient term = 0 at the anchor), the same functional form as applied to KURVS, at the anchor's own R/R_d (or x).
- The anchor for the s-curve: the same s (frozen text). Anchor pooled with the flat law's pooled offset for both laws (CFG165 found this equivalent: z = 0, E = 1).
- Bootstrap resamples with no root in [0,4] are excluded from the percentiles and their fraction reported (if > 2 % it is disclosed and the percentiles are flagged).
- "delta" = log mass offset; "foot" = canonical / alt, as CFG160.

## 2. The headline, pinned to the README (targets, not blind)

At the decision cell (mu = 0.67, delta = 0, canonical footing):
- H1: **s_mid = 0.67** (bootstrap 16-84 %: 0.51-0.85), where Delta'_flat = -Delta'_H; flat preferred below, rival above.
- s_f2 = **0.73** (Delta'_flat = +2 sigma_flat); s_h2 = **0.60** (Delta'_H = -2 sigma_H).
- Gas bracket: s_mid = **0.44 / 0.67 / 1.11 / 2.39** at mu = 0.25 / 0.67 / 1.5 / 4. Alt footing: **0.66**.
- Break-evens at s = 1: flat **2.11**, rival **0.62** (README table, stated there as read from a mu grid of step 0.25; my CFG165 got 2.14 / 0.65 with `inc_sfr_deg` and continuous root-finding; the frozen CFG162 text says root-finding).
- Placement table (s_eq; own decision cell Delta'_flat/Delta'_H; break-even flat/rival): none 0 (-2.3 sigma/-4.6 sigma; -); K21 1.00 (+3.3/-0.1; 2.11/0.62); Dalcanton & Stilp 1.42 (+4.1/+1.2; 3.10/1.26); P3 1.62 (+3.5/+1.3; 3.56/1.56); Price 1.69 (+4.7/+1.9; 3.73/1.67); P2 3.00 (+6.0/+3.7, class "neither"; >4/3.83).
- Full-grid counts: s = 1: 14 lean rival, 6 lean flat (of 24); s = 0.5: 10 lean flat, 4 lean rival; s >= 2.5: no cell leans flat.
- Power R0 (Delta'_flat - Delta'_H)/sigma: 2.5, 3.4, 3.1, 2.6 at s = 0, 1, 2, 4.
- Bottom-line claims to test: "every published prescription sits above s_mid at mu = 0.67"; "at mu = 1.5 K21 is below and the others above (straddle)"; "at mu = 4 all but P2 below"; "for the published prescriptions the rival's break-even gas is 0.6-1.7 and flat's 2.1-3.7".
- Controls the README reports: C1 reproduces CFG160's rows (+0.1441/-0.0060 at s = 1; s = 0.6: +0.058/-0.092; s = 1.4: +0.211/+0.060); C3 P2 = CFG141 P2 cell (+0.390 +-0.065 / +0.237 +-0.063); C2 (Price alpha) failed as frozen (a wrong 3/(8y) term; correct expansion y + 1/2 - 1/(8y)).
- I derived by hand now (labelled): K1/K0 = 1 + 1/(2y) - 1/(8y^2) + ..., so alpha_Price(y) = y + 1/2 - 1/(8y) + O(1/y^2). This agrees with the README's post hoc statement; it is not independent of it in the sense that I read that statement first, but I did the series myself (K0 ~ 1 - 1/(8y) + 9/(128y^2), K1 ~ 1 + 3/(8y) - 15/(128y^2)).

## 3. Exact pass lines (scored per row; agreement is per row, not global)

Each is |mine - target| <= line, mine computed with my declared conventions, continuous root-finding.
- s_mid, s_f2, s_h2 at the decision cell: **0.02 in s** each.
- Bootstrap 16th and 84th percentiles of s_mid: **0.03** each (N = 2000; the seed differs, so I do not require the same stream).
- s_mid at mu = 0.25, 1.5: **0.03**; at mu = 4: **0.05** (the curve is flatter there, so a 0.003 dex offset moves s by about 0.03-0.05; this looser line is frozen now for that reason); alt footing: 0.02.
- Break-evens at s = 1 (flat, rival): **0.03**. (If mine are within 0.03 of CFG165's 2.14/0.65 but not of the README's 2.11/0.62, that is scored as "matches README" only if within 0.03 of the README; the difference is then reported as grid vs continuous root.)
- Break-evens at the other placed prescriptions (3.10/1.26, 3.56/1.56, 3.73/1.67, 3.83): **0.08** (slope sensitivity, frozen now); P2 flat: the README says ">4"; I compute the root on an extended grid to mu = 30 and require it > 4 (pass) and report the number.
- Placement s_eq: K21 exact by definition; **0.03** for D&S, P3, Price; **0.10** for P2 (it sits on the flat part of the curve; the P2 cell is reproduced to 1e-12 by CFG162 so the shift would come only from the K21 curve's flat part).
- Each placed prescription's own decision cell (flat z, H z): **0.3 sigma** each, class exact.
- Full-grid counts (flat-lean / rival-lean at the stated s): within **1 cell**; "no cell leans flat for s >= 2.5" exact.
- R0 separation: within **0.3**; the sigma in the denominator is not stated in the frozen text; I report with the mean of the two sigmas and also sigma_flat and sigma_H, and score the mean (not scored against sigma_flat alone).
- Ordering claims (each of the four bottom-line claims of section 2): exact agreement of above/below classification, with the margin |s_eq - s_mid| reported; a claim also "fails on margin" if the margin is < 0.03.
- C1 rows: **0.005** in Delta' (inc_star). C3 (P2 cell): **0.005**.
- **Verdict language.** REPRODUCES = every row of the group within its line; PARTLY = at least half of the group within its line; DISAGREES otherwise. Reported per group: crossings; gas-bracket crossings; break-evens; placements; counts; power; ordering claims. There is no single global pass.

## 4. Hand ESTIMATES (made after reading the README; labelled) with P(reproduce within the pass line)

| quantity | my estimate | P(within line) |
|---|---|---|
| s_mid at decision cell | 0.67 +-0.02 (from interpolating the CFG160 rows: sum Delta'_flat + Delta'_H = -0.034 at s = 0.6, +0.138 at s = 1) | 0.80 |
| bootstrap 16-84 % | 0.51-0.85, ends +-0.03 | 0.65 |
| s_f2 / s_h2 | 0.73 (inc_star; CFG165 got 0.71 with inc_sfr, which is why I pinned inc_star) / 0.60 | 0.75 / 0.70 |
| s_mid at mu = 0.25 / 1.5 / 4 | 0.44 / 1.11 / 2.39 | 0.65 / 0.60 / 0.45 |
| alt footing s_mid | 0.66 | 0.85 |
| break-evens s = 1 | flat 2.10 +-0.04, rival 0.63 +-0.03 (a 0.003 offset from inc_star shifts CFG165's 2.14/0.65 down by about 0.03-0.05) | 0.65 / 0.65 |
| placements D&S / P3 / Price / P2 | 1.42 / 1.62 / 1.69 / 3.00 | 0.65 / 0.60 / 0.60 / 0.50 |
| break-evens at placed prescriptions (line 0.08) | as README | 0.55 (jointly for the six numbers 0.20) |
| own decision cells of the prescriptions | as README | 0.70 |
| grid counts (within 1 cell) | as README | 0.85 (exact 0.5) |
| R0 separation | 2.5 / 3.4 / 3.1 / 2.6 | 0.80 |
| all four ordering claims reproduce | yes | 0.85 |
| C1 rows and C3 | pass | 0.9 |
| joint: every headline row inside its line | | 0.15 |

Estimates for the attacks (section 6): (a) the ordering "all prescriptions above s_mid" survives every placement variant except K21 itself under R_e = 2 R_eff (there s_mid moves to about 1.05-1.1 in K21 units and K21 at s = 1 sits at or just below it), p = 0.75 that this K21 flip happens; P2 moves by more than 0.3 under the mean-pressure-fraction axis (p = 0.65); the non-P2 prescriptions move by < 0.15 under Delta'_H matching (p = 0.7). (b) s_mid moves by <= 0.05 under inc column, sigma_anchor 7/15 and the anchor rules (p = 0.85), by more than 0.05 under gas-disc scale 3 R_d (p = 0.6), and by more than 0.10 under some leave-one-disc-out (p = 0.65); the R_e-invariant q_mid (mean V_c^2/V^2 - 1 at the crossing) within 15 % across R_e variants (p = 0.5). (c) the both-within-1-sigma region is empty (p = 0.97; analytically Delta'_flat - Delta'_H >= 2.5 sigma everywhere on the map, so |z_flat| <= 1 and |z_H| <= 1 needs a separation <= 2 sigma); the minimum over the map of max(|z_flat|, |z_H|) is about 1.4 (range 1.25-1.7); the both-within-2-sigma region covers about 8 % (4-15 %) of the s x log mu box s in [0,4], mu in [0.25,4], delta = 0, canonical. (d) under flat truth at (s_true, mu_true) on flat's break-even curve the recovered s_mid at the analysis mu = 0.67 is essentially the observed one: the map cannot tell a flat world (s, mu) = (1, 2.1) from a rival world (1, 0.65), by construction, so P(s_mid >= 0.67 | flat truth, nuisance N1) of about 0.3-0.5 (as CFG165's P(lean rival | flat truth) = 0.31 / 0.45).

## 5. MUTATE controls (>= 3; each flips a load-bearing cell; exit 1 = the control bites, exit 0 = does not bite)

Env var `CFG168_MUTATE=k` on the main script. Each MUTATE writes its own outputs (name by mode).
- **M1 (velocities):** KURVS v_last x 10^0.3 (g_obs x 4). Frozen expectation: Delta'_flat > 0 at every s in [0,4], no s_mid in [0,4], H1 fails, exit 1. (CFG165's analogous M5 at P4: +0.556.)
- **M2 (label swap in the 2-sigma crossings, not in s_mid):** the definitions of s_f2 and s_h2 use the other law's Delta'/sigma. Expectation, stated now: **s_mid is label-symmetric and does NOT change** (the map is not label-symmetric only in the 2-sigma classes; this is the CFG165 M3 lesson); the swapped s_f2 moves from 0.73 to about 1.65 and the swapped s_h2 from 0.60 to about 0.03, so the s_f2/s_h2 headline bites (exit 1) and the s_mid row does not.
- **M3 (anchor removed):** the SPARC anchor offset set to 0 (raw KURVS Delta). Expectation: both curves shift up by about 0.09 and s_mid falls to about 0.25 +-0.1, the median (not pooled) 0.064 is not used. Bites (exit 1).
- **M4 (gas):** the decision cell at mu = 1.5. Expectation: s_mid = 1.11 (the README's row), so the headline moves by about 0.44 and bites.
- **M5 (informational; expected NOT to bite):** sigma_out permuted across galaxies (seed 168). CFG165's M6 did not bite; I expect s_mid within +-0.05 (p = 0.7), exit 0 in that case. Kept either way.
- **M6 (placement):** (i) Price alpha replaced by y (the constant 1/2 dropped); expectation: s_eq(Price) falls from 1.69 to about 1.55 (moves by > 0.03 = the pass line; bites). (ii) Dalcanton & Stilp with the sign flipped (pressure subtracts): expectation: no root in [0,6], "unplaced" (bites). Both are recorded in one run; exit 1 if either bites.
- **M7 (informational; expected NOT to bite):** brentq replaced by a linear interpolation on a s grid of step 0.25: s_mid within 0.02 of the root-found one.
A MUTATE whose expectation is wrong is kept and recorded, never repaired.

## 6. The four attacks (frozen procedures; results reported whatever they are)

### (a) What fixes the axis normalisation: how far each prescription moves under other placements
Key observation (declared before computing): because placement is by equality of Delta'_flat, the ORDER of a prescription against s_mid, s_f2, s_h2 does not depend on the normalisation of the s axis at the decision cell (if Delta'_flat(s) is monotone; checked). The normalisation changes the numeric s labels, Kretschmer's +-40 % band, and, importantly, the placement when the gas moves (the matching is done once, at mu = 0.67, and is reused at other mu). So the test is on those.
Variants, each recomputing all six s_eq and s_mid in the variant's own units:
- A1 match on Delta'_H instead of Delta'_flat;
- A2 the physical axis: mean unweighted pressure fraction f = <(V_c^2 - V^2)/V^2> over the ten discs; placement s_eq^f = f(prescription)/f(K21); also the crossing reported as q_mid = f(s_mid);
- A3 the geometric-mean and median of alpha_presc/alpha_K21 over the ten discs;
- A4 matching at each gas mu = 0.25, 0.67, 1.5, 4: s_eq(mu); and the DIRECT check: Delta'_flat(prescription applied itself, mu) against Delta'_flat(s_eq K21, mu), for mu in the bracket;
- A5 R_e = 1.5 and 2 R_eff for K21 (KURVS and anchor);
- A6 anchor uncorrected for both curve and placement;
- A7 sigma in the prescriptions = sigma_0 (paper's central value) instead of sigma_out.
Also for every prescription: the bootstrap probability that s_mid (from the 2000 resamples) lies below its placement.
**Pass/fail meaning.** PASS (the README's placement claims are robust to the placement choice) if in every variant A1-A4, A6, A7: each prescription stays on the same side of its variant's s_mid as in the README AND moves by <= 0.15 in s or 15 % (whichever larger); and in A5: all five non-K21 prescriptions stay above s_mid (invariantly, by the ordering argument). K21's own side is reported, not required (the R_e = 2 R_eff K21 flip is the known CFG160 row). FAIL if any variant flips a non-K21 ordering or moves one by more than the line; the size and direction are reported. The direct check A4 passes at |Delta'_direct - Delta'_placed| <= 0.02 in every prescription and mu; failing means the s_eq map is not an equivalence away from mu = 0.67.

### (b) Is the crossing stable to the definitions?
Variants of s_mid, s_f2, s_h2 at the decision cell:
- inclination column: `inc_sfr_deg` (mine in CFG165) vs `inc_star_deg`; inclination error 3 deg / 8 deg; mass error 0.10 / 0.20 dex (if the shared module exposes it);
- R_e: R_eff, 1.5 R_eff, 2 R_eff (KURVS and anchor), and anchor kept at 1.68 R_disk while KURVS varies;
- anchor: sigma_anchor 7 / 10 / 15 km/s; anchor uncorrected; anchor mean vs pooled vs median (median 0.064 vs pooled 0.092; the frozen text says pooled, the median is the variant); anchor sub-selection by inclination (>= 45 deg instead of 30 deg) and by log M* (>= 10 instead of 9.5) if the loaded anchor object exposes them, otherwise recorded as "not done";
- baryon gas scale 1, 2, 3 R_d (the gas disc extent);
- jackknife: the ten leave-one-disc-out s_mid; and the bootstrap of the ten discs with the anchor ALSO bootstrapped (the frozen bootstrap holds it fixed).
**Pass/fail.** PASS if every non-R_e variant moves s_mid by <= 0.05 (about a third of the bootstrap half-width 0.17), the jackknife range is <= 0.085 (half the bootstrap half-width), and q_mid moves by <= 15 % across the R_e variants; s_f2 and s_h2 by <= 0.05. The fail cases are reported per variant; a disagreement about which variant fails is not a disagreement with CFG162's numbers.

### (c) The break-evens as a function of s: is there any (s, mu) where both laws are within 1 sigma?
- Compute Delta'_flat(s, mu) and Delta'_H(s, mu) on s in {0, 0.05, ..., 4} x mu in 60 log-spaced points [0.25, 4], for delta = 0, canonical, and over the 24 cells (mu x delta x footing) at the s of section 2.
- (c1) Region R1 = {|z_flat| <= 1 and |z_H| <= 1}: its area fraction of the box, and the minimum over the map of max(|z_flat|, |z_H|). Also the analytic bound: R1 is empty whenever (Delta'_flat - Delta'_H)/sigma > 2 everywhere; I verify the minimum separation on the map.
- (c2) Region R2 = both within 2 sigma (the README's s_h2 < s < s_f2 window at mu = 0.67 and its extension in mu): area fraction, and its extent in s at mu = 0.25, 0.67, 1.5, 4.
- (c3) Break-even curves mu_f(s) and mu_h(s) (continuous root; "none in [0.25, 30]" recorded) at s = 0.25, 0.5, ..., 4, and the README's 2.11 / 0.62 at s = 1.
- (c4) The README's statement "for the published prescriptions s = 1.0-1.7, flat fits if mu ~ 2.1-3.7, rival if mu ~ 0.6-1.7" checked with the direct (prescription itself) break-evens.
**Pass/fail.** The README makes no claim of a both-within-1-sigma region, so this attack is a scope statement, not a pass/fail on CFG162's arithmetic: it is reported as "R1 empty / not empty (area)". (c4) PASSES if the direct break-evens lie within the README's quoted ranges (rounded) for K21, D&S, P3 and Price; it FAILS if the direct break-evens differ from the placed ones by more than 0.3 in mu.

### (d) What a null result would have looked like on this map
- (d1) The scale scan: KURVS v_last x {0.85, 0.9, 1.0, 1.1, 1.26, 1.5, 1.995}: s_mid, its existence in [0,4], and the classes of K21 at s = 1. This shows how far the data would have to move for the crossing to vanish or land outside the published range 1.0-1.7.
- (d2) Mock truths (N = 2000 per family; seed 168; re-run seed 169 must agree in every fraction to +-0.02): truth law in {flat, rival}; the mock's mock-V generated as in CFG165 (e): the real KURVS baryons, sigma_out, errors and anchor; g_obs from the law at (s_true, mu_true) with V^2 = g R - s_true alpha_K21 sigma^2 (V^2 floored at 0.25 % of V_c^2, the floor fraction disclosed); analysed by the CFG162 map (analysis mu = 0.67). Families: ideal (s_true = 1, mu_true = 0.67); N1 (mu_true lognormal median 1.0, 0.3 dex; s_true = lognormal(0, 0.4) per galaxy x coherent lognormal(0, 0.2)); N2 (median 2.0); and the point truths (s_true, mu_true) = (1, 2.14) for flat and (1, 0.65) for rival (on the break-even curves).
- Report: the distribution of s_mid (16-50-84 %), P(no s_mid in [0,4]), P(s_mid < 0.67), P(s_mid > 1.0), and P(K21 classed lean rival | truth).
**Pass/fail meaning.** The map is INFORMATIVE ABOUT THE LAW only if P(s_mid >= 0.67 | flat truth, N1) < 0.05 and P(s_mid >= 0.67 | rival truth, N1) > 0.3. Failing it means the map's crossing does not discriminate the laws once the gas and pressure are uncertain (the same finding as CFG165 (e) for the lean class); this is reported as the weight of the map, not as an error of CFG162, whose reading (a map, not a verdict) already says the crossing must be quoted with s and mu. (d1) is reported, not scored.

## 7. Script plan

Scratch dir: `cfg168/`. All scripts: `sys.dont_write_bytecode = True`; repo found from `ZF_REPO` or by walking up from `__file__` (prints `<repo>`); the CFG165 module is imported from `<repo>/campaign_fresh_gravity/CFG165_kurvs_referee/` read-only by adding it to `sys.path`; `MUTATE` is popped from the environment before that import.
- `cfg168_common.py`: glue only: imports the CFG165 module, builds `cell_s(s, mu, delta, foot, inc_col, ...)` with the K21 `scale` key, own alpha functions for Price / D&S / P2 / P3 (via spec kind `alpha`, `fn(S, anchor)`), the brentq wrappers, and the extended-mu root finder.
- `cfg168_main.py`: my controls C1-C5 (C1 P2 via alpha := 2R/R_d equals the module's own P2; C2 Price alpha: y + 1/2 - 1/(8y) at y = 50 to 2e-4 and the numeric -d ln K0/d ln y to 1e-6; C3 README rows at s = 0.6, 1, 1.4 (0.005) and the CFG141 P2 cell (0.005); C4 Delta'_flat(s) monotone increasing on [0,4] so s_eq is unique; C5 the ten IDs are the f_DM rows, no x outside [0,4]); R0; H1; crossings + bootstrap + gas bracket + footing; the s grid counts; the gas axis at s = 1; placements and break-evens; the verdict-vs-target table of section 3. Outputs `CFG168_main.out`, `CFG168_main_results.json`. Runtime < 3 min.
- MUTATE variants: `CFG168_MUTATE=1..7 python3 cfg168_main.py` writing `CFG168_MUTATE_<k>.out/.json`. Exit 0 in the main run if my own controls pass (whether or not the README numbers are reproduced; that is scored in the verdict table); exit 1 in a MUTATE run if the frozen expectation holds (the control bites); M5 and M7 exit 0 when they do not bite.
- `cfg168_attacks.py`: attacks (a), (b), (c); `CFG168_attacks.out/_results.json`. Runtime < 8 min.
- `cfg168_null.py`: attack (d); N = 2000, seeds 168 and 169; runtime < 10 min.
- `run_all.sh` and `CFG168_manifest.txt` (sha256 of inputs, scripts, outputs). No run > 15 min.

## 8. What would count as disagreement with CFG162

- A pass-line miss in section 3 for the headline crossings (s_mid, s_f2, s_h2), the gas-bracket crossings, the break-evens at s = 1, or a placement: reported as a disagreement, and diagnosed in phase 2 by opening CFG162's script (the convention that explains it is named, not silently adopted).
- A different class of a prescription's own decision cell, or a different sign of an ordering claim (above/below s_mid) at any mu in {0.67, 1.5, 4}.
- A break-even that is coarse-grid interpolated in CFG162 but continuous in mine, differing by more than 0.03: recorded as "definition (grid vs root)", not as an arithmetic error; but the frozen CFG162 text promised root-finding, so it is also a departure of the README from its frozen text.
- The README's summary lines that do not survive the attacks (possible, stated in advance to be checked): "every published prescription sits above s_mid" (K21's +-40 % band 0.6-1.4 has its lower edge below s_mid = 0.67 and above s_h2 = 0.60 by construction of the README's own numbers; the R_e = 2 R_eff K21 row); "the literature does not decide once the gas is uncertain" (checked in (d)); "for the published prescriptions ... 2.1-3.7" leaves out P2, which is also a published prescription (Burkert et al. 2010), with s_eq = 3.0 and flat break-even > 4.
- Noted at reading (not disagreements yet): the README says MUTATE "velocities x 2" while the frozen text says x 10^0.3 (a factor 1.995); the README's "main run ... exits 1" comes from the failed C2 only; the README's break-evens 2.11 / 0.62 differ from my CFG165's 2.14 / 0.65, which had a different inclination column.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model or the framework; a lean is not a detection; the theory is not closed.
