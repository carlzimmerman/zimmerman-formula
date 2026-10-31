# BA1_joint_shear_statistic: FROZEN CRITERIA (committed alone, before any script or joint number)

**Question.** Is "all 15 keys under |Z| = 2" a fit? The keys share clusters and are correlated, and most sit on one side. Both Argon (its Lane 3) and I (wound 5) flagged this. Grade every rule on a joint χ².

**Standing.** κ = ½ FITTED. Footings never pooled. Not "theory closed". Nothing here says the data favour the framework. The per-key |Z| ≤ 2 gate stays as frozen everywhere; this is reported beside it.

## The statistic
- **Correlation R** among the 15 measured keys, from one common set of 2,000 bootstrap draws of the 326 clusters, with the same draws entering every key (X21's machinery, `counts`, `wls`). Computed at f★ 0.034, canonical, per h cell, for each gas scale.
- **Covariance** C_ij = R_ij s_i s_j, with s_i each key's grader error, on one template (N5 of the 10-31 report).
- **d = measured − predicted,** on one template.
- **χ² = dᵀ C⁺ d** in the eigenbasis of R, keeping modes with eigenvalue ≥ 1e-3 of the largest, since G-OUT-Mall is nearly a sum of its terciles. dof = modes kept. p from χ²(dof).
- Headline is the worse h cell.

## Verdict (Argon's lines)
- **JOINT PASS:** p ≥ 0.05.
- **JOINT FAIL:** p < 0.01.
- **JOINT MARGINAL:** otherwise.

## Graded rules, each at both f★ where it exists
FC1, MA1, MA1 at z_obs, NZ1, NZ1 at z_obs, on eRASS1's gas. MA1, NZ1, and each at z_obs, on X-COP's gas scale. ZN1's rule when it lands.

## Reported, not graded
- χ² without the two INNER keys, since their error is dominated by a failing cross-shear null.
- The largest three eigenmodes' contributions, in key terms.
- R from the 30-patch jackknife instead of the bootstrap.

## Checks
- **K1:** R = identity reproduces Σ Z² exactly.
- **K2:** the common bootstrap's standard deviation of each key against its own `s` (statistical part): median ratio within 0.8–1.25.
- **K3:** 10,000 draws from C with d = 0 give mean χ² = dof within 1 %, and p uniform at 0.05 within 1 percentage point.
- **MUTATE:** d × 2 must raise χ² × 4 exactly.
