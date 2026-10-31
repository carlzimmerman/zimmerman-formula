# AS1_outer_slope: FROZEN CRITERIA (committed alone, before any script or slope number)

**Question.** Argon's reply to ARGON_BRIEF_2026-10-30 ranks one test first: fit ΔΣ = A (R/300 kpc)^(−γ) over 150–800 kpc on Brouwer+21's isolated KiDS-1000 stack, in four stellar-mass bins. Its claim is that the law gives γ = 1.00 and any finite route E halo gives γ = 1.675, independent of k, Υ and footing. Run it as stated, then run the same statistic on the spectroscopically isolated lenses and on the models themselves. Argon's derivation of 1.675 uses a bare halo with no baryons, no neighbours, no hole term and no r_ta cut.

**Already known to me (not blind).** BL1's post-hoc note that route E's ΔΣ falls about as R⁻² past R200 while B21's RAR data fall about as R⁻¹. SI1's and SI2's printed data and model vectors. I have not fitted a slope to any of them.

## Data
- **D1, Argon's named data:** B21 `Fig-3_Lensing-rotation-curves_Massbin-{1,2,3,4}.txt` (isolated KiDS-bright) with `Fig-3_Lensing-rotation-curves_Massbins_covmatrix.txt`, each bin's own block. ESD_t/bias as the release's README states; covariance is the release's value divided by its bias product.
- **D2, spectroscopic:** SI1's rebuilt stack (commit ed3c0f8bb1), S3 and S1, all lenses, Δ = L − I, 36-patch jackknife.
- **D3, like for like with D1:** the same S3 and S1 stacks as raw L − R, with no iso-random hole subtraction, which is closer to what D1's stack does.

The bins used are those with 0.15 < R < 0.80 Mpc: six bins on all three.

## Estimator (fixed)
GLS over the six bins, full six-bin covariance: minimise χ²(A, γ) on a γ grid −1 to 5, step 0.001, with A analytic. σ_γ is the half-width of Δχ² = 1. Hartlap factor (36 − 6 − 2)/35 on D2 and D3; none on D1, whose covariance is analytic. Report γ, σ_γ, A, χ², p with 4 degrees of freedom.

## Frozen classes (Argon's own cuts, with one power condition added here)
Each sample separately.
- **NOT POWERED:** σ_γ > 0.225. Then 1.00 and 1.675 cannot be separated at 3σ.
- **FAVOURS LAW:** γ in [0.85, 1.20], and (1.675 − γ)/σ_γ > 3.
- **FAVOURS FINITE HALO:** γ ≥ 1.45.
- **OTHER:** anything else.

## Reported, not graded
**Model slopes through the same estimator and weights, on D2 and D3:** law L(a) and route E H (SI1/SI2's models, FC1's rule, neighbours by the same model), at R0 and at S2's ladder R2, both footings. Report (γ_data − γ_model)/σ_γ for each. This is the comparison the bare 1.00 and 1.675 stand in for.

Also the ratio d/m per bin for each model, and the D1 samples' S/N in the six bins.

## Checks (any failure makes the verdict NOT DECIDED)
- **K1:** a noise-free power law with γ = 1.3 through the estimator, with each sample's covariance, returns 1.3 within 0.002.
- **K2:** D1's reader: √diag(C) equals the release's error/bias within 2 % in each bin of each mass bin.
- **K3:** D2's data vector equals SI1's committed `d` (S3, S1), |d| ≤ 1e-9.
- **MUTATE:** data × (R/0.3)^(−0.5) raises γ by 0.5 within 0.002 for every sample.

## What this cannot show
- A power law is not a model. Over 150–800 kpc route E's profile bends at R200, and the fit ignores that.
- It ignores amplitude. A matching slope at the wrong amplitude is not a fit; SI1 and SI2's χ² stand for that.
- D1's class does not separate a real tail from leakage in photometric isolation. D1 versus D2/D3 compares different lens samples at very different N, so a difference between them suggests leakage or selection and does not establish either.
- No class here says the data favour the framework. It compares two members of this record.

κ = ½ FITTED. Footings never pooled. Cold dark energy is a gravitating field component, never a particle. Not theory closed.
