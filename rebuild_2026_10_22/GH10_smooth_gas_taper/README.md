# GH10_smooth_gas_taper: does a smooth gas profile change GH9's kSZ class?

**Verdict as frozen: FORM-DEPENDENT.** Criteria d607e31b11. All checks pass. BELOW holds for F2 and goes away for F1 at the primary normalisation. Only the template changes; GH8's data still show no detection (null p 0.21).

| k 1.8, D1, R fm | A(1.8) ± s | A(1.8) + 2e | BELOW | Bias vs sharp | χ² |
|---|---|---|---|---|---|
| Sharp (GH9) | 0.237 ± 0.187 | 0.611 | yes | | 9.1 |
| F2, same total mass | 0.307 ± 0.226 | 0.760 | yes | 1.30 | 8.8 |
| F1, same total mass | 0.558 ± 0.374 | 1.306 | **no** | 2.35 | 8.3 |
| F1, Zhang's mass in R_vir (reported) | 0.304 ± 0.203 | 0.710 | yes | | 8.3 |
| F2, Zhang's mass in R_vir (reported) | 0.268 ± 0.198 | 0.663 | yes | | 8.8 |

Null χ² is 10.9/8. R cut and ctx agree. Full table in `gh10.out`.

**What it shows.**
- **The sharp cut matters somewhat.** It inflates the template near 2' (76 vs 63 F2, 39 F1), so the proposal's direction is right. The bias is 1.3–2.35 depending on form; the frozen ≥ 2 test passes for F1 only, and about 3× is not seen.
- **The escape costs gas inside R_vir.** Comparing F1's two normalisations at the same form (0.304/0.558), F1's primary template holds about 54 % of Zhang's measured gas inside R_vir, because a Gaussian of scale 1.8 R_vir spreads the same total further out. With Zhang's gas kept inside R_vir, BELOW holds for both forms. This reading is post-hoc; the frozen verdict is FORM-DEPENDENT.
- **No dip.** No template has one. Every template peaks near 2', exactly where the data are lowest. The proposal's explanation of the dip fails. GH8's dip is compatible with noise, and the north and south samples disagree at large θ.
- **No fit preference.** χ² 7.9–9.1 for all templates; none is significant against null.

**For the theory.** GH9's "below at every extent" wording is softened: BELOW depends on assuming the template's shape at fixed Zhang gas, and a low-gas-in-R_vir, extended form is not excluded by this column. That form would need its own check against Zhang's X-ray profile and GH5's tSZ. Route E's lensing gap stays unsolved.

**Limits.** No two-halo term. Two taper forms, one chosen from the proposal, one from me. GH8's marginal control, inherited β, K2 velocity failure and non-blind status remain. Not a statement that the law wins or that gas is excluded.

κ = ½ FITTED; c_f EXTERNAL. Footings are not at issue in this column and are not pooled. Not theory closed. Cold dark energy is a gravitating field component, never a particle.

Reproduce: `python3 gh10.py` (needs GH7/GH8 work files in `_external_data`).
