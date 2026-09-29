# CFG183 — Referee re-derivation of CFG175 (a third a0(z) law, a0 ∝ t(z)/t0, through the KURVS/KROSS pipeline)

- **Criteria:** `CFG183_FROZEN_CRITERIA.md` (committed 9f29e8e5c, sha256 6fc6d6f4…) before any script existed. Its section 10 (dated data note on the KURVS sigma methods) was added before hashing, on the coordinator's message. Every CFG175 README number in it is a TARGET I read, not a blind prediction; my hand estimates were made after reading it.
- **Order of work:** my scripts written from the frozen text → main run, MUTATE 1–8, attacks (a)–(c) with a4 and c4b, onset grid (d), mocks (e) at seeds 183 and 184, and the stability check all run and saved → ONLY THEN `CFG175_t_law_a0z.py`, `.out`, `_results.json` (and its MUTATE outputs) opened → `CFG183_compare.py` written after that (post-comparison, labelled, not part of any frozen result).
- **Repo untouched. No network, no new data. No absolute home path in any output** (`<repo>`, `<scratch>`).
- Standing rules kept: κ = ½ is FITTED; a0(z) FLAT is the framework's distinctive law, a0 ∝ H(z) the rival, T (a0 ∝ t(z)/t0) the owner's third reading; nothing here says the data favour any law or that the theory is closed; a lean is not a detection.

## Bottom line

**CFG175 REPRODUCES on every pass line P1–P10 (P11, determinism, is reported in section 7) and on all 18 status labels.** Its arithmetic, its summary sentence and its two pinned MUTATE controls are right. What the attacks change is the weight the verdict can carry:

1. **The s = 1 "excluded" label is convention-fragile, as flagged in advance.** T's lower 1σ edge at Kretschmer's correction is 3.547 against the ceiling 3.47 (margin 0.077, 2.2%). It survives every numerical convention I varied (σ convention, inclination column, Ω_m, single z, anchor pooled or median) but not the physical-model choices: 2 of 13 variants flip it (gas-disc scale 1 R_d: 2.51; R_e = 2 R_eff: 2.50), 4 of 10 leave-one-out samples flip it (dropping KURVS-13, -16, -17 or -21), only 52% of ten-disc bootstrap resamples keep it, and in the six discs that the σ methods note does NOT flag it is "gas-allowed" (lower edge 2.58). The other four published prescriptions (s = 1.42–3.00) have margins ≥ 1.17 and are stable to ceilings up to 4.6.
2. **P0 is not physically excluded by anything in the repo, and it is not a neutral default.** The tabulated outer velocities carry no pressure correction; the outer σ is an observed line width (an upper bound on the supporting dispersion). T fits the KURVS P0 reading at gas ≈ 1 M* (PHIBSS median), which needs at least 85% of σ_obs² (1σ; central value all of it) to be non-supporting if K21's radial-support model otherwise holds (a4); at Kretschmer's own lower band edge (α × 0.6) T needs μ = 3.0 [2.4, 3.7], which is gas-ALLOWED.
3. **The P0 fit does not repeat at KROSS at a common gas:** T over-predicts there (−0.041 ± 0.023 at P0, μ = 0.67); R_T(P0) = 2.67 (1σ [1.45, 4.93]) is 1.1σ_ln above the in-repo PHIBSS bracket and 0.16σ_ln from the literature bracket's edge. KROSS itself is heterogeneous (T's P0 level runs from −0.153 to +0.177 across the RT / RT+ / v/σ0 sub-samples).
4. **Mock worlds:** the observed P0 pattern is ≈ 10× more frequent in T at P0 (W1) than in any Kretschmer-pressure world (W2/W3/W6), but only 1.5–1.9× more frequent than in a flat world at its own fit point s = 0.4 (W5); the s = 1 exclusion label is not informative (0.28–0.47 in a T world that fits at P0, 0.60–0.63 in one that needs gas 4.3).

Nothing here says the data favour flat, the rival or T; a lean is not a detection.

## 1. Table vs CFG175, row by row

"CFG175" = its README, and its committed `.out`/`.json` (read after my runs). Mine = the frozen main run (`inc_star_deg`, R_e = R_eff, anchor pooled). Verdict = the frozen pass lines of criteria section 5.

| row | CFG175 | mine | line | verdict |
|---|---|---|---|---|
| P1 t/t0 at Ω_m 0.3111, z = 0.85 / 1.5 / 2.5 (dex) | −0.3256 / −0.5089 / −0.7220 | −0.3256 / −0.5089 / −0.7220; quadrature vs closed form 2e-16 | 0.01 | **REPRODUCES** |
| P1 at Ω_m 0.315 | −0.3264 / −0.5099 | −0.3264 / −0.5099 | 0.002 | **REPRODUCES** |
| P2 flat / rival decision cell | +0.1441 / −0.0060 | +0.1441 / −0.0060 | 5e-4 | **REPRODUCES** |
| P2 break-evens s = 1: KURVS flat / rival | 2.1089 / 0.6211 | 2.1090 / 0.6211 | 0.01 | **REPRODUCES** |
| P2 KROSS flat / rival | 0.6358 / 0.0520 | 0.6359 / 0.0520 | 0.005 | **REPRODUCES** |
| P3 T-anchor minus flat-anchor (dex) | 0.00000 | 0.0 | 0.01 | **REPRODUCES** (vacuous, see below) |
| P4 Δ′_T decision cell | +0.3227 ± 0.0465 (z +6.93) | +0.3227 ± 0.0465 (z +6.94) | 0.010 / 0.004 / 0.3 | **REPRODUCES** |
| P5 T at P0, μ = 0.67 | +0.0457 ± 0.0537 (z +0.85) | +0.0457 ± 0.0537 (z +0.85) | 0.010 / 0.005 / 0.2 | **REPRODUCES** |
| P5 flat / rival z at P0 | −2.28 / −4.62 | −2.28 / −4.62 | 0.2 / 0.3 | **REPRODUCES** |
| P6 R0 | +0.1786 (3.84σ) | +0.1786 (3.84σ) | 0.010 / 0.3 | **REPRODUCES** |
| P7 T KURVS μ_be [1σ], s = 0 / 1 / 1.42 / 1.62 / 1.69 / 3.00 | 1.007 [0.616, 1.465]; 4.335 [3.547, 5.267]; 5.655 [4.636, 6.876]; 6.261 [5.126, 7.627]; 6.470 [5.294, 7.887]; 10.186 [8.227, 12.602] | 1.007 [0.616, 1.465]; 4.335 [3.547, 5.268]; 5.656 [4.636, 6.877]; 6.262 [5.127, 7.627]; 6.471 [5.295, 7.888]; 10.187 [8.227, 12.603] | 4% / 6% | **REPRODUCES** |
| P7 flat KURVS | none; 2.109; 3.096; 3.565; 3.730; 6.845 | none; 2.109; 3.096; 3.566; 3.730; 6.846 (intervals as CFG175) | 4% / 6% | **REPRODUCES** |
| P7 rival KURVS | none; 0.621; 1.257; 1.567; 1.676; 3.829 | same | 4% / 6% | **REPRODUCES** |
| P8 T KROSS μ_be | 0.377; 1.528; 1.947; 2.140; 2.207; 3.391 | 0.377; 1.528; 1.948; 2.140; 2.207; 3.391 | 5% | **REPRODUCES** |
| P8 R_T | 2.673 / 2.838 / 2.904 / 2.926 / 2.932 / 3.004 | 2.672 / 2.838 / 2.904 / 2.926 / 2.932 / 3.004 | 0.08 | **REPRODUCES** |
| P9 18 status labels | T: allowed, then excluded ×5; flat: over, allowed ×4, excluded; rival: over, allowed ×5 | identical (0 of 18 differ) | exact | **REPRODUCES** |
| P9 summary and "strongly disfavoured" flag | "gas-excluded under every published prescription and gas-allowed only without pressure support; STRONGLY DISFAVOURED (z +6.9)" | same | exact | **REPRODUCES** (EDGE-DIFFERS was not triggered; the 2%-margin cell reproduces) |
| P10 fit points μ = 0.67: KURVS rival / flat / T | 1.033 / 0.389 / < 0 | 1.033 / 0.389 / < 0 | 0.04 | **REPRODUCES** |
| P10 KROSS rival / flat / T | 1.868 / 1.039 / 0.256 | 1.868 / 1.039 / 0.256 | 0.08 / 0.06 / 0.06 | **REPRODUCES** |
| P11 determinism | | second full run byte-identical (28 of 28 files) | exact | **REPRODUCES** |

Full-map check (post-comparison, `CFG183_compare.out`): 90 map cells (three laws × six s × KURVS μ ∈ {0.25, 0.67, 1.5, 4} plus KROSS μ = 0.67): max |ΔΔ′| 1.75e-5, max |Δσ| 2.1e-6; 95 finite break-even values and edges: worst relative difference 4.8e-4 (KROSS rival, 0.05199 vs 0.05202).

**Every difference, classified.**
- **Numerical (≤ 1.8e-5 in Δ′; ≤ 5e-4 relative in break-evens):** different code paths. CFG175 exec's CFG141's pipeline and re-implements the P4 pooling and anchor in its own `terms`/`DS`/`pooled` functions; mine imports the CFG165 referee module. The break-even solvers differ (their 36-node log grid + brentq, mine 200 nodes + brentq).
- **Reporting convention:** where no break-even exists, CFG175 still prints an upper edge (flat s = 0: "nan [nan, 0.174]"); I print none. Its KROSS rival s = 1 lower edge is "nan" (no +σ root above 0.01); mine reports the open side as 0.01. Neither enters a label.
- **Exit convention:** CFG175's MUTATE runs exit 0 when the control behaves; mine exit 1 when the control bites, as the frozen text says. Its MUTATE=1 and MUTATE=2 outputs match my M1 and M2 (T rows equal flat's / rival's; identical status rows).
- **Definition:** none needed. My guess for the interval convention (roots of Δ′(μ) = ±σ(μ) with σ at the trial μ) was the one CFG175 uses.
- **README wording / framing (no number wrong):**
  1. The bottom line says T "needs μ = 4.3–10.2 … above the declared ceiling of 3.47". The rule is about the lower 1σ edge, and at s = 1 that is 3.547, 2.2% above the ceiling; the README's own table note states the rule but does not say the margin is that thin.
  2. C3 (T's anchor equals flat's) cannot fail: the SPARC redshifts are exactly 0 in the loader and t/t0(0) = 1, so the anchor difference is 0.0 in both implementations. It is a vacuous control (mine included).
  3. "Under Kretschmer's correction and every stronger published one" treats P0 as "no pressure correction" as if that were the null; the data note (section 4) says it is the uncorrected table, which the authors themselves regard as needing a correction that grows with radius.

## 2. Where independence stops

Imported read-only from `CFG165_kurvs_referee/CFG165_referee_kurvs_p4.py` (shared, NOT independent): `load_kurvs` (with `inc_star_deg`), `load_sparc_anchor`, `load_kross`, `cell` (which calls `per_object`, `pool`, `anchor_pool`), `spec`, `corr`, `gbar`, `gpred`, `alpha_K`, `E_of_z`, and through it `CFG4_common.nu_mono`, the a0 constants and Kretschmer's α(x) as quoted (unverified literature). The law enters the imported pipeline through the module-level `E_of_z` (its "H" output), patched in my own process inside a context manager (`CFG183_common.law_ctx`); controls: E := 1 gives H ≡ flat to 0.0, and the original E replays the rival to 0.0. Also shared: all data files and CFG140's set-up choices (gas bracket, mass error 0.15 dex, inclination ±5°, thin exponential discs, spherical surrogate, g_obs = V²/R, the z = 0 anchor), CFG162's placed s values, and CFG164's PHIBSS-prior summary numbers. Mine: t(z)/t0 (closed form plus quadrature), the residual bookkeeping around the imported cell, break-even root finding and intervals, the status rule, the matrix, fit points, R_T, all attacks and mocks. Agreement therefore shows that the frozen text plus the data plus the shared pipeline determine the numbers; it does not test ν_mono, α(x), the prescriptions, the gas priors, or whether a flowing-vacuum a0 ∝ t(z) is physical.

## 3. MUTATE (exit 1 = the control bites; all 8 saved separately; wrong expectations kept)

| M | what | result | frozen expectation | verdict |
|---|---|---|---|---|
| M1 | T := flat | T rows equal flat's to 0.0; T status s = 0…3: over, allowed ×4, excluded; sentence lost; exit 1 | bites | bites (as expected) |
| M2 | T := rival | rows equal to 0.0; T: over, allowed ×5; exit 1 | bites | bites |
| M3 | T := reciprocal, f = t0/t(z) | D′(decision) −0.064, D′(P0) −0.336; T status over, allowed ×5; exit 1 | "T over-predicts at every s ≤ ~1.5" | bites, but my expectation was **WRONG in detail**: only s = 0 over-predicts; at s ≥ 1 a break-even exists at μ = 0.20 [0.01, 0.51] (allowed) |
| M4 | Einstein–de Sitter time, −0.597 dex at z = 1.5 | D′(decision) +0.350, μ_be(s = 1) 4.65 [3.82, 5.64]; verdict and sentence unchanged; exit 1 (numbers leave P4/P7 lines) | +0.35, μ_be ≈ 5, verdict unchanged | bites on numbers, not on the headline, as predicted (μ_be 7% below my ≈5) |
| M5 | T evaluated at the KROSS redshift for KURVS (−0.33 dex) | D′(decision) +0.264, μ_be(s = 1) 3.60 [2.89, 4.43]; s = 1 label flips to ALLOWED; exit 1 | +0.26; 3.3 [2.7, 4.1]; allowed | bites; the amplitude decides the s = 1 label (μ_be 0.3 above my estimate) |
| M6 | KURVS v_last × 10^0.3 | D′(decision) +0.729, D′(P0) +0.646; all six labels excluded; exit 1 | P0 fit lost, all excluded | bites |
| M7 | flat and T status rows swapped in the printer | printed matrix changes; exit 1 | bites | bites: the printer is label-dependent |
| M8 | σ_out (with its error and gradient) permuted, seed 183 | D′(P0) unchanged (+0.046); D′(decision) +0.292; s = 1 label flips to ALLOWED (lower edge 3.18); exit 1 | "does not bite" | **WRONG expectation kept**: the pairing of σ with the discs moves the s = 1 label (P0 unchanged, since P0 has no σ-term); CFG168's M5 bit in the same way |

## 4. Attacks

### (a) Is P0 physically possible? What must be true, given the σ methods note (criteria section 10)

**What is and is not in the tabulated velocities (from the data note, taken as given):** the outer velocities are inclination-corrected only; no pressure-support correction sits in them (the authors apply a Burkert+10 correction, with one constant σ0, only in their inner f_DM analysis, and call large-radius corrections "poorly constrained by data"). The outer σ(R) is the observed line width: instrumental broadening removed, beam smearing corrected only for σ0 within 3.4 R_d, unresolved bulk and non-circular motion not removed; outer/full ratio 1.13 ± 0.26. So P0 is "the uncorrected table read as V_c", P4 adds a simulation-calibrated term to it, and neither is "already in the data". There is no double-counting risk for P4.

- **a1 s-bands (KURVS, μ fixed; s0 [s at D′ = −σ, s at D′ = +σ]):**

  | μ | flat | rival | T |
  |---|---|---|---|
  | 0.67 | 0.389 [0.233, 0.549] | 1.033 [0.805, 1.301] | < 0 [< 0, 0.023] |
  | 1.01 | 0.534 [0.368, 0.712] | 1.258 [1.002, 1.568] | 0.001 [< 0, 0.147] |
  | 1.50 | 0.742 [0.555, 0.952] | 1.577 [1.276, 1.952] | 0.165 [0.012, 0.305] |
  | 2.05 | 0.975 [0.761, 1.229] | 1.926 [1.571, 2.377] | 0.325 [0.177, 0.481] |
  | 3.47 | 1.579 [1.273, 1.968] | 2.789 [2.286, 3.442] | 0.737 [0.543, 0.971] |

  T fits at P0 for gas ≈ 1 M*; at the ceiling gas it fits at s ≈ 0.74, inside Kretschmer's own ±40% band (0.6–1.4). T's 1σ upper s stays below 0.6 for μ ≤ 2.05 (outside the calibration's own scatter) and reaches 0.97 at 3.47.
- **a2 K21 as a band (break-even and status, ceiling 3.47):** s = 0.6: T 3.005 [2.412, 3.695] **allowed** (flat 1.166, rival 0.035); s = 0.8: T 3.680 [2.994, 4.485] allowed; s = 1.0: T 4.335 excluded; s = 1.4: T 5.595 [4.586, 6.801] excluded. **T is gas-excluded only at Kretschmer's central α and above; at α × 0.6 it is gas-allowed.**
- **a3 what s means (KURVS ten discs):** mean pressure fraction q̄ = mean(1 − V²/V_c²) and V_c/V − 1 (min / median / max): s = 0.1: 0.074, 0.01 / 0.05 / 0.07; s = 0.3: 0.188, 0.03 / 0.13 / 0.21; s = 0.6: 0.308, 0.05 / 0.25 / 0.38; s = 1: 0.415, 0.09 / 0.39 / 0.59; s = 3: 0.654, 0.25 / 0.95 / 1.36. For the isotropic-LOS reading with K21's gradient, s equals (σ_R/σ_los)².
- **a4 required non-supporting fraction f_ns = 1 − s_eff/s_phys of σ_obs² (s_phys = 1, s_eff = s0 clipped at 0; in brackets at the 1σ upper s):** T: μ = 0.67: 1.00 [0.98]; 1.01: 1.00 [0.85]; 1.5: 0.84 [0.69]; 2.05: 0.67 [0.52]; 3.47: 0.26 [0.03]. Flat: 0.61 [0.45]; 0.47 [0.29]; 0.26 [0.05]; 0.03; negative. Rival: ≈ 0 or negative throughout. Classification (frozen): **CONTAMINATION-ALLOWED** (f_ns at μ = 0.67, 1.01, 1.5 lies in [0.7, 1.0]): P0 is the right model for T only if most of the observed outer σ_obs² is non-supporting (beam-smeared, unresolved or non-circular width, or vertical rather than radial), with the gas at ≈ 1 M*. Reported plainly both ways: contamination would move all three laws' fit points down the s axis (flat's fit at s = 0.39 would already need f_ns ≈ 0.6), the ordering of the laws along it does not change, and the note gives no measure of the contamination beyond 3.4 R_d, none at 4–7 R_d, and no anisotropy or vertical geometry.
- **Meaning:** **P0 is not excluded by anything in the repo**, and it is the same kind of statement as the K21 correction: a model of an unmeasured quantity. It is not a neutral default (the tabulated V are uncorrected and the authors regard a correction as needed), and T needs it (or a gas mass of ≳ 3 M*) to fit at all. The one in-hand measure, an outer/full σ ratio of 1.13 ± 0.26, shows the outer dispersion is not smaller than the beam-corrected profile.

### (b) Is the 3.47 ceiling a fair line? — DECLARED CHOICE
3.47 is the 84th percentile of CFG164's most gas-rich declared variant (HI equal to the molecular gas); it is not a physical bound.
- **Status matrix by ceiling** (s = 0 / 1 / 1.42 / 1.62 / 1.69 / 3.00; a = allowed, e = excluded, o = over):

  | ceiling | flat | rival | T |
  |---|---|---|---|
  | 1.69, 1.90, 2.00 | oaeeee | oaaaae | aeeeee |
  | 2.57 | oaaeee | oaaaae | aeeeee |
  | **3.47** | oaaaae | oaaaaa | aeeeee |
  | 3.80, 4.00 | oaaaae | oaaaaa | aaeeee |
  | 5.00 | oaaaae | oaaaaa | aaaeee |

- **Lowest ceiling at which T becomes allowed (= lower 1σ edge):** s = 1: 3.547; 1.42: 4.636; 1.62: 5.127; 1.69: 5.295; 3.00: 8.227. So T is excluded at every published s for all ceilings ≤ 3.5 (the frozen "ceiling-robust" test passes trivially) and **ceiling-fragile above 3.55 at s = 1**, above 4.6 at s = 1.42.
- **Prior-derived smooth alternative** (lognormals matched to the READ CFG164 medians and 16–84% ranges: approximate): P(prior μ ≥ μ_be) at s = 1 is 0.002 (primary), 0.025 (h = 0.5), 0.081 (h = 1), 0.014 (M), 0.013 (Z) for T; 0.078 / 0.285 / 0.479 / 0.190 / 0.187 for flat; 0.83–0.99 for the rival. At s ≥ 1.42 T is ≤ 0.03 in every prior. So relative to flat, T's prior-support at Kretschmer's correction is lower by a factor of 5–40; that ordering does not depend on any hard ceiling, but the size of the "exclusion" does.
- **Fair?** As a declared line applied to all three laws alike it is acceptable, and it excludes flat at P2. It is not fair to read the s = 1 label as a measurement: a ceiling anywhere in 3.55–4.6 makes T allowed at s = 1 and excluded at 1.42+. And a ceiling of 2.0 (near KURVS-15's dust limit) would exclude flat at s ≥ 1.42 and the rival at P2.
- **b3 (ADDED after the frozen list, labelled; T's s = 1 lower edge vs the 3.47 line under 13 conventions):** main 3.547; σ fixed at the break-even 3.535; σ fixed at μ = 0.67 3.589; anchor = median 3.901; anchor = none 5.196; `inc_sfr_deg` 3.566; Ω_m = 0.3111 3.544; Ω_m = 0.30 3.534; single z = 1.5 3.544; gas-disc scale 3 R_d 5.165; alt a0 footing 3.797 — all excluded. **Gas-disc scale 1 R_d 2.511 and R_e = 2 R_eff (KURVS and anchor) 2.501: ALLOWED.** 2 of 13 flip; the numerical conventions are stable, the physical-model choices are not.

### (c) Does the P0 fit survive? (survival := |z_T(P0)| < 2 and the break-even interval overlaps [0.60, 1.69])
- **c1 anchor and definition variants (T at P0, μ = 0.67):** pooled +0.046 (z 0.85), μ_be 1.007 — survives; anchor = median +0.073 (1.36), 1.232 [0.808, 1.726] — survives; **anchor = none +0.137 (2.64), 1.830 [1.338, 2.398] — fails**; gas-disc scale 1 R_d +0.010, 0.724; 3 R_d +0.077, 1.449; alt footing +0.055, 1.090 — survive; R_e variants identical at P0 (no pressure term).
- **c3 inclination column:** `inc_star_deg` +0.0457, 1.007; `inc_sfr_deg` +0.0492, 1.033 — survives (as predicted, ≤ 0.004).
- **c2 KROSS:** T at KROSS: P0 −0.041 ± 0.023 (z −1.8), s = 1 +0.099 ± 0.021 (z +4.7). Differential D_T = Δ′_KURVS − Δ′_KROSS: P0 +0.087 ± 0.058 (1.5σ), s = 1 +0.224 ± 0.051 (4.4σ). Joint χ² of the two anchored levels at common μ = 0.67: T at P0 3.9, at s = 0.26 7.9, at s = 1 70.5; flat at s = 1 10.8; rival at s = 1 17.1. R_T(P0) = 2.67, σ_ln = 0.61 (from the two break-even intervals), 1σ [1.45, 4.93]: 1.07σ_ln from the in-repo bracket's upper edge 1.39, 0.16σ_ln from the literature bracket's edge 2.42: **not KROSS-consistent by the frozen 1σ test** (1.45 > 1.39), consistent within ~1σ_ln, so weakly so. KROSS sub-samples (n = 390 = 217 RT + 173 RT+): T at P0 / s = 1: all −0.041 / +0.099; RT only −0.153 (z −5.1, over-predicts, no break-even) / +0.032 (μ_be 0.917); RT+ only +0.058 (+2.1σ) / +0.160; v/σ0 ≥ 2 +0.112 / +0.174; v/σ0 ≥ 3 +0.177 / +0.217; log M* in KURVS range −0.036 / +0.088; b/a > 0.5 −0.087 / +0.041; z < 0.85 −0.046 / +0.091; z ≥ 0.85 −0.036 / +0.106. T's KROSS P0 level swings by 0.33 dex across the sub-samples, so "T fits KURVS at P0 and needs gas rising 2.7× to KURVS" is not a stable statement about KROSS.
- **c4 leave-one-out (T):** P0 fit survives in **10 of 10**; T's s = 1 label stays "excluded" in **6 of 10**: dropping KURVS-13 (lower edge 3.283), -16 (3.427), -17 (3.028), -21 (3.394) flips it; the others give 3.49–3.79. Flat's P0 z ranges −1.8 to −3.1, rival's −3.9 to −5.9. **Bootstrap of the ten discs (N = 2000, seed 183):** Δ′_T(P0) 16/50/84% = −0.005 / +0.047 / +0.096; μ_be(P0) 0.64 / 1.02 / 1.43; |z_T(P0)| < 2 in 85.2%; μ_be(P0) in [0.60, 1.69] in 79.9%; **T's s = 1 label "excluded" in only 52.3%**.
- **c4b flagged-sub-sample split (partition fixed by the σ methods note, frozen before residuals were used):** A = flagged discs among the ten (KURVS 15, 16, 17, 21; n = 4): T at P0 +0.074 (z +1.06), μ_be(P0) 1.237 [0.701, 1.902]; s = 1 μ_be 5.50, lower edge 4.10, EXCLUDED. U = unflagged (3, 7, 8, 9, 11, 13; n = 6): T at P0 +0.024 (z +0.30), μ_be(P0) 0.842 [0.315, 1.510]; s = 1 μ_be 3.41, lower edge 2.58, **ALLOWED**. Flat's P0 z: A −1.75, U −1.58; rival's: −4.05 / −2.94. **The P0 fit is NOT DRIVEN BY FLAGGED σ PROFILES (holds in both classes); the s = 1 exclusion IS driven by them** (I had seen the ten discs' Δ′ list before writing this partition, but the partition is mechanical from the note's flags and was fixed in the criteria before any run).
- **Verdicts (frozen rule):** P0 fit ROBUST? **No** (fails only for the no-anchor reading, which drops the SPARC z = 0 offset of +0.09 dex that the real data carry; passes every other row and every LOO). s = 1 exclusion ROBUST? **No** (bootstrap 0.52, LOO 6/10). KROSS-CONSISTENT? **No at 1σ, marginal** (see above).

### (d) Dependence on the flow-onset redshift (grid z_on ∈ {∞, 30, 20, 10, 7, 5} × Ω_m ∈ {0.3111, 0.315})
- **Amplitude at z = 1.5:** −0.509 / −0.516 / −0.522 / −0.545 / −0.570 / −0.610 dex (Ω_m 0.3111; the 0.315 column is −0.510 … −0.611); spread 0.102 dex (CFG181 found 0.105 over its wider set), driven by the z_on = 5 cells.
- **Pipeline:** Δ′_T(decision) +0.322 → +0.353; Δ′_T(P0) +0.045 → +0.076; μ_be(s = 0) 1.004 → 1.235; μ_be(s = 1) 4.331 → 4.693 (lower edge 3.544 → 3.861). Status labels identical in all 12 cells (allowed at s = 0, excluded at s ≥ 1); P0 survival holds in all 12. Control: the z_on = ∞, Ω_m = 0.315 row equals the main run (+0.3227, +0.0457).
- **Verdict: ONSET-ROBUST** by the frozen rule (spread < 0.12, labels kept). **One-sided:** any later onset lowers T further, so the Big-Bang member (the headline) is the most gas-friendly member of the T family; the s = 1 margin *widens* with later onset (0.077 → 0.39). The onset spread cannot rescue the s = 1 label. (My estimate μ_be(s = 1) ≈ 5.3 at z_on = 5 was too high; the result is 4.69.)

### (e) What a null would have looked like (mock worlds; N = 10,000 per world and family; seeds 183 and 184)
Real ten-disc baryons, σ_out, errors and anchor (+0.092 dex offset added, the CFG168 lesson). Control E-C1: a noiseless mock analysed at its true (law, s, μ) returns Δ′ = 0 to within 0.005 in all six worlds. Families: ideal and N1 (frozen) and, POST HOC (added after seeing the frozen families), `+sc` (0.12 dex intrinsic scatter per disc). Worlds: W1 T (s, μ) = (0, 1.0); W2 flat (1, 2.14); W3 rival (1, 0.65); W4 T (1, 4.3); W5 flat (0.4, 0.67); W6 rival (1.03, 0.67). Seed 183 numbers (seed 184 agrees: 1 of 288 fractions at the ±0.02 line, exactly 0.0200, the rest inside it):

| world (family) | mean z at P0: flat / rival / T | mean z at s = 1: flat / rival / T | P(O), the observed P0 pattern | P(T "excluded" at s = 1) |
|---|---|---|---|---|
| W1 T (0, 1.0), ideal | −2.82 / −6.16 / +1.07 | +2.79 / −0.69 / +6.42 | 0.650 | 0.281 |
| W1, N1 | −2.15 / −5.07 / +1.30 | +2.92 / −0.37 / +6.40 | 0.450 | 0.434 |
| W2 flat (1, 2.14), ideal | −0.80 / −2.92 / +1.63 | +3.68 / −0.05 / +7.61 | 0.068 | 0.634 |
| W3 rival (1, 0.65), ideal | −0.79 / −3.02 / +1.72 | +3.73 / −0.07 / +7.66 | 0.052 | 0.654 |
| W4 T (1, 4.3), ideal | −0.61 / −2.46 / +1.55 | +3.52 / +0.06 / +7.38 | 0.051 | 0.611 |
| W5 flat (0.4, 0.67), ideal | −2.08 / −5.09 / +1.39 | +3.22 / −0.53 / +7.13 | 0.422 | 0.438 |
| W6 rival (1.03, 0.67), ideal | −0.80 / −2.99 / +1.66 | +3.65 / −0.13 / +7.59 | 0.054 | 0.617 |

(The real data: P0 z = −2.28 / −4.62 / +0.85; s = 1 z = +3.28 / −0.14 / +6.94.)
- **Frozen reading (P(O | W1) − P(O | other), ideal / N1):** vs W2 +0.58 / +0.42 (seed 184: +0.59 / +0.40), vs W3 +0.60 / +0.42, vs W6 +0.60 / +0.41: IDENTIFIES (points to T); vs **W5 +0.23 / +0.17 (seed 184: +0.22 / +0.15): the frozen line reads IDENTIFIES for ideal and WEAK for N1**; with the post-hoc scatter +0.23 / +0.16 vs W5 (IDENTIFIES / WEAK). **My frozen expectation ("DEGENERATE between T at P0 and flat with Kretschmer pressure and more gas, |ΔP| < 0.10, P = 0.75") was WRONG.** The observed P0 pattern is rare in a flat world at (1, 2.14): the mock gives flat z(P0) = −0.8 there, not −2.3. The reason (diagnosed, not repaired): the mocks are zero-heterogeneity worlds, and the real data's P0 reading relative to their s = 1 reading has an extra ≈ −0.09 dex that a smooth world lacks (real D′_flat(P0) − D′_flat(s = 1, μ = 2.1) = −0.13; mock −0.04). The post-hoc 0.12 dex scatter moves z_flat(W2) only from −0.80 to −0.44, so it does not close the gap. What can be said: the P0 pattern points to LOW-pressure worlds of any law (T at P0, or flat at its own fit point s = 0.4), and between those two it is weak (ΔP 0.15–0.24).
- **The s = 1 exclusion label is not informative:** P(T "excluded" | W4) = 0.60–0.63 and | W1 = 0.28–0.47 (frozen line: > 0.5 and < 0.05 both). It fires in a third to a half of the worlds in which T fits at P0 with gas 1 M*, and in only ≈ 0.6 of those in which T needs 4.3 M*: the label carries little information at the 2% margin.
- **Caveats:** KURVS only (no KROSS in the mocks); no COSMOS half; the floored-galaxy fraction is 0–14% (worlds with pressure and N1 scatter reach 10–14%); mocks lack the real data's heterogeneity.

## 4b. Provenance note (dated 2026-09-29, added on the coordinator's message; from the calc chat, commit 27bcce5a4, with the data chat's digitisation 5e8617c81; taken as given, not re-verified by me)

The KURVS outer velocity that every a0(z) lane reads (`v_at_last_point_kms`, the paper's Table B1 column 3) is the authors' fitted exponential-disc MODEL evaluated at R_max, not a measured data point: model(R_max)/sin i_SFR equals the column to about 1% for all ten discs. My lane imports the same column through the CFG165 loader (`load_kurvs`), so it inherits this. **It does not change what I reproduced:** CFG175's numbers, CFG183's re-derivation of them, the MUTATE outcomes and the attacks are all statements about the pipeline as run on that column, and they stand as printed. The calc chat re-runs the test with the measured markers as CFG189; nothing in this README anticipates that result.

**How it bears on the P0 versus P4 question (attack (a)):** a model value at R_max carries no measured outer-dispersion signal. The observed σ_out enters the pipeline only through the pressure term (α σ_out²), never through V. So (i) the pressure correction is being added to a fitted-model velocity, and whether that model already absorbs some of the outer support (it was fitted to the inner rotation curve and extrapolated) is not something the tabulated column can tell; (ii) the P0-versus-P4 contrast is a contrast between a model V read as V_c and a model V plus a calibrated term, and neither sees a measured outer V; (iii) this is consistent with what the mocks and mutations found: permuting σ_out across the discs leaves the P0 level unchanged (M8: +0.0457 before and after) and changes the s = 1 statistics only through the pairing (the s = 1 label flips), and CFG165's M6 did not bite for the same reason (the mean σ level carries the lean, not the per-disc pairing). The attack-(a) reading above should therefore be taken as conditional on the model column: the conditions I list for P0 (most of σ_obs² non-supporting) are conditions on the pressure term, and they would have to be re-derived on measured outer markers, which is what CFG189 does.

## 5. Plain answers to the four questions asked

1. **Is P0 physically possible, given the σ methods note?** Not excluded by anything in the repo, and not a neutral default. The tabulated outer V carry no pressure correction; σ_out is the observed line width, an upper bound on the supporting dispersion (beam smearing beyond 3.4 R_d uncorrected, unresolved and non-circular motion not removed); the authors apply a radius-growing correction in their own inner analysis and call the outer one poorly constrained. For T to fit at the PHIBSS median gas, at least 85% (1σ; central value all) of σ_obs² must be non-supporting if K21's structure otherwise holds; at K21's lower band edge (α × 0.6) T needs gas 3.0 M*, which is inside the declared ceiling. Nothing in the repo measures the contamination at 4–7 R_d or the anisotropy. And the outer V read by every lane is the authors' fitted model at R_max, not a measured point (section 4b): it carries no measured outer-dispersion signal, so the P0-versus-P4 contrast is a contrast on the pressure term added to a model value, conditional until CFG189 repeats it on the measured markers.
2. **Is the 3.47 ceiling fair?** A declared choice (84th percentile of the h = 1 variant), applied to all three laws alike, acceptable as such; but T's s = 1 label flips for any ceiling ≥ 3.55, while T at s ≥ 1.42 stays excluded up to ceilings ≈ 4.6. The smooth prior-support numbers (T 0.002–0.08 at s = 1 against flat 0.08–0.48) carry the ordering without a hard line.
3. **Is the s = 1 exclusion label convention-fragile?** Yes, on physical choices, not on numerical ones: 2.2% margin; 2 of 13 model variants flip it; 4 of 10 leave-one-out; 52% of bootstrap resamples; ALLOWED in the six discs the σ note does not flag (EXCLUDED in the four it flags); flips under one σ_out permutation, one amplitude change (M5) and the K21 lower band edge. The summary sentence "gas-excluded under every published prescription" is therefore right as computed and rests, at Kretschmer's correction, on a label that no robustness test supports at the 90% level. The exclusions at s = 1.42–3.00 are stable to the ceiling, the onset and the numerical conventions.
4. **Are a T world and a flat world with more gas distinguishable on this map?** Only partly. A flat world at Kretschmer's pressure and gas 2.1 M* does NOT reproduce the observed P0 pattern in the mocks (P(O) 0.07 against 0.65 for T at P0) — a wrong expectation of mine, kept — but a flat world at its own fit point (s = 0.4, gas 0.67) does 0.42, so T at P0 and flat at low pressure are only weakly separated (ΔP 0.15–0.24). The s = 1 exclusion label does not separate them at all. The KURVS − KROSS differential and the gas ratio R_T do not separate the three laws either (CFG170).

## 6. Hand-estimate scorecard (criteria section 4; wrong expectations kept)

| estimate | result |
|---|---|
| t/t0 −0.326 / −0.509 dex | −0.3256 / −0.5089 (in) |
| Δ′_T decision +0.32 ± 0.02; σ 0.047; z 6.9 ± 0.4 | +0.3227; 0.0465; 6.94 (in) |
| Δ′_T(P0) +0.05 ± 0.02; σ 0.054 | +0.0457; 0.0537 (in) |
| R0 +0.179 ± 0.01 | +0.1786 (in) |
| T μ_be s = 0: 1.0 ± 0.1; s = 1…3: 4.3 / 5.65 / 6.3 / 6.5 / 10.2 | 1.007; 4.335 / 5.656 / 6.262 / 6.471 / 10.187 (in) |
| lower/upper edge at s = 1: 3.55 ± 0.25 / 5.27 ± 0.4 | 3.547 / 5.268 (in) |
| status of T at s = 1 "excluded" (P 0.55); 18 labels (0.50); headline (0.50); ALL rows first run (0.35) | all reproduce; **my probabilities were too low** (the shared pipeline plus the pinned conventions determine the numbers) |
| KROSS T μ_be 0.38 ± 0.05 / 1.53 ± 0.10; R_T 2.67–3.0; fit points | in |
| MUTATE M1–M6 all bite as predicted (P 0.55) | M1, M2, M4, M5, M6 as predicted; **M3 wrong in detail**; M7 as predicted; **M8 wrong (it bites)** |
| (a) s0 at μ = 1.5 / 2.05 / 3.47: ≈ 0.2 / 0.4 / 0.7 | 0.165 / 0.325 / 0.737 (in, 2.05 low by 0.075) |
| (a) T at α × 0.6: μ_be ≈ 3.0 [2.4, 3.7], allowed (P 0.70) | 3.005 [2.412, 3.695], allowed (in) |
| (b) flip ceilings and matrices | as predicted (3.55; 4.0 → {s = 1}; 5.0 → {1, 1.42}; 2.0 excludes flat ≥ 1.42, rival at P2) |
| (c) median anchor +0.07 (z 1.3), μ_be ≈ 1.3; inclination ≤ 0.005 | +0.0732 (1.36), 1.232; 0.0035 (in) |
| (c) ≥ 1 LOO flips the s = 1 label (P 0.85); P0 survival in all LOO (0.70) | 4 flip; 10 of 10 (in) |
| (c) KROSS T at P0 over-predicts by "several σ" (Δ′ ≈ −0.05 ± 0.04 vs σ 0.015–0.02) | −0.041 ± 0.023, −1.8σ: **σ estimate wrong** |
| (c) R_T(P0) 1σ [2.0, 3.5], ≈ 2.4σ above the in-repo bracket | 1σ [1.45, 4.93], 1.07σ_ln: **my σ_ln (0.27) was too small; the real one is 0.61** |
| (d) −0.51 / −0.53 / −0.55 / −0.61 dex; spread 0.10; Δ′ +0.32 → +0.36; Δ′(P0) +0.05 → +0.08 | −0.510 / −0.523 / −0.546 / −0.611; 0.102; +0.353; +0.076 (in) |
| (d) μ_be(s = 1) ≈ 4.3 → 5.3 | 4.335 → 4.693: **too high** |
| (a4) f_ns of T at μ ≤ 1.5 in [0.7, 1.0]; (c4b) subsets ≥ 3 discs (0.6), P0 fit in both (0.5) | 1.00 / 1.00 / 0.84; A = 4, U = 6; holds in both (in) |
| (e) P(O) degenerate between W1 and W2, |ΔP| < 0.10 (P 0.75) | ΔP +0.58: **WRONG** (see (e)); vs W5 +0.15…+0.24 |
| (e) s = 1 exclusion informative only "up to about half" | 0.60–0.63 vs 0.28–0.47 (in the sense stated) |

## 7. Files, controls and re-run

Scripts: `CFG183_common.py` (my helpers; imported by all), `CFG183_referee_main.py` (main and `MUTATE=k`, k = 1–8), `CFG183_attacks_abc.py` (a, a4, b, b3, c, c4b), `CFG183_onset_d.py`, `CFG183_null_e.py SEED` (mocks), `CFG183_null_e_stability.py`, `CFG183_compare.py` (post-comparison, opens the CFG175 files), `run_all.sh`. Outputs: `CFG183_main.out` / `_results.json`, `CFG183_MUTATE_{1..8}.out` / `_results.json`, `CFG183_attacks_abc.out` / `_results.json`, `CFG183_onset_d.out` / `_results.json`, `CFG183_null_e_seed{183,184}.out`, `CFG183_null_e_results_seed{183,184}.json`, `CFG183_null_e_stability.out`, `CFG183_compare.out`, `CFG183_determinism.out`, `run_all.out`, `CFG183_manifest.txt` (sha256 of the scripts and outputs; `.err` files hold warnings only and are empty here).

Controls (main run, all pass): P1 (three lines), C-import (E := 1 gives H ≡ flat; the original E replays the rival, both 0.0), P2, P3 (vacuous); mock E-C1 passes in all six worlds.

```
export ZF_REPO=<repo>
cd <lane dir holding these scripts>
bash run_all.sh
# expected: main rc 0; MUTATE 1-8 rc 1 (all bite); attacks_abc 0; onset_d 0; null_e seeds 183 and 184 0; stability 0; compare 0
```
Runtimes on an idle machine: main ≈ 12 s, each MUTATE ≈ 25 s, attacks ≈ 15 s, onset ≈ 5 s, each mock seed ≈ 3–5 min (12 processes), compare a few seconds.

**P11 determinism: PASS.** The full `run_all.sh` re-run (with the machine heavily loaded) reproduced all 28 `.out` and `_results.json` files byte for byte against the first saved set (sha256, `CFG183_determinism.out`); the mock outputs are deterministic because every (world, family) job seeds its own generator from (seed, world, family).

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.

## In-place re-run (orchestrator)

`bash run_all.sh` was re-run in this directory with `ZF_REPO` set (`run_all.out`): main 0; MUTATE 1-8 exit 1 (all bite); attacks, onset, the null mocks (seeds 183 and 184), the stability check and the post-comparison exit 0. Every `.out`, `.err` and `_results.json` is identical to the referee's apart from timing lines (the referee's `run_all.out` lacks the `stability` line because it ran that script separately). `CFG183_determinism.out` is the referee's own determinism check (28 of 28 files identical by sha256 on its full re-run), kept as produced. The frozen criteria are `../CFG183_FROZEN_CRITERIA.md` (9f29e8e5c).
