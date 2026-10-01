# CFG244 -- the bound part of an early cold fluid as the owner of the law's dark density: phase 2 (Gate H ambiguous, Gate A the binding FAIL; a scoped no-go)

Criteria frozen and committed before any script: `campaign_fresh_gravity/CFG244_FROZEN_CRITERIA.md` (commit 84e100c47, sha256 `944adc802daf4bac0b2b01343476b42e705adfb5d19332c564064727a4aca058`, identical to the file I wrote). Run as frozen; every departure is listed in section 9.

**Nothing here is closure. kappa = 1/2 stays FITTED. There is no dark-matter particle and no new species: the class is a pressureless, conserved, collisionless FLUID, and the cold MASS (Omega_c h^2 = 0.1200) is still REQUIRED and supplied by nothing in the class. A bound-core reading that matches LambdaCDM is not a derivation of the law.** A scoped no-go is not a theorem. A lean is not a detection. The repository was only read (CFG118's code is imported read-only); everything was written in the scratch directory.

**Re-run (about 3 minutes on a 16-core machine).** From the lane directory: `ZF_REPO=<repo root> bash CFG244_run_all.sh` (inside the repository the root is found by walking up, so `bash CFG244_run_all.sh` suffices; `CFG244_NPROC` sets the process count for Gate A, default min(14, cores)). It runs H, then A, then D as a labelled POST-HOC extra (A binds), then every MUTATE with the frozen expected exit code beside the observed one (`unexpected outcomes: 0`), then `CFG244_verdict.py`. Python 3 with numpy and scipy and a C compiler (`cc`, used by CFG118's `shellcore.c` into a temporary directory); nothing downloaded. No output prints an absolute home path (`<repo>` and `<lane>` are substituted; checked by grep).

## 1. Bottom line

- **Gate H (satellites): outcome class H4 -- PASS, AMBIGUOUS** in the frozen wording ("the satellites do not separate the route from B"). On the primary (P2) kernel the outcome is H2 ("the route is a DIFFERENT LAW from B at satellites": Delta chi2_V2 = +11.68 canonical and +9.42 alt, (b) acceptable), but on the record's own exponential RAR kernel the alt footing falls to +8.60 (< 9), the two kernels land in different categories, and the frozen rule reports the more cautious class. H1 and H3 (the binding FAILs) are not reached on either kernel.
- **Gate A (amount): the BINDING FAIL.** The bound cold mass of spherical secondary infall onto a static baryon core does not reproduce C(r) = (a0/4 pi) M_b(<r): all three sub-tests fail on every bracket and both footings. The radial scale goes as M^p with **p = 0.343 / 0.339 / 0.327** (q = 0.05 / 0.1 / 0.2; the turnaround reading, 1/3, not 1/2; the frozen window is |p - 1/2| <= 0.0291), so R_s/r_M varies by **3.03 / 3.04 / 3.20** across 1e9-1e12 Msun against the 1.22 that a 10% line allows. At q = 0.1 the local ratio C_bound/C_target is 0.81-4.56 at x about 1.1 and 0.10-0.15 at x about 28 (cumulative 1.27-4.04 and 0.38-0.65), and 2.9-15.9 at x about 0.11. The binding failure is named: **the radial scale follows the turnaround (M^(1/3)), not r_M (M^(1/2)); too much bound cold mass inside r_M and too little outside.**
- **Stop rule:** the lane stops at Gate A. Gate D was run only as a labelled POST-HOC extra and says the route REDUCES TO LAMBDACDM PLUS A COINCIDENCE (section 6); it is not a verdict input.
- **The plain answer to the question asked** (section 4): at the record's own error model the data prefer the bound-core reading (b) over the best "satellites own nothing" variant, by Delta chi2 = +13.6 / +11.3 (canonical / alt; P2 kernel; V1) and +12.5 / +10.5 on the record's own kernel; the whole of that preference is carried by the ultra-faints, so yes, **the record's UFD failure of B (3.5-3.9 sigma for the isolated law) is what favours the bound-fluid reading** in this machinery. It is a lean, not a detection: it clears the frozen Delta chi2 >= 9 line in the strict view (V2) only on the P2 kernel, and the ultra-faint gate is weakly diagnostic for an NFW halo.

## 2. Gate table (P = PASS, F = FAIL, U = UNDEFINED, N = NOT ADDRESSED; each cell cites its script; MAIN = the frozen stop-rule verdict, PH = post-hoc extra after the stop, never part of the verdict)

| gate | cell | script |
|---|---|---|
| controls C-H1 .. C-H5 | **P** (5 of 5) | `CFG244_H_satellites.py` |
| **Gate H** | **PASS, class H4 (AMBIGUOUS)**; P2 kernel alone: H2; RAR kernel: H4 | `CFG244_H_satellites.py` |
| &nbsp;&nbsp;H1 / H3 (binding FAILs) | **not reached** (Delta_V1 > 0 on every row; (b) acceptable: all |z_b| < 2, chi2_b(V1) = 2.30 <= 11.34) | same |
| controls C-A1, C-A1b, C-A2, C-A3, C-A4b | **P** | `CFG244_A_infall_bound.py` |
| control C-A4 (test-shell energy drift < 1e-3) | **F, kept**: -4.3e-3 (q = 0.05), -1.4e-3, -6.5e-4 | same |
| **Gate A (amount and scale)** | **F, BINDING, STOP (MAIN)** | same |
| &nbsp;&nbsp;A1 local amount (point cores, both footings) | **F** (largest |ratio - 1| 14.9-22.5 canonical, 13.6-19.4 alt) | same |
| &nbsp;&nbsp;A2 cumulative amount | **F** (largest |ratio - 1| 8.0-10.7 canonical, 6.8-9.8 alt) | same |
| &nbsp;&nbsp;A3 scale exponent | **F** (p = 0.343, 0.339, 0.327 against 1/2; turnaround reading holds for every q) | same |
| bound-fraction diagnostic (reported) | inside x <= 30 the bound fraction is >= 0.9948; "ever turned around" differs by <= 0.0052 | same |
| Gate D (distinctness) | **N in the frozen verdict**; PH: REDUCES TO LAMBDACDM PLUS A COINCIDENCE | `CFG244_D_distinctness_POSTHOC.py` |
| G2, G3, G5 | N (by premise / statement only, as frozen) | not run |

## 3. Gate H in full

**Rule (frozen).** Three populations, N = 88: P1 MW ultra-faints (31 resolved + 9 limits by Kaplan-Meier = 40), P2 MW classical dSphs (14), P3 M31 LVD (34). Offset = median log10(sigma_obs/sigma_pred) with the record's single-radius estimator; error = statistic + Upsilon floor (+ collapse-mass floor for (b) in V1) by the record's committed recipe (bootstrap 2000, seed 244001); chi2 = sum of (offset/error)^2 over the three populations. (a) = the lowest chi2 of (a0) Newtonian with no phantom, (a1) the isolated law of the satellite's own baryons (the record's B reading), (a2) the law with the host's external field (g = g_N nu(sqrt(g_N^2 + g_host^2)/a0)); (b) = Moster+13 (clamped 1e9) + Duffy-full NFW, (1 - f_b) M_NFW, no phantom (the record's LambdaCDM comparator). V1 = the record's error model; V2 = no collapse-mass floor for (b). Delta = chi2_a - chi2_b.

**Table, primary kernel P2** (offset dex / chi2; z = offset/error in `CFG244_H_satellites.out`):

| footing | population | (a0) | (a1) | (a2) | (b) V1 | (b) V2 |
|---|---|---|---|---|---|---|
| canonical | P1 UFDs | +1.078 / 46.62 | +0.329 / 15.21 | +0.656 / 15.23 | +0.080 / 0.37 | +0.080 / 2.16 |
| canonical | P2 classical | +0.515 / 14.28 | +0.036 / 0.19 | +0.115 / 1.38 | -0.029 / 0.14 | -0.029 / 0.14 |
| canonical | P3 M31 LVD | +0.610 / 24.53 | +0.049 / 0.48 | +0.160 / 2.79 | -0.062 / 1.79 | -0.062 / 1.90 |
| canonical | **total chi2** | 85.43 | **15.88** | 19.41 | **2.30** | **4.20** |
| canonical | **Delta chi2** (a = (a1)) | | | | **+13.58** (V1) | **+11.68** (V2) |
| alt | P1 | +1.078 / 46.62 | +0.309 / 13.39 | +0.637 / 14.34 | +0.080 / 0.37 | +0.080 / 2.16 |
| alt | P2 | +0.515 / 14.28 | +0.016 / 0.04 | +0.095 / 0.95 | -0.029 / 0.14 | -0.029 / 0.14 |
| alt | P3 | +0.610 / 24.53 | +0.031 / 0.19 | +0.139 / 2.14 | -0.062 / 1.79 | -0.062 / 1.90 |
| alt | **total chi2** | 85.43 | **13.62** | 17.44 | **2.30** | **4.20** |
| alt | **Delta chi2** | | | | **+11.32** (V1) | **+9.42** (V2) |

**Table, the record's own exponential RAR kernel** (the cross-check the frozen rule requires): canonical totals (a0) 85.43, (a1) 14.75, (a2) 17.69, (b) 2.30 (V1) / 4.20 (V2): **Delta +12.45 (V1) / +10.55 (V2)**; alt (a1) 12.80, (a2) 15.96: **Delta +10.50 / +8.60**. P1 (a1) offsets +0.325 / +0.304 (z 3.78 / 3.55): the record's committed 3.77 / 3.55 sigma is reproduced by control C-H1b.

**Outcome class in the frozen wording: H4 -- PASS, AMBIGUOUS.** Reason, stated: P2 kernel gives H2 (Delta_V2 >= 9 on both footings, (b) acceptable); the RAR kernel gives Delta_V2(alt) = +8.60 < 9, so H4; the kernels disagree and the frozen rule takes the more cautious class. (b) acceptable on its own: z_b = +0.61 (P1), -0.38 (P2), -1.34 (P3), chi2_b(V1) = 2.30.

**What the table says about (a2) and (a0).** (a0) fails everywhere (UFD +1.08 dex): the "own nothing, Newtonian" reading is excluded by 6.8 sigma on the UFDs and 3.8-5.0 sigma on the other two. (a2), the law with the host's external field, is worse than (a1): the UFD median moves **+0.327 dex** with the host on (my frozen estimate said +0.01 to +0.08: wrong, section 7). The record's own EFE rule (h43's `a_int`, labelled, not a frozen variant) gives +0.764 / +0.196 / +0.248 on P1 / P2 / P3. So (a) = (a1) on both footings.

**Robustness rows (reported, none changes the verdict; Delta chi2 canonical V1/V2 | alt V1/V2):** baseline at 500 resamples +13.5/+11.7 | +11.2/+9.5; (b) collapse mass x0.1: +11.1/**-1.1** | +8.9/-3.4; x0.3: +14.4/+9.0 | +12.2/+6.8; x3: +10.8/+10.7 | +8.6/+8.5; x10: +4.6/+4.3 | +2.4/+2.0 with (b) failing its acceptance (chi2_b(V1) = 11.15, a population at the line); Dutton-Maccio concentration: +8.3/+7.8 | +6.0/+5.6 and (b) not acceptable (the LVD); Duffy relaxed: +10.8/+10.7 | +8.5/+8.4; the CFG91 error recipe (bootstrap SE and Upsilon propagated into the halo and gas): +14.2/+12.5 | +12.1/+10.5; floors on P1 only (the frozen letter): +13.4/+11.7 | +11.1/+9.5. Clamp scan of (b) on P1 (KM median): +0.204 / +0.143 / +0.080 / +0.023 / -0.037 for M_coll = 1e8 / 3e8 / 1e9 / 3e9 / 1e10. Leave-one-population-out: without P1 Delta = **-1.3 (V1) / -1.4 (V2)** (canonical): without the ultra-faints the two readings are not separated (a1: chi2 0.19 + 0.48; b: 0.14 + 1.79); without P2 +13.5/+11.6; without P3 +14.9/+13.1. Collins+13 in place of P3: +15.4/+13.6. UFD offset against M_V (resolved only, Spearman): (a1) rho = +0.45 (p 0.011), (a2) +0.64 (p < 0.001), (b) +0.31 (p 0.089): the ordering is in the data, flagged only (CFG83). The record's sum rule S (a hybrid, not a reading of this class) gives medians -0.059 / -0.118 / -0.107.

**Planted-sample power (MH4; 200 mock data sets per truth, bootstrap 200 each).** Truth (b): outcome counts H1 0, H2 56, H3 3, H4 141, median Delta (canonical V1, V2, alt V1, V2) = +10.2, +9.0, +7.7, +6.9, so **P(H2 | truth b) = 0.28**: even if the bound core were true the frozen line returns H4 70% of the time. Truth (a1): H1 150, H4 50, median Delta = -12.8, -52.9, -12.5, -52.5, so P(H1 | truth a1) = 0.75. The observed Delta (+13.6 / +11.7 canonical) lies on the (b) side of both planted distributions. Mock design (per-system scatter from the real systems, limits kept at their real distance above the median, 200 resamples instead of 2000) is a disclosed approximation.

## 4. The plain answer: which reading do the data prefer, and does the UFD failure favour the bound-fluid reading?

**At the record's own error model (V1, the record's recipe, both footings, N = 88) the data prefer the bound-core reading (b) over "satellites own nothing" (best variant (a1), the record's B reading) by Delta chi2 = +13.6 (canonical) and +11.3 (alt) on the class's P2 kernel, +12.5 and +10.5 on the record's own kernel. In the strict view V2 (no collapse-mass floor for (b)) the preference is +11.7 / +9.4 (P2) and +10.6 / +8.6 (RAR kernel). The record's UFD failure of B does favour the bound-fluid reading: it carries the entire difference** (without the ultra-faints the two readings tie, Delta about -1.3), and the isolated law's ultra-faint offset is +0.33 dex (3.9 sigma) against +0.08 (0.6 sigma) for the bound core.

**Caveats, which make this a lean and not a detection.** (1) The strict-view line (Delta_V2 >= 9 on both footings and both kernels) is not cleared on the record's own kernel; the frozen class is H4. (2) The test is weakly diagnostic for an NFW halo: (b)'s ultra-faint offset stays inside 2 sigma of zero for every collapse mass in the 1e8-1e10 scan (+0.204 to -0.037 dex against an error of 0.132), the V2 preference vanishes at x0.1 (Delta -1.1) and (b) fails its own acceptance at x10 and under the Dutton-Maccio concentration (the LVD): the preference is for "a halo of order 1e9 Msun in each UFD", and 33 of the 40 UFDs take the clamped Moster value 1e9 (an extrapolation, not a measurement). (3) The record's own error model is kinder to (b) than V2 (it adds a 0.121 dex collapse-mass floor), by design; the frozen rule requires a preference for (b) to survive V2. (4) Power: if (b) were true the frozen line would return H2 only 28% of the time. (5) The ultra-faint offsets are binary- and tide-sensitive (CFG46, CFG51, CFG66, CFG93); the eight binary-corrected systems and the two multi-epoch systems are not re-scored here. (6) A preference for (b) is a statement about satellites; it says nothing about hosts, where Gate A fails.

**What it means for the route.** If (b) is the reading, then at satellites the class is the LambdaCDM comparator with a declared stellar-to-halo relation: the class cannot supply that collapse mass from its own constants. This is a different law from candidate B's isolated-law dwarf reading, not a derivation of anything: a bound-core reading that matches LambdaCDM at satellites is LambdaCDM there.

## 5. Gate A in full

**Code: CFG118's own code was IMPORTED READ-ONLY** (module `CFG118_secondary_infall`: set-up, `shellcore.c` compiled at run time into a temporary directory, snapshot and target helpers; CFG118's `main()` is not run and nothing in CFG118 is edited or written). The new layer in `CFG244_A_infall_bound.py` adds the bound classification, the bound-restricted binned products and shell bootstrap, and the three sub-tests. I did not write an independent shell code (frozen: only if every sub-test passes). Runs: 24 main (N = 20,000) + 24 at N = 5,000 (4 masses x 3 brackets x point and exponential cores), a no-core run, CFG118's own Hubble-flow control and three test orbits; 1.5 minutes wall on 14 processes.

**Classification (frozen: instantaneous).** E_i at z = 0 in the z = 0 potential (shells + core, the smooth background and Lambda of the integrator), bound iff E_i < Phi_eff(r_s), r_s the outermost saddle of the net radial force (closed form checked: r_s = 242.94 kpc, relative difference 0). Inside x = r/r_M <= 30 the bound fraction is 0.9948-1.0000 over all point runs; "ever turned around" differs by at most 0.0052 (one 1e10 Msun run, q = 0.05); the boundness-flip proxy (turned around but unbound plus unturned but bound) is at most 0.0052. Outside the zero-velocity radius (r_ta to 3 r_ta) 95.6% of the shells are unbound on the instantaneous classifier (43% on the Newtonian-only one, MA5), so the Lambda term is what removes them. **The bound part inside x <= 30 is the whole cold fluid there:** Gate A is CFG118's result for the bound subset, and it reproduces CFG118's committed ratios exactly (control C-A1b: 48 runs, max relative difference 0).

**Sub-tests (point cores, canonical footing, q = 0.05 / 0.1 / 0.2; min-max over the four masses).**

| quantity | x = 0.11 | x = 1.12 | x = 28.2 |
|---|---|---|---|
| local C_bound/C_target, q = 0.05 | 6.33-23.51 | 0.99-4.57 | 0.08-0.15 |
| local, q = 0.1 | 2.89-15.88 | 0.81-4.56 | 0.10-0.15 |
| local, q = 0.2 | 1.05-16.67 | 0.89-3.98 | 0.09-0.21 |
| cumulative M_c,bound/M_c,target, q = 0.05 | 6.52-30.74 | 1.44-3.96 | 0.36-0.66 |
| cumulative, q = 0.1 | 2.79-21.82 | 1.27-4.04 | 0.38-0.65 |
| cumulative, q = 0.2 | 0.01-15.09 | 1.04-3.81 | 0.39-0.65 |

- **A1** fails on all 12 (footing, bracket) combinations for the point cores (and for the exponential spheres: largest |ratio - 1| 31.6-357); **A2** fails on all 12 (largest 6.8-13.7); the noise guard (shell bootstrap and the 5,000-vs-20,000 difference) never rescues a bin: every failure is a guarded failure.
- **A3.** R_s (the radius where M_c,bound(<r) = M_b) for q = 0.05: 1.9 / 4.0 / 9.5 / 20.3 kpc at 1e9 / 1e10 / 1e11 / 1e12 Msun, i.e. x = R_s/r_M = 1.596 / 1.041 / 0.777 / 0.526 against the target sqrt(3) = 1.732 at every mass; exponent p = 0.343 (time-averaged estimator 0.349, 5,000 shells 0.340); q = 0.1: x = 1.707 / 1.224 / 0.844 / 0.562, p = 0.339; q = 0.2: x = 1.815 / 1.398 / 0.854 / 0.567, p = 0.327. The exponential spheres give p = 0.243 / 0.249 / 0.232. The turnaround radius scales as M^(1/3) (x_ta = 193 / 132 / 90 / 61).
- **The new-ingredient rule.** No baryon-coupled relaxation was added (the frozen A-ext is a post-hoc extra on the orchestrator's request only). Its ingredients, if added, would be a growing baryon core (an assembly redshift and time scale, constants counted against G4 unless tied to Lambda or kappa) or baryon-driven segregation, scored separately and never pooled with this verdict.
- **Untested hypotheses inherited from CFG118 (declared in the frozen file):** a static core present from z = 100, the smooth Omega_b background, spherical symmetry with three brackets, z_i = 100, the 3 r_ta extent, N_s; non-spherical collapse, mergers, tidal torques, feedback, and a growing core.

## 6. Gate D (POST-HOC extra after the stop; not a verdict input; frozen estimate compared)

`CFG244_D_distinctness_POSTHOC.py`: D1-D7 against the frozen thresholds all come out NOT DISTINCT from LambdaCDM, so **the route REDUCES TO LAMBDACDM PLUS A COINCIDENCE (the numerical statement a0 = kappa c sqrt(G rho_Lambda), kappa fitted, which enters no equation of the class)** -- a statement about this class, not about candidate B. The numbers: D1 the effective a0 (3 G M_b/R_s^2) varies by 0.98 dex over 1e9-1e12 Msun against the committed RAR bound 0.048 dex; D2 a0(z = 2.5): the route follows the collapse epoch (LambdaCDM-native +0.334 dex by the class's structure: argued from the absence of an acceleration scale, CFG230 R02's Newtonian-only half, not computed from simulations at z = 2.5), distinct from B's flat 0.00 and not from LambdaCDM (committed cap 1.3 sigma); D3 reading (b) is the record's LambdaCDM comparator (identical by construction); D4 the scatter of log10(C_bound/C_target) over the 12 (q, M) cases is 0.26 dex (std) at x about 1.1 and 0.12 dex at x about 28 against 0.048; D5 the bound density slopes (q = 0.1): inner -1.70 to -1.91, outer -2.35 to -2.71 (EdS -9/4, NFW -3 (memory), target -1 and -2); D6 gamma-hat = 1.000 for the route, LambdaCDM and B's Arm C; D7 the route follows LambdaCDM's colour-split halo masses. **A disclosure that could flip D1 under another reading:** the frozen text defines the LambdaCDM value of D1 as the same as the route's (same fluid), which scores it NOT DISTINCT; the SHMR-based comparator computed here (Moster + Duffy, M_* = M_b) has a spread of 1.11 dex and exponent 0.311, 0.13 dex from the route's. Read literally with the 0.05 dex model-to-model rule that would be DISTINCT, but the difference is baryon loss and feedback that the route does not have (a disagreement between two cold-collapse models), not a prediction beyond LambdaCDM; I scored per the frozen text and flag it. The frozen estimate P(D finds a difference) = 0.07: held.

## 7. How the frozen hand estimates fared (kept, wrong ones included)

| estimate (frozen) | result | |
|---|---|---|
| E-H1: P(Delta_V2 >= 9 on both footings) 0.56; expected Delta_V2 about +12 / +10 | P2 kernel +11.68 / +9.42; RAR kernel +10.55 / +8.60 | numbers held; the 9-line is cleared on one kernel only |
| E-H2: P(H1) 0.01, P(H3) 0.08, P(H2) 0.48, P(H4) 0.43 | **H4** (H2 on the P2 kernel alone) | H4 was frozen at 0.43 and H2 (modal) at 0.48: partly wrong on the modal class (the P2 kernel alone gives H2; the kernel disagreement made it H4); P(H1), P(H3) held |
| E-H3: best (a) = (a1), P 0.9 | (a1) on both footings | held |
| E-H3: (a2) - (a1) UFD median +0.01 to +0.08 dex, P 0.8 | **+0.327 dex** | **wrong by 4x** (my arithmetic used a 2e4 Msun, 30 pc UFD; typical UFD internal accelerations are 1e-3 a0 or less, so the host's 0.01-0.1 a0 dominates) |
| E-H3: (a0) UFD offset >= +0.8 dex, P 0.85 | +1.078 | held |
| E-H4: (b) acceptable in V1 canonical, P 0.85 | acceptable (|z_b| <= 1.34, chi2_b 2.30) | held |
| E-H4: planted power P(H2 \| truth b) about 0.7, P(H1 \| truth a1) about 0.03 | **0.28 and 0.75** | **both wrong, the second in the opposite direction** (I underweighted the LVD's small error 0.046; the frozen lines are roughly symmetric and the (b) power is low) |
| hand sums chi2_a1 = 14.7 / 12.8, chi2_b(V1) = 2.2, Delta about +12.5 / +10.6 | RAR kernel 14.75 / 12.80, 2.30, +12.45 / +10.50 | held (restates the record) |
| E-A1: P(A1, A2, A3 all pass) 0.005 | FAIL, all three | held |
| E-A2: bound fraction >= 0.99 inside x <= 30 (P 0.9); "ever turned" differs < 1% (0.85); flip < 5% (0.6) | 0.9948; 0.0052; 0.0052 | held |
| E-A3: R_cum(1.12) in [1.0, 4.5], R_cum(28.2) in [0.25, 0.70] (P 0.7 each) | 1.04-4.04 and 0.36-0.66 | held (restates CFG118) |
| E-A3: local ratio at x about 0.11 >= 2 for point cores (P 0.8) | 1.05-23.5 (q = 0.2, 1e9 Msun: 1.05) | partly wrong (one noisy cell) |
| E-A4: p in [0.29, 0.38] (0.90); turnaround reading (0.90); P(p within 0.0291 of 1/2) 0.01; spread about 3.2 | 0.327-0.343; yes; no; 3.03-3.20 | held |
| E-A5: the noise-limited local-bin resolution control most likely to fail | not run (my frozen C-A3 is the cumulative one: **passed**, largest 0.080); **the control that failed is C-A4, the energy drift** | the failure came from the wrong place; see below |
| controls: all reproduction controls pass at first run (P 0.55) | one control failed (C-A4) | wrong |
| E-D1: P(D finds a distinct observable) 0.07 | none, with the D1 definitional caveat | held |
| expected binding failure: Gate A, sub-tests A2 and A3, P 0.90 | Gate A: A1, A2 and A3 all fail | held (A1 also fails) |

## 8. MUTATE controls and failed controls (frozen expected codes; observed)

| id | change | target cell | expected | observed |
|---|---|---|---|---|
| MH1 | swap the readings' labels | verdict H2 -> H1 (Delta changes sign) | bites | **bites** (exit 1) |
| MH2 | every sigma_obs x 0.5 | Delta_V1 canonical +13.47 -> -72.90; verdict H2 -> H1 | bites | **bites** |
| MH3 | host off | the (a2) - (a1) UFD cell +0.327 -> 0.000; verdict H2 -> H2 | bites on the cell, verdict unchanged | **bites on the cell; verdict unchanged**, as stated in advance |
| MH4 | planted samples, 200 per truth | modal outcome H4 (truth b) vs H1 (truth a1) | bites; power 0.7 / 0.03 | **bites; power 0.28 / 0.75** |
| MH5 | (b) collapse mass / 100 | P1 |z_b| 0.60 -> 2.22 (line 2); verdict H2 -> H1 | bites | **bites** |
| MA1 | evaluator fed the target's profile | A1 and A2 flip FAIL -> PASS | bites | **bites** |
| MA2 | no baryon core | bound fraction inside x <= 30: 0.9948 -> 0.0000 | bites | **bites** |
| MA3 | target scale proportional to M^(1/3) | A3 flips FAIL -> PASS | bites | **bites** |
| MA4 | classify by "ever turned around" | bound-fraction cell | does NOT bite (P 0.85) | **does not bite** (exit 0; 0.9948 vs 1.0000) |
| MA5 | Lambda removed from the classifier | outer-region unbound fraction 0.956 -> 0.429 (>= 0.05); inner bound fractions differ by <= 0.0052 | bites on the outer cell | **bites** |
| MD1 | plant route = LambdaCDM / plant route a0(z) flat | D verdict REDUCES <-> DISTINCT | bites | **bites** |

`unexpected outcomes: 0` in `run_all.out`. The MUTATE rows of H compare against the P2-kernel verdict (H2), not the final cautious class (H4); MH1 and MH2 send it to H1, which is a binding FAIL in the frozen wording.

**Failed controls and corrections (kept).** **C-A4 FAILS**: the test shell in the static softened 1e10 point mass drifts in energy by -4.30e-3 (q = 0.05), -1.40e-3 (q = 0.1) and -6.5e-4 (q = 0.2) over the run against my frozen line 1e-3. This is CFG118's own integrator (it reported -0.43%, -0.14%, -0.06% for the same orbits; I had read those numbers and froze a line that two of the three could not meet); the pericentres land on the bracket exactly (0.0500, 0.1000, 0.2000). It does not touch the headline (the failure is a factor 3-20 and the cumulative mass at x about 28 agrees to 8% between 5,000 and 20,000 shells, control C-A3), and CFG158's independent code agrees with CFG118's ratios. No line was changed. The first full invocation of `CFG244_run_all.sh` ran without `ZF_REPO` set (the lane was in a scratch directory outside the repository) and every script stopped at repository discovery (4 spurious exit codes); re-run with `ZF_REPO` set, all outcomes as frozen.

## 9. Departures and ambiguities (each handled as the frozen file's rules require)

1. **Footings.** Gate H uses the record's rounded footings 9.36e-11 and 1.13e-10 m/s^2 (the values its committed numbers use, needed for control C-H1); Gate A uses CFG118's 9.3603e-11 and 1.1312e-10.
2. **Upsilon floor.** The record's committed recipe is used: half the range of the offset between Upsilon_V = 1 and 4 (the median is monotone in Upsilon, so this equals the {1, 2, 4} range); the deep-MOND estimator of CFG28's T5 is not added to the floor (the committed recipe that reproduces 3.77 sigma does not). In V2 the (b) Upsilon floor is about 0 (the record holds the halo mass at its Upsilon = 2 value), so "equal floors" means the same recipe for both, and (a)'s floor (0.075 dex) is larger than (b)'s; the CFG91 recipe row propagates Upsilon into the halo and gas and changes nothing in the class.
3. **Collapse-mass floor in V1** is applied by the record's code to every population (it acts only on satellites with M_* < 1e5); the frozen letter (P1 only) is a robustness row with the same class.
4. **Kernel disagreement** (P2 vs RAR) is resolved as frozen (H4).
5. **Planted samples** use 200 bootstrap resamples (not 2000) and place the limits at their real distance above the median (disclosed in the script).
6. **Gate A.** A bin counts as a failure only beyond the noise guard (frozen); the boundness-flip fraction is a proxy (turned-around-but-unbound plus unturned-but-bound at z = 0), because the kernel does not record the potential at the turnaround epoch; the half-own-mass term is neglected in the classification potential (about 1e-3 of the core mass over r); the exponential spheres were run (not dropped), no run exceeded 1.5 minutes. The z = 0 rank estimator of R_s is primary; the time-averaged one agrees to 0.01.
7. **Gate D** was run after the stop as a labelled post-hoc extra; its D2 value is argued, not simulated.
8. The frozen file's lane directory name is `CFG244_lane`; the scripts find the repository by `ZF_REPO` or by walking up, so they run from a directory inside the repository or anywhere with `ZF_REPO` set.

## 10. What was NOT tested

Non-spherical collapse, mergers, tidal torques and tidal stripping of satellites (reading (b) is the unstripped halo); a growing baryon core, adiabatic contraction and feedback (the new ingredient A-ext was not run); other angular-momentum distributions; the Boltzmann (CMB) evolution of the early fluid and the cosmic amount (premise); G5 beyond a statement; the hosts of CFG59 (SLUGGS, X-ray ellipticals, S0, UGC 2487) and the KiDS rows; numerical AQUAL/QUMOND external-field solutions (reading (a2) is an angle-averaged approximation, from memory, unverified); dispersion anisotropy and Jeans modelling; distance and size systematics as nuisance parameters; the multi-epoch and binary-corrected rows (not re-scored); the 5,000-shell local-bin resolution control of CFG118; an independent re-derivation (not triggered: nothing passed everything). Literature facts marked "(memory)" in the output are unverified. Nothing here says the theory is closed or refuted, kappa = 1/2 stays fitted, and there is no dark-matter particle.

## 11. Files

`CFG244_common.py`, `CFG244_H_satellites.py`, `CFG244_A_infall_bound.py`, `CFG244_D_distinctness_POSTHOC.py`, `CFG244_verdict.py`, `CFG244_run_all.sh`; outputs `.out` and `_results.json` for each (`CFG244_H_satellites`, `CFG244_A_infall_bound`, `CFG244_D_distinctness_POSTHOC`, `CFG244_verdict`), `_MUTATE_<id>.out` / `_results.json` for MH1-MH5, MA1-MA5, MD1; `CFG244_A_infall_bound_sims.json` (the binned products of the 49 simulations, 2 MB, reused by the MUTATE runs); `run_*.log` (shell transcripts) and `run_all.out`. The frozen criteria are `../CFG244_FROZEN_CRITERIA.md` (84e100c47).

## In-place re-run (orchestrator)

`CFG244_run_all.sh` was re-run in this directory (`run_all.out`: `unexpected outcomes: 0`, about 1.8 min). Every `_results.json` is identical to the agent's apart from the `seconds` field; the `.out` files differ only in timing lines and in the key order of one printed Python dict (the Gate A simulation products in `CFG244_A_infall_bound_sims.json` reorder the same way). Verdicts, gate cells and table numbers are unchanged: Gate H class H4, Gate A the binding FAIL, MUTATE outcomes as stated (MA4 declared non-biting). Not blind: the frozen estimates restate the record's UFD failure of B and CFG118's committed ratios; the Gate A result reproduces CFG118 by construction (it imports its code), so it is the bound-subset reading of a known result, not an independent test. Gate D is a post-hoc extra scored per the frozen text; the agent's flag that a literal 0.05-dex reading would call the SHMR comparator DISTINCT (0.13 dex) stands.
