# CFG151 — Referee: an independent re-derivation of CFG120's door-1 headline (a fixed nonlocal kernel gives C ∝ M_b², the target needs C ∝ M_b)

- **Criteria:** frozen in `../CFG151_FROZEN_CRITERIA.md` (785fdd82a; sha256 0c1aa5a86fea…, printed first by every run), before any code. The target lane is CFG120 (door 1, 9e4757627). The menu of doors was written knowing the target, and so was CFG120.
- **Script:** `cfg151_kernel_referee.py` (sha256 c65513465a4a…), one file, numpy and scipy, one process. Nothing is imported from the repository; CFG44's target is my own code. It was not edited after the first run. Runs take 29-34 s.
- **Post-hoc script:** `cfg151_posthoc.py`, written after the frozen runs and after opening CFG120's code. It holds four comparison diagnostics, P1-P4. None is a pass line and none changes a verdict.
- **Runs** (in place, in this directory):
  - **Main:** 16 of 16 checks pass; **exit 0**. All four headline parts pass on both footings.
  - **MUTATE=a** (normalisation proportional to 1/M_b): 10 of 16; **exit 1**. H1a and H1b flip, as declared. H1c flips too (not required); H1d does not (not required).
  - **MUTATE=b** (the kernel keyed to each mass): 10 of 16; **exit 1**. H1a, H1b and H1c flip, as declared; H1d does not (not required).
  - All eight controls pass in all three modes, so neither exit 1 is confounded.

## Bottom line

**CFG120's headline reproduces with independent code.** A fixed linear translation-invariant kernel gives C_model ∝ M_b² at fixed profile, while the target has C ∝ M_b. So at a fixed radius R = C_model/C_target is proportional to M_b. Across 10⁹-10¹² M☉ it spans exactly a factor 1000 wherever all masses are in range, whatever the kernel. The best a single kernel can do is centre that factor in ln, which leaves the mass spread √1000 = 31.622777. CFG120 prints 31.6228.

- **Measured:** the exponent of C_model is 2.000000 and of C_target 1.000000. This holds for six point-mass kernel shapes at 20 radii, and for exponential spheres at h = 3 kpc from separate convolution runs, on both footings.
- **The spread:** S(r) = 1000.000000 and F = 31.622777 at all 60 overlap radii, for every shape, on both footings.
- **Every other point-mass number of CFG120's G1 row reproduces:** 0.0316-31.6, the 1.222 window, the M-versus-2M ratio 2.000000000000 with its 41%, the 0.998 "linear band", and the 3.9735 (factor 53.17) fit.
- **On spheres, no single normalisation reaches the [0.9, 1.1] band:** 0 of 8 cases (4 shapes × 2 h assignments) on each footing.
- **One refinement:** the floor is attained exactly by a smooth kernel. CFG120's own K_M, frozen at 10^10.5 M☉, gives R = M_b/10^10.5 at every x (to 7 × 10⁻¹⁶), so max |ln R| = 3.4539 on the whole G1 grid. CFG120's grid-built K* reached 3.739. The certificate is unchanged.
- **The amplitude is not the spread.**
  - The best-fit amplitude ratio N*(10⁹)/N*(10¹²) depends on the kernel shape: 103.7 for K_M frozen at 10^10.5, and exactly √1000 = 31.623 for the power law.
  - For the finite-range RM kernels it is inverted (7.6 × 10⁻⁷ and 1.1 × 10⁻¹¹), because their range of 10-17 kpc cannot reach 30 r_M(10¹²) = 1158 kpc.
  - The phantom's own mass enters g_tot, so C_model is quadratic in the amplitude.
- **The task's MUTATE (normalisation ∝ 1/M_b) changes the headline but does not remove the spread.** On the overlap, S falls to 5.67-124.5 for K_M frozen at 10^10.5 and to 13.0-104 for the power law. For the RM shapes S stays at 1000, with R ∝ 1/M_b, because the fitted multiplier puts them in the phantom-dominated regime. The mass-keyed kernel (MUTATE=b) removes the spread exactly for K_M: S = 1, and the exponent of C_model is 1.000000.

## Comparison with CFG120 (opened only after the three frozen runs)

| quantity | CFG120 (README; its script-A/B `.out`) | CFG151 (this lane) | agreement |
|---|---|---|---|
| scaling at fixed r | "exact scaling R proportional to M_b" (sympy; numeric 1.5 × 10⁻¹³ at h = 2 kpc) | exponent of C_model 2.000000, of C_target 1.000000 (point masses; spheres at h = 3 kpc, separate runs), both footings | yes |
| mass spread F on the overlap | 31.6228, both footings | 31.622777 (S = 1000.000000), every shape, both footings | yes, to all printed digits |
| overlap ends, canonical | 3.87-36.55 (README); 3.867-36.550 (`.out`) | 3.8589-36.6085 (analytic) | −0.21% / +0.16%: CFG120's ends are snapped to its 6000-point radial grid (P1 reproduces 3.867 / 36.550 exactly) |
| overlap ends, alt | 3.514-33.284 (`.out` only) | 3.5102-33.3010 | the same grid snapping (P1 reproduces them) |
| R of the best universal kernel | "0.032 to 31.6" | 0.03162 to 31.6228 (K_M frozen at 10^10.5, N = 1) | yes |
| worst max \|ln R\| of a realised best kernel on the G1 grid | 3.739 (grid-built K*, jumps in B*) | 3.4539 (smooth K_M frozen at 10^10.5) | mine lower; the floor 3.4539 is attained |
| "linear band minimax deviation" | 0.998 (0.99800) | (S − 1)/(S + 1) = 0.998002 | yes; CFG120's code defines it this way |
| single-kernel mass window | 1.222 (grid value 1.2219795) | 1.1/0.9 = 1.2222 (analytic) | yes |
| R(2M)/R(M) at fixed r | 2.000000000000; residual 41% | 2.000000000000; √2 − 1 = 41.4% | yes |
| best RM fit, point masses | 3.9735 (factor 53.173); A = 0.007938, λ0 = 0.07974 kpc, μ0 = 4.6 × 10⁻⁷/kpc | power law, one normalisation: 3.9735 (factor 53.17), N = 0.09955/kpc = CFG120's A/λ0 | yes; CFG120's fit is the power law |
| recalled RM sets, point masses, max \|ln R\| at 10⁹ (canonical; alt) | 3.082, 4.451, 5.271, 6.577; 3.087, 4.310, 5.267, 6.431 | the same eight numbers | yes, to 3 decimals |
| recalled RM (3 kpc, 0.1/kpc) on h = 2 kpc spheres, smallest R | 2.2 × 10⁻⁴⁸ canonical, 6.36 × 10⁻⁴⁴ alt | e^−109.734 = 2.2 × 10⁻⁴⁸, e^−99.464 = 6.4 × 10⁻⁴⁴ (at 10¹²) | yes |
| power law at CFG120's fitted N on h = 2 kpc spheres (P2) | max R 0.0446 / 44.6 at 10⁹ / 10¹², min 0.00272 (alt 0.0419 / 41.9 / 0.00229) | 0.0446 / 44.60 / 0.00272 (alt 0.0419 / 41.88 / 0.00229) | yes, to 3-4 digits (post hoc) |
| spheres, G1 | 0 of 18 (K*, RM fit, recalled RM × 3 profiles × 2 footings) | 0 of 16 (K_M@10^10.5, RM 0.06, RM 0.10, power law × 2 h assignments × 2 footings) | yes (different kernel sets) |

## Results (main run)

**Point masses** (canonical). N* is the best-fit normalisation at one mass; "common" is one normalisation for all 13 masses. The alt footing gives:
- the same K_M numbers;
- power-law N* larger by √(a0,alt/a0,can) = 1.099, with the same ratio and residuals;
- RM residuals about 9% smaller.

| shape | N*(10⁹) | N*(10^10.5) | N*(10¹²) | N*(10⁹)/N*(10¹²) | residual at 10⁹ / 10¹² | common N | common max \|ln R\| |
|---|---|---|---|---|---|---|---|
| K_M frozen at 10^10.5 | 10.62 | 1 | 0.1024 | 103.7 | 1.089 / 1.053 | 1.000000 | **3.4539** (the floor) |
| K_M frozen at 10⁹ | 1 | 0.1024 | 0.01441 | 69.4 | 0 / 1.502 | 0.1278 | 3.910 |
| K_M frozen at 10¹² | 153 | 10.62 | 1 | 153 | 1.877 / 0 | 10.10 | 4.595 |
| RM, μ0 = 0.06/kpc | 0.579 | 2.33 | 7.6 × 10⁵ | 7.6 × 10⁻⁷ | 2.02 / 34.4 | 7.6 × 10⁵ | 34.36 |
| RM, μ0 = 0.10/kpc | 0.917 | 20.5 | 8.2 × 10¹⁰ | 1.1 × 10⁻¹¹ | 2.52 / 57.5 | 8.2 × 10¹⁰ | 57.49 |
| power law | 0.366 | 0.0651 | 0.01157 | 31.623 | 1.540 / 1.540 | 0.0996 | 3.9735 |

- N is dimensionless for K_M and in kpc⁻¹ (= A/λ0) for RM and the power law.
- The target's required value of B(r) = r N k (1 + N m) at fixed r is a0/(4πG M_b): 5.344 × 10⁻², 1.690 × 10⁻³ and 5.344 × 10⁻⁵ kpc⁻² at 10⁹, 10^10.5 and 10¹² M☉ (canonical). The ratio is exactly 1000.
- The four recalled RM sets as given are inside the band at 0 of 13 masses. Their residuals run from 3.1 at 10⁹ to 64-112 at 10¹².

**Exponential spheres** (canonical). "h(M)" is h = 2, 3, 4, 5 kpc for 10⁹-10¹² M☉, the task's assignment; "h = 2" is h = 2 kpc at every mass, which is CFG120's P1.

| shape | h | N*(10⁹) … N*(10¹²) | N*(10⁹)/N*(10¹²) | common max \|ln R\| | G1 passable | spread S on the overlap |
|---|---|---|---|---|---|---|
| K_M@10^10.5 | h(M) | 25.2, 4.91, 0.902, 0.129 | 194.5 | 5.739 | no | 615-1005 |
| K_M@10^10.5 | h = 2 | 25.2, 4.52, 0.672, 0.113 | 222.7 | 5.739 | no | 1000 |
| RM 0.06 | h(M) | 1.80, 1.16, 16.7, 7.7 × 10⁵ | 2.3 × 10⁻⁶ | 34.16 | no | 448-1228 |
| RM 0.10 | h(M) | 1.86, 3.86, 651, 8.0 × 10¹⁰ | 2.3 × 10⁻¹¹ | 56.98 | no | 410-1688 |
| power law | h(M) | 1.75, 0.406, 0.0732, 0.0164 | 106.9 | 4.794 | no | 393-1101 |
| power law | h = 2 | 1.75, 0.324, 0.0550, 0.0125 | 140.4 | 4.928 | no | 1000 |

- With h fixed at 2 kpc the spread at fixed radius is exactly 1000, as the scaling requires.
- With h(M) it ranges from 380 to 1690 (all shapes, both footings), inside the frozen estimate of 100 to 10⁴.
- Even with its own normalisation, every sphere misses the band. Per-mass residuals are 0.6-2.8 for K_M@10^10.5 and 0.64-1.7 for the power law, against ln 1.1 = 0.095.

## Controls (all pass, identical in all three modes)

- **C1a:** a Gaussian kernel on a Gaussian sphere matches the closed form (a Gaussian of summed variance). Errors: ρ_D 5.6 × 10⁻⁹, M_D 3.2 × 10⁻⁸ (line 10⁻⁶).
- **C1b:** the power law on a Gaussian sphere matches my Fourier-space closed form, N M √2 D(r/√2σ)/(4πσr) with D Dawson's function, to 3.8 × 10⁻¹³. This tests the log-singular Q.
- **C1c:** K_M on a compact sphere (h = 10⁻⁵ r0) reproduces the point mass. Errors: ρ_D 6.0 × 10⁻¹⁰, M_D 1.6 × 10⁻⁷ (line 10⁻⁶). The frozen estimate missed; see below.
- **C1d:** the point-mass kernel masses m(r) by quadrature match the closed forms to 6.7 × 10⁻¹⁶.
- **C2a:** my target ODE reproduces the point-mass M_c and ρ_c to 5.5 × 10⁻¹² (13 masses, both footings).
- **C2b:** the target's own identity holds on all 7 (M, h) spheres and both footings. With ρ_c from a finite difference of my M_c(r), ρ_c r³ g_tot = (a0/4π) M_b(<r) to 1.9 × 10⁻⁹. Moving the ODE start from 10⁻⁶ h to 10⁻⁷ h changes M_c by 5.9 × 10⁻¹¹.
- **C2c:** the sphere's closed-form M_b(<r) matches quadrature to 1.3 × 10⁻¹⁴, and r_M(10⁹ M☉) = 1.220283 kpc.
- **C3** (positive control): K_M at its own mass gives R = 1 to 6.7 × 10⁻¹⁶, and the fitter returns N = 1 to 4.4 × 10⁻¹³.
- **Diagnostics** (added in stage 2 before the first run; no pass line): spline against direct ρ_D agree to 1.2 × 10⁻⁸ on every unit grid. There were 0 quadrature warnings.

## MUTATE

- **MUTATE=a** (the task's example): N(M) = N0 × 10^10.5/M_b, with N0 the main run's point-mass best fit at 10^10.5.
  - **Bites on H1a and H1b.**
  - The exponent of C_model falls to 0.30-0.75 for K_M@10^10.5 (frozen estimate 0.30-0.75).
  - Its spread falls to 5.67 at r = 3.86 kpc and 124.5 at 36.6 kpc (estimate about 5.6 and 124).
  - For the power law the spread falls to 13.0-104.
  - **For both RM shapes S stays at 1000 and the exponent is 0.000000.** The fitted multiplier (1.8 × 10⁶ and 2.2 × 10¹⁰) puts the phantom's mass far above the baryons'. There C_model ∝ N² M_b², so N ∝ 1/M_b makes C_model mass-independent and R ∝ 1/M_b. The spread returns inverted.
  - So a 1/M_b normalisation cancels the M_b² only where the phantom is light, as the spec expected.
- **MUTATE=b** (length and amplitude keyed to each mass): **bites on H1a, H1b and H1c.**
  - K_M keyed gives R = 1, S = 1 and an exponent of 1.000000, as CFG120's own MUTATE=a does.
  - The keyed RM shapes give S = 1 (phantom-dominated at their fitted multiplier).
  - The keyed power law gives S = 3.13-13.69 (see the missed estimates).
- **H1d flips in neither mode.** That was declared as not required: on spheres even the mass-keyed kernel is not exact.

## Estimates: matched and missed (reported plainly; nothing was repaired)

- **Matched** (frozen hand estimates):
  - overlap ends 3.859 / 36.61 (alt 3.510 / 33.30);
  - K_M@10^10.5 per-mass N* 10.6, 1, 0.102, with ratio about 104 and residuals 1.09 / 1.05;
  - power-law ratio exactly 31.62, with residual 1.54 at every mass;
  - power-law common residual 3.974 (factor 53.2);
  - RM common residuals "tens" (34.4 and 57.5);
  - the floor 3.4539 at N = 1;
  - sphere spread between 100 and 10⁴;
  - both MUTATE=a estimates.
- **Missed 1, C1c finite size.** The estimate was "about 2(h/r)², below 2 × 10⁻⁸"; M_D deviated by 1.6 × 10⁻⁷. Post hoc (P3):
  - At 1,200 grid points the deviation is mostly grid error.
  - At 4,800 points it falls to −4.02 × 10⁻⁸, −5.06 × 10⁻⁹ and −5.25 × 10⁻¹⁰ at r = 0.1, 0.3 and 1 r0. That matches the finite-size term of M_D: 2h²(4πr²K′)/m = −4.03 × 10⁻⁸, −4.71 × 10⁻⁹ and −5.12 × 10⁻¹⁰, which is about 4(h/r)² at r ≪ r0.
  - My coefficient 2 was a factor 2 too small for M_D, and the estimate left out the grid error.
  - C1c passes its 10⁻⁶ line either way.
- **Missed 2, the MUTATE=b power-law spread.** The estimate was "about 2-8"; the run gives 3.13-13.69.
  - The estimate used the keyed amplitude N = 1/r_M, but the frozen H1b evaluates at the best common multiplier, which is c = 0.4466.
  - Post hoc (P4): the closed form S = (r_M,hi/r + c)/(r_M,lo/r + c) gives 1.99-8.36 at c = 1 and 3.13-13.69 at c = 0.4466. The estimate was stated at the wrong point.
- **The spec's reasoning about the amplitude does not cover finite-range kernels.**
  - The spec said the best-fit N goes as M^−1 where the phantom is light and as M^−1/2 where it dominates.
  - That holds for K_M and the power law. For RM the per-mass best fit rises by 6 to 11 orders of magnitude from 10⁹ to 10¹² M☉, because the kernel's range cuts off long before 30 r_M.
  - No estimate or pass line depended on this.

## The four questions, resolved from CFG120's code after the runs (comparison observations, not re-scores)

1. **h = 2 kpc.** CFG120 did not run h = 2, 3, 4, 5 kpc.
   - Its script B, header line 8, runs "(P1) exponential sphere with h = 2.0 kpc for every mass (CFG44 B1's Bcommon default, COMPACT expsphere)" on the 13-mass grid, plus h = 0.1 r_M and h = 0.5 r_M. So its README row "h = 2 kpc" means h = 2 kpc at every mass: my secondary assignment.
   - On that profile my numbers reproduce its printed ones (table above).
   - With h(M) = 2-5 kpc, which only this lane ran, the fixed-radius spread falls from 1000 to 380-1690 and G1 still fails.
   - I did not check the attribution to CFG44's B1.
2. **The 3.97 fit's domain: point masses only.** `cfg120_common.rm_residual` evaluates `R_point` over the 13 masses and x in [0.1, 30].
   - Its differential-evolution box has μ0 ≥ 10⁻⁵/kpc, but the Nelder-Mead polish is unbounded and ended at μ0 = 4.6 × 10⁻⁷/kpc.
   - So "the best 3-parameter Rahvar-Mashhoon fit" is the power law. My one-parameter power-law fit gives the same 3.9735 at the same A/λ0.
3. **3.74 against 3.4539.**
   - CFG120's K* is built from a per-radius ln-centred B*(r) on a 6000-point grid. B* jumps where a grid mass enters or leaves its x-range, and its own note says the grid interpolates across each jump (3.739).
   - A smooth kernel attains the floor exactly: K_M frozen at 10^10.5 has a constant B = 1/(4π r0²), so R = M_b/10^10.5 at every x and max |ln R| = 3.4539 on the whole grid.
   - CFG120's certificate, 31.6228, is exact. Its constructive check was suboptimal, not wrong.
4. **"0.998".** Script A, lines 133-135, defines the linear-band minimax deviation at each radius as (cmax − cmin)/(cmax + cmin), with `span = fac ** 2` and `lin = (span - 1) / (span + 1)`. That is (S − 1)/(S + 1) = 999/1001 = 0.998002, my reading.
5. **Also, the overlap ends.** CFG120 takes them from `np.geomspace(1e-2, 2e3, 6000)` (`ov = rgrid[both]`). Snapping my analytic ends to that grid gives exactly its 3.867 / 36.550 and 3.514 / 33.284 (P1). The analytic overlap is 3.8589-36.6085 kpc (canonical).

**Notes CFG120's README could take, for the coordinator to relay** (this lane edits no CFG120 file):
- the overlap "3.87-36.55" is grid-snapped (analytic 3.859-36.61);
- "the best 3-parameter RM fit" is the power law on point masses only;
- the sphere row is h = 2 kpc at every mass;
- a smooth kernel attains the floor 3.4539.

## Disclosed departures and choices

1. **Point-mass headline.** ρ_D = N M k(r) is used exactly, and m(r) comes from quadrature (checked by C1d). My convolution code is exercised on a point mass through C1c's compact sphere, not in the headline itself.
2. **The Gaussian controls' grid** runs to 12σ_tot, not 3,000 kpc, where a Gaussian underflows. The spec's grid statement is for the exponential spheres.
3. **H1c's "every shape"** was read to include K_M frozen at 10⁹ and 10¹², which the spec listed only for the spread. That is the stricter reading, and all pass.
4. **H1a's separate sphere runs** were done per footing for every shape. The RM and power-law exponents do not depend on a0.
5. **In the MUTATE modes the fitted "N"** is a common multiplier of the mode's base normalisation: N0 × 10^10.5/M_b (a) or 1/r_M(M) (b).
6. **The recalled RM sets** were also evaluated on spheres (reported only).
7. **Stage-2 additions before the first run:** the spline and quadrature-warning diagnostics. After the runs: `cfg151_posthoc.py` (P1-P4), written knowing CFG120's numbers.
8. **Housekeeping.** A development import left a `__pycache__` in this directory; it and three empty stderr captures were deleted before the README. No output file was edited.

## Where independence stops

- I read CFG120's frozen criteria and README first, including the convolution formula, the scaling theorem, K_M, B(r), the overlap, the centring and its printed numbers. The re-derivation was not blind to the answer.
- The core, R ∝ M_b at fixed r for a linear map, is algebra; any correct linear code reproduces it. The agreement therefore checks CFG120's arithmetic, grids, definitions and footings, not the physics of its phantom reading.
- The kernel forms and the recalled RM values are CFG120's, from memory there. I did not check them against the literature.
- CFG44's target is my own code from its README and `Bcommon.py` docstrings, but the definition is CFG44's. Nothing here derives the target.
- The fit metric, the grids and the two a0 values were adopted from CFG120 so that the numbers are comparable.
- Everything in "Comparison", "The four questions" and `cfg151_posthoc.py` was written after reading CFG120's code and outputs.

## Untested

- CFG120's G2-G5, T1e (the total-mass kernel), T1f (far-shell leakage) and its sympy proof.
- Its K* on extended profiles; the h = 0.1 r_M and h = 0.5 r_M families; the full 3-parameter RM fit (only its power-law limit is reproduced).
- Time-nonlocal and memory kernels; kernels that are not translation-invariant or not linear in ρ_b; the relativistic completion; non-spherical baryons.
- Whether CFG120's Reading P is the Newtonian limit of Mashhoon-type nonlocal gravity.
- The attribution of h = 2 kpc to CFG44's B1.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
