# CFG167 — Referee re-derivation of CFG161 (the KURVS − KROSS differential under P4)

- **Criteria:** `CFG167_FROZEN_CRITERIA.md` (committed 665c7c4e4, sha256 cfe9e062…) before any script existed. Hand estimates in it were made after reading the CFG161 README and my own CFG165 outputs, and are disclosed as such.
- **Order of work:** phase 1 = criteria only. Phase 2 = my scripts written from the frozen text → main run, MUTATE M1–M5, attacks (a)–(d) at seed 167, re-run at 168 → ONLY THEN CFG161's `.py`, `.out`, `.json` opened → `CFG167_diag_post.py` written after that (labelled post-comparison, not part of any frozen result).
- **Repo untouched. No network, no new data. No absolute home path in any output** (`<repo>` is printed; checked by grep).
- **Not a blind re-derivation.** My own CFG165 had already computed this differential (+0.151 ± 0.045); the README numbers were targets I read.

## Bottom line

**CFG161's numbers REPRODUCE, to 7 × 10⁻⁶ in D, in σ_D and in D_H, in all eight rows, with the class labels equal. The frozen controls C1 and C2 pass, and MUTATE M1–M4 bite. What does not survive the attacks is the weight the label "lands on the rival" can carry.**

- **The arithmetic is right.** D = +0.1483 ± 0.0445, D_H = +0.0722, 3.33σ from flat and 1.71σ from the rival, class "lands on the rival". R3's absolute levels (KURVS +0.144 / −0.006; KROSS −0.004 ± 0.020 / −0.082) also reproduce.
- **The label is a sliver.** With σ_D = 0.0445 the class "lands on the rival" is D in (0.089, 0.161]. The observed +0.148 is 0.013 (0.29 σ_D) below the "manufactures evolution" edge. The same rule gives "manufactures" for α × 1.4, for the RT-only KROSS sub-sample, for a b/a > 0.5 cut, for dropping the lowest-error 5% of KROSS, and for leaving out KURVS-7. It gives "consistent with both" for the RT+ subset, v/σ0 ≥ 2 and v/σ0 ≥ 3.
- **Plain answer 1 — does the 3.3σ from flat hold under common versus independent calibration errors?** It is a purely statistical number, and it holds at ≥ 2σ only if the calibration errors are common to the two samples.
  - Common α scale (ln s ~ N(0, 0.4)), common tilt and common mass zero-point together: total z_flat = **2.5** (sd_sys 0.039).
  - Independent errors (α scales, tilt, mass zero-points, gas ratio): total z_flat = **0.83** (sd_sys 0.172). Independent α scales alone give 1.44 and independent mass zero-points alone 1.02.
  - KROSS sub-sample selection alone (sd of the KROSS mean Δ_flat over the (c) variants, 0.057; post-comparison extra): 2.05.
  - The KURVS α is applied at x = 1.0–3.5 and KROSS's at x = 1, so a common α normalisation error only partly cancels: dD/d ln s ≈ 0.077.
- **Plain answer 2 — is "lands on the rival" a consistent rival world?** **No, not at the common gas fraction the rule uses (μ = 0.67 in both samples).**
  - There the rival's absolute level at KROSS is −0.082 (−4.1σ). The joint χ² of the two anchored levels is 16.5 for the rival against 0.06 for flat (flat needs KURVS gas about 3 times KROSS's, μ_K ≈ 2.1).
  - The rival fits both only if KROSS gas is ≲ 0.3 M* and KURVS gas is ≈ 0.7–0.75 M* (χ² 2.5 at μ_R = 0.27; 0.13 at 0.10). Flat fits both at μ_R = 0.5–0.7 with μ_K ≈ 2.
  - With gas free, both laws can be made to fit; the differential does not choose between them. It is a differential-only statement, not an a₀ verdict, and no gas is measured.
- **What a null would have looked like.** In the ideal mock (gas and α known) a flat truth gives D = −0.021 ± 0.041 and a rival truth +0.038 ± 0.038; the observed +0.148 has P(D ≥ obs | flat) < 2.5 × 10⁻⁴ and likelihood ratio ≈ 80. With gas and calibration free (CAL-IND) the ratio is 2.1, P(D ≥ obs | flat) = 0.051, and the rule labels "lands on the rival" in 11% of flat-truth trials and 22% of rival-truth trials. The rule cannot identify the rival at this power.
- κ = ½ and Ω_c h² stay fitted. a₀(z) FLAT is the framework's distinctive law, a₀ ∝ H(z) the rival. Nothing here says the data favour either model or that the theory is closed; a lean is not a detection.

## 1. Where independence stops

Imported read-only (a shared, not independent element) from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` as `M`: `load_kurvs`, `load_sparc_anchor`, `load_kross`, `per_object`, `pool` (χ²/dof inflation), `anchor_pool`, `cell`, `SP/spec`, `alpha_K`, `E_of_z`, `gbar`, `gpred`, `enclosed`, and through it `CFG4_common.nu_mono` and the a₀ constants. Also shared: all data files, CFG140's set-up choices (gas bracket, mass errors 0.15, inclination ±5°, thin exponential discs, spherical surrogate, g_obs = V²/R), and Kretschmer's α(x) as quoted (unverified literature; C3 checks only the arithmetic).
Written fresh here: D, σ_D, the exact D_H, the four-class rule, R0–R3, the controls, the MUTATEs, and every attack (bootstrap, systematics Monte Carlo, permutation null, anchor-geometry fit, gas surface, selection variants, mock power).
Agreement to 7 × 10⁻⁶ therefore shows that the frozen text, the data and these shared pieces determine the numbers. It does not test ν_mono, α(x) or the physics. CFG161 itself runs CFG140/141's own code paths (exec'd), so the two pipelines differ in the pooling and KROSS-loading code, and agree.
One convention is not blind: I use `inc_star_deg` (CFG140's column, known from CFG165's post-comparison diagnostic); `inc_sfr_deg` gives +0.151 ± 0.045 (P4), reported.

## 2. Table vs CFG161, row by row (D = Δ_flat(KURVS) − Δ_flat(KROSS), μ = 0.67, δ = 0, canonical, unanchored)

"CFG161" = the README table (and its committed json). "Mine" = the frozen main run (`inc_star_deg`). "Δ json" = mine minus CFG161's committed json.

| row | CFG161 D ± σ_D | mine D ± σ_D | CFG161 D_H | mine D_H | class (CFG161 / mine) | Δ json (D) | verdict |
|---|---|---|---|---|---|---|---|
| P0 | +0.017 ± 0.058 | +0.0167 ± 0.0584 | +0.069 | +0.0690 | consistent / consistent | −3 × 10⁻⁶ | REPRODUCES (C1) |
| P1 | +0.273 ± 0.070 | +0.2732 ± 0.0704 | +0.078 | +0.0781 | manufactures / same | −7 × 10⁻⁶ | REPRODUCES (C1) |
| P2 | +0.265 ± 0.065 | +0.2648 ± 0.0651 | +0.077 | +0.0769 | manufactures / same | −6 × 10⁻⁶ | REPRODUCES |
| P3 | +0.218 ± 0.070 | +0.2178 ± 0.0697 | +0.074 | +0.0740 | manufactures / same (2.06σ from the rival: edge row) | −5 × 10⁻⁶ | REPRODUCES |
| **P4 primary** | **+0.148 ± 0.044** | **+0.1483 ± 0.0445** | **+0.072** | **+0.0722** | **lands on the rival / same** (z 3.33 and 1.71) | −5 × 10⁻⁶ | **REPRODUCES** |
| P4 α × 0.6 (both samples) | +0.110 ± 0.045 | +0.1102 ± 0.0454 | +0.071 | +0.0711 | rival / same | −4 × 10⁻⁶ | REPRODUCES |
| P4 α × 1.4 (both samples) | +0.175 ± 0.046 | +0.1747 ± 0.0461 | +0.073 | +0.0732 | manufactures / same (2.20σ: edge row) | −5 × 10⁻⁶ | REPRODUCES |
| P4 KURVS σ0 (KU) | +0.126 ± 0.050 | +0.1257 ± 0.0503 | +0.074 | +0.0745 | rival / same | −5 × 10⁻⁶ | REPRODUCES |
| R0 | σ_D 0.044, D_H +0.072, ratio 1.6, deep +0.083 | 0.0445, +0.0722, 1.62, +0.0835 | | | | | REPRODUCES |
| R3 KURVS (anchored) | +0.144 ± 0.044 (+3.3σ); rival −0.006 (−0.1σ) | +0.1441 ± 0.0439 (+3.28σ); −0.0060 (−0.14σ) | | | | | REPRODUCES |
| R3 KROSS (anchored) | −0.004 ± 0.020 (−0.2σ); rival −0.082 (−4.1σ) | −0.0042 ± 0.0202 (−0.21σ); −0.0821 (−4.06σ) | | | | | REPRODUCES |
| C2 decision cell | +0.1441 / −0.0060 | +0.1441 / −0.0060 | | | | | REPRODUCES |
| MUTATE (v × 10^0.3) | D +0.556 ± 0.051; 11.0σ / 9.6σ; H1 fails | D +0.5561 ± 0.0507; 10.97σ / 9.56σ; H1 fails | | | | | REPRODUCES |

The KURVS-only variants of the α band (option B, reported by me only): × 0.6 gives +0.060 ± 0.045 (consistent with both), × 1.4 gives +0.217 ± 0.046 (manufactures). The README's +0.110 and +0.175 identify option A (α scaled in both samples), as I assumed.

**Every difference, classified.**
1. **Numerical (7 × 10⁻⁶ or less in D, σ_D, D_H; 6 × 10⁻⁵ in the raw pooled Δ):** different code paths for the pooling and the KROSS loader. Not a Monte Carlo (both deterministic), not a definition, not physics.
2. **Definition (mine, declared):** inclination column. `inc_star_deg` (used in the main run) matches; `inc_sfr_deg` (my CFG165 default) moves P4 to +0.151 ± 0.045.
3. **README/provenance (CFG161):** the anchor-corrected absolute table (KURVS +0.144 / KROSS −0.004 ± 0.020 / −0.082) is not printed by CFG161's committed script, `.out` or `.json` (they print the unanchored R3 only). The README says the numbers came from an uncommitted exploratory probe. My independent computation reproduces them, so the numbers are right and their committed provenance is missing.
4. **README typo/label (CFG161):** (i) the README, the MUTATE strings and the MUTATE section say "velocities × 2"; the code multiplies v and its error by 10^0.3 (a 0.5% difference in V, no effect); (ii) the script's rule prints the label "P4 manufactures evolution" for the P0–P3 rows too (the README table writes "manufactures" correctly); (iii) the README sentence "P4 does not manufacture evolution; P1, P2 and P3 do" omits that its own table shows α × 1.4 manufacturing.
5. **Criteria expectation wrong (CFG161, frozen):** "D rises by about 0.6 dex" under MUTATE. The rise is 0.41 (0.148 → 0.556): the pressure term dilutes the shift. My hand estimate (0.56 ± 0.02) was right.
6. **Physics:** none found; no arithmetic disagreement.

## 3. Pass lines (frozen section 4)

| line | result | verdict |
|---|---|---|
| P1 C1: P0 and P1 differentials to the 3-decimal print | +0.0167 ± 0.0584, +0.2732 ± 0.0704 | REPRODUCES |
| P2 C2: decision cell within 0.001 | +0.1441 / −0.0060 | REPRODUCES |
| P3 all 8 rows: D, D_H, σ_D within 0.005 | max 0.0005 | REPRODUCES |
| P4 z within 0.10 of 3.3 / 1.7 | 3.33 / 1.71 | REPRODUCES |
| P5 class labels, EDGE-DIFFERS allowed | all 8 equal; no edge case triggered | REPRODUCES |
| P6 R0 | 0.0445, +0.0722, 1.62, +0.0835 | REPRODUCES |
| P7 R3 | within 0.0005; KROSS σ 0.0202; z −0.21 / −4.06 | REPRODUCES |
| P8 H1 passes, exit 0 | passes, rc 0 (H1 = D within 2σ_D of one prediction; not a validation of P4) | REPRODUCES |
| P9 determinism | main output byte-identical on a second run | REPRODUCES |

Overall: **REPRODUCES** (11 of 11 in-script checks pass; controls and pass lines kept exactly as they came).

## 4. MUTATE (exit 1 = the control bites; bite := H1 fails or class ≠ "lands on the rival")

| MUTATE | what | result | frozen expectation | verdict |
|---|---|---|---|---|
| M1 | KURVS v × 10^0.3 (and its error) | D +0.5561 ± 0.0507; 10.97σ / 9.56σ; manufactures; H1 fails; rc 1 | +0.56 ± 0.02 | bites; expectation right |
| M2 | KROSS pressure correction removed | D +0.2960 ± 0.0456; 6.50σ / 4.95σ; manufactures; rc 1 | ≈ +0.30 | bites; expectation right |
| M3 | verdict labels swapped | class "lands on flat"; H1 passes; rc 1 (bites through the class change) | "lands on flat" (the rule is label-symmetric, unlike CFG160's lean map) | bites; expectation right |
| M4 | KURVS μ = 4, KROSS 0.67 | D −0.1187 ± 0.0454; −2.62σ / −3.81σ; manufactures on the negative side; H1 fails; rc 1 | −0.12 ± 0.03 | bites; expectation right |
| M5 | σ_out permuted across KURVS, seed 167 (informational) | D +0.1298 ± 0.0490; class unchanged; rc 0 | need not bite; |ΔD| < 0.02 | does NOT bite (ΔD −0.019), as expected, kept |

M3 bites only through the class change, because H1 (within 2σ of at least one prediction) is invariant to which label carries which number.

## 5. The attacks (seed 167; re-run at 168)

### (a) Error model — mixed: the statistical error is right, the systematics decide
- **(a1) bootstrap: ROBUST.** SD(D_boot) = 0.0422 against σ_D = 0.0445 (ratio 0.95); 95% percentile interval +0.067 to +0.233; P(D_boot ≤ 0) = 10⁻⁴. But 37% of bootstrap draws fall in "manufactures" and 56% in "lands on the rival": the class label is a coin toss between two neighbours. Leave-one-out: D from +0.118 (without KURVS-17) to +0.163 (without KURVS-7, which flips the class to "manufactures").
- **(a2) correlated-systematics Monte Carlo: SOFT** (z_flat ≥ 2 under the common set only). Per source, sd_sys / total z_flat: common α scale 0.030 / 2.76; independent α scales 0.093 / 1.44; common tilt 0.023 / 2.97; independent mass zero-points (0.15 dex each) 0.138 / 1.02; common mass zero-point 0.008 / 3.28; gas ratio lnN(0, 0.5) 0.047 / 2.30. **Common set 0.039 / 2.52; independent set 0.172 / 0.83.** The class of D under the alternative calibrations is "lands on the rival" in 62% (common) and 17% (independent) of draws.
- **(a3) permutation null: ROBUST.** SD(D_perm) = 0.110 against a mean analytic error 0.097 (ratio 1.14); the 2σ tail is 8.5% against a nominal 4.6%, so the error model is mildly optimistic. The real D sits at the 92nd percentile of the pseudo-KURVS distribution (informational).
- **(a4) anchor geometry: ROBUST.** The SPARC z = 0 offset depends on x non-monotonically (0.135 / 0.168 / 0.077 in x < 1.5 / 1.5–2.5 / > 2.5), and a linear fit has slope −0.0065 per unit x: the KURVS-minus-KROSS offset is −0.0064 ± 0.0066, D_adj = +0.155, class unchanged (the same with R/R_d). My hand estimate (a shift of 0.02–0.05, D_adj ≈ 0.10–0.13) was wrong in size and sign; kept.
- **(a5) gas surface (informational).** D falls with KURVS gas relative to KROSS: g = 0.5 gives +0.195, 1.0 gives +0.148, 2 gives +0.073 (on the rival's D_H), 3 gives +0.012, 4 gives −0.038. Break-even for D = 0 is g = 3.2, for D = D_H(g) it is g = 2.1. Best joint fits are in the bottom line (answer 2); the post-comparison profile at pinned KROSS gas is in `CFG167_diag_post.out`.

### (b) Power under flat truth and rival truth — INFORMATIVE only in the idealised family
- **Ideal (gas and α known):** D = −0.021 ± 0.041 (flat truth) and +0.038 ± 0.038 (rival truth); P(D ≥ obs) = 0 and 0.003; LR at D_obs = 81 (Gaussian). The rule's "lands on the rival" fires in 0.3% of flat-truth and 11% of rival-truth trials.
- **GAS:** LR 9.9, "lands on the rival" 3.6% / 19.9%. **CAL (common α scale):** LR 6.5, 5.0% / 21.4%. **CAL-IND (independent):** LR 2.15, 11.0% / 22.5%, and "manufactures" fires in 20% of trials under either truth.
- Frozen reading test: ideal INFORMATIVE; GAS, CAL, CAL-IND all WEAK (LR 2–10). Mock caveats: no anchor offset in the mock; KROSS σ0 stands in for its profile; a floored pressure term affects 28% of KURVS galaxies under flat truth at μ = 0.67 (11% under rival truth, 5% and 3% of KROSS), which biases the mock D means low (−0.021 and +0.038, against D_H ≈ +0.075).

### (c) KROSS sub-sample selection — FRAGILE
Variants (D ± σ_D; class): all +0.148 (rival); RT only +0.213 (manufactures); RT+ only +0.090 (both); v/σ0 ≥ 2 +0.072 (both); v/σ0 ≥ 3 +0.025 (both); log M* in KURVS's range +0.157 (rival); log M* below / above median +0.138 / +0.161 (rival); b/a > 0.5 +0.199 (manufactures); z below / above 0.85 +0.148 / +0.149 (rival); drop the top 5% correction +0.147 (rival); drop the lowest-error 5% +0.165 (manufactures). Seven variants (including KURVS-7 leave-one-out) leave the ±0.05 window or change class. D ranges over +0.025 to +0.213.
- **The KROSS sample is heterogeneous beyond its statistical error** (post-comparison): its mean Δ_flat is +0.027 for RT and +0.151 for RT+ (difference −0.123 ± 0.030, 4.2σ), and the sub-sample means have sd 0.057 against a pooled error of 0.015.
- **KROSS-internal redshift lever:** Δ_flat(z ≥ 0.85) − Δ_flat(z < 0.85) = −0.001 ± 0.030 (flat's 0: −0.03σ; the pipeline's rival prediction +0.013: −0.5σ): no information.
- Mass-matched KROSS (n ≤ 10 draws, informational): mean D +0.163, sd 0.103.

### (d) What a null would have looked like — NULL-DISTINGUISHABLE, with the caveats above
- The class map is in the bottom line; a fail would have been D > +0.161 or D < −0.089, and the observed value misses the first edge by 0.013.
- P(D ≥ obs | flat truth): ideal 0.0000, CAL 0.0125, CAL-IND 0.051 (frozen test: < 0.01 and < 0.10 → NULL-DISTINGUISHABLE; the CAL-IND value is just above 0.05).
- "P4 is wrong" null (true α × 0.6 or × 1.4 in both samples): true × 0.6, flat truth: D = +0.017 ± 0.058, "lands on the rival" 8.8%; rival truth: +0.076 ± 0.056, 35%. True × 1.4: flat truth −0.021 (2.5%), rival truth +0.026 (12%). A wrong α scale does not by itself manufacture the observed D.

### Stability (seed 168 re-run)
Every verdict label is unchanged (ROBUST, SOFT, ROBUST, ROBUST, FRAGILE; power families WEAK/INFORMATIVE; NULL-DISTINGUISHABLE). The frozen stability line (every fraction within ±0.01) **fails**: the largest differences are 0.019 (mass-matched class fractions, N = 2000) and 0.018 (power class fractions, N = 4000), which is Monte Carlo noise at these N; no repair.

## 6. Hand-estimate scorecard (frozen section 3; wrong expectations kept)

| estimate | result |
|---|---|
| D_P0, P1, P2: +0.017 / +0.273 / +0.265 | +0.0167 / +0.2732 / +0.2648 (in) |
| D_P3 +0.21 ± 0.02 | +0.2178 (in) |
| D_P4 +0.148, D_H +0.072, σ_D 0.044 | +0.1483, +0.0722, 0.0445 (in) |
| α × 0.6: +0.11 to +0.12; × 1.4: +0.18 to +0.20 | +0.1102 (in); +0.1747 (below the range by 0.005: my linear extrapolation overshot) |
| KURVS-only α × 0.6 ≈ +0.06 | +0.060 (in) |
| all eight class labels equal (P 0.6) | equal |
| M1 D +0.56 ± 0.02; M2 ≈ +0.30; M3 "lands on flat"; M4 −0.12 ± 0.03; M5 does not bite | +0.556; +0.296; as expected; −0.119; as expected (all in) |
| (a1) SD(D_boot) 0.045–0.065 | 0.042 (below my range; the ratio line still passes) |
| (a2) common: sd_sys 0.03–0.05, z 2.4–2.9; independent α: sd ≈ 0.12, z 1.1–1.3 | common 0.039 / 2.52 (in); independent α 0.093 / 1.44 (out, milder); full independent set 0.172 / 0.83 (mass zero-point and gas added, harsher) |
| (a3) ratio in [0.75, 1.33] (P 0.65) | 1.14 |
| (a4) shift 0.02–0.05, D_adj 0.10–0.13 | −0.006, +0.155: **wrong** |
| (a5) D(g = 2) ≈ 0.07; D = 0 at g ≈ 3–4; flat fits both near μ_K ≈ 2 | 0.073; 3.2; μ_R 0.63, μ_K 2.03 (in) |
| (c) D range ±0.04; P(every class kept) 0.4 | range +0.025 to +0.213 (−0.12 / +0.065): **wrong, more fragile** |
| (b) ideal: P(rival class given flat truth) 0.06, given rival truth 0.45, LR 15; nuisance LR 1.5–3, P(rival class given flat truth) 0.15–0.35 | 0.003, 0.114, 81; LR 9.9 / 6.5 / 2.15 and 0.036 / 0.050 / 0.110: **wrong** (mock D means −0.021 and +0.038, not +0.02 and +0.07) |
| (d) P(D ≥ obs given flat truth, ideal) 0.002–0.005; flat-truth mean D +0.02 | < 2.5 × 10⁻⁴; mean −0.021: wrong sign |
| P(all headline cells reproduce) 0.5 | they do |

## 7. Files and re-run

Files (scratch dir; nothing in the repo): `CFG167_FROZEN_CRITERIA.md`, `README.md`, `CFG167_referee_diff_p4.py` (main and MUTATE; also the helper module the others import), `CFG167_attacks_ac.py`, `CFG167_power_bd.py`, `CFG167_diag_post.py` (post-comparison), `CFG167_main.out/_results.json`, `CFG167_MUTATE_{1..5}.out/_results.json`, `CFG167_attacks_ac.out` and `_results_seed167.json`, `CFG167_attacks_ac_seed168.out` and `_results_seed168.json`, `CFG167_power_bd.out` and `_results_seed167.json`, `CFG167_power_bd_seed168.out` and `_results_seed168.json`, `CFG167_diag_post.out/_results.json`, `CFG167_manifest.txt`.

```
export ZF_REPO=<repo>
python3 CFG167_referee_diff_p4.py > CFG167_main.out                                  # rc 0
for k in 1 2 3 4 5; do MUTATE=$k python3 CFG167_referee_diff_p4.py > CFG167_MUTATE_$k.out; done   # rc 1 = bites (M5: rc 0, does not bite)
python3 CFG167_attacks_ac.py 167 > CFG167_attacks_ac.out                              # rc 0, ~1 min
python3 CFG167_power_bd.py 167 > CFG167_power_bd.out                                  # rc 0, ~20 s
python3 CFG167_attacks_ac.py 168 > CFG167_attacks_ac_seed168.out; python3 CFG167_power_bd.py 168 > CFG167_power_bd_seed168.out
python3 CFG167_diag_post.py > CFG167_diag_post.out                                    # post-comparison; rc 0
```
Whole set runs in under two minutes. `ZF_REPO` is required unless the scripts sit inside the repo tree (they walk up from `__file__`).

## 8. What would count as disagreement, and what I found

- Any headline cell outside the pass lines: **none**. Any class label mismatch: **none**.
- Reading-level disagreements with CFG161's framing (all confirmed by the attacks): (1) "lands on the rival" is a 0.072-wide sliver 0.013 from the "manufactures" edge and flips within the README's own α band and under seven KROSS/KURVS sub-samples; (2) the 3.3σ is statistical and falls to 2.5σ (common calibration errors) or 0.8σ (independent); (3) at a common gas fraction the rival's absolute level fails at KROSS (−4.1σ, joint χ² 16.5), so the label is not a consistent rival world; (4) the rule's power to name the rival is 11–22% even when the rival is true.
- Not disagreements: the arithmetic, the controls, the MUTATE, the R3 levels. The uncommitted provenance of the anchored table is recorded in section 2, item 3.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

`./run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 1-4 exit 1 (bite); MUTATE 5 exit 0 (informational); attacks and power at seeds 167 and 168 and the post-comparison diagnostic exit 0. Every `.out` and `.json` is identical to the referee's. The frozen criteria are `../CFG167_FROZEN_CRITERIA.md` (665c7c4e4). Independence stops at the imported CFG165 pipeline (loaders, `per_object`, `pool`, `nu_mono`, Kretschmer alpha as quoted) and CFG140's set-up choices.

## Provenance note (append-only; reported by the calc chat in 27bcce5a4, with the data chat's digitisation in 5e8617c81; no verdict changes)

The KURVS outer velocity that every a0(z) lane read, `v_at_last_point_kms` (the paper's Table B1 column 3), is the authors' fitted exponential-disc MODEL evaluated at R_max, not a measured data point: the data chat's digitisation shows model(R_max)/sin i_SFR equals it to about 1% for all ten discs. This lane imports the same column through the CFG165 loader, so it reproduced its target as that lane ran it; the note changes what the column means, not what was reproduced. The calc chat re-runs the test with the measured markers as CFG189 (criteria frozen first). Recorded here as reported and not re-verified by this lane's author.
