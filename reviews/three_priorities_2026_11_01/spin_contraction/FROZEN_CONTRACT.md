# TP01-SC finite experiment, frozen before extraction

Base checkpoint: `0fe706856e8a897a9ab350be4931dbf36416ada4`; shared inputs may be dirty. Actual file hashes in the v2 manifests identify evidence. Only this directory is writable by this route. No production simulation, download, source modification, staging or commit.

## Primary finite assertion

For seeds 1–9 of LC1's `M1e12_s{seed}_ng64`, reconstruct the z=0 paired contraction from actual LC1 and ZN1 particle snapshots, and the pre-disc state from the X48 z_f snapshot used to initialize both branches. Verify N, mass, seed, grid, softening and disc-axis alignment. Measure Bullock spin within the pre-disc virial radius, NFW cumulative-profile concentration, and X77's smooth-core strength S. Use the same shrinking-sphere centre, virial convention 18 pi^2 rho_m, convergence cut max(3 eps, radius of particle 200), and finite concentration/core grids as the existing analyses. Reconstruct f_Q from the median of (Q_live-1)/(Q_Blumenthal-1) at 2,3,4 disc scale lengths, with LC1's spherical disc load and mass-removal convention. Reproduce each stored LC1 f_Q and R_live to relative tolerance 1e-6; numerical failure prevents scientific grading.

The joint statistic is the actual same-epoch pair (S_no_disc(z=0), f_Q), and independently S_disc(z=0)=R_live*S_no_disc(z=0). Do not multiply a z_f core strength by a z=0 response ratio. Keep the empirical pairs intact in conditional propagation. Nine seed identities are the complete finite population tested, not independent cosmological halos sampled from the real universe.

## Predeclared diagnostics and controls

Report Spearman associations with exact two-sided permutation p-values over all 9! permutations: f_Q versus pre-disc spin and concentration; pre-disc S versus spin; S_no_disc(z=0) versus spin; S_disc(z=0) versus spin; and f_Q versus S_no_disc(z=0). Holm-adjust those six p-values. Report leave-one-seed-out correlation ranges.

Predict log S_disc from pre-disc log S, log spin, log concentration, and the two nested pairs (log S, log spin) and (log S, log concentration), using ordinary least squares with an intercept, leaving each seed out. Compare held-out squared prediction errors to leave-one-out intercept-only prediction. Separately predict f_Q from log spin, log concentration, and their pair. These are prognostic finite-sample diagnostics, not calibrated response laws. Positive held-out skill (1-SSE/SSE_intercept >0) and a stable correlation sign are necessary evidence to pursue an association, not a discovery threshold.

Controls: independent cumulative count and spherical-contraction reconstruction versus LC1's stored results; rotation/translation/velocity-boost invariance of spin; zero internal velocities give zero spin; identity contraction at zero baryons; and an intentionally permuted response vector must alter a nonconstant joint pair statistic. Preserve failed controls and repair implementation only in a new recorded run.

## Conditional continuation, only after the primary diagnostics

Inspect the measured seed association before attempting SPARC. No measured galaxy spin or spin-retention map exists in these inputs. Thus an empirical forward model with assigned galaxy spins is unavailable. A clearly labelled capacity envelope is allowed: apply all nine measured joint (S_no_disc/median S_no_disc, f_Q) pairs to each selected galaxy, either with no brightness association (ensemble mean) or through a single perfect inverse-spin rank association with surface-brightness quantile. This is an assumed association, never measured galaxy spins. Do not fit scatter amplitude, response strength, rank correlation, or mass-dependent parameters.

Use the frozen NR1-primary cache as a reproducible conditional baseline, reproduce its median Upsilon and rms, then disclose that NR2 has superseded its low-mass medians. If a rebase to NR2 is implemented it must reproduce NR2's median Upsilon/rms before interpretation. SPARC calculations use actual observed baryonic radial loads and existing smooth-core profile plus Blumenthal response; one-mass response homology is an explicit additional assumption. Grade both rms<=0.110 and median Upsilon in [0.50,0.80], and HS1's |b|<=2 sigma at fixed Upsilon=0.50, 2 R_d, V_flat 60–120, quality<=2, inclination>=30. Joint success is capacity under those assumptions, not a physical completion. No optimisation across associations is allowed.

## Scope and resource limits

One numerical thread, no new zooms, minutes per individual command and below 1 GiB working memory where feasible. Record Python/NumPy/SciPy versions, input hashes before/after, result hashes, commands, timing, controls and exact case counts using a v2 computation manifest. Store raw per-seed/per-galaxy tables. Small n, one mass, spherical profile fits, isolated spheres lacking external tidal torques, artificial steady discs and resolution-edge inner profiles limit every inference. If the association fails, that closes this measured extrapolation, not arbitrary baryonic dynamics.
