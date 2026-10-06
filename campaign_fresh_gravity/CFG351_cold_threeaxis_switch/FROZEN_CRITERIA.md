# CFG351: a switch that reads the cold component's three-axis shell crossing (full-rank sigma_c). FROZEN CRITERIA

Written and committed alone, before any CFG351 script exists. Standing: kappa = 1/2 (FITTED, the only declared
constant); kernel nu_mono; causality criterion B; c_T = 1; beta = 0; no DM particle (the cold MASS is still required;
this lane describes the cold component's phase-space state, not a particle species). Nothing here can say "theory
closed". Baselines (read-only): CFG347 (theta_b readers, flicker), CFG349 (memory ratchet, no legal action), CFG350
(coarse-grained sigma: baryon routes NO-GO; the cold route R-c passed (a), (b), conservation, failed the edge: ON in
unbound sheets). DE12's transition()/host() (24 hosts) and L341's growth harness are exec'd read-only, as in CFG350.

## 0. Owner decision (recorded verbatim) and the MS1 column
Owner decision, 2026-10-06, given in the orchestrator chat: "yeah let the switch read the cold component".
This relaxes MS1 (the switch reads baryons only) FOR THIS EXPLORATION ONLY. Every result table carries a separate
column "under original MS1": there, any sigma_c reader is the MS1 matter/carrier door and is NOT ADMISSIBLE (as in
CFG350), whatever its test results.

## 1. The B extension this lane needs (stated, counted as a cost)
B's cold component is pressureless dust (CFG4 T5, CFG345), which has no sigma. This lane extends B's specification:
the cold component is a cold collisionless phase-space sheet (a 3D Lagrangian manifold x(q,t), v(q,t) in 6D, Vlasov
dynamics), exactly cold at the start (sigma_c = 0 on FRW). Its local second moment is the fine-grained stream sum
sigma_c,ij(x) = sum_s w_s (v_s - vbar)_i (v_s - vbar)_j, w_s = rho_s / sum rho_s over the streams s at x (no smoothing
scale). Between caustics it obeys the 10-moment closure with heat flux 0 (CFG350): D sigma/Dt = -(L sigma + sigma L^T),
solution sigma = G sigma0 G^T. New streams (rank changes) arise only at caustics, i.e. in the kinetic step.

## 2. Routes (fixed now)
- **R-3 (scored):** f = H(det sigma_c), H(0) = 0, H(x > 0) = 1. 0 constants (threshold det = 0).
- **R-3s (scored):** f = 27 det sigma_c / (tr sigma_c)^3 for sigma_c != 0, f(0) = 0 (range [0,1], 1 iff isotropic).
  0 constants.
- The verdict uses the better of R-3 and R-3s (stated now).
- **MUTATE (CFG351_MUTATE=1, separate outputs):** f = H(tr sigma_c) (any crossing). It must be ON in sheets,
  reproducing CFG350's R-c failure; the MUTATE run exits 1 when the sheet test fails.

Action: L = L_cold(phase-space sheet; Vlasov-Poisson) + L_gas + f(sigma_c) L_M, f a state function of the cold
state, so the action is ordinary (no multiplier, no history field), as in CFG350 D2.

## 3. Tests
**(a) FRW + linear.** A1: the closure keeps sigma_c = 0 exactly on FRW (K1 integration), so f = 0 exactly for both
routes. A2: single stream before first crossing: 1D Zel'dovich stream-sum sigma = 0 exactly at D A = 0.9. A3: L341
growth with f = 0: D/D_LCDM = 1 within 1e-6 on both footings. (a) PASS = A1 and A2 and A3.
Reported A4 (fragility): f for sigma_0 = eps I, eps -> 0+ (a primordial isotropic dispersion).

**(a') unbound sheets and filaments.** A'1: separable 3-axis Zel'dovich map x_i = q_i + D A_i sin q_i
(A_1 > A_2 > A_3), stream-sum sigma on a grid: numerical rank (eigenvalues > 1e-10 of the max) equals the number of
crossed axes; f_R3 = 0 and f_R3s <= 1e-12 at every point while D A_3 < 1 (sheet: 1 axis crossed, filament: 2);
det > 0 in the triple-crossed zone once D A_3 > 1. A'2: third-axis crossing implies turnaround along all three axes
(ZA in EdS: axis i turns around at lambda_i D = 1/2, crosses at 1); the lag versus turnaround is reported (ZA, the
spherical top-hat 1.062 vs 1.686, and the self-similar run below). (a') PASS = A'1 and A'2.
Reported A'3: hierarchical substructure inside sheets (collapsed sub-clumps are full rank locally).

**(b) bound.** B1: at r = 30 kpc on all 24 hosts sigma_c is full rank: Jeans-isotropic NFW sigma_r > 0 AND 30 kpc lies
inside the host's rank-3 region (r < r_rank3 from the self-similar run, section 4). B2 fidelity (CFG347/350 test):
a 10% gas compression at Omega(30 kpc); sigma_c responds only through gravity (10-moment closure for sigma_c under the
induced cold-flow divergence); df from the route; dev = df (4 pi G rho_ph + |g_ph| k)/|A| <= 0.10 (CFG350 fid_dev).
The fractional sigma_c^2 response is quantified. B3 no flicker: f non-decreasing to 1e-12 over 10 cycles, all hosts.
(b) PASS = B1 and B2 and B3.

**(c) transition.** C1: the 10-moment closure is strongly hyperbolic on full-rank states (1000 random states, CFG350
Jacobian) AND the rank never changes in a smooth closure step (1000 random invertible G on rank-1/2/3 states);
Jacobian eigenvector counts on rank-1/2 states reported. C2: switch stress Pi = -2 L_M sigma df/dsigma: R-3 identically
0 (sigma adj(sigma) = det I, x delta(x) = 0); R-3s chi = 2 |L_M| ||f (I - 3 sigma/tr sigma)|| / (rho_c tr sigma / 3) < 1 at
30 kpc and at the edge (|L_M| ~ g_ph^2/(8 pi G), as CFG350). Reported: R-3's front impulse ratio |L_M|/(rho_c sigma_c^2)
at the edge. C3 edge: f = 0 on FRW, in voids and in unbound sheets/filaments (A'1), and the ON edge of every host at
>= 0.3 r_ta (CFG350's C3 line, kept for comparability; r_ta = CFG347/350's 5.55 rho_m-bar radius). Reported: the edge's
offset from B's turnaround edge in kpc vs the record's 100 kpc tolerance, its width, and CFG337's ell_min.
(c) PASS = C1 and C2 and C3.

**(d) conservation.** D1: sympy, the conservative 10-moment form (1D, g = 0) has zero momentum and energy residuals.
D2: f is a state function (ordinary action); for R-3 the switch adds no force or momentum to the cold component:
Pi = 0 and adj(sigma)(v_s - vbar) = 0 for every stream on rank-deficient states (1000 random rank-2 three-stream
points, max norm <= 1e-10). (d) PASS = D1 and D2.

## 4. The rank-3 edge model (fixed now)
A full-rank sigma needs >= 4 streams (N streams give rank <= N - 1). In spherical self-similar secondary infall
(EdS, point seed, delta M/M ∝ M^-1, radial orbits; Bertschinger 1985 collisionless case) stream counts are odd, so the
rank-3 region is the >= 5-stream zone: inside the SECOND caustic, assuming generic (non-coplanar) small non-radial
velocities. A numpy shell run (N shells, softened, radial) gives the caustic radii in units of the current r_ta.
Control K3: its first caustic must reproduce 0.364 r_ta (Bertschinger 1985, quoted) within 10%.

## 5. Reported, not scored (cannot raise the verdict)
Ownership: class E (globulars, wide binaries) inside a full-rank host; class A dwarfs (own full-rank clump); whether
the record's ownership rule (CFG333 R2) keeps class E Newtonian. UFD link: CFG344's CDM-like cold structure vs the
switch (UFD clumps full rank). Constant count; the extension cost (section 1).

## 6. Decision (frozen)
- **SWITCH WORKS:** (a), (a'), (b), (c) and (d) all pass, 0 constants.
- **WITH COST:** all five pass, n >= 1 constants.
- **PARTIAL:** four of the five pass.
- **NO-GO:** three or fewer; the obstruction is stated.
Under original MS1: NOT ADMISSIBLE regardless (column kept).

## 7. Controls
K1: single-stream FRW closure keeps sigma_c = 0 exactly. K2: Zel'dovich sheet rank 1, idealised filament rank 2,
isothermal sphere rank 3 (Jeans sigma = v_c/sqrt 2, isotropic, det > 0). K3: shell-run first caustic 0.364 r_ta +- 10%.
MUTATE as above.

## 8. Lean (Lean 4 + Mathlib, no sorry)
Single-stream invariance (sigma = 0 stays 0 under congruence); det = 0 for rank < 3 (sum of two outer products in 3D);
det > 0 for isotropic eps I; congruence keeps det sign (rank invariance via det (G S G^T) = det G^2 det S); FRW-off
identity (H 0 = 0); sigma adj(sigma) = det I (stress zero); conservation (periodic telescoping); positivity (isotropic
f = 1, f in [0,1] as stated where proved).
