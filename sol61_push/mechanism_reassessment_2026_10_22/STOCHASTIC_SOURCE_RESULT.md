# A conditional quantum origin for coarse source fields

stochastic_source_run starts all coarse fields at zero and evolves the standard light-spectator stochastic inflation approximation for the existing potential. Vacuum modes crossing the horizon supply the noise. No occupied X population or initial classical source displacement is inserted. This supplies a conditional origin for field amplitudes, not yet a cold particle population.

Write Phi=H(f1+i f2)/sqrt(2), X=H(x1+i x2)/sqrt(2), z=(f1,f2,x1,x2), and v(z)=V/H^4. For constant imposed H,

    dz_a = -(1/3) partial_a v dN + (1/(2 pi)) dW_a,
    <dW_a dW_b> = delta_ab dN.

The drift is differentiated directly from the existing positive carrier potential, including masses, cubic coupling and quartic. The noise prescription is the leading stochastic light-field approximation, not a new force or an exact solution of the full quantum field theory. Its standard framework is described by [Starobinsky and Yokoyama, astro-ph/9407016](https://arxiv.org/abs/astro-ph/9407016). Here it is a declared approximation; this source's abstract authenticates the framework, not an independent verification of our four-field implementation.

Choose the exploratory high inflation scale H=1.3445e10 GeV identified by the preceding free-source abundance estimate, 60 e-folds, and the existing MeV mass/coupling benchmark. The scale is **not selected by the action or inferred from this run**. Evolve 4096 independent patches at dN=.02 and .01, with common Brownian increments and fixed PCG64 seed 20261022. No radiation-era evolution is included.

The finer run gives

    <|X|²>/H² = 1.54258 +/- 0.02399 (Monte Carlo standard error),
    <|Phi|²>/H² = 0.972195 +/- 0.012411,
    lambda <|Phi|^4>/H^4 = 0.0138886.

The X result agrees with the effectively free expectation 60/(4 pi²)=1.51982 within one standard error. The Phi variance changes by about 4.6e-5 fractionally under timestep refinement. Its infinite-duration quartic equilibrium value would be 1.17147; the finite 60-e-fold evolution has not reached that equilibrium, and no equilibrium check is claimed. The 10th, 50th and 90th percentiles of |X| are approximately 5.50e9,1.41e10,2.50e10 GeV. All sampled amplitudes exceed the empty-Phi tachyon threshold, but the same run also generates a large nonzero Phi background.

All three declared checks pass; the completed manifest validates. The full field samples are retained in results.json for reproducibility. They are **not complete post-inflation Cauchy data**: this overdamped description does not supply canonical momenta, charge fluctuations or subhorizon spectra. Assigning zero momenta by fiat would be another untested matching assumption. Ensemble symmetry supplies no preferred charge sign.

The useful implication is a correction to the next formation calculation: a quantum-seeded X reservoir and an empty daughter sector are not consistent with this tested light-field inflationary setup. The daughter background's quartic effective mass, subsequent oscillations/thermalization, and source-induced instability must be evolved together. The isolated empty-Phi Hessian is a diagnostic, not the full stability operator around the generated two-field state. Abundance, final temperature and surviving charge populations remain uncomputed after that nonlinear stage.

## Full potential-curvature check on the generated state

stochastic_hessian_run evaluates the actual four-real-field potential Hessian on all 4096 generated samples. In units of H, its blocks are

    A = (m/H)² I + sqrt(2)(g/H)[[x1,x2],[x2,-x1]]
                   + lambda (|f|² I + 2 f f^T),
    C = sqrt(2)(g/H)[[f1,f2],[-f2,f1]],
    D = (M/H)² I.

Because the Phi and X curvatures differ by many orders of magnitude, the code checks A and the Schur complement D-C^T A^-1 C separately rather than trusting poorly conditioned full-matrix eigenvalues. The minimum A eigenvalue is 5.39e-7 H² and the minimum Schur eigenvalue is 0.99973344 M². Both are positive throughout the sampled ensemble, even though the artificial empty-Phi Hessian has a negative eigenvalue in every one of these samples. The completed manifest validates.

Thus there is no instantaneous negative-curvature direction at these sampled end-of-inflation field values. This does not prove dynamical stability, rule out later tachyonic episodes, or exclude parametric resonance with a time-dependent positive curvature. It establishes that the generated daughter background must be included when deriving the onset of conversion; the empty-daughter instability alone cannot serve as the formation trigger for this ensemble.

## Existing repository route and the isocurvature gate

The repository already investigated stochastic misalignment in ../../campaign_fresh_gravity/CFG362_inflation_amount/README.md for a different one-field, ultralight equilibrium model. It explicitly found that the amount is relocated into an unspecified inflation scale, and required an extremely long inflationary equilibrium to suppress isocurvature. Our finite-duration two-field calculation does not supersede that finding or establish a new generic production mechanism. Its additional information is the generated two-field state and the failure of the empty-daughter approximation for this action and benchmark.

In particular, fitting a free source amplitude is not sufficient for cosmological viability. If the final dark-matter yield is proportional to |X|², and X is a light spectator uncorrelated with the primordial curvature perturbation, the canonical two-real-field fluctuation estimate gives

    P_S = 4(H/(2 pi))²/(x1_phys²+x2_phys²)
        approximately 2/N_pre

at a representative random-walk background built over N_pre e-folds before the scale of interest exits. Here x1_phys,x2_phys are the canonical real components, not the dimensionless samples. Even granting N_pre=60 gives P_S of order 0.03. For comparison, the standard uncorrelated, nearly scale-invariant CDM isocurvature limit beta_iso<0.038 corresponds to P_S of order 8e-11 for P_R approximately 2.1e-9 ([Planck 2018 inflation constraints](https://doi.org/10.1051/0004-6361/201833887)). This benchmark would require N_pre of order 2.5e10, or a physically demonstrated suppression of the source-to-final-yield response, under those assumptions.

The run's 60 total e-folds are not 60 prior e-folds at every CMB scale; no CMB pivot matching was performed. This estimate is therefore a diagnostic obstruction to the naive light-source/misalignment interpretation, not a computed isocurvature spectrum of the interacting model. Nonlinear conversion must propagate spatial perturbations as well as mean abundance. Internal dark-sector interactions cannot simply be assumed to erase the initial isocurvature. The higher-H source is not an established viable solution.
