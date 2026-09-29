# CFG180 — Referee re-derivation of CFG170 (the two-epoch gas-ratio test, KROSS z ≈ 0.85 vs KURVS z ≈ 1.5): FROZEN CRITERIA (phase 1)

(Lane number: originally announced as CFG176; renumbered CFG180 by the coordinator. The scratch dir keeps its cfg176 name.)

Written 2026-09-29, before any CFG180 script exists and before any CFG180 number is computed.
Nothing below may change after a result is seen; later deviations go in the README as disclosed departures.

## 0. Ground rules, and what this phase read

- **Phase 1 read only:** `CFG170_FROZEN_CRITERIA.md`, `CFG170_README.md`, the READMEs of CFG160, CFG162 and CFG164, and the READMEs of CFG165, CFG166, CFG167 and CFG168. Files were located by `ls`/`grep` of names. I also read the `def` signatures and the `load_kross`, `gbar`, `corr`, `per_object`, `pool`, `anchor_pool`, `cell`, `classify` bodies of `CFG165_referee_kurvs_p4.py` (I may import that file; it is my own earlier referee module).
- **NOT opened in phase 1:** `CFG170_two_epoch_gas_ratio.py`, every CFG170 `.out` and `_results.json` (including `_firstrun*` and `_MUTATE*`), and every data file. Data files are opened only when my phase-2 scripts read them.
- **The README numbers below are TARGETS I read, not blind predictions.** My hand estimates (section 3) were made after reading the README and are labelled so.
- **Phase 2 order:** my scripts written from this file alone → main run, MUTATE runs, attacks and mocks all run and saved → ONLY THEN CFG170's script, `.out` and `.json` opened → `CFG180_diag_post.py` written after that (labelled post-comparison; not part of any frozen result).
- **Standing rules:** κ = ½ is FITTED; a₀(z) FLAT is the framework's distinctive law and a₀ ∝ H(z) the rival; nothing here says the data favour either law or the framework; a lean is not a detection; failed controls and wrong expectations are kept, never repaired. Repo untouched; no network; no new downloads; no absolute home path printed (`<repo>` is printed; the repo is found from `ZF_REPO` or by walking up from `__file__` until a directory containing `data_assembly/` is found).

## 1. What is re-derived, and where independence STOPS

### Re-derived here from the CFG170 frozen text and README alone
- the break-even gas fraction μ_be of each law for each sample at each prescription s (my own root-finder);
- the 1σ root-find interval on μ_be, R_law and its conservative interval, the open-edge convention;
- R_obs (in-repo and literature brackets) from the samples' median z and M*;
- the disfavoured/not rule, the matrix, the R0 power row, the summary label;
- both CFG170 controls (C1, C2) and my own MUTATE controls;
- every attack in section 6 and the mock-null study.

### Imported read-only from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` (SHARED, NOT INDEPENDENT)
Imported by a path insert, with `MUTATE` forced to `"0"` during the import and restored afterwards (the module reads it at import for its own harness):
- `load_kurvs(ids, inc_col)`, `load_kross()`, `load_sparc_anchor()`;
- `per_object`, `pool`, `anchor_pool`, `cell`, `classify` (used only for C2's cross-check), `corr`, `spec`, `gbar`, `gpred`, `enclosed`, `alpha_K`, `E_of_z`, `KURVS_IDS`;
- and through it `CFG4_common` (`nu_mono`, a₀ constants).

Consequences, stated before the data:
1. CFG165, CFG167 and CFG168 already showed that this shared pipeline reproduces CFG160 (KURVS), CFG161 (KROSS at μ = 0.67) and CFG162 (KURVS break-evens 2.109 / 0.621). So an agreement with CFG170 on the KURVS/KROSS Δ′(μ) function is NOT an independent check of that function. It checks that the CFG170 text plus this pipeline determine the numbers.
2. What is independent here: the root-finding, the interval construction, R_law, R_obs, the rule, and the attacks. The mock generator is new code.
3. Also shared and not tested: Kretschmer's α(x) as quoted; ν_mono; the CFG140 set-up (thin exponential discs, spherical surrogate, gas bracket, mass error 0.15, ±5° inclination); the KROSS selection as coded in `load_kross` (390 discs; RT and RT+, v/σ₀ ≥ 1); all data tables.
4. **Conventions I fix (declared before any number):**
   - KURVS inclination column `inc_star_deg` (CFG140's; CFG168 showed it reproduces 2.109 / 0.621). `inc_sfr_deg` is an attack variant.
   - KURVS uses `sig` = σ_out (from the module), KROSS σ₀; R_e = R_eff (Refac = 1); gas scale 2 R_d; the anchor is SPARC's pooled flat offset at the same s, as in `cell()`.
   - The prescription placements are the rounded s values of the CFG170 frozen text: s ∈ {0, 1.00, 1.42, 1.62, 1.69, 3.00}, implemented as `spec("P4", scale=s)` for both samples and for the anchor. (CFG168's unrounded s_eq are 1.422 / 1.617 / 1.688 / 3.001; the difference is a declared tolerance, not a bug.)
   - **R_obs constants are INPUTS, not re-derived in the main run:** in-repo e = +0.23 ± 0.52 and mass slope −0.30; literature exponent 2.5, mass slope −0.36, ±20%. The in-repo fit is re-derived only in attack A3 (from `phibss13_joined.csv`, with the selection rule read from the CFG164/166 READMEs: 73 rows → 51 clean). If my row selection does not give 51 rows, A3 reports the row count and stops there. The main matrix always uses the README constants.

## 2. Headline pinned (README targets, read not predicted)

- **Verdict:** NON-DIAGNOSTIC. No law is disfavoured by both brackets at s = 1.
- **R_obs:** in-repo 1.00, 2σ [0.73, 1.39]; literature (ABSTRACT-LEVEL) 2.02 [1.61, 2.42]. (1 + z) ratio 1.3669; mass factors 0.935 (in-repo) and 0.923 (literature); median log M* 10.14 (KURVS), 10.04 (KROSS); median z 1.53 and 0.85.
- **μ_be, KURVS / KROSS, [1σ root interval]** (target table; "no be" = no break-even):

| s | flat KURVS | flat KROSS | rival KURVS | rival KROSS |
|---|---|---|---|---|
| 0 | no be | no be | no be | no be |
| 1.00 | 2.109 [1.596, 2.705] | 0.636 [0.478, 0.805] | 0.621 [0.289, 1.006] | 0.052 [< 0.01, 0.185] |
| 1.42 | 3.096 [2.423, 3.887] | 0.998 [0.820, 1.188] | 1.257 [0.822, 1.766] | 0.352 [0.211, 0.504] |
| 1.62 | 3.565 [2.808, 4.462] | 1.166 [0.979, 1.367] | 1.567 [1.076, 2.144] | 0.494 [0.344, 0.655] |
| 1.69 | 3.730 [2.942, 4.665] | 1.225 [1.035, 1.429] | 1.676 [1.165, 2.279] | 0.544 [0.391, 0.707] |
| 3.00 | 6.845 [5.407, 8.611] | 2.301 [2.050, 2.569] | 3.829 [2.873, 4.994] | 1.475 [1.267, 1.698] |

- **R_law [interval]:**
  - flat: 3.32 [1.98, 5.66] at s = 1; 3.10 [2.04, 4.74] at 1.42; 3.06 [2.06, 4.56] at 1.62; 3.04 [2.06, 4.51] at 1.69; 2.97 [2.11, 4.20] at 3.00.
  - rival: 11.9 [1.56, open] at s = 1; 3.57 [1.63, 8.39] at 1.42; 3.17 [1.64, 6.23] at 1.62; 3.08 [1.65, 5.83] at 1.69; 2.60 [1.69, 3.94] at 3.00.
- **Matrix:** in-repo bracket disfavours flat AND rival at every s ≥ 1; literature bracket disfavours neither at any s.
- **Calibration scatter (Kretschmer only):** R_flat = 4.26 at s = 0.6 and 3.11 at s = 1.4; R_rival has no break-even at s = 0.6 (over-predicts KROSS even at μ = 0.01) and is 3.63 at s = 1.4.
- **Controls:**
  - C1: KURVS s = 1 break-evens 2.109 flat / 0.621 rival (1e-3);
  - C2: KROSS anchor-corrected Δ′ at μ = 0.67, s = 1 is −0.004 flat / −0.082 rival (3 decimals; CFG165's committed −0.0042 / −0.0821).
- **R0 power:** |log R_flat − log R_rival| = 0.56 dex at s = 1 and 0.01–0.06 dex at s = 1.42–3.00, against a 0.28-dex in-repo bracket width.
- **Explanatory checks in the README:** at s = 1, R in (1 + μ) is 1.90 flat and 1.54 rival; at μ = 0.01 the KROSS rival Δ′ at s = 1 is +0.0065 ± 0.020.

## 3. Hand ESTIMATES (made AFTER reading the README; labelled; scored in the README)

"P" is my probability that my phase-2 number falls inside the stated line.

| # | estimate | line | P |
|---|---|---|---|
| E1 | C1: KURVS s = 1 break-evens 2.109 / 0.621 | 1e-3 | 0.90 |
| E2 | KROSS s = 1: flat 0.636; rival 0.052 (near the μ = 0.01 floor) | flat 1%; rival 10% or 0.006 abs | 0.80; 0.60 |
| E3 | KURVS and KROSS central μ_be at s = 1.42–3.00, all 16 values | each 1.5% | 0.75 |
| E4 | R_flat(s = 1) = 3.32; R_rival(s = 1) = 11.9 | 2%; 5% | 0.80; 0.55 |
| E5 | intervals: ≥ 90% of the 40 μ edges within 4% under convention A (σ frozen at μ_be) | 4% | 0.50 |
| E5b | under A or B (σ recomputed at each μ), the better one matches at that level | 4% | 0.75 |
| E6 | the full matrix (5 s × 2 laws × 2 brackets) reproduces exactly | exact | 0.85 |
| E7 | R_obs numbers of section 2 | ±0.02 / ±0.03 | 0.90 |
| E8 | s = 0.6 / 1.4 rows (4.26, none, 3.11, 3.63) | 3% / 4% | 0.70 |
| E9 | **quadrature attack A5 flips s = 1 to DIAGNOSTIC (against the rival)**; stays NON-DIAGNOSTIC at s = 1.42–3.00 | hand calc from README edges: rival R_lo,q ≈ 2.7 > 2.42, flat R_lo,q ≈ 2.3 < 2.42 | 0.60 (s = 1); 0.80 (s ≥ 1.42) |
| E10 | A1 required distance is 0 for BOTH truths at s ≥ 1.42; s = 1: flat-truth 0, rival-truth ≈ 0.32 dex | ±0.05 dex | 0.85; 0.70 |
| E11 | A2: intervals become disjoint at s = 1.42 only for f* ≈ 0.15 (N × ≈ 45; range 15–500) and the anchor floor alone leaves them marginal | f* < 0.3 | 0.80; floor-limited 0.50 |
| E12 | A4 reconciling offset (dex, KURVS log g needed to reconcile R_obs = 1.00): flat +0.15 (0.12–0.18), rival +0.08 (0.04–0.12) at s = 1; flat +0.12 (0.09–0.16) at s = 1.42 | as stated | 0.70 |
| E13 | signs in section 6-B (table there) | sign | 0.75 each |
| E14 | mocks: ideal, flat truth, R_true = 1: P(correct-only label) < 0.30 at s = 1.42 | — | 0.85 |
| E15 | mocks: flat truth + KURVS offset +0.15 dex, R_true = 1: R_flat ≈ 3 ± 0.7 at s = 1.42 (the observed pattern is reproduced) | — | 0.70 |
| E16 | bootstrap A7: the frozen root-find interval is narrower than the 16–84% resampling interval for R_law at s = 1.42 (KURVS has only ten discs) | — | 0.50 |
| E17 | joint: every pass line of section 4 met | — | 0.30 |

## 4. Exact pass lines (reproduction of CFG170's README)

The convention risks I know of (which sigma the ±σ roots use; the inclination column; the rounded s) go into the tolerances below. All lines are declared now.

- **P1 controls.** C1 to 1e-3; C2 to 0.001. Failing either makes the main run exit 2 (the run still prints everything).
- **P2 central μ_be** (20 values plus the s = 0 "no break-even" flags): relative 1.5% each. Exception: KROSS rival at s = 1, 10% or 0.006 absolute. The six "no break-even" cells at s = 0 must be "no break-even" exactly.
- **P3 intervals.** Convention A is primary: σ_Δ′ evaluated once at the central root, then the roots of Δ′ = ±σ. Convention B is a variant: σ_Δ′(μ) recomputed at each μ. The line is 4% per edge, ≥ 90% of edges, with the open edges identical (KROSS rival s = 1 lower edge < 0.01; the s = 0.6 rival no-root). Each convention's result is printed. The verdict is "REPRODUCES" if A or B passes; the convention that passes is named.
- **P4 R_law.** Centre 2%; edges 6% (rival at s = 1: R_lo 5%; R_hi must be open).
- **P5 R_obs.** In-repo 1.00 ± 0.02, [0.73, 1.39] ± 0.03; literature 2.02 ± 0.03, [1.61, 2.42] ± 0.03; median z 1.53 and 0.85 ± 0.01; median log M* 10.14 / 10.04 ± 0.01; (1 + z) ratio 1.3669 ± 0.001; mass factors 0.935 / 0.923 ± 0.005.
- **P6 matrix and label:** exact, all 20 flags plus "n/a" at s = 0. The frozen rule is implemented in BOTH forms (literal text: the gap to the nearest bracket edge exceeds R_law's 1σ half-interval on that side; and interval overlap). They must agree in every cell (this tests the README's claim that the rule reduces to overlap).
- **P7 the s = 0.6 / 1.4 rows:** 3% (4.26, 3.11); rival s = 0.6 "no break-even" exact; rival s = 1.4 = 3.63 within 4%.
- **P8 R0:** 0.56 ± 0.02 dex at s = 1; 0.01–0.06 dex at s = 1.42–3.00 within 0.01 dex each.
- **P9 explanatory checks:** R in (1 + μ): 1.90 / 1.54 (0.03); KROSS rival Δ′ at μ = 0.01, s = 1: +0.0065 ± 0.003 (σ 0.020 ± 0.003).
- **P10 README's departure claim:** with the first-run convention (any missing ±σ edge root gives "no break-even") exactly ONE row changes, the rival at s = 1 (README disclosure 1). Pass = exactly that row and no verdict flag change.
- **Overall label:** "REPRODUCES" only if P1–P6 pass; "PARTIAL" if P1 and P6 pass with P2–P5 partly out; "DISAGREES" otherwise. Every failing row is printed with its size.

## 5. MUTATE controls (each flips a load-bearing cell; exit 1 = the control bites, exit 0 = it does not bite and is kept)

`MUTATE=k python3 CFG180_two_epoch_referee.py`. Each run uses my whole pipeline with one change and reports the baseline value beside the mutated one. Bite lines are pinned now.

| k | mutation | load-bearing cell | bites iff |
|---|---|---|---|
| M1 | KURVS observed velocities (and errors) × 10^0.3 | μ_be(KURVS) → R_flat at s = 1.42 | R_flat(1.42) rises by more than 50% over baseline |
| M2 | the two laws swapped inside the break-even solver (flat solved with the rival's a₀(z) and vice versa) | R_flat(s = 1) and the matrix | mutated R_flat(1) is within 5% of the baseline R_rival(1) AND differs from the baseline R_flat by more than a factor 2 |
| M3 | KROSS gas / pressure radius R = r_im (not 2 r_im), so x = 0 and α = 1.475 s | KROSS μ_be and R_flat at s = 1.42 | R_flat(1.42) changes by more than 25% (either sign) |
| M4 | R_obs replaced by R_flat(s = 1.42) with the in-repo bracket's relative width | flat's in-repo disfavoured flag at s = 1.42 | flat flips from disfavoured to not disfavoured |
| M5 | R_obs replaced by 10 × R_flat(s = 1.42) (in both brackets' relative widths) | flat's literature-bracket flag at s = 1.42 (baseline: not disfavoured) | flat flips to disfavoured |
| M6 | μ search range restricted to [0.01, 1.0] | KURVS flat μ_be at s = 1 (2.109) | the KURVS flat root becomes "no break-even" and R_flat(1) is undefined |

Expectations before the run (hand): M1 bites (P 0.95), M2 bites (0.9), M3 bites (0.8; the direction is uncertain, I expect R_flat up because KROSS's break-even falls with lower α), M4 bites (0.95), M5 bites (0.95), M6 bites (0.95). A control that does not bite is reported as such.

## 6. The attacks (frozen procedures; N and seeds pinned; every result labelled a sensitivity, not a change of the frozen headline)

### A — Is the NON-DIAGNOSTIC verdict robust, and what would a diagnostic result have required?  [script `CFG180_attacks_A.py`]

- **A1 structural required precision.** For each s ∈ {1, 1.42, 1.62, 1.69, 3.00} and each truth ∈ {flat, rival}: treat the truth law's central R_law as the measured R_obs, and take the distance in dex from that R to the OTHER law's 1σ interval (0 if inside).
  - Call w*(truth, s) that distance. A bracket half-width w on R_obs (in dex) makes the wrong law disfavoured only if w < w*.
  - Meaning: "STRUCTURALLY NON-DIAGNOSTIC at s" if w* < 0.02 dex for both truths (no R_obs precision helps: the wrong law's own root-find interval already contains the right law's R). "R_obs-limited at s" if w* ≥ 0.07 dex for at least one truth (0.07 dex = the in-repo 1σ bracket half-width, exponent se 0.52 × log10 1.3669).
  - Also print the descriptive R_obs windows: for a zero-width R_obs, the ranges of R_obs where exactly one law is disfavoured, at each s.
- **A2 sample-size requirement.** Scale each sample's Δ′ error as σ_f = sqrt(f² σ_raw² + σ_anchor²) (the anchor pooled error is a floor that more discs cannot lower), with f on the grid {1, 0.7, 0.5, 0.35, 0.25, 0.15, 0.1, 0.05, 0}, and recompute the ±σ_f roots and both laws' R_law intervals.
  - Report for each s the largest f at which the flat and rival intervals are disjoint (f*), the disc-number factor 1/f*², and whether f = 0 (the anchor floor alone) is already disjoint.
  - Meaning: "reachable with more discs" if f* ≥ 0.1 (a factor ≤ 100 in N); "floor-limited" if the intervals are not disjoint even at f = 0; anything else "N-hungry".
- **A3 R_obs precision from data already in the repo.** Re-fit log μ = a − b (log M* − 10.5) + e log(1 + z) on the clean PHIBSS rows of `phibss13_joined.csv` (selection: the CFG164/166 README description; if the count is not 51, print the count and stop A3). Report e ± se, and e ± se for the z-only fit and for the fit restricted to z < 1.7. Convert the se to a dex half-width on R_obs (× log10 1.3669) and compare with A1's w*.
  - Also print: the exponent separation between the in-repo e and the abstract-level 2.5 in units of the in-repo se (algebra: (2.5 − 0.23)/0.52 = 4.4σ).
  - Also print the sample-size formula: the se scales as 1/√n, so the number of clean rows needed for a given w*.
  - Meaning: "no existing in-repo dataset suffices" if the best se gives a half-width larger than the smallest w* > 0 (or if w* = 0 everywhere).
  - I open no other gas dataset for this. Candidates found by name only (`sharma2024_gs21b.csv`, `romanoliveira2023_gasmasses.csv`, `budhies_hi.csv`, `mightee_hi_highz/`) are listed but not used unless a phase-2 script's column check shows a z ≈ 0.85–1.5 gas-mass column; then A3 adds one row and says so.
- **A4 reconciling offset (the direction of the R mismatch).** For each s, bracket and law: μ_K = μ_be(KROSS) and μ_U = R_obs × μ_K. The reconciling offset is KURVS's anchor-corrected Δ′(μ_U) in dex, and its ratio to σ_Δ′. It is the common KURVS-minus-KROSS pipeline offset that would make the law consistent with the measured gas evolution. Compare with CFG161/167's differential D = +0.148 ± 0.044 at a common μ (which equals the R_obs = 1 reconciling offset by construction, a check).
- **A5 interval convention.** Recompute the matrix and the summary with the quadrature interval: R_lo,q = R exp(−√(a_U² + a_K²)), R_hi,q = R exp(+√(b_U² + b_K²)), where a_U = ln(μ_U/μ_U,lo), b_U = ln(μ_U,hi/μ_U), a_K = ln(μ_K,hi/μ_K), b_K = ln(μ_K/μ_K,lo). A missing edge root leaves that side open. Meaning: "convention-fragile" if the frozen summary (exactly one law disfavoured by both brackets at s = 1) changes. The frozen conservative interval is unchanged as the headline.
- **A6 bracket width.** In-repo bracket at k σ_e with k ∈ {1, 1.5, 2, 2.5, 3}; literature at ±{10, 20, 30, 40}%. Report the summary at s = 1 and s = 1.42 for each pair (frozen and quadrature intervals).
- **A7 resampling check of the root-find error.** B = 300 bootstrap resamples of the ten KURVS discs (with replacement) and of the KROSS discs, seed 180, at s = 1 and 1.42; recompute μ_be and R_law. Report the 16–84% interval of log R_law and compare with the frozen interval. Meaning: the frozen root-find interval "under-covers" if the resampling interval is wider than the frozen conservative interval on either side by more than 0.03 dex; "adequate" otherwise. (The re-run at seed 181 must agree within 0.03 dex.)
- **A8 e-scan.** For the point-bracket R_obs(e) = 1.3669^e × 0.935 with e from −1 to 3.5 in steps of 0.25, print which laws are not disfavoured at each s (frozen intervals). Meaning: does any e disfavour exactly one law at s ≥ 1.42?

### B — Sensitivity of the gas-ratio construction to the calibration and gas-prior choices found by CFG165–168  [script `CFG180_attacks_B.py`]

Variants are run at s = 1.42 (primary) and s = 1.00, each reporting R_flat, R_rival with intervals, both brackets' flags, and the log shift from baseline. Deterministic; no random draws. Each variant changes ONE input.

| id | change | origin |
|---|---|---|
| V1 | KURVS `inc_sfr_deg` instead of `inc_star_deg` | CFG165 |
| V2a/b | α scale × 0.6 / × 1.4 on KURVS only; V2c/d the same on KROSS only (independent calibration errors) | CFG167 |
| V3a/b | α scale × 0.6 / × 1.4 on both and on the anchor (common) | CFG160/167 |
| V4a–c | gas scale 1 / 3 / 4 R_d in both samples | CFG165 (b), CFG168 |
| V5a/b | gas scale 3 for KURVS only / 3 for KROSS only | CFG168 |
| V6 | anchor offset: median 0.064 instead of the pooled 0.092, both samples | CFG168 |
| V7a/b | KURVS V × 1.10 / × 0.90 | CFG168 (d1) |
| V8a/b | KROSS V × 1.10 / × 0.90 | CFG168 (d1) |
| V9a/b | KROSS σ₀ × 0.8 / × 1.25 (instrument, beam smearing) | CFG160 untested list |
| V10a/b | KURVS σ_out × 0.8 / × 1.25 | CFG160 |
| V11a–e | KROSS sub-samples: RT only; b/a > 0.5; v/σ₀ ≥ 2; v/σ₀ ≥ 3; drop the 5% lowest-error discs | CFG167 (c) |
| V12 | KURVS jackknife: drop each of the ten discs (ten runs) | CFG168 |
| V13a/b | R_e = 2 R_eff (with Refac_anchor also 2) for KURVS only / both samples | CFG160/165 |
| V14a–d | log M* zero-point + 0.10 and − 0.10, KURVS only and KROSS only (independent stellar-mass pipelines) | CFG167 |
| V15 | per-disc gas: μ scaled ∝ (M*/10^10.5)^(−0.22) (the CFG164 mass slope) in both samples, normalised to the same median μ | CFG164/166 |

- **Pass/fail meanings:**
  - "the NON-DIAGNOSTIC verdict is ROBUST" iff no single variant makes exactly one law disfavoured by both brackets at s = 1 (the frozen summary) AND none does so at s = 1.42 under the extended reading (same rule at s = 1.42). Otherwise "FRAGILE" and the variants are listed.
  - Each variant is classed COMMON-MODE if log R_flat and log R_rival move by the same sign and their difference (the separation) changes by < 0.03 dex; DIFFERENTIAL if the separation changes by ≥ 0.06 dex; otherwise MIXED.
  - "moves as much as the bracket" if |Δ log R| ≥ 0.14 dex (the in-repo 2σ half-width).
- **Direction expectations (hand, E13):**
  - R_law up: V2a/b (KURVS α up), V7a (KURVS V up), V10b (KURVS σ_out up), V8b (KROSS V down), V9a (KROSS σ₀ down), V2c (KROSS α down);
  - R_law down: V2d, V7b, V10a, V8a, V9b, and V14 with KURVS log M* raised (more KURVS predicted baryons lowers μ_be(KURVS)); in general any change that raises KURVS's predicted baryons or KROSS's observed g pushes R down, and the reverse pushes it up;
  - V3a/b: R_flat falls as s rises (the README's s = 0.6 → 4.26, 1.4 → 3.11);
  - V4, V5, V6, V13 and V15: sign not predicted (the sign depends on the radii and where each sample's root sits); I will report them as they come.

### C — What a null would have looked like: mock two-epoch worlds  [script `CFG180_null_mocks.py`, argument s]

- **Mock construction (new code):**
  - Truth = the real discs' baryons (with the real M*), σ_out / σ₀, errors, inclinations, and the real anchor.
  - For each mock, draw per-disc stellar-mass errors ε_M ~ N(0, mass_err) applied to the TRUE baryons (the assumed baryons stay at the catalogue), inclination errors δi ~ N(0, 5°) (V_obs = V_true sin i_true / sin i_meas), and velocity noise N(0, eV).
  - True observed acceleration g = 10^{off} × ν-law(g_bar,true(μ_true), a₀ × (1 or E(z))), where "off" is the sample's pipeline offset: the anchor-pooled flat offset (0.092) is inserted in every world so the anchor subtraction cancels (declared: offset-consistent mock), plus the family's KURVS offset D.
  - V_mock² = g R − α s σ² floored at 0.25% of g R (the CFG165 floor; the floored fraction is printed).
  - The full analysis (my main pipeline, including the ±σ roots and R_law) is applied to each mock at the given s.
- **Families (each: N = 200 mocks per family, seed 180, re-run at seed 181; s ∈ {1.00, 1.42}, run as two script invocations):** truth law ∈ {flat, rival}, μ_true(KROSS) = 0.7, and:
  - F1: R_true = 1.0 (gas does not evolve), D = 0;
  - F2: R_true = 2.0, D = 0;
  - F3: R_true = 1.0, D = +0.15 dex on KURVS log g (a common KURVS–KROSS pipeline offset of the size CFG161 found);
  - F4: R_true = 1.0, D drawn per mock ~ N(0, 0.17) dex (the independent-calibration systematic of CFG167's plain answer 1).
- **Reported per family:** median and 16–84% of R_flat and R_rival (with "no break-even" fractions); the fraction of mocks whose frozen-rule label (one bracket, centred at R_true with the in-repo relative width [0.73, 1.39] / 1.00, and again with ±20%) is CORRECT-ONLY (the wrong law disfavoured and the true law not), WRONG-ONLY, BOTH, NEITHER; and whether the mock reproduces the observed pattern (both R_law ≥ 2.5 and both disfavoured by the in-repo bracket).
- **Meaning:**
  - The test "has power" at (s, truth) if in F1 P(CORRECT-ONLY) ≥ 0.5 and P(WRONG-ONLY) ≤ 0.05.
  - The observed pattern is "reproducible by a null" if F3 or F4 with either truth gives P(pattern) ≥ 0.2.
  - What the null looks like: R_flat and R_rival both ≈ R_true × 10^{D/slope}, i.e. the two laws' R move together.

### D — Extras (declared, unscored)

- The (1 + μ) ratios at every s, for both laws.
- The R_law obtained if KROSS and KURVS both use the same fixed gas scale as a fraction of R_eff.
- The number of discs with a floored V_mock, per family.

## 7. Script plan (all in the scratch dir; nothing in the repo; each < 15 min)

| file | contents | run |
|---|---|---|
| `CFG180_lib.py` | shared helpers of mine: repo finder, the guarded CFG165 import, `delta_prime(sample, μ, s, law, …)`, the root-finder (log-bracket grid of 400 points in [0.01, 30], `brentq`, count of sign changes), interval roots A and B, R_law with open edges, R_obs, disfavour rule (both forms), the mock generator | imported |
| `CFG180_two_epoch_referee.py` | main (sections 2, 4) and `MUTATE=1…6` | `python3 CFG180_two_epoch_referee.py > CFG180_main.out`; `MUTATE=k …` writes `CFG180_MUTATE_k.out/_results.json`; est. < 2 min |
| `CFG180_attacks_A.py` | A1–A8 | seed 180, N = 300 bootstrap; est. 3–6 min |
| `CFG180_attacks_B.py` | V1–V15 | deterministic; est. 5–10 min |
| `CFG180_null_mocks.py` | C; `python3 CFG180_null_mocks.py 1.42` and `… 1.00`, seeds 180 and 181 | est. < 12 min per invocation; if a run would exceed 15 min, N is reduced only by splitting families across invocations, never below 200 per family |
| `CFG180_diag_post.py` | phase 2, AFTER my runs are saved: reads CFG170's script, `.out`, `.json` and `_firstrun*`, compares row by row, isolates any difference | post-comparison, not part of any frozen result |
| `run_all.sh`, `CFG180_manifest.txt` | orchestration; sha256 of scripts, outputs and inputs | — |

- **Exit convention:** main exits 0 iff C1 and C2 pass (2 otherwise). MUTATE exits 1 iff the control bites, 0 if it does not bite. Attacks and mocks exit 0.
- **Output hygiene:** no absolute home path printed (`<repo>`, `<scratch>`); a grep for the home prefix over all outputs is part of `run_all.sh`.
- **Determinism:** the main run and A1–A6, A8 and B are deterministic; A7 and C use `numpy.random.default_rng(seed)` with the seeds above.

## 8. What would count as disagreement with CFG170

1. Any pass line of section 4 missed by more than its tolerance (each miss printed with its size; conventions A/B and the rounded s are the declared causes to test first).
2. Any cell of the disfavoured matrix, or the summary label, differing (P6).
3. The two forms of the rule disagreeing in any cell (P6): the README's claim of algebraic equivalence would then be wrong.
4. P10 failing: the first-run convention changing more than the one row the README names, or changing a verdict flag.
5. **Robustness findings that would contradict the README's wording** (these count as valid disagreements even if every number reproduces):
   - A5 or A6 turning the s = 1 summary into DIAGNOSTIC, contradicting "no verdict depends on this convention" and the NON-DIAGNOSTIC label being convention-independent (my estimate E9 says this is likely for A5);
   - any B variant making exactly one law disfavoured by both brackets;
   - A1 showing the statistic structurally non-diagnostic for reasons beyond the README's stated "0.01–0.06 dex against a 0.28-dex bracket" (that the root-find intervals themselves, not R_obs, already swamp the separation);
   - A3 or A4 contradicting the README's two stated explanations (a common pipeline offset versus a biased-low in-repo exponent), for instance if the reconciling offset needed is far outside the CFG161/167 differential and its systematic scatter;
   - A7 showing the root-find interval under-covers.
6. **Not a disagreement:** shared-pipeline physics (ν_mono, α(x), pressure prescriptions, KROSS/KURVS selections), which this lane does not test.

κ = ½ and Ω_c h² stay fitted. a₀(z) flat is the framework's distinctive law; a₀ ∝ H(z) the rival. Nothing here says the data favour either model, or that the theory is closed.
