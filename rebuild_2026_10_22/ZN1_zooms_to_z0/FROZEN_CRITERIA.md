# ZN1_zooms_to_z0: FROZEN CRITERIA (committed alone, before any new snapshot or number)

**Question.** X48's zooms stop at z_f, with M/2 collapsed. Every cluster rule so far has guessed the rest: a single r⁻³ tail to a budget (FC1, MA1), a frozen core with a solved tail (NZ1), an r⁻⁹ᐟ⁴ tail (GX1). Each passes X-COP or the shear, not both. What does the same collapse produce at z = 0, and does that one profile, with no fitted parameter, pass both? The owner approved this on 10-31 ("Yes, alongside X80").

**Disclosed.** I have seen MA1, XH1 and NZ1. My expectation, on record before any new snapshot: X-COP probably passes, and G-OUT-M3 is the key most at risk, because fair share inside R₂₀₀ gives less mass than MA1's budget. A fail is reported as found.

**Standing.** κ = ½ FITTED. Footings never pooled. Cold dark energy, never a particle. No ΛCDM input. No a₀ in the dynamics, as X48. Not "theory closed". Nothing here says the data favour the framework. No downloads.

## Runs
- Seeds 1, 2, 3 at 10¹³ and 10¹⁴, ng 64: six runs, chosen before any result, the same seeds as X80's and X48's resolution sets.
- Each continues from X48's `snap_zf.npz` to z = 0, with X48's own `accel`, step rule (η 0.2), softening (ε fixed at 0.01 r_f, physical) and background. Nothing else changes. X48's files are read only.
- Snapshots at z = 0.5, 0.25 and 0.
- Single thread, nice 15, preemptible (SIGTERM → checkpoint, exit 75, `--resume`). Six runs alongside X80, about 12 GB more.
- A mass with fewer than 2 finished seeds makes the lane UNDECIDED.

## Measurement (per snapshot)
- Centre: X81's `centre`. M(<r) in spheres. R₂₀₀ from M(<R₂₀₀) = 200 ρ_c(z) (4π/3) R₂₀₀³ on the native background.
- Shape: m(x) = M(<x R₂₀₀)/M₂₀₀, tabulated on log-spaced x. Resolved for r ≥ 3ε. Inside that, M ∝ r².
- Edge: x_edge is where M reaches 90 % of the run's total mass. Beyond it the isolated sphere is not trusted.
- Stack: median m(x) over the seeds at each mass and snapshot, tagged with the median log M₂₀₀ actually measured.

## The rule for a cluster (no fitted parameter, cluster path only)
Everything is at the cluster's own z_obs.
- **M₂₀₀:** fair share inside R₂₀₀: (1 + R_nat) M_b(<R₂₀₀) = 200 ρ_c(z_obs) (4π/3) R₂₀₀³, with M_b = the grader's own (1 + f★) × gas. R_nat as FC1.
- **Shape:** from the snapshot nearest z_obs (z_obs < 0.125: z = 0; 0.125–0.375: z = 0.25; above: z = 0.5). Interpolated in log M₂₀₀ between the two masses, clamped outside.
- **Cold mass:** M_c(r) = f_c M₂₀₀ m(r/R₂₀₀) for r ≤ x_edge R₂₀₀. The zooms evolve all of Ω_m; f_c is FC1's cold share.
- **Beyond x_edge:** ρ_c ∝ r^(−γ), continuous at the edge, with M_c(r_ta) = M_fair as in every lane since GS1. γ is solved per cluster. If M_c at the edge already exceeds M_fair, there's no tail: the cell is counted and M_c stays constant.
- S, η, r₀ and a₀ do not enter. SPARC and groups stay as FC1. This lane does not touch them.

## Grade
- **X-COP:** XH1's line, unchanged: 35 points, |mean Δ| ≤ 0.05, rms ≤ 0.10.
- **Shear:** X74's 15 cluster keys, both h, |Z| ≤ 2.
- Graded at f★ 0.034 and 0.0615.

## Verdict
- **Z0 PROFILE PASSES BOTH:** X-COP and all keys, at both f★.
- **F★-DEPENDENT:** both pass at exactly one f★.
- **X-COP ONLY** or **KEYS ONLY:** naming what fails.
- **FAILS BOTH.**
- **[NOISE-LIMITED]** appended if grading each seed's shape alone (seed 1 at both masses, then 2, then 3) gives more than one class.
- **[MASS-DEFINITION-DEPENDENT]** appended if reported line 1 changes the class.

A pass would mean one native profile fits both cluster data sets with no knob. It would not derive κ, and it would say nothing about SPARC, lensing around galaxies or the Milky Way.

## Reported, not graded
1. M₂₀₀ from MA1's budget fixed point on this profile, in place of fair share inside R₂₀₀.
2. The z = 0 shape for every cluster, in place of the nearest snapshot.
3. **Where the late mass lands:** M(<r, z = 0)/M(<r, z_f) at r/r_f = 0.1, 0.2, 0.5, 1, 1.5; and the fraction of the mass gained after z_f that ends inside r_f.
4. **Does the core freeze?** Smooth-core S and r₀ (X77's fit) and c_nfw at z_f, 0.5, 0.25, 0, against NZ1's assumption that they don't change.
5. M₂₀₀(z = 0) against nominal M. The native slope between R₂₀₀ and x_edge R₂₀₀, against 2.25 and NZ1's solved 1.87.
6. By seed: all of the above. The energy check over the continuation.

## Checks
- **K1, engine:** continuing from X48's last checkpoint of a finished run reproduces X48's own `snap_zf.npz`: max |d| ≤ 1e-12 relative, positions and velocities.
- **K2, measurement:** on a sampled exact NFW (c = 4, N as the zooms), m(x) comes back within 2 % for x ≥ 0.05, and R₂₀₀ within 1 %.
- **K3, harness:** feeding MA1's cold mass profile through this lane's cluster path reproduces MA1's predictions: |d| ≤ 1e-9.
- **K4:** every run's N is unchanged, and M(<R₂₀₀) = 200 ρ_c V to 1e-6.
- **MUTATE** (`--mutate`, separate outputs): r in the shape × 1.5. It must move X-COP's rms by more than 0.01 and G-IN-Mall by more than 0.05, else UNDECIDED.
- Any K failure: no verdict, exit 1.
