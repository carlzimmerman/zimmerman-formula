# PARAMRED lane D (KAPPA) FROZEN CRITERIA: can the kappa / two-footing structure be reduced without deriving kappa?

Written before any script of this lane exists and before any number below was computed by this lane. kappa = 1/2 is FITTED. Nothing here derives kappa (the 32-pi campaign is closed; not retried). The footings are never pooled: they are compared as two fixed-point hypotheses, never merged into one prediction. No dark-matter particle. Raw / framework-native a0 levels only (no LCDM mass functions, no "within X% of LCDM" in any verdict). Repo-relative paths only.

## 0. Disclosure: what I have already read (so nothing here can be called blind)

Read before freezing:
- CFG493 (campaign_fresh_gravity/CFG493_kappa_combined): README, .out, criteria, results JSON. So the route values, errors, levers and the combined value (log a0 -10.1073 +- 0.0985 dex; kappa_Lambda 0.417 +- 0.095; kappa_crit 0.345 +- 0.078) and its variants V1-V11 are KNOWN to me. They are the baseline, not a result of this lane.
- CFG281 README headline (local ALFALFA chain, s* = 1.449, "NOT CALIBRATED": clause (ii) recipe half-width 0.216 > 0.20, clause (iii) distance drift 0.105 > 0.10) and the recipe table in its stage-B JSON.
- CFG571 README (ALMA predictions; "alt footing" in the code is a z = 0 level A0_f times the same z-shape; CFG216 states "canonical decides; alt is reported").
- Memory notes: coefficient footing (Z identity, kappa Z = sqrt(8 pi / 3)), kappa-vs-MOND-form footing, the 32-pi campaign (closed), forecast-statistic-must-see-shared-systematics.

NOT seen before this freeze: any combination containing a route beyond CFG493's P1-P3; the CFG281 route re-expressed at H0 = 67.4 and its shared-term decomposition; any per-footing 95% interval built by this lane; any likelihood ratio between the two footings' kappa = 1/2 predictions; any sealed-test sensitivity number computed here.

## 1. Hypotheses, pre-registered (trial count = 4 verdict hypotheses + 6 reported sensitivities + 3 negative controls)

- H1 (footing is an astrophysical convention). The ratio a0(alt kappa = 1/2) / a0(canonical kappa = 1/2) equals a distance-scale, M/L, H0 or flux-scale factor of the data pipeline.
- H2 (the within-footing kappa interval shrinks). A ledger-wide scan of independent a0 estimates, combined by the same rule as CFG493, tightens the interval.
- H3 (the footings are separable at z = 0). The combined a0 prefers one footing's kappa = 1/2 prediction over the other at a likelihood ratio >= 10.
- H4 (a sealed test pins kappa). ALMA 2026-11-06 / 11-28 or Gaia DR4 2026-12-02 can measure a0 to better than half the combined error.

No other hypothesis is tried. Any further variant is labelled post hoc.

## 2. Step 1: what distinguishes the footings (fixed numbers, derived before computing)

Definitions (CFG493 criteria section 1, adopted unchanged): H0 = 67.4 km/s/Mpc, Omega_Lambda = 0.685, rho_Lambda = Omega_Lambda rho_crit. kappa_Lambda = a0 / (c sqrt(G rho_Lambda)); kappa_crit = a0 / (c sqrt(G rho_crit)). Canonical footing: kappa_Lambda = 1/2 <=> a0 = 9.3603e-11. Alt footing: kappa_crit = 1/2 <=> a0 = 1.1312e-10 (recorded values, 5 significant figures).

Derived prediction written now: because both footings use the same law with a different density, a0_alt / a0_can = sqrt(rho_crit / rho_Lambda) = 1 / sqrt(Omega_Lambda) = 1.208241 (log10 = 0.082157 dex), independent of H0, and identical for every data route. kappa_crit = sqrt(Omega_Lambda) kappa_Lambda exactly. In kappa_Lambda terms the alt footing's "1/2" is kappa_Lambda = 0.5 / sqrt(0.685) = 0.604092. The original cH0/Z form (Z = sqrt(32 pi / 3)) is the alt footing's kappa_crit = 1/2.

Tests:
- T1 (identity). Relative deviation of the recorded ratio 1.1312e-10 / 9.3603e-11 from 1/sqrt(0.685) is <= 5e-4 (the recorded values are rounded; CFG493 K1b shows 2.2e-4).
- T1b (lever test, the discriminator between "convention" and "relabelling"). A pipeline convention moves different routes by different amounts (CFG493 measured levers: gas -1.05 / -0.84 / -1.21; Hubble-flow 0 / +2.17 / +2.28). A footing moves every route by the same factor. H1 is supported only if the footing's log shift matches some single pipeline factor within 0.002 dex AND is route-independent; it is route-independent by construction, so the test is the first clause: compare 0.0822 dex with each listed convention shift (H0 73.04 vs 67.4: +0.0349 dex; Upsilon 0.5 -> 0.7: -0.031 dex (CFG493 criteria section 0 / K1); SPARC-vs-ALFALFA HI flux: 0.0527 dex; quadrature-vs-nu_mono kernel: the V3 mean shift). Pre-registered expectation: no match within 0.002 dex, T1 passes.
- Outcome mapping: T1 pass and T1b no-match = "RELABELLING BY THE COSMIC DENSITY RATIO" (the footing is a normalization of kappa by the measured sqrt(Omega_Lambda), a discrete choice of which density the law uses, not an astrophysical nuisance). T1 pass and T1b match = "CONVENTION PROVEN" (would allow the verdict footing = nuisance proven). T1 fail = report as unexplained.
- Which choice the framework selects: the frozen statement S1 (THEORY_CANONICAL_2026-10-14.md) writes rho_DE, so the framework's own statement selects the canonical footing; it has no say about H0, M/L or flux scale. State both facts.

## 3. Step 2: the combination

Estimator, adopted unchanged from CFG493: Gaussian in L = log10 a0; generalised least squares with C = diag(e_r^2) + Lambda Sigma Lambda^T; shared parameters S_gas (sigma 0.0473 dex), S_star (0.068 dex), S_HF (0.0174 dex); route values, unique terms, shared terms and levers are read from campaign_fresh_gravity/CFG493_kappa_combined/cfg493_kappa_combined_results.json (nothing is re-fitted from raw data). Pull = |L_hat - L_candidate| / sigma_hat (dex), as CFG493.

Inclusion rules, adopted verbatim from CFG493 section 2 (not re-tuned):
- I1 a0 in a committed artifact or reproducible with a control; I2 M/L-insensitive (|lever_star| x 0.068 <= 0.05 dex); I3 passed its own lane's load-bearing controls; I4 no galaxy enters two included routes (one route per survey); I5 distances can be put on the footing's convention.

Candidate list declared now (all a0 estimates in the ledger that are not P1-P3):
- C1 CFG281 local ALFALFA width chain (matched set LC), put on H0 = 67.4 with the 67.4 bracket of its own recipe table.
- C2 SPARC full-sample estimators A, B, C (MNRAS v3). C3 SPARC Hubble-flow gas points (H0 67.4). C4 KiDS late-type z 0.2 and z 0.4. C5 PAPER43 pool. C6 the free-M/L SPARC literature value (2023). C7 CFG397 anchor. C8 LITTLE THINGS / the 2017 reductions reductions. C9 high-z one-sided s* bounds (CFG270, CFG272-280). C10 CFG260 BUDHIES z ~ 0.2.
- Not estimators of a0 (fixed-a0 score tests; cannot enter): CFG515, CFG516, CFG529, CFG531, CFG549, CFG583, CFG584.

Screening is printed as a table (I1-I5 per candidate) before any combination. Pre-registered expectation: no candidate passes all of I1-I5.

Verdict rule for H2 (frozen):
- Extended primary set = P1, P2, P3 plus every candidate that passes I1-I5.
- CONSTRAINT TIGHTENED iff sigma_ext <= 0.90 x sigma_CFG493 (0.0984754 dex) AND the consistency chi2 has p >= 0.05 AND the extended set's shared-systematic floor (all unique terms to 0) is printed beside it. Otherwise NO REDUCTION.
- Control K-rep: re-computing the three-route GLS from the JSON must return L_hat = -10.1073217 and sigma_hat = 0.0984754 to 1e-6.

Reported sensitivities, never the verdict (each is a labelled departure from the inclusion rules):
- S1 C1 added as a fourth route. Value L = log10(9.3603e-11) + log_s(H0 67.4 bracket) from the CFG281 JSON. Unique terms (dex, half-widths taken as 1 sigma as in CFG493): resample SD, width correction delta, sin i_eff, R scale, distance-window drift, all from the CFG281 JSON; the M* zero point and H0 rows enter as shared S_star and S_HF with levers measured from the same table (S_star lever = delta log_s / delta tau_ms; S_HF lever = delta log_s / log10(73.0/67.4)); the gas lever is the all-baryons lever (from the band table, -d log_s/dt at t = -0.15 vs +0.15) minus the star lever; no flux-tie term (ALFALFA is the reference scale).
- S2 / S3 CFG493 variants V1 / V2 (P1 replaced by SPARC estimator C / A), read from the JSON, plus a stress version with P1's measured gas lever (-1.048) given to the replaced route.
- S4 CFG493 variant V8 (KiDS late rows added), read from the JSON.
- S5 leave-one-route-out over P1, P2, P3.
- S6 CFG493 variants V1-V11 envelope: min / max L_hat and sigma, and the pull of each footing's kappa = 1/2 in each.

Candidate kappa values, fixed now. Canonical footing (kappa_Lambda): 1/2 (a0 9.3603e-11); 1/sqrt(pi) = 0.5642; 0.6; the MOND-literature form cH0 / (2 pi) (kappa_Lambda 0.5567); cH_Lambda / (2 pi) (0.4608); the literal 1/(2 pi) = 0.1592 (listed because the MOND-form shorthand "kappa = 1/(2 pi)" is sometimes used with the wrong denominator). Alt footing (kappa_crit): 1/2 (= cH0 / Z, a0 1.1312e-10); 1/sqrt(pi); 0.6; cH0 / (2 pi) (kappa_crit 0.4607); the literal 1/(2 pi). The value kappa_Lambda = 0.6041 (the alt footing's 1/2) is also listed as a canonical-footing candidate.
Classification per candidate: EXCLUDED if pull >= 2.0, DISFAVOURED if 1.0 <= pull < 2.0, ALLOWED if pull < 1.0. 95% interval: L_hat +- 1.96 sigma_hat, mapped to kappa_Lambda and kappa_crit.

H3 rule (frozen). Likelihood ratio LR = exp(0.5 (pull_alt^2 - pull_can^2)) between "canonical kappa = 1/2" and "alt kappa = 1/2" given the combined a0 of the CFG493 primary set. WEAK if max(LR, 1/LR) < 3; MODERATE 3-10; STRONG >= 10. H3 holds only for STRONG. Computed also for S1-S3 (reported). Comparison of two fixed points is not pooling.

Non-independence report: print the GLS route correlation matrix (shared S terms), the effective number of independent routes (mean single-route variance / sigma_hat^2), and a table of dataset pairs with the reason they are not independent (shared galaxies, shared single-dish flux anchor, shared Hubble-flow scale, same recipe family, shared M*).

## 4. Step 3: what could pin kappa

A test pins kappa better than the combined error iff the a0 precision it can reach is below sigma_hat / 2 (0.0492 dex), with its stated systematic floors included. For ALMA: required M_gas scales as 1 / a0 (lever -1 in the deep regime), the CFG571 stellar-mass branch moves the framework's number by 0.6 dex, the KURVS systematic floor is 0.15 dex, and F-DESI vs F-flat separate by <= 0.02 dex. For Gaia DR4: the current canonical prediction is Newtonian (gamma_v - 1 <= 8.9e-4 at 50 kAU, independent of kappa); under the older MI prescription 22% of a0 moved gamma_v by 3.3% (DR4 pre-registration, record), with frozen sigma_sys 0.02. Arithmetic only; no data.

## 5. Negative controls (MUTATE mode, all in the script)

- MA (can the rule fire?): inject a fake independent route at L_hat with unique error 0.02 dex and no shared levers. The verdict machinery must return CONSTRAINT TIGHTENED.
- MB (is the consistency gate live?): inject a fake route at L_hat + 0.30 dex with unique error 0.02 dex. It must trip p < 0.05 and must NOT return CONSTRAINT TIGHTENED.
- MC (is T1 live?): replace Omega_Lambda = 0.685 by 0.60 in the denominators. T1 must FAIL.

## 6. Verdict set

CONSTRAINT TIGHTENED (with the new interval), NO REDUCTION, or "footing = nuisance proven". The last is available only if T1b matches an astrophysical convention. A relabelling result (T1 pass, T1b no-match) is reported as a structural finding, not as a reduction of the allowed interval; it does not remove the need to state both footings.

## 7. Process

Criteria first (this file). Then one script, `kappa_lane.py`, deterministic, pure Python, no numpy, reads only small JSON, writes `kappa_lane_results.json`, takes every margin from that JSON, and has `--mutate`. Compute gate: before each run, the pgrep / chain.log check in the brief; if it fires, nothing runs and the run is reported as queued.
