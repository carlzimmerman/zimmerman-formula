# CFG150 — Referee of CFG102's headline: the gate scalar's stiffness and costs at m₂ = 10⁻¹² Pa under two boundary conditions. FROZEN CRITERIA

Written 2026-09-29, before any code or run of this lane. This is a referee lane in the CFG84–86 way: re-derive one headline of CFG102 (committed d533c0698) with my own code, from its frozen question and README only, then compare. The target numbers below were read from CFG102's README, so this is a re-derivation, not a blind prediction. A failure to reproduce is a valid outcome.

## The headline under test (read from CFG102's README)

CFG102 re-derived CFG49's dynamical gate scalar χ. It found that CFG49's numbers reproduce only when the background χ₀ is solved with free ends. With χ₀ = t at both ends the costs change, but the stiffness does not. At m₂ = 10⁻¹² Pa:
- μ_uni = 1.474 × 10²⁸ J/m under both boundary conditions. μ_uni is the smallest gradient stiffness that makes all 24 galaxy layers stable.
- Flagship potential Φ_χ(r_F): −13.67 v_f² with Dirichlet ends (D: χ₀ = t at 1 kpc and 2 × 10⁴ kpc), and −13.50 v_f² with Neumann ends (N: χ₀′ = 0 at both, the free or natural condition).
- Sun potential Φ_χ(8 kpc): −9.29 × 10⁵ v_f² (D) and +7.647 × 10⁷ v_f² (N).
- Reported alongside but not part of the headline: the flagship force, −45.60 g_MOND (D) and −44.02 (N).

## The model (as read from CFG102's frozen file and CFG49's README)

- A static scalar χ on a spherical background. It is dimensionless, in the units of the gate variable t. Its energy is
  E[χ] = ∫ r² dr { (μ/2) χ′² + (m₂/2)(χ − t)² − B W(χ) }.
  - t is DE12's baryon-only gate variable, t = (U − 1)/(2w) + ½, with w = 0.25 and t_U = 1/(2w) = 2.
  - W is DE12's smooth step: 0 for χ ≤ 0 and 1 for χ ≥ 1. B = a₀² q(y)/(8πG) is DE12's coupling.
- The background χ₀ solves −μ∇²χ₀ + m₂(χ₀ − t) − B W′(χ₀) = 0 on DE12's radial domain, 1 ≤ r ≤ 2 × 10⁴ kpc, with D or N ends.
- Stability uses the second variation: the energy change to second order in a small perturbation. Negative means unstable.
  - The gas's perturbation of the gate variable, ε, adds (a/2)ε² + (m₂/2)(δχ − ε)², with a = c_s²/(ρ_b h²), h = t_U 4πG ν(y)/(H² x_c,eff) and c_s = 117 km/s (10⁶ K).
  - Minimising over ε at each point is exact, because a > 0 and m₂ > 0. It leaves
    E₂[δχ] = ½ ∫ r² { μ δχ′² + [g_eff − B W″(χ₀)] δχ² } dr, with g_eff = a m₂/(a + m₂).
- A layer is UNSTABLE if E₂ can be negative on any of five windows in the baryons' t, with δχ = 0 at each window's ends: (0, ½), (⅛, ⅝), (¼, ¾), (⅜, ⅞) and (½, 1). Each window is clipped to DE13's layer range, t in [0.004, 0.996].
- The 24 layers are z ∈ {0.25, 1, 2.5, 4} × M_b ∈ {10¹⁰, 10¹¹, 10¹²} M☉ × footing ∈ {canonical, alt}. Only w = 0.25 is used, with the phantom's amplification on (amp = True).
- μ_min(layer) is the smallest μ above which the layer stays stable, with χ₀ re-solved at every trial μ. μ_uni is the largest μ_min over the 24 layers.
- The cost uses DE13's A = 1 convention: Φ_χ = −4πG t_U m₂ (χ₀ − t)/(H² x_c,eff).
  - Flagship: z = 2.5, M_b = 10¹¹ M☉, canonical footing, at r_F = √(GM_b/(0.1 a₀)). The units are v_f² = √(GM_b a₀) and g_MOND = ν(0.1) · 0.1 a₀.
  - Sun: z = 0, M_b = 6 × 10¹⁰ M☉, canonical footing, at r = 8 kpc.

## My method (chosen to differ from CFG102's at each step)

- **Coordinate and fields.** I use s = ln r. Fields are piecewise linear in s between grid nodes (P1 finite elements).
- **Discrete energy.**
  - The gradient term is integrated exactly on each element.
  - The (χ − t)² and W(χ) terms use 3-point Gauss–Legendre quadrature (a standard integration rule), with t, B and a evaluated exactly at the quadrature radii. The scheme is consistent, not lumped.
- **Background grid.** Uniform in s over [1, 2 × 10⁴] kpc: 2¹⁶ elements for the stiffness search and 2¹⁷ for the costs.
- **Background solver.** The unknown is χ itself, not χ − t.
  - Newton's method on the exact gradient and tridiagonal Hessian of my discrete energy, started from the B = 0 (linear) solution at the same μ.
  - A backtracking line search on the energy is a safeguard. If the Hessian is not positive definite, I add a declared diagonal shift, τ m₂ times the lumped mass, with τ = 10⁻³, 10⁻², … until it is.
  - Converged when every nodal residual is ≤ 10⁻¹³ of the summed absolute sizes of its terms (round-off sits near 10⁻¹⁵). A solve that misses this is flagged.
  - D fixes the end nodes at t(1 kpc) and t(2 × 10⁴ kpc). N leaves them free, which imposes χ′ = 0 naturally.
- **Stability test, per window.**
  - Each window gets its own grid: 4000 elements, uniform in s, between the exact radii where t crosses the window's limits (found by root-finding on t(r)). δχ = 0 at both ends. χ₀ at the quadrature points is the background's piecewise-linear value.
  - The test quantity is λ_min, the smallest eigenvalue of the window operator scaled by its lumped r² mass (the diagonal of the r²-weighted inner product). It is in Pa and comes from LAPACK's tridiagonal eigensolver (LAPACK is the standard linear-algebra library). Stable means λ_min > 0.
  - Λ(μ) is the smallest λ_min over the five windows.
- **μ_min.** Brent's method (a bracketing root-finder) on Λ(10ˣ) for x = log₁₀ μ in [20, 34], to a tolerance of 10⁻⁷ in x.
  - Probes then follow at x* + 0.0005, 0.005, 0.05, 0.3, 1, 2 and 4 (capped at 34). All must be stable, and x* − 0.0005 must be unstable.
  - If a probe is unstable, the root is found again above it and the largest root is kept. The non-monotone case is reported.
- **Costs.** δ = χ₀ − t is formed at the grid nodes and interpolated linearly in s to r_F or 8 kpc. Then Φ_χ = −4πG t_U m₂ δ/(H² x_c,eff).
- **Layers.** I re-type DE12's layer formulas (host halo, phantom density, gas density, U, t, B, ν, h, a) from reading its code. The constants and interpolation tables come from L352 through DE12's own loader, executed read-only (the route DE13, CFG49 and CFG102 also use). I re-type DE12's step W and its first two derivatives.
- **Compute.** One process, with BLAS threads set to 1. Runtimes are printed. Expected: about 20–30 minutes for the main run on this loaded machine.

## Pass lines (scored; a failure is kept)

- **P1 [headline]** μ_uni(D) and μ_uni(N) are each within 1% of 1.474 × 10²⁸ J/m.
- **P2 [headline]** |μ_uni(D)/μ_uni(N) − 1| ≤ 10⁻³.
- **How the costs are scored.** P3–P5 are scored at μ_ref = 1.474 × 10²⁸ J/m, CFG102's printed value. That way P1 and P3–P5 test separate things.
  - The band for each potential is 2% of CFG102's value, widened by |dΦ/d ln μ| × 3.4 × 10⁻⁴.
  - The widening is the effect of CFG102's four-digit rounding: its unrounded μ_uni can lie anywhere in [1.4735, 1.4745) × 10²⁸.
  - My code computes dΦ/d ln μ by a ±0.1% finite difference and prints it. A rough estimate made while writing this file puts it near −7 × 10⁷ v_f² for the Sun under D, so the rounding alone moves that number by about ±2.5%.
- **P3D** Flagship, D: negative and within the band of −13.67 v_f².
- **P3N** Flagship, N: negative and within the band of −13.50 v_f².
- **P4D** Sun, D: negative and within the band of −9.29 × 10⁵ v_f².
- **P4N** Sun, N: positive and within the band of +7.647 × 10⁷ v_f².
- **P5 [my addition]** Φ_F(D) − Φ_F(N) lies in [−0.19, −0.15] v_f².
  - At 2% the P3 lines cannot tell D from N, because the two differ by 1.2%. P5 can.
  - CFG102's rounded values give −0.17 ± 0.01. I add 0.01 for my own error.

## Reported rows (not scored)

- **R1.** μ_min per layer at m₂ = 10⁻¹² (D and N) and at m₂ = ∞. Also reported:
  - which layer sets μ_uni (CFG102: z = 2.5, 10¹² M☉, alt);
  - μ_uni(10⁻¹²)/μ_uni(∞) (CFG102: 0.382);
  - ℓ = √(μ_uni/m₂) (CFG49: 3.9 kpc).
- **R2.** The four potentials, their D − N difference and the flagship force at my own μ_uni (the fully independent chain), with the deviations from CFG102.
- **R3.** The flagship force at μ_ref (CFG102: −45.60 and −44.02 g_MOND); dΦ/d ln μ for each potential; t and χ₀ − t at r_F and at 8 kpc.
- **R4.** Solver statistics: Newton iterations, the largest final residual, and whether χ₀ is a local minimum of the χ-only energy.

## Controls (load-bearing: a failed control is a failure, kept)

**Analytic checks of my solver**
- **A1.** Constant coefficients on a window [r_a, r_b]. The exact lowest eigenvalue of −μ r⁻²(r² v′)′ + g v, with v = 0 at both ends, is μ(π/L)² + g, where L = r_b − r_a. Mine must match within 10⁻⁴ (relative) on [100, 150] and [50, 300] kpc.
- **A2.** The same windows with g < 0, run through the whole μ_min chain (eigenvalue, root-finder, probes). The root must be μ* = −g L²/π² within 10⁻⁴.
- **A3.** A harmonic profile, t = 10⁵ × (1 kpc/r), with B = 0, m₂ = 10⁻¹² Pa and μ = 1.474 × 10²⁸ J/m.
  - D: the exact solution is χ = t. |χ − t| must be ≤ 10⁻⁶ t at 8 kpc and at 38.6 kpc (the flagship radius).
  - N: the exact solution is χ = t + [A e^((r−r₁)/ℓ) + C e^(−(r−r₀)/ℓ)]/r, with A and C fixed by χ′ = 0 at both ends. My χ − t must match it within 10⁻⁴ at 8 kpc and at 38.6 kpc.
- **A4.** A manufactured nonlinear solution. Take χ_m = 0.5 − 0.8 ln(r/200 kpc), which crosses the gate between 107 and 374 kpc.
  - Choose t so that χ_m solves the equation exactly: t = χ_m + (0.8 μ/r² − B_c W′(χ_m))/m₂.
  - B_c is a constant set so that max B_c|W″| = 0.5 m₂.
  - With D ends, my solution must match χ_m within 10⁻⁶ at every node.
- **A5.** Code checks.
  - My gradient and Hessian equal central finite differences of my own discrete energy within 10⁻⁶ (relative), and the Hessian is symmetric.
  - My W, W′ and W″ equal DE12's within 10⁻¹², and W′ and W″ match finite differences of my W within 10⁻⁵.

**Checks that my layers are DE12's**
- **L1.** My re-typed layer quantities (t, B, ρ_b, y, ν, a) equal DE12's transition() on DE12's own grid within 10⁻¹² (relative). This holds for all 24 layers, the flagship case and the Sun case.
- **L2.** My t = ½ radius matches DE12's committed r_edge_kpc within 10⁻⁵ (relative) on all 24 layers. t falls strictly with r across every layer.
- **L3 (the m₂ = ∞ limit: χ₀ = t and g_eff = a).** My per-layer μ_min equals DE13's committed form-(i) value μ_U/t_U² within 0.5% on all 24 layers. Their maximum (CFG102: 3.860 × 10²⁸ J/m) agrees within 0.5%.
- **L4.** DE13's N1 costs at m₂ = ∞, with μ = my μ_uni(∞): 31.8 v_f² at r_F and 2.13 × 10⁸ v_f² at the Sun. These are DE13's committed values; mine must match within 1%.
  - I compute them two ways. The direct form is −4πG t_U [B W′(t) + μ∇²t]/(H² x_c,eff), with ∇²t from my own 5-point stencil in s at step 0.01. The second way is my solver at m₂ = 10⁻⁸ Pa (the large-m₂ limit, ℓ ≈ 60 pc), with D ends.
  - The two ways must agree within 2 × 10⁻³.

**Numerical checks**
- **S1.** μ_min of the layer that sets μ_uni (D) is recomputed with (2¹⁵ background, 2000 window) and (2¹⁷, 8000) elements. Both must lie within 10⁻³ of the primary value.
- **S2.** The four potentials at μ_ref are recomputed on 2¹⁵, 2¹⁶ and 2¹⁸ elements. The 2¹⁸ values must lie within 0.2% of the primary (2¹⁷).
- **S3 (branch).** For the flagship, the Sun and the layer that sets μ_uni, at μ_ref with D and with N:
  - continuation in B (B → βB for β = ⅛, ¼, …, 1, each solve starting from the last) gives the same χ₀ as the direct solve, within 10⁻⁹ relative;
  - the χ-only Hessian there is positive definite, so χ₀ is a local minimum.
- **S4.** The probes above every root are stable (monotone above the root). A violation is reported, and the largest root is kept.

## MUTATE (each run must exit 1)

- **MUTATE=bc** swaps the boundary conditions: the run labelled D uses free ends, and the run labelled N uses χ₀ = t ends.
  - Expected: P1 and P2 still pass, because μ_uni does not see the ends. P3D and P3N still pass (1.2% < 2%). P4D, P4N and P5 fail.
  - This checks that the evaluator can tell D from N.
- **MUTATE=slaved** replaces χ₀ by t in the stability test (the slaved background, CFG102's attack A2). Nothing else changes.
  - Expected: μ_uni rises to about 3.86 × 10²⁸ J/m (CFG102 reports a ratio of 2.62; read, not blind), so P1 fails.
  - The cost lines are scored at μ_ref, so they should still pass.
- The MUTATE runs compute only the P-lines and the R-rows, with no controls. Each writes its own outputs.

## Files (stage 2)

- Code: campaign_fresh_gravity/CFG150_gate_scalar_referee/cfg150_referee.py.
- Outputs: cfg150_main.out and cfg150_main_results.json; cfg150_MUTATE_bc.out and cfg150_MUTATE_bc_results.json; cfg150_MUTATE_slaved.out and cfg150_MUTATE_slaved_results.json.
- The repository root comes from ZF_REPO or from a search up from the script's own path. No file contains an absolute path.
- The script prints the sha256 of this file and stops if it has changed. The main run exits 0 only if every P-line and every control passes.
- The DE12 and DE13 reference values are read from their committed results files at run time. The only uncommitted change in DE12's results file is its elapsed_s field.

## What I read, and what I did not

Read before writing this file:
- CFG102: README.md, cfg102_frozen.py and FROZEN_HASH.txt.
- CFG49: README.md, and campaign_fresh_gravity/CFG49_REFEREE.md.
- DE12_mond_sector_gate_stiffness.py in full. It is the layer definition.
- DE13_gate_gradient_repair.py, in part:
  - its docstring, the set-up that loads DE12, layer_fine, quad (the second-variation coefficients), and the F1/N1 section;
  - a grep that showed the names and signatures of its tri, neg_count and wcount routines, but not their bodies.
- The DE12 and DE13 rows of real_research/dark_energy_2026/README.md.
- A grep of L352 for its constants and table grid. LYG runs from −14 to 14 in 280,001 steps (10⁻⁴ dex).
- For house style: CFG118_FROZEN_CRITERIA.md and CFG84's frozen spec.
- git: the diff of DE12's results file, and the log lines of DE12 and DE13.

Not read before my frozen runs:
- any CFG102 script (cfg102_common.py, the a, b and c scripts, post1–3, runN.sh) or any CFG102 .out or .json;
- any CFG49 script or output (CV6_*.py, cv6_common.py, .out, .json), or CFG49_referee_mu.py and its .out;
- the bodies of DE13's discretisation and inertia routines, and the rest of DE13.
- After both frozen runs I will open CFG102's scripts and outputs to compare, and say so in the README.

## Where independence stops

- **The model is shared.** The question and the model are CFG102's (its frozen file) and CFG49's. A mistake in the model itself would not be caught: the energy, the reduced second variation, the windows, the A = 1 cost formula, or the flagship and Sun definitions.
- **The layers are DE12's.** I re-typed DE12's formulas from reading its code and took L352's constants and tables through DE12's own loader, so an error in DE12 or L352 would be shared. DE13's layer range and window list are adopted, not re-derived.
- **The control references are shared.** The reference values for L2–L4 are DE12's and DE13's committed outputs.
- **Not blind.** The target numbers were read. I also know CFG102's method in outline from its frozen file and README. I chose each step differently: the grid and discretisation, the unknown, the solver, the window grids, the eigenvalue test and the root-finder.
- **My own.** Every line of the solver, the discretisation, the stability test, the root-finder, the cost evaluation and the controls.

## Untested (declared)

- CFG102's 115-point extended plane and its 976-point fine scan.
- Its attacks A1–A6, the H3 bars (T, F and S at every m₂), and H1a, H1b and H2.
- Every m₂ other than 10⁻¹². The m₂ = ∞ limit appears only as a control.
- The edge-tracking counts, the baryon UV speed, the m₂ = 10⁻¹⁶ row, and non-monotone stability at small m₂.
- CV6_C (the switched stiffness) and CV6_D (the T3 cross term).
- The physics scope is inherited: a frozen spherical background, an isothermal fluid gas, no gas self-gravity, and linear stability only.
- Whether the Sun number means anything physically. CFG102 calls it a truncation artefact of the 1 kpc inner edge. This lane tests only that it reproduces.

## Readings (declared)

- **All P-lines pass.** CFG102's headline reproduces from independent code: μ_uni does not see the boundary condition, and the costs do. This changes no verdict. Every cost bar still fails in CFG102, and that is not re-tested here.
- **P1 and P2 pass but a cost line fails.** I say which line, and whether the dΦ/d ln μ band, the grid check S2 or the branch check S3 explains it.
- **P1 fails.** If L3 passes, the difference lies in the finite-m₂ background. If L3 fails, it lies in the layer or window set-up.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
