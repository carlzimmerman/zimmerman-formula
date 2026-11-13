# QX3 iter2 frozen criteria: v3s's K(Q) sector as the linear clustering component

Frozen before any graded number. Kappa = 1/2 FITTED; not theory closed. Adopts nothing; TEST lane that reopens a dust-like
cold sector (owner 11-04 rule). Name: cold dark energy, never cold dark matter. No particle. Rules: ../../SWARM_BRIEF.md.

## Mechanism, derived from the action

v3s carries 2K(Q) with K = mu_K^2 (Q - 1)^2. As a k-essence-type sector, p = A (Q - 1)^2 with A = c^4 mu_K^2 / (8 pi G).
To be derived and Lean-certified:
- D1: rho = Q dp/dQ - p = A (Q^2 - 1); exactly p <= rho^2/(4A) for Q >= 1. Dilute limit: p = rho^2/(4A), so this is an n = 1
  polytrope, and c_s^2 = rho/(2A).
- D2: Jeans wavenumber k_J^2 = 4 pi G rho / c_s^2 = 8 pi G A / c^4 = mu_K^2. It is PHYSICAL and fixed, independent of density
  and of time.
- D3: self-gravitating hydrostatic cores have radius R = pi sqrt(K_p/(2 pi G)) with K_p = 2 pi G / mu_K^2, so R = pi/mu_K for every
  mass (n = 1 Lane-Emden; the u'' = -u reduction is Lean-certified).
Linear growth (sub-horizon, Newtonian): delta_d'' + 2 H delta_d' = 4 pi G [rho_d delta_d (1 - (k/(a mu_K))^2) + rho_b delta_b].

## G1: CMB-lensing SHAPE, mu_K -> infinity

- Model: CLASS linear C_L^phiphi. Baryons + this dust + massless neutrinos (N_eff 3.046), T_cmb 2.7255 (FIRAS), flat, constant
  vacuum term (J's Lambda) fills to flat.
- Inputs, all bracketed, with no Planck parameter values: omega_b in {0.0215, 0.0230} (BBN D/H bracket); H0 in {65, 75};
  n_s in {0.95, 0.98}.
- Fitted per corner: omega_d in [0.03, 0.25] and A_s (the amplitude). Data: raw Planck PR4 lensing, 9 bandpowers (L 8-400),
  CMB-marginalised covariance, package binning rule (cfg917_lib, read only).
- Shape PASS if the worst corner's min chi^2 <= 18.48 (chi^2, 7 dof, p = 0.01). FAIL otherwise.
- Code test K1: FFP10's spectrum through the same binning gives chi^2 8.86 (already on the record).
- MUTATE (bites if FAIL): baryons only (omega_d = 0) with A_s refit. It must give chi^2 > 18.48 at every corner. If it does not,
  the shape gate has no power and G1 is NO VERDICT.

## G2: lowest mu_K that keeps the shape

- At G1's best fit per corner, apply the Jeans growth ratio R(k, z) from the ODE above, to C_L via a Limber ratio, and refit A_s.
- mu_min = the smallest mu_K with Delta chi^2 <= 4 relative to mu = infinity, at the worst corner.
- The ODE starts at z = 3400 with CDM-like dust and delta_b = 0 until z = 1090. This is GENEROUS to the mechanism (it ignores
  Jeans suppression before z = 3400), so mu_min is a lower bound.
- Known answer K2: at mu = 1e6 Mpc^-1 the ratio R is 1 to 1e-3.

## G3: galaxies keep the law, i.e. dust stays out

- Reference SPARC-like galaxy: M_b = 1e10 Msun, R_opt = 10 kpc.
- Collapse brings in dust M_d >= f_cap (omega_d/omega_b) M_b, with f_cap = 0.76 (X22 a2b532e3c6), whenever the galaxy's mass is far
  above the dust Jeans mass at turnaround (computed and reported).
- Captured dust sits as an n = 1 core of radius pi/mu_K. This is generous: the baryon potential would compress it further.
  Enclosed fraction (sin xi - xi cos xi)/pi with xi = pi r/R.
- Line: M_d(< R_opt)/M_b <= 0.3. This is the extra mass the law-only RAR leaves room for, about 0.1 dex at baryon-dominated radii,
  above the 0.057 dex intrinsic scatter.
- mu_max = the largest mu_K meeting the line.

## Label

- PASS (lensing and galaxies consistent) only if G1 passes, MUTATE bites, and mu_min <= mu_max (a window exists).
- FAIL if G1 passes but mu_min > mu_max (no window: the sector that makes lensing ruins galaxies). FAIL also if G1 fails.
- Linear growth door: label from the same window. Both footings: a0 does not enter G1/G2 at linear order with the law off on
  the linear web; that is stated as assumption A-web and checked against WG2 (the law on the web overshoots 11-14x even with a
  smooth matter term). If A-web is false, every corner gets worse.
