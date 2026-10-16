# CFG820 FROZEN CRITERIA: a lower bound on the stiffness length L* from the outer-halo globular clusters (committed before any script)

**Why it is new.** CFG691 bounds L* to [5.75 pc (Saturn), ≳ 1 kpc (SPARC)]. CFG332 found the four outer-halo globulars
Newtonian (Pal 3's excess is explained by binaries, CFG334), while the plain law misses them by 4–5σ. The two have never been
combined. The screening ties the boost to s = r/ℓ_γ with ℓ_γ = L*²/(2 r_M), so the globulars' Newtonian dispersions bound
L* from below.

**Prediction per cluster (no fitted parameter except L*).**
- σ²_pred = σ²_N [1 + S(s)(B_law − 1)].
- σ_N and B_law are CFG332's own functions, exec'd read-only: Wolf estimator; Υ_V = 1.6 (SPS, CFG332 route 1); the law
  with the host's algebraic EFE (h93, `pred_efe_alg`), B_law = (σ_law/σ_N)².
- S(s) is CFG691's universal screening profile, interpolated in ln s from its table, with asymptotes s/2 (small s) and
  1 − 1/s (large s).
- s = r_{1/2}/ℓ_γ, with r_{1/2} = (4/3) r_h, r_M = √(G M/a₀) and M = Υ_V L_V.

**Likelihood.** χ²(L*) = Σ [ln σ_obs − ln σ_pred]² / [(e_σ/σ_obs)² + (ln 10 × 0.15/2)²]. The Υ width is 0.15 dex (CFG332's
WID), carried as a σ² uncertainty. L* is scanned on a log grid from 5.75 pc to 3000 pc.
- **Primary:** NGC 2419, Pal 4 and Pal 14. Pal 3 is excluded because its excess is explained by binaries (CFG334).
- **Bracket:** all four.

**Outputs and classes.**
- The 95% lower bound L*_95 is the smallest L* with χ²(L*) − χ²_min ≤ 3.84.
- **BOUND TIGHTENED** if L*_95 > 5.75 pc; report the value.
- Consequence (reported, not a verdict): S for the ultra-faint dwarfs at L*_95 (CFG691 ladder, M_b = 10³–10⁴ M☉,
  r_h 20–40 pc), i.e. whether they are forced to be screened.

**Controls.**
- K1: at L* → ∞ (S → 0), the predictions equal CFG332 route 1(a) Newtonian; T reproduces 0.27 without Pal 3.
- K2: at L* = 0 (S = 1), they equal route 1(b-EFE).
- MUTATE (separate output): with S := 1 everywhere, the scan gives no bound.

Both footings, never pooled. κ = ½ fitted; not theory closed.
