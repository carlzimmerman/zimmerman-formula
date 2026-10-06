# CFG350: an EMERGENT switch from the coarse-grained phase-space state (velocity dispersion / entropy). FROZEN CRITERIA

Written and committed alone, before any CFG350 script exists. Standing: kappa = 1/2 (FITTED, the only declared
constant); kernel nu_mono; causality criterion B; c_T = 1; beta = 0; no DM particle (the cold mass is still required).
Nothing here can say "theory closed". Baselines (read-only): CFG347 (theta_b readers, PARTIAL: flicker), CFG348 (energy
reader, NO-GO), CFG349 (khronon ratchet, PARTIAL + LEGALITY FAIL: an irreversible smooth-flow source has no legal
action; class E inherits). DE12's transition() (24 hosts) and L341's growth harness are exec'd read-only, as in CFG349.

## 1. Hypothesis and the state variables (fixed now)
The switch is not a fundamental field. It is a function of the coarse-grained second moment of the distribution
function, sigma_ij = P_ij / rho (P = pressure tensor), which obeys the standard 10-moment (Gaussian-closure) system
(Levermore 1996; Brown, Roe & Groth 1995): D rho/Dt = -rho theta; rho Du/Dt = -div P + rho g;
D sigma/Dt = -(L sigma + sigma L^T), L_ij = d_j u_i, heat flux Q = 0. Its exact solution in smooth flow is the
congruence sigma(t) = G sigma_0 G^T with dG/dt = -L G, det G = rho/rho_0, so det sigma / rho^2 is conserved and
s = ln(sqrt(det sigma)/rho) is the reversible adiabat. Irreversible change happens only at caustics (new streams) and
shocks (entropy jump), i.e. in weak solutions, as in hydrodynamics.
For a multi-component point: sigma^2 = sum_s rho_s [tr sigma_s + |u_s - u_bar|^2] / (3 sum_s rho_s) (1D-equivalent).

**MS check (decides which routes are scored).** MS1-MS5: the switch reads baryons (+ the MOND-sector phantom), never the
carrier, the total matter or curvature. A reader of the cold component's dispersion sigma_c is the matter/carrier door
(MS1 leak) and B's S_cold is pressureless dust with no defined sigma. So sigma_c routes are REPORTED, NOT SCORED.

**Scored routes (MS-allowed, baryons only):**
- **R-b0:** f = H(sigma_b^2), H(0) = 0, H(x>0) = 1 ("multi-stream / non-cold"), sigma_b over gas (thermal + turbulent)
  and stars. 0 constants.
- **R-b1:** f = S(sigma_b^2/sigma_ref^2 - 1), S a C-infinity step from 0 at 0 to 1 at 1 (no shape constant).
  sigma_ref is 1 constant, set to the minimum value that passes (a) (the most lenient admissible point).
- **R-s:** f = H(s_b - s_IGM(z)), the baryon entropy above the mean-IGM adiabat computed from the FRW thermal history.
  0 constants.
**Reported, not scored:** R-c (sigma_c, MS-forbidden); R-q (a "has been shocked/shell-crossed" label: a history tag,
not a state function, if cooling erases the state); R-* (stellar sigma only: needs a coarse-graining scale L).

**FRW thermal history (fixed):** T_gas = 2.725 (1+z) K for z >= 150, adiabatic (1+z)^2 below, reionisation at
z_re = 7.7 (Planck 2018), then T0 = 1e4 K (scored; Lya-forest T0 >= 1e4 K at z ~ 2-4, quoted literature, not re-read
here); lenient T0 = 5e3 K at z = 0 reported. mu = 0.59 (ionised), 1.22 (neutral). sigma_th = sqrt(k T/(mu m_p)).
**Reference MOND-ON systems (quoted literature, not re-read):** local gas discs, outer HI sigma = 10 km/s (scored);
classical dSphs Carina 6.6, Leo II 6.6, Sextans 7.9, Draco 9.1, Sculptor 9.2, Fornax 11.7 km/s (reported).

## 2. Tests (24 DE12 hosts: z in {0.25,1,2.5,4}, M_b in {1e10,1e11,1e12}, both footings; r = 30 kpc; gas at 1e6 K)
- **(a) FRW + linear.** A1: f = 0 exactly (or below threshold with a finite margin) on the mean IGM at every
  z <= 1100 after recombination, and in linear parcels (delta <= 0.1). A2: single-stream until shell crossing
  (Zel'dovich sheet delta_lin = 1, sphere 1.686); the closure keeps sigma = 0 exactly before crossing (numerical
  1D Zel'dovich multi-stream sigma). A3: L341 growth with the FRW value of f: D/D_LCDM = 1 within 1e-6.
  (a) PASS = A1 and A2 and A3.
- **(b) bound.** B1a: f >= 0.9 at 30 kpc on all 24 hosts. B1b: f >= 0.9 in a local gas disc (sigma_HI = 10 km/s).
  B2 fidelity (CFG347/349 test): 10% compression at Omega(30 kpc); sigma^2 -> sigma^2 (1.1)^(2/3) in the closure;
  dev = delta f (4 pi G rho_ph + |g_ph| k)/|A| <= 0.10 at k = 1/kpc, 1/(10 kpc) on all 24 hosts. B3 no flicker: f
  non-decreasing to 1e-12 under 10 compression cycles on all hosts (the closure ODE integrated).
  The adiabatic response of sigma under the compression is reported. (b) PASS = B1a and B1b and B2 and B3.
- **(c) transition.** C1: the 10-moment system is strongly hyperbolic for sigma positive definite (numerical flux
  Jacobian: real speeds u, u +- sqrt(sigma_xx) (x2), u +- sqrt(3 sigma_xx), 10 independent eigenvectors, 1000 random
  states); the sigma -> 0 dust limit is reported (dust's own Jordan block). C2: the switch's consistent stress
  (Pi = -2 rho sigma d(f L_M/rho)/d sigma, |L_M| ~ g_ph^2/(8 pi G)) keeps the effective pressure positive:
  chi = 2 |L_M| max S' /(rho sigma_ref^2) < 1 at 30 kpc and at the edge (R-b0: exactly 0 since x delta(x) = 0).
  C3 edge: f = 0 on the mean IGM and in voids, f = 0 in unbound shell-crossed sheets/filaments (WHIM, T 1e5-1e7 K),
  and the ON edge of each host at >= 0.3 r_ta (the first caustic / accretion shock of self-similar infall, quoted
  0.364 / 0.347 r_ta, Bertschinger 1985). (c) PASS = C1 and C2 and C3.
- **Conservation (d).** D1: the moment system in conservative form conserves momentum and energy (sympy:
  d_t(rho u) + d_x(rho u^2 + P) = 0, d_t E + d_x(u E + P u) = 0 with E = rho u^2/2 + P/2, 1D, g = 0). D2: with f a
  state function, f L_M is a function of the parcel configuration in smooth flow (sigma = sigma(rho) on the adiabat),
  so the parcel action is ordinary: energy conserved and free of any multiplier (sympy; contrast CFG349's L-ord).
  D3: H-theorem-like monotonicity: s conserved in smooth flow (det sigma ∝ rho^2), non-decreasing at caustics/shocks
  (numerical: s across a Zel'dovich crossing and a Rankine-Hugoniot gamma = 5/3 shock); radiative cooling lowers s
  (reported: non-monotone for collisional baryons). (d) PASS = D1 and D2 (D3 reported).
- **Ownership (reported):** does a local sigma reader read a subsystem's OWN dispersion (GC core, wide binary) or its
  host's? FG001 class E is NEWTONIAN, class A ON. If both read ON, or if E and A cannot be separated, it is said.
- **Constants:** every number not G, c, a0 (kappa), H, rho_b, Omega_c h^2, k_B, m_p.

## 3. Decision (frozen; computed per scored route, verdict = best scored route)
- **EMERGENT SWITCH WORKS:** (a), (b), (c), (d) all pass with 0 new constants.
- **WITH COST:** all four pass with n >= 1 constants.
- **PARTIAL:** three of the four pass.
- **NO-GO:** fewer; the obstruction is stated as a theorem or an example.
R-c/R-q/R-* results are reported beside the verdict and cannot raise it. No verdict says "theory closed" or that data
favour the framework.

## 4. Controls
- K1: the single-stream closure on FRW: sigma_0 = 0 stays exactly 0; sigma_0 > 0 gives sigma ∝ a^-2 within 1e-8.
- K2: the singular isothermal sphere (rho = sigma^2/(2 pi G r^2)): the Jeans integral returns sigma = v_c/sqrt2 within 1e-6.
- MUTATE (CFG350_MUTATE=1, separate outputs `*_MUTATE.*`): replace sigma by the instantaneous theta_b reader
  (CFG347's R1, f = H(-theta_b)). It must flicker: B3 FAILS and the run exits 1.

## 5. Lean (Lean 4 + Mathlib, no sorry)
sigma = 0 invariance and positivity under the congruence; det(G S G^T) = det(G)^2 det S; the adiabat
det sigma/rho^2 conserved; no flicker for the zero threshold under any compression; the empty-window obstruction for
R-b1 (if it occurs); conservative-form total momentum conservation (periodic telescoping sum); the IGM sigma bound.
