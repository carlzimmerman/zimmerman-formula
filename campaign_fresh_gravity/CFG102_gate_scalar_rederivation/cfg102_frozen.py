"""
CFG102 -- FROZEN CRITERIA (written before ANY run of any CFG102 script; hash in FROZEN_HASH.txt).
Independent action-level re-derivation of CFG49's dynamical gate scalar (CV6).  Read before writing: CFG49 README, the docstring
statements of its scripts, DE12/DE13 (scripts, read-only, as CFG49 itself builds on them), the CFG48 README/Gcommon for conventions.
NOT read before my own runs: any body of a CFG49 script (incl. cv6_common.py), any CFG49 .out / _results.json.
kappa = 1/2 is FITTED; nothing here says the theory is closed or that any data favour the framework; this is a SCOPED no-go check.

MODEL AS READ.  A scalar chi (dimensionless, in the units of the gate variable t), spherical static background:
    E[chi] = int r^2 dr { (mu/2) chi'^2 + (m2/2)(chi - t)^2 - B W(chi) },  mu [J/m], m2 [Pa], B = a0^2 q(y^2)/(8 pi G) [Pa]
  t = DE12's baryon-only gate variable (t = (U-1)/(2w) + 1/2, w = 0.25, t_U = 1/(2w) = 2, reading A+), W = DE12's C^inf step (Wd).
  Layers = DE12/DE13's 24 galaxy transitions: z in {0.25,1,2.5,4} x M_b in {1e10,1e11,1e12} x footing in {canonical, alt}, w = 0.25,
  amp = True; gas isothermal 1e6 K, c_s = 117 km/s.  DE12's transition() is exec'd read-only (grid replaced by an argument, as DE13 does).
  Gas: the gate variable is eps = dt = h drho_b, h = t_U 4 pi G nu(y)/(H^2 x_c,eff) (DE13's transverse A = nu); gas energy
  (1/2) a eps^2, a = c_s^2/(rho_b h^2).  Eliminating eps (algebraic, Schur): g_eff = a m2/(a + m2).
  Second variation about the EXACT background chi0 (not chi0 = t):
     E2[dchi] = (1/2) int r^2 { mu dchi'^2 + [ g_eff - B W''(chi0) ] dchi^2 }.
  chi0 solves  -mu (1/r^2)(r^2 chi0')' + m2 (chi0 - t) - B W'(chi0) = 0  on DE12's FULL grid (20000 pts, 1 kpc..2e4 kpc, geometric),
  Dirichlet chi0 = t at both ends (declared scan choice; Neumann is tested only as attack A6), same discrete energy as the Hessian
  (DE13's tri() discretisation: trapezoid r^2 weights, off-diagonal mu rm^2/dr), Newton from the B = 0 linear solution with damping.
  Fine layer grid: DE13's layer_fine (8000 pts log-uniform in r between the t = 0.996 and t = 0.004 radii); chi0 is interpolated in ln r.
  UNSTABLE = a negative eigenvalue (exact LDL^T inertia count) in ANY of DE13's five half-layer Dirichlet windows in t
  [(0,.5),(.125,.625),(.25,.75),(.375,.875),(.5,1.0)] (t of the baryons, t-width 0.5 = DE13's lenient scale).
  mu_min(layer; m2) = bisection (24 steps, log10 mu in [20,34], chi0 re-solved consistently at every trial mu);
  mu_uni(m2) = max over the 24 layers.  Edge tolerance for tracking: chi0 = 1/2 radius vs t = 1/2 radius within 10%.
  Costs: Phi_chi = -4 pi G t_U m2 (chi0 - t)/(H^2 x_c,eff) [= -4 pi G C t_U (B W' + mu lap chi0)], force = -dPhi/dr, in units of
  v_f^2 = sqrt(G M a0) and of g_MOND = nu(0.1) 0.1 a0 (flagship: z = 2.5, M_b = 1e11, canonical, r_F = sqrt(G M/(0.1 a0)));
  Sun: z = 0, M_b = 6e10, canonical, r = 8 kpc.  Both use mu = mu_uni(m2) of the 24 layers.
  Baryon UV speed = sqrt(c_s^2 + m2 h^2 rho_b) (CV6_A's principal symbol), max over the in-layer points (0<t<1) of the 24 layers [in units of c];
  the full-grid max and the flagship value are reported alongside (I do not know which point CFG49 quotes).
  m2 SCAN (declared, in Pa): 10^-16 .. 10^-8 in half-decade steps (17 values) + m2 = inf (control, chi0 = t, g_eff = a).

PASS LINES.  Each printed CFG49 number is `reproduced` if mine agrees to the digits CFG49 gives (rounding); otherwise the difference is stated.
CFG49 targets: mu_uni in [1.5e28, 3.9e28] J/m; m2 >= ~1e-12 Pa (tracking within 10%); flagship Phi_chi = -13.5 v_f^2, force -44 g_MOND;
  Sun 7.7e7 v_f^2; UV speed 2.3 c (73 c at m2 = 1e-9); m2=inf N1 = 31.8 v_f^2 (r_F), 2.13e8 (Sun), eta_U = 3.2e-14 (galaxies);
  H3: T holds for 8 m2 values, F holds 0, S holds 0, all three 0; at m2 = 1e-16: flagship force +0.0895 g_M, Sun +3.86e4 v_f^2, 16/24 edges off > 10%.

HYPOTHESES (declared; pass/fail as stated; H2 and H3 are reported as run whatever they do)
  H1a [load-bearing; MUTATE=a must FAIL] mu = 0: all 24 layers unstable at every scanned m2.
  H1b [load-bearing; MUTATE=a,b must FAIL] at mu = mu_uni(m2) all 24 layers stable (recomputed at 1.000001 mu_uni), every scanned m2.
  H2  [reported] mu_min(layer; m2) >= 0.98 mu_min(layer; m2=inf) on every layer whose chi0 edge is within a factor 2 of the t edge.
  H3  [reported, conjunction] exists a scanned m2 with mu = mu_uni(m2) such that (T) edges 24/24 within 10%, (F) |Phi_chi(r_F)| <= 0.1 v_f^2
      and |force|/g_M <= 0.023, (S) |Phi_chi(Sun)| <= 0.1 v_f^2.

CONTROLS (load-bearing; a failed control is a failure)
  C1 m2 = inf: per-layer mu_min (form-(i)-equivalent) gives eta_U = 8 pi G t_U^2 mu/c^4 = 3.2e-14 (galaxies universal, 2 digits) and
     the N1 potentials of the slaved chi0 = t at mu_uni(inf): 31.8 v_f^2 (r_F), 2.13e8 (Sun) to 3 digits (DE13's committed numbers).
  C2 discrete gradient of E equals finite differences of E, and the Hessian equals finite differences of the gradient (1e-6 rel), Hessian symmetric.
  C3 closed-form limit: constant coefficients, planar-equivalent radial Dirichlet window: lowest eigenvalue = mu (pi/L)^2 + g to 1e-3
     (u = r dchi has the same spectrum; L in r).
  C4 Schur elimination: the inertia of the 2-field Hessian [[K + m2 - BW'', -m2],[-m2, a + m2]] (per node, tridiagonal x diagonal)
     equals the negative-mode count of the Schur-reduced 1-field matrix (Haynsworth), on 3 layers x 3 mu.
  C5 chi0 solver: converged (local relative residual <= 1e-8) on every layer x scanned (m2, mu_uni); m2 large (1e-3) gives chi0 -> t inside the layer to 1e-3.
  C6 mu = 0, m2 = inf reproduces DE12's Gamma = k sqrt(c_gate^2 - c_s^2): here: the pointwise sign test (a - B W'' < 0 where c_gate > c_s) agrees with
     DE12's c_gate2 > c_s^2 on every fine-grid node of every layer (exact boolean match).
  MUTATE=a: mu = 0 everywhere in the mu_uni role; MUTATE=b: mu -> -mu_uni.  H1b must fail in both (rc = 1).

ATTACK (all reported, none tunes anything; defined here before the run)
  A1 per-layer mu_min at m2 in {1e-12, 1e-16, inf}: which layers (z, M_b, footing) set mu_uni (argmax) at each m2.
  A2 chi0 = t (slaved background, same g_eff) vs consistent chi0: mu_uni ratio per m2.
  A3 tracking tolerance: for tol in {10, 20, 30, 50, 100}% the number of layers passing per m2; the layers failing at m2 = 1e-16 (signed edge error).
  A4 the plane: extend m2 down to 1e-30 (EXTENSION, outside the declared scan, flagged) and, at every m2 in 1e-30..1e-8 (decade steps) and
     mu/mu_uni in {1, 2, 5, 10, 100}: is stability preserved (24/24), T, F, S; number of points passing all four.  Also the m2-scaling of F, S.
  A5 window choice: at m2 in {1e-12, 1e-16} the stability of mu_uni(m2) tested with (i) t-windows (declared), (ii) windows in chi0 in [0,1],
     (iii) the FULL domain (gas modulus a on the full grid).
  A6 chi0 boundary condition: Neumann at both ends instead of Dirichlet, flagship/Sun cost at m2 in {1e-12, 1e-16} (mu_uni fixed at the Dirichlet value).
"""
