# CFG119 — Door 7: a fuzzy-dark-matter soliton plus baryons against the CFG44 target

- **Criteria:** frozen in `../CFG119_FROZEN_CRITERIA.md` (b09ca1480), before any script or number. The shared gates G1–G5 are in `../closure_map/TEN_DOORS_GATES_2026-09-29.md`. The menu of doors was written knowing the target.
- **Script:** `CFG119_fdm_soliton.py`, one file. It imports the CFG44 target (`../CFG44_fluid_target/Bcommon.py`) read-only and the report harness from `../CFG7_common.py`. The main run takes about 80 s wall on 12 worker processes; the MUTATE run about 30 s.
- **Runs:**
  - The main run passes 9 of 14 checks and exits 1. The load-bearing failures are H1 on both footings, which is the answer, and the control C1 as frozen (see Controls).
  - The MUTATE run passes H1 on both footings and 8 of 11 checks. It exits 1 because C1 fails in both modes.
  - The two runs differ on H1, so the control is informative.

## Bottom line

**No. The Schrödinger–Poisson ground state, with the baryons in its potential, does not reproduce the target for any boson mass on the declared grid, even with the soliton mass free per galaxy.**

- **The closest single galaxy misses by 4.0 dex** (alt footing; 4.3 dex canonical). That galaxy is m = 10⁻²³ eV, M_b = 10⁹ M☉, the exponential sphere, with the free M_sol = 0.76 M_b. There C_SP/C_target is 10⁻²·⁶ at r_M and 10⁻⁴·⁰ at 30 r_M. The pass band is ±0.04 dex.
- **With one m at every mass, the best choice is the lightest, 10⁻²³ eV.** Its worst galaxy (M_b = 10¹² M☉, point mass) still misses by 1.2 × 10⁵ dex.
- **Heavier m miss by up to 10¹¹ dex.** Their ground states are bound on the Bohr radius a_B = ħ²/(G M_b m²), which runs from 7 r_M down to 2 × 10⁻¹⁰ r_M across the grid.
- **All 128 cells fail in both the inner core and the outer envelope**, as the frozen shape expectations said. The cells are footing × geometry × M_b × m × rule.
  - Where its core reaches 0.1 r_M (16 of the 128 cells, all with m ≤ 10⁻²² eV and M_b ≤ 10¹⁰ M☉), the ground state is flat there. Its log slope is −0.0005 to −0.07, against the target's −0.55 to −1.
  - Everywhere else its exponential fall-off has already begun inside 0.1 r_M. The slope at 30 r_M is −9 to −3 × 10¹¹, against −2.
  - The worst point is x = 30 in every cell.
- **Rule (i), Schive's core–halo relation, is no better than the free rule in any cell** (it cannot be).
- **G4 fails anyway:** m is a new constant. **G2 fails for every m on the grid** at the 5%-to-30/Mpc line.

**Why a lighter boson would not rescue it.** This is a remark, not a computed row; masses below 10⁻²³ eV were not run.
- A ground state is cored. For the point mass, inside the core C_SP/C_target = (4πG/a₀) ρ r (1 + M_sol(<r)/M_b), which grows at least as ρ(r)·r.
- So a core wider than r_M makes the ratio rise at least fivefold from x = 0.1 to x = 1. That forces J ≥ 0.35 dex, far outside ±0.04.
- A core narrower than r_M leaves the exponential envelope to cover x up to 30. That is what fails by 4 to 10¹¹ dex on the grid.
- A lighter m would also move G2 further from its line.

## Results

J is the largest |log₁₀(C_SP/C_target)| over x in [0.1, 30], on the canonical footing. Each cell gives rule (ii) (free M_sol), with rule (i) (Schive) in brackets. The alt footing, in the `.out`, gives J 6–11% smaller and the same verdict everywhere.

| baryons | m = 10⁻²³ eV | 10⁻²² eV | 10⁻²¹ eV | 10⁻²⁰ eV |
|---|---|---|---|---|
| point, 10⁹ M☉ | 4.89 (9.05) | 370 (459) | 3.7 × 10⁴ (3.8 × 10⁴) | 3.7 × 10⁶ (3.7 × 10⁶) |
| point, 10¹⁰ M☉ | 116 (174) | 1.2 × 10⁴ (1.2 × 10⁴) | 1.2 × 10⁶ (1.2 × 10⁶) | 1.2 × 10⁸ (1.2 × 10⁸) |
| point, 10¹¹ M☉ | 3.7 × 10³ (4.1 × 10³) | 3.7 × 10⁵ (3.8 × 10⁵) | 3.7 × 10⁷ (3.7 × 10⁷) | 3.7 × 10⁹ (3.7 × 10⁹) |
| point, 10¹² M☉ | 1.18 × 10⁵ (1.21 × 10⁵) | 1.2 × 10⁷ (1.2 × 10⁷) | 1.2 × 10⁹ (1.2 × 10⁹) | 1.2 × 10¹¹ (1.2 × 10¹¹) |
| exp, 10⁹ M☉ (h = 2 kpc) | 4.26 (7.22) | 56.1 (101) | 605 (1.05 × 10³) | 6.1 × 10³ (1.1 × 10⁴) |
| exp, 10¹⁰ M☉ (h = 3 kpc) | 43.8 (76.5) | 539 (804) | 5.5 × 10³ (8.1 × 10³) | 5.5 × 10⁴ (8.1 × 10⁴) |
| exp, 10¹¹ M☉ (h = 4 kpc) | 474 (647) | 5.1 × 10³ (6.5 × 10³) | 5.1 × 10⁴ (6.5 × 10⁴) | 5.1 × 10⁵ (6.5 × 10⁵) |
| exp, 10¹² M☉ (h = 5 kpc) | 4.6 × 10³ (5.5 × 10³) | 4.7 × 10⁴ (5.5 × 10⁴) | 4.7 × 10⁵ (5.5 × 10⁵) | 4.7 × 10⁶ (5.5 × 10⁶) |

- **R1 at the closest cell** (exponential sphere, 10⁹ M☉, 10⁻²³ eV, free M_sol = 0.64 M_b, canonical footing):
  - log₁₀ ratio is −3.57 at x = 0.1, −2.58 at x = 1 and −4.26 at x = 30.
  - The soliton is too thin everywhere. Adding mass does not help: M_sol r_c is fixed by m, so more mass shrinks the core and the envelope gets worse.
- **R2:** the best m under rule (ii) is 10⁻²³ eV for every mass, both geometries and both footings.
  - So the four masses agree, but at the light edge of the grid, and that m still misses by 4 to 1.2 × 10⁵ dex.
- **Rule-(ii) optima:**
  - All 64 lie inside the searched range, 10⁻¹⁶ to 10⁴ M_b. They run from M_sol = 0.76 M_b down to 6.7 × 10⁻¹² M_b.
  - Each sits where adding mass stops helping, because self-gravity starts to shrink the state.
- **Rule-(i) masses:** Schive at z = 0, with M_h the target's cold mass inside 30 r_M (about 29 M_b). This gives M_sol = 0.41 m₂₂⁻¹ M_b at M_b = 10⁹ M☉ and 0.0041 m₂₂⁻¹ M_b at 10¹² M☉.
- **Validity of the point-mass cells:** in 6 of the 16 point-mass (m, M_b) pairs the Bohr radius lies inside the Schwarzschild radius of M_b (a_B/r_s = 0.89 to 9 × 10⁻⁵).
  - The Newtonian ground state is only formal there.
  - Those cells fail by 1.2 × 10⁷ dex or more. The exponential spheres have no such cells.

## Controls

- **C2 PASS.** With self-gravity off, the point-mass ground state is hydrogen-like to 1e-6 on the solver grid of all 16 (m, M_b) pairs:
  - eigenvalue to 5.2 × 10⁻⁸;
  - wavefunction to 8.2 × 10⁻⁸ (sup norm over ψ(0));
  - log-space tail to 2.5 × 10⁻⁷ relative, down to ln ψ = −1.35 × 10¹¹ at 30 r_M.
- **C1 FAIL as frozen, kept load-bearing.** The no-baryon ground state is not within 3% of Schive's fitting formula out to 3 r_c. It departs by up to +6.3%, at 2.68 r_c, and the 3% line holds only to 1.76 r_c.

| r/r_c | 0.5 | 1 | 1.5 | 2 | 2.5 | 3 |
|---|---|---|---|---|---|---|
| ρ/ρ₀, SP ground state | 0.8351 | 0.5000 | 0.2295 | 0.0870 | 0.0289 | 0.00881 |
| (1 + 0.091 (r/r_c)²)⁻⁸ | 0.8353 | 0.4982 | 0.2253 | 0.0835 | 0.0273 | 0.00834 |
| SP/fit − 1 | −0.03% | +0.36% | +1.8% | +4.2% | +6.1% | +5.6% |

  - **The error is the fitting formula's, not the solver's.**
    - An independent shooting integration (C1x) agrees with the finite-difference solution to 2.5 × 10⁻⁷ in the eigenvalue and 1.4 × 10⁻⁷ in ρ/ρ₀.
    - The four boson masses agree to 3 × 10⁻¹², as the SP scaling requires.
  - **The ground state's numbers:** E = −0.1627692 G²M²m³/ħ², r_c = 2.67940 ħ²/(G M m²) and M(<r_c) = 0.23635 M_sol.
    - It reproduces Schive's amplitude to +2.0%: 1.938 against 1.9 M☉ pc⁻³ kpc⁴.
    - Schive's two scaling relations together imply M_c r_c = 4.99 × 10⁷ m₂₂⁻² M☉ kpc. The ground state gives 5.41 × 10⁷, 8.6% higher.
  - **An undeclared reading:** measured against the central density, the difference is 0.43% of ρ₀. That reading was not declared and does not re-score C1.
  - C1 fails in both modes, so both runs exit 1.
- **MUTATE.** The target's own ρ_c goes through the same evaluator and the same one-m aggregation.
  - It passes every cell (worst 2.2 × 10⁻⁶ dex), so H1 passes on both footings.
  - So the evaluator can pass; what fails is the SP ground state.
- **Numerics.** These checks were added beyond the frozen file; all pass.
  - **N0:** the imported target satisfies its own identity to 3 × 10⁻¹⁰. Its point-mass M_h = 29.016689 M_b, against √901 − 1 = 29.016662: 9 × 10⁻⁷, inside the 10⁻⁶ line.
  - **N1:** all 2,344 SP states converged within 13 iterations, nodeless, with node-free tails. The worst final |ΔE/E| is 1.0 × 10⁻¹¹; the frozen line is 10⁻⁸.
  - **N2:** Newton–Raphson on the coupled system, with a differential Poisson equation, reproduces the 32 canonical rule-(i) states. E agrees to 1.3 × 10⁻⁸ and J to 2.2 × 10⁻⁸ (relative).
  - **N3:** halving the grid step changes E by at most 8.6 × 10⁻⁸ and J by at most 7 × 10⁻⁸ (relative), on five final states.

## Gates

| gate | verdict | basis |
|---|---|---|
| G1 target | **FAIL** | H1 fails on both footings. The closest galaxy misses by 4.0 dex; the best single m misses by 1.2 × 10⁵ dex. |
| G2 CMB and growth | **FAIL** for every m on the grid (a statement from HBG's fit) | See the notes below the table. |
| G3 reciprocity and energy | PASS (statement) | Ordinary Newtonian gravity: action equals reaction and no extra force acts on the baryons. The ground state is bound. Not computed. |
| G4 constants | **FAIL** | m is a new constant, and no tie to Λ or κ is declared. Rule (ii) adds an M_sol per galaxy; rule (i) imports Schive's simulation calibration. |
| G5 well-posedness | PASS (statement) | A minimally coupled Klein–Gordon field with m² > 0: no ghost, no gradient instability, causal. It has no fifth force, so it is Solar-System (Cassini) safe. |

**G2 in detail:**
- **Half-power scale:** k₁/₂ = 1.6, 4.5, 12.5 and 34.8 /Mpc for m = 10⁻²³ to 10⁻²⁰ eV.
- **Where growth stays within 5%:** only to k = 1.2, 3.5, 9.7 and 26.9 /Mpc.
- **At m = 10⁻²⁰ eV** growth is 10.3% low at 30/Mpc. The 5% line to 30/Mpc needs m ≥ 1.28 × 10⁻²⁰ eV, above the grid.
- **What was evaluated:** the linear equation is δ̈ + 2Hδ̇ + (ħ²k⁴/4m²a⁴ − 4πGρ̄)δ = 0 (comoving k). Only HBG's fitted transfer function is evaluated here.
- **Not computed:** the CMB spectra and lensing.

## Untested hypotheses

Declared in the frozen file:
- the envelope of excited states and granules, the NFW-like outer halo of FDM simulations (only the ground state is tested);
- self-interactions;
- non-spherical and time-dependent solutions;
- baryonic feedback.

Also untested here:
- boson masses off the grid (see the remark in the bottom line);
- relativistic corrections (see the point-mass validity row);
- the CMB spectra.

## Disclosed departures and open choices

1. **Method.** The frozen file names shooting with self-consistent iteration, or imaginary-time relaxation.
   - Here the lowest eigenpair inside the self-consistent iteration is found by finite-difference inverse iteration, not by shooting. It is a symmetric tridiagonal problem in t = ln r, polished by Rayleigh-quotient iteration, and a nodeless eigenvector certifies the ground state.
   - The self-consistent loop uses Anderson mixing and starts from the rescaled no-baryon soliton.
   - Shooting is used as the independent check of the no-baryon soliton (C1x). Newton–Raphson on the coupled system checks the baryon runs (N2).
2. **Grid.** The declared grid runs from 10⁻³ to 10³ r_M, but for most (m, M_b) the ground state's own scale lies far inside 10⁻³ r_M.
   - So the solver grid runs from min(10⁻³ r_M, 10⁻⁶ × the smallest physical scale) to max(10³ r_M, 300 a_B). Its inner edge reaches 2 × 10⁻²⁰ r_M.
   - The declared grid lies inside it. The step is 10⁻³ in ln r.
   - Tails are computed in log space by an exact piecewise-constant-potential sweep, so ratios of 10⁻¹⁰¹¹ are computed, not floored.
3. **Convergence.** E converges to 10⁻¹¹ between iterations; the frozen line is 10⁻⁸.
4. **Rule (i).**
   - Schive's M_c is the mass inside r_c. It is converted to the SP normalisation by M_sol = M_c/f_c, with f_c = 0.23635 from C1.
   - The relation is taken at z = 0 (a = 1). M_h is the target's cold mass only, as frozen.
   - Rule (ii) minimises over every M_sol, so this conversion cannot change H1.
5. **Rule (ii).**
   - The search is over log₁₀(M_sol/M_b) in [−16, 4]: a 0.5-dex scan, then golden section to 10⁻³ dex. The objective is the frozen largest |log ratio|.
   - Every J exceeds the band's larger half-width (0.0458 dex), so no M_sol could pass even under the asymmetric band.
6. **Footings.**
   - H1 is scored separately on each footing, as two load-bearing checks.
   - The canonical a₀ is Bcommon's 9.3603 × 10⁻¹¹ m/s², so the evaluator matches the imported target. FP0's value differs by 2.6 × 10⁻⁶.
   - The alt a₀ is FP0's 1.1312 × 10⁻¹⁰ m/s².
7. **G2** is read on the amplitude: T_F ≥ 0.95 for all k ≤ 30/Mpc, CFG43's convention for "growth within 5%". HBG's k₁/₂ is where the power halves, as HBG define it.
8. **MUTATE** does not run the SP scans, which its headline does not use. C1 and C2 run in both modes.
9. **Added checks** not in the frozen file: N0, C1x, C1a (reported), N1–N3, and the reported point-mass validity row.
10. **C1** is read pointwise, the natural reading of "within 3%". It fails and stays load-bearing.
11. **Parallel run** on 12 processes. The results do not depend on the worker count.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.

## Referee check by the reviewing chat (appended 2026-09-29; the text above is unchanged)

- **Re-run:** both modes were re-run in place.
  - Every `.out` line and every JSON value is identical apart from timing (the `seconds` fields).
  - The main run exits 1 and the MUTATE run exits 1 (C1 in both); H1 flips from FAIL to PASS.
- **C1 fails on a mis-set tolerance, not a solver fault.**
  - `CFG119_referee_sp_shooting.py` is an independent plain shooting solve; it reads no CFG119 code. It reproduces:
    - E M⁻² = −0.162769, r_c M = 2.67941 and f_c = 0.23635;
    - Schive's amplitude, 1.9374;
    - the C1 table to every printed digit.
  - The exact ground state departs from Schive's fit by +4.2% at 2 r_c and +6.1% at 2.5 r_c. The frozen line of 3% out to 3 r_c was tighter than the fit's real accuracy beyond about 1.8 r_c.
  - C1 stays a failed, disclosed control, as frozen. It bears on the check, not on H1, which fails by 4 dex or more.
  - The referee script's MUTATE multiplies the Poisson source by 1.05. It moves E M⁻² to −0.1795, r_c M to 2.5518 and the amplitude to 1.845, and the script exits 1 against 0 for the main run. f_c and the profile shape are universal and do not move.
- **Scope of the large J values.** The 10⁵–10¹¹ dex misses are the formal exponential tails of a hydrogen-like ground state. They measure how far outside the target the ground state lies, not a physical density at 30 r_M.
  - The verdict rests on the closest cell (4.0 dex) and on the analytic remark that no core width can pass.
  - In FDM simulations the soliton sits inside an NFW-like envelope of excited states and granules. That envelope is declared untested here; on average it behaves as cold dark matter, which is door 6's question (CFG118).
