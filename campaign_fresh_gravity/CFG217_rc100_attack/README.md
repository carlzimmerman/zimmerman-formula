# CFG217 — the attack on CFG216: gas prior, pressure, prior-driven f_DM and a mis-scaling mock

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
