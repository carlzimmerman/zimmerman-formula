# CFG175 — a third a₀(z) law, a₀ ∝ t(z)/t₀ (CFG174's accumulation reading), through the KURVS/KROSS pipeline

- **Criteria:** frozen in `CFG175_FROZEN_CRITERIA.md` (cc39c2055), before any number of this lane was computed.
  - The data had been seen by many lanes, and the law was written with the KURVS results known. Both are disclosed there.
- **Script:** `CFG175_t_law_a0z.py`, a few seconds.
  - It runs CFG141's pipeline read-only and unmutated in every mode, with CFG160's P4 α verbatim and CFG170's root-finding.
  - The laws are flat a₀, the rival a₀ E(z), and T = a₀ t(z)/t₀, the flat-ΛCDM age ratio on the pipeline's background (Ω_m = 0.315).
  - T is −0.33 dex at z = 0.85 and −0.51 dex at z = 1.5.
- **Runs:**
  - The main run passes C1–C3 and exits 0. The headline is reported.
  - MUTATE=1 sets T to flat: T's rows equal flat's exactly, and the headline changes; exit 0.
  - MUTATE=2 sets T to the rival: T's rows equal the rival's exactly; exit 0.

## Bottom line

**By the declared rule, T is STRONGLY DISFAVOURED. It is gas-excluded under every published pressure prescription (z = +6.9 at the decision cell), and gas-allowed only without pressure support. Stated plainly both ways: T's standing turns entirely on the outer pressure support.**

- **Under Kretschmer's correction and every stronger published one (s = 1.00–3.00),** T needs a KURVS gas fraction μ = 4.3–10.2. That is above the declared ceiling of 3.47.
  - At the decision cell (μ = 0.67, s = 1), T under-predicts by +0.323 ± 0.047 (+6.9σ). Flat is at +3.3σ and the rival at −0.1σ.
- **With no pressure correction (P0, s = 0),** T is the only one of the three laws that fits KURVS:
  - T +0.046 ± 0.054 (+0.85σ); flat −2.3σ; rival −4.6σ.
  - Its break-even there is μ = 1.01 [0.62, 1.47], the median of CFG164's measured PHIBSS prior.
  - Flat and the rival over-predict at P0 for every gas fraction.
- **So a falling a₀(z) is, on these data, nearly equivalent to ignoring the outer pressure support.** T lives at the low-pressure end of CFG162's axis.
- The expectation written into the criteria was right in both halves.

| s (prescription) | flat: KURVS μ_be | rival: KURVS μ_be | T: KURVS μ_be | status (flat / rival / T) | T: KROSS μ_be | R_T |
|---|---|---|---|---|---|---|
| 0 (P0, none) | none (over-predicts) | none (over-predicts) | **1.007 [0.616, 1.465]** | over / over / **allowed** | 0.377 [0.227, 0.538] | 2.67 |
| **1.00 (P4, Kretschmer)** | 2.109 [1.596, 2.705] | 0.621 [0.289, 1.006] | **4.335 [3.547, 5.267]** | allowed / allowed / **excluded** | 1.528 [1.324, 1.744] | 2.84 |
| 1.42 (Dalcanton & Stilp) | 3.096 [2.423, 3.887] | 1.257 [0.822, 1.766] | 5.655 [4.636, 6.876] | allowed / allowed / excluded | 1.947 [1.723, 2.186] | 2.90 |
| 1.62 (P3, fixed height) | 3.565 [2.808, 4.462] | 1.567 [1.076, 2.144] | 6.261 [5.126, 7.627] | allowed / allowed / excluded | 2.140 [1.906, 2.390] | 2.93 |
| 1.69 (Price n = 1) | 3.730 [2.942, 4.665] | 1.676 [1.165, 2.279] | 6.470 [5.294, 7.887] | allowed / allowed / excluded | 2.207 [1.969, 2.460] | 2.93 |
| 3.00 (P2, self-gravitating) | 6.845 [5.407, 8.611] | 3.829 [2.873, 4.994] | 10.19 [8.23, 12.60] | **excluded** / allowed / excluded | 3.391 [3.090, 3.710] | 3.00 |

- Brackets are 1σ root-find intervals. "Excluded" means the lower edge of the KURVS break-even lies above 3.47, the 84th percentile of CFG164's most gas-rich declared prior (HI equal to the molecular gas).
- The same rule excludes flat at P2, so it is not aimed at T.

## The fit point on the pressure axis (μ = 0.67)

- **KURVS:** the rival fits at s₀ = 1.03 and flat at 0.39. T needs s₀ < 0: even with no correction it under-predicts slightly at μ = 0.67, and it fits at μ = 1.0.
- **KROSS:** the rival 1.87, flat 1.04, T 0.26.
- **The ordering is the same in both samples:** the lower a law's a₀(z), the less outer pressure support it can tolerate.
- **KROSS alone (reported, not the headline rule):** under Kretschmer, T needs μ = 1.53 [1.32, 1.74] at z ≈ 0.85, and flat needs 0.64. KROSS's own gas is not measured here.

## The two-epoch ratio for T (reported)

- T needs the gas fraction to rise by R_T = 2.7–3.0 between KROSS and KURVS, like flat and the rival (CFG170).
- The in-repo PHIBSS bracket [0.73, 1.39] excludes that. The abstract-level literature bracket [1.61, 2.42] lies just below it, even at P0 (2.67).
- The ratio does not distinguish T from the other two laws.

## Reading

- **Under the published pressure corrections, the data want flat or rising a₀(z), and T fails badly:**
  - it needs 4–10× M* of cold gas in ten rotation-supported discs;
  - CFG164's measured prior puts their gas at about 1× M*;
  - KURVS-15's dust limits its gas to < 1.9× M* (nominal).
- **Without any pressure correction, T is preferred of the three,** at the measured gas.
  - No lane has excluded P0: CFG140's correction calls it a scenario.
  - But every published treatment of these discs' measured outer dispersions (σ_out/σ₀ ≈ 1.05, CFG141) applies a substantial correction.
- **What would decide it** is the same as for the other two laws:
  - a measurement of the outer pressure support: the discs' vertical structure, or a pressure-free tracer;
  - the discs' own gas.
  - If the outer dispersion carries no pressure support, T is preferred. If it carries the support the simulations and analytic models give, T is excluded.
- **This is one reading of the owner's picture,** the accumulation reading of CFG174's Q3. A non-accumulating reading makes no a₀(z) prediction here.

## Controls

- **C1:** with CFG174's cosmology, t/t₀ gives −0.3256 / −0.5089 / −0.7220 dex at z = 0.85 / 1.5 / 2.5 (CFG174: −0.33 / −0.51 / −0.72). At the pipeline's Ω_m = 0.315 the values used are −0.3264 / −0.5099.
- **C2:** flat and the rival reproduce CFG160's decision cell (+0.1441 / −0.0060) and CFG170's s = 1 break-evens (KURVS 2.1089 / 0.6211; KROSS 0.6358 / 0.0520).
- **C3:** T's SPARC anchor equals flat's; the anchor is at z = 0.
- **R0 (power):** Δ′_T − Δ′_flat at the decision cell is +0.179 dex, 3.8σ. T sits further from flat than the rival does: at z = 1.5 its a₀ is 0.51 dex lower, while the rival's is 0.37 dex higher.
- **MUTATE=1 and MUTATE=2:** as above; both behave.

## Untested (declared)

- pressure beyond the placed prescriptions;
- the COSMOS half of KURVS;
- KROSS's gas;
- t(z) beyond flat ΛCDM.

κ = ½ and Ω_c h² stay fitted. Nothing here says the data favour any model, or that the theory is closed.

## Provenance correction: the KURVS outer velocity is a model value (appended 2026-09-29; the text above is unchanged)

- **The KURVS outer velocity this lane uses is the authors' fitted exponential-disc MODEL evaluated at R_max, not the last measured data point.** It is Table B1 col 3, read as `v_at_last_point_kms` through CFG140's loader.
- **How this was established.** The data chat's digitisation of the paper's figures (5e8617c81, `data_assembly/arxiv_tables/kurvs_rc_profiles/`) includes a control file (`kurvs_rc_control_vs_table.csv`). In it, the authors' model curve at R_max divided by sin i_SFR equals the tabulated velocity to about 1% for all ten discs (for example KURVS-3: 208.6 against 209.8 km/s; KURVS-15: 113.2 against 112.2). I checked this from the control file alone.
- **Where the record says otherwise.** Where this lane or CFG140 calls the velocity "measured" or "the velocity at the last observed point", read "the fitted model at R_max". The authors deprojected it with i_SFR; CFG140 uses i* only in its inclination-error term.
- **The a₀(z) numbers here are therefore model-velocity numbers.** The measured outer markers can differ from the model: an indicative, unreconciled probe found −15% to +10% for seven discs.
- **A re-run with the measured outer markers** is planned as a new frozen lane (proposed CFG189), after CFG184. The measured markers have not been read in the meantime.

## After CFG183's independent re-derivation (appended 2026-09-29; the text above is unchanged)

- **Wording (it replaces the "STRONGLY DISFAVOURED" label above): T is disfavoured under Kretschmer at the decision cell with a 2% margin; not robust to the gas ceiling, the sample or the calibration.**
- **What reproduces.** CFG183 (73373cd0d) is the Opus chat's independent re-derivation. It reproduces every pass line and all 18 status labels:
  - T's decision cell +0.3227 ± 0.0465;
  - P0: T +0.0457 ± 0.0537, flat −2.28σ, rival −4.62σ;
  - every break-even, fit point and R_T.
- **(1) The s = 1 "gas-excluded" label is fragile.** T's lower 1σ edge is 3.547 against the declared ceiling of 3.47 (margin 0.077, 2.2%). It flips:
  - for any ceiling ≥ 3.55;
  - for 2 of 13 physical variants (gas-disc scale 1 R_d: 2.51; R_e = 2 R_eff: 2.50);
  - for 4 of 10 leave-one-out samples (dropping KURVS-13, -16, -17 or -21);
  - under one σ_out permutation (CFG183's M8).
  - Only 52% of bootstrap resamples keep it, and in the six discs the σ-methods note does not flag, T reads gas-allowed (lower edge 2.58).
  - At s ≥ 1.42 the margins are ≥ 1.17, and T stays excluded for ceilings up to about 4.6.
- **(2) P0 is the uncorrected table, not a neutral null.** The tabulated outer velocities carry no pressure correction, and σ_out is an observed line width, an upper bound on the supporting dispersion. The corresponding phrasing above ("gas-allowed only without pressure support") should be read with that in mind.
  - For T to fit at the PHIBSS-median gas, at least 85% of σ_obs² must be non-supporting (1σ; the central value needs all of it).
  - At Kretschmer's own lower band edge (α × 0.6), T needs μ = 3.0 [2.4, 3.7], which is gas-ALLOWED.
- **(3) The P0 fit does not repeat at KROSS at a common gas.** T over-predicts there: −0.041 ± 0.023 at μ = 0.67, P0. KROSS itself is heterogeneous: T's P0 level runs from −0.153 to +0.177 across the RT, RT+ and v/σ₀ sub-samples.
- **(4) Mocks** (N = 10,000 per world):
  - The s = 1 exclusion label is not informative. It fires in 0.28–0.47 of worlds where T fits at P0 with 1 M* of gas, and in 0.60–0.63 of worlds where T needs 4.3 M*.
  - The observed P0 pattern is about 10× more frequent in a T-at-P0 world than in Kretschmer-pressure worlds, but only 1.5–1.9× more frequent than in a flat world at its own fit point (s = 0.4).
- **(5) The onset of the flow is not a loophole.** T's amplitude at z = 1.5 varies by 0.102 dex over the flow-onset redshifts tested, and one-sidedly: a later onset lowers T further and widens the s = 1 margin.
- **(6) Framing items, mine:**
  - the bottom line quotes central break-evens (4.3–10.2), while the rule uses the lower 1σ edge (3.547 at s = 1);
  - C3 cannot fail: SPARC's redshifts are exactly 0 in the loader, so t/t₀ = 1 and the control is vacuous;
  - calling P0 "no pressure correction" reads it as a null, which it is not.
- **CFG189's measured-marker re-run** (T +5.5σ; s = 1 break-even 3.80, lower edge below the ceiling) carries the same caveat.
