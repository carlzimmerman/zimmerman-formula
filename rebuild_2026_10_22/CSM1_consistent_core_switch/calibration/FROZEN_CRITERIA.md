# CSM1 calibration finite contract — frozen before new grades

Checkpoint: 2c6b17d683c1a69a1c95754c255de1cc6f79800a; preserve dirty work. Writes confined to this calibration directory. No PM simulation, no fitted parameter or mass reassignment.

For L in {3.75,3.9,4}, both canonical/alt footings separately: eta(M)=4/(3 B(1)) [L S9(M)/S9(1e14)]^(5/4), with the existing clamped piecewise-linear S9 interpolation in log mass. Core=max(floor,eta(M)Sigma_coll(M)); above-floor switch uses this identical function. SPARC own amplitude stays at own M200; basin switch evaluates the same actual X43 sig_core at BS1's selected basin mass with own fallback, in the selected background A/B. Groups and clusters retain their own existing mass and GS1 measured gas budget; isolated lenses retain own mass, X53's coarse collapse table, units and own sc>floor flag. Exact-EPS versus X53 table difference is diagnostic only.

Before corrected claims, reproduce old CL3 L3.75 (its rounded per-footing thresholds) SPARC, groups, clusters and lens scores, and original X53 cf4 halo lens scores. Grade baseline agreement at absolute 1e-6 for recorded grade numbers (group, clusters, SPARC); lens chi-square 1e-6. Failure stops dependent corrected runs.

Corrected grades preserve CL2/CL3 line criteria: SPARC line function in both backgrounds, group CONSISTENT, all 15 cluster keys abs Z<=2 at both h cells, lens all-radii dchi2(ENV2H-L2H)<=9 and dchi2(ENV2H-pure halo H2H)<0. Dwarfs/MW independently delegated; calibration alone cannot assert full suite passes. Actual model grades required; root movements alone establish none.

Controls: finite decision accounting, direct selected-mass/core equality, identical own amplitude, input hashes before/after, source transformations unique-count checked, all expected populations, measured peak RSS<1GB per process, source flag-inversion twin with nonzero violations and changed scores. Narrow rerun of L3.75 for repeatability; no tuning scans. Each scorer runs in a fresh one-thread subprocess/fork; no macOS RLIMIT_AS claim. CPU/wall bounds and observed RSS recorded.

Not a validation of EPS, physical basin nonlocality, native S9 transfer/convergence, background fit, cold-sector mechanism, or a covariant parent. kappa=1/2 remains fitted. Scientific failure is a valid finite result, separate from execution/benchmark failure.
