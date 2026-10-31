# GH10_smooth_gas_taper: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** GH8/GH9's template cuts Zhang's gas at a sharp 3D wall, k R_vir. An outside proposal says this inflates the expected CAP near 2' by about 3×, so A(1.8) is biased low by that factor, and that a smooth profile explains the data's 2' dip. Does a smooth taper change GH9's class, and does the template acquire that dip?

**Fixed.** GH8's lenses, CAPs, velocities, weights, R (fm, cut, ctx), covariance and shuffle and jackknife errors, through GH9's propagation code read-only. Only the gas template changes. Beam 1.6' as in GH7.

**Tapers,** applied to Zhang's β 0.43, r_c 6 kpc density, integrated to 6 k R_vir:
- **F1:** exp(−r²/2(k R_vir)²), the proposal's scale.
- **F2:** ½ erfc[ln(r/k R_vir)/(√2 × 0.3)].

**Normalisation.**
- **Primary:** total gas mass equals the sharp template's mass inside k R_vir, the proposal's "same mass".
- **Reported:** Zhang's mass inside R_vir kept fixed.

**Mass scale.** D1 (GH9's primary) graded; D = 0 reported.

**Grade.** e = larger of shuffle and jackknife σ, as GH9.
- **BELOW SURVIVES TAPER:** k 1.8, D1, primary: A + 2e < 1 at all three R, F1 and F2.
- **TAPER REMOVES BELOW:** A + 2e ≥ 1 at all three R, F1 and F2.
- **FORM-DEPENDENT:** otherwise.

**Reported with fixed tests.**
- **Bias factor:** A_taper/A_sharp at k 1.8. The proposal's claim holds only if it is ≥ 2.
- **Dip:** the stacked template has a local minimum at θ 1.5–3' and rises at least 1.5× from it by 8'.
- **Fit:** χ² at best A for sharp, F1, F2, null χ² alongside. GH8's data are consistent with zero (p 0.21), so a fit preference is not a detection.
- Also k 1 and k 3.

**Checks.**
- **K1:** sharp tables rebuilt through the same harness match GH7's at D 0.
- **K2:** GH9's D1 A(1.8) at fm reproduced to 1e-3.
- **K3:** F2 at width 0.005 matches the sharp template within 2 % of peak, k 1.8, one cell.
- **K4:** F1 and F2 total mass equals sharp to 1e-3.
- **K5:** template half width 24' vs 16' changes F1 at k 3, lowest z, by under 2 % of peak.
- **MUTATE:** doubling F1 halves A exactly; flipping velocities flips That; shuffled F1 estimator mean within 0.1 s of zero.
- NOT DECIDED if K1–K5 or MUTATE fail.

**Limits stated up front.** No two-halo term. No detection in the data, so this tests a template bias, not gas. GH8's marginal control, inherited β and K2 velocity failure remain. Not a statement that the law wins.

κ = ½ FITTED; c_f EXTERNAL. Canonical and alt are not at issue in this column; footings are not pooled. Not theory closed. Cold dark energy is a gravitating field component, never a particle.
