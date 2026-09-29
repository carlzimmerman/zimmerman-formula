# CFG150 — Referee of CFG102's headline: the gate scalar's stiffness and its costs at m₂ = 10⁻¹² Pa under two boundary conditions

- **Criteria:** frozen in `../CFG150_FROZEN_CRITERIA.md` (committed 454c3efc7, sha256 bb3aad15…), before any code of this lane.
  - The script checks that hash before it does anything else, and stops if the file has changed.
  - The target numbers were read from CFG102's README, so this is a re-derivation, not a blind prediction.
- **Script:** `cfg150_referee.py`, one file, one process (BLAS threads set to 1).
  - It imports nothing from CFG102 or CFG49.
  - It executes DE12's definitions read-only, for L352's constants and tables and for the L1 comparison.
  - Wall times on this heavily loaded machine: main 168 s, MUTATE=bc 121 s, MUTATE=slaved 23 s.
- **Runs:**
  - The main run passes 7 of 7 P-lines and 13 of 13 controls and exits 0.
  - MUTATE=bc fails P4D, P4N and P5, as frozen, and exits 1.
  - MUTATE=slaved fails P1, as frozen, and exits 1.
- **Post hoc** (written after the frozen runs and labelled so in their headers; neither changes a frozen number):
  - `post1_newton_diagnostic.py` examines the 12 background solves that missed the frozen residual line.
  - `post2_costs_at_cfg102_mu.py` evaluates my potentials at CFG102's unrounded μ_uni and looks at the one loose control residual (L4, the Sun).

## Bottom line

**Yes. CFG102's headline reproduces from independent code, far inside the frozen bands.**

- **μ_uni(10⁻¹² Pa) = 1.47387 × 10²⁸ J/m under both boundary conditions.**
  - The Dirichlet and Neumann values agree to 5 × 10⁻¹⁰. (Dirichlet, D: χ₀ = t at 1 kpc and 2 × 10⁴ kpc. Neumann, N: free ends, χ₀′ = 0.)
  - The layer that sets it is CFG102's: z = 2.5, M_b = 10¹² M☉, alt footing.
  - It is 8.5 × 10⁻⁵ below CFG102's printed 1.474 × 10²⁸, and 1.7 × 10⁻⁴ above CFG102's unrounded 1.473625 × 10²⁸.
- **The four potentials match.**
  - At μ = 1.474 × 10²⁸, the scored point, they lie 2.8–8.0 × 10⁻⁴ from CFG102's printed values.
  - At CFG102's own unrounded μ_uni (post2, post hoc) they agree to at most 8.7 × 10⁻⁶. The flagship potentials agree to 4 × 10⁻⁷, the Sun potentials to 8.7 × 10⁻⁶ (D) and 3 × 10⁻⁷ (N), and the flagship forces to 4 × 10⁻⁶.
  - Flagship: −13.675 v_f² (D) and −13.504 v_f² (N). Their difference, D − N, is −0.171 v_f²; CFG102 also has −0.171.
  - Sun: −9.297 × 10⁵ v_f² (D) and +7.649 × 10⁷ v_f² (N).
- **The boundary-condition effect is real, not an artefact of CFG102's code.**
  - At 8 kpc, where t = 78,044, χ₀ − t is +180 with χ₀ = t at the ends and −14,833 with free ends. That is the Sun's sign flip.
  - At r_F the two differ by 1.3%.
- **This changes no verdict.**
  - CFG102's cost bars, scans and attacks were not re-run.
  - Whether the Sun number means anything physically is not tested. CFG102 calls it a truncation artefact of the 1 kpc inner edge.
- **One solver miss, disclosed, harmless on diagnosis.**
  - 12 of the 1,242 background solves in the main run missed the frozen residual line (10⁻¹³) within 60 Newton iterations.
  - All 12 lie on the two z = 4, 10¹² M☉ layers, at μ = 10²⁰ J/m, the bottom of the search bracket, 7.3 decades below those layers' roots.
  - Post hoc, a patient solve converges at every one of them. It changes no stability decision, no μ_min (by at most 1.3 × 10⁻¹⁰) and not μ_uni. With patient solves, all 24 layers are stable just above μ_uni (post1).

## Comparison with CFG102 and CFG49 at m₂ = 10⁻¹² Pa

CFG102's numbers are from its committed `cfg102_b_results.json` (D) and `cfg102_b_results_BCN.json` (N), each at its own unrounded μ_uni. CFG49 printed only the free-end (N) case (`CV6_B_layers.out`). Mine are at μ = 1.474 × 10²⁸, the scored point, unless the row says otherwise.

| item | CFG49 (N) | CFG102 D | CFG102 N | CFG150 D | CFG150 N |
|---|---|---|---|---|---|
| μ_uni (J/m) | 1.474e28 | 1.473625e28 | 1.473625e28 | 1.473875e28 | 1.473875e28 |
| layer setting μ_uni | — | 2.5/1e12/alt | 2.5/1e12/alt | 2.5/1e12/alt | 2.5/1e12/alt |
| ℓ = √(μ_uni/m₂) (kpc) | 3.93 | 3.934 | 3.934 | 3.934 | 3.934 |
| μ_uni(10⁻¹²)/μ_uni(∞) | 0.3818 | 0.382 | 0.382 | 0.3818 | 0.3818 |
| per-layer μ_min(10⁻¹²)/μ_min(∞) | 0.052–1.000 | — | — | 0.0519–1.0000 | 0.0519–1.0000 |
| flagship Φ_χ(r_F) (v_f²) | −13.5 | −13.67131 | −13.50074 | −13.67519 | −13.50441 |
| flagship Φ_χ at CFG102's μ (post2) | — | −13.671306 | −13.500742 | −13.671300 | −13.500737 |
| flagship D − N (v_f²) | — | −0.17056 | | −0.17077 | |
| flagship force (g_MOND) | −44 | −45.5997 | −44.0191 | −45.6126 | −44.0302 |
| Sun Φ_χ(8 kpc) (v_f²) | +7.65e7 | −9.28778e5 | +7.647307e7 | −9.29747e5 | +7.649158e7 |
| Sun Φ_χ at CFG102's μ (post2) | — | −9.287779e5 | +7.647307e7 | −9.287859e5 | +7.647305e7 |
| flagship force at CFG102's μ (post2) | — | −45.5997 | −44.0191 | −45.5995 | −44.0189 |
| potentials at my own μ_uni (R2) | — | | | F −13.67389, S −9.29426e5 | F −13.50319, S +7.64854e7 |
| μ_uni(∞) (J/m) | 3.9e28 | 3.859883e28 | | 3.860637e28 | |

- **μ_uni.** Mine is 1.69 × 10⁻⁴ above CFG102's unrounded value.
  - Per layer at 10⁻¹², my μ_min sits a median 1.8 × 10⁻⁴ above CFG102's (largest difference 3.3 × 10⁻⁴).
  - The same small positive offset appears at m₂ = ∞ against DE13's committed values (median 2.1 × 10⁻⁴, largest 3.3 × 10⁻⁴).
  - That offset is consistent in sign and size with where the windows end. My windows end at the exact radii where t crosses the window limits; DE13's and CFG102's end at the nodes of an 8000-point layer grid, which makes the window slightly shorter. This explanation is not tested separately.
  - The two z = 4, 10¹² M☉ layers, whose μ_min is set by χ₀ lagging t, differ by only −4 × 10⁻⁵.
- **Potentials at the scored point.** They differ from CFG102's printed values by +3.8 × 10⁻⁴ (flagship D), +3.3 × 10⁻⁴ (flagship N), +8.0 × 10⁻⁴ (Sun D) and +2.8 × 10⁻⁴ (Sun N).
  - Most of that is the μ offset: dΦ/d ln μ is −15.29 and −14.46 v_f² for the flagship (D, N), and −3.78 × 10⁶ and +7.29 × 10⁷ v_f² for the Sun.
  - post2 removes it by evaluating my potentials at CFG102's own μ.

## Results in more detail

- **Per-layer μ_min** (the `.out` lists all 24 layers at m₂ = ∞ and at 10⁻¹² for D and N).
  - The D and N values are identical on every layer to at least 6 printed digits. The layers sit 25–3000 kpc out, so the background there does not see the 1 kpc and 2 × 10⁴ kpc ends at ℓ = 3.9 kpc.
  - Each of the 74 roots is clean: Λ, the smallest window eigenvalue, is negative 5 × 10⁻⁴ decades below the root and positive at every probe above it (S4).
- **The Sun's sensitivity to μ is much smaller than the frozen file guessed.**
  - The file estimated dΦ/d ln μ ≈ −7 × 10⁷ v_f² for the Sun under D. The run finds −3.78 × 10⁶, about 20 times less.
  - So CFG102's four-digit rounding of μ_uni moves P4D by only ±0.14%. The band's widening was small (1.3 × 10³ within a band of 1.99 × 10⁴ v_f²).
- **R3.**
  - At r_F, t = 28.316 and χ₀ − t = +0.6846 (D) and +0.6760 (N): χ₀ lies above t there.
  - At 8 kpc, t = 7.8044 × 10⁴ and χ₀ − t = +180.3 (D) and −14,833 (N).
- **R4: the Newton statistics of the main run.**
  - 1,242 solves; 12 unconverged (largest final residual 0.21); diagonal shifts up to τ = 10³; 115 line-search halvings.
  - Every solve used by a control converged, including the flagship and Sun cost solves and every solve at μ_ref.

## Controls (13 of 13 pass)

**Analytic checks of my solver**
- **A1:** constant coefficients on a window. The lowest eigenvalue equals μ(π/L)² + g within 6 × 10⁻⁸ ([100, 150] kpc) and 2.4 × 10⁻⁷ ([50, 300] kpc). The line was 10⁻⁴.
- **A2:** the whole μ_min chain (eigenvalue, Brent's root-finder, probes) with g < 0. The root equals −gL²/π² within 3.5 × 10⁻⁸ and 5.5 × 10⁻⁸.
- **A3:** the harmonic profile t = 10⁵ kpc/r with B = 0.
  - D gives χ = t to 4 × 10⁻¹⁰ of t.
  - N matches the closed form, t + [A e^((r−r₁)/ℓ) + C e^(−(r−r₀)/ℓ)]/r, to 4.5 × 10⁻⁹ at 8 kpc and 8.4 × 10⁻⁶ at r_F.
- **A4:** a manufactured nonlinear solution crossing the gate, with max B|W″| = 0.5 m₂. The solver recovers it to 4.7 × 10⁻¹⁴ in 4 Newton iterations.
- **A5:** code checks.
  - My W, W′ and W″ equal DE12's to 6.8 × 10⁻¹⁶, and my W′ and W″ match finite differences.
  - My gradient and Hessian equal finite differences of my discrete energy to 3.4 × 10⁻¹¹ and 3.6 × 10⁻¹¹. The finite-difference Hessian is symmetric to 1.0 × 10⁻¹¹.

**Checks that my layers are DE12's**
- **L1:** my re-typed t, B, ρ_b, y, ν and a equal DE12's `transition()` on DE12's own grid to ≤ 8.9 × 10⁻¹⁶, on all 24 layers and the Sun case.
- **L2:** my t = ½ radii match DE12's committed `r_edge_kpc` to 9.5 × 10⁻⁸. t falls strictly across all 24 layers, with a single crossing of ½ on each.
- **L3:** at m₂ = ∞, my per-layer μ_min matches DE13's committed form-(i) value μ_U/t_U² within 3.3 × 10⁻⁴ (median 2.1 × 10⁻⁴). My maximum is 3.8606 × 10²⁸ against 3.860 × 10²⁸.
- **L4:** DE13's N1 costs at m₂ = ∞ with μ = my μ_uni(∞).
  - Flagship: 31.837 v_f² by the direct formula and 31.827 by my solver at m₂ = 10⁻⁸ Pa, against DE13's 31.831 (+2.1 × 10⁻⁴ and −1.1 × 10⁻⁴).
  - Sun: 2.1315 × 10⁸ direct and 2.1304 × 10⁸ by the solver, against 2.1257 × 10⁸. That is +2.7 × 10⁻³ and +2.3 × 10⁻³: inside the 1% line, but the loosest residual of the lane.
  - The two ways agree to 3.2 × 10⁻⁴ (flagship) and 4.7 × 10⁻⁴ (Sun).
  - post2 traces the Sun's +0.27% to the Laplacian estimate (see Post hoc). About 0.02% of it is my μ_uni(∞) being 1.95 × 10⁻⁴ above DE13's.

**Numerical checks**
- **S1:** μ_min of the layer that sets μ_uni moves by −3.2 × 10⁻⁸ at (2¹⁵ background, 2000 window) elements and +8.4 × 10⁻⁹ at (2¹⁷, 8000).
- **S2:** the four potentials move by at most 1.6 × 10⁻⁷ between 2¹⁷ and 2¹⁸ elements.
- **S3:** continuation in B reproduces the direct χ₀ to ≤ 7.2 × 10⁻¹² for the flagship, the Sun and the layer that sets μ_uni, under D and N. At all six, χ₀ is a local minimum of the χ-only energy (its Hessian is positive definite).
- **S4:** all 74 roots are monotone above and unstable just below.

## MUTATE

- **MUTATE=bc** swaps the ends: the D-labelled runs use free ends and the N-labelled runs use χ₀ = t.
  - P1 and P2 still pass: μ_uni is unchanged at 1.473875 × 10²⁸. P3D and P3N still pass, since the flagship values are only 1.3% apart.
  - P4D (+7.649 × 10⁷ against −9.29 × 10⁵), P4N (−9.297 × 10⁵ against +7.647 × 10⁷) and P5 (+0.171 against [−0.19, −0.15]) fail, as frozen. Exit 1.
  - So the evaluator tells D from N, and only through the Sun and the D − N line.
- **MUTATE=slaved** replaces χ₀ by t in the stability test.
  - μ_uni rises to 3.8611 × 10²⁸ J/m, set by the z = 4, 10¹² M☉, alt layer. The ratio to the consistent value is 2.620; CFG102's attack A2 reports 2.62.
  - P1 fails; the cost lines, scored at μ_ref, pass. Exit 1.

## Post hoc (after the frozen runs; no frozen number changes)

**post1: the 12 unconverged solves** (`post1_newton_diagnostic.py`, `.out`, `_results.json`)
- **Q1:** re-running the deterministic root searches with every background solve logged reproduces the frozen run exactly: 1,100 solves, 12 unconverged, μ_uni = 1.473875 × 10²⁸ (D and N).
  - All 12 are on the z = 4, 10¹² M☉ layers (canonical and alt, D and N).
  - Each sits at x = log₁₀ μ = 20.000 (evaluated twice, because Brent re-evaluates the bracket's ends) or at 20.00007 (Brent's first step). That is 7.3 decades below those layers' roots.
  - There ℓ = 0.3 pc, so the background is nearly local. On these two layers B is 2–4 × 10⁻¹³ Pa, so B·|W″| reaches 3.9–4.1 m₂ (|W″| peaks at 9.84), and the χ-only energy is not convex there. Newton with the declared shift stalls at residuals of about 0.2.
  - These are the only such layers. On every other layer B·|W″| stays below m₂: the z = 4, 10¹¹ M☉ layers reach 0.97–0.99 m₂, and the layer that sets μ_uni reaches 0.27 m₂. These figures come from post2's direct evaluation over each layer.
- **Q2:** at each of the 12 points, a patient solve (continuation in B over 16 steps, up to 400 iterations each) converges to residuals ≤ 7 × 10⁻¹⁴.
  - Λ stays negative at every point: −1.46 to −1.52 × 10⁻¹² Pa against −2.12 to −2.19 × 10⁻¹² frozen.
  - So no stability decision depended on an unconverged background.
- **Q3:** the four affected root searches were redone with the patient solver at every trial μ.
  - The μ_min values are unchanged to at most 1.3 × 10⁻¹⁰: 2.005281 × 10²⁷ (alt) and 2.398620 × 10²⁷ (canonical), under D and N.
  - The probes stay monotone, and μ_uni stays 1.473875 × 10²⁸.
- **Q4:** at 1.0001 × μ_uni, with patient solves, all 24 layers are stable under both D and N, and every solve converged.
  - The smallest Λ is +1.05 × 10⁻¹⁷ Pa, on the layer that sets μ_uni, just above its own root. So μ_uni is the largest layer μ_min, as the headline needs.
- **Runtime:** 47 minutes, almost all of it the patient solves at μ = 10²⁰ on this loaded machine.

**post2: the potentials at CFG102's own μ, the L4 Sun residual, and where the energy is non-convex** (`post2_costs_at_cfg102_mu.py`, `.out`, `_results.json`; 2 s)
- **At CFG102's unrounded μ_uni = 1.4736252534 × 10²⁸ J/m** (read from its committed JSON), my unchanged solver gives the following (CFG102 in brackets):
  - flagship: −13.671300 (−13.671306) under D and −13.500737 (−13.500742) under N;
  - Sun: −9.287859 × 10⁵ (−9.287779 × 10⁵) under D and +7.647305 × 10⁷ (+7.647307 × 10⁷) under N;
  - flagship force: −45.5995 (−45.5997) and −44.0189 (−44.0191);
  - flagship D − N: −0.170563 (−0.170564).
  - Every quantity agrees to ≤ 8.7 × 10⁻⁶. The small differences at the scored point were almost entirely the μ offset.
- **The L4 Sun residual is the Laplacian estimate.** At DE13's own μ_U:
  - DE13's way (np.gradient twice on DE12's 20,000-point grid, then interpolation to the radius) reproduces DE13's committed N1 to 2 × 10⁻¹¹ (flagship) and 3.5 × 10⁻¹⁰ (Sun).
  - My 5-point stencil in ln r is stable to 3 × 10⁻⁵ for steps 0.003–0.03, and sits +1.1 × 10⁻⁵ (flagship) and +2.5 × 10⁻³ (Sun) from DE13's value.
  - At smaller steps it drifts (Sun +0.5% at 0.001, +2.1% at 0.0003; flagship −0.1% at 0.0003). That drift is consistent with differentiating twice a profile built from a table interpolated linearly at 10⁻⁴ dex. It is larger near y ≈ 1.4 (the Sun at 8 kpc) than at y = 0.1 (r_F). This reading is not tested further.
  - So DE13's committed Sun N1 differs by about 0.25% from the step-converged Laplacian, through how its grid samples the tabulated kernel. That is inside L4's 1% line.
  - It bears only on the m₂ = ∞ control, not on the finite-m₂ costs: there χ₀ is a screened average of t, and no second derivative of t is taken.
- **Non-convexity.** Over each layer, B times the step's largest |W″| (9.84) exceeds m₂ = 10⁻¹² only on the two z = 4, 10¹² M☉ layers (4.07 alt, 3.93 canonical). The next are the z = 4, 10¹¹ M☉ layers (0.985, 0.969), and the layer that sets μ_uni is at 0.273.

## What CFG102's and CFG49's code do (opened only after all three frozen runs)

- **CFG102** (`cfg102_common.py`, `cfg102_b_scan.py`).
  - It uses DE13's discretisation (trapezoid r² weights, off-diagonal μ r_m²/Δr) on DE12's 20,000-node geometric grid.
  - Its windows are node masks on DE13's 8,000-node layer grid. The unknown is δ = χ − t.
  - The solver is a modified Newton with a Cholesky-regularised Hessian, converged when a merit against a static scale is ≤ 10⁻⁸.
  - Stability comes from a Cholesky test on the scaled window matrix, and μ_min from a 24-step bisection that assumes stability is monotone.
  - Its N flagship and Sun solves at 10⁻¹² stopped at the 300-iteration cap with merit 1.0 × 10⁻⁹, inside its 10⁻⁸ line. My N solves of the same cases converge to 10⁻¹³ in a few iterations, and the numbers agree (post2).
- **CFG49** (`cv6_common.py`, `solve_chi`).
  - It minimises the discrete energy over every node, starting from χ = t, with no end fixed. Those are free (natural, Neumann) ends, exactly as CFG102 inferred from the numbers.
  - Its tolerance is 10⁻⁷ on a relative residual. Its printed 10⁻¹² row matches my N column in every printed digit this lane also computes: μ_uni, ℓ, the μ_uni ratio and the per-layer ratio range, the flagship potential and force, and the Sun potential. (Its UV speed is not computed here.)
- **A shared loading detail, harmless.**
  - DE13, CFG49 and CFG102 load DE12 with a blanket replace of DE12's MUTATE line. The same text also sits inside DE12's own loader for L352, where DE12 uses it to switch L352's flag off. The blanket replace rewrites that copy too, so L352's flag then reads the environment.
  - In the part of L352 that runs (before its Z1 section), the flag only labels an output dictionary and prints a line. So no number anywhere depends on it.
  - My loader replaces only DE12's own line.

## Independence

- **Read before the frozen runs:**
  - CFG102's README, frozen question and hash, and CFG49's README and referee note;
  - DE12's script in full, the layer definition;
  - DE13's docstring, its loader, `layer_fine`, `quad` and its F1/N1 section (a grep also showed the names of its discretisation routines, not their bodies);
  - a grep of L352's constants;
  - the key layout of DE12's and DE13's committed results files, to write the control code.
- **Not read before the frozen runs:** any CFG102 or CFG49 script or output.
- **Where independence stops.**
  - The model is CFG102's and CFG49's: the energy, the reduced second variation, the windows, the A = 1 cost formula, and the flagship and Sun definitions. A mistake in the model itself would be shared.
  - The layers are DE12's. I re-typed its formulas from reading them and took L352's constants and tables through DE12's own loader, so an error in DE12 or L352 would be shared. DE13's layer range and window list are adopted.
  - The control references (L2–L4) are DE12's and DE13's committed outputs.
  - The targets were read. I knew CFG102's method in outline and chose each step differently: the grid and discretisation, the unknown, the solver, the window grids and their ends, the eigenvalue test, the root-finder, and the interpolation of the costs (in ln r, where CFG102 interpolates in r).
- **My own:** every line of the solver, the discretisation, the stability test, the root-finder, the cost evaluation and the controls.

## Untested (declared)

- CFG102's 115-point extended plane and 976-point fine scan; its attacks A1–A6; the H3 bars; H1a, H1b and H2.
- Every m₂ other than 10⁻¹². The m₂ = ∞ limit is used only as a control.
- The edge-tracking counts, the baryon UV speed, the m₂ = 10⁻¹⁶ row, and non-monotone stability at small m₂.
- CV6_C (the switched stiffness) and CV6_D (the T3 cross term).
- The inherited physics scope: a frozen spherical background, an isothermal fluid gas, no gas self-gravity, and linear stability only.
- The physical meaning of the Sun number.

## Disclosed departures, development runs and choices

1. **Development runs before the frozen main** (scratch harnesses, not committed). None computed a stability result at m₂ = 10⁻¹² or any cost.
   - The first harness ran A1–A5 and timed background solves on the harmonic A3 profile.
   - The second ran L1, L2 and the layer construction, and timed three background solves on layer 0.25/1e10/canonical (μ = 10²², 10²⁸, 10³⁴).
   - It also computed one m₂ = ∞ root for that layer: 6.149339 × 10²⁴ against DE13's 6.147426 × 10²⁴.
2. **Two code fixes before the frozen main.** Neither followed a number: both stopped the script before it computed anything.
   - A keyword containing a hyphen (a syntax error).
   - The DE12 loader's uniqueness assertion, which failed because DE12's flag line appears twice (see the shared loading detail above). The loader now replaces only the occurrence at a line start.
3. **Wfun guard.** `Wfun` sets W′ and W″ to 0 where W's formula would overflow (arguments within about 10⁻¹⁰⁰ of 0 or 1). This was written before any run. DE12's formula would give NaN at such points.
4. **The residual line (10⁻¹³) was missed by 12 solves.** They are flagged in R4, as the frozen file says, and diagnosed post hoc (post1).
5. **The Sun-sensitivity estimate in the frozen file was about 20 times too large** (see Results). It only widened a band, and slightly.
6. **Brent re-evaluates the bracket ends**, so x = 20 and x = 34 are each solved twice per root. This is harmless and visible in post1's log.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
