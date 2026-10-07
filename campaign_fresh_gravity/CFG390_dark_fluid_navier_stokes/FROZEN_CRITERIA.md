# CFG390 FROZEN CRITERIA: a two-fluid "Navier-Stokes" system for the cold fluid. Is it consistent, and does it settle into the law?

Committed alone, before any script. kappa = 1/2 is FITTED. Both a0 footings (9.3603e-11 and 1.1312e-10 m/s^2) are scored separately
and never pooled. No new particle species: the cold fluid is the record's ~eV Bose field (CFG383/384), and its AMOUNT is an input
(5.364 per original baryon), not derived. Never "theory closed". Owner asked for "a Navier-Stokes equation for the dark fluid".
Local compute only, light CPU (single process, nice), no downloads.

## 1. The system (as proposed), with every refinement declared

Non-relativistic, Landau-type two-fluid. Condensate (s) and normal (n) components of the cold fluid; baryons (b) static.

- Mass: d_t rho_s + div(rho_s v_s) = -C ; d_t rho_n + div(rho_n v_n) = +C.
- Condensate (inviscid): d_t v_s + (v_s.grad) v_s = -grad mu_s, mu_s = Phi + h(rho_s) + Q + kappa_s ln(rho_s/rho_ph);
  h = g rho_s/m^2 (self-interaction, = c_s^2 of CFG384), Q = -(hbar^2/2m^2) lap(sqrt rho_s)/sqrt rho_s.
- Normal: rho_n (d_t + v_n.grad) v_n = -grad p_n - rho_n grad Phi + div[eta (grad v + grad v^T - (2/3) I div v)] + exchange;
  p_n = rho_n sigma_n^2, eta = m vbar/(3 sigma_x) (dilute-gas form).
- Gravity: lap Phi = 4 pi G (rho_b + rho_s + rho_n). The phantom is NOT a source.
- Target: rho_ph = -div[(nu(y) - 1) g_b]/(4 pi G) with g_b the baryon field vector (spherical: M_ph(<r) = r^2 (nu - 1) g_b/G),
  y = |g_b|/a0, nu(y) = 1/(1 - exp(-sqrt y)) (analytic kernel, as the owner's spec; CFG375 C1: it differs from the record's
  monotonised nu_mono by <= 2.4% near y ~ 10; disclosed, not changed).

Declared refinements (R1-R6), fixed now:
- **R1 (sign of C).** The proposal writes C = (rho_n - rho_n_eq)/tau_rel. With d_t rho_n = +C that ANTI-relaxes. A1b checks this
  symbolically. The frozen system uses the corrected sign.
- **R2 (thermodynamic form of C).** Primary: Onsager form C = L (mu_s - mu_n), L = rho_n/(sigma_n^2 tau_rel) >= 0, so that near
  equilibrium it equals (rho_n_eq - rho_n)/tau_rel. The task's relaxation-time form (sign-corrected, with CFG383's Bose rho_n_eq) is
  tested in A4b for H-theorem compatibility and reported.
- **R3 (normal free energy).** f_n = sigma_n^2 [rho_n ln(rho_n/rho_crit) - rho_n], so mu_n = Phi + sigma_n^2 ln(rho_n/rho_crit), with
  rho_crit = zeta(3/2) m / (g_dof lambda_T^3), lambda_T = h/(m sigma_n sqrt(2 pi)), k T = m sigma_n^2 (CFG383, g_dof = 1). This is the
  classical (Boltzmann) normal gas whose saturation density is the Bose critical density. In equilibrium rho_n is capped at rho_crit
  (Bose saturation, declared).
- **R4 (condensate free energy).** f_s = g rho_s^2/(2 m^2) + (hbar^2/8m^2) |grad rho_s|^2/rho_s
  + kappa_s [rho_s ln(rho_s/rho_ph) - rho_s + rho_ph] (generalised relative entropy, >= 0, zero only at rho_s = rho_ph).
- **R5 (exchange momentum).** Converted mass carries momentum at v_* = theta v_s + (1 - theta) v_n; primary donor rule (theta = 1 if
  C > 0, 0 if C < 0); theta is kept symbolic in A2/A4.
- **R6 (sink).** The settling term's target part, +kappa_s grad ln rho_ph, is an external force on the condensate. Its momentum goes
  to the khronon/vacuum sink with one direct coupling (CFG373 + CFG381). This is declared now; A2 tests whether it is needed.
- Temperatures sigma_n are uniform per host (isothermal bath; viscous and conversion heat is removed to the bath). Baryons static.

## 2. Parameters (no fits in this lane)
- m: primary 0.8066 eV (CFG383 m_half, g_dof = 1); bracket 0.62 and 0.71 eV reported.
- lambda (self-coupling) at the Bullet limit sigma/m = 1 cm^2/g, sigma = lambda^2/(128 pi m^2) (CFG384). Used for h and tau_rel.
- tau_rel = 1/(D sigma_x vbar n), D = max(1, Bose degeneracy) (CFG384).
- **kappa_s (primary): settling rate = CFG382's.** In the overdamped (critically damped) reading, the relaxation rate of the settling
  term on scale r is sqrt(kappa_s)/r; equating to Gamma_382 = lambda_382 sqrt(4 pi G rho_tot) on an isothermal profile gives
  sqrt(kappa_s) = lambda_382 V with lambda_382 = 0.027995 (CFG382 primary) and V = 200 km/s (CFG382's anchor): sqrt(kappa_s) = 5.60 km/s.
  One universal constant for both hosts.
- **Bracket (reported, NOT verdict input):** sqrt(kappa_s) = 300, 1000, 3000 km/s and kappa_s -> infinity (ideal settling).
- Hosts:
  - MW: M_b = 6e10 Msun, Hernquist a = 3 kpc (spherical, declared), sigma_n = 150 km/s.
  - Cluster: M_b = 1e14 Msun, Hernquist a = 250 kpc (declared), sigma_n = 1000 km/s.
- Supply S = 5.364 M_b/f_ret, uniform initially in its Lagrangian sphere R_L: (4 pi/3) R_L^3 Omega_c rho_crit0 = S
  (Omega_c = 0.266, h = 0.674; CFG375). MW: f_ret = 0.18 (primary, the record's reservoir reading CFG365/375); f_ret = 1 reported.
  Cluster: f_ret = 1 (clusters retain, CFG379). The domain is closed at R_L (cold mass conserved); R_dom = R_L/2 reported.
- R500 (cluster): the radius where the law's mass M_law = nu g_b r^2/G has mean density 500 rho_crit0.

## 3. Tasks and checks

**(A) Symbolic (sympy), 1D slab with all terms (the 3D stresses are the standard symmetric divergence forms).**
Total-derivative tests use the Euler operator: an expression is a pure flux iff its variational derivative in every field vanishes.
- A1 mass: the summed mass equation is a pure flux. A1b: the proposed C anti-relaxes (d C/d rho_n > 0 for d_t rho_n = +C); declared R1.
- A2 momentum: exchange terms cancel exactly; quantum pressure, interaction pressure, normal pressure, viscosity and gravity (summed
  with the baryon reaction) are pure fluxes; the settling term kappa_s rho_s grad ln(rho_s/rho_ph) is NOT a flux unless rho_ph is
  uniform. Expected: "sink required" = TRUE (declared R6). Passes as "conserved with declared sink".
- A3 Galilean invariance: every equation keeps its form under x -> x - U t, v -> v - U (target co-moving with the baryons).
- A4 H-theorem: with F = sum(kinetic) + gravitational + f_s + f_n, static rho_ph and rho_b, eta >= 0, the Onsager C and donor exchange:
  d_t(F density) + div J = -(4/3) eta (d_x v_n)^2 - L (mu_s - mu_n)^2 + C (1/2 - theta)(v_s - v_n)^2 <= 0, identically.
  A4b: the sign-corrected relaxation-time C with Bose rho_n_eq: report whether a state exists where F increases.
  A4c: with a time-dependent rho_ph, the extra term -kappa_s rho_s d_t ln rho_ph is reported (energy exchanged with the sink).
- A5 rest state: is rho_s = rho_ph, v = 0 a stationary solution? Expected NO in a gravitating host: the residual is
  -grad(Phi + h + Q); it is stationary only where Phi + h + Q is uniform. The true rest state is
  kappa_s ln(rho_s/rho_ph) + h + Q = mu - Phi. Scored as asked; A5 failing is a PARTIAL item, not INCONSISTENT.

**(B) Spherical test, quasi-static relaxation limit (declared).** The end state of the frozen system is its equilibrium: v = 0,
mu_s = mu_n = mu (uniform), with rho_s solved from kappa_s ln(rho_s/rho_ph) + h(rho_s) = mu - Phi, rho_n = min(rho_crit,
rho_crit exp((mu - Phi)/sigma_n^2)), Phi self-consistent (baryons + rho_s + rho_n), and mu set by the cold mass in R_dom. Q is
evaluated a posteriori (flagged if |Q| > 1e-3 of the other terms). The quasi-static assumption is flagged wherever tau_rel or the
settling time exceeds the age.
- MW score: law recovered iff max |V/V_law - 1| <= 0.05 over 10-100 kpc (V^2 = G M_tot(<r)/r; V_law^2 = nu g_b r), at the primary
  kappa_s, m, f_ret = 0.18, on EACH footing.
- Cluster score: unsettled fraction u500 = M_n(<R500)/M_cold(<R500) >= 0.3 at primary m and kappa_s, each footing.
  Local rho_n/(rho_n + rho_s) at R500 reported.
- Viscosity (role), a Lagrangian spherical isothermal Navier-Stokes control for the normal fluid alone in the cluster's baryon
  potential + self-gravity, closed box 3 Mpc, uniform start, 120 shells:
  eta_ref = dilute-gas eta with the mean free path capped at the local radius (Knudsen cap, declared); runs at eta_ref, 0.1 eta_ref, 0.
  - V1: both eta > 0 runs end within 2% (rms in ln rho) of the hydrostatic isothermal profile at the same mass.
  - V2: F is non-increasing in the eta > 0 runs (any rise <= 1% of the total decrease).
  - V3: the eta = 0 run keeps its kinetic energy: final KE/peak KE >= 10x that of the eta_ref run.
  - The Knudsen number lambda_mfp/r at R500 (cluster) and 10 kpc (MW) is reported. Kn > 1 means the NS form is not valid there.

## 4. Controls (can fail)
- C1: M_ph from the integrated rho_ph returns M_ph(<r) to 1e-3; rho_ph > 0 on the grid.
- C2: the equilibrium solution holds the supply mass to 1e-6; for kappa_s -> infinity, rho_s/rho_ph is uniform to 1e-3; with the
  supply set equal to M_ph(<R_dom) (supply-matched, ideal), the law is reproduced to 1e-3 over 10-100 kpc.
- C3: rho_crit reproduces CFG383's u = 0.5 at m_half for the cluster (rho = 0.85*500 rho_crit/3, sigma = 1000 km/s) to 1e-6.
- C4: the normal fluid alone in a fixed potential gives the Boltzmann profile to 1e-6.

## 5. Verdict (declared)
- **CONSISTENT-AND-REPRODUCES:** A1-A5 pass (A2 with the declared sink), the MW law is recovered within 5% on both footings, and
  u500 >= 0.3 on both footings.
- **INCONSISTENT:** a conservation law (A1, A2 beyond the declared settling sink) or the H-theorem A4 fails.
- **PARTIAL:** anything else (e.g. A1-A4 pass but A5, the MW or the cluster criterion fails).
The bracket kappa_s values are reported and never change the verdict.

## 6. MUTATE (CFG390_MUTATE=1, separate outputs *_MUTATE)
kappa_s = 0 (no settling) everywhere. Declared flips: (i) A2 "sink required" becomes FALSE; (ii) the MW law is NOT recovered at any
kappa_s cell; (iii) the condensate collapses to a Thomas-Fermi core supported only by h (its half-mass radius < 1 kpc in the MW).
The MUTATE run exits rc 1.
