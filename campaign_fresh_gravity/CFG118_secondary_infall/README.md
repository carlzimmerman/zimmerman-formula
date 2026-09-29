# CFG118 — Door 6: spherical secondary infall of cold matter onto a baryon core (shell crossing)

- **Criteria:** frozen in `../CFG118_FROZEN_CRITERIA.md` (b09ca1480), before any script or number. The shared gates G1–G5 are in `../closure_map/TEN_DOORS_GATES_2026-09-29.md`. The menu of doors was written knowing the target.
- **Files:**
  - `CFG118_secondary_infall.py` does the set-up, runs, analysis and report.
  - `shellcore.c` is the integrator. The script compiles it at run time into a temporary directory, so a C compiler is needed.
  - Outputs: `CFG118_secondary_infall.out` and `_results.json` (main run), the `_MUTATE` pair, and `_sims.json`, which holds the simulations' binned products. The MUTATE run reuses `_sims.json` after a hash check.
- **Runs:**
  - The main run passes 3 of 9 checks and exits 1: the headline H1 fails and control C3 fails.
  - The MUTATE run passes H1 and still exits 1, because C3 is a simulation control that MUTATE does not touch. The headline flips from FAIL to PASS, as the frozen file requires.
  - Runtime: 50 simulations plus 3 test orbits took 11.9 min wall on 8 processes (about 20 CPU-min) on the shared machine at load ~100. An identical first run at lower load took 5.5 min. The MUTATE run takes 20 s.
  - The second full run reproduced all 50 simulations of the first exactly, apart from the timing fields.

## Bottom line

**Secondary infall of CDM onto a baryon core does not produce the target C(r) = ρ_c r³ g_tot = (a₀/4π) M_b(<r). H1 fails: a scoped no-go on G1 for this door.**

- **The shape is wrong in every run.** That covers 4 masses × 2 core geometries × 3 angular-momentum brackets, on both footings. C_infall/C_target falls steadily with radius:
  - 4–360 at x = r/r_M ≈ 0.1 for the exponential spheres (0.2–24 for the point masses, whose innermost bins are noisy);
  - 0.8–5.6 at x ≈ 1;
  - 0.05–0.21 at x ≈ 28.

  The target needs a flat 1. Each curve's longest stretch inside ±10% is 0.1–0.2 dex, and some curves have none.
- **Even the closest case misses.** The closest single case (10⁹ M☉ point mass, q = 0.2) misses by 91%. Even the best bracket is off somewhere by a factor of 33 (canonical) or 39 (alt).
- **Why:** too much cold mass inside r_M and too little outside. These cumulative masses (canonical footing) are stable to resolution:
  - at x ≈ 1 the simulated M_c(<r) is 1.0–4.2 times the target's;
  - at x ≈ 28 it is 0.28–0.66 times.

  The infall's radial scale also grows like the turnaround, ∝ M^(1/3) or slower, not like r_M ∝ M^(1/2) (R2). So one set of constants cannot serve every mass even where the shape comes close.
- **Controls:** C1 and C2 pass; **C3 fails.**
  - At 5,000 vs 20,000 shells the local binned ratios differ by a median 56%.
  - The cumulative cold mass agrees to a median 2% at x ≈ 28.
  - H1 fails at 5,000 shells too (the best bracket's largest deviation is 22 canonical, 18 alt).

  So C3 limits the precision of individual ratio values; it does not rescue G1.

## Results (R1 and H1)

C_infall/C_target on 25 bins of 0.1 dex, x = 0.1 to 31.6. The G1 range is the bins with centres in [0.1, 30]. Each range below is over the 8 mass–geometry cases.

| footing | q = r_peri/r_ta | largest \|ratio − 1\| (case) | ratio at x ≈ 0.11: point / exp | x ≈ 1.12 | x ≈ 28.2 |
|---|---|---|---|---|---|
| canonical (a₀ = 9.3603e-11) | 0.05 | 307 (10¹⁰ exp) | 6.3–23.5 / 133–308 | 0.99–5.08 | 0.052–0.162 |
| canonical | 0.10 | 67.5 (10¹¹ exp) | 2.9–15.9 / 42.6–68.5 | 0.81–4.56 | 0.070–0.168 |
| canonical | 0.20 | 31.6 (10⁹ exp) | 1.05–16.7 / 6.7–32.6 | 0.89–4.28 | 0.070–0.212 |
| alt (a₀ = 1.1312e-10) | 0.05 | 357 (10¹⁰ exp) | 4.7–17.2 / 126–358 | 0.88–5.56 | 0.048–0.152 |
| alt | 0.10 | 59.9 (10¹¹ exp) | 3.3–14.6 / 39.3–60.9 | 0.76–3.99 | 0.059–0.143 |
| alt | 0.20 | 37.9 (10¹¹ exp) | 0.17–14.7 / 4.4–38.9 | 0.77–3.80 | 0.062–0.175 |

- **H1:**
  - 0 of 8 mass–geometry cases pass for any bracket on either footing.
  - The declared x range within 10% (R1) is at most 0.2 dex. It is "none" for 6 curves on the canonical footing and 3 on the alt.
  - The full curves are in the `.out` and in `_results.json` (`numbers.R1`).
- **The set-up:**
  - The z = 0 turnaround mass is 23.6 M_b for point cores at every mass, and 19.7–23.6 M_b for the exponential spheres.
  - r_ta(z = 0) = 236, 508, 1095 and 2358 kpc, which is x_ta = 193, 132, 90 and 61 (∝ M^(−1/6)).
  - The shells extend to 3 r_ta, i.e. 77.8 M_b of cold mass for point cores (68–78 M_b for the spheres), so each shell is about 0.004 M_b.
  - The measured zero-velocity radius at z = 0 equals the single-shell prediction to three decimals.
- **Realised first pericentres** (median r_p1/r_ta): 0.046–0.048 for q = 0.05, 0.092–0.095 for 0.1, and 0.179–0.185 for 0.2, i.e. 90–96% of the bracket. In a static potential the formula lands on the bracket exactly (the test orbit under Controls), so the shortfall comes from the potential deepening while the shell falls in.
- **Discreteness (reported):**
  - Shell-bootstrap σ of the ratio: ≤ 0.01 at x ≈ 28, 0.01–0.03 at x ≈ 10, 0.03–0.15 at x ≈ 3.
  - At x ≈ 0.1 the bins hold 0.1–21 time-averaged shells, and the bootstrap σ is 0.2–4 for point cores and up to ~180 for exponential spheres.
  - So the inner bins are noisy, but the outer deficit is not.

## Controls

- **C1 PASS.** With no core, every shell stays on the Planck18 Hubble flow at z = 0 to 4.3e-7 in position and 2.0e-7 in velocity. This needed the Hubble-time step fraction η_H = 3e-4; a pre-run test at 1e-3 gave 4.9e-6.
- **C2 PASS.**
  - Set-up: Einstein–de Sitter, a single collisionless background (Bertschinger's set-up), a point seed, q = 0.05.
  - The least-squares log-slope over r/r_ta ∈ [0.03, 0.15] (7 bins; range declared before the run) is **−2.238**, against −9/4.
  - The local slopes span −2.10 to −2.96, so the reported local-slope line fails; the outermost bin, at 0.149 r_ta, is steeper.
  - M_ta = 56.4 seed masses at a = 1.
- **C3 FAIL.**
  - The largest |ratio_5k/ratio_20k − 1| over x ∈ [0.3, 30] is 2.82, across 48 curves (both footings); the median curve's largest is 0.56.
  - Over [3, 30] the median is 0.33 and the largest 0.96.
  - Post-hoc breakdown:
    - the cumulative M_c(<r) agrees to a median 12% (largest 25%) over [1, 30], and to a median 2% (largest 10%) at x ≈ 28;
    - the local 0.1-dex bin masses typically move by 20–40% between resolutions. That is consistent with caustic and stream structure that one local dynamical time of averaging does not smooth; this reading was not tested separately. The shell bootstrap resamples one realization and does not capture it.
- **Numerical diagnostic (reported).** A test shell in the static softened 10¹⁰ M☉ point mass, turning around at 0.7 kpc (the innermost main-run shells), was run over the whole ~2,000-orbit run:
  - its pericentres land on the bracket exactly (0.0500, 0.1000, 0.2000);
  - its energy drifts by −0.43% (q = 0.05), −0.14% and −0.06%;
  - at η = 0.03 the q = 0.05 drift was −5.5% in a pre-run test, hence η = 0.01.
- **Integrator counters.** Across all 50 runs there were no step-floor hits, no reflections, no counting fallbacks and no angular-momentum fallbacks. The slow tier's displacement bound stayed at D ≤ 0.0101.

## MUTATE

- MUTATE=1 evaluates G1 on the target's own binned ρ_c and M_c in place of the simulated ones.
- H1 then passes on both footings for all three brackets (deviation 0.00), so the evaluator can pass.
- The run exits 1 only because C3 fails in both runs.
- The physics is validated by C1 and C2.

## R2: the radial scale against M_b

- **Declared scale:** the radius where the 5-bin sliding log-slope of ρ_c first crosses −2, outward from x = 0.1.
  - Exponents: 0.42, 0.39, 0.38 for point cores (q = 0.05, 0.1, 0.2) and 0.25, 0.28, 0.54 for exponential spheres.
  - The crossings sit at x = 0.1–2.7, in the noisy inner bins, so these values are erratic.
- **Post-hoc cumulative scale:** the radius where M_c(<r) = M_b. The target puts it at x = √3 for a point mass, i.e. ∝ M^(1/2).
  - Exponents: 0.32–0.35 for point cores and 0.22–0.24 for exponential spheres. The 5,000-shell runs agree within 0.02.
  - For point cores it moves from x = 1.5–1.9 at 10⁹ M☉ to x = 0.54–0.57 at 10¹² M☉.
- **Turnaround:** the z = 0 radius scales as M^0.333 (point) and M^0.342 (exp), the declared expectation.
- **Reading:** the infall's radial scale follows the turnaround, not r_M. The shape fails at each mass separately, and the mass scaling fails across masses.

## Gates

| gate | status | note |
|---|---|---|
| G1 target | **FAIL** | H1 fails for every mass, both geometries, all three brackets and both footings; even the best bracket is off by a factor of ≥ 30 somewhere |
| G2 CMB and growth | pass by construction (not re-tested) | The cold fluid is CDM. The set-up's smooth-baryon background slows the cold perturbation a little; that is a set-up simplification, not the mechanism. |
| G3 reciprocity and energy | pass as a statement | Ordinary Newtonian gravity. The static core is an untested hypothesis. |
| G4 constants | no new dynamical constant | A pass that depended on the initial-condition choices (z_i = 100, the core present from z_i, q, the smooth-background reading) would have counted them against G4. |
| G5 well-posedness | pass as a statement | Collisionless CDM is well posed; Newtonian gravity is Cassini-safe. |

The door lives or dies on G1. Within the declared set-up, it dies.

## Untested hypotheses

- **Declared in the frozen file:**
  - non-spherical collapse, mergers and tidal torques;
  - baryonic feedback and a growing baryon core;
  - warm or self-interacting dark matter;
  - any angular-momentum distribution other than the three brackets.
- **From the set-up:**
  - The full baryon core is present and static from z = 100. It binds the cosmic-density cold matter within a few kpc at z = 100, and that sets much of the inner excess.
  - The baryons outside the core stay smooth. The cold perturbation then grows as δ_c ∝ a^0.90 in the matter era instead of a, so M_ta is lower than with clustering baryons.
  - The only perturbation is the core: no surrounding large-scale overdensity (a point seed, ε = 1).
  - The start is z_i = 100.
  - Newtonian dynamics.

## Disclosed departures and readings

1. **Smooth baryon background (a declared reading, fixed before any run).**
   - The cold shells carry Ω_c = 0.2655 as frozen. The other cosmic baryons (Ω_b outside the core) are a uniform background on the Hubble flow.
   - Without it C1 cannot hold: Ω_c shells moving with Planck18's H(z) are a 16% under-density at z = 100.
   - Inside x = 28 it is at most 0.18% of M_b + M_c. g_tot counts M_b + M_c only, as defined.
2. **The angular-momentum formula.**
   - At a shell's first turnaround: j² = 2[Φ(r_ta) − Φ(q r_ta)] / ((q r_ta)⁻² − r_ta⁻²).
   - This is the energy/pericentre relation in the potential of the mass enclosed at that moment: the shells inside r_ta at their current radii, the shell's own half mass, the core, the smooth background and Λ.
   - A first version used the point-mass form j² = 2 G M(<r_ta) r_ta q/(1+q). In a timing run it gave realised first pericentres of 0.097 r_ta for q = 0.05, about 2q. It was replaced before any H1 number was computed, to meet the frozen "r_peri/r_ta equals the bracket".
3. **The integrator.**
   - It is C rather than the numpy code the task's implementation note suggested. The point-mass pericentres need steps of ~kyr for 13.8 Gyr, which is too slow in numpy on this loaded machine.
   - It is a kick-drift-kick leapfrog with individual power-of-two steps. Variable steps make any adaptive leapfrog only approximately symplectic; the energy test above measures that.
   - The step has two declared fractions: η = 0.01 of t_loc = min(√(r/g), r/|v|, r²/j) and η_H = 3e-4 of 1/H. Both were fixed on numerical tests (C1 and the static orbit) before any H1 number.
   - "Sorting at every step" is implemented as exact enclosed masses at every kick:
     - every shell is re-sorted at every multiple of the level-17 step (0.105 Myr);
     - the fast tier is re-sorted at every tick;
     - the other shells are counted at their exact current positions.
4. **The dynamical time.** It is Binney & Tremaine's t_dyn = √(3π/(16 G ρ̄(<r))), from M_b + M_c at z = 0, capped at 0.9 of the run. No G1 bin reached the cap; the longest window is 6.0 Gyr.
5. **The G1 estimator.** The same binned C is used for the simulation and the target (0.1-dex bins). H1 is required on both footings; the per-footing verdicts are reported too.
6. **C2.**
   - Pure collisionless EdS, with no smooth background, a 10¹⁰ M☉ point seed, z_i = 100 and 20,000 shells.
   - The self-similar range [0.03, 0.15] r_ta was declared before the run.
   - The load-bearing test is the least-squares slope; the local slopes are reported.
7. **C1** uses the 10¹⁰ M☉ point configuration's shells with the core removed.
8. **Softening.** The point mass is softened at 10⁻³ of the canonical r_M on both footings. The simulation does not otherwise depend on a₀.
9. **MUTATE** reuses the main run's cached simulation products; the simulations are deterministic.
10. **Post-hoc rows.** These were added after the first full run showed C3 failing: the C3 breakdown, H1 at 5,000 shells, the cumulative mass against the target's, and the R2 cross-check. They are reported only, and no frozen verdict depends on them.
11. **The bootstrap** uses `np.einsum`. On this machine numpy's matmul prints spurious Accelerate warnings (as CFG116 noted); the two agree to 2e-12.

Reproduce with `python3 CFG118_secondary_infall.py`, then `MUTATE=1 python3 CFG118_secondary_infall.py`. `CFG118_NPROC` sets the number of processes (default 8).

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Referee check by the reviewing chat (appended 2026-09-29; the text above is unchanged)

- **Re-run from scratch:** all 50 simulations, 8 processes, 11.9 min wall, then MUTATE. Every number is identical.
  - The `.out` files differ only in timing and in the order of the per-run progress lines.
  - `_sims.json` holds the same 50 runs when matched by their `spec`; they are stored in completion order.
  - The results JSONs differ only in `seconds`.
  - The main run passes 3 of 9 checks and exits 1 (H1 and C3). MUTATE passes 6 of 9 and exits 1 (C3). H1 flips.
- **A hand check of C2:** the Einstein–de Sitter turnaround mass at a = 1 is 56.4 seed masses. The linear estimate for a pure Hubble-flow start at z = 100 is M_ta/M_seed = (3/5)(a/a_i)/1.062 = 57.1, with 3/5 the growing-mode share and 1.062 the linear overdensity at turnaround. They agree to 1.2%.
- **The verdict does not rest on the failed C3.** At x ≈ 28 the cumulative cold mass converges between resolutions to a median 2%, and on its own it is 0.28–0.66 of the target's there.
- **H1's reading is stricter than the frozen text** (both footings must pass). It fails on each footing separately, so that choice is moot.
