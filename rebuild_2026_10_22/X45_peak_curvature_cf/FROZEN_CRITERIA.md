# X45_peak_curvature_cf — FROZEN CRITERIA (committed alone, before any script or number of this lane)

**Question.** X44 showed that scale-free self-similar infall gives c_f = 1.85, while the data need c_f ≈ 4–4.2.
Does the structure of the initial density peak supply the concentration? The peak's height ν and curvature x are the
ingredients of the Dalal et al. (2010) picture. If c_f comes out from them, X43's rule is regraded halo by halo with the
derived c_f(M) and no simulation number.

Standing rules: κ = ½ FITTED. Footings never pooled. Route E, Newtonian, cold dark energy not matter. The record's own
P(k). No ΛCDM concentration relation and no simulation calibration. Not "theory closed". Nothing here may say the data
favour the framework.

## 1. Construction (all frozen; first-principles statistics + spherical collapse)

- **P(k):** EM1's CLASS run on background A (record refit), linear at z = 0, physical units. D(z) is CLASS's.
- **Peak filter:** Gaussian, with M = (2π)^{3/2} ρ̄ R_G³ (the BBKS mass convention).
- **Spectral moments:** σ_j² = ∫ k^{2j} P W_G² k² dk/2π², γ = σ₁²/(σ₀σ₂).
- **Object:** the half-mass object M/2 at the Lacey–Cole median formation z_f (as X41/X43). Its height is
  ν = δ_c / (σ₀(R_G) D(z_f)), with δ_c = 1.686.
- **Curvature:** x̄ = ⟨x | ν⟩, the exact mean over the BBKS peak-curvature distribution f(x) exp[−(x − γν)²/(2(1 − γ²))]
  (BBKS A15), by numerical integration.
- **Mean profile around the peak** (BBKS, smoothed field):
  δ(r) = (ν − γx̄)/(1 − γ²) · ξ(r)/σ₀ − (x̄ − γν)/(1 − γ²) · ∇²ξ(r)/σ₂, with ξ, ∇²ξ from P W_G².
  - Check: δ(0) = νσ₀ and −∇²δ(0) = x̄σ₂.
- **Shells:** Lagrangian radius q with enclosed linear mean δ̄(<q).
  - Turnaround at D(z_ta) = 1.062/δ̄; collapse at D(z_c) = 1.686/δ̄ (EdS spherical-collapse thresholds, disclosed).
  - Final physical radius r = ½ r_ta, with r_ta = a(z_ta) q / 5.55^{1/3}.
  - The shells collapsed by z_f form the halo. r_out is the outermost one.
  - If r(q) is not monotone, the shells are sorted (count reported).
- **Concentration:** ρ(r) from M(<r). r₋₂ is where d ln ρ / d ln r = −2, from a smoothed log-derivative.
  **c_f,pk = r_out / r₋₂.** If the slope never crosses −2, the mass is flagged and the X44 timing value 1.85 is used
  (disclosed).
- **Mass grid:** c_f,pk is evaluated at lg M = 10.0 … 15.5 (12 points) and interpolated in lg M.

## 2. Regrade

X43's committed script is executed with η → η(M) = (4/(3B(1))) c_f,pk(M)^{5/4} per system. Nothing else changes: SPARC,
X30's cluster keys, P4's 63 groups, and X43's verdict rule. The label is **PK PASSES** or **PK FAILS: <keys>**.

Reported:
- the c_f,pk(M) table, with ν, x̄ and z_f;
- c_f,pk at the group and cluster medians against the data's required 4–4.2 (X44);
- the non-monotone shell counts.

## 3. Checks (all must pass; `--mutate` must fail K1)

- **K0:** a constant c_f = 4 reproduces X43 exactly (as X44's K0).
- **K1:** the BBKS profile identities δ(0) = νσ₀ and −∇²δ(0) = x̄σ₂ hold to 1e-6 relative, at one mass.
- **K2:** the curvature mean reproduces the high-ν limit, ⟨x|ν⟩ → γν (relative difference < 0.05 at ν = 6).
- **K3:** EM1's σ₈ (own vs F3) to 1e-3.
- **MUTATE:** the sign of the curvature term in δ(r) is flipped; K1's Laplacian identity must fail.
