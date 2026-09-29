# CFG165 — Referee re-derivation of CFG160 (KURVS a₀(z) under the Kretschmer et al. 2021 pressure-support calibration, P4)

- **Criteria:** `CFG165_FROZEN_CRITERIA.md` (committed 3dc7f31bd, sha256 055e8b58…) before any script existed. Hand estimates in it were made after reading the CFG160/141/140 READMEs and are disclosed as such.
- **Order of work:** my own scripts written from the frozen text alone → main run, MUTATE M1–M6, attacks (a)–(d), power (e) all run and saved → ONLY THEN CFG140/141/160 scripts and outputs opened → `CFG165_diag_conventions.py` written after that (labelled post-comparison; not part of the frozen main).
- **Repo untouched. No network. No absolute home path in any output** (`<repo>` is printed).

## Bottom line

**The decision cell REPRODUCES, and every sensitivity row REPRODUCES.** With my declared conventions the decision cell is Δ′_flat = +0.147 ± 0.044 (+3.3σ), Δ′_H = −0.003 ± 0.045 (−0.1σ), class LEAN RIVAL, against CFG160's +0.144 ± 0.044 and −0.006 ± 0.044. The whole residual difference (0.003 dex) is ONE definition: I used the Hα-geometry inclination column (`inc_sfr_deg`), CFG140 uses `inc_star_deg`. Swapping that one column reproduces CFG160 to four decimals in every row I checked. Nothing else differs.

**What did not survive the attacks** (this is the referee's value, not an error in CFG160's arithmetic):
1. **"First in-regime reading whose central value favours the rival" does NOT survive as a statement about the frozen map.** P3 at the same decision cell (flat +0.250 ± 0.068, +3.7σ; rival +0.100 ± 0.068, +1.5σ) already reads "rival within 2σ, flat above +2σ" = lean rival by CFG160's own map, and P3 gives lean rival in 12 of 24 cells (P4: 14). It survives only in the narrower sense that P4's rival central value (−0.003) sits at zero, where P3's (+0.10) does not.
2. **The lean is a statement about a molecular-only gas budget.** It flips to lean flat at μ_tot ≥ about 1.2 and both readings over-predict at the repo's total-gas medians (μ_tot ≈ 4). Break-even μ: flat 2.14, rival 0.65 (bootstrap 68%: 1.7–2.6 and 0.4–1.0).
3. **The same P4 pipeline through 390 KROSS discs at z ≈ 0.85 points the other way:** flat Δ′ = −0.004 ± 0.015, the rival −0.082 (−4.1σ). The KURVS − KROSS differential (+0.151 ± 0.045) is 3.4σ from flat's 0 and 1.8σ from the rival's +0.071. P4 cuts the P1 "manufactured evolution" (+0.27) roughly in half but does not remove it.
4. **Power (e):** under gas and α nuisance the decision statistic barely discriminates. Likelihood ratio of the observed Δ′_flat, rival truth over flat truth: about 130 idealised, 1.2–1.7 with total-gas median 1.0, 0.5 with median 2.0. P(lean rival | flat truth) = 0.31 (N1) and 0.45 (N2), against the frozen requirement < 0.05.

So the frozen reading "a Kretschmer-conditional lean toward a₀ ∝ H(z), conditional three times" is arithmetically reproduced and fairly stated by CFG160, but it carries roughly no evidential weight once the gas is allowed to be anywhere in 1–2 M* and the α scatter is included. Nothing here says the data favour either law or the framework; κ = ½ and Ω_c h² stay fitted; a lean is not a detection.

## 1. Table vs CFG160, row by row (decision cell and full sensitivity table)

Canonical footing, δ = 0. "CFG160" = the committed `.out`/`.json`, read after my runs. "Mine" = the frozen main run (`inc_sfr_deg`). "Mine, inc_star" = the diagnostic swap (post-comparison). z-columns use each run's own Δ′/σ. Verdict lines are the frozen pass lines: decision cell |ΔΔ′| ≤ 0.01 and σ within 5%; sensitivity rows |Δz| ≤ 0.15.

| row | quantity | CFG160 | mine (frozen main) | mine, inc_star (diag) | verdict |
|---|---|---|---|---|---|
| **decision cell (μ = 0.67, P4)** | Δ′_flat ± σ | +0.144 ± 0.044 (+3.3σ) | +0.147 ± 0.044 (+3.32σ) | +0.144 ± 0.044 | **REPRODUCES** (Δ 0.003; σ within 1%) |
| | Δ′_H ± σ | −0.006 ± 0.044 (−0.1σ) | −0.003 ± 0.045 (−0.06σ) | −0.006 ± 0.044 | **REPRODUCES** (Δ 0.003) |
| | class | lean rival | lean rival | lean rival | matches |
| μ = 0.25 | flat / rival | +0.204 / +0.051 | +0.207 (+4.6σ) / +0.054 (+1.2σ) | +0.204 / +0.051 | **REPRODUCES** |
| μ = 1.5 | flat / rival | +0.053 (+1.2σ) / −0.092 (−2.1σ) | +0.055 (+1.25σ) / −0.089 (−2.01σ) | +0.053 (+1.21σ) / −0.092 (−2.09σ) | **REPRODUCES** (Δz 0.05 / 0.09) |
| μ = 4 | flat / rival | −0.123 / −0.255 | −0.121 (−2.7σ) / −0.252 (−5.7σ) | −0.123 / −0.255 | **REPRODUCES** (both over-predict) |
| α × 0.6 | flat / rival | +0.058 ± 0.045 (+1.3σ) / −0.092 ± 0.046 (−2.0σ) | +0.062 (+1.37σ) / −0.087 (−1.87σ) | +0.058 / −0.092 | **REPRODUCES** (Δz 0.07 / 0.13); rival is at the ±2σ edge |
| α × 1.4 | flat / rival | +0.211 (+4.6σ) / +0.060 (+1.3σ) | +0.212 (+4.64σ) / +0.062 (+1.37σ) | +0.211 / +0.060 | **REPRODUCES** (Δz 0.04 / 0.07) |
| R_e = 2 R_eff | flat / rival | +0.066 ± 0.046 (+1.4σ) / −0.084 ± 0.047 (−1.8σ) | +0.069 (+1.50σ) / −0.079 (−1.68σ), anchor unchanged; +0.071 (+1.53σ) / −0.078 (−1.65σ), anchor also 2× | +0.066 / −0.084 (anchor also 2×) | **REPRODUCES** (Δz ≤ 0.13) |
| P2 (CFG141) | flat / rival | +0.390 ± 0.065 / +0.237 ± 0.063 | +0.391 ± 0.065 / +0.238 ± 0.064 | +0.390 / +0.237 | REPRODUCES (ladder rung) |
| P3 (CFG141 README) | flat / rival | +0.24 ± 0.07 (3.5σ) / +0.09 ± 0.07 (1.3σ) | +0.250 (3.7σ) / +0.100 (1.5σ) | +0.242 (3.5σ) / +0.090 (1.3σ) | REPRODUCES (ladder rung) |
| P1 (CFG140) | flat / rival | +0.398 ± 0.070 / +0.244 | +0.399 / +0.245 | +0.398 / +0.244 | REPRODUCES (ladder rung) |
| P0 (CFG140) | flat / rival | −0.130 ± 0.057 / −0.279 | −0.125 ± 0.059 / −0.272 | −0.130 / −0.279 | REPRODUCES (ladder rung; the 0.005 is the same inclination column) |
| SPARC anchor C1 | median; pooled | +0.064; +0.092 ± 0.013 | +0.064; +0.092 ± 0.013 | (identical; not inclination-dependent) | REPRODUCES |
| 24-cell counts, P4 | flat > +2σ / within / < −2σ | 14 / 6 / (4, implied) | 14 / 6 / 4 | 14 / 6 / 4 | REPRODUCES |
| | rival > +2σ / within / < −2σ | 0 / 14 / 10 | 0 / 15 / 9 | 0 / 14 / 10 | REPRODUCES (mine differs by one edge cell, μ = 1.5 δ = 0 alt, at −1.98σ; disappears under inc_star) |
| grid counts, P2 / P3 | flat > 2σ | 21 / 16 | 21 / 16 | 21 / 16 | REPRODUCES |
| per galaxy | Δ_flat range | −0.11 (KURVS-8) … +0.48 (KURVS-17) | −0.106 … +0.483 | same | REPRODUCES |
| | x, α, V_c²/V² (P4 / P2) | 1.04–3.54, 2.57–3.91, 1.19–2.52 / 1.50–6.06 | identical ranges | | REPRODUCES |
| power R0 | separation per cell | 2.6–3.7σ | 3.1–4.1σ | | DIFFERS (my R0 uses V from the flat prediction and my own error model; frozen as a reported row, no pass line) |
| σ_out per galaxy | CFG141 table | 55±8, 69±13, 28±20, 51±5, 66±5, 61±10, 67±4, 73±4, 62±6, 77±9 | 55.3±7.6, 69.1±13.1, 27.9±20.3, 51.3±5.2, 65.8±4.7, 61.3±9.7, 67.1±4.2, 73.0±4.0, 61.7±6.3, 76.8±8.5 | | REPRODUCES (my σ_out routine written independently) |

**Every difference, classified.**
- **Definition (mine):** inclination column, `inc_sfr_deg` (mine) vs `inc_star_deg` (CFG140). Frozen text gave no column (only "±5°"); I declared `inc_sfr_deg` in section 1 before opening any script. Effect: 0.002–0.005 dex, sigma < 1%. Isolated by `CFG165_diag_conventions.py`.
- **Definition (CFG160's variant):** in the R_e = 2 R_eff row CFG160 applies the doubled R_e to the SPARC anchor too; my frozen row left the anchor at 1.68 R_disk (I also printed the both-2× variant). With both doubled and inc_star: exact.
- **Definition (pooling of Δ′_H's anchor):** I used the flat-law pooled anchor for both laws; CFG160 pools the anchor with the rival law's own weights. Tested: zero effect (the anchor is at z = 0, E = 1, so the two laws coincide).
- **Solver:** none. Kernel `nu_mono` is the same imported object; my pooling, χ²/dof inflation and error propagation reproduce theirs to 1e-4 once the inclination column matches.
- **README wording (CFG160):** (i) "flat is disfavoured in 14 of 24 and survives in 6 of 24" — 14 + 6 = 20; the missing 4 cells are Δ′_flat < −2σ (all at μ = 4 and δ ≥ 0), reported by neither the sentence nor the table; (ii) "the three largest residuals are KURVS 13, 17 and 21. These have the largest x" — the largest x are 21 (3.54), 8 (3.40), 17 (3.12); 13 is fourth (2.56) and 8 is the only large-x galaxy with a negative residual; (iii) "first in-regime reading whose central value favours the rival" — see the P3 point below.
- **Not a difference, but a check:** frozen R0 in my own error model gives 3.1–4.1σ, CFG160 2.6–3.7σ; both use "V replaced by the flat prediction's V" as declared; the ~0.5σ difference is my inclination and mass-slope handling under that substitution. Not scored.

## 2. Does "first reading favouring the rival" survive the P3 point?

**No, not as a statement about the frozen map.** CFG160's own map: "the rival within 2σ at the decision cell, and flat above +2σ there = a lean toward the rival." At the decision cell:
- P3 (CFG141): flat +0.250 ± 0.068 (+3.7σ), rival +0.100 ± 0.068 (+1.5σ) (with CFG140's inclination: +0.242 (3.5σ), +0.090 (1.3σ)). Class: lean rival.
- P4: flat +0.147 (+3.3σ), rival −0.003 (−0.1σ). Class: lean rival.
Across the grid P3 is lean rival in 12 of 24 cells, P4 in 14, P2 in 3. What is new about P4 is only that the rival's central value is at zero rather than +0.09 (still 0.1 dex inside the errors). The sentence should be read "the first reading whose rival central value is consistent with zero at the decision cell", if kept.

## 3. Where independence stops

Reused, not re-derived: `CFG4_common` (ν_mono and the a₀ constants, imported read-only, its two limits re-checked: 5e-7 and 1.5e-12); the Kretschmer α(x) as CFG160 quotes it (I did not read the paper and did not fetch it; C2 checks only the arithmetic); all data files; the CFG140 declared choices (gas bracket, mass/inclination errors, anchor selection, spherical surrogate). Re-derived from the frozen text: sample, baryon model, σ_out, correction, error propagation, pooling, ladder, grid, verdict map. The agreement to 1e-4 after one column swap therefore shows that the frozen text plus the data determine the numbers; it does not test ν_mono, α(x) or the physics.

## 4. Controls (kept as they came)

- **My controls:** C1 (α := 2R/R_d reproduces my own P2 grid, 1.1e-16), C2 (α(0) = 1.475, α(1) = 2.533, α(4) = 3.955; monotone on [0, 4]), C3 (kernel limits), C4 (10 IDs are the f_DM rows, inputs finite, no galaxy has x outside [0, 4]: x 1.04–3.54): 7/7 pass. C1 of the READMEs (SPARC anchor P0 median +0.064, pooled +0.092 ± 0.013): matches.
- **MUTATE** (exit 1 = the control bites; all runs saved):

| MUTATE | what it does | result | frozen expectation | verdict |
|---|---|---|---|---|
| M1 | α ≡ 0 (P0) | Δ′ −0.125 / −0.272; class non-diagnostic (both outside), flat at −2.12σ | "flat within 2σ (borderline) or both outside; must not be lean rival" | bites (exit 1); my "borderline" hedge is why |
| M1b | α ≡ 1 | −0.024 / −0.172 (−3.3σ); lean flat | est. flat 0.00 ± 0.03, rival −0.15 | bites (exit 1); estimate for the rival was 0.02 off |
| M2 | V_c² = V²/(1 + ασ²/V²) | −0.355 / −0.499; both outside | est. −0.35 / −0.50 | bites (exit 1) |
| M3 | laws swapped in the verdict | class non-diagnostic (both outside) | **I expected "lean flat"; that was WRONG.** After the swap flat sits at −0.06σ and the rival at +3.3σ; the map's "lean flat" requires the rival BELOW −2σ, so the swapped pair is not a lean flat. The map is not label-symmetric | bites (exit 1); wrong expectation kept |
| M4 | decision cell at μ = 1.5 | +0.055 (+1.25σ) / −0.089 (−2.01σ); lean flat | lean flat | bites (exit 1) |
| M5 | KURVS v_last × 10^0.3 | +0.556 (+10.9σ) / +0.409 (+7.6σ); both outside | H1 fails | bites (exit 1) |
| M6 | σ_out permuted, seed 165 (informational) | +0.158 (+2.9σ) / +0.005 (+0.1σ); lean rival | need not bite | **does not bite (exit 0)**: the per-galaxy pairing of σ with V is not what carries the lean; the mean σ level is. Kept |

## 5. The attacks (labelled sensitivity grids; the headline stays P4 at the decision cell)

### (a) Forking paths — PASS on shape, and the normalisation is what matters
- Alternatives at the decision cell (median α over the ten; class): Kretschmer table (3.16; lean rival), linear 1.475 + 1.204x (3.63; lean rival), abstract-linear 1 + 0.75x (2.34; lean rival, flat +0.105, +2.2σ), self-gravitating shape rescaled 1.265 R/R_e (3.53; lean rival), constants 1 / 2 / 2.53 / 3 / 3.955 (lean flat / lean flat / lean rival / lean rival / lean rival), table held flat beyond x = 3 (lean rival), table at x ± 0.5 (lean rival).
- Frozen test (every alternative with median α within ×[0.75, 1.25] of P4's keeps lean rival): **PASS** (8 alternatives, 0 change).
- The lean depends on the normalisation, not the shape: normalisation scan s = 0.3 / 0.5 / 0.6 / 0.75 / 1.0 / 1.25 / 1.4 → lean flat / lean flat / non-diagnostic / lean rival / lean rival / lean rival / lean rival. Flat Δ′ = 0 at s = 0.375; rival Δ′ = 0 at s = 1.015; flat drops below +2σ at s = 0.71. R_e,gas/R_eff = 1 / 1.25 / 1.5 / 2 / 3 → lean rival / lean rival / lean rival / non-diagnostic / lean flat.
- Usable calibrations without a fetch: P0–P3 (already run) and the abstract-linear reading. The Kretschmer choice remains one calibration made after P2 and P3 were known; the R_e definition (stellar R_eff vs the gas half-mass radius that the paper's R_e refers to) alone moves the class from lean rival to lean flat between R_e/R_eff = 1.5 and 3.
- **P3 (the "first" claim):** see section 2.

### (b) Gas prior — FAIL as pre-declared (expected)
- Repo data (no fit): PHIBSS (n = 9, CO-detected, z 0.9–2.4, log M* 9.5–10.6, biased high): M_mol/M* median 1.19 (16–84%: 0.79–2.54). Sharma+2024 (n = 186, z 0.76–1.04; the paper's fitted/stacked gas, not detections): M_H2/M* 0.27 (0.17–0.46), M_HI/M* 3.75 (1.39–11.2).
- Decision cell at each: μ = 0.27 lean rival; μ = 1.19 (PHIBSS median molecular) flat +0.087 (+1.97σ), rival −0.059: non-diagnostic; **Sharma total median μ = 4.0: flat −0.122, rival −0.253, both over-predict**; 16th percentile total μ = 1.56: lean flat; PHIBSS + Sharma-HI 4.9: both over-predict.
- Gas-disc scale (HI more extended): at μ = 1.5 the class is lean flat for 2 R_d, lean rival for 3 and 4 R_d; at μ = 4 flat within 2σ for 3–4 R_d.
- Break-even μ (bootstrap of the ten galaxies, 2000, seed 165): flat 2.14 (16/50/84%: 1.68 / 2.13 / 2.64); rival 0.65 (0.38 / 0.66 / 0.97); geometric midpoint 1.18. **The lean holds only for total gas below about 1.2 M*.** Frozen test (lean rival at the repo's total gas and its 16–84% range): **FAIL**.
- Caveat: the Sharma gas is a fitted/scaling quantity for KROSS-like galaxies and PHIBSS is CO-selected; neither is KURVS gas. CFG142's dust limit is not re-used.

### (c) Anchors — mixed
- **SPARC:** the P4 correction to the anchor is negligible (median V_c²/V² = 1.011, max 1.045); the anchor moves +0.005 P0 → P4 (my hand estimate +0.013–0.02 was too big). It does not test a pressure correction of KURVS's size. Anchor σ = 7 / 10 / 15 km/s moves Δ′_flat only 0.149 / 0.147 / 0.140. Binned by x (x < 1.5, 1.5–2.5, > 2.5) the anchor's pooled offset differs between bins (0.135, 0.168, 0.077 under P4), but the P0 → P4 shift is ≤ 0.005 in every bin.
- **KROSS through the identical P4 pipeline (n = 390, μ = 0.67, R = 2r_im so x = 1, α = 2.53; anchored by the same SPARC P4 anchor):** flat Δ′ = −0.004 ± 0.015 (−0.2σ), rival −0.082 (−4.1σ). Under P0 (no correction): −0.147 / −0.227; under P1/P2: +0.125 / +0.049 (over-corrected). So at z ≈ 0.85 the P4 correction lands on the flat law and excludes the rival. KURVS − KROSS differential: P0 +0.022 ± 0.060, P1 +0.274 ± 0.070, P2 +0.266 ± 0.065, **P4 +0.151 ± 0.045** vs flat 0 (+3.4σ) and rival +0.071 (+1.8σ). Frozen test "P4 differential within 2σ of both": **FAIL** (FAIL-flat: +3.4σ). Read: the P4 correction cuts CFG140's unexplained KURVS − KROSS excess (P1: +0.27) roughly in half but leaves it; neither law predicts it. Caveat: the same μ = 0.67 at z 0.85 and z 1.5, KROSS σ₀ as a constant σ, R_e = r_im.
- **Size of the correction (V_c/V − 1):** KURVS P4 9–59% (median 39%), inside the 10–87% that the repo's note attributes to Sharma+2021 (**PASS**, 0/10 above 0.87); P2 23–146%, above 0.87 for 6 of 10; P3 up to 131%. The P4 correction is the only one of the three inside the KROSS-scale range; KROSS P4 itself is 0–87% (median 12%), P1 reaches 176%.

### (d) Range and scatter at R_max — PASS with one wording error
- x = 1.04–3.54, none outside [0, 4], α unclipped; log M* 9.55–10.68 above the 10^9.5 floor. No extrapolation. Two quirks: the table's α(R_e) = 1.475 vs "≈ 1 at R_e" (47% above, inside the 40%–scatter edge; irrelevant at x ≥ 1), and holding α flat beyond x = 3 (0.004 change) or shifting x by ±0.5 (±0.02) leaves the class.
- **Scatter:** CFG160's ×0.6 / ×1.4 band treats the 40% as fully coherent (conservative for the pooled mean). If instead the 40% is random per galaxy (lognormal σ 0.4, 20000 draws, seed 165): Δ′_flat = +0.153 with extra sd 0.026 (my hand estimate 0.027), σ inflates 0.044 → 0.051, z_flat = +2.86, z_H = −0.05: class unchanged (lean rival). PASS.
- **"Largest x = 13, 17, 21":** FAIL (largest x: 21, 8, 17). Wording error in CFG160; no number depends on it.

### (e) What a null would have looked like — the lean carries little weight
N = 20000 per family, seed 165 (seed 166 re-run agrees to ±0.01 in every fraction). Mock truth = the real KURVS baryons, σ_out, errors and anchor; the law generates g; the mock V is g R − α_true σ²; the analysis is the P4 pipeline exactly. Families: ideal (μ_true = 0.67, α exact); N1 (μ_true lognormal median 1.0, 0.3 dex, α × lognormal(0, 0.4) per galaxy × coherent lognormal(0, 0.2)); N2 (same, median 2.0).

| family | truth | mean Δ′_flat (sd) | P(z_flat ≥ 3.3) | class fractions (lean rival / lean flat / non-diag) |
|---|---|---|---|---|
| ideal | flat | +0.024 (0.039) | 0.002 | 0.06 / 0.84 / 0.10 |
| ideal | rival | +0.162 (0.037) | 0.74 | 0.94 / 0.01 / 0.05 |
| N1 | flat | +0.070 (0.093) | 0.18 | 0.31 / 0.46 / 0.23 |
| N1 | rival | +0.202 (0.093) | 0.70 | 0.57 / 0.04 / 0.39 |
| N2 | flat | +0.159 (0.123) | 0.47 | 0.45 / 0.19 / 0.36 |
| N2 | rival | +0.292 (0.119) | 0.89 | 0.32 / 0.01 / 0.67 |

- **Likelihood ratio at the observed Δ′_flat (rival-truth density / flat-truth density):** ideal 130 (Gaussian), 128 (KDE); N1 1.18 / 1.72; N2 0.50 / 0.55.
- **Frozen reading test:** the lean is "justified as stated" only if P(lean rival | flat truth) < 0.05 and P(lean rival | rival truth) > 0.3. N1: 0.306 and 0.572; N2: 0.447 and 0.323. **NOT justified** — the lean is WEAK EVIDENCE once the total gas and α calibration are uncertain at the levels declared. It is strong only in the idealised world in which gas and α are known.
- **Direction correction to my hand estimate:** I expected P(z_flat ≥ 3.3 | flat truth) to FALL from N1 to N2. It rises (0.18 → 0.47): a true gas mass above the assumed 0.67 raises the observed acceleration relative to the assumed-gas prediction, so the mock analysis with too little gas over-reads Δ′ upward. My sign was wrong; kept.
- **Disclosed caveat (frozen mock left as is):** 17.7% of flat-truth galaxies in the ideal family (10% N2, 17% N1) come out with α_true σ² > V_c² (V² floored at 0.25% of V_c²). A flat-truth world with μ = 0.67 nearly excludes those galaxies, itself a finding about how large the P4 correction is. Extra, not frozen: dropping the floored galaxies changes the mean by < 0.01 and the class fractions by < 0.04 (`CFG165_power.out`, EXTRA block).

## 6. Hand-estimate scorecard (frozen criteria section 3; wrong expectations kept)

| estimate | result |
|---|---|
| Δ′_flat +0.14 ± 0.02; Δ′_H −0.015 ± 0.02; σ 0.044 ± 0.008 | +0.147 (in), −0.003 (in), 0.0442 (in) |
| per-galaxy extremes −0.10, +0.49 | −0.106, +0.483 (in) |
| μ-rows +0.20 / +0.054 / −0.12; α × 0.6 / × 1.4 +0.06 / +0.20; R_e × 2 +0.066 | +0.207 / +0.055 / −0.121; +0.062 / +0.212; +0.069 (all in) |
| lean rival at the decision cell | yes |
| grid counts flat 12–15, rival 8–11 | 14; 9 (in) |
| break-even μ flat ≈ 2.0, rival ≈ 0.65 | 2.14, 0.65 (in, 25%) |
| break-even s: flat ≈ 0.3, rival ≈ 0.96 | 0.375, 1.015 (flat estimate 0.08 off; class fine) |
| P4 differential ≈ +0.19 ± 0.08 | +0.151 ± 0.045 (in); "P(within 2σ of flat) = 0.5": WRONG, it is 3.4σ |
| SPARC anchor shift +0.013–0.02 | +0.005 (too big) |
| random-scatter extra sd 0.027; z_flat 2.8 | 0.026; 2.86 (in) |
| M3 "class flips to lean flat" | WRONG (both outside); see M3 |
| power: LR ideal ≈ 230, nuisance 2–5; P(z ≥ 3.3 | flat, nuisance) 0.10–0.25, N2 lower | 130; 1.2–1.7 and 0.5; 0.18 (N1) in range, N2 0.47 (wrong direction) |
| P(reproduce within 0.01): decision Δ′ 0.45 each, σ 0.25, all rows jointly 0.15 | all reproduced (my probabilities were too low: the setup convention was the single risk and it cost 0.003) |

## 7. What would count as disagreement, and what I found

- Decision cell or any sensitivity row outside the pass lines: **none** (after the one-column convention; before it, still inside).
- Grid counts: rival < −2σ is 9 (mine, frozen main) vs 10 (CFG160): one cell at the −2.0σ edge; agrees exactly under inc_star.
- **Valid disagreements found:** (1) the "first reading favouring the rival" sentence (P3 already qualifies by the map); (2) "largest x = 13, 17, 21"; (3) "14 + 6" bookkeeping; (4) the frozen readings' weight: the lean fails the frozen power test (e) and the gas test (b) and the KROSS test (c3), passes the shape test (a) and the range/scatter test (d).
- The frozen lean map is not label-symmetric; a mislabelled law pair does not read as a lean flat (M3).

## 8. Files and re-run

Files (scratch dir; nothing in the repo): `CFG165_FROZEN_CRITERIA.md`, `README.md`, `CFG165_referee_kurvs_p4.py`, `CFG165_attacks_abcd.py`, `CFG165_power_e.py`, `CFG165_diag_conventions.py` (post-comparison), `CFG165_main.out/_results.json`, `CFG165_MUTATE_{1,1b,2,3,4,5,6}.out/_results.json`, `CFG165_attacks.out/_results.json`, `CFG165_power.out/_results.json`, `CFG165_diag_conventions.out`, `CFG165_manifest.txt` (sha256 of inputs, scripts, outputs).

```
export ZF_REPO=<repo>
python3 CFG165_referee_kurvs_p4.py > CFG165_main.out                       # rc 0
for k in 1 1b 2 3 4 5 6; do MUTATE=$k python3 CFG165_referee_kurvs_p4.py > CFG165_MUTATE_$k.out; done   # rc 1 = bites (M6: rc 0, does not bite)
python3 CFG165_attacks_abcd.py > CFG165_attacks.out
python3 CFG165_power_e.py > CFG165_power.out                               # N = 20000, seeds 165 and 166
python3 CFG165_diag_conventions.py > CFG165_diag_conventions.out
```
Whole set runs in under 30 s.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## In-place re-run (orchestrator)

All scripts were re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 1, 1b, 2, 3, 4, 5 exit 1 (bite); MUTATE 6 exit 0 (does not bite, informational, kept); attacks 0; power 0; diagnostics 0. Every `.out` and `_results.json` is identical to the referee's apart from timing. The frozen criteria are `../CFG165_FROZEN_CRITERIA.md` (3dc7f31bd). Read the README's attack (b) and (e) results as the caveats on CFG160's lean: the lean holds only below about 1.2 M* of gas and, once gas and calibration nuisance are allowed, P(lean rival | flat truth) is 0.31-0.45, so it is weak evidence, not a detection.
