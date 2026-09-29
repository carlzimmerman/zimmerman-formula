# CFG180 — Referee re-derivation of CFG170 (the two-epoch gas-ratio test, KROSS z ≈ 0.85 vs KURVS z ≈ 1.5)

(Renumbered from CFG176 by the coordinator; the scratch dir keeps its old name.)

- **Criteria:** `CFG180_FROZEN_CRITERIA.md` (sha256 de83c056…, committed as "CFG180: frozen criteria") before any script existed. The CFG170 README numbers in it are TARGETS I read; my hand estimates were made after reading that README and are disclosed as such.
- **Order of work:** my scripts written from the frozen text alone → main run, MUTATE M1–M6 (all saved) → attacks A, B, mocks C run → ONLY THEN CFG170's script, `.out` and `.json` (including `_firstrun` and `_MUTATE*`) opened → `CFG180_diag_post.py` written after that (labelled post-comparison; not part of any frozen result). `CFG180_diag_B_nobe.py` and the labelled extras A2x and the μ_K = 1.5 mock run are also post-hoc.
- **Repo untouched. No network, no new data. No absolute home path in any output** (`<repo>` is printed; `run_all.sh` greps for it).
- **Not blind:** the README numbers were targets I read. What is independent is the code path from the frozen text, not the expectation.

## Bottom line

**Every headline row of CFG170 REPRODUCES (all pass lines P1–P10), and the NON-DIAGNOSTIC label reproduces under CFG170's frozen conservative interval. What does not survive the attacks is the weight that label can carry.** Nothing here says the data favour either law or the framework; κ = ½ and Ω_c h² stay fitted; a lean is not a detection.

1. **Arithmetic:** all 20 central μ_be, 39 interval edges, 10 R_law with intervals, the 20 disfavoured flags, the calibration-scatter rows, R0, and the two explanatory checks reproduce. Against CFG170's committed JSON, the worst relative differences are 5 × 10⁻⁴ (centres) and 2 × 10⁻⁴ (edges) when I use its interval convention (σ recomputed at each μ = "convention B"); my primary convention A (σ frozen at the central root) differs by at most 1.1% on edges. Both pass the frozen 4%.
2. **Does NON-DIAGNOSTIC survive the interval convention (my estimate E9)? At s ≥ 1.42 yes; at s = 1 it depends on the interval, and is on a knife-edge in every convention.** With the quadrature interval, at s = 1 exactly one law (the rival) is disfavoured by both brackets, so the frozen summary reads DIAGNOSTIC (against the rival). With the bootstrap 16–84% interval the same test stays NON-DIAGNOSTIC, marginally: the flat lower edge is 2.38 (2.42 at seed 181) against the literature bracket's 2.42, and the rival's is 2.24. CFG170's conservative interval is wider than the resampling interval in all four cases tested. At s = 1.42–3.00 the label stays NON-DIAGNOSTIC under the quadrature interval. The s = 1 result also rests on the rival's KROSS break-even at 0.05: 35–42% of KROSS bootstrap resamples have no rival break-even at all.
3. **What a diagnostic result would need (plain answer):** at s ≥ 1.42 no precision in R_obs would do it. The right law's R already lies inside the wrong law's own 1σ interval, so the bracket half-width that could separate them is 0 dex. That is a statement about the root-find intervals, not about R_obs. Even with infinite discs, keeping the SPARC anchor error as a floor, the two conservative intervals still overlap at every s. Removing that floor (post-hoc; the anchor is common to both epochs) the intervals separate only at f ≈ 0.1 (about 100× more discs per sample) at s = 1.42, f ≈ 0.03 (about 1100×) at s = 1.62, and f ≈ 0.01 (about 10⁴×) at s = 1.69. The systematic floor is worse: single-input calibration changes of the size CFG165–168 found move R_law by 0.05–0.6 dex against a separation of 0.06 dex (s = 1.42).
4. **Sensitivity to the calibration choices (B):** FRAGILE. A single-input change makes the frozen summary read "exactly one law disfavoured by both" in 14 (variant, s) combinations; the direction expectations for R_law came out right in 18 of 18 tests.
5. **A null would look like:** in ideal mocks the laws separate by 0.5–0.7 dex in R at moderate gas, and only with a common KURVS offset of +0.15 dex (the size CFG161 found) does the pair collapse toward the observed near-equality (R_flat 2.05 and R_rival 1.50 at s = 1.42 from a flat world with R_true = 1). The observed pattern (both R ≥ 2.5, both disfavoured by the in-repo bracket) appears in 0–5% of ideal or flat-truth-plus-offset mocks, 13–16% of random-offset mocks, and 17–23% of rival-truth-plus-offset mocks. The test has no power in the ideal worlds (section 4, C).

## 1. Where independence stops

- **Imported read-only from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` (shared, NOT independent):** `load_kurvs`, `load_kross`, `load_sparc_anchor`, `per_object`, `pool`, `anchor_pool`, `corr`, `spec`, `gbar`, `gpred`, `alpha_K`, `E_of_z`, and through it `CFG4_common` (`nu_mono`, a₀ constants). `MUTATE` is forced to "0" during the import. In B, `gbar` is patched only for variant V15 (per-disc gas), through a wrapper that changes nothing when `S.muw` is absent.
- CFG165, CFG167 and CFG168 showed this pipeline reproduces CFG160, CFG161 and CFG162. CFG170 runs CFG141's pipeline (exec'd), CFG160's P4 functions verbatim and its own root-finder. So agreement with CFG170 tests that the CFG170 text plus this pipeline determine the numbers. It does not test ν_mono, Kretschmer's α(x) as quoted, the pressure prescriptions, the CFG140 set-up (thin discs, spherical surrogate, gas bracket, mass 0.15 and inclination ±5° errors), or the KROSS/KURVS selections.
- **Independent here:** the break-even root-finder (400-point log grid + `brentq`, both interval conventions), R_law and the open-edge convention, R_obs, the disfavour rule (coded in both the literal and overlap forms), the mock generator, and every attack.
- **Inputs, not re-derived in the main run:** e = 0.23 ± 0.52 and mass slope −0.30 (in-repo); exponent 2.5, slope −0.36 and ±20% (literature, abstract-level, unread by me). The in-repo fit is re-derived in A3 and reproduces.
- **Conventions I fixed before any number:** KURVS `inc_star_deg`; R_e = R_eff; gas scale 2 R_d; the anchor at the same s; s applied to the anchor as well (as in `cell`); s rounded as in the CFG170 text. One ambiguity in the frozen text: "drop the 5% lowest-error discs" (V11e) was read as lowest eV/V.

## 2. Table against CFG170 (row by row; targets from its committed JSON, read after my runs)

R_law with the conservative interval; "mine" = primary convention A, μ_be to 3 decimals (CFG170 in the second entry). The full interval table is in `CFG180_main.out`.

| s | law | KURVS μ_be mine / CFG170 | KROSS μ_be mine / CFG170 | R mine [lo, hi] | R CFG170 [lo, hi] |
|---|---|---|---|---|---|
| 1.00 | flat | 2.109 / 2.109 | 0.636 / 0.636 | 3.316 [1.98, 5.66] | 3.317 [1.98, 5.66] |
| 1.00 | rival | 0.621 / 0.621 | 0.052 / 0.052 | 11.939 [1.58, open] | 11.945 [1.56, open] |
| 1.42 | flat | 3.096 / 3.096 | 0.998 / 0.998 | 3.103 [2.04, 4.73] | 3.103 [2.04, 4.74] |
| 1.42 | rival | 1.257 / 1.257 | 0.352 / 0.352 | 3.570 [1.64, 8.41] | 3.570 [1.63, 8.39] |
| 1.62 | flat | 3.566 / 3.565 | 1.167 / 1.166 | 3.057 [2.05, 4.55] | 3.057 [2.06, 4.56] |
| 1.62 | rival | 1.567 / 1.567 | 0.494 / 0.494 | 3.171 [1.65, 6.24] | 3.171 [1.64, 6.23] |
| 1.69 | flat | 3.730 / 3.730 | 1.225 / 1.225 | 3.044 [2.06, 4.50] | 3.044 [2.06, 4.51] |
| 1.69 | rival | 1.676 / 1.676 | 0.544 / 0.544 | 3.083 [1.65, 5.83] | 3.083 [1.65, 5.83] |
| 3.00 | flat | 6.846 / 6.845 | 2.302 / 2.301 | 2.974 [2.10, 4.19] | 2.974 [2.10, 4.20] |
| 3.00 | rival | 3.829 / 3.829 | 1.475 / 1.475 | 2.595 [1.69, 3.94] | 2.596 [1.69, 3.94] |

| other row | CFG170 | mine |
|---|---|---|
| s = 0: any break-even | none, all four | none, all four |
| calibration scatter s = 0.6: R_flat / R_rival | 4.256 (KURVS 1.166, KROSS 0.274) / none (KURVS 0.0346, no KROSS root) | 4.256 (1.1658, 0.2739) / none (KURVS 0.03455, no KROSS root) |
| s = 1.4: R_flat / R_rival | 3.109 / 3.630 | 3.109 / 3.629 |
| R_obs in-repo, 2σ | 1.005 [0.726, 1.391] | 1.005 [0.726, 1.391] |
| R_obs literature ±20% | 2.016 [1.613, 2.419] | 2.016 [1.613, 2.419] |
| medians z / log M* (KURVS; KROSS) | 1.529, 10.14; 0.850, 10.04 | same; (1 + z) ratio 1.3669 |
| matrix (in-repo / literature) | disfavoured / not, both laws, every s ≥ 1 | identical, 0 flag differences |
| summary at s = 1 | NON-DIAGNOSTIC | NON-DIAGNOSTIC |
| R0 (dex) | 0.56 at s = 1; 0.06, 0.02, 0.01, 0.06 at s = 1.42–3.00 | 0.5563; 0.0609, 0.0160, 0.0055, 0.0592 |
| C1 | 2.1089 / 0.6211 | 2.10898 / 0.62107 |
| C2 | −0.0042 / −0.0821 | −0.0042 / −0.0821 |
| first-run vs final (P10) | only the rival at s = 1 changes | same: only the rival at s = 1 has a missing edge root |
| explanatory | R in (1 + μ) 1.90 / 1.54; rival Δ′ at μ = 0.01: +0.0065 ± 0.020 | 1.900 / 1.541; +0.0065 ± 0.0197 |

**Every difference, classified:**
1. **Numerical / definition (interval convention):** CFG170's script recomputes σ_Δ′ at each μ ("B"). My primary reading ("A", σ at the central root) differs from it by ≤ 1.1% on edges and ≤ 1.3% on R interval edges; convention B agrees to 2 × 10⁻⁴. The frozen text does not choose; both pass. (The rival KURVS lower edge at s = 1, 0.293 against 0.289, is the kind of difference involved, about 1%.)
2. **Numerical (grid):** CFG170 brackets on a 36-point grid, I use 400; no root count differs (one sign change in every central function).
3. **Display / framing:** CFG170's printout for s = 0 flat KURVS shows "mu_be nan [nan, 0.174]": there is no central root but a −σ root exists at 0.174. It affects nothing (no R is formed). Mine prints "no be".
4. **Framing of CFG170's MUTATE controls:** both are evaluator-only. MUTATE=1 sets R_obs := R_flat with the in-repo relative width, so "flat not disfavoured" holds by construction (the bracket is centred on R_flat). MUTATE=2 sets R_obs := 10 R_flat, and at the in-repo bracket the baseline flat flag is already "disfavoured", so its flag does not flip. Neither touches Δ′, the break-even or the interval code. My M1–M6 do (section 3).
5. **README typo:** none found in the numbers. The disclosed departure 4 ("the frozen rule reduces to interval overlap") is CONFIRMED: the two forms agree in all 20 matrix cells (P6).
6. **Provenance:** the "1.3676" in the frozen criteria against the run-time 1.3669: reproduced (1.3669), as CFG170 disclosed.

## 3. Pass lines (frozen section 4) and MUTATE

| line | verdict | note |
|---|---|---|
| P1 controls C1, C2 | REPRODUCES | main exit 0 |
| P2 central μ_be, 20 values (1.5%; KROSS rival s = 1 10%) | REPRODUCES | no misses; s = 0 "no break-even" exact |
| P3 intervals (4%, ≥ 90% of 39 edges, open edge identical) | REPRODUCES, both conventions | 39/39 within 4% of the README targets for A and for B; against CFG170's JSON the worst edge difference is 1.1% (A) and 0.02% (B) |
| P4 R_law (centre 2%, edges 6%; rival s = 1 hi open) | REPRODUCES | no misses |
| P5 R_obs numbers | REPRODUCES | 1.005 [0.726, 1.391]; 2.016 [1.613, 2.419] |
| P6 matrix exact, summary NON-DIAGNOSTIC, two rule forms agree | REPRODUCES | 0 disagreements |
| P7 s = 0.6 / 1.4 rows | REPRODUCES | 4.26, none, 3.11, 3.63 |
| P8 R0 | REPRODUCES | |
| P9 explanatory checks | REPRODUCES | |
| P10 first-run convention | REPRODUCES | only (s = 1, rival) has a missing edge root |
| overall | **REPRODUCES** | `CFG180_main.out` |

**MUTATE outcomes** (exit 1 = bites; `CFG180_MUTATE_k.out`):

| k | mutation | result | verdict |
|---|---|---|---|
| M1 | KURVS V × 10^0.3 | R_flat(1.42) 3.10 → 13.63 | bites (exit 1) |
| M2 | laws swapped in the solver | R_flat(1) = 11.939 = baseline R_rival | bites (exit 1) |
| M3 | KROSS R = r_im (x = 0) | R_flat(1.42) 3.10 → 2.73 (−12%, under the 25% line) | **does NOT bite (exit 0)** |
| M4 | R_obs := R_flat(1.42), in-repo width | flat flag disfavoured → not | bites (exit 1) |
| M5 | R_obs := 10 R_flat(1.42) | flat literature flag not → disfavoured | bites (exit 1) |
| M6 | μ range [0.01, 1.0] | KURVS flat root at s = 1 → none | bites (exit 1) |

- **M3 did not bite, and my expectation was wrong on two counts:** I expected a change of more than 25% and the direction "R_flat up". R_flat went down by 12%. Kept as it came: the KROSS pressure radius at x = 0 (α = 1.475 s instead of 2.53 s) moves both the KROSS pressure term and its baryon radius, and the two nearly compensate in the ratio.
- **M1 wording:** the run prints a comment that a missing root is "counted as a rise"; in fact the mutated KURVS root exists (13.6), so the bite is a genuine 4.4× rise.

## 4. Attacks

### A — is NON-DIAGNOSTIC robust; what would a diagnostic result have required  (`CFG180_attacks_A.out`, seeds 180 and 181)

- **A1 structural required precision.** The distance in dex from the truth law's R to the other law's 1σ interval:

  | s | flat truth | rival truth | class |
  |---|---|---|---|
  | 1.00 | 0.000 | 0.324 | R_obs-limited, but only at a rival-truth R of 11.9 |
  | 1.42, 1.62, 1.69, 3.00 | 0.000 | 0.000 | STRUCTURALLY NON-DIAGNOSTIC |

  - At s = 1 the only w* > 0 is for a rival truth at R = 11.9, which is 6–12 times any R_obs the two brackets give (1.0 and 2.0). For the measured R_obs range the s = 1 row is also w* = 0.
  - The zero-width R_obs windows with exactly one law disfavoured: flat only, for R_obs in [1.58, 1.98] (s = 1), [1.64, 2.04] (1.42), [1.65, 2.05] (1.62, 1.69), [1.69, 2.10] (3.00). The literature central value 2.016 sits inside the s = 1.42–3.00 windows. The ±20% allowance is what puts the bracket back on flat's interval. That is an asymmetry of the intervals (the rival's is wider on the low side), not a difference in centres.
- **A2 sample-size requirement (frozen, with the SPARC anchor as a floor):** the conservative intervals are NOT disjoint at any f, including f = 0, at any s: floor-limited. The quadrature intervals separate at s = 1 for f ≤ 0.25 but not at s ≥ 1.42.
  - **A2x (post-hoc, no anchor floor; the anchor error is common to both epochs, so a per-sample floor double-counts it):** conservative intervals become disjoint at f = 0.5 (s = 1), 0.1 (s = 1.42), 0.03 (1.62), 0.01 (1.69), 0.15 (3.00), i.e. a disc-number factor 4, 100, 1100, 10⁴ and 44; the quadrature intervals need 2, 44, 400, 10⁴, 16. This is the statistical requirement only, and it is stated with the R_obs bracket still unspecified.
- **A3 R_obs precision from the repo.**
  - The in-repo fit reproduces: e = +0.228 ± 0.517 (51 clean PHIBSS rows; mass coefficient −0.298 ± 0.161); z only +0.089 ± 0.524; restricted to z < 1.7 (38 rows): −0.455 ± 1.581. A 1σ bracket half-width is 0.070 dex (0.215 dex for z < 1.7).
  - The in-repo e is 4.4σ from the abstract-level 2.5. The two brackets are not statistically compatible, so "in-repo bracket disfavours both, literature neither" is a statement about which bracket to believe.
  - No other in-repo table brackets z ≈ 0.85 → 1.5 in gas: `sharma2024_gs21b.csv` (225 rows, z 0.76–1.04, median M_H₂/M* 0.27, M_HI/M* 4.07, scaling-derived per CFG165) is the KROSS epoch only; the ALMA gas masses (6 rows) and the HI tables (z < 0.5) do not reach z ≈ 1.5.
  - The frozen A3 string reads "1-sigma half-width 0.070 dex ≤ smallest w* > 0 0.324 dex", which by its letter says the precision suffices. That is an empty reading (the 0.324 is the rival-truth row at R = 11.9); I keep the string as it came and give the correct one here: **no in-repo dataset, and no precision on R_obs, can disfavour one law at s ≥ 1.42, because w* = 0.**
  - Rough size, at s = 1.42 with the A2x statistical requirement met: R_obs would need a half-width below about half the 0.06-dex separation, 0.03 dex (se_e ≈ 0.22, about 5–6 times the 51 clean rows at the same scatter, and free of the selection bias).
- **A4 reconciling offset** (the KURVS pipeline offset that would make each law consistent with the measured gas evolution; in dex, and in σ):

  | s | in-repo flat | in-repo rival | literature flat | literature rival |
  |---|---|---|---|---|
  | 1.00 | +0.148 (3.4σ) | +0.082 (1.8σ) | +0.074 (1.7σ) | +0.074 (1.6σ) |
  | 1.42 | +0.174 (3.8σ) | +0.104 (2.3σ) | +0.078 (1.7σ) | +0.058 (1.3σ) |
  | 3.00 | +0.231 (4.2σ) | +0.155 (2.9σ) | +0.092 (1.6σ) | +0.047 (0.9σ) |

  - The check holds: the common-μ (0.67) flat differential is +0.1483, CFG161/167's +0.148.
  - Direction: KURVS needs to sit above KROSS by 0.05–0.23 dex in log g for either law to be consistent with either bracket. That size is inside CFG167's independent-calibration scatter (sd 0.17 dex). It is consistent with CFG170's first explanation (a common pipeline offset) and cannot exclude its second (an in-repo exponent biased low). This confirms the README's statement that the lane cannot separate them.
- **A5 interval convention** (quadrature R exp(± √(a_U² + a_K²)); an open side stays open):

  | s | flat q-interval | rival q-interval | flags in-repo (flat/rival) | flags literature (flat/rival) | both-bracket laws → label |
  |---|---|---|---|---|---|
  | 1.00 | [2.30, 4.84] | [2.73, open] | True/True | False/True | rival → **DIAGNOSTIC** |
  | 1.42 | [2.29, 4.19] | [2.05, 6.62] | True/True | False/False | none → NON-DIAGNOSTIC |
  | 1.62 | [2.29, 4.06] | [1.99, 5.12] | True/True | False/False | none |
  | 1.69 | [2.29, 4.02] | [1.97, 4.84] | True/True | False/False | none |
  | 3.00 | [2.29, 3.83] | [1.88, 3.52] | True/True | False/False | none |

  - So the s = 1 label depends on the interval construction: quadrature reads DIAGNOSTIC, the bootstrap 16–84% interval (A7) and the frozen conservative interval read NON-DIAGNOSTIC (the bootstrap margins are 0.04 for flat and 0.18 for the rival, in R). It is **not** a contradiction of the CFG170 README sentence "no verdict depends on this convention": that sentence is about the open-edge convention of its disclosed departure 1, which is reproduced (P10). It does limit what NON-DIAGNOSTIC at s = 1 means.
- **A6 bracket width:**

  | s | frozen conservative interval, any (k, a) | quadrature interval |
  |---|---|---|
  | 1.00 | NON-DIAGNOSTIC for all 20 (k σ_e, ±a) pairs | DIAGNOSTIC (rival) for a = 0.2 and 0.3 at every k = 1–3; NON-DIAGNOSTIC at a = 0.1 and 0.4 |
  | 1.42 | NON-DIAGNOSTIC for all 20 | DIAGNOSTIC (flat) for a = 0.1 at every k; NON-DIAGNOSTIC otherwise |

  The label depends on the literature allowance (a declared ±20%, "an allowance, not a measured error") as much as on the interval.
- **A7 bootstrap of the root-find error** (B = 300, seed 180; seed 181 in brackets; 16–84% of R):
  - s = 1 flat 2.38–4.81 (2.42–4.55), frozen [1.98, 5.66];
  - s = 1 rival 2.24–16.4 (2.19–18.8), only 174 (194) resamples have a root, frozen [1.58, open];
  - s = 1.42 flat 2.29–4.04 (2.32–4.13), frozen [2.04, 4.73];
  - s = 1.42 rival 2.08–5.72 (2.03–6.15), frozen [1.64, 8.41].
  - **The frozen conservative interval is at least as wide as the resampling interval in all four cases ("adequate"). The quadrature interval matches the resampling interval at s = 1.42 and for flat at s = 1; for the rival at s = 1 the bootstrap lower edge (2.2) is below the quadrature one (2.73), so under a bootstrap interval the rival is not disfavoured by the literature bracket.** My estimate E16 (frozen narrower) was wrong in direction. Seeds agree to 0.03 dex except the rival s = 1 upper edge (0.06 dex, a rooted-subset quantity).
  - For the rival at s = 1, 35–42% of resamples have no break-even: its KROSS root at 0.052 is fragile, so R_rival = 11.9 is not a determinate quantity.
- **A8 e-scan (point R_obs):** no exponent e in [−1, 3.5] leaves flat undisfavoured while disfavouring the rival, at any s. Rival-only-OK (i.e. flat disfavoured, rival not) occurs for e = 1.75–2.25 (s = 1), 2.00–2.25 (1.42), 2.00–2.50 (1.62–3.00); both are OK for e ≥ 2.5 (2.75 at s ≥ 1.62); both disfavoured for e ≤ 1.5–1.75.

### B — sensitivity to the calibration and gas-prior choices  (`CFG180_attacks_B.out`)

- **Verdict: FRAGILE.** Under the frozen literal summary, 14 (variant, s) combinations give exactly one law disfavoured by both brackets: V2c, V8b, V9a, V11a and V14c at both s (all KROSS-side changes that lower KROSS's break-even), V5a at both s, and V11b and V11e at s = 1. **All are against flat.**
  - In 12 of them the rival has NO break-even (it over-predicts KROSS even at μ = 0.01), and the literal rule cannot flag a law with no R. That label is arguably wrong for those cases (the rival is excluded by the KROSS epoch alone). Only V5a (gas scale 3 R_d for KURVS only) has both R defined and exactly one law flagged.
  - Post-hoc, counting "no break-even" as disfavoured (`CFG180_diag_B_nobe.out`): 6 combinations, V5a (flat) and V3a (α × 0.6 for both samples) and V13b (R_e = 2 R_eff for both) against the rival. V3a and V13b are CFG160's own scatter and R_e variants. So the label is fragile under either reading, and the direction of the fragility depends on the reading.
- **Size:** 81 of the (variant, s, law) shifts are ≥ 0.14 dex, spread over 28 of the 43 variants and over every input class. Shifts in log R_flat at s = 1.42: α × 0.6/1.4 on one sample −0.25/+0.16 (KURVS) and +0.30/−0.17 (KROSS); V ± 10% by 0.09–0.31; σ ± 25% by 0.21–0.27; log M* ± 0.1 by 0.14–0.35; gas scale by 0.05–0.21; KROSS sub-samples by 0.06–0.30. Against a separation of 0.06 dex (s = 1.42) and a bracket half-width of 0.14 dex.
- **Direction (c):** R rises when KURVS's α, V or σ_out rise or its M* falls, and when KROSS's α, σ₀ or V fall or its M* rises; the reverse lowers it. **18 of 18 sign expectations held** (E13). The rival's R responds about twice as strongly as flat's to each of them (ratio of log-R shifts 1.5–2.0), so all α/V/σ/mass calibration changes are DIFFERENTIAL (change in the separation ≥ 0.06 dex) rather than common-mode. Only the gas-scale changes (V4a–c, V5a/b), the inclination column (V1), the jackknife of most KURVS discs (V12) and V15 are common-mode (same shift in both laws, separation within 0.03 dex).
- **Others:** V1 (`inc_sfr_deg`) moves R by +0.003/+0.008 dex; V15 (mass-dependent gas at the same median μ) by +0.014/+0.016; the KURVS jackknife ranges R_flat 2.60–3.37 and R_rival 2.69–3.98 at s = 1.42 (the largest single-disc effect is KURVS #8, −0.078 dex).

### C — mock null worlds  (`CFG180_null_mocks_s*.out`, N = 200 per family, seeds 180 and 181)

- The truth law generates the accelerations (real baryons, errors, σ, inclinations, anchor offset inserted so it cancels), μ_true(KROSS) = 0.7, R_true = μ_KURVS/μ_KROSS. Coarser grid (200 points) than the main run, declared.
- **Ideal worlds (F1, R_true = 1, s = 1.42, seed 180 / 181):** flat truth gives R_flat 0.94 [0.71, 1.22] / 0.97 and R_rival 0.19 / 0.23 (no rival break-even in 88 / 77 of 200); the rival's R is not close to flat's. Rival truth gives R_flat 1.30, R_rival 0.75.
  - Labels (in-repo relative width, centred at R_true): flat truth CORRECT-ONLY 0.22 (0.17), WRONG-ONLY 0.00; rival truth CORRECT-ONLY 0.02 (0.00), WRONG-ONLY 0.03 (0.04), NEITHER 0.95.
  - Frozen power test (P(CORRECT-ONLY) ≥ 0.5 and P(WRONG-ONLY) ≤ 0.05): **NO POWER at s = 1.42 and s = 1.00, for both truths.** My estimate E14 (< 0.30) held.
  - With R_true = 2 (F2), flat truth is identified in 0.41–0.54 of mocks at s = 1.42 and rival truth in 0.00, with WRONG-ONLY 0.10.
- **The observed pattern** (both R_law ≥ 2.5 and both disfavoured by the in-repo bracket): flat truth with the +0.15-dex KURVS offset (F3) gives R_flat 2.05 and R_rival 1.50 and reproduces the pattern in 0.03–0.05 of mocks (WRONG-ONLY 0.47: the mock labels the TRUE law disfavoured); rival truth + offset gives R_flat 2.56 and R_rival 2.16 (BOTH 0.62) and the pattern in 0.17–0.18 (s = 1.42), 0.20–0.23 (s = 1); random-offset worlds (F4, sd 0.17 dex) 0.13–0.16.
  - Frozen meaning line "reproducible by a null: P(pattern) ≥ 0.2": met only at the edge, by a rival-truth world with the offset at s = 1 (0.23 and 0.20); missed everywhere else.
  - **My estimate E15 (a flat world + 0.15 dex offset gives R_flat ≈ 3) was wrong:** it gives 2.05. The real data (R_flat 3.1) need D ≈ +0.17 at s = 1.42 (A4), and a mock world with only 0.7 M* of gas is not the real one.
  - **Observation from F1 → F3:** the separation |log R_flat − log R_rival| is 0.5–0.7 dex at moderate gas and collapses to 0.07–0.13 dex when the world is forced to R ≈ 2–2.5. That is the observed situation (R ≈ 3, separation 0.06). I read it as the loss of a₀-dependence when the required gas is high (both laws approach their Newtonian limit). This is a hypothesis from the mocks, not a separate calculation.
- **Post-hoc, labelled:** with μ_true(KROSS) = 1.5 (fewer floored discs) the flat-truth F1 gets P(CORRECT-ONLY) 0.65–0.70 (HAS POWER), and the rival truth still 0.01–0.02. The frozen μ_true = 0.7 is the one that binds; the frozen result stands.
- **Caveat carried over from CFG165:** 3.4 of 10 KURVS and 26.5 of 390 KROSS discs (F1, s = 1.42) have V² floored, because the P4 pressure term α σ² exceeds g R at μ = 0.7. The mocks are worlds in which the correction is too large for the gas; the floor may be why R_flat is recovered 0.03 dex low (0.94 for R_true = 1; not tested separately).
- **Monte Carlo noise:** seeds 180 and 181 differ by up to 0.13 in a label fraction (typically 0.03–0.08) and by 0.02–0.03 in the pattern fraction. No conclusion above rests on a difference smaller than 0.15.

## 5. Hand-estimate scorecard (frozen section 3; wrong expectations kept)

| # | estimate | result |
|---|---|---|
| E1 | C1 2.109 / 0.621 (1e-3) | 2.10898 / 0.62107 (in) |
| E2 | KROSS s = 1: 0.636; rival 0.052 | 0.636; 0.052 (in) |
| E3 | 16 central μ_be within 1.5% | in (worst 0.05%) |
| E4 | R_flat(1) 3.32; R_rival(1) 11.9 | 3.316; 11.939 (in) |
| E5 | ≥ 90% of edges within 4% (convention A) | 39/39, worst 1.1% (in); E5b in |
| E6 | matrix exact | in |
| E7 | R_obs numbers | in |
| E8 | calibration rows | in |
| E9 | quadrature flips s = 1 to DIAGNOSTIC; stays NON-DIAGNOSTIC at s ≥ 1.42 (hand calc R_lo,q ≈ 2.7 and ≈ 2.3) | **in**: rival 2.73, flat 2.30; label DIAGNOSTIC at s = 1, NON-DIAGNOSTIC at s ≥ 1.42 |
| E10 | A1: w* = 0 both truths at s ≥ 1.42; s = 1 flat truth 0, rival truth ≈ 0.32 | in (0.000, 0.324) |
| E11 | A2: intervals disjoint at f* ≈ 0.15 (N × 45), f* < 0.3 (0.80); anchor floor leaves them marginal (0.50) | **wrong** for the frozen A2: intervals are not disjoint at any f at any s (floor-limited). The floor claim was right; the f* value was wrong. The post-hoc A2x gives 0.1 (N × 100) at s = 1.42 (quadrature 0.15, N × 44) |
| E12 | A4 offsets: flat +0.15 (0.12–0.18), rival +0.08 (0.04–0.12) at s = 1; flat +0.12 (0.09–0.16) at s = 1.42 | in at s = 1 (+0.148, +0.082); **wrong at s = 1.42** (flat +0.174) |
| E13 | 18 signs | 18 of 18 |
| E14 | ideal flat truth P(CORRECT-ONLY) < 0.30 at s = 1.42 | 0.22 / 0.17 (in) |
| E15 | flat + 0.15 dex offset gives R_flat ≈ 3 ± 0.7 | **wrong**: 2.05 |
| E16 | frozen interval narrower than the bootstrap (0.50) | **wrong**: wider in all four cases; the quadrature interval tracks the bootstrap |
| E17 | all pass lines met (0.30) | met |
| M1–M6 | M3 bites at 0.8 (with R_flat up) | **M3 did not bite**; the direction was down (−12%) |

## 6. What would count as disagreement, and what I found

- **Any pass line missed:** none. **Cell of the matrix or summary label differing:** none. **The two rule forms disagreeing:** none. **P10:** exactly the rival at s = 1.
- **Valid disagreements with the weight of the CFG170 wording (numbers all reproduce):**
  1. NON-DIAGNOSTIC at s = 1 depends on the conservative interval and on the ±20% literature allowance (A5, A6), and on a break-even (rival KROSS 0.052) that 35–42% of resamples do not have (A7).
  2. Its s ≥ 1.42 form is robust to the interval convention but structurally non-diagnostic (A1, A2): the root-find intervals, not R_obs, swamp the separation, a reason stronger than the README's "0.01–0.06 dex against a 0.28-dex bracket".
  3. B is FRAGILE: single-input calibration changes flip the frozen summary in 14 combinations, and the frozen summary rule cannot label a law with no break-even.
  4. CFG170's MUTATE controls are evaluator-only (framing); A3 finds the in-repo and literature exponents 4.4σ apart, so "the two brackets disagree" is a 4.4σ statement, not a difference of taste.
- **Not a disagreement:** shared-pipeline physics (ν_mono, α(x), P4, selections), untested here.

## 7. Files and re-run

Scratch dir (nothing in the repo): `CFG180_FROZEN_CRITERIA.md`, `README.md`, `CFG180_lib.py`, `CFG180_two_epoch_referee.py` (main and MUTATE), `CFG180_attacks_A.py`, `CFG180_attacks_B.py`, `CFG180_null_mocks.py`, `CFG180_diag_post.py` (post-comparison), `CFG180_diag_B_nobe.py` (post-hoc), `run_all.sh`; outputs `CFG180_main.out`/`_results.json`, `CFG180_MUTATE_{1..6}.out`/`_results.json`, `CFG180_attacks_A.out`/`_results.json`/`_seed181`, `CFG180_attacks_B.out`/`_results.json`, `CFG180_null_mocks_s{1.42,1.00}_seed{180,181}.out`/`_results.json` and the `_muK1.5_POSTHOC` pair, `CFG180_diag_post.out`, `CFG180_diag_B_nobe.out`, `CFG180_manifest.txt` (sha256 of inputs, scripts and outputs), `run_all.out`.

```
export ZF_REPO=<repo>
bash run_all.sh      # ~7 min; main 0; MUTATE 1,2,4,5,6 rc 1 (bite), MUTATE 3 rc 0 (does not bite); attacks 0; mocks 0
```

κ = ½ and Ω_c h² stay fitted. a₀(z) flat is the framework's distinctive law; a₀ ∝ H(z) the rival. Nothing here says the data favour either model, or that the theory is closed.

## Provenance note (append-only; reported by the calc chat in 27bcce5a4, with the data chat's digitisation in 5e8617c81; no verdict changes)

The KURVS outer velocity that every a0(z) lane read, `v_at_last_point_kms` (the paper's Table B1 column 3), is the authors' fitted exponential-disc MODEL evaluated at R_max, not a measured data point: the data chat's digitisation shows model(R_max)/sin i_SFR equals it to about 1% for all ten discs. This lane imports the same column through the CFG165 loader, so it reproduced its target as that lane ran it; the note changes what the column means, not what was reproduced. The calc chat re-runs the test with the measured markers as CFG189 (criteria frozen first). Recorded here as reported and not re-verified by this lane's author.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 1, 2, 4, 5, 6 exit 1 (bite); MUTATE 3 exit 0 (does not bite, kept); attacks A (seeds 180 and 181), attacks B, the null mocks (s = 1.42 and 1.00, seeds 180 and 181), the labelled post-hoc pair and both diagnostics exit 0. Every `.out` and `_results.json` is identical to the referee's apart from timing lines. The final line of `run_all.out` shows one difference from the referee's: the manifest step could not find `CFG180_FROZEN_CRITERIA.md`, which sits one directory up (`../CFG180_FROZEN_CRITERIA.md`, c2a256648); the committed `CFG180_manifest.txt` was regenerated by the orchestrator with that file copied in temporarily, so its hashes of the timing-bearing `.out` files differ from the referee's. Independence stops at the imported CFG165 module.
