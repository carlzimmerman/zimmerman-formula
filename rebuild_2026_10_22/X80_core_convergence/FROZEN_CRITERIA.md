# X80_core_convergence: FROZEN CRITERIA (committed alone, before any script or number)

**Question.** X77 measured η_native directly on the X48 zoom halos. At 1e12, ng 64 it gives 20.83, just inside the SPARC
limit of 21.2, after rising 14.5 % from ng 48. X77 fits the smooth core on [r_conv, r_vir], where r_conv = max(3ε,
radius of the 200th particle) shrinks as N grows. Pure cold collapse is expected to give a cusp, not a core. If so, the
fitted r₀ is set by r_conv (the resolution), and η_native has no converged value: it keeps rising with resolution and
the knife-edge pass is an artefact. If the fitted r₀ stays put while r_conv shrinks, the core is real collapse physics.
This lane decides which from the runs already on disk plus an analytic cusp calculation. No new N-body run.

**Data.** Every finished X48 1e12 snapshot (ng 38, 48, 64). Per run: r_vir and r_conv from X48's `measure()` unchanged;
the smooth-core a = r_vir/r₀ from X77's `fit()` unchanged (imported, not copied); x_c = r_conv/r_vir; y = r₀/r_vir = 1/a.

**T1 (same seed, different resolution).** For each seed with both ng 48 and ng 64: s = Δln y / Δln x_c.
Median s over seeds (68 % bootstrap, 10 000 resamples, seed 20261030).
- s ≥ 0.5: **CORE NUMERICAL** (r₀ follows the resolution cut).
- s ≤ 0.2: **CORE CONVERGED**.
- between, or the bootstrap interval spans both thresholds: **UNDECIDED**.

**T2 (analytic cusp).** Fit the smooth core, with X77's objective and a grid, to exact M(<r) of a cuspy profile sampled on
[x_c, 1]: NFW at each run's own c_nfw_fit (X48's reported fit), and Einasto α = 0.17 with r₋₂ = r_vir/c_nfw_fit
(reported). That gives a_cusp(x_c). Per run, compare the measured a with a_cusp at the run's own x_c.
- If |a/a_cusp − 1| ≤ 0.2 in at least 2/3 of the ng 64 runs, report **"zoom cores = cusp seen through the resolution cut"**.
- Otherwise report **"zoom cores are not a cusp under the cut"**.

**Combined verdict.**
- CORE NUMERICAL plus the cusp match: **COLLAPSE BRANCH HAS NO CONVERGED η**. X77's 1e12 pass is a resolution
  artefact, and route E needs a physical core scale that is not in the collisionless zooms.
- CORE CONVERGED: **NATIVE η STANDS** at its measured value.
- Anything else: UNDECIDED, with the numbers.

**Forecast (reported only, not graded).** η_native at the ng 80 x_c (r_conv scaled by (64/80)^1 for 200 particles in a
fixed cusp at fixed ε ratio; also the exact 3ε floor) and in the limit x_c → 3ε/r_vir, from T2's NFW curve.

**Checks.**
- **K1:** the T2 machinery on an exact smooth core (a = 6) returns a = 6 within 2 % at any x_c.
- **K2:** the imported X77 `fit()` reproduces X77's committed a for M1e12_s1_ng64 exactly.
- **MUTATE:** drop every particle inside r_conv × 2 by half (shuffle-thin to a softer centre). The fitted a must fall.

κ = ½ FITTED. Not theory closed. Nothing here says the data favour the framework. Cold dark energy is a gravitating
field component, never a particle. The zooms are collisionless; the floor physics is not in them.
