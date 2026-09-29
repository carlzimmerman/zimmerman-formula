# CFG151 -- Referee: independent re-derivation of CFG120's headline (door 1, a fixed nonlocal kernel). FROZEN CRITERIA

Written 2026-09-29, before any script or number of this lane. It re-derives ONE headline of CFG120 (door 1 of the ten doors, commit 9e4757627) with my own code, the CFG84-86 way: criteria frozen first, CFG120's scripts and outputs opened only after my frozen runs. The menu of doors (closure_map/TEN_DOORS_GATES_2026-09-29.md) was written knowing the target, and so was CFG120. A referee agreement or disagreement says nothing about the data.

Every number below that is not a pass line or a constant is an ESTIMATE, done by hand from the algebra written here. If a script disagrees with an estimate, the script wins and the difference is reported, not repaired. The declarations are frozen as of this file (the orchestrator's commit of it is the record). Anything added after the first run is labelled POST-HOC and cannot change a verdict. A failed control or headline line is kept.

## The headline under test (CFG120's words and numbers)

- README, "Why": "A fixed linear translation-invariant kernel makes C_model proportional to M_b^2 at fixed profile while C_target is proportional to M_b."
- README, G1 point-mass row:
  - "exact scaling R proportional to M_b";
  - "the best universal kernel leaves an ln-centred factor sqrt(1000) = 31.6228 (exact, both footings) on r = 3.87-36.55 kpc, R spanning 0.032 to 31.6";
  - "in the linear band the minimax deviation is 0.998 against 0.10 and the largest single-kernel mass window is 1.222 against 1e3";
  - "M versus 2M: the ratio is 2.000000000000 for every kernel (best centred residual 41%)";
  - "the best 3-parameter Rahvar-Mashhoon fit is worse (max |ln R| = 3.97, factor 53)".
- README, G1 exponential-sphere row: "0 of 18 (universal kernel x profile x footing)".
- Commit 9e4757627: "a fixed linear kernel makes C proportional to M_b^2 against the target's M_b (a sqrt(1000) mass spread)".

## Definitions (CFG120's, restated)

- Target (CFG44): C_target(r) = (a0/4 pi) M_b(<r). For a point mass, rho_c = a0/(4 pi G r sqrt(1+x^2)) and M_c = M (sqrt(1+x^2) - 1), with x = r/r_M and r_M = sqrt(G M/a0).
- Model (CFG120's Reading P): rho_D(x) = integral d^3x' K(|x - x'|) rho_b(x'). The kernel has the same constants at every mass. rho_D enters Poisson's equation and nothing else.
- C_model(r) = rho_D r^3 g_tot, with g_tot = G [M_b(<r) + M_D(<r)]/r^2 from the model's own phantom. R(r; M) = C_model/C_target.
- Overlap: the radii inside the G1 range x in [0.1, 30] for every mass from 1e9 to 1e12 Msun, i.e. r in [0.1 r_M(1e12), 30 r_M(1e9)].
- Full spread at radius r: S(r) = max_M R(r; M) / min_M R(r; M). It is taken at fixed r, for one fixed kernel, over the grid masses whose x-range contains r.
- Mass spread (the commit's word; the README says "ln-centred factor"): F(r) = sqrt(S(r)). It is the smallest max_M |ln R|, as a factor, that any fixed kernel can leave at radius r. CFG120's 31.6228 is F on the overlap.
- Normalisation: each kernel shape k(s) is multiplied by one number N.
  - The best-fit N at a mass minimises max |ln R| over the G1 x-grid at that mass (CFG120's T1c/T1g metric).
  - The best common N does the same over all masses at once.

## The algebra (my derivation; it goes into the script's docstring)

- Point mass: rho_D(r) = N M k(r) and M_D(<r) = N M m(r), with m(r) = 4 pi integral_0^r k s^2 ds. So R(r; M) = (4 pi G M/a0) r N k(r) [1 + N m(r)].
- At fixed r and a fixed kernel, R is proportional to M exactly: C_model goes as M^2 and C_target as M.
- Any profile at fixed shape and size: rho_b -> lambda rho_b gives rho_D -> lambda rho_D and M_D -> lambda M_D. So C_model -> lambda^2 C_model and C_target -> lambda C_target.
- On the overlap every grid mass is in range. So S = 1e12/1e9 = 1000 and F = sqrt(1000) = 31.6228, for every fixed kernel, on both footings.
- The bound is attained.
  - The functional B(r) = r N k(r) [1 + N m(r)] can be any positive function. (1 + m)^2 = 1 + 8 pi integral_0^r r' B dr' gives m, and then a positive kernel. I re-derived this lemma of CFG120.
  - A constant B attains the bound everywhere. CFG120's kernel frozen at M0 = 10^10.5 Msun, at N = 1, gives R = M/M0 at every x (ESTIMATE from the algebra). It is a smooth kernel with no jumps.
- At fixed r the target needs B_req = a0/(4 pi G M) = 1/(4 pi r_M^2). That is exactly 1/M, a factor 1000 across the range.
- The amplitude N is a different object. The phantom's own mass enters g_tot, so C_model is quadratic in N.
  - The best-fit N goes as M^-1 where the phantom is light (N m << 1) and as M^-1/2 where it dominates (N m >> 1).
  - So the ratio of best-fit amplitudes across 1e9-1e12 depends on the kernel shape. It is reported, not pinned.

## Method (declared)

- One script, `CFG151_door1_kernel_referee/cfg151_kernel_referee.py`. Single process, numpy and scipy, one BLAS thread; a few minutes per run expected. Paths come from ZF_REPO, else from `__file__`. It writes only into its own directory.
- Nothing is imported from the repository. I implement CFG44's target myself, from its README and the docstrings of `Bcommon.py`.
- Constants: G Msun = 1.3271244e20 m^3/s^2 (IAU nominal) and 1 kpc = 3.0856775814913673e19 m. a0 = 9.3603e-11 m/s^2 (canonical) and 1.1312e-10 (alt), CFG120's values. The task's rounded 9.36e-11 and 1.13e-10 move r_M by under 0.06%.
- Grids (CFG120's G1 conventions):
  - 13 point masses, log-spaced from 1e9 to 1e12 Msun (0.25 dex, so 10^10.5 is on the grid);
  - x on 200 log points in [0.1, 30];
  - S(r) at 60 log-spaced radii across the overlap, both ends included.
- Kernel shapes (the forms CFG120 states), each times one normalisation N:
  - K0: CFG120's closed-form kernel frozen at one mass, k(s) = 1/[4 pi s r0 sqrt(s^2 + r0^2)], with r0 = r_M(M0) per footing and M0 = 10^10.5 Msun (the grid's ln-centre). At N = 1 and M = M0 it is the target kernel. For the point-mass spread I also use M0 = 1e9 and 1e12.
  - RM: k(s) = (1 + mu0 s) exp(-mu0 s)/(4 pi s^2), with N = A/lambda0 and mu0 = 0.06 and 0.1 per kpc. The formula is from CFG120's criteria (section 2). The four recalled sets (lambda0 = 3 or 10 kpc, mu0 = 0.06 or 0.1, A = 1) are also run as given.
  - PL: the power law k(s) = 1/(4 pi s^2), with N = 1/lambda0.
- Baryons:
  - Point mass: rho_D = N M k(r) exactly. m(r) comes from quadrature and is checked against closed forms (C1d).
  - CFG44's exponential sphere: rho_b = M exp(-r/h)/(8 pi h^3), and M_b(<r) = M [1 - e^-y (1 + y + y^2/2)] with y = r/h.
  - Primary h assignment (the task's): h = 2, 3, 4, 5 kpc for M = 1e9, 1e10, 1e11, 1e12. Secondary: h = 2 kpc at every mass, because CFG120's README labels its CFG44-sphere row "h = 2 kpc".
- My convolution, derived from s ds = -r r' dmu:
  - rho_D(r) = (2 pi/r) integral_0^inf r' rho_b(r') [Q(r + r') - Q(|r - r'|)] dr', with Q(s) = integral s k(s) ds in closed form.
  - Q is asinh(s/r0)/(4 pi r0) for K0, -[E1(mu0 s) + exp(-mu0 s)]/(4 pi) for RM, and ln(s)/(4 pi) for PL.
  - Adaptive quadrature is split at r' = r (the log singularity of RM and PL), with relative tolerance 1e-10. The baryon integral stops at r' = 100 h.
  - CFG120's criteria print the same textbook formula. I derive and code it myself.
- M_D(<r) = 4 pi integral rho_D r^2 dr, by cumulative Simpson in ln r on a 1,200-point log grid from 1e-4 h to 3,000 kpc, plus the inner piece (4 pi/3) rho_D(r_min) r_min^3. Values at other radii come from cubic splines in (ln r, ln rho_D) and (ln r, ln M_D).
- My target for extended baryons (used by control C2; R itself uses the closed-form C_target):
  - dM_c/dr = (a0/G) r M_b(<r)/[M_b(<r) + M_c(<r)]. I derived it from rho_c r^3 g_tot = (a0/4 pi) M_b(<r). It matches Bcommon's docstring ('encl': w' = a0 r u_N/u).
  - It starts at r = 1e-6 h with the leading order M_c = sqrt(a0 M r^5/(15 G h^3)), integrated with DOP853 at rtol 1e-12.
- Fitting N. At every x, R = aN + bN^2 with a, b >= 0, so ln R rises with N.
  - The minimax N is the unique root of max ln R + min ln R = 0, found by bisection in ln N to 1e-12.
  - The G1 band test is exact: N_lo lifts min R to 0.9 and N_hi caps max R at 1.1. G1 is passable only if N_lo <= N_hi.

## Checks

Controls (each must pass; a failed control is kept and makes the main run exit 1):
- C1a (closed form): a Gaussian kernel on a Gaussian sphere. rho_D and M_D(<r) match the closed form (a Gaussian of variance sigma_b^2 + sigma_k^2 and mass N M) to 1e-6 relative, over r in [0.01, 5] sigma_tot.
- C1b (closed form, log-singular Q): PL on a Gaussian sphere. rho_D matches N M sqrt(2) D(r/(sqrt(2) sigma))/(4 pi sigma r) to 1e-6 relative, over r in [0.01, 30] sigma. D is Dawson's function; I derived this in Fourier space (K-hat = pi N/(2k)).
- C1c (point limit): K0 on a compact sphere (h = 1e-5 r0) reproduces the point mass, rho_D = M k(r) and M_D = M (sqrt(1 + r^2/r0^2) - 1), to 1e-6 relative at r in [0.1, 30] r0. ESTIMATE of the finite-size error: about 2 (h/r)^2, below 2e-8.
- C1d: the point-mass kernel mass m(r) by quadrature matches the closed forms to 1e-10: sqrt(1 + r^2/r0^2) - 1 (K0), [2 - exp(-mu0 r)(2 + mu0 r)]/mu0 (RM), and r (PL).
- C2a (target, point mass): my ODE gives M_c = M (sqrt(1+x^2) - 1) and rho_c = a0/(4 pi G r sqrt(1+x^2)) to 1e-8 relative at x in [0.1, 30].
- C2b (the target's own identity, spheres): take rho_c from a 5-point finite difference of my M_c(r). Then C = rho_c r^3 g_tot equals (a0/4 pi) M_b(<r) to 1e-7 relative at x in [0.1, 30], for each sphere and both footings. Starting the ODE at 1e-7 h instead of 1e-6 h changes M_c by less than 1e-8.
- C2c (units and profile): the sphere's closed-form M_b(<r) equals 4 pi integral rho_b r^2 dr to 1e-10. r_M(1e9 Msun) = 1.2203 kpc +- 1e-4 (canonical).
- C3 (positive control): K0 at N = 1 on a point mass of mass M0 gives R = 1 to 1e-8 at every x, and the fitter returns N = 1 +- 1e-6 there.

Headline H1 [the MUTATE must change it]. Each part is checked on both footings. H1 passes only if all four parts pass.
- H1a (scaling): at fixed r and fixed profile, d ln C_model / d ln M_b = 2.00 +- 0.02 and d ln C_target / d ln M_b = 1.00 +- 0.02. Both are measured between M = 1e9 and 1e12, for every kernel shape.
  - Point mass: at 20 radii of the overlap.
  - Sphere: at fixed h = 3 kpc, at 20 radii in [0.3, 300] kpc, from two separate convolution runs with M inside the quadrature (not factored out).
- H1b (the spread, point mass): for every kernel shape, at its best common N, S(r) = 1000 within 2% at every overlap radius, and F = sqrt(S) is within 2% of CFG120's 31.6228.
  - The overlap ends agree with CFG120's 3.87 and 36.55 kpc within 1% (canonical; ESTIMATE 3.859 and 36.61).
  - The alt ends are reported (ESTIMATE 3.510 and 33.30). CFG120 did not print them.
- H1c (no single normalisation, point mass): over all 13 masses and the x-grid, the best common N leaves max |ln R| >= ln sqrt(1000) - 0.02 = 3.434, for every shape.
  - The floor is 3.4539. The 0.02 allows for the fact that the x-grids of different masses do not share radii.
  - K0 at M0 = 10^10.5 attains the floor: residual within 2% of 3.4539, at N = 1.00 +- 0.02, with R = M/M0 at every x to 1e-8, spanning 0.0316 to 31.6 (CFG120: "0.032 to 31.6").
- H1d (no single normalisation, spheres): for every shape, both footings and both h assignments, no common N puts R inside [0.9, 1.1] at every x in [0.1, 30] and every mass (N_lo > N_hi). The minimax max |ln R| is also reported. This checks CFG120's "0 of 18" statement, not its numbers: its kernel K* is not rebuilt here.

## Reported rows (declared; no pass line)

- R1, the best-fit normalisation at each mass: N* for each shape at each of the 13 point masses and the 4 spheres per h assignment, the residual there, and the ratio N*(1e9)/N*(1e12).
  - ESTIMATES, point mass: K0 gives N* of about 10.6 at 1e9, exactly 1 at 10^10.5 and about 0.102 at 1e12. That is a ratio of about 104, with residuals of about 1.09 and 1.05 at the ends.
  - PL gives a ratio of exactly sqrt(1000) = 31.62, because its fit is scale-free in x. Its residual is 1.54 (factor 4.67) at every mass.
  - Also printed: B_req = a0/(4 pi G M) at each mass (ratio exactly 1000). Spheres: no estimate.
- R2, the sphere spread: S_exp(r) over the overlap at each shape's best common N. It is not exactly 1000, because h changes with mass. ESTIMATE: between 100 and 1e4.
- R3, corollaries of R proportional to M, against CFG120's printed numbers:
  - the single-kernel mass window 1.1/0.9 = 1.2222 (CFG120: 1.222);
  - R(2M)/R(M) = 2 and the centred residual sqrt(2) - 1 = 41% (CFG120: 2.000000000000 and 41%);
  - my reading of "the minimax deviation in the linear band 0.998": the best common rescaling under max |R - 1| leaves (S - 1)/(S + 1) = 999/1001 = 0.998. This reading is mine and is flagged.
- R4, the other fixed kernels:
  - PL's best common N on the point-mass grid. ESTIMATE max |ln R| = 3.974 (factor 53.2). CFG120's best 3-parameter RM fit prints 3.97 (factor 53). That would follow if its fit ran to mu0 -> 0 on the point-mass grid. Its README does not say which domain it fitted, so this is a comparison, not a pass line.
  - RM at mu0 = 0.06 and 0.1 with a best common N, and the four recalled sets as given: max |ln R| per mass. ESTIMATE: far above 3.97 (tens), because the kernel's range 1/mu0 = 10-17 kpc is far below 30 r_M(1e12) = 1158 kpc.

## MUTATE (each must change the headline, so each run exits 1)

- MUTATE=a (the task's example): the normalisation scales as 1/M_b, N(M) = N0 M0/M. N0 is the main run's point-mass best fit at M0 = 10^10.5 (N0 = 1 for K0), used for spheres too. H1a and H1b must fail.
  - I do not expect the spread to vanish. The 1/M_b cancels the M_b^2 only where the phantom's mass is negligible in g_tot.
  - ESTIMATE for K0 on a point mass: R(r; M) = [1 + (M0/M) m0(r)]/[1 + m0(r)]. S falls from 1000 to about 5.6 at r = 3.86 kpc and about 124 at 36.6 kpc. The exponent of C_model falls to about 0.30-0.75.
- MUTATE=b (the kernel keyed to each mass, in length and amplitude): K0 with r0 = r_M(M) and N = 1; RM and PL with A = 1 and lambda0 = r_M(M) (N = 1/r_M(M)), mu0 unchanged. H1a, H1b and H1c must fail.
  - ESTIMATE, point mass: K0 gives R = 1 to 1e-8, so S = 1 and the exponent of C_model is 1.00. PL gives R = 1 + r_M/r, so S is about 2-8 on the overlap.
  - The K0 part repeats CFG120's own MUTATE=a (disclosed).
- H1d need not flip in either mode: on spheres even the mass-keyed kernel is not exact.
- Each MUTATE run prints, for every declared line, whether it flipped. So an exit 1 caused by something else (a control) can be told apart.
- Outputs are named by mode: `cfg151_kernel_referee.out` and `cfg151_kernel_referee_results.json`, and the same with `_MUTATE_a` and `_MUTATE_b`.

## Readings (declared)

- H1 PASS: CFG120's headline reproduces with independent code: the M_b^2 scaling, the factor-1000 spread at fixed radius, the 31.6228 mass spread and the overlap. What the referee adds is only what R1-R4 show.
- H1 FAIL in any part: the disagreement is reported with its number and handed back. Nothing is tuned.

## What I read, and what I did not

- Read: `CFG120_FROZEN_CRITERIA.md`; `CFG120_door1_nonlocal_kernel/README.md`; `closure_map/TEN_DOORS_GATES_2026-09-29.md`; `CFG44_fluid_target/README.md`; the docstrings and signatures of CFG44's `Bcommon.py`, printed with Python's ast module so that no function body was seen; `CFG118_FROZEN_CRITERIA.md` (for house style).
- Also seen: file names in `campaign_fresh_gravity/` and git log subject lines, used to check that CFG151 was free. They include CFG120's commit subject and the subjects of other referee lanes' criteria commits, which I did not open.
- Not read before my frozen runs: any CFG120 script, .out, .json, cache or run log; the bodies of `Bcommon.py`; CFG44's B1-B4 scripts and outputs; any literature.

## Where independence stops

- I read CFG120's formulas and numbers first: the convolution formula, the scaling theorem, K_M, B(r) and its realisability, the overlap, the centring, and the printed 31.6228, 3.87-36.55, 1.222 and 3.97. My re-derivation is not blind to the answer.
- The headline's core (R proportional to M at fixed r, for a linear map) is algebra. Any correct linear code reproduces it. Agreement therefore checks CFG120's arithmetic, grids, definitions and footings, not the physics of the phantom reading.
- The kernel forms and the recalled RM values are CFG120's, and were from memory there. I did not check them against the literature.
- h = 2, 3, 4, 5 kpc is the task's statement. I did not read CFG44's B1 script, which fixes B1's h. CFG120's README labels its row "h = 2 kpc", so I run both.
- The target is my own code, but its definition is CFG44's. Nothing here derives the target.
- The fit metric (max |ln R|), the grids and the two a0 values are CFG120's, adopted so that the numbers are comparable.

## Untested (declared)

- CFG120's other results: G2-G5, T1e (the kernel keyed to the total mass), T1f (far-shell leakage), the sympy proof, and its K* on extended profiles ([0.002, 35] etc.).
- The h = 0.1 r_M and h = 0.5 r_M families, and the full 3-parameter RM fit.
- Time-nonlocal and memory kernels; kernels that are not translation-invariant or not linear in rho_b; the relativistic completion; non-spherical baryons.
- Whether Reading P is the Newtonian limit of Mashhoon-type nonlocal gravity.

kappa = 1/2 and Omega_c h^2 stay fitted. Nothing here says the data favour either model, or that the theory is closed.
