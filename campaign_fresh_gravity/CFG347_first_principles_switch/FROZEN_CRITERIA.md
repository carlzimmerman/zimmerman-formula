# CFG347: a first-principles bound-only switch from the framework's own structure? FROZEN CRITERIA

Written and committed alone, before any CFG347 script exists. Standing: kappa = 1/2 (FITTED, the only declared
constant); kernel nu_mono; causality criterion B; the switch reads BARYONS only (MS1-MS5), never the carrier or
curvature; c_T = 1; beta = 0; ownership = only the outermost bound (turned-around) system carries the phantom
(PAPER35 / FG001). No DM particle (the cold mass is still required). Nothing here can say "theory closed".

## 1. Routes (derive, do not posit)
- **R1 slaved theta_b gate.** L ⊃ B W(theta_b / theta_*), theta_b = nabla_mu u_b^mu (baryon flow expansion), W = 1
  (MOND on) at theta_b <= 0, W = 0 (off) at theta_b >= theta_*. Shapes: (i) saturated = DE12's C-inf step at width 1;
  (ii) unsaturated linear ramp W = max(0, 1 - x). B = a0^2 q(y)/(8 pi G) (DE7/DE12 constitutive coupling).
- **R2 leaf comparison.** The same gate with the khronon leaf normaliser theta_* = <K>_h (= 3H on FRW, CMC leaves,
  CFG329 diff-safe). Zero-constant threshold (x = 0) and width (x = 1). R1 alt normaliser theta_* = a0/c (also
  framework-native; a0 is time-independent under the FLAT law).
- **R3 dynamical theta_b switch (CFG337's lesson).** S_sigma = Int sqrt(-g)[ -(Z/2)(d sigma)^2_{c_sigma} - (Z M^2/2) sigma^2
  + C sigma nabla_mu u_b^mu ], MOND sector multiplied by f(sigma) = 1 - S(sigma) (S = DE12's C-inf step on [0,1]).
  Quasi-static source: sigma = (C/(Z M^2)) theta_b, so the threshold is theta_on = Z M^2 / C. Primary theta_on = a0/c
  (canonical footing), sensitivity theta_on = 3 H0 (reported, not scored).
  - zero-constant version: c_sigma = c (minimal, luminal), M a framework rate (H(z), 3H, a0/c), theta_on = a0/c.
  - costed version: c_sigma, M, Z free constants (n = 3); C fixed by theta_on.
- Route identification is part of the result: which record gate (CFG172D / XR36) each route reduces to.

## 2. Tests (24 record hosts = DE12's transition(), z in {0.25, 1, 2.5, 4}, M_b in {1e10, 1e11, 1e12}, both footings,
loaded read-only; "layer" = DE12's t in (0,1) band, as XR36)
- **(a) FRW + linear perturbations.** PASS iff f = 0 on the background AND in a finite neighbourhood (so the MOND
  term is absent from the quadratic action), and the growth ODE (L341's harness, exec read-only) gives
  D/D_LCDM = 1 at z = 0 within 1e-6.
- **(b) static virialised system.** (b1) theta_b = 0 exactly for steady rotating / pressure-supported flows (sympy) and
  f = 1 there (nu_mono), with no extra static force (for R2: the d<K>/dt force term must vanish).
  (b2) fidelity F_b: at r = 30 kpc on every host, the switch may change the gas compressive mode by at most 10%:
  |omega^2/omega_0^2 - 1| <= 0.1 at k = 1/kpc and 1/(10 kpc), 1e6 K gas (1e5 K reported). For R1: a compressive
  oscillation of amplitude delta = 0.1 at the orbital rate Omega(30 kpc) (theta_b = Omega delta) must keep W >= 0.9
  (no flicker) and |W - 1| <= 0.1.
  (b3) R3 reach and timing: the bound region (radius r_ta, where the mean enclosed density of DE12's NFW host + mean =
  5.55 rho_m-bar(z), the EdS turnaround value; approximation flagged) must hold the switch ON at its centre: Yukawa
  outside-weight (1 + u) e^-u <= 0.1, u = r_ta/ell, ell = c_sigma/M, i.e. ell <= r_ta/3.89; and the relaxation rate
  must be >= H(z): M >= sqrt(3) H(z) on every host.
- **(c) transition.** H1 no ghost (kinetic matrix positive definite at all k); H2 gradient (principal speeds^2 > 0);
  H3 Hadamard (growth bounded uniformly in k). For R1 H1 is m(k) = rho_b + B W''_theta k^2 > 0 for all k (XR36's form).
  For R3 decided on the full (xi, sigma) system with self-gravity -rho Gamma_g^2 and the gyroscopic trigger coupling.
  The f'(sigma)B mixing (CFG337's H4 term) is evaluated only if a route passes (a) and (b); otherwise NOT REACHED.
- **Switch width the theory picks:** ell_theta = sqrt(R B_layer / rho_b,layer) / theta_on (R = |W''|max for R1, the
  slaved pole 1/k_g; R = Z M^2 / B for R3), reported per layer against CFG337's ell_min (C2 lenient 183-378 kpc;
  C1 2.9 Mpc) and the 100 kpc tolerance (500 kpc reported).
- **R3 costed feasibility (not a knob scan):** the constants are pushed to their most lenient admissible values
  (M = max_hosts sqrt(3) H(z); ell = min_hosts r_ta / 3.89; c_sigma = M ell; Z = R B_edge / M^2 with R = 1, the
  weakest condensation, B_edge = max B on the layers, universal; per-host B_edge reported as LENIENT, not scored)
  and F_b is evaluated there with the exact roots of (A - w)(b - w) = G w (A = c_s^2 k^2, b = c_sigma^2 k^2 + M^2,
  G = C^2 k^2 / (rho_b Z)). If the most lenient point fails, the costed class fails.
- **Constant count:** every declared number beyond kappa = 1/2 (shape choices listed separately).

## 3. Decision (per route; the overall verdict is the best route's tier, order FP > COST > PARTIAL > NO-GO)
- **FIRST-PRINCIPLES CANDIDATE:** healthy in (a), (b), (c) with zero new constants.
- **CANDIDATE WITH COST:** healthy everywhere with n >= 1 new constant(s).
- **PARTIAL:** healthy on two of the three.
- **NO-GO:** otherwise; state the obstruction precisely and whether it is a theorem (Lean) or an example.
- Separately: whether the FIRST-PRINCIPLES tier is excluded by a theorem within the theta_b-reader class.

## 4. Controls
- **C1** XR36's recorded failure with its exact gate (DE12 step, Delta_x = 1, <K>_h = 3H, w = 0.25 layers):
  1/k_g range 132-1756 kpc on the 24 layers within 1%; ghost at 1/kpc on 24/24.
- **C2** GR limit (B = 0): every symbol reduces to gas + Jeans, healthy.
- **MUTATE** (CFG347_MUTATE=1, outputs *_MUTATE.*): threshold sign flipped (ON where theta_b >= theta_on). Must give
  f = 1 on FRW and chassis-like fast growth in the harness (sigma_8 / growth ratio >= 3 at z = 0); exits 1.

## 5. Expectations (written now, may be wrong; kept whatever happens)
R1 = XR36 (not CFG172D, which embeds the flow theta in V0's khronon theta-equation). R1-saturated fails (c) (mirror
lemma ghost) and (b2) (flicker); R1-ramp fails (b2); R2 adds a d<K>/dt force unless W'(0) = 0. R3 zero-constant is
healthy in (a) and (c) but fails (b3) (luminal range c/M >= Gpc). R3 costed: F_b likely fails at the most lenient
point. Expected verdict: PARTIAL, with a Lean no-go for the zero-constant tier.

## 6. Lean (Lean 4 + Mathlib, no sorry; `cd fable_independent_2026/lean_2026 && lake env lean <abs path>`)
Mirror lemma (MVT); slaved ghost sign; gyroscopic stability (real positive roots); fidelity bound
(|w - A| <= A/10 => G <= b/9 + A/10); luminal range bound; FRW-off neighbourhood identity; numeric instances.

## 7. Protocol
Scripts only in this folder; no downloads; <= 4 processes; no other lane's files edited (DE12, L341, XR36 read-only).
