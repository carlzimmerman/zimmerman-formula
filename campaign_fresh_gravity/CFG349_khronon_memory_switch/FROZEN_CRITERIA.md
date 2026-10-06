# CFG349: a causal MEMORY switch on the khronon clock (a ratchet along the baryon flow). FROZEN CRITERIA

Written and committed alone, before any CFG349 script exists. Standing: kappa = 1/2 (FITTED, the only declared
constant); kernel nu_mono; causality criterion B; the switch reads BARYONS only (MS1-MS5); c_T = 1; beta = 0; no DM
particle (the cold mass is still required). Nothing here can say "theory closed". Baselines (read-only): CFG347
(theta_b readers, PARTIAL: flicker), CFG348 (energy reader, NO-GO), CFG242 route A (latch with a decay term: no memory),
CFG48 (nonlocal gate stable but not a legal local term). DE12's transition() and L341's growth harness are exec'd
read-only, as in CFG347.

## 1. The construction (fixed now)
- **Ratchet (primary, R):** an auxiliary scalar m with first-order dynamics along the baryon flow, timed by the khronon:
  u_b^mu d_mu m = (u_b^mu d_mu T) * Gamma_b * H(-theta_b) * (1 - m),  theta_b = nabla_mu u_b^mu,
  H(x) = 1 for x >= 0 and 0 for x < 0 (the parcel "has stopped expanding", theta_b <= 0, including static theta_b = 0),
  Gamma_b = sqrt(4 pi G rho_b) (the parcel's own baryonic dynamical rate: reads baryons only, no new constant).
  No decay term: m never relaxes back. Initial data m = 0 on FRW at any z_i (theta_b = 3H > 0 there).
- **The MOND sector is multiplied by f(m) = m** (linear, no shape constant).
- **Sensitivity rates (reported, NOT scored):** Gamma = H(z); Gamma = a0/c; and the ramp u.dm = (-theta_b)_+ (1 - m)
  (then 1 - m = exp(-cumulative log-compression)).
- **Actions examined (legality):**
  - L-ord (ordinary action, Lagrange multiplier): S_m = Int sqrt(-g) lambda [u_b.dm - (u_b.dT) Gamma_b H(-theta_b)(1-m)]
    added to S_GR + S_b + S_khronon + Int sqrt(-g) f(m) L_MOND.
  - L-CTP (doubled-field / closed-time-path, as CFG242 route A): the physical limit of the doubled action gives the
    ratchet with no lambda back-reaction.
- **Legality checks (reported, each a named liability):** (L1) EOM derivable (sympy on the parcel reduction);
  (L2) diff-safety on the leaves (CFG329's method: every term a scalar built from u_b, T, rho_b, g); (L3) energy:
  L-ord energy function and the back-reaction at theta_b = 0; L-CTP the Bianchi residual nabla_mu T^{mu nu} != 0 where
  m changes. **Frozen consequence:** the tier is computed by the rule in section 3 from (a), (b), (c); the verdict line
  must append "LEGALITY PASS" or "LEGALITY FAIL (<reason>)". A legality failure cannot be hidden and cannot be upgraded.

## 2. Tests (DE12's 24 hosts: z in {0.25,1,2.5,4}, M_b in {1e10,1e11,1e12}, both footings; r = 30 kpc; c_s at 1e6 K)
- **(a) FRW + linear perturbations.**
  - A1 sympy/ODE: if theta_b > 0 along the whole past, m = 0 exactly (a finite OFF neighbourhood |delta theta| < 3H).
  - A2 linear parcels: theta_b/3H = 1 - f(z) delta/3 > 0 for delta_lin <= 0.1 at all z. Turnaround thresholds:
    spherical top-hat delta_lin,ta = (3/20)(6 pi)^(2/3) = 1.062 (sympy: theta = 0 at eta = pi); Zel'dovich sheet
    delta_lin = 3/(3 + f). PASS needs both >= 0.5.
  - A3 L341 growth with the switch value m = 0: D/D_LCDM = 1 within 1e-6.
  - (a) PASS = A1 and A2 and A3.
- **(b) bound systems.**
  - B1 ON: f = m >= 0.9 at r = 30 kpc on all 24 hosts, using the CONSERVATIVE lower bound on the ratchet exponent
    E >= (1/2) Gamma_b,ta (t(z_host) - t(z_ta)), with Gamma_b,ta = sqrt(4 pi G f_b 5.55 rho_m-bar(z_ta)) (the lowest
    density on the path), the 1/2 a duty factor for oscillating flows, and z_ta from rho_enc,tot(30 kpc) =
    44.4 rho_m-bar(z_ta) (spherical-collapse virialisation, 8 x 5.55; an approximation). z_ta <= z_host scores E = 0.
    The lenient bracket (5.55, no duty factor) is reported, not scored.
  - B2 fidelity (CFG347's test): a 10% compression at orbital rate. The ratchet can only raise m, by at most
    delta f <= (1 - m). Gas compressive-mode change dev = delta f (4 pi G rho_ph + |g_ph| k)/|A|,
    A = c_s^2 k^2 - 4 pi G (rho_b/f_b + rho_ph), at k = 1/kpc and 1/(10 kpc). PASS needs dev <= 0.10 on all 24 hosts.
  - B3 no flicker: under 10 cycles of a 10% compression at Omega(30 kpc), m is non-decreasing (maximum drop 0 to
    1e-12) on all hosts; and on CFG242's probe shell (radial orbit from its own turnaround) m never decreases.
  - (b) PASS = B1 and B2 and B3.
- **(c) transition / turnaround shell.**
  - C1 ghost: the baryon kinetic matrix in the physical limit equals rho (sympy: f(m) carries no velocity dependence).
  - C2 characteristics: the principal symbol of (delta rho, delta v_par, delta v_perp x2, delta m) has real speeds
    {0 (m, along u_b), 0, 0, +-c_s}; the H(-theta_b) source is bounded (|.| <= Gamma_b), so it is not principal.
  - C3 strong hyperbolicity: the symbol is diagonalizable (5 independent eigenvectors) for c_s > 0. The dust limit is
    reported, with dust alone as the control.
  - C4 Hadamard: the maximum linear growth rate over k in [1e-3, 1e3]/kpc is bounded by Gamma_Jeans + Gamma_b.
  - Edge sharpness (reported): the duration for m 0.1 -> 0.9 in turnaround free-fall times; the radial edge
    (m = 0.5 and 0.9) relative to r_ta on the top-hat infall trajectory, in kpc for every host.
  - (c) PASS = C1-C4.
- **Ownership (reported, not scored):** class A (accreted top-level, turned around on its own before accretion)
  keeps its own ON state; class E (formed embedded) inherits the host's state. FG001's class E is NEWTONIAN; if the
  construction gives class E an ON state, the record's classes are NOT reproduced, and this is said.
- **Constants:** count every number in the construction that is not G, c, a0 (kappa), H, rho_b or Omega_c h^2.

## 3. Decision (frozen)
- **MEMORY SWITCH WORKS:** (a), (b) and (c) all pass with 0 new constants.
- **WITH COST:** all pass with n >= 1 constants.
- **PARTIAL:** two of three pass.
- **NO-GO:** fewer; the obstruction is stated as a theorem or an example.
Plus the legality suffix (section 1). No verdict says "theory closed" or that data favour the framework.

## 4. Controls
- K1: reproduce CFG242's frozen latch E3 on its probe shell (GM = 1, softening 0.05, H = 0.01): n(t_ff) = 0.791 and
  min n over t >= t_ff = 0.143, within 1%; and the static decay exp(-t/2.05).
- K2: Gamma = 0 gives m = 0 for all time, so f = 0 and the force law is Newtonian (exact).
- MUTATE (CFG349_MUTATE=1, separate outputs `*_MUTATE.*`): reversible memory,
  u.dm = Gamma_b [H(-theta_b)(1 - m) - (1 - H(-theta_b)) m]. It must flicker like CFG347: B3 FAILS and the run exits 1.

## 5. Lean (Lean 4 + Mathlib, no sorry)
Ratchet monotonicity and [0,1] invariance (exact step update); FRW-off invariance (m stays 0 if never triggered);
distinct real characteristic roots (strong hyperbolicity) for c_s > 0; kinetic positivity; the L-ord partner
identity d/dt[lambda (1-m)] = s (1-m) (lambda must diverge as m -> 1 when unsourced); the fidelity bound; the
reversible fixed point = the duty fraction (MUTATE flicker).

## 6. Protocol
No downloads; no home paths or names; at most 4 processes; other lanes' files untouched.
