# CFG167 — referee re-derivation of CFG161 (the KURVS − KROSS differential under P4) — FROZEN CRITERIA (phase 1)

Written 2026-09-29 by the referee agent (Opus-chat lineage that wrote CFG165), BEFORE any CFG167 script exists or has been run.
Nothing below changes after a result is seen; any later departure goes in the README as a disclosed departure.

## 0. What I read, and what I did NOT open

Read (allowed list only): CFG161_FROZEN_CRITERIA.md, CFG161_README.md, CFG160_README.md, CFG140_README.md, CFG141_README.md,
CFG165_kurvs_referee/README.md and CFG165_kurvs_referee/*.py, *.out (my own earlier referee). Data files: names only
(`data_assembly/high_z_tf_tables/kross_v2.csv` header row was seen while reading my own loader's target; no numbers of it computed).
NOT opened in phase 1: CFG161's script, .out, .json (nor any CFG161 MUTATE file). Phase 2 opens them only after my main and all MUTATE runs are saved.
No network, no downloads, no repo edits. Scratch dir: `.../scratchpad/cfg167/`.

**Disclosure that limits blindness.** (i) My own CFG165 (section 5c3) already computed this differential: P4 = +0.151 ± 0.045, rival +0.071,
3.4σ / 1.8σ, P0 +0.022 ± 0.060, P1 +0.274 ± 0.070, P2 +0.266 ± 0.065 (inclination column `inc_sfr_deg`). So CFG167 is NOT a blind
re-derivation of the headline; it is a re-run of a known number under CFG140's own inclination column plus new attacks. (ii) From my CFG165 post-comparison
diagnostic I know the one convention difference (`inc_star_deg`, CFG140's column, moves numbers by 0.002–0.005). I adopt `inc_star_deg` for the frozen main
run because C1 requires CFG140's 3-decimal values; I also run `inc_sfr_deg` and report both. (iii) CFG161's numbers in its README are TARGETS I read, not
blind predictions. The estimates in section 3 were made AFTER reading them.

## 1. What is re-derived, and where independence STOPS

Imported read-only from `<repo>/campaign_fresh_gravity/CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` (imported as `M`; a shared, NOT independent element):
`load_kurvs` (with `inc_col`), `load_sparc_anchor`, `load_kross` (my own KROSS loader: RT/RT+, v/σ0 ≥ 1, R = 2 r_im, R_d = r_im/1.68, σ0 tabulated, mass err 0.15, i from b/a),
`per_object`, `pool` (weighted mean with χ²/dof inflation), `anchor_pool`, `cell`, `spec/SP` (P0–P4 correction specs), `alpha_K` (Kretschmer table as quoted),
`E_of_z`, `gbar`, `gpred`, `enclosed`, and through it `CFG4_common.nu_mono` and the a0 constants. Also shared: all data files, CFG140's declared choices (gas
bracket, mass 0.10/0.15 dex, inclination ±5°, thin exponential discs, spherical surrogate, g_obs = V²/R), and Kretschmer's α(x) as quoted (unverified literature).
So agreement of my D with CFG161's shows only that the frozen text plus the data plus these shared pieces determine the numbers; it does not test ν_mono, α(x), or the physics.

Written fresh in CFG167 (independent of CFG161): the differential D = Δ_flat(KURVS) − Δ_flat(KROSS) (raw pooled, no anchor), σ_D = hypot(σ_K, σ_R), the exact pipeline
rival prediction D_H = [Δ_flat − Δ_H]_K − [Δ_flat − Δ_H]_R, the four-class decision rule at 2σ_D, R0/R1/R2/R3 rows, controls, MUTATEs, and all four attacks (bootstrap,
correlated-systematics Monte Carlo, permutation null, anchor-geometry adjustment, gas-ratio surface, KROSS-selection variants, mock power).

Not testable here (declared): KROSS's own outer σ profile; KROSS gas; VELA's applicability; anisotropy; whether Kretschmer's α is applied to a Hα tracer at its stated R_e.

## 2. The headline pinned (targets = README numbers I READ; the criteria are not a blind prediction of them)

Primary cell: μ = 0.67, δ = 0, canonical footing, flat reading's Δ, no anchor (anchor cancels in D — an assumption attacked in (a4)).
Targets, CFG161 README (507725b7b criteria; results commit 9ff8e369a as cited by CFG160):

| row | D ± σ_D | D_H | rule verdict |
|---|---|---|---|
| P0 | +0.017 ± 0.058 | +0.069 | consistent with both |
| P1 (σ0 on KURVS, KROSS σ0) | +0.273 ± 0.070 | +0.078 | manufactures |
| P2 (σ_out on KURVS; KROSS σ0 at 2R/R_d) | +0.265 ± 0.065 | +0.077 | manufactures |
| P3 | +0.218 ± 0.070 | +0.074 | manufactures |
| **P4 primary (KU2, σ_out)** | **+0.148 ± 0.044** | **+0.072** | **lands on the rival** (3.3σ from flat, 1.7σ from rival) |
| P4 α × 0.6 | +0.110 ± 0.045 | +0.071 | lands on the rival |
| P4 α × 1.4 | +0.175 ± 0.046 | +0.073 | manufactures |
| P4 KURVS σ0 (KU) | +0.126 ± 0.050 | +0.074 | lands on the rival |

Other README targets: R0 σ_D = 0.044, D_H = +0.072 (deep-regime ½log10[E(1.53)/E(0.85)] = +0.083), |D_H|/σ_D = 1.6; R3 (anchor-corrected, P4): KURVS Δ′_flat +0.144 ± 0.044
(+3.3σ), Δ′_H −0.006 (−0.1σ); KROSS Δ′_flat −0.004 ± 0.020 (−0.2σ), Δ′_H −0.082 (−4.1σ). C1: P0 +0.017 ± 0.058 and P1 +0.273 ± 0.070. C2: Δ′_flat +0.1441, Δ′_H −0.0060.
MUTATE (README): KURVS v ×2 → D = +0.556, 11σ from flat, 9.6σ from rival, H1 fails, exit 1. (Note: the frozen CFG161 text says ×10^0.3 and "D rises about 0.6"; README says ×2 and D rises by 0.41 —
see section 6.)

**Decision-rule geometry (hand arithmetic from README numbers, made now):** with σ_D = 0.044, D_H = 0.072, the classes are in D: lands on flat [−0.088, −0.016); consistent with both [−0.016, 0.088];
**lands on the rival (0.088, 0.160]**; manufactures D > 0.160 or D < −0.088. The observed +0.148 sits 0.012 (0.27 σ_D) below the manufactures boundary. The "pass" is a 0.072-wide sliver.
Two rows are also within 0.02 of the boundary: P3 (|D − D_H| = 2.06σ) and α × 1.4 (2.22σ).

## 3. Hand ESTIMATES (labelled: made after reading the READMEs and my own CFG165 outputs; they are not blind predictions)

Reproduction probabilities are for my code meeting the pass lines in section 4.

| item | my estimate | P(pass) |
|---|---|---|
| D_P0, D_P1, D_P2 with inc_star | +0.017, +0.273, +0.265 (CFG165 had +0.022/+0.274/+0.266 with inc_sfr) | 0.85 each; jointly 0.7 |
| D_P3 | +0.21 ± 0.02 (P3 on KROSS with grad2 = 0: C = σ²R/R_d, between P4's factor 2.53 and P1's 6.7 at KROSS R/R_d = 3.36) | 0.55 (the frozen text never says how P3 acts on KROSS) |
| D_P4, D_H(P4) | +0.148 ± 0.003, +0.072 ± 0.003; σ_D 0.044 | 0.90 / 0.85 |
| α × 0.6, × 1.4 (α scaled in BOTH samples: option A) | +0.11 to +0.12; +0.18 to +0.20 (linear D(s) ≈ 0.017 + 0.128 s overshoots ×1.4 slightly) | 0.75 / 0.75; option B (KURVS only) gives ≈ +0.06 for ×0.6 and would NOT match the README's +0.110, which is what identifies option A |
| KURVS σ0 variant | +0.126 ± 0.050 | 0.8 |
| all 8 class labels equal README | | 0.60 (P3 and α × 1.4 are the edge rows) |
| R3 KROSS Δ′_flat, Δ′_H, σ | −0.004 (raw KROSS +0.093 ± 0.015, anchor +0.099 ± 0.013 → 0.020), −0.082 | 0.9 |
| C1 (with inc_star), C2 | exact | 0.9, 0.95 |
| deep-regime +0.083; |D_H|/σ_D = 1.6 | arithmetic: 0.5·log10(2.405/1.637) = 0.0836; 0.072/0.044 = 1.64 | 0.95 |
| MUTATE 1 (×10^0.3): D | +0.56 ± 0.02 (raise ≈ 0.41, not 0.6: pressure term dilutes the shift), σ_D ≈ 0.05, ≈ 11σ from flat | 0.75 within 0.01 of +0.556 |
| overall: every headline-table cell within its line | | 0.5 |

Attack outcome estimates (each will be scored against the result, wrong ones kept):
- (a1) bootstrap SD of D: 0.045–0.065 (n = 10 KURVS, heavy tails), so analytic σ_D within ×[0.75, 1.33]: P = 0.6.
- (a2) systematic MC. dD/dln s ≈ 0.077 per e-fold read off the README's ×0.6/×1.4 rows (linear-in-s estimate: 0.128 per unit s gives ±0.05 at 40%). Common 40% α scale: sd_sys ≈ 0.03–0.05, total z_flat ≈ 2.4–2.9 (P(≥ 2) = 0.75), z_rival ≈ 1.3. INDEPENDENT 40% per sample (KURVS raw slope ≈ 0.28 per unit s, KROSS ≈ 0.15): sd_sys ≈ 0.12, total z_flat ≈ 1.1–1.3 (P(≥ 2) = 0.10). The headline "3.3σ from flat" is not robust to independent calibration errors. 
- (a3) permutation null (10 random KROSS galaxies as pseudo-KURVS): sd within ×[0.75, 1.33] of the analytic pooled error: P = 0.65.
- (a4) anchor geometry: SPARC pooled offset varies with x (CFG165: 0.135 / 0.168 / 0.077 in x < 1.5 / 1.5–2.5 / > 2.5), so D is not anchor-free; D_adj ≈ +0.10 to +0.13, shift 0.02–0.05; P(|D_adj − D| ≤ 0.02) = 0.35; class stays lands-on-rival: 0.8.
- (a5) gas-ratio surface (μ_KURVS = g μ_KROSS): D(g = 2) ≈ 0.07 (on the rival's D_H), D = 0 near g ≈ 3–4; each law can fit both samples' absolute levels for some (μ_R, μ_K) with μ_K ≥ μ_R? flat: yes near μ_K ≈ 2, μ_R ≈ 0.67 (χ² ≲ 2); rival: KROSS −4.1σ needs μ_R ≲ 0.25 (probability the rival reaches χ²min ≤ 4 with μ_K ≥ μ_R in [0.1, 8]: 0.5).
- (c) KROSS selection variants: D range across variants with n ≥ 30: ±0.04; P(every variant keeps class = lands on rival) = 0.4 (the boundary is 0.012 away); KROSS-internal z-split gap: |gap| < 2σ (P = 0.85).
- (b) power, ideal family: P(lands on rival | flat truth) ≈ 0.06; P(lands on rival | rival truth) ≈ 0.45; P(manufactures | rival truth) ≈ 0.03; LR at D_obs ≈ 15 (exp(−(0.148−0.072)²/2σ²) / exp(−(0.148−0.02)²/2σ²) with σ = 0.044); nuisance families: LR 1.5–3 and P(lands on rival | flat truth) 0.15–0.35.
- (d) null: under flat truth D ~ 0.02 ± 0.044 (mean above 0 because the KURVS-only pressure over-read, CFG165 ideal flat mean Δ′ = +0.024); P(D ≥ 0.148 | flat truth, ideal) = 0.002–0.005.

## 4. Exact pass lines (main run vs the section 2 targets)

All comparisons against README 3-decimal values; my run uses `inc_star_deg` for KURVS (frozen).
- P1. C1: my D and σ_D under P0 and P1 equal +0.017 ± 0.058 and +0.273 ± 0.070 to the 3-decimal print (|Δ| ≤ 0.0015 each, i.e. rounding).
- P2. C2: Δ′_flat, Δ′_H of the KURVS P4 decision cell within 0.001 of +0.1441, −0.0060.
- P3. Table D and D_H, all 8 rows: within 0.005 absolute of the README values. σ_D within 0.005.
- P4. z vs flat (D/σ_D) and z vs rival ((D − D_H)/σ_D) for the P4 primary: within 0.10 of README's 1-decimal values 3.3 and 1.7 (the README rounding half-width 0.05 plus the 0.05 line).
- P5. Class label of all 8 rows equal to README. EDGE rule (frozen now): if a class differs but the numbers pass P3 and the boundary distance is ≤ 0.1σ_D-equivalent (P3 row: |D−D_H|/σ_D within 2 ± 0.1; α × 1.4 row: 2 ± 0.25), it is recorded EDGE-DIFFERS, not a disagreement.
- P6. R0: σ_D, D_H, |D_H|/σ_D within 0.005, 0.005, 0.1; deep-regime +0.083 within 0.001.
- P7. R3: KURVS/KROSS Δ′_flat, Δ′_H within 0.005; KROSS σ within 0.003; z within 0.15.
- P8. H1 passes (D within 2σ_D of at least one prediction) with exit 0; H1 is not a "pass" in any wider sense (it does not validate P4).
- P9. Consistency of my own run: rerunning main twice gives identical output (determinism).
Overall REPRODUCES iff P1–P4, P6–P8 pass and P5 has no non-edge mismatch.

## 5. MUTATE controls (each flips a load-bearing cell; exit 1 = the control BITES; bite := H1 fails OR class ≠ "lands on the rival")

Separate outputs per mode (`CFG167_MUTATE_<k>.out/_results.json`).
- **M1** KURVS v_last × 10^0.3 (g_obs ≈ ×4; the frozen CFG161 factor; README used ×2). Expect D ≈ +0.56, > 9σ from both predictions, manufactures; H1 fails; exit 1.
- **M2** KROSS pressure correction removed (α = 0 for KROSS only, KURVS at P4). Load-bearing: the cancellation of the pressure correction between samples. Expect D ≈ 0.243 − (−0.055) = +0.30, ≈ 6σ from flat and ≈ 5σ from the rival: manufactures; exit 1.
- **M3** labels swapped in the verdict (the number D_H attached to "flat", 0 attached to "rival"). The rule here IS label-symmetric (unlike CFG160's lean map, cf. my wrong M3 expectation in CFG165); expect class "lands on flat"; class ≠ main's, so bite, exit 1 (P = 0.9; if the class does not flip I keep the expectation as wrong).
- **M4** KURVS gas μ = 4 with KROSS μ = 0.67 (a gas-ratio flip). Expect D ≈ 0.148 − 0.27 = −0.12 ± 0.03: more than 2σ_D BELOW both predictions (tests the "either side" clause): manufactures on the negative side; H1 fails; exit 1 (P = 0.85).
- **M5** (informational; need not bite) KURVS σ_out permuted across galaxies, seed 167. Expect |ΔD| < 0.02, class unchanged, exit 0 (my CFG165 M6 did not bite for the same reason; kept whatever it does).
A control that fails to bite when expected (M1–M4) is kept and reported as a failed control, not repaired.

## 6. The attacks (frozen procedures; pre-declared N and seeds; each ends with a labelled verdict)

Seeds: 167 for every stochastic step; 168 re-run; agreement required to ±0.01 in each reported fraction for the re-run to be called stable. Headline stays P4 primary.

**(a) Error model: correlated systematics, the anchor, the sampling error.**
- (a1) Independent nonparametric bootstrap: resample the 10 KURVS and the 390 KROSS galaxies with replacement, N = 20000, seed 167; pool each with `M.pool` (inflation as in the main run); D; compare SD(D) to analytic σ_D. ROBUST if the ratio SD/σ_D ∈ [0.75, 1.33]. Also leave-one-out over the ten KURVS (D range) and a 95% percentile interval.
- (a2) Correlated-systematics Monte Carlo (N = 4000 draws, seed 167; each draw re-evaluates D through the pipeline). Nuisances: (i) coherent α scale, ln s ~ N(0, 0.4) applied to both samples (common normalisation); (ii) independent α scales per sample, each ln s ~ N(0, 0.4); (iii) common α tilt α·(1 + t(x − 2)), t ~ N(0, 0.15); (iv) independent stellar-mass zero-point offsets δM_K, δM_R ~ N(0, 0.15) dex each; (v) gas ratio g = μ_K/μ_R, ln g ~ N(0, 0.5) around 1. Report sd_sys of D for (i)–(v) separately and for "common set" = (i)+(iii)+(iv-common), and "independent set" = (ii)+(iii)+(iv)+(v); total σ = hypot(σ_D, sd_sys), z_flat, z_rival, and P(class = lands on the rival). Verdict: ROBUST if z_flat ≥ 2 under both sets; SOFT if only under the common set; NOT ROBUST if under neither.
- (a3) Permutation null of the error model: draw 10 KROSS galaxies at random as pseudo-KURVS (N = 20000, seed 167), D_perm = pool(pseudo) − pool(rest of KROSS); compare SD(D_perm) to the analytic hypot of the two pooled errors. ROBUST if the ratio ∈ [0.75, 1.33]. Also: where the real D sits in the D_perm distribution (informational; the real KURVS have different x).
- (a4) Anchor-geometry adjustment (D is anchor-free only if the z = 0 pipeline offset is geometry-independent): fit the SPARC anchor's per-galaxy P4 Δ_flat against x = R/R_eff − 1 (weighted linear fit, bootstrap N = 2000, seed 167) and against R/R_d (variant); evaluate at each KURVS galaxy's x (weighted by the KURVS pooling weights) and at KROSS x = 1; D_adj = D − (offset_K − offset_R). ROBUST if |D_adj − D| ≤ 0.02; report D_adj, its class, and the bootstrap sd of the shift.
- (a5) Gas-ratio surface (informational, no pass line): D as a function of g = μ_K/μ_R ∈ {0.5, 1, 1.5, 2, 3, 4} at μ_R = 0.67; break-even g for D = 0 and D = D_H(g); and a 2-D grid μ_R ∈ [0.1, 4] (13 log steps) × μ_K ∈ [0.1, 8] (17 log steps) of the anchor-corrected joint χ² of (KURVS Δ′, KROSS Δ′) for each law, restricted to μ_K ≥ μ_R; report the best cell per law and whether either reaches χ² ≤ 4. Reading: a differential can "land on" a law while the absolute levels disagree; only a joint fit says whether a common gas history rescues it.

**(b) Power under flat truth and rival truth with the same errors.** Mock truth = the real KURVS baryons, σ_out, errors and the real KROSS baryons, σ0, errors; the law generates g_true; V_mock² = g_true R − α_true σ²; the mock is analysed with the exact P4 pipeline. N = 4000 per (truth, family), chunks of 500, seeds 167 and 168. Families: IDEAL (μ = 0.67 both, α exact both); GAS (μ_R lognormal median 0.67 sd 0.3 dex; μ_K = g μ_R with ln g ~ N(0, 0.5), g median 1; α exact); CAL (GAS plus coherent lnN(0, 0.4) α scale common to both samples plus per-galaxy lnN(0, 0.2)); CAL-IND (GAS plus independent lnN(0, 0.4) scales per sample). Report per family and truth: mean and SD of D, the class fractions under the frozen rule, P(D ≥ D_obs), and the likelihood ratio at D_obs (Gaussian fit and KDE), plus P(class = manufactures | truth) (= how often P4 would be flagged although the truth is one of the laws). Frozen reading test: the observed "lands on the rival" is INFORMATIVE only if in the family P(lands on rival | flat) < 0.05 and LR > 10; WEAK if LR in [1, 10]; UNINFORMATIVE if LR < 1.5 or P(lands on rival | flat) > 0.20. Mock caveats to disclose: KROSS σ0 stands in for its σ profile; galaxies whose pressure term exceeds the whole V_c² are floored at 0.25% V_c² and the floored fraction is printed.

**(c) KROSS selection / comparison sub-sample.** Variants (each recomputes D, σ_D, D_H, class; min n = 30): all 390 (main); kin_type RT only; RT+ only; v/σ0 ≥ 2; ≥ 3; log M* within KURVS's range [9.55, 10.68]; log M* < median and ≥ median; b/a > 0.5 (inclination cap); z < 0.85 and z ≥ 0.85 halves (the split gap Δ_flat(z hi) − Δ_flat(z lo) is a KROSS-internal redshift lever and is compared to the rival's pipeline prediction for the same split); drop the 5% of KROSS with the largest pressure correction (V_c/V − 1); drop the lowest-error 5%; KROSS mass-matched to KURVS by nearest-log M* (one per KURVS galaxy, 20 neighbours each, N = 2000 random draws, seed 167); and KURVS leave-one-out (10 variants). Verdict: ROBUST iff every variant keeps D ∈ [0.098, 0.198] (±0.05 of the primary) AND keeps class = lands on the rival; FRAGILE otherwise (report which variants flip and by how far). Range of D across variants is reported regardless.

**(d) What a null would have looked like.** (i) The class map in D (section 2 geometry) with the observed D's distance to each boundary in σ_D. (ii) The simulated null distributions from (b), IDEAL and nuisance families: the D histogram (10 quantiles) under flat truth and rival truth. (iii) The permutation null of (a3). (iv) A "P4 is wrong" null: P4 true α scaled ×0.6 and ×1.4 in both samples (CAL family with fixed scale, N = 4000, seed 167) — how often the rule would call this "manufactures" or "lands on a law". (v) The explicit statement of the D value that would have counted as a fail (D > 0.160 or < −0.088, in CFG161's units). Verdict: NULL-DISTINGUISHABLE if P(D ≥ D_obs | flat truth, IDEAL) < 0.01 AND P(D ≥ D_obs | flat truth, CAL) < 0.10; otherwise NOT DISTINGUISHABLE from flat-truth-plus-nuisance.

## 7. Script plan (nothing written or run in phase 1)

Scratch dir → the orchestrator places under the repo lane dir. Convention for all: print `repo=<repo>`; never an absolute home path; `ZF_REPO` env var or walk up from `__file__` (needs `data_assembly/` and `campaign_fresh_gravity/`); import M by inserting `<repo>/campaign_fresh_gravity/CFG165_kurvs_referee` on `sys.path`; `sys.dont_write_bytecode = True`; set `OMP_NUM_THREADS`-type env to 2; each run < 15 min (expected < 3 min, main < 10 s).
1. `CFG167_referee_diff_p4.py`: main and MUTATE. `MUTATE=k python3 ...` for k = 1–5 → `CFG167_MUTATE_k.out/_results.json`; main → `CFG167_main.out/_results.json`. Prints: controls (C1, C2, α values, n and median z of both samples, kernel limits), R0 (before D), R1 (D under P0–P4 + α band + KU σ0 variant, each with D_H and verdict), R3 (anchored absolute levels), boundary geometry, both inclination columns, H1. Exit: main 0 iff all controls pass and H1 passes; MUTATE 1 when the control bites (bite := H1 fails OR class ≠ main class), 0 when it does not; controls failing in main → exit 2.
2. `CFG167_attacks_ac.py`: attacks (a1)–(a5), (c). Exit 0 always (informational), prints the frozen verdict labels.
3. `CFG167_power_bd.py`: (b) and (d). Exit 0.
4. `CFG167_diag_post.py`: phase 2 ONLY, written after CFG161's script/out/json are opened; labelled post-comparison, not part of any frozen result.
Run block (to be filled in the README): main; MUTATE 1–5; attacks; power; diag. Determinism: main run twice identical.

## 8. What would count as disagreement with CFG161

- Any headline table cell (section 2) outside the section 4 lines after the inclination column is matched (a numeric disagreement); a class label mismatch that is not EDGE-DIFFERS.
- The README's sentence "P4 does not manufacture evolution; P1, P2 and P3 do" is contradicted if my α × 1.4 row also reads manufactures (the README table already shows it does) and P3 is edge — I will report the sentence as an incomplete summary.
- Reading-level disagreements I already suspect (tested by (a)–(d), not asserted): (1) "lands on the rival" is a 0.072-wide sliver 0.012 below the manufactures boundary and flips within the README's own α band; (2) the differential's flat-vs-rival separation (|D_H|/σ_D = 1.6) cannot support a class decision at 2σ; the frozen "about 1.2σ" was a power statement, and the observed 3.3σ from flat is not a power statement; (3) the error model assumes the P4 calibration error is the same or cancels between samples — under independent calibration errors the 3.3σ falls to ≈ 1; (4) the anchor is assumed to cancel; (5) at common μ the absolute levels (flat fits KROSS, rival fits KURVS) mean a "lands on the rival" differential is not a consistent rival world (a5); (6) the criteria's MUTATE arithmetic ("D rises by about 0.6") is wrong (the README's +0.556 is a rise of 0.41) and the criteria's ×10^0.3 differs from the README's ×2 (0.5% in V).
- A CFG161 README statement I will check for wording only: "3.3σ from flat and 1.7σ from the rival" against my z (rounding), and "P4 α × 0.6 / × 1.4" applying to both samples (option A).

## 9. Readings (declared in advance)

- REPRODUCES + attacks pass: "CFG161's numbers stand as a weak consistency statement about P4 at 1.6σ power; not an a₀ verdict."
- REPRODUCES + (a2)/(b)/(c) FRAGILE or NOT ROBUST: "the numbers stand; the class label 'lands on the rival' does not carry weight beyond the sliver it occupies."
- Numeric non-reproduction: reported with the cause classified (definition / solver / error model), and no repair by post-hoc convention choice beyond the declared inc_star swap.

κ = ½ and Ω_c h² stay fitted. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival. Nothing here says the data favour either model, or that the theory is closed; a lean is not a detection.
