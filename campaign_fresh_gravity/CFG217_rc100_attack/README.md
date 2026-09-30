# CFG217 — the attack on CFG216: gas prior, pressure, prior-driven f_DM and a mis-scaling mock

> **Read the last section first (added 2026-09-29):** the 'about 0.15 to 0.25 dex between z ≈ 0.6 and z ≈ 2.5' below mixes two z baselines. On the chart's own axis V1 sits at −0.25 dex and V4 at −0.21 dex, not −0.15 and −0.13; the chart ticks are fixed.

- **Criteria:** `FROZEN_CRITERIA.md` (0c2aa7da9 + addendum 04a8a927f), committed before any number. **κ = ½ FITTED, NOT DERIVED.** The aim was to break CFG216's "the rival's z-dependence is not in the data".
- **Run:** `python3 campaign_fresh_gravity/CFG217_rc100_attack/cfg217_attack.py`, about 20 s. C1, C2 (the baseline reproduces CFG216 to 1e-16) and C4 pass. `C-recon` is a reported check and failed (0.229 dex). `MUTATE=1` passes: every slope moves by exactly +0.200.

## Bottom line

**The rival's deficit survives the pressure term, the g_bar dependence and a prior-driven f_DM. It does NOT survive a differential baryon-mass systematic of about 0.15 to 0.25 dex between z ≈ 0.6 and z ≈ 2.5. So CFG216 is gas-route-limited, not attack-robust.**

- **Frozen literal outcome: ATTACK-BROKEN, and it is a power artefact.**
  - The reconstruction of M★ from M_bar under the Tacconi+18 scaling was rejected: median |Δ log M★| = 0.229 dex against the 0.15 line, using the 38 RC41 overlaps.
  - So G1 ran on those 38 with actual M★ and M_gas. Even the baseline V0 fails the survival rule there: slope −0.056 [−0.123, +0.014].
  - The literal rule therefore cannot discriminate. The informative rows are below.
- **What survives** (full sample of 100, adopted baseline: rival slope −0.092 [−0.128, −0.055], 4.9σ from its expectation):
  - **G3, the pressure term:** at α = 1.68 the rival slope is −0.124 [−0.163, −0.083] (6.1σ), and at α = 0 (98 galaxies) −0.149. **The flat law's slope also goes negative:** −0.067 [−0.112, −0.028] and −0.098 [−0.140, −0.053]. So with moderate pressure support the data prefer neither pure law: a₀ declining with z, or heavier baryons at high z.
  - **G7, g_bar dependence:** the residual z-slopes are unchanged (flat −0.027, rival −0.092 [−0.125, −0.055]), so the drift is not a g_bar slope in disguise.
  - **G2, prior-driven f_DM (RC41 overlap, n = 38):** Spearman ρ(δ_flat, Δ_prior) = +0.28, p = 0.093, below the frozen line. The z-slope after removing it is +0.009 [−0.044, +0.075].
- **What does not survive** (post hoc, all 100 galaxies with the reconstructed M★; frozen G1 could not be run on all of them):

| variant | flat slope | rival slope | rival's deficit survives? |
|---|---|---|---|
| V0 baseline | −0.029 [−0.071, +0.002] | −0.092 [−0.128, −0.055] | yes |
| V1 gas fraction fixed with z | **+0.066 [+0.027, +0.101]** | **−0.003 [−0.038, +0.034]** | **no: reverses to rival-like** |
| V2 0.5 μ | +0.012 [−0.027, +0.051] | −0.056 [−0.090, −0.017] | borderline (2.99σ) |
| V3 2 μ | −0.082 [−0.123, −0.047] | −0.132 [−0.167, −0.095] | yes |
| V4 0.18 μ (α_CO 0.8) | +0.054 [+0.014, +0.097] | −0.019 [−0.058, +0.020] | **no: reverses** |
| V5 1.49 μ (α_CO 6.5) | −0.061 [−0.100, −0.026] | −0.113 [−0.150, −0.079] | yes |

  - Under V1 and V4 the rival becomes consistent (slope ≈ 0) and the flat law is disfavoured at 3.6σ and 2.5σ. The differential baryon-mass factors (low-z half / high-z half) are 1.20/0.85 for V1 and 0.73/0.54 for V4.
  - More gas (V3, V5) strengthens the anti-rival result but also pushes the flat law negative.
- **The mock (G5).**
  - **M1, flat truth:** a differential mis-scaling of only **+0.074 dex** between z 0.6 and 2.5 reproduces the observed δ_flat slope of −0.029.
  - **M2, rival truth:** a mis-scaling of **+0.259 dex** reproduces BOTH observed slopes (χ² = 0.02). Within the frozen plausible range (≤ 0.2 dex), the best χ² is 3.14. So M2 does not produce the pattern at a plausible mis-scaling, by the frozen line.
- **The data-side equivalent (post hoc):** baryon masses at z ≈ 2.5 that are 0.25 dex lower than at z ≈ 0.6 (relative to the analysis) would make the rival's slope exactly 0. The flat slope would then be +0.070, against the rival-true expectation of +0.073. The flat law's slope is zero at only −0.073 dex.

## What this means

- **RC100's δ(z) is a measurement of the differential baryon-mass calibration between z ≈ 0.6 and 2.5.** The rival is disfavoured at about 5σ on the adopted Tacconi+18 gas scaling, whose gas mass grows by about 0.21 dex over this range.
- **Two readings give the rival back.**
  - The gas fraction does not grow with z (V1).
  - The gas conversion is much lower than assumed (V4, α_CO 0.8). Observed gas fractions do grow with z, so V1 is a stress test, not a plausible reading. V4's low conversion is a ULIRG-like value and is also disfavoured for main-sequence discs.
- **Even without a mass systematic, the flat law is not clean.** Under moderate pressure (G3) or more gas (V3, V5), the data prefer a declining a₀ or heavier baryons.
- **Net:** CFG216's "W-flat" is robust to the pressure term and to g_bar, but not to the gas-mass route. It should be quoted as "flat-like under the adopted gas scaling; reversed by a differential gas systematic of about 0.15 to 0.25 dex". It should not be quoted as a 5σ result for the flat law.

## Fixes and disclosure

- The first run crashed at α = 0: for 2 galaxies V_c′² ≤ 0, i.e. the fit's pressure term exceeds V_c². They are now excluded from that variant and counted.
  - No output was written by the crashed run.
  - Its printed numbers up to the crash (baseline, G1, G2, G3 at α = 3.36 and 1.68) equal the final run's.
- **The frozen text's D3 needed an erratum** ("mixed" was unreachable). It was resolved before the run in addendum 1.
- The post hoc block (A, B) and the note under the decision rows were written after the frozen numbers were seen.
- The assumptions A1 (the prior centre is SED + Tacconi+18 molecular gas, with no HI) and A2 (V_c includes the Burkert term) are unverified for RC100.

## Chart (added 2026-09-29; drawn from the lane's own data and functions, no new statistic)

- `cfg217_calibration_sensitivity.png`, from `cfg217_plot.py`: the slopes of δ_flat and δ_rival on z for RC100, as functions of the change applied to the analysis baryon mass at z ≈ 2.5 relative to z ≈ 0.6.
  - The flat law's slope is zero at −0.075 dex, where the rival's slope (−0.065) equals the flat-true expectation (−0.060).
  - The rival's slope is zero at −0.25 dex, where the flat slope (+0.070) equals the rival-true expectation (+0.073).
  - The two hypotheses' calibrations are therefore about 0.18 dex apart. A 3σ separation needs the differential baryon-mass calibration known to about ±0.06 dex, on top of the statistical band (about ±0.04 in slope, i.e. ±0.06 dex).
- Bands are 95%, from 500 galaxy resamples per point. The variants' ticks use the median baryon-mass factors of the post hoc block.

## Input correction (appended 2026-09-29; the text above is unchanged)

- The RC100 CSV was corrected against the paper's Table 3 (data chat, 03922e8c7; details in `../CFG216_rc100_within_sample/INPUT_CORRECTION_2026-09-29.md`). `RC100_INPUT=corrected python3 cfg217_attack.py` writes `cfg217_attack_corrected*` and `cfg217_calibration_sensitivity_corrected.png`.
- **The headline is unchanged: the literal D3 is still ATTACK-BROKEN, the same power artefact.** The C-recon is still rejected (0.229 → 0.223 dex against 0.15), so G1 still runs on the RC41 overlap only (now 41 galaxies, was 38), where even the baseline fails.
- **What moves:**
  - **G2 flips from "no" to "yes" by the frozen line:** Spearman ρ(δ_flat, Δ_prior) goes from +0.28 (p = 0.093) to **+0.33 (p = 0.036)**. The z-slope of δ_flat after removing that dependence stays near zero: +0.014 [−0.027, +0.069].
  - **The mock:** the best χ² within the plausible 0.2 dex is 3.02 (was 3.14), still above the frozen 2. M2's best differential is +0.259 dex in both.
  - **The pressure variants, G7 and the data-side calibration** (rival slope exactly 0 at −0.250 dex, flat slope exactly 0 at −0.076 dex) move by 0.003 dex or less.
  - **Post hoc V2:** the rival's deficit reaches 3.1σ (was 2.99σ), so V2 flips from NO to YES, borderline either way. V1 and V4 still reverse the result.
- **Reading.** The gas-route limit stands. The prior-driven flag now also fires on the RC41 overlap, so RC100's δ partly reflects how far each fitted M_bar sits above its prior centre.

## Correction: V1's differential and the 3.6σ (appended 2026-09-29, after a referee question relayed by the orchestrator; the text above is unchanged except for the pointer under the title)

- **The label was on two baselines.** V1's "1.20 / 0.85" is the ratio of the median baryon-mass factors of the two z halves (median z 0.99 and 2.19, a baseline of about 1.2 in z): **−0.148 dex**, or −0.183 dex between the z < 1 and z > 2 medians. The chart's axis is the change between z = 0.6 and z = 2.5 of a tilt that is log-linear in log10 (1 + z) (baseline 1.9 in z; log10 (3.5/1.6) = 0.340). Regressing each variant's per-galaxy factor on that axis (`cfg217_label_check.py`, all 100 galaxies, reconstructed M★) gives the endpoint-equivalent positions:

| variant | half-median differential (what the README quoted) | endpoint-equivalent tilt (the chart's axis) | flat slope [sd] | flat tension \|slope\|/sd |
|---|---|---|---|---|
| V1 gas fraction fixed with z | −0.148 | **−0.251** | +0.066 [0.019] | 3.5 |
| V2 0.5 μ | −0.064 | −0.103 | +0.012 [0.019] | 0.6 |
| V3 2 μ | +0.069 | +0.111 | −0.082 [0.019] | 4.3 |
| V4 0.18 μ (α_CO 0.8) | −0.129 | **−0.211** | +0.054 [0.022] | 2.5 |
| V5 1.49 μ | +0.040 | +0.064 | −0.061 [0.019] | 3.3 |

  - The ratio is 1.6 to 1.7 for every variant, as expected from the two baselines (0.340 / 0.205 = 1.66 in log10 (1 + z)). The corrected-input copy gives the same picture (`cfg217_label_check_corrected.out`): V1 −0.248 (half-median −0.147), V4 −0.193, V2 −0.095, V3 +0.104, V5 +0.060; V1's flat tension 3.3σ.
  - **So the README's "about 0.15 to 0.25 dex" put V1's half-median figure at the low end and the data-side −0.25 (endpoint) at the high end.** On one axis, V1 is at −0.25 and V4 at −0.21: both at or beyond the frozen "plausible" ±0.2 dex band. V2 (−0.10) is inside it and is the borderline case (rival's deficit 2.9σ here, 2.99σ in the frozen post hoc block). The "stress test, not a plausible reading" verdict on V1 stands, and V4's position is now consistent with the same verdict.
  - **The chart's ticks were wrong by the same factor** (drawn at the half-median values on the endpoint axis, so V1 sat at −0.15 where the curves give a flat slope of +0.03, not V1's actual +0.066). `cfg217_plot.py` now computes each variant's tick from the regression; V1 sits where the rival's slope crosses zero. The first-version charts are kept as `cfg217_calibration_sensitivity_firstrun.png` and `..._corrected_firstrun.png`.
- **What the 3.6σ is.** It is `z_vs_flat_true` in `analyse()`: (the modified sample's flat slope − 0) / the standard deviation of that slope over 10,000 galaxy resamples of the SAME 100 galaxies. It is a tension against the flat expectation (slope 0), not a per-sample CI test (the CI excluding 0, [+0.027, +0.101], is the same statement). It contains only the observed sample's own scatter; it does not include mock-to-mock variation or the uncertainty of the calibration.
- **On the chart's axis, a pure tilt gives** (2,000 resamples, seed 217; original input): flat slope +0.011 / +0.030 / +0.050 / +0.070 / +0.090 / +0.110 at t = −0.10 / −0.15 / −0.20 / −0.25 / −0.30 / −0.35 dex, sd 0.019–0.020, so the flat tension is **0.6σ / 1.6σ / 2.6σ / 3.6σ / 4.6σ / 5.5σ**, reaching 2σ at −0.170, 3σ at −0.219 and 3.6σ at −0.249 dex (corrected input: 3.6σ at −0.258). The rival's slope is exactly 0 at −0.250 dex. The full table is in `cfg217_label_check.out`.
  - **This machinery therefore ties 3.6σ to about 0.25 dex, and at 0.15 dex it gives 1.6σ.** The referee's mock (0.5–1.9σ for 0.15 to 0.25 dex; 3.6σ near 0.35 dex) is about 0.1 dex to the right of this table (with the same sd, about 0.03 to 0.04 lower in slope at each tilt). The label does not explain that. Two candidates the referee's code can test directly: (a) the zero-tilt row (here flat slope −0.029 [0.0185], rival −0.092 [0.019]); (b) whether the mock's sd is the observed-sample bootstrap sd used here or a mock-to-mock sd with extra noise.
- **PHIBSS, from the referee's numbers (not recomputed here).** A baryon tilt of −0.19 ± 0.14 dex sits 0.8σ of its own error from the flat law's zero-slope tilt (−0.076) and 0.4σ from the rival's (−0.250), so it cannot separate them; this is the calibration limit the chart shows. The referee's tilt has to be put on this axis (the change between z = 0.6 and z = 2.5, log-linear in log10 (1 + z), of the analysis baryon mass, not of the gas alone) before the comparison is exact.
- **Disclosure.** `cfg217_label_check.py` and the corrected chart were written after the frozen numbers were seen; they are reported only and change no frozen verdict. The frozen G5 line's "about −0.18 dex" for V1 (median factor at z > 2 over z < 1) is a third baseline (median z 0.82 and 2.22, 0.249 in log10 (1 + z) against 0.340 for the endpoints) and is also not an endpoint figure.
